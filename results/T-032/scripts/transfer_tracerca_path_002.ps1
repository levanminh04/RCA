$ErrorActionPreference='Stop'
Set-Location -LiteralPath D:/RCA-flashticket
$base='results/T-032/runs/tracerca-path-002'
$receiptPath="$base/final-self-check.json"
$receipt=Get-Content -LiteralPath $receiptPath -Raw | ConvertFrom-Json
if($receipt.status -ne 'LOCAL_FINAL_METADATA_PASS_NO_RUNTIME'){throw 'Prepared receipt did not pass'}
foreach($row in $receipt.transfer_files){
 if((Get-FileHash -LiteralPath $row.local -Algorithm SHA256).Hash.ToLowerInvariant() -ne $row.sha256){throw "Local byte changed: $($row.local)"}
 if((Get-Item -LiteralPath $row.local).Length -ne $row.bytes){throw 'Local size changed'}
}
if((Get-FileHash -LiteralPath $receipt.archive.path -Algorithm SHA256).Hash.ToLowerInvariant() -ne $receipt.archive.sha256){throw 'Archive changed'}
$receiptHash=(Get-FileHash -LiteralPath $receiptPath -Algorithm SHA256).Hash.ToLowerInvariant()
$ssh=@('-i','D:/RCA-ext/keys/key2.pem','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes')
& ssh @ssh ubuntu@3.26.62.217 'test ! -e /home/ubuntu/rca/T-032/inputs/tracerca-path-002-code.tar.gz && test ! -e /home/ubuntu/rca/T-032/inputs/tracerca-path-002-final-self-check.json'
if($LASTEXITCODE -ne 0){throw 'Transfer destinations already exist or remote preflight failed'}
& scp @ssh $receipt.archive.path ubuntu@3.26.62.217:/home/ubuntu/rca/T-032/inputs/tracerca-path-002-code.tar.gz
if($LASTEXITCODE -ne 0){throw 'Archive transfer failed; retain partial remote output'}
& scp @ssh $receiptPath ubuntu@3.26.62.217:/home/ubuntu/rca/T-032/inputs/tracerca-path-002-final-self-check.json
if($LASTEXITCODE -ne 0){throw 'Inventory transfer failed; retain partial remote output'}
$verify=@'
import sys,json,hashlib,tarfile,time
from pathlib import Path,PurePosixPath
base=Path('/home/ubuntu/rca/T-032')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
receipt=base/'inputs/tracerca-path-002-final-self-check.json'
assert sha(receipt)==sys.argv[1],'transport receipt hash'
meta=json.loads(receipt.read_text(encoding='utf-8-sig'))
archive=base/'inputs/tracerca-path-002-code.tar.gz'
assert sha(archive)==meta['archive']['sha256'],'archive hash'
expected={str(Path(r['remote']).relative_to(base)):r for r in meta['transfer_files']}
assert len(expected)==47
with tarfile.open(archive,'r:gz') as tf:
 members=tf.getmembers()
 assert len(members)==len(expected)
 assert {m.name for m in members}==set(expected)
 for m in members:
  parts=PurePosixPath(m.name)
  assert m.isfile() and not parts.is_absolute() and '..' not in parts.parts
  assert m.name=='scripts/replay_tracerca_v2.py' or m.name=='sources/tracerca-path-002-inventory.json' or m.name.startswith('sources/rcaeval/RCAEval/')
  target=base/m.name
  assert target.resolve()==target and not target.exists(),'existing/redirected destination'
  blob=tf.extractfile(m).read();row=expected[m.name]
  assert len(blob)==row['bytes'] and hashlib.sha256(blob).hexdigest()==row['sha256']
 # Validate every member before the first filesystem mutation.
 for m in members:
  target=base/m.name;target.parent.mkdir(parents=True,exist_ok=True)
  with target.open('xb') as out:out.write(tf.extractfile(m).read())
checks=[]
for relative,row in expected.items():
 p=base/relative
 assert sha(p)==row['sha256'] and p.stat().st_size==row['bytes']
 checks.append({'remote':str(p),'local_source':row['local'],'sha256':sha(p),'expected_sha256':row['sha256'],'bytes':p.stat().st_size,'pass':True})
print(json.dumps({'status':'PASS','at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'archive_sha256':sha(archive),'receipt_sha256':sha(receipt),'file_count':len(checks),'files':checks,'runtime_import_checked':False}))
'@
$remote=$verify | & ssh @ssh ubuntu@3.26.62.217 "/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 - $receiptHash"
if($LASTEXITCODE -ne 0){throw 'Remote byte verification/unpack failed; retain artifacts'}
$check=$remote | ConvertFrom-Json
if($check.status -ne 'PASS'){throw 'Remote transfer verdict failed'}
$out="$base/transfer-check-001.json"
if(Test-Path -LiteralPath $out){throw 'Transfer receipt already exists'}
[IO.File]::WriteAllText((Join-Path (Get-Location) $out),($remote+"`n"),[Text.UTF8Encoding]::new($false))
Write-Output "PASS: $($check.file_count) files; sources and destinations byte-identical; no method executed."
