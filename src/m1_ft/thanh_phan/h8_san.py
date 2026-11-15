# -*- coding: utf-8 -*-
"""H8-san — sàn độ lớn cho đơn vị phân vị của span (T-064 H8).

Vấn đề P7 (đã kiểm, `results/T-063/ca-nen/PHAN-TICH.md`): E4 đặt ngưỡng h = phân vị q_hi của N × (1 + ε), không có sàn độ
lớn tuyệt đối; với n vài trăm mẫu, thao tác nền dịch ~0,1 ms vẫn có p rất nhỏ → thành phần lên tầng 1.

Phép tính: sau `e4.cham_phan_vi` của đơn vị span (`op|…`, `canh|…`), với mỗi hướng đã gắn cờ, tính **độ vượt trung bình**
của các mẫu A nằm ngoài ngưỡng: hướng lên mean(x − h | x > h), hướng xuống mean(l − x | x < l). Nếu nhỏ hơn δ thì bỏ cờ
hướng đó (F_raw = 0, e = 0) — cùng cách S21 của P7 bỏ cờ đơn vị không hợp lệ. Đơn vị metric/log/đếm không đổi.

Nguyên lý chọn δ (ghi trước khi chấm, không theo đáp án): độ dịch nhỏ hơn hạt lập lịch CPU của nhân Linux trên máy dùng
chung (CFS: `sched_min_granularity` cỡ 0,75–3 ms; quantum thực tế cỡ ms) không phân biệt được với nhiễu lập lịch, nên mặc
định δ = 1 ms. Tham số `delta_ms` cho phép biến thể.
Điều kiện thất bại: lỗi thật có độ vượt trung bình < δ (vd. trễ mạng 0,5 ms) bị bỏ cờ; tải nặng làm mọi thao tác chậm ≥ δ
thì sàn không giúp. Đối chứng: cùng bản với δ = 0 (phải trùng P7).
"""
import contextlib
import math

from m1 import e4
from m1_ft.chay import ThanhPhan, dang_ky
from fractions import Fraction

NS = 10 ** 9
_HE = {'us': 1000, 'ns': 1, 's': NS}


@dang_ky
class SanDoLon(ThanhPhan):
    ma = 'H8-san'

    def vao(self, inputs):
        he = _HE[inputs[6]['don_vi_thoi_gian']['spans.start_us']]
        self.delta = float(self.tham_so.get('delta_ms', 1.0)) * 1e6 / he  # theo đơn vị thời gian của span
        return inputs

    @contextlib.contextmanager
    def ngu_canh(self):
        goc = e4.cham_phan_vi
        dem = {'don_vi_xet': 0, 'huong_bo_co': 0, 'don_vi_bo_co': [], 'delta_don_vi_span': self.delta}

        def boc(N, A, m, ts, huong_cham=('len', 'xuong'), cache=None, khoa_don_vi=None, **kw):
            kq = goc(N, A, m, ts, huong_cham=huong_cham, cache=cache, khoa_don_vi=khoa_don_vi, **kw)
            if not (isinstance(khoa_don_vi, str) and khoa_don_vi.startswith(('op|', 'canh|'))):
                return kq
            dem['don_vi_xet'] += 1
            moi = None
            for d in huong_cham:
                if not kq.get(f'F_raw_{d}'):
                    continue
                Ah = [float(x) for x in A if x is not None and math.isfinite(float(x))]
                if d == 'len':
                    vuot = [x - kq['h'] for x in Ah if x > kq['h']]
                else:
                    vuot = [kq['l'] - x for x in Ah if x < kq['l']]
                tb = sum(vuot) / len(vuot) if vuot else 0.0
                if tb < self.delta:
                    moi = dict(kq) if moi is None else moi  # không sửa đối tượng trong cache của E4
                    moi[f'F_raw_{d}'], moi[f'e_{d}'], moi[f'e_{d}_q'] = 0, 0.0, Fraction(0)
                    dem['huong_bo_co'] += 1
                    dem['don_vi_bo_co'].append({'ma': khoa_don_vi, 'huong': d, 'vuot_tb': tb})
            return moi if moi is not None else kq

        e4.cham_phan_vi = boc
        try:
            yield dem
        finally:
            e4.cham_phan_vi = goc

    def ra(self, rec, inputs, ctx):
        ft = rec.setdefault('extra', {}).setdefault('m1_ft', {})
        ft.setdefault('chu_thich', {})[self.ma] = {'delta_ms': self.tham_so.get('delta_ms', 1.0),
                                                  'don_vi_span_xet': ctx['don_vi_xet'], 'huong_bo_co': ctx['huong_bo_co'],
                                                  'don_vi_bo_co': ctx['don_vi_bo_co'][:200]}
        return rec
