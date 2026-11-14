let WK_SEL=null;
function renderWeekend(S){
  if(WK_SEL)return renderGame(S,WK_SEL);
  const W=WEEKEND,D=(W.divs||{})[div]||{};const rk={},rt={};S.rows.filter(x=>!canada.has(x.t)&&x.mhr).forEach((x,i)=>rk[x.t]=i+1);S.rows.forEach(x=>rt[x.t]=x.r);
  const rk0=t=>{if(canada.has(t))return 'CAN';const M0=MHR[div]||{};if(M0[t]===undefined)return 'NR';return '#'+(S.rows.filter(x=>x.mhr&&!canada.has(x.t)&&M0[x.t]!==undefined).map(x=>x.t).sort((a,b)=>M0[b]-M0[a]).indexOf(t)+1)};
  const tag=t=>{const r=rt[t];if(r===undefined)return '';return `<span class="small"> (${rk[t]?'#'+rk[t]:canada.has(t)?'CAN':'NR'}, ${f2(r)})</span>`};
  const nice=d=>{const x=new Date(d+'T12:00:00');return x.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})};
  let h=`<div class="card"><h2 style="margin-top:0">${esc(W.label||'This weekend')}</h2><p class="small">${esc(W.status||'')} · updated ${esc(W.updated||'')}</p>`;
  if(W.note)h+=`<p class="small" style="margin:4px 0 0">${esc(W.note)}</p>`;
  if((D.summary||[]).length)h+='<ul class="wk">'+D.summary.map(s=>`<li>${esc(s)}</li>`).join('')+'</ul>';else h+='<p class="small">No summary yet for this division.</p>';
  h+='</div>';
  if((D.events||[]).length)h+='<div class="card"><h3 style="margin-top:0">Tournaments</h3>'+D.events.map(e=>`<p style="margin:6px 0"><b>${esc(e.name)}</b>${e.where?` <span class="small">· ${esc(e.where)}</span>`:''}<br><span class="small">${esc(e.result||'')}</span></p>`).join('')+'</div>';
  if(D.report){const RP=D.report,M0=MHR[div]||{},R={};S.rows.forEach(x=>R[x.t]=x.r);for(const t in M0)R[t]=M0[t];
    const pr={};Object.keys(M0).filter(t=>!canada.has(t)).sort((a,b)=>M0[b]-M0[a]);
    const set=new Set(RP.teams),cl=x=>Math.max(-7,Math.min(7,x)),T={};
    WEEKEND_GAMES.filter(g=>g[0]===div&&g[1]>=RP.from&&g[1]<=RP.to&&set.has(g[2])&&set.has(g[4])).forEach(g=>{for(const [me,gf,op,ga] of [[g[2],g[3],g[4],g[5]],[g[4],g[5],g[2],g[3]]]){const t=T[me]||(T[me]={w:0,l:0,t:0,gf:0,ga:0,d:0,p:0,n:0});t.n++;t.gf+=gf;t.ga+=ga;if(gf>ga)t.w++;else if(gf<ga)t.l++;else t.t++;t.d+=cl(gf-ga)-((R[me]||0)-(R[op]||0));t.p+=(R[op]||0)+cl(gf-ga)}});
    const rows=Object.entries(T).sort((a,b)=>b[1].d/b[1].n-a[1].d/a[1].n);
    h+=`<div class="card"><h3 style="margin-top:0">${esc(RP.title)}</h3><p class="small" style="margin:0 0 6px">Each team's goal differential per game compared with what its rating expected against these opponents. <b>+</b> = outperformed its rating, <b>−</b> = underperformed. "Played like" = the rating these results are worth (opponent rating + goal differential, capped at 7). Rating shown is the pre-tournament MHR rating.</p><table class="wkg rep"><tr><th>Team</th><th>Rec</th><th>GF-GA</th><th>Played like</th><th>vs rating</th></tr>`+rows.map(([k,t])=>{const d=t.d/t.n;return `<tr><td>${esc(k)}<span class="small"> (${rk0(k)}, ${R[k]!==undefined?f2(M0[k]!==undefined?M0[k]:R[k]):'–'})</span></td><td>${t.w}-${t.l}-${t.t}</td><td>${t.gf}-${t.ga}</td><td>${f2(t.p/t.n)}</td><td style="font-weight:700;color:${d>=0.25?'#1a7f37':d<=-0.25?'#c62828':'inherit'}">${d>=0?'+':'−'}${Math.abs(d).toFixed(2)}</td></tr>`}).join('')+'</table>'+(RP.note?`<p class="legend">${esc(RP.note)}</p>`:'')+'</div>'}
  if((D.scorers||[]).length){const SC=D.scorers;h+=`<div class="card"><h3 style="margin-top:0">${esc(D.scorers_title||'Top scorers')}</h3>`+(D.scorers_note?`<p class="small" style="margin:0 0 6px">${esc(D.scorers_note)}</p>`:'')+'<table class="wkg rep"><tr><th>Player</th><th>GP</th><th>G</th><th>A</th><th>PTS</th></tr>'+SC.map((p,i)=>`<tr><td>${i+1}. <b>${esc(p.name)}</b><br><span class="small">${esc(p.team)}${tag(p.team)}</span></td><td>${p.gp??''}</td><td>${p.g}</td><td>${p.a}</td><td><b>${p.g+p.a}</b></td></tr>`).join('')+'</table><p class="legend">Unofficial live stats, entered by scorekeepers in real time. Goals and assists are sometimes corrected later after video review.</p></div>'}
  if((D.goalies||[]).length){const GL=D.goalies;h+=`<div class="card"><h3 style="margin-top:0">${esc(D.goalies_title||'Top goalies')}</h3>`+(D.goalies_blurb?`<p class="small" style="margin:0 0 6px">${esc(D.goalies_blurb)}</p>`:'')+'<table class="wkg rep"><tr><th>Goalie</th><th>GP</th><th>W-L-T</th><th>GA</th><th>GAA</th></tr>'+GL.map((p,i)=>`<tr><td>${i+1}. <b>${esc(p.name)}</b><br><span class="small">${esc(p.team)}${tag(p.team)}</span></td><td>${p.gp}</td><td>${p.w}-${p.l}-${p.t}</td><td>${p.ga}</td><td><b>${(p.ga/p.gp).toFixed(2)}</b></td></tr>`).join('')+'</table><p class="legend">Unofficial live stats, entered by scorekeepers in real time. Goals against per game (games are 45 minutes).</p></div>'}
  h+='<div class="card"><h3 style="margin-top:0">Games to watch</h3>';
  const W2=(D.watch||[]).map(g=>Array.isArray(g)?{day:g[0],time:g[1],a:g[2],b:g[3],rink:g[4]||'',city:'',note:''}:g);
  if(W2.length)h+='<table class="wkg">'+W2.map((g,j)=>{const q=encodeURIComponent((g.rink+' '+(g.city||'')).trim());const loc=g.rink?`<div class="wkloc">📍 <b>${esc(g.rink)}</b>${g.city?', '+esc(g.city):''}<br><a href="https://www.google.com/maps/search/?api=1&query=${q}" target="_blank" rel="noopener">Map</a> · <a href="https://livebarn.com/en/venue" target="_blank" rel="noopener">LiveBarn</a>${g.note?' · '+esc(g.note):''}</div>`:'';return `<tr><td class="small" style="white-space:nowrap">${esc(g.day)}<br>${esc(g.time||'')}</td><td><span class="wkclick" data-gm="w${j}">${esc(g.a)}${tag(g.a)}<br>vs ${esc(g.b)}${tag(g.b)} <span class="small" style="color:var(--red,#c8102e)">›</span></span>${loc}</td></tr>`}).join('')+'</table><p class="legend">Times are local to the rink. LiveBarn opens its rink list; search the rink name to watch.</p>';
  else h+=`<p class="small">${esc(W.next||'Check back later in the week.')}</p>`;
  h+='</div>';
  const G=WEEKEND_GAMES.map((g,i)=>Object.assign(g.slice(),{gi:i})).filter(g=>g[0]===div).sort((a,b)=>a[1]<b[1]?1:a[1]>b[1]?-1:0);
  if(G.length){h+=`<div class="card"><h3 style="margin-top:0">Results this weekend <span class="small">(${G.length})</span></h3>`;
    let last='';G.forEach(g=>{const aw=g[3]>g[5],bw=g[5]>g[3];if(g[1]!==last){h+=`<div class="wkd">${nice(g[1])}</div>`;last=g[1]}h+=`<div class="wkr wkclick" data-gm="r${g.gi}"><div>${aw?'<b>':''}${esc(g[2])}${aw?'</b>':''}${tag(g[2])}</div><div class="sc num">${g[3]}</div><div>${bw?'<b>':''}${esc(g[4])}${bw?'</b>':''}${tag(g[4])}</div><div class="sc num">${g[5]}</div></div>`});
    h+='<p class="legend">Tap a game for the matchup page. Live USA rank and rating, with these games already counted. NR = not in MHR’s rankings, CAN = Canadian team.</p></div>'}
  return h;
}

function renderGame(S,key){
  const W=WEEKEND,D=(W.divs||{})[div]||{},M0=MHR[div]||{},cl=x=>Math.max(-7,Math.min(7,x));
  const rk={},rt={};S.rows.filter(x=>!canada.has(x.t)&&x.mhr).forEach((x,i)=>rk[x.t]=i+1);S.rows.forEach(x=>rt[x.t]=x.r);
  const rk0=t=>{if(canada.has(t))return 'CAN';if(M0[t]===undefined)return 'NR';return '#'+(S.rows.filter(x=>x.mhr&&!canada.has(x.t)&&M0[x.t]!==undefined).map(x=>x.t).sort((a,b)=>M0[b]-M0[a]).indexOf(t)+1)};
  const lr=t=>rk[t]?'#'+rk[t]:canada.has(t)?'CAN':'NR';
  const nice=d=>new Date(d+'T12:00:00').toLocaleDateString('en-US',{weekday:'long',month:'short',day:'numeric'});
  const back=`<p style="margin:0 0 8px"><a href="#wk=${div}">← Weekend</a></p>`;
  let a,b,ga=null,gb=null,date='',when='',loc=null;
  if(key[0]==='r'){const g=WEEKEND_GAMES[+key.slice(1)];if(!g||g[0]!==div)return back+'<p class="small">Game not found.</p>';[a,ga,b,gb]=[g[2],g[3],g[4],g[5]];date=g[1];when=nice(g[1])}
  else{const w=(D.watch||[])[+key.slice(1)];if(!w)return back+'<p class="small">This game has been played or removed. Check the results list.</p>';a=w.a;b=w.b;when=(w.day||'')+(w.time?' · '+w.time:'');loc=w}
  const pre=t=>M0[t]!==undefined?M0[t]:rt[t];const R=ga!==null?pre:(t=>rt[t]!==undefined?rt[t]:pre(t));const Ra=R(a),Rb=R(b),have=Ra!==undefined&&Rb!==undefined;
  const team=t=>{const x=S.byName&&S.byName[t];const nm=x?`<a href="javascript:void 0" data-t="${esc(t)}">${esc(t)}</a>`:esc(t);return nm};
  let h=back+`<div class="card"><p class="small" style="margin:0">${esc(when)}${loc&&loc.rink?' · 📍 '+esc(loc.rink)+(loc.city?', '+esc(loc.city):''):''}</p>`;
  if(ga!==null){const aw=ga>gb,bw=gb>ga;h+=`<table class="wkg" style="margin-top:8px;font-size:18px"><tr><td>${aw?'<b>':''}${team(a)}${aw?'</b>':''}</td><td class="num" style="width:40px;text-align:right"><b>${ga}</b></td></tr><tr><td>${bw?'<b>':''}${team(b)}${bw?'</b>':''}</td><td class="num" style="text-align:right"><b>${gb}</b></td></tr></table><p class="small" style="margin:6px 0 0">Final${ga===gb?' (tie)':''}</p>`}
  else h+=`<h2 style="margin:8px 0 0">${team(a)} <span class="small">vs</span> ${team(b)}</h2>`+(loc&&loc.rink?`<p class="small" style="margin:6px 0 0"><a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent((loc.rink+' '+(loc.city||'')).trim())}" target="_blank" rel="noopener">Map</a> · <a href="https://livebarn.com/en/venue" target="_blank" rel="noopener">LiveBarn</a>${loc.note?' · '+esc(loc.note):''}</p>`:'');
  h+='</div>';
  h+=`<div class="card"><h3 style="margin-top:0">The teams</h3><table class="wkg rep"><tr><th>Team</th><th>Before</th><th>Now</th></tr>`+[a,b].map(t=>`<tr><td>${team(t)}</td><td>${rk0(t)}, ${pre(t)!==undefined?f2(pre(t)):'–'}</td><td><b>${lr(t)}, ${rt[t]!==undefined?f2(rt[t]):'–'}</b></td></tr>`).join('')+`</table><p class="legend">Before = MHR’s last published rating (start of the weekend). Now = live rating with every result so far counted.</p></div>`;
  if(have){const exp=Ra-Rb,fav=exp>=0?a:b,by=Math.abs(exp);
    h+=`<div class="card"><h3 style="margin-top:0">${ga!==null?'Result vs ratings':'What the ratings say'}</h3>`;
    h+=`<p style="margin:0 0 6px">${by<0.25?'Ratings say this is a toss-up.':`${ga!==null?'Going in, ratings favored':'Live ratings favor'} <b>${esc(fav)}</b> by about <b>${by.toFixed(1)}</b> goals.`}</p>`;
    if(ga!==null){const gd=cl(ga-gb),diff=gd-exp,pa=Rb+gd,pb=Ra-gd;
      h+=`<p style="margin:0 0 6px">${Math.abs(diff)<0.5?'The result was close to what the ratings expected.':`<b>${esc(diff>0?a:b)}</b> beat the expectation by <b>${Math.abs(diff).toFixed(1)}</b> goals.`}</p>`;
      h+=`<table class="wkg rep"><tr><th>Team</th><th>Played like</th><th>vs rating</th></tr>`+[[a,pa,pa-Ra],[b,pb,pb-Rb]].map(([t,p,d])=>`<tr><td>${esc(t)}</td><td>${f2(p)}</td><td style="font-weight:700;color:${d>=0.25?'#1a7f37':d<=-0.25?'#c62828':'inherit'}">${d>=0?'+':'−'}${Math.abs(d).toFixed(2)}</td></tr>`).join('')+`</table><p class="legend">"Played like" = the rating this one game is worth: opponent’s rating plus goal differential (capped at 7). A team’s rating moves toward the average of these game values.</p>`}
    h+='</div>'}
  const others=t=>WEEKEND_GAMES.filter(g=>g[0]===div&&(g[2]===t||g[4]===t)&&!(ga!==null&&g[1]===date&&((g[2]===a&&g[4]===b)||(g[2]===b&&g[4]===a))&&g[3]===ga&&g[5]===gb));
  h+='<div class="card"><h3 style="margin-top:0">Their weekend</h3>'+[a,b].map(t=>{const L=others(t);let w=0,l=0,ti=0;WEEKEND_GAMES.filter(g=>g[0]===div&&(g[2]===t||g[4]===t)).forEach(g=>{const me=g[2]===t?g[3]:g[5],op=g[2]===t?g[5]:g[3];me>op?w++:me<op?l++:ti++});
    return `<p style="margin:8px 0 2px"><b>${esc(t)}</b> <span class="small">${w}-${l}-${ti} this weekend</span></p>`+(L.length?L.map(g=>{const me=g[2]===t,mf=me?g[3]:g[5],of=me?g[5]:g[3],op=me?g[4]:g[2];return `<div class="small">${mf>of?'W':mf<of?'L':'T'} ${mf}-${of} vs ${esc(op)} <span>(${lr(op)})</span></div>`}).join(''):'<div class="small">No other games yet.</div>')}).join('')+'</div>';
  return h;
}
document.addEventListener('click',e=>{const g=e.target.closest&&e.target.closest('[data-gm]');if(g){location.hash='#game='+div+'|'+g.dataset.gm;return}
  if(e.target.closest&&e.target.closest('.seg button,nav.tabs button'))WK_SEL=null},true);
