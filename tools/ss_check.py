#!/usr/bin/env python3
# tools/ss_check.py "<output of window.__ssl(day)>" : one Silver Stick live check (Nov 26 2026).
# Keeps only the tracked games (ids in data/silverstick_2026_gs.json), and ONLY if a score or status changed since the last check
# runs tools/ss_score.py and tools/live_pub.sh. Prints: changed or not, new FINALS (with the names), live count, next start, and what to schedule.
import json,sys,subprocess,datetime,zoneinfo,re,os
G=json.load(open('data/silverstick_2026_gs.json'))['games']
raw=sys.argv[1].split('|',1)[-1]
rows=[r.strip() for r in raw.split('##') if r.strip() and r.strip().split('~')[0] in G]
_now=datetime.datetime.now(zoneinfo.ZoneInfo('America/Chicago'))
def _young(i):  # a row with no LIVE word reads as FINAL; do not believe that for a game that started under 50 minutes ago
    g=G[i]; t0=datetime.datetime.strptime(g['date']+' '+g['ct'],'%Y-%m-%d %I:%M %p').replace(tzinfo=_now.tzinfo); return (_now-t0).total_seconds()<3000
rows=[(r.replace('FINAL (OT)','IN PROGRESS').replace('FINAL (SO)','IN PROGRESS').replace('FINAL','IN PROGRESS') if 'FINAL' in r and _young(r.split('~')[0]) else r) for r in rows]
cur={r.split('~')[0]:r for r in rows}
lp='/tmp/ss_last.json'; last=json.load(open(lp)) if os.path.exists(lp) else {}
ch=[i for i in cur if last.get(i)!=cur[i]]
newfin=[i for i in ch if 'FINAL' in cur[i] and 'FINAL' not in last.get(i,'')]
odd=[cur[i] for i in cur if '?:' in cur[i]]
anylive=any('IN PROGRESS' in v for v in cur.values())
if ch or anylive or (len(sys.argv)>2 and sys.argv[2].strip()):  # owner Nov 26 1:00 PM: the page's 'updated' time must move with every check while a game is live, even at the same score
    print(subprocess.run(['python3','tools/ss_score.py',' ## '.join(rows)],capture_output=True,text=True).stdout.strip()[-300:])
    if len(sys.argv)>2 and sys.argv[2].strip():   # box-score lines from window.__ssw(): goals, scorers, goalies (tools/ss_box.js)
        os.makedirs('/tmp/gs',exist_ok=True); open('/tmp/gs/ss_pk.txt','w').write(sys.argv[2].replace('PARTIAL ',''))
        r=subprocess.run(['python3','tools/live_full.py','/tmp/gs/ss_pk.txt'],capture_output=True,text=True); print((r.stdout.strip()+r.stderr.strip()[-300:])[-500:])
        subprocess.run(['python3','tools/ss_score.py',' ## '.join(rows)],capture_output=True,text=True)  # finals the box read confirmed go to pending
    o=subprocess.run(['tools/live_pub.sh','Silver Stick live'],capture_output=True,text=True).stdout
    print('\n'.join(l for l in o.split('\n') if re.search(r'published|live gaps|IN PROGRESS ·|HELD|held|moved',l))[-600:])
    last.update(cur); json.dump(last,open(lp,'w'))
else: print('no change, nothing live: nothing published')
for i in newfin:
    g=G[i]; p=cur[i].split('~'); print('NEW FINAL',g['y'],'Pool',g.get('pool'),'|',g['v'],p[1],'-',g['h'],p[2],'| id',i)
if odd: print('UNPARSED ROWS (fix tools/ss_list.js):',odd)
now=datetime.datetime.now(zoneinfo.ZoneInfo('America/Chicago')); today=now.date().isoformat()
def st(g): return datetime.datetime.strptime(g['date']+' '+g['ct'],'%Y-%m-%d %I:%M %p').replace(tzinfo=now.tzinfo)
live=[i for i in cur if 'IN PROGRESS' in cur[i]]
fin={i for i in last if 'FINAL' in last[i]}
pend=sorted((st(g),i) for i,g in G.items() if i not in fin and i not in live)
due=[x for x in pend if x[0]<=now]  # should have started, not on the sheet yet
nxt=[x for x in pend if x[0]>now]
print('now',now.strftime('%a %I:%M %p'),'| live',len(live),'| started but not on sheet',len(due),'| finals so far',len(fin))
if live or due or (nxt and (nxt[0][0]-now).total_seconds()<=600): print('NEXT CHECK: 7 minutes')
elif nxt: print('NEXT CHECK:',(nxt[0][0]+datetime.timedelta(minutes=3)).strftime('%a %b %d %I:%M %p'),'CT (next start + 3)')
else: print('NEXT CHECK: none, all games final')
