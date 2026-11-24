# BASH_ENV, chỉ dành cho bộ thử. SSH giả thực thi stdin bằng Bash trên laptop.
ps() {
  [[ "$*" = '-ww -eo pid=,ppid=,comm=,args=' ]] || return 90
  if [[ $CA = "$MAY_GIA-ps-loi" ]]; then return 6; fi
  if [[ $CA = ps-rong ]]; then return 0; fi
  printf '%s 1 bash bash -s\n' "$$"
  printf '900001 %s bash bash runner4.py\n900002 900001 k6 k6 run tu-do.js\n' "$$"
  printf '900003 1 sleep sleep 60\n'
  if [[ $CA = "$MAY_GIA-tien-trinh" ]]; then
    printf '51 1 k6 k6 --quiet run load.js\n52 1 python3 python3 runner4.py --output /tmp/grep.log\n'
  fi
}
crontab() {
  [[ "$*" = '-l' ]] || return 90
  case $CA in
    "$MAY_GIA-cron-loi") echo 'permission denied' >&2; return 1 ;;
    cron-trong) echo "no crontab for $(id -un)" >&2; return 1 ;;
    cron-dong-5) printf '#1\n#2\n#3\n#4\n* * * * * /fixture/lich-la-%s\n' "$MAY_GIA" ;;
    *) echo '# fixture' ;;
  esac
}
ssh() {
  [[ "$*" = '-i /etc/rca-lab/controller/id_ed25519 -o BatchMode=yes -o IdentitiesOnly=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=yes -o UserKnownHostsFile=/etc/rca-lab/controller/known_hosts ubuntu@load.fixture bash -s' ]] || return 90
  if [[ $CA = ssh-loi ]]; then cat >/dev/null; return 255; fi
  MAY_GIA=tai bash -s
}
sudo() {
  [[ $1 = -n ]] || return 90
  shift
  case $1 in
    ssh|docker) "$@" ;;
    cat) [[ $2 = /opt/flash-ticket-app/rca-faults/*/control/control.json ]] || return 90
         echo '{"action":"off"}' ;;
    *) return 90 ;;
  esac
}
git() {
  case "$*" in
    '-C /opt/rca-lab rev-parse HEAD') echo fixture-head ;;
    '--no-optional-locks -C /opt/rca-lab status --porcelain') [[ $CA != git-loi ]] ;;
    *) return 90 ;;
  esac
}
curl() {
  [[ "$*" = '-fsS -m 5 127.0.0.1:8474/proxies' ]] || return 90
  echo '{}'
}
python3() {
  case "$*" in
    *inventory.public_ip*) echo load.fixture ;;
    *json.load*) cat >/dev/null; echo '{}' ;;
    *) return 90 ;;
  esac
}
systemctl() {
  [[ "$*" = 'list-timers --all --no-pager' ]] || return 90
  if [[ $CA = timers-loi ]]; then return 7; fi
  echo 'fixture.timer'
}
