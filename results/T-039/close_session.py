"""Append authorized T039 handoff only; STATE is edited separately under lock."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[2];B=ROOT/'results/T-039'
log=ROOT/'tasks/T-039-p5b-online-boutique/LOG.md'
summary=json.loads((B/'doi-chieu/tong-hop.json').read_text(encoding='utf-8'))
report='''

### Kết thúc triển khai trong quyền — chuyển Claude phản biện kết quả

**Quyết định của Minh trong phiên:** quyền tải exact list/giữ toàn T039/giữ pin và chứng cứ commit-tree đã nằm ở các mục trước; Phiên4 ghi nguyên lời duyệt snapshot cũ và lời tiếp tục. Chưa ghi DECISIONS/WHY vì lời giao cấm; đề xuất chép quyết định chính thức đúng file/nội dung/lý do/ảnh hưởng ở results/T-039/de-nghi-ghi-quyet-dinh.md, chờ Minh duyệt riêng. Không chọn thiết kế nghiên cứu mới hoặc thay pin nội dung.

1. **Đã làm:** hoàn tất phần triển khai nguồn tham chiếu, mapping, dựng/chiếu và đối chiếu132graph/22opaqueID×2mức×full/N/A hiện hành. Tĩnh23entity/22edge và68operation/71edge,82relation/2logical-instance binding/53signal declarations; numbers từ doi-chieu/tong-hop.json#/record_counts và #/static_counts. Mapping10entity verified,20operation literal verified/32candidate unverified/3SQL unmapped. Kiểm và phân tích7nhóm có match tương ứng, nguồn→record→key→mapping→set,93key chains và53nhóm rawedge exclusions trong runs/phan-tich-002. Báo cáo đọc bằng tiếng Việt tại phan-tich-chenh-lech.md; source audit/lineage và bao-phu-nguon.md tách đọc/scan/excluded toàn274tree entries. Đầu ra sẵn để Claude phản biện, không tự nghiệm thu task.
2. **File thay đổi:** chỉ results/T-039/ (bản ghi/mapping/graph132comparison, nguồn registry/coverage đã khảo sát, báo cáo/script/fixtures/runs/manifest/prompt), nối LOG này và chỉ dòng T039 STATE. Không sửa SPEC/src/T035/T036/T037/T038/WHY/DECISIONS/REVIEW/platform. Nguồn tải còn nguyên; không tải thêm hoặc mở test/raw/Weight/Node values. Git diff toàn repo có thay đổi cũ/phiên khác; không rollback hoặc nhận các thay đổi đó là của T039. Protected observations của lượt004 cho build/compare và manifest T036/T037/T038 đều không đổi; kết quả chốt cuối ở ket-thuc-001/verification.json.
3. **Kiểm đã chạy:** thuc-thi-snapshot-004/verification.json PASS132; oracle literal giữ từ trước transform, owner conflict/unverified/empty denominator/projection; độc lập khóa/tập/giao/hiệu/members/exclusions/mẫu số; permutation và không đổi input; interval và conditional_reference nguyên; canonical allowlist và hash132graph/T035,228registry refs và snapshot4file đã kiểm. Typed trace denominator0/null do unknown, không lấp kiểu từ kiến trúc. Exact archive004 đã giữ; kiểm cuối kiểm archive bằng byte, JSON/provenance/prompt mẫu/hash/LOG append-only/STATEonlyrow rồi lập manifest. Pilot/cost/process input/memory theo run; lượt004 khoảng3,669s/71.557.120byte peak process, không benchmark cô lập hoặc đo giờ công toàn task. Lượt trước/failure giữ nguyên:001 ngắt trước oracle,002 mapping_target do điều phối nhầm level,003 PASS nhưng bindingduplicate/candidate metadata sửa ở004; analysis001 locatorfile không có được từ chối,002 sửa đúng source. Root đã lưu rõ135comparison lịch sử tái dựng là RECONSTRUCTED_NOT_ORIGINAL_BYTES vì runner đầu chỉ ghi canonical, không giả chúng là byte gốc. Không sửa shared để vượt lỗi. Chi phí/tổng byte giữ mọi lượt nằm trong manifest/cost và receipt.
4. **Còn mở và mức trả lời câu nguồn:** cây snapshot được phân hoạch đủ; inventory toàn deployment và ngữ nghĩa runtime chỉ đạt một phần. Chưa có app→build→image digest→deploy→dataset, selected instrumentation naming/Health binding, collector producer Source/Target/Node, tính độc lập metadata ngày hoặc nghĩa host của Node. Source code cho thấy context.TODO và current-span rename, nhưng chưa quy chúng là nguyên nhân dataset. Graph so ở miền dev-adapter có điều kiện, full không cả ngày; tỷ lệ1 phía T chỉ trên cạnh đủ mapping, không telemetrycoverage. T040/P6/P9 nhận đúng evidence/input/owner/cost/limits trong ban-giao.md và de-xuat-bo-sung-nguon.md; chưa thực hiện gói sau. Chưa chọn P6, xác nhận lợi ích RCA, đóng RQ3/RQ5/P5/G3 hoặc mở test. Minh/Claude cần đánh giá phần mô tả đã triển khai và giới hạn nguồn; nguồn mới phải có exactlist/revision/byte được duyệt trước lấy.

**Bước tiếp chính xác:** Minh copy prompt bên dưới (cũng ở results/T-039/prompt-claude.txt) sang Claude để phản biện kết quả; chưa có quyền ghi REVIEW thì trả lời chat. Đọc ban-giao.md, manifest và đầu ra thật; không chỉ LOG. Lệnh kiểm hash rẻ nếu được Minh giao: py -3 -X utf8 -B results/T-039/finish_results.py verify <ten-kiem-moi>. Tái lập runner cần tênrunmới và quyền chạy: py -3 -X utf8 -B results/T-039/execute_pinned.py <ten-run-moi>. Không tự đổi sang live src.

**Lệnh chốt cuối lượt này:** py -3 -X utf8 -B results/T-039/finish_results.py finalize. File kết quả dự kiến runs/ket-thuc-001/verification.json và manifest.json; có lỗi phải giữ lỗi/báo trước kết luận. **Đề xuất commit sau Minh duyệt riêng, chưa làm:** research: implement pinned T039 Online Boutique source graph comparison. Không push/commit bằng quyền triển khai.

### Prompt Claude — soát kết quả (Minh chuyển thủ công)

```text
'''
prompt=(B/'prompt-claude.txt').read_text(encoding='utf-8').strip()
with log.open('a',encoding='utf-8',newline='') as f:f.write(report+prompt+'\n```\n')
print('Appended T039 handoff; no STATE or other task touched')
