# -*- coding: utf-8 -*-
"""T-063 — bản máy đọc của results/T-063/o-dev-bo-sung.md (SPEC T-063 "Đầu ra"). Không thêm định nghĩa mới: mỗi trường
chép từ bảng trong file .md hoặc tệp nguồn ghi ở `nguon`. Tập chấp nhận phía chấm của T-064 nằm ở results/T-064/dap-an-*.json.
Dùng: py -3 -B results/T-063/dong-goi/tao_o_dev_bo_sung_json.py"""
import datetime as dt, hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parents[3]
def sh(p): return hashlib.sha256((R / p).read_bytes()).hexdigest()
NG = ['results/T-063/o-dev-bo-sung.md', 'results/T-063/chay/xac-nhan-ca-2.json', 'results/T-063/thu3/xac-nhan-ca-3-sua-sau.json',
      'results/T-063/thu3/dieu-kien-xac-nhan-3.md', 'results/T-064/dap-an-dev2.json']
o = [
 {'ma': 'POOL-EVENT', 'huong': 'H3', 'ban_trien_khai': 'bản 3', 'cach_tiem': "hook pool.hold Event (RcaFaults.java, commit e557307), 5 connection / pool max 5, 600 s",
  'dau_do': 'audit pool.hold.started; db_client_connections_usage{state=used}, pending_requests', 'tap_chap_nhan': ['event-service'],
  'xac_nhan': {'trang_thai': 'xác nhận', 'nguon': 'results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/86dea661'}, 'why': ['WHY-90', 'WHY-91']},
 {'ma': 'CONSUMER-BOOK-SLOW', 'huong': 'H4', 'ban_trien_khai': 'bản 2', 'cach_tiem': 'toxiproxy booking-amqp, tải ×1',
  'tap_chap_nhan': ['booking-service'], 'canh_goc': ['booking-service', 'broker', 'message'],
  'xac_nhan': {'trang_thai': 'không xác nhận (đợt 2, 3 lần); không thu lại ở ×1', 'nguon': 'results/T-063/thu3/BAN-GIAO-B.md §2'}},
 {'ma': 'CONSUMER-BOOK-SLOW-X3', 'huong': 'H4', 'ban_trien_khai': 'bản 3', 'cach_tiem': 'toxic bandwidth downstream booking-amqp 1 KB/s, 600 s, tải ×3 suốt chu kỳ',
  'dau_do': 'rabbitmqctl ready/unacked booking.*.q, send_oct kết nối Booking',
  'tap_chap_nhan': 'chờ Minh: {booking-service} (khai trước) hoặc {booking-service, broker}', 'canh_goc': ['booking-service', 'broker', 'message'],
  'xac_nhan': {'trang_thai': 'xác nhận', 'nguon': 'results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/659a9dfb'}, 'why': ['WHY-90', 'WHY-92']},
 {'ma': 'BINH-THUONG-X3', 'huong': 'đối chứng H4 (ca không lỗi, ×3)', 'ban_trien_khai': 'bản 3', 'cach_tiem': 'không can thiệp, tải ×3',
  'tap_chap_nhan': None, 'xac_nhan': {'trang_thai': 'xác nhận theo Sửa sau 1 (Minh nhận 14/11)', 'nguon': 'results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/1e5a3dc5'}, 'why': ['WHY-92', 'WHY-93']},
 {'ma': 'RECREATE-PAY', 'huong': 'H8-adapter', 'ban_trien_khai': 'bản 3', 'cach_tiem': 'docker compose up -d --force-recreate --no-deps payment-service tại t, cùng image/env',
  'dau_do': 'docker inspect Id/StartedAt; httpcheck :8083 (mẫu thô)', 'tap_chap_nhan': ['payment-service'],
  'xac_nhan': {'trang_thai': 'xác nhận theo Sửa sau 2 (Minh nhận 14/11)', 'nguon': 'results/T-063/thu3/xac-nhan-ca-3-sua-sau.json#/ca/ebd5ef38'}, 'why': ['WHY-93']},
 {'ma': 'PAUSE-PAYMENT', 'huong': 'H5', 'ban_trien_khai': 'bản 2', 'cach_tiem': 'docker pause payment-service',
  'dau_do': 'httpcheck liveness, docker state Paused', 'tap_chap_nhan': ['payment-service'],
  'xac_nhan': {'trang_thai': 'xác nhận theo Sửa sau 1 của đợt 2 (Minh nhận 13/11)', 'nguon': 'results/T-063/chay/xac-nhan-ca-2.json'}},
 {'ma': 'SLOW-BOOK-FLASH', 'huong': 'H7', 'cach_tiem': 'SLOW-BOOK dưới tải ×3', 'tap_chap_nhan': ['booking-service'],
  'xac_nhan': {'trang_thai': 'không dùng — thay bằng HTTP5-EVENT-FLASH (WHY-83)', 'nguon': 'results/T-064/dap-an-dev2.json'}},
 {'ma': 'HTTP5-EVENT-FLASH', 'huong': 'H7', 'ban_trien_khai': 'bản 2', 'cach_tiem': 'cùng hook/đích HTTP5-EVENT dưới tải ×3 từ t', 'tap_chap_nhan': ['event-service'],
  'xac_nhan': {'trang_thai': 'xác nhận', 'nguon': 'results/T-063/chay/xac-nhan-ca-2.json'}, 'why': ['WHY-83']},
 {'ma': 'CPU-BOOK-1', 'huong': 'H2', 'ban_trien_khai': 'bản 2', 'cach_tiem': '1 luồng đốt trong cgroup Booking (quota 1,0)', 'tap_chap_nhan': ['booking-service'],
  'xac_nhan': {'trang_thai': 'xác nhận', 'nguon': 'results/T-063/chay/xac-nhan-ca-2.json'}},
 {'ma': 'CPU-BOOK-2', 'huong': 'H2', 'ban_trien_khai': 'bản 2', 'cach_tiem': '= CPU-BOOK T-062 (2 luồng)', 'tap_chap_nhan': ['booking-service'],
  'xac_nhan': {'trang_thai': 'xác nhận', 'nguon': 'results/T-063/chay/xac-nhan-ca-2.json'}},
]
out = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'muc_dich': 'ô dev bổ sung T-063 (vị trí khác ô đánh giá T-059); bản máy đọc của o-dev-bo-sung.md',
       'nguon_sha256': {p: sh(p) for p in NG}, 'o': o}
(R / 'results/T-063/o-dev-bo-sung.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(len(o))
