import json,sys
for f in sys.argv[1:]:
    d=json.load(open(f)); a=d['audits']
    print('==',f, d['finalDisplayedUrl'], 'PERF', round(d['categories']['performance']['score']*100))
    for k in ('first-contentful-paint','largest-contentful-paint','total-blocking-time','cumulative-layout-shift','speed-index','server-response-time'):
        print('  %-28s %s'%(k, a[k]['displayValue']))
    opps=[]
    for k,v in a.items():
        det=v.get('details') or {}
        if det.get('type')=='opportunity' and v.get('score') is not None and v['score']<1:
            opps.append((v['title'], int(det.get('overallSavingsMs') or 0), int((det.get('overallSavingsBytes') or 0)//1024)))
    for t,ms,kb in sorted(opps,key=lambda x:-x[1])[:8]: print('   OPP %-55s %6d ms %6d KB'%(t[:55],ms,kb))
    lcp=a.get('largest-contentful-paint-element',{}).get('details',{}).get('items',[])
    try: print('   LCP:', lcp[0]['items'][0]['node']['snippet'][:140])
    except Exception: pass
    diag=a.get('diagnostics',{}).get('details',{}).get('items',[{}])[0]
    print('   requests',diag.get('numRequests'),'bytes',int(diag.get('totalByteWeight',0)//1024),'KB scripts',diag.get('numScripts'),'css',diag.get('numStylesheets'),'fonts',diag.get('numFonts'))
    # render-blocking details
    rb=a.get('render-blocking-resources',{}).get('details',{}).get('items',[])
    for it in rb[:10]: print('   RB %-90s %5d ms %5d KB'%(it['url'][-90:], it.get('wastedMs',0), it.get('totalBytes',0)//1024))
