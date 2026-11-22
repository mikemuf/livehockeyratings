#!/usr/bin/env python3
# tools/live_full.py FILE : FULL live update (score, status, goals with scorers and assists, goalies) for games ALREADY in data/gs_box.json.
# FILE holds the page's compact lines (window.__pk after window.__go(); format in tools/pk2jsonl.py), one game per line.
# Owner, Nov 22 2026 11:58 AM: the live page must mirror the scoresheet (period scores, who scored), not only the total.
# Keeps the app's team names, time and rink. Rows with no score are skipped. Prints *** FINAL for games that just ended.
import json,sys,re,subprocess,os
B=json.load(open('data/gs_box.json')); byid={k.split('|')[2]:k for k in B}
P={'1':'1ST','2':'2ND','3':'3RD','O':'OT','S':'SO'}; bydiv={}; keep={}
for l in open(sys.argv[1]).read().replace(' @@ ','\n').split('\n'):
    l=l.strip()
    if not l: continue
    head,_,gs=l.partition(' ::'); m=re.match(r'(\d+) (.*?) (\d+|null)-(\d+|null) G (.*)$',head)
    if not m: print('BAD LINE',l[:60]); continue
    gid,st,vs,hs,gl=m.groups()
    if vs=='null' or hs=='null': continue
    k=byid.get(gid)
    if not k: print('NOT IN BOX (first import needed):',gid,vs,hs,st); continue
    x=B[k]; div=k.split('|')[0]; goals=[]
    for g in [y for y in gs.strip().split(';') if y]:
        mm=re.match(r'(.)(\d+:\d+)([vh]):(.*?)(\[(.*)\])?$',g)
        if not mm: continue
        p,t,side,names,_,fl=mm.groups(); goals.append([P.get(p,p),t,1 if side=='h' else 0,['#'+n for n in names.split('/')],fl.split(',') if fl else []])
    if any(g[3]==['#'] or not g[3] for g in goals): goals=[]   # league hides names (EHF young ages): sides are unreliable too, keep the score only
    try: goalies=json.loads(gl)
    except Exception: goalies=[]
    st=st.strip() or ('FINAL' if x.get('st','').startswith('FINAL') else 'IN PROGRESS')
    if st=='UNOFFICIAL FINAL' or st=='': st='FINAL'
    if not str(x.get('st','')).startswith('FINAL') and st.startswith('FINAL'): print('*** FINAL',div,x['v'],vs,x['h'],hs)
    keep[k]={f:x.get(f) for f in ('v','h','time','date','rink','url')}
    M=json.load(open('data/gs_meta.json')).get(gid,{})
    bydiv.setdefault(div,[]).append(dict(id=int(gid),s=int(k.split('|')[1]),v=x['v'],h=x['h'],when=M.get('when',''),rink=M.get('rink',x.get('rink','')),vs=int(vs),hs=int(hs),st=st,goalies=goalies,goals=goals,pens=[]))
os.makedirs('/tmp/gs',exist_ok=True)
for div,rows in bydiv.items():
    f=f'/tmp/gs/full_{div}.jsonl'; open(f,'w').write(''.join(json.dumps(o)+'\n' for o in rows))
    print(div,subprocess.run(['python3','build/gs_import.py',div,f],capture_output=True,text=True).stdout.strip().split('\n')[-1],[(o['v'],o['vs'],o['h'],o['hs'],o['st'],len(o['goals'])) for o in rows])
B=json.load(open('data/gs_box.json'))
for k,old in keep.items():
    if k in B:
        for f,v in old.items():
            if v is not None and f in ('v','h'): B[k][f]=v
json.dump(B,open('data/gs_box.json','w'),ensure_ascii=False)
