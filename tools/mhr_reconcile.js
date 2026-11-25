// Tuesday-evening reconcile collector (Nov 24 2026). Run in Chrome ON a rank page of the outside ranking site (rank.php?y=2026&v=<list>), after it renders:
//   paste this file, then  window.__rc('2013', 30)  (birth year of OUR page, number of teams from the top of the list). Poll window.__st ("done n/m").
// It fetches OUR published page for our game list (since SINCE), loads each team's games page in a hidden frame, and keeps ONLY the games we do not have:
//   localStorage.rc_lines gets "year|rank|their team|our best name|day|opponent|W 3-2" lines (appended across lists). Read it in slices under 1 KB.
// Never read a rank page as page text.
window.__rc=async function(y,N,SINCE,DRE){
  SINCE=SINCE||'2026-11-18';DRE=DRE||/^Nov (1[89]|2[0-4])$/;const W=window;W.__st='loading ours';
  const h=await (await fetch('https://myplayerdata.com/members/ratings/?v='+Date.now())).text();
  const grab=n=>JSON.parse(h.match(new RegExp('const '+n+'\\s*=\\s*(\\[\\[.*?\\]\\]);'))[1]);
  const seen=new Set(),G=grab('BASE').concat(grab('WEEKEND_GAMES')).filter(g=>g[0]===y&&g[1]>=SINCE&&!seen.has(g.join('|'))&&seen.add(g.join('|')));
  const names=new Set();try{Object.keys(JSON.parse(h.match(/const MHR=(\{.*?\}\});/)[1])[y]||{}).forEach(n=>names.add(n))}catch(e){}
  grab('BASE').forEach(g=>{if(g[0]===y){names.add(g[2]);names.add(g[4])}});
  const w=s=>{s=s.toLowerCase().replace(/\b(1[0-6]u|u1[0-6]|aaa|hockey|club|academy|elite|jr\.?|the|premier|national|tier|new jersey|nj)\b/g,' ').replace(/\([^)]*\)/g,' ');return new Set(s.replace(/[^a-z0-9 ]/g,' ').split(' ').filter(x=>x.length>2))};
  const jac=(a,b)=>{let i=0;a.forEach(x=>{if(b.has(x))i++});return i/Math.max(1,a.size+b.size-i)};
  const NW=[...names].map(n=>[n,w(n)]);
  const ids=[];for(const a of document.querySelectorAll('table a')){const m=(a.getAttribute('href')||'').match(/[?&]t=(\d+)|team-info\/(\d+)/)   /* rank rows link team_info.php?y=2026&t=<id>: take t, not the year */;if(m){const id=m[1]||m[2];if(!ids.includes(id))ids.push(id)}if(ids.length>=N)break}
  const out=[];let k=0;
  for(const id of ids){k++;W.__st='team '+k+'/'+ids.length;const f=document.createElement('iframe');f.style.cssText='position:absolute;left:-6000px;top:0;width:1200px;height:900px';document.body.appendChild(f);f.src='/team-info/'+id+'/2026/games';
    await new Promise(r=>{f.onload=r;setTimeout(r,15000)});await new Promise(r=>setTimeout(r,900));
    try{const d=f.contentDocument;const name=(d.title||'').split(' - ')[0];const tw=w(name);let best='',sc=0;NW.forEach(([n,s])=>{const v=jac(s,tw);if(v>sc){sc=v;best=n}});
      const mine=[];G.forEach(g=>{const dd=+g[1].slice(8);if(g[2]===best)mine.push([dd,g[3],g[5]]);else if(g[4]===best)mine.push([dd,g[5],g[3]])});
      const L=d.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean);let n=0;
      for(let j=0;j<L.length;j++){if(!DRE.test(L[j]))continue;let opp=(L[j+2]||'').replace(/\*+$/,'');const nx=L.slice(j+4,j+8);const q=nx.findIndex(x=>/^[WLT]$/.test(x));
        if(q<0||!/^\d+ - \d+$/.test(nx[q+1]||''))continue;n++;const [x,z]=nx[q+1].split(' - ').map(Number),R=nx[q];const gf=R==='W'?Math.max(x,z):R==='L'?Math.min(x,z):x,ga=R==='W'?Math.min(x,z):R==='L'?Math.max(x,z):z;
        const day=+L[j].slice(4);const hi=mine.findIndex(m=>Math.abs(m[0]-day)<=1&&m[1]===gf&&m[2]===ga);
        if(hi>=0)mine.splice(hi,1);else out.push([y,k,name,sc>=0.5?best:'?'+best,day,opp,R+' '+gf+'-'+ga].join('|'))}
      mine.forEach(m=>out.push([y,k,name,best,m[0],'OURS-ONLY',m[1]+'-'+m[2]].join('|')));
      if(!n&&!L.length)out.push([y,k,name||id,'','', 'NO PAGE',''].join('|'));
    }catch(e){out.push([y,k,id,'','','ERR '+e.message,''].join('|'))}
    f.remove();await new Promise(r=>setTimeout(r,400))}
  localStorage.setItem('rc_lines',(localStorage.getItem('rc_lines')||'')+out.join('\n')+'\n');W.__st='done '+ids.length+' teams, '+out.length+' lines, ours '+G.length;return W.__st};
'ready'
