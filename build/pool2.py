# 2014 (USA 12U) + 2015 (USA 11U): one MHR pool (top 12U = 99.99), built like 2012/2013:
# full game logs from the top-40 teams' Rating Math pages (data/math1?u_nov4.txt) + anchors from the
# Nov 4 rank files; opponents seen only on math pages are anchored to the rating shown there.
import re
TIER=re.compile(r' (12U|11U|U13|U12|M13|M12)\b(.*)$')
def node(full):
    m=TIER.search(full)
    if not m: return None
    age,rest=m.group(1),m.group(2).strip()
    dv='2014' if age in ('12U','U13','M13') else '2015'
    if rest=='AAA': nm=full[:m.start()]
    else: nm=full
    return dv,nm,age in ('U13','U12','M13','M12')
def load_rank(fn,skip):
    out={}
    for line in open(fn):
        p=line.strip().split('|')
        if len(p)<5 or skip in p[0]: continue
        w,l,t=map(int,p[1].split('-'));out[p[0]]=(float(p[2]),w+l+t,p[1])
    return out
def build():
    games={};ratings={};canada=set();xmap={'2014':{},'2015':{}}
    for fn in ('data/math11u_nov4.txt','data/math12u_nov4.txt'):
        try: L=open(fn).read().split('\nG\n')
        except FileNotFoundError: continue
        names={}
        for line in L[0].split('\n')[1:]:
            i,n,r=line.split('|');names[int(i)]=(n,float(r) if r else None)
        loc={}
        for g in L[1].strip().split(';'):
            a,b,md,ga,gb=g.split(',');A=node(names[int(a)][0]);B=node(names[int(b)][0])
            if not A or not B: continue
            for X,(full,r) in ((A,names[int(a)]),(B,names[int(b)])):
                if r is not None: ratings[(X[0],X[1])]=r
                if X[2]: canada.add(X[1])
            ka,kb=(A[0],A[1],int(ga)),(B[0],B[1],int(gb))
            k=('2026-%s-%s'%(md[:2],md[2:]),)+tuple(sorted([ka,kb]))
            loc[k]=loc.get(k,0)+1
        for k,c in loc.items(): games[k]=max(games.get(k,0),c)
    out=[]
    for k,c in games.items():
        dt,(da,na,sa),(db,nb,sb)=k[0],k[1],k[2]
        if db!=da:
            al=nb+(' (12U)' if db=='2014' else ' (11U)'); xmap[da][al]=db+'|'+nb; nb=al
        for _ in range(c): out.append([da,dt,na,sa,nb,sb])
    r12=load_rank('data/nov04_usa12.txt','11U');r11=load_rank('data/nov04_usa11.txt','12U')
    M={'2014':{},'2015':{}};G={'2014':{},'2015':{}};R={'2014':{},'2015':{}}
    for dv,rk in (('2014',r12),('2015',r11)):
        for n,(r,gp,rec) in rk.items(): M[dv][n]=r;G[dv][n]=gp;R[dv][n]=rec
    for (dv,n),r in ratings.items():
        if n not in M[dv]:
            M[dv][n]=r
            if n not in canada: G[dv][n]=0;R[dv][n]='0-0-0'
    return out,xmap,M,G,R,sorted(canada)
