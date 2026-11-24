# T-074 E6 v2 — bước 1 bổ sung / điều kiện yên (CHỈ SELECT): đơn theo lifecycle_state, held, outbox chưa gửi 4 DB, hàng đợi.
set -u
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -X -At -v ON_ERROR_STOP=1 -d "$1"; }
echo "== utc $(date -u +%FT%T.%NZ)"
echo "== don theo lifecycle_state"; echo "select lifecycle_state||'='||count(*) from booking_schema.tbl_orders group by 1 order by 1" | P booking_db
echo "== held"; echo "select 'held='||held||' purchased='||purchased from booking_schema.tbl_ticket_type_inventory where ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453'" | P booking_db
for DB in event_db booking_db ticket_db payment_db; do
 echo "== outbox $DB (cot moc gui tim theo ten; liet ke cot de nguoi doc xac nhan)"
 P $DB <<'SQL'
select table_schema||'.'||table_name||': '||string_agg(column_name||':'||data_type, ', ' order by ordinal_position)
from information_schema.columns where table_name ~ 'outbox' group by table_schema, table_name;
DO $$ DECLARE t record; c text; n bigint; BEGIN
 FOR t IN SELECT table_schema s, table_name n FROM information_schema.tables WHERE table_name ~ 'outbox' LOOP
  SELECT column_name INTO c FROM information_schema.columns WHERE table_schema=t.s AND table_name=t.n
    AND column_name IN ('published_at','sent_at','dispatched_at','processed_at') ORDER BY column_name LIMIT 1;
  IF c IS NULL THEN RAISE NOTICE 'OUTBOX %.%: khong co cot moc gui -> CHUA KIEM DUOC', t.s, t.n;
  ELSE EXECUTE format('SELECT count(*) FROM %I.%I WHERE %I IS NULL', t.s, t.n, c) INTO n; RAISE NOTICE 'OUTBOX %.% chua_gui(% IS NULL)=%', t.s, t.n, c, n; END IF;
 END LOOP; END $$;
SQL
done
echo "== rabbit"; docker exec flash-ticket-infra-rabbitmq-1 rabbitmqctl list_queues -q name messages messages_unacknowledged | awk 'NR>1 && ($2!=0 || $3!=0)' ; echo "(het danh sach hang doi khac 0)"
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
