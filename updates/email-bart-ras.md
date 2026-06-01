# Email aan Bart Ras na interview

**Aan:** b.ras@windesheim.nl
**Onderwerp:** Bedankt voor het gesprek -- transcriptie + een paar tools voor jou

---

Bart,

Dankjewel voor je tijd vanmorgen. Fijn gesprek.

Hier alvast je transcriptie en samenvatting:

- [Transcriptie als PDF](https://windesheim-a-i-support.github.io/Inventarisatie-kleine-AI-toepassingen-binnen-het-team/downloads/interview-2026-06-01-bart-ras.pdf)
- [Transcriptie als Word](https://windesheim-a-i-support.github.io/Inventarisatie-kleine-AI-toepassingen-binnen-het-team/downloads/2026-06-01-bart-ras.docx)

Je radartjes staan ook live in het dashboard -- inclusief iedereen die ik al gesproken heb:

- [Dashboard](https://windesheim-a-i-support.github.io/Inventarisatie-kleine-AI-toepassingen-binnen-het-team/dashboard.html)

---

Zoals beloofd drie concrete dingen die je workflow direct verbeteren:

**1. Claude Code**
In plaats van code copy-pasten naar VS Code: Claude werkt dan direct in je codebase. Ziet alle bestanden, past aan, runt. Installeren via terminal: `npm install -g @anthropic-ai/claude-code`, daarna `claude` typen in je projectmap.

**2. CLAUDE.md**
Maak een bestand met de naam `CLAUDE.md` in je projectmap. Claude leest dit automatisch aan het begin van elke sessie -- je hoeft context dus niet meer elke keer opnieuw uit te leggen.

Wat je erin zet: wie je bent, wat het project doet, welke stijl je wil, welke tools beschikbaar zijn, wat hij absoluut niet mag doen. Eén keer schrijven, altijd actief.

Voorbeeld voor jouw legal agent:
```
# Legal agent
Ik ben CFO van vlastuin, een MKB-bedrijf in winkelinrichtingen.
Review inkomende NDAs op basis van de historische NDAs in /docs/ndas/.
Standaard NDA staat in /docs/standaard-nda.pdf.
Geef altijd: (1) must-haves, (2) nice-to-haves, (3) advies per tegenpartijtype.
```

**3. Claude Skills (voor je agents)**
Een lijst met kant-en-klare skills die je direct kunt installeren: [awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)

Skills zijn instructiebestanden die Claude vertellen hoe hij zich moet gedragen in een bepaalde rol. Vergelijkbaar met je CLAUDE.md, maar herbruikbaar over projecten heen -- je legal agent, Python agent, presentation agent kunnen elk hun eigen skill krijgen.

**Bonus: Caveman-modus**
Misschien het meest praktische trucje voor dagelijks gebruik. Claude praat normaal in lange beleefde zinnen die veel tokens kosten. Met caveman-modus vraag je hem kort en bondig te antwoorden -- geen "Zeker! Ik help je graag met..." maar gewoon de inhoud.

Vraag hem: *"Activeer caveman modus"* of installeer de caveman skill via de lijst hierboven. Scheelt tot 90% van je tokengebruik bij werkende sessies.

Groet,
Chris

*P.S. Deze e-mail, je transcriptie, je samenvatting en het dashboard zijn allemaal gegenereerd door AI agents -- als kleine demonstratie van wat er mogelijk is.*
