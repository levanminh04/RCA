"""Đọc/ghép/tách tuần tự để không nạp cả khối K vào RAM; không đọc nhãn."""
import hashlib
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
import adapter_t047 as ad


def kiem(path):
    path = ad.duong_ra(path)
    m = json.loads((path / 'pha1.json').read_text(encoding='utf-8'))
    h, pairs = hashlib.sha256(), set()
    with (path / m['tep']).open('rb') as f:
        for b in f:
            h.update(b)
            if not b.strip():
                continue
            r = json.loads(b)
            ad.kiem_ban_ghi(r)
            k = (r['config_id'], r['opaque_id'])
            if k in pairs:
                raise ValueError('trùng bản ghi')
            pairs.add(k)
    cfg, oid = {c for c, o in pairs}, {o for c, o in pairs}
    if (h.hexdigest() != m['sha256'] or len(pairs) != m['so_ban_ghi']
        or len(pairs) != len(cfg)*len(oid) or len(oid) != m['so_ca'] or sorted(cfg) != m['cau_hinh']):
        raise ValueError('hash/ma trận pha1 sai')
    return m


def ghi_log(paths):
    rows = [(ad.duong_ra(p), kiem(p)) for p in paths]
    stamp = datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
    text = '\n### Hash pha 1 trước đọc nhãn — '+stamp+'\n\n'
    text += '\n'.join(f"- `{p.relative_to(ad.ROOT).as_posix()}`: `{m['sha256']}`" for p, m in rows)+'\n'
    with (ad.ROOT/'tasks/T-047-khoi-k-luot-2/LOG.md').open('ab') as f:
        f.write(text.encode('utf-8'))
    return {str(p.relative_to(ad.ROOT)): m['sha256'] for p, m in rows}


def tach(path):
    path = ad.duong_ra(path)
    m = kiem(path)
    out = path/'theo-cau-hinh'
    out.mkdir(exist_ok=False)
    files, hashes, counts, oids = {}, {}, {}, {}
    try:
        with (path/m['tep']).open('rb') as f:
            for b in f:
                r = json.loads(b)
                cid = r['config_id']
                if cid not in files:
                    d = out/cid
                    d.mkdir()
                    files[cid] = (d/'ban-ghi.jsonl').open('xb')
                    hashes[cid], counts[cid], oids[cid] = hashlib.sha256(), 0, set()
                files[cid].write(b); hashes[cid].update(b)
                counts[cid] += 1; oids[cid].add(r['opaque_id'])
    finally:
        for f in files.values():
            f.close()
    for cid in files:
        ad.ghi(out/cid/'pha1.json', dict(m, sha256=hashes[cid].hexdigest(), so_ban_ghi=counts[cid],
                                         so_ca=len(oids[cid]), cau_hinh=[cid], tach_tu=m['sha256']))
        kiem(out/cid)
    h = hashlib.sha256()
    for cid in sorted(files):
        with (out/cid/'ban-ghi.jsonl').open('rb') as f:
            for chunk in iter(lambda: f.read(1024*1024), b''):
                h.update(chunk)
    if h.hexdigest() != m['sha256']:
        raise ValueError('nối tệp tách không khớp gốc')
    ad.ghi(out/'tach.json', dict(sha256_goc=m['sha256'], phan=sorted(files), noi_lai_dung_goc=True))
    return [out/c for c in sorted(files)]
