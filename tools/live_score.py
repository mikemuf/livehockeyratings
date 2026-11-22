#!/usr/bin/env python3
# tools/live_score.py DIV "id~season~visitor~home~when~rink~vs~hs~status ## ..."  : put live (or final) scores on the page, score only.
# The lines come from the page: __gsout lines mapped to [o.id,o.s,o.v,o.h,o.when,o.rink,o.vs,o.hs,o.st].join('~'), joined with ' ## '.
# Rows with an empty score are skipped. Keeps goals already stored for the game (gs_patch does the same for full lines).
import json,sys,subprocess,os
div=sys.argv[1]; rows=[r.strip() for r in sys.argv[2].split('##') if r.strip()]
B=json.load(open('data/gs_box.json')); M=json.load(open('data/gs_meta.json')); out=[]
for r in rows:
    p=r.split('~')
    if len(p)<9 or p[6]=='' or p[7]=='': continue
    i,se,v,h,w,rk,vs,hs,st=p[:9]
    M[i]={"s":int(se),"v":v,"h":h,"when":w,"rink":rk}
    old=B.get(f"{div}|{se}|{i}",{})
    out.append({"id":int(i),"s":int(se),"v":v,"h":h,"when":w,"rink":rk,"vs":int(vs),"hs":int(hs),"st":st or "IN PROGRESS","goalies":old.get('goalies_raw',[]),"goals":[],"pens":[]})
json.dump(M,open('data/gs_meta.json','w'))
f=f'/tmp/gs/ls_{div}_{os.getpid()}.jsonl'; os.makedirs('/tmp/gs',exist_ok=True)
open(f,'w').write(''.join(json.dumps(o)+'\n' for o in out))
print(subprocess.run(['python3','build/gs_import.py',div,f],capture_output=True,text=True).stdout.strip(), [ (o['v'],o['vs'],o['h'],o['hs'],o['st']) for o in out])
