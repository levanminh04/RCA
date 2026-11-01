# T-045 bước 2 (D1 phần E1 bật, E2), 2b (D3) và D4, phần Nezha-OB. Không đọc nhãn; không đọc verdict của cấu hình khối K (Đ-6).
set -e
source results/T-045/scripts/moi_truong.sh
loc() { grep -v "Deprecation\|utcfromtimestamp\|date_info"; }
$PY -B results/T-045/scripts/d4_e1_cp.py --ra results/T-045/e1-cp.json 2>&1 | loc > results/T-045/runs/b2-d4-nezha-001.stdout.txt
PYTHONHASHSEED=0 $PY -B results/T-045/scripts/chay_pha1.py --luot b2-d1-kE1E2-nezha-001 --cau-hinh K-E1,K-E2 --ds Nezha-OB 2>&1 | loc > results/T-045/runs/b2-d1-kE1E2-nezha-001.stdout.txt
for k in hoan_toan nguong nguong_cung_lop; do
  PYTHONHASHSEED=0 $PY -B results/T-045/scripts/chay_pha1.py --luot b2b-d3-$k-nezha-001 --cau-hinh K-E3 --ds Nezha-OB --khop $k 2>&1 | loc > results/T-045/runs/b2b-d3-$k-nezha-001.stdout.txt
done
for k in hoan_toan nguong nguong_cung_lop; do
  PYTHONHASHSEED=0 $PY -B results/T-045/scripts/chay_pha1.py --luot b2b-d3-$k-sim09-nezha-001 --cau-hinh K-E3 --ds Nezha-OB --khop $k --sim-th 0.9 2>&1 | loc > results/T-045/runs/b2b-d3-$k-sim09-nezha-001.stdout.txt
done
echo XONG
