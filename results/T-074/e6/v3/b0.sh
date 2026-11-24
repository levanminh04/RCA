#!/usr/bin/env bash
# E6, bước 0 (chỉ đọc). Trên exp-app/exp-obs: bash -s -- app|obs < b0.sh
bat_bao_loi() {
  set -Eeuo pipefail
  export LC_ALL=C
  trap 'rc=$?; echo "LOI_THU_THAP $may / $muc (rc=$rc)" >&2; exit "$rc"' ERR
}

tien_trinh() {
  local ds
  muc=ps
  echo '== tien trinh cam (toan may, co doi so)'
  ds=$(ps -ww -eo pid=,ppid=,comm=,args=)
  # Chụp ps xong mới lọc. Dùng quan hệ cha/con để bỏ đúng cây lệnh dò.
  awk -v me="$$" '
    NF < 4 || $1 !~ /^[0-9]+$/ || $2 !~ /^[0-9]+$/ { bad=1; next }
    {
      pid[NR]=$1; cha[$1]=$2; dong[NR]=$0
      $1=$2=""; sub(/^ +/, "")
      cam[NR]=($0 ~ /runner4|tai_linux|chuoi_tai|inj3|_het_han|_renew|rcaburn|stage_m1|run_m1|xuat_bo_sung|sau_v082|safe_export|orchestrator/ ||
               $0 ~ /(^|[[:space:]\/])k6([[:space:]]|$)/)
    }
    END {
      if (bad || !NR || !(me in cha)) exit 2
      for (i=1; i<=NR; i++) {
        if (!cam[i]) continue
        p=pid[i]
        while (p && p != me && p in cha) p=cha[p]
        if (p != me) { print dong[i]; found=1 }
      }
      if (!found) print "(khong co)"
    }' <<< "$ds"
}

doc_cron() {
  local ds rc user
  muc=crontab
  echo '== cron'
  user=$(id -un)
  if ds=$(crontab -l 2>&1); then
    printf '%s\n' "$ds"
  else
    rc=$?
    printf '%s\n' "$ds"
    # crontab của Ubuntu trả 1 cả khi đúng là chưa lập lịch cho user này.
    if [[ $rc != 1 || $ds != "no crontab for $user" ]]; then return "$rc"; fi
  fi
}

doc_may_tai() {
  may=tai muc=utc
  bat_bao_loi
  date -u +utc\ %FT%T.%NZ
  muc=docker
  echo '-- rca-tai theo trang thai:'
  sudo -n docker ps -a --filter name=rca-tai- --format '{{.State}}' | sort | uniq -c
  tien_trinh
  doc_cron
}

may=${1:-app} muc=utc
bat_bao_loi
[[ $may = app || $may = obs ]] || { echo 'Dùng: bash b0.sh app|obs' >&2; exit 2; }
utc=$(date -u +%FT%T.%NZ)
host=$(hostname)
echo "== utc $utc host $host may=$may"
muc=git
echo '== git'
git -C /opt/rca-lab rev-parse HEAD
dirty=$(git --no-optional-locks -C /opt/rca-lab status --porcelain | wc -l)
echo "dirty_lines=$dirty"
tien_trinh
muc=docker
echo '== docker ps -a (ten|trang thai)'
docker ps -a --format '{{.Names}}|{{.State}}|{{.Status}}'
if [[ $may = obs ]]; then
  echo '== STOP'
  for f in /srv/rca-lab/runs/STOP /srv/rca-lab/load-controller/STOP; do
    if [[ -e $f ]]; then echo "CO $f"; else echo "khong $f"; fi
  done
  muc=compose
  echo '== compose ls'
  docker compose ls -a
  muc=inventory
  K=/etc/rca-lab/controller
  T=$(python3 -B -c "import sys; sys.path.insert(0,'/opt/rca-lab'); from campaigns.lib import inventory; print(inventory.public_ip('load-generator'))")
  [[ -n $T ]]
  echo "== MAY TAI $T"
  muc=ssh
  { declare -f bat_bao_loi tien_trinh doc_cron doc_may_tai; echo doc_may_tai; } |
    sudo -n ssh -i "$K/id_ed25519" -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 \
      -o StrictHostKeyChecking=yes -o "UserKnownHostsFile=$K/known_hosts" "ubuntu@$T" bash -s
fi
if [[ $may = app ]]; then
  muc=inj
  echo '== inj'
  if [[ -d /home/ubuntu/t063/inj ]]; then
    ds=$(ls /home/ubuntu/t063/inj)
    awk '/deadline|\.pid$/ { print; n++ } END { if (!n) print "(khong deadline/pid)" }' <<< "$ds"
  else
    echo khong_co_dir
  fi
  muc=paused
  echo '== paused'
  ids=$(docker ps -aq)
  if [[ -n $ids ]]; then
    xargs -r docker inspect -f '{{.Name}} paused={{.State.Paused}} running={{.State.Running}}' <<< "$ids"
  fi
  muc=toxics
  echo '== toxics'
  curl -fsS -m 5 127.0.0.1:8474/proxies | python3 -c 'import json,sys; d=json.load(sys.stdin); print({k:[t.get("name") for t in v.get("toxics",[])] for k,v in d.items()})'
  muc=lease
  echo '== lease'
  for s in booking-service event-service; do
    lease=$(sudo -n cat "/opt/flash-ticket-app/rca-faults/$s/control/control.json")
    printf '%s: %.300s\n' "$s" "$lease"
  done
fi
doc_cron
muc=timers
ds=$(systemctl list-timers --all --no-pager)
awk 'tolower($0) ~ /rca|t06|t07|m1|tai/ { print; n++ } END { if (!n) print "(khong timer khop)" }' <<< "$ds"
muc=utc
date -u '+== utc ket thuc %FT%T.%NZ'
