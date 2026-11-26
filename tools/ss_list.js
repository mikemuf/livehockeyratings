// Silver Stick live score reader (Nov 25, 2026). Tab on https://gamesheetstats.com/seasons/16542/games?filter%5Bstatus%5D=all
// Paste once per tab; then `await window.__ssl('Nov 26')` returns "N rows | id~vs~hs~status ## ..." for that date's games that are live or final
// (feed everything after "| " to tools/ss_score.py). The list is virtualized inside a scrolling DIV; the reader scrolls it in 450 px steps (240 rows, about 8 s).
// TESTED Nov 25 8:40 PM on scheduled games only. A scheduled row reads:
//   "Nov 26, 2026 Sudbury Wolves U12 11U AAA (2015) 1:30 PM Toronto Marlboros U12 11U AAA (2015) Iroquois Park Sports Centre #6 10 Tournament"
// The start time (EASTERN) sits between the two teams; once a game is live the score takes that place. LIVE ROW FORMAT CONFIRMED Nov 26 12:27 PM: '... (2017) 0-1 LIVE Whitby ...' (score then the word LIVE; parsed as IN PROGRESS, mid '0-1'). FINAL row still to confirm at the first final. Old note:
// at the first live game read window.__ssraw[id] and window.__ssmid[id], confirm the parse below, fix it here if needed. Unknown middles come back as status "?:<middle text>".
window.__ssl=async(day)=>{const sc=[...document.querySelectorAll('div')].find(d=>/overflow-auto/.test(d.className)&&d.scrollHeight>d.clientHeight+200)||document.scrollingElement;
 const rows=new Map();sc.scrollTop=0;await new Promise(r=>setTimeout(r,500));let still=0;
 for(let i=0;i<400&&still<4;i++){document.querySelectorAll('a[href*="/games/"]').forEach(a=>{const m=a.getAttribute('href').match(/\/games\/(\d+)/);if(!m)return;let row=a;for(let k=0;k<10&&row&&!(/20\d\d/.test(row.innerText)&&/AAA/.test(row.innerText));k++)row=row.parentElement;if(row&&row.innerText.length<400)rows.set(m[1],row.innerText.replace(/\s+/g,' ').trim())});
  const before=sc.scrollTop;sc.scrollTop+=450;await new Promise(r=>setTimeout(r,260));if(sc.scrollTop===before)still++;else still=0}
 window.__ssraw=Object.fromEntries(rows);window.__ssmid={};const out=[];
 rows.forEach((t,id)=>{if(day&&t.indexOf(day)<0)return;const parts=t.split(/\(20\d\d\)/);if(parts.length<3)return;
  const mid=(parts[1].match(/^[^A-Za-z]*(?:[AP]M|Final|FINAL|OT|SO|Period|Int\w*|\d(?:st|nd|rd)\b[^A-Z]*)?[^A-Z]*/)||[''])[0].trim();window.__ssmid[id]=mid;
  if(/^\d{1,2}:\d\d [AP]M$/.test(mid))return; // not started
  const n=mid.match(/(\d{1,2})\s*[-–:]\s*(\d{1,2})/);const st=/final/i.test(t.slice(0,t.indexOf(parts[2])))?('FINAL'+(/\bOT\b/.test(mid)?' (OT)':/\bSO\b/.test(mid)?' (SO)':'')):'IN PROGRESS';
  out.push(n?id+'~'+n[1]+'~'+n[2]+'~'+st:id+'~~~?:'+mid)});
 return rows.size+' rows | '+out.join(' ## ')};
