# Project: Inventarisatie kleine AI-toepassingen

Windesheim hogeschool. Opdracht van Michiel Steeman. Twee werksporen:
1. Kleine AI-radartjes ophalen bij collega's via verbale interviews
2. AI-tools vinden die andere universiteiten gebruiken

## Taal en stijl
- Altijd Nederlands
- Geen m-dashes (gebruik --)
- Geen Co-Authored-By in commits
- Geen oplossingen aandragen tijdens interviews
- Emails aan Michiel: kort en scanbaar, max 10 regels per collega

## Bestandsstructuur

```
interviews/DATUM-NAAM.qmd        interview + rapport per collega
data/radartjes.csv               radartjes uit interviews
data/tools-in-gebruik.csv        tools per collega
data/tools-longlist.csv          longlist externe tools
03-processen-lectoraat.qmd       procesoverzicht lectoraat (website-pagina, na elk interview bijwerken)
updates/email-NAAM.md            email-concept per collega
updates/email-NAAM.eml           verstuurbare EML met PDF-bijlage
.github/workflows/render-quarto.yml   GitHub Actions (Quarto render)
```

## Interview workflow

Elke stap uitvoeren in volgorde. Specifieke bestanden stagen, nooit `git add .` of `git add interviews/`.

### 1. Transcript uitlezen
DOCX staat in `interviews/`. Uitlezen via Python zipfile + xml.etree (geen pandoc beschikbaar):
```python
import zipfile, xml.etree.ElementTree as ET
with zipfile.ZipFile('bestand.docx') as z:
    xml = z.read('word/document.xml')
root = ET.fromstring(xml)
for para in root.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
    texts = [t.text or '' for t in para.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')]
    print(''.join(texts))
```

### 2. QMD aanmaken
Bestandsnaam: `interviews/DATUM-NAAM.qmd`. Volg exact het format van bestaande interviews.
Vul zoveel mogelijk vragen in uit de interview template op basis van het transcript.

Secties in volgorde:
- Metadata (datum, naam, rol, duur)
- `## Jouw positie in het bredere beeld` -- DIRECT NA metadata, voor toolkit
- Digitale toolkit (tabel)
- `## Aantekeningen` -- gestructureerde notities per tijdstip, privé, niet gedeeld
- `## Gestructureerde Q&A` -- samenvatting per interviewvraag
- `## Radartjes` -- tabel met concrete radartjes
- `## Letterlijke signalen` -- quotes
- `## Nog niet oplossen`
- `## Samenvatting voor weekupdate`
- `## Aanbevolen tools en tips` -- op basis van analyse (stap 3)
- `## Research buddy` -- met wie samenwerken, wie kan wat leren van wie
- `## Volledige transcriptie` -- verbatim transcript ONDERAAN als appendix

### 3. Analyse
Inputs voor de analyse (allemaal lezen voor je radartjes en rapport schrijft):
- Ruwe transcript + ingevulde QMD (stap 2)
- Alle bestaande interview QMDs (`interviews/DATUM-*.qmd`)
- `data/radartjes.csv` -- patronen over alle collega's
- `data/tools-in-gebruik.csv` -- toolkit overzicht
- `data/tools-longlist.csv` + `02-direct-bruikbare-ai-tools.qmd`
- WebSearch: externe bewijzen dat genoemde pijnpunten breed voorkomen (andere hogescholen, universiteiten, NL hoger onderwijs context)
- WebSearch: specifieke tools die de persoon noemt -- wat doet het precies, alternatieven

Doel: identificeer radartjes, patronen, verbanden met andere interviews, externe validatie.

### 4. Radartjes toevoegen
`data/radartjes.csv` -- kolommen: datum, collega, rol, werkproces, klein_radartje, input, gewenste_output, frequentie, gevoeligheid, huidige_tool, opmerking

### 5. Tools toevoegen
`data/tools-in-gebruik.csv` -- kolommen: datum, collega, rol, tool, categorie, waarvoor, frequentie, tevredenheid, opmerking

### 6. Interviewtabel bijwerken
`01-inventarisatie-kleine-ai-toepassingen.qmd` -- collega toevoegen aan afgeronde tabel, verwijderen uit geplande tabel.

### 7. Procesoverzicht bijwerken
`03-processen-lectoraat.qmd` -- voeg nieuwe processen toe of update bestaande processen met nieuwe deelnemer. Dit is een website-pagina die een helikopterview geeft van alle werkprocessen in het lectoraat, gebaseerd op alle interviews samen.

### 8. Rapport voltooien in QMD
Vul op basis van stap 3 (analyse) de volgende secties in het QMD in:
- `## Jouw positie in het bredere beeld` -- vergelijking met alle collega's, gedeelde radartjes, wat deze persoon toevoegt
- `## Aanbevolen tools en tips` -- concrete tools uit de longlist + extern onderzoek die passen bij de radartjes
- `## Research buddy` -- wie in het lectoraat kan het meest van elkaar leren

### 9. Email-concept aanmaken
`updates/email-NAAM.md` -- bevat: bedankje, link naar PDF, radartjes ter verificatie, dashboard-link, relevante tips.

### 10. Committen
```bash
git add interviews/DATUM-NAAM.qmd "interviews/DOCX-bestand.docx" \
        data/radartjes.csv data/tools-in-gebruik.csv \
        01-inventarisatie-kleine-ai-toepassingen.qmd \
        03-processen-lectoraat.qmd \
        updates/email-NAAM.md
git commit -m "Voeg [naam] interview toe: X radartjes en Y tools"
git push origin main
```

### 11. Email versturen
1. Wacht tot GitHub Actions klaar is: `gh run list --limit 3`
2. Download PDF: `curl -o /tmp/naam.pdf "https://windesheim-a-i-support.github.io/.../downloads/interview-DATUM-NAAM.pdf"`
3. Maak EML aan met Python (email.mime) inclusief base64 PDF-bijlage en `X-Unsent: 1` header
4. Open: `xdg-open updates/email-NAAM.eml` -- opent in Thunderbird

## Pipeline: van DOCX naar gepubliceerd PDF

```
Interview (Teams-opname)
        ↓
DOCX transcriptie in interviews/
        ↓
Python: tekst uitlezen uit DOCX
        ↓
QMD aanmaken (template vragen ingevuld)
        ↓
ANALYSE: transcript + alle interviews + CSV data + WebSearch
  - radartjes identificeren
  - verbanden andere interviews
  - externe validatie pijnpunten
  - tools onderzoeken
        ↓
CSV bijwerken (radartjes + tools)
        ↓
03-processen-lectoraat.qmd bijwerken
        ↓
Rapport voltooien in QMD:
  - Jouw positie in het bredere beeld
  - Aanbevolen tools en tips
  - Research buddy
        ↓
git push origin main
        ↓
GitHub Actions (.github/workflows/render-quarto.yml)
  - rendert interviews/DATUM-*.qmd → PDF + DOCX
  - rendert dashboard.qmd apart (format: dashboard mag niet overschreven worden)
        ↓
GitHub Pages publiceert:
  downloads/interview-DATUM-NAAM.pdf
  downloads/DATUM-NAAM.docx
  dashboard.html
        ↓
EML aanmaken met PDF-bijlage → xdg-open → Thunderbird → versturen
```

## Git-regels
- Altijd specifieke bestanden stagen -- nooit `git add .` of `git add interviews/`
- Geen Co-Authored-By trailer in commits
- Geen lock files, .Rhistory, rendered PDFs in `interviews/`, losse HTML-bestanden committen

## Dashboard
Automatisch gegenereerd uit CSV-data. Niet handmatig aanpassen.
Live: https://windesheim-a-i-support.github.io/Inventarisatie-kleine-AI-toepassingen-binnen-het-team/dashboard.html
