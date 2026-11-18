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
