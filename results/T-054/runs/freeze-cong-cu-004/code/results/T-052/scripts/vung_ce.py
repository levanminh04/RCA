"""Đọc nguồn đã seal: vùng, C-e, vị trí N, C-d; không chạy lại M1."""
import time
from collections import Counter
from fractions import Fraction

from common import ROOT, RUN, native_index, native_rows, metadata, pin, read, save, timing
from m1_danh_gia import e7
from p3 import danh_gia
import numpy as np

BASE = 'K-E1+E2+E5'


def position(nodes, edges, root, q):
    incoming = Counter(b for a, b in edges)
    outgoing = Counter(a for a, b in edges)
    threshold = float(np.percentile([incoming[v] + outgoing[v] for v in nodes], q)) if nodes else None
    i, o = incoming[root], outgoing[root]
    group = ('không có trong trace' if root not in nodes else 'bậc 0' if i == o == 0 else
             'nguồn' if i == 0 else 'lá' if o == 0 else 'hub' if i + o >= threshold else 'giữa')
    return dict(group=group, in_degree=i, out_degree=o, percentile=q, threshold=threshold,
                node_count=len(nodes), definition='Trace N; R0 giữ span bọc; cùng alias, end<t, service/entity owner.')


def main():
    start = time.perf_counter()
    entries, _, _ = metadata()
    m, index = native_index()
    m51 = read('results/T-051/manifest.json')
    scored = read('results/T-052/ket-qua-dev-doc-lap-001.json')
    labels = scored['labels']
    real, ce = [], []
    top = Counter()
    for entry in entries:
        job = entry['job']
        item, _ = index[(job['opaque_id'], job['window'])]
        rows = native_rows(item, m, {BASE, 'K-R0'})
        rec, r0 = rows[BASE], rows['K-R0']
        root = labels[job['opaque_id']]['root']
        O = rec['sets']['observed']
        common = {'index': entry['index'], 'opaque_id': job['opaque_id'], 'dataset': job['dataset'],
                  'source': item['path'], 'status': rec['status'], 'O': O,
                  'coverage': rec['coverage'], 'do_phu_cham': rec['do_phu_cham']}
        if job['window'] == 'ce':
            returned = {e for b in rec['blocks'] for g in b['groups'] for e in g}
            mass = {e: danh_gia.phan_bo_hang(danh_gia.khoi_tu_ban_ghi(rec), e).get(1, Fraction(0)) for e in returned}
            top.update(mass)
            dist = danh_gia.phan_bo_hang(danh_gia.khoi_tu_ban_ghi(rec), root)
            n = len(returned)
            ce.append(dict(common, top_mass={k: v for k, v in mass.items() if v}, returned=n,
                       root_future_present=root in returned, RR_future=sum((v / r for r, v in dist.items()), Fraction(0)),
                       V0=rec['verdict'], N1=sum(t == 1 for t in rec['extra']['tang_P'].values()),
                       chance_returned_RR=sum((Fraction(1, r) for r in range(1, n + 1)), Fraction(0)) / n if n and root in returned else None))
            continue
        nodes = {u['ma'].split('|', 2)[1] for u in r0['extra']['don_vi_phan_vi'] if u['ma'].startswith('op|') and u['n_N'] > 0}
        edges = {tuple(x) for x in r0['extra']['G_N']}
        assert all(a in nodes and b in nodes for a, b in edges)
        regions = {f'cach_{k}': e7.mo_ta(rec['region']['T'], rec['region'][f'cach_{k}'], root, O) for k in (1, 2)}
        t12_path = f"results/T-051/t12-001/{entry['index']:02d}.json"
        pin(t12_path, m51['outputs'][t12_path])
        pair = read(t12_path)
        on = pair['worlds']['P']['region'][1]
        regions_on = {f'cach_{k}': e7.mo_ta(on['T'], on[f'cach_{k}'], root, O) for k in (1, 2)}
        controls = {}
        for name, r in rec['extra']['doi_chung'].items():
            if name == 'C-d3' and job['dataset'] != 'RE2-TT': continue
            dist = danh_gia.phan_bo_hang(r['blocks'], root) if r['trang_thai'] == 'OK' else {}
            controls[name] = dict(status=r['trang_thai'], metrics=danh_gia.do_ca(dist, r['trang_thai'] == 'OK'),
                                 RR=sum((v / rank for rank, v in dist.items()), Fraction(0)))
        real.append(dict(common, regions=regions, T12_on_regions=regions_on, controls=controls,
                    N_position_p75=position(nodes, edges, root, 75), N_position_p90=position(nodes, edges, root, 90)))
    summary = {}
    for ds in ('RE2-TT', 'Nezha-OB'):
        current = [r for r in real if r['dataset'] == ds]
        summary[ds] = {'n': len(current), 'regions': {}, 'controls': {},
                       'N_positions_p75': Counter(r['N_position_p75']['group'] for r in current)}
        for arm in ('regions', 'T12_on_regions'):
            summary[ds][arm] = {f'cach_{k}': {key: sum(r[arm][f'cach_{k}'][key] for r in current) / len(current)
                                          for key in ('p', 'R_ky_vong', 'R_ky_vong_tren_O', 'co_hop')} for k in (1, 2)}
        for name in current[0]['controls']:
            summary[ds]['controls'][name] = {'MRR': sum((r['controls'][name]['RR'] for r in current), Fraction(0)) / len(current),
                          'statuses': Counter(r['controls'][name]['status'] for r in current)}
    assert len(ce) == 30 and len(real) == 52
    ce_summary = {'n': len(ce), 'top_mass': top, 'unique_top_entities': sum(v > 0 for v in top.values()),
                  'V0': Counter(r['V0'] for r in ce), 'mean_N1': Fraction(sum(r['N1'] for r in ce), len(ce)),
                  'MRR_future': sum((r['RR_future'] for r in ce), Fraction(0)) / len(ce),
                  'root_future_absent': sum(not r['root_future_present'] for r in ce),
                  'caveat': 'Mốc trước tiêm chưa được xác nhận lành; RR nhãn tương lai không kiểm thiên lệch vật lý.'}
    save(ROOT / 'results/T-052/vung-ce-va-vi-tri-001.json', {'real': real, 'summary': summary, 'ce': ce,
          'ce_summary': ce_summary, 'limits': ['Vùng nghi ngờ; chưa có P/R/F1 vùng ảnh hưởng.',
          'Nhóm N dựng từ code và native R0 đã ghim; không suy vị trí vật lý hoặc topo chưa quan sát.']})
    save(RUN / 'vung-ce-summary.json', timing('regions_ce', start, PASS=True, real=52, ce=30,
          label_join='Đầu ra nguồn đã seal trước evaluator; không có lượt chạy phương pháp mới.'))


if __name__ == '__main__':
    main()
