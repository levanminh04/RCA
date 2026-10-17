"""Sinh bản hiện hành từ nguồn trước sửa và bằng chứng đã lưu của gói Q-155."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
OUT = ROOT / 'results/T-035'


def read(path):
    return json.loads(path.read_text('utf-8'))


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def render():
    comparison = read(BASE / 'comparison.json')
    assert comparison['pass'] and comparison['reused_cases'] == 0
    fixtures = [read(BASE / f'fixture-oracle-seed{i}-001/result.json') for i in range(3)]
    assert all(x['pass'] and x['case_count'] == 129 for x in fixtures)
    assert read(BASE / 'oracle-commands-001.json')['pass']
    assert read(BASE / 'legacy-commands-001.json')['pass']
    before = read(BASE / 'fixture-before-002/result.json')
    source = lambda name: (BASE / 'before/results/T-035' / name).read_text('utf-8')
    report = source('thong-ke-do-thi.md')
    report = replace_once(report, '| 1. Mô hình chung đủ nút/cạnh | Đạt theo hợp đồng v2, chờ nghiệm thu | dac-ta-do-thi.md; fixture cũ và bổ sung; routing/instrumentation FlashTicket thật chưa kiểm |',
                          '| 1. Mô hình chung đủ nút/cạnh | Đạt theo hợp đồng v2.1 trong miền đã kiểm, chờ nghiệm thu | dac-ta-do-thi.md; fixture cũ và bổ sung; ID va chạm bị từ chối rõ; routing/instrumentation FlashTicket thật chưa kiểm |')
    report = replace_once(report, '| 6. K1–K7 và F1–F11 | Đạt | kiem-dung-dan.md; K6 chỉ là kiểm mô tả, không đối chiếu độc lập đã xác nhận |',
                          '| 6. K1–K7 và F1–F11 | Đạt trong miền đã kiểm, bổ sung v2.1 | kiem-dung-dan.md; K5 cần đối chiếu đích literal bên cạnh hai phép chiếu; K6 chưa là đối chiếu độc lập đã xác nhận |')
    report = replace_once(report, 'T-036 nhận mô hình v2,', 'T-036 nhận mô hình v2.1,')
    report = replace_once(report, 'Prompt hiện tại trong LOG Phiên 7 và runs/sua-n1-001/; giữ prompt Phiên 6 làm lịch sử; Minh chuyển thủ công.',
                          'Prompt hiện tại trong LOG Phiên 8 và runs/sua-hop-dong-001/; prompt các phiên trước giữ làm lịch sử; Minh chuyển thủ công.')
    report += f'''
## 8. V2.1 — chính sách dữ liệu thiếu, định danh và lỗi đầu vào

Lượt Codex sạch phát hiện bốn lỗi cài đặt: tên thao tác thiếu ở một số dtype làm lỗi tạo khóa; ID endpoint trùng ID thao tác làm đổi/mất đích khi chiếu; thời gian âm/tràn được nhận; kiểu entity.type mâu thuẫn bị chọn theo thứ tự dòng. Đây là lỗi bộ dựng dùng chung, không là hạn chế RCA hoặc lỗi dataset đã xác nhận. Vì vậy kết quả đạt trên fixture/dev của bản v2 không chứng minh bộ dựng đã tuân thủ toàn hợp đồng.

V2.1 chuẩn hóa tên thiếu về null; từ chối identifier_collision trước xuất/chiếu; kiểm thời gian trước ép/cộng/nhân; gộp kiểu đã biết/unknown nhất quán và từ chối hai kiểu đã biết mâu thuẫn. Giữ định dạng ID và graph hợp lệ. Inventory-only vẫn riêng; ID thực thể quan sát/component trùng ID thao tác không được hỗ trợ trong hợp đồng này. Muốn hỗ trợ cần thiết kế namespace riêng, không âm thầm đổi đích. Quyền ở Q-155, lý do ở phần bổ sung WHY-52, chính sách tại dac-ta-do-thi.md §8.

{fixtures[0]['case_count']} ca literal mới đạt ở seed0/1/2, gồm đối chứng hợp lệ và đích literal độc lập; 18+33+3 ca trước cũng đạt ở ba seed. Nguồn `runs/sua-hop-dong-001/fixture-oracle-seed0-001/result.json#/cases` và các seed khác; lệnh/exit code tại oracle-commands-001.json và legacy-commands-001.json. Cùng oracle JSON chạy bản trước đạt {before['passed']}/{before['case_count']}; số fail là số ca kiểm, không là từng ấy lỗi độc lập.

Checker ban đầu so witness tuple/list native nên chín ca có JSON đúng bị báo trượt. Giữ oracle.py và các lượt đầu; oracle_json.py chỉ sửa comparator JSON strict, inputs/expected/digest trước code không đổi. Nguồn oracle-before-code.json và oracle-revision-002.json. Không sửa đáp án theo output bộ dựng. K5 vẫn được dùng để kiểm nhất quán; các đáp án đích literal mới kiểm thêm trường hợp hai phép chiếu có thể cùng sai.

Hồi quy v2.1: {comparison['case_count']} ca chạy mới, không reuse, {comparison['window_count']} khoảng K1/K2/K4/K5 đạt, {comparison['graph_count']} graph khớp từng byte bản đã lưu. Mọi nội dung kết quả ca ngoài chi phí máy khớp bản v2; nguồn `runs/sua-hop-dong-001/comparison.json#/cases`, `#/graphs`, `#/all_K1_K2_K4_K5`. Không ghi đè các graph/JSON mô tả cũ; các bảng mô tả giữ nguyên do đầu ra đồng nhất. Chi phí lượt mới {comparison['seconds']/60:.2f} phút, RAM đỉnh {comparison['peak_rss_bytes']/1024**3:.2f} GiB (`#/seconds`, `#/peak_rss_bytes`).

Bản sửa trả lời bốn lỗi hợp đồng trong miền fixture và hồi quy đã kiểm; chưa xác nhận routing/instrumentation FlashTicket thật, nghĩa vật lý cạnh/Node hoặc lợi ích RCA. Chưa tự nghiệm thu T-035/P5/G3, chọn P6 hoặc đóng RQ3. Minh yêu cầu phiên Codex sạch soát lại toàn task như lần đầu, nhận xét trước lịch sử; Claude vẫn phản biện chính thức.
'''
    checks = source('kiem-dung-dan.md')
    checks += f'''
## Kiểm v2.1 sau sửa lỗi hợp đồng

- Trước sửa: toàn bộ 4.310 artifact của manifest v2 và 362 mục nguồn khớp; nguồn quyền/thiết kế và bản trước giữ ở runs/sua-hop-dong-001/ (preflight.json, input-verification.json, before/). Không lấy hash mới làm xác minh nguồn cũ.
- Oracle mới có {fixtures[0]['case_count']} ca literal, đáp án viết trước builder, receipt oracle-before-code.json; thiết kế fixture_design.md. Nhóm: tên thiếu nhiều dtype, va chạm ID và project độc lập, biên thời gian/cộng/nhân int64/ns ưu tiên, kiểu mâu thuẫn và unknown hai thứ tự. Kiểm cả Prepared.graph/build và vocabulary/null khi cần, so đích literal, node/edge/count/witness và lỗi mong đợi.
- Sửa checker sau lượt đầu chỉ chuẩn hóa comparator JSON strict; bản gốc/đáp án và run fail giữ nguyên. AST hàm tạo fixture và digest inputs/expected trước code được kiểm không đổi ở oracle-revision-002.json. Phép đổi đích sai bị comparator từ chối; không đổi đáp án cho khớp builder.
- 129 ca mới đạt seed0/1/2 (fixture-oracle-seed0-001 đến seed2-001/result.json); 18 fixture gốc,33messaging,3ca thiếu attributes/links trước đạt cả ba seed. Command receipts ghi argv, seed, thời gian và exit code; dùng code đóng băng frozen-code.json.
- Hồi quy đủ {comparison['case_count']} ca/{comparison['window_count']} khoảng, K1/K2/K4/K5 đạt; {comparison['graph_count']} graph byte bằng bản v2, mọi trường ca trừ chi phí máy khớp; comparison.json. Không phát lại baseline RCA, K3/K6/K8 hoặc nguồn phụ mức ngày; bằng chứng mô tả trước giữ trong đúng phạm vi.

Các đường trên tính từ runs/sua-hop-dong-001/. Việc fixture và hồi quy đạt không tự khẳng định mọi instrumentation thực tế, lợi ích RCA hoặc đủ căn cứ chọn P6. ID va chạm được từ chối là giới hạn tường minh, không coi là đã hỗ trợ hai miền trùng nhau. Gói sửa và prompt mới được trình để tự soát/phản biện/nghiệm thu; task chưa đóng.
'''
    return {'dac-ta-do-thi.md': (BASE / 'contract-v2.1.md').read_text('utf-8'),
            'thong-ke-do-thi.md': report, 'kiem-dung-dan.md': checks}


def main():
    for name, value in render().items():
        (OUT / name).write_text(value, encoding='utf-8')
    print(json.dumps({'written': list(render())}, ensure_ascii=False))


if __name__ == '__main__':
    main()
