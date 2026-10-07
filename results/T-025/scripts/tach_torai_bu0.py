"""T-025 phiên 3 (R1, Minh duyệt 07/10): tách số TORAI B có điều kiện theo "đủ nền" / "N có bù 0".

Phân tích đặt ra SAU khi thấy số (REVIEW R1). Vai evaluator: đọc `cham/cham-b.json` (số theo ca đã chấm),
`cham/phan-tich-b.json` (A có chứa mốc) và `cham/soi-bin-torai.json`; không đọc bản ghi mới, không chạy phương pháp.
Độ đo theo ca là trung bình 3 seed như `cham-b.json`.

python tach_torai_bu0.py → results/T-025/cham/tach-torai-bu0.json
"""
import json

import chung

C = chung.OUT / 'cham'


def tom(rows):
    if not rows:
        return {'n': 0}
    return {'n': len(rows), **{k: sum(r[k] for r in rows) / len(rows) for k in ('hit@1', 'hit@3', 'hit@5', 'rr')}}


def main():
    cb = json.loads((C / 'cham-b.json').read_text(encoding='utf-8'))['theo_bo_phat_hien']
    pt = json.loads((C / 'phan-tich-b.json').read_text(encoding='utf-8'))['theo_ca']
    sb = json.loads((C / 'soi-bin-torai.json').read_text(encoding='utf-8'))['theo_bo']
    out = {'mo_ta': __doc__.strip(), 'theo_bo': {}}
    for nhom in ('bocpd', 'nsigma'):
        ca = cb[nhom]['torai_B']['ca']
        bu = {o: sb[nhom]['theo_ca'][o]['bu_0'] for o in ca}
        res = {}
        for ten, la_bu in (('du_nen', False), ('N_bu_0', True)):
            ids = [o for o in ca if bu[o] == la_bu]
            sai = [o for o in ids if not ca[o]['t_hat_dung']]
            dp = [c['ty_le_du_phong'] for o in ids for c in ca[o]['chan_doan']]
            res[ten] = {'tren_ca_co_luot_rca': tom([ca[o] for o in ids]),
                        't_hat_dung': tom([ca[o] for o in ids if ca[o]['t_hat_dung']]),
                        'bao_dong_sai_A_chua_moc': tom([ca[o] for o in sai if pt[o][nhom]['A_chua_moc']]),
                        'bao_dong_sai_A_khong_chua_moc': tom([ca[o] for o in sai if not pt[o][nhom]['A_chua_moc']]),
                        'du_phong': {'so_luot': len(dp), 'tb': sum(dp) / len(dp) if dp else None,
                                     'so_luot_bang_1': sum(x == 1 for x in dp)}}
        out['theo_bo'][nhom] = res
    chung.ghi_json(C / 'tach-torai-bu0.json', out)
    print(json.dumps(out['theo_bo'], ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
