# -*- coding: utf-8 -*-
"""H6a — bỏ trace bảo trì nền của thư viện (T-064 H6).

Vấn đề (đã kiểm, `results/T-063/span-goc/PHAN-TICH.md`): FlashTicket có nhiều trace bắt đầu bằng một lời gọi CLIENT từ
luồng bảo trì của thư viện — pool kết nối (Hikari housekeeper/connection-adder, Agroal), service discovery (Eureka
heartbeat/cache refresh/replicator, TaskBatchingWorker), khám phá cụm (JGroups ping), health indicator (Redis INFO, Mongo
hello). Chúng không thuộc hành vi nghiệp vụ hay đường giao dịch; P7 coi mỗi thao tác của chúng là một đơn vị chấm.

Phép tính (đầu vào): trace có **span gốc** (không cha) là kind CLIENT và `thread.name` khớp tiền tố luồng bảo trì thư viện
(danh sách cố định dưới, suy từ tên luồng chuẩn của thư viện, không từ đáp án) → bỏ **toàn bộ trace** khỏi đầu vào span.
Không đụng trace bắt đầu bằng điểm vào HTTP, job `spring-scheduling` hay job Keycloak (`Timer-0`, dọn phiên) — đó là hành vi
ứng dụng, có thể là nguồn lỗi thật (outbox/Saga).
Điều kiện thất bại: lỗi thật biểu hiện **chỉ** ở trace bảo trì (vd. pool không tạo được kết nối) bị mất ở kênh span — kênh
pool (H3) và log phải bù. Thiếu thông tin luồng (span không có trong `bo_sung.span_phu`) → giữ span, đếm vào chẩn đoán.
Đối chứng: cùng bản không có H6a.
"""
from m1_ft.chay import ThanhPhan, dang_ky

TIEN_TO_LUONG = ('HikariPool-', 'agroal-', 'DiscoveryClient-', 'TaskBatchingWorker-', 'jgroups-', 'Timer runner-')
TEN_CLIENT_SUC_KHOE = ('INFO', 'hello admin', 'listDatabases admin')  # health indicator Redis/Mongo trên luồng event loop


@dang_ky
class BoTraceNen(ThanhPhan):
    ma = 'H6a-bo-trace-nen'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None

    def can_bo_sung(self):
        return ('span_phu',)

    def vao(self, inputs):
        spans = inputs[0]
        phu = (self.bo_sung or {}).get('span_phu')
        if phu is None:
            raise ValueError('H6a cần bo_sung.span_phu')
        tt = self.tham_so.get('tien_to_luong', TIEN_TO_LUONG)
        bo, thieu, ly_do = set(), 0, {}
        for s in spans:
            if s['parentSpanID']:
                continue
            p = phu.get(f"{s['traceID']}|{s['spanID']}")
            if p is None:
                thieu += 1
                continue
            luong = p.get('luong') or ''
            nen = p.get('kind') == 3 and (luong.startswith(tt) or
                                         (luong.startswith('lettuce-nioEventLoop') and s['operation'] in TEN_CLIENT_SUC_KHOE))
            if nen:
                bo.add(s['traceID'])
                ly_do[luong.split('-')[0]] = ly_do.get(luong.split('-')[0], 0) + 1
        moi = [s for s in spans if s['traceID'] not in bo]
        self.chan_doan = {'trace_bo': len(bo), 'span_bo': len(spans) - len(moi), 'goc_thieu_thong_tin': thieu,
                          'theo_tien_to_luong': ly_do}
        return [moi] + list(inputs[1:])

    def ra(self, rec, inputs, ctx):
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})[self.ma] = self.chan_doan
        return rec
