$script:L1Root=$PSScriptRoot
. "$PSScriptRoot/../tai/c1.ps1"
function Invoke-L1 {
 param([ValidateSet('app','tai','obs')][string]$May='app',[string]$Command,[switch]$Mutation)
 Assert-C1Running
 if($Mutation -and $May -eq 'obs'){throw 'exp-obs read only'}
 if($Mutation){Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" ("`n## "+[DateTime]::UtcNow.ToString('o')+" - $May`n`n"+'```sh'+"`n$Command`n"+'```')}
 $target=Get-C1Target $May
 $OutputEncoding=New-Object System.Text.UTF8Encoding($false)
 $encoded=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($Command.Replace("`r`n","`n")+"`n"))
 $encoded | & $script:C1Ssh -i $target.Key -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes "-oUserKnownHostsFile=$($target.Known)" "ubuntu@$($target.HostName)" 'base64 --decode --ignore-garbage | bash'
 $exit=$LASTEXITCODE
 if($Mutation){Add-Content -Encoding UTF8 "$script:L1Root/thay-doi-may.md" "`nExit: $exit"}
 if($exit -ne 0){throw "SSH $May exit $exit"}
}
function Get-L1AuthSource {
 $manifest=Get-Content -Raw -Encoding UTF8 "$script:C1Repo/results/T-058/dem-2026-11-10/artifacts-sha256.json" | ConvertFrom-Json
 $path="$script:C1Repo/results/T-058/dem-2026-11-10/auth.py"
 if((Get-FileHash $path -Algorithm SHA256).Hash.ToLower() -ne $manifest.files.'auth.py'.sha256){throw 'auth source hash mismatch'}
 $source=[IO.File]::ReadAllText($path)
 return $source.Substring(0,$source.IndexOf("if __name__=='__main__':"))
}
function Invoke-L1Python {
 param([string]$File,[switch]$Mutation,[switch]$Auth,[ValidateSet('app','tai','obs')][string]$May='app')
 $source=[IO.File]::ReadAllText((Resolve-Path $File))
 if($Auth){$source=(Get-L1AuthSource)+"`n"+[IO.File]::ReadAllText("$script:L1Root/api-lib.py")+"`n"+$source}
 Invoke-L1 -May $May -Mutation:$Mutation -Command ("python3 - <<'PY'`n"+$source+"`nPY")
}
