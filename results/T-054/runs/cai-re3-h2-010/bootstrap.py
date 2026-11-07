from pathlib import Path
import hashlib
import json
import datetime

ROOT = Path(__file__).resolve().parents[4]
RUN = Path(__file__).resolve().parent


def pin(p):
    b = p.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


previous = json.loads((ROOT/'results/T-054/manifest-chuan-bi-re3-009.json').read_text(encoding='utf-8'))
for rel, v in {**previous['outputs'], **previous['mutable_checkpoint']}.items():
    assert pin(ROOT/rel) == v, rel
code = ['src/p3/re3.py', 'src/m1/adapter.py', 'src/p3/adapters/baro.py', 'src/p3/adapters/circa.py',
        'src/p3/adapters/tracerca.py', 'src/p3/adapters/torai.py', 'results/T-054/scripts/nguon.py',
        'results/T-054/scripts/worker.py', 'results/T-054/scripts/cham.py']
docs = ['tasks/T-054-khoa-g3-chay-p7-a/SPEC.md', 'docs/WHY.md', 'docs/DECISIONS.md',
        'tasks/T-054-khoa-g3-chay-p7-a/LOG.md', 'docs/STATE.md']
before = {}
for rel in code + docs:
    p = ROOT/rel
    before[rel] = pin(p) if p.exists() else None
    if p.exists():
        target = RUN/'before'/rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(p.read_bytes())
checkpoint = {'schema': 'T054-RE3-H2-010', 'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'authorization': {'user_verbatim': 'Duyệt cài H2 theo báo cáo009',
                                'proposal': 'results/T-054/runs/chuan-bi-re3-009/bao-cao.md#Bản vá H2 cụ thể trình duyệt',
                                'code_files': code, 'documents': docs[:3]},
              'status': 'AUTHORIZED_SOURCES_RECORDED_BEFORE_CODE', 'before': before,
              'H1_units_inventory_resolution_open': True, 'RE3_telemetry_opened': False,
              'main_started': False, 'cloud_paused': True,
              'milestones': ['source/scope snapshot', 'reader/M1 and baseline adapters',
                             'grant/worker/held-out tables', 'synthetic/default verification', 'diff/manifest/report/handoff'],
              'next': 'Implement exact9code scope; fixture inputs only; no change to m1 core or locked data'}
(RUN/'checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
notes = {
    'docs/DECISIONS.md': '\n\n## T-054 — duyệt cài H2 RE3, 06/11/2026 — USER_CONFIRMED\n\nMinh: “Duyệt cài H2 theo báo cáo009”. Phạm vi là 9 file code cùng SPEC/WHY/DECISIONS trong mục Bản vá H2 cụ thể trình duyệt tại results/T-054/runs/chuan-bi-re3-009/bao-cao.md. Cài tuyến RE3 riêng và kiểm bằng dữ liệu tổng hợp; giữ mặc định TT/Nezha, bắt buộc profile thời gian/U/alias/r đã ghim. Duyệt cài không xác nhận các đơn vị/inventory còn thiếu, không mở telemetry hoặc đánh giá RE3, G3/main, cloud, commit/push.\n',
    'docs/WHY.md': '\n\n## T-054 — H2: adapter RE3 với profile tường minh, 06/11/2026\n\nMinh duyệt cài theo báo cáo009. Nhu cầu kỹ thuật: RE3 có schema riêng; source time/r/U/alias chưa đủ nguồn, worker hiện chọn TT/Nezha và TORAI lọc ts-* làm rỗng metric OB trong kiểm tổng hợp. Chọn reader/profile riêng, kiểm hợp đồng trước I/O và dispatch/chấm held-out riêng; không sửa công thức M1/kernel baseline. Phương án tái dùng nguyên adapter TT làm mất metric; giả tên dataset hoặc tự đoán đơn vị/U từ nhãn làm sai đầu vào. Thêm tham số dataset tùy chọn giữ mặc định cũ cho BARO/CIRCA/TraceRCA; literal re2-tt không tự chứng minh sai số. Bằng chứng metadata/code và27kiểm ở009, chưa kiểm trên RE3 thật. Điều kiện thất bại: profile thiếu/sai, alias va chạm, clock không biểu diễn chính xác, owner ngoài U, source/grant khác binding; dừng trước method. Inventory/đơn vị/r/semantics status còn OPEN; duyệt cài không biến giả định thành FACT. Phụ thuộc: khả năng thực thi RE3 bản cuối và bảng riêng; không xác nhận hiệu quả RCA, RQ3/RQ5 hay mở dữ liệu. Các kiểm tổng hợp mới sẽ nằm ở checkpoint010.\n',
    'tasks/T-054-khoa-g3-chay-p7-a/LOG.md': '\n\n## Tiếp tục phiên dài — 06/11/2026 — Codex, Windows, người làm — checkpoint010\n\nMinh: “Duyệt cài H2 theo báo cáo009”. Đã kiểm manifest009 (output bất biến và snapshot LOG/STATE hiện hành), lưu trước các file trong010/before và nguồn duyệt trong checkpoint. Nối DECISIONS/WHY và thêm đúng phạm vi SPEC trước sửa code. Mốc: reader/profile→M1/baseline→grant/worker/bảng riêng→synthetic/default→diff/manifest/bàn giao. Chỉ dữ liệu tổng hợp; H1 đơn vị/r/U/alias còn OPEN, cloud tạm dừng, không mở RE3/main. Không sửa m1/chuoi hoặc phát lô.\n'}
for rel, text in notes.items():
    with (ROOT/rel).open('a', encoding='utf-8', newline='') as f:
        f.write(text)
p = ROOT/'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md'
b = p.read_bytes()
needle = '## Phạm vi ghi'.encode('utf-8')
addition = ('\n\n**Bổ sung Minh duyệt H2 ngày06/11/2026:** “Duyệt cài H2 theo báo cáo009”. Cài đúng9file: `src/p3/re3.py` (mới), `src/m1/adapter.py`, `src/p3/adapters/baro.py`, `circa.py`, `tracerca.py`, `torai.py`, `results/T-054/scripts/nguon.py`, `worker.py`, `cham.py`; cập nhật đúng lý do/quyền vào WHY/DECISIONS. Reader và M1 RE3 nhận profile thời gian/U/alias/r tường minh đã ghim, thiếu thì chặn trước method; default TT/Nezha giữ nguyên. Worker/grant/bảng RE3 riêng, kiểm bằng synthetic; chưa mở telemetry/đánh giá RE3 hoặc G3/main. Không sửa lõi M1/cấu hình đã chọn, không quyết các trường H1 còn OPEN. Snapshot trước sửa và kiểm ở checkpoint010.').encode('utf-8')
assert b.count(needle) == 1
p.write_bytes(b.replace(needle, needle+addition, 1))
print('010 authorization, snapshots, DECISIONS/WHY/LOG/SPEC recorded; no code changed yet')
