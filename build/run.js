// node build/run.js [file] [div] [N] [--base]  -> top N (USA, MHR-ranked) ratings
const fs=require('fs');const f=process.argv[2]||'index.html',dv=process.argv[3]||'2012',N=+(process.argv[4]||25);
const h=fs.readFileSync(f,'utf8');const scripts=[...h.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m=>m[1]);const s=scripts.sort((a,b)=>b.length-a.length)[0];
const stub=`var document={getElementById:()=>({innerHTML:'',addEventListener(){},classList:{add(){},remove(){},toggle(){}},style:{},value:''}),querySelectorAll:()=>[],querySelector:()=>null,addEventListener(){},createElement:()=>({})};var window={addEventListener(){}};var localStorage={getItem:()=>null,setItem(){}};var location={hash:''};`;
let code=s.replace(/\n(render|init)\(\);?\s*$/,'\n');
const out=new Function(stub+code+`;if(${process.argv.includes('--base')}){added=[];for(let i=BASE.length-1;i>=0;i--)if(BASE[i][1]>MHR_THROUGH)BASE.splice(i,1);}
const S=solve('${dv}',${process.argv.includes('--base')}?[]:undefined);return S.rows.filter(x=>x.mhr&&!canada.has(x.t)).slice(0,${N}).map((x,i)=>(i+1)+'|'+x.t+'|'+x.r.toFixed(2)+'|'+(MHR['${dv}'][x.t]||0).toFixed(2)).join('\\n')`)();
console.log(out);
