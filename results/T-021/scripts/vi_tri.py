"""T-021 bước 3: nhóm vị trí service gốc theo Q-60(b) và quy tắc nhóm của SPEC T-021 (Đầu ra 3).

Chỉ dùng bậc đã lưu trong results/ (Minh chọn (a)). Không đọc dữ liệu đo.
Chạy: py -3 -X utf8 results/T-021/scripts/vi_tri.py --run vi-tri-001
Quy tắc nhóm (đồ thị service có hướng, cạnh từ bên gọi tới bên bị gọi):
  không có trong trace; bậc 0 (vào=0, ra=0); nguồn (vào=0, ra>0); lá (vào>0, ra=0);
  hub (vào>0, ra>0, tổng bậc >= phân vị q của mọi nút trong cùng đồ thị); giữa (vào>0, ra>0 còn lại).
  q = 75 (chính) và 90 (độ nhạy).
Bộ chỉ lưu bậc của root (Eadro, Nezha; S8 phương án (i)): "giữa hoặc hub", hub OPEN.
Gộp ca lên ô (S9): ô có nhóm X khi mọi ca của ô cùng nhóm X, nếu không thì "không ổn định".
"""
import argparse, collections, csv, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R = lambda *p: os.path.join(ROOT, *p)


def pct(vals, q):
    """Phân vị nội suy tuyến tính (giống numpy mặc định)."""
    v = sorted(vals)
    k = (len(v) - 1) * q / 100
    lo, hi = int(k), min(int(k) + 1, len(v) - 1)
    return v[lo] + (v[hi] - v[lo]) * (k - lo)


def group(present, din, dout, thr=None):
    if not present:
        return 'không có trong trace'
    if din == 0 and dout == 0:
        return 'bậc 0'
    if din == 0:
        return 'nguồn'
    if dout == 0:
        return 'lá'
    if thr is None:
        return 'giữa hoặc hub (hub OPEN)'
    return 'hub' if din + dout >= thr else 'giữa'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    out_dir = R('results/T-021/runs', a.run)
    os.makedirs(out_dir, exist_ok=False)
    per_case = []

    # RE2-TT, RE3-TT, RE2-OB: bậc của mọi service theo ca (T-002), hai cửa sổ
    src = 'results/T-002/local-inspection/run-002/all-service-positions.csv'
    g = collections.defaultdict(dict)
    with open(R(src), encoding='utf-8') as f:
        for x in csv.DictReader(f):
            g[(x['dataset'], x['case'], x['window'])][x['service']] = (int(x['in_degree']), int(x['out_degree']))
    for (ds, case, win), nodes in sorted(g.items()):
        _, *mid, fault, rep = case.split('_')
        root = '_'.join(mid)
        tot = [i + o for i, o in nodes.values()]
        t75, t90 = pct(tot, 75), pct(tot, 90)
        present = root in nodes
        din, dout = nodes.get(root, (0, 0))
        per_case.append(dict(dataset={'re2tt': 'RE2-TT', 're3tt': 'RE3-TT', 're2ob': 'RE2-OB'}[ds], case=case,
                             root=root, fault=fault, do_thi=win, gia_thuyet_dong_ho='', root_present=present,
                             vao=din, ra=dout, so_nut=len(nodes), nguong_p75=t75, nguong_p90=t90,
                             nhom_p75=group(present, din, dout, t75), nhom_p90=group(present, din, dout, t90),
                             nguon=src))

    # Eadro: bậc root trên đồ thị toàn file (có cả đoạn tiêm)
    src = 'results/T-009/runs/inspect-004/root-degree-whole-file.json'
    for i, x in enumerate(json.load(open(R(src), encoding='utf-8'))):
        din, dout = x['whole_file_in_degree'] or 0, x['whole_file_out_degree'] or 0
        gr = group(x['root_present'], din, dout)
        per_case.append(dict(dataset='Eadro-' + x['dataset'], case=x['session'] + '|' + x['fault'], root=x['root'],
                             fault=x['fault'], do_thi='toàn file', gia_thuyet_dong_ho='', root_present=x['root_present'],
                             vao=din, ra=dout, so_nut='', nguong_p75='', nguong_p90='', nhom_p75=gr, nhom_p90=gr,
                             nguon=f'{src}#{i}'))

    # Nezha: bậc root trên các file phút chồng ±60 s quanh lúc tiêm, hai giả thuyết đồng hồ
    src = 'results/T-008/runs/evidence-002/summary.json'
    for i, x in enumerate(json.load(open(R(src), encoding='utf-8'))['root_windows']):
        din, dout = x['in_degree'] or 0, x['out_degree'] or 0
        gr = group(x['root_present'], din, dout)
        per_case.append(dict(dataset='Nezha-' + x['dataset'], case=f"{x['dataset']}|{x['root']}|{x['fault']}|{x['inject_time']}",
                             root=x['root'], fault=x['fault'], do_thi='phút chồng ±60 s quanh lúc tiêm',
                             gia_thuyet_dong_ho=x['clock_interpretation'], root_present=x['root_present'],
                             vao=din, ra=dout, so_nut='', nguong_p75='', nguong_p90='', nhom_p75=gr, nhom_p90=gr,
                             nguon=f'{src}#root_windows[{i}]'))

    with open(os.path.join(out_dir, 'vi-tri-theo-ca.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(per_case[0]))
        w.writeheader()
        w.writerows(per_case)

    # Gộp lên ô (dataset, đồ thị, giả thuyết đồng hồ, root, lỗi)
    cells = collections.defaultdict(list)
    for x in per_case:
        cells[(x['dataset'], x['do_thi'], x['gia_thuyet_dong_ho'], x['root'], x['fault'])].append(x)
    cell_rows = []
    for k, xs in sorted(cells.items()):
        row = dict(zip(['dataset', 'do_thi', 'gia_thuyet_dong_ho', 'root', 'fault'], k), so_ca=len(xs))
        for q in ('p75', 'p90'):
            gs = {x['nhom_' + q] for x in xs}
            row['nhom_' + q] = gs.pop() if len(gs) == 1 else 'không ổn định'
        row['vao'] = '/'.join(sorted({str(x['vao']) for x in xs}))
        row['ra'] = '/'.join(sorted({str(x['ra']) for x in xs}))
        cell_rows.append(row)
    with open(os.path.join(out_dir, 'vi-tri-theo-o.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(cell_rows[0]))
        w.writeheader()
        w.writerows(cell_rows)

    # Tóm tắt: số ô theo nhóm, mỗi (dataset, đồ thị, giả thuyết)
    summ = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r_ in cell_rows:
        key = f"{r_['dataset']} | {r_['do_thi']} | {r_['gia_thuyet_dong_ho'] or '-'}"
        summ[key]['p75'][r_['nhom_p75']] += 1
        summ[key]['p90'][r_['nhom_p90']] += 1
    out = {k: {q: dict(c) for q, c in v.items()} for k, v in summ.items()}
    # Kiểm: Nezha, số sự kiện lệch nhóm giữa hai giả thuyết đồng hồ
    ev = collections.defaultdict(set)
    for x in per_case:
        if x['dataset'].startswith('Nezha'):
            ev[x['case']].add(x['nhom_p75'])
    out['_kiem'] = dict(nezha_su_kien=len(ev), nezha_lech_dong_ho=sum(1 for v in ev.values() if len(v) > 1),
                        so_ca_theo_bo=dict(collections.Counter((x['dataset'], x['do_thi']) and x['dataset'] + '|' + x['do_thi'] for x in per_case)))
    with open(os.path.join(out_dir, 'tom-tat.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
