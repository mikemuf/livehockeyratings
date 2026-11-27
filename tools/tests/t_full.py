import asyncio,sys
from playwright.async_api import async_playwright
async def main():
    y=sys.argv[1] if len(sys.argv)>1 else '2013'
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/livehockeyratings/index.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("y=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith(y));if(b)b.click()}",y); await pg.wait_for_timeout(900)
        t=await pg.evaluate("document.querySelector('section.view.on').innerText")
        hs=await pg.evaluate("[...document.querySelectorAll('section.view.on h2,section.view.on h3,section.view.on h4,section.view.on summary')].map(e=>e.tagName+': '+e.innerText.trim().slice(0,70)+' @'+Math.round(e.getBoundingClientRect().top+scrollY))")
        print('chars',len(t),'height',await pg.evaluate("document.documentElement.scrollHeight")); print('\n'.join(hs))
        await pg.screenshot(path='/tmp/full_top.png',clip={'x':0,'y':0,'width':390,'height':2200},full_page=True)
        print('errs',errs)
        await b.close()
asyncio.run(main())
