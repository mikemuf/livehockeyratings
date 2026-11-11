// MHR pools: 13U+14U are ONE rating pool (top team = 99.99); games vs other pools (15U/16U/18U) don't count.
const XMAP={'2012':{'Dallas Stars Elite (13U)':'2013|Dallas Stars','Thunder Bay Kings (U14)':'2013|Thunder Bay Kings'},
 '2013':{'Team Dallas (14U)':'2012|Team Dallas','Vegas Jr Golden Knights (14U)':'2012|Vegas Jr Golden Knights','San Jose Jr Sharks (14U)':'2012|San Jose Jr Sharks','Thunder Bay Kings (U15)':'2012|Thunder Bay Kings','California Jr Reign (#1) (14U AA)':'2012|California Jr Reign (14U AA)'}};
const XPOOL=/\b(1[5-8]U|U1[6-8])\b|\bHS\b/;
const nodeOf=(dv,t)=>(XMAP[dv]&&XMAP[dv][t])||dv+'|'+t;
const inPool=g=>!XPOOL.test(g[2])&&!XPOOL.test(g[4]);
const POOLS={A:['2012','2013'],B:['2014','2015']},POOL_OF={'2012':'A','2013':'A','2014':'B','2015':'B'};
const _pool={};
function solvePool(extra,pool){
  pool=pool||'A';const PD=POOLS[pool];const _c=_pool[pool]=_pool[pool]||{};
  const key=JSON.stringify(extra||[])+allGames().length;if(_c.k===key)return _c.v;
  const all=allGames().concat(extra||[]).filter(g=>PD.includes(g[0]));const G=[],xc={},_xs=new Set();
  for(const g of all){const [dv,dt,a,ga,b,gb]=g;const A=nodeOf(dv,a),B=nodeOf(dv,b);
    if(!inPool(g)){if(dt<=MHR_THROUGH)for(const [t,x] of [[a,A],[b,B]])if(!XPOOL.test(t))xc[x]=(xc[x]||0)+1;continue}
    const k=dt+'|'+(A<B?A+'|'+ga+'|'+B+'|'+gb:B+'|'+gb+'|'+A+'|'+ga);if(dv!==A.slice(0,4)||dv!==B.slice(0,4)){if(_xs.has(k))continue;_xs.add(k)}
    G.push([dv,dt,A,ga,B,gb])}
  const GB=G.filter(g=>g[1]<=MHR_THROUGH);
  const cur=rawSolve(G), base=rawSolve(GB);
  const M={},MG={};for(const dv of PD){for(const t in (MHR[dv]||{}))M[dv+'|'+t]=MHR[dv][t];
    const g=(typeof MHR_GP!=='undefined'&&MHR_GP[dv])||{};for(const t in g)MG[dv+'|'+t]=g[t]-(xc[dv+'|'+t]||0)}
  const cs=[];for(const t in M){if(t in base.ix)cs.push(M[t]-base.r[base.ix[t]])}
  cs.sort((a,b)=>a-b);const off=cs.length?(cs.length%2?cs[(cs.length-1)/2]:(cs[cs.length/2-1]+cs[cs.length/2])/2):0;
  const {teams,ix,opp,gp,rec,agd}=cur;const n=teams.length;
  const T=teams.map((t,i)=>t in M?M[t]:(t in base.ix?base.r[base.ix[t]]+off:null));
  const nb=new Array(n).fill(0),sb=new Array(n).fill(0),gb=new Array(n).fill(0);
  for(const [d,dt,a,ga,b,gbb] of GB){const i=ix[a],j=ix[b];const dd=Math.max(-CAP,Math.min(CAP,ga-gbb));nb[i]++;nb[j]++;sb[i]+=T[j];sb[j]+=T[i];gb[i]+=dd;gb[j]-=dd}
  const p=new Array(n).fill(0),c=new Array(n).fill(0),corr=new Array(n).fill(0);
  for(let i=0;i<n;i++){const t=teams[i];
    if(T[i]===null){corr[i]=0;continue}
    const ph=Math.max(0,(MG[t]||0)-nb[i]);
    if(ph>0){p[i]=ph;c[i]=((nb[i]+ph)*T[i]-sb[i]-gb[i])/ph}
    else if(nb[i]>0)corr[i]=T[i]-(sb[i]+gb[i])/nb[i];}
  const gd=agd.map((v,i)=>v*gp[i]);
  let r=T.map(v=>v===null?ANCHOR:v);
  const live=G.length>GB.length;
  for(let it=0;it<(live?2500:0);it++){const nw=new Array(n);
    for(let i=0;i<n;i++){let s=0;for(const j of opp[i])s+=r[j];
      const v=p[i]>0?(s+gd[i]+p[i]*c[i])/(gp[i]+p[i]):(s+gd[i])/gp[i]+corr[i];nw[i]=0.5*r[i]+0.5*v}
    r=nw}
  if(n){const vals=Object.values(M);if(vals.length){const top=Math.max(...vals);let mx=-Infinity;for(let i=0;i<n;i++)if(teams[i] in M&&r[i]>mx)mx=r[i];if(isFinite(mx)){const sh=top-mx;for(let i=0;i<n;i++)r[i]+=sh}}}
  const sched=r.map((_,i)=>opp[i].reduce((s,j)=>s+r[j],0)/gp[i]);
  const v={teams,ix,r,rec,agd,sched,gp,M,G,GB,ncomp:cur.ncomp,base};_c.k=key;_c.v=v;return v;
}
function solveFull(dv,extra){
  const P=solvePool(extra,POOL_OF[dv]);const pre=dv+'|';
  const rows=[];for(let i=0;i<P.teams.length;i++){const t=P.teams[i];if(!t.startsWith(pre))continue;
    const nm=t.slice(pre.length);rows.push({t:nm,r:P.r[i],rec:P.rec[i],agd:P.agd[i],sched:P.sched[i],gp:P.gp[i],mhr:(t in P.M)&&((MHR_REC[dv]||{})[nm]!=='0-0-0'),adj:P.r[i]-(P.sched[i]+P.agd[i])})}
  rows.sort((a,b)=>b.r-a.r);
  const byName=Object.fromEntries(rows.map(x=>[x.t,x]));
  for(const [k,nd] of Object.entries(XMAP[dv]||{})){const i=P.ix[nd];if(i!==undefined)byName[k]={t:k,r:P.r[i],rec:P.rec[i],agd:P.agd[i],sched:P.sched[i],gp:P.gp[i],mhr:nd in P.M,adj:0,other:true}}
  const G=allGames().concat(extra||[]).filter(g=>g[0]===dv&&inPool(g));
  const liveN=G.filter(g=>g[1]>MHR_THROUGH).length;
  return {rows,G,byName,comps:P.ncomp,liveN,nMhr:Object.keys(MHR[dv]||{}).filter(t=>(pre+t) in P.base.ix).length};
}

// --- "Lite" divisions (2014 = USA 12U, 2015 = USA 11U; one MHR pool, top 12U = 99.99).
// No full game history: each team starts exactly at its published MHR numbers (rating, record, AGD, schedule),
// and every newer game is folded in with MHR's formula: AGD and schedule are running averages over all games,
// rating = AGD + schedule + the team's published adjustment. Iterated so opponents' new ratings feed back in.
const LITE_DIVS=Object.keys(LITE);
// the top team of the first anchored division keeps its published rating (99.99 in a full pool; lower for 15U, which MHR rates inside the 16U pool)
const LITE_TOP=LITE_DIVS.length?Math.max(...Object.values(LITE[LITE_DIVS[0]]).map(a=>a[0])):99.99;
const _lite={};
function liteFind(dv,t){if(LITE[dv][t])return dv+'|'+t;for(const o of LITE_DIVS)if(o!==dv&&LITE[o][t])return o+'|'+t;return null}
function solveLite(dv,extra){
  const key=dv+JSON.stringify(extra||[])+allGames().length;if(_lite.k===key)return _lite.v;
  const T={};for(const d of LITE_DIVS)for(const [t,a] of Object.entries(LITE[d])){const [R,w,l,ti,agd,sch]=a;const n=w+l+ti;T[d+'|'+t]={dv:d,t,R,n,agd,sch,adj:R-(agd+sch),w,l,ti,dsum:0,opp:[],r:R}}
  const all=allGames().concat(extra||[]).filter(g=>LITE[g[0]]&&g[1]>MHR_THROUGH);
  const used=[],seen=new Set();
  for(const g of all){const A=liteFind(g[0],g[2]),B=liteFind(g[0],g[4]);if(!A||!B||A===B)continue;
    const k=g[1]+'|'+[A+':'+g[3],B+':'+g[5]].sort().join('|');if(seen.has(k))continue;seen.add(k);
    const d=Math.max(-CAP,Math.min(CAP,g[3]-g[5]));T[A].dsum+=d;T[B].dsum-=d;T[A].opp.push(B);T[B].opp.push(A);
    for(const [X,gf,ga] of [[T[A],g[3],g[5]],[T[B],g[5],g[3]]]){gf>ga?X.w++:gf<ga?X.l++:X.ti++}
    used.push(g)}
  const keys=Object.keys(T);
  for(let it=0;it<60;it++){const nr={};
    for(const k of keys){const x=T[k];const m=x.opp.length;if(!m){nr[k]=x.r;continue}
      const N=x.n+m;const agd=(x.agd*x.n+x.dsum)/N;const sch=(x.sch*x.n+x.opp.reduce((s,o)=>s+T[o].r,0))/N;nr[k]=agd+sch+x.adj}
    let top=-Infinity;for(const k of keys)if(T[k].dv===LITE_DIVS[0])top=Math.max(top,nr[k]);
    const sh=used.length?LITE_TOP-top:0;for(const k of keys)T[k].r=nr[k]+sh}
  const rows=[];for(const k of keys){const x=T[k];if(x.dv!==dv)continue;const m=x.opp.length,N=x.n+m;
    const agd=m?(x.agd*x.n+x.dsum)/N:x.agd,sch=m?(x.sch*x.n+x.opp.reduce((s,o)=>s+T[o].r,0))/N:x.sch;
    rows.push({t:x.t,r:x.r,rec:[x.w,x.l,x.ti],agd,sched:sch,gp:N,mhr:true,adj:x.r-(agd+sch)})}
  rows.sort((a,b)=>b.r-a.r);
  const byName=Object.fromEntries(rows.map(x=>[x.t,x]));
  for(const k of keys){const x=T[k];if(x.dv!==dv&&!byName[x.t]&&x.opp.length)byName[x.t]={t:x.t,r:x.r,rec:[x.w,x.l,x.ti],agd:x.agd,sched:x.sch,gp:x.n+x.opp.length,mhr:true,adj:0,other:true}}
  const G=used.filter(g=>g[0]===dv);
  const v={rows,G,byName,comps:1,liveN:G.length,nMhr:rows.length,lite:true};_lite.k=key;_lite.v=v;return v;
}
function solve(dv,extra){return LITE[dv]?solveLite(dv,extra):solveFull(dv,extra)}
