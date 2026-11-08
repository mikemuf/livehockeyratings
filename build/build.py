# Rebuild the Live Ratings app: Nov 2 base + Nov 4 MHR anchors + joint 13U/14U pool + games logged since + pending weekend games.
import json,re
h=open('build/base_nov2.html').read()
def getline(name):
    i=h.index('const '+name);j=h.index('\n',i);return i,j
def jconst(name):
    m=re.search(r'const '+name+r'\s*=\s*(\{.*?\}|\[.*?\]);\n',h,re.S);return json.loads(m.group(1))
i,j=getline('BASE ');BASE=json.loads(h[i:j].split('=',1)[1].strip().rstrip(';'))
# --- game edits
for g in BASE:
    for k in (2,4):
        if g[0]=='2012' and g[k]=='Connecticut Jr Rangers (Elite)': g[k]='Connecticut Jr Rangers (National)'
    if g[0]=='2013' and g[1]=='2026-10-05' and 'Woodbridge Wolfpack' in (g[2],g[4]): g[1]='2026-10-04'
teams={dv:{x for g in BASE if g[0]==dv for x in (g[2],g[4])} for dv in ('2012','2013')}
have={(g[0],g[1],frozenset((g[2],g[4]))) for g in BASE}
def add(g,report):
    k=(g[0],g[1],frozenset((g[2],g[4])))
    bad=[t for t in (g[2],g[4]) if t not in teams[g[0]]]
    if bad: report.append(('unknown',g,bad));return
    if k in have and len(g)<7: return
    if g in BASE: return
    BASE.append(g);have.add(k)
rep=[]
add(["2012","2026-11-01","Shattuck St Mary's",9,"Top Gun (Elite)",1],rep)
for f,dv in (('build/games_added_nov3.txt','2012'),('build/games13_added_nov4.txt','2013')):
    for l in open(f):
        d,a,ga,b,gb=l.strip().split('|');add([dv,'2026-'+d,a,int(ga),b,int(gb)],rep)
for g in json.load(open('data/pending_games.json')): add(g,rep)
for r in rep: print(*r)
h=h[:i]+'const BASE = '+json.dumps(BASE)+';'+h[j:]
# --- anchors from Nov 4 rank files
AL=json.load(open('build/aliases.json'))
EXTRA={'2012':{'Tri-Valley Bulls (#1) 14U AA':'Tri-Valley Bulls (14U AA)','West Seneca Wings 14U AA':'West Seneca Wings (14U AA)','Canton Steel 14U AA':'St Lawrence Steel (14U AA)','California Jr Reign (#1) 14U AA':'California Jr Reign (14U AA)','California Bears 14U AA':'California Bears','Great Lakes HC 14U AA':'Great Lakes HC','St Louis Knights 14U AA':'St Louis Knights (14U AA)','Plymouth Flyers (Black) 14U AA':'Plymouth Flyers Black (14U AA)','Hartland Huskies (Black) 14U AA':'Hartland Huskies (Black) (14U AA)','Fairmont Prep (Green) 14U':'Fairmont Prep (Green)','CDA Hockey Academy U15 Prep':'CDA Hockey Academy','Connecticut Jr Rangers (Elite)':'Connecticut Jr Rangers (National)'},
 '2013':{'Saginaw Jr Spirit 13U A':'Saginaw Jr Spirit','Toledo Cherokee 13U AA':'Toledo Cherokee','St Clair Shores Saints (Red) 13U A':'St Clair Shores Saints (Red)','Cheektowaga Warriors (Red) 13U AA':'Cheektowaga Warriors (Red)','Detroit Bulldogs (Gold) 13U A':'Detroit Bulldogs (Gold)','Music City Marauders 13U AA':'Music City Marauders','Cleveland Barons (Eldred)':'Cleveland Barons AA'}}
X={'2012':[("Mauricie Estacades",92.09),("RHA Winnipeg",98.51),("Team Minnesota Red",98.31),("Team Minnesota Blue",97.64),("Minnesota Lakers",94.69),("Kuper Academy",94.07),("Cascades Elite",95.82),("North Shore Winter Club",95.95),("St George's School",94.68),("Long Island Gulls",82.28)],
   '2013':[("Biggby Coffee",82.94),("Red Bank Generals",82.85),("Hartford Jr Wolfpack",82.69),("Palmyra Black Knights",83.99),("Saginaw Jr Spirit (14U AA)",84.93),("Sioux Falls Power",85.48)]}
files={'2012':['nov04_usa14.txt','nov04_on15.txt'],'2013':['nov04_usa13.txt','nov04_on14.txt']}
M={};G={};R={}
for dv,fs in files.items():
    al={**AL[dv],**EXTRA[dv]};M[dv]={};G[dv]={};R[dv]={};um=[]
    for f in fs:
        for l in open('data/'+f):
            p=l.strip().split('|')
            if len(p)<3: continue
            n=al.get(p[0],p[0])
            if n not in teams[dv]: um.append(p[0]);continue
            if n in M[dv]: continue
            w,lo,t=map(int,p[1].split('-'));M[dv][n]=float(p[2]);G[dv][n]=w+lo+t;R[dv][n]=p[1]
    for n,r in X[dv]:
        if n in teams[dv] and n not in M[dv]: M[dv][n]=r;G[dv][n]=0;R[dv][n]='0-0-0'
        elif n not in teams[dv]: print('extra not in app',dv,n)
    print(dv,'anchored',len(M[dv]),'unmatched',len(um),um[:15])
def setline(name,val):
    global h
    i=h.index('const '+name+'=');j=h.index('\n',i);h=h[:i]+'const '+name+'='+json.dumps(val)+';'+h[j:]
setline('MHR_REC',R);setline('MHR_GP',G);setline('MHR',M)
h=re.sub(r"const MHR_THROUGH='[^']*', MHR_PUBLISHED='[^']*';","const MHR_THROUGH='2026-11-03', MHR_PUBLISHED='Nov 4';",h)
# --- joint-pool solver (13U+14U one MHR pool; ignore games vs 15U/16U/18U; dedupe cross-listed 13U-14U games)
a=h.index('function solve(dv,extra){');b=h.index('const f2=x=>x.toFixed(2)',a)
h=h[:a]+open('build/solver.js').read()+h[b:]

# --- UI: movement arrows vs last published MHR rank
def rep(old,new):
    global h
    assert h.count(old)==1,old[:60]; h=h.replace(old,new)
rep("function table(rows,numbered){","function prevRanks(list){const m=MHR[div]||{};const o=list.filter(x=>m[x.t]!==undefined).slice().sort((a,b)=>m[b.t]-m[a.t]);const p={};o.forEach((x,i)=>p[x.t]=i+1);return p}\nfunction mv(prev,now){if(!prev)return '';const d=prev-now;if(!d)return '';return d>0?`<span class=\"mv up\" title=\"Up ${d} from #${prev} in MHR ${MHR_PUBLISHED}\">▲${d}</span>`:`<span class=\"mv dn\" title=\"Down ${-d} from #${prev} in MHR ${MHR_PUBLISHED}\">▼${-d}</span>`}\nfunction table(rows,numbered){const pv=numbered?prevRanks(rows):{};")
rep('<td class="t">${esc(x.t)}</td>','<td class="t">${esc(x.t)}${numbered?mv(pv[x.t],k+1):\'\'}</td>')
rep("<p class=\"legend\">Tap any team for its math page. Canadian teams","<p class=\"legend\"><span class=\"mv up\">▲</span> <span class=\"mv dn\">▼</span> = spots moved since MHR’s last published ratings ('+MHR_PUBLISHED+'), from games applied live. Tap any team for its math page. Canadian teams")
rep("<style>","<style>.mv{font-size:11px;font-weight:700;margin-left:6px;white-space:nowrap}.mv.up{color:#16a34a}.mv.dn{color:#dc2626}")

# --- UI: teams MHR doesn't rate (display only; their games never touch the ratings)
UNR=json.load(open('data/unrated_games.json'))
rep("function renderRank(S){","const UNRATED="+json.dumps(UNR)+";\nfunction unratedTable(){const G=UNRATED.filter(g=>g[0]===div);const known=new Set(cache[div]?cache[div].rows.map(x=>x.t):[]);const T={};G.forEach(g=>{[[2,3,4,5],[4,5,2,3]].forEach(([a,af,b,bf])=>{const t=g[a];if(known.has(t))return;const o=T[t]=T[t]||{w:0,l:0,t:0,gf:0,ga:0,games:[]};const f=g[af],x=g[bf];o.gf+=f;o.ga+=x;f>x?o.w++:f<x?o.l++:o.t++;o.games.push(`${g[1].slice(5)} ${f>x?'W':f<x?'L':'T'} ${f}-${x} vs ${g[b]}`)})});const ks=Object.keys(T).sort((a,b)=>(T[b].w*2+T[b].t)-(T[a].w*2+T[a].t));if(!ks.length)return '';let h=`<h2>Not rated by MHR<span class=\"n\">${ks.length}</span></h2><p class=\"small\">Too few games for an MHR rating (or not an MHR-tracked team). Their games are shown for reference only and don’t change anyone’s rating, same as MHR.</p><div class=\"wrap\"><table><thead><tr><th class=\"t\">Team</th><th>Rec</th><th>GF-GA</th><th>GP</th><th class=\"t\">Games</th></tr></thead><tbody>`;ks.forEach(k=>{const o=T[k];h+=`<tr><td class=\"t\">${esc(k)}</td><td>${o.w}-${o.l}-${o.t}</td><td>${o.gf}-${o.ga}</td><td>${o.games.length}</td><td class=\"t small\">${o.games.map(esc).join('<br>')}</td></tr>`});return h+'</tbody></table></div>'}\nfunction renderRank(S){")
rep("  h+='<p class=\"legend\"><span class=\"mv up\">","  h+=unratedTable();\n  h+='<p class=\"legend\"><span class=\"mv up\">")
open('index.html','w').write(h);print('ok',len(h))
