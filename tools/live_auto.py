#!/usr/bin/env python3
# tools/live_auto.py "id~vs~hs~status ## ..."  : update the score and status of games ALREADY in data/gs_box.json (any birth year),
# straight in the file (names, time, rink and stored goals are kept). Lines come from window.__sl() in a reader tab.
# A game not yet in gs_box needs its first import with tools/live_score.py DIV "full ~ lines" (app names, Central time).
# Prints what changed and every game that just went FINAL (those need the finals procedure).
import json,sys
B=json.load(open('data/gs_box.json')); byid={k.split('|')[2]:k for k in B}
for r in sys.argv[1].replace('done ','').replace('wait ','').split('##'):
    p=[x.strip() for x in r.strip().split('~')]
    if len(p)<4 or p[1]=='' or p[2]=='' or p[1]=='null': continue
    k=byid.get(p[0])
    if not k: print('NOT IN BOX (first import needed):',r.strip()); continue
    x=B[k]; old=(x['vs'],x['hs'],x['st']); st=p[3] or 'IN PROGRESS'
    x['vs'],x['hs'],x['st']=int(p[1]),int(p[2]),st
    if old!=(x['vs'],x['hs'],x['st']): print(('*** FINAL ' if st.startswith('FINAL') and not str(old[2]).startswith('FINAL') else 'upd ')+k.split('|')[0],x['v'],x['vs'],x['h'],x['hs'],st)
json.dump(B,open('data/gs_box.json','w'),ensure_ascii=False)
