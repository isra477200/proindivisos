// Comprueba en vivo el evento calculadora_usada de las dos calculadoras y pagina_tipo=herramienta (sin enviar nada a GA4). Uso: node calccheck.js
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const out = {};
  for (const u of ['https://zonaproindiviso.com/cuanto-vale-mi-parte-de-un-piso/','https://zonaproindiviso.com/simulador-extincion-de-condominio/']) {
    const pg = await (await b.newContext()).newPage(); const hits = [];
    await pg.route(/\/g\/collect/, r => { const q = new URL(r.request().url()).searchParams; const ep={}; for (const [k,v] of q) if (k.startsWith('ep.')) ep[k.slice(3)]=v; hits.push({en:q.get('en'),...ep}); r.fulfill({status:204,body:''}); });
    await pg.goto(u+'?d='+Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(3000);
    const inp = await pg.$('.zpc-form input[type="number"], .zpc-form input[type="text"], .zpc-form input');
    await inp.scrollIntoViewIfNeeded(); await inp.fill('250000'); await inp.dispatchEvent('input'); await pg.waitForTimeout(5000);
    out[u.replace('https://zonaproindiviso.com','')] = { dl: await pg.evaluate(() => (window.dataLayer||[]).filter(e => e.event==='calculadora_usada')), hits: hits.filter(h => h.en!=='page_view').concat(hits.filter(h=>h.en==='page_view').map(h=>({en:'page_view',pagina_tipo:h.pagina_tipo}))) };
    await pg.close();
  }
  console.log(JSON.stringify(out, null, 1)); await b.close();
})();
