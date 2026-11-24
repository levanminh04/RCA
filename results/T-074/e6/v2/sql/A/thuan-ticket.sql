\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF n <> 1 THEN RAISE EXCEPTION 'access_snapshot so dong=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF r.event_status IS DISTINCT FROM 'PUBLISHED' OR r.source_config_version IS DISTINCT FROM 4
     OR r.event_starts_at IS DISTINCT FROM '2026-12-03 22:16:31.402736+00'::timestamptz OR r.event_ends_at IS DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz
  THEN RAISE EXCEPTION 'access_snapshot khac buoc 1'; END IF;
  UPDATE ticket_schema.tbl_event_access_snapshots SET event_starts_at='2026-12-31 22:16:31.402736+00'::timestamptz, event_ends_at='2027-01-01 22:16:31.402736+00'::timestamptz
   WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' AND event_starts_at='2026-12-03 22:16:31.402736+00'::timestamptz AND event_ends_at='2026-12-04 22:16:31.402736+00'::timestamptz;
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE access_snapshot rows=%', n; END IF;
  SELECT * INTO r FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF r.event_starts_at IS DISTINCT FROM '2026-12-31 22:16:31.402736+00'::timestamptz OR r.event_ends_at IS DISTINCT FROM '2027-01-01 22:16:31.402736+00'::timestamptz
  THEN RAISE EXCEPTION 'hau kiem access_snapshot khong dat'; END IF;
END $$;
SELECT 'SAU_TRONG_GD '||row_to_json(s) FROM ticket_schema.tbl_event_access_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
