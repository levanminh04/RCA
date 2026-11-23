# T-071 — chờ lượt E3 (a) xong trên exp-obs (chỉ đọc). Thoát khi get.log có "xong" hoặc có file lỗi/can thiệp, hoặc script không còn.
param([int]$Pid1 = 928814, [int]$Nhip = 120)
. 'D:/RCA-flashticket/results/T-058/dem-2026-11-10/remote.ps1'
$cmd = "D=/srv/rca-lab/runs/t071-e3; echo utc=`$(date -u +%FT%TZ) song=`$(kill -0 $Pid1 2>/dev/null && echo co || echo khong); ls `$D; tail -1 `$D/get.log 2>/dev/null"
while ($true) {
  try { $o = Invoke-Oracle -Machine obs -Command $cmd } catch { $o = "loi_ssh: $_" }
  $s = ($o | Out-String); Write-Output $s
  if ($s -match ' xong' -or $s -match 'CAN-CAN-THIEP|CHUA-XAC-MINH|LOI-START' -or $s -match 'song=khong') { Write-Output 'KET_THUC'; break }
  Start-Sleep -Seconds $Nhip
}
