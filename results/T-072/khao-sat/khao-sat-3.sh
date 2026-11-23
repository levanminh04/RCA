#!/bin/bash
# T-072 khảo sát 3: chỉ ĐỌC; instant query, cửa sổ ≤ 10 phút.
P=http://127.0.0.1:9090/api/v1
q() { echo "### $1 @ $2"; curl -s -G --max-time 30 "$P/query" --data-urlencode "query=$3" --data-urlencode "time=$2"; echo; sleep 0.5; }
PA=1795100379
q err-10m $((PA+600)) 'httpcheck_error{http_url=~".*8083.*"}[10m]'
q ok-10m $((PA+700)) 'httpcheck_status{http_url=~".*8083.*",http_status_code!=""}[10m]'
