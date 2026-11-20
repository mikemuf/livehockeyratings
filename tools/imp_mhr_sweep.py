import json,re,datetime,sys
APPLY=len(sys.argv)>1
p='data/weekend_public.json';W=json.load(open(p));R=json.load(open('/home/claude/player/data/ratings.json'))
V={'119':'2011','114':'2012','125':'2013','124':'2014','123':'2015','122':'2016'}
CT={'Canlan Ice Sports - West Dundee','Carol Stream Ice Rink','Centene Community Ice Center','Elk Grove Ice Arena','Orbit Ice Arena','Arctic Ice Arena','Bellerive Ice Center','Deep South Ice Sports Complex'}
PT={'San Diego Ice Arena'}  # US Pacific only. British Columbia stays on daylight time all year: BC rink time + 1 hour = Central (see WEEKEND_SOURCES miss log, Nov 20 2026)
CITY={'Centene Community Ice Center':'Maryland Heights, MO','UPMC Lemieux Sports Complex':'Cranberry Township, PA','RMU Island Sports Center':'Pittsburgh, PA','Alpha Ice Complex':'Pittsburgh, PA','Printscape Arena':'Canonsburg, PA','Canlan Ice Sports - West Dundee':'West Dundee, IL','Carol Stream Ice Rink':'Carol Stream, IL','Orbit Ice Arena':'Palatine, IL','ICENTER':'Salem, NH','Rhode Island Sports Center':'North Smithfield, RI','Bog Ice Arena':'Kingston, MA','Chiller Ice Works':'Columbus, OH','OhioHealth Ice Haus':'Columbus, OH','USA Hockey Arena':'Plymouth, MI','San Diego Ice Arena':'San Diego, CA','ION International Training Center':'Leesburg, VA'}
AL=json.load(open('/tmp/alias.json')) if __import__('os').path.exists('/tmp/alias.json') else {}
def norm(y,n):
    Ry=R[y]
    if (y+'|'+n) in AL: return AL[y+'|'+n]
    if n in Ry: return n
    c=[n.replace(' Hockey Academy',''),n.replace(' Hockey Club',''),re.sub(r' \((Premier|T1|Tier 1)\)$','',n),n.replace('New Jersey','NJ'),n.replace('Minnesota','MN'),n+' (Elite)',n.replace(' Hockey Club','')+' (Elite)']
    for x in c:
        if x in Ry: return x
    return None
od={'Thu':0,'Fri':1,'Sat':2,'Sun':3}
def key(g):
    if isinstance(g,list): return (9,0)
    try: tm=datetime.datetime.strptime(g['time'],'%I:%M %p');return (od.get(g['day'],8),tm.hour*60+tm.minute)
    except Exception: return (od.get(g['day'],8),9999)
y=None;unm={};add={}
for l in open(sys.argv[2] if len(sys.argv)>2 else 'data/sched_nov20_mhr.txt'):
    l=l.strip()
    if l.startswith('#V'): y=V.get(l[2:]) or l[2:];continue
    q=l.split('|')
    if len(q)<6: continue
    t=re.sub(r'^\d+ ','',q[0]);a=norm(y,t);b=norm(y,q[3])
    if not a: unm[(y,t)]=1;continue
    if not b: unm[(y,q[3])]=unm.get((y,q[3]),0)+1; b=q[3]
    day={'20':'Fri','21':'Sat','22':'Sun'}[q[1]];rk=q[5]
    try: lt=datetime.datetime.strptime(q[2].upper(),'%I:%M%p')
    except Exception: print('bad time',l);continue
    off=0 if rk in CT else (-2 if rk in PT else 1);z='CT' if rk in CT else ('PT' if rk in PT else 'ET')
    ct=(lt-datetime.timedelta(hours=off)).strftime('%-I:%M %p')
    D=W['divs'].setdefault(y,{});D.setdefault('watch',[])
    if any(isinstance(g,dict) and g['day']==day and {g['a'],g['b']}=={a,b} and abs(key(g)[1]-key({'day':day,'time':ct})[1])<=90 for g in D['watch']): continue
    D['watch'].append({'day':day,'time':ct,'a':a,'b':b,'rink':rk,'city':CITY.get(rk,''),'note':{'**':'Tournament','*':'League'}.get(q[4],''),'local':lt.strftime('%-I:%M %p')+' '+z,'tz':'CT'});add[y]=add.get(y,0)+1
for yy in add: W['divs'][yy]['watch'].sort(key=key)
print('added',add);print('unmatched',sorted(unm.items()))
if APPLY: json.dump(W,open(p,'w'),ensure_ascii=False,indent=1)
