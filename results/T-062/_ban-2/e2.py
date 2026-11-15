#!/usr/bin/env python3
"""T-062 E2: đầu ra M1 → định dạng 0.2 (bộ chuyển đổi T-061, không sửa) → băm cả đợt → chỉ mục → phát lại có đáp án.

Thứ tự bắt buộc (SPEC T-062 luật 5): bước 1–3 KHÔNG đọc sổ tiêm lỗi; chỉ khi cả đợt đã băm (bước 3) mới mở sổ
`tiem-loi/so.jsonl` ở bước 4 để ghép đáp án vào bản phát lại (thư mục riêng `ket-qua/phat-lai/`).

Dùng (từ D:/RCA-flashticket): py -3 -B results/T-062/e2.py [--phat-lai]
  1. Kiểm gói ca `ca/<mã>/<mã>.tgz` (sha256 ghi trong chay/nhat-ky.jsonl lúc nhận), adapter theo m1-source-pins.
  2. manifest-ca.json (method-output-1, request, adapter) → chuyen-doi.py T-061 → ket-qua/<mã>.json
  3. ket-qua/manifest-ket-qua.json + ket-qua/chi-muc/danh-sach-su-co.json (cùng trường với T-061 chi-muc.py)
  4. (--phat-lai) đọc sổ, ghép đáp án + tập chấp nhận T-059 → ket-qua/phat-lai/<mã>.phat-lai.json, bang-cham.json
"""
import hashlib, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding='utf-8')
R = Path('D:/RCA-flashticket'); O = R / 'results/T-062'; CA = O / 'ca'; KQ = O / 'ket-qua'
T061 = R / 'results/T-061'
ADAPTER = CA / '_nguon' / 'adapter_flashticket.py'

# Đáp án theo T-059 (danh-muc-loi.md): root khai trước và tập chấp nhận chung.
DAP_AN = {
    'EVENT-DB-LAT': ('event-service → event_db (data)', ['event-service', 'event_db'], 'D9-01'),
    'REDIS-BOOK': ('booking-service → cache (data)', ['booking-service', 'cache'], 'D9-03'),
    'HTTP5-EVENT': ('event-service', ['event-service'], 'D9-05'),
    'SLOW-BOOK': ('booking-service', ['booking-service'], 'D9-06'),
    'NET-GW-BOOK': ('api-gateway → booking-service (http)', ['api-gateway', 'booking-service'], 'D9-07'),
    'CPU-BOOK': ('booking-service', ['booking-service'], 'D9-08'),
    'FLASH-HEALTHY': ('root = null (tải tăng khỏe)', [], 'D9-11'),
    'BINH-THUONG': ('root = null (ca bình thường)', [], '—'),
}

def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def received():
    """Mã ca + sha256 gói đã nhận, đọc từ nhật ký bộ chạy (không chứa nhãn ô ở dòng 'M1 xong')."""
    out = {}
    for l in (O / 'chay' / 'nhat-ky.jsonl').read_text(encoding='utf-8').splitlines():
        d = json.loads(l.lstrip('\ufeff'))
        if d.get('msg') == 'M1 xong': out[d['id']] = d['tgz_sha256']
    return out

def buoc_1_2():
    ids = received()
    if not ids: raise SystemExit('Chưa có ca nào có M1')
    # adapter không nằm trong m1-source-pins; hash khóa ghi ở T-058 m1-execution-plan-v2.json#/files_sha256
    plan = json.loads((R / 'results/T-058/dem-2026-11-10/m1-execution-plan-v2.json').read_text(encoding='utf-8'))
    if sha(ADAPTER) != plan['files_sha256']['src/m1/adapter_flashticket.py']: raise SystemExit('adapter lệch bản khóa T-058')
    if sha(CA / '_nguon' / 'm1-p7-config.json') != plan['files_sha256']['m1-p7-config.json']: raise SystemExit('config M1 lệch P7')
    files = {'_nguon/adapter_flashticket.py': {'sha256': sha(ADAPTER), 'bytes': ADAPTER.stat().st_size}}
    for i, h in sorted(ids.items()):
        if sha(CA / i / f'{i}.tgz') != h: raise SystemExit(f'gói {i} lệch hash lúc nhận')
        for rel in (f'{i}/outputs/{i}/method-output-1.json', f'{i}/cases/{i}/request.json', f'{i}/outputs/{i}/summary.json'):
            p = CA / rel; files[rel] = {'sha256': sha(p), 'bytes': p.stat().st_size}
    (CA / 'manifest-ca.json').write_text(json.dumps({'files': files}, indent=1) + '\n', encoding='utf-8')
    KQ.mkdir(exist_ok=True)
    for i in sorted(ids):
        ra = KQ / f'{i}.json'
        if ra.exists(): continue          # tất định; không chuyển lại ca đã có
        r = subprocess.run([sys.executable, '-B', '-I', str(T061 / 'chuyen-doi.py'),
                            '--vao', str(CA / i / 'outputs' / i / 'method-output-1.json'),
                            '--request', str(CA / i / 'cases' / i / 'request.json'),
                            '--manifest', str(CA / 'manifest-ca.json'), '--goc-manifest', str(CA),
                            '--adapter', str(ADAPTER), '--ma-ca', i, '--ra', str(ra)],
                           capture_output=True, text=True, encoding='utf-8', errors='replace')
        print(i, 'chuyển đổi rc', r.returncode, (r.stdout + r.stderr).strip()[-300:])
        if r.returncode: raise SystemExit(f'chuyển đổi {i} lỗi')
    return sorted(ids)

def buoc_3(ids):
    files = {f'{i}.json': {'sha256': sha(KQ / f'{i}.json'), 'bytes': (KQ / f'{i}.json').stat().st_size} for i in ids}
    (KQ / 'manifest-ket-qua.json').write_text(json.dumps({'ids': ids, 'files': files}, indent=1) + '\n', encoding='utf-8')
    dong = []
    for i in ids:
        kq = json.loads((KQ / f'{i}.json').read_text(encoding='utf-8')); sc = kq['su_co']
        dong.append({'ma': sc['ma'], 't_ms': sc['moc']['t_ns'] // 10**6, 't_utc': sc['moc']['t_utc'],
                     'trang_thai': sc['trang_thai'], 'ket_luan': sc['ket_luan'], 'ket_luan_hien_thi': sc['ket_luan_hien_thi'],
                     'nghi_nguon_hang_1': ', '.join(n['id'] for n in kq['nut'] if n['noi_bat']) or '—',
                     'so_thuc_the_quan_sat': kq['do_phu']['so_quan_sat'], 'so_thuc_the_co_hang': kq['do_phu']['so_tra_hang'],
                     'file': f'{i}.json', 'sha256_file': files[f'{i}.json']['sha256']})
    dong.sort(key=lambda x: x['t_ms'], reverse=True)
    (KQ / 'chi-muc').mkdir(exist_ok=True)
    (KQ / 'chi-muc' / 'danh-sach-su-co.json').write_text(json.dumps(
        {'dinh_dang': 'flashticket-rca-danh-sach', 'phien_ban': '0.2', 'su_co': dong}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('chỉ mục:', len(dong), 'sự cố')

def buoc_4(ids):
    # Kiểm đủ đợt và byte từng file trước khi mở sổ
    mk = json.loads((KQ / 'manifest-ket-qua.json').read_text(encoding='utf-8'))
    if sorted(mk['ids']) != sorted(ids): raise SystemExit('đợt lệch manifest kết quả')
    for i in ids:
        if sha(KQ / f'{i}.json') != mk['files'][f'{i}.json']['sha256']: raise SystemExit(f'{i}.json đổi sau khi băm')
    h_mk = sha(KQ / 'manifest-ket-qua.json')
    # ---- chỉ từ đây mới đọc sổ tiêm lỗi ----
    so_b = (O / 'tiem-loi' / 'so.jsonl').read_bytes(); so = [json.loads(x) for x in so_b.decode('utf-8').splitlines()]
    prev = '0' * 64
    for line in so_b.decode('utf-8').splitlines():          # kiểm chuỗi hash nối dòng
        if json.loads(line)['prev_sha256'] != prev: raise SystemExit('sổ tiêm lỗi gãy chuỗi hash')
        prev = hashlib.sha256(line.encode()).hexdigest()
    (KQ / 'phat-lai').mkdir(exist_ok=True)
    bang = []
    for i in ids:
        kq = json.loads((KQ / f'{i}.json').read_text(encoding='utf-8'))
        beg = [e for e in so if e.get('event') == 'cycle-begin' and e.get('opaque_id') == i]
        if len(beg) != 1: raise SystemExit(f'không có đúng một chu kỳ cho {i}')
        cell = beg[0]['cell']
        fs = [e for e in so if e.get('event') in ('fault-start', 'normal-mark', 'flash-ramp-start') and e.get('opaque_id') == i]
        root, accept, ho = DAP_AN[cell]
        nut = {n['id']: n for n in kq['nut']}
        hang = {a: (nut[a]['hang'] if a in nut else None) for a in accept}
        co_hang = [h for h in hang.values() if h]
        best = min(co_hang) if co_hang else None
        top1 = [n['id'] for n in kq['nut'] if n.get('hang') == 1]
        if accept:
            nx = (f'Đáp án: {root} (ô {cell}, họ {ho}). Hạng tốt nhất trong tập chấp nhận {accept}: '
                  + (f'#{best}' if best else 'không có hạng') + f'. Hạng 1 của M1: {", ".join(top1) or "—"}.')
        else:
            nx = f'Đáp án: {root} (ô {cell}). Kết luận M1: {kq["su_co"]["ket_luan"]}; hạng 1: {", ".join(top1) or "—"}.'
        out = dict(kq)
        out['phat_lai'] = {
            'canh_bao': 'Bản phát lại: đáp án ghép SAU khi kết quả cả đợt đã băm; không dùng để chẩn đoán trực tuyến.',
            'nguon_dap_an': ['results/T-062/tiem-loi/so.jsonl'], 'sha256_dap_an': {'so.jsonl': hashlib.sha256(so_b).hexdigest()},
            'sha256_manifest_ket_qua': h_mk, 'sha256_ket_qua_truoc_ghep': mk['files'][f'{i}.json']['sha256'],
            # trường T-061 (bản 2, 12/11, sửa N2 REVIEW.md, Minh duyệt): chỉ điền khi root là MỘT nút; root là cạnh (có '→')
            # thì null — đáp án đầy đủ ở root_khai_truoc + tap_chap_nhan (bản 1 lấy phần tử đầu tập, gọi sai một đầu cạnh là đáp án).
            'thanh_phan_tiem': (accept[0] if len(accept) == 1 and '→' not in root else None), 'ho_loi': f'{ho} — {root}',
            'o_loi': cell, 'root_khai_truoc': root, 'tap_chap_nhan': accept,
            'hang_trong_tap': hang, 'hang_tot_nhat': best,
            'moc_xac_nhan_utc': fs[0].get('inj', {}).get('t') if fs else None, 'nhan_xet': nx}
        (KQ / 'phat-lai' / f'{i}.phat-lai.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        bang.append({'ma': i, 'o': cell, 'root': root, 'tap_chap_nhan': accept, 'hang_tot_nhat': best, 'hang_1_m1': top1,
                     'ket_luan_m1': kq['su_co']['ket_luan'], 'trang_thai_m1': kq['su_co']['trang_thai']})
    (KQ / 'phat-lai' / 'bang-cham.json').write_text(json.dumps({'sha256_manifest_ket_qua': h_mk, 'ca': bang},
                                                               ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for b in bang: print(b)

def day(ids, phat_lai):
    """Đẩy lên exp-obs:/opt/flash-ticket-obs/rca-ket-qua/ (dashboard G2 đọc qua public/rca; xem giao-dien/dinh-dang-chi-muc.md)."""
    SCP = 'C:/Program Files/Git/usr/bin/scp.exe'; SSH = 'C:/Program Files/Git/usr/bin/ssh.exe'
    key = 'D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key'; kn = 'UserKnownHostsFile=D:/RCA-ext/overnight-T058/out/known_hosts'
    tgt = 'ubuntu@213.35.116.128'; stage = '/home/ubuntu/t062-day'
    run = lambda c: subprocess.run([SSH, '-i', key, '-o', kn, '-o', 'BatchMode=yes', tgt, c], check=True, stdin=subprocess.DEVNULL)
    run(f'rm -rf {stage} && mkdir -p {stage}/chi-muc {stage}/phat-lai/chi-muc')
    up = lambda src, dst: subprocess.run([SCP, '-q', '-i', key, '-o', kn] + [str(s) for s in src] + [f'{tgt}:{dst}'], check=True)
    up([KQ / f'{i}.json' for i in ids], stage + '/')
    up([KQ / 'chi-muc' / 'danh-sach-su-co.json'], stage + '/chi-muc/')
    if phat_lai:
        subprocess.run([sys.executable, '-B', str(O / 'giao-dien' / 'chi-muc-phat-lai.py'), str(KQ / 'phat-lai')], check=True)
        up([KQ / 'phat-lai' / f'{i}.phat-lai.json' for i in ids], stage + '/phat-lai/')
        up([KQ / 'phat-lai' / 'chi-muc' / 'danh-sach-phat-lai.json'], stage + '/phat-lai/chi-muc/')
    D = '/opt/flash-ticket-obs/rca-ket-qua'
    run(f'set -e; sudo mkdir -p {D}/chi-muc {D}/phat-lai/chi-muc; sudo cp {stage}/*.json {D}/; '
        f'sudo cp {stage}/chi-muc/danh-sach-su-co.json {D}/chi-muc/; '
        + (f'sudo cp {stage}/phat-lai/*.json {D}/phat-lai/; sudo cp {stage}/phat-lai/chi-muc/*.json {D}/phat-lai/chi-muc/; ' if phat_lai else '')
        + f'sudo chmod -R a+rX {D}; ls {D} | wc -l')
    print('đã đẩy', len(ids), 'ca', '(+ phát lại)' if phat_lai else '')

if __name__ == '__main__':
    ids = buoc_1_2(); buoc_3(ids)
    if '--phat-lai' in sys.argv: buoc_4(ids)
    if '--day' in sys.argv: day(ids, '--phat-lai' in sys.argv)
