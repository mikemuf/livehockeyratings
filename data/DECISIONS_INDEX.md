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
