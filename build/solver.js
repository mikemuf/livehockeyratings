// MHR pools: 13U+14U are ONE rating pool (top team = 99.99); games vs other pools (15U/16U/18U) don't count.
const XMAP={'2012':{'Dallas Stars Elite (13U)':'2013|Dallas Stars','Thunder Bay Kings (U14)':'2013|Thunder Bay Kings'},
 '2013':{'Team Dallas (14U)':'2012|Team Dallas','Vegas Jr Golden Knights (14U)':'2012|Vegas Jr Golden Knights','San Jose Jr Sharks (14U)':'2012|San Jose Jr Sharks','Thunder Bay Kings (U15)':'2012|Thunder Bay Kings','California Jr Reign (#1) (14U AA)':'2012|California Jr Reign (14U AA)'}};
const XPOOL=/\b(1[5-8]U|U1[6-8])\b|\bHS\b/;
const nodeOf=(dv,t)=>(XMAP[dv]&&XMAP[dv][t])||dv+'|'+t;
const inPool=g=>!XPOOL.test(g[2])&&!XPOOL.test(g[4]);
const _pool={};
function solvePool(extra){
  const key=JSON.stringify(extra||[])+allGames().length;if(_pool.k===key)return _pool.v;
  const all=allGames().concat(extra||[]);const G=[],xc={},_xs=new Set();
  for(const g of all){const [dv,dt,a,ga,b,gb]=g;const A=nodeOf(dv,a),B=nodeOf(dv,b);
    if(!inPool(g)){if(dt<=MHR_THROUGH)for(const [t,x] of [[a,A],[b,B]])if(!XPOOL.test(t))xc[x]=(xc[x]||0)+1;continue}
    const k=dt+'|'+(A<B?A+'|'+ga+'|'+B+'|'+gb:B+'|'+gb+'|'+A+'|'+ga);if(dv!==A.slice(0,4)||dv!==B.slice(0,4)){if(_xs.has(k))continue;_xs.add(k)}
    G.push([dv,dt,A,ga,B,gb])}
  const GB=G.filter(g=>g[1]<=MHR_THROUGH);
  const cur=rawSolve(G), base=rawSolve(GB);
  const M={},MG={};for(const dv of ['2012','2013']){for(const t in (MHR[dv]||{}))M[dv+'|'+t]=MHR[dv][t];
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
  const v={teams,ix,r,rec,agd,sched,gp,M,G,GB,ncomp:cur.ncomp,base};_pool.k=key;_pool.v=v;return v;
}
function solve(dv,extra){
  const P=solvePool(extra);const pre=dv+'|';
  const rows=[];for(let i=0;i<P.teams.length;i++){const t=P.teams[i];if(!t.startsWith(pre))continue;
    const nm=t.slice(pre.length);rows.push({t:nm,r:P.r[i],rec:P.rec[i],agd:P.agd[i],sched:P.sched[i],gp:P.gp[i],mhr:(t in P.M)&&((MHR_REC[dv]||{})[nm]!=='0-0-0'),adj:P.r[i]-(P.sched[i]+P.agd[i])})}
  rows.sort((a,b)=>b.r-a.r);
  const byName=Object.fromEntries(rows.map(x=>[x.t,x]));
  for(const [k,nd] of Object.entries(XMAP[dv]||{})){const i=P.ix[nd];if(i!==undefined)byName[k]={t:k,r:P.r[i],rec:P.rec[i],agd:P.agd[i],sched:P.sched[i],gp:P.gp[i],mhr:nd in P.M,adj:0,other:true}}
  const G=allGames().concat(extra||[]).filter(g=>g[0]===dv&&inPool(g));
  const liveN=G.filter(g=>g[1]>MHR_THROUGH).length;
  return {rows,G,byName,comps:P.ncomp,liveN,nMhr:Object.keys(MHR[dv]||{}).filter(t=>(pre+t) in P.base.ix).length};
}
