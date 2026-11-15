$ErrorActionPreference='Stop'
$root=$PSScriptRoot
$a=Get-Content -Raw -Encoding UTF8 "$root/out/l1r20261112v2a/analysis.json"|ConvertFrom-Json
$b=Get-Content -Raw -Encoding UTF8 "$root/out/l1r20261112v2b/analysis.json"|ConvertFrom-Json
$sa=Get-Content -Raw -Encoding UTF8 "$root/out/l1r20261112v2a/state.json"|ConvertFrom-Json
$sb=Get-Content -Raw -Encoding UTF8 "$root/out/l1r20261112v2b/state.json"|ConvertFrom-Json
function Rel($x,$y){if(!$x){return 'N/A'};return ([double](100*[Math]::Abs($y-$x)/$x)).ToString('F3',[Globalization.CultureInfo]::InvariantCulture)+'%'}
$routes=@();$gateway=@()
foreach($p in $a.routes.PSObject.Properties){$n=$p.Name;$x=[int]$p.Value;$y=[int]$b.routes.$n;$routes+=@{route=$n;k6A=$x;gatewayA=[int]$a.gateway.matchedRoutes.$n;k6B=$y;gatewayB=[int]$b.gateway.matchedRoutes.$n;absoluteDifference=[Math]::Abs($y-$x);relativeToA=Rel $x $y}}
foreach($p in $a.routeIds.PSObject.Properties){$n=$p.Name;$x=[int]$p.Value;$y=[int]$b.routeIds.$n;$gateway+=@{route=$n;k6A=$x;gatewayA=[int]$a.gateway.routeIds.$n;k6B=$y;gatewayB=[int]$b.gateway.routeIds.$n;absoluteDifference=[Math]::Abs($y-$x);relativeToA=Rel $x $y}}
$pins=@();foreach($f in @('hanh-trinh.js','cau-hinh.json')){$ha=(Get-FileHash -Algorithm SHA256 "$root/out/l1r20261112v2a/$f").Hash;$hb=(Get-FileHash -Algorithm SHA256 "$root/out/l1r20261112v2b/$f").Hash;$hl=(Get-FileHash -Algorithm SHA256 "$root/k6/$f").Hash;$pins+=@{file=$f;a=$ha;b=$hb;current=$hl;equal=($ha -eq $hb -and $hb -eq $hl)}}
if(@($pins|Where-Object {!$_.equal}).Count){throw 'Comparison input mismatch'}
$oa=@($a.orders.PSObject.Properties|ForEach-Object {$_.Name});$ob=@($b.orders.PSObject.Properties|ForEach-Object {$_.Name});$overlap=@($oa|Where-Object {$_ -in $ob}).Count
$result=@{utc=[DateTime]::UtcNow.ToString('o');runs=@('l1r20261112v2a','l1r20261112v2b');routes=$routes;gatewayRoutes=$gateway;inputPins=$pins;orderOverlap=$overlap;totalA=$a.totals.route_responses;totalB=$b.totals.route_responses}
$result|ConvertTo-Json -Depth 10|Set-Content -Encoding UTF8 "$root/lap-2-luot.json"
$routeTable=($routes|Sort-Object {$_.route}|ForEach-Object {"| $($_.route) | $($_.k6A) | $($_.gatewayA) | $($_.k6B) | $($_.gatewayB) | $($_.absoluteDifference) | $($_.relativeToA) |"})-join "`n"
$gwTable=($gateway|Sort-Object {$_.route}|ForEach-Object {"| $($_.route) | $($_.k6A) | $($_.gatewayA) | $($_.k6B) | $($_.gatewayB) | $($_.absoluteDifference) | $($_.relativeToA) |"})-join "`n"
$summary="| journey_started | $($a.totals.journey_started) | $($b.totals.journey_started) |`n| journey_finished | $($a.totals.journey_finished) | $($b.totals.journey_finished) |`n| purchase finished | $($a.journeys.journey_finished.purchase) | $($b.journeys.journey_finished.purchase) |`n| journey_failed | $([int]$a.totals.journey_failed) | $([int]$b.totals.journey_failed) |`n| dropped_iterations | $([int]$a.totals.dropped_iterations) | $([int]$b.totals.dropped_iterations) |`n| HTTP 401 | $([int]$a.totals.gateway_401) | $([int]$b.totals.gateway_401) |`n| token_refresh_success | $($a.totals.token_refresh_success) | $($b.totals.token_refresh_success) |`n| token_refresh_failure | $([int]$a.totals.token_refresh_failure) | $([int]$b.totals.token_refresh_failure) |"
$text=[IO.File]::ReadAllText("$root/lap-2-template.md")
$values=@{'@TIME_A@'="$($sa.StartedAt) -> $($sa.FinishedAt)";'@TIME_B@'="$($sb.StartedAt) -> $($sb.FinishedAt)";'@INPUT_CHECK@'='SHA256 source/config A = B = current';'@SUMMARY@'=$summary;'@GATEWAY_TABLE@'=$gwTable;'@ROUTE_TABLE@'=$routeTable;'@TOTAL_A@'=[string]$a.totals.route_responses;'@TOTAL_B@'=[string]$b.totals.route_responses;'@TOTAL_DIFF@'=[string][Math]::Abs($b.totals.route_responses-$a.totals.route_responses);'@TOTAL_REL@'=(Rel $a.totals.route_responses $b.totals.route_responses);'@RATE_A@'=([double]$a.totals.route_responses/600).ToString('F4',[Globalization.CultureInfo]::InvariantCulture);'@RATE_B@'=([double]$b.totals.route_responses/600).ToString('F4',[Globalization.CultureInfo]::InvariantCulture);'@ORDER_OVERLAP@'=[string]$overlap;'@MATCH_CHECK@'="Gateway missing A/B: $($a.gateway.missing.Count)/$($b.gateway.missing.Count); status/route mismatches: $($a.gateway.mismatches.Count)/$($b.gateway.mismatches.Count); duplicate IDs: $($a.gateway.duplicateTraces.Count)/$($b.gateway.duplicateTraces.Count); extra requests: $($a.gateway.extraRequests.Count)/$($b.gateway.extraRequests.Count)."}
foreach($k in $values.Keys){$text=$text.Replace($k,$values[$k])}
[IO.File]::WriteAllText("$root/lap-2-luot.md",$text,(New-Object System.Text.UTF8Encoding($false)))
foreach($tag in @('l1p20261112v2','l1r20261112v2a','l1r20261112v2b')){
 $data=Get-Content -Raw -Encoding UTF8 "$root/out/$tag/analysis.json"|ConvertFrom-Json
 $data.steps.PSObject.Properties|ForEach-Object {[PSCustomObject]@{step=$_.Name;requests=$_.Value}}|Export-Csv -NoTypeInformation -Encoding UTF8 "$root/out/$tag/steps.csv"
 $data.journeys.journey_started.PSObject.Properties|ForEach-Object {$j=$_.Name;[PSCustomObject]@{journey=$j;started=$_.Value;finished=[int]$data.journeys.journey_finished.$j;failed=[int]$data.journeys.journey_failed.$j;percent=$data.mixMeasuredPercent.$j}}|Export-Csv -NoTypeInformation -Encoding UTF8 "$root/out/$tag/journeys.csv"
}
$result|ConvertTo-Json -Depth 10
