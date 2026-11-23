# -*- coding: utf-8 -*-
"""T-072 bước 1 — sinh `bieu-thuc.json` (nguồn duy nhất cho biểu thức luật cảnh báo W4).

Chạy: py -3 results/T-072/sinh_bieu_thuc.py  →  ghi results/T-072/bieu-thuc.json.
Bộ chấm offline (`cham_offline.py`) và bộ sinh file luật Grafana (bước 4) đọc file JSON này, không chép lại biểu thức.
Ngưỡng KHÔNG nằm ở đây: chỉ có tên tham số; giá trị tính máy móc từ dữ liệu E2 theo `quy-tac-chon-nguong.json` (bước 3).
"""
import json, pathlib

RA = pathlib.Path(__file__).with_name('bieu-thuc.json')

G = 'http_server_request_duration_seconds'
CUA_SO = '5m'            # khoảng nhìn lùi của rate/increase
CUA_SO_S = 300
SO_YC_TOI_THIEU = 30     # số request tối thiểu của route trong cửa sổ để luật được đánh giá
SO_5XX_TOI_THIEU = 3     # số 5xx tối thiểu trong cửa sổ để luật lỗi được phép kích hoạt
TUOI_DO_TOI_DA_S = 60    # lần dò mới nhất cũ hơn mức này = "thiếu lần dò"
ROUTES = ['booking', 'event', 'payment', 'ticket']   # mã route gateway có lưu lượng của bộ tải
URLS = [  # 8 đích của receiver httpcheck (observability/collector/agent-docker-host.yaml, lab 407b4f5)
    ('keycloak', 'http://10.0.0.158:8080/realms/master'),
    ('api-gateway', 'http://10.0.0.158:8081/actuator/health/liveness'),
    ('booking-service', 'http://127.0.0.1:8082/actuator/health/liveness'),
    ('payment-service', 'http://127.0.0.1:8083/actuator/health/liveness'),
    ('ticket-service', 'http://127.0.0.1:8084/actuator/health/liveness'),
    ('user-service', 'http://127.0.0.1:8085/actuator/health/liveness'),
    ('event-service', 'http://127.0.0.1:8086/actuator/health/liveness'),
    ('discovery-server', 'http://127.0.0.1:8761/actuator/health/liveness'),
]


def sel(route, them=''):
    return f'service_name="api-gateway",http_route="{route}"' + (',' + them if them else '')


def tong(route):
    return f'sum by (http_route) (increase({G}_count{{{sel(route)}}}[{CUA_SO}]))'


MA_5XX = 'http_response_status_code=~"5.."'


def so_5xx(route):
    return f'sum by (http_route) (increase({G}_count{{{sel(route, MA_5XX)}}}[{CUA_SO}]))'


def p95(route):
    return (f'histogram_quantile(0.95, sum by (http_route, le) (rate({G}_bucket{{{sel(route)}}}[{CUA_SO}]))) '
            f'and on (http_route) ({tong(route)} >= {SO_YC_TOI_THIEU})')


def ty_le_loi(route):
    # Chuỗi 5xx chỉ xuất hiện sau lỗi đầu tiên → "or 0 * tổng" để có giá trị 0 khi chưa từng có 5xx.
    return (f'(({so_5xx(route)} or on (http_route) 0 * {tong(route)}) / {tong(route)}) '
            f'and on (http_route) ({tong(route)} >= {SO_YC_TOI_THIEU}) '
            f'and on (http_route) (({so_5xx(route)} or on (http_route) 0 * {tong(route)}) >= {SO_5XX_TOI_THIEU})')


LAN_LOI = 'max by (http_url) (timestamp(httpcheck_error))'
LAN_PHAN_HOI = 'max by (http_url) (timestamp(httpcheck_status{http_status_code!=""}))'
LAN_BAT_KY = 'max by (http_url) (timestamp(httpcheck_error) or timestamp(httpcheck_status{http_status_code!=""}))'
LIVE = (f'((({LAN_LOI} > on (http_url) {LAN_PHAN_HOI}) or on (http_url) ({LAN_LOI} unless on (http_url) {LAN_PHAN_HOI})) '
        f'and on (http_url) ((time() - {LAN_LOI}) <= {TUOI_DO_TOI_DA_S})) * 0 + 1 '
        f'or on (http_url) ({LAN_PHAN_HOI} and on (http_url) ((time() - {LAN_PHAN_HOI}) <= {TUOI_DO_TOI_DA_S})) * 0')
_CU = f'((time() - {LAN_BAT_KY}) > {TUOI_DO_TOI_DA_S})'
LIVE_3 = (f'(((({LAN_LOI} > on (http_url) {LAN_PHAN_HOI}) or on (http_url) ({LAN_LOI} unless on (http_url) {LAN_PHAN_HOI})) * 0 + 1 '
          f'or on (http_url) {LAN_PHAN_HOI} * 0) unless on (http_url) {_CU}) '
          f'or on (http_url) ({_CU} * 0 + 2)')
DO_MOI = f'count((time() - {LAN_BAT_KY}) <= {TUOI_DO_TOI_DA_S})'
GW_MOI = f'time() - max(timestamp({G}_count{{service_name="api-gateway",http_route=~"{"|".join(ROUTES)}"}}))'


def luat(ma, loai, tieu_de, expr, dieu_kien, for_s, no_data, nhan, tham_so=None, ghi_chu=None):
    d = {'uid': ma, 'loai': loai, 'tieu_de': tieu_de, 'promql': expr, 'dieu_kien': dieu_kien,
         'for_s': for_s, 'no_data_state': no_data, 'exec_err_state': 'Error', 'keep_firing_for_s': 0, 'nhan': nhan}
    if tham_so:
        d['tham_so_nguong'] = tham_so
    if ghi_chu:
        d['ghi_chu'] = ghi_chu
    return d


rules = []
for r in ROUTES:
    rules.append(luat(f't072-p95-{r}', 'he-thong', f'p95 gateway route {r}', p95(r),
                      {'phep': '>', 'nguong': f'theta_p95_{r}', 'don_vi': 's'}, 60, 'OK',
                      {'t072_loai': 'he-thong', 't072_tin_hieu': 'p95', 'http_route': r, 'service_name': 'api-gateway'},
                      tham_so=f'theta_p95_{r}'))
for r in ROUTES:
    rules.append(luat(f't072-loi-{r}', 'he-thong', f'tỷ lệ 5xx gateway route {r}', ty_le_loi(r),
                      {'phep': '>', 'nguong': f'theta_loi_{r}', 'don_vi': 'tỷ lệ'}, 60, 'OK',
                      {'t072_loai': 'he-thong', 't072_tin_hieu': 'loi-5xx', 'http_route': r, 'service_name': 'api-gateway'},
                      tham_so=f'theta_loi_{r}'))
rules.append(luat('t072-live', 'he-thong', 'liveness: lần dò mới nhất là lỗi', LIVE,
                  {'phep': '>', 'nguong': 0.5, 'don_vi': '0 = dò tốt, 1 = dò lỗi'}, 20, 'OK',
                  {'t072_loai': 'he-thong', 't072_tin_hieu': 'live'},
                  ghi_chu='Đa chiều: một instance mỗi http_url. Không ngưỡng chọn từ dữ liệu (trạng thái nhị phân).'))
rules.append(luat('t072-mat-do', 'quan-sat', 'mất quan sát: thiếu lần dò liveness', DO_MOI,
                  {'phep': '<', 'nguong': len(URLS), 'don_vi': 'số đích có lần dò trong 60 s'}, 60, 'Alerting',
                  {'t072_loai': 'quan-sat', 't072_tin_hieu': 'mat-do'}))
rules.append(luat('t072-mat-gw', 'quan-sat', 'mất quan sát: histogram gateway không có mẫu mới', GW_MOI,
                  {'phep': '>', 'nguong': TUOI_DO_TOI_DA_S, 'don_vi': 's tuổi mẫu mới nhất'}, 60, 'Alerting',
                  {'t072_loai': 'quan-sat', 't072_tin_hieu': 'mat-gw'}))

doc = {
    'phien_ban': 'T072-bieu-thuc-1',
    'trang_thai': 'đề xuất, chốt trước E2 (cổng E2 điều kiện 3); chưa có ngưỡng',
    'sinh_boi': 'results/T-072/sinh_bieu_thuc.py',
    'nguon': {
        'prometheus': 'exp-obs, nhận OTLP (--web.enable-otlp-receiver), lookback-delta mặc định 5m (cờ không đặt trong observability/compose.yaml lab 407b4f5)',
        'histogram': f'{G}_bucket/_count, service_name="api-gateway", nhãn http_route = mã route Spring Cloud Gateway '
                     '(infrastructure/api-gateway/src/main/resources/application.yaml của FlashTicket 36a3725d)',
        'httpcheck': 'receiver httpcheck của Collector agent exp-app, collection_interval 10s, 8 đích',
        'khao_sat': 'results/T-072/khao-sat/ (truy vấn instant chỉ đọc 20/11, LOG phiên 1)',
    },
    'grafana': {
        'datasource_uid': 'prometheus',
        'eval_interval_s': 10,
        'nhom_luat': 't072-w4',
        'thu_muc': 'T-072 W4 cảnh báo',
        'truy_van': {'instant': True, 'relativeTimeRange': {'from': 600, 'to': 0}},
        'dieu_kien': 'A = PromQL (instant); C = Threshold trên A; condition = C',
        'ghi_chu': 'Grafana yêu cầu khoảng đánh giá là bội của 10 s; 10 s = nhịp mẫu histogram và nhịp dò.',
    },
    'tham_so_co_dinh': {
        'cua_so_rate': CUA_SO, 'cua_so_rate_s': CUA_SO_S,
        'so_yeu_cau_toi_thieu_5m': SO_YC_TOI_THIEU,
        'so_5xx_toi_thieu_5m': SO_5XX_TOI_THIEU,
        'tuoi_lan_do_toi_da_s': TUOI_DO_TOI_DA_S,
        'routes': ROUTES,
        'loi': 'http_response_status_code =~ 5..; không tính 4xx (401, 409, 429)',
        'p95': 'mọi mã trạng thái của route; histogram_quantile nội suy tuyến tính trong bucket; vượt bucket hữu hạn lớn nhất (10 s) trả 10',
        'bucket_le_s': [0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1, 2.5, 5, 7.5, 10],
    },
    'liveness_ba_trang_thai': {
        'dinh_nghia': 'Tại thời điểm đánh giá t, với mỗi http_url: lần dò mới nhất = mẫu mới nhất trong (t−300, t] của '
                      'httpcheck_error (dò lỗi) hoặc httpcheck_status có nhãn http_status_code (dò có phản hồi, mọi mã).',
        'trang_thai': {
            '0_do_tot': 'lần dò mới nhất có phản hồi và tuổi ≤ 60 s',
            '1_do_loi': 'lần dò mới nhất là lỗi và tuổi ≤ 60 s',
            '2_thieu_lan_do': 'không có lần dò nào tuổi ≤ 60 s (gồm không có mẫu trong 5 phút)',
        },
        'promql_3_trang_thai': LIVE_3,
        'ghi_chu': [
            'Khi đầu dò lỗi, receiver vẫn ghi httpcheck_status cho 5 lớp với giá trị 0 và KHÔNG có nhãn http_status_code '
            '(khảo sát PAUSE-PAYMENT 19/11); vì vậy "phản hồi" lọc theo http_status_code!="".',
            'Khi một đích treo, mọi đích chỉ được dò ~30 s một lần (scrape chờ timeout); 60 s ≥ 2 nhịp đó.',
            'Cùng ngữ nghĩa "lần dò mới nhất" với WHY-99 (kênh live-down của M1); khác: thêm tuổi tối đa 60 s để tách '
            '"thiếu lần dò" khỏi "dò tốt".',
            'promql_3_trang_thai trả 2 khi tuổi > 60 s (đích có mẫu trong 5 phút); đích không có mẫu nào trong 5 phút '
            'thì không có chuỗi → bộ chấm và luật t072-mat-do coi là 2.',
        ],
    },
    'luat': rules,
    'xuat_cho_T071': {
        'bat_buoc': [
            {'ten': f'tin-hieu/{x["uid"]}', 'promql': x['promql'], 'kieu': 'query_range', 'step_s': 10}
            for x in rules
        ] + [{'ten': 'tin-hieu/live-3-trang-thai', 'promql': LIVE_3, 'kieu': 'query_range', 'step_s': 10}]
          + [{'ten': f'phu/tong-{r}', 'promql': tong(r), 'kieu': 'query_range', 'step_s': 10} for r in ROUTES]
          + [{'ten': f'phu/5xx-{r}', 'promql': f'{so_5xx(r)} or on (http_route) 0 * {tong(r)}', 'kieu': 'query_range',
              'step_s': 10} for r in ROUTES]
          + [{'ten': f'phu/ty-le-loi-chua-chan-5xx-{r}',
              'promql': f'(({so_5xx(r)} or on (http_route) 0 * {tong(r)}) / {tong(r)}) and on (http_route) ({tong(r)} >= {SO_YC_TOI_THIEU})',
              'kieu': 'query_range', 'step_s': 10} for r in ROUTES],
        'vi_sao_phu': ('Luật lỗi chỉ có chuỗi khi ≥ 3 lỗi 5xx trong 5 phút, nên ở giờ khỏe thường không có điểm. Quy tắc chọn '
                       'ngưỡng và bộ chấm cần tỷ lệ, số 5xx và tổng request ở mọi bước; các chuỗi phu/* cho các giá trị đó.'),
        'khuyen_nghi_tho': [
            {'ten': 'tho/gw-bucket', 'selector': f'{G}_bucket{{service_name="api-gateway",http_route=~"{"|".join(ROUTES)}"}}'},
            {'ten': 'tho/gw-count', 'selector': f'{G}_count{{service_name="api-gateway"}}'},
            {'ten': 'tho/httpcheck-error', 'selector': 'httpcheck_error'},
            {'ten': 'tho/httpcheck-status-co-ma', 'selector': 'httpcheck_status{http_status_code!=""}'},
        ],
        'cach_xuat': ('query_range theo khúc ≤ 10 phút, nghỉ giữa khúc (I11); khoảng xuất phủ mỗi lượt từ 600 s trước '
                      'load-start tới hết lượt + 300 s; mẫu thô xuất bằng instant query `selector[10m]` theo khúc liền nhau, '
                      'giữ timestamp gốc. Mỗi khúc ghi số điểm, lỗi khúc; thiếu điểm ghi rõ, không nội suy.'),
        'kiem_xuat_duoc': 'mỗi chuỗi tin-hieu/* của route có lưu lượng có điểm ở mọi bước 10 s trong lúc có tải (trừ khi guard loại).',
    },
    'khong_phu': [
        'Route gateway không có lưu lượng của bộ tải (user, event-images, payment-vnpay-callbacks) và request không khớp '
        'route (nhãn http_route rỗng, ví dụ 401): không có luật, vì không có dữ liệu E2 để chọn ngưỡng.',
        'Lỗi không đi qua gateway hoặc không thành 5xx/độ trễ ở gateway (ví dụ hàng đợi RabbitMQ chậm sau khi request đã trả).',
        'Lần lỗi đầu tiên của một tổ hợp (route, mã 5xx) mới: chuỗi mới sinh ra với giá trị đã > 0, rate/increase không thấy '
        'phần tăng trước mẫu đầu (Prometheus không bật created-timestamp-zero-ingestion). Chỉ mất phần đầu, lỗi kéo dài vẫn thấy.',
        'Gateway khởi động lại: chuỗi mới theo container_id; sum by bỏ qua, nhưng mất phần tăng trước mẫu đầu như trên.',
    ],
}

RA.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(RA, len(rules), 'rules')
