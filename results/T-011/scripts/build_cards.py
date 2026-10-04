"""Render metadata-only cards from run-001 counts; no network or telemetry."""
import csv
import json
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
RUN=BASE/"runs/run-001"
SUMMARY=json.loads((RUN/"count-summary.json").read_text(encoding="utf-8"))
LABELS=json.loads((RUN/"labels-from-code.json").read_text(encoding="utf-8"))
ROWS=list(csv.DictReader((RUN/"inventory.csv").open(encoding="utf-8")))


def num(n): return f"{n:,}".replace(",", ".")


def card(name,title,is_cloud):
    original=SUMMARY["datasets"][name+"_Original"]
    prep=SUMMARY["datasets"][name+"_Preprocessed"]
    case_count=len(original["date_tokens"])
    dates=", ".join(original["date_tokens"])
    special=("Cloud Computing có 6 archive metric nhưng 5 archive log; thiếu `Log Data/20240207.zip` ở tree. README nói ngày này chỉ có CloudTrail CSV, không có EKS log cần parser. Không diễn giải thành không có mọi log của ngày đó."
        if is_cloud else "Cả 4 ngày có archive metric và log ở Preprocessed; sự có mặt không chứng minh chất lượng nội dung hoặc coverage entity.")
    labeltext=("FACT nhãn riêng: `Baseline/Nezha/20240124/20240124-fault_list.json` có một record cho ngày 2024-01-24, `inject_type = infinite loop bug`, `inject_pod = ip-10-1-100-109.ap-northeast-1.compute.internal`, `inject_time = 2024-01-24 03:10:51`, `inject_timestamp = 1706087451`. File `root_cause_hipster.json` dùng cùng entity. Tên trường pod nhưng giá trị giống host; chưa có mapping service, không tự sửa. Đây là 1 record nhãn trong code, không xác minh toàn 6 archive và không là onset."
        if is_cloud else "FACT README kho code chỉ rõ ca 20211203 có root MongoDB-v1 trong `readme.pptx` bên trong dữ liệu. Chưa tải PPTX nên đây là lời nguồn. Code `Baseline/FastPC/baseline_evaluation.py` chứa 5 cặp folder/nhãn pod, lưu nguyên tại labels-from-code.json. Folder 0901 không có trong 4 archive hiện tại; mapping năm/release còn OPEN, không gọi 5 nhóm là census Product Review hiện tại.")
    faults=("HF Original README liệt kê cryptojacking, silent pod degradation fault, malware attack, mistakes made by GitOps, configuration change failure, bug infection."
        if is_cloud else "HF Original README liệt kê DDoS attack, external storage failure, node resource contention stress test, noisy neighbor issue. Paper §3.1 dùng các mô tả OOM/high CPU/external-storage-full/DDoS. Mapping tên giữa hai nguồn theo từng ngày còn OPEN.")
    stack=("Nguồn mô tả CloudWatch Metrics/Logs và JMeter; một số scenario dùng Prometheus."
        if is_cloud else "Nguồn mô tả OpenShift, Prometheus, Elasticsearch và JMeter.")
    return f'''# {title} — Original và Preprocessed

Ngày kiểm: 03/10/2026. **Hoàn tất xác minh nguồn/metadata; chất lượng số đo chưa kiểm.** Q-47 cho kiểm số đo ngoài bộ bảo toàn; Q-49/WHY-13 chọn OpenRCA Bank, không chọn LEMMA làm bộ bảo toàn. Chưa chọn dataset thí nghiệm hoặc chia dữ liệu. Hai biến thể dùng chung nguồn, không phải hai dataset độc lập. FACT nguồn được phân biệt với FACT file.

## 1. Danh tính, nguồn và phạm vi đã kiểm

| Mục | Nội dung |
|---|---|
| Tác giả/version | LEMMA-RCA, Lecheng Zheng và cộng sự; paper arXiv v4 (25/08/2026), nguồn/code/HF ghim revision tại [manifest](runs/run-001/manifest.json). Không lấy “main” hiện hành thay revision đã kiểm. |
| Nguồn chính | [Paper v4](https://arxiv.org/html/2406.05375v4), [kho tác giả](https://github.com/lemma-rca/rca_baselines), [Original](https://huggingface.co/datasets/Lemma-RCA-NEC/{name}_Original), [Preprocessed](https://huggingface.co/datasets/Lemma-RCA-NEC/{name}_Preprocessed). Snapshot nằm trong manifest. |
| Stack/công cụ lỗi | {stack} Các scenario có kiểm soát theo paper Appendix J; không suy một công cụ tiêm chung khi nguồn chưa chỉ rõ. |
| Giấy phép dữ liệu/code | **OPEN material conflict**: HF frontmatter là CC BY-NC 4.0, cuối cùng README là CC BY-ND 4.0. GitHub README intro NC, phần License ND; file LICENSE là NC. Paper Appendix F/trang tác giả là ND. Xem [license-and-source-conflicts](license-and-source-conflicts.md). Phép sao chép/kiểm nội bộ phi thương mại có giao quyền theo cả hai, xem xac-minh-nguon-va-doc-lap.md; không chốt một license hoặc quyền phân phối bản biến đổi. |
| Census ngoài archive | {case_count} date token: {dates}. Original {original['archive_files']} ZIP; Preprocessed {prep['archive_files']} ZIP. Đây là census file public, không xác minh số incident/repetition. [count-summary](runs/run-001/count-summary.json), [inventory](runs/run-001/inventory.csv). |
| Đã có/được đọc/thực kiểm | Telemetry đã tải: 0 archive; Q-47 cho kiểm các bộ ngoài bảo toàn; giao quyền license cho phép kiểm nội bộ phi thương mại theo phạm vi báo cáo nguồn, ca thực kiểm: 0. Đã đọc README, API metadata, code và label riêng; không mở ZIP/NPY/log. |
| Chạy lại | `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts`; dựng thẻ `py -3 -B results/T-011/scripts/build_cards.py`. Lượt lấy nguồn và chi phí có ở manifest. |

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí MRP | Trạng thái/kết quả | Phạm vi và giải thích khác |
|---|---|---|
| 1. Công khai/tải/giấy phép | FACT metadata truy cập; OPEN giấy phép và tải telemetry | Archive chưa thử tải, license chưa thống nhất; công khai không thay điều khoản. |
| 2. Nhãn root/thời điểm | FACT nguồn có nhãn; OPEN census | Nhãn riêng/code/PPTX có phạm vi khác nhau; injection không là onset quan sát. |
| 3. Trace cha–con | OPEN cả hai biến thể | README raw nói có cả trace; paper/preprocessed tập trung metric/log. Chưa có schema trace raw/parent và không được kết luận không có trace. |
| 4. Metric/log | FACT có archive theo modality; OPEN chất lượng | {special} |
| 5. Root/vị trí | OPEN | Số entity hệ thống không phải số root; mapping host/pod→service và graph theo ca chưa kiểm. |
| 6. Tài nguyên/mạng/mã nguồn | FACT tên scenario nguồn; OPEN nhóm/độ phủ file | Không tự gán nhóm chỉ từ tên; lỗi cấu hình có thể gây tài nguyên, cần mô tả scenario. |
| 7. Triệu chứng ngoài root | OPEN — chưa kiểm | Chưa chạy kiểm số đo trong nhánh nguồn; narrative scenario không thay phép đo theo ca. |
| 8. Normal đủ học ngưỡng | OPEN | Paper mô tả lịch chạy; chưa kiểm normal label/độ dài/gap/warm-up từng archive. |
| 9. Bộ độc lập | OPEN ở mức bộ chọn | Khác nhóm/stack với TT là thông tin đầu vào; Original/Preprocessed cùng lineage; PR–Cloud chưa đủ bằng chứng độc lập. Xem xac-minh-nguon-va-doc-lap.md. |

## 3. Nhãn, số ca và khả năng phân xử

{labeltext}

{faults}

Nguồn code/label nguyên văn, số đếm literal và mapping chưa xác minh lưu tại [labels-from-code.json](runs/run-001/labels-from-code.json); script dùng AST, không chạy code tác giả. Ngày file không được coi là số lần lặp. Bảng root×fault×repetition đầy đủ, tổng root khác nhau, ô thiếu và label parse errors của archive: **OPEN**, cần label/PPTX nội bộ sau đúng quyền. Không chép label code cũ thành nhãn mới.

| Root/graph | Có trong graph? | Bậc vào/ra raw và số node/cạnh |
|---|---|---|
| Entity ở label nguồn | OPEN | OPEN; chưa trace hoặc adjacency có nguồn |
| Đồ thị từ kiến trúc | CANDIDATE — chưa kiểm | Cần mapping entity và định nghĩa cạnh; không tương đương đồ thị span |

Vị trí graph có thể bị confound bởi service/fault/workload. Không tự định nghĩa hub hay suy topology toàn hệ từ sơ đồ paper.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

| Nguồn/biến thể | Ca telemetry đã kiểm | Bằng chứng schema | Chất lượng |
|---|---:|---|---|
| Metric Original | 0 | README JSON; code Prometheus đọc `data/result`, metric pod/instance và cặp time/value | NaN/gap/cadence/unit/constant/trùng và mapping OPEN |
| Metric Preprocessed | 0 | README NPY; code kỳ vọng `KPI_Label`, `Pod_Name` hoặc `Node_Name`, `KPI_Feature`, `Sequence`, `time` | Schema kỳ vọng không chứng minh schema mọi archive |
| Log Original | 0 | Parser Elasticsearch đọc `hits/hits/_source`, `@timestamp`, `message`, kubernetes pod hoặc hostname | Cột trace ID/có giá trị/chuỗi trong payload/ghép trace đều OPEN |
| Log Preprocessed | 0 | README messages/templates; code xuất Node/Pod, Timestamp, Messages rồi đặc trưng log | Chưa xác minh có giữ ID, parser loại timestamp trong message không chứng minh mất timestamp riêng |
| Trace Original/Preprocessed | 0/0 | README raw tuyên bố trace; chưa biết member/schema | Parent/status/type/MQ/database coverage OPEN |

Code tham chiếu: [metric_json2npy.py](runs/run-001/sources/code__IT__data_preprocessing__metric_json2npy.py) dòng 15–31, 69–127, 136–190; [json2message.py](runs/run-001/sources/code__IT__data_preprocessing__json2message.py) dòng 49–112. Các parser này không mặc định áp được mọi ngày của Cloud/PR.

| Phép đếm span | Kết quả |
|---|---|
| Tổng span / root sentinel / có parent cần resolve | OPEN; chưa đọc span |
| Cha duy nhất / thiếu / không duy nhất / tỷ lệ resolve | OPEN; chưa có tử/mẫu, không ghi 0% |

## 5. Dữ liệu bình thường và mốc thời gian

HF Preprocessed README ghi PPTX scenario dùng JST, metric/log dùng UTC: phải chuyển mốc PPTX lùi 9 giờ khi đối chiếu, giữ bản nhãn gốc. Đây là FACT tài liệu, chưa kiểm clock file. Code label JSON là nguồn khác; không tự áp dịch 9 giờ thêm lần nữa lên epoch.

{('Nhãn JSON Cloud 20240124 có epoch quy về 09:10:51 UTC, còn inject_time là 03:10:51 không ghi timezone. Nếu hiểu chuỗi là UTC thì lệch 21.600 giây (6 giờ); chưa có căn cứ cho cách hiểu đó. [label-time-check](runs/run-001/label-time-check.json) giữ hai giá trị và phép đổi; OPEN timezone/ý nghĩa mốc, không tự sửa nhãn hoặc áp quy tắc JST của PPTX sang JSON.' if is_cloud else '')}

Mốc nhãn thực là injection, onset hay interval kết thúc cho mọi ngày: OPEN. Độ dài normal trước/sau, số điểm hợp lệ, contamination/warm-up/tải đổi: OPEN cả Original và Preprocessed. Không gọi phần trước sự cố “đã sạch” chỉ từ timeline narrative. Cần PPTX/label và từng file theo [inspection-plan](inspection-plan.md).

## 6. Ước lượng thô triệu chứng lan — tiêu chí 7

**OPEN — chưa kiểm**, vì nhánh hiện chỉ kiểm nguồn/metadata. Q-47 và giao quyền hai license cho phép kiểm nội bộ phi thương mại sau ghi lý do gói; xem đối chiếu điều khoản trong xac-minh-nguon-va-doc-lap.md. Chưa chạy ba q trong SPEC; không có OR/metric/graph số đo nào. Câu nguồn kể ảnh hưởng downstream không thay nhãn vùng hoặc số đếm. Tải chung, pod bị loại khi preprocessing, kênh nhiễu và clock lệch đều có thể tạo/che mất bất thường ngoài root.

## 7. Task nào chấm được bằng nhãn hiện có?

| Task | Nhãn/đơn vị thật đã biết | Phạm vi chấm |
|---|---|---|
| Xếp hạng root | Root theo pod/host ở code, hoặc lời README về PPTX | CANDIDATE MRR/Hit/NDCG đúng entity sau xác minh mapping; chưa chấm service hoặc operation |
| Phát hiện theo thời gian | Một số source có injection/failure time, toàn bộ chưa kiểm | OPEN P/R/F1 onset/window; chỉ injection-regime nếu đủ mốc và giao thức sau |
| Vùng ảnh hưởng | Chưa thấy tập nhãn thật theo từng ca trong source đã đọc | OPEN; không lấy tất cả entity hoặc root thay vùng |
| Bất thường từng trace | Chưa nhãn trace và schema | OPEN |

Chưa baseline/training; số ngày không chứng minh đủ nhãn có giám sát hoặc chuyển hệ. Chưa dùng ranking tác giả làm kết quả của nhóm.

## 8. Rò nhãn và thông tin phục vụ G1

Date token, PPTX, label JSON và hằng số `reals` là metadata phục vụ census/chấm. [RCA_methods_metric.py](runs/run-001/sources/code__Baseline__metric_only__RCA_methods_metric.py) dòng 39–54 chọn KPI `label` theo case ID, dòng 58–81 chọn metric theo case ID. Đây là FACT code; chưa chứng minh KPI bằng root. Tuy nhiên adapter tự phát hiện không được chép logic từ tên ca mà không có nguồn cấu hình độc lập với nhãn. Code còn tạo timestamp giả ở dòng 180–182; không dùng đó để chấm thời gian thật.

Nguy cơ label nằm trong biên cửa sổ/order: OPEN với IT; không mặc định đối xứng như RCAEval. Original/Preprocessed là cùng lineage; tránh chia hai bản của cùng ca sang hai phía. Q-49/WHY-13 bảo toàn OpenRCA Bank; LEMMA không giữ ngoài. Nhãn học, dev cấu hình và test chấm vẫn do G1 quyết. Chưa có adapter chứng minh loại rò.

## 9. Kích thước và chi phí

| Biến thể | ZIP | Byte ZIP theo HF | Tổng byte mọi file public |
|---|---:|---:|---:|
| Original | {original['archive_files']} | {num(original['archive_bytes'])} | {num(original['all_file_bytes'])} |
| Preprocessed | {prep['archive_files']} | {num(prep['archive_bytes'])} | {num(prep['all_file_bytes'])} |

Nguồn số: [summary](runs/run-001/count-summary.json), LFS/hash từng archive trong [inventory](runs/run-001/inventory.csv). Paper/site ghi original size là một đại lượng khác dung lượng ZIP HF; không suy giải nén từ tỷ số đó. RAM/giây đọc mẫu, giải nén thực, chi phí adapter: OPEN. Mẫu đề xuất và tổng byte ở inspection-plan; **Q-46 không duyệt tải toàn kho**.

## 10. Những điều còn mở

| Vấn đề | Cần ai/đầu vào | Kết luận phụ thuộc |
|---|---|---|
| NC/ND mâu thuẫn | Tác giả xác định license/version; Minh quyết bước tiếp | Tiêu chí 1 và phần dùng/phân phối dữ liệu |
| Phạm vi dùng LEMMA | Q-47 cấp quyền gói; giao quyền license cho kiểm nội bộ phi thương mại | Schema file, graph, triệu chứng chưa kiểm; license chính xác và quyền phân phối phái sinh vẫn OPEN |
| Label/PPTX, clock, entity mapping | Code/README + file riêng đúng quyền; Codex | Ranking và time detection đúng đơn vị |
| Trace thật và schema theo ngày | Member/schema raw, không chỉ loader | Tiêu chí 3, dựng graph từ trace |
| Root×fault×lặp, normal, chất lượng | Đủ ngày/schema/root cần kiểm trong kế hoạch | Phân xử RQ1/RQ3; một mẫu không bao phủ toàn release |

Bằng chứng này đủ mô tả kho public và giới hạn nhãn/code; chưa xác lập dữ liệu có đáp ứng mọi tiêu chí G1. Không kết luận thắng/thua từ chi phí hoặc sự có sẵn.
'''


def main():
    if (BASE/'runs/inspect-008/summary.json').exists():
        from build_file_report import main as build_current
        build_current()
        return
    cards="# LEMMA-RCA — thẻ IT\n\nQ-47 bỏ OT khỏi phạm vi mới; catalog cũ chỉ giữ lịch sử. Xem [xác minh nguồn/độc lập](xac-minh-nguon-va-doc-lap.md) cho bản kiểm hiện hành, PR license còn OPEN và xác nhận timezone tác giả. LEMMA không phải bộ bảo toàn Q-49; license chính xác còn OPEN; kiểm nội bộ phi thương mại có giao quyền cả hai license.\n\n"
    cards+=card("Product_Review","Product Review",False)+"\n---\n\n"+card("Cloud_Computing","Cloud Computing",True)
    (BASE/"the-dataset.md").write_text(cards,encoding="utf-8")
    plan='''# LEMMA-RCA — kế hoạch kiểm file sau metadata

**Q-47 đã duyệt gói bốn ZIP và quyền kiểm ngoài bộ bảo toàn; nhánh nguồn chưa tải telemetry.** Q-49/WHY-13 bảo toàn OpenRCA Bank, không phải LEMMA. License NC/ND chính xác chưa giải quyết. Giao quyền của cả hai cho phép sao chép/kiểm nội bộ phi thương mại; không chia sẻ dataset hoặc payload đã biến đổi. Root ghi lý do trước tải đúng mẫu Q-47. Tất cả revision và LFS SHA-256 nằm trong [inventory](runs/run-001/inventory.csv).

## Mẫu khởi đầu theo mục tiêu

- Product Review 20211203: README tác giả chỉ rõ MongoDB-v1 và PPTX nhãn. Chọn để xác minh nhãn root, timezone JST/UTC, alias pod/service, metric–log alignment và cấu trúc NPY; không chọn vì nhỏ.
- Cloud Computing 20240124: có file nhãn riêng với epoch/time/entity/fault, chọn để kiểm thời gian và host/pod mapping ở hệ khác. Ca này không đại diện cho mọi schema Cloud.
- Dùng cả metric và log mỗi ca để kiểm cross-modality; chỉ schema chưa đủ xét triệu chứng. Nếu chưa quyền telemetry, tiếp nhận chỉ metadata/label đúng phạm vi, không parent-quality/graph/symptom.

| Dataset | File đề xuất | Byte | Mục tiêu |
|---|---|---:|---|
'''
    chosen=[]
    for row in ROWS:
        if row["dataset"] in ("Product_Review_Preprocessed","Cloud_Computing_Preprocessed") and Path(row["path"]).stem in ("20211203","20240124"):
            chosen.append(row)
            plan+=f"| {row['dataset']} | `{row['path']}` | {num(int(row['bytes']))} | Mapping nhãn/clock và hai modality ở ca có nguồn nhãn |\n"
    total=sum(int(r["bytes"]) for r in chosen)
    plan+=f"\nTổng bốn ZIP đề xuất: **{num(total)} byte**. Mục lục ZIP đã được parent kiểm trong runs/sizes-001: tổng member 17.500.872.729 byte, là kích thước khai báo chưa giải nén xác nhận. RAM/thời gian đọc còn OPEN. Chi tiết member và chi phí xem ../T-003/dung-luong-tai-va-giai-nen.md; không lặp tải mục lục.\n"
    plan+='''
## Phủ phần còn lại trước kết luận toàn release

Mẫu trên chỉ trả lời hai ca, chưa phủ nhiều root/fault/lặp. Các date token ở bảng sau là tầng metadata chưa biết schema; phải lấy nhãn/schema từng ngày trước, rồi kiểm ít nhất mỗi schema và mỗi root tại đúng ca root. Nếu so repetition phải kiểm đủ repetition. Không coi bốn/sáu date token là bốn/sáu incident khi chưa nhãn nội bộ.

| Dataset/biến thể | File | Byte | Phạm vi/dependency |
|---|---|---:|---|
'''
    for row in ROWS:
        if not row["path"].endswith(".zip"): continue
        role="Original: truy schema/trace hoặc nhãn không còn ở Preprocessed; chưa duyệt tải"
        if row["dataset"].endswith("Preprocessed"):
            role="Phủ ngày và kiểm mapping/schema trước khi suy toàn release"
            if "20240207" in row["path"]: role="Ngoại lệ CloudTrail, cần counterpart CSV raw/label; không suy không có log"
            if row in chosen: role="Mẫu Q-47 đã duyệt; kiểm nội bộ phi thương mại theo giao quyền license"
        plan+=f"| {row['dataset']} | `{row['path']}` | {num(int(row['bytes']))} | {role} |\n"
    orig_total=sum(int(r["bytes"]) for r in ROWS if r["dataset"].endswith("Original") and r["path"].endswith(".zip"))
    prep_total=sum(int(r["bytes"]) for r in ROWS if r["dataset"].endswith("Preprocessed") and r["path"].endswith(".zip"))
    plan+=f"\nToàn bộ Preprocessed ZIP: {num(prep_total)} byte; toàn bộ Original ZIP: {num(orig_total)} byte. Đây là chi phí census file public, **không phải đề nghị tải trọn hoặc ngân sách đã duyệt**. Giới hạn >5 GB phải trình Minh.\n"
    plan+='''
Nếu cần kiểm trace thật, ưu tiên cùng ca có label 20211203/20240124 để đối chiếu raw–processed; bản Original tương ứng có byte chính xác trong bảng, PR lớn nên cần tìm metadata/member hoặc xin tác giả file riêng trước. Chưa có file sample độc lập công khai trong tree đã kiểm. Không tải Original chỉ để lấp ô “trace”. Có thể giữ trace OPEN nếu chưa quyền hoặc tác giả chưa làm rõ; không gọi “không có trace”.

OT bỏ hẳn khỏi phạm vi mới theo Q-47. Giữ catalog/nguồn lịch sử; không khảo sát, tải hoặc đề xuất dùng OT tiếp.

## Kiểm và tiếp nhận

Sau quyền phù hợp: kiểm hash/CRC/member sizes trước extract; giữ mọi lượt. Phân biệt label injection/onset; giữ clock gốc rồi đối chiếu JST/UTC; graph parent dùng khóa ghép; log ID cột/payload/match tách riêng. Chọn SLI độc lập nhãn; case-dependent selector trong code công bố không tự được phép. Đo normal/quality từng kênh, rồi q theo SPEC chỉ khi có quyền số đo. Lượt >1 giờ cần Minh cho phép.

Lệnh chỉ đọc kết quả đã có: `py -3 -B results/T-011/scripts/collect_metadata.py --verify --validate-counts`. Không chạy `--sources` đè lượt cũ. Build thẻ là bước ghi trong phạm vi SPEC; nguồn số là run-001.
'''
    (BASE/"inspection-plan.md").write_text(plan,encoding="utf-8")
    dump={"selected_preprocessed_files":chosen,"selected_zip_bytes":total,"all_preprocessed_zip_bytes":prep_total,
          "all_original_zip_bytes":orig_total,"status":"Q47 sample authorized; not preserved under Q49; narrow internal noncommercial audit covered by both license assertions; exact license unresolved; no archive fetched by source branch"}
    (BASE/"runs/source-final-001/inspection-proposal.json").write_text(json.dumps(dump,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("Built two IT cards and exact archive inspection proposal; no telemetry")


if __name__=="__main__": main()
