# Exact-duration reference runs. Existing controller files stay unchanged.
$ErrorActionPreference='Stop'
. "$PSScriptRoot/../phan-tich.ps1"
$root=$script:L1Root
$cases=@(@{tag='l1ps20261113a';seconds=150;step=0;mult=1},@{tag='l1ps20261113b';seconds=180;step=90;mult=3})
foreach($case in $cases){
 $launchParams=@{Tag=$case.tag;Seconds=$case.seconds;Scenario='hanh-trinh';May='tai';Multiplier=$case.mult}
 if($case.step){$launchParams.BuocTai=$case.step}
 Start-Tai @launchParams
 $deadline=[DateTime]::UtcNow.AddSeconds($case.seconds+150)
 do {
  Start-Sleep -Seconds 10
  $state=((Get-Tai -Tag $case.tag -May tai)-join "`n")|ConvertFrom-Json
  if([DateTime]::UtcNow -gt $deadline){throw 'Timed out; retain container and all data'}
 }while($state.Running)
 Receive-Tai -Scenario hanh-trinh -Tag $case.tag -May tai
 $count=0
 foreach($line in Get-Content "$root/out/$($case.tag)/outputs.sha256"){
  $parts=$line -split '\s+',2
  $name=$parts[1].TrimStart('*',' ')
  if((Get-FileHash -LiteralPath "$root/out/$($case.tag)/$name").Hash.ToLower() -ne $parts[0]){throw "Output mismatch: $name"}
  $count++
 }
 Analyze-Tai -Tag $case.tag
 [IO.File]::AppendAllText("$root/linux/ps-reference.jsonl",((@{utc=[DateTime]::UtcNow.ToString('o');case=$case;state=$state;hashesMatched=$count}|ConvertTo-Json -Depth 5 -Compress)+"`n"),(New-Object Text.UTF8Encoding($false)))
}
