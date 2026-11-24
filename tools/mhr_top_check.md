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
