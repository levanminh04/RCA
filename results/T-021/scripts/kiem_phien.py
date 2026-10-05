"""T-021: khoảng cách giữa các lần tiêm trong cùng phiên (Eadro) hoặc cùng ngày (Nezha), từ nhãn đã lưu.

Dùng cho câu hỏi cửa sổ và đơn vị chia. Chỉ đọc nhãn trong results/. Không đọc dữ liệu đo.
Chạy: py -3 -X utf8 results/T-021/scripts/kiem_phien.py --run kiem-phien-001
"""
import argparse, collections, json, os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R = lambda *p: os.path.join(ROOT, *p)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--run', required=True)
    a = ap.parse_args()
    out_dir = R('results/T-021/runs', a.run)
    os.makedirs(out_dir, exist_ok=False)
    out = {}
    src = 'results/T-009/runs/run-001/labels.json'
    lab = json.load(open(R(src), encoding='utf-8'))
    s = collections.defaultdict(list)
    for x in lab:
        s[(x['dataset'], x['source'])].append(x)
    for ds in ('SN', 'TT'):
        first, gaps, durs = [], [], set()
        for (d, _), v in s.items():
            if d != ds:
                continue
            v.sort(key=lambda x: x['start'])
            first.append(v[0]['start'] - v[0]['session_start'])
            gaps += [b['start'] - a_['end_derived'] for a_, b in zip(v, v[1:])]
            durs |= {x['duration'] for x in v}
        out['Eadro-' + ds] = dict(nguon=src, so_phien=len(first), so_lan_tiem=sum(len(v) for (d, _), v in s.items() if d == ds),
                                  giay_tu_dau_phien_toi_lan_tiem_dau=[round(min(first), 1), round(max(first), 1)],
                                  giay_nghi_giua_hai_lan_tiem=[round(min(gaps)), round(sorted(gaps)[len(gaps) // 2]), round(max(gaps))],
                                  thoi_luong_tiem_giay=sorted(durs))
    src = 'results/T-008/runs/run-001/labels.json'
    lab = json.load(open(R(src), encoding='utf-8'))
    d = collections.defaultdict(list)
    for x in lab:
        d[(x['dataset'], x['date'])].append(int(x['inject_timestamp_raw']))
    for ds in ('OB', 'TT'):
        gaps = []
        for (k, _), v in d.items():
            if k == ds:
                v.sort()
                gaps += [b - a_ for a_, b in zip(v, v[1:])]
        gaps.sort()
        out['Nezha-' + ds] = dict(nguon=src, so_ngay=sum(1 for (k, _) in d if k == ds),
                                  giay_giua_hai_lan_tiem=[gaps[0], gaps[len(gaps) // 2], gaps[-1]],
                                  ghi_chu='Nezha không ghi thời lượng tiêm; khoảng là giữa hai mốc tiêm')
    with open(os.path.join(out_dir, 'ket-qua.json'), 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == '__main__':
    main()
