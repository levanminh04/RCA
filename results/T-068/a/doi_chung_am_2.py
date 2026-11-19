#!/usr/bin/env python3
"""T-068 A, bản 2 (19/11, sửa theo phản biện Codex điểm 1, 2, 4, 6): đối chứng âm cho bộ kiểm độc lập và bộ dựng
service-graph-5. Bản 1 (`doi_chung_am.py`, `doi-chung-am.json`) giữ nguyên làm bằng chứng lượt cũ.

Dùng: py -3 -I doi_chung_am_2.py <thư mục tạm> <repo lab> <thư mục đồ thị v5> <tệp JSON ra>
Ghi đúng một đối tượng JSON vào <tệp JSON ra> (byte LF); mã thoát 0 khi mọi mục đạt, 1 khi không.

Bộ kiểm độc lập (dem_doc_lap.py) phải báo lệch với bản sao bị sửa:
 1 sai số; 2 cạnh DB tới đích ngoài classes; 3 link trên cạnh; 4 sai p95; 5 kỳ vọng trên cửa sổ dịch 1.000 ms;
 7 cạnh cha–con tới đích ngoài classes; 11 nút chú thích mất link; 12 nút chú thích đặt var-dv rỗng.
Bộ dựng (service_graph.py):
 6 file ca có cửa sổ dịch 1.000 ms -> kiểm chéo dừng, không ghi file;
 8 span DB kind SERVER -> không vẽ, đếm "không vẽ" (bộ kiểm độc lập trên cùng span cũng không kỳ vọng cạnh);
 9 quan hệ cha–con tới dịch vụ ngoài classes -> không vẽ, kiểm chéo vẫn đếm đủ;
 10a --tat-ca, gói ca thứ hai không tồn tại -> thoát khác 0, không ghi file nào;
 10b --tat-ca, gói ca thứ hai sai sha256 -> thoát khác 0, không ghi file nào (kể cả ca thứ nhất);
 10c --tat-ca hai ca đúng -> thoát 0, ghi đủ file (đối chứng dương cho 10a, 10b).
"""
import importlib.util
import json
import pathlib
import shutil
import subprocess
import sys

R = pathlib.Path('D:/RCA-flashticket')
DU = R / 'results/T-065/may-l11/du-lieu'
NT = R / 'results/T-068/a/nguon-trace.json'
KIEM = R / 'results/T-068/kiem/dem_doc_lap.py'
BAN, CA = 'V082-V066+H8a', 'eb48d6b3'
CA2 = '46aab4be'
BAN_KC, CA_KC = 'p7', 'ebd5ef38'  # cặp "không có đầu ra"


def nap(ten, p):
    spec = importlib.util.spec_from_file_location(ten, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    tmp, lab, sg_dir, ra = (pathlib.Path(x) for x in sys.argv[1:5])
    if tmp.exists():
        sys.exit(f'thư mục tạm đã có: {tmp}')
    ket = {}

    def chay(dt, ban, ca, extra=()):
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', str(KIEM), '--du-lieu', str(DU), '--do-thi', str(dt),
                            '--nguon-trace', str(NT), '--cap', f'{ban}/{ca}', *extra],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        return {'ma_thoat': r.returncode, 'loi': json.loads(r.stdout)['loi']}

    def sua(ten, ban, ca, f):
        g = json.loads((sg_dir / ban / f'{ca}.json').read_text(encoding='utf-8'))
        f(g)
        d = tmp / ten / ban
        d.mkdir(parents=True, exist_ok=True)
        (d / f'{ca}.json').write_bytes(json.dumps(g, ensure_ascii=False).encode('utf-8'))
        return chay(tmp / ten, ban, ca)

    def bao(r):  # bộ kiểm phải báo lệch
        return r['ma_thoat'] == 1 and bool(r['loi'])

    muc = {}
    r = chay(sg_dir, BAN, CA)
    muc['0_goc'] = (r, r['ma_thoat'] == 0 and not r['loi'])
    r = chay(sg_dir, BAN_KC, CA_KC)
    muc['0b_goc_khong_co_dau_ra'] = (r, r['ma_thoat'] == 0 and not r['loi'])
    for ten, f in [
        ('1_sai_so', lambda g: g['canh'][0].update(detail__so_A=g['canh'][0]['detail__so_A'] + 1)),
        ('2_db_ngoai_classes', lambda g: g['canh'].append({**g['canh'][0], 'id': 'x', 'target': 'khong-co',
                                                           'detail__loai': 'db'})),
        ('3_link_canh', lambda g: g['canh'][0].update(detail__url='/d/x')),
        ('4_sai_p95', lambda g: g['canh'][1].update(detail__p95_A_ms=(g['canh'][1]['detail__p95_A_ms'] or 0) + 0.001)),
        ('7_cha_con_ngoai_classes', lambda g: g['canh'].append({**next(e for e in g['canh']
                                                                       if e['detail__loai'] == 'span_cha_con'),
                                                                'id': 'y', 'target': 'khong-co'})),
    ]:
        r = sua(ten, BAN, CA, f)
        muc[ten] = (r, bao(r))
    r = chay(sg_dir, BAN, CA, ['--lech-cua-so-ms', '1000'])
    muc['5_sai_cua_so'] = (r, bao(r))
    for ten, f in [
        ('11_chu_thich_mat_link', lambda g: [n.update(detail__url='') for n in g['nut']]),
        ('12_chu_thich_dv_rong', lambda g: [n.update(detail__url=n['detail__url'] + '&var-dv=') for n in g['nut']]),
    ]:
        r = sua(ten, BAN_KC, CA_KC, f)
        muc[ten] = (r, bao(r))

    sg = nap('sg', lab / 'campaigns/g1/service_graph.py')
    kd = nap('kd', KIEM)
    nt = json.loads(NT.read_text(encoding='utf-8'))

    # 6: bộ dựng với cửa sổ sai.
    d6 = tmp / '6_du_lieu' / BAN
    d6.mkdir(parents=True)
    ca = json.loads((DU / BAN / f'{CA}.json').read_text(encoding='utf-8'))
    ca['cua_so_ms'] = [x + 1000 for x in ca['cua_so_ms']]
    (d6 / f'{CA}.json').write_bytes(json.dumps(ca, ensure_ascii=False).encode('utf-8'))
    try:
        sg.build_case(tmp / '6_du_lieu', [BAN], CA, nt[CA]['goi'], nt[CA]['sha_ngoai'], tmp / '6_ra')
        muc['6_bo_dung_sai_cua_so'] = ({'ket_qua': 'không dừng'}, False)
    except sg.TraceError as e:
        co_file = (tmp / '6_ra').exists()
        muc['6_bo_dung_sai_cua_so'] = ({'dung': str(e)[:200], 'co_ghi_file': co_file}, not co_file)

    # 8, 9: span tổng hợp; bộ dựng (observe) và bộ kiểm (ky_vong) chạy trên cùng dữ liệu.
    gia = {'ca': 'gia', 'classes': {'a': 's', 'b': 's', 'booking_db': 'd'},
           'thao_tac': [{'id': 'o1', 'chu': 'a'}, {'id': 'o2', 'chu': 'x'}, {'id': 'o3', 'chu': 'b'},
                        {'id': 'o4', 'chu': 'b'}],
           'canh_thao_tac': [{'source': 'o1', 'target': 'o2', 'so_N': 1, 'so_A': 0},
                             {'source': 'o1', 'target': 'o3', 'so_N': 1, 'so_A': 0},
                             {'source': 'o3', 'target': 'o4', 'so_N': 2, 'so_A': 0}]}  # d1, d2: cha c2 cùng chủ b
    db = {'db.system': 'postgresql', 'db.name': 'booking_db'}
    # (owner, parent, phase, kind, err, dur_ns, attrs)
    spans = {('t', 'p'): ('a', '', 'N', 2, False, 5 * 10**6, {}),
             ('t', 'c1'): ('x', 'p', 'N', 2, False, 3 * 10**6, {}),          # 9: cha–con a -> x (x ngoài classes)
             ('t', 'c2'): ('b', 'p', 'N', 2, False, 2 * 10**6, {}),          # cha–con a -> b (vẽ)
             ('t', 'd1'): ('b', 'c2', 'N', 2, False, 1 * 10**6, db),         # 8: span DB kind SERVER
             ('t', 'd2'): ('b', 'c2', 'N', 3, False, 1 * 10**6, db)}         # span DB CLIENT (vẽ)
    o = sg.observe(gia, spans)
    ds = {f'{t}:{s}': {'chu': v[0], 'cha': f'{t}:{v[1]}' if v[1] else None, 'phia': v[2], 'kind': v[3],
                       'loi': v[4], 'tg': v[5], 'tt': v[6]} for (t, s), v in spans.items()}
    bang, chu_span, khong_ve, _, cc = kd.ky_vong(gia, ds)
    ve = sorted(list(o['svc']) + [k + ('db',) for k in o['db']])
    ve8 = {'canh_ve': [list(k) for k in ve], 'so_db_ve': {f'{k[0]}->{k[1]}': g.n['N'] for k, g in o['db'].items()},
           'khong_ve_bo_dung': dict(o['khong_ve']), 'khong_ve_bo_kiem': khong_ve,
           'canh_bo_kiem': [list(k) for k in sorted(bang)], 'nut_bo_dung': sorted(o['own']),
           'nut_bo_kiem': sorted(chu_span), 'cha_con_bo_kiem': {'|'.join(k): v for k, v in cc.items()}}
    dat8 = (o['db'].get(('b', 'booking_db')) is not None and o['db'][('b', 'booking_db')].n['N'] == 1
            and any('không phải span phía client' in k for k in o['khong_ve'])
            and len(bang[('b', 'booking_db', 'db')]['N']) == 1)
    dat9 = (set(o['svc']) == {('a', 'b')} and ('a', 'x', 'span_cha_con') not in bang
            and any('ngoài thực thể' in k and 'x' in k for k in o['khong_ve']) and 'x' not in o['own']
            and sum(o['khong_ve'].values()) == khong_ve and set(chu_span) == set(o['own']))
    muc['8_db_kind_server'] = (ve8, dat8)
    muc['9_cha_con_ngoai_classes'] = ({'xem': '8_db_kind_server'}, dat9)

    # 10: --tat-ca với hai ca; dữ liệu là bản sao trong thư mục tạm.
    def tat_ca(ten, sua_nguon):
        du = tmp / ten / 'du-lieu'
        (du / BAN).mkdir(parents=True)
        for c in (CA, CA2):
            shutil.copyfile(DU / BAN / f'{c}.json', du / BAN / f'{c}.json')
        (du / 'chi-muc-ban.json').write_bytes(json.dumps({'ban': [{'ban': BAN, 'cac_ca': [CA, CA2]}]}).encode())
        n = {c: dict(nt[c]) for c in (CA, CA2)}
        sua_nguon(n[CA2])
        (tmp / ten / 'nguon.json').write_bytes(json.dumps(n).encode())
        out = tmp / ten / 'ra'
        r = subprocess.run([sys.executable, '-I', '-X', 'utf8', '-B', str(lab / 'campaigns/g1/service_graph.py'), '--tat-ca',
                            '--nguon-trace', str(tmp / ten / 'nguon.json'), '--du-lieu', str(du),
                            '--ra-do-thi', str(out)], capture_output=True, text=True, encoding='utf-8', errors='replace')
        files = sorted(p.relative_to(out).as_posix() for p in out.rglob('*') if p.is_file()) if out.exists() else []
        return {'ma_thoat': r.returncode, 'stderr_cuoi': r.stderr.strip()[-200:], 'file_ghi': files}

    r = tat_ca('10a_thieu_goi', lambda x: x.update(goi=str(tmp / 'khong-co.tgz')))
    muc['10a_tat_ca_thieu_goi'] = (r, r['ma_thoat'] != 0 and not r['file_ghi'])
    r = tat_ca('10b_sai_hash', lambda x: x.update(sha_ngoai='0' * 64))
    muc['10b_tat_ca_sai_hash'] = (r, r['ma_thoat'] != 0 and not r['file_ghi'])
    r = tat_ca('10c_dung', lambda x: None)
    muc['10c_tat_ca_dung'] = (r, r['ma_thoat'] == 0 and len(r['file_ghi']) == 4)

    dat = all(v[1] for v in muc.values())
    out = {'phien_ban_bo_dung': sg.VERSION, 'do_thi': sg_dir.as_posix(), 'dat': dat,
           'muc': {k: {'dat': v[1], 'chi_tiet': v[0]} for k, v in muc.items()}}
    ra.write_bytes((json.dumps(out, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
    print('DAT' if dat else 'KHONG DAT', file=sys.stderr)
    sys.exit(0 if dat else 1)


if __name__ == '__main__':
    main()
