#!/usr/bin/env python3
# tools/ss_score.py "id~vs~hs~status ## ..." : Silver Stick live scores (GameSheet season 16542).
# A game not yet in data/gs_box.json gets its first import through tools/live_score.py with the rating names,
# Central time and rink from data/silverstick_2026_gs.json; every line then goes through tools/live_auto.py.
# Lines with an empty score are skipped. Bracket games (new ids, posted Saturday night) must be added to silverstick_2026_gs.json first.
import json,sys,subprocess,datetime
G=json.load(open('data/silverstick_2026_gs.json')); S=G['season']; g=G['games']
B=json.load(open('data/gs_box.json')); have={k.split('|')[2] for k in B}
first={}
for r in sys.argv[1].replace('done ','').replace('wait ','').split('##'):
    p=[x.strip() for x in r.strip().split('~')]
    if len(p)<4 or p[1] in ('','null') or p[2] in ('','null'): continue
    i=p[0]
    if i in have: continue
    if i not in g: print('NOT A KNOWN SILVER STICK GAME (add to silverstick_2026_gs.json):',r.strip()); continue
    x=g[i]; d=datetime.date.fromisoformat(x['date'])
    when=f"{d.strftime('%b')} {d.day}, {d.year}, {x['ct']}"
    first.setdefault(x['y'],[]).append('~'.join([i,str(S),x['v'],x['h'],when,x['rink'],p[1],p[2],p[3]]))
for y,rows in first.items():
    print(subprocess.run(['python3','tools/live_score.py',y,' ## '.join(rows)],capture_output=True,text=True).stdout.strip()[:400])
print(subprocess.run(['python3','tools/live_auto.py',sys.argv[1]],capture_output=True,text=True).stdout.strip())
