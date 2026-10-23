# shawlabs.dev

Shaw Labs: where Suraj Shaw builds in the open. Experiments, case studies and notes.

Plain HTML and CSS. No framework, no build step on Vercel.

- `src/pages/*.html` are the pages. The first line of each is its title and description.
- `src/styles.css` is the notebook design.
- `python3 build.py` writes the site to `dist/`, which Vercel serves (see `vercel.json`).

Add a new case study: copy `src/pages/world-chaos-map.html`, add it to `PAGES` in `build.py`, link it from the experiments table, add it to `sitemap.xml`.
