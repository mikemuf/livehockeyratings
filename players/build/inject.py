# python3 inject.py <page.html> ["Mon D, YYYY"]  -> writes db.json's data blocks into the page
import json,re,sys
p=sys.argv[1]; h=open(p,encoding='utf8').read(); d=json.load(open('db.json'))
for k in ('T11','T12','T13','T14','T15','C11','C12','C13','C14','C15','S','G','GAMES','LOGS','GLOG'):
    pat=re.compile(r'^const '+k+r'=.*?;[ \t]*(//[^\n]*)?$',re.M)
    assert len(pat.findall(h))==1,k
    h=pat.sub(lambda m:'const '+k+'='+json.dumps(d[k],separators=(',',':'),ensure_ascii=False)+';',h,count=1)
h=h.replace('id:"12-"+i,yr:2012,rank:i+1,','id:"12-"+i,yr:2012,rank:t[2]||i+1,').replace('id:"13-"+i,yr:2013,rank:i+1,','id:"13-"+i,yr:2013,rank:t[2]||i+1,')
# TREC: team games played, from the record in ../data/ratings.json (all divisions except Ontario 2014/2015)
import os
rt=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','data','ratings.json')))
trec={}
# Ontario 2014 and 2015 are left out: their records on the ratings site only count games against rated opponents, not the full season.
for key in ('T11','C11','T12','C12','T13','C13','T14','T15'):
    yy='20'+key[1:]
    for i,t in enumerate(d[key]):
        v=rt.get(yy,{}).get(t[0])
        if v and v.get('rec'): trec[key[1:]+'-'+('C' if key[0]=='C' else '')+str(i)]=sum(int(x) for x in v['rec'].split('-'))
h,n=re.subn(r'^const TREC=.*?;$',lambda m:'const TREC='+json.dumps(trec,separators=(',',':'))+';',h,count=1,flags=re.M); assert n==1,'TREC'
nod=[k for k,v in d['GAMES'].items() if not v]
if len(sys.argv)>2: h,n=re.subn(r'pulled [A-Z][a-z]{2} \d{1,2}, \d{4}','pulled '+sys.argv[2],h); assert n>=1
open(p,'w',encoding='utf8').write(h); print('injected',len(h),'no-data teams',nod)
