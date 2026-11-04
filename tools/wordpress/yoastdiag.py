"""Diagnóstico Yoast de specs: frases consecutivas que empiezan igual y subtítulos vs palabras de contenido. Uso: python3 yoastdiag.py blog/x.json slug [slug...]"""
import sys,os,json,subprocess,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import yoastpre as Y
from pagebuilder import _kw_words,_topic
f=sys.argv[1]; slugs=sys.argv[2:]
S=[s for s in json.load(open(f)) if s['slug'] in slugs]
for s in S:
    it=dict(url=s['slug'],html=Y.html_of(s),keyword=s['focus_kw'],title=s['yoast_title'],description=s['meta_desc'],slug=s['slug'],permalink='https://zonaproindiviso.com/blog/x/')
    r=subprocess.run(['node','research.js'],input=json.dumps([it]),capture_output=True,text=True,cwd=Y.YOAST_DIR); d=json.loads(r.stdout)
    r2=subprocess.run(['node','research2.js'],input=json.dumps([it]),capture_output=True,text=True,cwd=Y.YOAST_DIR); d2=json.loads(r2.stdout)
    print('==',s['slug'],'| kw:',s['focus_kw'],'| contenido:',_kw_words(s['focus_kw']),'| subtítulos',d2['sub']['matches'],'/',d2['sub']['count'],f"{d2['sub']['percentReflectingTopic']:.0f}%")
    for sb in d['sentenceBeginnings']: print('  3x «%s»:'%sb['word']); [print('     -',x) for x in sb['s']]
    if d2['sub']['percentReflectingTopic']<30 or d2['sub']['percentReflectingTopic']>75:
        for h in d2['heads']: print('   ','✓' if _topic(h.split(': ',1)[1],s['focus_kw']) else ' ',h)
