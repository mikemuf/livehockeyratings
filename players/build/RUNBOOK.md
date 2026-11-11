# Player database: weekly update runbook

The page is `players/index.html`, served at https://mikemuf.github.io/livehockeyratings/players/.
A second copy is kept as a Claude artifact (https://claude.ai/artifact/GD1DB4CsbbXf5tAwnc3YZs); update both. Everything needed to rebuild it is in `players/build` (scripts) and `players/data` (stored data).

## Before anything else

If the file `players/data/LOCK` exists, another session is in the middle of a large update (new teams or a re-pull). Do not harvest, build or push. Tell Mike in one line that the weekly update was skipped because a manual update was in progress, and stop.

## Rules

- Team list is frozen (`data/teams.json`): Bantam = 50 USA + 10 Ontario for each of 2012 and 2013; Peewee = 25 USA (from the Nov 10 ranking) + 10 Ontario (from the Nov 11 ranking; in Ontario 2014 = U13 and 2015 = U12) for each of 2014 and 2015, added Nov 11, 2026. The ratings site's Canada list for Peewee includes Quebec, BC and Alberta teams; only Ontario teams were taken. Do not add or remove teams unless Mike asks.
- Read InStat through rendered pages only (hidden same-origin iframes). Do not intercept or call InStat's internal API.
- Never enter a password. If InStat shows a sign-in page, stop and tell Mike he needs to sign in to Hudl in the Claude desktop app's browser.
- Hand corrections live in the page itself and must survive: `POSFIX` (positions), `BORN` and `GBORN` (2013-born players on 2012 teams), `mult` (16% per rating point, 95 = 1.00), `MINGP`. `inject.py` does not touch them.
- Goalies show plain GA/G plus Adj GA/G and Avg opp. Adj GA/G is opponent-only (`gmult` in the page: 94 = 1.00, goals count 16% less per point above 94 and 25% more per point below, capped at 88). `gmult` is a hand setting; `inject.py` does not touch it.
- Do not publish if the canary fails or the sanity checks fail. Report instead.

- 15U (2011 birth year): top 50 USA from MHR's Nov 11, 2026 15U Tier 1 ranking, added Nov 11, 2026. The ratings site carries 2011 as an anchored division (`data/*_usa15.txt`, MHR `rank.php?y=2026&v=119`). The page shifts 15U opponent ratings by `OFF` (3.83) for the multipliers only. No InStat page was found for Middlesex Islanders 15U or Neponset Valley 15U, and Mid-Fairfield 15U has no games.
- The ratings site and the database link to each other: ratings team pages link to `players/#team=<key>` (map built from `data/teams.json` in `build/build.py`), and the database links to `#team=<year>|<team name>` on the ratings site.

## Steps

All commands run from `players/data`.

1. Get the repo current: `git -C <repo> pull`. The Wednesday ratings update must already be pushed (it runs at 1:15 AM Central).
2. Current ratings: `node ../build/ratings_from_site.js ../../index.html ratings.json`
3. Prepare the browser script: `python3 ../build/prep.py` writes `harvest_run.js` (team ids, recently stored game ids, a 24-day look-back cutoff, and two canary games).
4. In the built-in browser open `https://app.hudl.com/instat/hockey/teams/1151096` and confirm the page shows a team (not a sign-in page). Run the contents of `harvest_run.js` with the JavaScript tool. It returns immediately and keeps working.
5. Poll every few minutes (JavaScript tool calls time out at 45 s, so only read status):
   `JSON.stringify({phase:__pdb.phase,t:__pdb.tdone,m:__pdb.mdone,of:__pdb.mtotal,err:__pdb.err.slice(0,5)})`
   Team pages take about 20 seconds each in a hidden pane (125 teams, about 40 minutes), then the new games.
   If the tab was reloaded or the computer dropped, `__pdb` is gone: run the script again.
6. When `phase` is `done`, collect: `JSON.stringify({T:__pdb.T,M:__pdb.M})`. A large result is saved to a tool-results file; a small one comes back inline. Save it as `harvest.json` (if the tool wrapped it as a JSON string, decode it first). If it is over about 250,000 characters, collect `T` and `M` in separate calls, or `M` in slices.
7. Merge: `python3 ../build/merge.py harvest.json`
   - `CANARY FAILED` means InStat changed its page layout. Stop, publish nothing, tell Mike.
   - "not ready" games have no box score yet; they are picked up next week by the look-back.
8. Build: `python3 ../build/build.py` writes `db.json`. Check the printout:
   - skater and team-game counts should not drop compared with last week (the last run's numbers are in `run_log.txt`);
   - `TEAMS MISSING FROM RATINGS` should be empty (a renamed team on the ratings site: fix the name in `teams.json`);
   - new `UNMATCHED` opponents with several games may need an entry in `alias.json` (InStat name: ratings-site name).
9. Inject: `python3 ../build/inject.py ../index.html "Nov 18, 2026"` (today's date).
10. Test before pushing: extract the page's `<script>` to a file and run `node --check` on it; confirm `S`, `GAMES`, `LOGS` parse and the page still contains `const mult=r=>Math.exp(0.16*(r-95));`.
11. Append one line to `run_log.txt` (date, games added, total games, skaters, goalies, anything odd). Commit `players/` and push.
12. Update the Claude artifact copy too (Mike wants both kept current): copy `players/index.html` to a temp file with the back link `href="../"` changed to `href="https://mikemuf.github.io/livehockeyratings/"`, then publish it with the artifact tools to slug `7b26226d-b439-4f30-a1e4-ed16bf451c6e` as `index.html` (get the current version with get_artifact and pass it as base_version). If the artifact tools are unavailable, say so in the report.
13. Message Mike: games added, which teams had new games and which top teams had none, new players who cracked the top of the Adjusted P/G list, anything that looked wrong, then the link.

## Power play

Each new game is read twice: the Overview page (box score) and the Skaters page in InStat's PP view (power-play time, goals, assists). The PP choice is remembered by InStat, so the script switches the selector back to Game total at the end. `browser/pp_backfill.js` re-reads PP data for every stored game if it is ever needed again.

## Known limits

- New players get InStat's own position label, which is unreliable. `pos.json` holds the positions inferred on Nov 10, 2026 from line combinations and faceoffs; re-running that inference needs a separate pull of each team's Lines and Faceoffs pages and is not part of the weekly run.
- The team overview page lists a team's last 25 games. That covers a weekly run; after a gap of several weeks, check the team's Games tab as well.
- Peewee positions come from `positions_lines.py` (line units + faceoffs) run on `data/lines_peewee.json`, pulled Nov 11, 2026. Peewee teams with no InStat games: 2014 Top Gun; 2015 Boston Jr Eagles, Lovell Winter Club (not found in InStat), South Shore Kings, Bay State Breakers. Several eastern Peewee teams have only 1 to 5 games.
- InStat team ids per database team are in `wanted.json`. Teams with no InStat data: 2012 MN Lakers, MN Grey Ducks, MN Moose; 2013 Team North Dakota, MN Blue Ox.
