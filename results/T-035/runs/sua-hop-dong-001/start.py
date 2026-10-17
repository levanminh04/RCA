"""Ghi nguồn quyền và bản trước của gói sửa hợp đồng đã duyệt."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
ALLOWED = [
    'src/do_thi/builder.py', 'src/do_thi/README.md',
    'results/T-035/dac-ta-do-thi.md', 'results/T-035/kiem-dung-dan.md',
    'results/T-035/thong-ke-do-thi.md', 'results/T-035/scripts/write_docs.py',
    'results/T-035/manifest.json', 'docs/WHY.md', 'docs/DECISIONS.md',
    'tasks/T-035-p5-do-thi-tu-trace/LOG.md', 'docs/STATE.md',
]
APPROVAL = 'duyệt sửa trong phiên này luôn, sau khi sửa, tạo 1 prompt cho phiên codex sạch mới review lại 035 1 lần nữa , phiên này review lại như lần đầu không neo theo những phần đã có tránh anchor'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text('utf-8'))


def write(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def main():
    assert not (BASE / 'preflight.json').exists()
    manifest = read(ROOT / 'results/T-035/manifest.json')
    for item in manifest['files']:
        p = ROOT / item['path']
        assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], item['path']
    upstream = read(ROOT / 'results/T-035/runs/sua-n1-001/input-verification.json')
    for item in upstream['checks']:
        assert sha(ROOT / item['path']) == item['expected'], item['path']
    for item in upstream['governing']:
        assert sha(ROOT / item['path']) == item['sha256'], item['path']
    snapshot = {}
    for folder in ['src', 'docs', 'tasks', 'results/T-035']:
        for p in (ROOT / folder).rglob('*'):
            if p.is_file() and BASE not in p.parents and '__pycache__' not in p.parts:
                snapshot[p.relative_to(ROOT).as_posix()] = {'sha256': sha(p), 'bytes': p.stat().st_size}
    for name in ALLOWED:
        p = BASE / 'before' / name
        p.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, p)
    review = Path('C:/Users/84583/.codex/attachments/528b2260-3900-4a45-844f-36f07b4c62dc/Pasted text.txt')
    shutil.copyfile(review, BASE / 'nhan-xet-duoc-minh-chuyen.txt')
    write(BASE / 'input-verification.json', {'checks': upstream['checks'], 'governing': upstream['governing'],
                                            'previous_manifest': 'before/results/T-035/manifest.json',
                                            'previous_artifacts_verified': len(manifest['files']), 'pass': True})
    write(BASE / 'preflight.json', {'created_utc': datetime.now(timezone.utc).isoformat(),
          'classification': 'EXECUTE', 'approval': APPROVAL, 'decision': 'Q-155',
          'allowed_files': ALLOWED, 'allowed_new_directory': BASE.relative_to(ROOT).as_posix(),
          'files': snapshot, 'HEAD': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
          'git_status': subprocess.check_output(['git', 'status', '--short'], cwd=ROOT, text=True, encoding='utf-8'),
          'previous_manifest_sha256': sha(BASE / 'before/results/T-035/manifest.json'),
          'previous_artifacts_verified': len(manifest['files']), 'upstream_checks': len(upstream['checks'])})
    (BASE / 'de-xuat-da-duyet.txt').write_text('''Gói sửa được Minh duyệt ngay sau đề xuất trong chat:
1. builder.py: tên thiếu về None; từ chối va chạm giữa ID thực thể/component và ID thao tác trước dựng/chiếu; kiểm miền thời gian và tràn int64 trước ép/cộng/nhân; từ chối kiểu đã biết mâu thuẫn, không hạ kiểu đã biết thành unknown.
2. README, đặc tả, kiểm đúng đắn, báo cáo, script sinh tài liệu và manifest cập nhật theo bằng chứng mới.
3. Nối WHY, DECISIONS, LOG; chỉ dòng T-035 trong STATE. Mọi đầu ra mới, fixture literal trước code, bản trước/sau và prompt nằm trong runs/sua-hop-dong-001/.
4. Kiểm fixture cũ/mới và hồi quy đủ dev, ước lượng 40–50 phút, giữ mọi lượt. Không sửa SPEC, baseline, FlashTicket; không mở test hoặc commit/push.
5. Sau sửa soạn prompt Codex sạch soát toàn T-035 từ nguồn gốc như lần đầu, nhận xét độc lập trước lịch sử. Không đổi vai trò chính thức, không tự mở/gửi phiên.
Lời duyệt nguyên văn: ''' + APPROVAL + '\n', 'utf-8')
    decisions = ROOT / 'docs/DECISIONS.md'
    assert '| Q-155 |' not in decisions.read_text('utf-8')
    with decisions.open('a', encoding='utf-8') as f:
        f.write(f'\n| Q-155 | 15/10/2026 | “{APPROVAL}” | Minh duyệt gói sửa bốn lỗi hợp đồng T-035 sau lượt tự soát Codex sạch. Phạm vi và bản đề xuất tại results/T-035/runs/sua-hop-dong-001/de-xuat-da-duyet.txt và preflight.json. Gồm fixture, hồi quy dev, tài liệu, prompt Codex sạch soát toàn task từ nguồn trước lịch sử. Giữ vai trò Codex người làm, Claude phản biện chính thức; chưa nghiệm thu, không mở test hoặc commit/push. |\n')
    with (ROOT / 'docs/WHY.md').open('a', encoding='utf-8') as f:
        f.write('''
### Bổ sung WHY-52 — Chuẩn hóa dữ liệu thiếu, miền ID và chính sách lỗi đầu vào (15/10/2026, Q-155)

- **Chọn:** tên thao tác thiếu ở dtype pandas khác nhau đều về None trước tạo khóa. Giữ ID hiện hành và từ chối rõ va chạm giữa miền ID thực thể/component với ID thao tác; kiểm cả dựng và API project. Thời gian phải không âm, nguyên và biểu diễn được an toàn trong int64 nanosecond trước ép/cộng/nhân. Kiểu unknown không thay kiểu đã biết; hai kiểu đã biết khác nhau bị từ chối, không chọn theo thứ tự dòng.
- **Vì sao:** đặc tả đã hứa giữ tên null, địa chỉ đúng thực thể và từ chối thời gian sai; DT18-NV2 cần nút/cạnh phản ánh đúng thành phần. Phản ví dụ nhỏ đã tái lập lỗi dtype, đổi/mất đích cạnh, wrap thời gian và kiểu phụ thuộc thứ tự. Đây là sửa cài đặt/hợp đồng kỹ thuật, không là hạn chế RCA của dataset hoặc bằng chứng lợi ích đồ thị.
- **Phương án khác:** thêm namespace vào mọi ID sẽ hỗ trợ va chạm nhưng đổi địa chỉ/schema và toàn đầu ra hợp lệ; chọn từ chối minh bạch trong gói sửa tối thiểu đã duyệt. Không suy loại đích từ chuỗi ID. Bỏ kiểm thời gian hoặc chọn kiểu cuối cùng che đầu vào mâu thuẫn. Dùng một hàm project để kiểm chính nó không đủ phát hiện lỗi chung; oracle mới phải ghi đích literal độc lập.
- **Bằng chứng / chưa kiểm khi viết:** nhận xét Minh chuyển được lưu nguyên văn tại runs/sua-hop-dong-001/nhan-xet-duoc-minh-chuyen.txt. Thiết kế và oracle mới sẽ ghi trước code. Phương án sửa và hồi quy chưa chạy; dự kiến dữ liệu hợp lệ giữ nguyên phải được kiểm, chưa được dùng như kết quả.
- **Điều kiện thất bại / hệ quả:** nguồn cần dùng ID va chạm bị từ chối rõ; muốn hỗ trợ phải trình đổi namespace riêng. Metadata kiểu mâu thuẫn cần chủ nguồn xác minh, không xác định kiểu nào đúng. Quyền nhận trọn bộ dựng, K1/K5/K7 và bàn giao T-036/P9 phụ thuộc kết quả; không tự trả lời RQ3, xác nhận runtime FlashTicket, chọn P6 hoặc đóng task.
''')
    with (ROOT / 'tasks/T-035-p5-do-thi-tu-trace/LOG.md').open('a', encoding='utf-8') as f:
        f.write('''
## Phiên 8 — 15/10/2026 — Codex — LEVANMINH — Người làm

**Mở phiên / quyền:** EXECUTE theo lời Minh Q-155; sửa bốn lỗi hợp đồng đã trình, fixture có đáp án trước code, hồi quy đủ dev và prompt Codex sạch soát toàn T-035 như lượt đầu. Giữ Claude phản biện chính thức, không sửa SPEC. Phạm vi đúng preflight.json và de-xuat-da-duyet.txt trong runs/sua-hop-dong-001/.

**Kiểm trước sửa:** toàn bộ 4.310 artifact ở manifest trước và 362 mục nguồn khớp; AGENTS/SPEC/B13/B16 giữ hash nguồn. Bản trước của 11 file đã được giữ. Nhận xét và quyền được lưu; WHY ghi lựa chọn và phần chưa kiểm trước dùng. Bước tiếp: thiết kế/oracle literal, ghi hash trước code, sửa bộ dựng, kiểm fixture/đối chứng, chạy hồi quy và đối chiếu.
''')
    state = ROOT / 'docs/STATE.md'
    lines = state.read_text('utf-8').splitlines()
    row = '| T-035 | P5a: đặc tả đồ thị phụ thuộc và bộ dựng từ trace | P5 (G3) | Codex | Claude | Đang sửa bốn lỗi hợp đồng và kiểm hồi quy theo Q-155 (15/10/2026); giữ kết quả cũ. Đầu ra và nhật ký tại runs/sua-hop-dong-001/, LOG Phiên 8. Chưa nghiệm thu/đóng task. | `tasks/T-035-p5-do-thi-tu-trace/` |'
    assert sum(x.startswith('| T-035 |') for x in lines) == 1
    state.write_text('\n'.join(row if x.startswith('| T-035 |') else x for x in lines) + '\n', 'utf-8')
    print(json.dumps({'pass': True, 'decision': 'Q-155', 'old_artifacts': len(manifest['files']),
                      'source_checks': len(upstream['checks']), 'approved_files': len(ALLOWED)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
