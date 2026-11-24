\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
SELECT 'TRUOC '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453' FOR UPDATE;
DO $$ DECLARE n int; r record; q bigint; BEGIN
  SELECT count(*) INTO n FROM event_schema.tbl_events WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF n <> 1 THEN RAISE EXCEPTION 'tbl_events so dong=%', n; END IF;
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF r.status IS DISTINCT FROM 'PUBLISHED' OR r.source_config_version IS DISTINCT FROM 4 OR r.row_version IS DISTINCT FROM 3
     OR r.sale_ends_at IS DISTINCT FROM '2026-12-02 22:16:31.402736+00'::timestamptz OR r.starts_at IS DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.ends_at IS DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz
     OR r.checkin_starts_at IS DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.checkin_ends_at IS DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz
  THEN RAISE EXCEPTION 'tbl_events: gia tri da khoa khac buoc 1'; END IF;
  SELECT count(*) INTO n FROM event_schema.tbl_ticket_types WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453' AND event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF n <> 1 THEN RAISE EXCEPTION 'tbl_ticket_types so dong=%', n; END IF;
  SELECT configured_quantity INTO q FROM event_schema.tbl_ticket_types WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453';
  IF q IS DISTINCT FROM 100000 THEN RAISE EXCEPTION 'configured_quantity khac buoc 1: %', q; END IF;
  UPDATE event_schema.tbl_events
     SET sale_ends_at='2026-12-30 22:16:31.402736+00'::timestamptz, starts_at='2026-12-31 22:16:31.402736+00'::timestamptz, ends_at='2027-01-01 22:16:31.402736+00'::timestamptz,
         checkin_starts_at='2026-12-31 22:16:31.402736+00'::timestamptz, checkin_ends_at='2027-01-01 22:16:31.402736+00'::timestamptz
   WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86' AND sale_ends_at='2026-12-02 22:16:31.402736+00'::timestamptz AND starts_at='2026-12-03 22:16:31.402736+00'::timestamptz AND ends_at='2026-12-04 22:16:31.402736+00'::timestamptz;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE tbl_events rows=%', n; END IF;
  -- hau kiem trong giao dich
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF r.sale_ends_at IS DISTINCT FROM '2026-12-30 22:16:31.402736+00'::timestamptz OR r.starts_at IS DISTINCT FROM '2026-12-31 22:16:31.402736+00'::timestamptz OR r.ends_at IS DISTINCT FROM '2027-01-01 22:16:31.402736+00'::timestamptz
     OR r.checkin_starts_at IS DISTINCT FROM '2026-12-31 22:16:31.402736+00'::timestamptz OR r.checkin_ends_at IS DISTINCT FROM '2027-01-01 22:16:31.402736+00'::timestamptz
  THEN RAISE EXCEPTION 'hau kiem tbl_events khong dat'; END IF;
  SELECT configured_quantity INTO q FROM event_schema.tbl_ticket_types WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453';
  IF q IS DISTINCT FROM 100000 THEN RAISE EXCEPTION 'hau kiem configured_quantity khong dat: %', q; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
SELECT 'SAU_TRONG_GD '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453';
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
