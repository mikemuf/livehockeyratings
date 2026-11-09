function renderWeekend(S){
  const W=WEEKEND,D=(W.divs||{})[div]||{};const rk={},rt={};S.rows.filter(x=>!canada.has(x.t)&&x.mhr).forEach((x,i)=>rk[x.t]=i+1);S.rows.forEach(x=>rt[x.t]=x.r);
  const tag=t=>{const r=rt[t];if(r===undefined)return '';return `<span class="small"> (${rk[t]?'#'+rk[t]:canada.has(t)?'CAN':'NR'}, ${f2(r)})</span>`};
  const nice=d=>{const x=new Date(d+'T12:00:00');return x.toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})};
  let h=`<div class="card"><h2 style="margin-top:0">${esc(W.label||'This weekend')}</h2><p class="small">${esc(W.status||'')} · updated ${esc(W.updated||'')}</p>`;
  if((D.summary||[]).length)h+='<ul class="wk">'+D.summary.map(s=>`<li>${esc(s)}</li>`).join('')+'</ul>';else h+='<p class="small">No summary yet for this division.</p>';
  h+='</div>';
  if((D.events||[]).length)h+='<div class="card"><h3 style="margin-top:0">Tournaments</h3>'+D.events.map(e=>`<p style="margin:6px 0"><b>${esc(e.name)}</b>${e.where?` <span class="small">· ${esc(e.where)}</span>`:''}<br><span class="small">${esc(e.result||'')}</span></p>`).join('')+'</div>';
  h+='<div class="card"><h3 style="margin-top:0">Games to watch</h3>';
  if((D.watch||[]).length)h+='<table class="wkg">'+D.watch.map(g=>`<tr><td class="small" style="white-space:nowrap">${esc(g[0])}<br>${esc(g[1]||'')}</td><td>${esc(g[2])}${tag(g[2])}<br>vs ${esc(g[3])}${tag(g[3])}${g[4]?`<br><span class="small">${esc(g[4])}</span>`:''}</td></tr>`).join('')+'</table>';
  else h+=`<p class="small">${esc(W.next||'Check back later in the week.')}</p>`;
  h+='</div>';
  const G=WEEKEND_GAMES.filter(g=>g[0]===div).slice().sort((a,b)=>a[1]<b[1]?1:a[1]>b[1]?-1:0);
  if(G.length){h+=`<div class="card"><h3 style="margin-top:0">Results this weekend <span class="small">(${G.length})</span></h3>`;
    let last='';G.forEach(g=>{const aw=g[3]>g[5],bw=g[5]>g[3];if(g[1]!==last){h+=`<div class="wkd">${nice(g[1])}</div>`;last=g[1]}h+=`<div class="wkr"><div>${aw?'<b>':''}${esc(g[2])}${aw?'</b>':''}${tag(g[2])}</div><div class="sc num">${g[3]}</div><div>${bw?'<b>':''}${esc(g[4])}${bw?'</b>':''}${tag(g[4])}</div><div class="sc num">${g[5]}</div></div>`});
    h+='<p class="legend">Live USA rank and rating, with these games already counted. NR = not in MHR’s rankings, CAN = Canadian team.</p></div>'}
  return h;
}
