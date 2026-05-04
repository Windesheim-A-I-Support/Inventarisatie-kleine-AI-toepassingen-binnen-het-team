Read AGENTS.md first.

Then inspect the full repository structure before changing anything.

Your goal is to make this Quarto project robust and ready for use.

Work in this order:

1. Read AGENTS.md.
2. Read all files in the agents/ folder.
3. Check whether the repository structure matches AGENTS.md.
4. Check whether data/radartjes.csv and data/tools.csv have correct headers.
5. Check whether _quarto.yml renders the correct files.
6. Check whether GitHub Actions builds HTML, DOCX and PDF.
7. Check whether GitHub Pages deployment is correctly configured.
8. Check whether index.qmd links match the actual output files.
9. Add or fix only what is needed.

Important rules:

- Do not turn this into a broad AI strategy.
- Do not create a huge tool database.
- Do not invent interview results.
- Do not add real interview content.
- Keep the project focused on small AI-radartjes within the team.
- Keep interview input separate from interpretation.
- Keep the language clear and practical.
- Do not use m-dashes.
- Do not add unnecessary complexity.

First task:

Make a short implementation plan based on the current repo state.

Then apply the smallest set of changes needed so that:

- quarto render works
- HTML site output works
- DOCX output works
- PDF output works
- GitHub Pages can publish from _site
- download links on index.qmd are valid
- the repo is safe to use as a public project template

After making changes, show:

1. What you changed
2. Why you changed it
3. What commands you ran
4. Whether the render succeeded
5. Any remaining risks or manual steps

# Inventarisatie van kleine AI-toepassingen binnen het team

Dit project verzamelt kleine, concrete AI-toepassingen die collega’s binnen het team zelf zien in hun werk.

Het doel is eerst goed inventariseren. Dus nog geen oplossingen aandragen, geen grote strategie maken en geen lange toolcatalogus bouwen.

## Aanleiding

Uit het gesprek met Michiel kwam naar voren dat de focus moet liggen op kleine radartjes: concrete onderdelen van het werk waar AI mogelijk direct kan helpen.

Het gaat om twee praktische werksporen:

1. Kleine AI-radartjes ophalen bij collega’s.
2. Een paar direct bruikbare AI-tools vinden waar het team snel iets aan heeft.

## Uitgangspunten

- Eerst luisteren, dan pas duiden
- Geen oplossingen aandragen tijdens de inventarisatie
- Focus op kleine onderdelen van het werk
- Focus op direct bruikbare tools
- Waar mogelijk letten op academische of universitaire inbedding