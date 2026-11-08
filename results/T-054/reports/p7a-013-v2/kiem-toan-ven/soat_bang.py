"""Soát máy mọi số ở bảng §4 và §5 của một bản báo cáo P7(a) so với phan-tich-nhom.json (đáp REVIEW R1).

Chạy: py -3 -B results/T-054/reports/p7a-013-v2/kiem-toan-ven/soat_bang.py <bao-cao.md> [<bao-cao khác> ...]
In số ô đã so và danh sách lệch (làm tròn 3 chữ số với §4; theo số chữ số in ra với §5).
"""
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
PT = json.loads((REPO / 'results/T-054/reports/p7a-013-v2/phan-tich-nhom.json').read_bytes())
NAME = {'M1': 'M1', 'TORAI B (ba seed, gộp trong ca)': 'torai_B', 'SimpleRCA (M4)': 'simplerca', 'TraceRCA': 'tracerca',
        'BARO': 'baro', 'CIRCA (RHT+DA)': 'circa', 'CIRCA RHT, phụ': 'circa_rht_aux', 'MicroRank': 'microrank',
        'C-a0 (bỏ E1/E2/E5/E7)': 'C-a0', 'C-a0': 'C-a0', 'C-a1 (còn E1)': 'C-a1', 'C-a1': 'C-a1',
        'C-d1 (sâu nhất)': 'C-d1', 'C-d1': 'C-d1', 'C-d2 (khởi phát sớm nhất)': 'C-d2', 'C-d2': 'C-d2',
        'C-d3 (đường tới đích)': 'C-d3', 'C-c (RRF ba baseline)': 'C-c', 'C-c': 'C-c', 'C-g (SimpleRCA + E6b)': 'C-g',
        'C-g': 'C-g', 'T12-on': 'T12-on'}


def num(s):
    return float(s.strip().replace('−', '-').replace('+', '').replace(',', '.'))


def soat(path):
    txt = Path(path).read_text(encoding='utf-8')
    s4 = txt.split('## 4.')[1].split('## 5.')[0]
    s5 = txt.split('## 5.')[1].split('**Thông tin cấu trúc')[0]
    bad, n, ds = [], 0, None
    bang = PT['bang_theo_ve_P']
    for line in s4.splitlines():
        if 'RE2-TT, 60 ca' in line:
            ds = 'RE2-TT'
        if 'Nezha-OB, 34 ca' in line:
            ds = 'Nezha-OB'
        m = re.match(r'\| (.+?) \| ([0-9,]+) \| ([0-9,]+) \| ([0-9,]+) \| ([0-9,]+) \| ([0-9,]+) \|', line)
        if m and ds and m.group(1) in NAME:
            v = bang[f'{ds}|{NAME[m.group(1)]}']
            exp = [v['MRR']['xap_xi'], v['hit@1'], v['hit@3'], v['Hit5_Q']['xap_xi'], v['ndcg@5']]
            for k, (e, g) in enumerate(zip(exp, m.groups()[1:])):
                n += 1
                if abs(round(e, 3) - num(g)) > 1e-9:
                    bad.append({'muc': '§4', 'bo': ds, 've': m.group(1), 'cot': ['MRR', 'Hit@1', 'Hit@3', 'Hit@5', 'NDCG@5'][k],
                                'file': round(e, 4), 'bao_cao': g})
        m2 = re.match(r'\| bỏ E1 / bỏ E2 / bỏ E5 \| ([0-9,]+) / ([0-9,]+) / ([0-9,]+)', line)
        if m2 and ds:
            for a, g in zip(('bo-E1', 'bo-E2', 'bo-E5'), m2.groups()):
                n += 1
                e = bang[f'{ds}|{a}']['MRR']['xap_xi']
                if abs(round(e, 3) - num(g)) > 1e-9:
                    bad.append({'muc': '§4', 'bo': ds, 've': a, 'cot': 'MRR', 'file': round(e, 4), 'bao_cao': g})
    so = PT['so_cap']
    for line in s5.splitlines():
        m = re.match(r'\| `(.+?)` \| ([^|]+) \| (\d+)/(\d+)/(\d+) \| ([^|]+) \| \[([^;]+); ([^\]]+)\] \|', line)
        if not m:
            continue
        key = m.group(1).replace('\\|', '|')
        v = so[key]
        dtxt = m.group(2).strip()
        dig = len(dtxt.split(',')[1]) if ',' in dtxt else 0
        ci = v['CI_bootstrap_cell']['CI']['rr']
        if (v['win'], v['tie'], v['loss']) != tuple(int(x) for x in m.group(3, 4, 5)):
            bad.append({'muc': '§5', 'khoa': key, 'cot': 'thắng/hòa/thua'})
        for name, e, g, d in (('delta', v['delta_mean']['xap_xi'], dtxt, dig), ('CI lo', ci['lo'], m.group(7), 3),
                              ('CI hi', ci['hi'], m.group(8), 3)):
            n += 1
            if abs(round(e, d) - num(g)) > 1e-9 and not (abs(e) < 5e-4 and num(g) == 0):
                bad.append({'muc': '§5', 'khoa': key, 'cot': name, 'file': e, 'bao_cao': g.strip()})
    return {'file': str(path), 'so_o_da_so': n, 'lech': bad}


if __name__ == '__main__':
    print(json.dumps([soat(p) for p in sys.argv[1:]], ensure_ascii=False, indent=1))
