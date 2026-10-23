// Comprueba en vivo la cadena de consentimiento: banner de Complianz → WP Consent API → modo de consentimiento de Site Kit → GA4 (gcs).
// Antes de aceptar, los hits deben llevar gcs=G100 (todo denegado, pings sin cookies); tras «Aceptar», gcs=G111 y cookie _ga.
// Tras «Denegar», sigue G100 y sin _ga. Uso: node consentcheck.js [url] (requiere playwright).
const { chromium } = require('playwright');
const URL0 = process.argv[2] || 'https://zonaproindiviso.com/';
(async () => {
  const b = await chromium.launch();
  for (const modo of ['accept', 'deny']) {
    const ctx = await b.newContext({ viewport: { width: 1366, height: 900 } }); const pg = await ctx.newPage(); const hits = [];
    pg.on('request', r => { const u = r.url(); if (/\/g\/collect/.test(u)) { const q = new URL(u).searchParams; hits.push(q.get('en') + ':' + q.get('gcs')); } });
    await pg.goto(URL0 + '?c=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(4000);
    const banner = await pg.$('.cmplz-cookiebanner'); const vis = banner ? await banner.isVisible() : false;
    console.log(`[${modo}] banner visible:`, vis, '| antes:', JSON.stringify(hits)); hits.length = 0;
    const btn = await pg.$(modo === 'accept' ? '.cmplz-cookiebanner .cmplz-accept' : '.cmplz-cookiebanner .cmplz-deny');
    if (!btn) { console.log('sin botón', modo); await ctx.close(); continue; }
    await btn.click(); await pg.waitForTimeout(7000);
    // navegación a una 2ª página para ver el estado persistido
    await pg.goto('https://zonaproindiviso.com/vender-proindiviso/madrid/getafe/?c=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(5000);
    const cookies = (await ctx.cookies()).map(c => c.name).filter(n => /^_ga|cmplz/.test(n));
    const consent = await pg.evaluate(() => ({ cmplz: (document.cookie.match(/cmplz_statistics=([^;]+)/) || [])[1], wpapi: typeof window.wp_has_consent === 'function' ? window.wp_has_consent('statistics') : 'sin wp consent api', sk: typeof window._googlesitekitConsentCategoryMap }));
    console.log(`[${modo}] después:`, JSON.stringify(hits), '| cookies:', JSON.stringify(cookies), '| consent:', JSON.stringify(consent));
    await ctx.close();
  }
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
