import json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent
items=json.loads((P/'migration-inputs-001/manifest.json').read_text())['cases'][:14];branches=['prior_df4','prior_kappa4','prior_precision4','causal_fixed','causal_expanding','compressed_row','compressed_calendar'];names=[]
for item in items:names+=[item['opaque_id']+'--full-sham-thread1.json']+[item['opaque_id']+'--'+b+'.json' for b in branches]
names+=['migration-boundary-51071.json','migration-boundary-51840.json','migration-boundary-complete.json','owned-engine-verification-001.json']
raise SystemExit(subprocess.call([sys.executable,'-X','utf8',str(P/'receive.py'),'receive-owned-engine-001',*names]))
