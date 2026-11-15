# -*- coding: utf-8 -*-
"""H7 — chuẩn hóa theo tải (T-064 H7: "tải tăng so với sự cố").

Vấn đề P7 (đã kiểm, `results/T-062/chay/thu-gia/LAN-CA-NEN.md` §1, ca FLASH): kênh `workload` của mọi service tăng
5→15 req/s bị chấm là bất thường tự sinh; kênh `error` là **số** lỗi 5xx/s nên tăng theo tải dù tỷ lệ lỗi không đổi.

Phép tính (đầu vào metric, ở mức bundle của gói ca rồi dựng lại bằng `m1.adapter_flashticket.normalize_metrics` — cùng code
ghim, nên mọi bất biến nguồn/mốc/chỉ số hàng giữ nguyên):
- H7a `bo_luu_luong_ngoai`: điểm vào E = thành phần sở hữu nhiều span gốc SERVER nhất trong cửa sổ (từ `bo_sung.span_phu`).
  ρ_x = trung bình workload ở A / ở N. Nếu ρ_E ≥ 1 + τ (lưu lượng vào tăng), mọi thành phần x có ρ_x/ρ_E trong [1/κ, κ]
  được coi là tăng **do tải ngoài**: bỏ chuỗi workload của x khỏi đầu vào. Thành phần lệch khỏi tỷ lệ (vd. vòng thử lại tự
  sinh) vẫn giữ kênh. Mặc định τ = 0,2; κ = 1,5.
- H7b `ty_le_loi`: thay chuỗi `error` (số 5xx/s) của mỗi service bằng tỷ lệ 5xx/tổng request tại cùng mốc đánh giá
  (hai truy vấn cùng bước); workload = 0 thì tỷ lệ 0 nếu error = 0, ngược lại bỏ điểm. Nguyên lý SRE: SLI lỗi là tỷ lệ.
- H7c `log_theo_luu_luong` (mặc định tắt): với thành phần x thuộc tập H7a (tăng theo tải ngoài), số dòng log lỗi ở A
  chia cho ρ_x và làm tròn về số nguyên trước khi chấm (`m1.kenh.don_vi_log` được bọc trong lúc chạy) — tức so **tỷ lệ dòng lỗi trên request**
  N với A, cùng nguyên lý SLI của H7b. Thành phần không thuộc tập H7a giữ số đếm thô.
Điều kiện thất bại: lỗi gây tăng lưu lượng tỷ lệ đều (vd. retry đều ở mọi service) bị coi là tải ngoài; tỷ lệ lỗi bị nhiễu
ở mức tải rất thấp. Đối chứng: cùng bản không có H7; `chi_dung_lai` = true (không biến đổi) phải trùng P7.
"""
import contextlib
import math

from m1 import adapter_flashticket as ad
from m1 import kenh as m1kenh
from m1_ft.chay import ThanhPhan, dang_ky


def _tb(values, lo, hi):
    xs = [float(v) for t, v in values if lo <= float(t) < hi and v is not None and math.isfinite(float(v))]
    return sum(xs) / len(xs) if xs else None


@dang_ky
class ChuanHoaTai(ThanhPhan):
    ma = 'H7-tai'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None

    def can_bo_sung(self):
        return ('span_phu', 'bundles')

    def bien_doi_bundle(self, bundles, inputs):
        spans, metrics, logs, inventory, aliases, t, params = inputs
        bs = self.bo_sung or {}
        bundles = [dict(b) for b in bundles]
        ts = self.tham_so
        cd = {'diem_vao': None, 'rho': {}, 'bo_workload': [], 'ty_le_loi': False}
        self.rho_log = {}
        if not ts.get('chi_dung_lai'):
            phu = bs['span_phu']
            dem = {}
            for s in spans:
                if not s['parentSpanID']:
                    p = phu.get(f"{s['traceID']}|{s['spanID']}")
                    if p and p.get('kind') == 2:
                        dem[s['owner']] = dem.get(s['owner'], 0) + 1
            E = max(sorted(dem), key=lambda k: dem[k]) if dem else None
            cd['diem_vao'] = E
            wl = next((b for b in bundles if b['channel'] == 'workload'), None)
            er = next((b for b in bundles if b['channel'] == 'error'), None)
            lo, mid, hi = t - 300, t, t + 300
            if wl is not None and ts.get('bo_luu_luong_ngoai', True) and E is not None:
                rho = {}
                for s in wl['result']:
                    sv = s['metric'].get('service_name')
                    n, a = _tb(s['values'], lo, mid), _tb(s['values'], mid, hi)
                    if n and a is not None and n > 0:
                        rho[sv] = a / n
                cd['rho'] = {k: round(v, 4) for k, v in sorted(rho.items())}
                rE = rho.get(E)
                tau, kappa = float(ts.get('tau', 0.2)), float(ts.get('kappa', 1.5))
                if rE is not None and rE >= 1 + tau:
                    giu = []
                    for s in wl['result']:
                        sv = s['metric'].get('service_name'); r = rho.get(sv)
                        if r is not None and 1 / kappa <= r / rE <= kappa:
                            cd['bo_workload'].append(sv)
                            if ts.get('log_theo_luu_luong'):
                                self.rho_log[aliases.get(sv, sv)] = r
                        else:
                            giu.append(s)
                    wl_moi = dict(wl, result=giu)
                    bundles = [wl_moi if b is wl else b for b in bundles]
            if er is not None and wl is not None and ts.get('ty_le_loi', True):
                tong = {s['metric'].get('service_name'): {str(t0): float(v) for t0, v in s['values']} for s in wl['result']}
                moi = []
                for s in er['result']:
                    sv = s['metric'].get('service_name'); w = tong.get(sv, {})
                    vals = []
                    for t0, v in s['values']:
                        if str(t0) not in w:
                            continue
                        e, n = float(v), w[str(t0)]
                        if n > 0:
                            vals.append([t0, repr(e / n)])
                        elif e == 0:
                            vals.append([t0, '0'])
                    moi.append(dict(s, values=vals))
                bundles = [dict(er, result=moi) if b is er else b for b in bundles]
                cd['ty_le_loi'] = True
        self.chan_doan = cd
        return bundles

    @contextlib.contextmanager
    def ngu_canh(self):
        goc = m1kenh.don_vi_log
        rho = dict(getattr(self, 'rho_log', {}) or {})
        dem = {'don_vi_chia': {}}

        def boc(dong_N, dong_A, quy_tac, E3_bat, tham_so_E3=None):
            out = goc(dong_N, dong_A, quy_tac, E3_bat, tham_so_E3)
            if not rho or E3_bat:
                return out
            moi = []
            for u in out:
                r = rho.get(u['thuc_the'])
                if r and u.get('nhom') == 'log_loi':
                    # làm tròn về số nguyên: E4 dùng nhị thức chính xác (binom.sf/cdf cần n nguyên — số thực cho NaN,
                    # lộ ở ca thử 865c8e93 HTTP5-EVENT-FLASH 13/11, LOG T-064). Sai số ≤ 0,5 dòng.
                    u = dict(u, n_A=int(round(u['n_A'] / r)))
                    dem['don_vi_chia'][u['thuc_the']] = round(r, 4)
                moi.append(u)
            return moi

        m1kenh.don_vi_log = boc
        try:
            yield dem
        finally:
            m1kenh.don_vi_log = goc

    def ra(self, rec, inputs, ctx):
        cd = dict(self.chan_doan, log_chia_rho=(ctx or {}).get('don_vi_chia', {}))
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})[self.ma] = cd
        return rec
