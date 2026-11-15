. "$PSScriptRoot/l1.ps1"
$files=@{}
$files['mock_vnpay.py']=[Convert]::ToBase64String([IO.File]::ReadAllBytes('D:/Project/flash-ticket-platform/deploy/rca-test/mock_vnpay.py'))
$files['mock-runner.py']=[Convert]::ToBase64String([IO.File]::ReadAllBytes("$PSScriptRoot/mock-runner.py"))
$source='FILES = '+($files | ConvertTo-Json -Compress)+"`n"+[IO.File]::ReadAllText("$PSScriptRoot/dung-vnpay.py")
Invoke-L1 -May app -Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY")
