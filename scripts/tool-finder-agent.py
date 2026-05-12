#!/usr/bin/env python3
"""
Tool-finder agent voor AI-inventarisatie.

Zoekt nieuwe AI-tools via Claude + web search en voegt ze toe aan
tools-longlist.csv zonder duplicaten.

Gebruik:
  python3 scripts/tool-finder-agent.py
  python3 scripts/tool-finder-agent.py --thema "supply chain finance"
  python3 scripts/tool-finder-agent.py --rondes 3
  python3 scripts/tool-finder-agent.py --thema "transcriptie" --rondes 2 --commit

Vereisten:
  pip install anthropic
  export ANTHROPIC_API_KEY=sk-...
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / "data" / "tools-longlist.csv"

CSV_HEADERS = [
    "toolnaam",
    "type",
    "waarvoor",
    "gebruikers",
    "aantal_universiteiten",
    "universiteiten_voorbeeld",
    "in_literatuuronderzoek",
    "literatuuronderzoek_toelichting",
    "direct_bruikbaar_voor_team",
    "kosten",
    "data_en_privacy",
    "link",
    "github_link",
    "in_top5",
    "reden_selectie_of_afwijzing",
]

SYSTEM_PROMPT = """\
Je bent een onderzoeksassistent voor een Windesheim lectoraat (hogeschool NL) \
dat AI-tools inventariseert voor onderzoekers en medewerkers.

Zoek nieuwe AI-tools die relevant zijn voor een of meer van deze domeinen:
- Academisch literatuuronderzoek (screenen, samenvatten, citatie-analyse, systematische reviews)
- Supply chain finance en kritieke grondstoffen (data-analyse, monitoring, netwerkanalyse)
- Werkprocesautomatisering (transcriptie, documentanalyse, e-mail, agendabeheer)
- Kennisgrafen, semantisch zoeken en RAG (Retrieval-Augmented Generation)
- Onderzoeksagenten en automatisch onderzoek

Selectiecriteria die je meeweegt per tool:
1. Universitaire adoptie — gebruiken Nederlandse of internationale universiteiten het?
2. Academische verankering — is de tool gepubliceerd of geciteerd in onderzoek?
3. Gebruiksgemak — is het direct bruikbaar zonder technische kennis?
4. Privacy — cloud met verwerkersovereenkomst, of lokaal draaien?
5. Kosten — gratis basisversie beschikbaar?

Geef output ALTIJD als een JSON-array met exact deze veldnamen:
toolnaam, type, waarvoor, gebruikers, aantal_universiteiten, universiteiten_voorbeeld,
in_literatuuronderzoek, literatuuronderzoek_toelichting, direct_bruikbaar_voor_team,
kosten, data_en_privacy, link, github_link, in_top5, reden_selectie_of_afwijzing

Regels voor de velden:
- in_top5: altijd "Nee" voor nieuwe tools
- in_literatuuronderzoek: exact "Ja" of "Nee"
- direct_bruikbaar_voor_team: exact "Ja" of "Nee"
- link: domein zonder https:// (bijv. elicit.com)
- github_link: github.com/user/repo of leeg
- universiteiten_voorbeeld: noem NL instellingen ALTIJD als je ze vindt
- reden_selectie_of_afwijzing: 1-2 zinnen waarom de tool wel of niet interessant is

Nooit een tool toevoegen die al in de bekende lijst staat.
Zoek minimaal 5 nieuwe tools per instructie.
"""


def check_deps() -> None:
    try:
        import anthropic  # noqa: F401
    except ImportError:
        print("Fout: anthropic package niet gevonden.")
        print("Installeer met: pip install anthropic")
        sys.exit(1)

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("Fout: ANTHROPIC_API_KEY niet ingesteld.")
        print("Stel in met: export ANTHROPIC_API_KEY=sk-...")
        sys.exit(1)


def load_existing_tools() -> set[str]:
    """Laad bestaande toolnamen (lowercase) voor duplicate-check."""
    if not CSV_PATH.exists():
        return set()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        return {row["toolnaam"].lower().strip() for row in csv.DictReader(f)}


def append_tools_to_csv(tools: list[dict]) -> tuple[int, list[str]]:
    """
    Voeg nieuwe tools toe aan CSV.
    Geeft (aantal_toegevoegd, lijst_van_overgeslagen_duplicaten) terug.
    """
    existing = load_existing_tools()
    nieuwe: list[dict] = []
    skipped: list[str] = []

    for tool in tools:
        naam = str(tool.get("toolnaam", "")).strip()
        if not naam:
            continue
        if naam.lower() in existing:
            skipped.append(naam)
            continue
        nieuwe.append(tool)
        existing.add(naam.lower())

    if not nieuwe:
        return 0, skipped

    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS, extrasaction="ignore")
        for tool in nieuwe:
            writer.writerow({h: str(tool.get(h, "")) for h in CSV_HEADERS})

    return len(nieuwe), skipped


def extract_json(text: str) -> list[dict]:
    """Extraheer JSON-array uit Claude's tekst (ook ingebed in markdown)."""
    # Strip markdown code blocks
    text = re.sub(r"```(?:json)?\s*", "", text)
    text = text.replace("```", "")

    # Zoek langste JSON-array in de tekst
    candidates = re.findall(r"\[[\s\S]*?\]", text, re.DOTALL)
    for candidate in sorted(candidates, key=len, reverse=True):
        try:
            data = json.loads(candidate)
            if isinstance(data, list) and all(isinstance(d, dict) for d in data):
                return data
        except json.JSONDecodeError:
            continue

    # Fallback: probeer de volledige tekst
    try:
        data = json.loads(text.strip())
        if isinstance(data, list):
            return data
    except json.JSONDecodeError:
        pass

    return []


def run_search_round(client, thema: str, bestaand: set[str]) -> list[dict]:
    """
    Voer één zoekronde uit via de Claude agentic loop met web search.
    Geeft lijst van gevonden tools als dicts.
    """
    bestaand_str = "\n".join(f"- {naam}" for naam in sorted(bestaand))

    messages = [
        {
            "role": "user",
            "content": (
                f'Zoek nieuwe AI-tools voor het thema: "{thema}"\n\n'
                f"Al bekende tools — NIET opnieuw toevoegen:\n{bestaand_str}\n\n"
                "Stap 1: Gebruik web_search om nieuwe tools te vinden.\n"
                "Stap 2: Zoek voor elke interessante tool of Nederlandse universiteiten "
                "of hogescholen het gebruiken.\n"
                "Stap 3: Geef een JSON-array terug met minimaal 5 nieuwe tools "
                "(niet in de bekende lijst hierboven)."
            ),
        }
    ]

    max_iteraties = 20

    for iteratie in range(max_iteraties):
        response = client.beta.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8096,
            system=SYSTEM_PROMPT,
            tools=[
                {
                    "type": "web_search_20250305",
                    "name": "web_search",
                    "max_uses": 10,
                }
            ],
            messages=messages,
            betas=["web-search-2025-03-05"],
        )

        tool_uses = [b for b in response.content if b.type == "tool_use"]

        # Klaar: geen tool use meer of einde bereikt
        if not tool_uses or response.stop_reason == "end_turn":
            full_text = "".join(
                b.text for b in response.content if hasattr(b, "text")
            )
            return extract_json(full_text)

        # Tool use aanwezig: verwerk en loop verder
        messages.append({"role": "assistant", "content": response.content})

        tool_results = []
        for block in tool_uses:
            if block.name == "web_search":
                query = block.input.get("query", "") if hasattr(block, "input") else ""
                print(f"    zoeken: {query[:80]}")

                # Web search is server-side: resultaten zitten in block.content
                content = getattr(block, "content", None)
                if not content:
                    content = [{"type": "text", "text": "Geen zoekresultaten."}]

                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": content,
                    }
                )

        if tool_results:
            messages.append({"role": "user", "content": tool_results})
        else:
            # Geen verwerkte tool results — stop om oneindige loop te voorkomen
            break

    print("  waarschuwing: max iteraties bereikt zonder eindantwoord")
    return []


def git_commit_push(n_nieuw: int, thema: str) -> None:
    """Commit en push CSV-wijzigingen naar origin/main."""
    try:
        subprocess.run(["git", "add", str(CSV_PATH)], cwd=REPO_ROOT, check=True)
        msg = (
            f"Tool-finder agent: {n_nieuw} nieuwe tools toegevoegd\n\n"
            f"Thema: {thema}\n\n"
            "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
        )
        subprocess.run(["git", "commit", "-m", msg], cwd=REPO_ROOT, check=True)
        subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, check=True)
        print("  gepushed naar origin/main")
    except subprocess.CalledProcessError as e:
        print(f"  git fout: {e}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Tool-finder agent: zoekt nieuwe AI-tools en voegt ze toe aan de longlist."
    )
    parser.add_argument(
        "--thema",
        default="AI tools voor academisch onderzoek, supply chain finance en werkprocesautomatisering",
        help="Zoekthema (bijv. 'transcriptie', 'supply chain', 'systematische review')",
    )
    parser.add_argument(
        "--rondes",
        type=int,
        default=2,
        help="Aantal zoekrondes (default: 2)",
    )
    parser.add_argument(
        "--commit",
        action="store_true",
        help="Commit en push na afloop als er nieuwe tools zijn",
    )
    args = parser.parse_args()

    check_deps()
    import anthropic

    client = anthropic.Anthropic()
    totaal_toegevoegd = 0

    print(f"Thema      : {args.thema}")
    print(f"Rondes     : {args.rondes}")
    print(f"CSV        : {CSV_PATH}")
    print(f"Bestaand   : {len(load_existing_tools())} tools")

    for ronde in range(1, args.rondes + 1):
        print(f"\n=== Ronde {ronde}/{args.rondes} ===")
        bestaand = load_existing_tools()

        tools_gevonden = run_search_round(client, args.thema, bestaand)
        print(f"  gevonden : {len(tools_gevonden)} tools")

        if not tools_gevonden:
            print("  geen tools gevonden of geen geldige JSON; volgende ronde")
            continue

        n, skipped = append_tools_to_csv(tools_gevonden)
        totaal_toegevoegd += n

        if skipped:
            print(f"  duplicaat: {', '.join(skipped)}")
        print(f"  nieuw    : {n} tools toegevoegd")

    print(f"\nTotaal toegevoegd : {totaal_toegevoegd} tools")
    print(f"Totaal in CSV     : {len(load_existing_tools())} tools")

    if args.commit and totaal_toegevoegd > 0:
        print("\nCommit en push...")
        git_commit_push(totaal_toegevoegd, args.thema)
    elif totaal_toegevoegd > 0 and not args.commit:
        print("\nNiet gecommit. Gebruik --commit om te pushen.")


if __name__ == "__main__":
    main()
