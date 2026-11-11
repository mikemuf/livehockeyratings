# python3 positions_lines.py lines.json [key prefixes...] -> updates pos.json for the given team keys (default: 14-, 15-)
# Positions are inferred, not taken from InStat's labels: every 5-man line unit should hold exactly 2 defensemen,
# so the script finds the D/F split that best fits the units' ice time. Faceoffs help: a player who takes 3+ a game
# is a forward, one who takes none over many games leans defense; an InStat "F" label also counts as evidence.
import json,re,sys,collections
L=json.load(open(sys.argv[1]))
# team keys to (re)compute: plain prefixes, or one argument 're:<regex>' matched against the whole key
class _Sel(str):
    def startswith(self,p): return bool(_RX.fullmatch(self)) if _RX else str.startswith(self,p)
_RX=re.compile(sys.argv[2][3:]) if len(sys.argv)>2 and sys.argv[2].startswith('re:') else None
pref=tuple(sys.argv[2:]) or ('14-','15-')
W=json.load(open('wanted.json')); D=json.load(open('box.json')); d=json.load(open('db.json')); POS=json.load(open('pos.json'))
sec=lambda s:int(s.split(':')[0])*60+int(s.split(':')[1]) if ':' in s else 1
clean=lambda x:re.sub(r'[^a-z]','',x.lower())
E2K={i:k for k,v in W.items() for i in v}
FO=collections.defaultdict(lambda:[0,0])   # pid@key -> [games, faceoffs]
for m in D['M']:
    if 'FO' not in m and not any(_Sel(E2K.get(x.split('=',1)[0],'')).startswith(pref) for x in m['tl']): continue
    for side,x in enumerate(m['tl']):
        tid,tn=x.split('=',1); key=E2K.get(tid)
        if not key or not _Sel(key).startswith(pref): continue
        si=m['S'].index(tn.upper()) if tn.upper() in m['S'] else side
        for p in m['P']:
            r=p.split('|')
            if int(r[0])!=si or r[3]=='GK': continue
            f=FO[r[9]+'@'+key]; f[0]+=1; f[1]+=(m.get('FO') or {}).get(r[0]+'|'+r[1],0)
src=collections.Counter(); rep=[]
for key,ids in W.items():
    if not _Sel(key).startswith(pref): continue
    roster=[s for s in d['S'] if s[0]==key]
    if not roster: continue
    units=collections.Counter()
    for i in ids:
        for u,t in (L.get(i) or {}).items():
            ps=tuple(sorted(u.split('~')))
            if len(ps)==5 and not any('noname' in p.lower() for p in ps): units[ps]+=sec(t)
    tot=collections.Counter()
    for u,w in units.items():
        for p in u: tot[p]+=w
    info={}
    for s in roster:
        last=clean(s[2].split()[-1]) if s[2].split() else ''
        cand=[p for p in tot if re.match(r'^(\d+)',p).group(1)==str(s[1]) and clean(p.split('.',1)[1]).endswith(last[-5:])]
        if not cand: cand=[p for p in tot if clean(p.split('.',1)[1])==last and p[len(re.match(r'^\d+',p).group(0))]==s[2][0].upper()]
        tok=max(cand,key=lambda x:tot[x]) if cand else None
        f=FO.get(s[12]); info[s[12]]=(tok,tuple(f) if f else None)
    a={}; sc=collections.Counter(); hard=set()
    for srow in roster:
        tok,f=info[srow[12]]
        if not tok: continue
        s_=0.0
        if srow[3]=='F': s_-=0.4
        elif srow[3]=='D': s_+=0.05
        if f and f[0]>=3:
            if f[1]==0: s_+=0.5*min(1,f[0]/15)
            elif f[1]/f[0]>=3: hard.add(tok); s_-=5
            elif f[1]>=3: s_-=0.3
        sc[tok]+=s_
    for p in tot: a[p]=1 if sc[p]>0.2 else 0
    U=list(units.items())
    def cost(a): return sum(w*abs(sum(a[p] for p in u)-2) for u,w in U)+sum(tot[p]*max(0,(-sc[p] if a[p] else sc[p])) for p in a)
    if U:
        c=cost(a); imp=True; it=0
        while imp and it<60:
            imp=False; it+=1
            for p in sorted(a,key=lambda x:-tot[x]):
                if p in hard: continue
                a[p]=1-a[p]; c2=cost(a)
                if c2<c-1e-9: c=c2; imp=True
                else: a[p]=1-a[p]
    for s in roster:
        tok,f=info[s[12]]
        if tok and tot[tok]>=120: pos='D' if a[tok] else 'F'; src['lines+faceoffs']+=1
        elif f and f[0]>=3: pos='D' if f[1]==0 else 'F'; src['faceoffs']+=1
        else: pos='F'; src['default F']+=1
        POS[s[12]]=pos
    mx=max(x[5] for x in roster); reg=[s for s in roster if s[5]>=max(2,0.4*mx)]
    rep.append((key,sum(1 for s in reg if POS[s[12]]=='D'),sum(1 for s in reg if POS[s[12]]!='D')))
json.dump(POS,open('pos.json','w'))
print('positions set by',dict(src))
print('regulars D/F per team:',' '.join(f'{k}:{dd}D/{ff}F' for k,dd,ff in rep))
print('D-count distribution',sorted(collections.Counter(r[1] for r in rep).items()))
