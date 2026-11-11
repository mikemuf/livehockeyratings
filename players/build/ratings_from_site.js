// node ratings_from_site.js <ratings site index.html> <out ratings.json>
// Runs the live ratings site's own solver and writes every team's rating, rank, pool and record.
const fs=require('fs');const f=process.argv[2],out=process.argv[3];
const h=fs.readFileSync(f,'utf8');const s=[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]).sort((a,b)=>b.length-a.length)[0];
const stub=`var document={getElementById:()=>({innerHTML:'',addEventListener(){},classList:{add(){},remove(){},toggle(){}},style:{},value:''}),querySelectorAll:()=>[],querySelector:()=>null,addEventListener(){},createElement:()=>({})};var window={addEventListener(){}};var localStorage={getItem:()=>null,setItem(){}};var location={hash:''};`;
const code=s.replace(/\n(render|init)\(\);?\s*$/,'\n');
const R=new Function(stub+code+`;const O={};for(const dv of ['2011','2012','2013','2014','2015']){const S=solve(dv);if(process.env.PROBE)return [Object.keys(S),S.rows[0]];O[dv]={};let u=0,c=0;
 for(const x of S.rows){const ca=canada.has(x.t);const ranked=!!x.mhr;O[dv][x.t]={rating:+x.r.toFixed(2),rank:ranked?(ca?++c:++u):0,pool:ca?'Canada':'USA',rec:x.rec.join('-')}}}return O`)();
if(process.env.PROBE){console.log(JSON.stringify(R));process.exit()}
fs.writeFileSync(out,JSON.stringify(R));console.log(Object.keys(R).map(k=>k+':'+Object.keys(R[k]).length).join(' '));
