# T-074 E6 bước 1 bổ sung — exp-app — CHỈ SELECT
set -u
E=3e7c1df9-ada4-4081-94a1-548b80a5da86
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -v ON_ERROR_STOP=1 -At; }
echo "== utc $(date -u +%FT%T.%NZ)"
echo "== sectors event_db"; echo "select count(*) from event_schema.tbl_event_sectors where event_id='$E'" | P event_db
echo "== sector_inventory booking"; echo "select count(*) from booking_schema.tbl_sector_inventory where event_id='$E'" | P booking_db
echo "== promotions"; echo "select count(*) from event_schema.tbl_promotions where event_id='$E'" | P event_db; echo "select count(*) from booking_schema.tbl_promotion_inventory where event_id='$E'" | P booking_db
echo "== rang buoc tbl_events"; echo "select conname||': '||pg_get_constraintdef(oid) from pg_constraint where conrelid='event_schema.tbl_events'::regclass and contype='c'" | P event_db
echo "== rang buoc tbl_ticket_types"; echo "select conname||': '||pg_get_constraintdef(oid) from pg_constraint where conrelid='event_schema.tbl_ticket_types'::regclass and contype='c'" | P event_db
echo "== rang buoc inventory"; echo "select conname||': '||pg_get_constraintdef(oid) from pg_constraint where conrelid='booking_schema.tbl_ticket_type_inventory'::regclass and contype='c'" | P booking_db
echo "== rang buoc sales_snapshot"; echo "select conname||': '||pg_get_constraintdef(oid) from pg_constraint where conrelid='booking_schema.tbl_event_sales_snapshots'::regclass and contype='c'" | P booking_db
echo "== trigger"; for D in event_db booking_db ticket_db payment_db; do echo "-- $D"; echo "select tgrelid::regclass||': '||tgname from pg_trigger where not tgisinternal" | P $D; done
echo "== cot trang thai don"; echo "select column_name from information_schema.columns where table_schema='booking_schema' and table_name='tbl_orders' and column_name ~ '(status|state)'" | P booking_db
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
