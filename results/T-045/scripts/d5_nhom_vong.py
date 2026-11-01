"""T-045 D5 (không nhãn, chỉ mô tả; SPEC T-045 bước 2b), phần điều kiện cần: hai cách đọc nhóm vòng của E5 (C′
`co_vong`, A `ke_canh`; CĐ3) chỉ khác nhau khi đồ thị con F_raw có nhóm vòng (SCC ≥ 2 nút) (`src/m1/e5.py:84–195`:
mọi nhánh khác nhau đều nằm dưới `S = comp.get(e)` khác None). Đồ thị con F_raw là đồ thị con của đồ thị cạnh
quan sát N ∪ A (`extra.canh`), mà khi T12 tắt thì cạnh này giống nhau ở mọi cấu hình khối K và mọi thế giới của một
ca (dựng từ span, `span.canh_goi`). Vậy ca có đồ thị cạnh không có SCC ≥ 2 thì D5 = 0 ở cả 16 cấu hình và ba thế
giới. Script này đếm SCC trên `extra.canh` của bản ghi R0 (T1) từng ca; ca có SCC cần chạy hai cách đọc.
Chạy: $PY -B results/T-045/scripts/d5_nhom_vong.py <lượt R0> --ra <json>
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1 import e5  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('luot')
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    d = Path(a.luot)
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    out = {'luot': a.luot, 'ca': {}}
    for x in (d / meta['tep']).read_text(encoding='utf-8').splitlines():
        if not x:
            continue
        r = json.loads(x)
        if r['status'] not in ('OK', 'NO_EVIDENCE'):
            out['ca'][r['opaque_id']] = {'status': r['status']}
            continue
        canh = [tuple(c) for c in (r.get('extra') or {}).get('canh') or []]
        nut = sorted({v for c in canh for v in c})
        nhom = sorted(sorted(c) for c in e5.scc(nut, {(p, q) for p, q in canh if p != q}) if len(c) >= 2)
        out['ca'][r['opaque_id']] = {'status': r['status'], 'so_canh': len(canh), 'nhom_vong_do_thi_canh': nhom,
                                     'nhom_vong_F_raw_P_R0': (r.get('extra') or {}).get('nhom_vong_P'),
                                     'D5_bang_0_moi_cau_hinh': not nhom}
    out['tong_hop'] = {'so_ca': len(out['ca']),
                       'so_ca_co_nhom_vong': sum(1 for c in out['ca'].values() if c.get('nhom_vong_do_thi_canh')),
                       'so_ca_D5_bang_0': sum(1 for c in out['ca'].values() if c.get('D5_bang_0_moi_cau_hinh'))}
    Path(a.ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps(out['tong_hop'], ensure_ascii=False))


if __name__ == '__main__':
    main()
