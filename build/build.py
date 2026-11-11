# Rebuild the Live Ratings app: Nov 2 base + Nov 4 MHR anchors + joint 13U/14U pool + games logged since + pending weekend games.
import json,sys
sys.path.insert(0,'build');import pool2,re
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
# new teams first seen this weekend (Mike: all games count, MHR records them)
for dv,ns in {'2012':['Edina','OMGHA','Rochester Mustangs'],'2013':['HKMK Bled']}.items(): teams[dv].update(ns)
have={(g[0],g[1],frozenset((g[2],g[4]))) for g in BASE}
def add(g,report):
    if g[0] in ('2014','2015'):
        if g not in BASE: BASE.append(g)
        return
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
for g in json.load(open('data/games_wk_nov6.json')): add(g,rep)
for g in json.load(open('data/games_mhr_fix_nov11.json')): add(g,rep)
for g in json.load(open('data/pending_games.json')): add(g,rep)
P2games,P2X,P2M,P2G,P2R,P2CA=pool2.build()
BASE.extend(P2games);print('pool2 games',len(P2games))
# cross-age opponents in 2014/2015 pending games: 'Name (12U)' in a 2015 game / 'Name (11U)' in a 2014 game
for g in json.load(open('data/games_wk_nov6.json'))+json.load(open('data/games_mhr_fix_nov11.json'))+json.load(open('data/pending_games.json')):
    if g[0] not in ('2014','2015'): continue
    for n in (g[2],g[4]):
        for suf,dv in ((' (12U)','2014'),(' (11U)','2015')):
            if n.endswith(suf) and dv!=g[0]: P2X.setdefault(g[0],{})[n]=dv+'|'+n[:-len(suf)]
for r in rep: print(*r)
h=h[:i]+'const BASE = '+json.dumps(BASE)+';'+h[j:]
# --- anchors from Nov 4 rank files
AL=json.load(open('build/aliases.json'))
EXTRA={'2012':{'Tri-Valley Bulls (#1) 14U AA':'Tri-Valley Bulls (14U AA)','West Seneca Wings 14U AA':'West Seneca Wings (14U AA)','Canton Steel 14U AA':'St Lawrence Steel (14U AA)','California Jr Reign (#1) 14U AA':'California Jr Reign (14U AA)','California Bears 14U AA':'California Bears','Great Lakes HC 14U AA':'Great Lakes HC','St Louis Knights 14U AA':'St Louis Knights (14U AA)','Plymouth Flyers (Black) 14U AA':'Plymouth Flyers Black (14U AA)','Hartland Huskies (Black) 14U AA':'Hartland Huskies (Black) (14U AA)','Fairmont Prep (Green) 14U':'Fairmont Prep (Green)','CDA Hockey Academy U15 Prep':'CDA Hockey Academy','Connecticut Jr Rangers (Elite)':'Connecticut Jr Rangers (National)'},
 '2013':{'Saginaw Jr Spirit 13U A':'Saginaw Jr Spirit','Toledo Cherokee 13U AA':'Toledo Cherokee','St Clair Shores Saints (Red) 13U A':'St Clair Shores Saints (Red)','Cheektowaga Warriors (Red) 13U AA':'Cheektowaga Warriors (Red)','Detroit Bulldogs (Gold) 13U A':'Detroit Bulldogs (Gold)','Music City Marauders 13U AA':'Music City Marauders','Cleveland Barons (Eldred)':'Cleveland Barons AA'}}
X={'2012':[("Mauricie Estacades",92.09),("RHA Winnipeg",98.51),("Team Minnesota Red",98.31),("Team Minnesota Blue",97.64),("Minnesota Lakers",94.69),("Kuper Academy",94.07),("Cascades Elite",95.82),("North Shore Winter Club",95.95),("St George's School",94.68),("Long Island Gulls",82.28)],
   '2013':[("Biggby Coffee",82.94),("Red Bank Generals",82.85),("Hartford Jr Wolfpack",82.69),("Palmyra Black Knights",83.99),("Saginaw Jr Spirit (14U AA)",84.93),("Sioux Falls Power",85.48)]}
files={'2012':['nov11_usa14.txt','nov11_on15.txt'],'2013':['nov11_usa13.txt','nov11_on14.txt']}
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
M.update(P2M);G.update(P2G);R.update(P2R)
setline('MHR_REC',R);setline('MHR_GP',G);setline('MHR',M)
h=re.sub(r"const MHR_THROUGH='[^']*', MHR_PUBLISHED='[^']*';","const MHR_THROUGH='2026-11-10', MHR_PUBLISHED='Nov 11';",h)
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
rep("function renderRank(S){","const UNRATED="+json.dumps(UNR)+";\nfunction unratedTable(){const S=cache[div];const G=UNRATED.filter(g=>g[0]===div);const known=new Set(S?S.rows.map(x=>x.t):[]);const T={};G.forEach(g=>{[[2,3,4,5],[4,5,2,3]].forEach(([a,af,b,bf])=>{const t=g[a];if(known.has(t))return;const o=T[t]=T[t]||{w:0,l:0,t:0,gf:0,ga:0,games:[],d:[],op:[]};const f=g[af],x=g[bf];o.gf+=f;o.ga+=x;f>x?o.w++:f<x?o.l++:o.t++;const opp=S&&S.byName[g[b]];if(opp){o.d.push(Math.max(-7,Math.min(7,f-x)));o.op.push(opp.r)}o.games.push(`${g[1].slice(5)} ${f>x?'W':f<x?'L':'T'} ${f}-${x} vs ${g[b]}${opp?' ('+f2(opp.r)+')':''}`)})});const ks=Object.keys(T);ks.forEach(k=>{const o=T[k],n=o.d.length;o.agd=n?o.d.reduce((a,b)=>a+b,0)/n:null;o.sch=n?o.op.reduce((a,b)=>a+b,0)/n:null;o.r=n?o.agd+o.sch:null});ks.sort((a,b)=>(T[b].r??-1e9)-(T[a].r??-1e9));if(!ks.length)return '';let h=`<h2>Under 5 games — rating not published by MHR<span class=\"n\">${ks.length}</span></h2><p class=\"small\">MHR keeps a rating for these teams but doesn’t publish it until 5 games. Estimated here with MHR’s formula (average goal differential, capped at ±7, plus average opponent rating) from the games below. Display only: these games don’t change any other team’s rating.</p><div class=\"wrap\"><table><thead><tr><th class=\"t\">Team</th><th>Rating</th><th>Rec</th><th>AGD</th><th>Sched</th><th>GP</th><th class=\"t\">Games</th></tr></thead><tbody>`;ks.forEach(k=>{const o=T[k];h+=`<tr><td class=\"t\">${esc(k)}</td><td class=\"rating\"><span class=\"num\">${o.r==null?'—':f2(o.r)}</span></td><td>${o.w}-${o.l}-${o.t}</td><td class=\"${(o.agd??0)>=0?'pos':'neg'}\">${o.agd==null?'':fs(o.agd)}</td><td>${o.sch==null?'':f2(o.sch)}</td><td>${o.games.length}</td><td class=\"t small\">${o.games.map(esc).join('<br>')}</td></tr>`});return h+'</tbody></table></div>'}\nfunction renderRank(S){")
rep("  h+='<p class=\"legend\"><span class=\"mv up\">","  h+=unratedTable();\n  h+='<p class=\"legend\"><span class=\"mv up\">")

# --- 2014 (USA 12U) and 2015 (USA 11U) "lite" divisions: anchored to MHR rank pages, live games folded in
def liteload(fn,skip):
    out={}
    for line in open(fn):
        p=line.strip().split('|')
        if len(p)<5 or skip in p[0]: continue
        w,l,t=map(int,p[1].split('-'));out[p[0]]=[float(p[2]),w,l,t,float(p[3]),float(p[4])]
    return out
LITE={}
h=h.replace("(MHR_REC[div]||{})[x.t]||x.rec.join('-')","(((MHR_REC[div]||{})[x.t]||'0-0-0')!=='0-0-0'?MHR_REC[div][x.t]:x.rec.join('-'))")
h=h.replace('const XPOOL=','Object.assign(XMAP,'+json.dumps(P2X)+');\nconst XPOOL=',1)
h=h.replace('CANADA_BASE = [','CANADA_BASE = ['+','.join(json.dumps(x) for x in P2CA)+(',' if P2CA else ''),1)
h=h.replace('const BASE = ','const LITE='+json.dumps(LITE)+';\nconst BASE = ',1)
i=h.index('const MHR=');j=h.index('\n',i);mh=json.loads(h[i+len('const MHR='):j].rstrip(';'))
for dv in LITE: mh[dv]={t:a[0] for t,a in LITE[dv].items()}
h=h[:i]+'const MHR='+json.dumps(mh)+';'+h[j:]
rep('<button data-div="2013">2013 Minor</button>','<button data-div="2013">2013 Minor</button><button data-div="2014">2014 Major</button><button data-div="2015">2015 Minor</button>')
rep('<option value="2013">2013 Bantam Minor</option>','<option value="2013">2013 Bantam Minor</option><option value="2014">2014 Peewee Major (12U)</option><option value="2015">2015 Peewee Minor (11U)</option>')
rep('<small>2026-27 Bantam</small>','<small>2026-27 Bantam &amp; Peewee</small>')
rep('<style>','<style>.bar{flex-wrap:wrap;row-gap:6px}@media (max-width:560px){.seg{margin-left:0;width:100%}.seg button{flex:1;padding:6px 4px}}')
h=h.replace("div==='2012'?'2012 Bantam Major':'2013 Bantam Minor'","({'2012':'2012 Bantam Major','2013':'2013 Bantam Minor','2014':'2014 Peewee Major (12U)','2015':'2015 Peewee Minor (11U)'})[div]")
# --- public site: Weekend tab; hide internal tabs (Schedule, Add scores, Handoff)
WK=json.load(open('data/weekend_public.json'))
WG=[g[:6] for g in json.load(open('data/games_wk_nov6.json'))+json.load(open('data/pending_games.json')) if WK['from']<=g[1]<=WK['to']]
rep('  <button data-view="sched">Schedule</button>\n','')
rep('  <button data-view="add">Add scores</button>\n','')
rep('  <button data-view="export">Handoff</button>\n','')
rep('<button data-view="rank" class="on">USA</button>','<button data-view="rank" class="on">USA</button>\n  <button data-view="wk">Weekend</button>')
rep(' <section class="view" id="v-can"></section>',' <section class="view" id="v-wk"></section>\n <section class="view" id="v-can"></section>')
rep("let cache={};","const WEEKEND="+json.dumps(WK)+";\nconst WEEKEND_GAMES="+json.dumps(WG)+";\n"+open('build/weekend.js').read()+"let cache={};")
rep("  if(view==='can')","  if(view==='wk')document.getElementById('v-wk').innerHTML=renderWeekend(S);\n  if(view==='can')")
rep('<style>','<style>ul.wk{margin:8px 0 0;padding-left:18px}ul.wk li{margin:6px 0;line-height:1.4}table.wkg{width:100%;border-collapse:collapse;table-layout:fixed}table.wkg td:first-child{width:84px}table.wkg td{overflow-wrap:anywhere;white-space:normal;text-align:left;background:none}table.wkg{border:0}table.wkg td{padding:6px 4px;border-top:1px solid rgba(128,128,128,.2);vertical-align:top;text-align:left}.wkd{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.04em;opacity:.65;margin:12px 0 2px}.wkr{display:grid;grid-template-columns:1fr auto;gap:2px 10px;padding:7px 0;border-top:1px solid rgba(128,128,128,.2);text-align:left}.wkr .sc{text-align:right;font-weight:600}')
# --- links between the ratings site and the player database (players/): each team page links to its roster,
#     and a link like #team=2012|Chicago Mission (used by the player database) opens that team's page.
PT=json.load(open('players/data/teams.json'));PDB={}
for k,t in PT.items(): PDB.setdefault(str(t['yr']),{})[t['name']]=k
rep("<a class=\"back\" id=\"tog-ca\">${canada.has(x.t)?'Move to USA':'Move to Canada'}</a></p></div>`;",
    "<a class=\"back\" id=\"tog-ca\">${canada.has(x.t)?'Move to USA':'Move to Canada'}</a></p>${(PDB[div]||{})[x.t]?`<p style=\"margin:12px 0 0\"><a class=\"plink\" style=\"padding:0\" href=\"players/#team=${PDB[div][x.t]}\">Roster and player stats &rsaquo;</a></p>`:''}</div>`;")
rep("let cache={};","const PDB="+json.dumps(PDB)+";\nlet cache={};")
rep("\nrender();\n</script>","\nfunction fromHash(){let m=null;try{m=decodeURIComponent(location.hash).match(/^#team=(\\d{4})\\|(.+)$/)}catch(e){}if(!m)return;div=m[1];selTeam=m[2];view='team'}\nwindow.addEventListener('hashchange',()=>{fromHash();render();window.scrollTo(0,0)});\nfromHash();render();\n</script>")
open('index.html','w').write(h);print('ok',len(h))
