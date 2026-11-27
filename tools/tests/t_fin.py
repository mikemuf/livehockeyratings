import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/livehockeyratings/index.html'); await pg.wait_for_timeout(1500)
        await pg.evaluate("y=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith(y));if(b)b.click()}",'2015'); await pg.wait_for_timeout(800)
        t=await pg.evaluate("document.querySelector('section.view.on').innerText")
        import re
        for k in ['SCORING LEADERS','ADJUSTED SCORING','GOALIES: ADJUSTED','GOALIES: GOALS AGAINST']:
            i=t.find(k); print('==',k,i, t[i:i+330].replace('\n',' | ') if i>=0 else '')
        print('errs',errs,'overflow',await pg.evaluate("document.documentElement.scrollWidth"))
        await b.close()
asyncio.run(main())
