# T-074 E6 v2 — sinh SQL tĩnh cho hai biến thể sức chứa: A (96.000, đúng A3), B (giữ 100.000, không ghi sức chứa).
# Chạy: py -3 -I tao_sql.py   (ghi vào sql/A, sql/B cạnh file này). Không kết nối DB.
# Nguồn số: ../b1-app.out, ../b1b-app.out (exp-app 2026-11-23T18:04Z).
from pathlib import Path

E = '3e7c1df9-ada4-4081-94a1-548b80a5da86'
TT = 'ffb36fc7-e30a-4efe-987f-ca5533520453'
O = {'sale': '2026-12-02 22:16:31.402736+00', 'start': '2026-12-03 22:16:31.402736+00', 'end': '2026-12-04 22:16:31.402736+00'}
N = {'sale': '2026-12-30 22:16:31.402736+00', 'start': '2026-12-31 22:16:31.402736+00', 'end': '2027-01-01 22:16:31.402736+00'}
OJ = {'saleEndsAt': '1796249791.402736000', 'eventStartsAt': '1796336191.402736000', 'eventEndsAt': '1796422591.402736000'}
NJ = {'saleEndsAt': '1798668991.402736000', 'eventStartsAt': '1798755391.402736000', 'eventEndsAt': '1798841791.402736000'}
O_CAP, PURCHASED = 100000, 41705
N_CAP = {'A': 96000, 'B': 100000}
HERE = Path(__file__).resolve().parent


def ts(x): return f"'{x}'::timestamptz"
def js(x): return f"'{x}'::jsonb"
def qty(n): return f"'\"{n}\"'::jsonb"           # configuredQuantity là CHUỖI JSON


DAU = """\\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
"""
CUOI = """COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
"""


def ngay_trong(col, a, b):  # col thuộc {a, b} (NULL không thuộc)
    return f"({col} IS NOT DISTINCT FROM {a} OR {col} IS NOT DISTINCT FROM {b})"


# ------------------------------------------------------------------ THUẬN
def event_thuan(bt):
    cap = N_CAP[bt]
    s = DAU + f"""SELECT 'TRUOC '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='{E}' FOR UPDATE;
SELECT 'TRUOC '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='{TT}' FOR UPDATE;
DO $$ DECLARE n int; r record; q bigint; BEGIN
  SELECT count(*) INTO n FROM event_schema.tbl_events WHERE id='{E}';
  IF n <> 1 THEN RAISE EXCEPTION 'tbl_events so dong=%', n; END IF;
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='{E}';
  IF r.status IS DISTINCT FROM 'PUBLISHED' OR r.source_config_version IS DISTINCT FROM 4 OR r.row_version IS DISTINCT FROM 3
     OR r.sale_ends_at IS DISTINCT FROM {ts(O['sale'])} OR r.starts_at IS DISTINCT FROM {ts(O['start'])} OR r.ends_at IS DISTINCT FROM {ts(O['end'])}
     OR r.checkin_starts_at IS DISTINCT FROM {ts(O['start'])} OR r.checkin_ends_at IS DISTINCT FROM {ts(O['end'])}
  THEN RAISE EXCEPTION 'tbl_events: gia tri da khoa khac buoc 1'; END IF;
  SELECT count(*) INTO n FROM event_schema.tbl_ticket_types WHERE id='{TT}' AND event_id='{E}';
  IF n <> 1 THEN RAISE EXCEPTION 'tbl_ticket_types so dong=%', n; END IF;
  SELECT configured_quantity INTO q FROM event_schema.tbl_ticket_types WHERE id='{TT}';
  IF q IS DISTINCT FROM {O_CAP} THEN RAISE EXCEPTION 'configured_quantity khac buoc 1: %', q; END IF;
  UPDATE event_schema.tbl_events
     SET sale_ends_at={ts(N['sale'])}, starts_at={ts(N['start'])}, ends_at={ts(N['end'])},
         checkin_starts_at={ts(N['start'])}, checkin_ends_at={ts(N['end'])}
   WHERE id='{E}' AND sale_ends_at={ts(O['sale'])} AND starts_at={ts(O['start'])} AND ends_at={ts(O['end'])};
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE tbl_events rows=%', n; END IF;
"""
    if bt == 'A':
        s += f"""  UPDATE event_schema.tbl_ticket_types SET configured_quantity={cap}
   WHERE id='{TT}' AND event_id='{E}' AND configured_quantity={O_CAP};
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE tbl_ticket_types rows=%', n; END IF;
"""
    s += f"""  -- hau kiem trong giao dich
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='{E}';
  IF r.sale_ends_at IS DISTINCT FROM {ts(N['sale'])} OR r.starts_at IS DISTINCT FROM {ts(N['start'])} OR r.ends_at IS DISTINCT FROM {ts(N['end'])}
     OR r.checkin_starts_at IS DISTINCT FROM {ts(N['start'])} OR r.checkin_ends_at IS DISTINCT FROM {ts(N['end'])}
  THEN RAISE EXCEPTION 'hau kiem tbl_events khong dat'; END IF;
  SELECT configured_quantity INTO q FROM event_schema.tbl_ticket_types WHERE id='{TT}';
  IF q IS DISTINCT FROM {cap} THEN RAISE EXCEPTION 'hau kiem configured_quantity khong dat: %', q; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='{E}';
SELECT 'SAU_TRONG_GD '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='{TT}';
""" + CUOI
    return s


def booking_thuan(bt):
    cap = N_CAP[bt]
    chain = "c"
    for k in ('saleEndsAt', 'eventStartsAt', 'eventEndsAt'):
        chain = f"jsonb_set({chain}, '{{{k}}}', {js(NJ[k])}, false)"
    s = DAU + f"""SELECT 'TRUOC '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='{E}' FOR UPDATE;
SELECT 'TRUOC '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='{TT}' FOR UPDATE;
DO $$ DECLARE n int; k int; c jsonb; c2 jsonb; c3 jsonb; r record; ri record; BEGIN
  SELECT count(*) INTO n FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}';
  IF n <> 1 THEN RAISE EXCEPTION 'sales_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}';
  c := r.configuration_snapshot;
  IF r.event_status IS DISTINCT FROM 'PUBLISHED' OR r.source_config_version IS DISTINCT FROM 4 OR r.row_version IS DISTINCT FROM 0
     OR r.sale_ends_at IS DISTINCT FROM {ts(O['sale'])}
  THEN RAISE EXCEPTION 'sales_snapshot: cot khac buoc 1'; END IF;
  -- nhan dien va phien ban trong JSON (so dung kieu JSONB)
  IF c->'eventId' IS DISTINCT FROM to_jsonb('{E}'::text) OR c->'schemaVersion' IS DISTINCT FROM '1'::jsonb
     OR c->'sourceConfigVersion' IS DISTINCT FROM '"4"'::jsonb OR jsonb_typeof(c->'ticketTypes') IS DISTINCT FROM 'array'
  THEN RAISE EXCEPTION 'sales_snapshot: nhan dien/phien ban JSON khac'; END IF;
  IF c->'saleEndsAt' IS DISTINCT FROM {js(OJ['saleEndsAt'])} OR c->'eventStartsAt' IS DISTINCT FROM {js(OJ['eventStartsAt'])}
     OR c->'eventEndsAt' IS DISTINCT FROM {js(OJ['eventEndsAt'])}
  THEN RAISE EXCEPTION 'sales_snapshot: ngay JSON khac buoc 1 (thieu khoa hoac sai kieu)'; END IF;
  SELECT count(*) INTO n FROM jsonb_array_elements(c->'ticketTypes') x WHERE x->'ticketTypeId' = to_jsonb('{TT}'::text);
  IF n <> 1 THEN RAISE EXCEPTION 'ticketTypes khop ticketTypeId=%', n; END IF;
  SELECT (o-1)::int INTO k FROM jsonb_array_elements(c->'ticketTypes') WITH ORDINALITY x(v,o) WHERE v->'ticketTypeId' = to_jsonb('{TT}'::text);
  IF c->'ticketTypes'->k->'configuredQuantity' IS DISTINCT FROM {qty(O_CAP)} THEN RAISE EXCEPTION 'configuredQuantity khac buoc 1'; END IF;
  SELECT count(*) INTO n FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}';
  IF n <> 1 THEN RAISE EXCEPTION 'inventory so dong=%', n; END IF;
  SELECT * INTO ri FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}';
  IF ri.event_id::text IS DISTINCT FROM '{E}' OR ri.configured_capacity IS DISTINCT FROM {O_CAP} OR ri.held IS DISTINCT FROM 0 OR ri.purchased IS DISTINCT FROM {PURCHASED}
  THEN RAISE EXCEPTION 'inventory khac buoc 1'; END IF;
  c2 := {chain};
"""
    if bt == 'A':
        s += f"""  c2 := jsonb_set(c2, ARRAY['ticketTypes', k::text, 'configuredQuantity'], {qty(cap)}, false);
"""
    s += f"""  UPDATE booking_schema.tbl_event_sales_snapshots SET sale_ends_at={ts(N['sale'])}, configuration_snapshot=c2
   WHERE event_id='{E}' AND sale_ends_at={ts(O['sale'])} AND configuration_snapshot = c;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE sales_snapshot rows=%', n; END IF;
"""
    if bt == 'A':
        s += f"""  UPDATE booking_schema.tbl_ticket_type_inventory SET configured_capacity={cap}
   WHERE ticket_type_id='{TT}' AND event_id='{E}' AND configured_capacity={O_CAP} AND held=0 AND purchased={PURCHASED};
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE inventory rows=%', n; END IF;
"""
    s += f"""  -- hau kiem trong giao dich: dung gia tri, dung kieu, khong them/bot khoa
  SELECT configuration_snapshot INTO c3 FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}';
  IF c3->'saleEndsAt' IS DISTINCT FROM {js(NJ['saleEndsAt'])} OR c3->'eventStartsAt' IS DISTINCT FROM {js(NJ['eventStartsAt'])}
     OR c3->'eventEndsAt' IS DISTINCT FROM {js(NJ['eventEndsAt'])}
     OR c3->'ticketTypes'->k->'configuredQuantity' IS DISTINCT FROM {qty(cap)}
     OR c3->'ticketTypes'->k->'ticketTypeId' IS DISTINCT FROM to_jsonb('{TT}'::text)
     OR (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c3) x) IS DISTINCT FROM (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c) x)
     OR jsonb_array_length(c3->'ticketTypes') IS DISTINCT FROM jsonb_array_length(c->'ticketTypes')
  THEN RAISE EXCEPTION 'hau kiem sales_snapshot khong dat'; END IF;
  IF (SELECT sale_ends_at FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}') IS DISTINCT FROM {ts(N['sale'])}
  THEN RAISE EXCEPTION 'hau kiem sale_ends_at khong dat'; END IF;
  IF (SELECT configured_capacity FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}') IS DISTINCT FROM {cap}
  THEN RAISE EXCEPTION 'hau kiem inventory khong dat'; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='{E}';
SELECT 'SAU_TRONG_GD '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='{TT}';
""" + CUOI
    return s


def ticket_thuan(bt):
    return DAU + f"""SELECT 'TRUOC '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='{E}' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}';
  IF n <> 1 THEN RAISE EXCEPTION 'access_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}';
  IF r.event_status IS DISTINCT FROM 'PUBLISHED' OR r.source_config_version IS DISTINCT FROM 4
     OR r.event_starts_at IS DISTINCT FROM {ts(O['start'])} OR r.event_ends_at IS DISTINCT FROM {ts(O['end'])}
  THEN RAISE EXCEPTION 'access_snapshot khac buoc 1'; END IF;
  UPDATE ticket_schema.tbl_event_access_snapshots SET event_starts_at={ts(N['start'])}, event_ends_at={ts(N['end'])}
   WHERE event_id='{E}' AND event_starts_at={ts(O['start'])} AND event_ends_at={ts(O['end'])};
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE access_snapshot rows=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}';
  IF r.event_starts_at IS DISTINCT FROM {ts(N['start'])} OR r.event_ends_at IS DISTINCT FROM {ts(N['end'])}
  THEN RAISE EXCEPTION 'hau kiem access_snapshot khong dat'; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='{E}';
""" + CUOI


def payment_thuan(bt):
    return DAU + f"""SELECT 'TRUOC '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='{E}' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}';
  IF n <> 1 THEN RAISE EXCEPTION 'finance_snapshot so dong=%', n; END IF;
  SELECT count(*) INTO n FROM payment_schema.tbl_event_payouts WHERE event_id='{E}';
  IF n <> 0 THEN RAISE EXCEPTION 'co payout (%), ngoai pham vi', n; END IF;
  SELECT * INTO r FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}';
  IF r.event_ends_at IS DISTINCT FROM {ts(O['end'])} OR r.cancelled_at IS NOT NULL OR r.source_fee_version IS DISTINCT FROM 3
  THEN RAISE EXCEPTION 'finance_snapshot khac buoc 1'; END IF;
  UPDATE payment_schema.tbl_event_finance_snapshots SET event_ends_at={ts(N['end'])}
   WHERE event_id='{E}' AND event_ends_at={ts(O['end'])};
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE finance_snapshot rows=%', n; END IF;
  IF (SELECT event_ends_at FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}') IS DISTINCT FROM {ts(N['end'])}
  THEN RAISE EXCEPTION 'hau kiem finance_snapshot khong dat'; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='{E}';
""" + CUOI


# ------------------------------------------------------------------ NGHỊCH
def event_nghich(bt):
    caps = f"{O_CAP}, {N_CAP['A']}" if bt == 'A' else f"{O_CAP}"
    s = DAU + f"""SELECT 'TRUOC_NGHICH '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='{E}' FOR UPDATE;
SELECT 'TRUOC_NGHICH '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='{TT}' FOR UPDATE;
DO $$ DECLARE n int; r record; q bigint; BEGIN
  SELECT count(*) INTO n FROM event_schema.tbl_events WHERE id='{E}'; IF n <> 1 THEN RAISE EXCEPTION 'tbl_events so dong=%', n; END IF;
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='{E}';
  IF NOT ({ngay_trong('r.sale_ends_at', ts(O['sale']), ts(N['sale']))} AND {ngay_trong('r.starts_at', ts(O['start']), ts(N['start']))}
          AND {ngay_trong('r.ends_at', ts(O['end']), ts(N['end']))}) OR r.status IS DISTINCT FROM 'PUBLISHED'
  THEN RAISE EXCEPTION 'tbl_events: gia tri thu ba/thieu'; END IF;
  SELECT count(*) INTO n FROM event_schema.tbl_ticket_types WHERE id='{TT}' AND event_id='{E}'; IF n <> 1 THEN RAISE EXCEPTION 'tbl_ticket_types so dong=%', n; END IF;
  SELECT configured_quantity INTO q FROM event_schema.tbl_ticket_types WHERE id='{TT}';
  IF q IS NULL OR q NOT IN ({caps}) THEN RAISE EXCEPTION 'configured_quantity gia tri thu ba: %', q; END IF;
  UPDATE event_schema.tbl_events SET
     sale_ends_at = CASE WHEN sale_ends_at = {ts(N['sale'])} THEN {ts(O['sale'])} ELSE sale_ends_at END,
     starts_at = CASE WHEN starts_at = {ts(N['start'])} THEN {ts(O['start'])} ELSE starts_at END,
     checkin_starts_at = CASE WHEN starts_at = {ts(N['start'])} THEN {ts(O['start'])} ELSE checkin_starts_at END,
     ends_at = CASE WHEN ends_at = {ts(N['end'])} THEN {ts(O['end'])} ELSE ends_at END,
     checkin_ends_at = CASE WHEN ends_at = {ts(N['end'])} THEN {ts(O['end'])} ELSE checkin_ends_at END
   WHERE id='{E}';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE tbl_events rows=%', n; END IF;
"""
    if bt == 'A':
        s += f"""  UPDATE event_schema.tbl_ticket_types SET configured_quantity={O_CAP} WHERE id='{TT}' AND configured_quantity={N_CAP['A']};
"""
    s += f"""  SELECT * INTO r FROM event_schema.tbl_events WHERE id='{E}';
  IF r.sale_ends_at IS DISTINCT FROM {ts(O['sale'])} OR r.starts_at IS DISTINCT FROM {ts(O['start'])} OR r.ends_at IS DISTINCT FROM {ts(O['end'])}
     OR (SELECT configured_quantity FROM event_schema.tbl_ticket_types WHERE id='{TT}') IS DISTINCT FROM {O_CAP}
  THEN RAISE EXCEPTION 'hau kiem nghich event khong dat'; END IF;
END $$;
SELECT 'SAU_NGHICH_TRONG_GD '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='{E}';
""" + CUOI
    return s


def booking_nghich(bt):
    qs = f"{qty(O_CAP)}, {qty(N_CAP['A'])}" if bt == 'A' else qty(O_CAP)
    caps = f"{O_CAP}, {N_CAP['A']}" if bt == 'A' else f"{O_CAP}"
    s = DAU + f"""SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='{E}' FOR UPDATE;
SELECT 'TRUOC_NGHICH '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='{TT}' FOR UPDATE;
DO $$ DECLARE n int; k int; c jsonb; c2 jsonb; c3 jsonb; r record; cap bigint; BEGIN
  SELECT count(*) INTO n FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}'; IF n <> 1 THEN RAISE EXCEPTION 'sales_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}';
  c := r.configuration_snapshot;
  IF c->'eventId' IS DISTINCT FROM to_jsonb('{E}'::text) OR c->'schemaVersion' IS DISTINCT FROM '1'::jsonb OR jsonb_typeof(c->'ticketTypes') IS DISTINCT FROM 'array'
  THEN RAISE EXCEPTION 'nhan dien JSON khac'; END IF;
  IF NOT ({ngay_trong('r.sale_ends_at', ts(O['sale']), ts(N['sale']))}
          AND {ngay_trong("c->'saleEndsAt'", js(OJ['saleEndsAt']), js(NJ['saleEndsAt']))}
          AND {ngay_trong("c->'eventStartsAt'", js(OJ['eventStartsAt']), js(NJ['eventStartsAt']))}
          AND {ngay_trong("c->'eventEndsAt'", js(OJ['eventEndsAt']), js(NJ['eventEndsAt']))})
  THEN RAISE EXCEPTION 'sales_snapshot: gia tri thu ba/thieu/sai kieu'; END IF;
  SELECT count(*) INTO n FROM jsonb_array_elements(c->'ticketTypes') x WHERE x->'ticketTypeId' = to_jsonb('{TT}'::text);
  IF n <> 1 THEN RAISE EXCEPTION 'ticketTypes khop ticketTypeId=%', n; END IF;
  SELECT (o-1)::int INTO k FROM jsonb_array_elements(c->'ticketTypes') WITH ORDINALITY x(v,o) WHERE v->'ticketTypeId' = to_jsonb('{TT}'::text);
  IF c->'ticketTypes'->k->'configuredQuantity' IS NULL OR NOT (c->'ticketTypes'->k->'configuredQuantity' = ANY (ARRAY[{qs}]))
  THEN RAISE EXCEPTION 'configuredQuantity gia tri thu ba/sai kieu'; END IF;
  SELECT count(*) INTO n FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}'; IF n <> 1 THEN RAISE EXCEPTION 'inventory so dong=%', n; END IF;
  SELECT configured_capacity INTO cap FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}';
  IF cap IS NULL OR cap NOT IN ({caps}) THEN RAISE EXCEPTION 'inventory gia tri thu ba: %', cap; END IF;
  c2 := c;
"""
    for key in ('saleEndsAt', 'eventStartsAt', 'eventEndsAt'):
        s += f"""  IF c2->'{key}' = {js(NJ[key])} THEN c2 := jsonb_set(c2, '{{{key}}}', {js(OJ[key])}, false); END IF;
"""
    if bt == 'A':
        s += f"""  IF c2->'ticketTypes'->k->'configuredQuantity' = {qty(N_CAP['A'])} THEN
     c2 := jsonb_set(c2, ARRAY['ticketTypes', k::text, 'configuredQuantity'], {qty(O_CAP)}, false); END IF;
"""
    s += f"""  UPDATE booking_schema.tbl_event_sales_snapshots SET configuration_snapshot=c2,
         sale_ends_at = CASE WHEN sale_ends_at = {ts(N['sale'])} THEN {ts(O['sale'])} ELSE sale_ends_at END
   WHERE event_id='{E}' AND configuration_snapshot = c;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE sales_snapshot rows=%', n; END IF;
"""
    if bt == 'A':
        s += f"""  UPDATE booking_schema.tbl_ticket_type_inventory SET configured_capacity={O_CAP} WHERE ticket_type_id='{TT}' AND configured_capacity={N_CAP['A']};
"""
    s += f"""  SELECT configuration_snapshot INTO c3 FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}';
  IF c3->'saleEndsAt' IS DISTINCT FROM {js(OJ['saleEndsAt'])} OR c3->'eventStartsAt' IS DISTINCT FROM {js(OJ['eventStartsAt'])}
     OR c3->'eventEndsAt' IS DISTINCT FROM {js(OJ['eventEndsAt'])} OR c3->'ticketTypes'->k->'configuredQuantity' IS DISTINCT FROM {qty(O_CAP)}
     OR (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c3) x) IS DISTINCT FROM (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c) x)
     OR (SELECT sale_ends_at FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}') IS DISTINCT FROM {ts(O['sale'])}
     OR (SELECT configured_capacity FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}') IS DISTINCT FROM {O_CAP}
  THEN RAISE EXCEPTION 'hau kiem nghich booking khong dat'; END IF;
END $$;
SELECT 'SAU_NGHICH_TRONG_GD '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='{E}';
""" + CUOI
    return s


def ticket_nghich(bt):
    return DAU + f"""SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='{E}' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}'; IF n <> 1 THEN RAISE EXCEPTION 'access_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}';
  IF NOT ({ngay_trong('r.event_starts_at', ts(O['start']), ts(N['start']))} AND {ngay_trong('r.event_ends_at', ts(O['end']), ts(N['end']))})
  THEN RAISE EXCEPTION 'access_snapshot gia tri thu ba/thieu'; END IF;
  UPDATE ticket_schema.tbl_event_access_snapshots SET
     event_starts_at = CASE WHEN event_starts_at = {ts(N['start'])} THEN {ts(O['start'])} ELSE event_starts_at END,
     event_ends_at = CASE WHEN event_ends_at = {ts(N['end'])} THEN {ts(O['end'])} ELSE event_ends_at END
   WHERE event_id='{E}';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE access_snapshot rows=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}';
  IF r.event_starts_at IS DISTINCT FROM {ts(O['start'])} OR r.event_ends_at IS DISTINCT FROM {ts(O['end'])} THEN RAISE EXCEPTION 'hau kiem nghich ticket khong dat'; END IF;
END $$;
""" + CUOI


def payment_nghich(bt):
    return DAU + f"""SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='{E}' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}'; IF n <> 1 THEN RAISE EXCEPTION 'finance_snapshot so dong=%', n; END IF;
  SELECT count(*) INTO n FROM payment_schema.tbl_event_payouts WHERE event_id='{E}'; IF n <> 0 THEN RAISE EXCEPTION 'co payout (%)', n; END IF;
  SELECT * INTO r FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}';
  IF NOT {ngay_trong('r.event_ends_at', ts(O['end']), ts(N['end']))} THEN RAISE EXCEPTION 'finance_snapshot gia tri thu ba/thieu'; END IF;
  UPDATE payment_schema.tbl_event_finance_snapshots SET
     event_ends_at = CASE WHEN event_ends_at = {ts(N['end'])} THEN {ts(O['end'])} ELSE event_ends_at END
   WHERE event_id='{E}';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE finance_snapshot rows=%', n; END IF;
  IF (SELECT event_ends_at FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}') IS DISTINCT FROM {ts(O['end'])} THEN RAISE EXCEPTION 'hau kiem nghich payment khong dat'; END IF;
END $$;
""" + CUOI


# ------------------------------------------------------------------ KIỂM (chỉ SELECT; bản "khoa" thêm FOR SHARE để chờ giao dịch ghi kết thúc)
def trang_thai(expr, o, n):
    return (f"CASE WHEN ({expr}) IS NULL THEN 'THIEU' WHEN ({expr}) = {o} THEN 'CU' "
            f"WHEN ({expr}) = {n} THEN 'DICH' ELSE 'KHAC:'||({expr})::text END")


def kiem(db, khoa):
    pre = "\\set ON_ERROR_STOP on\nSELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();\n"
    if khoa:
        pre += "BEGIN;\n"
    L = []
    def T(name, frm, expr, o, n):
        L.append(f"SELECT 'TRUONG|{name}|'||COALESCE(({ 'SELECT ' + trang_thai(expr, o, n) + ' FROM ' + frm }), 'THIEU_DONG');")
    if db == 'event':
        if khoa:
            L.append(f"SELECT 1 FROM event_schema.tbl_events WHERE id='{E}' FOR SHARE; SELECT 1 FROM event_schema.tbl_ticket_types WHERE id='{TT}' FOR SHARE;")
        f1 = f"event_schema.tbl_events WHERE id='{E}'"
        T('event.sale_ends_at', f1, 'sale_ends_at', ts(O['sale']), ts(N['sale']))
        T('event.starts_at', f1, 'starts_at', ts(O['start']), ts(N['start']))
        T('event.checkin_starts_at', f1, 'checkin_starts_at', ts(O['start']), ts(N['start']))
        T('event.ends_at', f1, 'ends_at', ts(O['end']), ts(N['end']))
        T('event.checkin_ends_at', f1, 'checkin_ends_at', ts(O['end']), ts(N['end']))
        T('event.ticket_types.configured_quantity', f"event_schema.tbl_ticket_types WHERE id='{TT}'", 'configured_quantity', str(O_CAP), str(N_CAP['A']))
        L.append(f"SELECT 'PHU|event.so_dong_events|'||count(*) FROM event_schema.tbl_events WHERE id='{E}';")
    elif db == 'booking':
        if khoa:
            L.append(f"SELECT 1 FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}' FOR SHARE; SELECT 1 FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}' FOR SHARE;")
        f1 = f"booking_schema.tbl_event_sales_snapshots WHERE event_id='{E}'"
        T('booking.sale_ends_at', f1, 'sale_ends_at', ts(O['sale']), ts(N['sale']))
        for k in ('saleEndsAt', 'eventStartsAt', 'eventEndsAt'):
            T(f'booking.json.{k}', f1, f"configuration_snapshot->'{k}'", js(OJ[k]), js(NJ[k]))
        T('booking.json.configuredQuantity', f"{f1}",
          f"(SELECT v->'configuredQuantity' FROM jsonb_array_elements(configuration_snapshot->'ticketTypes') v WHERE v->'ticketTypeId' = to_jsonb('{TT}'::text))",
          qty(O_CAP), qty(N_CAP['A']))
        T('booking.inventory.configured_capacity', f"booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}'", 'configured_capacity', str(O_CAP), str(N_CAP['A']))
        L.append(f"SELECT 'PHU|booking.ticketTypes_khop|'||count(*) FROM booking_schema.tbl_event_sales_snapshots s, jsonb_array_elements(s.configuration_snapshot->'ticketTypes') v WHERE s.event_id='{E}' AND v->'ticketTypeId' = to_jsonb('{TT}'::text);")
        L.append(f"SELECT 'PHU|booking.held|'||COALESCE((SELECT held::text FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}'),'THIEU');")
        L.append(f"SELECT 'BAO|booking.purchased|'||COALESCE((SELECT purchased::text FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='{TT}'),'THIEU');")
    elif db == 'ticket':
        if khoa:
            L.append(f"SELECT 1 FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}' FOR SHARE;")
        f1 = f"ticket_schema.tbl_event_access_snapshots WHERE event_id='{E}'"
        T('ticket.event_starts_at', f1, 'event_starts_at', ts(O['start']), ts(N['start']))
        T('ticket.event_ends_at', f1, 'event_ends_at', ts(O['end']), ts(N['end']))
    elif db == 'payment':
        if khoa:
            L.append(f"SELECT 1 FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}' FOR SHARE;")
        T('payment.event_ends_at', f"payment_schema.tbl_event_finance_snapshots WHERE event_id='{E}'", 'event_ends_at', ts(O['end']), ts(N['end']))
        L.append(f"SELECT 'PHU|payment.payouts|'||count(*) FROM payment_schema.tbl_event_payouts WHERE event_id='{E}';")
    s = pre + "\n".join(L) + "\n"
    if khoa:
        s += "COMMIT;\n"
    return s


# Trường (15) và trạng thái mong đợi khi "DICH" theo biến thể; PHU mong đợi
TRUONG = ['event.sale_ends_at', 'event.starts_at', 'event.checkin_starts_at', 'event.ends_at', 'event.checkin_ends_at',
          'event.ticket_types.configured_quantity', 'booking.sale_ends_at', 'booking.json.saleEndsAt', 'booking.json.eventStartsAt',
          'booking.json.eventEndsAt', 'booking.json.configuredQuantity', 'booking.inventory.configured_capacity',
          'ticket.event_starts_at', 'ticket.event_ends_at', 'payment.event_ends_at']
SUC_CHUA = {'event.ticket_types.configured_quantity', 'booking.json.configuredQuantity', 'booking.inventory.configured_capacity'}
PHU = {'event.so_dong_events': '1', 'booking.ticketTypes_khop': '1', 'booking.held': '0', 'payment.payouts': '0'}

for bt in ('A', 'B'):
    d = HERE / 'sql' / bt
    d.mkdir(parents=True, exist_ok=True)
    for db, f in (('event', event_thuan), ('booking', booking_thuan), ('ticket', ticket_thuan), ('payment', payment_thuan)):
        (d / f'thuan-{db}.sql').write_text(f(bt), encoding='utf-8', newline='\n')
    for db, f in (('event', event_nghich), ('booking', booking_nghich), ('ticket', ticket_nghich), ('payment', payment_nghich)):
        (d / f'nghich-{db}.sql').write_text(f(bt), encoding='utf-8', newline='\n')
    for db in ('event', 'booking', 'ticket', 'payment'):
        (d / f'kiem-{db}.sql').write_text(kiem(db, False), encoding='utf-8', newline='\n')
        (d / f'kiem-khoa-{db}.sql').write_text(kiem(db, True), encoding='utf-8', newline='\n')
    (d / 'truong.txt').write_text(''.join(f"{t}|{'CU' if (bt == 'B' and t in SUC_CHUA) else 'DICH'}\n" for t in TRUONG), encoding='utf-8', newline='\n')
    (d / 'phu.txt').write_text(''.join(f'{k}|{v}\n' for k, v in PHU.items()), encoding='utf-8', newline='\n')
print('xong')
