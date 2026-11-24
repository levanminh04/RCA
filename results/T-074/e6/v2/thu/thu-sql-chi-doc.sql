-- T-074 E6 v2 — phép thử LOGIC SQL bằng hằng JSONB, CHỈ ĐỌC (không đụng bảng). Chạy khi có quyền đọc exp-app:
--   docker exec -i flash-ticket-infra-postgres-1 psql -U postgres -X -At -v ON_ERROR_STOP=1 -d postgres < thu-sql-chi-doc.sql
-- Mỗi dòng in TEN|ket_qua|mong; mọi dòng phải ket_qua = mong.
\set ON_ERROR_STOP on
BEGIN TRANSACTION READ ONLY;
WITH c(v) AS (VALUES ('{"saleEndsAt":1796249791.402736000,"eventId":"3e7c1df9-ada4-4081-94a1-548b80a5da86","ticketTypes":[{"ticketTypeId":"ffb36fc7-e30a-4efe-987f-ca5533520453","configuredQuantity":"100000"}]}'::jsonb))
SELECT x FROM (
 SELECT 'J01 so bang khac so le 0|'||((v->'saleEndsAt') = '1796249791.402736'::jsonb)||'|true' x FROM c
 UNION ALL SELECT 'J02 khoa mat IS DISTINCT FROM -> true|'||((v->'khongCo') IS DISTINCT FROM '1796249791.402736000'::jsonb)||'|true' FROM c
 UNION ALL SELECT 'J03 so khac chuoi|'||(('"1796249791.402736000"'::jsonb) IS DISTINCT FROM '1796249791.402736000'::jsonb)||'|true' FROM c
 UNION ALL SELECT 'J04 configuredQuantity chuoi khac so|'||((v->'ticketTypes'->0->'configuredQuantity') IS DISTINCT FROM '100000'::jsonb)||'|true' FROM c
 UNION ALL SELECT 'J05 configuredQuantity chuoi dung|'||((v->'ticketTypes'->0->'configuredQuantity') IS NOT DISTINCT FROM '"100000"'::jsonb)||'|true' FROM c
 UNION ALL SELECT 'J06 jsonb_set create_missing=false khong tao khoa|'||(jsonb_set(v,'{khongCo}','1'::jsonb,false) = v)||'|true' FROM c
 UNION ALL SELECT 'J07 jsonb_set doi dung khoa co san|'||(jsonb_set(v,'{saleEndsAt}','1798668991.402736000'::jsonb,false)->'saleEndsAt' = '1798668991.402736'::jsonb)||'|true' FROM c
 UNION ALL SELECT 'J08 NOT IN voi NULL la NULL (vi the dung IS NOT DISTINCT FROM)|'||coalesce((NULL::timestamptz NOT IN ('2026-12-04 22:16:31.402736+00'))::text,'null')||'|null' FROM c
 UNION ALL SELECT 'J09 dem ticketTypeId trung|'||(SELECT count(*) FROM jsonb_array_elements('[{"ticketTypeId":"a"},{"ticketTypeId":"a"}]'::jsonb) e WHERE e->'ticketTypeId' = to_jsonb('a'::text))||'|2' FROM c
 UNION ALL SELECT 'J10 ->> mat phan biet so/chuoi|'||(('{"q":96000}'::jsonb->>'q') = ('{"q":"96000"}'::jsonb->>'q'))||'|true' FROM c
 UNION ALL SELECT 'J11 = ANY mang jsonb dung kieu|'||(('96000'::jsonb) = ANY (ARRAY['"100000"'::jsonb,'"96000"'::jsonb]))||'|false' FROM c
) t;
ROLLBACK;
