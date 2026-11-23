#!/bin/bash
# T-072 bước 1: khảo sát nhẹ, chỉ ĐỌC Prometheus exp-obs (truy vấn instant; cửa sổ trong biểu thức ≤ 10 phút).
P=http://127.0.0.1:9090/api/v1
q() { # $1 nhãn, $2 thời điểm epoch, $3 biểu thức
  echo "### $1 @ $2"
  curl -s -G --max-time 30 "$P/query" --data-urlencode "query=$3" --data-urlencode "time=$2"
  echo
  sleep 0.5
}
T067=$(date -u -d '2026-11-18T08:30:00Z' +%s)
B1=$(date -u -d '2026-11-19T09:50:00Z' +%s)
FL=$(date -u -d '2026-11-19T12:30:00Z' +%s)
X3=$(date -u -d '2026-11-19T16:05:00Z' +%s)
NOW=$(date -u +%s)
echo "### now $NOW"
q build "$NOW" 'prometheus_build_info'
G='http_server_request_duration_seconds'
for T in $T067 $B1 $FL $X3 $NOW; do
  q nhan-route "$T" "count by (http_route, http_request_method, http_response_status_code) (${G}_count{service_name=\"api-gateway\"})"
  q tang-5m "$T" "sum by (http_route, http_response_status_code) (increase(${G}_count{service_name=\"api-gateway\"}[5m]))"
done
q le "$T067" "count by (le) (${G}_bucket{service_name=\"api-gateway\"})"
q mau-10m "$T067" "count_over_time(${G}_count{service_name=\"api-gateway\",http_route=\"payment\"}[10m])"
q mau-10m-b1 "$B1" "count_over_time(${G}_count{service_name=\"api-gateway\",http_route=\"booking\"}[10m])"
q mot-chuoi "$T067" "${G}_count{service_name=\"api-gateway\",http_route=\"payment\"}"
q ts-raw "$T067" "${G}_count{service_name=\"api-gateway\",http_route=\"payment\",http_response_status_code=\"200\"}[2m]"
q p95-5m "$T067" "histogram_quantile(0.95, sum by (http_route, le) (rate(${G}_bucket{service_name=\"api-gateway\"}[5m])))"
q p95-5m-fl "$FL" "histogram_quantile(0.95, sum by (http_route, le) (rate(${G}_bucket{service_name=\"api-gateway\"}[5m])))"
q svc-co-hist "$T067" "count by (service_name) (${G}_count)"
q httpcheck-ten "$T067" 'count by (__name__, http_url) ({__name__=~"httpcheck_.*"})'
q httpcheck-status "$T067" 'httpcheck_status{http_url=~".*8083.*"}'
q httpcheck-mau "$T067" 'count_over_time(httpcheck_status{http_url=~".*8083.*"}[10m])'
q httpcheck-err-b1 "$B1" 'count by (http_url) (count_over_time(httpcheck_error[10m]))'
q httpcheck-err-now "$NOW" 'count by (http_url) (count_over_time(httpcheck_error[10m]))'
q ts-status-raw "$T067" 'httpcheck_status{http_url=~".*8083.*",http_status_class="2xx"}[1m]'
