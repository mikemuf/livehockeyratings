# Handoff from the live-ratings thread (Nov 18, 2026)

All live-ratings work moved to the player-database thread on Nov 18. This file holds what was known here and is not already in README.md, SCHEDULING.md, WEEKEND_SOURCES.md or the weekend_*.txt runbooks.

## the owner's standing rules (consolidated)
- Reports: summary only, never the top-25 list. 2012 always first. Each team gets (rank, rating) in parentheses. Include upcoming games with both teams' rankings. Lead with the real story (upsets, tournament results, standings/tiebreak scenarios, head-to-head history).
- Goalies: goals against / GAA only (no saves, shots or SV%).
- Never write "Coach MUF". Never reference the owner himself, his opinions or his predictions on the public site. His son Michael may be named like any other player on a game sheet.
- The final reply of every scheduled run is delivered to the owner as a message. It must be the actual score/news update: no meta talk, no "I checked and found nothing, so no message", no self-corrections.
- Check frequency follows the games (SCHEDULING.md): every 15 min during games, every ~5 min in semifinals and finals, no repeated no-news runs.
- Games to watch must drop a game once it is final (weekend.js `played()` filter does this automatically when the game is in a games file or pending_games.json).
- MHR team pages are the source of truth for scores. All games count. Shootout = one-goal win (3-4 SO counts as 3-4, not a tie).
- Never click or solve CAPTCHAs.
- Only change scheduled tasks when the owner explicitly asks.

## Nov 18 MHR update: details
- Files: data/nov18_*. MHR_THROUGH='2026-11-17', MHR_PUBLISHED='Nov 18'. Last weekend's games are in data/games_wk_nov13.json; pending_games.json was cleared.
- Dump thresholds: usa14, usa14_agd, usa13, usa13_agd, on15, on14 = full tables. usa12 = rating >= 87 plus the key AAA teams below that (221 lines). usa11 = rating >= 84, non-AAA teams only if >= 87.5. usa15 = top 115 with team ids. on16 = 51 rows. usa10 = top 150. on11: " U11 AA" suffix renamed to " AA".
- 10U rank page (usa10) is often empty on first load: reload it. It has no rank cell, so the dump uses an index offset.
- New 2012 teams/aliases: Prairie Storm U15 AA, Calgary CNHA Northstars, St Albert Sabres. 2013: Lafayette Locomotive (14U AA). New X anchors in build.py: Prairie 94.40, CNHA 94.79, St Albert 94.58, Calgary Edge School 96.11, OHA Edmonton 97.83, Lafayette 87.31 (LA Kings' Western Canada trip opponents).
- Accuracy of our live predictions vs MHR: 2012 17/25 exact, mean abs error 0.065. 2013 14/25 exact, mean error 0.156, mostly because MHR shifted the whole 13U/14U pool down about 0.2.
- Top-25 rating-math check: all match except Dallas 2012 (MHR counts 22 games, we have 21). Find the missing game next week.
- Corrected: 2013 Milwaukee vs Windy City on 11-07 is 5-1 (was 5-0) in games_wk_nov6.json.

## GameSheet notes not in the runbooks
- Reapers/Mission game sheets are often left LIVE or stuck at 0-0 after the game ends. Always confirm finals on MHR. Example: 2011 Reapers–Mission on Sun Nov 15 was recorded 1-0 Mission from a stale sheet; MHR shows Reapers 4-3 (fixed, box entry removed).
- Season ids: Mission exhibitions 15464, Reapers account 15356, LC 2011 Weekend Series 16677, 2012 Challenger Cup 16410 (final = game 3157305).

## Scraping / comparison approach
- Rank pages: run JS that parses the table into compact rows and writes them to window.__out (or into <main><pre>); never get_page_text on a full rank page.
- Live scans used small window globals: __live (live games on a GameSheet list), __peek (one game's box score via an off-screen iframe /seasons/<S>/games/<id>?tab=box-score), __scan / __tg (MHR team game pages for a date range).
- Missing-game sweep ("cmp"): for each top-N team, build a multiset of date+score from its MHR team page and compare with the app's allGames for that team; anything on MHR but not in the app goes to pending_games.json (or the week's games file). This found 25 missing games on Nov 18.

## Weekend Nov 20–22
- data/weekend_public.json 2012 watch list includes Team Illinois' four games and Top Gun vs Boston Jr Eagles (Sat 10:50, ICENTER). See data/weekend_nov20.txt.

## Scheduled tasks
- The player-database thread (see the private notes) owns the Wednesday MHR update, the Sat/Sun 7:12 planner and the Friday live-check start.
- All tasks bound to the old live-ratings thread are disabled. delete_trigger is blocked, so disable with update_trigger enabled=false.
