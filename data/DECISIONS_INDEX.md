# DECISIONS INDEX (My Player Data). READ THE RELEVANT DEPARTMENT BEFORE PROPOSING OR CHANGING ANYTHING, and name the existing rule in the reply.
Agreed with the owner Nov 21, 2026, 6:47 PM. One line per decision: what, when, where it lives. A new request ADJUSTS what is here; it never silently replaces it. Add a line the moment a decision is made; add a lesson the moment a mistake is found.
Detail files: SCHEDULING.md (page and planner rules), LIVE_CHECK.md (weekend log, finals procedure, miss logs), WEEKEND_SOURCES.md (league table, search log), ROUNDUP_QUEUE.md; in /home/claude/player: build/IG_SLOT.md, IG_POSTING.md, IG_INBOX.md, IG_PLAYER_HANDLES.md, SALES.md, OWNER_CHECKLIST.md, member/NOTES.md.

## 1. RATINGS (how results go in and how changes show)
- Every tracked final goes into the ratings (Nov 20, 9:09 PM). Finals procedure: LIVE_CHECK.md / summary in SCHEDULING.md.
- Rating-change display: green/red change shown for teams that played since Wednesday; an idle team shows a change only when a team that played dropped below it; never for every idle team (Nov 20, 9:26 PM; build.py rd/rdIdle). The field-drift question is CLOSED (Nov 21, 6:37 PM): do not reopen unless the owner does.
- Drift check BEFORE publishing: idle teams moving more than 0.10 = stop. A game between a pool's pinned #1 and a team 7+ rating points below goes to data/held_games.json and is reported (Nov 22, 1:45 AM; two 2016 Little Caesars v Fox Motors games are held, owner to decide).
- Scores from a follower or a DM are never entered on their word: confirm on a scoring site, league/club site or the teams' Instagram first (Nov 21, 7:13 PM).
- Shootout win = one-goal win. MHR is the weekly anchor (Wednesday 1:15 AM) and the LAST place to look for weekend results. North American rank = USA and Canada together; country rank in parentheses.
- Members and the public never see how the numbers are calculated; no data sources shown except links to official scoresheets/event pages.

## 2. LIVE SCORES PAGE AND DESIGN
- Page order: Live now > Big games card > Games to watch > event sections > Other games > Final scores at the bottom (Nov 21, 4:39-4:58 PM; weekend.js).
- Big games = both top 10, or #1 v top 15; still-to-play only; listed once; dark card, gold border. NEVER a light background or a default-blue link on the dark theme (Nov 21, 4:54 PM and 11:41 PM): links use var(--blue).
- No outside links on game lists; tap opens our game page; official scoresheet link at the bottom of the game page. No Map links, no LiveBarn links (Nov 21, 11:29 PM).
- No leaders tables, no "Where the top 30 are", no "Events this weekend" card once in report form (Nov 21).
- Event sections: named for the EVENT, a small table (rows + rh) with rank in front and rating after every team, at most two short lines, no retelling of scores, no list of Sunday games (Nov 21, 11:29 PM; all years converted Nov 22, 12:25 AM). From Saturday night they report where the event stands and what is left.
- Sections update with EVERY final, all weekend (Nov 21, 11:35 and 11:42 PM): after each final search the sections for both teams and for lines that speak of a passed game as upcoming or unposted; re-read every section against the clock before a day's closing message. Work out the bracket from the OTHER teams' schedule pages; say when a team's event is over.
- Final scores list: ordered by rank, best-ranked team first; weekday small on each row; games with no score yet at the bottom (Nov 21, 11:41 PM).
- Games with no live scoresheet follow the clock: Live now from start time, "Finished, score not posted yet" after two hours (Nov 21, 5:20 PM).
- All times Central. Team weekend pages; birth-year tabs; goal-siren label while games are on.
- Every new link or button is clicked once in Chrome before it is called done (Nov 21, 10:30 PM).

## 3. RESEARCH (finding games and scores)
- Read the LEAGUE TABLE in WEEKEND_SOURCES.md first every Thursday. A league only has to be found once.
- For every game with no sheet: three GameSheet searches (home club, visiting club, their league), logged next to the game (Nov 21, 5:30 and 7:16 PM). A newly found source is opened and read immediately, before any Instagram or page work.
- GameSheet lists show about 20 rows: read big leagues one age division at a time (tools: __readDivs, league_import.py, missing.py).
- "Game sheet" means whatever scoring site the game is played under. Go to the event's own site, the home club's season, team sites, Instagram for schedules. Do not guess ids.
- Never read InStat through its internal interface; rendered pages only; never click the InStat page with the mouse. Never open an MHR rank page as page text.

## 4. MARKETING (Instagram and public copy)
- Slots: question 7:00 AM and 7:00 PM, answer 8:30 PM (IG_SLOT.md). Answers carry collaborator invites: exact unique name AND hockey picture; otherwise skip and give the handle to the owner. 5-game minimum for listed players.
- Game stories: rule A both teams NA top 30; B overtime/shootout with a top-30 team; C upset (10+ ranks apart, beaten team top 30); ranks before the game; else ROUNDUP_QUEUE. Scorers listed in the reply for phone-only mentions.
- Captions: no price, "Link in bio". Every Instagram link (stickers, bio) goes to https://myplayerdata.com/live/ (Nov 21, 9:01 PM). Sticker text "LIVE SCORES: TAP HERE" / "SEE THE FULL LIST".
- Never delete posts. No comment replies, likes or profile changes without asking. Inbox: send nothing without the owner's yes. No discount codes by DM.
- Explainers say what a stat MEANS, never the formula; invented numbers labelled "for illustration only"; opponents by rating, never "weak". Never say where player data comes from. Do not name MHR publicly. Motto: "We gather the data. You decide what it means."
- Volume follows follower growth; no Game of the Week segment for now (Nov 21, 3:03 PM).

## 5. SALES (SALES.md)
- Goal: most net revenue, whatever the mix of price and members (Nov 21, 9:25 PM). Daily sales check 9:10 PM; Monday business review.
- Free for now: Live Scores and all team ratings at /live/ (and the plain-text feed /live/feed/). Paid: the player database (Nov 21, 8:52 PM). If ratings are ever locked again, the feed comes down the same day.
- Price stays $19 first month then $79, season $349, until the numbers say otherwise; one change at a time. No emails to non-payers for now (Nov 21, 9:01 PM).
- Analytics page: revenue, renewals/at risk, what members use, people (duplicates grouped), sign-in code step, free page, funnel by source. Most-viewed players kept but folded away.

## 6. PLAYER DATABASE
- InStat sweeps Sunday, Monday, Tuesday and Thursday at 1:00 AM. InStat wins over GameSheet for player stats. Goalies by goals against only.
- Never put the database page, data or scripts in a public repo.

## 7. STANDING RULES
- Never enter passwords or secret keys; the owner types them. Never ask for them. No bank details. No accounts created on other sites.
- The owner's name stays off everything public; commits to the public repo as "My Player Data"; never reference the owner on the site; his son may be named like any other player. Never use the old nickname.
- Do it from this thread, in his browser, whenever possible. About 3-minute updates during long jobs. Real clock, Central time. Final reply of a scheduled run is the result, no meta, no site link at the end.
- Do not put work off to "the morning" (Nov 21, 11:54 PM): if work remains when a reply goes out, schedule the continuation at once and say so.
- Keep OWNER_CHECKLIST.md current.

## 8. LESSONS (why / fix / prevention live in the miss logs; one line each here)
- Read the code before proposing a site change (Nov 21, 4:36 PM). Check new colours on the dark theme (4:54 PM, 11:41 PM).
- Do not use the site's "rec" field as a game count (Nov 21, afternoon).
- Reopened a settled rating question: read this index first (6:37 PM).
- A league sat unread for hours after it was found: open new sources immediately; search by league, not only by club (7:16 PM).
- Free-page link went nowhere: click every new link (10:30 PM).
- Event section stale three hours after the final: sections update with every final (11:25 PM).
- Published before the drift check and lifted a whole birth year by 0.22: check before publishing; hold pinned-#1 blowouts (Nov 22, 1:45 AM).
- Nov 22 8:29 AM: live checks no longer message scores to the owner; page only, one-line reply (SCHEDULING.md, last section).
- Nov 22 8:50 AM: mistake log + prevention for 'live score not available' (SCHEDULING.md last section; tools/live_gaps.py runs in live_pub.sh).
- Nov 22 9:06 AM: owner restated: nothing about games in the chat; mistake log 2 (blank reads, sheet links, 'fixed' claims) in SCHEDULING.md.
- Nov 22 10:30 AM: research: data/TEAM_PAGES.md = club schedule pages, read Thursdays and game-day mornings (owner's method).
- Nov 22 11:29 AM: Live Scores UI: wide-screen score spacing, darker light background, bold team names in Live now (SCHEDULING.md last section).
- Nov 22 11:45 AM: event tables: result next to the team on wide screens (SCHEDULING.md UI section, item 4).
- Nov 22 11:47 AM: owner-sent stream link = 'Watch live now' button on that Live now row (SCHEDULING.md last section). No Map/LiveBarn rule unchanged.
- Nov 22 11:54 AM (owner): game page 'The teams' table: rank then rating in parentheses ('#2 (94.78)') instead of '#2, 94.78' which read like a money figure. Backup /tmp/weekend.js.bak8.
- Nov 22 11:58 AM: live game pages mirror the scoresheet (goals, scorers, periods) every cycle: MISTAKE LOG 3 in SCHEDULING.md.
- Nov 22 12:23 PM: player totals in section bullets are computed ({{pts:...}}), never typed; STALE RISK guard at every publish (MISTAKE LOG 4).
- Nov 22 3:27 PM: INSTAGRAM PAUSED (account disabled, appeal pending): no posts, stories, follows or Instagram pages until the owner says so (player/build/IG_SLOT.md).
- Nov 22 3:41 PM: never open Instagram in Chrome to read scores or find handles (likely trigger of the Nov 22 account disable); no automated follows (owner 3:36 PM).
- Nov 23, 8:37 AM: the owner handed day-to-day decisions to Claude ("your company to run"). What Claude decides alone, what still needs his yes, and the one-report-a-day shape: top of /home/claude/player/build/SALES.md. Separate Monday review switched off; the 9:10 PM report covers it.
- Nov 23, 8:36 PM: InStat sweep moved from 1:00 AM to 7:00 AM Central (Sunday 6:00 AM). Details and the timing study: /home/claude/player/data/NIGHTLY.md.
- OWNER, Nov 24 2026 9:00 PM: NO Tuesday-night reconcile. The official weekly ratings come out about 1 AM Wednesday, four hours later, with every adjustment already in them; the 1:15 AM Wednesday update takes those as the new base, so a Tuesday sweep is work that gets replaced the same night. Monday night's reconcile stays (Tuesday's Top 10 post rests on it). Do not schedule a Tuesday run again.
- OWNER, Nov 23 2026 11:42 PM: our team ratings ARE the outside weekly ratings done faster. Every game that will be in Wednesday's update must be in ours first: there should be no disconnect. Games entered late (Monday/Tuesday) count as weekend games, including ones dated Monday. So: reconcile our game log against the outside game lists Monday night (tools/mhr_top_check.md) [Tuesday evening run DROPPED by the owner Nov 24 9:00 PM, see next line], all ranked teams, not only the top; "last place to look" (line above) applies to LIVE scores only, not to completeness.
- Nov 24 2:06 PM: STORY RULE (loosened same day): up to 12 slides a day through Meta Business Suite only, 3 per sitting, sittings 1 hour apart, count Active stories first; sticker says PREVIEW until Thu Nov 26, then SCORES (player/build/SALES.md, STORY RULE RESET).
- Nov 24 4:31 PM: FREE PAGE OPENS ON 2013 for Silver Stick week (owner 4:22 PM): default birth year '2013' in build/build.py, index.html and site/members/ratings/index.html. Put '2012' back Mon Nov 30. Links can also open a year directly with #wk=YYYY.
- Nov 24 7:22 PM: SILVER STICK ON EVERY TEAM PAGE + PLAYERS TO WATCH (owner 7:19 PM: coverage good enough that people come here instead of the tournament's site). Team weekend pages of the 90 Silver Stick teams (2011, 2013, 2015) open with a Silver Stick card: four games (date, Central time, opponent with rank and rating, rink), the pool by rating, what it takes, the team's three players to watch, each opponent's top scorer (names link to the player database = the locked panel on the free page). Last weekend's games, recaps and sections stay BELOW it, headed "Last weekend". Weekend tab: "Silver Stick: players to watch" section (three a pool, 8+ games) right under the preview. Data: W['ss'] in weekend_public.json from tools/silverstick_team.py (rerun after the Wednesday ratings update and after any schedule change); card code in build/weekend.js renderTeamWk. NEXT for the event: pool tables with points, wins, goal share and the wildcard line on the Weekend tab and each team card; results flow into the card.
- OWNER, Nov 24 2026 10:04 PM: user feedback is "too much reading, almost like a school book report". He wants a quick, fast news report: sections, tables and lists, not long sentences. SAME information, less reading.
  DONE for Silver Stick (build/weekend.js, the block starting "const SSN="): one news card drawn from W.ss[year]: chips (30 teams, 6 pools, 8 advance...), How it works (label | short fact), The draw (hardest pool, easiest road,
  wildcard edge, no favorite, not here), Pools (six small tables, rank + team + rating, tap a team), Games to circle (time | matchup | pool), Players to watch (table with GP G A PTS). Ranks and ratings are read live, so nothing goes stale.
  The two text sections ("International Silver Stick preview", "Silver Stick: players to watch") stay in weekend_public.json (team pages and checks read them) but are NOT drawn on the Weekend tab when W.ss[year] exists.
  RULE FOR EVERY EVENT FROM NOW ON: facts go in tables or label | fact rows; one line per item; no paragraph bullets. When results start, the pool tables become standings (W L T PTS GF GA) in the same card.
- OWNER, Nov 25 2026 2:29 AM: after the Wednesday update the official page is the truth. Do NOT re-verify last week's scores and do NOT run the top-25 game-by-game math check: whatever the official pages show is the new base, last week's scores no longer matter.
  The Wednesday routine is now: lists in, checksums match, baseline equals the published ratings, publish. (The stored Wednesday task text still lists the old steps 4 and 5: skip them.)
- OWNER, Nov 25 2026 2:29 AM: tournament game sheets are found through gamesheetinc.com search (Scores & Stats), then Game Status = All. Look there FIRST for any event, before waiting for a tournament site to post a link.
- Nov 26: Instagram collaborator invites back on for SAVED handles only, in Meta's composer, 2-3 per post; owner finds new handles and sends them (player/build/IG_POSTING.md, last section).
- Nov 26: Helper Desk (Grok) for mail reading, weekend score research, event scouting: player/build/HELPER_DESK.md. Scores are a trial; Claude verifies before import.
- Nov 26: top bar = Game Day | Ratings | Players (site/nav.js; app not changed). player/member/NOTES.md last section.
- Nov 26: Instagram lists: no power-play time category; skip any list with 3+ of the top five from one team (player/build/ig_make.py pick_question).
- Nov 26 8:17 AM: owner allows tags and collaborator invites on instagram.com again, human pace only (limits in player/build/IG_POSTING.md, last section).
- Nov 26 8:41 AM: tournament scoring leaderboards (plain + adjusted) and road difficulty ARE shown on the live event card (reverses the Nov 21 no-leaders rule for events covered live only). data/weekend_nov26.txt top.
