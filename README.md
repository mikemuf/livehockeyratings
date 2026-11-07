# Live Hockey Ratings

Live MyHockeyRankings-style ratings for 2012 (USA 14U + Ontario U15) and 2013 (USA 13U + Ontario U14), anchored to MHR's weekly Wednesday ratings and updated live with weekend results.

- `index.html` — the app (served by GitHub Pages at https://mikemuf.github.io/livehockeyratings/)
- `data/` — MHR rank dumps, pending provisional games, weekend event notes
- `build/` — rebuild pipeline: `python3 build/build.py` (base app + anchors + games), `node build/run.js index.html 2012 25` (top 25)
