// Runs in a signed-in InStat tab (app.hudl.com/instat/hockey/...) through the browser's JavaScript tool.
// Reads rendered pages only, in hidden same-origin iframes. Fire-and-forget: poll window.__pdb for progress.
(()=>{ if(window.__run) return 'already running';
window.__run=1;
const TEAMS='__TEAMS__'.split(',').filter(Boolean);
const KNOWN=new Set('__KNOWN__'.split(','));
const CUT='__CUT__';
const CANARY='__CANARY__'.split(',').filter(Boolean); // already-stored games re-read to prove the parser still works
const W=ms=>new Promise(r=>setTimeout(r,ms));
let saved=null;try{saved=JSON.parse(localStorage.getItem('pdbH')||'null')}catch(e){}
const st=window.__pdb=(saved&&saved.cut===CUT&&saved.nt===TEAMS.length)?Object.assign(saved,{err:[],resumed:1}):{T:{},M:{},newIds:{},phase:'teams',tdone:0,mdone:0,mtotal:0,err:[],cut:CUT,nt:TEAMS.length};
const save=()=>{try{localStorage.setItem('pdbH',JSON.stringify(st))}catch(e){st.err.push('save:'+e)}};
const mk=()=>{const f=document.createElement('iframe');f.className='pdbf';f.style.cssText='position:fixed;left:0;top:0;width:1400px;height:900px;opacity:0.01;pointer-events:none';document.body.appendChild(f);return f};
const load=async(f,u,ready,max)=>{f.src='about:blank';await W(200);f.src=u;for(let k=0;k<max*2;k++){await W(500);try{const d=f.contentDocument;if(d&&d.body&&f.contentWindow.location.pathname===u&&ready(d))return d}catch(e){}}try{return f.contentDocument}catch(e){return null}};
const toks=d=>d.body.innerText.split(/[\n\t]/).map(s=>s.trim()).filter(Boolean);
const sec=s=>{const p=s.split(':');return p.length==2?+p[0]*60+ +p[1]:0};
const n0=s=>(s==='-'||s==='—'||s===undefined)?0:(parseInt(s)||0);
const label=d=>{const t=toks(d);const i=t.indexOf('EPISODES SEARCH');return i>=0?t[i+1]:''};
const leaf=(d,l)=>[...d.querySelectorAll('*')].filter(e=>e.children.length===0&&e.innerText&&e.innerText.trim()===l);
// Opens a game's Skaters page and switches the situation selector (Game total / EV / PP / PK) to `want`. The choice is remembered by InStat.
const ppView=async(f,id,want)=>{const u='/instat/hockey/matches/'+id+'/skaters';f.src='about:blank';await W(200);f.src=u;let d=null;
 for(let k=0;k<40;k++){await W(500);try{const x=f.contentDocument;if(x&&x.body&&f.contentWindow.location.pathname===u&&(x.body.innerText.match(/\nPosition\n/g)||[]).length>=2&&label(x)){d=x;break}}catch(e){}}
 if(!d)return null;
 if(label(d)!==want){const e=leaf(d,label(d)).filter(x=>!/^(TH|TD)$/.test(x.tagName))[0];if(e){(e.closest('button,[role=button]')||e).click();await W(900);const o=leaf(d,want).pop();if(o)o.click();for(let k=0;k<12&&label(d)!==want;k++)await W(500);await W(2500)}}else await W(700);
 if(label(d)!==want)return null;
 const t=toks(d);const S=[];const rows=[];let side=-1;
 for(let i=0;i<t.length-9;i++){if(t[i+1]==='Position'&&t[i+2]==='POS'){S.push(t[i]);side=S.length-1;continue}
  if(side>=0&&/^\d{1,3}$/.test(t[i])&&/^(F|D)$/.test(t[i+2])&&/^(\d+:\d\d|-)$/.test(t[i+3])&&!/^\d+$/.test(t[i+1])){const ppt=sec(t[i+3]),g=n0(t[i+5]),a=n0(t[i+8]);if(ppt||g||a)rows.push([side,t[i],ppt,g,a]);i+=3}}
 return {S,rows};};
const team=async(f,id)=>{const rec={id,m:{},gk:{}};
 let d=await load(f,'/instat/hockey/teams/'+id,d=>d.querySelector('a[href*="/matches/"]'),14);
 if(d){await W(1500);
  // The overview lists 25 games at a time: press "Show more" until the list reaches back past the cutoff date.
  const oldest=()=>{let o='99999999';d.querySelectorAll('a[href*="/matches/"]').forEach(a=>{const m=a.parentElement.innerText.match(/(\d\d)\.(\d\d)\.(\d{4})/);if(m){const v=m[3]+m[2]+m[1];if(v<o)o=v}});return o};
  for(let k=0;k<10&&oldest()>=CUT;k++){const b=[...d.querySelectorAll('button,div,span,a')].filter(e=>e.children.length===0&&e.innerText&&e.innerText.trim()==='Show more').pop();if(!b)break;const n0=d.querySelectorAll('a[href*="/matches/"]').length;(b.closest('button')||b).click();rec.more=(rec.more||0)+1;for(let j=0;j<12&&d.querySelectorAll('a[href*="/matches/"]').length===n0;j++)await W(400);await W(300)}
  const t=toks(d);rec.name=t[2];rec.sub=t[3];rec.ov=d.body.innerText.includes('OVERVIEW');
  d.querySelectorAll('a[href*="/matches/"]').forEach(a=>{const mid=a.getAttribute('href').split('/matches/')[1].split('/')[0];const tx=a.parentElement.innerText;const dm=tx.match(/(\d\d)\.(\d\d)\.(\d{4})/);rec.m[mid]=dm?dm[3]+dm[2]+dm[1]:'';});}
 d=await load(f,'/instat/hockey/teams/'+id+'/goalies',d=>d.body.innerText.includes('SCSV%')&&d.querySelector('a[href*="/players/"]'),10);
 if(d){await W(1000);const grab=()=>{const t=toks(d);const s=t.lastIndexOf('SCSV%');if(s<0)return;for(let i=s+1;i<t.length-7;i++){if(/^\d{1,2}$/.test(t[i])&&/[A-Za-z]/.test(t[i+1])&&/^\d+$/.test(t[i+2])&&/^\d+:\d\d$/.test(t[i+3]))rec.gk[t[i]+'|'+t[i+1]]=[t[i+2],t[i+3],t[i+4],t[i+5],t[i+6],t[i+7]].join(',')}};grab();
  const el=d.querySelector('[class*="RowsList"]');if(el){for(let y=0;y<=el.scrollHeight;y+=200){el.scrollTop=y;el.dispatchEvent(new Event('scroll',{bubbles:true}));await W(200);grab()}}}
 st.T[id]=rec;st.tdone++;
 for(const mid in rec.m){if(rec.m[mid]>=CUT&&!KNOWN.has(mid))st.newIds[mid]=rec.m[mid]}};
const match=async(f,id)=>{const cnt=d=>(d.body.innerText.match(/Shirt number/g)||[]).length;
 const d=await load(f,'/instat/hockey/matches/'+id,d=>cnt(d)>=2&&/\d\d\.\d\d\.\d{4}/.test(d.body.innerText.slice(0,400))&&d.querySelectorAll('a[href*="/teams/"]').length>=2,20);const rec={id,S:[],P:[],ok:false};
 if(d){await W(800);const t=toks(d);const di=t.findIndex(x=>/^\d\d\.\d\d\.\d{4}$/.test(x));rec.h=di>=0?[t[di],t[di+1],t[di+2],t[di+3],t[di+4]].join('~'):'';
  rec.tl=[];d.querySelectorAll('a[href*="/teams/"]').forEach(a=>{const i=a.getAttribute('href').split('/teams/')[1].split('/')[0];const n=a.innerText.trim();if(n&&rec.tl.length<2&&!rec.tl.some(x=>x.startsWith(i+'=')))rec.tl.push(i+'='+n)});
  const links=[...d.querySelectorAll('a[href*="/players/"]')].map(a=>[a.innerText.trim(),a.getAttribute('href').split('/players/')[1].split('/')[0],0]);
  let side=-1;for(let i=0;i<t.length-13;i++){if(t[i+1]==='Shirt number'){rec.S.push(t[i]);side=rec.S.length-1;continue}
   if(side>=0&&/^\d{1,3}$/.test(t[i])&&/^(F|D|GK)$/.test(t[i+2])&&/^\d+:\d\d$/.test(t[i+3])&&!/^\d+$/.test(t[i+1])){const L=links.find(l=>!l[2]&&l[0]===t[i+1]);if(L)L[2]=1; /* links are consumed in page order, so players sharing a name ("noname noname") each get their own id */const pen=t[i+13];rec.P.push([side,t[i],t[i+1],t[i+2],sec(t[i+3]),n0(t[i+6]),n0(t[i+7]),n0(t[i+9]),pen&&pen.includes(':')?+pen.split(':')[0]:n0(pen),L?L[1]:''].join('|'));const fo=n0(t[i+14]);if(fo){rec.FO=rec.FO||{};rec.FO[side+'|'+t[i]]=fo}i+=3}}
  rec.ok=rec.S.length===2&&rec.P.length>=10&&!!rec.h&&rec.tl.length===2;}
 // power-play view of the same game: PP time, goals and assists per player
 if(rec.ok){const pp=await ppView(f,id,'PP');if(pp){rec.PP={};const idx=pp.S.map((n,i)=>{const k=rec.S.indexOf(n.toUpperCase());return k>=0?k:i});pp.rows.forEach(r=>{const k=idx[r[0]]+'|'+r[1];if(!(k in rec.PP))rec.PP[k]=[r[2],r[3],r[4]]})}else rec.ok=false}
 st.M[id]=rec;st.mdone++;};
(async()=>{try{
 const fs=[mk(),mk(),mk()];let q=TEAMS.filter(i=>!(i in st.T));
 await Promise.all(fs.map(async f=>{while(q.length){const id=q.shift();try{await team(f,id)}catch(e){st.err.push('t'+id+':'+e)}if(st.tdone%10===0)save()}}));save();
 st.phase='matches';let mq=Object.keys(st.newIds).concat(CANARY).filter(i=>!(st.M[i]&&st.M[i].ok));const mq0=mq[0];st.mtotal=mq.length;
 await Promise.all(fs.map(async f=>{while(mq.length){const id=mq.shift();try{await match(f,id)}catch(e){st.err.push('m'+id+':'+e)}if(st.mdone%12===0)save()}}));
 // put InStat's situation selector back to Game total so Mike's own view is unchanged
 if(mq0)try{await ppView(fs[0],mq0,'Game total')}catch(e){}
 st.phase='done';save();}catch(e){st.err.push('fatal:'+e);st.phase='failed'}})();
return 'started '+TEAMS.length+' teams';})()
