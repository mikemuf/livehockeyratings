// Silver Stick box-score reader (Nov 26 2026, owner 1:30 PM: "why are the goal details not showing up"). Paste once into the season games tab
// AFTER tools/ss_list.js. Each check: `const r=await window.__ssl(DAY);window.__ssboxgo(DAY);r` then `await window.__ssw()` -> compact lines
// "id STATUS vs-hs G [goalies] :: goals" joined by ' @@ ' (the format tools/live_full.py reads). Reads each live game's Box score tab in a hidden
// frame, three at a time; a final game is read once more after it ends (window.__ssfin remembers). 2017-division rows are skipped.
// Goal = period digit + clock + v|h + ':' + 'num NAME/num ASSIST/...'. Names DO show for the 2015 division (seen Nov 26).
window.__ssfin=window.__ssfin||{};
window.__ssbox1=async(id)=>{const f=document.createElement('iframe');f.style.cssText='position:absolute;left:-6000px;width:1200px;height:900px';document.body.appendChild(f);f.src='/seasons/16542/games/'+id+'?tab=box-score';
 await new Promise(r=>{f.onload=r;setTimeout(r,12000)});let L=[];for(let k=0;k<12;k++){await new Promise(r=>setTimeout(r,600));try{L=f.contentDocument.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean)}catch(e){}if(L.includes('PENALTIES BY PERIOD'))break}
 let line='';try{const vi=L.findIndex(x=>/VISITOR$/.test(x)),hi=L.findIndex(x=>/^HOME\b/.test(x));const v=L[vi+1],h=L[hi+1];const dash=L.indexOf('-',vi);const vs=+L[dash-2],hs=+L[dash+1];
  const st=L.slice(vi+2,dash-2).find(x=>/^(FINAL.*|UNOFFICIAL FINAL|IN PROGRESS|INTERMISSION.*|.*PERIOD|OVERTIME|SHOOTOUT)$/.test(x))||'';
  const sec=(a,b)=>{const i=L.indexOf(a),j=b?L.indexOf(b):L.length;return i<0?[]:L.slice(i+1,j<0?L.length:j)};
  const PER=/^(1ST|2ND|3RD|OT\d*|\dTH|SO|OVERTIME|SHOOTOUT)$/,NONE=/^NO (GOALS|PENALTIES)$/i,TAG=/^(PP|SH|EN|PS|GW|GWG|SO|ENG|PPG|SHG)$/;
  const gl=[];let side=-1;for(const x of sec('GOALTENDING','GOALS BY PERIOD')){if(/^GOALIE/.test(x)){side++;continue}if(/^#\d+ /.test(x))gl.push([side,x])}
  const goals=[];let per='',cur=null;for(const x of sec('GOALS BY PERIOD','PENALTIES BY PERIOD')){if(PER.test(x)){per=x;continue}if(NONE.test(x))continue;if(/^\d{1,2}:\d\d$/.test(x)){cur={p:per,t:x,tags:[],pl:[],team:''};goals.push(cur);continue}if(!cur)continue;if(TAG.test(x)){cur.tags.push(x);continue}if(/^#/.test(x)){cur.pl.push(x);continue}if(!cur.team)cur.team=x}
  const sd=t=>{const a=(t||'').toUpperCase(),V=(v||'').toUpperCase().replace(/\s*\(.*$/,''),H=(h||'').toUpperCase().replace(/\s*\(.*$/,'');return a&&(a===H||a.indexOf(H)===0||H.indexOf(a)===0)?'h':a&&(a===V||a.indexOf(V)===0||V.indexOf(a)===0)?'v':'?'};
  const pk=goals.map(g=>(g.p==='OVERTIME'?'O':g.p==='SHOOTOUT'?'S':g.p[0])+g.t+sd(g.team)+':'+g.pl.map(x=>x.replace(/ \(\d+\)/,'').replace('#','')).join('/')+(g.tags.length?'['+g.tags.join(',')+']':'')).join(';');
  if(!isNaN(vs)&&!isNaN(hs)){line=id+' '+st+' '+vs+'-'+hs+' G '+JSON.stringify(gl)+' :: '+pk;if(/FINAL/.test(st))window.__ssfin[id]=1}else line='';window.__ssboxraw=window.__ssboxraw||{};window.__ssboxraw[id]=L.slice(0,80).join(' | ')}catch(e){line=''}
 f.remove();return line};
window.__ssboxgo=(day)=>{const ids=[];Object.entries(window.__ssraw||{}).forEach(([id,t])=>{if(t.indexOf(day)<0||/\(2017\)/.test(t))return;const parts=t.split(/\(20\d\d\)/);if(parts.length<3)return;if(!/^\s*\d+\s*[-–]\s*\d+/.test(parts[1]))return;const live=/^\s*\d+\s*[-–]\s*\d+\s+LIVE\b/i.test(parts[1]);if(live||!window.__ssfin[id])ids.push(id)});
 window.__pkdone=false;window.__pk=[];(async()=>{for(let i=0;i<ids.length;i+=3){const r=await Promise.all(ids.slice(i,i+3).map(x=>window.__ssbox1(x)));r.forEach(x=>{if(x)window.__pk.push(x)})}window.__pkdone=true})();return ids.length};
window.__pklast=window.__pklast||{};window.__ssw=async()=>{for(let k=0;k<80&&!window.__pkdone;k++)await new Promise(r=>setTimeout(r,500));const ch=window.__pk.filter(l=>{const id=l.split(' ')[0];if(window.__pklast[id]===l)return false;window.__pklast[id]=l;return true});return (window.__pkdone?'':'PARTIAL ')+ch.join(' @@ ')};
// __ssw returns ONLY the lines that changed since the last call (Nov 26 1:40 PM), so an unchanged game costs nothing to pass on.
