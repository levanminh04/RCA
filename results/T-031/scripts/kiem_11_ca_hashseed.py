"""T-031: kiểm tập "ca lỗi làm tròn" (Q-82) có đổi theo hash seed không.

Đọc bản ghi `ols+rht` (ban-ghi-1.json) của runs/circa-ols-h{0,1,2}-001; ca có ít nhất một
khóa > 1e10 là ca lỗi làm tròn. Không dùng nhãn, không chấm. Chạy từ gốc repo:
    py -3 results/T-031/scripts/kiem_11_ca_hashseed.py
"""
import glob
import json
from pathlib import Path

GOC = Path('results/T-031')
NGUONG = 1e10


def main():
    out = {'mo_ta': __doc__, 'nguong': NGUONG, 'theo_hashseed': {}}
    tap = {}
    for h in (0, 1, 2):
        s, n = set(), 0
        for d in sorted(glob.glob(str(GOC / f'runs/circa-ols-h{h}-001/luot/*'))):
            b = json.loads(Path(d, 'ban-ghi-1.json').read_text(encoding='utf-8'))
            assert b['variant'] == 'ols+rht' and b['status'] == 'OK', d
            n += 1
            if any(abs(float(x['key'][0])) > NGUONG for x in b['ranking']):
                s.add(b['opaque_id'])
        tap[h] = s
        out['theo_hashseed'][str(h)] = {'so_luot': n, 'so_ca': len(s), 'ca': sorted(s)}
    out['giong_nhau'] = tap[0] == tap[1] == tap[2]
    (GOC / 'kiem-11-ca-hashseed.json').write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
    print(json.dumps({k: v['so_ca'] for k, v in out['theo_hashseed'].items()}), out['giong_nhau'])


if __name__ == '__main__':
    main()
