"""T-045 D5 (không nhãn, chỉ mô tả; SPEC T-045 bước 2b): số kênh có trạng thái kế thừa khác nhau giữa cách đọc nhóm
vòng C′ (`co_vong`, cách chạy thật) và A (`ke_canh`, chẩn đoán; CĐ3), ở 16 cấu hình khối K và mốc giả.

Cách tính (quyết định của người làm theo quyền Minh giao, chat 31/10/2026; LOG phiên 1): không chạy chuỗi lần hai với
cách đọc A. Với mỗi bản ghi C′, dựng lại kênh có cờ từ `extra.kenh_co_the_gioi` và cạnh từ `extra.canh`, chạy
`e5.phan_loai` với cả hai cách đọc. Bản ghi chỉ được dùng khi đạt **kiểm tái lập**: F_I ở ba thế giới và
`inherited_by` ở P của cách C′ tính lại trùng đúng bản ghi; và không có kênh có cờ ngoài U (`evidence_refs` ⊆ đơn vị
của `extra.kenh_co`). Bản ghi trượt được liệt kê để chạy lại riêng với `--doc-nhom-vong ke_canh`. E9 tắt ở khối K nên
không cần khởi phát. Không đọc `verdict`, thứ hạng hay nhãn (Đ-6).

Đại lượng: theo (cấu hình, cửa sổ thật/mốc giả, thế giới): số kênh có đề xuất giải thích khác nhau (tập mã kênh trong
`inherited_by`), số kênh có F_I khác nhau (chỉ khác khi E5 bật), số ca có nhóm vòng trên đồ thị con F_raw.
Chạy: $PY -B results/T-045/scripts/d5_tinh_lai.py --luot that=<lượt K> --luot moc_gia=<lượt K mốc giả> --ra <json>
"""
import argparse
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1 import e5  # noqa: E402
from m1.kieu import Kenh  # noqa: E402

WORLDS = ('P', 'S_lo', 'S_hi')


def ib_khoa(ds):
    return sorted((i['ma'], i['giai_thich_ma'], i['quy_tac'], i['trang_thai']) for i in ds)


def mot_ban_ghi(r):
    if r['status'] not in ('OK', 'NO_EVIDENCE'):
        return {'tai_lap': False, 'ly_do': f"status {r['status']}"}
    ex = r['extra']
    bat = 'E5' in r['config_id'].split('-', 1)[1].split('+')
    canh = [tuple(c) for c in ex['canh']]
    ngoai_U = sorted(set(r.get('evidence_refs') or []) - {k['don_vi'] for k in ex['kenh_co']})
    out = {'ngoai_U': len(ngoai_U), 'the_gioi': {}}
    tai_lap = not ngoai_U
    for w in WORLDS:
        kc = ex['kenh_co_the_gioi'][w]
        kenh = [Kenh(k['thuc_the'], k['ten'], k['huong'], k['lop'], k['s'], don_vi=k['don_vi']) for k in kc]
        cv = e5.phan_loai(kenh, canh, bat=bat, doc_nhom_vong='co_vong')
        a = e5.phan_loai(kenh, canh, bat=bat, doc_nhom_vong='ke_canh')
        ok_FI = all(cv['F_I'].get(k['ma'], 1) == k['F_I'] for k in kc)
        ok_ib = ib_khoa(cv['inherited_by']) == ib_khoa(r['inherited_by']) if w == 'P' else True
        tai_lap = tai_lap and ok_FI and ok_ib
        de_xuat_cv = {i['ma'] for i in cv['inherited_by']}
        de_xuat_a = {i['ma'] for i in a['inherited_by']}
        out['the_gioi'][w] = {'nhom_vong': len(cv['nhom_vong']),
                              'kenh_de_xuat_khac': len(de_xuat_cv ^ de_xuat_a),
                              'kenh_F_I_khac': sum(1 for m in set(cv['F_I']) | set(a['F_I'])
                                                   if cv['F_I'].get(m, 1) != a['F_I'].get(m, 1)),
                              'kenh_co': len(kc)}
    out['tai_lap'] = tai_lap
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--luot', action='append', required=True, help='<that|moc_gia>=<thư mục lượt khối K>')
    ap.add_argument('--ra', required=True)
    a = ap.parse_args()
    kq = {'luot': {}, 'tong_hop': {}, 'can_chay_lai_ke_canh': []}
    for x in a.luot:
        nhan, d = x.split('=', 1)
        d = Path(d)
        meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
        theo = {}
        f = open(d / meta['tep'], encoding='utf-8')  # đọc theo dòng: tệp khối K khoảng 0,9 GB
        for line in f:
            if not line.strip():
                continue
            r = json.loads(line)
            v = mot_ban_ghi(r)
            theo[f"{r['config_id']}|{r['opaque_id']}"] = v
            if not v['tai_lap']:
                kq['can_chay_lai_ke_canh'].append([nhan, r['config_id'], r['opaque_id']])
        kq['luot'][nhan] = {'thu_muc': str(d), 'sha256_pha1': meta['sha256'], 'ban_ghi': theo}
        th = collections.defaultdict(lambda: collections.Counter())
        for k, v in theo.items():
            cfg = k.split('|')[0]
            th[cfg]['ban_ghi'] += 1
            th[cfg]['tai_lap'] += int(v['tai_lap'])
            for w, t in (v.get('the_gioi') or {}).items():
                th[cfg][f'{w}|kenh_de_xuat_khac'] += t['kenh_de_xuat_khac']
                th[cfg][f'{w}|kenh_F_I_khac'] += t['kenh_F_I_khac']
                th[cfg][f'{w}|ca_co_nhom_vong'] += int(t['nhom_vong'] > 0)
                th[cfg][f'{w}|ca_co_khac'] += int(t['kenh_de_xuat_khac'] > 0 or t['kenh_F_I_khac'] > 0)
        kq['tong_hop'][nhan] = {c: dict(v) for c, v in sorted(th.items())}
    Path(a.ra).write_text(json.dumps(kq, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'can_chay_lai_ke_canh': len(kq['can_chay_lai_ke_canh']),
                      'tong_hop': {n: {c: {k: v for k, v in x.items() if k.startswith(('ban_ghi', 'tai_lap', 'P|'))}
                                       for c, x in t.items()} for n, t in kq['tong_hop'].items()}},
                     ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
