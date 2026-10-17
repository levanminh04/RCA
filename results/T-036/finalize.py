"""Tổng hợp kiểm hiện có, ghi bàn giao và kiểm phạm vi đã duyệt. Không chạy thực nghiệm."""
from datetime import datetime, timezone
import difflib
import hashlib
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TASK = ROOT / 'tasks/T-036-p5b-hop-dong-chung'
BASE = ROOT / 'results/T-036'
OUT = BASE / 'runs/ket-phien-001'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, sort_keys=True)
        f.write('\n')


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args]).decode('utf-8')


def main():
    OUT.mkdir(exist_ok=False)
    preflight = read(BASE / 'runs/chuan-bi-001/preflight.json')
    final = read(BASE / 'runs/kiem-005/result.json')
    previous = read(BASE / 'runs/kiem-004/result.json')
    assert final['all_pass'] and previous['all_pass']
    repeat = []
    for name in ['entity.json', 'operation.json', 'projection.json', 'compare-unknown.json',
                 'compare-two-queues.json', 'compare-trace-builder-messaging.json',
                 'trace-synthetic-messaging.json', 'compatibility.json', 'trace-projections.json', 'code-hashes.json']:
        one = BASE / 'runs/kiem-004' / name
        two = BASE / 'runs/kiem-005' / name
        repeat.append(dict(artifact=name, left_sha256=digest(one), right_sha256=digest(two),
                           byte_identical=one.read_bytes() == two.read_bytes()))
    assert all(r['byte_identical'] for r in repeat)
    save(OUT / 'determinism.json', dict(runs=['kiem-004', 'kiem-005'], checks=repeat, all_identical=True))
    for path, expected in read(BASE / 'runs/kiem-005/code-hashes.json').items():
        assert digest(ROOT / path) == expected, path
    checks = read(BASE / 'runs/chuan-bi-001/input-verification.json')['checks']
    seconds = final['seconds']
    ram = final['peak_working_set_bytes'] / 1024**2
    report = f'''# Kiểm đúng đắn và mức kết luận T-036

Tự soát SPEC từ DT18/cô, MRP, LESSONS, WHY/DECISIONS, B11–B16 và code/đầu ra T-035 chưa phát hiện điểm phải sửa SPEC. Nhận xét độc lập được ghi LOG Phiên 2 trước implementation. Codex giữ người làm, Claude phản biện chính thức. Đầu ra hiện chờ phản biện; chưa nghiệm thu hoặc đóng task.

## 1. Nguồn và thứ tự bằng chứng

`runs/chuan-bi-001/input-verification.json#/checks`: {len(checks)} artifact được chọn kiểm hash, tất cả khớp; gồm toàn bộ manifest T-035 và nguồn công khai được dùng ban đầu. `preflight.json` ghi môi trường, base commit, quyền ghi, manifest hash và hash tài liệu bảo vệ. B11-C/B12/B13/B14/B16 ghim revision/hash nội dung trong `nguon.json#/sources`, đều không dirty lúc đọc. Không lấy HEAD làm hash file.

Registry hiện có {len(read(BASE/'nguon.json')['sources'])} nguồn. Bổ sung capture metadata đã kiểm hash ở `runs/chuan-bi-001/revision-verification.json`: tách RCAEval code commit, snapshot dataset và tree object Nezha; README Nezha khớp blob trong tree đã lưu. Những revision đó chưa chứng minh revision ứng dụng/deployment sinh dataset. Repo TT/Augmented-OB chỉ là nguồn ứng viên cho task sau, chưa tải.

`fixtures/oracle-before-code.json#/implementation_exists` là false; hash input/expected/definition khớp. Oracle cơ sở literal có trước implementation, không dùng builder để sinh đáp án. Các phép kiểm mở rộng trong checker (hai nguồn, nội bộ sau alias, nút cô lập, default exchange, tích hợp trace builder) được thêm khi tự đọc implementation; không gọi chúng là toàn bộ oracle trước mã. Tính đúng không chỉ dựa vào việc chạy không lỗi.

## 2. Đầu vào → xử lý → trung gian → đầu ra

| Phần kiểm | Bằng chứng và kết quả |
|---|---|
| Inventory/owner/resource | `fixtures/input.json` → `build` → `runs/kiem-005/entity.json#/resource_bindings`; DB1/DB2 riêng, một PG chung, owner riêng và metric PG chung. Inventory không là observed_nodes hay tập ứng viên RCA. |
| Quan hệ và phép chiếu | Oracle `expected.json#/entity_edges` và `#/projected_entity_record_ids` → `entity.json`, `operation.json`, `projection.json`. Entity-only được báo exclusion; không tạo operation giả. Nội bộ/span-parent không thành cạnh entity. Callback/scheduler không có caller giả. |
| Messaging | Hai queue cùng consumer, fan-out, republish: queue_metric_address giữ riêng; không event_count tĩnh, không suy logical edge từ broker. `compare-two-queues.json#/views/typed` ghi đủ tập và mẫu số. |
| Tích hợp T-035 | `trace-synthetic-messaging.json` do builder T-035 dựng từ span tổng hợp → `compare-trace-builder-messaging.json`. Các chặng broker khớp; cạnh inferred logical của trace giữ riêng trong trace_only khi nguồn tĩnh không ghi quan hệ ấy. Không coi ví dụ là runtime FT. |
| Alias/kiểu/miền | `compare-unknown.json#/views`: đầu mút khớp nhưng typed loại unknown. Checker kiểm alias thiếu/mơ hồ/chưa xác minh, operation khác owner, cạnh nội bộ sau alias, địa chỉ thiếu cả hai phía, relation domain và interval lỗi. Không đổi nghĩa quan sát theo thiết kế. |
| Tập và mẫu số | `result.json#/checks` đối chiếu danh sách literal cho giao/phần riêng/S/T, unknown/khác kiểu/rỗng. Mẫu số 0 là null, không gọi precision/recall. Members giữ bản ghi tĩnh và cạnh trace riêng. |
| Nhãn và lỗi đầu vào | API thuần; trường lạ/nhãn bị từ chối, provenance thiếu hoặc ID/kiểu mâu thuẫn bị báo. Không nhận tên ca, đường dẫn ca hay mốc tiêm để chọn cạnh. Locator nguồn chỉ truy vết. |
| Graph dev có sẵn | `compatibility.json#/graphs`: {final['compatibility_graph_count']} graph full/N/A ở hai mức, hai hệ, theo manifest hiện hành. Kiểm hash trước nạp, không sửa đầu vào. Không có mapping nguồn kiến trúc trong phép này nên loại trừ unmapped; chưa là đối chiếu kiến trúc thật. |
| Chiếu graph dev | `trace-projections.json`: {final['trace_projection_pair_count']} cặp thao tác/entity khớp, giữ ngoại lệ span-parent. Dùng graph lưu sẵn; không đọc trace thô/test hoặc chạy lại baseline. |

## 3. Các lượt và chi phí thực đo

- `runs/kiem-001/failure.json`: dừng vì selector lấy thêm graph lịch sử trong manifest, đường dẫn không thuộc thư mục hiện hành. Các kiểm trước exception được giữ. Sửa selector trong checker, không sửa đầu vào hay oracle để đạt.
- `runs/kiem-002/result.json`: kiểm ban đầu đạt. Sau tự đọc lại code, bổ sung loại nội bộ sau alias và báo nút cô lập; không sửa SPEC.
- `runs/kiem-003/result.json`: kiểm bổ sung đạt. Sau đó thêm phép tích hợp T-035 messaging tổng hợp.
- `runs/kiem-004/result.json` và `runs/kiem-005/result.json`: mỗi lượt {final['passed']} kiểm đạt, 0 lỗi. Lượt cuối {seconds:.3f} giây, peak working set khoảng {ram:.1f} MiB; số gốc ở `#/seconds`, `#/peak_working_set_bytes`, Python allocation peak ở `#/python_tracemalloc_peak_bytes`. RAM gồm Python/thư viện và cả checker, không chỉ API. Không chạy việc nặng khác đồng thời.
- Đảo bản ghi ở ba seed trong checker; hai process khác PYTHONHASHSEED giữ mọi graph/kết quả so sánh trung gian giống từng byte, kiểm ở `runs/ket-phien-001/determinism.json#/checks`. Mã đã chạy được lưu ở `runs/kiem-004/code/`, `runs/kiem-005/code/` cùng hash. Các lượt cũ chưa lưu snapshot mã riêng, không dùng chúng thay bằng chứng của hai lượt cuối.

## 4. Kết luận theo câu hỏi nguồn

**FACT:** công cụ giữ được các phản ví dụ đã kiểm, truy ngược bản ghi/provenance và phân tách mẫu số đúng hợp đồng. Thiết kế/code, quan sát runtime và lợi ích RCA không bị nâng chung một nhãn. Bộ dựng tĩnh không sinh event_count hoặc tự thêm quan hệ do correlation. Comparator không sửa graph trace.

**Suy luận có giới hạn:** hợp đồng có thể dùng làm đầu vào khảo sát T-037–039 trong các nhu cầu đã kiểm. Chưa chứng minh inventory/quan hệ toàn hệ đầy đủ; chưa có đối chiếu kiến trúc thật TT/OB. Khớp typed của non-messaging không xác nhận transport HTTP/RPC vì T-035 chưa ghi transport; members giữ channel nguồn tĩnh.

**OPEN:** runtime/build/deployment/instrumentation FlashTicket; revision ứng dụng TT/OB sinh dataset; nghĩa host của Node; độc lập metadata ngày; độ đầy đủ telemetry; lợi ích cấu trúc và lựa chọn P6. DB→instance được giữ trong lớp binding tĩnh; T-035 chưa có trường tương đương. Thiếu telemetry/mapping resource không được điền từ tên DB. Phản ví dụ, phương án bổ sung/owner/ảnh hưởng cụ thể tại `ban-giao.md` §2–3; muốn sửa hợp đồng trace hoặc thu thêm phải trình Minh riêng.

T-036 đáp ứng phần hợp đồng/công cụ trong phạm vi kiểm, chưa trả lời xong RQ3/RQ5 hoặc toàn P5b. T-037–040 cần SPEC riêng. P6/P7/P9/P10 nhận nghĩa vụ còn thiếu; dừng phản biện hay nghiệm thu công cụ không tự cho mở test hoặc khẳng định RCA có lợi.

## 5. Tự soát cuối và bàn giao

Kiểm hash/manifest/phạm vi/diff ở `runs/ket-phien-001/final-verification.json`; diff phiên ở `changes.diff`. Chỉ nối LOG, cập nhật đúng dòng T-036 trong STATE; giữ SPEC và các tài liệu nguồn. Prompt Claude lấy nguyên văn mẫu ở `prompt-claude.txt` và LOG Phiên 2. Không thêm quyết định khoa học, không tự sửa WHY/DECISIONS, không commit/push.
'''
    (BASE / 'kiem-dung-dan.md').write_text(report, encoding='utf-8')
    template = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')

    def block(heading):
        tail = template.split(heading, 1)[1]
        return re.search(r'```text\n(.*?)\n```', tail, re.S).group(1)

    common = block('## Prompt chung')
    placeholders = re.findall(r'<[^>]+>', common)
    values = [
        'T-036; D:/RCA-flashticket/tasks/T-036-p5b-hop-dong-chung/SPEC.md',
        'soát kết quả',
        'P5; chuẩn bị G3',
        'Codex người làm; Claude người phản biện chính thức',
        'D:/RCA-flashticket/AGENTS.md; docs/STATE.md; tasks/T-036-p5b-hop-dong-chung/SPEC.md và LOG.md; '
        'docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; '
        'docs/reference/sources/advisor-2026-09-23.md; nguồn và manifest tại results/T-036/nguon.json',
        'không có bản phản biện chính thức T-036 trước lượt này',
        'D:/RCA-flashticket/results/T-036/manifest.json; hop-dong.md; nguon.json; fixtures/; runs/; kiem-dung-dan.md; '
        'ban-giao.md; src/do_thi_tinh/README.md và code; results/T-035/manifest.json và các đầu vào SPEC liệt kê; '
        'Windows/PowerShell, Python theo README; diff phiên ở results/T-036/runs/ket-phien-001/changes.diff',
        'chỉ đọc và trả lời trong chat; chưa có quyền ghi REVIEW, LOG, STATE, SPEC, code hoặc kết quả',
    ]
    assert len(placeholders) == len(values)
    for placeholder, value in zip(placeholders, values):
        common = common.replace(placeholder, value, 1)
    prompt = '\n\n'.join([common, block('### Soát kết quả'), block('### G3 — Khóa thiết kế trước khi mở test')]) + '\n'
    (BASE / 'prompt-claude.txt').write_text(prompt, encoding='utf-8')
    save(OUT / 'prompt-check.json', dict(common_metadata_fields=len(placeholders),
         stage_exact=block('### Soát kết quả') in prompt,
         gate_exact=block('### G3 — Khóa thiết kế trước khi mở test') in prompt,
         template_sha256=digest(ROOT / 'docs/review-prompt.md'), no_remaining_placeholders=not re.search(r'<[^>]+>', prompt)))
    state = ROOT / 'docs/STATE.md'
    old_state = state.read_bytes()
    old_log = (TASK / 'LOG.md').read_bytes()
    (OUT / 'STATE-before.md').write_bytes(old_state)
    (OUT / 'LOG-before-final.md').write_bytes(old_log)
    text = old_state.decode('utf-8-sig')
    lines = text.splitlines(keepends=True)
    matched = [i for i, line in enumerate(lines) if line.startswith('| T-036 |')]
    assert len(matched) == 1
    i = matched[0]
    parts = lines[i].split('|')
    parts[6] = (' Chờ Claude phản biện kết quả (15/10/2026). Codex đã tự soát từ nguồn và triển khai trong SPEC; '
                'báo cáo/manifest tại results/T-036/, LOG Phiên 2 và prompt-claude.txt. '
                'Mô tả T-036 ở mục Task đang mở là mốc trước triển khai; hiện trạng theo dòng này. '
                'Chưa nghiệm thu, đóng task hoặc chọn P6. ')
    lines[i] = '|'.join(parts)
    state.write_bytes(''.join(lines).encode('utf-8'))
    endlog = f'''
**Hoàn tất implementation / tự soát:** bổ sung bảng mapping nút cô lập, loại cạnh nội bộ sau alias, phân biệt default exchange rỗng với thiếu, bảo toàn provenance/record membership và giữ source evidence khác runtime/RCA. Registry cập nhật revision cụ thể khi nguồn lưu chứng minh được; giữ 15 nguồn hiện hành, không nâng tree/code/dataset revision thành application deployment. Nguồn registry ban đầu giữ ở runs/chuan-bi-001/nguon-ban-dau.json. Kiểm tích hợp messaging dùng span tổng hợp qua T-035, không mở trace thô.

**Kết thúc Phiên 2:**
1. Đã tự soát SPEC độc lập từ nguồn, chưa phát hiện lỗi cần sửa SPEC; đã cài hợp đồng/registry, builder/comparator, oracle, kiểm, báo cáo và bàn giao. Đầu ra công cụ đạt các phản ví dụ đã kiểm; chưa có inventory/đối chiếu kiến trúc đủ ba hệ. T-036 chờ Claude phản biện, Minh nghiệm thu; tự soát không thay phản biện chính thức.
2. File thay đổi đúng quyền: results/T-036/; src/do_thi_tinh/__init__.py, build.py, compare.py, README.md; nối LOG này; chỉ dòng T-036 trong docs/STATE.md. SPEC không sửa. Giữ mọi thay đổi có sẵn. Không sửa T-035/platform/WHY/DECISIONS hoặc file task khác; không mở test, tải repo, bật EC2, dùng subagent, commit/push.
3. Kiểm: manifest đầu vào khớp; oracle literal có trước code; lượt cuối {final['passed']} kiểm đạt, 312 graph dev full/N/A đọc tương thích và 156 cặp chiếu khớp. Hai process seed khác cho trung gian giống từng byte; kết quả ở runs/kiem-004, kiem-005 và runs/ket-phien-001/determinism.json. Lượt cuối {seconds:.3f}s, RAM peak working set {ram:.1f}MiB; số gốc trong result.json. Giữ lượt lỗi kiem-001 (selector graph lịch sử), các lượt sau và snapshot mã hai lượt cuối. Kiểm cuối diff/phạm vi/manifest ở runs/ket-phien-001/final-verification.json; không chạy lại baseline hoặc trace thô.
4. Câu nguồn: cung cấp biểu diễn và phép so có điều kiện cho P5, chưa trả lời RQ3/RQ5, toàn P5b hoặc cơ chế RCA. OPEN: deployment/runtime FT; revision ứng dụng sinh TT/OB; nghĩa host/metadata ngày; độ đầy đủ telemetry; lựa chọn/lợi ích P6. Binding DB→instance được giữ ngoài cạnh trace; T-035 chưa có trường tương đương. ban-giao.md nêu phản ví dụ, phương án adapter/mapping cần trình, owner và quyết định phụ thuộc. Không coi thiếu bằng chứng là không thể làm hoặc tự loại nhóm khỏi nghiên cứu.

**Quyết định/bất đồng:** không có phản biện chính thức T-036 trước phiên này, không có bất đồng với Claude được kết luận thay. Không thêm quyết định khoa học. Quyền triển khai đã được Q-157/SPEC ghi, không tự sửa sổ. Minh quyết nghiệm thu hoặc bước sửa sau phản biện. Nội dung nên vào báo cáo: phân biệt nguồn/quan sát, logical DB/instance, địa chỉ messaging/metric shared và mẫu số có điều kiện, cùng giới hạn fixture/runtime.

**Bước tiếp chính xác:** Minh mở phiên Claude mới tại D:/RCA-flashticket, copy results/T-036/prompt-claude.txt (cũng dưới đây). Claude đọc nguồn/đầu ra/code trước các kết luận, kiểm độc lập theo mẫu. Phạm vi mặc định của prompt chỉ đọc/trả lời chat; ghi REVIEW cần Minh cấp đúng file lượt. Không tự gửi hoặc tự mở phiên. T-037–040 cần SPEC riêng sau hợp đồng được xem xét; không triển khai từ quyền T-036.

**Lệnh cuối của phiên:** py -3 -X utf8 -B results/T-036/finalize.py (tổng hợp và kiểm diff/phạm vi/manifest); lệnh kiểm hành vi cuối: & 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe' -X utf8 -B results/T-036/check.py kiem-005. Không chạy lại tên run cũ. Nếu phát hiện lỗi lúc tổng hợp, giữ kết quả lỗi và trình đúng phạm vi; không sửa SPEC.

**Đề xuất nội dung commit, chưa thực hiện:** feat: add sourced static graph contract and trace comparison for T-036. Minh yêu cầu không commit/push trong phiên này; không thực hiện.

### Prompt Claude — soát kết quả (Minh chuyển thủ công)

```text
{prompt}```
'''
    with (TASK / 'LOG.md').open('a', encoding='utf-8', newline='') as f:
        f.write(endlog)
    assert (TASK / 'LOG.md').read_bytes().startswith(old_log)
    new_lines = state.read_text(encoding='utf-8').splitlines()
    old_lines = old_state.decode('utf-8-sig').splitlines()
    assert [j for j, (a, b) in enumerate(zip(old_lines, new_lines)) if a != b] == [i]
    assert len(new_lines) == len(old_lines)
    protected = []
    for path, expected in preflight['protected_hashes'].items():
        protected.append(dict(path=path, unchanged=digest(ROOT / path) == expected))
    assert all(x['unchanged'] for x in protected)
    # Tracked diff ngoài đúng STATE phải giữ nguyên nội dung đầu phiên.
    def outside_state(diff):
        return ''.join(part for part in re.split(r'(?=^diff --git )', diff, flags=re.M)
                       if not part.startswith('diff --git a/docs/STATE.md b/docs/STATE.md'))
    old_diff = (BASE / 'runs/chuan-bi-001/tracked-before.diff').read_text(encoding='utf-8')
    current_diff = git('diff', '--binary')
    assert outside_state(old_diff) == outside_state(current_diff), 'outside_scope_tracked_diff_changed'
    before_status = preflight['git_status_before'].splitlines()
    after_status = git('status', '--porcelain').splitlines()
    prefixes = ['results/T-036/', 'src/do_thi_tinh/', 'tasks/T-036-p5b-hop-dong-chung/', 'docs/STATE.md']
    def outside_status(lines):
        return [line for line in lines if not any(line[3:].startswith(prefix) for prefix in prefixes)]
    assert outside_status(before_status) == outside_status(after_status), 'outside_scope_status_changed'
    # Diff đầy đủ file mới: base rỗng; STATE/LOG so phần của phiên đã lưu.
    source_files = [ROOT / 'src/do_thi_tinh' / p for p in ['__init__.py', 'build.py', 'compare.py', 'README.md']]
    artifact_files = sorted(p for p in BASE.rglob('*') if p.is_file())
    change_text = ''
    for path in source_files + artifact_files:
        if path.suffix not in {'.py', '.md', '.txt', '.json', '.jsonl'}:
            continue
        if path.is_relative_to(OUT) or '/runs/' in path.as_posix():
            continue
        change_text += ''.join(difflib.unified_diff([], path.read_text(encoding='utf-8').splitlines(True),
                              fromfile='/dev/null', tofile=path.relative_to(ROOT).as_posix()))
    change_text += ''.join(difflib.unified_diff(old_lines, new_lines, fromfile='STATE-before', tofile='docs/STATE.md', lineterm='\n'))
    change_text += ''.join(difflib.unified_diff(old_log.decode('utf-8').splitlines(True),
                          (TASK/'LOG.md').read_text(encoding='utf-8').splitlines(True),
                          fromfile='LOG-before-final', tofile='tasks/T-036-p5b-hop-dong-chung/LOG.md'))
    (OUT / 'changes.diff').write_text(change_text, encoding='utf-8')
    subprocess.run(['git', '-C', str(ROOT), 'diff', '--check'], check=True)
    source_checks = []
    for source in read(BASE/'nguon.json')['sources']:
        p = Path(source['path']); p = p if p.is_absolute() else ROOT / p
        source_checks.append(dict(source=source['id'], ok=digest(p) == source['sha256']))
    assert all(x['ok'] for x in source_checks)
    assert all(digest(ROOT/path) == expected for path, expected in preflight['manifest_hashes'].items())
    save(OUT / 'final-verification.json', dict(
        protected=protected, sources=source_checks, state_only_task_row=True, log_append_only=True,
        outside_tracked_diff_unchanged=True, outside_git_status_unchanged=True,
        spec_unchanged=digest(TASK/'SPEC.md') == preflight['spec_sha256'],
        dependency_manifests_unchanged=True, diff_check=True,
        prompt_template_exact=True, determinism=True, test_pass=True,
        current_checks=final['passed'], failed_checks=final['failed'],
        current_run='runs/kiem-005', historical_failed_runs_retained=['runs/kiem-001'],
        state_sha256=digest(state), log_sha256=digest(TASK/'LOG.md'),
        final_status='awaiting_official_review_and_Minh_acceptance', commit_push=False,
        note='STATE phần diễn giải ngoài dòng T-036 giữ nguyên theo quyền; dòng task ghi rõ mốc hiện hành'))
    files = source_files + sorted(p for p in BASE.rglob('*') if p.is_file() and p != BASE/'manifest.json')
    records = [dict(path=p.relative_to(ROOT).as_posix(), bytes=p.stat().st_size, sha256=digest(p)) for p in files]
    save(BASE / 'manifest.json', dict(task='T-036', schema_version=1, created_utc=datetime.now(timezone.utc).isoformat(),
        files=records, count=len(records), total_bytes=sum(r['bytes'] for r in records),
        excludes='manifest self; append-only LOG and STATE hashes in final-verification',
        final_verification='runs/ket-phien-001/final-verification.json',
        source_registry='nguon.json', spec_sha256=preflight['spec_sha256'],
        input_manifests=preflight['manifest_hashes'], decision_state_changes=[],
        state='awaiting_official_review_and_Minh_acceptance', tests_opened=False, commit_push=False))
    assert all(digest(ROOT/r['path']) == r['sha256'] for r in records)
    print(json.dumps(dict(ok=True, artifacts=len(records), bytes=sum(r['bytes'] for r in records),
                          passed=final['passed'], prompt=str(BASE/'prompt-claude.txt'))))


if __name__ == '__main__':
    main()
