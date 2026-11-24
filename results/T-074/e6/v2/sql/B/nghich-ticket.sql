\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'; IF n <> 1 THEN RAISE EXCEPTION 'access_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF NOT ((r.event_starts_at IS NOT DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.event_starts_at IS NOT DISTINCT FROM '2026-12-31 22:16:31.402736+00'::timestamptz) AND (r.event_ends_at IS NOT DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz OR r.event_ends_at IS NOT DISTINCT FROM '2027-01-01 22:16:31.402736+00'::timestamptz))
  THEN RAISE EXCEPTION 'access_snapshot gia tri thu ba/thieu'; END IF;
  UPDATE ticket_schema.tbl_event_access_snapshots SET
     event_starts_at = CASE WHEN event_starts_at = '2026-12-31 22:16:31.402736+00'::timestamptz THEN '2026-12-03 22:16:31.402736+00'::timestamptz ELSE event_starts_at END,
     event_ends_at = CASE WHEN event_ends_at = '2027-01-01 22:16:31.402736+00'::timestamptz THEN '2026-12-04 22:16:31.402736+00'::timestamptz ELSE event_ends_at END
   WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE access_snapshot rows=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF r.event_starts_at IS DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.event_ends_at IS DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz THEN RAISE EXCEPTION 'hau kiem nghich ticket khong dat'; END IF;
END $$;
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
