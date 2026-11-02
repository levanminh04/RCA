"""T-046 bản 4, C3 (thêm 15:49): khóa riêng cặp cổng (g*, c*) khi không `verdict` nào đạt. Đọc kết quả đánh giá bản 4,
kiểm trạng thái 'V4_truot_c1' hoặc 'khong_co_k', ghi `ung-vien.json` (tệp khóa) gồm toàn bộ đánh giá cộng mục `khoa`.
`luat_chon.to_hop_chon` ghi 'g*|c*|V0' chỉ để các script sau khóa đọc cùng định dạng; V0 là quy tắc hiện hành, không
phải `verdict` được chọn (`khoa.verdict` = null). Verdict báo cáo sau khóa: V0, V3, V4:q*.

Chạy: $PY -B results/T-046/scripts/b5d_khoa_cong.py --danh-gia results/T-046/danh-gia-ban4-luot2.json
      --chan-doan results/T-046/chan-doan-cong-ban3.json --ra results/T-046/ung-vien.json
"""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--danh-gia', required=True)
    ap.add_argument('--chan-doan', required=True)
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    if Path(a.ra).exists():
        raise SystemExit('tệp khóa đã có: không ghi đè')
    dg_byte = Path(a.danh_gia).read_bytes()
    dg = json.loads(dg_byte.decode('utf-8'))
    if dg['luat_chon']['ket_qua'] not in ('V4_truot_c1', 'khong_co_k'):
        raise SystemExit(f"trạng thái đánh giá không cho khóa riêng cổng: {dg['luat_chon']['ket_qua']}")
    cd = json.loads(Path(a.chan_doan).read_bytes().decode('utf-8'))
    g, c = dg['minimax']['cong_phan_vi'], dg['minimax']['cong_dem']
    q = (dg.get('V4') or {}).get('q_sao')
    out = dict(dg)
    out['nguong'] = cd['nguong']
    out['danh_gia_nguon'] = {'tep': a.danh_gia, 'sha256': hashlib.sha256(dg_byte).hexdigest()}
    out['khoa'] = {'cong_phan_vi': g, 'cong_dem': c, 'verdict': None,
                   'ly_do': 'không verdict nào đạt (b) và (c1) với (g*, c*) (SPEC bản 4 C3, thêm 15:49)',
                   'verdict_bao_cao_sau_khoa': ['V0', 'V3'] + ([f'V4:{q}'] if q is not None else [])}
    out['luat_chon'] = dict(dg['luat_chon'], to_hop_chon=f'{g}|{c}|V0', ghi_chu_to_hop_chon='định dạng cho script sau khóa; V0 không được chọn')
    du = (json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
    Path(a.ra).write_bytes(du)
    print('sha256', hashlib.sha256(du).hexdigest())


if __name__ == '__main__':
    main()
