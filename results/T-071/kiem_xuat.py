"""T-071 — kiểm lượt xuất: số điểm theo phút trong cửa sổ có tải cho từng chuỗi (đọc file đã xuất, không truy vấn)."""
import gzip, json, sys, pathlib, collections, datetime as dt
d = pathlib.Path(sys.argv[1]); tai0, tai1 = sys.argv[2], sys.argv[3]  # ISO, ví dụ 2026-11-18T07:57:34Z
f = lambda s: dt.datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()
a, b = f(tai0), f(tai1)
tom = json.loads((d / 'tom-tat.json').read_text(encoding='utf-8'))
out = {'cua_so_tai': [tai0, tai1], 'xuat': str(d), 'chuoi': {}}
for ten, m in tom['chuoi'].items():
    r = json.load(gzip.open(d / m['file'], 'rt', encoding='utf-8'))
    step = r.get('step_s') or 10
    e = {'loai': r['loai'], 'bo_nhan': len(r['result']), 'khuc_loi': len(m['khuc_loi'])}
    if r['loai'] == 'range' and r['result']:
        # phút đầy đủ trong cửa sổ tải (bỏ phút chứa mốc đầu/cuối)
        p0 = int(a // 60 + 1) * 60; p1 = int(b // 60) * 60
        per = []
        for s in r['result']:
            ts = sorted(float(t) for t, _ in s['values'])
            c = collections.Counter(int(t // 60) * 60 for t in ts if p0 <= t < p1)
            per.append([c.get(p, 0) for p in range(p0, p1, 60)])
            gaps = [t2 - t1 for t1, t2 in zip(ts, ts[1:]) if a <= t1 and t2 <= b and t2 - t1 > step]
            e.setdefault('khoang_ho_trong_tai_s', []).append(max(gaps) if gaps else 0)
            e.setdefault('diem_dau_utc', []).append(dt.datetime.fromtimestamp(ts[0], dt.timezone.utc).strftime('%H:%M:%S'))
        flat = [x for p in per for x in p]
        e.update(so_phut_day_du=p1 - p0 and (p1 - p0) // 60, mau_phut_min=min(flat), mau_phut_max=max(flat),
                 phut_thieu=sum(x < 60 // step for x in flat))
    elif r['loai'] == 'tho' and r['result']:
        ts = [float(t) for s in r['result'] for t, _ in s['values'] if a <= float(t) <= b]
        e['diem_trong_tai'] = len(ts)
        per_set = [sum(1 for t, _ in s['values'] if a <= float(t) <= b) for s in r['result']]
        e['diem_moi_bo_nhan_min_max'] = [min(per_set), max(per_set)]
    out['chuoi'][ten] = e
json.dump(out, open(d.parent / 'kiem-xuat.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
for k, v in out['chuoi'].items(): print(k, {x: y for x, y in v.items() if x not in ('diem_dau_utc',)}, v.get('diem_dau_utc', [''])[:1])
