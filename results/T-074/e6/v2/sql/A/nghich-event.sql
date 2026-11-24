\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
SELECT 'TRUOC_NGHICH '||row_to_json(t) FROM event_schema.tbl_ticket_types t WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453' FOR UPDATE;
DO $$ DECLARE n int; r record; q bigint; BEGIN
  SELECT count(*) INTO n FROM event_schema.tbl_events WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86'; IF n <> 1 THEN RAISE EXCEPTION 'tbl_events so dong=%', n; END IF;
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF NOT ((r.sale_ends_at IS NOT DISTINCT FROM '2026-12-02 22:16:31.402736+00'::timestamptz OR r.sale_ends_at IS NOT DISTINCT FROM '2026-12-30 22:16:31.402736+00'::timestamptz) AND (r.starts_at IS NOT DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.starts_at IS NOT DISTINCT FROM '2026-12-31 22:16:31.402736+00'::timestamptz)
          AND (r.ends_at IS NOT DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz OR r.ends_at IS NOT DISTINCT FROM '2027-01-01 22:16:31.402736+00'::timestamptz)) OR r.status IS DISTINCT FROM 'PUBLISHED'
  THEN RAISE EXCEPTION 'tbl_events: gia tri thu ba/thieu'; END IF;
  SELECT count(*) INTO n FROM event_schema.tbl_ticket_types WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453' AND event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'; IF n <> 1 THEN RAISE EXCEPTION 'tbl_ticket_types so dong=%', n; END IF;
  SELECT configured_quantity INTO q FROM event_schema.tbl_ticket_types WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453';
  IF q IS NULL OR q NOT IN (100000, 96000) THEN RAISE EXCEPTION 'configured_quantity gia tri thu ba: %', q; END IF;
  UPDATE event_schema.tbl_events SET
     sale_ends_at = CASE WHEN sale_ends_at = '2026-12-30 22:16:31.402736+00'::timestamptz THEN '2026-12-02 22:16:31.402736+00'::timestamptz ELSE sale_ends_at END,
     starts_at = CASE WHEN starts_at = '2026-12-31 22:16:31.402736+00'::timestamptz THEN '2026-12-03 22:16:31.402736+00'::timestamptz ELSE starts_at END,
     checkin_starts_at = CASE WHEN starts_at = '2026-12-31 22:16:31.402736+00'::timestamptz THEN '2026-12-03 22:16:31.402736+00'::timestamptz ELSE checkin_starts_at END,
     ends_at = CASE WHEN ends_at = '2027-01-01 22:16:31.402736+00'::timestamptz THEN '2026-12-04 22:16:31.402736+00'::timestamptz ELSE ends_at END,
     checkin_ends_at = CASE WHEN ends_at = '2027-01-01 22:16:31.402736+00'::timestamptz THEN '2026-12-04 22:16:31.402736+00'::timestamptz ELSE checkin_ends_at END
   WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE tbl_events rows=%', n; END IF;
  UPDATE event_schema.tbl_ticket_types SET configured_quantity=100000 WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453' AND configured_quantity=96000;
  SELECT * INTO r FROM event_schema.tbl_events WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF r.sale_ends_at IS DISTINCT FROM '2026-12-02 22:16:31.402736+00'::timestamptz OR r.starts_at IS DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.ends_at IS DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz
     OR (SELECT configured_quantity FROM event_schema.tbl_ticket_types WHERE id='ffb36fc7-e30a-4efe-987f-ca5533520453') IS DISTINCT FROM 100000
  THEN RAISE EXCEPTION 'hau kiem nghich event khong dat'; END IF;
END $$;
SELECT 'SAU_NGHICH_TRONG_GD '||row_to_json(e) FROM event_schema.tbl_events e WHERE id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
