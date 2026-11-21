#!/usr/bin/env python3
"""Compact live lines -> gs jsonl. Usage: pk2jsonl.py OUT.jsonl < lines
Line: ID STATUS VS-HS G [[0,"#31 NAME"],...] :: P MM:SS v|h : NUM NAME/NUM NAME[flags];...
(made in the page by the `pk` helper noted in data/LIVE_CHECK.md). Team names, time and rink come from data/gs_meta.json
(id -> {s,v,h,when,rink}); add a game there before its first read."""
import sys,json,re
M=json.load(open('/home/claude/livehockeyratings/data/gs_meta.json'))
P={'1':'1ST','2':'2ND','3':'3RD','O':'OT','S':'SO'}
out=[]
for l in sys.stdin:
    l=l.strip()
    if not l: continue
    head,_,gs=l.partition(' ::');gs=gs.strip()
    m=re.match(r'(\d+) (.*?) (\d+|null)-(\d+|null) G (.*)$',head)
    gid,st,vs,hs,gl=m.groups();meta=M[gid]
    goals=[]
    for g in [x for x in gs.split(';') if x]:
        mm=re.match(r'(.)(\d+:\d+)([vh]):(.*?)(\[(.*)\])?$',g)
        p,t,side,names,_,fl=mm.groups()
        goals.append([P.get(p,p),t,1 if side=='h' else 0,['#'+n for n in names.split('/')],fl.split(',') if fl else []])
    o=dict(id=int(gid),s=meta['s'],v=meta['v'],h=meta['h'],when=meta['when'],rink=meta.get('rink',''),vs=0 if vs=='null' else int(vs),hs=0 if hs=='null' else int(hs),st=st,goalies=json.loads(gl),goals=goals,pens=[])
    out.append(json.dumps(o))
open(sys.argv[1],'w').write('\n'.join(out)+'\n');print(len(out),'games')
