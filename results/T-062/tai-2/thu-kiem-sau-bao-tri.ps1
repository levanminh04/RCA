$ErrorActionPreference='Stop'
. "$PSScriptRoot/l1.ps1"
$dir="$PSScriptRoot/bo-sung-1"
$order=Get-Content -Raw -Encoding UTF8 "$dir/giao-dich-sau-bao-tri.json"|ConvertFrom-Json
$from=([DateTimeOffset]::Parse($order.utcStart).AddSeconds(-1)).ToString('yyyy-MM-ddTHH:mm:ssZ')
$until=([DateTimeOffset]::Parse($order.utcEnd).AddSeconds(8)).ToString('yyyy-MM-ddTHH:mm:ssZ')
$source=[IO.File]::ReadAllText("$PSScriptRoot/log-giao-dich.py")
$source=$source.Replace("oid='2f6c01b2-ab05-49d5-affc-3c0bbafb67a2'",("oid='"+$order.orderId+"'"))
$source=$source.Replace('2026-11-12T22:17:30Z',$from).Replace('2026-11-12T22:18:45Z',$until)
$source=$source.Substring(0,$source.IndexOf("print(json.dumps({'mockAudit'"))
$source+="`nfor l in open('/opt/flash-ticket-app/l1-vnpay/audit.jsonl'):`n v=json.loads(l)`n if v.get('attemptId')=='"+$order.attemptId+"': print(json.dumps({'mockAudit':v}))`n"
$records=Invoke-L1 -May app -Command ("python3 - <<'PY'`n"+$source+"`nPY")
[IO.File]::WriteAllText("$dir/log-giao-dich-sau-bao-tri.jsonl",($records -join "`n")+"`n",(New-Object System.Text.UTF8Encoding($false)))
$parsed=@($records|ForEach-Object {$_|ConvertFrom-Json})
$ids=@($parsed|ForEach-Object {$_.logs}|Where-Object {$_.eventName -match 'message.processed|booking.issuance-result|ticket.outbox.result|gateway.request.completed'}|ForEach-Object {$_.traceId}|Where-Object {$_}|Sort-Object -Unique)
$source=[IO.File]::ReadAllText("$PSScriptRoot/kiem-tempo.py")
$source="import urllib.request,json,collections,base64`nids="+(ConvertTo-Json -InputObject $ids -Compress)+"`n"+$source.Substring($source.IndexOf('def walk'))
$tempo=Invoke-L1 -May obs -Command ("python3 - <<'PY'`n"+$source+"`nPY")
[IO.File]::WriteAllText("$dir/tempo-sau-bao-tri.jsonl",($tempo -join "`n")+"`n",(New-Object System.Text.UTF8Encoding($false)))
$values=@($tempo|ForEach-Object {$_|ConvertFrom-Json})
$producer=($values|ForEach-Object {[int]$_.kinds.SPAN_KIND_PRODUCER}|Measure-Object -Sum).Sum
$consumer=($values|ForEach-Object {[int]$_.kinds.SPAN_KIND_CONSUMER}|Measure-Object -Sum).Sum
$result=@{utc=[DateTime]::UtcNow.ToString('o');orderId=$order.orderId;traceCount=$values.Count;producer=$producer;consumer=$consumer;traceIds=$ids;errors=@($values|Where-Object {$_.errorType})}
[IO.File]::WriteAllText("$dir/kiem-span-sau-bao-tri.json",($result|ConvertTo-Json -Depth 7),(New-Object System.Text.UTF8Encoding($false)))
$result|ConvertTo-Json -Depth 7
