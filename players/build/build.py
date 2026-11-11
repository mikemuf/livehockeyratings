import json,re,sys,glob,collections
from match import norm,agetag
R=json.load(open('ratings.json'))
D=json.load(open('box.json'))
W=json.load(open('wanted.json'))
ALIAS=json.load(open('alias.json'))
BORN={"1315186":2013,"1226025":2013,"1265803":2013}
# wanted team info
# Team list is frozen (teams.json). Ratings and ranks come from the current ratings file.
INFO={}; MISSING=[]
for key,t in json.load(open('teams.json')).items():
    r=R[str(t['yr'])].get(t['name'])
    if r: INFO[key]=dict(yr=t['yr'],rank=r['rank'] or 0,name=t['name'],rating=r['rating'],pool=t['pool'])
    else: INFO[key]=dict(yr=t['yr'],rank=0,name=t['name'],rating=t['rating'],pool=t['pool']); MISSING.append(key+' '+t['name'])
E2K={i:k for k,v in W.items() for i in v}
RN={y:{norm(k):k for k in R[y]} for y in R}
def rate(opp,yr,oid):
    yr=str(yr)
    if oid in E2K and INFO[E2K[oid]]['yr']==int(yr): return INFO[E2K[oid]]['name']
    if opp in ALIAS: return ALIAS[opp] if ALIAS[opp] in R[yr] else None
    tag=agetag(opp); us_ok={'2012':14,'2013':13}[yr]; key=norm(opp); cand=RN[yr].get(key)
    if not cand:
        best=None
        for k,v in RN[yr].items():
            if key and (key<=k or k<=key) and len(key&k)>=2:
                sc=len(key&k)/len(key|k)
                if not best or sc>best[0]: best=(sc,v)
        if best and best[0]>=0.6: cand=best[1]
    if not cand: return None
    pool=R[yr][cand]['pool']
    if tag and tag!=(us_ok if pool=='USA' else us_ok+1): return None
    return cand
TG={t['id']:t for t in D['T']}
S=[];G=[];GAMES={};LOGS={};GLOG={};GNUM={};report=[];unm=collections.Counter()
for key,info in INFO.items():
    ids=set(W.get(key,[])); yr=info['yr']
    games={}  # gkey -> dict
    for m in D['M']:
        tl=[x.split('=',1) for x in m['tl']]
        for side,(tid,tname) in enumerate(tl):
            if tid not in ids: continue
            h=m['h'].split('~'); date=h[0]; sc=h[2].replace(' ','').split(':')
            si=m['S'].index(tname.upper()) if tname.upper() in m['S'] else side
            mysc=(sc[0],sc[1]) if side==0 else (sc[1],sc[0])
            oid,oname=tl[1-side]
            rows=[p.split('|') for p in m['P'] if int(p.split('|')[0])==si and not re.search('noname',p,re.I)]
            gk=(date[3:5]+'-'+date[:2],norm(oname),mysc)
            g=dict(pp=m.get('PP') or {},date=date[3:5]+'-'+date[:2],ha='h' if side==0 else 'a',oid=oid,oname=oname,score=mysc[0]+':'+mysc[1],rows=rows,mo=int(date[3:5]))
            if gk not in games or len(rows)>len(games[gk]['rows']): games[gk]=g
    if not games: GAMES[key]=[]; continue
    # regulars filter
    cnt=collections.Counter(r[9] for g in games.values() for r in g['rows'] if r[3]!='GK')
    ng=len(games); reg={p for p,c in cnt.items() if c>=max(2,0.3*ng)} if ng>=4 else set(cnt)
    gl=[g for g in games.values() if ng<4 or sum(1 for r in g['rows'] if r[9] in reg)>=4]
    gl.sort(key=lambda g:((g['mo']-8)%12,g['date'],g['oname']))
    GL=[]
    for g in gl:
        rn=rate(g['oname'],yr,g['oid'])
        if rn: rr=R[str(yr)][rn]; GL.append([g['date'],g['ha'],rn,rr['rating'],rr['rank'] or 0,1 if rr['pool']=='Canada' else 0,g['score']])
        else: unm[g['oname']+f' [{yr}]']+=1; GL.append([g['date'],g['ha'],g['oname'],0,0,0,g['score']])
    GAMES[key]=GL
    pl={}
    for gi,g in enumerate(gl):
        for r in g['rows']:
            if r[3]=='GK': continue
            p=pl.setdefault(r[9],dict(pid=r[9],num=collections.Counter(),name=r[2],pos=collections.Counter(),log=[]))
            pp=g['pp'].get(r[0]+'|'+r[1],[0,0,0]); p['num'][r[1]]+=1; p['pos'][r[3]]+=1; p['log'].append([gi,int(r[4]),int(r[5]),int(r[6]),int(r[7]),int(r[8]),pp[0],pp[1],pp[2]])
    roster=[dict(pid=p['pid'],num=int(p['num'].most_common(1)[0][0]),name=p['name'],pos=p['pos'].most_common(1)[0][0],log=p['log']) for p in pl.values()]
    used=set(); out=[]
    ln=lambda x:{w for w in re.sub(r'[^a-z ]','',x.lower()).split() if w not in('jr','sr','ii','iii')}
    for i,r in enumerate(roster):
        if i in used: continue
        for j in range(i+1,len(roster)):
            s=roster[j]
            if j in used or s['num']!=r['num'] or not (ln(r['name'])&ln(s['name'])): continue
            if {x[0] for x in r['log']}&{x[0] for x in s['log']}: continue
            used.add(j); a,b=(r,s) if len(r['log'])>=len(s['log']) else (s,r)
            r=dict(a,log=sorted(r['log']+s['log']),note=f"Combined from two InStat profiles for #{a['num']}: {a['name']} ({len(a['log'])} GP) and {b['name']} ({len(b['log'])} GP).",pos=a['pos'] if a['pos']==b['pos'] else a['pos']+'/'+b['pos'])
            report.append(('merged',key,a['name'],b['name']))
        out.append(r)
    for r in out:
        L=r['log']; gp=len(L)
        nm=r['name'].title() if r['name'].isupper() or r['name'].islower() else r['name']
        S.append([key,r['num'],nm,r['pos'],sum(x[1] for x in L),gp,sum(x[2] for x in L),sum(x[3] for x in L),sum(x[2]+x[3] for x in L),sum(x[4] for x in L),sum(x[5] for x in L),r.get('note',''),r['pid']])
        LOGS[r['pid']+'@'+key]=L
    for gi,g in enumerate(gl):
        gks=[r for r in g['rows'] if r[3]=='GK']
        if not gks: continue
        tt=sum(int(r[4]) for r in gks); top=max(gks,key=lambda r:int(r[4]))
        if int(top[4])>=0.85*tt and int(top[4])>=1500:
            GLOG.setdefault(key+'|'+top[2],[]).append([gi,int(g['score'].split(':')[1])]); GNUM[key+'|'+top[2]]=int(top[1])
    seen=set()
    for i in W.get(key,[]):
        for k,v in (TG.get(i,{}).get('gk') or {}).items():
            n,name=k.split('|',1); f=v.split(',')
            if name in seen or re.search('noname',name,re.I): continue
            seen.add(name)
            try: G.append([key,int(n),name,int(f[0]),int(f[1].split(':')[0])*60+int(f[1].split(':')[1]),float(f[2]) if f[2]!='-' else 0,int(float(f[3])) if f[3]!='-' else 0,int(float(f[4])) if f[4]!='-' else 0,int(f[5].rstrip('%')) if f[5]!='-' else 0])
            except Exception as e: report.append(('gkerr',key,k,v))
have={g[0]+'|'+g[2] for g in G}
for k,L_ in GLOG.items():
    if k not in have and len(L_)>=1:
        key,name=k.split('|',1); G.append([key,GNUM[k],name,len(L_),0,0,0,0,0])
POSX=json.load(open('pos.json')) if __import__('os').path.exists('pos.json') else {}
for s in S:
    s[12]=s[12]+'@'+s[0]
    if s[12] in POSX: s[3]=POSX[s[12]]
# expected goals-against model: GA ~ exp(a+b*(opp rating - team rating))
import math
X=[];Y=[]
for key,GLs in GAMES.items():
    for g in GLs:
        if g[3]: X.append(g[3]-INFO[key]['rating']); Y.append(int(g[6].split(':')[1]))
xa,xb=math.log(sum(Y)/len(Y)),0.0
for it in range(60):
    mu=[math.exp(xa+xb*x) for x in X]
    g0=sum(y-m for y,m in zip(Y,mu)); g1=sum((y-m)*x for y,m,x in zip(Y,mu,X))
    h00=sum(mu); h01=sum(m*x for m,x in zip(mu,X)); h11=sum(m*x*x for m,x in zip(mu,X))
    det=h00*h11-h01*h01; xa+=(h11*g0-h01*g1)/det; xb+=(-h01*g0+h00*g1)/det
print('xGA model',len(X),round(xa,4),round(xb,4),'GA at even',round(math.exp(xa),2))
T12=[[INFO[f'12-{i}']['name'],INFO[f'12-{i}']['rating'],INFO[f'12-{i}']['rank']] for i in range(50)]; T13=[[INFO[f'13-{i}']['name'],INFO[f'13-{i}']['rating'],INFO[f'13-{i}']['rank']] for i in range(50)]
C12=[[INFO[f'12-C{i}']['name'],INFO[f'12-C{i}']['rating'],INFO[f'12-C{i}']['rank']] for i in range(10)]; C13=[[INFO[f'13-C{i}']['name'],INFO[f'13-C{i}']['rating'],INFO[f'13-C{i}']['rank']] for i in range(10)]
json.dump(dict(S=S,G=G,GAMES=GAMES,LOGS=LOGS,GLOG=GLOG,XA=round(xa,4),XB=round(xb,4),T12=T12,T13=T13,C12=C12,C13=C13,BORN={k+'@'+s[0]:v for k,v in BORN.items() for s in S if s[12].startswith(k+'@')}),open('db.json','w'),separators=(',',':'))
nodata=[k+' '+INFO[k]['name'] for k in INFO if not GAMES.get(k)]
low=[(k,INFO[k]['name'],len(GAMES[k])) for k in INFO if 0<len(GAMES[k])<6]
print('skaters',len(S),'goalies',len(G),'team-games',sum(len(v) for v in GAMES.values()),'teams with data',sum(1 for v in GAMES.values() if v))
print('NODATA',nodata); print('LOW',low)
print('merged',len([r for r in report if r[0]=='merged']),[r for r in report if r[0]!='merged'][:5])
print('UNMATCHED',len(unm),sum(unm.values()),unm.most_common(40))
if '-v' in sys.argv:
    for k in INFO: print(k,INFO[k]['name'],len(GAMES[k]),len([s for s in S if s[0]==k]))

print('TEAMS MISSING FROM RATINGS',MISSING)
