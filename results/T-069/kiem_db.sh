#!/bin/bash
# T-069 bước 7 — kiểm DB chỉ đọc trên exp-app (chạy qua stdin SSH sau khi lượt thu xong, để không thêm tải giữa thực nghiệm).
# Số dòng và kích thước các bảng mà truy vấn nền quét; số dòng tạo trước mốc thu ca cũ (thu2 bắt đầu 13/11 07:14Z, thu bù 3 14/11 07:24Z)
# để ước lượng kích thước bảng lúc thu ca cũ (giả định không xóa dòng — ghi rõ là ước lượng); EXPLAIN (không ANALYZE) của truy vấn nền.
Q() { docker exec flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -At -F'|' -c "$2"; }
echo "== utc $(date -u +%FT%TZ)"
echo "== booking_db: số dòng, tạo trước 13/11 07:14Z, trước 14/11 07:24Z, kích thước"
for t in tbl_orders tbl_reservations tbl_order_items tbl_outbox_messages tbl_inbox_messages; do
  c=$(Q booking_db "select column_name from information_schema.columns where table_schema='booking_schema' and table_name='$t' and column_name in ('created_at','occurred_at','processed_at') order by column_name limit 1")
  Q booking_db "select '$t', count(*), count(*) filter (where $c < '2026-11-13 07:14+00'), count(*) filter (where $c < '2026-11-14 07:24+00'), pg_size_pretty(pg_total_relation_size('booking_schema.$t')) from booking_schema.$t"
done
Q booking_db "select 'orders theo trạng thái', lifecycle_state, count(*) from booking_schema.tbl_orders group by 2 order by 2"
echo "== ticket_db"
for t in tbl_ticket_deliveries tbl_issuances tbl_tickets; do
  c=$(Q ticket_db "select column_name from information_schema.columns where table_schema='ticket_schema' and table_name='$t' and column_name in ('created_at','requested_at','issued_at') order by column_name limit 1")
  if [ -n "$c" ]; then Q ticket_db "select '$t', count(*), count(*) filter (where $c < '2026-11-13 07:14+00'), count(*) filter (where $c < '2026-11-14 07:24+00'), pg_size_pretty(pg_total_relation_size('ticket_schema.$t')) from ticket_schema.$t";
  else Q ticket_db "select '$t', count(*), null, null, pg_size_pretty(pg_total_relation_size('ticket_schema.$t')) from ticket_schema.$t"; fi
done
echo "== event_db"
Q event_db "select 'tbl_outbox_messages', count(*), count(*) filter (where occurred_at < '2026-11-13 07:14+00'), count(*) filter (where occurred_at < '2026-11-14 07:24+00'), pg_size_pretty(pg_total_relation_size('event_schema.tbl_outbox_messages')) from event_schema.tbl_outbox_messages"
echo "== chỉ mục của tbl_orders, tbl_ticket_deliveries"
Q booking_db "select indexname, indexdef from pg_indexes where schemaname='booking_schema' and tablename in ('tbl_orders','tbl_reservations')"
Q ticket_db "select indexname, indexdef from pg_indexes where schemaname='ticket_schema' and tablename in ('tbl_ticket_deliveries','tbl_issuances')"
echo "== EXPLAIN (không chạy) truy vấn nền của worker hết hạn đơn"
Q booking_db "explain select o1_0.id from booking_schema.tbl_orders o1_0 where o1_0.lifecycle_state='PENDING_PAYMENT' and o1_0.expires_at<=now() order by o1_0.id limit 100"
echo "== pg_stat: lượt quét tuần tự/chỉ mục"
Q booking_db "select relname, seq_scan, seq_tup_read, idx_scan, n_live_tup from pg_stat_user_tables where schemaname='booking_schema' and relname in ('tbl_orders','tbl_reservations')"
Q ticket_db "select relname, seq_scan, seq_tup_read, idx_scan, n_live_tup from pg_stat_user_tables where schemaname='ticket_schema' and relname in ('tbl_ticket_deliveries','tbl_issuances','tbl_tickets')"
