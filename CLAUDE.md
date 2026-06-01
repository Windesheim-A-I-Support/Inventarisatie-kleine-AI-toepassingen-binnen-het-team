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
interviews/DATUM-NAAM.qmd        interview per collega
data/radartjes.csv               radartjes uit interviews
data/tools-in-gebruik.csv        tools per collega
data/tools-longlist.csv          longlist externe tools
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

Secties in volgorde:
- Metadata (datum, naam, rol, duur)
- Digitale toolkit (tabel)
- `## Aantekeningen` -- gestructureerde notities per tijdstip, privé, niet gedeeld
- `## Gestructureerde Q&A` -- samenvatting per interviewvraag
- `## Radartjes` -- tabel met concrete radartjes
- `## Letterlijke signalen` -- quotes
- `## Nog niet oplossen`
- `## Samenvatting voor weekupdate`
- `## Volledige transcriptie` -- verbatim transcript ONDERAAN als appendix

### 3. Radartjes toevoegen
`data/radartjes.csv` -- kolommen: datum, collega, rol, werkproces, klein_radartje, input, gewenste_output, frequentie, gevoeligheid, huidige_tool, opmerking

### 4. Tools toevoegen
`data/tools-in-gebruik.csv` -- kolommen: datum, collega, rol, tool, categorie, waarvoor, frequentie, tevredenheid, opmerking

### 5. Interviewtabel bijwerken
`01-inventarisatie-kleine-ai-toepassingen.qmd` -- collega toevoegen aan afgeronde tabel, verwijderen uit geplande tabel.

### 6. Email-concept aanmaken
`updates/email-NAAM.md` -- bevat: bedankje, link naar PDF, radartjes ter verificatie, dashboard-link, relevante tips.

### 7. Committen
```bash
git add interviews/DATUM-NAAM.qmd "interviews/DOCX-bestand.docx" \
        data/radartjes.csv data/tools-in-gebruik.csv \
        01-inventarisatie-kleine-ai-toepassingen.qmd \
        updates/email-NAAM.md
git commit -m "Voeg [naam] interview toe: X radartjes en Y tools"
git push origin main
```

### 8. Email versturen
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
QMD aanmaken (aantekeningen + verbatim)
        ↓
CSV bijwerken (radartjes + tools)
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
