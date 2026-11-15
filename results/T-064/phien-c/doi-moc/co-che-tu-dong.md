# Cơ chế các ca đổi (sinh tự động bởi `co_che_ca_doi.py`)

kp = khởi phát của kênh có cờ, tính theo giây so với **t gốc** (không phải t' của bản dời). Chỉ đọc đầu ra đã lưu.

## P7 -> V052-DM-P7-t-30 — dev2: so_voi tot_len, dK 1, ca đổi 6
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['api-gateway']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:payment-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=13.3 kp=+50s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=8.03 kp=+10s, workload/xuong s=0.72 kp=+10s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:event-service; 3:booking-service; 4:payment-service
  -   api-gateway: workload/xuong s=111 kp=+10s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   event-service: GET /api/v1/events/{id}/len s=82.4 kp=-30s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.6 kp=+0s, Session.merge com.flashticket.booking_service.entity.Reservation/len s=32 kp=-30s, GET/len s=25.5 kp=-10s
  -   payment-service: workload/xuong s=0.72 kp=+10s
### 729604d2 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['ticket-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.merge com.flashticket.booking_service.entity.PurchaseLimit/len s=5.67 kp=+0s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   ticket-service: SELECT ticket_schema.tbl_inbox_messages/len s=4.89 kp=-30s
### fb1cf0e9 (FLASH-HEALTHY) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:keycloak; 3:event-service; 4:ticket-service
  -   booking-service: Session.merge com.flashticket.booking_service.entity.Order/len s=1.23e+03 kp=+0s, SELECT com.flashticket.booking_service.entity.TicketTypeInventory/len s=488 kp=+10s, SELECT com.flashticket.booking_service.entity.PromotionUsage/len s=328 kp=+0s, TicketTypeInventoryRepository.findAllById/len s=310 kp=+0s
  -   keycloak: DELETE keycloak_db.OUTBOX_ENTRY/len s=570 kp=+0s, ScheduledTaskRunner.run/len s=239 kp=+20s, SELECT keycloak_db.OFFLINE_CLIENT_SESSION/len s=209 kp=+0s, SELECT keycloak_db.OUTBOX_ENTRY/len s=158 kp=+0s
  -   event-service: SELECT event_schema.tbl_event_sectors/len s=219 kp=+0s, Transaction.commit/len s=216 kp=+0s, SELECT event_schema.tbl_ticket_types/len s=199 kp=+0s, E2:api-gateway->event-service/len s=189 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=190 kp=+0s, SELECT ticket_schema.tbl_tickets/len s=115 kp=+10s, SELECT ticket_schema.tbl_ticket_deliveries/len s=103 kp=+0s, ticket_db/len s=91.5 kp=+0s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:booking-service; 3:event-service; 4:payment-service
  -   keycloak: DELETE keycloak_db.OUTBOX_ENTRY/len s=551 kp=-30s, SELECT keycloak_db.OUTBOX_ENTRY/len s=168 kp=-10s, ScheduledTaskRunner.run/len s=73.8 kp=-30s
  -   booking-service: SELECT com.flashticket.booking_service.entity.TicketTypeInventory/len s=476 kp=-30s, SELECT com.flashticket.booking_service.entity.PromotionUsage/len s=355 kp=-30s, TicketTypeInventoryRepository.findAllById/len s=310 kp=-10s, workload/len s=260 kp=+10s
  -   event-service: Transaction.commit/len s=237 kp=-30s, E2:api-gateway->event-service/len s=232 kp=+0s, SELECT event_schema.tbl_event_sectors/len s=232 kp=-30s, SELECT event_schema.tbl_ticket_types/len s=208 kp=-10s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=200 kp=-20s, Transaction.commit/len s=83.5 kp=+0s, PaymentSagaRepository.findForUpdateByOrderId/len s=75.4 kp=+0s, ChargeRepository.existsByProviderAndMerchantAccountAndProviderChargeId/len s=70.9 kp=+0s
### 83073ed1 (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['ticket-service']
- P7:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:payment-service; 3:api-gateway; 3:booking-service
  -   ticket-service: SELECT ticket_db/len s=169 kp=-30s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=22.4 kp=-30s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.0→1.0, p1 0.0→1.0
- nhóm hạng 1: ['keycloak'] → ['event-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:payment-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+0s, workload/xuong s=0.72 kp=+10s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:booking-service; 3:ticket-service; 4:api-gateway
  -   event-service: GET /api/v1/events/{id}/len s=114 kp=-30s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+10s, OrderRepository.currentDatabaseTime/len s=108 kp=+10s, SELECT booking_schema.tbl_orders/len s=108 kp=-30s, SELECT booking_db/len s=71.7 kp=-20s
  -   ticket-service: TicketJobs.deliver/len s=11.2 kp=+20s, workload/xuong s=0.24 kp=+30s
  -   api-gateway: workload/len s=50.6 kp=+10s, error/len s=3.6 kp=+10s, log_loi/len s=1
### 46aab4be (PAUSE-PAYMENT) — đổi: hang_ky_vong None→3.0, p3 0.0→1.0
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:user-service; 4:config-discovery
  -   booking-service: SELECT booking_schema.tbl_orders/len s=433 kp=+0s, SELECT booking_db/len s=311 kp=+0s, OrderRepository.currentDatabaseTime/len s=200 kp=+0s, workload/xuong s=49 kp=+10s
  -   api-gateway: workload/xuong s=52.9 kp=+30s, log_loi/len s=1, error/len s=0.36 kp=+40s
  -   user-service: find user_db.tbl_organizer_applications/len s=28.7 kp=+90s, workload/xuong s=0.08 kp=+10s
  -   config-discovery: workload/xuong s=2.3 kp=+10s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:payment-service; 4:user-service
  -   booking-service: SELECT booking_schema.tbl_orders/len s=428 kp=-20s, SELECT booking_db/len s=295 kp=-20s, OrderRepository.currentDatabaseTime/len s=202 kp=-20s, workload/xuong s=49 kp=+10s
  -   api-gateway: workload/xuong s=26.6 kp=+30s, log_loi/len s=1, error/len s=0.36 kp=+40s
  -   payment-service: OrderPaymentSnapshotRepository.findForUpdateByOrderId/len s=8.63 kp=-30s, PaymentWorker.publishOutbox/len s=3.83 kp=-30s, workload/xuong s=0.522 kp=+10s
  -   user-service: workload/xuong s=0.08 kp=+10s

## P7 -> V052-DM-P7-t-30 — t062: so_voi bang, dK 0, ca đổi 3
### 00eaea92 (FLASH-HEALTHY) — đổi: 
- nhóm hạng 1: ['payment-service'] → ['booking-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:event-service; 4:ticket-service
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=144 kp=+10s, SELECT payment_schema.tbl_outbox_messages/len s=46.3 kp=+10s, workload/len s=5.5 kp=+30s, PaymentWorker.selectEventRefundOrders/len s=3.96 kp=+0s
  -   booking-service: workload/len s=139 kp=+0s
  -   event-service: workload/len s=6.26 kp=+10s
  -   ticket-service: error/len s=5.2 kp=+30s, workload/len s=5.2 kp=+30s, log_loi/len s=0.659
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:payment-service; 3:ticket-service; 4:event-service
  -   booking-service: OrderRepository.findByIdAndBuyerSubject/len s=631 kp=-30s, workload/len s=139 kp=+0s, SELECT com.flashticket.booking_service.entity.Order/len s=70.8 kp=-30s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=135 kp=-20s, workload/len s=5.5 kp=+30s, PaymentWorker.selectEventRefundOrders/len s=5.02 kp=-10s
  -   ticket-service: TicketJobs.cancel/len s=102 kp=-20s, error/len s=5.2 kp=+30s, workload/len s=5.2 kp=+30s, log_loi/len s=0.634
  -   event-service: workload/len s=6.28 kp=+10s
### a5539fba (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['keycloak'] → ['ticket-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:api-gateway; 2:booking-service; 2:booking_db
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=220 kp=+80s, DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=31 kp=+20s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:keycloak; 3:api-gateway; 3:booking-service
  -   ticket-service: SELECT ticket_db/len s=241 kp=-30s
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=220 kp=-30s, DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=28.8 kp=-30s
### e8661e0a (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['event-service'] → ['ticket-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:ticket-service; 3:api-gateway; 3:booking-service
  -   event-service: SELECT event_schema.tbl_event_sectors/len s=119 kp=+0s, SELECT event_schema.tbl_outbox_messages/len s=34.6 kp=+0s
  -   ticket-service: TicketJobs.cancel/len s=57.9 kp=+0s
- V052-DM-P7-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:event-service; 3:api-gateway; 3:booking-service
  -   ticket-service: TicketJobs.cancel/len s=55.7 kp=+0s
  -   event-service: SELECT event_schema.tbl_promotions/len s=36.1 kp=-30s

## P7 -> V055-DM-P7-t+30 — dev2: so_voi xau_di, dK 1, ca đổi 6
### eb48d6b3 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['event-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:payment-service; 4:api-gateway
  -   booking-service: Session.persist com.flashticket.booking_service.entity.IdempotencyRequest/len s=83.2 kp=+0s, SELECT booking_schema.tbl_outbox_messages/len s=32.5 kp=+0s
  -   event-service: event_db/len s=82.7 kp=+0s
  -   payment-service: UPDATE payment_schema.tbl_outbox_messages/len s=12.1 kp=+0s
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   event-service: GET /api/v1/events/{id}/len s=52.8 kp=+30s
### 4af494a5 (EVENT-DB-LAT) — đổi: hang_ky_vong 2.0→1.0, p1 0.0→1.0
- nhóm hạng 1: ['payment-service'] → ['event-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:event-service; 3:ticket-service; 4:keycloak
  -   payment-service: InboxMessageRepository.findById/len s=996 kp=+10s, Channel.waitForConfirms/len s=21.2 kp=+10s
  -   event-service: latency-50/len s=988 kp=+10s, Transaction.commit/len s=651 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=573 kp=+0s, SELECT event_schema.tbl_promotions/len s=565 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=262 kp=+0s
  -   keycloak: OutboxDrainerTask.run/len s=128 kp=+0s
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:ticket-service; 3:keycloak; 4:booking-service
  -   event-service: latency-50/len s=736 kp=+30s, Transaction.commit/len s=339 kp=+40s, SELECT event_schema.tbl_event_layouts/len s=330 kp=+40s, SELECT event_schema.tbl_promotions/len s=317 kp=+30s
  -   ticket-service: SELECT ticket_db/len s=269 kp=+30s
  -   keycloak: OutboxDrainerTask.run/len s=128 kp=+40s
  -   booking-service: Session.find com.flashticket.booking_service.entity.EventSalesSnapshot/len s=55.8 kp=+30s
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['api-gateway']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:payment-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=13.3 kp=+50s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=8.03 kp=+10s, workload/xuong s=0.72 kp=+10s
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:event-service; 3:booking-service; 4:ticket-service
  -   api-gateway: workload/xuong s=110 kp=+30s, EVALSHA/len s=55.7 kp=+40s, error/len s=1.22 kp=+30s, log_loi/len s=0.903
  -   event-service: GET /api/v1/events/{id}/len s=50.1 kp=+30s, error/len s=1.2 kp=+30s, log_loi/len s=0.903
  -   booking-service: workload/xuong s=126 kp=+30s, SELECT booking_db/len s=38.1 kp=+30s, SELECT booking_schema.tbl_orders/len s=18.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=12.8 kp=+50s
  -   ticket-service: workload/xuong s=48 kp=+30s
### 729604d2 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['payment-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.merge com.flashticket.booking_service.entity.PurchaseLimit/len s=5.67 kp=+0s
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   payment-service: Session.merge com.flashticket.payment_service.entity.OrderPaymentSnapshot/len s=10.3 kp=+30s
### 83073ed1 (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['booking-service']
- P7:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.persist com.flashticket.booking_service.entity.Order/len s=35 kp=+80s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.0→3.0
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:payment-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+0s, workload/xuong s=0.72 kp=+10s
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:booking-service; 3:event-service; 4:payment-service
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=1.95e+03 kp=+40s, SELECT keycloak_db.OFFLINE_USER_SESSION/len s=894 kp=+40s
  -   booking-service: workload/xuong s=126 kp=+30s, SELECT booking_schema.tbl_orders/len s=102 kp=+50s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+30s, SELECT booking_db/len s=69.3 kp=+30s
  -   event-service: GET /api/v1/events/{id}/len s=56.2 kp=+30s, workload/len s=4.92 kp=+30s, error/len s=3.66 kp=+30s, log_loi/len s=0.902
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+30s, workload/xuong s=0.72 kp=+30s

## P7 -> V055-DM-P7-t+30 — t062: so_voi xau_di, dK 0, ca đổi 2
### a89954d1 (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:keycloak; 3:payment-service; 4:api-gateway
  -   event-service: GET /api/v1/events/{id}/len s=664 kp=+0s, event_db/len s=88.9 kp=+0s, error/len s=2.84 kp=+10s, log_loi/len s=1
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=644 kp=+120s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=119 kp=+120s
  -   payment-service: SELECT com.flashticket.payment_service.entity.OrderPaymentSnapshot/len s=163 kp=+10s, RefundRepository.findAllByOrderIdOrderByCreatedAtAscIdAsc/len s=11.6 kp=+10s
  -   api-gateway: GET event/len s=23.9 kp=+0s, error/len s=13.4 kp=+10s, log_loi/len s=0.833
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:api-gateway; 4:booking-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=644 kp=+120s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=119 kp=+120s
  -   event-service: GET /api/v1/events/{id}/len s=342 kp=+30s, event_db/len s=88.9 kp=+30s, error/len s=2.84 kp=+30s, log_loi/len s=0.895
  -   api-gateway: GET event/len s=25 kp=+30s, error/len s=12.9 kp=+30s, log_loi/len s=0.745
  -   booking-service: SELECT booking_schema.tbl_outbox_messages/len s=20.7 kp=+40s
### f728fce2 (NET-GW-BOOK) — đổi: hang_ky_vong 1.0→3.0, p1 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['event-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:keycloak; 4:api-gateway
  -   booking-service: E2:api-gateway->booking-service/len s=1.03e+03 kp=+0s
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=293 kp=+20s
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=178 kp=+100s
  -   api-gateway: latency-90/len s=349 kp=+10s, latency-50/len s=15.5 kp=+30s
- V055-DM-P7-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:keycloak; 3:booking-service; 4:api-gateway
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=302 kp=+30s
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=178 kp=+100s
  -   booking-service: SELECT booking_db/len s=57 kp=+70s
  -   api-gateway: latency-90/len s=349 kp=+30s, latency-50/len s=15.5 kp=+30s

## V032 -> V053-DM-V032-t-30 — dev2: so_voi bang, dK 1, ca đổi 5
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['api-gateway']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:payment-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=13.3 kp=+50s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=8.03 kp=+10s, workload/xuong s=0.72 kp=+10s
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:event-service; 3:booking-service; 4:payment-service
  -   api-gateway: workload/xuong s=111 kp=+10s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   event-service: GET /api/v1/events/{id}/len s=82.4 kp=-30s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.6 kp=+0s, Session.merge com.flashticket.booking_service.entity.Reservation/len s=32 kp=-30s, GET/len s=25.5 kp=-10s
  -   payment-service: workload/xuong s=0.72 kp=+10s
### 729604d2 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['ticket-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.merge com.flashticket.booking_service.entity.PurchaseLimit/len s=5.67 kp=+0s
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   ticket-service: SELECT ticket_schema.tbl_inbox_messages/len s=4.89 kp=-30s
### fb1cf0e9 (FLASH-HEALTHY) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['keycloak']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:keycloak; 3:event-service; 4:ticket-service
  -   booking-service: Session.merge com.flashticket.booking_service.entity.Order/len s=1.23e+03 kp=+0s, SELECT com.flashticket.booking_service.entity.TicketTypeInventory/len s=488 kp=+10s, SELECT com.flashticket.booking_service.entity.PromotionUsage/len s=328 kp=+0s, TicketTypeInventoryRepository.findAllById/len s=310 kp=+0s
  -   keycloak: DELETE keycloak_db.OUTBOX_ENTRY/len s=570 kp=+0s, ScheduledTaskRunner.run/len s=239 kp=+20s, SELECT keycloak_db.OFFLINE_CLIENT_SESSION/len s=209 kp=+0s, SELECT keycloak_db.OUTBOX_ENTRY/len s=158 kp=+0s
  -   event-service: SELECT event_schema.tbl_event_sectors/len s=219 kp=+0s, Transaction.commit/len s=216 kp=+0s, SELECT event_schema.tbl_ticket_types/len s=199 kp=+0s, E2:api-gateway->event-service/len s=189 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=190 kp=+0s, SELECT ticket_schema.tbl_tickets/len s=115 kp=+10s, SELECT ticket_schema.tbl_ticket_deliveries/len s=103 kp=+0s, ticket_db/len s=91.5 kp=+0s
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:booking-service; 3:event-service; 4:payment-service
  -   keycloak: DELETE keycloak_db.OUTBOX_ENTRY/len s=551 kp=-30s, SELECT keycloak_db.OUTBOX_ENTRY/len s=168 kp=-10s, ScheduledTaskRunner.run/len s=73.8 kp=-30s
  -   booking-service: SELECT com.flashticket.booking_service.entity.TicketTypeInventory/len s=476 kp=-30s, SELECT com.flashticket.booking_service.entity.PromotionUsage/len s=355 kp=-30s, TicketTypeInventoryRepository.findAllById/len s=310 kp=-10s, workload/len s=260 kp=+10s
  -   event-service: Transaction.commit/len s=237 kp=-30s, E2:api-gateway->event-service/len s=232 kp=+0s, SELECT event_schema.tbl_event_sectors/len s=232 kp=-30s, SELECT event_schema.tbl_ticket_types/len s=208 kp=-10s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=200 kp=-20s, Transaction.commit/len s=83.5 kp=+0s, PaymentSagaRepository.findForUpdateByOrderId/len s=75.4 kp=+0s, ChargeRepository.existsByProviderAndMerchantAccountAndProviderChargeId/len s=70.9 kp=+0s
### 83073ed1 (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['ticket-service']
- V032:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:payment-service; 3:api-gateway; 3:booking-service
  -   ticket-service: SELECT ticket_db/len s=169 kp=-30s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=22.4 kp=-30s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.0→1.0, p1 0.0→1.0
- nhóm hạng 1: ['keycloak'] → ['event-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:payment-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+0s, workload/xuong s=0.72 kp=+10s
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:booking-service; 3:ticket-service; 4:api-gateway
  -   event-service: GET /api/v1/events/{id}/len s=114 kp=-30s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+10s, OrderRepository.currentDatabaseTime/len s=108 kp=+10s, SELECT booking_schema.tbl_orders/len s=108 kp=-30s, SELECT booking_db/len s=71.7 kp=-20s
  -   ticket-service: TicketJobs.deliver/len s=11.2 kp=+20s, workload/xuong s=0.24 kp=+30s
  -   api-gateway: workload/len s=50.6 kp=+10s, error/len s=3.6 kp=+10s, log_loi/len s=1

## V032 -> V053-DM-V032-t-30 — t062: so_voi bang, dK 0, ca đổi 3
### 00eaea92 (FLASH-HEALTHY) — đổi: 
- nhóm hạng 1: ['payment-service'] → ['booking-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:event-service; 4:ticket-service
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=144 kp=+10s, SELECT payment_schema.tbl_outbox_messages/len s=46.3 kp=+10s, workload/len s=5.5 kp=+30s, PaymentWorker.selectEventRefundOrders/len s=3.96 kp=+0s
  -   booking-service: workload/len s=139 kp=+0s
  -   event-service: workload/len s=6.26 kp=+10s
  -   ticket-service: error/len s=5.2 kp=+30s, workload/len s=5.2 kp=+30s, log_loi/len s=0.659
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:payment-service; 3:ticket-service; 4:event-service
  -   booking-service: OrderRepository.findByIdAndBuyerSubject/len s=631 kp=-30s, workload/len s=139 kp=+0s, SELECT com.flashticket.booking_service.entity.Order/len s=70.8 kp=-30s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=135 kp=-20s, workload/len s=5.5 kp=+30s, PaymentWorker.selectEventRefundOrders/len s=5.02 kp=-10s
  -   ticket-service: TicketJobs.cancel/len s=102 kp=-20s, error/len s=5.2 kp=+30s, workload/len s=5.2 kp=+30s, log_loi/len s=0.634
  -   event-service: workload/len s=6.28 kp=+10s
### a5539fba (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['keycloak'] → ['ticket-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:api-gateway; 2:booking-service; 2:booking_db
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=220 kp=+80s, DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=31 kp=+20s
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:keycloak; 3:api-gateway; 3:booking-service
  -   ticket-service: SELECT ticket_db/len s=241 kp=-30s
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=220 kp=-30s, DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=28.8 kp=-30s
### e8661e0a (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['event-service'] → ['ticket-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:ticket-service; 3:api-gateway; 3:booking-service
  -   event-service: SELECT event_schema.tbl_event_sectors/len s=119 kp=+0s, SELECT event_schema.tbl_outbox_messages/len s=34.6 kp=+0s
  -   ticket-service: TicketJobs.cancel/len s=57.9 kp=+0s
- V053-DM-V032-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:event-service; 3:api-gateway; 3:booking-service
  -   ticket-service: TicketJobs.cancel/len s=55.7 kp=+0s
  -   event-service: SELECT event_schema.tbl_promotions/len s=36.1 kp=-30s

## V032 -> V056-DM-V032-t+30 — dev2: so_voi xau_di, dK 1, ca đổi 7
### eb48d6b3 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['event-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:payment-service; 4:api-gateway
  -   booking-service: Session.persist com.flashticket.booking_service.entity.IdempotencyRequest/len s=83.2 kp=+0s, SELECT booking_schema.tbl_outbox_messages/len s=32.5 kp=+0s
  -   event-service: event_db/len s=82.7 kp=+0s
  -   payment-service: UPDATE payment_schema.tbl_outbox_messages/len s=12.1 kp=+0s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   event-service: GET /api/v1/events/{id}/len s=52.8 kp=+30s
### 4af494a5 (EVENT-DB-LAT) — đổi: hang_ky_vong 2.0→1.0, p1 0.0→1.0
- nhóm hạng 1: ['payment-service'] → ['event-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:event-service; 3:ticket-service; 4:keycloak
  -   payment-service: InboxMessageRepository.findById/len s=996 kp=+10s, Channel.waitForConfirms/len s=21.2 kp=+10s
  -   event-service: latency-50/len s=988 kp=+10s, Transaction.commit/len s=651 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=573 kp=+0s, SELECT event_schema.tbl_promotions/len s=565 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=262 kp=+0s
  -   keycloak: OutboxDrainerTask.run/len s=128 kp=+0s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:ticket-service; 3:keycloak; 4:booking-service
  -   event-service: latency-50/len s=736 kp=+30s, Transaction.commit/len s=339 kp=+40s, SELECT event_schema.tbl_event_layouts/len s=330 kp=+40s, SELECT event_schema.tbl_promotions/len s=317 kp=+30s
  -   ticket-service: SELECT ticket_db/len s=269 kp=+30s
  -   keycloak: OutboxDrainerTask.run/len s=128 kp=+40s
  -   booking-service: Session.find com.flashticket.booking_service.entity.EventSalesSnapshot/len s=55.8 kp=+30s
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['api-gateway']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:payment-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=13.3 kp=+50s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=8.03 kp=+10s, workload/xuong s=0.72 kp=+10s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:event-service; 3:booking-service; 4:ticket-service
  -   api-gateway: workload/xuong s=110 kp=+30s, EVALSHA/len s=55.7 kp=+40s, error/len s=1.22 kp=+30s, log_loi/len s=0.903
  -   event-service: GET /api/v1/events/{id}/len s=50.1 kp=+30s, error/len s=1.2 kp=+30s, log_loi/len s=0.903
  -   booking-service: workload/xuong s=126 kp=+30s, SELECT booking_db/len s=38.1 kp=+30s, SELECT booking_schema.tbl_orders/len s=18.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=12.8 kp=+50s
  -   ticket-service: workload/xuong s=48 kp=+30s
### 729604d2 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['payment-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.merge com.flashticket.booking_service.entity.PurchaseLimit/len s=5.67 kp=+0s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   payment-service: Session.merge com.flashticket.payment_service.entity.OrderPaymentSnapshot/len s=10.3 kp=+30s
### 83073ed1 (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['booking-service']
- V032:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.persist com.flashticket.booking_service.entity.Order/len s=35 kp=+80s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.0→3.0
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:payment-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+0s, workload/xuong s=0.72 kp=+10s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:booking-service; 3:event-service; 4:payment-service
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=1.95e+03 kp=+40s, SELECT keycloak_db.OFFLINE_USER_SESSION/len s=894 kp=+40s
  -   booking-service: workload/xuong s=126 kp=+30s, SELECT booking_schema.tbl_orders/len s=102 kp=+50s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+30s, SELECT booking_db/len s=69.3 kp=+30s
  -   event-service: GET /api/v1/events/{id}/len s=56.2 kp=+30s, workload/len s=4.92 kp=+30s, error/len s=3.66 kp=+30s, log_loi/len s=0.902
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+30s, workload/xuong s=0.72 kp=+30s
### 46aab4be (PAUSE-PAYMENT) — đổi: hang_ky_vong 1.0→3.0, p1 1.0→0.0
- nhóm hạng 1: ['payment-service'] → ['booking-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:api-gateway; 4:user-service
  -   payment-service: live-ms/len s=3e+03 kp=+10s, live-down/len s=1 kp=+10s
  -   booking-service: SELECT booking_schema.tbl_orders/len s=433 kp=+0s, SELECT booking_db/len s=311 kp=+0s, OrderRepository.currentDatabaseTime/len s=200 kp=+0s, workload/xuong s=49 kp=+10s
  -   api-gateway: workload/xuong s=52.9 kp=+30s, log_loi/len s=1, error/len s=0.36 kp=+40s
  -   user-service: find user_db.tbl_organizer_applications/len s=28.7 kp=+90s, workload/xuong s=0.08 kp=+10s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:payment-service; 4:user-service
  -   booking-service: SELECT booking_schema.tbl_orders/len s=435 kp=+50s, OrderRepository.currentDatabaseTime/len s=191 kp=+50s, SELECT booking_db/len s=90.2 kp=+30s, workload/xuong s=48.5 kp=+30s
  -   api-gateway: workload/xuong s=51.9 kp=+30s, log_loi/len s=0.987, error/len s=0.36 kp=+40s
  -   payment-service: live-ms/len s=2.93e+03 kp=+30s, live-down/len s=1 kp=+30s
  -   user-service: workload/xuong s=0.08 kp=+30s

## V032 -> V056-DM-V032-t+30 — t062: so_voi xau_di, dK 0, ca đổi 2
### a89954d1 (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['keycloak']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:keycloak; 3:payment-service; 4:api-gateway
  -   event-service: GET /api/v1/events/{id}/len s=664 kp=+0s, event_db/len s=88.9 kp=+0s, error/len s=2.84 kp=+10s, log_loi/len s=1
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=644 kp=+120s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=119 kp=+120s
  -   payment-service: SELECT com.flashticket.payment_service.entity.OrderPaymentSnapshot/len s=163 kp=+10s, RefundRepository.findAllByOrderIdOrderByCreatedAtAscIdAsc/len s=11.6 kp=+10s
  -   api-gateway: GET event/len s=23.9 kp=+0s, error/len s=13.4 kp=+10s, log_loi/len s=0.833
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:api-gateway; 4:booking-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=644 kp=+120s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=119 kp=+120s
  -   event-service: GET /api/v1/events/{id}/len s=342 kp=+30s, event_db/len s=88.9 kp=+30s, error/len s=2.84 kp=+30s, log_loi/len s=0.895
  -   api-gateway: GET event/len s=25 kp=+30s, error/len s=12.9 kp=+30s, log_loi/len s=0.745
  -   booking-service: SELECT booking_schema.tbl_outbox_messages/len s=20.7 kp=+40s
### f728fce2 (NET-GW-BOOK) — đổi: hang_ky_vong 1.0→3.0, p1 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['event-service']
- V032:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:keycloak; 4:api-gateway
  -   booking-service: E2:api-gateway->booking-service/len s=1.03e+03 kp=+0s
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=293 kp=+20s
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=178 kp=+100s
  -   api-gateway: latency-90/len s=349 kp=+10s, latency-50/len s=15.5 kp=+30s
- V056-DM-V032-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:keycloak; 3:booking-service; 4:api-gateway
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=302 kp=+30s
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=178 kp=+100s
  -   booking-service: SELECT booking_db/len s=57 kp=+70s
  -   api-gateway: latency-90/len s=349 kp=+30s, latency-50/len s=15.5 kp=+30s

## V041 -> V054-DM-V041-t-30 — dev2: so_voi xau_di, dK 0, ca đổi 5
### eb48d6b3 (BINH-THUONG) — đổi: verdict CAUSE_FOUND→NO_INTRINSIC_ANOMALY, k 1→0
- nhóm hạng 1: ['event-service'] → ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   event-service: event_db/len s=82.7 kp=+0s
- V054-DM-V041-t-30:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.5, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['api-gateway']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:ticket-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s
  -   ticket-service: workload/xuong s=48 kp=+0s
- V054-DM-V041-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:event-service; 3:booking-service; 4:payment-service
  -   api-gateway: workload/xuong s=111 kp=+10s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   event-service: GET /api/v1/events/{id}/len s=82.4 kp=-30s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.6 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.9 kp=-20s
  -   payment-service: workload/xuong s=0.72 kp=+10s
### 83073ed1 (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['ticket-service']
- V041:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V054-DM-V041-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   ticket-service: SELECT ticket_db/len s=169 kp=-30s
### 60166807 (CPU-BOOK-2) — đổi: hang_ky_vong 2.5→4.0, p3 1.0→0.0
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:booking-service; 3:ticket-service; 4:payment-service
  -   event-service: SELECT event_schema.tbl_event_images/len s=782 kp=+0s, Transaction.commit/len s=457 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=453 kp=+0s, SELECT event_schema.tbl_event_sectors/len s=444 kp=+0s
  -   booking-service: SELECT booking_schema.tbl_idempotency_requests/len s=759 kp=+0s, SELECT/len s=599 kp=+0s, UPDATE booking_schema.tbl_orders/len s=557 kp=+0s, POST /internal/v1/orders/{orderId}/purchase-snapshot/len s=318 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=318 kp=+0s, ticket_db/len s=167 kp=+0s, SELECT ticket_schema.tbl_issuances/len s=141 kp=+0s, SELECT ticket_schema.tbl_tickets/len s=56.1 kp=+10s
  -   payment-service: SELECT payment_schema.tbl_inbox_messages/len s=315 kp=+0s, SELECT payment_schema.tbl_payment_sagas/len s=227 kp=+0s, payment_db/len s=162 kp=+0s, SELECT payment_schema.tbl_payment_attempts/len s=158 kp=+0s
- V054-DM-V041-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:keycloak; 3:booking-service; 4:ticket-service
  -   event-service: SELECT event_schema.tbl_event_images/len s=773 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=455 kp=-10s, Transaction.commit/len s=448 kp=-20s, SELECT event_schema.tbl_event_sectors/len s=410 kp=-30s
  -   keycloak: SELECT keycloak_db.JGROUPS_PING/len s=763 kp=-20s, SELECT keycloak_db.OFFLINE_USER_SESSION/len s=307 kp=-20s, SELECT keycloak_db.OUTBOX_ENTRY/len s=199 kp=-20s, UPDATE keycloak_db.OFFLINE_USER_SESSION/len s=113 kp=-20s
  -   booking-service: SELECT booking_schema.tbl_idempotency_requests/len s=747 kp=-20s, POST /internal/v1/orders/{orderId}/purchase-snapshot/len s=331 kp=-20s, SELECT com.flashticket.booking_service.entity.TicketTypeInventory/len s=289 kp=-30s, booking_db/len s=275 kp=-30s
  -   ticket-service: SELECT ticket_db/len s=397 kp=-20s, TicketJobs.cancel/len s=196 kp=-30s, ticket_db/len s=160 kp=-20s, SELECT ticket_schema.tbl_issuances/len s=147 kp=-30s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.5→1.0, p1 0.0→1.0
- nhóm hạng 1: ['keycloak'] → ['event-service']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:api-gateway
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   api-gateway: workload/len s=79.3 kp=+10s, error/len s=3.6 kp=+10s, log_loi/len s=1
- V054-DM-V041-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:booking-service; 3:ticket-service; 4:api-gateway
  -   event-service: GET /api/v1/events/{id}/len s=114 kp=-30s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+10s, SELECT booking_schema.tbl_orders/len s=108 kp=-30s, SELECT booking_db/len s=71.7 kp=-20s
  -   ticket-service: TicketJobs.deliver/len s=11.2 kp=+20s, workload/xuong s=0.24 kp=+30s
  -   api-gateway: workload/len s=50.6 kp=+10s, error/len s=3.6 kp=+10s, log_loi/len s=1

## V041 -> V054-DM-V041-t-30 — t062: so_voi bang, dK 1, ca đổi 1
### a5539fba (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['ticket-service']
- V041:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V054-DM-V041-t-30:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:api-gateway; 2:booking-service; 2:booking_db
  -   ticket-service: SELECT ticket_db/len s=241 kp=-30s

## V041 -> V057-DM-V041-t+30 — dev2: so_voi xau_di, dK 0, ca đổi 5
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→2.5, p1 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['api-gateway']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:ticket-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s
  -   ticket-service: workload/xuong s=48 kp=+0s
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:event-service; 3:booking-service; 4:ticket-service
  -   api-gateway: workload/xuong s=110 kp=+30s, EVALSHA/len s=55.7 kp=+40s, error/len s=1.22 kp=+30s, log_loi/len s=0.903
  -   event-service: GET /api/v1/events/{id}/len s=50.1 kp=+30s, error/len s=1.2 kp=+30s, log_loi/len s=0.903
  -   booking-service: workload/xuong s=126 kp=+30s, SELECT booking_db/len s=38.1 kp=+30s, SELECT booking_schema.tbl_orders/len s=18.8 kp=+50s
  -   ticket-service: workload/xuong s=48 kp=+30s
### 6949870c (REDIS-BOOK) — đổi: hang_ky_vong 1.0→2.5, p1 1.0→0.0, canh_hang_ky_vong 2.0→30.5, canh_top3 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['payment-service']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:payment-service; 3:api-gateway; 4:booking_db
  -   booking-service: latency-50/len s=1.33e+03 kp=+10s, GET/len s=971 kp=+0s, latency-90/len s=657 kp=+10s, SET/len s=567 kp=+0s
  -   payment-service: INSERT payment_schema.tbl_payment_confirmations/len s=29.7 kp=+0s, latency-90/len s=22.1 kp=+10s
  -   api-gateway: latency-90/len s=1.1e+03 kp=+30s, latency-50/len s=12.3 kp=+30s
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:cache; 3:booking-service; 4:api-gateway
  -   payment-service: INSERT payment_schema.tbl_payment_confirmations/len s=24.1 kp=+50s, latency-90/len s=21.3 kp=+30s
  -   cache: mem/len s=7.56 kp=+190s
  -   booking-service: latency-50/len s=1.34e+03 kp=+30s, latency-90/len s=657 kp=+30s
  -   api-gateway: latency-90/len s=988 kp=+30s, latency-50/len s=10.2 kp=+30s
### 60166807 (CPU-BOOK-2) — đổi: hang_ky_vong 2.5→1.0, p1 0.0→1.0
- nhóm hạng 1: ['event-service'] → ['booking-service']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:booking-service; 3:ticket-service; 4:payment-service
  -   event-service: SELECT event_schema.tbl_event_images/len s=782 kp=+0s, Transaction.commit/len s=457 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=453 kp=+0s, SELECT event_schema.tbl_event_sectors/len s=444 kp=+0s
  -   booking-service: SELECT booking_schema.tbl_idempotency_requests/len s=759 kp=+0s, SELECT/len s=599 kp=+0s, UPDATE booking_schema.tbl_orders/len s=557 kp=+0s, POST /internal/v1/orders/{orderId}/purchase-snapshot/len s=318 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=318 kp=+0s, ticket_db/len s=167 kp=+0s, SELECT ticket_schema.tbl_issuances/len s=141 kp=+0s, SELECT ticket_schema.tbl_tickets/len s=56.1 kp=+10s
  -   payment-service: SELECT payment_schema.tbl_inbox_messages/len s=315 kp=+0s, SELECT payment_schema.tbl_payment_sagas/len s=227 kp=+0s, payment_db/len s=162 kp=+0s, SELECT payment_schema.tbl_payment_attempts/len s=158 kp=+0s
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:payment-service; 4:config-discovery
  -   booking-service: SELECT com.flashticket.booking_service.entity.EventSalesSnapshot/len s=6.43e+03 kp=+50s, SELECT booking_schema.tbl_idempotency_requests/len s=612 kp=+30s, UPDATE booking_schema.tbl_orders/len s=443 kp=+30s, SELECT com.flashticket.booking_service.entity.TicketTypeInventory/len s=275 kp=+40s
  -   event-service: SELECT event_schema.tbl_event_images/len s=593 kp=+30s, Transaction.commit/len s=395 kp=+30s, SELECT event_schema.tbl_event_layouts/len s=370 kp=+30s, SELECT event_schema.tbl_event_sectors/len s=363 kp=+30s
  -   payment-service: SELECT payment_schema.tbl_inbox_messages/len s=291 kp=+30s, SELECT payment_schema.tbl_payment_sagas/len s=209 kp=+30s, payment_db/len s=151 kp=+40s, SELECT payment_schema.tbl_charges/len s=143 kp=+30s
  -   config-discovery: POST/len s=219 kp=+50s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.5→4.0, p3 1.0→0.0
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:api-gateway
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   api-gateway: workload/len s=79.3 kp=+10s, error/len s=3.6 kp=+10s, log_loi/len s=1
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:booking-service; 3:event-service; 4:api-gateway
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=894 kp=+40s
  -   booking-service: workload/xuong s=126 kp=+30s, SELECT booking_schema.tbl_orders/len s=102 kp=+50s, SELECT booking_db/len s=69.3 kp=+30s
  -   event-service: GET /api/v1/events/{id}/len s=56.2 kp=+30s, workload/len s=4.92 kp=+30s, error/len s=3.66 kp=+30s, log_loi/len s=0.902
  -   api-gateway: workload/len s=79.3 kp=+30s, error/len s=3.6 kp=+30s, log_loi/len s=0.902
### 46aab4be (PAUSE-PAYMENT) — đổi: hang_ky_vong 1.0→3.0, p1 1.0→0.0
- nhóm hạng 1: ['payment-service'] → ['booking-service']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:api-gateway; 4:user-service
  -   payment-service: live-ms/len s=3e+03 kp=+10s, live-down/len s=1 kp=+10s
  -   booking-service: SELECT booking_schema.tbl_orders/len s=433 kp=+0s, SELECT booking_db/len s=311 kp=+0s, workload/xuong s=49 kp=+10s
  -   api-gateway: workload/xuong s=52.9 kp=+30s, log_loi/len s=1, error/len s=0.36 kp=+40s
  -   user-service: find user_db.tbl_organizer_applications/len s=28.7 kp=+90s, workload/xuong s=0.08 kp=+10s
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:payment-service; 4:user-service
  -   booking-service: SELECT booking_schema.tbl_orders/len s=435 kp=+50s, SELECT booking_db/len s=90.2 kp=+30s, workload/xuong s=48.5 kp=+30s
  -   api-gateway: workload/xuong s=51.9 kp=+30s, log_loi/len s=0.987, error/len s=0.36 kp=+40s
  -   payment-service: live-ms/len s=2.93e+03 kp=+30s, live-down/len s=1 kp=+30s
  -   user-service: workload/xuong s=0.08 kp=+30s

## V041 -> V057-DM-V041-t+30 — t062: so_voi xau_di, dK 0, ca đổi 2
### 1ad3afeb (EVENT-DB-LAT) — đổi: canh_hang_ky_vong 2.0→3.0
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 3:booking_db
  -   event-service: latency-90/len s=3.78e+03 kp=+10s, latency-50/len s=1.32e+03 kp=+10s, Transaction.commit/len s=688 kp=+0s, SELECT event_schema.tbl_event_images/len s=644 kp=+0s
  -   api-gateway: latency-50/len s=1.65e+03 kp=+30s, latency-90/len s=307 kp=+10s
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:config-discovery; 3:api-gateway; 4:booking-service
  -   event-service: latency-90/len s=4.14e+03 kp=+30s, latency-50/len s=1.32e+03 kp=+30s, SELECT event_schema.tbl_event_layouts/len s=530 kp=+40s, Transaction.commit/len s=485 kp=+60s
  -   config-discovery: POST/len s=11.6 kp=+60s
  -   api-gateway: latency-50/len s=1.33e+03 kp=+30s, latency-90/len s=264 kp=+30s
### f728fce2 (NET-GW-BOOK) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0, canh_hang_ky_vong 2.0→25.5, canh_top3 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['event-service']
- V041:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:api-gateway; 4:booking_db
  -   booking-service: E2:api-gateway->booking-service/len s=1.03e+03 kp=+0s
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=293 kp=+20s
  -   api-gateway: latency-90/len s=349 kp=+10s, latency-50/len s=15.5 kp=+30s
- V057-DM-V041-t+30:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 3:booking_db
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=302 kp=+30s
  -   api-gateway: latency-90/len s=349 kp=+30s, latency-50/len s=15.5 kp=+30s

## P7 -> V059-TG-P7-t-300 — dev2: so_voi xau_di, dK 1, ca đổi 12
### eb48d6b3 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['ticket-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:payment-service; 4:api-gateway
  -   booking-service: Session.persist com.flashticket.booking_service.entity.IdempotencyRequest/len s=83.2 kp=+0s, SELECT booking_schema.tbl_outbox_messages/len s=32.5 kp=+0s
  -   event-service: event_db/len s=82.7 kp=+0s
  -   payment-service: UPDATE payment_schema.tbl_outbox_messages/len s=12.1 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:ticket-service; 2:payment-service; 3:api-gateway; 3:booking-service
  -   ticket-service: SELECT ticket_db/len s=180 kp=-300s
  -   payment-service: PaymentSagaRepository.findRecoverableOrderIds/len s=25.5 kp=-290s
### 4af494a5 (EVENT-DB-LAT) — đổi: 
- nhóm hạng 1: ['payment-service'] → ['booking-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:event-service; 3:ticket-service; 4:keycloak
  -   payment-service: InboxMessageRepository.findById/len s=996 kp=+10s, Channel.waitForConfirms/len s=21.2 kp=+10s
  -   event-service: latency-50/len s=988 kp=+10s, Transaction.commit/len s=651 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=573 kp=+0s, SELECT event_schema.tbl_promotions/len s=565 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=262 kp=+0s
  -   keycloak: OutboxDrainerTask.run/len s=128 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:api-gateway; 3:booking_db
  -   booking-service: OrderRepository.findByIdAndBuyerSubject/len s=310 kp=-280s
  -   event-service: OutboxWorker.relay/len s=36.9 kp=-280s, latency-90/len s=1.95 kp=-290s
### 19b17e22 (CPU-BOOK-1) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['payment-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:payment-service; 4:ticket-service
  -   booking-service: SELECT booking_schema.tbl_ticket_type_inventory/len s=1.35e+03 kp=+0s, OrderRepository.findLockedByIdAndBuyerSubject/len s=902 kp=+0s, GET/len s=594 kp=+0s, PurchaseLimitRepository.findLockedById/len s=476 kp=+0s
  -   event-service: E2:api-gateway->event-service/len s=612 kp=+0s, event_db/len s=586 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=485 kp=+0s, SELECT event_schema.tbl_promotions/len s=265 kp=+0s
  -   payment-service: SELECT payment_schema.tbl_payment_confirmations/len s=262 kp=+0s, SELECT payment_schema.tbl_order_payment_snapshots/len s=225 kp=+0s, INSERT payment_schema.tbl_inbox_messages/len s=221 kp=+0s, Session.merge com.flashticket.payment_service.entity.InboxMessage/len s=217 kp=+0s
  -   ticket-service: SELECT ticket_schema.tbl_event_access_snapshots/len s=251 kp=+0s, ticket_db/len s=209 kp=+0s, SELECT ticket_db/len s=200 kp=+0s, UPDATE ticket_schema.tbl_ticket_deliveries/len s=183 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:api-gateway; 3:booking_db
  -   payment-service: PaymentWorker.selectEventRefundOrders/len s=17.7 kp=-290s, PaymentSagaRepository.findRecoverableOrderIds/len s=3.6 kp=-260s
  -   booking-service: INSERT booking_schema.tbl_orders/len s=17.3 kp=-290s, ticket.issued.v1 process/len s=13.2 kp=-300s
### e9c9679b (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→10.5, p1 1.0→0.0, p3 1.0→0.0
- nhóm hạng 1: ['event-service'] → ['payment-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:api-gateway; 3:booking-service; 4:payment-service
  -   event-service: GET /api/v1/events/{id}/len s=85.2 kp=+20s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   api-gateway: workload/xuong s=69.2 kp=+10s, EVALSHA/len s=67.9 kp=+0s, error/len s=1.2 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=127 kp=+30s, SELECT booking_db/len s=38.8 kp=+0s, SELECT booking_schema.tbl_orders/len s=19.8 kp=+50s, OrderRepository.currentDatabaseTime/len s=13.3 kp=+50s
  -   payment-service: SELECT payment_schema.tbl_payment_sagas/len s=8.03 kp=+10s, workload/xuong s=0.72 kp=+10s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:user-service; 4:api-gateway
  -   payment-service: SELECT payment_schema.tbl_charges/len s=71.7 kp=-300s, RefundRepository.findIdsToPoll/len s=44.4 kp=-230s, INSERT payment_schema.tbl_payment_sagas/len s=14.3 kp=-300s, SELECT com.flashticket.payment_service.entity.PaymentSaga/len s=13.2 kp=-300s
  -   booking-service: Session.persist com.flashticket.booking_service.entity.Reservation/len s=32.7 kp=-280s
  -   user-service: latency-50/len s=5.33 kp=-290s
### 729604d2 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['payment-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 2:booking_db; 2:broker
  -   booking-service: Session.merge com.flashticket.booking_service.entity.PurchaseLimit/len s=5.67 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:keycloak; 3:booking-service; 4:user-service
  -   payment-service: ChargeRepository.existsByProviderAndMerchantAccountAndProviderChargeId/len s=171 kp=-300s, E2:ticket-service->payment-service/len s=28.4 kp=-290s
  -   keycloak: DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=40.5 kp=-300s
  -   booking-service: Session.merge com.flashticket.booking_service.entity.Order/len s=11.3 kp=-300s
  -   user-service: latency-90/len s=4.33 kp=-300s
### 6949870c (REDIS-BOOK) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['api-gateway']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:payment-service; 3:api-gateway; 4:booking_db
  -   booking-service: latency-50/len s=1.33e+03 kp=+10s, GET/len s=971 kp=+0s, latency-90/len s=657 kp=+10s, SET/len s=567 kp=+0s
  -   payment-service: RefundRepository.findIdsByState/len s=37.6 kp=+0s, PaymentWorker.pollRefunds/len s=31.1 kp=+130s, INSERT payment_schema.tbl_payment_confirmations/len s=29.7 kp=+0s, latency-90/len s=22.1 kp=+10s
  -   api-gateway: latency-90/len s=1.1e+03 kp=+30s, latency-50/len s=12.3 kp=+30s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:booking-service; 3:keycloak; 4:ticket-service
  -   api-gateway: GET event/len s=119 kp=-300s
  -   booking-service: SELECT booking_schema.tbl_orders/len s=73.1 kp=-300s, SELECT com.flashticket.booking_service.entity.Order/len s=23.2 kp=-300s
  -   keycloak: DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=39.2 kp=-290s
  -   ticket-service: INSERT ticket_schema.tbl_issuances/len s=28 kp=-300s
### 5fb8208f (NET-GW-BOOK) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['api-gateway']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:payment-service; 3:api-gateway; 4:booking_db
  -   booking-service: E2:api-gateway->booking-service/len s=535 kp=+0s, OrderRepository.findEventIdById/len s=156 kp=+10s, booking_db/len s=110 kp=+0s, INSERT booking_schema.tbl_reservations/len s=24.5 kp=+0s
  -   payment-service: PaymentSagaRepository.findRecoverableOrderIds/len s=10.2 kp=+0s, PaymentWorker.recoverSagas/len s=6.82 kp=+0s
  -   api-gateway: latency-90/len s=1.26e+03 kp=+30s, latency-50/len s=30.5 kp=+30s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:api-gateway; 2:ticket-service; 3:payment-service; 4:booking-service
  -   api-gateway: EVALSHA/len s=48.1 kp=-300s
  -   ticket-service: SELECT ticket_schema.tbl_tickets/len s=44 kp=-290s, latency-90/len s=5.08 kp=-260s
  -   payment-service: ticket.issuance-result.v1 process/len s=24.6 kp=-290s, PaymentWorker.pollRefunds/len s=9.88 kp=-260s
### 83073ed1 (BINH-THUONG) — đổi: verdict NO_INTRINSIC_ANOMALY→CAUSE_FOUND, k 0→1
- nhóm hạng 1: ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service'] → ['event-service']
- P7:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:booking-service; 3:api-gateway; 3:booking_db
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=55.7 kp=-300s, SELECT event_schema.tbl_ticket_types/len s=41 kp=-260s, latency-50/len s=2.75 kp=-80s
  -   booking-service: GET /api/v1/events/{eventId}/availability/len s=40 kp=-290s, UPDATE booking_schema.tbl_purchase_limits/len s=13.9 kp=-300s
### 60166807 (CPU-BOOK-2) — đổi: hang_ky_vong 1.0→2.0, p1 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:ticket-service; 4:payment-service
  -   booking-service: Session.persist com.flashticket.booking_service.entity.Reservation/len s=1.33e+03 kp=+20s, TicketTypeInventoryRepository.saveAll/len s=1.22e+03 kp=+40s, SELECT booking_schema.tbl_idempotency_requests/len s=759 kp=+0s, SELECT/len s=599 kp=+0s
  -   event-service: SELECT event_schema.tbl_event_images/len s=782 kp=+0s, Transaction.commit/len s=457 kp=+0s, SELECT event_schema.tbl_event_layouts/len s=453 kp=+0s, SELECT event_schema.tbl_event_sectors/len s=444 kp=+0s
  -   ticket-service: SELECT ticket_db/len s=318 kp=+0s, ticket_db/len s=167 kp=+0s, SELECT ticket_schema.tbl_issuances/len s=141 kp=+0s, UPDATE ticket_schema.tbl_ticket_deliveries/len s=98.6 kp=+0s
  -   payment-service: SELECT payment_schema.tbl_inbox_messages/len s=315 kp=+0s, SELECT payment_schema.tbl_payment_sagas/len s=227 kp=+0s, payment_db/len s=162 kp=+0s, SELECT payment_schema.tbl_payment_attempts/len s=158 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:booking-service; 3:payment-service; 4:api-gateway
  -   keycloak: DELETE keycloak_db.OUTBOX_ENTRY/len s=118 kp=-300s, SELECT org.keycloak.models.jpa.session.PersistentClientSessionEntity/len s=6.19 kp=-220s
  -   booking-service: OrderRepository.currentDatabaseTime/len s=78.4 kp=-290s, Session.find com.flashticket.booking_service.entity.EventSalesSnapshot/len s=10.6 kp=-300s
  -   payment-service: PaymentSagaRepository.findRecoverableOrderIds/len s=21.1 kp=-250s, PaymentWorker.recoverSagas/len s=6.67 kp=-230s
### 98ea5ba4 (HTTP5-EVENT-FLASH) — đổi: hang_ky_vong 2.0→10.0, p3 1.0→0.06666666666666667
- nhóm hạng 1: ['keycloak'] → ['payment-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:booking-service; 4:payment-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=962 kp=+0s
  -   event-service: GET /api/v1/events/{id}/len s=125 kp=+0s, workload/len s=4.92 kp=+10s, error/len s=3.66 kp=+10s, log_loi/len s=1
  -   booking-service: workload/xuong s=126 kp=+10s, SELECT booking_schema.tbl_orders/len s=101 kp=+10s, OrderRepository.currentDatabaseTime/len s=81.7 kp=+10s, SELECT booking_db/len s=72.4 kp=+0s
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=24.1 kp=+0s, workload/xuong s=0.72 kp=+10s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:api-gateway; 3:booking_db
  -   payment-service: PaymentConfirmationRepository.findById/len s=45.6 kp=-300s, PaymentWorker.recoverSagas/len s=4.39 kp=-260s
  -   booking-service: GET /api/v1/events/{eventId}/availability/len s=35.6 kp=-300s
### 46aab4be (PAUSE-PAYMENT) — đổi: hang_ky_vong None→10.0, p3 0.0→0.06666666666666667
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:user-service; 4:config-discovery
  -   booking-service: SELECT booking_schema.tbl_orders/len s=433 kp=+0s, SELECT booking_db/len s=311 kp=+0s, OrderRepository.currentDatabaseTime/len s=200 kp=+0s, workload/xuong s=49 kp=+10s
  -   api-gateway: workload/xuong s=52.9 kp=+30s, log_loi/len s=1, error/len s=0.36 kp=+40s
  -   user-service: find user_db.tbl_organizer_applications/len s=28.7 kp=+90s, workload/xuong s=0.08 kp=+10s
  -   config-discovery: workload/xuong s=2.3 kp=+10s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:booking_db; 3:broker
  -   booking-service: OrderExpiryWorker.expireDueOrders/len s=121 kp=-280s, basic.ack/len s=16.9 kp=-280s, latency-50/len s=2.78 kp=-290s
  -   api-gateway: latency-50/len s=2.29 kp=-300s
### f20b0ca5 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['booking-service'] → ['payment-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:payment-service; 3:api-gateway; 3:booking_db
  -   booking-service: UPDATE booking_schema.tbl_purchase_limits/len s=53.4 kp=+10s
  -   payment-service: SELECT payment_schema.tbl_order_payment_snapshots/len s=43.9 kp=+0s, OutboxMessageRepository.findFirstByAggregateIdAndMessageTypeInOrderByOccurredAtDescMessageIdDesc/len s=18.7 kp=+40s, PaymentSagaRepository.findRecoverableOrderIds/len s=10.7 kp=+70s, Session.find com.flashticket.payment_service.entity.PaymentAttempt/len s=5.28 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:ticket-service; 3:api-gateway; 3:booking-service
  -   payment-service: SELECT/len s=11.8 kp=-180s, PaymentWorker.pollRefunds/len s=5.05 kp=-220s
  -   ticket-service: TicketJobs.publish/len s=11.7 kp=-300s

## P7 -> V059-TG-P7-t-300 — t062: so_voi xau_di, dK 0, ca đổi 7
### 00eaea92 (FLASH-HEALTHY) — đổi: 
- nhóm hạng 1: ['payment-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:payment-service; 2:booking-service; 3:event-service; 4:ticket-service
  -   payment-service: OutboxMessageRepository.findDueForUpdate/len s=144 kp=+10s, SELECT payment_schema.tbl_outbox_messages/len s=46.3 kp=+10s, workload/len s=5.5 kp=+30s, PaymentWorker.selectEventRefundOrders/len s=3.96 kp=+0s
  -   booking-service: workload/len s=139 kp=+0s
  -   event-service: workload/len s=6.26 kp=+10s
  -   ticket-service: error/len s=5.2 kp=+30s, workload/len s=5.2 kp=+30s, log_loi/len s=0.659
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:payment-service; 3:api-gateway; 3:booking-service
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=226 kp=-230s, DELETE keycloak_db.OUTBOX_ENTRY/len s=106 kp=-290s, SELECT keycloak_db.OFFLINE_USER_SESSION/len s=101 kp=-230s
  -   payment-service: PaymentWorker.recoverSagas/len s=46.4 kp=-250s
### 2e2a5541 (SLOW-BOOK) — đổi: hang_ky_vong 1.0→10.5, p1 1.0→0.0, p3 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:keycloak; 3:payment-service; 4:api-gateway
  -   booking-service: latency-50/len s=1.76e+04 kp=+30s, latency-90/len s=1.31e+04 kp=+30s, GET /api/v1/orders/{orderId}/len s=1.08e+04 kp=+0s, SELECT booking_schema.tbl_orders/len s=252 kp=+0s
  -   keycloak: DELETE org.keycloak.models.jpa.entities.OutboxEntryEntity/len s=184 kp=+30s
  -   payment-service: SELECT payment_schema.tbl_order_payment_snapshots/len s=85.6 kp=+30s, SELECT payment_schema.tbl_payment_sagas/len s=38.7 kp=+30s, SELECT payment_schema.tbl_refunds/len s=29.6 kp=+10s, PaymentWorker.selectEventRefundOrders/len s=8.66 kp=+70s
  -   api-gateway: latency-90/len s=1.47e+03 kp=+10s, latency-50/len s=21.8 kp=+40s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:ticket-service; 3:payment-service; 4:api-gateway
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=1.44e+03 kp=-300s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=281 kp=-300s
  -   ticket-service: UPDATE ticket_schema.tbl_tickets/len s=161 kp=-300s
  -   payment-service: SELECT payment_schema.tbl_payment_confirmations/len s=51.1 kp=-290s
### 6c1a9fd8 (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['event-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:user-service; 3:api-gateway; 3:booking-service
  -   event-service: OutboxWorker.relay/len s=8.62 kp=+10s
  -   user-service: find user_db.tbl_organizer_applications/len s=6.8 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:payment-service; 3:api-gateway; 4:booking-service
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=335 kp=-230s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=61.8 kp=-230s
  -   payment-service: PaymentWorker.publishOutbox/len s=20.7 kp=-300s, PaymentWorker.selectEventRefundOrders/len s=12.9 kp=-260s
  -   api-gateway: latency-90/len s=1.71 kp=-290s
### a89954d1 (HTTP5-EVENT) — đổi: hang_ky_vong 1.0→9.0, p1 1.0→0.058823529411764705, p3 1.0→0.17647058823529413, verdict CAUSE_FOUND→NO_INTRINSIC_ANOMALY
- nhóm hạng 1: ['event-service'] → ['api-gateway', 'booking-service', 'booking_db', 'broker', 'cache', 'config-discovery', 'event-service', 'event_db', 'keycloak', 'keycloak_db', 'mongodb-instance', 'payment-service', 'payment_db', 'postgresql-shared-instance', 'ticket-service', 'ticket_db', 'user-service']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:keycloak; 3:payment-service; 4:api-gateway
  -   event-service: GET /api/v1/events/{id}/len s=664 kp=+0s, event_db/len s=88.9 kp=+0s, error/len s=2.84 kp=+10s, log_loi/len s=1
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=644 kp=+120s, SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=119 kp=+120s
  -   payment-service: SELECT com.flashticket.payment_service.entity.OrderPaymentSnapshot/len s=163 kp=+10s, RefundRepository.findAllByOrderIdOrderByCreatedAtAscIdAsc/len s=11.6 kp=+10s
  -   api-gateway: GET event/len s=23.9 kp=+0s, error/len s=13.4 kp=+10s, log_loi/len s=0.833
- V059-TG-P7-t-300:
  - verdict NO_INTRINSIC_ANOMALY
  - hạng: 1:api-gateway; 1:booking-service; 1:booking_db; 1:broker
### bf17acbf (CPU-BOOK) — đổi: hang_ky_vong 1.0→10.5, p1 1.0→0.0, p3 1.0→0.0
- nhóm hạng 1: ['booking-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:api-gateway; 3:event-service; 4:keycloak
  -   booking-service: Transaction.commit/len s=9.25e+03 kp=+0s, OutboxMessageRepository.findByMessageTypeInAndPublishedAtIsNullAndNextAttemptAtLessThanEqualOrderByOccurredAtAscMessageIdAsc/len s=2.31e+03 kp=+0s, SELECT booking_schema.tbl_order_items/len s=1.49e+03 kp=+0s, cpu/len s=1.43e+03 kp=+40s
  -   api-gateway: GET event/len s=708 kp=+0s, EVALSHA/len s=201 kp=+0s, GET booking/len s=157 kp=+0s, latency-50/len s=116 kp=+10s
  -   event-service: Transaction.commit/len s=615 kp=+0s, SELECT event_schema.tbl_event_images/len s=297 kp=+0s, SELECT event_schema.tbl_promotions/len s=288 kp=+0s, SELECT event_schema.tbl_ticket_types/len s=249 kp=+0s
  -   keycloak: SELECT keycloak_db.OUTBOX_ENTRY/len s=492 kp=+0s, SELECT keycloak_db.OFFLINE_USER_SESSION/len s=104 kp=+30s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:event-service; 3:payment-service; 4:api-gateway
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=2.48e+03 kp=-240s, SELECT keycloak_db.JGROUPS_PING/len s=5.78 kp=-220s
  -   event-service: SELECT event_schema.tbl_event_images/len s=59.5 kp=-300s, latency-50/len s=3.42 kp=-290s
  -   payment-service: PaymentSagaRepository.findRecoverableOrderIds/len s=18.4 kp=-300s
### e8661e0a (BINH-THUONG) — đổi: 
- nhóm hạng 1: ['event-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:event-service; 2:ticket-service; 3:api-gateway; 3:booking-service
  -   event-service: SELECT event_schema.tbl_event_sectors/len s=119 kp=+0s, SELECT event_schema.tbl_outbox_messages/len s=34.6 kp=+0s
  -   ticket-service: TicketJobs.cancel/len s=57.9 kp=+0s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:payment-service; 3:booking-service; 4:api-gateway
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=291 kp=-290s, SELECT keycloak_db.JGROUPS_PING/len s=6.67 kp=-280s
  -   payment-service: Transaction.commit/len s=82.1 kp=-300s
  -   booking-service: SELECT booking_db/len s=24 kp=-300s
### f728fce2 (NET-GW-BOOK) — đổi: hang_ky_vong 1.0→7.333333333333333, p1 1.0→0.0, p3 1.0→0.13333333333333333
- nhóm hạng 1: ['booking-service'] → ['keycloak']
- P7:
  - verdict CAUSE_FOUND
  - hạng: 1:booking-service; 2:event-service; 3:keycloak; 4:api-gateway
  -   booking-service: E2:api-gateway->booking-service/len s=1.03e+03 kp=+0s
  -   event-service: SELECT event_schema.tbl_outbox_messages/len s=293 kp=+20s
  -   keycloak: SELECT keycloak_db.OFFLINE_USER_SESSION/len s=178 kp=+100s
  -   api-gateway: latency-90/len s=349 kp=+10s, latency-50/len s=15.5 kp=+30s
- V059-TG-P7-t-300:
  - verdict CAUSE_FOUND
  - hạng: 1:keycloak; 2:payment-service; 3:api-gateway; 3:booking-service
  -   keycloak: SELECT org.keycloak.models.jpa.session.PersistentUserSessionEntity/len s=132 kp=-260s, SELECT keycloak_db.OFFLINE_USER_SESSION/len s=52.3 kp=-240s
  -   payment-service: Transaction.commit/len s=102 kp=-300s, PaymentWorker.recoverSagas/len s=29 kp=-300s

