# -*- coding: utf-8 -*-
"""T-069 bước 7.2–7.3 — so một ô cũ với mới trên đầu ra đã lưu (chỉ đọc).
Dùng: py -3 -B results/T-069/phan_tich_o.py <đầu ra cũ method-output-1.json> <đầu ra mới> [<thêm đầu ra để so, ví dụ lượt thử>...] [--goc <thực thể>] [--top 8]
In: 6 thực thể đầu (khóa xếp hạng); với thực thể gốc và các thực thể vượt lên: số kênh có cờ theo lớp, các kênh s lớn nhất;
kênh có ở bản này mà không ở bản kia (theo don_vi|huong); chú thích thành phần V082 (H5b, H8s1, H8a)."""
import json, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
a = sys.argv[1:]
goc = a[a.index('--goc') + 1] if '--goc' in a else None
top = int(a[a.index('--top') + 1]) if '--top' in a else 8
files = [x for i, x in enumerate(a) if not x.startswith('--') and (i == 0 or a[i - 1] not in ('--goc', '--top'))]
M = [json.load(open(f, encoding='utf-8')) for f in files]


def kc(m):
    return m['extra'].get('kenh_co', [])


tt = []
for i, m in enumerate(M):
    er = m.get('entity_ranking') or []
    print(f'== [{i}] {files[i]}\n   status={m.get("status")} verdict={m.get("verdict")} window={m.get("window")}')
    for j, e in enumerate(er[:6]):
        print(f'   {j + 1}. {e["entity"]:22s} tie={e.get("tie_group")} key={[round(x, 2) if isinstance(x, float) else x for x in e["key"]]}')
    tt.append([e['entity'] for e in er])
    ct = (m['extra'].get('m1_ft') or {}).get('chu_thich')
    if ct: print('   chu_thich:', json.dumps(ct, ensure_ascii=False)[:700])
# thực thể cần soi: gốc + mọi thực thể đứng trên gốc ở bất kỳ bản nào
soi = set([goc] if goc else [])
for r in tt:
    if goc in r:
        soi |= set(r[:r.index(goc)])
for ent in sorted(soi):
    print(f'\n##### {ent}')
    for i, m in enumerate(M):
        k = [x for x in kc(m) if x['thuc_the'] == ent]
        lop = collections.Counter(x['lop'] for x in k)
        print(f' [{i}] {len(k)} kênh có cờ; theo lớp {dict(lop)}; max s {max([x["s"] for x in k], default=0):.1f}')
        for x in sorted(k, key=lambda x: -x['s'])[:top]:
            print(f'      s={x["s"]:9.1f} {x["lop"]:10s} F_I={x["F_I"]} {x["huong"]:4s} {x["don_vi"]}')
    if len(M) >= 2:
        s0 = {x['don_vi'] + '|' + x['huong'] for x in kc(M[0]) if x['thuc_the'] == ent}
        s1 = {x['don_vi'] + '|' + x['huong'] for x in kc(M[1]) if x['thuc_the'] == ent}
        print(f'  chỉ ở [0]: {sorted(s0 - s1)[:12]}')
        print(f'  chỉ ở [1]: {sorted(s1 - s0)[:12]}')
