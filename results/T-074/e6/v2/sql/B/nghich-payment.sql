\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 'TRUOC_NGHICH '||row_to_json(s) FROM payment_schema.tbl_event_finance_snapshots s WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR UPDATE;
DO $$ DECLARE n int; r record; BEGIN
  SELECT count(*) INTO n FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'; IF n <> 1 THEN RAISE EXCEPTION 'finance_snapshot so dong=%', n; END IF;
  SELECT count(*) INTO n FROM payment_schema.tbl_event_payouts WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'; IF n <> 0 THEN RAISE EXCEPTION 'co payout (%)', n; END IF;
  SELECT * INTO r FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  IF NOT (r.event_ends_at IS NOT DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz OR r.event_ends_at IS NOT DISTINCT FROM '2027-01-01 22:16:31.402736+00'::timestamptz) THEN RAISE EXCEPTION 'finance_snapshot gia tri thu ba/thieu'; END IF;
  UPDATE payment_schema.tbl_event_finance_snapshots SET
     event_ends_at = CASE WHEN event_ends_at = '2027-01-01 22:16:31.402736+00'::timestamptz THEN '2026-12-04 22:16:31.402736+00'::timestamptz ELSE event_ends_at END
   WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86';
  GET DIAGNOSTICS n = ROW_COUNT; IF n <> 1 THEN RAISE EXCEPTION 'UPDATE finance_snapshot rows=%', n; END IF;
  IF (SELECT event_ends_at FROM payment_schema.tbl_event_finance_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86') IS DISTINCT FROM '2026-12-04 22:16:31.402736+00'::timestamptz THEN RAISE EXCEPTION 'hau kiem nghich payment khong dat'; END IF;
END $$;
COMMIT;
SELECT 'DA_COMMIT '||current_database()||' '||clock_timestamp();
