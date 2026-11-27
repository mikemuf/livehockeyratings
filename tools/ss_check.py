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
# The game's own page beats the list (Nov 26 2:42 PM: as game 3183161 was being closed the LIST showed '0-0 LIVE' while its page said FINAL 1-5).
_ov={}
for _l in (sys.argv[2] if len(sys.argv)>2 else '').replace('PARTIAL ','').split(' @@ '):
    _m=re.match(r'^(\d+) (.*?) (\d+)-(\d+) G ',_l.strip())
    if _m: _ov[_m.group(1)]='~'.join([_m.group(1),_m.group(3),_m.group(4),'FINAL' if 'FINAL' in _m.group(2) else 'IN PROGRESS'])
_lp='/tmp/ss_last.json'; _last=json.load(open(_lp)) if os.path.exists(_lp) else {}
def _fixrow(r):
    i=r.split('~')[0]
    if i in _ov: return _ov[i]
    o=_last.get(i)
    if o:  # never let a list row take goals away or reopen a final
        po,pn=o.split('~'),r.split('~')
        try:
            if 'FINAL' in po[3] or int(pn[1])+int(pn[2])<int(po[1])+int(po[2]): return o
        except Exception: pass
    return r
rows=[_fixrow(r) for r in rows]
cur={r.split('~')[0]:r for r in rows}
lp='/tmp/ss_last.json'; last=json.load(open(lp)) if os.path.exists(lp) else {}
ch=[i for i in cur if last.get(i)!=cur[i]]
newfin=[i for i in ch if 'FINAL' in cur[i] and 'FINAL' not in last.get(i,'')]
odd=[cur[i] for i in cur if '?:' in cur[i]]
anylive=any('IN PROGRESS' in v for v in cur.values())
if ch or anylive or (len(sys.argv)>2 and sys.argv[2].strip()):  # owner Nov 26 1:00 PM: the page's 'updated' time must move with every check while a game is live, even at the same score
    print(subprocess.run(['python3','tools/ss_score.py',' ## '.join(rows)],capture_output=True,text=True).stdout.strip()[-300:])
    if len(sys.argv)>2 and sys.argv[2].strip():   # box-score lines from window.__ssw(): goals, scorers, goalies (tools/ss_box.js)
        os.makedirs('/tmp/gs',exist_ok=True)
        # DELTA LINES (tools/ss_box.js __ssw, Nov 26 2:05 PM): 'id ST v-h G <goalies json or => :: +START:<new goals>' ; the full goal list is kept here
        sp='/tmp/gs/ss_pk_state.json'; S0=json.load(open(sp)) if os.path.exists(sp) else {}; full=[]
        for l in sys.argv[2].replace('PARTIAL ','').replace(' MORE','').split(' @@ '):
            m=re.match(r'^(\d+) (.*?) (\d+-\d+) G (.*?) :: \+(\d+):(.*)$',l.strip())
            if not m: 
                if l.strip(): print('BAD DELTA LINE',l[:70])
                continue
            i,st,sc,gl,start,new=m.groups(); e=S0.get(i,{'g':'[]','goals':[]}); start=int(start); new=[x for x in new.split(';') if x]
            if gl not in ('=','same'): e['g']=gl
            if start==0: e['goals']=new
            elif start==len(e['goals']): e['goals']+=new
            else: print('RESYNC NEEDED',i,'(run window.__ssresync("%s") in the tab; have %d goals, delta starts at %d)'%(i,len(e['goals']),start)); continue
            S0[i]=e; full.append(f"{i} {st} {sc} G {e['g']} :: {';'.join(e['goals'])}")
        json.dump(S0,open(sp,'w')); open('/tmp/gs/ss_pk.txt','w').write(' @@ '.join(full))
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
if live or due or (nxt and (nxt[0][0]-now).total_seconds()<=600): print('NEXT CHECK: 30 minutes')
elif nxt: print('NEXT CHECK:',(nxt[0][0]+datetime.timedelta(minutes=3)).strftime('%a %b %d %I:%M %p'),'CT (next start + 3)')
else: print('NEXT CHECK: none, all games final')
