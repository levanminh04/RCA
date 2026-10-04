"""T-013 owned-document polish, read-only adapter check, and handoff."""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

ROOT = Path('D:/RCA-flashticket')
OUT = ROOT / 'results/T-013'
TASK = ROOT / 'tasks/T-013-ho-so-baro'
WORK = Path('D:/RCA-ext/work/T-013')
REQUEST = Path('C:/Users/84583/.codex/attachments/2f6c5735-a241-4299-bd8c-25d4034a97de/Pasted text.txt')


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def correct_inline_math(text):
    # Find the opening parenthesis paired with each existing escaped close.
    # Add the missing opening escape; retain nested ordinary parentheses.
    pos = 0
    while True:
        end = text.find('\\)', pos)
        if end < 0:
            return text
        depth = 0
        start = end - 1
        while start >= 0 and text[start] != '\n':
            if text[start] == ')':
                depth += 1
            elif text[start] == '(':
                if depth == 0:
                    break
                depth -= 1
            start -= 1
        if start >= 0 and text[start] == '(' and (start == 0 or text[start - 1] != '\\'):
            text = text[:start] + '\\' + text[start:]
            end += 1
        pos = end + 2


def polish():
    replacements = {
        'trong30ca': 'trong 30 ca', 'trên90 baseline': 'trên 90 baseline',
        '30ca': '30 ca', '90ca': '90 ca', '100ca': '100 ca', '25 ca': '25 ca',
        'hai caT': 'hai ca T', 'caTT': 'ca TT', 'quy môTT': 'quy mô TT',
        'tậpOB': 'tập OB', 'fullTT': 'full TT', 'fullOB': 'full OB',
        'OBfull': 'OB full', 'TTprefix': 'TT prefix',
        'củaauth': 'của auth', 'tạiroot': 'tại root', 'ởcartservice': 'ở cartservice',
        'mẫuREADME': 'mẫu README', 'Top5': 'Top 5', 'top5': 'top 5',
        'ký10': 'ký 10', 'cadence1s': 'cadence 1 s',
        'thực0.256': 'thực 0.256', 'toàn0.256': 'toàn bộ 0.256', 'của0.256': 'của 0.256',
        'Chênh0.26': 'Chênh 0.26', 'điểm243': 'điểm 243', 'tại243': 'tại 243',
        'injection360': 'injection 360', 'điểm120': 'điểm 120', 'lấy120': 'lấy 120',
        'prefix120': 'prefix 120', 'prefix cố định≤120': 'prefix cố định ≤120',
        'từ12điểm': 'từ 12 điểm', 'toànbộ': 'toàn bộ',
        'dữ liệu0..T−1': 'dữ liệu 0..T−1', 'ngoài0..119': 'ngoài 0..119',
        'trongrange': 'trong range', 'gầnbiên': 'gần biên', 'lỗiindex': 'lỗi index',
        'chỉ số dòng': 'chỉ số dòng', 'list[108,100]': 'list [108,100]',
        'cột[100,108]': 'cột [100,108]', 'normal200điểm': 'normal 200 điểm',
        'có0alarm': 'có 0 alarm', 'rawshort≤100': 'raw short ≤100',
        'nhất0.': 'nhất 0.', 'vẫn córank': 'vẫn có rank', 'rankinvariance': 'rank invariance',
        'thành0': 'thành 0', 'thành1': 'thành 1', 'hàng0': 'hàng 0',
        'vị trí0': 'vị trí 0', 'còn0': 'còn 0', 'riêng std': 'riêng std',
        'warm-up': 'warm-up', 'hazard250': 'hazard 250',
        'phần0..T−1': 'phần 0..T−1', 'giảm1': 'giảm 1', 'hơn1': 'hơn 1',
        'lấy300': 'lấy 300', 'cắt300': 'cắt 300', 'trước+300': 'trước +300',
        'trước300': 'trước 300', 'window600': 'window 600',
        'có100 ca': 'có 100 ca', 'OB ở': 'OB ở', 'được((0.02,0.98)': 'được ((0.02,0.98)',
        'là0.02': 'là 0.02', 'là0.98': 'là 0.98', 'dùng8(': 'dùng 8(',
        'Recall1': 'Recall = 1', 'Recall là': 'Recall là',
        'R=1': 'R = 1', 'R luôn1': 'R luôn bằng 1', 'TP100/FP31': 'TP=100/FP=31',
        'dict có thể0': 'dict có thể 0', 'scale1': 'scale = 1', 'IQR0': 'IQR = 0',
        'IQR thật1': 'IQR thật bằng 1', 'IQR thật0': 'IQR thật bằng 0',
        'IQRthô90baseline': 'IQR thô trên 90 baseline',
        'baseline300dòng': 'baseline 300 dòng', 'bằng0': 'bằng 0', '90/90ca': '90/90 ca',
        'điểmT': 'điểm T', 'ngoài chuỗi': 'ngoài chuỗi', 'điểm600': 'điểm 600',
        'có điểm600': 'có điểm 600', 'ở100/100ca': 'ở 100/100 ca', 'ở99/100ca': 'ở 99/100 ca',
        'có alarm làTP': 'có alarm là TP', 'injection thêmFP': 'injection thêm FP',
        'vừaTP vừaFP': 'vừa TP vừa FP', 'củaMRP': 'của MRP',
        'k3': 'k=3', 'ddof0': 'ddof=0', 'ddof1': 'ddof=1', 'std0': 'std=0',
        'range0': 'range=0', 'chuỗi≤100': 'chuỗi ≤100', 'alarm108': 'alarm 108',
        'alarm100': 'alarm 100', 'chế độb': 'chế độ (b)', 'chế độ(b)': 'chế độ (b)',
        'b-online': '(b) online', 'b-hồi-cứu': '(b) hồi cứu',
        'T-007100OB': 'T-007: 100 ca OB', 'kịch bản30ca': 'kịch bản 30 ca',
        'vượt1h': 'vượt 1 giờ', 'lượt>1h': 'lượt >1 giờ', 'dừng1h': 'dừng sau 1 giờ',
        '600điểm': '600 điểm', '24phút': '24 phút', 'T1441': 'T=1441',
        'T600': 'T=600', 'T1441': 'T=1441', '15.864MiB': '15.864 MiB',
        'điểm;': 'điểm;', 'Đợt1': 'Đợt 1', 'taskT-013': 'task T-013',
        'resultsT-013': 'results T-013', 'workT-013': 'work T-013',
        'cửa sổP3': 'cửa sổ P3', 'protocolG1': 'protocol G1', 'mappingG1': 'mapping G1',
        'mốcA': 'mốc A', 'phân tíchP4': 'phân tích P4', 'protocolP3': 'protocol P3',
        'trongT-013': 'trong T-013', 'chờWHY': 'chờ WHY', 'từngca': 'từng ca',
        'Hồ sơ9mục': 'Hồ sơ 9 mục', 'Window và3leak paths': 'Window và 3 leak paths',
        'CSV/filebắtbuộc': 'CSV/file bắt buộc', 'csv16cột': 'csv 16 cột',
        '.csv16cột': '.csv 16 cột', 'mởphiênHEAD': 'mở phiên HEAD', 'khối task': 'khối task',
        'dòngT013': 'dòng T-013', 'reviewerClaude': 'reviewer Claude',
        'taskcũ/common ngoài1dòng': 'task cũ/common ngoài 1 dòng',
        'đối chiếu': 'đối chiếu', '≤2.23e-16': ' ≤2.23e-16',
        'NaN/inf/hằng/hòa/đơnvị/têncột/nềnngắn/prior/hazard/biên/normalcontrol':
            'NaN/inf/hằng/hòa/đơn vị/tên cột/nền ngắn/prior/hazard/biên/normal control',
    }
    for p in sorted(OUT.glob('*.md')):
        old = p.read_text(encoding='utf-8-sig')
        text = correct_inline_math(old)
        for a, b in replacements.items():
            text = text.replace(a, b)
        if text != old:
            p.write_text(text, encoding='utf-8')
    print('Owned Markdown readability and inline math corrected; no scientific values changed.')


def check_adapter():
    import numpy as np
    import pandas as pd
    meta = json.loads((WORK / 'metrics-selected.json').read_text(encoding='utf-8'))
    source = Path(meta['source'])
    frame = pd.read_parquet(source)
    with np.load(WORK / 'metrics-selected.npz', allow_pickle=False) as saved:
        assert frame.columns.tolist() == saved['columns'].tolist()
        assert np.array_equal(frame.to_numpy(), saved['values'], equal_nan=True)
        shape = list(saved['values'].shape)
    assert hashlib.sha256(source.read_bytes()).hexdigest() == meta['source_sha256']
    assert hashlib.sha256((WORK / 'metrics-selected.npz').read_bytes()).hexdigest() == meta['output_sha256']
    result = {'status': 'pass', 'source': str(source), 'shape': shape,
              'all_columns_equal': True, 'all_values_equal_including_nan': True,
              'source_hash_unchanged': True, 'adapter_output_hash_unchanged': True}
    dump(OUT / 'trung-gian/kiem-adapter.json', result)
    print(json.dumps(result, ensure_ascii=False))


def finalize():
    log_path = TASK / 'LOG.md'
    log = log_path.read_text(encoding='utf-8')
    assert '## Kết thúc phiên — bàn giao T-013' not in log
    request = REQUEST.read_text(encoding='utf-8-sig')
    task_block = re.search(r'^<task>\r?\n.*?^</task>', request, re.M | re.S).group(0)
    now = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
    correction = f'''\n- {now} — tự kiểm bàn giao: parse và cơ chế đạt; chuẩn hóa cách trình bày, kiểm lại adapter từng giá trị. Không có gói mới, không sửa nguồn/env.\n
## Đính chính nhật ký trước bàn giao (chỉ ghi thêm)

- Khối task ở mục mở phiên lấy nhầm lần xuất hiện `<task>` trong câu hướng dẫn, nên có dư phần trước khối thật. Bản đúng nguyên văn ở dưới; nội dung task khoa học không đổi.
- Lỗi chép bảng mốc T-013: dòng RobustScorer[t_inject] được đính chính bằng Table 3 bài gốc. Bản trước sửa giữ tại `results/T-013/runs/moc-truoc-dinh-chinh.json`; bản hiện hành `doi-chieu-moc.json`. Không có phép đo hoặc lựa chọn tham số dựa trên ô chép nhầm.
- Các lượt hỏng được giữ: mở phiên đã ghi file thành công nhưng print gặp encoding; lượt cơ chế đầu thiếu Parquet engine; lượt kế thiếu file mốc trong T-005 (đã dùng metadata dev T-002); lượt tính chính hoàn tất rồi lỗi pip freeze (uv venv không có pip); lần viết ví dụ đầu dùng path tương đối (đã sửa resolve). Không bỏ lượt hỏng hoặc chạy lại các phần đã có đầu ra hợp lệ. Console/progress/failure và scripts trong danh sách file bàn giao.

**Khối task đúng nguyên văn, thay cho bản trích dư ở đầu LOG:**

```text
{task_block}
```
'''
    with log_path.open('a', encoding='utf-8', newline='') as f:
        f.write(correction)

    # Paths only: including this script and the predictable verification output
    # avoids cyclic hashes or a moving prompt list.
    paths = sorted(str(p.relative_to(ROOT)).replace('\\', '/') for p in OUT.rglob('*') if p.is_file())
    inventory_name = 'results/T-013/danh-sach-file.json'
    if inventory_name not in paths:
        paths.append(inventory_name)
    paths = sorted(paths)
    task_paths = ['tasks/T-013-ho-so-baro/SPEC.md', 'tasks/T-013-ho-so-baro/LOG.md']
    external = sorted(str(p).replace('\\', '/') for p in WORK.rglob('*') if p.is_file())
    assert external == ['D:/RCA-ext/work/T-013/metrics-selected.json', 'D:/RCA-ext/work/T-013/metrics-selected.npz']
    inventory = {'task_outputs': task_paths, 'result_outputs': paths, 'external_outputs': external,
                 'shared_mutation': 'docs/STATE.md: exactly the T-013 row',
                 'other_agents_changes': 'Not owned by T-013; not edited or included as our outputs.'}
    dump(OUT / 'danh-sach-file.json', inventory)

    report = '''A. Đã làm: hoàn thành ba hồ sơ chín mục cho BARO (kèm N-Sigma RCA), BOCPD và N-Sigma phát hiện; ví dụ độc lập trên một ca dev RE2-TT và một ca OB; giải thích cửa sổ, chế độ (b), so hai code và đủ CSV đầu vào/ca chạy.

B. File đã thay đổi: `tasks/T-013-ho-so-baro/SPEC.md`, `LOG.md`, toàn bộ đầu ra `results/T-013/` và đúng dòng T-013 trong `docs/STATE.md`. Ngoài repo: `D:/RCA-ext/work/T-013/metrics-selected.npz` và `metrics-selected.json`. Danh sách từng file ở `results/T-013/danh-sach-file.json` và prompt dưới. Không sửa task cũ, tài liệu chung khác, source hay môi trường. Không commit/push.

C. Kiểm tra đã chạy và kết quả: 131 phép kiểm cơ chế; điểm độc lập khớp official, sai số normalized lớn nhất 0; posterior BOCPD sai số tối đa 2.23e-16; top 5 metric mẫu README khớp. Đã kiểm lặp lại, đảo cột, normal-normal và các ca biên. Đảo cột giữ điểm nhưng có thể đổi rank khi hòa; list N-Sigma theo thứ tự cột; hai prefix BOCPD chỉ trả sentinel ngoài range. Những hành vi này được báo rõ, không gọi là PASS nghiệp vụ. Parse mọi file, CSV 16 cột/6 dòng, adapter mọi giá trị, source HEAD/status và diff kiểm sạch trong phạm vi; chi tiết `kiem-tra.json`, `kiem-ban-giao.json`.

D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM: năm điểm D1–D5 trong `dinh-chinh-task-cu.md`: K1 chưa tách công thức bài/code và đơn vị chấm; T-006 suy IQR=0 từ scale=1; T-007 chưa giới hạn “chạy đúng” khi có sentinel; T-006 nói Recall luôn 1 thiếu điều kiện; T-001 cần tách RAM ma trận khỏi tổng chi phí. Đã bổ sung script, phản ví dụ và số kiểm trong T-013. IQR thô xác nhận 90/90 baseline; loại riêng sentinel không đổi P/R/F1 tập OB cũ. Chưa có bằng chứng phải đổi các số tái lập cũ; không sửa file task cũ.

E. Chỗ lệch khỏi SPEC và lý do: dùng môi trường py312 sẵn có chỉ đọc Parquet rồi NPZ vì pin thiếu engine; phương pháp vẫn chạy môi trường ghim. Dùng metadata dev T-002 vì ca chọn không có trong metadata T-005; lấy metadata môi trường bằng uv vì venv không có pip. Đã ghi các thay đổi ở cuối SPEC, giữ lượt hỏng. Lỗi chép bảng mốc và trích khối task của T-013 đã đính chính, giữ dấu vết; không đổi rule ca hoặc cấu hình theo kết quả.

F. Đề xuất cho tài liệu chung: nháp DECISIONS về ủy quyền, WHY về quy tắc ví dụ/cách đối chiếu, K1 về công thức và đơn vị độ đo, cùng đoạn sửa tối thiểu D1–D5 trong `de-xuat-tai-lieu-chung.md`. Chưa ghi vào nguồn chung.

G. Phần chưa kiểm và lý do: BOCPD full TT vượt giới hạn một giờ đã thấy ở T-005; benchmark toàn tập/ảnh hưởng bản sửa extraction thuộc gói sau; cấu hình thực nghiệm tác giả chưa đủ để phân xử mọi sai lệch bảng; chế độ (b) hợp lệ và runtime chính thức cần protocol G1/recording độc lập lỗi và máy rảnh. Giả định, trường hợp sai và cách kiểm tiếp ở `doi-chieu-tieu-chi.md`. Không để phép kiểm rẻ trong phạm vi thành “chờ quyền”.

H. Cần Minh quyết: phản biện độc lập bằng Claude; việc đưa các nháp vào tài liệu chung; cửa sổ Q-54, protocol hồi cứu/online và cách xử lý các sai lệch code khi tổng hợp G1. T-013 không tự chốt các lựa chọn này.
'''
    common_source = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8')
    common = common_source.split('## Prompt chung', 1)[1].split('```text\n', 1)[1].split('```', 1)[0]
    g1 = common_source.split('**G1 — phương pháp, dataset, cách chia:**', 1)[1].split('```text\n', 1)[1].split('```', 1)[0]
    file_list = '\n' + '\n'.join('- ' + p for p in task_paths + paths + external)
    prompt = common.replace('<T-xxx>', 'T-013').replace('<T-xxx-tên>', 'T-013-ho-so-baro')
    prompt = prompt.replace('<danh sách>', file_list).replace('<commit gốc>', '93f13d4c4a966428177e2acc287d96bc89303e92')
    command = "$env:PYTHONIOENCODING='utf-8'; $env:PYTHONDONTWRITEBYTECODE='1'; & D:/RCA-ext/envs/py312-pin/Scripts/python.exe results/T-013/scripts/kiem_ban_giao.py"
    ending = f'''\n## Kết thúc phiên — bàn giao T-013

1. **Đã làm gì:** báo cáo A dưới đây; đối chiếu toàn bộ tiêu chí ở `doi-chieu-tieu-chi.md`.
2. **File đã thay đổi:** báo cáo B và danh sách đủ ở `danh-sach-file.json`/prompt dưới; ngoài repo đúng hai file adapter.
3. **Kiểm tra đã chạy và kết quả:** báo cáo C; kiểm bàn giao cuối được chạy lại sau khi ghi prompt và cập nhật STATE.
4. **Điều chưa chắc hoặc cần Minh quyết:** báo cáo G–H; nháp F chưa là quyết định.
5. **Bước tiếp theo chính xác:** Minh mở phiên Claude Code mới trong `D:/RCA-flashticket`, dán toàn bộ prompt cuối LOG; Claude đọc SPEC/LOG/danh sách file và chỉ ghi `tasks/T-013-ho-so-baro/REVIEW.md`. Người làm chưa sửa theo review khi Minh chưa quyết.
6. **Lệnh cuối cùng đã chạy để kiểm bàn giao:** `{command}`. Không chạy phương pháp lại. Trạng thái T-013: chờ phản biện (04/10/2026).

### Báo cáo cuối A–H

{report}

## Prompt phản biện cho Claude

```text
{prompt.rstrip()}

{g1.rstrip()}
```
'''
    with log_path.open('a', encoding='utf-8', newline='') as f:
        f.write(ending)

    state_path = ROOT / 'docs/STATE.md'
    old_row = '| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | đang làm (04/10/2026) | `tasks/T-013-ho-so-baro/` |'.encode('utf-8')
    new_row = old_row.replace('đang làm'.encode('utf-8'), 'chờ phản biện'.encode('utf-8'))
    with state_path.open('r+b') as f:
        before = f.read()
        assert before.count(old_row) == 1
        offset = before.index(old_row)
        # Read again immediately before the exact-row write.
        f.seek(0)
        assert f.read() == before
        f.seek(offset)
        f.write(new_row + before[offset + len(old_row):])
        f.truncate()
        f.flush()
    after = state_path.read_bytes()
    assert after == before.replace(old_row, new_row, 1)
    print(json.dumps({'handoff': 'written', 'result_file_count': len(paths),
                      'external_files': external, 'state_other_bytes_unchanged': True}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--polish', action='store_true')
    parser.add_argument('--adapter-check', action='store_true')
    args = parser.parse_args()
    if args.polish:
        polish()
    elif args.adapter_check:
        check_adapter()
    else:
        finalize()
