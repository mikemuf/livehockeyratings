# When to run live checks (the owner, Sun Nov 15 10:31 PM)

the owner wants the check frequency to follow the games, not the clock. No runs when nothing is happening.

## The weekend planner (scheduled task "Weekend live-ratings check", Sat & Sun 7:12 AM CT)
Each planner run:
1. Builds the day's list of tracked games with start times in Central. Sources:
   - The weekend file (data/weekend_*.txt) and the schedule files.
   - The tournament schedules and GameSheet lists.
   - MHR PREVIEW lines for top-25 teams.
   - The Reapers/Mission accounts.
2. If there are no tracked games that day, it sends one short line ("No tracked games today") and stops.
3. Otherwise it uses send_later for the first check at the first game's start + 15 min. It sends no score message at this point. The final reply is only a one-line plan, e.g. "Today: first puck 8:30 AM — live checks start 8:45."

## Live checks (send_later chain)
- Run every 15 min while any tracked game is in progress or starts within 30 min.
- Run every 5 min during tournament semifinals and championship games.
- Gap rule: if no game is live and the next start is more than 45 min away, schedule the next check for that start time + 15 min. Do not run during idle gaps.
- After the day's last tracked game is final:
  - Post the day's wrap-up message.
  - Stop the chain. No more runs that day.
- Late results:
  - At most one "late results" sweep, ~2 hours after the last game (MHR top-25 scan for that date).
  - Only message if something new was added.
- Sunday after the sweep: nothing more until the Wednesday MHR update.

## Friday evening games
The Wednesday MHR update builds the weekend schedule. If tracked teams play Friday, it sets a send_later for Friday at the first start + 15 min.

## Messages
- The final reply of every run reaches the owner. It is a short score or news update only.
- If a check finds nothing new, keep it to one line.
- Avoid scheduling a check that is likely to find nothing new.

## Nov 18, 2026: everything runs in one conversation now
the owner moved all live-ratings work into the player-database conversation. The Wednesday MHR update, the Saturday/Sunday 7:12 AM planner and the Friday live checks are now send_later chains in that conversation; each run schedules its own next run first. The old scheduled tasks of the same names are switched off. Reports link https://myplayerdata.com only, never the mikemuf.github.io address.


## Nov 18, 2026: this repository no longer serves a website
At the owner's request GitHub Pages is turned off here (Settings > Pages > branch None), so https://mikemuf.github.io/livehockeyratings/ no longer exists. The ratings app is still built here (`python3 build/build.py`), and after every build it must be copied onto the member site with `build/ratings_to_site.sh` from the private player repository, which publishes it at myplayerdata.com/members/ratings/. All reports link https://myplayerdata.com only.

Same evening: Pages now serves the branch `gone` (a single notice, "This page no longer exists."). Leave it on that branch; `main` is not served.


## Weekend tab format and events calendar (Nov 19, 2026, the owner's instructions)
- Layout: each division in `data/weekend_public.json` has `events` (shown first as "Events this weekend"), `sections` = [{"t": title, "b": [short bullets]}] (one card each: one section per event, a players-to-watch section, "Elsewhere"), and `watch`. The page adds "Where the top 10 are" by itself from `watch`. Keep `summary` to the first few bullets (the landing page shows them). Bullets are short; a bullet that starts "Label: text" shows the label in bold. No long paragraphs.
- Times: EVERY time is Central, in the bullets and in `watch`. A watch entry carries `time` (Central), `tz: "CT"` and, when the rink is in another zone, `local` (for example "4:00 PM ET"), shown as "at the rink". No duplicate games (the same game listed from both teams' schedules).
- Never say where schedules or stats come from, and never write as if talking to the owner.
- Events calendar: the private player repository has `EVENTS.md` (/home/claude/player/EVENTS.md) with every tournament seen so far, its dates and usual timing. Read it before writing a preview and add every new event to it. International Silver Stick (Whitby) starts US Thanksgiving Thursday.

## Ranks and ratings in the Weekend text go stale on Wednesdays (found Nov 19, 2026)
The Nov 20-22 previews were written Nov 17, before the Wednesday Nov 18 rating update, and still carried the old ranks and ratings on Thursday (43 mentions wrong, e.g. "all eight ranked in the top 16" when two teams had moved to #16 and #17). After EVERY ratings update, and again before any Instagram weekend post, re-check every "(#rank, rating)" and every "top N" claim in data/weekend_public.json against the current solver output (player repo: build/ratings_from_site.js -> data/ratings.json).

## One Weekend tab per birth year, USA and Ontario together (owner, Nov 19, 2026 4:44 PM)
Do not make an "Ontario" section. Everything for a birth year is in one place, organized by event and game, not by country: a big Ontario game gets its own section like any other event (the game, head-to-head, players to watch, goalies, what is next), smaller Ontario games go in "Elsewhere" beside the American ones, and "Where the top teams are" lists the USA top 10 and the Ontario top 5 in one card. Players-to-watch numbers come from the player database at that moment.

## Rank in front of every team (owner, Nov 19, 2026 5:08 PM)
Everywhere a game or team is listed on the Weekend tab: rank first, name, rating in parentheses, e.g. "#24 Philadelphia Jr Flyers (89.91)", "Ontario #3 Vaughan Kings (92.66)", "NR Belle Tire (83.57)". Ontario teams show their Ontario rank. For this to work, team names in data/weekend_public.json watch lists must be spelled exactly as in the ratings (e.g. "Ohio Jr Bluejackets", "St. Louis Blues"); a name that does not match shows no rank. Check for unmatched names after every edit.
Mistake fixed the same day: "Where the top teams are" printed "Ontario #undefined" because the rank table only held American teams; Ontario ranks are now computed too. Look at the live page after any change to build/weekend.js.

## North American rank (owner, Nov 19, 2026)
- One rank per birth year across USA and Canada together, ordered by rating. It is the number in front of every team on the Weekend tab and the `#N` in every text mention. The country rank and rating follow in parentheses: `#8 Chicago Mission (USA #5, 97.05)`.
- Ratings app has a North America tab (`renderNA`). `data/ratings.json` in the player repo carries `na` beside `rank` (country rank). `weekend_check.py` checks text mentions against `na`.
- Ontario U13 (2014) and U12 (2015) rank pages are MHR `rank.php?y=2026&v=134` and `v=133` -> `data/nov18_on13.txt`, `data/nov18_on12.txt` (name|record|rating|agd|sched). Refresh them with the weekly MHR update, along with on14/on15/on16/on11. Ontario teams with no game in our log are listed with MHR's published numbers unchanged (`ANCH` in build.py).
- Western Canada is not in the list yet; the owner is unsure those ratings compare.

## After every final: a mini write-up (owner, Nov 19, 2026, 10:09 PM) — applies to every live check
When a tracked game goes final, in the same check:
1. Enter the result (`data/pending_games.json` for rated teams, `data/unrated_games.json` otherwise) and the box score in `data/gs_box.json` when the scoring system gives one. The game then leaves "Games to watch" and shows under "Final scores".
2. Write a short recap into `data/weekend_public.json` under `recaps["<year>|<YYYY-MM-DD>|<team A>|<team B>"]` (the two team names in alphabetical order, exact app names). It shows as "Game recap" on that game's page. Four to six bullets, each starting with a label:
   - `Final:` score and what the game was.
   - `Scoring:` who scored and set up the goals, from the game sheet (GameSheet for Northeast Pack; the event's own scoring page elsewhere, for example Spordle for the Pat Quinn Classic). Power-play and game-winning goals when shown.
   - `Goalies:` goals against only.
   - `Standings:` what it did to the league or tournament standings (points, place, what each team needs next).
   - `Ratings:` how the live rating and North American rank moved for both teams (before and after), or "no change" with the reason.
   - `Next:` each team's next game, Central time.
3. Refresh the birth year's summary bullets so the top of the tab tells the current story.
4. Then the Instagram FINAL post, 10 minutes from any other post. Owner, Nov 19, 10:10 PM: the mini write-up goes in the Instagram post too. Slide: FINAL, both teams with North American rank, the score, and one or two lines on what it means. Caption: the recap in short form: who scored (goal scorers and the game winner, from the game sheet), what it did to the standings, how the ratings and ranks moved, then "Full recap and live ratings: link in bio". Scorer names in a FINAL post are fine (they are the facts of the game); still never build a post around one player.
Every number comes from the game sheet and the live build at that moment. Never mention the owner. Goal: a page people come back to after every game.
