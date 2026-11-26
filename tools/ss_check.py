#!/usr/bin/env python3
# tools/ss_check.py "<output of window.__ssl(day)>" : one Silver Stick live check (Nov 26 2026).
# Keeps only the tracked games (ids in data/silverstick_2026_gs.json), and ONLY if a score or status changed since the last check
# runs tools/ss_score.py and tools/live_pub.sh. Prints: changed or not, new FINALS (with the names), live count, next start, and what to schedule.
import json,sys,subprocess,datetime,zoneinfo,re,os
G=json.load(open('data/silverstick_2026_gs.json'))['games']
raw=sys.argv[1].split('|',1)[-1]
rows=[r.strip() for r in raw.split('##') if r.strip() and r.strip().split('~')[0] in G]
cur={r.split('~')[0]:r for r in rows}
lp='/tmp/ss_last.json'; last=json.load(open(lp)) if os.path.exists(lp) else {}
ch=[i for i in cur if last.get(i)!=cur[i]]
newfin=[i for i in ch if 'FINAL' in cur[i] and 'FINAL' not in last.get(i,'')]
odd=[cur[i] for i in cur if '?:' in cur[i]]
if ch:
    print(subprocess.run(['python3','tools/ss_score.py',' ## '.join(rows)],capture_output=True,text=True).stdout.strip()[-300:])
    o=subprocess.run(['tools/live_pub.sh','Silver Stick live'],capture_output=True,text=True).stdout
    print('\n'.join(l for l in o.split('\n') if re.search(r'published|live gaps|IN PROGRESS ·|HELD|held|moved',l))[-600:])
    last.update(cur); json.dump(last,open(lp,'w'))
else: print('no change: nothing published')
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
