// Solicitar indexación en Search Console desde el navegador interno (pestaña de Search Console abierta, viewport 1280×900).
// Pegar este bloque UNA vez con javascript_tool en la página de Search Console; después, por cada URL (una llamada por URL,
// porque javascript_tool corta a los 45 s):   zpStart('https://zonaproindiviso.com/…/'); await zpStep()
// zpStep devuelve 'OK' (indexación solicitada), 'CUOTA' (cuota diaria agotada: parar), 'WAIT_READY' / 'WAIT_RESULT' (volver a llamar
// a zpStep). Con el panel oculto, innerText no ve el contenido: todo se busca con textContent y los clics son eventos sintéticos.
// Cuota observada: ~8-10 el 24/10/2026; el 25/10/2026 entraron 10 seguidas sin «Cuota superada».
window.zpSleep = ms => new Promise(r => setTimeout(r, ms));
window.zpClick = el => ['mousedown', 'mouseup', 'click'].forEach(t => el.dispatchEvent(new MouseEvent(t, { bubbles: true, cancelable: true, view: window })));
window.zpCount = re => (document.body.textContent.match(re) || []).length;
window.zpCloseAll = () => {
  let n = 0;
  [...document.querySelectorAll('span')].filter(x => /^(Cerrar|Entendido)$/i.test(x.textContent.trim()))
    .forEach(x => { zpClick(x.closest('[role=button],button') || x); n++; });
  return n;
};
window.zpStart = url => {
  zpCloseAll();
  const inp = [...document.querySelectorAll('input')].find(i => (i.getAttribute('aria-label') || '').startsWith('Inspeccionar'));
  inp.focus();
  Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set.call(inp, url);
  inp.dispatchEvent(new Event('input', { bubbles: true }));
  for (const t of ['keydown', 'keypress', 'keyup']) inp.dispatchEvent(new KeyboardEvent(t, { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
  window.zpCur = { url, okBase: zpCount(/Se ha solicitado la indexación/g), qBase: zpCount(/Cuota superada/g), clicked: false, t0: Date.now() };
  return 'started';
};
window.zpStep = async () => {
  const c = window.zpCur;
  for (let i = 0; i < 35; i++) {
    await zpSleep(1000);
    if (zpCount(/Cuota superada/g) > c.qBase) return 'CUOTA';
    if (c.clicked && zpCount(/Se ha solicitado la indexación/g) > c.okBase) return 'OK';
    if (!c.clicked) {
      const t = document.body.textContent;
      const b = [...document.querySelectorAll('[role=button]')].find(x => /Solicitar indexación/.test(x.textContent));
      if (b && t.includes(c.url) && !/Recuperando datos/i.test(t) && Date.now() - c.t0 > 6000) {
        zpClick(b); c.clicked = true;
        c.okBase = zpCount(/Se ha solicitado la indexación/g); c.qBase = zpCount(/Cuota superada/g);
      }
    }
  }
  return c.clicked ? 'WAIT_RESULT' : 'WAIT_READY';
};
