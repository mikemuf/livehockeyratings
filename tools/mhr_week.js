// Run in Chrome on https://myhockeyrankings.com/rank.php?y=2026&v=114 (2012) or v=125 (2013) after it renders.
// Set window.__N (teams, default 25) and window.__DATES (regex of date labels, e.g. /^Nov [5-9]$/).
// Loads each top-N AAA team's MHR games page one at a time and writes into <main><pre>:
//   TEAM|DATE|TIME|OPPONENT|FLAG(**=tournament,*=league)|RESULT (W 3-2 / L 1-4 / T 2-2 / PREVIEW)|RINK
// Read it with get_page_text. Poll window.__wdone.
window.__wdone=false;window.__wp=0;(async()=>{
const N=window.__N||25,D=window.__DATES||/^Nov [5-9]$/;
const rows=[...document.querySelectorAll('tr')].filter(tr=>/^\d+\s/.test(tr.innerText.trim())&&/AAA/.test(tr.innerText));
const ids=[];for(const tr of rows){const a=tr.querySelector('a[href*="t="]');if(a)ids.push(a.getAttribute('href').match(/t=(\d+)/)[1]);if(ids.length>=N)break}
const out=[];
for(const id of ids){const f=document.createElement('iframe');f.style.cssText='position:absolute;left:-6000px;top:0;width:1200px;height:900px';document.body.appendChild(f);f.src='/team-info/'+id+'/2026/games';
 await new Promise(r=>{f.onload=r;setTimeout(r,15000)});await new Promise(r=>setTimeout(r,900));
 try{const d=f.contentDocument;const name=(d.title||'').split(' - ')[0].replace(/ (1[34]U|U1[45]) AAA$/,'');const L=d.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean);
  for(let j=0;j<L.length;j++){if(!D.test(L[j]))continue;const time=L[j+1]||'';let opp=L[j+2]||'';const fl=(opp.match(/\*+$/)||[''])[0];opp=opp.replace(/\*+$/,'').replace(/ (1[34]U|U1[45]) AAA$/,'');const rink=(L[j+3]||'').replace(/^WATCH /,'');
   const nx=L.slice(j+4,j+8);const k=nx.findIndex(x=>/^[WLT]$/.test(x));let res='';
   if(k>=0&&/^\d+ - \d+$/.test(nx[k+1]||''))res=nx[k]+' '+nx[k+1].replace(/ /g,'');else if(nx.slice(0,2).some(x=>/^Preview$/i.test(x)))res='PREVIEW';
   if(res)out.push([name,L[j],time,opp,fl,res,rink].join('|'))}}catch(e){}
 f.remove();window.__wp++;await new Promise(r=>setTimeout(r,500))}
document.querySelector('main').innerHTML='<pre></pre>';document.querySelector('main pre').textContent=out.join('\n');window.__wdone=true})();'started'
