#!/bin/bash
# T-025 trên EC2 thứ hai (3.107.246.249), tmux phiên "t025": SPEC bước 2 và 3 (phần N-Sigma).
# Thứ tự: kiểm dữ liệu → tự kiểm biên (N8) → N-Sigma tập chính → RCA tại t̂ của N-Sigma → N-Sigma đối chứng.
# Không đọc nhãn. Xem tiến độ: cat ~/rca/T-025/trang-thai.txt. Dừng: tmux kill-session -t t025.
set -u
B=~/rca/T-025
cd $B/repo
export PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 TMPDIR=$B/tmp MPLCONFIGDIR=$B/cache/mpl MPLBACKEND=Agg
export XDG_CACHE_HOME=$B/cache PYTHONPATH=$B/src/RCAEval:$B/src/baro:$B/repo/src:$B/src/CIRCA
P=$B/envs/main/bin/python
S=results/T-025/scripts
TT=$B/trang-thai.txt
buoc() {  # buoc <tên> <lệnh...>
  local ten=$1; shift
  echo "$(date -u +%FT%TZ) BAT DAU $ten" >> $TT
  "$@" > $B/runs/$ten.out 2> $B/runs/$ten.err
  local rc=$?
  echo "$(date -u +%FT%TZ) XONG $ten exit=$rc" >> $TT
  return $rc
}
buoc kiem-du-lieu $P -B -W ignore $S/kiem_du_lieu.py || { echo "DUNG: kiem du lieu loi" >> $TT; exit 1; }
grep -q '"so_tep_sai": 0' results/T-025/runs/kiem-du-lieu-ec2-001/kiem-du-lieu.json \
  || { echo "$(date -u +%FT%TZ) DUNG: hash du lieu sai" >> $TT; exit 1; }
[ -f results/T-025/runs/kiem-bien-m2-001/ket-thuc.json ] \
  || buoc kiem-bien $P -B -W ignore $S/rca_b.py kiem-bien-m2 t_co_dinh=dev-03d4910932:1,100,1440
buoc nsigma-chinh $P -B -W ignore $S/chay_b.py nsigma-chinh-m2 nsigma tap_cot=bocpd trang_thai=$TT
buoc rca-nsigma $P -B -W ignore $S/rca_b.py rca-nsigma-m2 tu=runs/nsigma-chinh-m2-001
buoc nsigma-doi-chung $P -B -W ignore $S/chay_b.py nsigma-doi-chung-m2 nsigma tap_cot=tat_ca trang_thai=$TT
echo "$(date -u +%FT%TZ) XONG CHUOI MAY 2" >> $TT
