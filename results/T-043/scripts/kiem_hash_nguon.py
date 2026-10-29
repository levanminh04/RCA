"""Bước 0 của T-043: kiểm hash mọi nguồn ở mục Đầu vào của SPEC trước khi dùng.

Chỉ đọc. Mỗi nhóm so file với manifest đã ghim của chính task nguồn.
Ghi một file kết quả JSON; lệch hoặc thiếu file thì báo FAIL cho nhóm đó.
Chạy: python -B results/T-043/scripts/kiem_hash_nguon.py --out results/T-043/runs/hash-nguon-001
"""
import argparse
import hashlib
import json
import os
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def sha256(path, chunk=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(chunk), b''):
            h.update(block)
    return h.hexdigest()


def doc(rel):
    with open(ROOT / rel, encoding='utf-8') as f:
        return json.load(f)


def kiem_danh_sach(entries, chi_lay=None, dung=None):
    """entries: [(path, sha256, bytes|None)]. chi_lay: tập path cần kiểm (None = tất cả).

    dung: tập path T-043 thực sự dùng (None = mọi file đã kiểm). Trạng thái nhóm tính trên file dùng;
    lệch ở file không dùng (báo cáo .md, script, sổ sách thay đổi được) ghi riêng, không dùng file đó.
    """
    out = {'pass': 0, 'fail': [], 'missing': [], 'checked': []}
    for path, sha, size in entries:
        if chi_lay is not None and path not in chi_lay:
            continue
        full = ROOT / path
        if not full.is_file():
            out['missing'].append(path)
            continue
        if size is not None and full.stat().st_size != size:
            out['fail'].append({'path': path, 'ly_do': 'bytes', 'ky_vong': size, 'thuc': full.stat().st_size})
            continue
        got = sha256(full)
        if got != sha:
            out['fail'].append({'path': path, 'ly_do': 'sha256', 'ky_vong': sha, 'thuc': got})
            continue
        out['pass'] += 1
        out['checked'].append(path)
    if chi_lay is not None:
        thieu = sorted(set(chi_lay) - {e[0] for e in entries})
        if thieu:
            out['khong_co_trong_manifest'] = thieu
    if dung is not None:
        loi_dung = [x for x in out['fail'] if x['path'] in dung] + [p for p in out['missing'] if p in dung]
        out['lech_o_file_khong_dung'] = [x for x in out['fail'] if x['path'] not in dung]
        out['file_dung'] = sorted(dung)
        out['status'] = 'PASS' if not loi_dung and not out.get('khong_co_trong_manifest') else 'FAIL'
    else:
        out['status'] = 'PASS' if not out['fail'] and not out['missing'] and not out.get('khong_co_trong_manifest') else 'FAIL'
    if chi_lay is None or len(out['checked']) > 20:
        out['checked'] = len(out['checked'])
    return out


def nhom():
    g = {}
    m = doc('results/T-041/manifest.json')
    g['T-041'] = ('results/T-041/manifest.json#/outputs',
                  [(e['path'], e['sha256'], e.get('bytes')) for e in m['outputs']], None)
    m = doc('results/T-034/runs/manifest-cuoi-007/manifest.json')
    g['T-034'] = ('results/T-034/runs/manifest-cuoi-007/manifest.json#/files',
                  [(e['path'], e['sha256'], e.get('bytes')) for e in m['files']],
                  {'results/T-034/ban-do-g2.json', 'results/T-034/goi-g2.md', 'results/T-034/bang-baseline.json'})
    m = doc('results/T-035/manifest.json')
    g['T-035'] = ('results/T-035/manifest.json#/files',
                  [(e['path'], e['sha256'], e.get('bytes')) for e in m['files']], None)
    m = doc('results/T-036/runs/doi-chieu-smtp-001/artifact-manifest.json')
    g['T-036'] = ('results/T-036/runs/doi-chieu-smtp-001/artifact-manifest.json#/files',
                  [(e['path'], e['sha256'], e.get('bytes')) for e in m['files']], None)
    m = doc('results/T-032/chuoi-bang-chung.json')
    g['T-032'] = ('results/T-032/chuoi-bang-chung.json#/nguon_da_dung',
                  [(p, v['sha256'], v.get('bytes')) for p, v in m['nguon_da_dung'].items()],
                  {'results/T-032/runs/call-interval-001/summary.json',
                   'results/T-032/runs/call-slow-001/summary.json',
                   'results/T-032/runs/chain-position-002/summary.json',
                   'results/T-032/runs/chain-position-002/units.json'})
    m = doc('results/T-026/runs/session-005/handoff-manifest.json')
    g['T-026'] = ('results/T-026/runs/session-005/handoff-manifest.json#/files',
                  [(p, v['sha256'], v.get('bytes')) for p, v in m['files'].items()], None,
                  {'results/T-026/allowlist-dev.json', 'results/T-026/nhan-dev.json',
                   'results/T-026/ban-ghi-dua-vao-cham.json', 'results/T-026/cham-a.json'})
    m = doc('results/T-024/work/danh-sach-tep-cuoi.json')
    g['T-024'] = ('results/T-024/work/danh-sach-tep-cuoi.json#/results_files',
                  [(e['path'], e['sha256'], e.get('bytes')) for e in m['results_files']], None,
                  {'results/T-024/ban-ghi-dua-vao-cham.json', 'results/T-024/cham-a.json'})
    for run in ('normal-source-001', 'continuation-001'):
        rel = f'results/T-042/runs/{run}/manifest.json'
        m = doc(rel)
        g[f'T-042/{run}'] = (rel + '#/files', [(e['path'], e['sha256'], e.get('bytes')) for e in m['files']], None)
    m = doc('results/T-040/manifest.json')
    g['T-040'] = ('results/T-040/manifest.json#/files',
                  [(e['path'], e['sha256'], e.get('bytes')) for e in m['files']],
                  {'results/T-040/ban-giao-p6.md', 'results/T-040/yeu-cau-quan-sat-p9.md', 'results/T-040/con-mo.json'})
    for task, run in (('T-038', 'results/T-038/manifest.json'), ('T-039', 'results/T-039/manifest.json')):
        m = doc(run)
        g[task] = (run + '#/files', [(e['path'], e['sha256'], e.get('bytes')) for e in m['files']],
                   {f'results/{task}/do-thi/thuc-the.json', f'results/{task}/mapping.json'})
    m = doc('results/T-022/mappings/universe-re2tt-dev.json')
    pins = {k: v for k, v in m['nguon'].items() if isinstance(v, str) and k.startswith('results/')}
    g['T-022-allowlist'] = ('results/T-022/mappings/universe-re2tt-dev.json#/nguon (ghim allowlist)',
                            [(p, s, None) for p, s in pins.items()], {'results/T-022/allowlist-dev.json'})
    return g


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    args = ap.parse_args()
    out_dir = ROOT / args.out
    out_dir.mkdir(parents=True, exist_ok=False)
    t0 = time.time()
    ket_qua = {'schema': 'T043-hash-nguon-v1', 'root': str(ROOT), 'nhom': {}}
    for ten, spec in nhom().items():
        manifest, entries, chi_lay = spec[:3]
        dung = spec[3] if len(spec) > 3 else None
        t1 = time.time()
        r = kiem_danh_sach(entries, chi_lay, dung)
        r['manifest'] = manifest
        r['giay'] = round(time.time() - t1, 2)
        ket_qua['nhom'][ten] = r
        print(ten, r['status'], 'pass', r['pass'], 'fail', len(r['fail']), 'missing', len(r['missing']), flush=True)
    # Nhãn dev RE2-TT không có manifest ghim: ghi hash tại lúc dùng; đối chiếu chéo nội dung làm ở pha 2 KS-16.
    ket_qua['khong_manifest'] = {p: sha256(ROOT / p) for p in ('results/T-022/nhan-dev.json',)}
    ket_qua['tong_giay'] = round(time.time() - t0, 1)
    ket_qua['status'] = 'PASS' if all(v['status'] == 'PASS' for v in ket_qua['nhom'].values()) else 'FAIL'
    with open(out_dir / 'ket-qua.json', 'w', encoding='utf-8') as f:
        json.dump(ket_qua, f, ensure_ascii=False, indent=1)
    print('TONG', ket_qua['status'], ket_qua['tong_giay'], 'giay')


if __name__ == '__main__':
    main()
