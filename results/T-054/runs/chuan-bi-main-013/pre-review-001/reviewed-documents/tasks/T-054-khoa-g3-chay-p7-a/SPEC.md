# T-054 — Hoàn thiện khóa G3(a), chạy và báo cáo P7(a)

> **Điều chỉnh theo Minh ngày 05/11/2026:** bỏ ràng buộc giữ test/dẫn xuất P7 ở local của Q-42 và phương án local trước đây. Được lập phương án phân chia P7 giữa EC2 và laptop để tối ưu tổng thời gian. Chưa mở test, chưa duyệt G3 hoặc tự phát lô; cần hoàn thiện bố trí nhiều máy, môi trường/đối chiếu đúng phần khác và nguồn/đích truyền cụ thể trước chạy. Các bảng lịch local cũ bên dưới là phương án lịch sử, phải thay bằng lịch nhiều máy trước khóa. Hồ sơ checkpoint004 và driver còn ghi local-only không còn là đề xuất vận hành hiện hành; không dùng nguyên gói ấy để phát main.

- **Trạng thái hiện hành 07/11/2026:** chuẩn bị013 theo Minh duyệt đã có output, chờ Claude kiểm bản cài và Minh duyệt G3/test/nguồn/chuyển/main/chấm. D1–D4/R3 đã chốt; H1 RE3 OPEN theo D2. Không commit/push. Các lịch local/005/011 bên dưới giữ lịch sử; nguồn vận hành sắp trình khóa là hồ sơ/runbook và protocol-candidate013.
- **Người làm:** Codex.
- **Người phản biện:** Claude.
- **Thuộc gói MRP:** chuẩn bị kết thúc P6/G3(a), thực thi P7(a), chuẩn bị trình G4.
- **Tổ chức:** một task, hai pha theo yêu cầu trực tiếp của Minh; có các mốc dừng quyền trong cùng task. SPEC không tự mở các quyền thực thi.
- **Nguồn duyệt:** lời Minh và hai lượt phản biện đã lưu tại `results/T-054/runs/soan-spec-001/`. Codex nhận N1–N5 của lượt cuối, không còn phản đối chưa xử lý đối với phương án ghi. Việc dừng phản biện SPEC không xác nhận G3 đã đạt.

## Mục tiêu

Hoàn thiện bằng chứng để Minh quyết khóa một bản P7(a), sau đó dùng đúng bản đó đánh giá và báo cáo tập test chính đã chia ở G1. Đây là task hoàn thiện công cụ đánh giá, kiểm dev, chuẩn bị khóa và đánh giá; không chọn lại thiết kế từ test.

Nguồn trực tiếp: [DT18 §2](../../docs/reference/sources/DT18-de-tai-va-nhiem-vu.md), [hướng dẫn cô §1/§3](../../docs/reference/sources/advisor-2026-09-23.md), [MRP RQ3/P7/§6–7](../../docs/MRP.md), [Q-211/Q-245–Q-248](../../docs/DECISIONS.md), [WHY-06/07/76/77/78](../../docs/WHY.md), [T-043 B3/B6/D8/D23](../T-043-thiet-ke-rca-m1/SPEC.md), [SPEC T-052](../T-052-t13-va-ho-so-g3/SPEC.md) và [hồ sơ 004](../../results/T-052/ho-so-g3-004.md).

DT18 cần đồ thị phụ thuộc, ánh xạ log/trace/metric, phát hiện dấu hiệu bất thường, vùng và xếp hạng; thực nghiệm công khai rồi áp dụng lên hệ bán vé. Cô yêu cầu hiểu sâu baseline, nhiều dataset, hạn chế, phương pháp đồ thị và so sánh. Task bao phủ RQ3b và phần can thiệp tính toán của RQ3d; RQ3c chỉ mô tả vùng nghi ngờ. Q-245 hoãn M1(b), nên RQ3a và Precision/Recall/F1 phát hiện công khai chưa được trả lời. Không có nhãn vùng độc lập thì chưa kiểm độ đúng vùng ảnh hưởng. LLM, quan hệ messaging/data đầy đủ và FlashTicket thuộc P8–P10; báo cáo G4 phải khai các phần thiếu này.

T-052 đã nghiệm thu phần dev và hồ sơ theo LOG Phiên 12; không mở lại nghiệm thu hoặc tính lại toàn bộ. Chỉ tính lại phần cụ thể khi provenance/parity chỉ ra không dùng được hoặc cần để kiểm tuyến mới. Nền giữ E1-U, E2-C, E5, z+S1, E6a, cạnh quan sát; E3(a)/E3b/E6b/E9/T12 tắt ở vế chính. E3 tắt vẫn giữ log lỗi cơ bản. T12-on là vế riêng. Giữ cờ đánh đổi E2, VC×E5 và chiều PageRank đảo OPEN. Cấu hình hiệu lực giữ epsilon=0,05, alpha=0,01; `nhanh_z=True`; `che_do={cong_phan_vi:G3,cong_dem:D1,thang:E4+T4c}`; `tach_cd3=True`. Ghim toàn bộ tham số từng vế theo `giao-thuc-p7-a-003.json#/configurations`, không lấy mặc định runner.

Nút chấm là dịch vụ/thực thể sau alias; cạnh gọi quan sát hướng caller→callee. Log/metric gắn owner; trace giữ span cha–con, operation và thời gian. E1 trừ hợp khoảng con khỏi span cha, không gọi kết quả là CPU time. E2-C tạo bằng chứng cạnh từ span bọc và span phía nhận đủ điều kiện, gán về callee. E5 dùng chiều cạnh/SCC trên miền đã khai để phân lớp; E6a xếp tầng/khóa; E7 duyệt cạnh từ tập đầu để tạo hai vùng. Graph gộp không thay index request/span.

## Câu hỏi, bằng chứng và quyết định

| Câu hỏi và nguồn | Lựa chọn/giải thích khác | Phép kiểm và bằng chứng | Hỗ trợ, bác bỏ hoặc chưa phân xử | Phần thiếu và quyết định phụ thuộc |
|---|---|---|---|---|
| Đủ khóa G3(a)? MRP §7, B6, hồ sơ 004 | Công thức đúng nhưng ghép sai nguồn, kết quả hoặc nhãn; hoặc toàn chuỗi đúng | Ba liên kết thành viên→nguồn/mốc, đầu vào thực chạy→bản ghi, seal→nhãn/ô; phản ví dụ và pilot toàn tuyến | Chỉ gỡ điểm chặn khi đường đúng đạt và đường sai bị chặn | A/B1/B2/C, môi trường, revision, nguồn cấp và quyền riêng |
| M1 đạt E-04 TT? Q-246 | Đạt/không đạt; ít ô/CI suy biến giới hạn suy luận | 60 ca, TORAI B ba seed, bootstrap cặp theo ô, cận làm tròn | Giữ biên 0,05 và cách đọc đã quyết; không chọn world | Chưa có kết quả test; không coi dev là độc lập |
| Hit@5 OB đổi thế nào? Q-246 | Cải thiện/không cải thiện hoặc chưa phân xử | 34 ca, M4, đảo dấu nguyên ô và chuyển mức từ TT tại P | Mức danh nghĩa phụ thuộc điều kiện từng phép | Giới hạn tái lập M4 theo Q-192 giữ nguyên |
| Bỏ quan hệ/thành phần làm đổi gì? RQ3d, D23 | E1/E2/E5, quy tắc ưu tiên hoặc thông tin thay cùng | Cặp đúng ca/cửa sổ/world, trung gian, ca giúp/hại và đối chiếu | Chỉ nói về bỏ thành phần khỏi chuỗi đã chọn; C-a1 còn E1 | Không khẳng định topology thật hoặc hơn nhánh không quan hệ được chọn độc lập |
| T12 đổi gì? D8 | Cạnh bổ sung đổi phép tính, nút không quan sát hoặc snapshot khác revision | Quan sát↔quan sát∪snapshot; cạnh/F_I/tầng/hạng/vùng | Chỉ hai snapshot cụ thể, E1/E2 vẫn từ span | Revision benchmark và quan hệ thiếu hai đầu còn OPEN |
| C-e có ưu tiên lặp một thực thể? WHY-77 | Tập trung hạng đầu, hòa lớn hoặc thiếu lịch sử | Tối đa 60 cửa sổ TT, top mass/returned/O/U/V0/N1; root tương lai ghép sau | Mô tả, không hiệu chuẩn detector hoặc xác nhận nền khỏe | H theo hỗ trợ lịch sử được kiểm, không suy từ tên ca |
| Ba máy giảm đường găng? Q-42/243/244, chỉ đạo Minh | Cloud giúp phủ nhánh hoặc setup lớn hơn tiết kiệm | Lô cần thiết, parity nguồn, toàn chi phí chuyển/hash/prepare/run/receive/score | Dùng cả hai EC2 cho lô đủ quyền và có ích; không tạo việc để giữ máy bận | Pilot-plan và số đo local sau dọn; ETA/chờ người tách riêng |

## Đầu vào

Trước tái dùng, kiểm hash theo manifest đúng lượt và trường thật sự cần. Hash chỉ chứng nhận đúng file, không thay tính đúng hay provenance. HEAD đơn lẻ không đại diện cây làm việc có thay đổi.

- G1: `results/T-021/goi-g1.md`, `chia-theo-o/A-phan-tang.csv`, mức tiếp xúc/vị trí và `results/T-052/ke-hoach-tap-test.json` (`/G1_source`, `/cohorts`, `/inventory`).
- Baseline: `results/T-022/giao-thuc-v2.md`, cấu hình/allowlist/nhãn dev; T-024/T-026/T-034 cùng manifest và bản ghi nguồn, giữ variant/seed/hòa/cửa sổ.
- P4/P5: `results/T-041/bao-cao.md`, `bang-chung.jsonl`, manifest; `results/T-040/ban-giao-p6.md`; snapshot T-038/T-039 và hợp đồng hiện hành.
- Thiết kế P6: T-043 đặc tả/hợp đồng/B6/đính chính, T-044 đính chính cài đặt; chuỗi T-048/T-053→T-049→T-050→T-051 và lý do nền hiện hành.
- Parity: T-024/T-026, native T-053, T-051; C-c/C-g dùng `results/T-050/doi-chung-003.json`, `cham-002/cham.json`, `manifest-chay-lai-002.json`. Không bỏ T-050 khỏi danh sách tham chiếu.
- Hồ sơ T-052: `manifest-dinh-chinh-g3-004.json`, `giao-thuc-p7-a-003.json`, bảng dev/native/seal, biên nhận F3 và lịch sử sửa. Pin LOG/STATE của manifest 004 là lịch sử trước nghiệm thu, không yêu cầu khôi phục file hiện hành.
- Máy: pin T-048/T-051/T-052/T-053; đo lại RAM/đĩa sau Minh dọn. Không dùng mốc D còn 65 GB trong AGENTS thay hiện trạng.
- RE3: chỉ metadata/schema được phép; chưa tải/mở telemetry. Adapter hiện chỉ RE2-TT/Nezha-OB, không suy hỗ trợ RE3 vì cùng RCAEval.

### Khối lượng: ca, cửa sổ, lần gọi và world

Ca là thành viên G1; cửa sổ không phải ca mới. Ô là `(dataset,root,fault)`. Lần gọi dưới đây là call/worker thật theo mã, không nhân world nếu lõi tính chung.

| Dataset | Dev ca/ô | Test chính ca/ô | Giữ ngoài ca/ô | Vai trò |
|---|---:|---:|---:|---|
| RE2-TT | 30/10 | 60/20 | — | Chính TT |
| Nezha-OB | 22/13 | 34/20 | — | Chính OB |
| RE3-OB | — | — | 30/10 | Bản cuối, quyền riêng |
| Eadro-TT | 27/27 | 54/54 | — | Không tự nhập lại thực nghiệm; Q-83 |

Đếm bằng CSV G1, đối chiếu kế hoạch test T-052. Test chính 2 dataset/94 ca/40 ô; dev 52 ca/23 ô. T13 có 82 cửa sổ = 52 thật + 30 TT giả nhưng chỉ 52 ca. C-e P7 tối đa 60 cửa sổ thêm trên 60 ca TT; H là số đủ lịch sử, 0≤H≤60. Dev + test = 146 ca; thêm RE3 = 176. So với 94 test chính, 146/94≈1,553 và 176/94≈1,872: **số ca duy nhất chưa hơn gấp đôi**.

| Dataset × vế | Ca × cửa sổ × seed × vế | Call/slot | World/chuẩn bị/đầu ra |
|---|---:|---:|---|
| TT: BARO, SimpleRCA, MicroRank, TraceRCA, CIRCA | 60×1×1×5 | 300 | Baseline cố định |
| TT: TORAI B | 60×1×3×1 | 180 | Seed 0/1/2; gộp trong ca |
| OB: sáu baseline | 34×1×1×6 | 204 slot | 136 gọi lõi; 68 UNSUPPORTED CIRCA/TORAI, không import/chạy lõi |
| Hai bộ: M1 và bỏ E1/E2/E5 | 94×1×1×4 | 376 | Mỗi call tính P/S_lo/S_hi |
| Hai bộ: C-a0/a1 | 94×1×1×2 | 188 | Ba world/call |
| Hai bộ: T12-on | 94×1×1×1 | 94 | Ba world/call |
| TT: C-e M1 cuối | H×1×1×1 | H≤60 | Ba world được tính, báo C-e P theo hợp đồng; 60−H dòng hỗ trợ riêng |
| Hai bộ: C-d1/d2 | 94×2 | 188 dẫn xuất | Có trong extra M1 tại P, không gọi lại M1 |
| TT: C-d3 | 60×1 | 60 worker riêng | Sau seal hạng chính |
| OB: C-d3 | 34 dòng hỗ trợ/mô tả | 0 solver mới | Không biến 22 NO_TARGET dev thành 34 kết quả test đã quan sát |
| Hai bộ: C-c/C-g | 94×2 | 188 dẫn xuất | Baseline+graph M1, chỉ P |

Nguồn tính: giao thức 003 `/matrix`, `/configurations`, `/C_e`, `/Cd3`; `p7_entry_v2.run_baseline`; `src/m1/chuoi.py` WORLDS/extra; T-043 D5/D8/D23. Baseline có 684 slot/616 core; M1-family có 658+H call, tạo 1.974+3H world rankings. Cộng baseline slot + M1-family + C-d3 TT = 1.402+H, tối đa 1.462 đơn vị, chưa tính prep TORAI. Bỏ 68 slot không gọi lõi OB: 1.334+H, tối đa 1.394. So với **94 lượt một phương pháp×một cửa sổ×một seed/ca**, (1.402+H)/94≈14,915–15,553, hơn gấp đôi trong đúng phép so này; không suy tỷ số thời gian.

| Việc chuẩn bị/chấm/tái dùng | Đếm hoặc công thức | Điều kiện/giới hạn |
|---|---|---|
| TORAI B hiện tại | 180 prep+180 core | v2 lặp prep trong từng seed |
| Ứng viên cache TORAI B | 60 prep+180 core | Kiểm trên laptop: byte CSV %.17g, hash nguồn/cửa sổ/config/env/transform và độc lập seed; chưa kiểm driver mới |
| CIRCA TT | 60 call→120 native records | RHT+DA chính và RHT-only phụ cùng lượt |
| MicroRank | full+top11 cùng call | Chấm phụ, không chạy lại |
| SimpleRCA M4 | 1 call/ca | M4 là tên quy ước, không phải bốn lượt |
| Baseline ở S_lo/S_hi | Kết quả cố định | Không nhân ba core call |
| Native baseline tuyến 003 | 540 TT+204 OB=744 records | 684 dòng chính; 60 CIRCA phụ, theo cấu trúc thành công/hỗ trợ khai trước |
| Hàng chấm P sau gộp seed | 18×94=1.692 | Gồm dòng thiếu hỗ trợ đã khai, không đồng nghĩa solver chạy |
| Hàng chấm S_lo/S_hi | 2×13×94=2.444 | 6 baseline cố định+7 M1-family |
| Tổng hàng chấm ma trận | 4.136+H C-e tại P | Không là số call phương pháp; variants phụ ghi riêng |
| CI/nhóm/bản loại lỗi | Theo cặp/nhóm khóa trong matrix | Số ca/ô còn lại phụ thuộc trạng thái; dùng mẫu chung nơi cần so |

TORAI B là baseline chính; TORAI A là bảng phụ ngoài A4 theo giao thức baseline đã chạy và lời Minh xác nhận lại trong LOG. A thêm 180 core và 180 prep theo hiện trạng, hoặc 60 prep sau parity; nguồn CSV A cho đúng ca dev-a5cabe5fa7 đã được cấp để pilot; nguồn A của cohort chạy chính vẫn chờ quyền riêng, không chọn lại A hay B. RE3 biết 30 ca/10 ô nhưng vế/seed/cửa sổ/support chưa khóa: Σca×cửa_sổ×seed×vế, world theo ngữ nghĩa lõi/adapter. Vị trí N dùng C-a0 đã có, **không dự toán mặc định thêm 94 K-R0**. Pilot là tập phủ nhánh liệt kê trước, không phải toàn 52 dev×toàn ma trận; retry cộng attempt thực riêng.

## Đầu ra

Lượt ghi SPEC này chỉ tạo SPEC/LOG, hồ sơ nguồn/đáp phản biện và manifest; nối Q-250/WHY-78 và dòng STATE. Các đầu ra công cụ sau đây thuộc quyền triển khai Minh đã cấp sau lượt ghi SPEC; thực nghiệm vẫn theo đúng miền và các quyền riêng đã ghi trong LOG.

| Đường dẫn trong results/T-054 | Nội dung |
|---|---|
| protocol.json | Ứng viên/LOCKED phân biệt; giả thuyết, nguồn cấp, lỗi, thời gian và diễn giải |
| matrix.json | Slot/cặp, config/seed/world, chuẩn bị/dẫn xuất, hỗ trợ/mẫu số, bảng khối lượng |
| source-manifest.json, environment.json, reuse.json | Code/thư viện/revision/blob; môi trường từng máy; trường tái dùng và kiểm tương đương |
| pilot-plan.json | Ca dev mờ, máy nguồn từng cửa sổ, tham chiếu, phủ nhánh, cold/warm, worker và trần |
| ho-so-g3.md | B6/sáu câu G3, A/B1/B2/C, tiếp xúc và phần còn chặn |
| runbook.md, authorization.json | Vận hành/quyền có nguồn; không tự sinh quyền |
| scripts/p7.py | CLI preflight/plan/run/status/drain/resume/verify/report |
| scripts/nguon.py, worker.py, bien_nhan.py | Nguồn/nhãn/support/vị trí N; đọc/cắt/chạy/phát pha; binding/attempt/seal |
| scripts/dieu_phoi.py | Queue bền đơn máy, partition cố định, tài nguyên và resume |
| scripts/cham.py, fixtures.py, pilot.py, lap_ho_so.py | Toàn ma trận/A4; phản ví dụ/diễn tập; pilot đúng driver; xuất báo cáo/hồ sơ |
| runs/<run-id>/ | Plan, mọi attempt/event/PID/stdout/stderr/cost, intermediate/output/seal; cả lượt hỏng |
| runs/freeze-<id>/ | Gói đúng byte code/metadata được phép, manifest từng file/gói; không gồm data/nhãn riêng |
| reports/<report-id>/ | JSON/CSV, báo cáo, nhóm/ca và OPEN; giữ bản đầu, không ghi đè |
| manifest-<lượt>.json | Pin và lineage từng gói; không ghi đè |

Bản đồ thật/nhãn riêng đề nghị ở `D:/RCA-ext/private/T-054/`: mỗi dataset có `case-source`, `runtime`, `runtime-binding`, `labels`, `label-binding`. Chỉ tạo sau quyền materialize; không vào git/gói cloud. Repo giữ schema/recipe/hash/con trỏ được phép. Báo cáo có hạn chế xác nhận/điều kiện; dữ liệu/đầu vào, giao thức, adapter/cài đặt, giả định phương pháp và giải thích khác tách riêng; quan hệ có thể bổ sung gì, chưa coi là đã giúp; phần thiếu và yêu cầu quan sát P9/P10.

## Phạm vi ghi

**Bổ sung Minh duyệt 07/11/2026 — chuẩn bị013.** Duyệt sửa `results/T-054/scripts/{p7,nguon,dieu_phoi,cham,fixtures}.py`, ghi `results/T-054/runs/chuan-bi-main-013/`, cập nhật SPEC/LOG và đúng dòng STATE, nối DECISIONS/WHY cùng hồ sơ G3/runbook. Duyệt SSH/dựng môi trường/fixture và đúng pilot dev cần bổ sung trên 16.176.181.251 và 13.236.44.106, vùng `/home/ubuntu/rca-p7/T-054/checkpoint013/`. Tải thêm ≤2 GiB/máy, fixture/dev ≤60 phút/máy. R1 chỉ đổi metadata và công thức chuẩn bị trước grant dữ liệu. D1–D4/R3 theo DECISIONS cùng ngày. TORAI A giữ một plan laptop, quyền theo slot, phát sau toàn phần khác A VERIFIED; thiếu quyền/sai pin A ghi chặn đúng slot, lỗi A chưa rõ giữ lượt và dừng A. Đủ A4 và snapshot mới được chấm, thiếu A không bình quân seed sống. Nguồn quyền chuẩn bị không mở test/main/RE3 hoặc commit/push.

**Đầu ra chuẩn bị013, chờ phản biện bản cài:** `runs/chuan-bi-main-013/candidate-validation.json` kê EC2_1=448job+2support/2worker, EC2_2=450job/1worker, laptop=742job/2worker tối đa. Hai EC2 mới30TT/máy; laptopOB/CIRCA/MicroRank/A. `protocol-candidate.json`, source-bundle, contract và placement013 thay ứng viên011 cho lần xin khóa tiếp theo, vẫn CANDIDATE. Mỗi EC2101fixture mã cuối;15đối chiếuDEV mới với14khớp nghiêm ngặt và một C-e sai khác số học Minh đã duyệt đúng phép. D1/D2/D4 theo DECISIONS ngày07/11 và báo cáo013; H1 chưa có nguồn, không mở RE3. Mọi điều kiện nguồn/quyền main vẫn chờ quyết định cuối, kể cả nguồnA và truyền test. Không lấy mã003/005/011 để phát013.



**Bổ sung Minh duyệt ngày 07/11/2026:** phần A trong `results/T-054/runs/hoan-thien-local-g3-011/h1-bo-sung-xin-duyet.md` cho sửa `src/p3/re3.py` và `results/T-054/scripts/worker.py` để nhận nghĩa mã gRPC tường minh, giữ kernel/tổng mã native và mặc định TT/Nezha; nối WHY/DECISIONS. Phần B cho đọc duy nhất column chunk (khối cột) `serviceName` của 30 trace và `container_name` của 30 log RE3 HF đúng revision; tổng metadata và chunk không quá 16 MiB. Chỉ xuất hợp tên toàn cohort, không phân bố theo ca hoặc tín hiệu/thời gian/message/ID/operation/statusCode. Đây là quyền metadata inventory riêng, không mở đánh giá RE3/G3/main. Snapshot và biên nhận ở checkpoint011.

**Bổ sung CIRCA Minh duyệt06/11/2026:** “Duyệt bổ sung 2 file CIRCA”; thêm `results/T-054/scripts/dieu_phoi.py` và `bien_nhan.py` đúng ba điều kiện theo010/bo-sung-circa-xin-duyet.md, nhận/kiểm hai variant/current và tạo hai bản ghi TIMEOUT cho RE3 như TT. Không nới quyền dữ liệu/chính sách lỗi/deadline.

**Bổ sung Minh duyệt H2 ngày06/11/2026:** “Duyệt cài H2 theo báo cáo009”. Cài đúng9file: `src/p3/re3.py` (mới), `src/m1/adapter.py`, `src/p3/adapters/baro.py`, `circa.py`, `tracerca.py`, `torai.py`, `results/T-054/scripts/nguon.py`, `worker.py`, `cham.py`; cập nhật đúng lý do/quyền vào WHY/DECISIONS. Reader và M1 RE3 nhận profile thời gian/U/alias/r tường minh đã ghim, thiếu thì chặn trước method; default TT/Nezha giữ nguyên. Worker/grant/bảng RE3 riêng, kiểm bằng synthetic; chưa mở telemetry/đánh giá RE3 hoặc G3/main. Không sửa lõi M1/cấu hình đã chọn, không quyết các trường H1 còn OPEN. Snapshot trước sửa và kiểm ở checkpoint010.

**Bổ sung Minh duyệt có điều kiện ngày06/11/2026:** cài đúng bản vá source_native trong báo cáo007: `src/p3/nezha.py`, `src/m1/adapter.py`, `src/m1/chuoi.py`, `src/p3/adapters/nezha.py`, `results/T-054/scripts/worker.py`; thêm lý do/quyền vào WHY/DECISIONS và lưu bản SPEC trước sửa ở checkpoint008. Reader/adapter mặc định legacy; workerT054 bật layout rõ choOB, không thay TT/nền/ca/seed/statistics. Giữ mẫu và timestamp từng nguồn; mapping phải kiểm đủ; BARO per-source giữ preprocessing/kernel và quy tắc hòa. Chỉ nhận tuyến mới hợp lệ sau kiểm synthetic/dev đủ trường. Đây là ngoại lệ có phạm vi cho câu không sửa src bên dưới; không sửa task lịch sử. Lưu mọi lượt, đổi pin/binding/plan sau code; chưa mở G3/main/telemetryRE3 hoặc commit/push.

- Hiện tại theo Q-250: `tasks/T-054-khoa-g3-chay-p7-a/SPEC.md`, LOG; `results/T-054/runs/soan-spec-001/` và `manifest-soan-spec-001.json`; nối Q-250/WHY-78, thêm đúng dòng T-054 STATE.
- Sau quyền triển khai riêng: đúng các file/nhóm results/T-054 liệt kê ở Đầu ra, LOG và dòng task STATE. Sổ DECISIONS/WHY chỉ nối quyết định Minh thật sự duyệt, không biến OPEN thành DECIDED.
- Vùng private local chỉ sau quyền dữ liệu. Sau quyền SSH/sync: vùng task riêng dự kiến `/home/ubuntu/rca-p7/T-054/` trên từng EC2, code/env và TT dev allowlist cụ thể. Không mirror cả repo/data.
- Không sửa src, T-052, AGENTS, MRP hoặc nguồn lịch sử. Wrapper task mới dùng API hiện có; nếu cần sửa lõi thì dừng đúng nhánh, trình file/patch/ảnh hưởng/phép kiểm.
- Reviewer chỉ ghi lượt được Minh cấp; bản chat Claude lưu nguyên văn làm nguồn, không tạo REVIEW.md đứng tên Claude.

| Nguồn → thay đổi kế hoạch | Vì sao | Ảnh hưởng |
|---|---|---|
| Helper T-052 → driver T-054 | Ba liên kết và toàn ma trận còn thiếu | Đánh giá mới, giữ kết quả T-052 |
| Payload rời → envelope tại tuyến thực chạy | Tránh gắn nhầm ca/config/window | Seal/nhãn/mẫu số/A4 |
| Pending/live RAM → queue/attempt bền đơn máy | Chạy độc lập agent/SSH, tránh chạy đôi | Resume, không dựng queue phân tán động |
| Quyết định trước G3 | Không chọn sau test | B chính/A phụ đã có; nguồn A và chính sách/trần thời gian còn cần đủ trước phần phụ thuộc |
| STATE/sổ | Lưu nguồn duyệt và trạng thái | Cập nhật sau nguồn quyết định; giữ dòng task đã đóng |

## Các bước

### Pha 1 — Hoàn thiện điều kiện để trình khóa G3(a)

1. **Nguồn/quyền/tái dùng.** Kiểm manifest/revision/cây thực chạy, lập reuse theo từng trường; đọc code/trung gian trước chạy thêm. Giữ dev đã hợp lệ. Ghim snapshot/U/alias, code ngoài repo và nguồn cấp nhãn; chốt OPEN ở phần cuối trước phần phụ thuộc. Không suy quyền chạy từ quyền ghi hồ sơ.

2. **Liên kết A/B1.** Giữ guard v3, thêm ba đối chiếu:
   - Thành viên G1→đúng locator/byte/hash/t hoặc t_ns/trace_guard/cửa sổ/C-e support. Nguồn riêng do Minh/người quản lý được chỉ định cấp; không lấy hash runtime tự khai làm provenance độc lập.
   - Đầu vào đã đọc/cắt/chuẩn hóa→kết quả: worker đóng normalized-input digest, nguồn, config hiệu lực/env/seed/token cùng kết quả tại tuyến thực chạy trước khi controller nhận. Controller không gắn mã ca mù vào payload rời. TORAI nối prep/bảng CSV/seed thực xử lý.
   - Seal→nhãn/ô: evaluator đối chiếu dataset/member/G1 revision/canonical root/fault/cell/alias với nguồn nhãn độc lập sau verify seal. Root ngoài U ở hai cohort hiện hành dừng đối chiếu nguồn, không chấm 0 hoặc mở U; root trong U vắng khỏi hạng vẫn 0. Không suy chính sách này sang RE3.
   - Fixture tráo root/ô/dataset/revision rồi rehash phải bị chặn; tráo output trước lớp gắn ca, đổi input/window/config/seed, thiếu/thừa/trùng ca/seed đều bị chặn trước chấm. Bản đúng cho số kỳ vọng. API phương pháp chỉ nhận tín hiệu/U/alias/tham số phi nhãn. Đây là kiểm lỗi ghép/provenance, không là bảo đảm chống worker cố ý giả mọi bằng chứng.

3. **Toàn tuyến B2.** Nối sáu baseline đúng variant/seed/env/window; M1/ba ablation/C-a0/a1/T12; C-d1/2 từ extra M1, C-c từ đúng BARO/M4/TraceRCA, C-g chỉ E6b sau M4. Hạng/vùng M1 seal trước C-d3; lookup TT theo `(dataset,case,arm,window,seed)` trong bundle đã verify, không chỉ số danh sách. C-d3 trả status/timeout riêng, không làm đổi seal/hạng/vùng chính. OB giữ dòng hỗ trợ theo hợp đồng, không gán kết quả dev thành kết quả test. C-e t′=t−300; insufficient đã xác minh có dòng riêng, không coi là NO_CAUSE hoặc 0 trên miền hỗ trợ; provenance chưa rõ thì BLOCKED. Vùng đủ 2 cách, kỳ vọng theo hòa, hợp vùng riêng, tỷ lệ O; O=0 thì N/A.

4. **Vị trí N và parity nguồn.** Lấy N từ `C-a0.extra.G_N` và `don_vi_phan_vi`, cùng định nghĩa nút, alias, membership N và p75/p90 của `vung_ce`. Pilot đối chiếu với K-R0 đã ghim. C-a0 thiếu trường thì vị trí N là N/A/BLOCKED; trình phần bổ sung, không tự thêm native. Bằng chứng cũ gồm 2 TT thật + 1 TT C-e + 2 OB, với 15 so sánh; không chứng minh toàn cohort.

   Mỗi vế pilot có bản tham chiếu T-024/T-026/T-050/native T-053/T-051 đúng case/window/seed/config, được kiểm pin trước khi dùng. Ghi máy nguồn **từng cửa sổ**, không gọi toàn bộ TT là EC2: native T-053 có TT thật 11 EC2/19 laptop; TT C-e 15/15; OB 9/13. Các số này dựng từ `phase1_seal` và command đã pin.

   Cùng máy/env/pin: so chính xác các trường tương ứng. Khác máy: cờ, quyết định ngưỡng, tập/tầng, khóa hòa và hạng phải khớp chính xác; số thực chỉ được khác trong dung sai khai trước và không được đổi quyết định. Ghi nguồn/chính sách dung sai; chưa chốt thì dừng. So normalized input, mẫu trung gian, trạng thái, coverage/U/O/returned, tầng/khóa/hòa/hạng và vùng/control dùng để chấm. Khác biệt chủ ý phải liệt kê trước. Parity giữa máy không thay parity với bản đã chọn thiết kế. TT driver laptop phải đối chiếu nguồn native trước test local.

5. **Pha thời gian và lỗi C.** Worker ghi bền start/end của kiểm nguồn, đọc, cắt, prep, đọc prep, method và ghi. Supervisor lưu pha/token/PID trước khi dừng. Không suy pha từ chuỗi lỗi hoặc review tự gán `method`. Hết giờ ở prep, trước worker, lỗi nguồn/adapter/runner/hạ tầng hoặc chưa rõ nguồn: dừng phần phụ thuộc trước seal. Lỗi phương pháp trên đầu vào/config hợp lệ và TIMEOUT ở pha đã khóa giữ ca/seed và tính trượt. Wrapper phải giữ variant đúng (M4, CIRCA chính/phụ rõ), không đưa sai phương pháp vào A4. M1 chạy trong tiến trình được giám sát, không làm treo controller.

   Receipt TIMEOUT bắt buộc có `max_monitor_gap_s`, nhịp giám sát, pha và ngưỡng khoảng hở khóa trước test. Chỉ đủ điều kiện xét trượt khi max_gap **nhỏ hơn** ngưỡng và mọi bằng chứng pha/đầu vào/config khác đạt; thiếu/bằng/vượt ngưỡng thì dừng phân loại. Đây là điều kiện cần, không tự chứng minh không sleep hoặc có lỗi vận hành. Khoảng trống heartbeat là mất quan sát; kiểm OS suspend/resume/boot/clock và process khi được phép. Không tự retry hoặc đổi thành method timeout. Ghim thứ tự vế/cache/reset. Đặt hạn theo cold path/pha hợp lệ, không lấy 22 s nóng thay 50 s lạnh. Timeout từng pha/vế và trần method×dataset phải có số trước LOCKED; còn null/OPEN thì không phát test.

6. **Thống kê và diễn giải.** Giữ Q-246: TT 60 ca, MRR M1−TORAI B, seed 0/1/2 bình quân trong ca; bootstrap cặp theo ô 10000 mẫu, seed 20261005. Lưu CI thô và cận 12 chữ số ROUND_HALF_EVEN, strict lo>−0,05; bằng biên không đạt. OB 34 ca, Hit@5 kỳ vọng M1−M4, đảo dấu nguyên ô một phía tại 0; mức 0,025 nâng lên 0,05 chỉ khi E-04 tại P qua và CI làm tròn lo<hi. Chỉ P điều khiển; S_lo/S_hi dùng mẫu chung là độ nhạy. McNemar phụ dùng tiêu chí chắc hạng 1, TORAI≥2/3 seed; all3 là độ nhạy. Báo ô hữu hiệu/khác 0/thua/lẫn chiều/ca cả hai trượt, ít ô, bootstrap undercoverage và giả định hoán đổi. Mức chỉ là danh nghĩa.

   Minh đã chốt cả hai công thức ngày 05/11/2026 (runs/trien-khai-004/quyet-dinh-minh.json): (i) bản loại lỗi loại nguyên cặp nếu M1 hoặc bất kỳ seed baseline có ERROR/TIMEOUT phương pháp đủ điều kiện; giữ NO_EVIDENCE/UNSUPPORTED, không bình quân seed sống; tính lại mô tả/CI, báo n/ô, rỗng thì N/A, không điều khiển chuyển mức; (ii) hoán vị ca TT hai phía, 10000 lần đổi dấu, seed 20261005, cộng 1 vào tử/mẫu, chỉ là độ nhạy, không thêm mức bác bỏ. Nghĩa vụ bản loại lỗi Q-211(6) đã có; hai công thức đã được Minh chốt, gói G3 chưa khóa. Fixture gồm đúng biên, p tại ngưỡng, CI suy biến, ít ô, ô khác cỡ, seed lỗi, cả hai trượt và world cho cách đọc trái nhau.

   Bảng diễn giải giữ tiêu chí Q-246:

   | Điều kiện | Diễn giải |
   |---|---|
   | TT lo>0 | Hơn TORAI B theo CI danh nghĩa, kèm giả định và số ô |
   | TT lo>−0,05 nhưng CI toàn âm | Đạt biên E-04 theo công thức dù kém TORAI B theo CI |
   | CI chứa 0 | Chưa phân biệt hơn/kém; đọc E-04 riêng theo cận dưới |
   | TT lo≤−0,05 | “Không đạt E-04. Chưa chứng minh được không thua quá 0,05” |
   | CI suy biến mà qua biên | Ghi cùng câu “đạt E-04 theo công thức; CI suy biến”, kèm số đếm; không nâng mức OB |
   | M1 hơn baseline nhưng thua C-a hoặc C-d2 | Giới hạn theo cặp; không khẳng định lợi ích quan hệ chung |

7. **Fixture và pilot đại diện.** Tái dùng bảng/dev/native/fixture phù hợp từ T-052. F3 chỉ gồm hai ca/seed 0 sau selector, không thay driver/guard mới. Pilot-plan chọn theo nguồn dev trước khi chạy: TT nhẹ/nặng thật/C-e, nhánh E1/E2/E5 đổi và ca đối chiếu không đổi; OB E2 giúp/C-d2 đổi và ca đối chiếu; T12 đổi/không đổi vùng; đủ 3 seed TORAI trên ca đại diện; kiểm A ở bảng phụ sau grant nguồn riêng; không chọn lại baseline. C-d3 gồm hỗ trợ/chu trình/thiếu đích. Dùng dữ liệu giả cho lỗi nguồn/timeout, C-e thiếu lịch sử/O=0/world nếu dev không chạm nhánh. Chạy bundle từ chọn nguồn→prep→method→seal→nhãn dev→bảng; mỗi tuyến khác có kiểm nguồn. Nhánh kiểm bằng mẫu giả không được gọi là đã kiểm thật. Dùng chính lượt pilot mới so với các tham chiếu ở bước 4; không nhất thiết thêm lượt.

   Theo gói thu gọn Minh duyệt ngày 05/11/2026: giữ các pilot một worker và baseline G2 đã hợp lệ làm tham chiếu; chỉ đo thêm 2 worker để chọn cách ổn định. Không yêu cầu thử 3/4 worker hoặc săn cấu hình nhanh nhất. Không chạy lại baseline dev diện rộng; lượt bổ sung phải gắn với lỗi/phép đối chiếu cụ thể chưa giải quyết. Driver dùng slot độc lập; cache liên vế là tối ưu hiệu năng, không là điều kiện khoa học để mở test. Chưa có lợi ích đủ căn cứ thì không dựng cache phức tạp. Byte prep TORAI/seed đã được kiểm trên laptop ở checkpoint003, không lặp chỉ để đo thời gian. Chỉ kiểm phần vận hành mới thay và tuyến C-e còn thiếu. Mọi lượt lỗi giữ nguyên; lượt hơn một giờ vẫn cần quyền theo AGENTS.

8. **Hồ sơ khóa.** Gồm B6/sáu câu G3, code/env/revision/gói đúng byte/config/cohort/U/alias/seed/world/errors/fallback/timeout/mẫu số/statistics/diễn giải/tiếp xúc/lịch/budget. A/B1/B2/C có bằng chứng hoặc điểm chặn rõ. Khóa gói byte thực chạy, hash gói/từng file và blob Git/provenance; không lấy checkout mới khác EOL làm nguồn. Tách `code_root`, `data_root`, `output_root`; gói code không kéo theo data/nhãn. Reviewer kiểm hồ sơ bằng prompt chuẩn, Minh chuyển thủ công. Script dừng WAIT_G3 rồi WAIT_TEST_GRANT nếu thiếu quyết định. Chưa có quyền commit thì chưa commit.

### Điều kiện chuyển pha

Đồng thời cần: Minh duyệt G3(a) đúng code/gói/config/env/matrix; nguồn có thể tái dựng và revision thực chạy được ghim (commit khi Minh duyệt riêng); grant đúng 60 TT + 34 Nezha/cửa sổ/vế/chấm; TORAI A/nguồn cấp/lỗi/ngân sách/độ nhạy/timeout/maxgap đã chốt; môi trường từng máy/pilot/tài nguyên đạt; không còn OPEN làm đổi phép so/mẫu số. RE3 và truyền test lên cloud không được suy từ các quyền này. Chưa đủ thì script dừng đúng mốc, không tự qua theo thời gian hoặc đồng thuận reviewer.

### Pha 2 — Chạy P7(a), kiểm và báo cáo

9. **Materialize theo quyền.** Lớp quản lý dựng nguồn/runtime/nhãn riêng từ đúng G1, kiểm collision mã mờ, revision/locator/byte/hash/unit/schema/alias/window. Nezha chỉ dùng miền được cấp và guard đúng; không mở ngoài cửa sổ. Lập mọi slot, cả thiếu hỗ trợ, trước chấm; không bỏ sau khi thấy điểm. API phương pháp không nhận case/path/root/fault/cell. Mốc tiêm dạng số được phép ở (a). Ghi mọi lần xem test, tách “đã xem” và “đã dùng để thiết kế”.

10. **Thực thi/kiểm/seal.** Bundle cùng ca/cửa sổ và các vế chung cache; giữ thứ tự/cold policy đã khóa. Cặp nhạy số học dùng cùng môi trường nếu parity chưa đủ. Giữ seed/variant và mọi attempt/raw status/intermediate/cost. Kiểm source/binding/schema/đủ trường chấm/hòa/U/O/returned và phân loại lỗi trước seal. Output tạm→flush/fsync phù hợp→atomic rename→seal; file tồn tại không có nghĩa đã xong. C-d3 chỉ chạy sau seal hạng chính; lỗi không đổi hạng/vùng. Nhánh độc lập đủ quyền có thể tiếp tục tính phi nhãn khi nhánh khác BLOCKED.

11. **Snapshot và thời điểm ghép nhãn — tiếp nhận N1.** Đóng snapshot toàn ma trận đã đăng ký: mỗi slot có kết cục hợp lệ cuối hoặc BLOCKED có lý do. BLOCKED không là trạng thái phương pháp. **Còn slot A4 ở trạng thái BLOCKED hoặc PENDING thì chưa ghép nhãn cho bảng nào; trình Minh quyết.** A4 phải đủ 60 TT/34 OB và seed theo hợp đồng, không chấm trên tập con.

   Chỉ sau verify snapshot/seal/label-binding và đủ A4 mới cho evaluator ghép nhãn/xuất bảng đủ nguồn. Ghi bền mốc ghép/chấm và mốc người làm/Minh/agent lần đầu xem độ đo. Đây là mốc evaluator/độ đo, không xóa tiếp xúc metadata G1. **Slot ngoài A4 chạy sau mốc xem, đúng pin và không đổi code, được báo là “chạy sau khi đã xem”; đổi code thì báo theo C-15 B.** Không lặng hoàn thiện nhánh lỗi sau khi xem rồi gọi là trước test. Các bảng ngoài chưa đủ vẫn BLOCKED; toàn task chưa xong. Ưu tiên chạy A4 không tự cho phép nhìn điểm sớm; lịch công bố theo bậc khác cần Minh quyết trước G3.

12. **Chấm và diễn giải.** Báo theo dataset/fault/ô/vị trí N/ca/world; MRR, NDCG@5, Hit@1/3/5, AC@k/Avg@5; kỳ vọng hòa và bảng RCAEval riêng; paired win/tie/loss, cỡ chênh/CI, status/mẫu số, bản loại lỗi và độ nhạy riêng. Báo vùng hai cách/hợp/tỷ lệ O, C-e top mass/returned/U/O/V0/N1 và root tương lai, T12, coverage và cost. Không gộp dataset. E-04 thất bại giữ câu Q-246; suy biến mà qua biên thì ghi cùng câu, kèm số đếm và giới hạn. Đọc trung gian nhóm giúp/hại/C-d2 thắng/vùng đổi cùng ca đối chiếu; không quy nguyên nhân vật lý từ vị trí tiêm/tương quan. Thiếu trung gian thì trình đúng phần bổ sung/phạm vi/chi phí/quyết định phụ thuộc, không tự chạy vượt quyền.

13. **Sửa sau test/kết thúc.** Kết quả đầu bản khóa là chính, giữ nguyên. Khi có lỗi, bảo toàn attempt/seal/phạm vi; tách cài đặt và thiết kế; trình patch/vế chạy lại/quyền trước sửa. Bản sửa dùng test phải khai/báo riêng, không gọi là kiểm độc lập. Kiểm độc lập cần dữ liệu phù hợp chưa dùng sau khóa, gồm lượt FT mới. RE3 chỉ mở riêng một lần cho bản cuối, chưa được phát lô ở đây.

### Điều phối qua đêm và bàn giao

Plan bất biến theo dataset/member/case/window/arm/seed/config/source/env; world ghi tính chung hoặc chấm dẫn xuất. Attempt tăng dần, token/thư mục riêng. Một supervisor/partition cố định trên mỗi máy; claim bằng tạo độc quyền/khóa OS, không giành lease chỉ vì heartbeat cũ. Không dùng queue phân tán/chuyển việc động. Chuyển partition cần xác nhận chủ cũ dừng, đủ quyền và parity.

Trạng thái bền gồm PENDING, RUNNING, COMPLETE_UNVERIFIED, VERIFIED, BLOCKED, FAILED_OPERATIONAL và các mốc WAIT quyền; dựng từ event/receipt, không từ một JSON viết dở. Worker/supervisor tách khỏi phiên agent/SSH. Windows khởi chạy ẩn, Linux dùng detached process/service khi được phép. Giữ CPU/RSS/I/O cả cây, đĩa và pha. Kết quả hạng chính và C-d3 có seal riêng.

| Khi tiếp nhận | Hành động |
|---|---|
| PID + creation time + command hash + token đúng, còn sống | Adopt, không phát bản sao |
| Output/receipt/schema/hash/seal đủ hợp lệ | VERIFIED, bỏ qua |
| Process chết, file dở | Giữ attempt, phân loại trước retry |
| Chưa có bằng chứng khởi chạy | PENDING |
| Không xác minh được chủ/output | BLOCKED, chờ kiểm, không đoán |

Retry đề nghị tối đa 2 retry/3 attempt, chỉ cho lỗi vận hành tạm thời đã phân loại, cùng pin. Schema/hash/permission/config/phase unknown không auto retry. Method error/timeout đủ điều kiện không retry để tìm điểm tốt. Ngưỡng/hạn cuối cùng cần Minh duyệt trước phát lô.

Diễn tập bằng ca giả: lỗi nguồn, timeout trước method/trong method, file dở, controller restart, SSH ngắt khi worker đang chạy và hai controller cùng claim. Nhận lại phải không chạy đôi/không nhận tệp dở; lỗi C-d3 không làm mất hạng chính. Heartbeat cũ hiện “chưa xác minh”. “Đã chạy ổn định” cần bundle đại diện mỗi máy tham gia qua kiểm nguồn/trung gian/output/seal, parity cần thiết đạt, tài nguyên/dung lượng đủ và diễn tập resume đạt. Chỉ PID còn sống chưa đủ.

Tự chạy qua ngắt phiên agent/SSH, **chưa tự khởi lại sau reboot**. Reboot cần Minh resume thủ công; Scheduled Task chỉ thêm khi đề xuất/duyệt riêng. Mốc sáng có điều kiện máy không reboot hoặc được nhận lại kịp. Không giữ agent hoạt động chỉ để giám sát sau bàn giao.

Một báo cáo bàn giao khi ổn định gồm: máy/partition/job/attempt, lô VERIFIED, pin, tài nguyên/ETA và phần chưa đo, lệnh status/drain/resume đã diễn tập, lỗi mới/dấu hiệu dừng, phần cần Minh và mốc WAIT nếu thiếu quyền. Minh tự kiểm khi thức. Tiến độ dễ xem có timestamp cuối/heartbeat/pha/running/verified/tổng/error/resources/phần còn lại/action.

CLI đã cài và kiểm trên fixture; plan/pin/executable thật từng máy phải được điền và kiểm trước dùng. Các placeholder dưới đây không phải lệnh phát chạy chính:

```text
py -3 -B D:\RCA-flashticket\results\T-054\scripts\p7.py status --plan <plan-local> --sha256 <pin>
py -3 -B D:\RCA-flashticket\results\T-054\scripts\p7.py drain --plan <plan-local> --sha256 <pin>
py -3 -B D:\RCA-flashticket\results\T-054\scripts\p7.py resume --plan <plan-local> --sha256 <pin>
```

`status` chỉ đọc. `drain` ngừng phát việc mới và chờ lượt đóng. `resume` verify plan/claim/process/output trước phát. Dừng khẩn cấp phải giữ attempt/receipt và phân loại. EC2 dùng SSH đúng host/executable đã ghim và cùng CLI trong vùng task. EC2 hỏng: partition dev độc lập khác tiếp tục. Laptop hỏng: lô EC2 độc lập tiếp tục theo plan đã khóa; nhận/chấm chờ phục hồi. Không tự đổi chủ lô hoặc phát trùng. Schema lạ: dừng nhánh, giữ ca/bằng chứng/bảng bị ảnh hưởng, không đoán mapping từ test.

### Lịch theo máy và phụ thuộc

Theo quyết định mới ngày 05/11/2026, P7 không còn bị bắt buộc giữ toàn test/dẫn xuất ở local. Phân bố TT/OB giữa EC2/laptop phải được lập theo tổng thời gian, điều kiện môi trường và nguồn dữ liệu thực; chưa chốt OB phải local.  Có bản sao lịch sử Nezha 154 file gồm 22 metric ngày + 66 trace + 66 log trên máy được preflight T-053; điều này không chứng minh đã đọc giá trị test hoặc có vi phạm cũ (Q-93). 34 OB test cùng hai ngày; metadata cho thấy 1/34 giao phút trace/log. Hồ sơ phải khai tiếp xúc ở mức lưu trữ/file, không coi allowlist file chỉ chứa dev. Không tự xóa/đọc raw bản sao cũ. Không gọi hai EC2 là “mới”: bước SSH đầu tiên được duyệt phải đối chiếu host key/identity và kiểm tên/hash vùng T-032 đã khai, không xem nội dung telemetry. IP/HostKeyAlias không tự chứng minh máy hiện tại.

| Lô | Máy/dữ liệu | Phụ thuộc | Worker tối đa | Tiếp nhận |
|---|---|---|---|---|
| Chuẩn bị đã làm | Hai EC2+laptop, code/DEV được cấp | SSH/env/pin | 2 | Inventory, dev nguồn khớp, kiểm resume/nhận/ghép |
| Main EC2_1 | 30 TT; M1-family210, TORAI B90, C-d3 30, C-e tối đa30 | G3/grant; prep→TORAI; M1 seal→C-d3 | 2 khi đủ RAM | 360 vị trí tối đa; TT654.702.162 byte/90tệp |
| Main EC2_2 | 30 TT còn lại; cùng cơ cấu | Như EC2_1; phân vùng không trùng | 2 khi đủ RAM | 360 vị trí tối đa; TT654.685.920 byte/90tệp |
| Main laptop | OB442 vị trí (68 UNSUPPORTED); TT5baseline300; A phụ180 | Nguồn/grant; A cần quyền CSV riêng | 2 khi đủ RAM | 922 vị trí; ưu tiên công cụ nhận/kiểm, không tạo cache liên vế mới |
| Nhận/kiểm/chấm | Laptop, compact từng host đã seal | Pin/receipt đủ; aggregate bằng đúng toàn plan trước nhãn | 1 | Nhận định kỳ vào thư mục mới; A4 thiếu vẫn chặn bảng |
| RE3 | Hợp đồng metadata pha1 đã có; schema/adapter thật còn OPEN | Nguồn/adapter/quyền riêng, bản cuối | Chưa phát | Không thuộc main94 |

Minh muốn tận dụng cả hai EC2 + laptop để giảm tổng thời gian, ưu tiên EC2 cho việc độc lập/nặng/đủ quyền. Không dựng queue phân tán chỉ để dùng máy. Đầu tiên lập job cần thiết và so setup/sync/hash/parity/receive với phần đường găng tiết kiệm. Không còn việc cloud có ích thì báo Minh có thể Stop, không tự bật/tắt hoặc Terminate. Lịch laptop đơn máy là phương án thay thế nếu không có lô cloud hữu ích; không tự bỏ chỉ đạo Minh.

Nguồn kết nối theo Minh: EC2 1 `13.211.127.97`, PEM `D:/RCA-ext/keys/keys.pem`; EC2 2 `3.107.156.186`, PEM `D:/RCA-ext/keys/key2.pem`. SSH/kiểm DEV đã thực hiện theo quyền mới; không in/nạp nội dung khóa vào log/prompt/manifest/repo. Nếu SSH từ chối do ACL, thực hiện đúng quyền Minh cấp cho bước kết nối; không sửa ACL trong lượt ghi hồ sơ. Ghim executable/Python/gói/RNG/PYTHONHASHSEED/BLAS-OMP threads 1/code upstream/số học Q-237; tách code root và data root. Runner dùng executable/PYTHONPATH theo hợp đồng từng máy; Linux wrapper dùng T025 env đã kiểm, không sửa src để chạy. Chưa đủ parity giữa máy thì cặp so dùng cùng môi trường. Minh chấp nhận riêng ba sai khác đã ghi ở numeric-parity-analysis.json: MicroRank OB một ca 1 ULP và M1/T12 một ca OB tối đa 2 ULP, các trường rời rạc đã đối chiếu không đổi. Giữ 1 luồng; không dung sai chung, không sửa/làm tròn kết quả. Sai khác mới vẫn dừng phần phụ thuộc. Ngoại lệ chỉ để chẩn đoán: Minh đã cấp một lượt MicroRank dev-607751ac0a với thiết lập luồng khác để kiểm sai khác số cuối; chưa duyệt thay cấu hình chính 1 luồng. Kết quả và giới hạn suy luận về thread lịch sử ở runs/trien-khai-003/diagnostic-thread-001/summary.json.

Số worker thực thi chỉ 1 hoặc 2 theo plan bất biến. Chọn 2 khi lô đại diện có overlap thật, output/input khớp tham chiếu và đủ RAM/đĩa; giữ một slot mỗi nhóm method×dataset để không cộng nhầm cost. DRAIN ngừng phát mới, nhận lại giữ token/PID và không chạy đôi. Không có yêu cầu đo 3/4 worker theo gói Minh vừa duyệt. Đĩa tính output nén + temp + lượt hỏng + gói nhận + dự phòng, không chỉ kích thước cuối.

Phạm vi cloud test cần cụ thể hóa trước truyền/chạy (ràng buộc local đã được Minh bỏ): chính xác ca/raw parquet/file CSV ngày-phút/CSV TORAI/feature/intermediate/ranking nào, byte, máy/thư mục/retention/quyền đọc và labels có đi hay không. “Dẫn xuất không nhãn” không tự được phép. TT parquet tách ca thuận lợi hơn OB file chung nhưng không tự có quyền. Máy local mạnh hơn là phương án khác. Chỉ chọn khi tổng chi phí thấp hơn phần local tiết kiệm và parity đạt.

## Kiểm đúng đắn

- Kiểm đúng nguồn/revision/variant và trung gian, không dùng điểm cuối khớp thay việc thành phần chạy đúng. Tái lập/kiểm phi nhãn có sẵn từ baseline dùng đúng miền; không tự nhận đã tái lập toàn bộ trong task này.
- Compact phải đủ field mới được dùng; ranking parity không chứng minh vùng/O/coverage/runtime. Cache key gồm nguồn/member/window/config/code/env/số học liên quan. TORAI prep kiểm byte CSV và tính độc lập seed trên laptop.
- Giữ khối TORAI hai cấp, hòa kỳ vọng, seed gộp trong ca, baseline cố định theo world. C-a0 bỏ E1/E2/E5/E6b/E7 trong đường hạng; C-a1 còn E1; C-d2 còn bằng chứng chuỗi; C-g chỉ E6b; D23 giới hạn ngân sách chọn tín hiệu. Không có graph random thì không khẳng định topology thật.
- Fixture tích hợp kiểm liên kết đúng/sai, không chỉ mock method; kiểm pha lỗi, timeout variant, seal-C-d3, A4 BLOCKED chặn **mọi bảng**, slot ngoài A4 sau khi xem được gắn đúng nhãn provenance. maxgap thiếu/bằng/vượt ngưỡng chặn tính trượt.
- Nguồn lỗi tách dữ liệu/giao thức/adapter-cài đặt/giả định phương pháp; cờ chồng lấn không cộng thành tỷ lệ nguyên nhân. Ghi phần thiếu quan sát vật lý/nhãn vùng/vị trí tiêm, giải thích đối lập và hệ quả FT. Không coi collector khôi phục được điều chưa từng ghi.
- Kiểm manifest, diff và file set toàn gói; giữ user changes. Hash lệch thì dừng đúng phần phụ thuộc; không ghim manifest mới thay kiểm upstream.

## Tiêu chí xong

Pha 1 đạt khi A/B1/B2/C có bằng chứng hoặc điểm chặn đúng, nguồn/code/config/env/cohort/policy/budget đủ để trình Minh khóa. Hồ sơ viết xong nhưng còn chặn là checkpoint, **không** hoàn thành cả task.

Cả task chỉ đề nghị nghiệm thu khi:

1. Quyết định G3 + grant đúng phạm vi có nguồn. Mọi slot bắt buộc có output VERIFIED hoặc kết cục hợp lệ thiếu hỗ trợ đã khóa; không đổi chưa chạy thành trượt trái quyết định budget được chọn.
2. Đủ bảng hợp lệ/ca/seed/mẫu số/seal/label-binding; không còn BLOCKED ảnh hưởng bảng bắt buộc. Giữ kết quả đầu bản khóa và mọi lượt hỏng.
3. A4 và mô tả được đọc đúng, kể cả kết quả âm/suy biến/khác dấu theo bộ/world. Phân tích quan trọng có trung gian/ca đối chiếu hoặc chỉ rõ bước chưa phân xử/bằng chứng thiếu/quyết định bị chặn. Không nhận cơ chế vật lý khi chưa có căn cứ.
4. Báo rõ ba mức: đã chạy xong gì; đủ bảng hợp lệ gì; RQ3b/d trả lời tới đâu. RQ3a, độ đúng vùng, LLM/FT và quan hệ thiếu vẫn khai ở G4.
5. LOG/manifest/runbook/báo cáo/STATE đủ để người khác, trên máy khác, không có chat nhận tiếp; diff/file set đúng. Minh nghiệm thu task/G4 riêng.

Nhánh bị chặn: vẫn xuất bản bảo toàn phi nhãn và báo cáo phần đã hợp lệ theo quyền ghép nhãn; liệt kê đúng bảng/bằng chứng/quyết định thiếu, không tự đóng task. Minh quyết bổ sung/giới hạn/đổi phạm vi. Kết quả âm/chưa phân xử có thể hợp lệ, nhưng bảng bắt buộc chưa chạy không được coi là xong.

## Không làm

- Không triển khai M1(b)/detector/LLM/GNN/đảo PageRank/chọn lại nền từ test; không dựng nhãn lan/không lan sau khi đã xem để kết luận.
- Không gọi vùng nghi ngờ là vùng ảnh hưởng đã kiểm đúng. D3/D16 trước kết luận (b)/khóa FT; nhãn vùng độc lập thuộc P10, LLM thuộc P8 và yêu cầu R-01–R-10 thuộc P9/P10.
- Không mở RE3 trong grant chính. Pha 1 phải chuẩn bị hợp đồng nguồn/adapter từ metadata/schema được phép; đây là đầu ra chuẩn bị bắt buộc, không đẩy toàn bộ sang sau chạy chính. Cài và kiểm trên telemetry RE3 cần phạm vi/quyền riêng; chưa được coi adapter hiện có đã tương thích. Thiếu thì OPEN và trình đúng phần xác minh/dung lượng/quyền riêng. Không lấy 4 root metadata làm U; giữ 30 ca/10 ô cho bản cuối.
- TT test được đề nghị chia sang hai EC2 theo transfer-plan005 sau G3/grant, không còn ràng buộc local-only. OB và A bố trí laptop theo chi phí/nguồn hiện có; không mở/xóa bản sao OB cũ trên EC2.
- Không sửa nguồn lịch sử/xóa lượt hỏng/commit/push/bật tắt máy/quyền ACL/Scheduled Task ngoài quyền đúng bước. Không coi đóng task là đóng RQ3.

## Chi phí ước lượng

Các số đã pin chỉ dùng đúng miền:

| Nguồn | Mốc | Giới hạn |
|---|---|---|
| T-048/pilot.json /case_timings | Native TT main mean laptop ~62 s/EC2 ~36 s | Khác cấu hình/bundle P7, không nhân thành ETA |
| T-053/runs/preflight-001.json | Máy EC2 cũ được đo: 2 vCPU/~8,15 GB; local từng có RAM khả dụng ~2,05 GB/D ~1,97 GB | Không thay đo sau khi Minh dọn hoặc hai máy hiện tại |
| T-052 baseline-local-001/summary.json | Một TT/sáu baseline-seed 0, stage ~82,54 s | Không là trần 60 ca/3 seed |
| T-052 ob-local-002/summary.json | Một OB, stage ~63,09 s; M1/T12 cache liên tiếp | Không là chi phí bảy vế lạnh |
| T-052 ec2-pilot-002/received/output/summary.json | 5 cửa sổ×3 config, 15 so sánh ~266,28 s; RSS process ~1,66 GB | Khác full matrix/local; RSS không tự là cả cây |
| T-052 pilot-f3-summary-001.json | 12 PASS, 404,16 s là upper bound gồm lượt lỗi | Không là runtime sạch/full guard |
| T-051/dinh-chinh-luot-1.md | ~821 MB nén→11,55 GB logic; inflate/nạp đáng kể | Cần stream/output/temp/reserve, không chỉ chừa đĩa nén |

Hiện hành ngày05/11: chuẩn bị nhiều máy hoàn tất để trình G3, không tiếp tục pilot mặc định. Dự toán005 **5–9 giờ** cho tính toán/chuyển/niêm phong/chấm là kịch bản chưa kiểm toàn cohort, không là trần hoặc ETA toàn nghiên cứu. Giả định cloud40–120s mỗi lượt family/C-e (chỉ một ca EC2_2 đo~67s), tối đa2worker/máy khi RAM đủ, dùng thời gian baseline đã có, setup/chuyển0,25–0,5h dự kiến. I/O/solver/ca khác, thiếu RAM hoặc lỗi có thể làm lâu hơn. Đọc ca/diễn giải cơ chế/báo cáo khoa học tính riêng, chưa có dự toán đáng tin. Không dùng25–27h tuần tự cũ làm ETA mới, không hứa mốc08:00.

Lịch: G3/grant→khóa nguồn/plan→sync/hash hai EC2 song song→ba queue chạy đồng thời. Mỗi ca prep trước method; M1 seal trước C-d3. Laptop nhận/kiểm định kỳ; chỉ chấm sau đủ snapshot/binding. Thời gian đường găng là max(queue EC2_1, queue EC2_2, queue laptop) cộng các pha ngoài queue, không cộng ba queue thành giờ trôi. Nguồn: placement-005.json, environments-005.json, transfer-plan-005.json, de-xuat-khoa-g3-005.json. Không mở telemetry test trong005.

Ngoại lệ Minh xác nhận ngày 05/11/2026 cho riêng P7: không đặt trần thời gian cộng dồn toàn đợt hoặc method×dataset; chạy đủ cohort. Giữ timeout từng lượt để xử lý treo và số đo tiến độ/tài nguyên. Nếu lỗi, không tiến triển, lặp vô tận hoặc hàng chục giờ chưa xong thì dừng/báo Minh; không tự tạo một trần cố định thay lời Minh. Lượt chưa chạy giữ PENDING/BLOCKED và bảng cần đủ cohort bị chặn, không gán method TIMEOUT. Quy tắc Q-40/P3 cũ giữ lịch sử, không áp trần cộng dồn vào P7. Lượt hơn một giờ, tải hơn 5 GB vẫn theo quyền thao tác AGENTS.

## Rủi ro và điều chưa chắc

### OPEN phải chốt trước khóa/phần phụ thuộc

| Mục | Nguồn và phương án | Quyết định/điểm dừng |
|---|---|---|
| Thời gian P7 — USER_CONFIRMED | Minh bỏ trần cộng dồn cố định, chạy đủ cohort; lỗi/hàng chục giờ chưa xong/không tiến triển thì dừng và báo. Timeout từng lượt vẫn có bằng chứng pha/monitor. | Không còn OPEN về trần cộng dồn. Unrun không thành TIMEOUT; A4 chưa đủ thì chưa ghép nhãn/chấm. Nguồn ở quyết định phiên 5, sổ chính thức chờ Minh duyệt dòng ghi. |
| Nguồn TORAI A | Q-74 Q3/P3 §6.6 đã yêu cầu cả A/B; baseline đã chạy B chính/A phụ. Minh xác nhận giữ A phụ ngoài A4, không mở lại lựa chọn baseline. Driver mới đã kiểm A tự sinh và A thật trên đúng ca dev-a5cabe5fa7 đủ ba seed; chưa kiểm toàn cohort | Đã có grant đúng ca dev-a5cabe5fa7 cho pilot, không phải toàn cohort. Trước phần A chính còn cần grant cụ thể 3 CSV tác giả logts/tracets_err/tracets_lat của đúng thành viên TT tại D:/RCA-ext/work/T-016/data/torai-TT + metric. Chưa xác minh đủ ca/hash/schema; nằm ngoài thư mục locked vẫn không được đọc. Locator có service/fault ở map riêng; method không nhận. Giữ nhãn hồi cứu P3 §4/lưới-ngưỡng toàn file. A ngoài A4 có thể chạy sau seal chính nhưng không tự miễn snapshot/công bố |
| Nguồn/nhãn | Ai cấp map/label ref độc lập từ G1/metadata được phép; schema đã thiết kế | Minh chỉ định/quyền materialize trước test; hash không thay provenance |
| Vận hành trình G3 | 1/2 worker; 1 luồng BLAS/OMP; ứng viên timeout 600 s/slot chính, C-d3 60 s; poll 0,1 s/maxgap strict <5 s; ERROR chưa phân xử giữ BLOCKED, không retry. | Kiểm đúng đường sửa trên dev/fixture; trình Minh khóa các số này với code/env/matrix. Không còn trần cộng dồn. |
| Độ nhạy — USER_CONFIRMED | Minh duyệt bản loại nguyên cặp và TT case-permutation ở bước 6 ngày 05/11/2026. | Chỉ độ nhạy, không điều khiển E-04/chuyển mức. Cài kiểm trong wrapper T054; không sửa lịch sử T052. |
| Công bố | Cơ sở ở bước 11 chặn mọi bảng khi A4 BLOCKED/PENDING; ngoài A4 chạy sau khi xem được đánh dấu riêng | Muốn theo bậc khác cần Minh chốt trước G3; BLOCKED không đổi thành 0 |
| Máy/quyền/hạn | SSH/sync/DEV hai EC2 đã được cấp và kiểm; lịch005 dùng cả hai EC2+laptop, không thêm cache liên vế | Dừng trước main; G3/grant test/nguồn A riêng. Không bật/tắt máy hoặc commit |

Dev đã chọn lặp. TT 60 TX1; OB 34 TX1 và 34 ca từng dò triệu chứng, ca liền kề/file chung. RE3 TX0 nghĩa là chưa thấy nguồn tiếp xúc; cùng hệ/công cụ ở các chiều khác, không độc lập hoàn toàn. M4 giữ giới hạn Q-192; snapshot chưa nối revision; A0/ba world không bao phủ mọi mất dữ liệu; bootstrap ít ô có undercoverage. Giữ nhận định có điều kiện, không coi hai tác giả đồng ý thay bằng chứng.

Trước khi Minh ngủ: cần G3 + grant đúng phạm vi + budget/policy để pha 2 được phát; máy bật, RAM/đĩa sau dọn, mạng, laptop cắm điện và không sleep/hibernate. Chỉ đổi thiết lập nguồn khi được phép; chưa kiểm thì không coi là đã tắt. Thiếu quyền thì bàn giao trạng thái WAIT rõ, script không tự qua. Máy restart cần nhận tiếp thủ công nếu chưa duyệt startup.

## Prompt bàn giao

Prompt trung tính, nguyên văn Prompt chung + Kiểm lại phản hồi và sửa + G3, nằm trong mục LOG hiện hành. Phản biện SPEC có thể đề xuất dừng theo lượt Claude cuối và việc Codex nhận N1–N5; Minh quyết chuyển hay dừng. Không tự gửi. Trước phần chưa có quyền, trình đúng gói/pilot/quyền máy/ngân sách và OPEN còn phụ thuộc; không xin lại quyền công cụ/pilot dev local đã cấp trong LOG. Không coi SPEC được ghi hoặc pilot đạt là G3/test đã mở.
