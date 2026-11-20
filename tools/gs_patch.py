# python3 tools/gs_patch.py /tmp/gs/gN.jsonl DIV < json   : replace fields of a stored live game line with what the sheet shows now
# (stdin = {"vs":..,"hs":..,"st":..,"goals":[...],"pens":[...],"goalies":[...]} , any subset), then import it.
import json,sys,subprocess
f,dv=sys.argv[1],sys.argv[2]; g=json.loads(open(f).read().strip()); g.update(json.loads(sys.stdin.read())); open(f,'w').write(json.dumps(g)+'\n')
print(subprocess.run(['python3','build/gs_import.py',dv,f],capture_output=True,text=True).stdout.strip().split('\n')[-1], g['v'],g['vs'],g['h'],g['hs'],g['st'])
