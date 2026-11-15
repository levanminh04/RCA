# -*- coding: utf-8 -*-
"""H1a — cạnh tới tài nguyên dữ liệu (DB/cache) thành đơn vị chấm, và xếp hạng cạnh (T-064 H1).

Vấn đề P7 (adapter ghim, `known_limits`): span JDBC/Redis thuộc service JVM, không có đầu bị gọi; DB/cache chỉ có kênh
metric `db-size`. Gốc dạng cạnh (vd. EVENT-DB-LAT: event-service → event_db) chỉ được chấm qua nút.

Nút, cạnh, tín hiệu, phép tính (luật 18):
- **Nút** giữ như P7 (inventory; thứ hạng nút **không đổi** ở thành phần này).
- **Cạnh message** (mới, 13/11): (chủ span → `broker`) cho span PRODUCER/CLIENT của thư viện RabbitMQ (scope chứa
  `rabbitmq`: publish, `basic.ack`, `waitForConfirms`). Loại `message`.
- **Cạnh dữ liệu** (mới): (chủ span → tài nguyên) cho span CLIENT có `db.system` ∈ {postgresql, redis, mongodb}; đầu bị
  gọi = `db.name`/`db.namespace` nếu thuộc inventory, Redis → `cache`. Loại `data`. Nguồn xác minh: thuộc tính span.
- **Cạnh gọi**: cặp span cha–con khác chủ, lấy mẫu bằng `m1.span.mau_canh` (cùng hàm P7 dùng cho đơn vị `canh|a|b`). Loại `http`.
- **Tín hiệu:** thời lượng đầy đủ của span CLIENT (lá, nên = thời gian chờ tài nguyên), chia N/A theo mốc kết thúc như
  `chuoi._chay`. **Phép tính:** `e4.cham_phan_vi` với cùng `tham_so_E4`, `m_span` của P7 (không qua cổng G3 — cạnh mới là
  đầu ra bổ sung, không vào xếp hạng nút). **Mọi cạnh chấm cùng một cách** để điểm so được với nhau: e = rA − rN (chênh
  tỷ lệ vượt ngưỡng h của N) khi qua cổng nhị thức p < α; không dùng điểm cạnh của P7 (cổng G3 + thang T4c, thang khác).
- **Xếp hạng cạnh:** khóa (có cờ hướng lên, điểm e_len) giảm dần; cùng khóa là hòa. Ghi `extra.m1_ft.canh_xep_hang`.
- **Điều kiện thất bại:** lỗi ở tài nguyên làm chậm mọi cạnh tới nó như nhau (DB chậm chung) → nhiều cạnh hòa; nút DB vẫn
  phải lên qua chiếu cạnh → nút khi chấm. Cạnh không có span (bị lọc, không đo) không xếp được.
- **Đối chứng:** bản không có H1a (bảng cạnh = UNSUPPORTED); đối chứng bỏ quan hệ trên cùng bản = xếp cạnh chỉ theo điểm
  nút hai đầu (chưa cài).
"""
import math

from m1 import chuoi, e4, span as m1span
from m1_ft.chay import ThanhPhan, dang_ky

NS = 10 ** 9
_HE = {'us': 1000, 'ns': 1, 's': NS}
HE_DB = {'postgresql', 'redis', 'mongodb'}


@dang_ky
class CanhDuLieu(ThanhPhan):
    ma = 'H1a-canh'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None

    def can_bo_sung(self):
        return ('span_phu',)

    def ra(self, rec, inputs, ctx):
        spans, _, _, inventory, aliases, t, params = inputs
        if rec.get('status') != 'OK':
            return rec
        phu = self.bo_sung['span_phu']
        he = _HE[params['don_vi_thoi_gian']['spans.start_us']]
        t_ns = int(round(t * NS)); lo, hi = t_ns - 300 * NS, t_ns + 300 * NS
        inv = set(aliases.get(x, x) for x in inventory)
        mau, khong_ro = {}, 0
        for s in spans:
            st, en = s['start_us'] * he, (s['start_us'] + s['duration_us']) * he
            if not (st >= lo and en < hi):
                continue
            p = phu.get(f"{s['traceID']}|{s['spanID']}")
            if not p:
                continue
            la_msg = 'rabbitmq' in (p.get('scope') or '') and p.get('kind') in (3, 4)
            if la_msg:
                dich = 'broker'
            elif p.get('kind') != 3 or (p.get('db') or '') not in HE_DB:
                continue
            else:
                dich = 'cache' if p['db'] == 'redis' else aliases.get(p.get('db_ten'), p.get('db_ten'))
            if dich not in inv:
                khong_ro += 1
                continue
            chu = aliases.get(s['owner'], s['owner'])
            m = mau.setdefault((chu, dich, 'message' if la_msg else 'data'), {'N': [], 'A': []})
            m['N' if en < t_ns else 'A'].append(s['duration_us'])
        ts = params['tham_so_E4']
        canh = []
        for (a, b, loai), m in sorted(mau.items()):
            kq = e4.cham_phan_vi(m['N'], m['A'], ts['m_span'], ts, huong_cham=['len'], cache=None, khoa_don_vi=f'h1|{a}|{b}|{loai}')
            canh.append({'nguon': a, 'dich': b, 'loai': loai, 'nguon_xac_minh': 'span_producer_client_rabbitmq' if loai == 'message' else 'span_client_db',
                         'co': int(bool(kq.get('F_raw_len'))), 'diem': float(kq.get('e_len') or 0.0) if kq.get('F_raw_len') else 0.0,
                         'n_N': len(m['N']), 'n_A': len(m['A']), 'trang_thai': kq.get('trang_thai')})
        rows = [dict(r, owner=chuoi._alias(aliases, r['owner'])) for r in spans
                if r['start_us'] * he >= lo and (r['start_us'] + r['duration_us']) * he < hi]
        prep = m1span.chuan_bi(rows, t=t_ns / he, tau=10 ** 6 / he, tinh_CP=False)
        # Sửa R1 (phản biện T-064 lượt 1, 13/11/2026): `m1span.mau_canh` gộp mẫu theo cặp service, không phân loại giao thức.
        # Tách mẫu theo loại span của span bọc w và con của nó TRƯỚC khi chấm: CLIENT(3) → SERVER(2) = 'http';
        # PRODUCER(4) → CONSUMER(5) = 'message'; cặp khác hoặc thiếu thông tin loại = 'khong_ro' (không đoán).
        # Điều kiện span bọc, thứ tự mẫu và phía N/A lấy nguyên từ `prep` của P7 (cùng vòng lặp với `mau_canh`).
        # `gop_loai_cu = true` tái lập hành vi cũ (mọi cặp là 'http') để làm đối chứng mã nguồn với hai lượt chọn đầu.
        if self.tham_so.get('gop_loai_cu'):
            nhom = {(a, b, 'http'): m for (a, b), m in m1span.mau_canh(prep).items()}
        else:
            nhom = {}
            for s in sorted(prep['spans'].values(), key=lambda x: (x['end'], x['khoa'])):
                if not s['boc']:
                    continue
                c = prep['spans'][s['con'][0]]
                kw = (phu.get(f"{s['khoa'][0]}|{s['khoa'][1]}") or {}).get('kind')
                kc = (phu.get(f"{c['khoa'][0]}|{c['khoa'][1]}") or {}).get('kind')
                loai = 'http' if (kw, kc) == (3, 2) else 'message' if (kw, kc) == (4, 5) else 'khong_ro'
                nhom.setdefault((s['chu'], c['chu'], loai), {'N': [], 'A': []})[s['phia']].append(s['g'])
        xm = {'http': 'span_cha_con', 'message': 'span_cha_con_producer_consumer', 'khong_ro': 'span_cha_con_khong_ro_loai'}
        for (a, b, loai), m in sorted(nhom.items()):
            khoa = f'h1|{a}|{b}' if loai == 'http' else f'h1|{a}|{b}|{loai}'
            kq = e4.cham_phan_vi(m['N'], m['A'], ts['m_span'], ts, huong_cham=['len'], cache=None, khoa_don_vi=khoa)
            canh.append({'nguon': a, 'dich': b, 'loai': loai, 'nguon_xac_minh': xm[loai],
                         'co': int(bool(kq.get('F_raw_len'))), 'diem': float(kq.get('e_len') or 0.0) if kq.get('F_raw_len') else 0.0,
                         'n_N': len(m['N']), 'n_A': len(m['A']), 'trang_thai': kq.get('trang_thai')})
        canh.sort(key=lambda c: (-c['co'], -c['diem'], c['nguon'], c['dich'], c['loai']))
        hang, nhom, truoc = 0, -1, None
        for i, c in enumerate(canh):
            k = (c['co'], c['diem'])
            if k != truoc:
                nhom += 1; hang = i + 1; truoc = k
            c['hang'], c['tie_group'] = hang, nhom
        ft = rec.setdefault('extra', {}).setdefault('m1_ft', {})
        ft['canh_xep_hang'] = canh
        ft.setdefault('chu_thich', {})[self.ma] = {'so_canh_du_lieu': sum(c['loai'] == 'data' for c in canh),
                                                  'so_canh_message': sum(c['loai'] == 'message' for c in canh),
                                                  'so_canh_goi': sum(c['loai'] == 'http' for c in canh),
                                                  'so_canh_goi_message': sum(c['nguon_xac_minh'] == 'span_cha_con_producer_consumer' for c in canh),
                                                  'so_canh_goi_khong_ro': sum(c['loai'] == 'khong_ro' for c in canh),
                                                  'gop_loai_cu': bool(self.tham_so.get('gop_loai_cu')),
                                                  'span_db_khong_ro_dich': khong_ro,
                                                  'so_canh_co_co': sum(c['co'] for c in canh)}
        return rec


@dang_ky
class CanhDinhVi(CanhDuLieu):
    """H1b — định vị cạnh có cờ bằng bằng chứng riêng của hai đầu (dùng quan hệ lân cận, luật 18).

    Nguyên lý: lời gọi tới tài nguyên/service là span con, nên thời gian **độc quyền** của span SERVER bên gọi (xử lý request
    đã trừ con) không tăng khi chỉ cạnh hay đích chậm; nó tăng khi chính bên đó thiếu tài nguyên (CPU, GC…). Metric lớp
    "tài nguyên" (không lan) cũng là bằng chứng riêng. Với cạnh có cờ (a → b):
      - a có bằng chứng riêng (đơn vị op SERVER có cờ, hoặc metric không lan có cờ) → `phia_goi`;
      - ngược lại b có bằng chứng riêng → `phia_dich`;
      - không bên nào có → `rieng_canh`;
      - `rieng_canh` nhưng bên gọi ở tầng 3 (bình thường) của thứ hạng nút P7 → `khong_anh_huong` (bất thường cạnh không
        làm thay đổi hành vi bên gọi, vd. nạn nhân tranh CPU máy ở service ít tải).
    Chỉ cạnh `rieng_canh` giữ cờ trong `canh_xep_hang` (đầu ra cạnh của bản); cạnh phía gọi/đích ghi `dinh_vi` và `co = 0`
    — bất thường đó thuộc về nút, đã có trong thứ hạng nút. Kind của thao tác lấy từ `bo_sung.span_phu` (đa số span).
    Điều kiện thất bại: lỗi cạnh làm bên gọi thiếu luồng (pool/thread chờ) → span SERVER chậm cả phần độc quyền → bị coi là
    phía gọi; lỗi đích không có tín hiệu riêng (DB không có metric chi tiết) → bị coi là riêng cạnh.
    """
    ma = 'H1b-canh-dinh-vi'

    def ra(self, rec, inputs, ctx):
        rec = super().ra(rec, inputs, ctx)
        if rec.get('status') != 'OK':
            return rec
        spans, _, _, _, aliases, _, _ = inputs
        phu = self.bo_sung['span_phu']
        kind = {}
        for s in spans:
            p = phu.get(f"{s['traceID']}|{s['spanID']}")
            if p:
                c = kind.setdefault((aliases.get(s['owner'], s['owner']), s['operation']), [0, 0])
                c[0] += 1; c[1] += int(p.get('kind') == 2)
        # `bo_kenh_dinh_vi` (lượt chọn 2, 13/11): tên kênh metric KHÔNG dùng làm bằng chứng riêng khi định vị. Nguyên lý:
        # kênh pool kết nối đo trạng thái kết nối từ bên gọi tới đích, tức là tín hiệu của chính cạnh dữ liệu (đích chậm →
        # connection bị giữ lâu → used/wait tăng), không phân biệt được "bên gọi hỏng" với "đích chậm". Mặc định rỗng:
        # hành vi như lượt 1.
        bo_ten = set(self.tham_so.get('bo_kenh_dinh_vi') or ())
        rieng, bi_bo = {}, {}
        for k in rec['extra'].get('kenh_co', []):
            dv, e = k.get('don_vi') or '', k['thuc_the']
            if dv.startswith('metric|') and k['lop'] == 'khong_lan':
                if k.get('ten') in bo_ten:
                    bi_bo.setdefault(e, []).append(dv)
                    continue
                rieng.setdefault(e, []).append(dv)
            elif dv.startswith('op|'):
                _, chu, op = dv.split('|', 2)
                c = kind.get((chu, op))
                if c and c[1] * 2 > c[0]:
                    rieng.setdefault(e, []).append(dv)
        ft = rec['extra']['m1_ft']
        dem = {'rieng_canh': 0, 'phia_goi': 0, 'phia_dich': 0, 'khong_anh_huong': 0}
        tang = rec['extra'].get('tang_P') or {}
        for c in ft['canh_xep_hang']:
            if not c['co']:
                continue
            if rieng.get(c['nguon']):
                c['dinh_vi'] = 'phia_goi'
            elif rieng.get(c['dich']):
                c['dinh_vi'] = 'phia_dich'
            elif tang.get(c['nguon'], 3) >= 3:
                c['dinh_vi'] = 'khong_anh_huong'
            else:
                c['dinh_vi'] = 'rieng_canh'
            dem[c['dinh_vi']] += 1
            if c['dinh_vi'] != 'rieng_canh':
                c['co_truoc_dinh_vi'], c['co'] = 1, 0
        canh = ft['canh_xep_hang']
        canh.sort(key=lambda c: (-c['co'], -c['diem'] if c['co'] else 0, c['nguon'], c['dich'], c['loai']))
        hang, nhom, truoc = 0, -1, None
        for i, c in enumerate(canh):
            key = (c['co'], c['diem'] if c['co'] else 0)
            if key != truoc:
                nhom += 1; hang = i + 1; truoc = key
            c['hang'], c['tie_group'] = hang, nhom
        ft['chu_thich'][self.ma] = {'dinh_vi': dem, 'bang_chung_rieng': {e: v[:8] for e, v in sorted(rieng.items())}}
        if bo_ten:
            ft['chu_thich'][self.ma].update({'bo_kenh_dinh_vi': sorted(bo_ten),
                                             'bang_chung_bi_bo': {e: v[:8] for e, v in sorted(bi_bo.items())}})
        return rec


@dang_ky
class CanhDanhSachChung(CanhDinhVi):
    """H1c — như H1b, nhưng hạng cạnh tính trong danh sách chung nút + cạnh (WHY-82): sau mỗi nhóm nút (thứ tự
    `entity_ranking`), chèn cạnh `rieng_canh` có đầu mút tốt nhất thuộc nhóm đó, theo e giảm dần; hạng = 1 + số phần tử
    đứng trước. Cạnh không định vị riêng (co = 0) xếp sau mọi phần tử, cùng một nhóm hòa."""
    ma = 'H1c-canh-chung'

    def ra(self, rec, inputs, ctx):
        rec = super().ra(rec, inputs, ctx)
        if rec.get('status') != 'OK':
            return rec
        ft = rec['extra']['m1_ft']
        if 'H1b-canh-dinh-vi' in ft['chu_thich']:
            ft['chu_thich'][self.ma] = ft['chu_thich'].pop('H1b-canh-dinh-vi')
        nhom_nut = {}
        for r in rec['entity_ranking']:
            nhom_nut.setdefault(r['tie_group'], []).append(r['entity'])
        nhom_cua = {e: g for g, es in nhom_nut.items() for e in es}
        co = [c for c in ft['canh_xep_hang'] if c['co']]
        khong = [c for c in ft['canh_xep_hang'] if not c['co']]
        vt, tg, ds = 0, 0, []
        for g in sorted(nhom_nut):
            vt += len(nhom_nut[g])
            gan = sorted([c for c in co if min(nhom_cua.get(c['nguon'], 1e9), nhom_cua.get(c['dich'], 1e9)) == g],
                         key=lambda c: (-c['diem'], c['nguon'], c['dich'], c['loai']))
            truoc = None
            for c in gan:
                if c['diem'] != truoc:
                    hang_nhom = vt + 1; truoc = c['diem']; tg += 1
                c['hang'], c['tie_group'] = hang_nhom, tg
                vt += 1
                ds.append(c)
        con = [c for c in co if c not in ds]  # đầu mút không có trong thứ hạng nút (không xảy ra với inventory đầy đủ)
        tg += 1
        for c in con + khong:
            c['hang'], c['tie_group'] = vt + 1, tg
        ft['canh_xep_hang'] = ds + con + khong
        ft['chu_thich'][self.ma]['thu_tu'] = 'danh_sach_chung (WHY-82)'
        return rec
