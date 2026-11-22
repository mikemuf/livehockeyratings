#!/usr/bin/env python3
# tools/live_gaps.py : games the Live Scores page shows RIGHT NOW as "IN PROGRESS · live score not available"
# (today's watch-list games that have started within the last 2 hours and have neither a live box line nor a final).
# Run by tools/live_pub.sh after every publish. Built Nov 22, 2026 after 90 minutes of live games showed no score
# because the checks read the scores but never imported them. Every row printed here needs either an import
# (build/gs_import.py) or, if the game truly has no live source, nothing: but look at each one.
import json,datetime,zoneinfo
now=datetime.datetime.now(zoneinfo.ZoneInfo('America/Chicago'))
day=now.strftime('%a'); iso=now.strftime('%Y-%m-%d')
W=json.load(open('data/weekend_public.json')); P=json.load(open('data/pending_games.json')); B=json.load(open('data/gs_box.json'))
B=[dict(v,div=k.split('|')[0]) for k,v in B.items()]
n=0
for y,d in W['divs'].items():
    for g in d.get('watch',[]):
        if g.get('day')!=day or not g.get('time'): continue
        try: t=datetime.datetime.strptime(iso+' '+g['time'],'%Y-%m-%d %I:%M %p').replace(tzinfo=now.tzinfo)
        except Exception: continue
        mins=(now-t).total_seconds()/60
        if mins<0 or mins>120: continue
        pr={g.get('a'),g.get('b')}
        if any(p[0]==y and p[1]==iso and {p[2],p[4]}==pr for p in P): continue
        if any(str(x.get('div'))==y and x.get('date')==iso and {x.get('v'),x.get('h')}==pr for x in B): continue
        n+=1; print('NO LIVE SCORE ON PAGE:',y,g['time'],g.get('a'),'v',g.get('b'),'|',g.get('note','')[:30],'| sheet' if g.get('sheet') else '| no sheet link')
print('live gaps',n)

# STALE-TEXT GUARD (owner, Nov 22 2026 12:23 PM): hand-typed player totals or "first N games" in section bullets go stale. Flag them at every publish.
try:
    import json as _j, re as _r
    _w=_j.load(open('/home/claude/livehockeyratings/data/weekend_public.json'))
    for _d,_D in (_w.get('divs') or {}).items():
        for _s in _D.get('sections',[]):
            for _b in _s.get('b',[]):
                if '{{pts:' in _b: continue
                if _r.search(r'\b(first|last|through|in (his|her|their))\s+(\w+\s+)?(one|two|three|four|five|six|\d+)\s+games?\b|\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+) (goals?|assists?|points?)\b',_b,_r.I):
                    print('STALE RISK (use {{pts:Player|Team|date}} or reword):',_d,'|',_s.get('t'),'|',_b[:110])
except Exception as _e: print('stale guard error',_e)
