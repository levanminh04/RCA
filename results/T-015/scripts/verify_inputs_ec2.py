import hashlib,json,pathlib,sys
task=pathlib.Path.home()/'rca/T-015'
expected=json.loads((task/'runs/setup/input-expected.json').read_text())
selected=sys.argv[1] if len(sys.argv)>1 else ''
if selected:
    assert selected=='re2tt_ts-auth-service_cpu_1'
    expected=[r for r in expected if r['path'].split('/')[0]==selected]
rows=[]
for row in expected:
    p=task/'data'/row['path'];h=hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda:f.read(2**20),b''):h.update(chunk)
    actual={'path':row['path'],'bytes':p.stat().st_size,'sha256':h.hexdigest()}
    actual['ok']=all(actual[k]==row[k] for k in ['bytes','sha256']);rows.append(actual)
(task/'runs/setup'/('auth-input-verified.json' if selected else 'input-verified.json')).write_text(json.dumps(rows,indent=2))
assert len(rows)==(3 if selected else 189) and all(row['ok'] for row in rows)
print('PASS: '+str(len(rows))+' files, '+str(sum(r['bytes'] for r in rows))+' bytes, all hashes exact')
