"""Chuẩn bị hợp đồng RE3 từ metadata lưu sẵn và code; không tải/mở telemetry."""
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / 'results/T-054'
RUN = OUT / 'runs/trien-khai-003'
sys.path.insert(0, str(OUT / 'scripts'))
from bien_nhan import atomic, ref

manifest = json.loads((ROOT / 'results/T-002/handoff-manifest.json').read_bytes())
pins = {v['path']: v for v in manifest['artifacts']}
paths = ['results/T-002/public-metadata/run-002/hf-tree.json',
         'results/T-002/public-metadata/run-002/count-summary.json',
         'results/T-002/local-inspection/run-002/schemas.json']
for relative in paths:
    assert hashlib.sha256((ROOT / relative).read_bytes()).hexdigest() == pins[relative]['sha256'], relative
tree = json.loads((ROOT / paths[0]).read_bytes())
files = [x for x in tree if x['type'] == 'file' and x['path'].startswith('re3ob_')]
sizes = Counter()
for item in files:
    sizes[Path(item['path']).name] += item['size']
cases = {x['path'].split('/')[0] for x in files}
assert len(cases) == 30
g1_ref = json.loads((OUT / 'protocol.json').read_bytes())['cohorts_source']
cohort = json.loads((ROOT / g1_ref['path']).read_bytes())
assert hashlib.sha256((ROOT / g1_ref['path']).read_bytes()).hexdigest() == g1_ref['sha256']
g1_pin = cohort['G1_source']; g1_path = ROOT / g1_pin['path']
assert hashlib.sha256(g1_path.read_bytes()).hexdigest() == g1_pin['sha256']
g1 = [r for r in csv.DictReader(g1_path.open(encoding='utf-8-sig', newline='')) if r['dataset'] == 'RE3-OB']
assert {r['case'] for r in g1} == cases
cells = {(r['root'], r['fault']) for r in g1}
assert len(cells) == 10
schemas = json.loads((ROOT / paths[2]).read_bytes())
re3_schemas = [k for k in schemas if k.startswith('re3ob_')]
document = {'schema': 'T054-RE3-PREPARATION-1', 'status': 'CONTRACT_CANDIDATE_NOT_EXECUTABLE',
 'scope': 'Pha1 bắt buộc chuẩn bị; telemetry chỉ mở riêng cho bản cuối',
 'metadata_verified': [ref(ROOT / p) for p in paths], 'g1': g1_pin,
 'cohort': {'cases': len(cases), 'cells': len(cells), 'byte_total': sum(sizes.values()), 'bytes_by_file': sizes},
 'observed_RE3_OB_local_schemas': re3_schemas, 'RE3_telemetry_opened': False, 'download_performed': False,
 'blockers_in_current_code': [
  {'path': 'src/m1/adapter.py', 'issue': 'ho_so_nguon chỉ có profile RE2-TT/Nezha-OB; profile metric/log/r/aliases RE3 chưa kiểm'},
  {'path': 'src/p3/adapters/torai.py', 'issue': 'metric chi_ts=True chỉ giữ ts-*; áp sang OB có thể làm rỗng nguồn metric'},
  {'path': 'src/p3/adapters/baro.py', 'issue': "dataset='re2-tt' cố định; cần kiểm quy tắc OB của upstream trước quyết định"},
  {'path': 'src/p3/adapters/circa.py', 'issue': "preprocess re2-tt cố định; cần kiểm mapping, graph và phép đo thật của OB"},
  {'path': 'src/p3/adapters/tracerca.py', 'issue': "dataset re2-tt và ánh xạ operation; chưa đối chiếu schema RE3"},
  {'path': 'results/T-054/scripts/nguon.py', 'issue': 'grant/slot chỉ nhận hai bộ chính; không đổi tên RE3 thành Nezha hoặc TT để lách'},
  {'path': 'results/T-054/scripts/cham.py', 'issue': 'A4 cố định 60TT/34Nezha, không dùng A4 để chấm RE3; cần bảng riêng đã khai trước'}],
 'implementation_proposal': [
  {'step': 'H0_metadata', 'state': 'DONE_METADATA_ONLY', 'output': 'hợp đồng này; không coi có modality là schema tương thích'},
  {'step': 'H1_schema_contract', 'permission': 'schema/metadata được phép, không đọc giá trị',
   'output': 'tên/cột/dtype/unit/cadence/nullability; inventory từ service quan sát/kiến trúc, không tập root; ánh xạ tường minh',
   'missing': 'chưa có schema RE3-OB trong hồ sơ schema local đã kiểm; cần nguồn schema/footer và quyền/phạm vi lấy'},
  {'step': 'H2_adapter_synthetic', 'permission': 'Minh duyệt đúng file code/hợp đồng sau H1, chưa mở telemetry',
   'proposed_files': ['src/m1/adapter.py: profile RE3-OB riêng', 'src/p3/adapters/: nhánh RE3 từng phương pháp cần sửa',
                      'results/T-054/scripts/nguon.py, worker.py, cham.py: nguồn/grant/bảng RE3 riêng'],
   'checks': ['ns/us/s và ranh giới cửa sổ', 'không truyền locator/nhãn vào method',
              'kênh metric không bị lọc hết vì ts-*', 'span cha/con, alias, log severity, missing signal',
              'trạng thái rỗng/lỗi/unsupported theo nguyên nhân; không cứu phương pháp bằng giả trường'],
   'acceptance': 'mẫu tổng hợp đúng chuẩn cho trung gian/đầu ra kỳ vọng; đối chứng sai bị bác; pin code/env'},
  {'step': 'H3_final_only', 'permission': 'bản cuối đã khóa và grant RE3 riêng đúng 30ca/10ô, nguồn/tải/byte/quyền đọc',
   'output': 'lần đánh giá RE3 độc lập đầu; giữ mọi attempt; không pilot/tune trên RE3'},
  {'step': 'H4_report', 'output': 'bảng riêng từng phương pháp/ca/ô/support, giới hạn chuyển hệ và công cụ; sửa dùng RE3 báo riêng'}],
 'effort': {'status': 'CHUA_KIEM', 'runtime_ETA': None,
            'reason': 'chưa có schema thật; không suy runtime RE3 từ TT/Nezha hoặc dung lượng 138MB',
            'download_if_later_granted_bytes': sum(sizes.values())},
 'main_test_independence': 'chuẩn bị H0-H2 trước mở RE3; không dùng RE3 cho chọn thiết kế/pilot',
 'decisions_required': ['nguồn và phạm vi đọc schema/footer', 'duyệt exact file/hợp đồng H2',
                        'support/matrix/env/window và quyền bản cuối RE3 trước H3']}
atomic(RUN / 'hop-dong-re3.json', document)
text = '''# Chuẩn bị RE3-OB trong pha 1

Đã kiểm metadata công bố và đối chiếu G1: 30 ca, 10 ô. Chưa tải hoặc mở telemetry RE3. Bảng dung lượng, pin nguồn và kiểm code nằm trong `hop-dong-re3.json` cùng thư mục.

Đây là hợp đồng chuẩn bị, chưa phải adapter đã cài. Hồ sơ schema local hiện không có RE3-OB. Adapter đang có còn giả định TT: TORAI lọc cột ts-*, BARO/CIRCA/TraceRCA ghim dataset re2-tt; profile M1 chỉ có TT/Nezha. Do đó không thể đổi nhãn dataset rồi tuyên bố RE3 được hỗ trợ.

Thứ tự cần làm: xác minh schema/đơn vị và inventory phi nhãn → duyệt file/hợp đồng sửa → kiểm adapter bằng mẫu tổng hợp đúng schema → khóa cho bản cuối → mở riêng RE3 một lần và báo bảng riêng. Không dùng RE3 làm pilot hoặc nơi chỉnh phương pháp. Nếu chưa lấy được schema trong quyền hiện có, ghi thiếu đúng nguồn schema/footer và trình quyền, không bỏ nghĩa vụ adapter khỏi kế hoạch.

P7 chính TT/Nezha và nhánh giữ ngoài RE3 có quyền/ma trận riêng. Đầu ra chuẩn bị H0 hiện đã có; H1-H4 còn theo các phụ thuộc trong JSON. Chưa có ETA cài/chạy RE3 vì chưa xác minh schema; dung lượng metadata không thay thời gian xử lý. Không sửa src trong lượt này.
'''
(RUN / 'hop-dong-re3.md').write_text(text, encoding='utf-8')
print(json.dumps({'metadata_cases': len(cases), 'cells': len(cells), 'bytes': sum(sizes.values()),
                  'RE3_OB_schema_records_available': len(re3_schemas), 'telemetry_opened': False}))
