const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch();
  const [url, w, h, mobile] = [process.argv[2], parseInt(process.argv[3]||'390'), parseInt(process.argv[4]||'844'), process.argv[5]==='m'];
  const ctx = await b.newContext({ viewport: { width: w, height: h }, isMobile: mobile, hasTouch: mobile });
  const pg = await ctx.newPage();
  await pg.goto(url + '?v=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(800);
  const res = await pg.evaluate((vw) => {
    const out = [];
    for (const el of document.querySelectorAll('body *')) {
      const r = el.getBoundingClientRect();
      if (r.width > 0 && (r.right > vw + 2 || r.left < -2)) {
        const cs = getComputedStyle(el);
        out.push({ tag: el.tagName.toLowerCase(), cls: (el.className && el.className.baseVal === undefined ? el.className : '').toString().slice(0, 60), id: el.getAttribute('data-id') || el.id, left: Math.round(r.left), right: Math.round(r.right), width: Math.round(r.width), pos: cs.position, text: (el.innerText || '').slice(0, 30).replace(/\n/g, ' ') });
      }
    }
    return out.slice(0, 40);
  }, w);
  console.log(JSON.stringify(res, null, 0));
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
