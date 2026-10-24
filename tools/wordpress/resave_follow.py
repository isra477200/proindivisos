"""Sigue los logs de los builders y regraba (resave_ids) los documentos ya publicados, en lotes, para acortar la ventana sin estilos.
Uso: python3 resave_follow.py log1 log2 ... ; termina cuando no hay builders vivos y no quedan pendientes."""
import sys, re, time, subprocess, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from resave_ids import resave
logs=sys.argv[1:]
done=set()
def pending():
    ids=[]
    for f in logs:
        if not os.path.exists(f): continue
        for m in re.finditer(r'^(\d+) META OK',open(f).read(),re.M):
            i=int(m.group(1))
            if i not in done: ids.append(i)
    return ids
def builders_alive():
    out=subprocess.run(['pgrep','-f','blogbuilder.py|geobuilder.py|lote[0-9]|blog_index.py|build_new.py'],capture_output=True,text=True).stdout
    return bool(out.strip())
while True:
    ids=pending()
    if ids:
        print(time.strftime('%H:%M:%S'),'regrabando',len(ids),flush=True)
        if resave(ids): done.update(ids)
    elif not builders_alive():
        time.sleep(20); ids=pending()
        if ids: continue
        print('fin; regrabados',len(done)); break
    time.sleep(90)
