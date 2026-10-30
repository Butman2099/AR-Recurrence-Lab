const { chromium } = require('playwright');
const files = process.argv.slice(2);
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'] });
  const out = {};
  for (const prof of ['desktop','mobile']) {
    for (const f of files) {
      const times=[];
      for (let k=0;k<5;k++){
        const ctx = await browser.newContext(prof==='mobile'?{viewport:{width:412,height:860},deviceScaleFactor:2.5,isMobile:true,hasTouch:true}:{viewport:{width:1280,height:800}});
        const page = await ctx.newPage(); const cdp = await ctx.newCDPSession(page);
        await cdp.send('Network.enable'); await cdp.send('Network.setCacheDisabled',{cacheDisabled:true});
        if (prof==='mobile'){
          await cdp.send('Network.emulateNetworkConditions',{offline:false,latency:60,downloadThroughput:9e6/8,uploadThroughput:1.5e6/8});
          await cdp.send('Emulation.setCPUThrottlingRate',{rate:4});
        }
        const t0=Date.now();
        await page.goto('http://localhost:8765/test.html?src='+encodeURIComponent(f));
        await page.waitForFunction(()=>window.__loaded!==undefined,{timeout:120000});
        times.push((Date.now()-t0)/1000);
        await ctx.close();
      }
      times.sort((a,b)=>a-b); out[prof+'|'+f]=times[2];
      console.log(prof, f, times.map(t=>t.toFixed(2)).join(' '));
    }
  }
  require('fs').writeFileSync('../results/loadtimes.json', JSON.stringify(out,null,1));
  await browser.close();
})();
