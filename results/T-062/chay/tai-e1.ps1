# T-062 E1: bọc công cụ tải của Codex (results/T-062/tai/chay-tai.ps1). Thêm Start-TaiFlash cho ô FLASH-HEALTHY:
# giống hệt Start-Tai, chỉ thay workload bằng chay/k6/workload-t062-flash.js (cùng hỗn hợp, fixture, token, image).
. "$PSScriptRoot/../tai/chay-tai.ps1"

# Khi gọi từ bộ chạy (powershell -Command), pipe token sang ssh bị thêm BOM UTF-8 → k6 JSON.parse lỗi (exit 107,
# D2 lần 1 19:22Z). Bọc hàm gốc: ghi token như cũ rồi gỡ BOM ngay trên máy tải (không đọc/in giá trị).
${function:Initialize-C1TokenGoc} = ${function:Initialize-C1Token}
function Initialize-C1Token {
 param([ValidateSet('obs','tai')][string]$May='tai')
 Initialize-C1TokenGoc -May $May
 Invoke-C1 -May $May -Mutation -Command "sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test `"`$(head -c1 /opt/rca-tai/secret/tokens.json)`" = '{'"
}

function Start-TaiFlash {
 param([Parameter(Mandatory)][ValidatePattern('^[a-z0-9][a-z0-9-]{0,47}$')][string]$Tag,
       [ValidateRange(1,100)][int]$Rate=5,[ValidateRange(1,100)][int]$FlashRate=15,
       [ValidateSet('tai','obs')][string]$May='tai')
 Assert-C1Running
 if(!(Test-Path "$script:C1Repo/results/T-062/ha-tang/A2-XONG")){throw 'A2-XONG missing: load prohibited'}
 $config=Get-Content -Raw -Encoding UTF8 "$script:C1Root/k6/cau-hinh.json" | ConvertFrom-Json
 Invoke-C1 -May $May -Mutation -Command "mkdir -p /opt/rca-tai/k6-e1"
 Send-C1File -May $May -Source "$PSScriptRoot/k6/workload-t062-flash.js" -Destination "/opt/rca-tai/k6-e1/workload-t062-flash.js"
 Invoke-C1 -May $May -Command "set -eu; test ! -e /opt/rca-tai/out/$Tag; test -z `"`$(sudo -n docker ps -q --filter name=rca-tai-)`""
 Initialize-C1Token -May $May
 $command=@'
set -euo pipefail
cd /opt/rca-tai
test ! -e out/__TAG__
mkdir out/__TAG__
cp k6-e1/workload-t062-flash.js out/__TAG__/workload-t062.js
cp k6/cau-hinh.json k6/fixtures.json out/__TAG__/
date -u --iso-8601=seconds > out/__TAG__/start-utc.txt
printf '{"machine":"__MAY__","seconds":1800,"rate":__RATE__,"flash_rate":__FLASH__,"workload":"flash","image":"__IMAGE__"}\n' > out/__TAG__/run.json
sha256sum out/__TAG__/workload-t062.js out/__TAG__/cau-hinh.json out/__TAG__/fixtures.json > out/__TAG__/inputs.sha256
sudo -n docker run -d --name rca-tai-__TAG__ --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/__TAG__:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/__TAG__:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=__MAY__ -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=__RATE__ -e FT_FLASH_RATE=__FLASH__ \
  __IMAGE__ run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
'@
 $command=$command.Replace('__TAG__',$Tag).Replace('__MAY__',$May).Replace('__RATE__',[string]$Rate).Replace('__FLASH__',[string]$FlashRate).Replace('__IMAGE__',$config.image)
 Invoke-C1 -May $May -Mutation -Command $command
}
