const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
  const ctx = await browser.newContext({ viewport: { width: 1500, height: 800 }, deviceScaleFactor: 2 });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8765/index.html'); await page.waitForTimeout(400);
  await page.click('nav button[data-tab=scrub]'); await page.selectOption('#sEvent','BR20');
  await page.evaluate(()=>{const r=document.querySelector('#sRange'); r.value=13; r.dispatchEvent(new Event('input'));});
  await page.waitForFunction(()=>document.querySelector('#sMV').loaded,{timeout:60000}); await page.waitForTimeout(1500);
  await (await page.$('#scrub')).screenshot({path:'../figs/ar_shots/d_scrub_wide.png'});
  await browser.close();
})();
