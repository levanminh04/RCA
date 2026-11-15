# -*- coding: utf-8 -*-
"""T-063 thu3 — thêm hai cờ "Sửa sau" vào xac_nhan_ca_3.py (SAU KHI xem kết quả hậu kiểm lượt chính; dieu-kien-xac-nhan-3.md mục "Sửa sau").
--sua-sau-1: C0 coi BINH-THUONG-X3 là ô không lỗi (điều kiện khai trước đã đúng; script quên ô này trong bộ ô không lỗi của C0).
--sua-sau-2: RECREATE-PAY: "phục hồi" = không có MẪU THÔ httpcheck_error :8083 nào có thời điểm trong [t + 180, t + 570]
             (truy vấn range-vector, không dùng query_range vì lookback 5 phút giữ giá trị cũ của chuỗi đẩy).
Không có cờ: chạy y như bản đã chốt. Dùng: py -3 -B results/T-063/thu3/scripts/va_sua_sau.py (sửa tại chỗ, có assert)."""
p = 'D:/RCA-flashticket/results/T-063/thu3/scripts/xac_nhan_ca_3.py'
s = open(p, encoding='utf-8').read()


def thay(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)


thay("SUA_SAU_1 = False  # thu3 không có ô PAUSE",
     "SUA_SAU_1 = False  # thu3 không có ô PAUSE (cờ cũ của đợt 2)\n"
     "S3_1 = '--sua-sau-1' in sys.argv  # thu3 Sửa sau 1: C0 nhận BINH-THUONG-X3 là ô không lỗi\n"
     "S3_2 = '--sua-sau-2' in sys.argv  # thu3 Sửa sau 2: httpcheck RECREATE-PAY theo mẫu thô")
thay("(cell in ('BINH-THUONG', 'FLASH-HEALTHY') or ('fault-start' in ev and 'fault-stop' in ev)))",
     "(cell in (KHONG_LOI if S3_1 else ('BINH-THUONG', 'FLASH-HEALTHY')) or ('fault-start' in ev and 'fault-stop' in ev)))")
thay("""            dk['httpcheck_phuc_hoi_t180_t570'] = bool(r2) and max(r2) == 0""",
     """            dk['httpcheck_phuc_hoi_t180_t570'] = bool(r2) and max(r2) == 0
            if S3_2:
                ts_loi = prom_tho('httpcheck_error{http_url=~".*:8083.*"}', t + 570, 600)
                c['httpcheck_error_8083_mau_tho_tuong_doi_t'] = [round(x - t) for x in ts_loi]
                dk['httpcheck_phuc_hoi_t180_t570'] = not any(t + 180 <= x <= t + 570 for x in ts_loi)""")
thay("""def tb(v):""", """def prom_tho(sel, at, rng):
    \"\"\"Thời điểm (epoch) mọi mẫu thô của bộ chọn trong (at − rng, at]: truy vấn range-vector, không có lookback.\"\"\"
    sc = ('import json,urllib.parse,urllib.request\\nu="http://localhost:9090/api/v1/query?"+urllib.parse.urlencode('
          '{"query":%r,"time":%d})\\nr=json.load(urllib.request.urlopen(u,timeout=60))["data"]["result"]\\n'
          'print(json.dumps([float(x[0]) for s in r for x in s["values"]]))\\n') % (f'{sel}[{rng}s]', at)
    r = subprocess.run([SSH] + OBS + ['python3 -'], input=sc, capture_output=True, text=True, encoding='utf-8', timeout=180)
    if r.returncode != 0: raise RuntimeError('prom: ' + r.stderr[-300:])
    return json.loads(r.stdout)


def tb(v):""")
thay("""'ton_queue_booking_cac_dau_do', 'payment_container', 'httpcheck_error_8083_max_t_t120_va_t180_t570') if k in c}}""",
     """'ton_queue_booking_cac_dau_do', 'payment_container', 'httpcheck_error_8083_max_t_t120_va_t180_t570',
                                    'httpcheck_error_8083_mau_tho_tuong_doi_t') if k in c}}""")
thay("RA.write_text(json.dumps({'nguon': str(G), 'dieu_kien': 'results/T-063/thu3/dieu-kien-xac-nhan-3.md', 'sua_sau_1': SUA_SAU_1,",
     "RA.write_text(json.dumps({'nguon': str(G), 'dieu_kien': 'results/T-063/thu3/dieu-kien-xac-nhan-3.md', 'thu3_sua_sau_1': S3_1, 'thu3_sua_sau_2': S3_2,")
compile(s, p, 'exec')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
