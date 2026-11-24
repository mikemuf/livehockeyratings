import json,re,sys
o=json.load(open('/tmp/nar/ours.json'));now=json.load(open('/tmp/nar/now.json'))
def w(s):
    s=re.sub(r'\b(1[0-6]u|u1[0-6]|aaa|hockey|club|academy|elite|jr\.?|the|premier|national|tier|new jersey|nj)\b',' ',s.lower());s=re.sub(r'\([^)]*\)',' ',s);return set(x for x in re.sub(r'[^a-z0-9 ]',' ',s).split() if len(x)>2)
miss=[]
for l in open('/tmp/nar/mhr.txt'):
    l=l.strip()
    if l.count('|')<2: continue
    y,name,gs=l.split('|',2); tw=w(name)
    # our team name best match
    best=max(now[y],key=lambda t:(len(w(t)&tw)/max(1,len(w(t)|tw))))
    sc=len(w(best)&tw)/max(1,len(w(best)|tw))
    mine=[]
    for d,a,sa,b,sb in o.get(y,[]):
        if a==best: mine.append((d,sa,sb))
        if b==best: mine.append((d,sb,sa))
    na=now[y][best]['na'] if sc>=0.5 else '?'
    for g in filter(None,gs.split(',')):
        m=re.match(r'(\d+)([WLT])(\d+)-(\d+)',g);d=int(m[1]);x,z=int(m[3]),int(m[4])
        gf,ga=(max(x,z),min(x,z)) if m[2]=='W' else (min(x,z),max(x,z)) if m[2]=='L' else (x,z)
        hit=[k for k in mine if abs(k[0]-d)<=1 and k[1]==gf and k[2]==ga]
        if hit: mine.remove(hit[0])
        else: miss.append((y,na,name,best if sc<1 else '',g))
    for k in mine: miss.append((y,na,name,'OURS-ONLY',k))
for m in miss: print(*m,sep=' | ')
print(len(miss))
