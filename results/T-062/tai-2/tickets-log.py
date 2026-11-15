import subprocess,json
n='flash-ticket-ticket-service-ticket-service-1'
r=subprocess.run(['sudo','-n','docker','logs','--since','2026-11-12T22:12:55Z','--until','2026-11-12T22:13:10Z',n],capture_output=True,text=True)
for line in (r.stdout+'\n'+r.stderr).splitlines():
 try:
  v=json.loads(line)
 except ValueError:
  continue
 if v.get('log',{}):
  pass
 if any(x in line for x in ['5e4ec9ab5ff94802b86c56e30b7edd38','d1098912621349fa836cf72fb951ccc1','f504626c2d8d4481b12ef2061f1ed260']):
  print(json.dumps(v))
