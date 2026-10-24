// Desde el 24/10/2026 los hits se capturan y se responden con 204 (page.route): la prueba no ensucia GA4 con visitas ni leads falsos.
// Comprueba en vivo que GTM carga GA4 y que los eventos llegan con sus parámetros. Uso: node ga4check.js [url] (requiere playwright).
// Comprueba: page_view con ep.pagina_tipo/lugar/lugar_nivel (ajustes de evento compartidos), llamada y whatsapp (clic), abrir_formulario
// (clic en enlace elementor-action), generate_lead con ep.form_name (simula el éxito del e-form añadiendo la clase form-state-success,
// sin enviar nada) y que con usuario_admin=si no sale ningún hit (excepción de GTM).
const { chromium } = require('playwright');
const URL0 = process.argv[2] || 'https://zonaproindiviso.com/vender-proindiviso/madrid/getafe/';
(async () => {
  const b = await chromium.launch(); const pg = await (await b.newContext({ viewport: { width: 1366, height: 900 } })).newPage();
  const hits = []; await pg.route(/\/g\/collect/, r => r.fulfill({ status: 204, body: "" })); // no envía nada a GA4: captura el hit y responde 204
  pg.on('request', r => { const u = r.url(); if (/\/g\/collect/.test(u)) { const q = new URL(u).searchParams; const ep = {}; for (const [k, v] of q) if (k.startsWith('ep.')) ep[k.slice(3)] = v; hits.push({ en: q.get('en'), gcs: q.get('gcs'), ...ep }); } });
  const show = (t) => { console.log(t, JSON.stringify(hits)); hits.length = 0; };
  await pg.goto(URL0 + (URL0.includes('?') ? '&' : '?') + 'v=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg.waitForTimeout(5000);
  console.log('CTX', JSON.stringify(await pg.evaluate(() => (window.dataLayer || []).find(e => e.event === 'zp_contexto'))));
  show('PAGE');
  await pg.evaluate(() => { document.addEventListener('click', e => { if (e.target.closest('a')) e.preventDefault(); }, true); });
  const tel = await pg.$('a[href^="tel:"]'); await tel.scrollIntoViewIfNeeded(); await tel.click(); await pg.waitForTimeout(6000); show('TEL');
  const wa = await pg.$('a[href*="wa.me"], a[href*="whatsapp"]'); await wa.scrollIntoViewIfNeeded(); await wa.click(); await pg.waitForTimeout(6000); show('WA');
  const pop = await pg.$('a[href*="elementor-action"]'); await pop.scrollIntoViewIfNeeded(); await pop.click(); await pg.waitForTimeout(6000); show('POPUP');
  await pg.evaluate(() => { const f = document.querySelector('form.e-form-base'); f.classList.remove('form-state-default'); f.classList.add('form-state-success'); }); await pg.waitForTimeout(6000); show('FORM');
  console.log('DL', JSON.stringify(await pg.evaluate(() => (window.dataLayer || []).filter(e => /formulario_enviado|popup_abierto/.test(e.event || '')))));
  // simulación de administrador: misma página con usuario_admin=si inyectado antes de GTM → no debe salir ningún hit
  const pg2 = await (await b.newContext()).newPage(); const hits2 = [];
  pg2.on('request', r => { if (/\/g\/collect/.test(r.url())) hits2.push(new URL(r.url()).searchParams.get('en')); });
  await pg2.route('**/*', async (route) => { const r = route.request(); if (r.resourceType() === 'document') { const res = await route.fetch(); let html = await res.text(); html = html.replace('"usuario_admin":"no"', '"usuario_admin":"si"'); return route.fulfill({ response: res, body: html, headers: { ...res.headers(), 'content-type': 'text/html; charset=UTF-8' } }); } return route.continue(); });
  await pg2.goto(URL0 + (URL0.includes('?') ? '&' : '?') + 'adm=' + Date.now(), { waitUntil: 'networkidle', timeout: 90000 }); await pg2.waitForTimeout(5000);
  console.log('ADMIN hits (esperado []):', JSON.stringify(hits2));
  await b.close();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
