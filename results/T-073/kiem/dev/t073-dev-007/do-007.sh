#!/bin/bash
# T-073 lượt 9: CX-06 #5 trên gói cũ RECREATE-PAY c4d7999f. Ghi chỉ runs/t073-dev-007 và m1/t073-dev.
O=/srv/rca-lab/runs/t073-dev-007; C=/srv/rca-lab/runs/t073-dev-code/campaigns/online; X=c4d7999f
cd $O
sudo -n python3 -B $C/check_old_case.py chuan-bi --ca $X > chuan-bi.json 2> chuan-bi.err || { echo LOI-chuan-bi >> xong.log; exit 1; }
T=$(python3 -c "import json;print(json.load(open('chuan-bi.json'))['t'])")
export RCA_ONLINE_OUT=$O RCA_M1_ROOT=/srv/rca-lab/m1/t073-dev RCA_RUN_M1=/opt/rca-lab/campaigns/runner/run_m1.py
python3 -B $C/orchestrator.py mot --t $T --ra $O/t073-g1 --dev-capture /srv/rca-lab/m1/t073-dev/sim-capture/$X \
  --dev-prom /srv/rca-lab/m1/cases/$X/prometheus.json --dev-bo-sung /srv/rca-lab/m1/bo-sung/$X/prometheus-bo-sung.json > orchestrator.out 2>&1
echo "rc=$? $(date -u +%FT%TZ)" >> xong.log; echo XONG >> xong.log
