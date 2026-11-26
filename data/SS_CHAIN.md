# Silver Stick live check: the ONE chain (owner Nov 26 12:38 PM: every 7 minutes during live games)

Each firing, in this order. Keep it short: three tool calls when nothing is final.

1. send_later the SAME short message ('SS LIVE CHECK (the one 7-minute chain). Read ... SS_CHAIN.md ...'), delay 7 minutes. If step 3 then prints a later 'NEXT CHECK' time, that is fine for one extra firing: the next firing reads the printout and schedules the later time instead of 7 minutes. Never two copies of the chain. An old message that says '15 min from now' is retired: do nothing, do not reschedule it.
2. Chrome tab 339724668 (https://gamesheetstats.com/seasons/16542/games?filter%5Bstatus%5D=all): `await window.__ssl('Nov 26')` (Fri 'Nov 27', Sat 'Nov 28', Sun 'Nov 29'). If window.__ssl is undefined: paste tools/ss_list.js (the window.__ssl=... part) first. FINAL = a score with no LIVE word (fixed Nov 26 1:22 PM). If the tab is gone: tabs_context, new tab, navigate, paste.
3. Shell, in /home/claude/livehockeyratings: `python3 tools/ss_check.py "<the whole string>"`. It publishes only when a tracked score or status changed, lists NEW FINAL lines, unparsed rows, live gaps, and prints NEXT CHECK.
4. For each NEW FINAL:
   - first final of the weekend: confirm the FINAL row format in window.__ssraw[id]; look at the 2011/2013/2015 pages at phone width (/tmp/t_live.py pattern), leaders and harder-road blocks.
   - STORY if it qualifies (rule A both teams NA top 30; B overtime/shootout with a top-30 team; C upset 10+ ranks apart with the beaten team top 30; ranks from BEFORE the game). Build with player/build/ig_story2.py (theme color, three-line wording: result with both names and ranks / how it went / who scored by name from the Box score tab), post through Meta Business Suite with the link sticker SILVER STICK COVERAGE -> https://myplayerdata.com/live/?y=YEAR (coordinates in player/build/IG_POSTING.md, last lines). Limits: 12 slides a day, 5+ minutes apart, keep 3 for the evening. Count used today is the last line of this file.
   - stop rule: a result that moves the rest of a birth year by more than about 0.15: hold it (data/held_games.json), tell the owner in one line.
5. Evening after the last final: late sweep, pool standings + leaders story slides, hand-written drama lines per birth year (weekend_nov26.txt), then schedule the next day's first tracked start + 3 minutes. Saturday night: bracket teams and Sunday games onto the watch lists (new sheet ids into silverstick_2026_gs.json). Sunday bracket: every 5 minutes.
6. Say nothing to the owner unless something is wrong or needs him (one line). No scores in chat.

STORY SLIDES USED Thu Nov 26: 2 (11:26 AM video, 12:00 PM link slide)
