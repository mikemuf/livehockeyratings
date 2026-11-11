// Types each query in window.__queries into InStat's own search box and records the team results.
// Progress is saved in localStorage 'pdbSR' so it can resume.
(async()=>{ if(window.__srRun) return; window.__srRun=1;
const W=ms=>new Promise(r=>setTimeout(r,ms));
let f=document.getElementById('pq');if(!f){f=document.createElement('iframe');f.id='pq';f.style.cssText='position:fixed;left:0;top:0;width:1400px;height:900px;opacity:0.01;pointer-events:none';document.body.appendChild(f)}
f.src='/instat/hockey';await W(7000);const d=f.contentDocument,win=f.contentWindow;
let R={};try{R=JSON.parse(localStorage.getItem('pdbSR')||'{}')}catch(e){}
const Q=(window.__queries||[]).filter(q=>!(q in R));
const st=window.__sr={R,done:0,total:Q.length,phase:'run'};
const set=Object.getOwnPropertyDescriptor(win.HTMLInputElement.prototype,'value').set;
const read=()=>[...d.querySelectorAll('a[href*="/teams/"]')].map(a=>a.getAttribute('href').split('/teams/')[1]+'='+a.innerText.trim().replace(/\n/g,' / '));
const inp=d.querySelector('input');set.call(inp,'');inp.dispatchEvent(new win.Event('input',{bubbles:true}));await W(2500);const recent=new Set(read());
for(const q of Q){set.call(inp,q);inp.dispatchEvent(new win.Event('input',{bubbles:true}));let last=null;for(let k=0;k<10;k++){await W(600);const cur=read().filter(x=>!recent.has(x)).join('|');if(cur===last&&(cur||k>=5))break;last=cur}st.R[q]=last||'';st.done++;if(st.done%5===0)try{localStorage.setItem('pdbSR',JSON.stringify(st.R))}catch(e){}}
try{localStorage.setItem('pdbSR',JSON.stringify(st.R))}catch(e){} st.phase='done'})();
