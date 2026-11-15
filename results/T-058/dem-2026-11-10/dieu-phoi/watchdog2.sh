#!/bin/bash
# Watchdog lượt đêm T-058: chặn Codex vượt phạm vi. Chạy nền, mỗi 3 phút một vòng.
# Vi phạm cứng -> dừng Codex (taskkill cây tiến trình), ghi ALERT.txt, thoát mã 3.
# Thay đổi trên máy 84 -> chỉ cảnh báo (có thể do CD của nhóm), không dừng.
W=/d/RCA-ext/overnight-T058; G=$W/guard; MARK=$G/MARKER
FT_REMOTE=https://github.com/levanminh04/flash-ticket-platform.git
alert(){ echo "$(date -u +%FT%TZ) $*" >> $G/ALERT.txt; echo "$(date -u +%FT%TZ) $*"; }
kill_codex(){
  if [ -f $G/codex.winpid ]; then taskkill //F //T //PID "$(cat $G/codex.winpid)" >/dev/null 2>&1; fi
  touch $G/KILLED
}
plink84(){ "/c/Program Files/PuTTY/plink.exe" -batch -ssh -l ubuntu -i "D:/RCA-ext/keys/FlashTicket-Control-Diagnosis.ppk" -hostkey "SHA256:GKGZPbWArBevP0sVSqS1S/ZM3NA1JylFkog+jkzUY28" -hostkey "SHA256:/GubrS13u1vnhHWZO/Il2Q9BOivtP6yYEGYXj61LZTQ" 52.64.237.84 "$1" < /dev/null 2>/dev/null; }
snap84(){ plink84 'cd /opt/flash-ticket-app/state && for f in *.current; do echo "${f%.current} $(cat $f)"; done; docker ps --format "{{.Names}}|{{.Image}}" | sort'; }

n=0
echo "$(date -u +%FT%TZ) watchdog2 bat dau" >> $G/watchdog.log
while true; do
  n=$((n+1))
  # Dừng khi launcher đã kết thúc
  [ -f $G/launcher.done ] && { echo "$(date -u +%FT%TZ) launcher xong, watchdog dung" >> $G/watchdog.log; exit 0; }

  # 1. File thay đổi trong vùng cấm (bỏ qua dữ liệu lớn, venv, IDE và file nội bộ git không mang nội dung)
  #    (a) git status của hai repo so với ảnh chụp gốc; (b) commit và nhánh cục bộ; (c) file mới sửa ở các vùng chính và thư mục khóa
  ch=""
  [ "$(git -C /d/RCA-flashticket status --porcelain=v1 2>/dev/null | sort)" != "$(cat $G/st-rca.txt)" ] && ch="$ch git-status-RCA"
  [ "$(git -C /d/Project/flash-ticket-platform status --porcelain=v1 2>/dev/null | sort)" != "$(cat $G/st-ft.txt)" ] && ch="$ch git-status-FlashTicket"
  [ "$( (git -C /d/RCA-flashticket rev-parse HEAD; git -C /d/RCA-flashticket for-each-ref --format='%(refname) %(objectname)'; git -C /d/Project/flash-ticket-platform rev-parse HEAD; git -C /d/Project/flash-ticket-platform for-each-ref --format='%(refname) %(objectname)') 2>/dev/null)" != "$(cat $G/refs-local.txt)" ] && ch="$ch commit-hoac-nhanh-cuc-bo"
  f=$(find /d/RCA-flashticket/src /d/RCA-flashticket/docs /d/RCA-flashticket/tasks /d/RCA-flashticket/results/T-058 /d/RCA-flashticket/AGENTS.md /d/RCA-flashticket/CLAUDE.md /d/RCA-ext/keys -path '*/__pycache__' -prune -o -newer $MARK -type f -print 2>/dev/null | head -5)
  [ -n "$f" ] && ch="$ch file:$(echo $f | tr '\n' ' ')"
  if [ -n "$ch" ]; then alert "VI PHAM: thay doi trong vung cam:$ch"; kill_codex; exit 3; fi

  # 2. Ref trên GitHub
  cur_ft=$(git ls-remote $FT_REMOTE 2>/dev/null | sort)
  if [ -n "$cur_ft" ] && [ "$cur_ft" != "$(cat $G/remote-ft.txt)" ]; then
    # refs/pull/*/merge do GitHub tự tính lại khi main đổi: bỏ qua. Nhánh hoặc tag đổi: tra tác giả; không tra được thì coi là nghi vấn.
    diffrefs=$(diff <(cat $G/remote-ft.txt) <(echo "$cur_ft") | grep '^>' | awk '$3 !~ /^refs\/pull\// {print $2" "$3}')
    mine=0
    while read -r sha ref; do
      [ -z "$sha" ] && continue
      who=$(curl -s -m 20 "https://api.github.com/repos/levanminh04/flash-ticket-platform/commits/$sha" | py -3 -c "import sys,json;d=json.load(sys.stdin);print((d.get('author') or {}).get('login',''), (d.get('committer') or {}).get('login',''), d.get('commit',{}).get('author',{}).get('email',''))" 2>/dev/null)
      if [ -z "$(echo $who | tr -d ' ')" ] || echo "$who" | grep -q -i -E "levanminh04|levanminh031204"; then mine=1; fi
      alert "ref FlashTicket doi: $ref $sha tac gia: ${who:-khong tra duoc}"
    done <<< "$diffrefs"
    echo "$cur_ft" > $G/remote-ft.txt
    if [ $mine = 1 ]; then alert "VI PHAM: co ref moi cua tai khoan levanminh04 trong dem"; kill_codex; exit 3; fi
  fi
  cur_rca=$(git -C /d/RCA-flashticket ls-remote origin 2>/dev/null | sort)
  if [ -n "$cur_rca" ] && [ "$cur_rca" != "$(cat $G/remote-rca.txt)" ]; then
    alert "VI PHAM: ref repo RCA tren GitHub thay doi"; echo "$cur_rca" > $G/remote-rca.txt; kill_codex; exit 3
  fi

  # 3. Máy 84: mỗi 5 vòng (khoảng 15 phút), chỉ cảnh báo
  if [ $((n % 5)) = 1 ]; then
    s=$(snap84)
    if [ -n "$s" ] && [ "$s" != "$(cat $G/84-snap.txt)" ]; then
      alert "CANH BAO: trang thai may 84 thay doi (co the do CD cua nhom). Xem 84-snap-$n.txt"
      echo "$s" > $G/84-snap-$n.txt; echo "$s" > $G/84-snap.txt
    fi
  fi
  echo "$(date -u +%FT%TZ) vong $n on" >> $G/watchdog.log
  sleep 180
done
