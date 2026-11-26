// Silver Stick box-score reader (Nov 26 2026, owner 1:30 PM: "why are the goal details not showing up"). Paste once into the season games tab
// AFTER tools/ss_list.js. Each check: `const r=await window.__ssl(DAY);window.__ssboxgo(DAY);r` then `await window.__ssw()` -> compact lines
// "id STATUS vs-hs G [goalies] :: goals" joined by ' @@ ' (the format tools/live_full.py reads). Reads each live game's Box score tab in a hidden
// frame, three at a time; a final game is read once more after it ends (window.__ssfin remembers). 2017-division rows are skipped.
// HALF-SAVED FINAL SHEET (seen Nov 26 1:47 PM, game 3183157): for a minute or so as a game is closed, every player and goalie reads 'NOT AVAILABLE' and the goalie list is empty; a minute later the names are back with (W)/(L) and PP/GWG tags. The wrapper at the bottom throws such a read away (returns '', does not mark the game read) so the next check reads it again. Names are NOT hidden by the league.
// Goal = period digit + clock + v|h + ':' + 'num NAME/num ASSIST/...'. Names DO show for the 2015 division (seen Nov 26).
window.__ssfin=window.__ssfin||{};
window.__ssbox1=async(id)=>{const f=document.createElement('iframe');f.style.cssText='position:absolute;left:-6000px;width:1200px;height:900px';document.body.appendChild(f);f.src='/seasons/16542/games/'+id+'?tab=box-score';
 await new Promise(r=>{f.onload=r;setTimeout(r,12000)});let L=[];for(let k=0;k<12;k++){await new Promise(r=>setTimeout(r,600));try{L=f.contentDocument.body.innerText.split('\n').map(s=>s.trim()).filter(Boolean)}catch(e){}if(L.includes('PENALTIES BY PERIOD'))break}
 let line='';try{const vi=L.findIndex(x=>/VISITOR$/.test(x)),hi=L.findIndex(x=>/^HOME\b/.test(x));const v=L[vi+1],h=L[hi+1];const dash=L.indexOf('-',vi);const vs=+L[dash-2],hs=+L[dash+1];
  const st=L.slice(vi+2,dash-2).find(x=>/^(FINAL.*|UNOFFICIAL FINAL|IN PROGRESS|INTERMISSION.*|.*PERIOD|OVERTIME|SHOOTOUT)$/.test(x))||'';
  const sec=(a,b)=>{const i=L.indexOf(a),j=b?L.indexOf(b):L.length;return i<0?[]:L.slice(i+1,j<0?L.length:j)};
  const PER=/^(1ST|2ND|3RD|OT\d*|\dTH|SO|OVERTIME|SHOOTOUT)$/,NONE=/^NO (GOALS|PENALTIES)$/i,TAG=/^(PP|SH|EN|PS|GW|GWG|SO|ENG|PPG|SHG)$/;
  const gl=[];let side=-1;for(const x of sec('GOALTENDING','GOALS BY PERIOD')){if(/^GOALIE/.test(x)){side++;continue}if(/^#\d+ /.test(x))gl.push([side,x])}
  const goals=[];let per='',cur=null;for(const x of sec('GOALS BY PERIOD','PENALTIES BY PERIOD')){if(PER.test(x)){per=x;continue}if(NONE.test(x))continue;if(/^\d{1,2}:\d\d$/.test(x)){cur={p:per,t:x,tags:[],pl:[],team:''};goals.push(cur);continue}if(!cur)continue;if(TAG.test(x)){cur.tags.push(x);continue}if(/^#/.test(x)){cur.pl.push(x);continue}if(/^NOT AVAILABLE$/i.test(x)){cur.pl.push('#- NOT AVAILABLE');continue}if(!cur.team)cur.team=x}
  const sd=t=>{const a=(t||'').toUpperCase(),V=(v||'').toUpperCase().replace(/\s*\(.*$/,''),H=(h||'').toUpperCase().replace(/\s*\(.*$/,'');return a&&(a===H||a.indexOf(H)===0||H.indexOf(a)===0)?'h':a&&(a===V||a.indexOf(V)===0||V.indexOf(a)===0)?'v':'?'};
  const pk=goals.map(g=>(g.p==='OVERTIME'?'O':g.p==='SHOOTOUT'?'S':g.p[0])+g.t+sd(g.team)+':'+g.pl.map(x=>x.replace(/ \(\d+\)/,'').replace('#','')).join('/')+(g.tags.length?'['+g.tags.join(',')+']':'')).join(';');
  if(!isNaN(vs)&&!isNaN(hs)){line=id+' '+st+' '+vs+'-'+hs+' G '+JSON.stringify(gl)+' :: '+pk;if(/FINAL/.test(st))window.__ssfin[id]=1}else line='';window.__ssboxraw=window.__ssboxraw||{};window.__ssboxraw[id]=L.slice(0,80).join(' | ')}catch(e){line=''}
 f.remove();return line};
window.__ssboxgo=(day)=>{const ids=[];Object.entries(window.__ssraw||{}).forEach(([id,t])=>{if(t.indexOf(day)<0||/\(2017\)/.test(t))return;const parts=t.split(/\(20\d\d\)/);if(parts.length<3)return;if(!/^\s*\d+\s*[-–]\s*\d+/.test(parts[1]))return;const live=/^\s*\d+\s*[-–]\s*\d+\s+LIVE\b/i.test(parts[1]);if(live||!window.__ssfin[id])ids.push(id)});
 window.__pkdone=false;window.__pk=[];(async()=>{for(let i=0;i<ids.length;i+=3){const r=await Promise.all(ids.slice(i,i+3).map(x=>window.__ssbox1(x)));r.forEach(x=>{if(x)window.__pk.push(x)})}window.__pkdone=true})();return ids.length};
// DELTAS (Nov 26 2:05 PM): javascript results are cut at about 1,000 characters, and five live games' full goal lists do not fit. __ssw now returns,
// per changed game, 'id ST v-h G <goalies json, or the word same when unchanged (an '=' got the whole answer blocked as 'query string data')> :: +START:<only the goals after the first START>' and pages the answer:
// if it ends with ' MORE', call window.__sspage() until it does not. tools/ss_check.py keeps the full lists (/tmp/gs/ss_pk_state.json) and prints
// RESYNC NEEDED if the two sides disagree: then run window.__ssresync(id) and the next check sends that game whole.
window.__pkst=window.__pkst||{};window.__more=[];
window.__sspage=()=>{let out='';while(window.__more.length&&(out.length+window.__more[0].length<880||!out)){out+=(out?' @@ ':'')+window.__more.shift()}return out+(window.__more.length?' MORE':'')};
window.__ssw=async()=>{for(let k=0;k<80&&!window.__pkdone;k++)await new Promise(r=>setTimeout(r,500));const res=[];
 for(const l of window.__pk){const m=l.match(/^(\d+) (.*?) (\d+-\d+) G (.*?) :: (.*)$/);if(!m)continue;const id=m[1],hd=m[2]+' '+m[3],gl=m[4],goals=m[5].split(';').filter(Boolean);const p=window.__pkst[id]||{n:0,g:null,h:''};
  const reset=goals.length<p.n||(p.sig&&goals.slice(0,p.n).join(';')!==p.sig);const start=reset?0:p.n;const nw=goals.slice(start);
  if(!reset&&!nw.length&&hd===p.h&&gl===p.g)continue;
  res.push(id+' '+hd+' G '+(gl===p.g?'same':gl)+' :: +'+start+':'+nw.join(';'));window.__pkst[id]={n:goals.length,g:gl,h:hd,sig:goals.join(';')}}
 window.__more=res;return (window.__pkdone?'':'PARTIAL ')+window.__sspage()};
window.__ssresync=id=>{delete window.__pkst[id]};
window.__ssbox1o=window.__ssbox1;window.__ssbox1=async id=>{const l=await window.__ssbox1o(id);const gs=(l.split(' :: ')[1]||'').split(';').filter(Boolean);const allna=gs.length>0&&gs.every(g=>/NOT AVAILABLE/.test(g));if(allna||(/ FINAL/.test(l)&&/ G \[\] /.test(l))){delete window.__ssfin[id];return ''}return l};
// ONE CALL PER CHECK (Nov 26 2:20 PM): await window.__ssgo('Nov 26') -> '<score rows of the tracked divisions> %% <delta lines>'.
window.__ssgo=async(day)=>{await window.__ssl(day);window.__ssboxgo(day);const p=await window.__ssw();const rows=[];Object.entries(window.__ssraw).forEach(([id,t])=>{if(t.indexOf(day)<0||/\(2017\)/.test(t))return;const parts=t.split(/\(20\d\d\)/);const m=(parts[1]||'').match(/^\s*(\d+)\s*[-\u2013]\s*(\d+)(\s+LIVE)?/);if(m)rows.push(id+'~'+m[1]+'~'+m[2]+'~'+(m[3]?'IN PROGRESS':'FINAL'))});return rows.join(' ## ')+' %% '+p};
