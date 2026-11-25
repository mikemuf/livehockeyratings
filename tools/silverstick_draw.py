"""Silver Stick preview: 'how teams advance' and 'the draw' bullets (owner, Nov 24 2026 6:50 PM: read the tournament rules and show
parents how hard some pools are next to others). Rules read from the tournament's own 2026 rules page (data/WEEKEND_SOURCES.md).
  node /home/claude/player/build/ratings_from_site.js index.html /tmp/r_new.json ; python3 tools/silverstick_draw.py ; tools/live_pub.sh "..."
Replaces the Wildcards / Toughest pool bullets in each 'Next: International Silver Stick' section and puts that section first."""
import json,re
R=json.load(open('/tmp/r_new.json')); SS=json.load(open('data/silverstick_2026.json')); MP=json.load(open('data/silverstick_2026_names.json'))
W=json.load(open('data/weekend_public.json'))
def info(y,t):
    n=MP.get(f'{y}|{t}'); d=R[y].get(n) if n else None
    disp=re.sub(r' \((Elite|Mueller)\)$','',n) if n else t
    disp={'Mid-Fairfield Hockey Club':'Mid-Fairfield','Middlesex Islanders East':'Middlesex Islanders'}.get(disp,disp)
    return disp,(d['na'] if d else None)
def lab(y,t):
    n,k=info(y,t); return f"#{k} {n}" if k else n+' (not rated)'
def draw(y):
    pools=SS[y]['pools']; rk={t:(info(y,t)[1] or 999) for ts in pools.values() for t in ts}
    S={p:sorted(ts,key=lambda t:rk[t]) for p,ts in pools.items()}
    n20=lambda p:sum(rk[t]<=20 for t in S[p])
    b=["How teams advance: only 8 of the 30 teams reach the quarterfinals. The six pool winners are seeded 1 to 6 and the two best second-place teams get in as wildcards, seeded 7 and 8.",
       "Wildcards and ties: points first, then head-to-head where the teams met, then most wins, then share of goals scored (goals for divided by goals for plus goals against), then fewest goals against. There is no overtime in pool play, so a tie is one point each and every goal counts.",
       "Quarterfinals: the best record plays the worst, and two teams from the same pool cannot meet again until the final."]
    hard=max(S,key=lambda p:(n20(p),-sum(rk[t] for t in S[p][:3])))
    b.append(f"Hardest pool: Pool {hard} has {n20(hard)} of the top 20 in North America ("+', '.join(lab(y,t) for t in S[hard] if rk[t]<=20)+") and one automatic spot.")
    easy=max(S,key=lambda p:rk[S[p][1]]-rk[S[p][0]] if rk[S[p][0]]<=10 else -1)
    b.append(f"Easiest road: {lab(y,S[easy][0])} in Pool {easy}. The next-best team in its pool is {lab(y,S[easy][1])}.")
    for p in S:
        if rk[S[p][1]]<=10 and rk[S[p][2]]>=40:
            g=[g for g in SS[y]['games'] if {g['a'],g['b']}=={S[p][0],S[p][1]}]
            when=f" They meet {g[0]['day']} at {g[0]['ct']} Central." if g else ''
            b.append(f"Wildcard edge: Pool {p} has two of the top 10, {lab(y,S[p][0])} and {lab(y,S[p][1])}, and nobody else in the top {rk[S[p][2]]-1}.{when} The loser can still stack points against the rest of the pool, and points are what decide the wildcards.")
    for p in S:
        if rk[S[p][0]]>10 and n20(p)>=3:
            b.append(f"No favorite: Pool {p} has no top-10 team but {n20(p)} of the top 20 ("+', '.join(lab(y,t) for t in S[p] if rk[t]<=20)+"). They take points off each other, which makes a wildcard from this pool harder to come by.")
    return b
for y in SS:
    d=W['divs'][y]; sec=[s for s in d['sections'] if 'International Silver Stick' in s['t']]
    assert len(sec)==1, y
    s=sec[0]; keep=[x for x in s['b'] if not re.match(r'(Wildcards:|Toughest pool:|How teams advance:|Wildcards and ties:|Quarterfinals:|Hardest pool:|Easiest road:|Wildcard edge:|No favorite:)',x)]
    i=next(k for k,x in enumerate(keep) if x.startswith('Format:'))+1
    nb=draw(y); adv=nb[:3]; drw=nb[3:]
    j=next((k for k,x in enumerate(keep) if x.startswith('Games to circle:')),len(keep))
    s['b']=keep[:i]+adv+keep[i:j]+drw+keep[j:]
    # Nov 24 2026 10 PM: the Pool lines, "The field" and "Not in the field" were written once and went stale when ranks moved (page said #14 Mission while the team page said #15). Rebuilt from the ratings every run.
    pools=SS[y]['pools']; rk={t:(info(y,t)[1] or 999) for ts in pools.values() for t in ts}
    def rat(t):
        n=MP.get(f'{y}|{t}'); d0=R[y].get(n) if n else None
        return f" ({d0['rating']:.2f})" if d0 and d0.get('rating') else ''
    pl={p:f"Pool {p}: "+', '.join(lab(y,t)+rat(t) for t in sorted(ts,key=lambda t:rk[t]))+'.' for p,ts in pools.items()}
    inn=sorted((k,t) for t,k in rk.items() if k<=10); names_in={MP.get(f'{y}|{t}') for t in rk}
    out=sorted((d0['na'],n) for n,d0 in R[y].items() if d0.get('na') and d0['na']<=10 and n not in names_in)
    cl=lambda n:{'Mid-Fairfield Hockey Club':'Mid-Fairfield','Middlesex Islanders East':'Middlesex Islanders'}.get(re.sub(r' \((Elite|Mueller)\)$','',n),re.sub(r' \((Elite|Mueller)\)$','',n))
    nb2=[]
    for x in s['b']:
        m=re.match(r'Pool ([A-F]): ',x)
        if m: x=pl[m.group(1)]
        elif x.startswith('The field:'): x=f"The field: 30 teams in six pools of five. {len(inn)} of the top 10 in North America and {sum(k<=30 for k in rk.values())} of the top 30 are entered: "+', '.join(lab(y,t) for k,t in inn)+'.'
        elif x.startswith('Not in the field:') and out: x='Not in the field: '+', '.join(f'#{k} {cl(n)}' for k,n in out)+'.'
        nb2.append(x)
    s['b']=nb2
    s['t']='International Silver Stick preview, Nov 26–29 (Whitby, Ontario)'
    d['sections']=[s]+[x for x in d['sections'] if x is not s]
    print('=====',y); [print(' -',x) for x in s['b'] if not x.startswith('Pool ')]
json.dump(W,open('data/weekend_public.json','w'),indent=1,ensure_ascii=False)
