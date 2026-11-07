"""Record the approved preparation scope and preserve the original bytes."""
from pathlib import Path
import hashlib
import json

RUN = Path(__file__).resolve().parent
ROOT = RUN.parents[3]
TASK = "tasks/T-054-khoa-g3-chay-p7-a"
FILES = [f"results/T-054/scripts/{name}.py" for name in
         ("p7", "nguon", "dieu_phoi", "cham", "fixtures")]
FILES += [f"{TASK}/SPEC.md", f"{TASK}/LOG.md", "docs/STATE.md",
          "docs/DECISIONS.md", "docs/WHY.md", "results/T-054/ho-so-g3.md",
          "results/T-054/runbook.md"]


def append(path, text):
    with path.open("ab") as stream:
        stream.write(("\n" + text.strip() + "\n").encode("utf-8"))


def main():
    pins = {}
    for name in FILES:
        data = (ROOT / name).read_bytes()
        target = RUN / "before" / name
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as stream:
            stream.write(data)
        pins[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    permission = {
        "user": "Duyệt chuẩn bị 013 và chốt D1–D4/R3 theo đề xuất trên",
        "scope": "five T054 scripts, 013 outputs, SPEC/LOG/STATE/WHY/DECISIONS and G3/runbook",
        "cloud": ["16.176.181.251", "13.236.44.106"],
        "cloud_directory": "/home/ubuntu/rca-p7/T-054/checkpoint013/",
        "download_limit_bytes_each": 2 * 1024**3,
        "fixture_dev_limit_seconds_each": 3600,
        "g3": False, "test_grant": False, "main_dispatch": False,
        "torai_A_main_grant": False, "commit_push": False,
    }
    for name, value in (("before-pins.json", pins), ("preparation-permission.json", permission)):
        with (RUN / name).open("x", encoding="utf-8") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2)
    append(ROOT / "docs/DECISIONS.md", """
## T-054 — duyệt chuẩn bị 013 và D1–D4/R3, 07/11/2026

Minh xác nhận “Duyệt chuẩn bị 013 và chốt D1–D4/R3 theo đề xuất trên”. Phạm vi và giới hạn thao tác ở `results/T-054/runs/chuan-bi-main-013/preparation-permission.json`. Codex làm, Claude phản biện. Duyệt sửa năm wrapper p7/nguon/dieu_phoi/cham/fixtures, dựng R1 và bộ 013, kiểm fixture/dev trên hai EC2 mới, cập nhật SPEC/LOG/STATE/WHY và hồ sơ G3/runbook. Mỗi máy tải thêm tối đa 2 GiB và chạy fixture/dev tối đa 60 phút. Lần này là chuẩn bị trước quyền test/main.

- D1. Khai đúng lần đọc 006 và việc cấu trúc thời gian cohort OB đã được dùng sửa adapter. Phạm vi quyền lịch sử chưa rõ được giữ nguyên như lịch sử. Khi báo OB phải nêu giới hạn tính độc lập của việc sửa adapter đó.
- D2. Cho phép trình khóa TT/Nezha khi H1 RE3 còn OPEN. RE3 cần nguồn, profile và quyền đánh giá riêng cho bản cuối. Điều kiện main TT/Nezha theo gói được khóa.
- D3. Giữ AC sleep bằng 0 trong đợt main được duyệt tới khi xong nhận/kiểm/chấm trên laptop, rồi khôi phục 2700 giây. DC theo thiết lập hiện hành.
- D4. Khóa bảng mô tả chênh Hit@5 cặp M1–M4 trên 34 OB, 30 ca còn lại và nhóm bốn ca từ audit006. A4 giữ đủ 34 ca và mức đã chốt. Bảng nhóm không phân xử riêng tác động adapter với độ khó ca.
- R3. Giữ bản sao trên hai EC2 cũ, loại hai máy đó khỏi lịch013.

G3, mở/đọc/chuyển test, nguồn A cho main, phát main và chấm cần quyết định cuối có nguồn đúng gói. Commit được chuẩn bị danh sách/diff cho Minh duyệt riêng.
""")
    append(ROOT / "docs/WHY.md", """
## T-054 — quyền, hàng chờ A và giới hạn trước chạy 013, 07/11/2026

Minh duyệt gói chuẩn bị013 và D1–D4/R3. Kiểm quyền phát main ở CLI cùng quyền G3/test để mọi đường run/resume dùng cùng điều kiện. Một supervisor laptop giữ tập slot bất biến. TORAI A chỉ được phát sau khi các slot khác A đã VERIFIED. Nguồn A thiếu quyền hoặc sai pin có biên nhận theo slot trước phát; lỗi chưa phân loại khi A chạy giữ attempt và dừng theo policy, ghi BLOCKED cho phần A chưa phát. Báo cáo giữ toàn ma trận và khai nhóm A chưa đủ seed/ca. Hai plan cùng host không phù hợp hợp đồng ghép hiện tại. Chỉ sắp A cuối danh sách chưa đủ khi hai worker hoạt động. Lý do là ngăn phần phụ làm mất bảng chính đã đủ điều kiện, giữ nguyên các ngưỡng và mẫu số thống kê.

Tái dùng M1 TT012, fixture C-d3 DAG/cyclic/no-target012, parity OB008 và nguồn CSV A đã audit006 sau kiểm hash. Chỉ chạy các tuyến dev thực sự khác. R1 dùng bản chiếu mờ từ nguồn đối chiếu riêng, giữ đầy đủ cohort/byte/hash, không đổi guard T052. D1 khai tiếp xúc đã dùng sửa adapter; D2 để profile RE3 OPEN cho đợt cuối; D4 là bảng mô tả nhóm đã xác định trước điểm. Hạn chế logts A thiếu N và nhánh OB lệch số mẫu vẫn phải khai theo bằng chứng hiện có. Gói chuẩn bị và đồng thuận phản biện chưa trả lời RQ3b/RQ3d bằng test.
""")
    spec = ROOT / TASK / "SPEC.md"
    text = spec.read_text(encoding="utf-8")
    marker = "## Phạm vi ghi\n"
    addition = """
**Bổ sung Minh duyệt 07/11/2026 — chuẩn bị013.** Duyệt sửa `results/T-054/scripts/{p7,nguon,dieu_phoi,cham,fixtures}.py`, ghi `results/T-054/runs/chuan-bi-main-013/`, cập nhật SPEC/LOG và đúng dòng STATE, nối DECISIONS/WHY cùng hồ sơ G3/runbook. Duyệt SSH/dựng môi trường/fixture và đúng pilot dev cần bổ sung trên 16.176.181.251 và 13.236.44.106, vùng `/home/ubuntu/rca-p7/T-054/checkpoint013/`. Tải thêm ≤2 GiB/máy, fixture/dev ≤60 phút/máy. R1 chỉ đổi metadata và công thức chuẩn bị trước grant dữ liệu. D1–D4/R3 theo DECISIONS cùng ngày. TORAI A giữ một plan laptop, quyền theo slot, phát sau toàn phần khác A VERIFIED; thiếu quyền/sai pin A ghi chặn đúng slot, lỗi A chưa rõ giữ lượt và dừng A. Đủ A4 và snapshot mới được chấm, thiếu A không bình quân seed sống. Nguồn quyền chuẩn bị không mở test/main/RE3 hoặc commit/push.
"""
    assert marker in text
    spec.write_text(text.replace(marker, marker + addition + "\n", 1), encoding="utf-8", newline="")
    append(ROOT / TASK / "LOG.md", """
## 07/11/2026 — Codex, Windows điều khiển hai EC2 mới, người làm T-054 — mở chuẩn bị013

Minh duyệt “Duyệt chuẩn bị 013 và chốt D1–D4/R3 theo đề xuất trên”. Đã lưu quyền và snapshot nguyên byte các file trong phạm vi ở runs/chuan-bi-main-013. Ghi quyết định trước khi áp dụng. Chỉ dùng fixture/dev, metadata đã có và công thức chuẩn bị nguồn; chưa grant test/main/A hoặc RE3. Khóa giới hạn tải thêm 2 GiB và fixture/dev 60 phút mỗi EC2. Các bước tiếp là sửa kiểm quyền và A, fixture, môi trường+dev hai máy, metadata R1+ma trận+gói, kiểm diff+manifest và bàn giao Claude.
""")
    state = ROOT / "docs/STATE.md"
    lines = state.read_text(encoding="utf-8").splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("- **T-054"):
            lines[index] = "- **T-054 — đang chuẩn bị013 theo Minh duyệt.** Codex làm, Claude phản biện. D1–D4/R3 đã chốt. Sửa quyền/A, R1, fixture/dev đúng phần thiếu trên hai EC2 mới và gói khóa. Dung lượng root máy vừa mở rộng còn 25,10 GiB tại lần đo. Chưa G3/test/main. [LOG](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).\n"
    state.write_text("".join(lines), encoding="utf-8", newline="")
    print("Recorded permission, decisions, rationale, SPEC and append-only LOG; snapshots preserved")


if __name__ == "__main__":
    main()
