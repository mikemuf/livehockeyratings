import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/livehockeyratings/index.html'); await pg.wait_for_timeout(1500)
        for y in ['2011','2015','2013']:
            await pg.evaluate("y=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith(y));if(b)b.click()}",y); await pg.wait_for_timeout(900)
            t=await pg.evaluate("document.querySelector('section.view.on').innerText"); i=t.upper().find('UP NEXT'); print(y,'h',await pg.evaluate("document.documentElement.scrollHeight"),t[i:i+260].replace('\n',' | '))
        await pg.screenshot(path='/tmp/sch1.png',clip={'x':0,'y':300,'width':390,'height':1000},full_page=True)
        yy=await pg.evaluate("Math.round(document.getElementById('sssched').getBoundingClientRect().top+scrollY)")
        await pg.screenshot(path='/tmp/sch2.png',clip={'x':0,'y':yy-10,'width':390,'height':1100},full_page=True)
        print('errs',errs,'overflow',await pg.evaluate("document.documentElement.scrollWidth"))
        await b.close()
asyncio.run(main())
