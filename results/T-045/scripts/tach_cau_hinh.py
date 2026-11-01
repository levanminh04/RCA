"""T-045: tách `ban-ghi.jsonl` của một lượt nhiều cấu hình (khối K: 16 cấu hình, khoảng 0,9 GB ở RE2-TT; T4: 9 cấu hình)
thành từng cấu hình, để pha 2 dùng nguyên `m1_danh_gia.pha2.cham` trên từng phần mà không nạp cả tệp vào bộ nhớ.
Không đọc nhãn; không đổi byte nào của bản ghi.

Đầu ra: `<lượt>/theo-cau-hinh/<config_id>/ban-ghi.jsonl` và `pha1.json` (cùng trường như `runner.pha1`), cùng
`<lượt>/theo-cau-hinh/tach.json` (sha256 từng phần). Kiểm: (1) sha256 tệp gốc khớp `pha1.json` của lượt; (2) nối các
dòng của mọi phần theo (config_id, opaque_id) cho đúng từng byte tệp gốc; (3) mỗi phần đủ số ca của lượt.
Chạy: $PY -B results/T-045/scripts/tach_cau_hinh.py <thư mục lượt>
"""
import hashlib
import json
import sys
from pathlib import Path


def main(d):
    d = Path(d)
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    goc = d / meta['tep']
    h = hashlib.sha256()
    phan = {}
    with open(goc, 'rb') as f:
        for dong in f:
            h.update(dong)
            if not dong.strip():
                continue
            r = json.loads(dong)
            phan.setdefault(r['config_id'], []).append(((r['config_id'], r['opaque_id']), dong.rstrip(b'\n')))
    if h.hexdigest() != meta['sha256']:
        raise SystemExit('hash tệp gốc lệch pha1.json')
    out = d / 'theo-cau-hinh'
    out.mkdir(exist_ok=False)
    h2 = hashlib.sha256()
    tach = {'luot': str(d).replace('\\', '/'), 'sha256_goc': meta['sha256'], 'phan': {}}
    for cid in sorted(phan):
        dong = sorted(phan[cid], key=lambda z: z[0])
        if len(dong) != meta['so_ca']:
            raise SystemExit(f'{cid}: {len(dong)} bản ghi, mong {meta["so_ca"]}')
        du = b'\n'.join(x for _, x in dong) + b'\n'
        h2.update(du)
        p = out / cid
        p.mkdir()
        (p / 'ban-ghi.jsonl').write_bytes(du)
        s = hashlib.sha256(du).hexdigest()
        m = {'tep': 'ban-ghi.jsonl', 'sha256': s, 'so_ban_ghi': len(dong), 'phien_ban': meta.get('phien_ban'),
             'cau_hinh': [cid], 'so_ca': meta['so_ca'], 'tach_tu': {'luot': tach['luot'], 'sha256': meta['sha256']}}
        (p / 'pha1.json').write_text(json.dumps(m, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n',
                                     encoding='utf-8')
        tach['phan'][cid] = s
    if h2.hexdigest() != meta['sha256']:
        raise SystemExit('nối các phần không ra đúng tệp gốc')
    tach['noi_lai_dung_goc'] = True
    (out / 'tach.json').write_text(json.dumps(tach, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'luot': tach['luot'], 'so_phan': len(tach['phan']), 'noi_lai_dung_goc': True}, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1])
