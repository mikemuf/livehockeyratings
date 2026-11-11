# python3 merge_pp.py pp.json -> adds per-game power-play time, goals and assists to stored games in box.json
# pp.json: {match id: "TeamA^TeamB^side,num,ppSeconds,ppGoals,ppAssists;..."}  ('x' = page has no table, '?' = not read)
import json,sys
D=json.load(open('box.json')); R=json.load(open(sys.argv[1])); ok=bad=empty=0; odd=[]
for m in D['M']:
    r=R.get(m['id'])
    if r is None or r=='?': bad+=1; continue
    if r=='x': m['PP']={}; empty+=1; continue
    parts=r.split('^'); names=[x.upper() for x in parts[:-1]]; rows=[x for x in parts[-1].split(';') if x]
    idx=[m['S'].index(n) if n in m['S'] else i for i,n in enumerate(names)]
    pp={}
    for x in rows:
        s,num,t,g,a=x.split(','); k=f"{idx[int(s)] if int(s)<len(idx) else int(s)}|{num}"
        if k not in pp: pp[k]=[int(t),int(g),int(a)]
    # sanity: power-play time can never exceed the player's total time in that game
    toi={p.split('|')[0]+'|'+p.split('|')[1]:int(p.split('|')[4]) for p in m['P']}
    if any(k in toi and v[0]>toi[k]+5 for k,v in pp.items()): odd.append(m['id'])
    m['PP']=pp; ok+=1
json.dump(D,open('box.json','w'),separators=(',',':'))
print('games with PP data',ok,'| no table',empty,'| not read',bad,'| PP time exceeds total time in',len(odd),odd[:10])
