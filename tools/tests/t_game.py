import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/livehockeyratings/index.html'); await pg.wait_for_timeout(1500)
        for y in ['2013','2011','2015']:
            await pg.evaluate("y=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith(y));if(b)b.click()}",y); await pg.wait_for_timeout(900)
            hs=await pg.evaluate("[...document.querySelectorAll('section.view.on h3,section.view.on h4,section.view.on summary')].map(e=>e.innerText.trim().slice(0,50)).filter(Boolean).join(' / ')")
            print(y,'h',await pg.evaluate("document.documentElement.scrollHeight"),hs[:600])
            keys=await pg.evaluate("[...new Set([...document.querySelectorAll('section.view.on tr[data-gm]')].map(e=>e.dataset.gm))]")
            print(' clickable finals',len(keys))
            out=await pg.evaluate("""(a)=>{const S=[];a.forEach(k=>{try{const B=k[0]==='b'?WEEKEND_BOX[+k.slice(1)]:(()=>{const g=WEEKEND_GAMES[+k.slice(1)];const i=boxFor(g[0],g[1],g[2],g[4]);return i>=0?WEEKEND_BOX[i]:null})();S.push(k+': '+(B?wkStory(B):'NO BOX'))}catch(e){S.push(k+' ERR '+e)}});return S}""",keys)
            for o in out: print('  ',o)
        # click test
        await pg.evaluate("()=>{const r=document.querySelector('section.view.on tr[data-gm]');r.click()}"); await pg.wait_for_timeout(800)
        t=await pg.evaluate("document.querySelector('section.view.on').innerText"); print('AFTER CLICK:',t[:500].replace('\n',' | '))
        print('errs',errs)
        await b.close()
asyncio.run(main())
