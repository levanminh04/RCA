P="sudo -n docker exec flash-ticket-infra-postgres-1 psql -U postgres -X -At -F |"
O=$($P -d booking_db -c "begin read only; select id from booking_schema.tbl_orders where lifecycle_state='COMPLETED' and created_at >= '2026-11-25T03:21:25Z' and created_at < '2026-11-25T03:31:27Z' order by created_at limit 1; rollback;" | grep -E '^[0-9a-f-]{36}$')
echo "ORDER=$O"
$P -d booking_db -c "begin read only; select o.lifecycle_state, o.created_at, coalesce(sum(i.quantity),0), count(i.id), string_agg(i.id::text, ',') from booking_schema.tbl_orders o left join booking_schema.tbl_order_items i on i.order_id=o.id where o.id='$O' group by 1,2; rollback;" | grep -v -E '^(BEGIN|ROLLBACK)$'
ITEMS=$($P -d booking_db -c "begin read only; select string_agg(quote_literal(i.id::text), ',') from booking_schema.tbl_order_items i where i.order_id='$O'; rollback;" | grep -v -E '^(BEGIN|ROLLBACK)$')
echo "VE=$($P -d ticket_db -c "begin read only; select count(*) from ticket_schema.tbl_tickets where order_item_id::text in ($ITEMS); rollback;" | grep -v -E '^(BEGIN|ROLLBACK)$')"
echo "ISSUANCE=$($P -d ticket_db -c "begin read only; select count(*) from ticket_schema.tbl_issuances where order_id::text='$O'; rollback;" | grep -v -E '^(BEGIN|ROLLBACK)$')"
echo "== tong trong cua so"
$P -d booking_db -c "begin read only; select lifecycle_state, count(*) from booking_schema.tbl_orders where created_at >= '2026-11-25T03:21:25Z' and created_at < '2026-11-25T03:31:27Z' group by 1 order by 1; rollback;" | grep -v -E '^(BEGIN|ROLLBACK)$'
