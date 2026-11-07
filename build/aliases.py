# Derive MHR-name -> app-name aliases by matching Oct 28 rank files to the Oct 28 anchors in the Nov 2 app.
import json,re,sys
from collections import defaultdict
h=open('build/base_nov2.html').read()
def jconst(name):
    m=re.search(r'const '+name+r'=(\{.*?\});\n',h);return json.loads(m.group(1))
MHR=jconst('MHR');REC=jconst('MHR_REC')
files={'2012':['oct28_usa14.txt','oct28_on15.txt'],'2013':['oct28_usa13.txt','oct28_on14.txt']}
AL={}
for dv,fs in files.items():
    key=defaultdict(list)
    for t,r in MHR[dv].items(): key[(REC[dv].get(t),round(r,2))].append(t)
    al={};miss=[]
    for f in fs:
        for l in open('data/'+f):
            p=l.strip().split('|')
            if len(p)<3: continue
            n,rec,r=p[0],p[1],round(float(p[2]),2)
            c=key.get((rec,r),[])
            if len(c)==1:
                if c[0]!=n: al[n]=c[0]
            else: miss.append((n,len(c)))
    AL[dv]=al;print(dv,'aliases',len(al),'unmatched',len(miss),miss[:8])
json.dump(AL,open('build/aliases.json','w'),indent=1)
