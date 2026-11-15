#!/bin/bash
# Chạy Codex cho lượt đêm T-058. Xử lý hết usage bằng cách chờ rồi resume. Hạn chót 00:00Z ngày 11/11.
W=/d/RCA-ext/overnight-T058; G=$W/guard; O=$W/out; mkdir -p $O
DEADLINE=$(date -u -d '2026-11-11T00:00:00Z' +%s)
SID="01a1c705-0249-7e32-a607-53d172d9c618"; tries=100; fails=0
log(){ echo "$(date -u +%FT%TZ) $*" >> $G/launcher.log; }
finish(){ log "ket thuc: $*"; echo "$*" > $G/launcher.done; exit 0; }
FLAGS=(-m gpt-6.1-sol -c 'model_reasoning_effort="high"' --dangerously-bypass-approvals-and-sandbox --skip-git-repo-check)

log "launcher2 bat dau (resume co STEER)"
MSG="Claude (dieu phoi) tam dung ban de them kenh chi dao. Tu gio: moi lan cap nhat out/CHECKPOINT.md (it nhat 15 phut mot lan) va truoc moi chang, doc out/STEER.md; muc nao chua xu ly thi lam theo va ghi \"da xu ly STEER #n\" vao out/LOG-dem.md. Doc out/STEER.md ngay bay gio. Cac job nohup tren may Oracle van chay; kiem lai trang thai roi lam tiep tu out/CHECKPOINT.md. Luat va han gio giu nguyen nhu AGENTS.md va PROMPT.md."
while true; do
  [ -f $G/KILLED ] && finish "watchdog da dung Codex"
  [ -f $O/DONE.md ] && finish "Codex tao DONE.md"
  now=$(date -u +%s); [ $now -ge $DEADLINE ] && finish "het han 00:00Z"
  tries=$((tries+1)); L=$G/codex-run-$tries.log
  cd $W
  if [ -z "$SID" ]; then
    log "lan $tries: chay moi"
    codex exec "${FLAGS[@]}" -o $G/last-$tries.txt - < $W/PROMPT.md > $L 2>&1 &
  else
    log "lan $tries: resume $SID"
    codex exec resume "${FLAGS[@]}" -o $G/last-$tries.txt "$SID" "$MSG" < /dev/null > $L 2>&1 &
  fi
  pid=$!
  MSG="Tiep tuc luot dem T-058. Doc out/STEER.md, out/CHECKPOINT.md va out/LOG-dem.md roi lam tiep tu buoc ke tiep. Luat va han gio giu nguyen nhu AGENTS.md va PROMPT.md."
  ps | awk -v p=$pid '$1==p{print $4}' > $G/codex.winpid
  # Còn hạn thì chờ; quá hạn thì dừng
  while kill -0 $pid 2>/dev/null; do
    if [ $(date -u +%s) -ge $DEADLINE ]; then taskkill //F //T //PID "$(cat $G/codex.winpid)" >/dev/null 2>&1; log "dung Codex vi het han"; fi
    sleep 30
  done
  wait $pid; rc=$?
  [ -z "$SID" ] && SID=$(grep -m1 -o -E 'session id: [0-9a-f-]+' $L | awk '{print $3}')
  log "lan $tries ket thuc rc=$rc sid=$SID"
  [ -f $G/KILLED ] && finish "watchdog da dung Codex"
  [ -f $O/DONE.md ] && finish "Codex tao DONE.md"
  if grep -q -i -E "usage limit|rate limit|429|quota|too many requests|limit reached|try again (at|in)" $L; then
    log "het usage; cho 15 phut roi thu lai"; fails=0; sleep 900; continue
  fi
  if [ $rc -ne 0 ]; then
    fails=$((fails+1)); [ $fails -ge 4 ] && finish "Codex loi $fails lan lien tiep (xem $L)"
    sleep 120; continue
  fi
  # Codex dừng bình thường mà chưa có DONE.md: nhắc làm tiếp tối đa 3 lần
  fails=$((fails+1)); [ $fails -ge 4 ] && finish "Codex dung nhieu lan ma chua xong"
  sleep 30
done
