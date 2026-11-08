"""Kiểm tương đương trên dev Nezha-OB (chạy trên EC2). Mỗi ca: M1 cấu hình khóa với adapter đã ghim (cu)
và với wrapper "root" (moi). So toàn bộ bản ghi; chỉ cho phép khác ở extra.dau_vao_cd3. Kiểm phép dựng đích
C-d3 từ trung gian (đường dùng cho test) trùng đích của lượt chạy đủ. Không đọc nhãn.

python -B dev_ec2.py <goc_code> <goc_du_lieu> <ds_ca.json> <thu_muc_ra>
"""
import json
import os
import sys
import time
from pathlib import Path

GOC, DATA, DS, RA = sys.argv[1:5]
os.environ['T054_ROOT'] = GOC
sys.path.insert(0, str(Path(__file__).resolve().parent))
import lane  # noqa: E402
from m1 import doi_chung  # noqa: E402
from fractions import Fraction  # noqa: E402

cfg = json.loads(Path(DS).read_text(encoding='utf-8'))
contract = json.loads((Path(GOC) / 'results/T-043/hop-dong.json').read_text(encoding='utf-8'))
ra = Path(RA)
ra.mkdir(parents=True, exist_ok=True)


def cd3_ban_ghi(raw):
    d = dict(raw['extra']['dau_vao_cd3'])
    d.setdefault('canh', raw['extra']['canh'])
    return json.loads(lane.dump(doi_chung.cd3([tuple(e) for e in d['canh']],
                                              {e: Fraction(*p) for e, p in d['diem'].items()}, d['dich'])))


for oid, row in cfg['cases'].items():
    dst = ra / (oid + '.json')
    if dst.exists():
        continue
    t = row['t_ns'] // 10 ** 9
    out = {'opaque_id': oid, 't': t, 'giay': {}}
    raws = {}
    for mode, sua in (('cu', False), ('moi', True)):
        t0 = time.perf_counter()
        data, n = lane.doc_ca(row, oid, cfg['inventory'], contract, DATA, sua=sua)
        params = lane.params_m1(cfg['config'], data)
        raws[mode] = json.loads(lane.dump(lane.chay_m1(data, t, params)))
        if mode == 'moi':
            spans_A, cd = lane.spans_A_goc(data, t, params)
            out['dan_xuat_tu_cu'] = json.loads(lane.dump(lane.cd3_tu_luu(raws['cu']['extra'], spans_A)))
        out['n_span_doi_root_' + mode] = n
        out['giay'][mode] = round(time.perf_counter() - t0, 2)
    cu, moi = raws['cu'], raws['moi']
    khac = sorted(k for k in set(cu) | set(moi) if k != 'extra' and cu.get(k) != moi.get(k))
    khac_extra = sorted(k for k in set(cu['extra']) | set(moi['extra'])
                        if k != 'dau_vao_cd3' and cu['extra'].get(k) != moi['extra'].get(k))
    dv_cu, dv_moi = cu['extra']['dau_vao_cd3'], moi['extra']['dau_vao_cd3']
    out.update(
        khac_ngoai_extra=khac, khac_extra_ngoai_cd3=khac_extra,
        diem_cd3_trung=dv_cu['diem'] == dv_moi['diem'],
        dich_cu=dv_cu['dich'], dich_moi=dv_moi['dich'],
        so_span_goc_A_cu=dv_cu['so_span_goc_A'], so_span_goc_A_moi=dv_moi['so_span_goc_A'],
        dan_xuat_trung_lan_chay=(out['dan_xuat_tu_cu']['dich'] == dv_moi['dich']
                                 and out['dan_xuat_tu_cu']['so_span_goc_A'] == dv_moi['so_span_goc_A']),
        cd3_cu=cd3_ban_ghi(cu), cd3_moi=cd3_ban_ghi(moi),
        cd3_dan_xuat_trung=out['dan_xuat_tu_cu']['cd3'] == cd3_ban_ghi(moi),
        ban_ghi_cu=cu, ban_ghi_moi=moi)
    out['TUONG_DUONG'] = (not khac and not khac_extra and out['diem_cd3_trung'] and out['dan_xuat_trung_lan_chay']
                          and out['cd3_dan_xuat_trung'])
    tmp = dst.with_suffix('.tmp')
    tmp.write_text(json.dumps(out, ensure_ascii=False, sort_keys=True), encoding='utf-8')
    tmp.replace(dst)
    print(oid, out['TUONG_DUONG'], out['dich_moi'], out['cd3_moi']['trang_thai'], out['giay'], flush=True)
print('XONG', flush=True)
