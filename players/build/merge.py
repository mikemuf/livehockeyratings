# python3 merge.py harvest.json  -> adds newly harvested games and refreshed goalie tables to box.json
import json,sys
D=json.load(open('box.json')); H=json.load(open(sys.argv[1]))
have={m['id'] for m in D['M']}; added=[]; bad=[]
# Canary: any already-stored game that was re-read must come back identical, or the page layout has changed.
OLD={m['id']:m for m in D['M']}; can=[m for m in H['M'].values() if m['id'] in OLD]
for m in can:
    o=OLD[m['id']]
    if sorted(m.get('P',[]))!=sorted(o['P']) or m.get('h')!=o['h'] or m.get('tl')!=o['tl']:
        print('CANARY FAILED for game',m['id'],'- InStat page layout may have changed. Nothing merged.'); print(' stored:',o['h'],len(o['P']),o['P'][:2]); print(' read now:',m.get('h'),len(m.get('P',[])),m.get('P',[])[:2]); sys.exit(2)
print('canary ok:',len(can),'stored game(s) re-read identically' if can else 'NO CANARY GAME IN HARVEST - do not publish without checking a known game')
for m in H['M'].values():
    if m['id'] in have: continue
    if m.get('ok') and m.get('h') and len(m.get('tl',[]))==2: D['M'].append(m); added.append(m)
    else: bad.append(m['id'])
TG={t['id']:t for t in D['T']}; gk=0
for t in H['T'].values():
    o=TG.get(t['id'])
    if not o: o={'id':t['id'],'m':{},'gk':{}}; D['T'].append(o); TG[t['id']]=o
    o['m'].update(t.get('m') or {})
    if t.get('gk'): o['gk']=t['gk']; gk+=1
    if t.get('name'): o['name']=t['name']
json.dump(D,open('box.json','w'),separators=(',',':'))
print('games added',len(added),'| not ready (no box score yet)',len(bad),bad[:20],'| goalie tables refreshed',gk,'| total games',len(D['M']))
for m in sorted(added,key=lambda m:m['h'].split('~')[0][6:]+m['h'].split('~')[0][3:5]+m['h'].split('~')[0][:2]): print(' ',m['id'],m['h'].replace('~',' | '),len(m['P']),'players')
