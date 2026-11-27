-- Môi trường thật: kết nối chạy SET ROLE booking_owner (application.yaml), schema thuộc role này.
CREATE ROLE booking_owner NOLOGIN;
GRANT booking_owner TO booking_admin;
CREATE SCHEMA IF NOT EXISTS booking_schema AUTHORIZATION booking_owner;
