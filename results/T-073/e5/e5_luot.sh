#!/bin/bash
# T-073 E5 (S4-9): một lượt PAUSE-PAYMENT, tải ×1 1800 s (600 nền | 600 lỗi | 600 hồi phục), như chu kỳ T-069/runner4.
# Chạy NỀN trên laptop (điều khiển qua SSH): tải bằng tai_linux.py trên exp-obs; tiêm bằng inj3.py trên exp-app
# (khóa exp-app của laptop; inj3 tự gỡ pause đúng hạn trên exp-app nếu laptop mất mạng). Sổ tiêm ghi bằng
# ledger_append.py (sudo -u ledger) trên exp-obs; đầu ra inj3 chỉ vào sổ, không vào nhật ký này. Bộ điều phối T-073
# không đọc sổ hay nhật ký này. Giờ đích tính theo đồng hồ exp-obs (date +%s qua SSH), không theo laptop.
#   bash e5_luot.sh <thư mục ra trên laptop>
set -u
O=${1:?thu muc ra}; mkdir -p "$O"
SP=/c/Users/84583/AppData/Local/Temp/claude/5926e3c52aa473a7/7a4e4d8c-3bff-46c2-bf4e-fa8eba770c1d/scratchpad
OBS="$SP/obs.sh"; APP="$SP/app.sh"
TAG=t073-e5-01-x1; CELL=PAUSE-PAYMENT; PHASE=600
SO=/srv/rca-lab/ledger/t073-e5-01.jsonl
TL="cd /opt/rca-lab && python3 load/controller/tai_linux.py"
INJ="python3 /opt/rca-lab/faults/injectors/docker/inj3.py"
L="$O/nhat-ky.jsonl"
log() { printf '{"utc": "%s", "msg": "%s"}\n' "$(date -u +%FT%T.%3NZ)" "$*" >> "$L"; }
obs_now() { "$OBS" 'date +%s'; }
so() {  # so <event> <json-khác (không ngoặc)>
  local rec="{\"utc\": \"$("$OBS" 'date -u +%FT%T.%6NZ')\", \"event\": \"$1\"${2:+, $2}}"
  printf '%s' "$rec" | "$OBS" "sudo -n -u ledger python3 -B /opt/rca-lab/campaigns/runner/ledger_append.py $SO" \
    || { log "LOI ghi so event=$1"; return 1; }
}
cho_toi() {  # cho_toi <epoch exp-obs> <nhãn>
  local d; d=$(( $1 - $(obs_now) )); log "cho $2 ${d}s"; [ $d -gt 0 ] && sleep $d; log "toi $2"
}
st() { py -3 -c 'import json,sys; d=json.load(sys.stdin); s=d["result"]["state"] if d.get("ok") else {}; print(d.get("ok"), s.get("Running"), s.get("StartedAt"), s.get("FinishedAt"), s.get("ExitCode"))' 2>/dev/null | tr -d '\r' || echo "False None None None None"; }

log "bat dau tag=$TAG cell=$CELL"
# 0. sạch trước chu kỳ (K10)
v=$("$APP" "$INJ verify"); echo "$v" > "$O/verify-truoc.txt"
echo "$v" | grep -q '"sach": true' || { log "DUNG: verify truoc khong sach"; so run-abort-dirty '"where": "truoc-chu-ky"'; exit 3; }
so cycle-begin "\"cell\": \"$CELL\", \"load_tag\": \"$TAG\", \"multiplier\": 1, \"phase_s\": $PHASE" || exit 3
# 1. tải
"$OBS" "$TL start --tag $TAG --seconds $((3*PHASE))" > "$O/tai-start.json" 2>&1
for i in 1 2 3; do read ok run sa fa ec < <("$OBS" "$TL get --tag $TAG" | st); [ "$ok" = True ] && break; sleep 5; done
if [ "$ok" != True ] || [ "$run" != True ]; then log "DUNG: tai khong Running sau start ok=$ok run=$run"; so cycle-abort '"reason": "load"'; exit 4; fi
S=$("$OBS" "date -d '$sa' +%s"); printf '{"tag": "%s", "StartedAt": "%s", "S_epoch": %s}\n' "$TAG" "$sa" "$S" > "$O/DA-PHAT"
log "tai Running StartedAt=$sa"; so load-start "\"epoch\": $S, \"StartedAt\": \"$sa\""
# 2. K6 sau tải (trước tiêm): lưu lượng route payment ở gateway trong 10 phút > 0, đầu dò 8083 mới
cho_toi $((S + PHASE - 30)) "k6"
"$OBS" 'P=http://127.0.0.1:9090; date -u +%FT%TZ; curl -s -m 10 "$P/api/v1/query" --data-urlencode "query=sum by (http_route) (increase(http_server_request_duration_seconds_count{service_name=\"api-gateway\",http_route=\"payment\"}[10m]))"; echo; curl -s -m 10 "$P/api/v1/query" --data-urlencode "query=time() - max by (http_url) (timestamp(httpcheck_status{http_url=~\".*:8083/.*\",http_status_code!=\"\"}))"; echo' > "$O/k6-sau-tai.txt" 2>&1
n=$(py -3 -c 'import json,sys; L=[l for l in open(sys.argv[1]) if l.startswith("{")]; r=json.loads(L[0])["data"]["result"]; a=json.loads(L[1])["data"]["result"]; print(int(bool(r) and float(r[0]["value"][1])>0 and bool(a) and float(a[0]["value"][1])<60))' "$O/k6-sau-tai.txt" 2>/dev/null | tr -d '\r' || echo 0)
if [ "$n" != 1 ]; then log "DUNG truoc tiem: K6 khong dat"; so cycle-abort '"reason": "k6"'; "$OBS" "$TL stop --tag $TAG" >> "$O/tai-stop.txt" 2>&1; exit 5; fi
log "k6 dat"
# 3. tiêm (đầu ra inj3 chỉ vào sổ)
cho_toi $((S + PHASE)) "tiem"
so mark "\"cell\": \"$CELL\""
r=$("$APP" "$INJ start $CELL --seconds $PHASE" 2>&1); rc=$?
if [ $rc -ne 0 ]; then so fault-start-failed "\"cell\": \"$CELL\", \"rc\": $rc"; log "tiem LOI rc=$rc (chi tiet trong so)";
  printf '%s' "{\"utc\": \"$(date -u +%FT%TZ)\", \"event\": \"inj-out\", \"out\": $(printf '%s' "$r" | py -3 -c 'import json,sys; print(json.dumps(sys.stdin.read()[-2000:]))')}" | "$OBS" "sudo -n -u ledger python3 -B /opt/rca-lab/campaigns/runner/ledger_append.py $SO"
else
  so fault-start "\"cell\": \"$CELL\", \"inj\": $(printf '%s' "$r" | py -3 -c 'import json,sys; print(json.dumps(sys.stdin.read()[-2000:]))')"; log "tiem rc=0"
fi
# 4. gỡ đúng hạn (idempotent; inj3 cũng tự gỡ ở +605 trên exp-app)
cho_toi $((S + 2*PHASE + 10)) "go"
r=$("$APP" "$INJ stop $CELL" 2>&1); so fault-stop "\"cell\": \"$CELL\", \"inj\": $(printf '%s' "$r" | py -3 -c 'import json,sys; print(json.dumps(sys.stdin.read()[-2000:]))')"; log "go xong"
v=$("$APP" "$INJ verify"); echo "$v" > "$O/verify-sau.txt"; so verify-sau "\"sach\": $(echo "$v" | grep -q '"sach": true' && echo true || echo false)"
log "verify sau: $(echo "$v" | grep -q '"sach": true' && echo sach || echo KHONG-SACH)"
# 5. chờ tải dừng, nhận kết quả
han=$((S + 3*PHASE + 90 + 900)); da_stop=0
while :; do
  sleep 30; read ok run sa2 fa ec < <("$OBS" "$TL get --tag $TAG" | st); echo "$(date -u +%FT%TZ) ok=$ok running=$run" >> "$O/get.log"
  [ "$ok" = True ] && [ "$run" = False ] && break
  if [ $(obs_now) -gt $han ]; then
    if [ $da_stop = 0 ]; then "$OBS" "$TL stop --tag $TAG" >> "$O/get.log" 2>&1; da_stop=1; log "qua han: stop --tag"; else log "van Running sau stop"; exit 6; fi
  fi
done
printf '{"tag": "%s", "StartedAt": "%s", "FinishedAt": "%s", "ExitCode": "%s"}\n' "$TAG" "$sa" "$fa" "$ec" > "$O/DA-XONG"
so cycle-end "\"load_tag\": \"$TAG\", \"FinishedAt\": \"$fa\", \"ExitCode\": \"$ec\""
for i in 1 2 3; do "$OBS" "$TL receive --tag $TAG" > "$O/receive.json" 2>&1 && break; sleep 60; done
log "xong"
