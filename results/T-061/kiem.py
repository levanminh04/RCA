"""T-061: tự kiểm định dạng và bộ chuyển đổi. Ghi `kiem-ket-qua.json`; thoát mã 1 nếu có phép kiểm hỏng.

Cách dùng (trong results/T-061, sau chay-tat-ca.sh): py -3 -B kiem.py
File tạm ghi trong results/T-061/tmp-kiem/ (ghi đè mỗi lần chạy). Không ghi bytecode.
Bản ghi ERROR/UNSUPPORTED sinh bằng sinh-ban-ghi-loi.py trong môi trường đã ghim của M1 (biến MOI_TRUONG_M1 dưới).
"""
import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import types
from pathlib import Path

sys.dont_write_bytecode = True

import jsonschema  # noqa: E402

GOC = Path(__file__).resolve().parent
G = GOC.parent / 'T-058' / 'dem-2026-11-10'
TMP = GOC / 'tmp-kiem'
CA = ['c12e47ab', 'f4a8c021']
KQ = []
MOI_TRUONG_M1 = {'python': 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe',
                 'PYTHONPATH': 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages'}


def nap(ten_file, ten_mo_dun):
    """Nạp một script của T-061 thành mô-đun, không ghi bytecode."""
    mod = types.ModuleType(ten_mo_dun)
    mod.__file__ = str(GOC / ten_file)
    exec(compile((GOC / ten_file).read_bytes(), str(GOC / ten_file), 'exec'), mod.__dict__)
    return mod


def chay_cd(*args):
    return subprocess.run([sys.executable, '-B', '-I', str(GOC / 'chuyen-doi.py'), *map(str, args)],
                          capture_output=True, text=True, encoding='utf-8', errors='replace')


def ghi(nhom, ten, dat, chi_tiet=None):
    KQ.append({'nhom': nhom, 'phep_kiem': ten, 'dat': bool(dat), 'chi_tiet': chi_tiet})


def doc(p):
    return json.load(open(p, encoding='utf-8'))


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    schema = doc(GOC / 'schema.json')
    jsonschema.Draft202012Validator.check_schema(schema)
    v = jsonschema.Draft202012Validator(schema)
    for c in CA:
        for ten in (f'{c}.json', f'{c}.phat-lai.json'):
            loi = [f'{"/".join(map(str, e.absolute_path))}: {e.message}' for e in v.iter_errors(doc(GOC / 'mau' / ten))]
            ghi('schema', ten, not loi, loi[:5] or None)

    for c in CA:
        m1 = doc(G / 'rca-ban-dau' / 'outputs' / c / 'method-output-1.json')
        kq = doc(GOC / 'mau' / f'{c}.json')
        nut = {n['id']: n for n in kq['nut']}
        # ---- đối chiếu theo con trỏ
        ghi(c, '/verdict → su_co.ket_luan', kq['su_co']['ket_luan'] == m1['verdict'], m1['verdict'])
        ghi(c, '/mode → su_co.che_do', kq['su_co']['che_do'] == m1['mode'], m1['mode'])
        ghi(c, '/status, /error', (kq['su_co']['trang_thai'], kq['su_co']['loi']) == (m1['status'], m1['error']))
        ghi(c, '/method_version', kq['nguon']['method_version'] == m1['method_version'], m1['method_version'])
        ghi(c, '/config_id', kq['nguon']['config_id'] == m1['config_id'], m1['config_id'])
        ghi(c, '/window/N, /window/A (ns)',
            [kq['su_co']['cua_so_nen']['tu_ns'], kq['su_co']['cua_so_nen']['den_ns']] == m1['window']['N'] and
            [kq['su_co']['cua_so_su_co']['tu_ns'], kq['su_co']['cua_so_su_co']['den_ns']] == m1['window']['A'] and
            kq['su_co']['moc']['t_ns'] == m1['window']['A'][0])
        ghi(c, 'ns → ms không làm tròn mất phần lẻ',
            all(x % 10**6 == 0 for x in m1['window']['N'] + m1['window']['A']))
        ghi(c, '/classes/* → nut[].lop_m1 (mọi thực thể)',
            all(nut[e]['lop_m1'] == cl for e, cl in m1['classes'].items()) and
            {e for e, n in nut.items() if n['lop_m1']} == set(m1['classes']), len(m1['classes']))
        ghi(c, '/sets/observed_entities ⊆ nut', set(m1['sets']['observed_entities']) <= set(nut),
            m1['sets']['observed'])
        er = {r['entity']: r for r in m1['entity_ranking']}
        ghi(c, '/entity_ranking[].tie_group → nut[].nhom_dong_hang, hang = tie_group+1',
            all(nut[e]['nhom_dong_hang'] == r['tie_group'] and nut[e]['hang'] == r['tie_group'] + 1 for e, r in er.items()),
            len(er))
        ghi(c, '/entity_ranking[].key → nut[].khoa_m1', all(nut[e]['khoa_m1'] == r['key'] for e, r in er.items()))
        ghi(c, 'thực thể không có trong /entity_ranking → hang null',
            all(n['hang'] is None for e, n in nut.items() if e not in er),
            sorted(e for e in nut if e not in er))
        ghi(c, '/blocks → xep_hang (thứ tự, thành viên, khóa)',
            [(x['thuc_the'], x['khoa_m1']) for x in kq['xep_hang']] ==
            [([e for g in b['groups'] for e in g], b['key']) for b in m1['blocks']])
        ghi(c, 'số đồng hạng = cỡ khối',
            all(n['so_dong_hang'] == sum(1 for r in er.values() if r['tie_group'] == n['nhom_dong_hang'])
                for n in nut.values() if n['hang']))
        canh_m1 = [tuple(x) for x in m1['extra']['canh']]
        canh_kq = [(x['nguon'], x['dich']) for x in kq['canh']]
        ghi(c, '/extra/canh[i] → canh[i] (cả hai đầu, giữ chiều)', canh_kq == canh_m1, len(canh_m1))
        ghi(c, 'không có cạnh ngoài /extra/canh', set(canh_kq) == set(canh_m1))
        ghi(c, '/diagnostics/so_canh_tinh → nguon_goc cạnh',
            all(x['nguon_goc'] == ('quan_sat' if m1['diagnostics']['so_canh_tinh'] == 0 else 'quan_sat_hoac_tinh')
                for x in kq['canh']))
        ghi(c, '/evidence_refs = tập don_vi của bang_chung',
            sorted({b['don_vi'] for b in kq['bang_chung']}) == m1['evidence_refs'], m1['evidence_refs'])
        ghi(c, '/extra/kenh_co[] → bang_chung[] (mã, thực thể, kênh, hướng, lớp, s, F_I, khởi phát)',
            [(b['id'], b['thuc_the'], b['kenh'], b['huong'], b['lop'], b['s'], b['F_I'], b['khoi_phat_ns'])
             for b in kq['bang_chung']] ==
            [(k['ma'], k['thuc_the'], k['ten'], k['huong'], k['lop'], k['s'], k['F_I'], k['khoi_phat'])
             for k in m1['extra']['kenh_co']], len(m1['extra']['kenh_co']))
        ghi(c, 'liên kết bằng chứng nút ↔ bang_chung.thuc_the',
            all(sorted(b['id'] for b in kq['bang_chung'] if b['thuc_the'] == e) == n['bang_chung'] for e, n in nut.items()))
        ghi(c, 'bằng chứng không có liên kết thì có lý do',
            all(b['lien_ket'] or b['ly_do_khong_lien_ket'] for b in kq['bang_chung']))
        ghi(c, 'không có trace ID / dòng log trong liên kết',
            all(lk['loai'] in ('metric', 'trace_tim_kiem') for b in kq['bang_chung'] for lk in b['lien_ket']))
        reg = m1['region']
        ap = m1['verdict'] == 'CAUSE_FOUND'
        ghi(c, '/region/T → vung.T_m1 (nguyên văn)', kq['vung']['T_m1'] == reg['T'], reg['T'])
        ghi(c, '/region/hop_cach_1, hop_cach_2, cach_1, cach_2 → vung (khi CAUSE_FOUND); rỗng kèm lý do khi không',
            (kq['vung']['hop_cach_1'] == reg['hop_cach_1'] and kq['vung']['hop_cach_2'] == reg['hop_cach_2'] and
             kq['vung']['cach_1'] == reg['cach_1'] and kq['vung']['cach_2'] == reg['cach_2'] and kq['vung']['goc'] == reg['T'])
            if ap else (not kq['vung']['goc'] and not kq['vung']['hop_cach_1'] and kq['vung']['ly_do']
                        and not reg['hop_cach_1'] and not reg['hop_cach_2']))
        ghi(c, '/inherited_by[] → giai_thich_ke_thua[]',
            [(x['thuc_the'], x['kenh_ma'], x['duong'], x['giai_thich_boi'], x['quy_tac'], x['trang_thai'])
             for x in kq['giai_thich_ke_thua']] ==
            [(x['thuc_the'], x['ma'], x['duong'], x['giai_thich_ma'], x['quy_tac'], x['trang_thai'])
             for x in m1['inherited_by']], len(m1['inherited_by']))
        ghi(c, '/sets/observed, /sets/returned, /do_phu_cham, /diagnostics/NO_VALID_CHANNEL',
            (kq['do_phu']['so_quan_sat'], kq['do_phu']['so_tra_hang'], kq['do_phu']['do_phu_cham'],
             kq['do_phu']['thieu_kenh_hop_le']) ==
            (m1['sets']['observed'], m1['sets']['returned'], m1['do_phu_cham'], m1['diagnostics']['NO_VALID_CHANNEL']))
        ghi(c, '/RANK_CHANGED, /OBS_DEPENDENT → do_phu',
            (kq['do_phu']['hang_doi_giua_the_gioi'], kq['do_phu']['don_vi_phu_thuoc_quan_sat']) ==
            (m1['RANK_CHANGED'], m1['OBS_DEPENDENT']), [m1['RANK_CHANGED'], m1['OBS_DEPENDENT']])
        h = hashlib.sha256((G / 'rca-ban-dau' / 'outputs' / c / 'method-output-1.json').read_bytes()).hexdigest()
        man = doc(G / 'artifacts-sha256.json')['files'][f'rca-ban-dau/outputs/{c}/method-output-1.json']['sha256']
        ghi(c, 'nguon.sha256_m1 = hash file = manifest T-058', kq['nguon']['sha256_m1'] == h == man, h[:16])
        # ---- quy tắc hiển thị
        ghi(c, 'nút nổi bật ⇔ nhóm 0 và lớp tu_sinh',
            all(n['noi_bat'] == (n['nhom_dong_hang'] == 0 and n['lop_m1'] == 'tu_sinh') for n in nut.values()))
        ghi(c, 'màu chỉ phụ thuộc vai_tro',
            len({(n['vai_tro'], n['hien_thi']['mau']) for n in nut.values()}) == len({n['vai_tro'] for n in nut.values()}))
        ghi(c, 'mốc chế độ a ghi nguồn bộ điều phối',
            kq['su_co']['moc']['nguon'] == 'bo_dieu_phoi' and 'bộ điều phối cấp' in kq['su_co']['moc']['mo_ta'])

    # ---- bốn điều phải giữ (SPEC)
    a = doc(GOC / 'mau' / 'c12e47ab.json')
    na = {n['id']: n for n in a['nut']}
    ghi('phai-giu', 'c12e47ab: NO_INTRINSIC_ANOMALY', a['su_co']['ket_luan'] == 'NO_INTRINSIC_ANOMALY')
    ghi('phai-giu', 'c12e47ab: 17 thực thể cùng một nhóm đồng hạng',
        len(na) == 17 and {n['nhom_dong_hang'] for n in na.values()} == {0} and all(n['so_dong_hang'] == 17 for n in na.values()))
    ghi('phai-giu', 'c12e47ab: không có bằng chứng', a['bang_chung'] == [] and all(not n['bang_chung'] for n in na.values()))
    ghi('phai-giu', 'c12e47ab: không nút nào nổi bật/nghi nguồn/gốc vùng dù đứng đầu',
        not any(n['noi_bat'] or n['vai_tro'] == 'nghi_nguon' or n['goc_vung'] for n in na.values())
        and a['vung']['ap_dung'] is False and len(a['vung']['T_m1']) == 17)
    b = doc(GOC / 'mau' / 'f4a8c021.json')
    nb = {n['id']: n for n in b['nut']}
    ghi('phai-giu', 'f4a8c021: CAUSE_FOUND, 16 thực thể có hạng',
        b['su_co']['ket_luan'] == 'CAUSE_FOUND' and sum(1 for n in nb.values() if n['hang']) == 16)
    ghi('phai-giu', 'f4a8c021: event-service thiếu dữ liệu, không hạng, không màu nghi nguồn',
        nb['event-service']['vai_tro'] == 'thieu_du_lieu' and nb['event-service']['hang'] is None
        and nb['event-service']['hien_thi']['mau'] == '#CA95E5' and nb['event-service']['hien_thi']['nhan_trong'] == '?')
    ghi('phai-giu', 'f4a8c021: dự đoán M1 giữ nguyên (api-gateway #1 nổi bật; ticket-service #2; config-discovery #3 kéo theo)',
        (nb['api-gateway']['hang'], nb['api-gateway']['noi_bat'], nb['ticket-service']['hang'], nb['ticket-service']['vai_tro'],
         nb['config-discovery']['hang'], nb['config-discovery']['vai_tro']) == (1, True, 2, 'nghi_nguon', 3, 'bi_keo_theo'))
    ghi('phai-giu', 'cả hai ca: mốc tham chiếu do bộ điều phối cấp',
        all(x['su_co']['moc']['nguon'] == 'bo_dieu_phoi' for x in (a, b)))
    ghi('phai-giu', 'liên kết chỉ sinh khi có truy vấn/định danh nguồn',
        all((lk['loai'] == 'metric' and bc['don_vi'].startswith('metric|')) or
            (lk['loai'] == 'trace_tim_kiem' and bc['don_vi'].startswith('op|'))
            for x in (a, b) for bc in x['bang_chung'] for lk in bc['lien_ket']))

    # ---- phát lại: thêm/bỏ đáp án không đổi dự đoán, hạng, vùng, màu
    kh = nap('khung-grafana.py', 'khung')
    for c in CA:
        goc = doc(GOC / 'mau' / f'{c}.json')
        pl = doc(GOC / 'mau' / f'{c}.phat-lai.json')
        bo = copy.deepcopy(pl)
        bo.pop('phat_lai')
        ghi('phat-lai', f'{c}: bỏ khối phat_lai → trùng bản gốc (mọi trường)', bo == goc)
        ghi('phat-lai', f'{c}: phat_lai trỏ đúng hash bản gốc đã băm',
            pl['phat_lai']['sha256_ket_qua_truoc_ghep'] ==
            doc(GOC / 'mau' / 'manifest-mau.json')['files'][f'{c}.json']['sha256'])
        f_goc, f_pl = kh.dung(goc), kh.dung(pl)
        tr = copy.deepcopy(f_pl)
        idx = [i for i, f in enumerate(tr[0]['schema']['fields']) if f['name'] == 'detail__dap_an']
        for i in reversed(idx):
            tr[0]['schema']['fields'].pop(i)
            tr[0]['data']['values'].pop(i)
        ghi('phat-lai', f'{c}: khung Grafana phát lại chỉ thêm trường detail__dap_an', len(idx) == 1 and tr == f_goc)
        # đổi đáp án giả sang thành phần khác: dự đoán vẫn không đổi
        gia = copy.deepcopy(pl)
        gia['phat_lai']['thanh_phan_tiem'] = 'api-gateway'
        f_gia = kh.dung(gia)
        ten = [f['name'] for f in f_gia[0]['schema']['fields']]
        giu = ['id', 'mainstat', 'secondarystat', 'color', 'highlighted', 'detail__hang', 'detail__vung']
        ghi('phat-lai', f'{c}: đổi đáp án sang thành phần khác không đổi màu/hạng/vùng/nổi bật',
            all(f_gia[0]['data']['values'][ten.index(t)] == f_goc[0]['data']['values'][ten.index(t)] for t in giu))

    # ---- cách ly nhãn và tất định của bộ chuyển đổi
    import ast
    cay = ast.parse((GOC / 'chuyen-doi.py').read_text(encoding='utf-8'))
    doc_str = ast.get_docstring(cay, clean=False)
    nhap = [n.names[0].name if isinstance(n, ast.Import) else n.module for n in ast.walk(cay)
            if isinstance(n, (ast.Import, ast.ImportFrom))]
    cam = {id(x) for n in cay.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'CAM_DOC'
           for x in ast.walk(n)}  # danh sách cấm đọc là chốt chặn, không phải tham chiếu
    chuoi = [n.value for n in ast.walk(cay) if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in cam
             and n.value != doc_str and any(x in n.value.lower() for x in ('phat-lai', 'phat_lai', 'dap_an', 'dap-an'))]
    ghi('cach-ly', 'chuyen-doi.py không import và không trỏ tới phat-lai/đáp án (AST, ngoài docstring)',
        not [m for m in nhap if m and 'phat' in m] and not chuoi, {'import': nhap, 'chuoi_vi_pham': chuoi})
    for c in CA:
        s = (GOC / 'mau' / f'{c}.json').read_text(encoding='utf-8')
        cam = [x for x in ('process_pause', 'operator_only_role', 'ledger', 'intervention', 'docker pause', 'f4a8c021.phat')
               if x in s]
        ghi('cach-ly', f'{c}: đầu ra không chứa chuỗi của sổ/kế hoạch', not cam, cam or None)
    if TMP.exists():
        shutil.rmtree(TMP)
    TMP.mkdir()
    chung = ['--manifest', G / 'artifacts-sha256.json', '--goc-manifest', G, '--adapter', G / 'src/m1/adapter_flashticket.py']
    rq = {c: G / 'rca-ban-dau/cases' / c / 'request.json' for c in CA}
    r = chay_cd('--vao', G / 'ledger-received.jsonl', '--request', rq['c12e47ab'], *chung, '--ma-ca', 'x',
                '--ra', TMP / 'khong-ghi.json')
    ghi('cach-ly', 'chuyen-doi.py từ chối đọc sổ tiêm lỗi', r.returncode != 0 and not (TMP / 'khong-ghi.json').exists(),
        (r.stdout + r.stderr).strip()[-120:])
    for c in CA:
        ra = TMP / f'{c}.json'
        r = chay_cd('--vao', G / 'rca-ban-dau/outputs' / c / 'method-output-2.json', '--request', rq[c], *chung,
                    '--ma-ca', c, '--ra', ra)
        x = doc(ra) if ra.exists() else {'nguon': {}}
        y = doc(GOC / 'mau' / f'{c}.json')
        x['nguon'].pop('file_m1', None); y['nguon'].pop('file_m1')
        ghi('tat-dinh', f'{c}: chạy trên method-output-2 (lần M1 thứ hai) cho cùng kết quả', x == y,
            (r.stdout + r.stderr).strip()[-120:] if r.returncode else None)

    # ---- ràng buộc mã ca (gói C2/C4)
    r = chay_cd('--vao', G / 'rca-ban-dau/outputs/c12e47ab/method-output-1.json', '--request', rq['c12e47ab'], *chung,
                '--ma-ca', 'f4a8c021', '--ra', TMP / 'sai-ma.json')
    ghi('rang-buoc-ca', 'mã ca khác thư mục file M1 → từ chối', r.returncode != 0 and not (TMP / 'sai-ma.json').exists(),
        (r.stdout + r.stderr).strip()[-100:])
    r = chay_cd('--vao', G / 'rca-ban-dau/outputs/c12e47ab/method-output-1.json', '--request', rq['f4a8c021'], *chung,
                '--ma-ca', 'c12e47ab', '--ra', TMP / 'sai-request.json')
    ghi('rang-buoc-ca', 'request.json của ca khác → từ chối', r.returncode != 0 and not (TMP / 'sai-request.json').exists(),
        (r.stdout + r.stderr).strip()[-100:])

    # ---- bản ghi NO_EVIDENCE / ERROR / UNSUPPORTED (gói C1), chuyển trong bộ nhớ
    cd = nap('chuyen-doi.py', 'chuyen_doi')
    ad_b = (G / 'src/m1/adapter_flashticket.py').read_bytes()
    ax = cd.AnhXa(cd.nap_adapter(ad_b, 'adapter_flashticket.py'))
    t_a = doc(rq['c12e47ab'])['t']
    nguon_thu = dict(doc(GOC / 'mau' / 'c12e47ab.json')['nguon'])
    for k in ('method', 'method_version', 'config_id', 'variant', 'why_ids', 'che_do_m1'):
        nguon_thu.pop(k, None)
    v = jsonschema.Draft202012Validator(doc(GOC / 'schema.json'))
    m1a = doc(G / 'rca-ban-dau/outputs/c12e47ab/method-output-1.json')
    try:
        cd.chuyen(m1a, 'c12e47ab', nguon_thu, ax, t_a + 1)
        lech = False
    except SystemExit:
        lech = True
    ghi('ban-ghi-loi', 'mốc request.json lệch /window/A/0 → từ chối', lech)
    m1b = copy.deepcopy(m1a)
    m1b['mode'] = 'b'
    try:
        cd.chuyen(m1b, 'c12e47ab', nguon_thu, ax, t_a)
        tu_choi_b = False
    except SystemExit:
        tu_choi_b = True
    ghi('ban-ghi-loi', 'chế độ khác a → từ chối (0.2 chỉ hỗ trợ chế độ a)', tu_choi_b)
    # NO_EVIDENCE: dựng tay theo hình dạng src/m1/chuoi.py:647–700 khi không có khối nào (mọi thực thể không có kênh OK)
    ne = copy.deepcopy(m1a)
    O = ne['sets']['observed_entities']
    ne.update({'status': 'NO_EVIDENCE', 'blocks': [], 'entity_ranking': [], 'verdict': 'INSUFFICIENT_EVIDENCE',
               'classes': {e: 'thieu_du_lieu' for e in O}, 'evidence_refs': [], 'inherited_by': [], 'do_phu_cham': 0.0,
               'region': {'T': [], 'cach_1': {}, 'cach_2': {}, 'hop_cach_1': [], 'hop_cach_2': []}})
    ne['sets']['returned'] = 0
    ne['diagnostics']['NO_VALID_CHANNEL'] = sorted(O)
    ne['extra'].update({'kenh_co': [], 'tang_P': {}, 'blocks_P': []})
    kq_ne = cd.chuyen(ne, 'c12e47ab', nguon_thu, ax, t_a)
    loi_ne = [e.message for e in v.iter_errors(kq_ne)]
    ghi('ban-ghi-loi', 'NO_EVIDENCE (dựng trong bộ nhớ): đạt schema, giữ cửa sổ và verdict, mọi nút thiếu dữ liệu, không hạng',
        not loi_ne and kq_ne['su_co']['trang_thai'] == 'NO_EVIDENCE' and kq_ne['su_co']['cua_so_su_co'] is not None
        and kq_ne['su_co']['ket_luan'] == 'INSUFFICIENT_EVIDENCE' and kq_ne['xep_hang'] == []
        and all(n['vai_tro'] == 'thieu_du_lieu' and n['hang'] is None for n in kq_ne['nut']), loi_ne[:3] or None)
    env = dict(os.environ, PYTHONPATH=MOI_TRUONG_M1['PYTHONPATH'])
    r = subprocess.run([MOI_TRUONG_M1['python'], '-B', str(GOC / 'sinh-ban-ghi-loi.py'), str(TMP)],
                       capture_output=True, text=True, encoding='utf-8', errors='replace', env=env)
    ghi('ban-ghi-loi', 'sinh bản ghi ERROR/UNSUPPORTED bằng src/m1/chuoi.py::_ban_ghi_loi', r.returncode == 0,
        (r.stdout + r.stderr).strip()[-200:])
    for st in ('ERROR', 'UNSUPPORTED'):
        p = TMP / f'ban-ghi-{st}.json'
        if not p.exists():
            ghi('ban-ghi-loi', f'{st}: chuyển đổi', False, 'không có bản ghi')
            continue
        rec = doc(p)
        kq = cd.chuyen(rec, 'c12e47ab', nguon_thu, ax, t_a)
        loi = [e.message for e in v.iter_errors(kq)]
        ghi('ban-ghi-loi', f'{st}: đạt schema; trạng thái, thông báo lỗi giữ nguyên; mốc từ request.json; '
            'cửa sổ/verdict rỗng; không nút/cạnh/hạng',
            not loi and kq['su_co']['trang_thai'] == st and kq['su_co']['loi'] == rec['error']
            and kq['su_co']['moc']['t_ns'] == t_a * 10**9 and kq['su_co']['cua_so_su_co'] is None
            and kq['su_co']['ket_luan'] is None and not kq['nut'] and not kq['canh'] and not kq['xep_hang'],
            loi[:3] or None)
        khung_loi = kh.dung(kq)
        chu = kh.panel_chu(1, kq, 0, 0)['options']['content']
        ghi('ban-ghi-loi', f'{st}: khung Grafana dựng được (0 nút) và panel ghi trạng thái, lỗi, verdict "—"',
            khung_loi[0]['data']['values'][0] == [] and st in chu and rec['error'] in chu and '`—`' in chu)

    # ---- phát lại: kiểm đủ đợt trước khi mở nguồn đáp án (gói C2)
    pl = nap('phat-lai.py', 'phat_lai')
    ids = doc(G / 'm1-launch-record.json')['ids']
    mm = GOC / 'mau' / 'manifest-mau.json'
    ghi('dot', 'đợt /ids = tập mẫu trong manifest mẫu, byte và mã ca khớp',
        sorted(pl.kiem_dot(ids, GOC / 'mau', mm)) == sorted(ids), ids)

    def phai_loi(ten, *a):
        try:
            pl.kiem_dot(*a)
            ghi('dot', ten, False)
        except pl.LoiDot as ex:
            ghi('dot', ten, True, str(ex)[:120])
    phai_loi('mã trùng trong danh sách → dừng', ids + ids[:1], GOC / 'mau', mm)
    phai_loi('danh sách thiếu một ca so với manifest mẫu → dừng', ids[:1], GOC / 'mau', mm)
    thieu = TMP / 'mau-thieu'
    thieu.mkdir()
    shutil.copy(GOC / 'mau' / f'{ids[0]}.json', thieu)
    phai_loi('thư mục mẫu thiếu một ca → dừng', ids, thieu, mm)
    sua = TMP / 'mau-sua'
    sua.mkdir()
    for i in ids:
        shutil.copy(GOC / 'mau' / f'{i}.json', sua)
    (sua / f'{ids[0]}.json').write_bytes((sua / f'{ids[0]}.json').read_bytes() + b' ')
    phai_loi('mẫu đổi byte sau khi băm → dừng', ids, sua, mm)
    lech_ma = TMP / 'mau-lech-ma'
    lech_ma.mkdir()
    mm_lech = {'files': {}}
    for i in ids:
        x = doc(GOC / 'mau' / f'{i}.json')
        if i == ids[0]:
            x['su_co']['ma'] = ids[1]
        b = (json.dumps(x, ensure_ascii=False, indent=1) + '\n').encode('utf-8')
        (lech_ma / f'{i}.json').write_bytes(b)
        mm_lech['files'][f'{i}.json'] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    (TMP / 'manifest-lech-ma.json').write_text(json.dumps(mm_lech), encoding='utf-8')
    phai_loi('mã ca trong mẫu khác thư mục nguồn → dừng', ids, lech_ma, TMP / 'manifest-lech-ma.json')
    r = subprocess.run([sys.executable, '-B', '-I', str(GOC / 'phat-lai.py'), '--dot', G / 'm1-launch-record.json',
                        '--thu-muc-mau', thieu, '--manifest-mau', mm, '--ke-hoach', TMP / 'khong-ton-tai.json',
                        '--so', TMP / 'khong-ton-tai.jsonl', '--manifest', G / 'artifacts-sha256.json',
                        '--goc-manifest', G], capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = r.stdout + r.stderr
    ghi('dot', 'CLI: đợt thiếu ca dừng ở bước kiểm đợt, trước khi mở nguồn đáp án (đường dẫn đáp án giả không bị đụng tới)',
        r.returncode != 0 and 'Dừng trước khi mở nguồn đáp án' in out, out.strip()[-140:])
    # ---- file chỉ mục danh sách sự cố
    cm = doc(GOC / 'mau' / 'chi-muc' / 'danh-sach-su-co.json')['su_co']
    mm_files = doc(mm)['files']
    ghi('chi-muc', 'chỉ mục: đủ mọi mẫu trong manifest mẫu, mỗi dòng trỏ đúng hash mẫu, mới nhất trước',
        sorted(x['file'] for x in cm) == sorted(mm_files)
        and all(mm_files[x['file']]['sha256'] == x['sha256_file'] for x in cm)
        and [x['t_ms'] for x in cm] == sorted((x['t_ms'] for x in cm), reverse=True))
    ok_dong = True
    for x in cm:
        m = doc(GOC / 'mau' / x['file'])
        noi_bat = ', '.join(n['id'] for n in m['nut'] if n['noi_bat']) or '—'
        ok_dong &= (x['ma'], x['trang_thai'], x['ket_luan'], x['nghi_nguon_hang_1']) == (
            m['su_co']['ma'], m['su_co']['trang_thai'], m['su_co']['ket_luan'], noi_bat)
    ghi('chi-muc', 'chỉ mục: mã, trạng thái, kết luận, nút nghi nguồn hạng 1 khớp từng mẫu', ok_dong)
    s_cm = (GOC / 'mau' / 'chi-muc' / 'danh-sach-su-co.json').read_text(encoding='utf-8')
    ghi('chi-muc', 'chỉ mục không chứa thông tin phát lại/đáp án',
        not any(t in s_cm for t in ('phat_lai', 'thanh_phan_tiem', 'process_pause', 'operator_only_role')))
    ghi('bytecode', 'không có __pycache__ mới trong results/T-061 và results/T-058/.../src/m1',
        not (GOC / '__pycache__').exists() and not (G / 'src/m1/__pycache__').exists())

    hong = [k for k in KQ if not k['dat']]
    (GOC / 'kiem-ket-qua.json').write_text(json.dumps({'so_phep_kiem': len(KQ), 'so_hong': len(hong), 'ket_qua': KQ},
                                                      ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for k in KQ:
        print(('ĐẠT ' if k['dat'] else 'HỎNG') + f" [{k['nhom']}] {k['phep_kiem']}")
    print(f'{len(KQ) - len(hong)}/{len(KQ)} đạt')
    return 1 if hong else 0


if __name__ == '__main__':
    sys.exit(main())
