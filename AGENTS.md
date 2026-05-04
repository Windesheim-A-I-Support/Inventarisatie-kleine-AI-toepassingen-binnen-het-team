# AGENTS.md

## Projectdoel

Dit project is een Quarto-gebaseerde inventarisatie van kleine AI-toepassingen binnen het team.

Het doel is niet om een grote AI-strategie te maken, maar om kleine, concrete werkonderdelen te vinden waar AI direct nuttig kan zijn.

De opdracht heeft twee werksporen:

1. Kleine AI-radartjes ophalen bij collega’s.
2. Een paar direct bruikbare AI-tools selecteren waar het team snel iets aan heeft.

## Belangrijke uitgangspunten

- Eerst luisteren, dan pas duiden.
- Tijdens interviews geen oplossingen aandragen.
- Geen grote toolcatalogus maken.
- Focus op praktische, kleine toepassingen.
- Focus op output waar Michiel en het team direct iets aan hebben.
- Houd ruwe interviewinput gescheiden van interpretatie en advies.
- Schrijf helder Nederlands.
- Gebruik geen m-dashes.
- Gebruik geen onnodige YAML front matter separators.

## Huidige projectstructuur

```text
.
├── _quarto.yml
├── index.qmd
├── 01-inventarisatie-kleine-ai-toepassingen.qmd
├── 02-direct-bruikbare-ai-tools.qmd
├── interviews/
│   └── _template-interview.qmd
├── updates/
│   └── week-01.qmd
├── data/
│   ├── radartjes.csv
│   └── tools.csv
└── .github/
    └── workflows/
        └── render-quarto.yml