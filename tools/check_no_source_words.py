import asyncio,re
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':390,'height':844})
        await pg.goto('file:///home/claude/livehockeyratings/index.html'); await pg.wait_for_timeout(1500)
        for y in ['2011','2012','2013','2014','2015','2016']:
            await pg.evaluate("y=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith(y));if(b)b.click()}",y); await pg.wait_for_timeout(700)
            t=await pg.evaluate("document.querySelector('section.view.on').innerText")
            for m in re.finditer(r'(?i)sheet|gamesheet|instat|myhockey|\bMHR\b',t): print(y,repr(t[max(0,m.start()-60):m.end()+40]))
        await b.close()
asyncio.run(main())
