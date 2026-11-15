# -*- coding: utf-8 -*-
"""H8-adapter — nối chuỗi metric của container được tạo lại trong cửa sổ (T-064 H8; phiên C, 14/11/2026).

Vấn đề P7 (đã kiểm, `results/T-064/phien-c/h8-adapter/dem-chuoi-trung.json`): `m1.adapter_flashticket.normalize_metrics`
ném `Multiple runtime series map to one logical metric without a declared aggregation` khi một metric logic
(kênh, thực thể) có hơn một định danh chuỗi. Metric gốc theo container (`cpu`, `mem`) mang nhãn `container_id`; khi
container bị tạo lại (triển khai lại, `--force-recreate`) trong [t−600, t+600], chuỗi cũ và mới cùng về một thực thể → cả ca
ERROR, M1 không cho kết quả. Ca thật: `thuong01` (11/11, triển khai giữa cửa sổ).

Nút, cạnh, phép tính (luật 18): thành phần không thêm nút hay cạnh; nó chỉ đổi bước đầu vào metric (trước adapter ghim).
Nơi đặt: Prometheus `exp-obs`, chuỗi `container_cpu_utilization_ratio`/`container_memory_usage_total_bytes` từ Collector.

Nguyên lý gộp (ghi trước khi chấm, không theo đáp án): một thành phần logic chạy **một** container tại một thời điểm
(Compose FlashTicket một bản sao mỗi service). Các chuỗi chỉ khác nhau ở nhãn định danh runtime (`NHAN_RUNTIME`) và **không
chồng lấn trong mốc mẫu gốc** (mẫu cuối của chuỗi trước < mẫu đầu của chuỗi sau, theo `native_timestamps`) là cùng một
chuỗi bị đổi định danh → nối theo thời gian. Mỗi mốc đánh giá có nhiều điểm (do lookback ~5 phút của PromQL lặp mẫu cũ
của container đã dừng) thì giữ điểm có mốc mẫu gốc mới nhất — đúng cách Prometheus chọn mẫu khi chỉ có một chuỗi. Điểm bị
bỏ luôn là bản lặp của một mẫu gốc đã có ở mốc khác (kiểm `mat_mau == 0`, ghi chẩn đoán).
Không gộp (giữ hành vi P7: adapter ném lỗi) khi: chồng lấn trong mốc mẫu gốc (hai container chạy song song — cần phép
gộp khai báo như tổng/trung bình, không đoán); khác nhãn ngoài `NHAN_RUNTIME`; kênh không có mốc mẫu gốc (chuỗi dẫn xuất).
Điều kiện thất bại: container mới khởi động có mức CPU/bộ nhớ khác hẳn (JVM khởi động) → bước nhảy ngay sau mốc tạo lại
có thể gắn cờ thành phần; đây là thông tin thật (thành phần vừa tạo lại), không phải lỗi gộp, nhưng có thể không phải gốc.
Đối chứng: bản cha không có thành phần (trên ca không có tình huống này, đầu vào phải trùng byte).
"""
from m1_ft.chay import ThanhPhan, dang_ky

NHAN_RUNTIME = frozenset({'container_id', 'container_name', 'service_instance_id'})


def _k(labels):
    return tuple(sorted((k, v) for k, v in labels.items() if k != '__name__'))


def noi_chuoi(bundles, inventory, owner_of):
    """→ (bundles mới, chẩn đoán). `owner_of(labels, inventory)` = `m1.adapter_flashticket._owner` (ánh xạ ghim).
    Không sửa đối tượng đầu vào. Bundle không có nhóm cần nối được trả nguyên đối tượng."""
    cd = {'nhom_noi': [], 'nhom_khong_noi': [], 'diem_lap_bo': 0, 'mat_mau': 0}
    out = []
    for b in bundles:
        if not b.get('native') or not b.get('result'):
            out.append(b); continue
        nat = {_k(x['metric']): x['values'] for x in (b.get('native_timestamps') or [])}
        nhom = {}
        for it in b['result']:
            o = owner_of(it['metric'], inventory)
            if o is not None:
                nhom.setdefault(o, []).append(it)
        thay = {}
        for o, its in sorted(nhom.items()):
            if len({_k(x['metric']) for x in its}) <= 1:
                continue
            chung = set.intersection(*[set(_k(x['metric'])) for x in its])
            khac = {k for x in its for k, _ in set(_k(x['metric'])) - chung}
            muc = {'kenh': b['channel'], 'thuc_the': o, 'so_chuoi': len(its)}
            if not khac <= NHAN_RUNTIME:
                cd['nhom_khong_noi'].append(dict(muc, ly_do='khac_nhan_ngoai_runtime', nhan=sorted(khac))); continue
            # mốc mẫu gốc của từng chuỗi
            kh = []
            for x in its:
                n = nat.get(_k(x['metric']))
                if n is None:
                    break
                ts = sorted({float(v) for _, v in n})
                kh.append((ts[0], ts[-1], x, n))
            if len(kh) != len(its):
                cd['nhom_khong_noi'].append(dict(muc, ly_do='thieu_moc_mau_goc')); continue
            kh.sort(key=lambda z: (z[0], z[1]))
            if any(kh[i][1] >= kh[i + 1][0] for i in range(len(kh) - 1)):
                cd['nhom_khong_noi'].append(dict(muc, ly_do='chong_lan_moc_mau_goc',
                                                 khoang=[[a, z] for a, z, _, _ in kh])); continue
            # nối: mỗi mốc đánh giá giữ điểm có mốc mẫu gốc mới nhất
            chon = {}  # eval -> (native_ts, value, native_raw)
            tat_ca_mau = set()
            for _, _, x, n in kh:
                nmap = {str(e): v for e, v in n}
                for e, v in x['values']:
                    nr = nmap.get(str(e))
                    if nr is None:
                        raise ValueError('H8-adapter: thiếu mốc mẫu gốc cho một điểm')  # adapter ghim cũng từ chối
                    tat_ca_mau.add((float(nr), v))
                    cu = chon.get(str(e))
                    if cu is None or float(nr) > cu[0]:
                        if cu is not None:
                            cd['diem_lap_bo'] += 1
                        chon[str(e)] = (float(nr), v, nr, e)
                    else:
                        cd['diem_lap_bo'] += 1
            giu = {(z[0], z[1]) for z in chon.values()}
            cd['mat_mau'] += len(tat_ca_mau - giu)
            nhan = {k: v for k, v in kh[-1][2]['metric'].items() if k not in khac}
            dsx = sorted(chon.values(), key=lambda z: float(z[3]))
            thay[o] = ({'metric': nhan, 'values': [[z[3], z[1]] for z in dsx]},
                       {'metric': nhan, 'values': [[z[3], z[2]] for z in dsx]})
            cd['nhom_noi'].append(dict(muc, nhan_bo=sorted(khac), khoang=[[a, z] for a, z, _, _ in kh]))
        if not thay:
            out.append(b); continue
        res, natv = [], []
        da = set()
        for it in b['result']:
            o = owner_of(it['metric'], inventory)
            if o in thay:
                if o not in da:
                    res.append(thay[o][0]); da.add(o)
                continue
            res.append(it)
        for x in b.get('native_timestamps') or []:
            o = owner_of(x['metric'], inventory)
            if o in thay:
                continue
            natv.append(x)
        natv += [thay[o][1] for o in sorted(thay)]
        out.append(dict(b, result=res, native_timestamps=natv))
    return out, cd


@dang_ky
class NoiChuoiContainer(ThanhPhan):
    ma = 'H8-adapter'

    def __init__(self, tham_so):
        super().__init__(tham_so)
        self.cd = {'goi_ghim': None, 'duong_ong': None}

    def bien_doi_goi_ghim(self, bundles, inventory, nhan='goi_ghim'):
        """Áp lên danh sách bundle metric TRƯỚC adapter ghim (dựng đầu vào, và đường ống metric của M1-FT)."""
        from m1 import adapter_flashticket as ad
        moi, cd = noi_chuoi(bundles, list(inventory), ad._owner)
        self.cd[nhan] = cd
        return moi

    def ra(self, rec, inputs, ctx):
        rec.setdefault('extra', {}).setdefault('m1_ft', {}).setdefault('chu_thich', {})[self.ma] = {
            'goi_ghim': self.cd['goi_ghim'], 'duong_ong': self.cd['duong_ong'], 'nhan_runtime': sorted(NHAN_RUNTIME)}
        return rec
