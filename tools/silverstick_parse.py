import re,json
from raw import P,S
RK={'Iroq':'Iroquois Park Sports Centre','McK':'McKinney Centre','Field':'Fieldgate','Can':'Canlan Ice Sports','THCC-W':'THCC-W'}
out={}
for y in P:
    pools={m[0]:[t.strip() for t in m[1].split(',')] for m in re.findall(r'([A-F])\[([^\]]+)\]',P[y])}
    games=[]
    for pm in re.finditer(r'([A-F]):(\S+)',S[y]):
        for g in pm[2].split(','):
            m=re.match(r'(Th|Fr|Sa)(\d+):(\d+)([ap])(.+)=(\d)-(\d)$',g); assert m,g
            h=int(m[2])%12+(12 if m[4]=='p' else 0); h-=1  # Eastern -> Central
            ct=f"{(h-1)%12+1}:{m[3]} {'AM' if h<12 else 'PM'}"
            games.append({'pool':pm[1],'day':{'Th':'Thu','Fr':'Fri','Sa':'Sat'}[m[1]],'ct':ct,'sort':('ThFrSa'.index(m[1])//2)*10000+h*60+int(m[3]),'rink':m[5],'a':pools[pm[1]][int(m[6])-1],'b':pools[pm[1]][int(m[7])-1]})
    for p,ts in pools.items():
        for t in ts: assert sum(1 for g in games if t in (g['a'],g['b']) and g['pool']==p)==4,(y,t)
    assert len(games)==60
    out[y]={'pools':pools,'games':sorted(games,key=lambda g:g['sort'])}
json.dump(out,open('ss.json','w'),indent=0)
print({y:len(out[y]['games']) for y in out})
