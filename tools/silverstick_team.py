"""Silver Stick data for the TEAM weekend pages and the 'Players to watch' section (owner, Nov 24 2026 7:19 PM: every team page shows
its Silver Stick pool and schedule, last weekend's report stays below; players to watch on the Weekend tab).
  node /home/claude/player/build/ratings_from_site.js index.html /tmp/r_new.json ; python3 tools/silverstick_team.py ; tools/live_pub.sh "..."
Writes weekend_public.json: W['ss'][year] = {pools:{A:[rating names]}, games:[{p,day,date,ct,sort,rink,a,b}], ptw:{team:[[name,g,a,gp],..3]}}
and a 'Silver Stick: players to watch' section (second section) on each Silver Stick birth year.
Players: skaters with 5+ games on record, by points a game (player/data/db.json), three a team on team pages, three a pool in the section."""
import json,re,collections
R=json.load(open('/tmp/r_new.json')); SS=json.load(open('data/silverstick_2026.json')); MP=json.load(open('data/silverstick_2026_names.json'))
W=json.load(open('data/weekend_public.json'))
db=json.load(open('/home/claude/player/data/db.json')); T=json.load(open('/home/claude/player/data/teams.json'))
key={(str(v['yr']),v['name']):k for k,v in T.items()}
byteam=collections.defaultdict(list)
for s in db['S']: byteam[s[0]].append(s)
RINK={'Iroq':'Iroquois Park Sports Centre, Rink %s, Whitby','McK':'McKinney Centre, Rink %s, Whitby','Field':'Fieldgate Sports Complex, Rink %s','Can':'Canlan Ice Sports, Rink %s, Oshawa'}
def rink(r):
    if r=='THCC-W': return 'Thornhill Community Centre (West), Markham'
    m=re.match(r'([A-Za-z]+)#?(\d)$',r); return RINK[m.group(1)]%m.group(2) if m and m.group(1) in RINK else r
DATE={'Thu':'2026-11-26','Fri':'2026-11-27','Sat':'2026-11-28','Sun':'2026-11-29'}
W['ss']={}
for y in SS:
    nm=lambda t:MP.get(f'{y}|{t}') or t
    pools={p:[nm(t) for t in ts] for p,ts in SS[y]['pools'].items()}
    games=[{'p':g['pool'],'day':g['day'],'date':DATE[g['day']],'ct':g['ct'],'sort':g['sort'],'rink':rink(g['rink']),'a':nm(g['a']),'b':nm(g['b'])} for g in SS[y]['games']]
    ptw={}
    for ts in pools.values():
        for t in ts:
            k=key.get((y,t)); sk=sorted([s for s in byteam.get(k,[]) if s[5]>=5 and s[3]!='G'],key=lambda s:-s[8]/s[5])[:3]
            if sk: ptw[t]=[[s[2],s[6],s[7],s[5]] for s in sk]
    try:
        _gs=json.load(open('data/silverstick_2026_gs.json'))['games']; _bk={(x['y'],x['k']):gid for gid,x in _gs.items()}
        for _k,_g in enumerate(games): _g['gs']=_bk.get((y,_k),'')
    except FileNotFoundError: pass
    W['ss'][y]={'pools':pools,'games':games,'ptw':ptw}
    # Nov 24 2026 10:10 PM (owner: "too much reading, like a school book report"): the Weekend tab now draws Silver Stick as a news card with tables
    # (build/weekend.js ssNews) from this data. circle = the games-to-circle pairs (rating names), watch = three scorers a pool, 8+ games.
    short=lambda n:{'Mid-Fairfield Hockey Club':'Mid-Fairfield','Middlesex Islanders East':'Middlesex Islanders'}.get(re.sub(r' \((Elite|Mueller)\)$','',n),re.sub(r' \((Elite|Mueller)\)$','',n))
    rev={short(t):t for ts in pools.values() for t in ts}
    circ=[]
    for sc in W['divs'][y]['sections']:
        if 'International Silver Stick' in sc['t']:
            for x in sc['b']:
                if x.startswith('Games to circle:'):
                    for m in re.finditer(r'(?:#\d+ )?([^;#]+?) against (?:#\d+ )?([^;#,]+?), (?:Thu|Fri|Sat|Sun)',x[16:]):
                        a,b2=rev.get(m.group(1).strip()),rev.get(m.group(2).strip())
                        if a and b2: circ.append([a,b2])
    W['ss'][y]['circle']=circ
    W['ss'][y]['watch']={p:[[v[0],t,v[1],v[2],v[3]] for _,v,t in sorted([((v[1]+v[2])/v[3],v,t) for t in ts for v in [x for x in ptw.get(t,[]) if x[3]>=8][:2]],key=lambda x:-x[0])[:3]] for p,ts in pools.items()}
    lab=lambda t:(f"{t} (#{R[y][t]['na']}, {R[y][t]['rating']:.2f})" if t in R[y] and R[y][t].get('na') else t)
    b=["The top scorers coming to Whitby in each pool, by points a game this season (eight or more games on record)."]
    for p,ts in pools.items():
        cand=sorted([(v[1]+v[2])/v[3] and ((v[1]+v[2])/v[3],v,t) for t in ts for v in [x for x in ptw.get(t,[]) if x[3]>=8][:2]],key=lambda x:-x[0])[:3]
        if cand: b.append(f"Pool {p}: "+'; '.join(f"{v[0]}, {lab(t)}: {v[1]} goal{'' if v[1]==1 else 's'} and {v[2]} assist{'' if v[2]==1 else 's'} in {v[3]} games" for _,v,t in cand)+'.')
    b.append("Open any team's page for its pool, its four games and its own players to watch.")
    d=W['divs'][y]; d['sections']=[s for s in d['sections'] if s['t']!='Silver Stick: players to watch']
    i=1 if d['sections'] and 'International Silver Stick' in d['sections'][0]['t'] else 0
    d['sections'].insert(i,{'t':'Silver Stick: players to watch','b':b})
    print(y,len(games),'games',len(ptw),'teams with players'); [print('  -',x[:230]) for x in b[:3]]
json.dump(W,open('data/weekend_public.json','w'),indent=1,ensure_ascii=False)
