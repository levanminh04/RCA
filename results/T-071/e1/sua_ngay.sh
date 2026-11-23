set -u
E=3e7c1df9-ada4-4081-94a1-548b80a5da86
D=/home/ubuntu/t071/e1; mkdir -p $D
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -v ON_ERROR_STOP=1 -At; }
echo "== utc bat dau $(date -u +%FT%T.%NZ)"
# 1. Giá trị đích đọc từ Event; dừng nếu khác giá trị đã kiểm lúc 12:58:20Z
DICH=$(echo "select starts_at||'|'||ends_at from event_schema.tbl_events where id='$E'" | P event_db)
echo "dich=$DICH"
[ "$DICH" = "2026-12-03 22:16:31.402736+00|2026-12-04 22:16:31.402736+00" ] || { echo "DICH LECH, dung"; exit 3; }
BK=$(echo "select (configuration_snapshot->>'eventStartsAt')||'|'||(configuration_snapshot->>'eventEndsAt') from booking_schema.tbl_event_sales_snapshots where event_id='$E'" | P booking_db)
echo "booking_json=$BK"
[ "$BK" = "1796336191.402736000|1796422591.402736000" ] || { echo "BOOKING LECH, dung"; exit 3; }
# 2. ticket_db: một giao dịch, lưu cũ, sửa đúng 1 dòng khớp giá trị cũ
P ticket_db > $D/ticket.out 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC '||json_build_object('db','ticket_db','bang','ticket_schema.tbl_event_access_snapshots','utc',clock_timestamp(),'dong',row_to_json(s)) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='$E' FOR UPDATE;
DO \$\$ DECLARE n int; BEGIN
  UPDATE ticket_schema.tbl_event_access_snapshots
     SET event_starts_at='2026-12-03 22:16:31.402736+00', event_ends_at='2026-12-04 22:16:31.402736+00'
   WHERE event_id='$E' AND event_starts_at='2026-11-19 22:16:31.402736+00' AND event_ends_at='2026-11-20 22:16:31.402736+00';
  GET DIAGNOSTICS n = ROW_COUNT;
  IF n <> 1 THEN RAISE EXCEPTION 'ticket rows=%', n; END IF;
  RAISE NOTICE 'ticket rows=%', n;
END \$\$;
COMMIT;
SQL
echo "ticket_rc=$?"; cat $D/ticket.out
# 3. payment_db
P payment_db > $D/payment.out 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC '||json_build_object('db','payment_db','bang','payment_schema.tbl_event_finance_snapshots','utc',clock_timestamp(),'dong',row_to_json(s)) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='$E' FOR UPDATE;
DO \$\$ DECLARE n int; BEGIN
  UPDATE payment_schema.tbl_event_finance_snapshots
     SET event_ends_at='2026-12-04 22:16:31.402736+00'
   WHERE event_id='$E' AND event_ends_at='2026-11-20 22:16:31.402736+00';
  GET DIAGNOSTICS n = ROW_COUNT;
  IF n <> 1 THEN RAISE EXCEPTION 'payment rows=%', n; END IF;
  RAISE NOTICE 'payment rows=%', n;
END \$\$;
COMMIT;
SQL
echo "payment_rc=$?"; cat $D/payment.out
echo "== utc xong $(date -u +%FT%T.%NZ)"
