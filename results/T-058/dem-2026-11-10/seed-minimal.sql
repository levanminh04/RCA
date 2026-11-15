\set ON_ERROR_STOP on
\connect event_db
BEGIN; SET LOCAL ROLE event_owner; SET LOCAL search_path=event_schema,pg_catalog; SET LOCAL lock_timeout='5s'; SET LOCAL statement_timeout='30s';
INSERT INTO tbl_categories(id,name) VALUES ('ede212d4-0415-44a4-a23f-5a73a52217b1','Concert');
INSERT INTO tbl_venues(id,name,address) VALUES ('6694373f-117b-4aad-8903-14725d3836f3','Concert hall','Synthetic test venue');
INSERT INTO tbl_events(id,organizer_subject,category_id,venue_id,title,description,sales_mode,status,starts_at,ends_at,sale_starts_at,sale_ends_at,checkin_starts_at,checkin_ends_at,purchase_limit,fee_rate,approved_by,approved_at) VALUES ('68bbd408-d7c0-4236-b139-0ecf9cd5d826','ae3a05cd-95c2-47ec-a041-9c9de198c4a1','ede212d4-0415-44a4-a23f-5a73a52217b1','6694373f-117b-4aad-8903-14725d3836f3','Evening concert','Synthetic event for API verification','QUANTITY','PUBLISHED','2026-11-17T20:13:25Z','2026-11-18T20:13:25Z','2026-11-09T20:13:25Z','2026-11-13T20:13:25Z','2026-11-17T20:13:25Z','2026-11-18T20:13:25Z',10,0.05,'01388e8e-721c-42d5-81b6-3f98f2c521df',now());
INSERT INTO tbl_ticket_types(id,event_id,name,sales_mode,unit_price,currency,configured_quantity,color_code) VALUES ('7e2e223b-d268-4665-aa39-61a5315597bc','68bbd408-d7c0-4236-b139-0ecf9cd5d826','Standard test','QUANTITY',20000,'VND',100,'#1677FF');
INSERT INTO tbl_ticket_types(id,event_id,name,sales_mode,unit_price,currency,configured_quantity,color_code) VALUES ('fa7a761a-3d7c-4857-9257-f81159150301','68bbd408-d7c0-4236-b139-0ecf9cd5d826','VIP test','QUANTITY',50000,'VND',100,'#FAAD14');
COMMIT;
\connect booking_db
BEGIN; SET LOCAL ROLE booking_owner; SET LOCAL search_path=booking_schema,pg_catalog; SET LOCAL lock_timeout='5s'; SET LOCAL statement_timeout='30s';
INSERT INTO tbl_event_sales_snapshots(event_id,organizer_subject,sales_mode,event_status,sale_starts_at,sale_ends_at,purchase_limit,configuration_snapshot,source_config_version,received_at) VALUES ('68bbd408-d7c0-4236-b139-0ecf9cd5d826','ae3a05cd-95c2-47ec-a041-9c9de198c4a1','QUANTITY','PUBLISHED','2026-11-09T20:13:25Z','2026-11-13T20:13:25Z',10,'{"schemaVersion": 1, "eventId": "68bbd408-d7c0-4236-b139-0ecf9cd5d826", "organizerSubject": "ae3a05cd-95c2-47ec-a041-9c9de198c4a1", "sourceConfigVersion": "1", "eventStatus": "PUBLISHED", "eventTitle": "Evening concert", "eventStartsAt": "2026-11-17T20:13:25Z", "eventEndsAt": "2026-11-18T20:13:25Z", "venueName": "Concert hall", "mode": "QUANTITY", "saleStartsAt": "2026-11-09T20:13:25Z", "saleEndsAt": "2026-11-13T20:13:25Z", "purchaseLimit": 10, "ticketTypes": [{"ticketTypeId": "7e2e223b-d268-4665-aa39-61a5315597bc", "name": "Standard test", "unitPrice": "20000", "currency": "VND", "sectorId": null, "configuredQuantity": "100", "colorCode": "#1677FF"}, {"ticketTypeId": "fa7a761a-3d7c-4857-9257-f81159150301", "name": "VIP test", "unitPrice": "50000", "currency": "VND", "sectorId": null, "configuredQuantity": "100", "colorCode": "#FAAD14"}], "sectors": [], "seats": [], "promotions": []}'::jsonb,1,now());
INSERT INTO tbl_ticket_type_inventory(ticket_type_id,event_id,configured_capacity,source_config_version) VALUES ('7e2e223b-d268-4665-aa39-61a5315597bc','68bbd408-d7c0-4236-b139-0ecf9cd5d826',100,1);
INSERT INTO tbl_ticket_type_inventory(ticket_type_id,event_id,configured_capacity,source_config_version) VALUES ('fa7a761a-3d7c-4857-9257-f81159150301','68bbd408-d7c0-4236-b139-0ecf9cd5d826',100,1);
COMMIT;
\connect payment_db
BEGIN; SET LOCAL ROLE payment_owner; SET LOCAL search_path=payment_schema,pg_catalog; SET LOCAL lock_timeout='5s'; SET LOCAL statement_timeout='30s';
INSERT INTO tbl_event_finance_snapshots(event_id,organizer_subject,event_ends_at,fee_rate,source_fee_version,received_at) VALUES ('68bbd408-d7c0-4236-b139-0ecf9cd5d826','ae3a05cd-95c2-47ec-a041-9c9de198c4a1','2026-11-18T20:13:25Z',0.05,1,now());
COMMIT;
\connect ticket_db
BEGIN; SET LOCAL ROLE ticket_owner; SET LOCAL search_path=ticket_schema,pg_catalog; SET LOCAL lock_timeout='5s'; SET LOCAL statement_timeout='30s';
INSERT INTO tbl_event_access_snapshots(event_id,organizer_subject,event_status,event_starts_at,event_ends_at,source_config_version,received_at) VALUES ('68bbd408-d7c0-4236-b139-0ecf9cd5d826','ae3a05cd-95c2-47ec-a041-9c9de198c4a1','PUBLISHED','2026-11-17T20:13:25Z','2026-11-18T20:13:25Z',1,now());
COMMIT;