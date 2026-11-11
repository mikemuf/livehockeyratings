# Live Hockey Ratings

Live MyHockeyRankings-style ratings for 2012 (USA 14U + Ontario U15) and 2013 (USA 13U + Ontario U14), anchored to MHR's weekly Wednesday ratings and updated live with weekend results.

- `index.html` — the app (served by GitHub Pages at https://mikemuf.github.io/livehockeyratings/)
- `players/index.html` — player database (15U 2011 and Bantam 2012/2013: top 50 USA + top 50 Ontario; Peewee 2014/2015: top 25 USA + top 10 Ontario), served at https://mikemuf.github.io/livehockeyratings/players/
- `data/` — MHR rank dumps, pending provisional games, weekend event notes
- `build/` — rebuild pipeline: `python3 build/build.py` (base app + anchors + games), `node build/run.js index.html 2012 25` (top 25)
