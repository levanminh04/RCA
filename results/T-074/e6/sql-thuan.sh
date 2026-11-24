# T-074 E6 — SQL THUẬN (pha ghi; CHƯA ĐƯỢC CHẠY, chờ hai phiên Codex kiểm và giao pha ghi)
# Chạy trên exp-app: bash sql-thuan.sh  (ghi nhật ký vào /home/ubuntu/t074/e6/)
# Mỗi DB một giao dịch. Trong giao dịch: khóa dòng → so MỌI giá trị đã khóa với số đọc ở bước 1
# (results/T-074/e6/b1-app.out, 23/11 18:04Z) → in TRUOC → UPDATE có điều kiện giá trị cũ → kiểm ROW_COUNT = 1 → in SAU → COMMIT.
# Khác số bước 1 → RAISE → rollback → dừng toàn bộ (set -e qua ON_ERROR_STOP và kiểm rc).
# Không đổi row_version / updated_at / source_config_version (xem ghi chú cuối file).
set -u
E=3e7c1df9-ada4-4081-94a1-548b80a5da86; TT=ffb36fc7-e30a-4efe-987f-ca5533520453
D=/home/ubuntu/t074/e6; mkdir -p $D
P() { docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -d "$1" -v ON_ERROR_STOP=1 -At; }
# Giá trị cũ (bước 1) và đích (gia-tri-dich.json)
O_SALE='2026-12-02 22:16:31.402736+00'; N_SALE='2026-12-30 22:16:31.402736+00'
O_START='2026-12-03 22:16:31.402736+00'; N_START='2026-12-31 22:16:31.402736+00'
O_END='2026-12-04 22:16:31.402736+00';   N_END='2027-01-01 22:16:31.402736+00'
O_CAP=100000; N_CAP=96000; PURCHASED=41705
O_J_SALE=1796249791.402736000; N_J_SALE=1798668991.402736000
O_J_START=1796336191.402736000; N_J_START=1798755391.402736000
O_J_END=1796422591.402736000;   N_J_END=1798841791.402736000
dung() { echo "DUNG: $1 (rc=$2) $(date -u +%FT%T.%NZ)"; exit 3; }
echo "== utc bat dau $(date -u +%FT%T.%NZ)" | tee $D/thuan.log

# ---------- 1. event_db: tbl_events (5 cột ngày cùng một UPDATE, thỏa checkin = starts/ends) + tbl_ticket_types ----------
P event_db >> $D/thuan.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC '||json_build_object('db','event_db','bang','tbl_events','utc',clock_timestamp(),'dong',row_to_json(e)) FROM event_schema.tbl_events e WHERE id='$E' FOR UPDATE;
SELECT 'TRUOC '||json_build_object('db','event_db','bang','tbl_ticket_types','utc',clock_timestamp(),'dong',row_to_json(t)) FROM event_schema.tbl_ticket_types t WHERE id='$TT' FOR UPDATE;
DO \$\$ DECLARE n int; BEGIN
  IF (SELECT count(*) FROM event_schema.tbl_events WHERE id='$E' AND sale_ends_at='$O_SALE' AND starts_at='$O_START' AND ends_at='$O_END'
        AND checkin_starts_at='$O_START' AND checkin_ends_at='$O_END' AND status='PUBLISHED') <> 1
     THEN RAISE EXCEPTION 'event: gia tri da khoa khac buoc 1'; END IF;
  IF (SELECT count(*) FROM event_schema.tbl_ticket_types WHERE id='$TT' AND event_id='$E' AND configured_quantity=$O_CAP) <> 1
     THEN RAISE EXCEPTION 'ticket_type: gia tri da khoa khac buoc 1'; END IF;
  UPDATE event_schema.tbl_events
     SET sale_ends_at='$N_SALE', starts_at='$N_START', ends_at='$N_END', checkin_starts_at='$N_START', checkin_ends_at='$N_END'
   WHERE id='$E' AND sale_ends_at='$O_SALE' AND starts_at='$O_START' AND ends_at='$O_END' AND checkin_starts_at='$O_START' AND checkin_ends_at='$O_END';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'tbl_events rows=%', n; END IF;
  UPDATE event_schema.tbl_ticket_types SET configured_quantity=$N_CAP WHERE id='$TT' AND event_id='$E' AND configured_quantity=$O_CAP;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'tbl_ticket_types rows=%', n; END IF;
END \$\$;
SELECT 'SAU '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='$E';
SELECT 'SAU '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='$TT';
COMMIT;
SQL
rc=$?; echo "event_rc=$rc" | tee -a $D/thuan.log; [ $rc -eq 0 ] || dung event_db $rc

# ---------- 2. booking_db: tbl_event_sales_snapshots (cột + 4 đường JSON) + tbl_ticket_type_inventory ----------
P booking_db >> $D/thuan.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC '||json_build_object('db','booking_db','bang','tbl_event_sales_snapshots','utc',clock_timestamp(),'dong',row_to_json(s)) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='$E' FOR UPDATE;
SELECT 'TRUOC '||json_build_object('db','booking_db','bang','tbl_ticket_type_inventory','utc',clock_timestamp(),'dong',row_to_json(i)) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='$TT' FOR UPDATE;
DO \$\$ DECLARE n int; k int; c jsonb; BEGIN
  SELECT configuration_snapshot INTO c FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='$E' AND sale_ends_at='$O_SALE';
  IF c IS NULL THEN RAISE EXCEPTION 'sales_snapshot: sale_ends_at khac buoc 1'; END IF;
  IF jsonb_typeof(c->'saleEndsAt')<>'number' OR (c->>'saleEndsAt')::numeric<>$O_J_SALE
     OR jsonb_typeof(c->'eventStartsAt')<>'number' OR (c->>'eventStartsAt')::numeric<>$O_J_START
     OR jsonb_typeof(c->'eventEndsAt')<>'number' OR (c->>'eventEndsAt')::numeric<>$O_J_END
     THEN RAISE EXCEPTION 'sales_snapshot JSON ngay khac buoc 1'; END IF;
  SELECT count(*) INTO n FROM jsonb_array_elements(c->'ticketTypes') x WHERE x->>'ticketTypeId'='$TT';
  IF n <> 1 THEN RAISE EXCEPTION 'ticketTypes khop ticketTypeId = %', n; END IF;
  SELECT (o-1)::int INTO k FROM jsonb_array_elements(c->'ticketTypes') WITH ORDINALITY x(v,o) WHERE v->>'ticketTypeId'='$TT';
  IF jsonb_typeof(c->'ticketTypes'->k->'configuredQuantity')<>'string' OR c->'ticketTypes'->k->>'configuredQuantity'<>'$O_CAP'
     THEN RAISE EXCEPTION 'configuredQuantity khac buoc 1'; END IF;
  IF (SELECT count(*) FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='$TT' AND event_id='$E'
        AND configured_capacity=$O_CAP AND held=0 AND purchased=$PURCHASED) <> 1
     THEN RAISE EXCEPTION 'inventory khac buoc 1 (capacity/held/purchased)'; END IF;
  UPDATE booking_schema.tbl_event_sales_snapshots
     SET sale_ends_at='$N_SALE',
         configuration_snapshot = jsonb_set(jsonb_set(jsonb_set(jsonb_set(configuration_snapshot,
              '{saleEndsAt}', '$N_J_SALE'::jsonb), '{eventStartsAt}', '$N_J_START'::jsonb), '{eventEndsAt}', '$N_J_END'::jsonb),
              ARRAY['ticketTypes', k::text, 'configuredQuantity'], to_jsonb('$N_CAP'::text))
   WHERE event_id='$E' AND sale_ends_at='$O_SALE' AND configuration_snapshot = c;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'sales_snapshot rows=%', n; END IF;
  UPDATE booking_schema.tbl_ticket_type_inventory SET configured_capacity=$N_CAP
   WHERE ticket_type_id='$TT' AND event_id='$E' AND configured_capacity=$O_CAP AND held=0 AND purchased=$PURCHASED;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'inventory rows=%', n; END IF;
END \$\$;
SELECT 'SAU '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='$E';
SELECT 'SAU '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='$TT';
COMMIT;
SQL
rc=$?; echo "booking_rc=$rc" | tee -a $D/thuan.log; [ $rc -eq 0 ] || dung booking_db $rc

# ---------- 3. ticket_db ----------
P ticket_db >> $D/thuan.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC '||json_build_object('db','ticket_db','bang','tbl_event_access_snapshots','utc',clock_timestamp(),'dong',row_to_json(s)) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='$E' FOR UPDATE;
DO \$\$ DECLARE n int; BEGIN
  UPDATE ticket_schema.tbl_event_access_snapshots SET event_starts_at='$N_START', event_ends_at='$N_END'
   WHERE event_id='$E' AND event_starts_at='$O_START' AND event_ends_at='$O_END';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'ticket rows=% (khac buoc 1?)', n; END IF;
END \$\$;
SELECT 'SAU '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='$E';
COMMIT;
SQL
rc=$?; echo "ticket_rc=$rc" | tee -a $D/thuan.log; [ $rc -eq 0 ] || dung ticket_db $rc

# ---------- 4. payment_db (payout phải vẫn 0) ----------
P payment_db >> $D/thuan.log 2>&1 <<SQL
BEGIN;
SELECT 'TRUOC '||json_build_object('db','payment_db','bang','tbl_event_finance_snapshots','utc',clock_timestamp(),'dong',row_to_json(s)) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='$E' FOR UPDATE;
DO \$\$ DECLARE n int; BEGIN
  IF (SELECT count(*) FROM payment_schema.tbl_event_payouts WHERE event_id='$E') <> 0 THEN RAISE EXCEPTION 'co payout, ngoai pham vi'; END IF;
  UPDATE payment_schema.tbl_event_finance_snapshots SET event_ends_at='$N_END'
   WHERE event_id='$E' AND event_ends_at='$O_END';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'payment rows=% (khac buoc 1?)', n; END IF;
END \$\$;
SELECT 'SAU '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='$E';
COMMIT;
SQL
rc=$?; echo "payment_rc=$rc" | tee -a $D/thuan.log; [ $rc -eq 0 ] || dung payment_db $rc
echo "== utc ket thuc $(date -u +%FT%T.%NZ)" | tee -a $D/thuan.log

# Ghi chú:
# - Thứ tự DB: event → booking → ticket → payment. Dừng ở DB lỗi; các DB trước đã COMMIT → xử lý theo nháp 4 §7 (50%).
# - Không đổi row_version/updated_at/source_config_version: giữ tối thiểu; rủi ro một ghi đè từ thực thể cũ trong bộ nhớ
#   service (không thấy trong code đã đọc, CHƯA-KIỂM) — người phản biện xét.
# - JSON số giữ 9 chữ số lẻ như giá trị gốc; JSON configuredQuantity giữ kiểu chuỗi.
# - Mất kết nối lúc COMMIT: xem nháp 4 §7 (đọc pg_stat_activity, đọc lại dưới khóa bằng kiem-sau-ghi.sh).
