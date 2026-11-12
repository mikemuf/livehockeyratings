// node make_preview.js <players/index.html> <players/data/box.json> <out preview/index.html>
// Builds the public preview site: top five skaters per birth year with full profiles, everything else locked,
// plus a demonstration of the membership flow. Only the previewed players' stats are written into the page;
// the search index carries names, teams and birth years only.
const fs=require('fs');
const [src,boxf,out]=process.argv.slice(2);
const html=fs.readFileSync(src,'utf8');
const js=html.match(/<script>([\s\S]*?)<\/script>/)[1];
const el=()=>({innerHTML:'',textContent:'',value:'',hidden:false,setAttribute(){},showModal(){},close(){},addEventListener(){},dataset:{}});
const els={};const document={getElementById:id=>els[id]||(els[id]=el()),addEventListener(){}};
const D=new Function('document','location','window',js+';return {skaters,goalies,TEAMS,loaded,MINGP,mult,mmss}')(document,{hash:''},{addEventListener(){}});
const games=JSON.parse(fs.readFileSync(boxf,'utf8')).M.length;
const pulled=(html.match(/pulled ([A-Z][a-z]{2} \d{1,2}, \d{4})/)||[])[1]||'';
const YEARS=[2011,2012,2013,2014,2015];
const r2=x=>Math.round(x*100)/100;
const pack=s=>({n:s.name,num:s.num,t:s.team.name,ty:s.team.yr,ca:s.team.ca?1:0,tr:s.team.rank,trt:s.team.rating,pos:s.pos,by:s.by,gp:s.gp,g:s.g,a:s.a,p:s.p,
  ppp:s.ppp,ppgl:s.ppgl,ppa:s.ppa,inv:Math.round(s.inv),tgf:s.tgf,pm:s.pm,pim:s.pim,toig:Math.round(s.toig),pptg:Math.round(s.pptg),ppg:r2(s.ppg),adj:r2(s.adj),p60:r2(s.p60),adj60:r2(s.adj60),opp:r2(s.opp),
  rk:s.trank,tn:s.tn,t1:r2(s.t1),t2:r2(s.t2),t5:r2(s.t5),
  log:s.log.map(l=>[l.date,l.ha,l.opp,l.or?r2(l.or):0,l.score,l.toi,l.g,l.a,l.ppp,l.pm,l.or?r2(l.m):0])});
const P={},LOCK={};
for(const y of YEARS){const q=D.skaters.filter(s=>s.by===y&&s.q).sort((a,b)=>b.adj-a.adj);P[y]=q.slice(0,5).map(pack);LOCK[y]=D.skaters.filter(s=>s.by===y).length-5}
const seen=new Set();const IDX=[];
for(const s of D.skaters){const k=s.name+'|'+s.team.name+'|'+s.team.yr;if(seen.has(k))continue;seen.add(k);IDX.push([s.name,s.team.name,s.team.yr,s.by,0])}
for(const g of D.goalies){const k=g.name+'|'+g.team.name+'|'+g.team.yr+'|G';if(seen.has(k))continue;seen.add(k);IDX.push([g.name,g.team.name,g.team.yr,g.by,1])}
IDX.sort((a,b)=>a[0].localeCompare(b[0]));
// Hub sections: live team ratings (top ten USA teams per birth year) and the weekend preview/recap from the ratings site.
const path=require('path');const root=path.resolve(path.dirname(src),'..');
const RT=JSON.parse(fs.readFileSync(path.join(root,'players/data/ratings.json'),'utf8'));
const WKD=JSON.parse(fs.readFileSync(path.join(root,'data/weekend_public.json'),'utf8'));
const TOP={};for(const y of YEARS){TOP[y]=Object.entries(RT[y]||{}).filter(([n,v])=>v.pool==='USA'&&v.rank>0).sort((a,b)=>a[1].rank-b[1].rank).slice(0,10).map(([n,v])=>[v.rank,n,v.rec||'',v.rating])}
const NT={};for(const y of YEARS)NT[y]=Math.max(0,Object.keys(RT[y]||{}).length-10);
const rkOf=(y,n)=>{const v=(RT[y]||{})[n];return v&&v.rank?(v.pool==='USA'?'#':'ON #')+v.rank:''};
const WK={label:WKD.label,status:WKD.status,updated:WKD.updated,divs:{}};
for(const y of YEARS){const d=(WKD.divs||{})[y];if(!d)continue;WK.divs[y]={s:(d.summary||[]).slice(0,4),w:(d.watch||[]).slice(0,6).map(g=>[g[0],g[1],g[2],rkOf(y,g[2]),g[3],rkOf(y,g[3]),g[4]||''])}}
const STATS={sk:D.skaters.length,gk:D.goalies.length,teams:D.loaded.size,games,pulled,min:D.MINGP};
const esc=s=>String(s).replace(/</g,'\\u003c');
const page=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Live ratings, weekend reports and the player database: preview</title>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Layout: demo ribbon, dark hero, stat strip, preview leaderboard (5 open rows + locked rows), player finder, pricing, footer. Dialogs for profile and the membership flow. */
:root{--bg:#f3f6f8;--panel:#fff;--ink:#14212b;--muted:#5b6b78;--line:#d5dde3;--accent:#0d5c8f;--accent-ink:#fff;--red:#b3262d;--soft:#e6eef3;--night:#0c1a24;--night2:#12283a;--gold:#f4d35e;--good:#1b7a4a;
 --b11:#f6c9c4;--b11-ink:#6e1a12;--b12:#f4d35e;--b12-ink:#4a3800;--b13:#a9dfbf;--b13-ink:#0f4d2a;--b14:#b8d4f1;--b14-ink:#0b3a66;--b15:#e3c8ee;--b15-ink:#4b1e63;
 --display:"Barlow Condensed","Arial Narrow",sans-serif;--body:"IBM Plex Sans",system-ui,sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--body);font-size:16px;line-height:1.5}
button{font:inherit;cursor:pointer}a{color:inherit}
.demo{background:var(--gold);color:#3a2c00;font-size:13px;text-align:center;padding:7px 14px}
.top{background:var(--night);color:#e9f1f6;position:sticky;top:0;z-index:5;border-bottom:3px solid var(--red)}
.top .in{max-width:1100px;margin:0 auto;padding:10px 16px;display:flex;align-items:center;gap:8px 18px;flex-wrap:wrap}
.brand{font-family:var(--display);font-weight:700;font-size:24px;letter-spacing:.03em;text-transform:uppercase;line-height:1}
.brand span{color:var(--gold)}
.top nav{margin-left:auto;display:flex;gap:6px 16px;align-items:center;flex-wrap:wrap}
.top nav a{text-decoration:none;font-weight:500;font-size:15px;opacity:.9}
.btn{border:0;border-radius:6px;padding:10px 18px;font-weight:600;background:var(--red);color:#fff}
.btn.alt{background:transparent;color:inherit;border:1px solid currentColor}
.btn.big{font-size:18px;padding:13px 26px}
.hero{background:linear-gradient(160deg,var(--night) 0%,var(--night2) 100%);color:#e9f1f6}
.hero .in{max-width:1100px;margin:0 auto;padding:54px 16px 46px}
.hero h1{font-family:var(--display);font-weight:700;text-transform:uppercase;font-size:clamp(40px,7vw,72px);line-height:.95;margin:0 0 16px;letter-spacing:.01em;max-width:15ch}
.hero h1 em{font-style:normal;color:var(--gold)}
.hero p{max-width:58ch;font-size:18px;margin:0 0 24px;color:#c5d3dd}
.hero .cta{display:flex;gap:12px;flex-wrap:wrap}
.strip{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:1px;background:#24394a;border-top:1px solid #24394a}
.strip div{background:var(--night);padding:16px;text-align:center}
.strip b{display:block;font-family:var(--display);font-size:34px;line-height:1;color:#fff}
.strip span{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#93a9b8}
section{max-width:1100px;margin:0 auto;padding:44px 16px 8px}
h2{font-family:var(--display);font-weight:700;text-transform:uppercase;font-size:34px;letter-spacing:.02em;margin:0 0 6px;line-height:1}
.lede{color:var(--muted);margin:0 0 18px;max-width:70ch}
.tabs{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}
.tab{border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:6px;padding:7px 14px;font-family:var(--display);font-size:19px;text-transform:uppercase;letter-spacing:.04em}
.tab[aria-pressed="true"]{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
.sheet{background:var(--panel);border:1px solid var(--line);border-radius:8px;overflow-x:auto;position:relative}
table{border-collapse:collapse;width:100%;min-width:760px;font-variant-numeric:tabular-nums}
th,td{padding:9px 10px;text-align:right;white-space:nowrap;border-bottom:1px solid var(--line);font-size:14px}
th{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);background:var(--soft)}
th:nth-child(2),td:nth-child(2),th:nth-child(3),td:nth-child(3){text-align:left}
tr.open{cursor:pointer}tr.open:hover td{background:var(--soft)}
.name{font-weight:600}.sub{color:var(--muted);font-size:12px}
.born{display:inline-block;font-size:11px;font-weight:600;border-radius:4px;padding:1px 6px;margin-left:4px}
.b11{background:var(--b11);color:var(--b11-ink)}.b12{background:var(--b12);color:var(--b12-ink)}.b13{background:var(--b13);color:var(--b13-ink)}.b14{background:var(--b14);color:var(--b14-ink)}.b15{background:var(--b15);color:var(--b15-ink)}
tr.lock td{color:transparent;user-select:none}
tr.lock td span.bar{display:inline-block;height:10px;border-radius:5px;background:var(--line);vertical-align:middle}
.gate{position:absolute;left:0;right:0;bottom:0;height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;text-align:center;padding:16px;background:linear-gradient(180deg,rgba(255,255,255,0) 0%,var(--panel) 38%)}
.gate b{font-family:var(--display);font-size:26px;text-transform:uppercase;letter-spacing:.02em}
.gate p{margin:0;color:var(--muted);max-width:44ch}
.grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:18px}
.card h3{font-family:var(--display);font-size:22px;text-transform:uppercase;letter-spacing:.03em;margin:0 0 6px}
.card p{margin:0;color:var(--muted);font-size:15px}
.find{display:flex;gap:8px;flex-wrap:wrap}
.find input{flex:1;min-width:220px;font:inherit;padding:12px 14px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink)}
.hits{margin-top:10px;display:grid;gap:8px}
.hit{display:flex;gap:10px 14px;align-items:center;flex-wrap:wrap;background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:12px 14px}
.hit .who{flex:1;min-width:200px}
.plans{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px;max-width:760px}
.plan{background:var(--panel);border:2px solid var(--line);border-radius:10px;padding:22px;display:flex;flex-direction:column;gap:8px}
.plan.best{border-color:var(--red)}
.plan .tag{align-self:flex-start;background:var(--red);color:#fff;font-size:12px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;border-radius:4px;padding:2px 8px}
.plan h3{font-family:var(--display);font-size:26px;text-transform:uppercase;margin:0}
.price{font-family:var(--display);font-size:54px;font-weight:700;line-height:1}
.price small{font-family:var(--body);font-size:15px;font-weight:400;color:var(--muted)}
.plan ul{margin:6px 0 12px;padding-left:18px;color:var(--muted);font-size:15px}
footer{max-width:1100px;margin:0 auto;padding:36px 16px 60px;color:var(--muted);font-size:13px}
dialog{border:0;border-radius:10px;padding:0;width:min(880px,94vw);max-height:90vh;color:var(--ink);background:var(--panel)}
dialog::backdrop{background:rgba(8,16,22,.6)}
.dl{padding:22px}
.dl h2{font-size:30px}
.x{float:right;border:1px solid var(--line);background:var(--panel);border-radius:6px;padding:4px 10px;color:var(--ink)}
.kv{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:8px;margin:10px 0 16px}
.kv div{background:var(--soft);border-radius:6px;padding:8px 10px}
.kv span{display:block;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.kv b{font-family:var(--display);font-size:24px}
.dl h3{font-family:var(--display);text-transform:uppercase;letter-spacing:.04em;font-size:18px;margin:16px 0 4px;color:var(--muted)}
.steps{display:flex;gap:6px;margin:0 0 16px;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:var(--muted)}
.steps span{flex:1;border-top:3px solid var(--line);padding-top:6px}
.steps span.on{border-color:var(--red);color:var(--ink);font-weight:600}
label{display:block;font-size:13px;font-weight:600;margin:10px 0 4px}
.dl input[type=text],.dl input[type=email]{width:100%;font:inherit;padding:11px 12px;border:1px solid var(--line);border-radius:6px;background:var(--panel);color:var(--ink)}
.dl input:disabled{background:var(--soft);color:var(--muted)}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.note{background:#fff7d6;color:#4a3800;border-radius:6px;padding:10px 12px;font-size:14px;margin:12px 0}
.choice{display:flex;gap:12px;align-items:center;border:2px solid var(--line);border-radius:8px;padding:12px 14px;margin-bottom:8px;cursor:pointer}
.choice[aria-pressed="true"]{border-color:var(--red)}
.choice b{font-family:var(--display);font-size:24px}
.acts{display:flex;gap:10px;justify-content:flex-end;margin-top:16px;flex-wrap:wrap}
.acts .btn.alt{color:var(--ink)}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
@media (max-width:640px){.hero .in{padding:36px 16px 30px}.top nav a.hide{display:none}}
</style></head><body>
<div class="demo">Preview build for demonstration. Accounts and payments are not active, and nothing you type on this page is saved or sent.</div>
<div class="top"><div class="in"><div class="brand">Player Database <span>Premium</span></div>
<nav><a class="hide" href="#ratings">Live ratings</a><a class="hide" href="#weekend">This weekend</a><a class="hide" href="#preview">Players</a><a class="hide" href="#find">Find a player</a><a class="hide" href="#pricing">Pricing</a><button class="btn alt" data-act="signin">Sign in</button><button class="btn" data-act="join">Become a member</button></nav></div></div>
<div class="hero"><div class="in">
<h1>Live ratings. <em>Every top player.</em> Every weekend, in one place.</h1>
<p>Team ratings that move as scores come in, a preview and recap of every weekend, and game-by-game stats for AAA players born 2011 through 2015. See where your player stands today, and measure his development all season.</p>
<div class="cta"><button class="btn big" data-act="join">Become a member</button><a class="btn big alt" href="#ratings" style="text-decoration:none">See the preview</a></div>
</div>
<div class="strip"><div><b id="s-sk"></b><span>Skaters</span></div><div><b id="s-gk"></b><span>Goalies</span></div><div><b id="s-tm"></b><span>Teams</span></div><div><b id="s-gm"></b><span>Games logged</span></div><div><b>5</b><span>Birth years</span></div><div><b>Daily</b><span>Updates</span></div></div></div>

<section id="ratings"><h2>Live team ratings</h2>
<p class="lede">No waiting for a weekly release. Ratings move as each score is entered, so you know where a team stands before the weekend is over. Top ten USA teams shown here.</p>
<div class="tabs ytabs"></div>
<div class="sheet"><table><thead><tr><th>#</th><th>Team</th><th>Record</th><th>Rating</th></tr></thead><tbody id="rt"></tbody></table>
<div class="gate"><b id="rt-n"></b><p>The full live ratings are for members: every team, USA and Canada, with schedule strength, game-by-game results and each roster's player stats.</p><button class="btn" data-act="join">Become a member</button></div></div>
</section>

<section id="weekend"><h2>This weekend</h2>
<p class="lede"><span id="wk-label"></span>. A preview of the games that matter before the weekend, then a recap of what happened: upsets, big moves in the rankings and tournament results.</p>
<div class="tabs ytabs"></div>
<div id="wk"></div>
</section>

<section id="preview"><h2>Top five players, by birth year</h2>
<p class="lede">These five profiles are open in full: tap a name to see every stat and the complete game log. Ranked by Adjusted Points per Game, which weights each game's points by the opponent's rating. Minimum <span id="s-min"></span> games.</p>
<div class="tabs ytabs"></div>
<div class="sheet"><table><thead><tr><th>#</th><th>Player</th><th>Team</th><th>Pos</th><th>GP</th><th>G</th><th>A</th><th>P</th><th>PPP</th><th>INV%</th><th>P/G</th><th>Adj P/G</th><th>Avg opp</th></tr></thead><tbody id="tb"></tbody></table>
<div class="gate"><b id="gate-n"></b><p>Full rankings, every profile and every game log are for members.</p><button class="btn" data-act="join">Become a member</button></div></div>
</section>

<section><h2>What members get</h2><p class="lede">The same view a scout or advisor would build by hand, already done for every player.</p>
<div class="grid3">
<div class="card"><h3>Adjusted scoring</h3><p>Points against a top-five team count for more than points against a team ranked fiftieth. Every game is weighted by the opponent's rating, so players on hard schedules get proper credit.</p></div>
<div class="card"><h3>Full game logs</h3><p>Each player's line for every game: ice time, goals, assists, power-play points, plus/minus, with the opponent's rating and rank beside it.</p></div>
<div class="card"><h3>Involvement</h3><p>The share of his team's goals a player had a hand in, and how he compares with his own teammates. It separates the players who drive a team from the ones riding along.</p></div>
<div class="card"><h3>Power play and ice time</h3><p>Power-play points, power-play minutes and time on ice per game, so you can see how a player is used, not only what he scored.</p></div>
<div class="card"><h3>Goalies</h3><p>Goals against per game, adjusted for the opponents each goalie actually faced, with the average rating of those opponents.</p></div>
<div class="card"><h3>Team ratings</h3><p>Every roster links to that team's rating, rank and schedule strength, updated as results come in.</p></div>
</div></section>

<section id="find"><h2>Is your player in the database?</h2><p class="lede">Search by name. Members can open the full profile.</p>
<div class="find"><input id="q" type="text" placeholder="Type a player's name" autocomplete="off" aria-label="Player name"></div><div class="hits" id="hits"></div></section>

<section id="pricing"><h2>Membership</h2><p class="lede">Live ratings, weekend reports and full access to every birth year and every player profile, updated daily as games come in.</p>
<div class="plans">
<div class="plan best"><span class="tag">Best value</span><h3>Season pass</h3><div class="price">$99 <small>one payment</small></div><ul><li>The full 2026-27 season</li><li>Every birth year, 2011 to 2015</li><li>Skaters, goalies and team ratings</li><li>Live ratings and weekend reports</li><li>Player stats updated daily as games come in</li></ul><button class="btn" data-act="join" data-plan="season">Get the season pass</button></div>
<div class="plan"><h3>Monthly</h3><div class="price">$29 <small>per month</small></div><ul><li>Everything in the season pass</li><li>Billed monthly</li><li>Cancel any time</li></ul><button class="btn alt" style="color:var(--ink)" data-act="join" data-plan="monthly">Start monthly</button></div>
</div></section>

<footer>Stats run through <span id="s-date"></span>. Team ratings are live; player stats are refreshed as games are posted. This page is a preview; membership is not yet open.</footer>

<dialog id="prof"><div class="dl" id="prof-in"></div></dialog>
<dialog id="flow"><div class="dl" id="flow-in"></div></dialog>
<script>
const P=${esc(JSON.stringify(P))};
const LOCK=${JSON.stringify(LOCK)};
const IDX=${esc(JSON.stringify(IDX))};
const STATS=${JSON.stringify(STATS)};
const TOP=${esc(JSON.stringify(TOP))};
const NT=${JSON.stringify(NT)};
const WK=${esc(JSON.stringify(WK))};
const $=id=>document.getElementById(id);
const esc=s=>String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const mmss=s=>Math.floor(s/60)+":"+String(Math.round(s%60)).padStart(2,"0");
const fmt=n=>n.toLocaleString("en-US");
$("s-sk").textContent=fmt(STATS.sk);$("s-gk").textContent=fmt(STATS.gk);$("s-tm").textContent=fmt(STATS.teams);$("s-gm").textContent=fmt(STATS.games);$("s-min").textContent=STATS.min;$("s-date").textContent=STATS.pulled;
let year=2012;
function tabs(){const h=Object.keys(P).map(y=>'<button class="tab" aria-pressed="'+(+y===year)+'" data-y="'+y+'">'+y+' born</button>').join("");document.querySelectorAll(".ytabs").forEach(e=>e.innerHTML=h);hub()}
function hub(){$("rt").innerHTML=(TOP[year]||[]).map(r=>'<tr><td>'+r[0]+'</td><td style="text-align:left"><span class="name">'+esc(r[1])+'</span></td><td>'+r[2]+'</td><td><b>'+r[3].toFixed(2)+'</b></td></tr>').join("")+Array.from({length:5},(_,k)=>'<tr class="lock" aria-hidden="true"><td>'+(k+11)+'</td>'+[150,50,44].map((v,j)=>'<td><span class="bar" style="width:'+Math.round(v*(0.7+((k*7+j*3)%5)/10))+'px"></span></td>').join("")+'</tr>').join("");
  $("rt-n").textContent=fmt(NT[year])+" more "+year+" teams";$("wk-label").textContent=WK.label+(WK.status?" ("+WK.status.toLowerCase()+")":"");
  const d=WK.divs[year];
  $("wk").innerHTML=d?'<div class="card"><h3>The story</h3>'+d.s.map(t=>'<p style="margin:0 0 10px">'+esc(t)+'</p>').join("")+'</div>'+(d.w.length?'<div class="sheet" style="margin-top:12px"><table><thead><tr><th>Day</th><th>Time</th><th>Games to watch</th><th>Rink</th></tr></thead><tbody>'+d.w.map(g=>'<tr><td>'+esc(g[0])+'</td><td>'+esc(g[1])+'</td><td style="text-align:left"><b>'+esc(g[2])+'</b>'+(g[3]?' <span class="sub">('+g[3]+')</span>':'')+' vs <b>'+esc(g[4])+'</b>'+(g[5]?' <span class="sub">('+g[5]+')</span>':'')+'</td><td style="text-align:left">'+esc(g[6])+'</td></tr>').join("")+'</tbody></table></div>':''):'<div class="card"><p style="margin:0">The weekend report for this birth year is being added.</p></div>'}
function table(){const rows=P[year];const w=[30,120,110,18,18,14,14,18,16,26,30,34,30];
  $("tb").innerHTML=rows.map((x,i)=>'<tr class="open" tabindex="0" data-i="'+i+'"><td>'+(i+1)+'</td><td><span class="name">'+esc(x.n)+'</span> <span class="sub">#'+x.num+'</span><span class="born b'+(x.by%100)+'">'+x.by+' born</span></td><td>'+esc(x.t)+' <span class="sub">'+x.ty+(x.ca?" ON":"")+'</span></td><td>'+x.pos+'</td><td>'+x.gp+'</td><td>'+x.g+'</td><td>'+x.a+'</td><td><b>'+x.p+'</b></td><td>'+x.ppp+'</td><td>'+x.inv+'%</td><td>'+x.ppg.toFixed(2)+'</td><td><b>'+x.adj.toFixed(2)+'</b></td><td>'+x.opp.toFixed(1)+'</td></tr>').join("")
   +Array.from({length:7},(_,k)=>'<tr class="lock" aria-hidden="true"><td>'+(k+6)+'</td>'+w.slice(1).map((v,j)=>'<td><span class="bar" style="width:'+Math.round(v*(0.7+((k*7+j*3)%5)/10))+'px"></span></td>').join("")+'</tr>').join("");
  $("gate-n").textContent=fmt(LOCK[year])+" more "+year+"-born players";}
function profile(x){const kv=(l,v)=>'<div><span>'+l+'</span><b>'+v+'</b></div>';
  $("prof-in").innerHTML='<button class="x" data-close>Close</button><h2>'+esc(x.n)+' <span class="born b'+(x.by%100)+'" style="font-family:var(--body);vertical-align:middle">'+x.by+' born</span></h2><p class="lede">#'+x.num+' · '+x.pos+' · '+esc(x.t)+' '+x.ty+(x.ca?" (Ontario)":"")+' · team ranked '+(x.ca?"Canada ":"USA ")+'#'+x.tr+' ('+x.trt.toFixed(2)+')</p>'
   +'<div class="kv">'+kv("Games",x.gp)+kv("Goals",x.g)+kv("Assists",x.a)+kv("Points",x.p)+kv("P / game",x.ppg.toFixed(2))+kv("Adj P / game",x.adj.toFixed(2))+kv("Adj P / 60",x.adj60.toFixed(2))+kv("Avg opponent",x.opp.toFixed(1))+kv("+/-",(x.pm>0?"+":"")+x.pm)+kv("TOI / game",mmss(x.toig))+'</div>'
   +'<h3>Role on his team</h3><div class="kv">'+kv("Involvement",x.inv+"%")+kv("Team scoring rank",x.rk?x.rk+" of "+x.tn:"-")+kv(x.rk===1?"2nd scorer P/G":"Team leader P/G",(x.rk===1?x.t2:x.t1).toFixed(2))+kv("5th scorer P/G",x.t5?x.t5.toFixed(2):"-")+'</div>'
   +'<h3>Power play</h3><div class="kv">'+kv("PP points",x.ppp)+kv("PP goals",x.ppgl)+kv("PP assists",x.ppa)+kv("PP TOI / game",mmss(x.pptg))+'</div>'
   +'<h3>Game log</h3><div class="sheet"><table><thead><tr><th>Date</th><th>Opponent</th><th>Opp rating</th><th>Weight</th><th>Score</th><th>TOI</th><th>G</th><th>A</th><th>P</th><th>PPP</th><th>+/-</th></tr></thead><tbody>'
   +x.log.slice().reverse().map(l=>'<tr><td>'+l[0]+'</td><td style="text-align:left">'+(l[1]==="a"?"at ":"vs ")+esc(l[2])+'</td><td style="text-align:right">'+(l[3]?l[3].toFixed(2):"-")+'</td><td>'+(l[10]?l[10].toFixed(2):"-")+'</td><td>'+l[4]+'</td><td>'+mmss(l[5])+'</td><td>'+l[6]+'</td><td>'+l[7]+'</td><td><b>'+(l[6]+l[7])+'</b></td><td>'+(l[8]||"-")+'</td><td>'+(l[9]>0?"+":"")+l[9]+'</td></tr>').join("")+'</tbody></table></div>';
  $("prof").showModal();$("prof").scrollTop=0}
// Membership flow (demonstration only: nothing is stored or sent)
const F={step:1,plan:"season",player:""};
function flow(){const st=n=>'<span class="'+(F.step===n?"on":"")+'">'+n+'. '+["Plan","Account","Payment","Done"][n-1]+'</span>';
  let h='<button class="x" data-close>Close</button><h2>Become a member</h2><div class="steps">'+st(1)+st(2)+st(3)+st(4)+'</div>';
  if(F.step===1)h+='<div class="choice" role="button" tabindex="0" aria-pressed="'+(F.plan==="season")+'" data-plan="season"><div style="flex:1"><b>Season pass</b><div class="sub">Full 2026-27 season, one payment</div></div><b>$99</b></div><div class="choice" role="button" tabindex="0" aria-pressed="'+(F.plan==="monthly")+'" data-plan="monthly"><div style="flex:1"><b>Monthly</b><div class="sub">Billed monthly, cancel any time</div></div><b>$29</b></div><div class="acts"><button class="btn" data-next>Continue</button></div>';
  if(F.step===2)h+='<label for="f-name">Your name</label><input id="f-name" type="text" autocomplete="off"><label for="f-email">Email</label><input id="f-email" type="email" autocomplete="off" placeholder="you@example.com"><label for="f-player">Your player (optional)</label><input id="f-player" type="text" autocomplete="off" placeholder="We will pin his profile to your home page" value="'+esc(F.player)+'"><div class="note">Demonstration: no account is created and nothing typed here is saved or sent.</div><div class="acts"><button class="btn alt" data-back>Back</button><button class="btn" data-next>Continue</button></div>';
  if(F.step===3)h+='<p class="lede" style="margin-bottom:8px">'+(F.plan==="season"?"Season pass: $99, one payment":"Monthly: $29 per month")+'</p><label>Card number</label><input type="text" disabled value="Card entry appears here"><div class="row2"><div><label>Expiry</label><input type="text" disabled value="MM / YY"></div><div><label>Security code</label><input type="text" disabled value="CVC"></div></div><div class="note">Payments are not active in this preview. In the live site this step is handled by a payment processor; card details never touch our pages.</div><div class="acts"><button class="btn alt" data-back>Back</button><button class="btn" data-next>Finish demo</button></div>';
  if(F.step===4)h+='<h3 style="color:var(--good)">This is where a new member lands</h3><p>'+(F.plan==="season"?"Season pass":"Monthly membership")+' active. The full database opens: every birth year, every profile, every game log.</p>'+(F.player?'<div class="card" style="margin:12px 0"><h3>My player</h3><p><b style="color:var(--ink)">'+esc(F.player)+'</b><br>Pinned to the member home page, with his full profile, game log and what changed since his last game.</p></div>':'')+'<div class="acts"><button class="btn alt" data-sample>Open a sample full profile</button><button class="btn" data-close>Back to the preview</button></div>';
  $("flow-in").innerHTML=h}
function signin(){$("flow-in").innerHTML='<button class="x" data-close>Close</button><h2>Sign in</h2><label for="si">Email</label><input id="si" type="email" autocomplete="off" placeholder="you@example.com"><div class="note">Demonstration: sign-in is not active. Members would get a one-time sign-in link by email, so there is no password to remember.</div><div class="acts"><button class="btn" data-close>Close</button></div>';$("flow").showModal()}
function hits(){const q=$("q").value.trim().toLowerCase();if(q.length<3){$("hits").innerHTML="";return}
  const r=IDX.filter(x=>x[0].toLowerCase().includes(q)).slice(0,6);
  $("hits").innerHTML=r.length?r.map(x=>{const open=P[x[3]]&&P[x[3]].find(p=>p.n===x[0]&&p.t===x[1]&&p.ty===x[2]);return '<div class="hit"><div class="who"><b>'+esc(x[0])+'</b> <span class="born b'+(x[3]%100)+'">'+x[3]+' born</span><br><span class="sub">'+(x[4]?"Goalie · ":"")+esc(x[1])+' '+x[2]+'</span></div>'+(open?'<button class="btn alt" style="color:var(--ink)" data-open="'+x[3]+'|'+P[x[3]].indexOf(open)+'">Open profile</button>':'<button class="btn" data-act="join" data-player="'+esc(x[0])+'">Unlock his profile</button>')+'</div>'}).join(""):'<div class="hit"><div class="who">No player by that name yet. The database covers the top USA and Ontario teams in each birth year.</div></div>'}
document.addEventListener("click",e=>{const t=e.target;
  const y=t.closest("[data-y]");if(y){year=+y.dataset.y;tabs();table();return}
  const row=t.closest("tr.open");if(row){profile(P[year][+row.dataset.i]);return}
  const op=t.closest("[data-open]");if(op){const[a,b]=op.dataset.open.split("|");profile(P[a][+b]);return}
  if(t.closest("[data-close]")){t.closest("dialog").close();return}
  const act=t.closest("[data-act]");if(act){if(act.dataset.act==="signin"){signin();return}F.step=1;F.plan=act.dataset.plan||F.plan;F.player=act.dataset.player||F.player;flow();$("flow").showModal();return}
  const pl=t.closest(".choice");if(pl){F.plan=pl.dataset.plan;flow();return}
  if(t.closest("[data-next]")){if(F.step===2){const v=$("f-player");if(v)F.player=v.value.trim()}F.step=Math.min(4,F.step+1);flow();return}
  if(t.closest("[data-back]")){F.step=Math.max(1,F.step-1);flow();return}
  if(t.closest("[data-sample]")){$("flow").close();profile(P[year][0]);return}});
document.addEventListener("keydown",e=>{if(e.key==="Enter"){const r=e.target.closest&&e.target.closest("tr.open,.choice");if(r)r.click()}});
$("q").addEventListener("input",hits);
tabs();table();
</script></body></html>`;
fs.mkdirSync(require('path').dirname(out),{recursive:true});
fs.writeFileSync(out,page);
console.log('preview written',page.length,'bytes;',Object.entries(P).map(([y,a])=>y+': '+a.map(x=>x.n).join(', ')).join(' | '));
