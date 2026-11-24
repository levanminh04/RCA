\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
SELECT 'TRUOC '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453' FOR UPDATE;
DO $$ DECLARE n int; k int; c jsonb; c2 jsonb; c3 jsonb; r record; ri record; BEGIN
  SELECT count(*) INTO n FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF n <> 1 THEN RAISE EXCEPTION 'sales_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  c := r.configuration_snapshot;
  IF r.event_status IS DISTINCT FROM 'PUBLISHED' OR r.source_config_version IS DISTINCT FROM 4 OR r.row_version IS DISTINCT FROM 0
     OR r.sale_ends_at IS DISTINCT FROM '2026-12-02 22:16:31.402736+00'::timestamptz
  THEN RAISE EXCEPTION 'sales_snapshot: cot khac buoc 1'; END IF;
  -- nhan dien va phien ban trong JSON (so dung kieu JSONB)
  IF c->'eventId' IS DISTINCT FROM to_jsonb('3e7c1df9-ada4-4081-94a1-548b80a5da86'::text) OR c->'schemaVersion' IS DISTINCT FROM '1'::jsonb
     OR c->'sourceConfigVersion' IS DISTINCT FROM '"4"'::jsonb OR jsonb_typeof(c->'ticketTypes') IS DISTINCT FROM 'array'
  THEN RAISE EXCEPTION 'sales_snapshot: nhan dien/phien ban JSON khac'; END IF;
  IF c->'saleEndsAt' IS DISTINCT FROM '1796249791.402736000'::jsonb OR c->'eventStartsAt' IS DISTINCT FROM '1796336191.402736000'::jsonb
     OR c->'eventEndsAt' IS DISTINCT FROM '1796422591.402736000'::jsonb
  THEN RAISE EXCEPTION 'sales_snapshot: ngay JSON khac buoc 1 (thieu khoa hoac sai kieu)'; END IF;
  SELECT count(*) INTO n FROM jsonb_array_elements(c->'ticketTypes') x WHERE x->'ticketTypeId' = to_jsonb('ffb36fc7-e30a-4efe-987f-ca5533520453'::text);
  IF n <> 1 THEN RAISE EXCEPTION 'ticketTypes khop ticketTypeId=%', n; END IF;
  SELECT (o-1)::int INTO k FROM jsonb_array_elements(c->'ticketTypes') WITH ORDINALITY x(v,o) WHERE v->'ticketTypeId' = to_jsonb('ffb36fc7-e30a-4efe-987f-ca5533520453'::text);
  IF c->'ticketTypes'->k->'configuredQuantity' IS DISTINCT FROM '"100000"'::jsonb THEN RAISE EXCEPTION 'configuredQuantity khac buoc 1'; END IF;
  SELECT count(*) INTO n FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453';
  IF n <> 1 THEN RAISE EXCEPTION 'inventory so dong=%', n; END IF;
  SELECT * INTO ri FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453';
  IF ri.event_id::text IS DISTINCT FROM '3e7c1df9-ada4-4081-94a1-548b80a5da86' OR ri.configured_capacity IS DISTINCT FROM 100000 OR ri.held IS DISTINCT FROM 0 OR ri.purchased IS DISTINCT FROM 41705
  THEN RAISE EXCEPTION 'inventory khac buoc 1'; END IF;
  c2 := jsonb_set(jsonb_set(jsonb_set(c, '{saleEndsAt}', '1798668991.402736000'::jsonb, false), '{eventStartsAt}', '1798755391.402736000'::jsonb, false), '{eventEndsAt}', '1798841791.402736000'::jsonb, false);
  c2 := jsonb_set(c2, ARRAY['ticketTypes', k::text, 'configuredQuantity'], '"96000"'::jsonb, false);
  UPDATE booking_schema.tbl_event_sales_snapshots SET sale_ends_at='2026-12-30 22:16:31.402736+00'::timestamptz, configuration_snapshot=c2
   WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' AND sale_ends_at='2026-12-02 22:16:31.402736+00'::timestamptz AND configuration_snapshot = c;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE sales_snapshot rows=%', n; END IF;
  UPDATE booking_schema.tbl_ticket_type_inventory SET configured_capacity=96000
   WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453' AND event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' AND configured_capacity=100000 AND held=0 AND purchased=41705;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE inventory rows=%', n; END IF;
  -- hau kiem trong giao dich: dung gia tri, dung kieu, khong them/bot khoa
  SELECT configuration_snapshot INTO c3 FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF c3->'saleEndsAt' IS DISTINCT FROM '1798668991.402736000'::jsonb OR c3->'eventStartsAt' IS DISTINCT FROM '1798755391.402736000'::jsonb
     OR c3->'eventEndsAt' IS DISTINCT FROM '1798841791.402736000'::jsonb
     OR c3->'ticketTypes'->k->'configuredQuantity' IS DISTINCT FROM '"96000"'::jsonb
     OR c3->'ticketTypes'->k->'ticketTypeId' IS DISTINCT FROM to_jsonb('ffb36fc7-e30a-4efe-987f-ca5533520453'::text)
     OR (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c3) x) IS DISTINCT FROM (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c) x)
     OR jsonb_array_length(c3->'ticketTypes') IS DISTINCT FROM jsonb_array_length(c->'ticketTypes')
  THEN RAISE EXCEPTION 'hau kiem sales_snapshot khong dat'; END IF;
  IF (SELECT sale_ends_at FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86') IS DISTINCT FROM '2026-12-30 22:16:31.402736+00'::timestamptz
  THEN RAISE EXCEPTION 'hau kiem sale_ends_at khong dat'; END IF;
  IF (SELECT configured_capacity FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453') IS DISTINCT FROM 96000
  THEN RAISE EXCEPTION 'hau kiem inventory khong dat'; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
SELECT 'SAU_TRONG_GD '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453';
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
