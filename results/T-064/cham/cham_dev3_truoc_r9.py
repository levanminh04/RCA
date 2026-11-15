# -*- coding: utf-8 -*-
"""Chấm lô 5 (T-064; tiêu chí results/T-064/tieu-chi-chon.md; đáp án khai trước results/T-064/dap-an-dev3.json; WHY-95).
Cùng bộ chấm `src/m1_ft/cham.py` như `cham_dev2.py`, `phien-c/cham_phien_c.py`. Chỉ đọc đầu ra đã nhận; nhãn chỉ ở phía chấm.
Dùng: py -3 -B cham_dev3.py <spec.json> <ra.json>
spec = {"tap": {"<tên>": "<file tập> | t062"}, "d": <giây, mặc định 0>, "ban": ["<mã bản>", ...] | {"<tên>": {"ban": "<mã>", "d": d}},
        "cap": [["<A đối chiếu>", "<B xét>"], ...]}
Tìm đầu ra của (bản, ca, d), theo thứ tự: kiem/nhan-luot5/l5/<nhóm>/d<d>/<bản>/<ca>/; khi d = 0 thêm cham/dau-ra-dev3/,
cham/dau-ra-dev2/ (ca dev), bien-the/<bản>/ra-*/ (T-062) và đầu ra P7 ghim. `loi-chay.json` = lỗi chạy (trượt, tiêu chí §2).
Không thấy gì: MISSING (cũng tính trượt, nhưng được đếm riêng ở `thieu` để không lẫn với lỗi phương pháp)."""
import glob, hashlib, json, os, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R)); T = R / 'results/T-064'
from src.m1_ft import cham  # noqa: E402

DA_F = Path(os.environ.get('DAP_AN', T / 'dap-an-dev3.json'))  # biến môi trường chỉ để kiểm bộ chấm bằng đáp án cũ
DA = json.loads(DA_F.read_text(encoding='utf-8'))
LOI = {x['o']: x for x in DA['o_loi']}; KL = {x['o'] for x in DA['o_khong_loi']}
BANG = json.loads((R / 'results/T-062/ket-qua/phat-lai/bang-cham.json').read_text(encoding='utf-8'))
CANH062 = {c['id']: (c['root']['caller'], c['root']['callee'], c['root'].get('kind'))
           for c in json.loads((R / 'results/T-059/danh-muc-loi.json').read_text(encoding='utf-8'))['cells']
           if isinstance(c.get('root'), dict) and c['root'].get('type') == 'edge'}
DEV2 = {c['ma'] for c in json.loads((T / 'tap-chon-dev2-13.json').read_text(encoding='utf-8'))['ca']}
T062 = {c['ma'] for c in BANG['ca']}


def nhom(ma):
    return 'dev2' if ma in DEV2 else ('t062' if ma in T062 else 'dev3')


def tim(ban, ma, d):
    g = nhom(ma)
    ung = [T / 'kiem/nhan-luot5/l5' / g / f'd{d}' / ban / ma]
    if d == 0:
        if g == 't062':
            ung += [Path(p) for p in sorted(glob.glob(str(T / 'bien-the' / glob.escape(ban) / 'ra-*' / ma)), reverse=True)]
            if ban == 'P7':
                ung.append(R / 'results/T-062/ca' / ma / 'outputs' / ma)
        else:
            ung += [T / 'cham/dau-ra-dev3' / ban / ma, T / 'cham/dau-ra-dev2' / ban / ma]
    elif g == 't062':
        ung += [T / 'bien-the' / ban / 'ra-doi-moc' / ma]
    else:
        ung += [T / 'cham/dau-ra-dev2' / ban / ma, T / 'cham/dau-ra-dev3' / ban / ma]
    for u in ung:
        f = u / 'method-output-1.json'
        if f.exists():
            return json.loads(f.read_text(encoding='utf-8')), hashlib.sha256(f.read_bytes()).hexdigest(), u.relative_to(R).as_posix()
        if (u / 'loi-chay.json').exists():
            return {'status': 'ERROR'}, None, u.relative_to(R).as_posix()
    return {'status': 'MISSING'}, None, None


def tap_tu_file(f):
    if f == 't062':
        out = []
        for c in BANG['ca']:
            cn = CANH062.get(c['o'])
            out.append({'ma': c['ma'], 'o': c['o'], 'loai': 'loi' if c['tap_chap_nhan'] else 'khong_loi',
                        'tap_chap_nhan': c['tap_chap_nhan'], 'canh': cn})
        return out
    out = []
    for c in json.loads((R / f).read_text(encoding='utf-8'))['ca']:
        if c['o'] in LOI:
            x = LOI[c['o']]
            if not isinstance(x['tap_chap_nhan'], list):
                raise SystemExit('đáp án chưa chốt: ' + c['o'])
            cn = (x['root']['caller'], x['root']['callee'], x['root'].get('kind')) if x['root'].get('type') == 'edge' else None
            out.append({'ma': c['ma'], 'o': c['o'], 'loai': 'loi', 'tap_chap_nhan': x['tap_chap_nhan'], 'canh': cn})
        elif c['o'] in KL:
            out.append({'ma': c['ma'], 'o': c['o'], 'loai': 'khong_loi'})
        else:
            raise SystemExit('ô không có đáp án khai trước: ' + c['o'])
    return out


def cham_tap(ban, d, tap):
    loi, kl, ca = {}, {}, {}
    for c in tap:
        rec, sh, nguon = tim(ban, c['ma'], d)
        canh = None
        if c['loai'] == 'loi':
            if c.get('canh'):
                canh = cham.cham_canh(rec, c['canh'])
            r = cham.cham_ca_loi(cham.chieu_canh_ve_nut(rec), c['tap_chap_nhan'])
            loi[c['ma']] = r
        else:
            r = cham.cham_ca_khong_loi(rec)
            kl[c['ma']] = r
        ca[c['ma']] = {'o': c['o'], 'status': rec.get('status'), 'verdict': rec.get('verdict'),
                       'nhom_hang_1': cham.nhom_hang_1(rec) if rec.get('status') == 'OK' else [],
                       **{k: r[k] for k in r if k in ('p1', 'p3', 'hang_ky_vong', 'k')}, 'sha256': sh, 'nguon': nguon,
                       **({'bang_canh': canh} if canh is not None else {})}
    bc = [v['bang_canh'] for v in ca.values() if 'bang_canh' in v]
    return {'tong': cham.tong_hop(loi), 'K': sum(v['k'] for v in kl.values()), 'so_ca_khong_loi': len(kl),
            'thieu': sorted(m for m, v in ca.items() if v['status'] == 'MISSING'),
            'loi_chay': sorted(m for m, v in ca.items() if v['status'] not in ('OK', 'MISSING')),
            'bang_canh': {'so_o': len(bc), 'top3': sum(x.get('top3', 0) for x in bc if x.get('trang_thai') == 'OK'),
                          'trang_thai': [x.get('trang_thai') for x in bc], 'hang': [x.get('hang_ky_vong') for x in bc]},
            'ca': ca, '_loi': loi}


def so_cap(A, B):
    doi = {}
    for m, b in B['ca'].items():
        a = A['ca'][m]
        dd = {}
        for k in ('hang_ky_vong', 'p1', 'p3', 'verdict', 'k', 'status'):
            if a.get(k) != b.get(k):
                dd[k] = [a.get(k), b.get(k)]
        if sorted(a['nhom_hang_1']) != sorted(b['nhom_hang_1']):
            dd['nhom_hang_1'] = [a['nhom_hang_1'], b['nhom_hang_1']]
        if 'bang_canh' in a or 'bang_canh' in b:
            x, y = a.get('bang_canh') or {}, b.get('bang_canh') or {}
            for k in ('trang_thai', 'hang_ky_vong', 'top3'):
                if x.get(k) != y.get(k):
                    dd[f'canh_{k}'] = [x.get(k), y.get(k)]
        if dd:
            doi[m] = dict(dd, o=b['o'])
    return {'so_voi': cham.so_sanh(B['tong'], A['tong']), 'khong_xau_di': cham.khong_xau_di(B['tong'], A['tong']),
            'tut_qua_2_bac': cham.tut_qua_2_bac(B['_loi'], A['_loi']), 'dK': B['K'] - A['K'], 'doi': doi}


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    taps = {t: tap_tu_file(f) for t, f in spec['tap'].items()}
    ban = spec['ban'] if isinstance(spec['ban'], dict) else {b: {'ban': b, 'd': spec.get('d', 0)} for b in spec['ban']}
    kq = {ten: {t: cham_tap(v['ban'], v.get('d', 0), tp) for t, tp in taps.items()} for ten, v in ban.items()}
    cap = {f'{a} -> {b}': {t: so_cap(kq[a][t], kq[b][t]) for t in taps} for a, b in spec.get('cap', [])}
    for v in kq.values():
        for x in v.values():
            x.pop('_loi')
    nguon = {f: hashlib.sha256((R / f).read_bytes()).hexdigest() for f in
             [DA_F.resolve().relative_to(R).as_posix(), 'results/T-064/tieu-chi-chon.md', 'results/T-062/ket-qua/phat-lai/bang-cham.json',
              'results/T-059/danh-muc-loi.json'] + [f for f in spec['tap'].values() if f != 't062']}
    Path(sys.argv[2]).write_text(json.dumps({'nguon_sha256': nguon, 'spec': spec, 'ban': kq, 'cap': cap},
                                            ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for ten, v in kq.items():
        print(ten, {t: (round(x['tong']['AC@1'], 3), round(x['tong']['AC@3'], 3), round(x['tong']['tong_hang_cat'], 2),
                        'K', x['K'], 'c', x['bang_canh']['top3'], 'thieu', len(x['thieu']), 'loi', len(x['loi_chay']))
                    for t, x in v.items()})


if __name__ == '__main__':
    main()
