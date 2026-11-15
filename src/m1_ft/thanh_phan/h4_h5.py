# -*- coding: utf-8 -*-
"""H4 (queue) và H5 (thành phần "chết im") — kênh metric mới từ gói bổ sung, gán về service bằng quy ước tên/cổng tĩnh.

H4. Nút: service consumer (đã có trong inventory). Tín hiệu: `queue-ready`, `queue-unacked` theo `rabbitmq_queue_name`
    (TD-02, có từ 12/11 21:35Z). Gán queue → service theo quy ước đặt tên `<tiền tố>.<sự kiện>.q|dlq` của FlashTicket
    (tiền tố = tên service bỏ "-service"): queue `.q` cộng vào `queue-ready`/`queue-unacked` của service consumer; `.dlq`
    cộng vào `dlq-ready`. Lớp **"tài nguyên"** (hướng lên không lan: tồn đọng là bằng chứng tự sinh ở consumer).
    Điều kiện thất bại: broker chậm chung làm mọi queue tồn (thuộc nút `broker`, H1); queue không theo quy ước tên → bỏ, đếm.
H5. Nút: service JVM. Tín hiệu: `live-down` (1 = đầu dò liveness của Collector không nhận phản hồi trong bước), `live-ms`
    theo `http_url` (TD-04, có từ 12/11 23:27Z). Gán URL → service theo bảng cổng của `exp-app` (cố định, không nhãn).
    Lớp `live-down`: "tài nguyên" (không lan — thành phần tự không phản hồi); `live-ms`: "độ trễ".
    Điều kiện thất bại: máy quá tải làm mọi đầu dò chậm; liveness bị chặn quyền (401) vẫn tính là phản hồi.
Đối chứng: bản không có thành phần. Không dùng tên ca/nhãn.
"""
from m1_ft.chay import ThanhPhan, dang_ky

TIEN_TO = {'booking': 'booking-service', 'payment': 'payment-service', 'ticket': 'ticket-service',
           'event': 'event-service', 'user': 'user-service'}
CONG = {'8081': 'api-gateway', '8082': 'booking-service', '8083': 'payment-service', '8084': 'ticket-service',
        '8085': 'user-service', '8086': 'event-service', '8761': 'discovery-server', '8080': 'keycloak'}


def _cong_nhom(series):
    """Cộng các chuỗi cùng service theo mốc thời gian (mỗi chuỗi đã gán `service_name`)."""
    gop = {}
    for s in series:
        sv = s['metric']['service_name']
        g = gop.setdefault(sv, {})
        for t, v in s['values']:
            try:
                g[t] = g.get(t, 0.0) + float(v)
            except ValueError:
                continue
    return [{'metric': {'service_name': sv}, 'values': [[t, repr(v)] for t, v in sorted(g.items(), key=lambda x: float(x[0]))]}
            for sv, g in sorted(gop.items())]


@dang_ky
class KenhQueue(ThanhPhan):
    ma = 'H4-queue'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None
        self.cd = {}

    def can_bo_sung(self):
        return ('bundles', 'bundles_bo_sung')

    def kenh_moi(self):
        return {'queue-ready': 'tài nguyên', 'queue-unacked': 'tài nguyên', 'dlq-ready': 'tài nguyên'}

    def bien_doi_bundle(self, bundles, inputs):
        out, bo = [], 0
        dlq = []
        for b in bundles:
            if b['channel'] not in ('queue-ready', 'queue-unacked'):
                out.append(b); continue
            gan = []
            for s in b['result']:
                q = s['metric'].get('rabbitmq_queue_name') or ''
                sv = TIEN_TO.get(q.split('.')[0])
                if not sv or not (q.endswith('.q') or q.endswith('.dlq')):
                    bo += 1; continue
                x = {'metric': {'service_name': sv}, 'values': s['values']}
                if q.endswith('.q'):
                    gan.append(x)                       # queue chính → kênh của consumer
                elif b['channel'] == 'queue-ready':
                    dlq.append(x)                       # .dlq ready → kênh dlq-ready
                # .dlq unacked: bỏ (không có consumer)
            out.append(dict(b, result=_cong_nhom(gan)))
        if dlq:
            out.append({'channel': 'dlq-ready', 'native': False, 'query': '(gộp .dlq từ queue-ready)', 'step_seconds': 15,
                        'result': _cong_nhom(dlq), 'native_timestamps': None})
        self.cd = {'chuoi_queue_bo': bo}
        return out

    def ra(self, rec, inputs, ctx):
        co = [k['don_vi'] for k in (rec.get('extra') or {}).get('kenh_co', []) if any(k['don_vi'].endswith('_' + c) for c in self.kenh_moi())]
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})[self.ma] = dict(self.cd, don_vi_co_co=co)
        return rec


@dang_ky
class KenhLiveness(ThanhPhan):
    ma = 'H5-liveness'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.bo_sung = None
        self.cd = {}

    def can_bo_sung(self):
        return ('bundles', 'bundles_bo_sung')

    def kenh_moi(self):
        return {'live-down': 'tài nguyên', 'live-ms': 'độ trễ'}

    def bien_doi_bundle(self, bundles, inputs):
        out, bo = [], 0
        for b in bundles:
            if b['channel'] not in ('live-down', 'live-ms'):
                out.append(b); continue
            gan = []
            for s in b['result']:
                u = s['metric'].get('http_url') or ''
                cong = u.split('://', 1)[-1].split('/', 1)[0].rsplit(':', 1)[-1]
                sv = CONG.get(cong)
                if not sv:
                    bo += 1; continue
                gan.append({'metric': {'service_name': sv}, 'values': s['values']})
            out.append(dict(b, result=gan))
            if b['channel'] == 'live-down' and self.tham_so.get('chet_im_giay') is not None:
                self.chet = self._chet_im(gan, float(inputs[5]), float(self.tham_so['chet_im_giay']))
        self.cd = {'chuoi_url_bo': bo}
        return out

    @staticmethod
    def _chet_im(series, t, toi_thieu):
        """H5b (lượt chọn 2, 13/11). Thành phần "chết im" = đầu dò sống của chính nó: (i) phản hồi ở MỌI mẫu trước t
        (≥ 4 mẫu), (ii) từ mẫu không phản hồi đầu tiên sau t tới hết cửa sổ KHÔNG phản hồi lại lần nào, (iii) đoạn đó dài
        ≥ `toi_thieu` giây (mặc định dùng 60 s = 4 bước dò 15 s, để loại một lần dò hụt hay khởi động lại ngắn).
        Trả {service: {'tu': ts đầu, 'den': ts cuối, 'so_mau': n}}."""
        out = {}
        for s in series:
            v = sorted((float(a), float(b)) for a, b in s['values'])
            N = [x for ts, x in v if ts < t]; A = [(ts, x) for ts, x in v if ts >= t]
            if len(N) < 4 or any(x != 0 for x in N) or not A:
                continue
            i = next((j for j, (_, x) in enumerate(A) if x == 1), None)
            if i is None or any(x != 1 for _, x in A[i:]) or A[-1][0] - A[i][0] < toi_thieu:
                continue
            out[s['metric']['service_name']] = {'tu': A[i][0], 'den': A[-1][0], 'so_mau': len(A) - i}
        return out

    def ra(self, rec, inputs, ctx):
        co = [k['don_vi'] for k in (rec.get('extra') or {}).get('kenh_co', []) if any(k['don_vi'].endswith('_' + c) for c in self.kenh_moi())]
        ct = rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})
        ct[self.ma] = dict(self.cd, don_vi_co_co=co)
        if self.tham_so.get('chet_im_giay') is None or rec.get('status') != 'OK':
            return rec
        # H5b: quan sát trực tiếp "thành phần không còn phản hồi" không cùng thang với điểm lệch s của E4 (kênh nhị phân
        # có e ≤ 1, còn độ trễ của bên phụ thuộc cho s hàng trăm) → không so bằng khóa; đặt thành phần chết im thành
        # nhóm đầu thứ hạng (nhiều thành phần: một nhóm hòa). Thành phần đã chết không thể là nạn nhân chậm của bên khác
        # trong cùng cửa sổ; bên phụ thuộc chậm là hệ quả. Điều kiện thất bại: thành phần chết VÌ nguyên nhân ở nơi khác
        # (máy chủ, phụ thuộc làm liveness hỏng), khi đó gốc thật xếp sau nó. `extra.blocks_P` giữ thứ hạng trước sửa.
        ten = {r['entity'] for r in rec['entity_ranking']}
        chet = sorted(e for e in getattr(self, 'chet', {}) if e in ten)
        ct[self.ma]['chet_im'] = {'nguong_giay': self.tham_so['chet_im_giay'], 'thanh_phan': {e: self.chet[e] for e in chet},
                                  'khong_trong_thu_hang': sorted(e for e in getattr(self, 'chet', {}) if e not in ten)}
        if not chet:
            return rec
        dai = len(rec['entity_ranking'][0]['key'])
        khoa = [float(rec['entity_ranking'][0]['key'][0]) + 1.0] + [0.0] * (dai - 1)
        con = [r for r in rec['entity_ranking'] if r['entity'] not in chet]
        doi, moi = {}, [{'entity': e, 'key': list(khoa), 'tie_group': 0} for e in chet]
        for r in con:
            g = doi.setdefault(r['tie_group'], len(doi) + 1)
            moi.append(dict(r, tie_group=g))
        rec['entity_ranking'] = moi
        if rec.get('blocks') is not None:
            kb = [{'key': list(khoa), 'groups': [list(chet)]}]
            for b in rec['blocks']:
                gs = [[e for e in g if e not in chet] for g in b['groups']]
                gs = [g for g in gs if g]
                if gs:
                    kb.append(dict(b, groups=gs))
            rec['blocks'] = kb
        rec['verdict'] = 'CAUSE_FOUND'
        return rec
