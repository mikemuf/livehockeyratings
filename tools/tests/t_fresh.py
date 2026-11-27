import asyncio
from playwright.async_api import async_playwright
P='/home/claude/site/members/ratings/index.html'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        pg=await b.new_page(viewport={'width':390,'height':844}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('http://127.0.0.1:8765/live/?y=2015'); await pg.wait_for_timeout(2500)
        fr=pg.frames[-1]
        print('btn hidden',await pg.evaluate("document.getElementById('mpdR').hidden"))
        print('upd',await fr.evaluate("document.body.innerText.match(/updated[^\\n]*/)[0]"), await fr.evaluate("div"))
        orig=open(P).read(); open(P,'w').write(orig.replace('12:44 PM CT','12:59 PM CT'))
        try:
            # case 1: near top -> silent swap on check
            await pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); await pg.wait_for_timeout(2500)
            fr=pg.frames[-1]
            print('after auto:',await fr.evaluate("document.body.innerText.match(/updated[^\\n]*/)[0]"), await fr.evaluate("div"), 'gd class',await fr.evaluate("document.body.classList.contains('gd')"))
            # case 2: scrolled -> pill
            await fr.evaluate("window.scrollTo(0,900)"); await pg.wait_for_timeout(300)
            open(P,'w').write(orig.replace('12:44 PM CT','1:06 PM CT'))
            await pg.evaluate("document.dispatchEvent(new Event('visibilitychange'))"); await pg.wait_for_timeout(2000)
            print('pill hidden',await pg.evaluate("document.getElementById('mpdP').hidden"), await fr.evaluate("document.body.innerText.match(/updated[^\\n]*/)[0]"))
            await pg.click('#mpdP'); await pg.wait_for_timeout(2000); fr=pg.frames[-1]
            print('after pill:',await fr.evaluate("document.body.innerText.match(/updated[^\\n]*/)[0]"), await fr.evaluate("div"),'scroll',await fr.evaluate("document.scrollingElement.scrollTop"))
            await pg.screenshot(path='/tmp/fresh.png')
        finally: open(P,'w').write(orig)
        print('errs',errs); await b.close()
asyncio.run(main())
