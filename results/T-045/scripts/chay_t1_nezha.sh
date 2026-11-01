# T-045 bước 2, phần Nezha-OB (RE2-TT dừng vì ĐC1). Mỗi seed một tiến trình (Đ-2); xáo hàng ở seed 0 (Đ-3);
# kiểm ghép (Đ-1) trên 2 ca đầu.
set -e
source results/T-045/scripts/moi_truong.sh
loc() { grep -v "Deprecation\|utcfromtimestamp\|date_info"; }
PYTHONHASHSEED=0 $PY -B results/T-045/scripts/chay_pha1.py --luot b1-kiem-ghep-nezha-001 --cau-hinh T1 --ds Nezha-OB --dau 2 --kiem-ghep 2>&1 | loc > results/T-045/runs/b1-kiem-ghep-nezha-001.stdout.txt
for s in 0 1 2; do
  PYTHONHASHSEED=$s $PY -B results/T-045/scripts/chay_pha1.py --luot b2-t1-nezha-seed$s-001 --cau-hinh T1 --ds Nezha-OB 2>&1 | loc > results/T-045/runs/b2-t1-nezha-seed$s-001.stdout.txt
done
PYTHONHASHSEED=0 $PY -B results/T-045/scripts/chay_pha1.py --luot b2-t1-nezha-xao0-001 --cau-hinh T1 --ds Nezha-OB --xao 0 2>&1 | loc > results/T-045/runs/b2-t1-nezha-xao0-001.stdout.txt
echo XONG
