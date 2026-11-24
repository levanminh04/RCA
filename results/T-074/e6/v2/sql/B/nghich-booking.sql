\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
SELECT 'TRUOC_NGHICH '||row_to_json(i) FROM booking_schema.tbl_ticket_type_inventory i WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453' FOR UPDATE;
DO $$ DECLARE n int; k int; c jsonb; c2 jsonb; c3 jsonb; r record; cap bigint; BEGIN
  SELECT count(*) INTO n FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'; IF n <> 1 THEN RAISE EXCEPTION 'sales_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  c := r.configuration_snapshot;
  IF c->'eventId' IS DISTINCT FROM to_jsonb('3e7c1df9-ada4-4081-94a1-548b80a5da86'::text) OR c->'schemaVersion' IS DISTINCT FROM '1'::jsonb OR jsonb_typeof(c->'ticketTypes') IS DISTINCT FROM 'array'
  THEN RAISE EXCEPTION 'nhan dien JSON khac'; END IF;
  IF NOT ((r.sale_ends_at IS NOT DISTINCT FROM '2026-12-02 22:16:31.402736+00'::timestamptz OR r.sale_ends_at IS NOT DISTINCT FROM '2026-12-30 22:16:31.402736+00'::timestamptz)
          AND (c->'saleEndsAt' IS NOT DISTINCT FROM '1796249791.402736000'::jsonb OR c->'saleEndsAt' IS NOT DISTINCT FROM '1798668991.402736000'::jsonb)
          AND (c->'eventStartsAt' IS NOT DISTINCT FROM '1796336191.402736000'::jsonb OR c->'eventStartsAt' IS NOT DISTINCT FROM '1798755391.402736000'::jsonb)
          AND (c->'eventEndsAt' IS NOT DISTINCT FROM '1796422591.402736000'::jsonb OR c->'eventEndsAt' IS NOT DISTINCT FROM '1798841791.402736000'::jsonb))
  THEN RAISE EXCEPTION 'sales_snapshot: gia tri thu ba/thieu/sai kieu'; END IF;
  SELECT count(*) INTO n FROM jsonb_array_elements(c->'ticketTypes') x WHERE x->'ticketTypeId' = to_jsonb('ffb36fc7-e30a-4efe-987f-ca5533520453'::text);
  IF n <> 1 THEN RAISE EXCEPTION 'ticketTypes khop ticketTypeId=%', n; END IF;
  SELECT (o-1)::int INTO k FROM jsonb_array_elements(c->'ticketTypes') WITH ORDINALITY x(v,o) WHERE v->'ticketTypeId' = to_jsonb('ffb36fc7-e30a-4efe-987f-ca5533520453'::text);
  IF c->'ticketTypes'->k->'configuredQuantity' IS NULL OR NOT (c->'ticketTypes'->k->'configuredQuantity' = ANY (ARRAY['"100000"'::jsonb]))
  THEN RAISE EXCEPTION 'configuredQuantity gia tri thu ba/sai kieu'; END IF;
  SELECT count(*) INTO n FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453'; IF n <> 1 THEN RAISE EXCEPTION 'inventory so dong=%', n; END IF;
  SELECT configured_capacity INTO cap FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453';
  IF cap IS NULL OR cap NOT IN (100000) THEN RAISE EXCEPTION 'inventory gia tri thu ba: %', cap; END IF;
  c2 := c;
  IF c2->'saleEndsAt' = '1798668991.402736000'::jsonb THEN c2 := jsonb_set(c2, '{saleEndsAt}', '1796249791.402736000'::jsonb, false); END IF;
  IF c2->'eventStartsAt' = '1798755391.402736000'::jsonb THEN c2 := jsonb_set(c2, '{eventStartsAt}', '1796336191.402736000'::jsonb, false); END IF;
  IF c2->'eventEndsAt' = '1798841791.402736000'::jsonb THEN c2 := jsonb_set(c2, '{eventEndsAt}', '1796422591.402736000'::jsonb, false); END IF;
  UPDATE booking_schema.tbl_event_sales_snapshots SET configuration_snapshot=c2,
         sale_ends_at = CASE WHEN sale_ends_at = '2026-12-30 22:16:31.402736+00'::timestamptz THEN '2026-12-02 22:16:31.402736+00'::timestamptz ELSE sale_ends_at END
   WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' AND configuration_snapshot = c;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE sales_snapshot rows=%', n; END IF;
  SELECT configuration_snapshot INTO c3 FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF c3->'saleEndsAt' IS DISTINCT FROM '1796249791.402736000'::jsonb OR c3->'eventStartsAt' IS DISTINCT FROM '1796336191.402736000'::jsonb
     OR c3->'eventEndsAt' IS DISTINCT FROM '1796422591.402736000'::jsonb OR c3->'ticketTypes'->k->'configuredQuantity' IS DISTINCT FROM '"100000"'::jsonb
     OR (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c3) x) IS DISTINCT FROM (SELECT array_agg(x ORDER BY x) FROM jsonb_object_keys(c) x)
     OR (SELECT sale_ends_at FROM booking_schema.tbl_event_sales_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86') IS DISTINCT FROM '2026-12-02 22:16:31.402736+00'::timestamptz
     OR (SELECT configured_capacity FROM booking_schema.tbl_ticket_type_inventory WHERE ticket_type_id='ffb36fc7-e30a-4efe-987f-ca5533520453') IS DISTINCT FROM 100000
  THEN RAISE EXCEPTION 'hau kiem nghich booking khong dat'; END IF;
END $$;
SELECT 'SAU_NGHICH_TRONG_GD '||row_to_json(s) FROM booking_schema.tbl_event_sales_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
