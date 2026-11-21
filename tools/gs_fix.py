# after gs_import: map Northeast Pack names to app names per division; convert Eastern game time to Central
import json,re
MAP={'2012':{'New Jersey Rockets':'NJ Rockets','Wolfpack Hockey Club':'Woodbridge Wolfpack','Mid Fairfield':'Mid-Fairfield','Mount St. Charles':'Mount St Charles'},
     '2011':{'New Jersey Rockets':'New Jersey Rockets (Premier)','Wolfpack Hockey Club':'Woodbridge Wolfpack','Mid Fairfield':'Mid-Fairfield Hockey Club (National)','Mount St. Charles':'Mount St Charles Hockey Academy'}}
b=json.load(open('data/gs_box.json'))
for k,x in b.items():
    if '|15483|' in k and x['date']>='2026-11-20':
        m=MAP[x['div']]; x['v']=m.get(x['v'],x['v']); x['h']=m.get(x['h'],x['h'])
        if not x.get('_ct'):
            mm=re.match(r'(\d+):(\d\d) (AM|PM)',x['time'])
            if mm:
                h=int(mm.group(1))%12+(12 if mm.group(3)=='PM' else 0)-1
                x['time']='%d:%s %s'%((h-1)%12+1,mm.group(2),'AM' if h<12 else 'PM'); x['_ct']=1
        print(k,x['v'],x['vs'],x['h'],x['hs'],x['st'],x['time'])
# Other GameSheet seasons (times already Central): season -> {sheet name: app name}
OTHER={'16484':{'St. Louis Aaa Blues':'St Louis Blues','Dallas Stars':'Dallas Stars Elite'},'16444':{'Carshield':'CarShield'},'15464':{'St.louis':'St Louis Blues','St.Louis':'St Louis Blues','ST.LOUIS':'St Louis Blues'}}
for k,x in b.items():
    sid=k.split('|')[1]
    if sid in OTHER:
        m=OTHER[sid]; x['v']=m.get(x['v'],x['v']); x['h']=m.get(x['h'],x['h']); print(k,x['v'],x['vs'],x['h'],x['hs'],x['st'],x['time'])
json.dump(b,open('data/gs_box.json','w'))
