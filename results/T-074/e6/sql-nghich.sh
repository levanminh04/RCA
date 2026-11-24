# T-074 E6 — SQL NGHỊCH (hoàn tác; CHỈ chạy sau quyết định của Minh ở nhánh lỗi 50%/99%, nháp 4 §7)
# Nguyên tắc: với từng trường, chỉ đảo khi trường còn mang giá trị ĐÍCH; giữ nguyên nếu đang mang giá trị CŨ;
# gặp giá trị THỨ BA ở bất kỳ trường nào → RAISE, không đảo gì trong DB đó, dừng (giữ máy ở điều phối).
# JSON đảo từng đường dẫn, không thay cả tài liệu.
set -u
E=3e7c1df9-ada4-4081-94a1-548b80a5da86; TT=ffb36fc7-e30a-4efe-987f-ca5533520453
D=/home/ubuntu/t074/e6; mkdir -p $D
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -v ON_ERROR_STOP=1 -At; }
O_SALE='2026-12-02 22:16:31.402736+00'; N_SALE='2026-12-30 22:16:31.402736+00'
O_START='2026-12-03 22:16:31.402736+00'; N_START='2026-12-31 22:16:31.402736+00'
O_END='2026-12-04 22:16:31.402736+00';   N_END='2027-01-01 22:16:31.402736+00'
O_CAP=100000; N_CAP=96000
O_J_SALE=1796249791.402736000; N_J_SALE=1798668991.402736000
O_J_START=1796336191.402736000; N_J_START=1798755391.402736000
O_J_END=1796422591.402736000;   N_J_END=1798841791.402736000
echo "== utc bat dau $(date -u +%FT%T.%NZ)" | tee $D/nghich.log

P event_db >> $D/nghich.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='$E' FOR UPDATE;
SELECT 'TRUOC_NGHICH '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='$TT' FOR UPDATE;
DO \$\$ DECLARE r record; BEGIN
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='$E';
  IF r.sale_ends_at NOT IN ('$O_SALE','$N_SALE') OR r.starts_at NOT IN ('$O_START','$N_START') OR r.ends_at NOT IN ('$O_END','$N_END')
     THEN RAISE EXCEPTION 'event: gia tri thu ba'; END IF;
  -- ngày diễn và check-in đảo cùng nhau (ràng buộc checkin = starts/ends; sale_ends_at <= ends_at)
  UPDATE event_schema.tbl_events SET
     sale_ends_at = CASE WHEN sale_ends_at='$N_SALE' THEN '$O_SALE'::timestamptz ELSE sale_ends_at END,
     starts_at = CASE WHEN starts_at='$N_START' THEN '$O_START'::timestamptz ELSE starts_at END,
     checkin_starts_at = CASE WHEN starts_at='$N_START' THEN '$O_START'::timestamptz ELSE checkin_starts_at END,
     ends_at = CASE WHEN ends_at='$N_END' THEN '$O_END'::timestamptz ELSE ends_at END,
     checkin_ends_at = CASE WHEN ends_at='$N_END' THEN '$O_END'::timestamptz ELSE checkin_ends_at END
   WHERE id='$E';
  IF (SELECT configured_quantity FROM event_schema.tbl_ticket_types WHERE id='$TT') NOT IN ($O_CAP,$N_CAP) THEN RAISE EXCEPTION 'ticket_type: gia tri thu ba'; END IF;
  UPDATE event_schema.tbl_ticket_types SET configured_quantity=$O_CAP WHERE id='$TT' AND configured_quantity=$N_CAP;
END \$\$;
SELECT 'SAU_NGHICH '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='$E';
SELECT 'SAU_NGHICH '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='$TT';
COMMIT;
SQL
echo "event_rc=$?" | tee -a $D/nghich.log

P booking_db >> $D/nghich.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='$E' FOR UPDATE;
SELECT 'TRUOC_NGHICH '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='$TT' FOR UPDATE;
DO \$\$ DECLARE c jsonb; k int; s timestamptz; BEGIN
  SELECT configuration_snapshot, sale_ends_at INTO c, s FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='$E';
  SELECT (o-1)::int INTO k FROM jsonb_array_elements(c->'ticketTypes') WITH ORDINALITY x(v,o) WHERE v->>'ticketTypeId'='$TT';
  IF k IS NULL THEN RAISE EXCEPTION 'khong thay ticketTypeId'; END IF;
  IF s NOT IN ('$O_SALE','$N_SALE')
     OR (c->>'saleEndsAt')::numeric NOT IN ($O_J_SALE,$N_J_SALE)
     OR (c->>'eventStartsAt')::numeric NOT IN ($O_J_START,$N_J_START)
     OR (c->>'eventEndsAt')::numeric NOT IN ($O_J_END,$N_J_END)
     OR (c->'ticketTypes'->k->>'configuredQuantity') NOT IN ('$O_CAP','$N_CAP')
     THEN RAISE EXCEPTION 'sales_snapshot: gia tri thu ba'; END IF;
  IF (c->>'saleEndsAt')::numeric=$N_J_SALE THEN c := jsonb_set(c,'{saleEndsAt}','$O_J_SALE'::jsonb); END IF;
  IF (c->>'eventStartsAt')::numeric=$N_J_START THEN c := jsonb_set(c,'{eventStartsAt}','$O_J_START'::jsonb); END IF;
  IF (c->>'eventEndsAt')::numeric=$N_J_END THEN c := jsonb_set(c,'{eventEndsAt}','$O_J_END'::jsonb); END IF;
  IF (c->'ticketTypes'->k->>'configuredQuantity')='$N_CAP' THEN c := jsonb_set(c, ARRAY['ticketTypes',k::text,'configuredQuantity'], to_jsonb('$O_CAP'::text)); END IF;
  UPDATE booking_schema.tbl_event_sales_snapshots SET configuration_snapshot=c,
         sale_ends_at = CASE WHEN sale_ends_at='$N_SALE' THEN '$O_SALE'::timestamptz ELSE sale_ends_at END
   WHERE event_id='$E';
  IF (SELECT configured_capacity FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='$TT') NOT IN ($O_CAP,$N_CAP) THEN RAISE EXCEPTION 'inventory: gia tri thu ba'; END IF;
  UPDATE booking_schema.tbl_ticket_type_inventory SET configured_capacity=$O_CAP WHERE ticket_type_id='$TT' AND configured_capacity=$N_CAP;
END \$\$;
SELECT 'SAU_NGHICH '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='$E';
SELECT 'SAU_NGHICH '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='$TT';
COMMIT;
SQL
echo "booking_rc=$?" | tee -a $D/nghich.log

P ticket_db >> $D/nghich.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='$E' FOR UPDATE;
DO \$\$ BEGIN
  IF (SELECT count(*) FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='$E'
        AND event_starts_at IN ('$O_START','$N_START') AND event_ends_at IN ('$O_END','$N_END')) <> 1
     THEN RAISE EXCEPTION 'ticket: gia tri thu ba'; END IF;
  UPDATE ticket_schema.tbl_event_access_snapshots SET
     event_starts_at = CASE WHEN event_starts_at='$N_START' THEN '$O_START'::timestamptz ELSE event_starts_at END,
     event_ends_at = CASE WHEN event_ends_at='$N_END' THEN '$O_END'::timestamptz ELSE event_ends_at END
   WHERE event_id='$E';
END \$\$;
SELECT 'SAU_NGHICH '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='$E';
COMMIT;
SQL
echo "ticket_rc=$?" | tee -a $D/nghich.log

P payment_db >> $D/nghich.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='$E' FOR UPDATE;
DO \$\$ BEGIN
  IF (SELECT event_ends_at FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='$E') NOT IN ('$O_END','$N_END')
     THEN RAISE EXCEPTION 'payment: gia tri thu ba'; END IF;
  UPDATE payment_schema.tbl_event_finance_snapshots SET event_ends_at='$O_END' WHERE event_id='$E' AND event_ends_at='$N_END';
END \$\$;
SELECT 'SAU_NGHICH '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='$E';
COMMIT;
SQL
echo "payment_rc=$?" | tee -a $D/nghich.log
echo "== utc ket thuc $(date -u +%FT%T.%NZ)" | tee -a $D/nghich.log
# Ghi chú: mỗi DB độc lập; lỗi "giá trị thứ ba" ở một DB không chặn DB khác — người chạy xem rc từng DB và DỪNG trình Minh
# nếu có rc ≠ 0. Đảo sức chứa về 100.000 luôn thỏa purchased <= capacity.
