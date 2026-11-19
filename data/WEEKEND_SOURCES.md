# Where weekend schedules come from (keep this current; add every source that proves reliable)

Goal (the owner, Nov 17 2026): the Weekend tab is the one place a parent looks: who plays whom, which tournaments, matchups to watch, rink, map, LiveBarn, standings and the story so far. All six birth years, 2011 to 2016.

## 1. League and tournament GameSheet pages (best: schedule, results, standings, scorers, goalies in one place)
- Northeast Pack: gamesheetstats.com/seasons/15483 (2026/27). Division filter ids: 14U (2012) 83550, 15O (2011) 83551. Pages: /standings, /schedule, /scores, /players, /goalies (add ?filter[division]=ID). The games list is virtualized: scroll in steps and collect rows. League site: nepackhockey.com/schedules (links the GameSheet season and a PDF per showcase).
- For any other league or tournament, find its GameSheet season id from the event's own site and use the same pages.

## 2. MyHockeyRankings team schedules (tools/mhr_sched.js)
- Covers the top N teams of a rank page in about 2 minutes per birth year. Dump for Nov 20-22 is in data/sched_nov20_mhr.txt.
- Limit: only what teams have posted. On Tue Nov 17 about half of the top 25 in each birth year had nothing posted for the coming weekend, including Bishop Kearney and Pens Elite, who were known to be playing (NE Pack). Treat "nothing posted" as unknown, not as "not playing". Re-run Thursday and Friday; more games appear late in the week.
- "**" marks a tournament game and shows the rink, which identifies the event (e.g. eight 2014 teams at Centene Community Ice Center, St. Louis, Nov 20-21).

## 3. Still to try (not yet proven)
- Team and club websites with their own schedules (the owner's suggestion: chicagofury.com, Mid-Fairfield, etc.) for top teams that post nothing on MHR.
- Tournament and league sites: Tier 1 Hockey Federation (tier1hockeyfederation.com showcases), T1EHL, HPHL, EHF, AYHL, International Silver Stick (Whitby, US Thanksgiving weekend: 2011, 2013 and 2015 fields per the owner).
- Instagram weekend-preview accounts (the owner's suggestion). Not attempted.
- MHR's own weekend preview article (usually published late in the week).

## Writing rules
See the preferences in data/weekend_nov6.txt and weekend_nov20.txt: lead with the main event, rank and rating in parentheses, head-to-head from earlier this season, goalies by goals against only, never mention the owner.

## Ontario (owner, Nov 19, 2026: cover Canada too, a carousel per birth year)
- MHR Ontario rank pages for tools/mhr_sched.js: U16 (2011) v=137, U15 (2012) v=136, U14 (2013) v=135; U13 (2014) and U12 (2015) are probably v=134 and v=133 (check the page title), U11 (2016) v=132. Times on MHR are local (Eastern); subtract one hour for Central.
- Limit found Nov 19: the GTHL clubs (Marlboros, Jr Canadiens, Vaughan Kings, North York, Titans, Rebels) post almost nothing ahead of time below U16. On Nov 19 the U15 and U14 top three had nothing posted. STILL NEEDED: the GTHL's own schedule (gthlcanada.com game centre), OMHA ETA, ALLIANCE and HEO schedule pages. Find them, record the exact pages here, and build the Ontario sections for 2012-2015 from them.

## GTHL schedule and scores (found Nov 19, 2026): the source for the Toronto clubs at every age
- Page: gthlcanada.com/schedule/ shows a framed schedule from agilex.ca (SSP/schedules.aspx?event=187). Opening the agilex address directly says "The requested URL is invalid"; it only loads when reached FROM the GTHL page. In Chrome: open gthlcanada.com/schedule/, then run `const s=document.querySelector('iframe[src*=agilex]').src;const a=document.createElement('a');a.href=s;document.body.appendChild(a);a.click()` so the schedule opens as the top page with the right referrer.
- Then by script: set `ddlDiv` (U10..U18; U16=2011, U15=2012, U14=2013, U13=2014, U12=2015, U11=2016), `ddlCat`='A3' (AAA), `dpFrom`/`dpTo` like '20-Nov-2026', click `sche_btnSearch`, wait 5 s, read the table rows. Columns: date, time (Eastern), Away : Home (score appears between them once played), arena, type (LG = league). About 30 seconds for all five ages.
- The same page shows final scores, so it is also the results source for GTHL games on game day.
- Names differ from ours: "Jr. Canadiens" = Toronto Jr Canadiens, "Toronto Young Nationals" = Toronto Nationals, "Reps Hockey Club" = Toronto Reps.
- Dump for Nov 20-22: data/sched_nov20_gthl.txt.
- Still to find: OMHA ETA (York Simcoe, Whitby, Quinte, Barrie...), ALLIANCE (Huron-Perth, Waterloo, Chatham-Kent, Elgin Middlesex...), HEO (Ottawa), NOHA schedule pages.

## Owner's method for finding events (Nov 19, 2026)
If two teams from different cities are playing each other in a third city (a Toronto team against a Pittsburgh team in Detroit), there is an event in that city: look for it. Then search GameSheet for it. GameSheet has schedules, scores, standings and scorers, but tournament names are typed by people and change from year to year, so search by city, rink, date and team names as well as by the event name. Record every event found in EVENTS.md with its GameSheet season id.
