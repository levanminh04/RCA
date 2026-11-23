# -*- coding: utf-8 -*-
"""T-069 bước 7 — nền của bản ghim có ồn hơn bản 3 không? (chỉ đọc đầu ra V082 đã lưu; không dùng nhãn ngoài tên ô để nhóm)
Dùng: py -3 -B results/T-069/phan_tich_nen.py [--ban V082-V066+H8a|P7] > results/T-069/phan-tich/nen.txt
So từng thực thể: max s trên ca không lỗi cũ (6) và mới (6); s của các kênh nghi ngờ trên mọi ca cũ/mới cùng ô."""
import json, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8')
R = 'D:/RCA-flashticket'
ban = sys.argv[sys.argv.index('--ban') + 1] if '--ban' in sys.argv else 'V082-V066+H8a'
TC = json.load(open(f'{R}/results/T-069/tieu-chi.json', encoding='utf-8'))
BT = json.load(open(f'{R}/results/T-069/bang-theo-o.json', encoding='utf-8')) if False else None


def cu_path(ma):
    for g in ('dev2', 'dev3'):
        for base in (f'{R}/results/T-064/kiem/nhan-r9/r9', f'{R}/results/T-064/kiem/nhan-luot5/l5'):
            p = f'{base}/{g}/d0/{ban}/{ma}/method-output-1.json'
            if os.path.exists(p): return p
    for p in (f'{R}/results/T-064/cham/dau-ra-dev2/{ban}/{ma}/method-output-1.json', f'{R}/results/T-064/cham/dau-ra-dev3/{ban}/{ma}/method-output-1.json'):
        if os.path.exists(p): return p


# ca mới: theo thứ tự lịch t069-chinh (sổ đã nhận hoặc nhật ký runner) — dùng danh sách truyền qua biến môi trường T069_MOI "o:ma,o:ma"
moi = [x.split(':') for x in os.environ['T069_MOI'].split(',')]
dem = {}; cap = []
for cp in TC['cap_ca']:
    o = cp['o']; k = dem.get(o, 0); dem[o] = k + 1
    cung = [m for oo, m in moi if oo == o]
    cap.append((o, cp['loai'], cp['cu']['ma'], cung[k] if k < len(cung) else None))


def doc(p):
    if not p or not os.path.exists(p): return None
    return json.load(open(p, encoding='utf-8'))


def max_s(m):
    o = {}
    for x in m['extra'].get('kenh_co', []):
        e = x['thuc_the']; o.setdefault(e, [0, 0]); o[e][0] = max(o[e][0], x['s']); o[e][1] += 1
    return o


NGHI = ['booking-service|op|booking-service|SELECT booking_schema.tbl_orders', 'booking-service|op|booking-service|SELECT booking_db',
        'ticket-service|op|ticket-service|SELECT ticket_db', 'keycloak|op|keycloak|SELECT keycloak_db.OUTBOX_ENTRY']
print(f'Bản: {ban}\n')
print('== Ca không lỗi: max s / số kênh có cờ theo thực thể (cũ | mới)')
ent = ['api-gateway', 'booking-service', 'event-service', 'payment-service', 'ticket-service', 'keycloak', 'user-service']
print(f'{"ô":16s} {"mã cũ":12s} {"mã mới":9s} ' + ' '.join(f'{e[:12]:>25s}' for e in ent))
for o, loai, mc, mm in cap:
    if loai == 'loi' or not mm: continue
    a, b = doc(cu_path(mc)), doc(f'{R}/results/T-069/dau-ra/dev3/d0/{ban}/{mm}/method-output-1.json')
    if not a or not b: print(o, mc, mm, 'thiếu'); continue
    sa, sb = max_s(a), max_s(b)
    print(f'{o:16s} {mc:12s} {mm:9s} ' + ' '.join(f'{sa.get(e, [0, 0])[0]:7.0f}/{sa.get(e, [0, 0])[1]:<3d}|{sb.get(e, [0, 0])[0]:7.0f}/{sb.get(e, [0, 0])[1]:<3d}  ' for e in ent)
          + f' verdict {a.get("verdict")[:6]}|{b.get("verdict")[:6]}')
print('\n== s của kênh nghi ngờ trên mọi ca (cũ → mới; 0 = không có cờ)')
print(f'{"ô":22s} ' + ' '.join(f'{n.split("|")[-1][:28]:>30s}' for n in NGHI))
for o, loai, mc, mm in cap:
    if not mm: continue
    a, b = doc(cu_path(mc)), doc(f'{R}/results/T-069/dau-ra/dev3/d0/{ban}/{mm}/method-output-1.json')
    if not a or not b: continue
    def s(m, n):
        e, rest = n.split('|', 1)
        return max([x['s'] for x in m['extra'].get('kenh_co', []) if x['thuc_the'] == e and x['don_vi'] == rest and x['huong'] == 'len'], default=0)
    print(f'{o:22s} ' + ' '.join(f'{s(a, n):12.0f} → {s(b, n):<14.0f}' for n in NGHI))
