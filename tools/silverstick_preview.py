import json,re,subprocess,datetime
R=json.load(open('/tmp/r_new.json')); SS=json.load(open('data/silverstick_2026.json')); MP=json.load(open('data/silverstick_2026_names.json'))
MP['2015|Pittsburgh Penguins']='Pittsburgh Penguins Elite (Mueller)'; MP['2013|Connecticut Nor\'Easter']="Nor'easters"
json.dump(MP,open('data/silverstick_2026_names.json','w'),indent=0)
W=json.load(open('data/weekend_public.json'))
def info(y,t):
    n=MP.get(f'{y}|{t}'); d=R[y].get(n) if n else None
    disp=re.sub(r' \((Elite|Mueller)\)$','',n) if n else t
    disp={'Mid-Fairfield Hockey Club':'Mid-Fairfield','Middlesex Islanders East':'Middlesex Islanders'}.get(disp,disp)
    return disp,(d['na'] if d else None),(d['rating'] if d else None)
def lab(y,t,rt=True):
    n,k,r=info(y,t)
    if k is None: return n+' (not rated)'
    return f"#{k} {n}"+(f" ({r:.2f})" if rt else '')
def ss_section(y):
    pools=SS[y]['pools']; allt=[t for ts in pools.values() for t in ts]
    rk={t:info(y,t)[1] or 999 for t in allt}
    top10=sorted([t for t in allt if rk[t]<=10],key=lambda t:rk[t]); top30=[t for t in allt if rk[t]<=30]
    infield={MP.get(f'{y}|{t}') for t in allt}
    missing=[n for n,d in sorted(R[y].items(),key=lambda x:x[1]['na'] or 999) if d['na'] and d['na']<=10 and n not in infield]
    b=[f"The field: 30 teams in six pools of five. {len(top10)} of the top 10 in North America and {len(top30)} of the top 30 are entered: "+', '.join(lab(y,t,False) for t in top10)+'.']
    if missing: b.append("Not in the field: "+', '.join(f"#{R[y][n]['na']} {re.sub(r' Hockey Academy$| \(Elite\)$','',n)}" for n in missing)+'.')
    b.append("Format: Four pool games each from Thursday to Saturday. A win is 2 points and a tie is 1; there is no overtime in pool play. The six pool winners and two wildcards reach the quarterfinals, and the champion is crowned Sunday.")
    b.append("Wildcards: The two best teams that do not win a pool. Ties in points go to head-to-head, then wins, then share of goals scored, so every goal counts.")
    stren={}
    for p,ts in pools.items():
        srt=sorted(ts,key=lambda t:rk[t]); stren[p]=sum(sorted(rk[t] for t in ts)[:3])
        b.append(f"Pool {p}: "+', '.join(lab(y,t) for t in srt)+'.')
    tough=min(stren,key=stren.get); tt=sorted(pools[tough],key=lambda t:rk[t])[:3]
    b.append(f"Toughest pool: Pool {tough}, with "+', '.join(lab(y,t,False) for t in tt)+" chasing one automatic spot.")
    gs=[g for g in SS[y]['games'] if rk[g['a']]<=20 and rk[g['b']]<=20]
    gs=sorted(gs,key=lambda g:rk[g['a']]+rk[g['b']])[:5]; gs=sorted(gs,key=lambda g:g['sort'])
    if gs: b.append("Games to circle: "+'; '.join(f"{lab(y,g['a'],False)} against {lab(y,g['b'],False)}, {g['day']} {g['ct']}" for g in gs)+'.')
    first=SS[y]['games'][0]; b.append(f"First game: Thursday at {first['ct']} Central. Scores and the pool tables will be here all weekend.")
    return {'t':'Next: International Silver Stick, Nov 26–29 (Whitby, Ontario)','b':b}
WRAP={
'2012':["Shattuck St Mary's (#2, 99.95) swept three games at Little Caesars (#7, 97.24): 5-1, 8-3 and 4-1.",
 "Mid-Fairfield (#1, 99.99) went 3-0 in Pittsburgh and is 32-0-3. The Chicago Reapers pushed it on Sunday before losing 5-3.",
 "Upset of the weekend: the Chicago Reapers (#30, 95.72) beat Mount St Charles (#16, 96.36) 5-4 in overtime on Saturday.",
 "Bishop Kearney (#14, 96.56) won all three at the Northeast Pack, 5-3 over the Chicago Mission, 9-1 over the Rockets and 4-2 over Mount St Charles, and is second in the league.",
 "Team Illinois (#10, 97.09) won its own showcase at 4-0 and outscored its opponents 33-3.",
 "Pat Quinn Classic: Yale Hockey Academy won the title, 3-2 over Delta Hockey Academy in the final, and finished 5-0."],
'2011':["Bishop Kearney (#3, 95.86) had the best weekend in the age group: 3-0 in Pittsburgh, including a 4-2 win over Pittsburgh Penguins Elite (#1, 96.84). It leads the Northeast Pack with 25 points.",
 "Mount St Charles (#4, 95.61) has won eight straight league games and sits two points back.",
 "Chicago Mission (#13, 93.91) went 1-2: a 5-4 loss to Mount St Charles, a 3-2 win over Mid-Fairfield with three power-play goals, and a 7-3 loss to Penguins Elite.",
 "In Toronto, Vaughan Kings (#2, 96.04) shut out Toronto Jr Canadiens (#5, 95.16) 2-0 and are still unbeaten at 26-0-1.",
 "Toronto Jr Canadiens (#5, 95.16) answered Sunday with a 3-1 win over Toronto Marlboros (#7, 94.62).",
 "Oakland Jr Grizzlies (#12, 93.99) held off Fox Motors 5-4."],
'2013':["Upset: Milwaukee Jr Admirals (#27, 90.48) beat the Chicago Reapers (#2, 94.80) 5-2 on Sunday afternoon, hours after the Reapers won the first game 8-0.",
 "Most of the rest of the top 20 were off ahead of the Silver Stick.",
 "Toronto Marlboros (#3, 94.32) beat Vaughan Kings (#10, 92.75) 3-2 and Don Mills 5-1, and are still unbeaten at 21-0-1.",
 "Little Caesars (#5, 93.58) beat Compuware 10-1. Mid-Fairfield (#6, 93.54) swept Providence 8-2 and 9-3.",
 "Middlesex Islanders (#23, 90.85) won twice in New England, 5-3 over South Shore Kings and 5-2 over Providence.",
 ],
'2014':["Florida Alliance (#6, 98.64) won the St. Louis showcase at 5-0, beating Victory Honda (#19, 96.16) 8-6 in the final.",
 "Chicago Mission (#45, 94.28) lost its first three, then won twice in overtime: 3-2 over Philadelphia and 4-3 over Vegas (#29, 95.68).",
 "Chicago Reapers (#28, 95.70) finished fourth after a 4-3 loss to St Louis Blues (#16, 96.48). They trailed 4-0.",
 "In Toronto, Toronto Marlboros (#5, 98.93) beat Don Mills (#12, 97.11) 4-1. Don Mills then tied Markham 1-1 on Sunday."],
'2015':["Toronto Jr Canadiens (#1, 95.25) beat Toronto Marlboros (#8, 93.47) 7-1 and moved to #1 in North America.",
 "Mid-Fairfield (#6, 93.96) went 3-1 on its New England trip: 5-2 and 7-2 at Providence, then a 4-3 loss and a 6-0 win at Bay State Breakers.",
 "Upset: HB Detroit shut out Oakland Jr Grizzlies (#39, 90.40) 4-0 on Sunday, a day after Oakland tied Victory Honda 4-4.",
 "Providence Capitals (#16, 92.16) bounced back with a 3-1 win over the Jr Terriers."],
'2016':["St Louis Blues (#12, 96.57) won the only top-25 matchup of the weekend, 3-2 at Chicago Mission (#33, 94.63).",
 "In Toronto, Toronto Marlboros (#4, 97.90) beat Vaughan Kings (#7, 97.43) 4-1. Vaughan answered with a 5-0 win over Markham.",
 "Markham lost again Sunday, 2-1 to North York Rangers.",
 "Toronto Jr Canadiens (#3, 97.90) edged Toronto Titans (#29, 94.82) 2-1 on Sunday."]}
for y,d in W['divs'].items():
    d['sections']=[s for s in d['sections'] if s['t']!='Weekend wrap' and not s['t'].startswith('Next: International Silver Stick')]
    new=[{'t':'Weekend wrap','b':WRAP[y]}]
    if y in SS: new.append(ss_section(y))
    d['sections']=new+d['sections']
W['status']='Weekend wrap. Final'
W['updated']=subprocess.check_output(['date','+%a %b %-d, %-I:%M %p CT']).decode().strip()
W['next']='Next: the International Silver Stick in Whitby, Nov 26–29.'
json.dump(W,open('data/weekend_public.json','w'),indent=1,ensure_ascii=False)
for y in SS:
    print('=====',y)
    for x in ss_section(y)['b']: print(' -',x)
