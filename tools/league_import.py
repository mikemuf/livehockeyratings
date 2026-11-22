#!/usr/bin/env python3
# tools/league_import.py <file> [--write]   lines: AGE~day(20/21/22 of the current month)~visitor~vs-hs~home~OT
# Maps league team names to ratings names (unique substring match on the club's key word), skips games already in pending_games.json
# (same year, date, pair AND score), prints what it would add and anything it could not resolve. Ontario leagues: U16=2011 ... U11=2016.
import json,sys,re
AGE={'U16':'2011','U15':'2012','U14':'2013','U13':'2014','U12':'2015','U11':'2016'}
KEY={'greater kingston':'kingston','u15 north shore':'north shore whitecaps','north shore w':'north shore whitecaps','york-simcoe':'york simcoe','grey-bruce':'grey bruce','ajax-pickering':'ajax','elgin-middlesex':'elgin','huron-perth':'huron','chatham-kent':'chatham','sarnia-lambton':'sarnia','soo jr':'soo','london jr':'london jr','kitchener jr':'kitchener','windsor jr':'windsor','peterborough':'peterborough','whitby wildcats aaa':'whitby'}
R=json.load(open('/tmp/r_new.json')); P=json.load(open('data/pending_games.json')); YM='2026-11-'
def find(y,n):
    k=n.lower().strip()
    for a,b in KEY.items():
        if k.startswith(a) or a in k: k=b; break
    else: k=' '.join(k.replace('-',' ').split()[:2])
    c=[t for t in R[y] if k in t.lower().replace('-',' ')]
    if len(c)>1:
        e=[t for t in c if '(a)' not in t.lower() and ' aa' not in t.lower()]
        c=e if len(e)==1 else c
    return c
add=[];bad=[];dup=0
for ln in open(sys.argv[1]):
    ln=ln.strip()
    if not ln: continue
    age,day,v,sc,h,ot=(ln.split('~')+[''])[:6]; y=AGE[age]; vs,hs=map(int,sc.split('-'))
    cv,ch=find(y,v),find(y,h)
    if len(cv)!=1 or len(ch)!=1: bad.append((ln,cv[:3],ch[:3])); continue
    V,H=cv[0],ch[0]; d=YM+day
    if vs>=hs: g=[y,d,V,vs,H,hs]
    else: g=[y,d,H,hs,V,vs]
    if any(x[0]==y and x[1]==d and {x[2],x[4]}=={V,H} and sorted([x[3],x[5]])==sorted([vs,hs]) for x in P+add): dup+=1; continue
    add.append(g)
print('new',len(add),'already in',dup,'unresolved',len(bad))
for b in bad: print('  UNRESOLVED',b)
for g in add: print('  +',g[0],g[1],'#%s'%R[g[0]][g[2]].get('na'),g[2],g[3],'#%s'%R[g[0]][g[4]].get('na'),g[4],g[5])
if '--write' in sys.argv:
    json.dump(P+add,open('data/pending_games.json','w')); json.dump(add,open('/tmp/league_added.json','w')); print('written')
