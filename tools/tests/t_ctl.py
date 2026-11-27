import asyncio
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox','--allow-file-access-from-files'])
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file:///home/claude/livehockeyratings/index.html'); await pg.wait_for_timeout(1500)
        for y in ['2013','2011','2015']:
            await pg.evaluate("y=>{const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim().startsWith(y));if(b)b.click()}",y); await pg.wait_for_timeout(800)
            t=await pg.evaluate("document.querySelector('section.view.on').innerText")
            i=t.upper().find('WHO CONTROLS THEIR POOL'); print('==',y,i, t[i:i+520].replace('\n',' | ') if i>=0 else '')
            if y=='2013':
                await pg.evaluate("()=>{const h=[...document.querySelectorAll('section.view.on *')].find(e=>e.children.length===0&&/who controls their pool/i.test(e.textContent));if(h)h.scrollIntoView()}"); await pg.wait_for_timeout(400); await pg.screenshot(path='/tmp/ctl.png')
        print('errs',errs,'overflow',await pg.evaluate("document.documentElement.scrollWidth"))
        await b.close()
asyncio.run(main())
