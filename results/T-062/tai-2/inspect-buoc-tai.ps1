$ErrorActionPreference='Stop'
. "$PSScriptRoot/l1.ps1"
$files=@{}
foreach($name in @('hanh-trinh.js','cau-hinh.json')){$files[$name]=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$PSScriptRoot/k6/$name"))}
$stamp=[DateTime]::UtcNow.ToString('yyyyMMddTHHmmssfffZ')
$directory="/opt/rca-tai/bo-sung-1/inspect-$stamp"
$source=@'
import ast,base64,json,pathlib,subprocess
root=pathlib.Path('__DIR__');root.mkdir(parents=True)
files=__FILES__
for n,b in files.items():(root/n).write_bytes(base64.b64decode(b))
secrets=root/'secret';secrets.mkdir()
(secrets/'l1-tokens.json').write_text(json.dumps({'tokens':[{'access_token':'placeholder','refresh_token':'placeholder'} for _ in range(40)]}))
image=json.loads((root/'cau-hinh.json').read_text())['image']
outputs={}
for mode,step in [('step',120),('whole_run',0)]:
    command=['sudo','-n','docker','run','--rm','--network','none',
        '-v',str(root)+':/scripts:ro','-v',str(secrets)+':/secret:ro',
        '-e','FT_TEST_ENVIRONMENT=true','-e','FT_LOAD_SECONDS=240',
        '-e','FT_LOAD_MULTIPLIER=3','-e','FT_LOAD_STEP_SECONDS='+str(step),
        image,'inspect','--include-system-env-vars','--execution-requirements','/scripts/hanh-trinh.js']
    result=subprocess.run(command,capture_output=True,text=True)
    (root/(mode+'.stdout.json')).write_text(result.stdout)
    (root/(mode+'.stderr.txt')).write_text(result.stderr)
    if result.returncode:raise SystemExit('k6 init failed: '+mode+' exit '+str(result.returncode))
    outputs[mode]=json.loads(result.stdout)
print(json.dumps({'directory':str(root),'outputs':outputs}))
'@
$source=$source.Replace('__DIR__',$directory).Replace('__FILES__',($files|ConvertTo-Json -Compress))
$result=Invoke-L1 -May tai -Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY")
[IO.File]::WriteAllText("$PSScriptRoot/bo-sung-1/k6-inspect.json",($result -join "`n")+"`n",(New-Object System.Text.UTF8Encoding($false)))
$parsed=($result -join "`n")|ConvertFrom-Json
$parsed.outputs|ConvertTo-Json -Depth 15
