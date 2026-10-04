#!/usr/bin/env bash
# T-018: chạy một lượt chay_gdn.py, ghi tải máy lúc bắt đầu (E13) và log vào results/T-018/runs/<nhan>.log
# Cách dùng: bash chay_nen.sh <nhan> <tham số chay_gdn.py...>
nhan=$1; shift
LOG=/d/RCA-flashticket/results/T-018/runs/$nhan.log
{
  echo "# lượt $nhan bắt đầu $(date '+%Y-%m-%d %H:%M:%S')"
  powershell -NoProfile -Command "\$c=(Get-CimInstance Win32_Processor).LoadPercentage; \$r=[int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024); \"# tai CPU % = \$c ; RAM trong MB = \$r\""
  echo "# lệnh: chay_gdn.py --nhan $nhan $*"
  timeout 3600 /d/RCA-ext/envs/py38-gdn/Scripts/python.exe -u /d/RCA-flashticket/results/T-018/scripts/chay_gdn.py --nhan $nhan "$@"
  echo "# EXIT=$? kết thúc $(date '+%Y-%m-%d %H:%M:%S')"
} > "$LOG" 2>&1
