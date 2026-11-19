# Live Hockey Ratings

Live MyHockeyRankings-style ratings for 2012 (USA 14U + Ontario U15) and 2013 (USA 13U + Ontario U14), anchored to MHR's weekly Wednesday ratings and updated live with weekend results.

- `index.html` — the app. Since Nov 17, 2026 the public address https://mikemuf.github.io/livehockeyratings/ forwards visitors to https://myplayerdata.com/ (one script line at the top of `build/base_nov2.html`, carried into `index.html` by every build: keep it). The member site at myplayerdata.com/members/ still loads this file for its Ratings tab, so keep publishing updates here as before. To view the page directly, open it with `?stay=1`.
- `players/index.html` — stub that sends visitors to the preview; the full player database lives in the private repository `mikemuf/player`
- `preview/index.html` — public preview of the paid version, rebuilt from the private repository
- `data/` — MHR rank dumps, pending provisional games, weekend event notes
- `build/` — rebuild pipeline: `python3 build/build.py` (base app + anchors + games), `node build/run.js index.html 2012 25` (top 25)

## 2016 (Squirt) division, added Nov 17, 2026
- Anchored like 2011: `data/nov11_usa10.txt` (MHR USA 10U - All, `rank.php?y=2026&v=122`, top 150) and `data/nov11_on11.txt` (MHR Ontario U11 AAA, `v=132`, all 53). Format: name|record|rating|AGD|sched|MHR team id. Names drop the state, " 10U AAA" and " U11 AAA"; Ontario " U11 AA" becomes " AA".
- Weekly MHR update: re-read both pages, save new files and point `F10` / `ON11` in `build/build.py` at them, the same way `F15` / `ON16` are refreshed for 2011.
- 2016 is its own MHR pool (top 10U = 99.9). `build/solver.js` now pins each anchored division to its own top rating and no longer matches a team name across anchored divisions.
- `players/data/teams.json` was refreshed from the player database's team list (705 teams, including 2016) so team pages link to rosters.


Nov 18, 2026: GitHub Pages is off for this repository. The app is served to members from myplayerdata.com; see data/SCHEDULING.md.
