// Comprueba en vivo que GTM carga GA4 y que los eventos llamada/whatsapp (clic) y generate_lead (/gracias/) llegan a GA4. Uso: node ga4check.js (requiere playwright).
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1366, height: 900 } })).newPage();
  const hits = [];
  pg.on('request', r => { const u = r.url(); if (/\/g\/collect/.test(u)) { const q = new URL(u).searchParams; hits.push(q.get('en')); } });
  await pg.goto('https://zonaproindiviso.com/?v=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(5000);
  console.log('HOME', JSON.stringify(hits)); hits.length = 0;
  await pg.evaluate(() => { document.addEventListener('click', e => { if (e.target.closest('a')) e.preventDefault(); }, true); });
  const tel = await pg.$('a[href^="tel:"]'); await tel.scrollIntoViewIfNeeded(); await tel.click(); await pg.waitForTimeout(6000);
  console.log('TEL', JSON.stringify(hits)); hits.length = 0;
  const wa = await pg.$('a[href*="wa.me"], a[href*="whatsapp"]'); await wa.scrollIntoViewIfNeeded(); await wa.click(); await pg.waitForTimeout(6000);
  console.log('WA', JSON.stringify(hits));
  const dl = await pg.evaluate(() => (window.dataLayer||[]).filter(e => e.event && /linkClick|click/i.test(e.event)).map(e => e.event + ' ' + (e['gtm.elementUrl']||'')));
  console.log('DL clicks', JSON.stringify(dl));
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
