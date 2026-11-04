const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const [url, out, w, h, mobile] = [process.argv[2], process.argv[3], parseInt(process.argv[4]||'1366'), parseInt(process.argv[5]||'900'), process.argv[6]==='m'];
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile, userAgent: mobile ? 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1' : undefined });
  const pg = await ctx.newPage();
  await pg.goto(url + (url.includes('?')?'&':'?') + 'v=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(1000);
  const info = await pg.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight }));
  console.log(JSON.stringify(info));
  await pg.screenshot({ path: out, fullPage: true });
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
