"""Import GameSheet box scores (JSON lines from tools/gs_games.js) into data/gs_box.json.
Usage: python3 build/gs_import.py DIV file.jsonl   (DIV = birth year, e.g. 2012)
Team names are mapped to app names; the published file carries no GameSheet ids."""
import json,sys,re
NAME={'2012 LITTLE CAESARS AAA':'Little Caesars','HURON-PERTH LAKERS':'Huron Perth Lakers','BIGGBY':'Biggby Coffee','NASHVILLE JR PREDATORS':'Nashville Jr. Predators',
 'ST LOUIS BLUES':'St. Louis Blues','NEW JERSEY COLONIALS':'NJ Colonials','TOP GUN ELITE':'Top Gun (Elite)','BOSTON JR EAGLES ELITE':'Boston Jr Eagles (Elite)',
 'UPPER CANADA COLLEGE':'Upper Canada College','TORONTO JR CANADIENS':'Toronto Jr Canadiens','CHATHAM-KENT CYCLONES':'Chatham-Kent Cyclones','WINDY CITY STORM':'Windy City Storm',
 'SEACOAST PERFORMANCE ACADEMY':'Seacoast Performance Academy','CHICAGO FURY':'Chicago Fury','CLEVELAND BARONS':'Cleveland Barons','FOX MOTORS':'Fox Motors',
 'MASTERS ACADEMY':'Masters Academy','OHIO BLUE JACKETS':'Ohio Blue Jackets','HILL ACADEMY':'Hill Academy','TEAM ILLINOIS':'Team Illinois',
 'PITTSBURGH PENGUINS ELITE':'Pittsburgh Penguins Elite','BISHOP KEARNEY SELECTS':'Bishop Kearney Selects',"SHATTUCKS ST MARY'S":"Shattuck St Mary's","LITTLE CAESAR'S":'Little Caesars'}
MON={'Nov':'11','Oct':'10','Dec':'12'}
def nm(s):
    s=re.sub(r'\s+(20\d\d|2011 WEEKEND SERIES)$','',s.strip().upper())
    return NAME.get(s,s.title())
def clean(p):  # "#94 ZACHARY XANDERS (2)" -> ["94","Zachary Xanders",2]
    m=re.match(r'#(\S+)\s+(.*?)(?:\s+\((\d+)\))?$',p.strip())
    if not m: return ['',p.title(),None]
    return [m.group(1),m.group(2).title().replace("'S","'s"),int(m.group(3)) if m.group(3) else None]
dv,fn=sys.argv[1],sys.argv[2]
box=json.load(open('data/gs_box.json')) if __import__('os').path.exists('data/gs_box.json') else {}
n=0
for line in open(fn):
    line=line.strip()
    if not line.startswith('{'): continue
    g=json.loads(line)
    if 'err' in g or g.get('vs') is None: continue
    m=re.match(r'([A-Z][a-z]{2}) (\d+), (\d{4}), (.*)',g['when']);date=f"{m.group(3)}-{MON[m.group(1)]}-{int(m.group(2)):02d}"
    v,h=nm(g['v']),nm(g['h'])
    side=lambda x:x if x in (0,1) else (0 if nm(str(x))==v else 1 if nm(str(x))==h else None)
    rec={'div':dv,'date':date,'time':m.group(4),'rink':g.get('rink',''),'v':v,'h':h,'vs':g['vs'],'hs':g['hs'],'st':g['st'] or 'FINAL',
         'goalies':[[s,]+clean(re.sub(r'\s*\((W|L|T|OTL|SOL)\)$','',x))[:2]+[(re.search(r'\((W|L|T|OTL|SOL)\)$',x) or [None,''])[1]] for s,x in g['goalies']],
         'goals':[[p,t,side(sd),[clean(x) for x in pl],tags] for p,t,sd,pl,tags in g['goals']],
         'pens':[[p,t,side(sd)]+[clean(a[0]) if a and a[0].startswith('#') else ['',a[0].title() if a else '',None]]+[a[1].capitalize() if len(a)>1 else ''] for p,t,sd,a in g['pens']]}
    box[f"{dv}|{g['s']}|{g['id']}"]=rec;n+=1
json.dump(box,open('data/gs_box.json','w'),indent=0,ensure_ascii=False)
print('imported',n,'total',len(box))
