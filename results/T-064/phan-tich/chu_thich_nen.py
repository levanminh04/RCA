# -*- coding: utf-8 -*-
"""Chú thích thao tác nền cho mọi ca không tiêm lỗi (tiêu chí §7, báo cáo kèm — KHÔNG đổi cách đếm K).
Với mỗi ca không lỗi × bản (P7, V002-H8s1, V028-H1c+H8s1): liệt kê kênh có cờ (`extra.kenh_co`) kèm số của đơn vị trong
`extra.don_vi_phan_vi` (n_N, n_A, tỉ lệ đuôi N → A, ngưỡng h), và các hướng bị H8-san bỏ (`extra.m1_ft.chu_thich`).
Chỉ số thay thế cho "giao dịch có suy giảm không": số đơn vị thao tác của api-gateway có cờ thô hướng lên (F_raw_len = 1)
trên tổng đơn vị hợp lệ của api-gateway — đây là phía M1 nhìn thấy, CHƯA đối chiếu số liệu k6.
Dùng: py -3 -B results/T-064/phan-tich/chu_thich_nen.py → chu-thich-thao-tac-nen.json + results/T-064/chu-thich-thao-tac-nen.md"""
import json, sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket/results')
BAN = ['P7', 'V002-H8s1', 'V028-H1c+H8s1']
DEV = {c['ma']: c['o'] for c in json.loads((R / 'T-064/tap-chon-dev2-13.json').read_text(encoding='utf-8'))['ca']}
KL = set(x['o'] for x in json.loads((R / 'T-064/dap-an-dev2.json').read_text(encoding='utf-8'))['o_khong_loi'])
CA = [('dev2', m, o) for m, o in DEV.items() if o in KL]
CA += [('t062', c['ma'], c['o']) for c in json.loads((R / 'T-062/ket-qua/phat-lai/bang-cham.json').read_text(encoding='utf-8'))['ca'] if not c['tap_chap_nhan']]


def duong(tap, ban, ma):
    if tap == 'dev2': return R / 'T-064/cham/dau-ra-dev2' / ban / ma / 'method-output-1.json'
    if ban == 'P7': return R / 'T-062/ca' / ma / 'outputs' / ma / 'method-output-1.json'
    tm = 'ra-khong-hoi-quy-2' if ban.startswith('V028') else 'ra-khong-hoi-quy-1'
    return R / 'T-064/bien-the' / ban / tm / ma / 'method-output-1.json'


out = {'ghi_chu': __doc__, 'ca': []}
for tap, ma, o in CA:
    for ban in BAN:
        f = duong(tap, ban, ma)
        if not f.exists(): out['ca'].append({'tap': tap, 'ma': ma, 'o': o, 'ban': ban, 'thieu': str(f)}); continue
        d = json.loads(f.read_text(encoding='utf-8')); e = d['extra']
        dv = {x['ma']: x for x in e['don_vi_phan_vi']}
        co = []
        for k in e['kenh_co']:
            x = dv.get(k['don_vi'], {})
            co.append({'thuc_the': k['thuc_the'], 'don_vi': k['don_vi'], 'huong': k['huong'], 'lop': k['lop'], 's': round(k['s'], 1), 'F_I': k['F_I'],
                       'n_N': x.get('n_N'), 'n_A': x.get('n_A'), 'r_N': x.get('r_len_N'), 'r_A': x.get('r_len_A'), 'h': x.get('h')})
        gw = [x for x in e['don_vi_phan_vi'] if x['ma'].startswith('op|api-gateway|') and x.get('hop_le')]
        h8 = ((e.get('m1_ft') or {}).get('chu_thich') or {}).get('H8-san') or {}
        out['ca'].append({'tap': tap, 'ma': ma, 'o': o, 'ban': ban, 'verdict': d['verdict'], 'so_kenh_co': len(co), 'kenh_co': co,
                          'thuc_the_co_co': sorted({c['thuc_the'] for c in co}),
                          'gateway_don_vi_hop_le': len(gw), 'gateway_co_tho_len': sum(1 for x in gw if x.get('F_raw_len')),
                          'h8_bo': h8.get('don_vi_bo_co')})
(R / 'T-064/phan-tich/chu-thich-thao-tac-nen.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')

L = ['# T-064 — Chú thích thao tác nền ở ca không tiêm lỗi', '',
     'Sinh bởi `results/T-064/phan-tich/chu_thich_nen.py` từ đầu ra đã lưu; số đầy đủ ở `results/T-064/phan-tich/chu-thich-thao-tac-nen.json`.',
     'Bảng này là báo cáo kèm (tiêu chí §7). **K vẫn đếm thô**, không trừ theo chú thích.',
     'Cột "Gateway" là số đơn vị thao tác của `api-gateway` có cờ thô hướng lên trên tổng đơn vị hợp lệ. Đây là chỉ số thay thế phía M1 cho câu "giao dịch có suy giảm không"; **chưa đối chiếu số liệu k6**.',
     'Với đơn vị `op|…`: ngưỡng `h` và độ vượt tính bằng micro giây; tỉ lệ đuôi = tỉ lệ lần chạy vượt `h`, ghi N → A. Với đơn vị `metric|…`: `h` theo đơn vị của metric đó, n là số mẫu của cửa sổ; kênh log không có các cột này.',
     'Lưu ý mục 3: độ vượt lớn nhất bị bỏ ở nhiều ca nằm sát sàn 1 ms (762–985 µs), nên kết quả K nhạy với giá trị sàn; chưa quét sàn khác.', '',
     '## 1. Tổng quan', '', '| Tập | Ca | Ô | Bản | Kết luận | Số kênh có cờ | Thực thể có cờ | Gateway |', '|---|---|---|---|---|---|---|---|']
for c in out['ca']:
    if 'thieu' in c: L.append(f"| {c['tap']} | {c['ma']} | {c['o']} | {c['ban']} | thiếu đầu ra | | | |"); continue
    tt = ', '.join(c['thuc_the_co_co']) if len(c['thuc_the_co_co']) <= 4 else f"{len(c['thuc_the_co_co'])} thực thể"
    L.append(f"| {c['tap']} | {c['ma']} | {c['o']} | {c['ban']} | {c['verdict']} | {c['so_kenh_co']} | {tt} | {c['gateway_co_tho_len']}/{c['gateway_don_vi_hop_le']} |")
L += ['', '## 2. Kênh có cờ ở ca còn bị kết luận có nguyên nhân dưới V028 (tối đa 8 kênh mạnh nhất mỗi ca)', '',
      '| Ca | Ô | Thực thể | Đơn vị | Hướng | s | n_N → n_A | Tỉ lệ đuôi N → A | h |', '|---|---|---|---|---|---|---|---|---|']
fmt = lambda v: '' if v is None else (f'{v:.3f}' if isinstance(v, float) and v < 10 else f'{v:.0f}' if isinstance(v, float) else str(v))
for c in out['ca']:
    if c.get('ban') != 'V028-H1c+H8s1' or c.get('verdict') == 'NO_INTRINSIC_ANOMALY' or 'thieu' in c: continue
    for k in sorted(c['kenh_co'], key=lambda k: -k['s'])[:8]:
        L.append(f"| {c['ma']} | {c['o']} | {k['thuc_the']} | `{k['don_vi']}` | {k['huong']} | {k['s']} | {fmt(k['n_N'])} → {fmt(k['n_A'])} | {fmt(k['r_N'])} → {fmt(k['r_A'])} | {fmt(k['h'])} |")
L += ['', '## 3. Hướng có cờ bị sàn 1 ms (H8-san) bỏ, bản V028', '', '| Ca | Ô | Số hướng bị bỏ | Độ vượt trung bình lớn nhất (µs) | Đơn vị có độ vượt lớn nhất |', '|---|---|---|---|---|']
for c in out['ca']:
    if c.get('ban') != 'V028-H1c+H8s1' or 'thieu' in c: continue
    b = c['h8_bo'] or []
    m = max(b, key=lambda x: x['vuot_tb']) if b else None
    L.append(f"| {c['ma']} | {c['o']} | {len(b)} | {m['vuot_tb']:.0f} | `{m['ma']}` |" if m else f"| {c['ma']} | {c['o']} | 0 | | |")
L += ['', '## 4. Đọc bảng thế nào', '',
      '- Quan sát, không phải cơ chế. Cơ chế từng ca và phần chưa xác định ở `results/T-064/phan-tich/ghi-chu-co-che-dev2.md` (Q1, Q4).',
      '- Ca BINH-THUONG còn cờ dưới V028: nguyên nhân chưa xác định (Q4). FLASH-HEALTHY: độ trễ thật tăng dưới tải, việc tính ca này thế nào chờ Minh.', '']
(R / 'T-064/chu-thich-thao-tac-nen.md').write_text('\n'.join(L), encoding='utf-8', newline='\n')
print('\n'.join(L[8:]))
