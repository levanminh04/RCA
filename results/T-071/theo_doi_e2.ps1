# T-071 — theo dõi chuỗi E2 trên exp-obs từ laptop (chỉ đọc). Thoát khi chuỗi tới trạng thái cuối
# (xong_chuoi / dung_chuoi / loi_noi_bo) hoặc tiến trình chuỗi không còn. Mỗi 600 s đọc trang-thai.json và dòng cuối nhật ký.
# Dùng: powershell -File theo_doi_e2.ps1 -Pid 906913
param([int]$ChuoiPid = 906913, [int]$Nhip = 600)
. 'D:/RCA-flashticket/results/T-058/dem-2026-11-10/remote.ps1'
$cmd = @"
K=/srv/rca-lab/runs/t071-e2
song=`$(kill -0 $ChuoiPid 2>/dev/null && echo co || echo khong)
cuoi=`$(grep -oE '"loai": "(xong_chuoi|dung_chuoi|loi_noi_bo)"' `$K/chuoi.jsonl | tail -1)
echo "utc=`$(date -u +%FT%TZ) pid_song=`$song cuoi=`$cuoi"
tr -d '\n' < `$K/trang-thai.json | cut -c1-300; echo
grep '"loai": "ket_qua_luot"' `$K/chuoi.jsonl | cut -c1-160
"@
while ($true) {
  try { $o = Invoke-Oracle -Machine obs -Command $cmd } catch { $o = "loi_ssh: $_" }
  Write-Output $o
  $s = ($o | Out-String)
  if ($s -match 'cuoi="loai"' -or $s -match 'pid_song=khong') { Write-Output 'KET_THUC'; break }
  Start-Sleep -Seconds $Nhip
}
