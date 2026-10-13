"""Detached finite dependency coordinator, all output retained."""
import json,pathlib,subprocess,sys,time
P=pathlib.Path(__file__).resolve().parent
while not (P/'log-semantics-catalog-001.json').exists():
 (P/'log-correlation-queue-status.json').write_text(json.dumps({'state':'WAIT_LOG_SEMANTICS','time':time.time()}));time.sleep(3)
with (P/'log-correlation.stdout').open('x') as out,(P/'log-correlation.stderr').open('x') as err:
 p=subprocess.Popen([sys.executable,'-B','-X','utf8',str(P/'log_correlation.py')],stdout=out,stderr=err,start_new_session=True,cwd=P)
 (P/'log-correlation.pid').write_text(str(p.pid));code=p.wait()
(P/'log-correlation-queue-status.json').write_text(json.dumps({'state':'COMPLETE' if code==0 else 'ERROR','exit':code,'time':time.time()}));raise SystemExit(code)
