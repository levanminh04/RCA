# -*- coding: utf-8 -*-
"""Phiên C — chấm và so từng ô cho lô dời mốc và lô H8 (T-064). Chỉ đọc đầu ra đã chép về repo; nhãn chỉ ở phía chấm.
Cùng bộ chấm `src/m1_ft/cham.py`, cùng đáp án khai trước như công cụ đã dùng:
- 13 ca dev bản 2: `results/T-064/tap-chon-dev2-13.json` + `results/T-064/dap-an-dev2.json` (như `cham/cham_dev2.py`);
- 9 ca T-062: `results/T-062/ket-qua/phat-lai/bang-cham.json` + cạnh gốc từ `results/T-059/danh-muc-loi.json`
  (như `cham/cham_kiem_cai_dat.py`).
Dùng: py -3 -B cham_phien_c.py <spec.json> <ra.json>
spec = {"ban": {"<tên>": {"dev2": "<mẫu đường dẫn có {id}>", "t062": "<mẫu>"}}, "cap": [["<tên A>", "<tên B>"], ...]}
Với mỗi bản: tổng (AC@1, AC@3, tổng hạng cắt), K, bảng cạnh, từng ca. Với mỗi cặp (A = đối chiếu, B = bản xét): theo ca —
đổi hạng kỳ vọng, đổi p1/p3, đổi kết luận ở ca không lỗi, đổi nhóm hạng 1, đổi cờ/hạng cạnh; và so tổng theo §3."""
import hashlib, json, sys
from pathlib import Path
sys.dont_write_bytecode = True; sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); sys.path.insert(0, str(R))
from src.m1_ft import cham  # noqa: E402

DA = json.loads((R / 'results/T-064/dap-an-dev2.json').read_text(encoding='utf-8'))
LOI = {x['o']: x for x in DA['o_loi']}; KL = {x['o'] for x in DA['o_khong_loi']}
TAP = json.loads((R / 'results/T-064/tap-chon-dev2-13.json').read_text(encoding='utf-8'))['ca']
BANG = json.loads((R / 'results/T-062/ket-qua/phat-lai/bang-cham.json').read_text(encoding='utf-8'))
CANH = {c['id']: (c['root']['caller'], c['root']['callee'], c['root'].get('kind'))
        for c in json.loads((R / 'results/T-059/danh-muc-loi.json').read_text(encoding='utf-8'))['cells']
        if isinstance(c.get('root'), dict) and c['root'].get('type') == 'edge'}
LOAI = {'data': 'data', 'http': 'http'}


def _doc(p):
    f = Path(p)
    if not f.exists():
        return {'status': 'MISSING'}, None
    return json.loads(f.read_text(encoding='utf-8')), hashlib.sha256(f.read_bytes()).hexdigest()


def cham_tap(mau, tap):
    loi, kl, ca = {}, {}, {}
    for c in tap:
        rec, sh = _doc(mau.format(id=c['ma']))
        canh = None
        if c['loai'] == 'loi':
            if c.get('canh'):
                canh = cham.cham_canh(rec, c['canh'])
            r = cham.cham_ca_loi(cham.chieu_canh_ve_nut(rec), c['tap_chap_nhan']); loi[c['ma']] = r
        else:
            r = cham.cham_ca_khong_loi(rec); kl[c['ma']] = r
        ca[c['ma']] = {'o': c['o'], 'status': rec.get('status'), 'verdict': rec.get('verdict'),
                       'nhom_hang_1': cham.nhom_hang_1(rec) if rec.get('status') == 'OK' else [],
                       **{k: r[k] for k in r if k in ('p1', 'p3', 'hang_ky_vong', 'k')}, 'sha256': sh,
                       **({'bang_canh': canh} if canh is not None else {})}
    bc = [v['bang_canh'] for v in ca.values() if 'bang_canh' in v]
    return {'tong': cham.tong_hop(loi), 'K': sum(v['k'] for v in kl.values()), 'so_ca_khong_loi': len(kl),
            'thieu': sorted(m for m, v in ca.items() if v['status'] == 'MISSING'),
            'bang_canh': {'so_o': len(bc), 'top3': sum(x.get('top3', 0) for x in bc if x.get('trang_thai') == 'OK'),
                          'trang_thai': [x.get('trang_thai') for x in bc], 'hang': [x.get('hang_ky_vong') for x in bc]},
            'ca': ca, '_loi': loi}


def tap_dev2():
    out = []
    for c in TAP:
        if c['o'] in LOI:
            x = LOI[c['o']]
            cn = (x['root']['caller'], x['root']['callee'], x['root'].get('kind')) \
                if x['root'] and x['root'].get('type') == 'edge' else None
            out.append({'ma': c['ma'], 'o': c['o'], 'loai': 'loi', 'tap_chap_nhan': x['tap_chap_nhan'], 'canh': cn})
        elif c['o'] in KL:
            out.append({'ma': c['ma'], 'o': c['o'], 'loai': 'khong_loi'})
        else:
            raise SystemExit('ô không có đáp án khai trước: ' + c['o'])
    return out


def tap_t062():
    out = []
    for c in BANG['ca']:
        cn = None
        if c['o'] in CANH:
            a, b, k = CANH[c['o']]; cn = (a, b, LOAI.get(k, k))
        out.append({'ma': c['ma'], 'o': c['o'], 'loai': 'loi' if c['tap_chap_nhan'] else 'khong_loi',
                    'tap_chap_nhan': c['tap_chap_nhan'], 'canh': cn})
    return out


def so_cap(A, B):
    """A = đối chiếu, B = bản xét; theo ca."""
    doi = {}
    for m, b in B['ca'].items():
        a = A['ca'][m]; d = {}
        for k in ('hang_ky_vong', 'p1', 'p3', 'verdict', 'k', 'status'):
            if a.get(k) != b.get(k):
                d[k] = [a.get(k), b.get(k)]
        if sorted(a['nhom_hang_1']) != sorted(b['nhom_hang_1']):
            d['nhom_hang_1'] = [a['nhom_hang_1'], b['nhom_hang_1']]
        if 'bang_canh' in a or 'bang_canh' in b:
            ca_, cb = a.get('bang_canh') or {}, b.get('bang_canh') or {}
            for k in ('trang_thai', 'hang_ky_vong', 'top3'):
                if ca_.get(k) != cb.get(k):
                    d[f'canh_{k}'] = [ca_.get(k), cb.get(k)]
        if a['sha256'] != b['sha256']:
            d['_sha_khac'] = True
        if d:
            doi[m] = dict(d, o=b['o'])
    return {'so_voi': cham.so_sanh(B['tong'], A['tong']), 'khong_xau_di': cham.khong_xau_di(B['tong'], A['tong']),
            'tut_qua_2_bac': cham.tut_qua_2_bac(B['_loi'], A['_loi']), 'dK': B['K'] - A['K'],
            'so_ca_doi_dai_luong': sum(1 for v in doi.values() if set(v) - {'_sha_khac', 'o'}),
            'so_ca_khac_sha': sum(1 for v in doi.values() if v.get('_sha_khac')), 'doi': doi}


def main():
    spec = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    taps = {'dev2': tap_dev2(), 't062': tap_t062()}
    kq = {}
    for ten, mau in spec['ban'].items():
        kq[ten] = {t: cham_tap(mau[t], taps[t]) for t in ('dev2', 't062') if mau.get(t)}
    cap = {}
    for a, b in spec.get('cap', []):
        cap[f'{a} -> {b}'] = {t: so_cap(kq[a][t], kq[b][t]) for t in ('dev2', 't062') if t in kq[a] and t in kq[b]}
    for v in kq.values():
        for x in v.values():
            x.pop('_loi')
    nguon = {f: hashlib.sha256((R / f).read_bytes()).hexdigest() for f in
             ('results/T-064/tap-chon-dev2-13.json', 'results/T-064/dap-an-dev2.json', 'results/T-064/tieu-chi-chon.md',
              'results/T-062/ket-qua/phat-lai/bang-cham.json', 'results/T-059/danh-muc-loi.json')}
    Path(sys.argv[2]).write_text(json.dumps({'nguon_sha256': nguon, 'spec': spec, 'ban': kq, 'cap': cap},
                                            ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for ten, v in kq.items():
        print(ten, {t: (x['tong'], 'K', x['K'], 'canh', x['bang_canh']['top3'], 'thieu', len(x['thieu'])) for t, x in v.items()})
    for k, v in cap.items():
        print(k, {t: (x['so_voi'], 'dK', x['dK'], 'doi', x['so_ca_doi_dai_luong'], 'sha', x['so_ca_khac_sha']) for t, x in v.items()})


main()
