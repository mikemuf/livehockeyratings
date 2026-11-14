// GameSheet box-score scraper. Run on https://gamesheetstats.com/seasons/<S>/games.
// window.__GS_Q = list of search strings (rink names etc.; GameSheet lists cap at ~25 rows, so split by rink). Default [''].
// window.__GS_DATES = /Nov 1[3-5]/. Only games with a score in the list (final or live) are opened.
// Writes one JSON object per line into <main><pre>; poll window.__gsdone, then get_page_text.
window.__gsdone=false;window.__gsp=0;(async()=>{
const S=location.pathname.match(/seasons\/(\d+)/)[1],DT=window.__GS_DATES||/Nov 1[3-5]/,Q=window.__GS_Q||[''];
const ids=new Map();if(window.__GS_IDS){window.__GS_IDS.forEach(x=>ids.set(String(x),1))}else
for(const q of Q){const f=document.createElement('iframe');f.style.cssText='position:absolute;left:-6000px;width:1200px;height:900px';document.body.appendChild(f);f.src='/seasons/'+S+'/games?filter%5Bstatus%5D=all'+(q?'&filter%5Bquery%5D='+encodeURIComponent(q):'');await new Promise(r=>{f.onload=r;setTimeout(r,12000)});await new Promise(r=>setTimeout(r,3500));
 for(const a of f.contentDocument.querySelectorAll('a[href*="/games/"]')){const m=a.getAttribute('href').match(/\/games\/(\d+)/);if(!m)continue;let row=a;for(let k=0;k<10&&row&&!(/2026/.test(row.innerText)&&/(\d+-\d+|\d:\d\d [AP]M)/.test(row.innerText));k++)row=row.parentElement;const tx=row?row.innerText:'';if(DT.test(tx)&&/(^|\s)\d+-\d+(\s|$)/.test(tx))ids.set(m[1],1)}f.remove()}
const out=[];window.__gsn=ids.size;
for(const id of ids.keys()){const f=document.createElement('iframe');f.style.cssText='position:absolute;left:-6000px;width:1200px;height:900px';document.body.appendChild(f);f.src='/seasons/'+S+'/games/'+id+'?tab=box-score';
 await new Promise(r=>{f.onload=r;setTimeout(r,12000)});let L=[];for(let k=0;k<12;k++){await new Promise(r=>setTimeout(r,700));L=f.contentDocument.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean);if(L.includes('PENALTIES BY PERIOD'))break}
 try{const g={id:+id,s:+S};const vi=L.findIndex(x=>/VISITOR$/.test(x));g.v=L[vi+1];const hi=L.findIndex(x=>/^HOME\b/.test(x));g.h=L[hi+1];
  const di=L.findIndex(x=>/^[A-Z][a-z]{2} \d+, 2026/.test(x));g.when=L[di];g.rink=L[di+1]&&!/Attendance|DIVISION/.test(L[di+1])?L[di+1]:'';
  const dash=L.indexOf('-',vi);g.vs=+L[dash-2];g.hs=+L[dash+1];g.st=L.slice(vi+2,dash-2).find(x=>/^(FINAL.*|IN PROGRESS|INTERMISSION.*|.*PERIOD|OVERTIME|SHOOTOUT)$/.test(x))||'';
  const sec=(a,b)=>{const i=L.indexOf(a),j=b?L.indexOf(b):L.length;return i<0?[]:L.slice(i+1,j<0?L.length:j)};
  const PER=/^(1ST|2ND|3RD|OT\d*|\dTH|SO|OVERTIME|SHOOTOUT)$/,NONE=/^NO (GOALS|PENALTIES)$/i,TAG=/^(PP|SH|EN|PS|GW|GWG|SO|ENG|PPG|SHG)$/;
  const gl=[],gt=sec('GOALTENDING','GOALS BY PERIOD');let side=-1;for(const x of gt){if(/^GOALIE/.test(x)){side++;continue}if(/^#\d+ /.test(x))gl.push([side,x])}g.goalies=gl;
  const goals=[];let per='',cur=null;for(const x of sec('GOALS BY PERIOD','PENALTIES BY PERIOD')){if(PER.test(x)){per=x;continue}if(NONE.test(x))continue;if(/^\d{1,2}:\d\d$/.test(x)){cur={p:per,t:x,tags:[],pl:[],team:''};goals.push(cur);continue}if(!cur)continue;if(TAG.test(x)){cur.tags.push(x);continue}if(/^#/.test(x)){cur.pl.push(x);continue}if(!cur.team)cur.team=x}
  g.goals=goals.map(o=>[o.p,o.t,o.team===g.v?0:o.team===g.h?1:o.team,o.pl,o.tags]);
  const pens=[];per='';cur=null;for(const x of sec('PENALTIES BY PERIOD')){if(/^Powered by/.test(x))break;if(PER.test(x)){per=x;continue}if(NONE.test(x))continue;if(/^\d{1,2}:\d\d$/.test(x)){cur={p:per,t:x,a:[]};pens.push(cur);continue}if(cur)cur.a.push(x)}
  g.pens=pens.map(o=>{const a=o.a.filter(x=>!/^(MINOR|MAJOR|MISCONDUCT|MATCH|GAME MISCONDUCT|BENCH)$/.test(x));const team=a[a.length-1];return [o.p,o.t,team===g.v?0:team===g.h?1:team,a.slice(0,-1)]});
  out.push(JSON.stringify(g))}catch(e){out.push(JSON.stringify({id:+id,err:String(e)}))}
 f.remove();window.__gsp++}
document.querySelector('main').innerHTML='<pre></pre>';document.querySelector('main pre').textContent=out.join('\n');window.__gsdone=true})();'started'
