# -*- coding: utf-8 -*-
"""H8-log — kênh log nghiệp vụ theo trường kết cục của hợp đồng B16 (T-064 H8; phiên C, 14/11/2026).

Dữ liệu (đã đếm, `results/T-064/phien-c/h8-log/dem-log-nghiep-vu.json`): log JSON của api-gateway, booking, payment,
ticket (và event-service khi lỗi) mang `outcome` ∈ {SUCCESS, REJECTED, RETRY, FAILED, UNKNOWN} (B16 §log, dòng 56) và
`reasonCode`. Nơi đặt: log ứng dụng (Collector filelog → Loki → gói ca `raw-logs.jsonl`), đọc bằng `bo_sung.log_phu`.
Nút: thực thể sở hữu bản ghi (service.name, cùng ánh xạ với adapter ghim). Không thêm cạnh; lan truyền theo lớp kênh của
M1 (E1/E5 dùng lớp như các kênh cùng loại).

Ngữ nghĩa kết cục (B16, không theo đáp án): SUCCESS hoàn tất; REJECTED bị từ chối theo luật nghiệp vụ (xác thực, giới
hạn tốc độ) — quyết định đúng của hệ thống, không phải hỏng hóc; RETRY lỗi tạm thời sẽ thử lại; FAILED thất bại cuối;
UNKNOWN kết cục không xác định. "Kết cục lỗi" = FAILED ∪ UNKNOWN. RETRY không tính lỗi (tương tự WARN: tự phục hồi).

H8-log-kq (phép tính trên kênh `log_loi` sẵn có của P7): dòng log có `outcome` được phân loại lỗi/không lỗi theo kết cục
thay vì severity (severity_raw → 'ERROR' nếu kết cục lỗi, 'INFO' nếu không); dòng không có `outcome` giữ nguyên. Cùng đơn
vị, cùng E4 đếm, cùng cổng D1, cùng lớp `lan_nguoc`. Lý do: trường kết cục là trường hợp đồng; severity do người viết
code chọn. Điều kiện thất bại: dịch vụ ghi FAILED cho lỗi của bên khác (triệu chứng phía gọi) — như `log_loi` của P7.

H8-log-chuoi (hai kênh metric mới, qua đường metric chung, cùng E4 phân vị + G3 như kênh metric khác):
- `log-kq-loi` (lớp "lỗi"): mỗi ô 15 s, số bản ghi kết cục lỗi / số bản ghi có outcome (ô trống → 0, như H7b).
- `log-kq-ok` (lớp "lưu lượng"): số bản ghi SUCCESS mỗi giây trong ô 15 s. Phủ cả việc xử lý bất đồng bộ (RabbitMQ: saga
  thanh toán, phát vé) mà kênh `workload` HTTP của P7 không thấy.
Ô 15 s đóng dấu ở **đầu ô** [a, a + 15) nên ô chứa mốc t thuộc A, không trộn N/A. Lưới bắt đầu tại t − 300.
Điều kiện thất bại: dịch vụ chỉ ghi log khi lỗi (event-service) → N không có bản ghi, mọi ô N = 0; tải thay đổi làm
`log-kq-ok` đổi theo tải (như workload, H7 không áp cho kênh này).
Đối chứng: bản cha không có thành phần. Không dùng nhãn, tên ca, mốc tiêm ngoài t.
"""
from m1_ft.chay import ThanhPhan, dang_ky

KQ_LOI = frozenset({'FAILED', 'UNKNOWN'})
KQ_HOP_LE = frozenset({'SUCCESS', 'REJECTED', 'RETRY', 'FAILED', 'UNKNOWN'})
NS = 10 ** 9


@dang_ky
class LogKetCuc(ThanhPhan):
    ma = 'H8-log-kq'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None
        self.cd = {}

    def can_bo_sung(self):
        return ('log_phu',)

    def vao(self, inputs):
        spans, metrics, logs, inventory, aliases, t, params = inputs
        cho = {}
        for r in self.bo_sung['log_phu']:
            k = (r['timestamp'], r['entity'], r['message'], r['severity_raw'])
            cho.setdefault(k, []).append(r['outcome'])
        for v in cho.values():
            v.sort(key=lambda o: (o is None, str(o)))
        moi, doi = [], {'len_loi': 0, 'xuong_khong_loi': 0, 'giu': 0, 'co_outcome': 0, 'outcome_la': 0}
        theo_tt = {}
        loi = set(params['ho_so_nguon']['quy_tac_log']['loi'])
        for r in logs:
            k = (r['timestamp'], r['entity'], r['message'], r['severity_raw'])
            ds = cho.get(k)
            if not ds:
                raise ValueError('H8-log-kq: dòng log đầu vào không ghép được với log thô')
            o = ds.pop(0)
            if o is None or o not in KQ_HOP_LE:
                doi['giu'] += 1; doi['outcome_la'] += int(o is not None)
                moi.append(r); continue
            doi['co_outcome'] += 1
            sev = 'ERROR' if o in KQ_LOI else 'INFO'
            truoc = (str(r['severity_raw']).strip().upper() if isinstance(r['severity_raw'], str) else '') in loi
            if (sev == 'ERROR') != truoc:
                c = theo_tt.setdefault(r['entity'], {'len_loi': 0, 'xuong_khong_loi': 0})
                kieu = 'len_loi' if sev == 'ERROR' else 'xuong_khong_loi'
                doi[kieu] += 1; c[kieu] += 1
            moi.append(dict(r, severity_raw=sev))
        con = sum(len(v) for v in cho.values())
        if con:
            raise ValueError(f'H8-log-kq: {con} bản ghi log thô không có dòng đầu vào tương ứng')
        self.cd = dict(doi, theo_thuc_the=theo_tt, so_dong=len(logs))
        return [spans, metrics, moi, inventory, aliases, t, params]

    def ra(self, rec, inputs, ctx):
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})[self.ma] = self.cd
        return rec


@dang_ky
class LogChuoiKetCuc(ThanhPhan):
    ma = 'H8-log-chuoi'
    BUOC = 15

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None
        self.cd = {}

    def can_bo_sung(self):
        return ('log_phu', 'bundles')

    def kenh_moi(self):
        return {'log-kq-loi': 'lỗi', 'log-kq-ok': 'lưu lượng'}

    def bien_doi_bundle(self, bundles, inputs):
        t = int(inputs[5]); b0 = t - 300; so_o = 600 // self.BUOC
        dem = {}
        for r in self.bo_sung['log_phu']:
            o = r['outcome']
            if o not in KQ_HOP_LE or r['entity'] is None:
                continue
            i = (r['timestamp'] - b0 * NS) // (self.BUOC * NS)
            if not 0 <= i < so_o:
                continue
            c = dem.setdefault(r['entity'], [[0, 0, 0] for _ in range(so_o)])  # [tổng, lỗi, success]
            c[i][0] += 1; c[i][1] += int(o in KQ_LOI); c[i][2] += int(o == 'SUCCESS')
        loi, ok = [], []
        for sv in sorted(dem):
            v = dem[sv]
            moc = [str(b0 + k * self.BUOC) for k in range(so_o)]
            loi.append({'metric': {'service_name': sv},
                        'values': [[m, repr(x[1] / x[0] if x[0] else 0.0)] for m, x in zip(moc, v)]})
            ok.append({'metric': {'service_name': sv},
                       'values': [[m, repr(x[2] / self.BUOC)] for m, x in zip(moc, v)]})
        q = '(log nghiệp vụ B16, phiên C)'
        them = [{'channel': 'log-kq-loi', 'native': False, 'query': q, 'step_seconds': self.BUOC, 'result': loi,
                 'native_timestamps': None},
                {'channel': 'log-kq-ok', 'native': False, 'query': q, 'step_seconds': self.BUOC, 'result': ok,
                 'native_timestamps': None}]
        self.cd = {'thuc_the': sorted(dem), 'ban_ghi': {sv: sum(x[0] for x in v) for sv, v in sorted(dem.items())},
                   'ket_cuc_loi': {sv: sum(x[1] for x in v) for sv, v in sorted(dem.items())}}
        return [b for b in bundles if b['channel'] not in self.kenh_moi()] + them

    def ra(self, rec, inputs, ctx):
        co = [k['don_vi'] for k in (rec.get('extra') or {}).get('kenh_co', [])
              if any(k['don_vi'].endswith('_' + c) for c in self.kenh_moi())]
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})[self.ma] = dict(
            self.cd, chan_doan_metric=getattr(self, 'chan_doan_metric', None), don_vi_co_co=co)
        return rec
