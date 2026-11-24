\set ON_ERROR_STOP on
SELECT 'PHIEN '||pg_backend_pid()||' '||current_setting('application_name')||' '||clock_timestamp();
BEGIN;
SELECT 1 FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86' FOR SHARE;
SELECT 'TRUONG|ticket.event_starts_at|'||COALESCE((SELECT CASE WHEN (event_starts_at) IS NULL THEN 'THIEU' WHEN (event_starts_at) = '2026-12-03 22:16:31.402736+00'::timestamptz THEN 'CU' WHEN (event_starts_at) = '2026-12-31 22:16:31.402736+00'::timestamptz THEN 'DICH' ELSE 'KHAC:'||(event_starts_at)::text END FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'), 'THIEU_DONG');
SELECT 'TRUONG|ticket.event_ends_at|'||COALESCE((SELECT CASE WHEN (event_ends_at) IS NULL THEN 'THIEU' WHEN (event_ends_at) = '2026-12-04 22:16:31.402736+00'::timestamptz THEN 'CU' WHEN (event_ends_at) = '2027-01-01 22:16:31.402736+00'::timestamptz THEN 'DICH' ELSE 'KHAC:'||(event_ends_at)::text END FROM ticket_schema.tbl_event_access_snapshots WHERE event_id='3e7c1df9-ada4-4081-94a1-548b80a5da86'), 'THIEU_DONG');
COMMIT;
