import pathlib, subprocess, time, json, hashlib, sys
ROOT=pathlib.Path(__file__).resolve().parents[4]; OUT=pathlib.Path(__file__).parent
SSH=['ssh','-i','D:/RCA-ext/keys/key2.pem','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','ConnectTimeout=20','ubuntu@3.26.62.217']
def call(name,script):
 script=script.replace('\r\n','\n').replace('\r','\n')
 t=time.time();r=subprocess.run(SSH+['bash -s'],input=script.encode('utf-8'),capture_output=True)
 r.stdout=r.stdout.decode('utf-8',errors='replace');r.stderr=r.stderr.decode('utf-8',errors='replace')
 (OUT/(name+'-stdout.txt')).write_text(r.stdout,encoding='utf-8');(OUT/(name+'-stderr.txt')).write_text(r.stderr,encoding='utf-8')
 with (OUT/'root-commands.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'name':name,'command':SSH+['bash -s'],'stdin':script,'exit_code':r.returncode,'wall_s':time.time()-t},ensure_ascii=False)+'\n')
 print(json.dumps({'name':name,'exit_code':r.returncode,'wall_s':round(time.time()-t,2),'stdout':r.stdout[-1600:],'stderr':r.stderr[-500:]},ensure_ascii=False),flush=True)
 if r.returncode:raise RuntimeError('remote failed; preserved outputs')
if __name__=='__main__':
 call(sys.argv[1],sys.stdin.read())
