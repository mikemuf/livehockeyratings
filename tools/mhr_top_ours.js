const fs=require('fs');const h=fs.readFileSync('index.html','utf8');
const grab=n=>JSON.parse(h.match(new RegExp('const '+n+'\\s*=\\s*(\\[\\[.*?\\]\\]);'))[1]);
const G=grab('BASE').concat(grab('WEEKEND_GAMES'));const seen=new Set,o={};
for(const g of G){if(g[1]<'2026-11-18')continue;const k=g.join('|');if(seen.has(k))continue;seen.add(k);(o[g[0]]=o[g[0]]||[]).push([+g[1].slice(8),g[2],g[3],g[4],g[5]])}
fs.writeFileSync('/tmp/nar/ours.json',JSON.stringify(o));console.log(Object.keys(o).map(k=>k+':'+o[k].length).join(' '),JSON.stringify(o).length)
