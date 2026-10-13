import json,pathlib,subprocess,sys
P=pathlib.Path(__file__).resolve().parent;v=json.loads((P/'backend-status-summary-001.json').read_text());names=[]
for x in v['cases']:
 names.append(x['opaque_id']+'--backend-status.json')
 if x['status']=='PASS':names.append(x['literal_records_artifact']['file'])
names+=['backend-source-verification-001.json']
raise SystemExit(subprocess.call([sys.executable,'-X','utf8',str(P/'receive.py'),'receive-backend-literals-001',*names]))
