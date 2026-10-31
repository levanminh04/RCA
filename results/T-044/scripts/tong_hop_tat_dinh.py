"""Tổng hợp lượt tất định tat-dinh-005 (cùng cấu trúc tat-dinh-004/tong-hop.json)."""
import json
import sys
from pathlib import Path

d = Path(sys.argv[1])
goc_cu = sys.argv[2] if len(sys.argv) > 2 else '253dbe46'
bg = {h: json.loads((d / f'ban-ghi-h{h}.json').read_text(encoding='utf-8')) for h in (0, 1, 2)}
# seed ghi trong đầu ra của tat_dinh.py (C7); thiếu (lượt cũ) thì None
seed = {h: v.pop('hash_seed', None) for h, v in bg.items()}
seed_khop = all(s == str(h) for h, s in seed.items())
goc = bg[0]['0']
lech, n_bien_the = [], 0
for h, v in bg.items():
    for x, bang in v.items():
        n_bien_the += 1
        for ma, s in bang.items():
            if goc.get(ma) != s:
                lech.append(f'h{h}-x{x}|{ma}')
        if set(bang) != set(goc):
            lech.append(f'h{h}-x{x}|tap_ma_khac')


def ket(p):
    r = json.loads(p.read_text(encoding='utf-8'))
    return {(x['test'], x.get('ma')): x['ket_qua'] for x in r}


k0 = ket(d / 'pytest-h0-x0.json')
py = {}
for h in (0, 1, 2):
    for x in (0, 1, 2, 3):
        p = d / f'pytest-h{h}-x{x}.json'
        k = ket(p)
        py[p.name] = {'so_phep': len(k), 'so_truot': sum(1 for v in k.values() if v != 'passed'), 'giong_h0_x0': k == k0}
cu = json.loads((d / f'bo-truong-moi-{goc_cu}.json').read_text(encoding='utf-8'))
moi = json.loads((d / 'bo-truong-moi-sau-sua.json').read_text(encoding='utf-8'))
so_lech = sum(1 for m in set(cu) | set(moi) if cu.get(m) != moi.get(m))
ok = seed_khop and not lech and all(v['so_truot'] == 0 and v['giong_h0_x0'] for v in py.values())
n_phep = len(k0)
out = {
    'buoc': 'SPEC T-044 bước 6, tiêu chí 5; lượt xác nhận trên máy local Windows (so với ' + goc_cu + ')',
    'cach_chay': {
        'ban_ghi': 'PYTHONHASHSEED=<0|1|2> python -B results/T-044/scripts/tat_dinh.py > ban-ghi-h<hs>.json',
        'pytest': 'PYTHONHASHSEED=<0|1|2> M1_XAO=<rỗng|1|2|3> M1_KET_QUA=pytest-h<hs>-x<x>.json python -B -m pytest -q '
                  '-p no:cacheprovider -W ignore (trong results/T-044/tests); x0 là thứ tự gốc',
        'moi_truong': 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe (Python 3.12.10), '
                      'PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages (drain3)'},
    'ban_ghi': {'so_ban_ghi_moi_bien_the': len(goc), 'so_bien_the': n_bien_the, 'so_sha256_lech': len(lech),
                'lech': lech, 'hash_seed_ghi_trong_dau_ra': seed, 'hash_seed_khop': seed_khop},
    'pytest': py,
    'so_voi_truoc_sua': {
        'cach_chay': f'git archive {goc_cu} src results/T-043 results/T-044 vào thư mục tạm; PYTHONHASHSEED=0 python -B '
                     'results/T-044/scripts/so_ban_ghi_truoc_sau.py <gốc> trên cây cũ và cây hiện tại',
        'so_ban_ghi': len(moi), 'so_lech_sau_khi_bo_truong_moi': so_lech,
        'tep': [f'bo-truong-moi-{goc_cu}.json', 'bo-truong-moi-sau-sua.json']},
    'ket_luan': (f'PASS: {len(goc)} bản ghi giống hệt qua 4 thứ tự × 3 hash seed; {n_phep} phép kiểm qua và giống hệt '
                 f'ở cả 12 biến thể' if ok else 'FAIL'),
}
(d / 'tong-hop.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
print(out['ket_luan'], '| lệch so với trước sửa:', so_lech)
