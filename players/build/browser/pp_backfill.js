// Reads each stored game's Skaters page in the PP (power play) view and records PP time, goals and assists per player.
// Rendered pages only, in hidden same-origin iframes. Progress is saved in localStorage 'pdbPP' so it can resume.
(async()=>{ if(window.__ppRun) return; window.__ppRun=1;
const IDS=window.__ppIds||(await (await fetch('https://mikemuf.github.io/livehockeyratings/players/data/box.json?'+Date.now())).json()).M.map(m=>m.id);
document.querySelectorAll('iframe.pdbf').forEach(f=>f.remove());
const W=ms=>new Promise(r=>setTimeout(r,ms));
let R={};try{R=JSON.parse(localStorage.getItem('pdbPP')||'{}')}catch(e){}
const st=window.__pp={R,done:0,total:0,phase:'run',err:[],clicks:0};
const mk=()=>{const f=document.createElement('iframe');f.className='pdbf';f.style.cssText='position:fixed;left:0;top:0;width:1600px;height:900px;opacity:0.01;pointer-events:none';document.body.appendChild(f);return f};
const toks=d=>d.body.innerText.split(/[\n\t]/).map(s=>s.trim()).filter(Boolean);
const sec=s=>{const p=s.split(':');return p.length==2?+p[0]*60+ +p[1]:0};
const n0=s=>(s==='-'||s==='—'||s===undefined)?0:(parseInt(s)||0);
const label=d=>{const t=toks(d);const i=t.indexOf('EPISODES SEARCH');return i>=0?t[i+1]:''};
const leaf=(d,l)=>[...d.querySelectorAll('*')].filter(e=>e.children.length===0&&e.innerText&&e.innerText.trim()===l);
const one=async(f,id)=>{const u='/instat/hockey/matches/'+id+'/skaters';f.src='about:blank';await W(200);f.src=u;let d=null;
 for(let k=0;k<36;k++){await W(500);try{const x=f.contentDocument;if(x&&x.body&&f.contentWindow.location.pathname===u&&(x.body.innerText.match(/\nPosition\n/g)||[]).length>=2&&label(x)){d=x;break}}catch(e){}}
 if(!d){try{const x=f.contentDocument;st.R[id]=(x&&x.body&&x.body.innerText.includes('EPISODES SEARCH'))?'x':'?';}catch(e){st.R[id]='?'}return}
 if(label(d)!=='PP'){const e=leaf(d,label(d)).filter(x=>!/^(TH|TD)$/.test(x.tagName))[0];if(e){(e.closest('button,[role=button]')||e).click();await W(900);const pp=leaf(d,'PP').pop();if(pp){pp.click();st.clicks++}for(let k=0;k<12&&label(d)!=='PP';k++)await W(500);await W(2500)}}
 else await W(700);
 if(label(d)!=='PP'){st.R[id]='?';return}
 const t=toks(d);const S=[];const rows=[];let side=-1;
 for(let i=0;i<t.length-9;i++){if(t[i+1]==='Position'&&t[i+2]==='POS'){S.push(t[i]);side=S.length-1;continue}
  if(side>=0&&/^\d{1,3}$/.test(t[i])&&/^(F|D)$/.test(t[i+2])&&/^(\d+:\d\d|-)$/.test(t[i+3])&&!/^\d+$/.test(t[i+1])){const ppt=sec(t[i+3]),g=n0(t[i+5]),a=n0(t[i+8]);if(ppt||g||a)rows.push([side,t[i],ppt,g,a].join(','));i+=3}}
 st.R[id]=S.join('^')+'^'+rows.join(';');};
try{const ids=IDS.filter(i=>!(i in st.R)||st.R[i]==='?');st.total=ids.length;const fs=[mk(),mk(),mk()];
 await Promise.all(fs.map(async f=>{while(ids.length){const id=ids.shift();try{await one(f,id)}catch(e){st.err.push(id+':'+e);st.R[id]='?'}st.done++;if(st.done%20===0)try{localStorage.setItem('pdbPP',JSON.stringify(st.R))}catch(e){}}}));
 try{localStorage.setItem('pdbPP',JSON.stringify(st.R))}catch(e){} st.phase='done';}catch(e){st.err.push('fatal:'+e);st.phase='failed'}})();
