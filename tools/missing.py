#!/usr/bin/env python3
# tools/missing.py : watch-list games (Fri/Sat/Sun already started) with no result in pending_games.json
import json,datetime
W=json.load(open('data/weekend_public.json')); P=json.load(open('data/pending_games.json')); r=json.load(open('/tmp/r_new.json'))
dm={'Thu':'2026-11-19','Fri':'2026-11-20','Sat':'2026-11-21'}
n=0
for y,d in W['divs'].items():
    for g in d.get('watch',[]):
        if g.get('day') not in dm: continue
        a,b=g.get('a'),g.get('b')
        have=sum(1 for p in P if p[0]==y and p[1]==dm[g['day']] and {p[2],p[4]}=={a,b})
        same=sum(1 for h in d['watch'] if h.get('day')==g['day'] and {h.get('a'),h.get('b')}=={a,b})
        if have<same:
            n+=1; print(y,g['day'],g.get('time'),'#%s'%r[y].get(a,{}).get('na','?'),a,'v','#%s'%r[y].get(b,{}).get('na','?'),b,'|',g.get('rink','')[:26],'|',g.get('note','')[:20])
print('missing',n)
