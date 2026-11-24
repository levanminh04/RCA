# T-074 E6 — KIỂM SAU GHI (chỉ SELECT; chạy sau sql-thuan.sh, và dùng để đọc lại khi mất kết nối)
# In TRANG_THAI từng trường: CU / DICH / KHAC (giá trị thứ ba), kèm kiểu JSON. Đạt khi mọi trường = DICH và kiểu đúng.
set -u
E=3e7c1df9-ada4-4081-94a1-548b80a5da86; TT=ffb36fc7-e30a-4efe-987f-ca5533520453
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -v ON_ERROR_STOP=1 -At; }
O_SALE='2026-12-02 22:16:31.402736+00'; N_SALE='2026-12-30 22:16:31.402736+00'
O_START='2026-12-03 22:16:31.402736+00'; N_START='2026-12-31 22:16:31.402736+00'
O_END='2026-12-04 22:16:31.402736+00';   N_END='2027-01-01 22:16:31.402736+00'
O_CAP=100000; N_CAP=96000
O_J_SALE=1796249791.402736000; N_J_SALE=1798668991.402736000
O_J_START=1796336191.402736000; N_J_START=1798755391.402736000
O_J_END=1796422591.402736000;   N_J_END=1798841791.402736000
echo "== utc $(date -u +%FT%T.%NZ)"
echo "== phien dang mo (tim giao dich cu khi mat ket noi)"; echo "select pid||'|'||datname||'|'||state||'|'||coalesce(xact_start::text,'')||'|'||left(query,60) from pg_stat_activity where datname in ('event_db','booking_db','ticket_db','payment_db') and pid<>pg_backend_pid()" | P postgres
P event_db <<SQL
SELECT 'event.'||k||'='||CASE WHEN v=o THEN 'CU' WHEN v=n THEN 'DICH' ELSE 'KHAC:'||v END FROM (
  SELECT 'sale_ends_at' k, sale_ends_at::text v, '$O_SALE'::timestamptz::text o, '$N_SALE'::timestamptz::text n FROM event_schema.tbl_events WHERE id='$E'
  UNION ALL SELECT 'starts_at', starts_at::text, '$O_START'::timestamptz::text, '$N_START'::timestamptz::text FROM event_schema.tbl_events WHERE id='$E'
  UNION ALL SELECT 'checkin_starts_at', checkin_starts_at::text, '$O_START'::timestamptz::text, '$N_START'::timestamptz::text FROM event_schema.tbl_events WHERE id='$E'
  UNION ALL SELECT 'ends_at', ends_at::text, '$O_END'::timestamptz::text, '$N_END'::timestamptz::text FROM event_schema.tbl_events WHERE id='$E'
  UNION ALL SELECT 'checkin_ends_at', checkin_ends_at::text, '$O_END'::timestamptz::text, '$N_END'::timestamptz::text FROM event_schema.tbl_events WHERE id='$E'
  UNION ALL SELECT 'ticket_type.configured_quantity', configured_quantity::text, '$O_CAP', '$N_CAP' FROM event_schema.tbl_ticket_types WHERE id='$TT') x;
SQL
P booking_db <<SQL
WITH s AS (SELECT sale_ends_at, configuration_snapshot c FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='$E'),
     t AS (SELECT x AS v FROM s, jsonb_array_elements(s.c->'ticketTypes') x WHERE x->>'ticketTypeId'='$TT')
SELECT 'booking.'||k||'='||CASE WHEN v=o THEN 'CU' WHEN v=n THEN 'DICH' ELSE 'KHAC:'||v END||' kieu='||coalesce(ty,'-') FROM (
  SELECT 'sale_ends_at' k, sale_ends_at::text v, '$O_SALE'::timestamptz::text o, '$N_SALE'::timestamptz::text n, NULL ty FROM s
  UNION ALL SELECT 'json.saleEndsAt', (c->>'saleEndsAt')::numeric::text, ($O_J_SALE)::text, ($N_J_SALE)::text, jsonb_typeof(c->'saleEndsAt') FROM s
  UNION ALL SELECT 'json.eventStartsAt', (c->>'eventStartsAt')::numeric::text, ($O_J_START)::text, ($N_J_START)::text, jsonb_typeof(c->'eventStartsAt') FROM s
  UNION ALL SELECT 'json.eventEndsAt', (c->>'eventEndsAt')::numeric::text, ($O_J_END)::text, ($N_J_END)::text, jsonb_typeof(c->'eventEndsAt') FROM s
  UNION ALL SELECT 'json.ticketTypes.configuredQuantity', v->>'configuredQuantity', '$O_CAP', '$N_CAP', jsonb_typeof(v->'configuredQuantity') FROM t
  UNION ALL SELECT 'inventory.configured_capacity', configured_capacity::text, '$O_CAP', '$N_CAP', NULL FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='$TT') x;
SELECT 'booking.json.ticketTypes_khop='||count(*) FROM booking_schema.tbl_event_sales_snapshots s, jsonb_array_elements(s.configuration_snapshot->'ticketTypes') x WHERE s.event_id='$E' AND x->>'ticketTypeId'='$TT';
SELECT 'booking.inventory held='||held||' purchased='||purchased FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='$TT';
SQL
P ticket_db <<SQL
SELECT 'ticket.event_starts_at='||CASE WHEN event_starts_at='$O_START' THEN 'CU' WHEN event_starts_at='$N_START' THEN 'DICH' ELSE 'KHAC:'||event_starts_at END
    ||' ticket.event_ends_at='||CASE WHEN event_ends_at='$O_END' THEN 'CU' WHEN event_ends_at='$N_END' THEN 'DICH' ELSE 'KHAC:'||event_ends_at END
FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='$E';
SQL
P payment_db <<SQL
SELECT 'payment.event_ends_at='||CASE WHEN event_ends_at='$O_END' THEN 'CU' WHEN event_ends_at='$N_END' THEN 'DICH' ELSE 'KHAC:'||event_ends_at END FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='$E';
SELECT 'payment.payouts='||count(*) FROM payment_schema.tbl_event_payouts WHERE event_id='$E';
SQL
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
# Đạt: 6 dòng event = DICH; 6 dòng booking = DICH với kiểu number ×3, string ×1; ticketTypes_khop=1; ticket 2 DICH; payment DICH, payouts=0.
