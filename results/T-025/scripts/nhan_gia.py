"""T-025: sinh nhãn giả cho chạy khô evaluator (SPEC, Kiểm đúng đắn; Minh duyệt 07/10/2026 "duyệt a, b").

Không đọc nhãn thật (`results/T-022/nhan-dev.json`). Lấy mã mờ từ allowlist, universe U, và lưới `times` từ bản ghi
bộ phát hiện (không có nhãn). Mốc tiêm, root, loại lỗi gán ngẫu nhiên với seed cố định; 10 ô giả × 3 ca để bootstrap
theo ô chạy được như thật. Định dạng theo `src/p3/nhan.py` (so_ca, cases[opaque_id, root, fault, cell,
nhom_vi_tri_p75, inject_time]).

python nhan_gia.py <thư mục lượt bộ phát hiện có times> <tệp ra> [seed=20261007] [moc_chi_so=<i>] [root_tu=<lượt RCA>]
moc_chi_so: đặt mốc giả ở chỉ số i của mọi ca (để thành công chung đi qua nhánh t̂ ≥ t_tiêm).
root_tu: lấy root giả từ thứ hạng BARO trong lượt RCA đó, ở vị trí ngẫu nhiên 0..9; 1/5 số ca dùng root không tồn tại
(nhánh root vắng). Hai tùy chọn chỉ để phủ nhánh mã khi chạy khô; vẫn không đọc nhãn thật.
"""
import json
import random
import sys
from pathlib import Path

import chung

LOAI = ('cpu', 'mem', 'disk', 'delay', 'loss', 'socket')


def main(det_dir, out, seed='20261007', moc_chi_so=None, root_tu=None):
    rng = random.Random(int(seed))
    al = chung.nap_allowlist()
    ids = sorted(al)
    U = json.loads((chung.ROOT / 'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    d = chung.OUT / det_dir
    times = {}
    for p in sorted(d.glob('luot/*/ban-ghi-0.json')):
        r = json.loads(p.read_text(encoding='utf-8'))
        times[r['opaque_id']] = r['times']
    o = [(rng.choice(U), rng.choice(LOAI)) for _ in range(10)]
    baro = {}
    if root_tu:
        for p in sorted((chung.OUT / root_tu).glob('luot/baro-*/ban-ghi-0.json')):
            r = json.loads(p.read_text(encoding='utf-8'))
            baro[r['opaque_id']] = [x['entity'] for x in r['entity_ranking']]
    thu_tu = ids[:]
    rng.shuffle(thu_tu)
    cases = []
    for i, oid in enumerate(thu_tu):
        root, fault = o[i // 3]
        if baro:
            root = 'ts-khong-ton-tai' if rng.random() < 0.2 else baro[oid][rng.randrange(10)]
        tl = times[oid]
        cases.append({'opaque_id': oid, 'root': root, 'fault': fault, 'cell': f'{root}|{fault}',
                      'nhom_vi_tri_p75': rng.choice(('gia-1', 'gia-2')),
                      'inject_time': int(tl[int(moc_chi_so)] if moc_chi_so is not None
                                         else tl[rng.randrange(150, len(tl) - 150)])})
    doc = {'mo_ta': 'NHÃN GIẢ cho chạy khô T-025; không phải nhãn thật.', 'seed': int(seed), 'so_ca': len(cases),
           'cases': sorted(cases, key=lambda c: c['opaque_id'])}
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    chung.ghi_json(out, doc)
    print(json.dumps({'so_ca': len(cases), 'tep': str(out)}, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], **dict(a.split('=', 1) for a in sys.argv[3:]))
