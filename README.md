# shawlabs.dev

Shaw Labs: where Suraj Shaw builds in the open. Experiments, case studies and notes.

Plain HTML and CSS. No framework, no build step on Vercel.

- `src/pages/*.html` are the pages. The first line of each is its title and description.
- `src/styles.css` is the design. `src/explorer.html` and `src/explorer.js` are the headline explorer, using the real v3.2.0 harm constants.
- `python3 build.py` writes the site to `dist/`, which Vercel serves (see `vercel.json`).

Add a new case study: copy `src/pages/world-chaos-map.html`, add it to `PAGES` in `build.py`, link it from the experiments table, add it to `sitemap.xml`.

## Adding an experiment

- **About people?** It goes on the scale. In `src/pages/index.html`, add a `.tile` button (set `data-n` to how many people it involves and `data-st` to live, build, design, proto or research) and a matching `.sp` section with the question, method, readings and an instrument. Toy code lives in `src/bench.js` and `src/lab.js`.
- **Not about people?** It goes on the shelf. Add one object to `src/shelf.json` and rebuild.

Then run `python3 build.py`.

## lastround.shawlabs.dev

The `lastround/` folder is a separate site for the Last Round app: home, privacy policy, alpha terms, support and help. It has no JavaScript and makes no third-party requests; its fonts are served from the site.

Deploy it as its own Vercel project from this repo with **Root Directory** set to `lastround`, then add the domain `lastround.shawlabs.dev`. Build locally with `python3 lastround/build.py`.
