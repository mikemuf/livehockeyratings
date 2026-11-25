# Monday-night game check for the top teams (first run Mon Nov 23 2026, 11:20 PM-11:45 PM; owner: "make sure you get all the games so the ratings are accurate")
Why: Tuesday's North America Top 10 post rests on the weekend's games. The first check found 59 finished games (Nov 18-22) missing from our log,
mostly 2014 (New England elite teams' event with North Jersey Avalanche and Buffalo; Little Caesars league games) plus Ontario league games.
Steps (about 10 minutes):
1. `node tools/mhr_top_ours.js` -> /tmp/nar/ours.json (our games since last Wednesday, per birth year). Fix the date in the script each week.
2. Chrome, new tab on the outside ranking site's rank page (any). Run the collector (in data/LIVE_CHECK.md history / this file's git log: loads each list
   in a hidden iframe, takes the top 13 USA / top 9 Ontario team ids, loads each team's games page, stores `y|team|dayRESscore,...` in window.__o).
   Lists: USA 119 (2011), 114 (2012), 125 (2013), 124 (2014), 123 (2015), 122 (2016: NO team rows came back, not checked);
   Ontario 137 (2011), 136 (2012), 135 (2013), 134 (2014), 133 (2015), 132 (2016: empty); Western Canada 173 (2012).
   Never read a rank page as page text. Read window.__o about 17 lines at a time (output is cut near 1,000 characters).
   The tab FROZE once after ~150 team pages (an ad overlay, "#google_vignette"): close it, open a new tab, run the rest in smaller batches.
3. Paste the lines into /tmp/nar/mhr.txt, `python3 tools/mhr_top_diff.py` -> games they have and we do not (and ours-only).
4. Second pass for the teams with misses, this time with opponent names (`y|team|day|opponent|result`).
5. Add `[year, date, winner-or-home, goals, other, goals]` with APP names to data/pending_games.json (only when both teams are in the ratings),
   `python3 build/build.py`, `tools/live_pub.sh "..."`. The week's additions are kept in data/mhr_check_<date>_added.json.
Not added on Nov 23 (on purpose): games against teams outside the ratings (2011 Shattuck v two Calgary U17 teams; 2015 Dallas v Houston AA; 2014 Sun County v Loudoun AA);
a second Vaughan Kings 5-3 Toronto Red Wings (2013, listed on both Nov 20 and Nov 21, looks like a duplicate); Monday Nov 23 games (post says "through Sunday");
2012 Team Illinois v CarShield is 14-0 there and 13-0 on our page (no effect on the rating, check the sheet).

## FASTER WAY (Tue Nov 24 2026, 8:10-8:56 PM: 315 team pages, 145 games added). Use this from now on.
The comparison now happens INSIDE the browser, so only the misses come back.
1. New Chrome tab on a rank page of the outside site. Paste tools/mhr_reconcile.js once per site visit: store it with `localStorage.setItem('rc_src', <the __rc function text>)`
   and after every navigation run `eval(localStorage.getItem('rc_src'))`. Clear `localStorage.rc_lines` at the start of the night.
2. ONE LIST PER PAGE LOAD: navigate to rank.php?y=2026&v=<list>, wait 7 s, `window.__rc('<our year>', N)` (not awaited), wait, poll `window.__st` until "done ...".
   Lists: USA 119/114/125/124/123/122 = 2011..2016 (N 30); Ontario 137/136/135/134/133/132 = 2011..2016 (U16..U11, N 20); Western Canada U15 173 = 2012 (N 15).
   The 2016 lists DO return teams this way (ids come from the row links `team_info.php?y=2026&t=<id>`; take t, not the year).
   Speed: about 4.5 s a team when the tab is in front, 8-10 s when it is behind another tab (press Shift on it first). A batch of tool calls longer than ~3 minutes times out: one list per batch.
   The page FROZE again after about 190 team pages in one page load (several lists run through hidden frames): results are only saved at the end of a list, so run each list on a fresh page load.
3. `await window.__exp()`; read window.__un (names with no match) and window.__rows in slices of 55; rows are "yy,day,a,gf,b,ga" with indexes into the sorted name list.
4. Paste the rows into /tmp/nar/rows.txt; python: rebuild the name list from site/members/ratings/index.html, drop a==b, drop games where either team has no North America rank,
   drop anything in data/held_games.json, merge the two teams' views of one game (max of the two counts), drop games we hold within a day at the same score, write winner first.
   Print every addition whose two teams already have a game this week and read them (series are normal; a different score on the same day is not).
5. Copy /tmp/nar/now.json to /tmp/r_old.json, append to data/pending_games.json, build, DRIFT CHECK (idle teams' median move and how many moved over 0.10; a few one-game teams tied to
   a team that played is fine, a whole field moving is not), then rerun tools/silverstick_draw.py and tools/silverstick_team.py if an event preview is up, then tools/live_pub.sh.
   The night's additions are kept in data/mhr_check_<date>_added.json.
SETTLED Nov 24: 2013 Toronto Marlboros 5-1 on Nov 23 is a NEW game against Toronto Nationals, not a second listing of the 5-1 over Don Mills (added). 2013 Vaughan Kings 5-3 Toronto Red Wings
is listed once now. 2012 Team Illinois v CarShield no longer differs from our 13-0. NOT added: games against teams with no rank on our page (Alberta U15 teams, AA teams, Belle Tire 2013,
Long Island Gulls 2015), opponents outside our lists (2011 Calgary U17 teams, South Kent, Atlantic Coast, BioSteel, Upper Canada College; 2012 RHA Winnipeg/Kelowna, Airdrie, Okotoks, Bow Valley;
2015 Houston; 2016 NJ Devils, Mercer), and the two held 2016 Little Caesars v Fox Motors games.
MISTAKE Nov 24: the first team-id pattern caught the year in `y=2026` and loaded one wrong team 30 times in the test; caught on the 3-team test run before any list was used. Check: always test with N=3 and read the team names.
STILL OPEN: Western Canada U13 list for the 2014 page (list number not found yet).

## WHEN TO RUN (owner, Nov 24 2026 9:00 PM): MONDAY NIGHT ONLY. Never Tuesday night: the official weekly update lands about 1 AM Wednesday and replaces it.
The Nov 24 Tuesday run (145 games) is live but only stands until the 1:15 AM Wednesday update; nothing from it needs redoing.
