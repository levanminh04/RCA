#!/bin/bash
# T-072 bước 1, khảo sát 2: chỉ ĐỌC Prometheus exp-obs. Instant query; mọi cửa sổ trong biểu thức ≤ 10 phút.
P=http://127.0.0.1:9090/api/v1
q() { echo "### $1 @ $2"; curl -s -G --max-time 30 "$P/query" --data-urlencode "query=$3" --data-urlencode "time=$2"; echo; sleep 0.5; }
PA=1795100379            # PAUSE-PAYMENT fault-start (sổ T-069), chỉ để khảo sát dạng chuỗi khi đầu dò lỗi
T067=$(date -u -d '2026-11-18T08:30:00Z' +%s)
NOW=$(date -u +%s)
PM=$((PA+120))
q err-raw "$PM" 'httpcheck_error[2m]'
q st-raw-8083 "$PM" 'httpcheck_status{http_url=~".*8083.*"}[1m]'
q st-raw-8082 "$PM" 'httpcheck_status{http_url=~".*8082.*",http_status_class="2xx"}[1m]'
q gap-8082 "$PM" 'count_over_time(httpcheck_status{http_url=~".*8082.*",http_status_class="2xx"}[5m])'
q ts-sel "$PM" 'max by (http_url) (timestamp(httpcheck_error))'
q ts-ok "$PM" 'max by (http_url) (timestamp(httpcheck_status{http_status_code!=""}))'
LERR='max by (http_url) (timestamp(httpcheck_error))'
LOK='max by (http_url) (timestamp(httpcheck_status{http_status_code!=""}))'
LANY='max by (http_url) (timestamp(httpcheck_error) or timestamp(httpcheck_status{http_status_code!=""}))'
LIVE="((($LERR > on (http_url) $LOK) or on (http_url) ($LERR unless on (http_url) $LOK)) and on (http_url) ((time() - $LERR) <= 60)) * 0 + 1"
FRESH="count((time() - $LANY) <= 60)"
for T in $T067 $PM $((PA+300)) $((PA+590)) $((PA+640)) $((PA+700)) $NOW; do
  q live "$T" "$LIVE"
  q fresh "$T" "$FRESH"
done
G='http_server_request_duration_seconds'
SEL='service_name="api-gateway",http_route="payment"'
TOT="sum by (http_route) (increase(${G}_count{$SEL}[5m]))"
E5="sum by (http_route) (increase(${G}_count{$SEL,http_response_status_code=~\"5..\"}[5m]))"
ERR="(($E5 or on (http_route) 0 * $TOT) / $TOT) and on (http_route) ($TOT >= 30)"
P95="histogram_quantile(0.95, sum by (http_route, le) (rate(${G}_bucket{$SEL}[5m]))) and on (http_route) ($TOT >= 30)"
for T in $T067 $PM $((PA+300)) $((PA+590)) $((PA+700)) $NOW; do
  q err-pay "$T" "$ERR"
  q p95-pay "$T" "$P95"
  q tot-pay "$T" "$TOT"
done
q p95-pay-raw-pause "$((PA+300))" "sum by (le) (increase(${G}_bucket{$SEL}[5m]))"
