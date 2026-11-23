# Same-day second games (doubleheaders) in 2012/2013: build.py drops a pending game whose (division, date, pair) is already present unless it has a 7th element.
# This marks the later one(s) 'dh' when the scores differ, so both count. Run by tools/live_pub.sh before every build. (Mistake log, Nov 22 2026.)
import json,collections
P=json.load(open('data/pending_games.json')); seen=collections.defaultdict(list); n=0
for g in P:
    if g[0] not in ('2012','2013'): continue
    k=(g[0],g[1],frozenset((g[2],g[4])))
    if seen[k] and len(g)<7 and all(g[:6]!=x[:6] for x in seen[k]): g.append('dh'); n+=1; print('DOUBLEHEADER marked:',g)
    seen[k].append(g)
if n: json.dump(P,open('data/pending_games.json','w'))
