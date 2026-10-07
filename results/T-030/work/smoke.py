import sys, json, time
from pathlib import Path
ROOT=Path('D:/RCA-flashticket'); sys.path[:0]=[str(ROOT/'src'), str(ROOT/'results/T-030/tests')]
import fixture
from p3 import runner, selector, nhan
t=time.time(); repo=fixture.tao_repo('smoke', so_ca=1); print('fixture', round(time.time()-t,1))
al=selector.nap_allowlist(repo/'allowlist.json'); oid=sorted(al)[0]; tm=nhan.nap_moc(repo/'nhan.json')[oid]
out=ROOT/'results/T-030/work/smoke-runs'
for m,kw in [('baro',{}),('simplerca',{}),('microrank',{}),('tracerca',{}),('circa',{'model':'ols'}),('circa',{'model':'svr'}),('torai_A',{'seed':0}),('torai_B',{'seed':0}),('nsigma',{}),('bocpd',{})]:
    t=time.time()
    try:
        recs=runner.chay_luot(al,oid,m,'a',tm,out,600,repo_root=repo,torai_tt=repo/'torai-TT',**kw)
        for r in recs:
            print(m, r.get('variant'), r['status'], r.get('error'), (r.get('entity_ranking') or [])[:3] if 'entity_ranking' in r else r.get('alarms')[:5], r['cost']['wall_s'], r['cost']['peak_rss_mb'])
    except Exception as e:
        print(m,'LOI',type(e).__name__,e)
    print('  t',round(time.time()-t,1))
