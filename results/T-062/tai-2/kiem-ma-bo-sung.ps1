$ErrorActionPreference='Stop'
. "$PSScriptRoot/l1.ps1"
$issues=@()
Get-ChildItem $PSScriptRoot -Filter '*.ps1'|ForEach-Object {
 $errors=$null;$tokens=$null
 [Management.Automation.Language.Parser]::ParseFile($_.FullName,[ref]$tokens,[ref]$errors)|Out-Null
 if($errors){$issues+=@{path=$_.Name;errors=@($errors|ForEach-Object {$_.Message})}}
}
$files=@{}
foreach($name in @('tunnel-supervisor.py','tunnel-remote.py','kiem-mock.py','kiem-token-con-han.py','bang-buoc-tai.py','giao-dich-sau-bao-tri.py','analyze.py')){
 $files[$name]=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$PSScriptRoot/$name"))
}
$source="import ast,base64,json`nfiles="+($files|ConvertTo-Json -Compress)+"`nfor n,b in files.items(): ast.parse(base64.b64decode(b).decode('utf-8-sig'),filename=n)`nprint(json.dumps({'pythonSourcesParsed':len(files),'errors':0}))"
$ast=((Invoke-L1 -May tai -Command ("python3 - <<'PY'`n"+$source+"`nPY"))-join "`n")|ConvertFrom-Json
$value=@{utc=[DateTime]::UtcNow.ToString('o');powershellParseErrors=$issues;python=$ast}
[IO.File]::WriteAllText("$PSScriptRoot/bo-sung-1/kiem-ma.json",($value|ConvertTo-Json -Depth 8),(New-Object System.Text.UTF8Encoding($false)))
$value|ConvertTo-Json -Depth 8
if($issues.Count){throw 'PowerShell syntax errors'}
