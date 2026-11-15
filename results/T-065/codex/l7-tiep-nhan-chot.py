"""Chốt bằng chứng L7 đã thu trên UI; không gửi truy vấn hay sửa máy chủ."""
import datetime as dt
import hashlib
import json
import pathlib
import re
import subprocess
import sys

BASE = pathlib.Path('results/T-065')
OUT = BASE / 'kiem/004-r1-ui06'


def read(p):
    return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))


def write(p, obj):
    pathlib.Path(p).write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def iso(ms):
    return dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z')


def evidence():
    dom = (OUT / '19-inspector-request-response.txt').read_text(encoding='utf-8')
    assert 'button "Collapse all"' in dom and 'tab "Query" [selected]' in dom
    generic = []
    for line in dom.splitlines():
        m = re.match(r'\s*- generic: (.*)$', line)
        if m:
            value = m[1]
            generic.append(json.loads(value) if value.startswith('"') else value)

    def scalar(key):
        values = [x[len(key) + 1:] for x in generic if x.startswith(key + ':')]
        assert len(values) == 1, (key, values)
        return json.loads(values[0])

    query = scalar('expr')
    lo, hi = int(scalar('from')), int(scalar('to'))
    status = scalar('status')
    arrays = []
    for i, value in enumerate(generic):
        if value != '[41]':
            continue
        data = []
        for item in generic[i + 1:]:
            m = re.fullmatch(r'(\d+):(-?\d+(?:\.\d+)?)', item)
            if not m:
                break
            assert int(m[1]) == len(data)
            data.append(float(m[2]) if '.' in m[2] else int(m[2]))
        assert len(data) == 41
        arrays.append(data)
    assert len(arrays) == 4
    routes = [json.loads(x.split(':', 1)[1]) for x in generic if x.startswith('http_route:')]
    assert routes == ['/actuator/health', '/api/v1/orders/{orderId}']
    frames = [{'labels': {'http_request_method': 'GET', 'http_route': routes[i]},
               'time_ms': arrays[2 * i], 'values': arrays[2 * i + 1]} for i in range(2)]
    source_index = read('results/T-064/ban-xuat/chi-muc-ban.json')
    entry = source_index['ban'][2]['cac_ca'][15]
    assert entry['ca'] == '2e2a5541' and sha(entry['dau_ra']) == entry['sha256']
    source = read(entry['dau_ra'])
    assert source['window']['don_vi'] == 'ns'
    window_ms = [source['window']['N'][0] // 1_000_000, source['window']['A'][1] // 1_000_000]
    assert source['window']['N'][1] == source['window']['A'][0]
    assert window_ms == [lo, hi + 1]
    assert [lo, hi] == [1794435513000, 1794436112999]
    assert status == 200
    assert query == 'sum by (http_request_method, http_route) (rate(http_server_request_duration_seconds_count{service_name="booking-service"}[1m]))'
    assert scalar('requestId') == '31A'
    normalized = {
        'utc_doc_DOM': '2026-11-14T12:15:02.455Z',
        'doi_chieu_lan_bam': 19,
        'gio_bam': None,
        'nguon': '19-inspector-request-response.txt',
        'cach_luu': 'Trích xuất các trường và toàn bộ mảng số từ cây Inspector đã Expand all; không phải JSON transport xuất từ clipboard.',
        'request': {'url': scalar('url'), 'method': scalar('method'), 'panel': 31,
                    'datasource': 'prometheus', 'expr': query, 'from': lo, 'to': hi,
                    'intervalMs': scalar('intervalMs'), 'requestId': scalar('requestId')},
        'response': {'results': {'A': {'status': status, 'frames': frames}}},
        'nguon_phuong_phap': {'file': entry['dau_ra'], 'pointer': '/window', 'window_source': source['window'], 'window_half_open_ms': window_ms},
        'anh': ['anh/19-2e2a5541-inspector-p31.jpg', 'anh/19-2e2a5541-inspector-bien-response.jpg']}
    summary = {'panel': 31, 'datasource': 'prometheus', 'query': query,
               'from_ms': lo, 'to_ms': hi, 'from': iso(lo), 'to': iso(hi), 'step': '15s',
               'http': str(status), 'status_field': 'response.results.A.status',
               'frames': len(frames), 'rows': 'A:41 rows', 'total_points': sum(len(x['values']) for x in frames),
               'timeSeries': [{'labels': f['labels'], 'points': len(f['time_ms']),
                               'first': iso(f['time_ms'][0]), 'last': iso(f['time_ms'][-1]),
                               'before_from': sum(t < lo for t in f['time_ms']),
                               'after_to': sum(t > hi for t in f['time_ms'])} for f in frames],
               'request_response_file': '19-inspector-request-response.txt',
               'extracted_file': '19-inspector-trich-xuat.json', 'observed_utc': normalized['utc_doc_DOM']}
    write(OUT / '19-inspector-trich-xuat.json', normalized)
    journal = OUT / 'nhat-ky-bam.jsonl'
    rows = [json.loads(x) for x in journal.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
    assert len(rows) == 19 and rows[-1]['stt'] == 19 and rows[-1]['utc'] is None
    record = rows[-1]
    error = {'stt': 20, 'utc': now(), 'doi_chieu_lan_bam': 19,
             'hanh_dong': 'Nối lỗi thu Inspector đầu phiên, không bấm liên kết mới',
             'loi': 'Inspector Unexpected error khi local không còn listener 13000/PID tunnel cũ; không có mã HTTP trong cây lỗi.',
             'bang_chung': '19-inspector-loi-request-response.txt', 'may': '19-su-co-tunnel.json',
             'ket_qua': 'loi_thu_bang_chung', 'gio_su_kien_chinh_xac': None,
             'ghi_chu': 'utc là giờ nối nhật ký; không phải giờ bấm 19 hay giờ Refresh lỗi. Giữ lỗi; không suy là lỗi data link.'}
    success = {**record, 'stt': 21, 'utc': now(), 'doi_chieu_lan_bam': 19,
               'gio_bam': None, 'hanh_dong': 'Nối Query Inspector panel 31 của cùng đích lần 19 sau khôi phục tunnel',
               'query_inspector': summary, 'anh': normalized['anh'][0], 'anh_bo_sung': normalized['anh'][1],
               'anh_trang_dich': record['anh'], 'ket_qua': 'dat',
               'kiem': {'uid': True, 'ban': True, 'ca': True, 'service': True, 'operation': True,
                        'window': True, 'request': True, 'response': True},
               'ghi_chu': 'Không bấm lại panel 23. utc là giờ nối bằng chứng; giờ đọc DOM ở query_inspector.observed_utc; giờ bấm gốc giữ null.'}
    with journal.open('a', encoding='utf-8') as f:
        for x in (error, success):
            f.write(json.dumps(x, ensure_ascii=False, separators=(',', ':')) + '\n')
    compared = read(OUT / 'doi-chieu-dich.json')
    hit = next(x for x in compared['lan_bam'] if x['lan_bam'] == 19)
    hit.update(bang_chung=21, query_inspector=summary, anh=normalized['anh'][0],
               anh_trang_dich=record['anh'], anh_bo_sung=normalized['anh'][1], ket_qua='dat', phan_loai_rong=None,
               gio_bam=None, bang_chung_su_co='19-su-co-tunnel.json')
    hit['kiem'].update(service=True, request=True, response=True)
    stream = next(x for x in compared['luong'] if x['ca'] == '2e2a5541' and x['luong'] == 'chinh_23')
    stream.update(ket_qua='dat', lan_bam_chot=19, bang_chung=21)
    compared.update(utc=now(), trang_thai='dat', passed=sum(x['ket_qua'] == 'dat' for x in compared['luong']),
                    journal_rows=21, r1='Đủ bằng chứng mẫu được duyệt; chờ Claude kiểm lại và Minh quyết.')
    assert compared['passed'] == compared['total'] == 12
    write(OUT / 'doi-chieu-dich.json', compared)
    state = read(BASE / 'codex/L7-trang-thai.json')
    state.update(trang_thai='xong', cap_nhat=now(), buoc='12/12 luồng đạt; đã nối Inspector của lần bấm 19; chờ phản biện',
                 bao_cao='kiem/004-r1-ui06/BAO-CAO.md', r1='du_bang_chung_mau_cho_kiem_lai',
                 task='dat_mot_phan', G_c='Chờ bản M1-FT đề xuất cuối cùng chỉ mục/hash của T-064',
                 tunnel={'pid': 43220, 'exec_session': 46123, 'local': '127.0.0.1:13000', 'remote': '10.0.0.215:3000'},
                 checkpoint_lich_su=state.pop('checkpoint', None))
    write(BASE / 'codex/L7-trang-thai.json', state)
    print(json.dumps({'passed': compared['passed'], 'total': compared['total'], 'query_inspector': summary}, ensure_ascii=False))


def seal():
    prior = read(BASE / 'codex/manifest-L7-tiep-nhan-truoc.json')
    original = read(BASE / 'codex/manifest-L7-truoc.json')
    reception = read(OUT / 'tiep-nhan-integrity.json')
    changed_allowed = {'codex/L7-trang-thai.json', 'kiem/004-r1-ui06/BAO-CAO.md',
                       'kiem/004-r1-ui06/doi-chieu-dich.json', 'kiem/004-r1-ui06/nhat-ky-bam.jsonl',
                       'kiem/004-r1-ui06/may.jsonl'}
    files = {}
    paths = set(prior['files'])
    paths.update(p.relative_to(BASE).as_posix() for p in OUT.rglob('*') if p.is_file())
    paths.update({'codex/manifest-L7-tiep-nhan-truoc.json', 'codex/l7-tiep-nhan-chot.py'})
    report_rel = 'kiem/004-r1-ui06/kiem-cuoi-tiep-nhan.json'
    paths.discard(report_rel)
    missing = []
    for i, p in enumerate(sorted(paths)):
        f = BASE / p
        if not f.exists():
            missing.append(p)
            continue
        files[p] = {'sha256': sha(f), 'bytes': f.stat().st_size}
        if i % 2000 == 0:
            print(f'Hash {i}/{len(paths)}', flush=True)
    assert not missing, missing
    modified = sorted(p for p in prior['files'] if prior['files'][p] != files[p])
    assert set(modified) == changed_allowed, modified
    assert all(files[p] == v for p, v in original['files'].items())
    protected = {p: sha(p) == h for p, h in reception['protected'].items()}
    assert all(protected.values()), protected
    log_path = pathlib.Path(prior['task_log']['file'])
    log = log_path.read_bytes()
    assert hashlib.sha256(log[:prior['task_log']['bytes']]).hexdigest() == prior['task_log']['sha256']
    assert len(log) > prior['task_log']['bytes']
    for name, prefix_key in [('nhat-ky-bam.jsonl', 'journal_prefix_bytes'), ('may.jsonl', 'machine_prefix_bytes')]:
        rel = 'kiem/004-r1-ui06/' + name
        prefix = (OUT / name).read_bytes()[:reception[prefix_key]]
        assert hashlib.sha256(prefix).hexdigest() == prior['files'][rel]['sha256']
    d = read(OUT / 'doi-chieu-dich.json')
    journal = [json.loads(x) for x in (OUT / 'nhat-ky-bam.jsonl').read_text(encoding='utf-8-sig').splitlines() if x.strip()]
    assert len(journal) == d['journal_rows'] == 21
    assert journal[18]['stt'] == 19 and journal[18]['utc'] is None
    assert all(x['doi_chieu_lan_bam'] == 19 for x in journal[19:])
    assert len([x for x in journal if not x.get('doi_chieu_lan_bam')]) == d['attempt_count'] == 15
    assert d['passed'] == d['total'] == len(d['luong']) == 12
    assert len(set((x['ca'], x['luong']) for x in d['luong'])) == 12
    rows = {x['stt']: x for x in journal}
    for stream in d['luong']:
        assert stream['ket_qua'] == 'dat'
        ev = rows[stream['bang_chung']]
        assert ev['query_inspector']['http'] == '200'
        assert ev['query_inspector']['frames'] > 0
        assert all(x['points'] > 0 for x in ev['query_inspector']['timeSeries'])
        image = OUT / ev['anh']
        assert image.stat().st_size > 0
    old_d = read(BASE / 'codex/manifest-L7-tiep-nhan-truoc.json')
    # Báo cáo cũ và nhật ký/checkpoint giữ bằng hash/snapshot; không xóa lượt lỗi.
    assert files['kiem/004-r1-ui06/checkpoint-v041-p23.json'] == old_d['files']['kiem/004-r1-ui06/checkpoint-v041-p23.json']
    sources = []
    index = read('results/T-064/ban-xuat/chi-muc-ban.json')
    for sample in read(OUT / 'mau-chon.json')['samples']:
        pointer = sample['nguon_chi_muc'].split('#', 1)[1]
        entry = index
        for part in pointer.strip('/').split('/'):
            entry = entry[int(part)] if isinstance(entry, list) else entry[part]
        assert entry['ca'] == sample['ca'] and sha(entry['dau_ra']) == entry['sha256']
        w = read(entry['dau_ra'])['window']
        assert w['don_vi'] == 'ns' and w['N'][1] == w['A'][0]
        assert [w['N'][0] // 1_000_000, w['A'][1] // 1_000_000] == sample['cua_so_ms_nua_mo']
        sources.append({'file': entry['dau_ra'], 'pointer': pointer, 'hash_match': True, 'window_match': True})
    template = pathlib.Path('docs/review-prompt.md').read_text(encoding='utf-8-sig')
    block = lambda h: re.search(r'```text\n(.*?)\n```', template[template.index(h):], re.S).group(1)
    log_text = log.decode('utf-8-sig').replace('\r\n', '\n')
    prompt = log_text.split('### Prompt cho Claude — kiểm lại phản hồi L6 và L7 đã chốt\n\n')[-1].strip()
    tail = '\n\n' + block('### Kiểm lại phản hồi và sửa') + '\n\n' + block('### G4 — Kết quả')
    assert prompt.endswith(tail)
    common = block('## Prompt chung')
    pattern = '^' + '(.*?)'.join(re.escape(x) for x in re.split(r'<[^>]+>', common)) + '$'
    assert re.fullmatch(pattern, prompt[:-len(tail)], re.S)
    assert len(re.findall(r'<[^>]+>', common)) == 8
    for image in [OUT / 'anh/19-2e2a5541-inspector-p31.jpg', OUT / 'anh/19-2e2a5541-inspector-bien-response.jpg']:
        raw = image.read_bytes()
        assert raw.startswith(b'\xff\xd8') and raw.endswith(b'\xff\xd9')
    check = subprocess.run(['git', 'diff', '--check'], capture_output=True, text=True, encoding='utf-8')
    assert check.returncode == 0, check.stdout + check.stderr
    new_files = sorted((set(files) | {report_rel}) - set(prior['files']))
    report = {'utc': now(), 'status': 'dat', 'prior_files_checked': len(prior['files']),
              'missing': [], 'modified_files': modified, 'new_files': new_files,
              'old_pre_L7_files_unchanged': len(original['files']), 'protected': protected,
              'log_append_only': True, 'journal_append_only': True, 'machine_log_append_only': True,
              'original_click_19_utc_null': True, 'new_link_clicks_this_reception': 0,
              'flows_passed': 12, 'flows_total': 12, 'journal_rows': 21, 'click_attempts': 15,
              'sources': sources, 'prompt_common_template_match_except_metadata': True,
              'prompt_stage_exact': True, 'prompt_gate_exact': True, 'git_diff_check_exit': check.returncode,
              'manifest_scope': 'Giữ toàn bộ mục đã ghim; chỉ thêm đầu ra thuộc L7, không kéo tệp điều phối khác vào phạm vi.',
              'changed_file_set_including_log_and_manifest': [str(BASE / p).replace('\\', '/') for p in sorted(set(modified) | set(new_files))] + ['results/T-065/manifest.json', str(log_path).replace('\\', '/')],
              'tool_errors_preserved': ['19-su-co-tunnel.json và cây lỗi Inspector',
                  'Ảnh API timeout ba lần; hai lần click tab native thiếu geometry; đưa đúng tab ra trước bằng Ctrl+3 rồi chụp thành công.',
                  'Script evidence lần đầu dừng trước ghi vì window là object ns; đã sửa đọc schema ns và đối chiếu biên.',
                  'Một lệnh đọc prompt ra stdout lỗi cp1252; tạo prompt bằng UTF-8 và kiểm nguyên khối.',
                  'Seal lần đầu dừng trước ghi manifest vì phép so prompt chưa chuẩn hóa CRLF; chuẩn hóa newline trong phép đọc rồi kiểm nguyên khối, không sửa prompt.'],
              'scientific_decisions_added': [], 'R1': 'Đủ bằng chứng mẫu, chờ Claude kiểm lại và Minh quyết',
              'G_c': 'Chờ bản M1-FT đề xuất cuối T-064', 'STATE_not_modified': True}
    write(OUT / 'kiem-cuoi-tiep-nhan.json', report)
    files[report_rel] = {'sha256': sha(OUT / 'kiem-cuoi-tiep-nhan.json'), 'bytes': (OUT / 'kiem-cuoi-tiep-nhan.json').stat().st_size}
    manifest = {'utc': now(), 'status': 'xong', 'status_scope': 'L7', 'task_status': 'dat_mot_phan',
                'prior_manifest': 'codex/manifest-L7-tiep-nhan-truoc.json',
                'pre_L7_manifest': 'codex/manifest-L7-truoc.json', 'excluded': prior['excluded'],
                'task_log': {'file': str(log_path).replace('\\', '/'), 'bytes': len(log), 'sha256': hashlib.sha256(log).hexdigest()},
                'new_files': new_files, 'modified_files': modified, 'files': files}
    write(BASE / 'manifest.json', manifest)
    print(json.dumps({'hashed': len(files), 'modified': modified, 'new_files': new_files, 'checks': 'dat'}, ensure_ascii=False), flush=True)


def verify():
    m = read(BASE / 'manifest.json')
    bad = []
    for i, (p, v) in enumerate(m['files'].items()):
        f = BASE / p
        if not f.exists() or f.stat().st_size != v['bytes'] or sha(f) != v['sha256']:
            bad.append(p)
        if i % 2000 == 0:
            print(f'Verify {i}/{len(m["files"])}', flush=True)
    lp = pathlib.Path(m['task_log']['file'])
    assert sha(lp) == m['task_log']['sha256'] and lp.stat().st_size == m['task_log']['bytes']
    assert not bad, bad
    print(json.dumps({'verified': len(m['files']), 'mismatch': bad, 'task_log_match': True}, ensure_ascii=False), flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'evidence':
        evidence()
    elif sys.argv[1] == 'seal':
        seal()
    elif sys.argv[1] == 'verify':
        verify()
    else:
        raise SystemExit('evidence | seal | verify')
