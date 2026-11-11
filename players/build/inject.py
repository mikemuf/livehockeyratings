# python3 inject.py <page.html> ["Mon D, YYYY"]  -> writes db.json's data blocks into the page
import json,re,sys
p=sys.argv[1]; h=open(p,encoding='utf8').read(); d=json.load(open('db.json'))
for k in ('T12','T13','C12','C13','S','G','GAMES','LOGS','GLOG'):
    pat=re.compile(r'^const '+k+r'=.*?;[ \t]*(//[^\n]*)?$',re.M)
    assert len(pat.findall(h))==1,k
    h=pat.sub(lambda m:'const '+k+'='+json.dumps(d[k],separators=(',',':'),ensure_ascii=False)+';',h,count=1)
h=h.replace('id:"12-"+i,yr:2012,rank:i+1,','id:"12-"+i,yr:2012,rank:t[2]||i+1,').replace('id:"13-"+i,yr:2013,rank:i+1,','id:"13-"+i,yr:2013,rank:t[2]||i+1,')
nod=[k for k,v in d['GAMES'].items() if not v]
if len(sys.argv)>2: h,n=re.subn(r'pulled [A-Z][a-z]{2} \d{1,2}, \d{4}','pulled '+sys.argv[2],h); assert n>=1
open(p,'w',encoding='utf8').write(h); print('injected',len(h),'no-data teams',nod)
