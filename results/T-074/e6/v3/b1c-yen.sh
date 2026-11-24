#!/usr/bin/env bash
# E6, bước 1c. Chỉ đọc. Đối chiếu trước và sau dump bằng các lần gọi riêng.
set -eu -o pipefail
phut=
if (( $# )); then
  if [[ $# != 2 || $1 != --phut-khong-tai || ! $2 =~ ^(0|[1-9][0-9]*)$ ]]; then
    echo 'Dùng: bash b1c-yen.sh [--phut-khong-tai N] (số phút người trực đã xác nhận)' >&2
    exit 2
  fi
  phut=$2
fi

loi() { echo "LOI_THU_THAP $1" >&2; exit "${2:-2}"; }
doc_sql() {
  local db=$1 sql=$2
  kq=$(docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -X -At \
    -v ON_ERROR_STOP=1 -d "$db" -c "$sql") || loi "$db / $muc: psql" "$?"
}
ban=0
date -u '+== utc %FT%T.%NZ'
muc=don
doc_sql booking_db "WITH dem AS (
  SELECT lifecycle_state, count(*) AS n FROM booking_schema.tbl_orders GROUP BY lifecycle_state
), etats(lifecycle_state) AS (
  VALUES ('PENDING_PAYMENT'), ('ISSUING'), ('COMPLETED'), ('CANCELLED'), ('EXPIRED'), ('ISSUANCE_FAILED')
) SELECT lifecycle_state, coalesce(n, 0) FROM etats FULL JOIN dem USING (lifecycle_state)
  ORDER BY lifecycle_state"
declare -A dem_don=()
while IFS= read -r dong; do
  [[ $dong =~ ^([A-Z_]+)\|([0-9]+)$ ]] || loi 'đơn: thiếu trạng thái hoặc số đếm'
  trang_thai=${BASH_REMATCH[1]} so=${BASH_REMATCH[2]}
  case $trang_thai in
    PENDING_PAYMENT|ISSUING|COMPLETED|CANCELLED|EXPIRED|ISSUANCE_FAILED) ;;
    *) loi "đơn: trạng thái ngoài lược đồ $trang_thai" ;;
  esac
  [[ ! ${dem_don[$trang_thai]+co} ]] || loi "đơn: lặp $trang_thai"
  dem_don[$trang_thai]=$so
  echo "don|$trang_thai|$so"
done <<< "$kq"
[[ ${#dem_don[@]} = 6 ]] || loi 'đơn: thiếu kết quả theo trạng thái'
chua_xong=$((10#${dem_don[PENDING_PAYMENT]} + 10#${dem_don[ISSUING]}))
echo "don|CHUA_KET_THUC|$chua_xong"
(( chua_xong == 0 )) || ban=1

muc=kho
doc_sql booking_db "SELECT held, purchased FROM booking_schema.tbl_ticket_type_inventory
  WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453'"
[[ $kq =~ ^([0-9]+)\|([0-9]+)$ ]] || loi 'kho: cần đúng một dòng held và purchased'
echo "held=${BASH_REMATCH[1]} purchased=${BASH_REMATCH[2]}"
[[ ${BASH_REMATCH[1]} = 0 ]] || ban=1

muc=outbox
dem_outbox() {
  doc_sql "$1" "SELECT count(*) FROM $2 WHERE published_at IS NULL"
  [[ $kq =~ ^[0-9]+$ ]] || loi "$1: cần đúng một số outbox"
  echo "outbox_chua_gui|$1|$kq"
  [[ $kq = 0 ]] || ban=1
}
dem_outbox event_db event_schema.tbl_outbox_messages
dem_outbox booking_db booking_schema.tbl_outbox_messages
dem_outbox ticket_db ticket_schema.tbl_outbox_messages
dem_outbox payment_db payment_schema.tbl_outbox_messages

queues=$(docker exec flash-ticket-infra-rabbitmq-1 rabbitmqctl list_queues -q name messages messages_unacknowledged) || loi rabbitmqctl "$?"
n_queue=0
n_ban=0
while IFS= read -r dong; do
  [[ $dong =~ ^name[[:space:]]+messages[[:space:]]+messages_unacknowledged$ ]] && continue
  [[ $dong =~ ^([^[:space:]]+)[[:space:]]+([0-9]+)[[:space:]]+([0-9]+)$ ]] || loi 'RabbitMQ: dòng thiếu tên hoặc số'
  ten=${BASH_REMATCH[1]} msg=${BASH_REMATCH[2]} unacked=${BASH_REMATCH[3]}
  n_queue=$((n_queue + 1))
  if [[ $msg != 0 || $unacked != 0 ]]; then
    echo "queue|$ten|messages=$msg|unacked=$unacked"
    n_ban=$((n_ban + 1))
    ban=1
  fi
done <<< "$queues"
(( n_queue > 0 )) || loi 'RabbitMQ: thiếu số liệu hàng đợi'
echo "queue_so=$n_queue queue_khac_0=$n_ban"
echo "phut_khong_tai=${phut:-chua_xac_nhan}"
date -u '+== utc ket thuc %FT%T.%NZ'
if (( ban )) || [[ $phut =~ ^[0-9]$ ]]; then
  echo KHONG_YEN
  exit 1
fi
if [[ -z $phut ]]; then
  echo 'Người trực đối chiếu thời gian không tải (cần ≥ 10 phút).'
  exit 2
fi
echo YEN
