# python3 prep.py [YYYYMMDD today] -> harvest_run.js, ready to paste into the browser's JavaScript tool
import json,sys,datetime
b=json.load(open('box.json')); w=json.load(open('wanted.json'))
today=datetime.datetime.strptime(sys.argv[1],'%Y%m%d') if len(sys.argv)>1 else datetime.datetime.now()
cut=(today-datetime.timedelta(days=24)).strftime('%Y%m%d')
ids=sorted({i for v in w.values() for i in v},key=int)
d=lambda m:(lambda x:x[2]+x[1]+x[0])(m['h'].split('~')[0].split('.'))
known=sorted(m['id'] for m in b['M'] if d(m)>=cut)
import os
HERE=os.path.dirname(os.path.abspath(__file__))
rec=sorted((m for m in b['M'] if d(m)>=cut),key=lambda m:m['id'])
canary=[rec[-1]['id'],rec[len(rec)//2]['id']] if len(rec)>=2 else [b['M'][-1]['id']]
s=open(os.path.join(HERE,'harvest.template.js')).read().replace('__TEAMS__',','.join(ids)).replace('__KNOWN__',','.join(known)).replace('__CUT__',cut).replace('__CANARY__',','.join(canary))
open('harvest_run.js','w').write(s); print('canary',canary);print('teams',len(ids),'known recent games',len(known),'cutoff',cut,'script chars',len(s))
