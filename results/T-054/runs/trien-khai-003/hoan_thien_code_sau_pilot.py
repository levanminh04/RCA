"""Chỉ áp dụng sau khi lô ghim code đã dừng; giữ byte code pilot trước sửa."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path.insert(0, str(OUT / 'scripts'))
from dieu_phoi import status

if status(RUN / 'pilot-local-005/queue')['controller'] is not None:
    raise RuntimeError('Pilot vẫn chạy; không sửa code đã pin')
before = RUN / 'code-pilot-002'
before.mkdir(exist_ok=False)
for p in (OUT / 'scripts').glob('*.py'):
    (before / p.name).write_bytes(p.read_bytes())

# Generator giữ trạng thái quyết định và nguồn quyền hiện hành, không reset về phiên soạn SPEC.
p = OUT / 'scripts/lap_ho_so.py'
s = p.read_text(encoding='utf-8')
s = s.replace("'torai_A': 'OPEN: chưa tự loại hoặc thêm trước Minh quyết', 'test_sources_materialized': False}",
"""'torai_A': {'scope': 'A phụ ngoài A4, B chính theo P3 và Minh xác nhận lại',
                         'source_grant': False},
            'auxiliary': [{'dataset': 'RE2-TT', 'opaque_id': 'test-' + m[:10],
                           'member_sha256': m, 'arm': 'torai_A', 'view': 'main', 'seed': seed,
                           'worlds': ['P'], 'a4': False, 'source_access': 'WAIT_A_SOURCE_GRANT'}
                          for m in cohort['cohorts']['RE2-TT']['members_locked_sha256'] for seed in (0, 1, 2)],
            'test_sources_materialized': False}""")
start = s.index('def build_documents():')
end = s.index("\n\nif __name__ == '__main__':", start)
s = s[:start] + '''def build_documents():
    """Đọc/kiểm hồ sơ hiện hành; không ghi đè lịch sử hoặc reset quyền bằng mặc định cũ.

    Cập nhật hồ sơ phải có nguồn quyết định mới và manifest riêng. Lệnh này không
    còn tái sinh ứng viên cũ trước câu trả lời Minh về A/B hay tự hạ/nâng quyền.
    """
    current = {name: read_pin(ref(OUT / name)) for name in
               ('protocol.json', 'matrix.json', 'authorization.json', 'source-manifest.json')}
    source = current['source-manifest.json']
    for path, expected in source['own_scripts'].items():
        actual = ref(ROOT / path)
        if actual['sha256'] != expected['sha256']:
            raise ValueError('source-manifest chưa cập nhật code: ' + path)
    return {'status': current['protocol.json']['status'],
            'matrix': current['matrix.json']['counts'],
            'own_scripts': len(source['own_scripts']),
            'authorization': ref(OUT / 'authorization.json'),
            'documents_overwritten': False, 'test_opened': False}
''' + s[end:]
p.write_text(s, encoding='utf-8')

# Nguồn nhãn dev cũng được dựng lại từ G1 độc lập lúc evaluator gọi, không tin bản nhãn do runtime tự khai.
p = OUT / 'scripts/nguon.py'
s = p.read_text(encoding='utf-8')
needle = 'def compare_labels(labels, independent, runtime, aliases, universe):\n'
assert needle in s
s = s.replace(needle, needle + "    if independent.get('schema') == 'T054-DEV-LABEL-ORIGINALS-1':\n        independent = original_dev_labels(independent, aliases)\n")
s += '''

def original_dev_labels(descriptor, aliases):
    """Chỉ evaluator sau seal gọi. G1 gốc là nguồn nhãn, tách khỏi runtime mới."""
    import csv
    import io
    source = original_dev_sources(descriptor['source_descriptor'])
    pin = descriptor['source_descriptor']['g1_ref']
    path = Path(pin['path'])
    if not path.is_absolute():
        path = ROOT / path
    if digest(path) != pin['sha256']:
        raise Blocked('nguồn G1 nhãn đổi hash')
    ds = descriptor['source_descriptor']['dataset']
    by_member = {}
    for row in csv.DictReader(io.StringIO(path.read_text(encoding='utf-8-sig'))):
        if row['dataset'] != ds or row['vai_tro'] != 'dev':
            continue
        member = fingerprint([ds, row['case']])
        if member not in source['cases_by_member']:
            continue
        canonical = aliases.get(row['root'], row['root'])
        by_member[member] = {'member_sha256': member, 'root': canonical,
                             'fault': row['fault'], 'cell': [ds, canonical, row['fault']]}
    if set(by_member) != set(source['cases_by_member']):
        raise Blocked('G1 dev label thiếu/thừa thành viên')
    return {'dataset': ds, 'g1_revision': pin['sha256'],
            'alias_sha256': fingerprint(aliases), 'by_member': by_member}
'''
p.write_text(s, encoding='utf-8')

# Không cho snapshot tự gắn VERIFIED vào lỗi chưa phân loại rồi vượt bước chấm.
p = OUT / 'scripts/worker.py'
s = p.read_text(encoding='utf-8')
needle = "            data = source_record['extra']['dau_vao_cd3']\n"
assert needle in s
s = s.replace(needle, "            data = dict(source_record['extra']['dau_vao_cd3'])\n"
                      "            if 'canh' not in data:\n"
                      "                data['canh'] = source_record['extra']['canh']\n")
p.write_text(s, encoding='utf-8')

p = OUT / 'scripts/bien_nhan.py'
s = p.read_text(encoding='utf-8')
s += '''

def verify_dev_error_reproduction(pin, job, envelope, invocation):
    """Chỉ ERROR dev đã tái hiện đúng baseline gốc và có audit code/đầu vào.

    Không cấp chính sách lỗi test/TIMEOUT; các trường hợp đó vẫn BLOCKED.
    """
    c = read_pin(pin)
    if (job.get('evaluation_mode') != 'dev' or c.get('scope') != 'DEV_BASELINE_REPRODUCTION_ONLY'
            or c.get('job_sha256') != fingerprint(job)
            or c.get('result_sha256') != fingerprint(envelope)
            or c.get('invocation_sha256') != fingerprint(invocation)):
        raise Blocked('phân loại lỗi dev không cùng job/output/phạm vi')
    old = read_pin(c['baseline_reference'])
    record, = envelope['records']
    if (record.get('status') != 'ERROR' or old.get('status') != 'ERROR'
            or old.get('opaque_id') != job['slot']['opaque_id']):
        raise Blocked('không suy giấy tái hiện ERROR sang TIMEOUT/lỗi khác')
    for key in ('method', 'mode', 'seed', 'status', 'error', 'window', 'blocks', 'entity_ranking', 'ranking_native', 'observed_entities'):
        if old.get(key) != record.get(key):
            raise Blocked('ERROR dev khác bản gốc: ' + key)
    if c.get('origin') != 'method_implementation_assumption':
        raise Blocked('chưa phân xử nguồn lỗi')
    from nguon import compare_sources
    compare_sources(read_pin(job['runtime_ref']), read_pin(job['independent_source_ref']),
                    job['slot']['dataset'], job['g1_revision'])
    audit = read_pin(c['input_audit'])
    arm = job['slot']['arm']
    if (arm not in ('microrank', 'tracerca') or audit['t'] != job['t']
            or audit['trace_sha256'] != job['source']['files']['traces.parquet']['sha256']
            or audit['normal_count'][arm] != 0 or audit['anomalous_count'][arm] <= 0):
        raise Blocked('thiếu bằng chứng operation mới tại đầu vào hợp lệ')
    if len(c.get('code_evidence', [])) < 2:
        raise Blocked('thiếu code method và adapter ánh xạ lỗi')
    for item in c['code_evidence']:
        path = Path(item['path'])
        if not path.is_absolute():
            path = ROOT / path
        if digest(path) != item['sha256']:
            raise Blocked('code phân loại lỗi thay đổi')
    return c
'''
p.write_text(s, encoding='utf-8')

p = OUT / 'scripts/dieu_phoi.py'
s = p.read_text(encoding='utf-8')
needle = "    if any(r.get('status') in ('ERROR', 'TIMEOUT') for r in records):\n        raise Blocked('lỗi phương pháp cần phân loại với bằng chứng, chưa tự tính trượt')\n"
assert needle in s
s = s.replace(needle, "    if any(r.get('status') in ('ERROR', 'TIMEOUT') for r in records):\n"
                      "        from bien_nhan import verify_dev_error_reproduction\n"
                      "        path = attempt / 'dev-error-reproduction.json'\n"
                      "        if not path.is_file():\n"
                      "            raise Blocked('lỗi phương pháp cần phân loại với bằng chứng, chưa tự tính trượt')\n"
                      "        verify_dev_error_reproduction(ref(path), job, envelope, invocation)\n")
p.write_text(s, encoding='utf-8')

p = OUT / 'scripts/cham.py'
s = p.read_text(encoding='utf-8')
needle = "            results[key] = verify_envelope(envelope, invocation, job['slot'], slot['token'])\n"
assert needle in s
s = s.replace(needle, needle + "            if any(r.get('status') in ('ERROR', 'TIMEOUT') for r in results[key]):\n"
                             "                from bien_nhan import verify_dev_error_reproduction\n"
                             "                if not receipt.get('dev_error_reproduction'):\n"
                             "                    raise Blocked('snapshot lỗi chưa có finalization/phân loại được duyệt')\n"
                             "                verify_dev_error_reproduction(receipt['dev_error_reproduction'], job, envelope, invocation)\n")
p.write_text(s, encoding='utf-8')
print('Updated generator, original dev label reader and snapshot failure gate; preserved code-pilot-002')
