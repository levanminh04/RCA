# T-074 E6 bước 1 — exp-app — CHỈ SELECT
set -u
E=3e7c1df9-ada4-4081-94a1-548b80a5da86; TT=ffb36fc7-e30a-4efe-987f-ca5533520453
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -v ON_ERROR_STOP=1 -At; }
echo "== utc $(date -u +%FT%T.%NZ)"
for DB in event_db booking_db ticket_db payment_db; do
 echo "== COT ($DB): bảng có event_id hoặc ticket_type_id; cột ngày/sức chứa/json"
 P $DB <<SQL
select c.table_schema||'.'||c.table_name||'.'||c.column_name||'|'||c.data_type
from information_schema.columns c
where c.table_schema not in ('pg_catalog','information_schema')
  and exists (select 1 from information_schema.columns k where k.table_schema=c.table_schema and k.table_name=c.table_name and k.column_name in ('event_id','ticket_type_id','id'))
  and (c.column_name ~ '(sale|start|end|checkin|check_in).*_at$' or c.column_name ~ '(capacity|quantity)' or c.data_type in ('json','jsonb'))
order by 1;
SQL
done
echo "== EVENT tbl_events"; echo "select row_to_json(e) from event_schema.tbl_events e where id='$E'" | P event_db
echo "== EVENT tbl_ticket_types"; echo "select row_to_json(t) from event_schema.tbl_ticket_types t where event_id='$E'" | P event_db
echo "== BOOKING sales_snapshot"; echo "select row_to_json(s) from booking_schema.tbl_event_sales_snapshots s where event_id='$E'" | P booking_db
echo "== BOOKING json kieu"; echo "select jsonb_typeof(configuration_snapshot->'saleEndsAt')||'|'||jsonb_typeof(configuration_snapshot->'eventStartsAt')||'|'||jsonb_typeof(configuration_snapshot->'eventEndsAt')||'|'||(select string_agg(x->>'ticketTypeId'||':'||jsonb_typeof(x->'configuredQuantity')||':'||(x->>'configuredQuantity'),',') from jsonb_array_elements(configuration_snapshot->'ticketTypes') x)||'|'||pg_typeof(configuration_snapshot)::text from booking_schema.tbl_event_sales_snapshots where event_id='$E'" | P booking_db
echo "== BOOKING inventory"; echo "select row_to_json(i) from booking_schema.tbl_ticket_type_inventory i where ticket_type_id='$TT'" | P booking_db
echo "== TICKET access_snapshot"; echo "select row_to_json(s) from ticket_schema.tbl_event_access_snapshots s where event_id='$E'" | P ticket_db
echo "== PAYMENT finance_snapshot"; echo "select row_to_json(s) from payment_schema.tbl_event_finance_snapshots s where event_id='$E'" | P payment_db
echo "== PAYMENT payouts dem"; echo "select count(*) from payment_schema.tbl_event_payouts where event_id='$E'" | P payment_db
echo "== BOOKING don theo trang thai"; echo "select status||'='||count(*) from booking_schema.tbl_orders group by status order by 1" | P booking_db
echo "== utc ket thuc $(date -u +%FT%T.%NZ)"
