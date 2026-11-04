"""Sube un snippet PHP del repo a Code Snippets (WordPress) por REST.
Uso: python3 snip.py FICHERO.php "Nombre del snippet" [ID]   → sin ID lo crea; con ID lo actualiza (código y nombre), activo y global.
Quita la cabecera <?php. Avisa si el cuerpo supera ~14 KB (el WAF de Hostinger corta cuerpos REST de más de ~15 KB) y si el snippet
queda desactivado o con error de código."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
env = dict(l.strip().split('=', 1) for l in open(os.path.join(HERE, 'wp.env')) if '=' in l)
f, name = sys.argv[1], sys.argv[2]
sid = sys.argv[3] if len(sys.argv) > 3 else None
code = open(f).read()
if code.lstrip().startswith('<?php'): code = code.lstrip()[5:].lstrip('\n')
body = json.dumps({'name': name, 'code': code, 'scope': 'global', 'active': True, 'priority': 10}, ensure_ascii=False)
if len(body.encode()) > 14000: print('AVISO: cuerpo de', len(body.encode()), 'bytes (WAF ~15 KB)')
url = env['WP'] + '/wp-json/code-snippets/v1/snippets' + (f'/{sid}' if sid else '')
out = subprocess.run(['curl', '-sS', '--max-time', '90', '-u', env['P1'], '-X', 'PUT' if sid else 'POST', '-H', 'Content-Type: application/json; charset=utf-8',
                      url, '--data-binary', body], capture_output=True, text=True).stdout
try:
    d = json.loads(out)
    print('id', d.get('id'), 'activo', d.get('active'), 'error', d.get('code_error'), d.get('message', ''))
except Exception:
    print('RESPUESTA NO JSON:', out[:400])
