# T-054 — Pilot dev thật, thời gian thực đo và checkpoint 003

Ngày 05/11/2026. Codex là người làm; Claude vẫn là người phản biện chính thức. **Đã thực hiện hai gói pilot local trên bốn ca dev. Chưa hoàn tất pha 1, chưa đủ đề nghị G3, chưa chạy chính.** Báo cáo này không thay REVIEW hoặc quyết định của Minh.

## 1. Yêu cầu và quyền đã dùng

Minh yêu cầu đọc kỹ các yêu cầu trước, tiếp tục triển khai, sửa câu chữ sai, ghi checkpoint đầy đủ và dừng báo trước chạy chính. Nguồn: `runs/trien-khai-003/quyen-minh.txt`.

Lệnh tiếp tục được dùng cho công cụ và pilot dev local cần thiết. Không suy ra quyền test/RE3, SSH/sync, commit/push hoặc chốt lựa chọn khoa học. Hai quyền phát sinh được lưu nguyên văn:

- `grant-A-dev.json`: đúng ba CSV tác giả logts/tracets_err/tracets_lat của ca dev-a5cabe5fa7, pilot A ba seed. Không gồm ca A khác hoặc cohort chính.
- `grant-diagnostic-thread.json`: một lượt MicroRank dev-607751ac0a để kiểm thiết lập luồng. Không đổi cấu hình chính hoặc chấp nhận dung sai. Câu hỏi đã nói quá mạnh rằng nguồn lịch sử dùng 16 luồng; đã đính chính ngay: hồ sơ chỉ ghi current16 lúc kiểm kê, còn source thread lịch sử OPEN. Không dùng tiền đề sai làm kết luận.

Nguồn mục tiêu vẫn là DT18, hướng dẫn cô và MRP RQ3/P7. P7(a) kiểm xếp hạng và tác dụng can thiệp tính toán của các thành phần đã chọn; không tự trả lời detector, vùng ảnh hưởng thật hoặc cơ chế vật lý. Lượt này tiếp tục tự soát của người làm, không nhận là một lượt soát mù mới. Báo cáo 001 và LOG giữ giới hạn thứ tự đọc ban đầu.

## 2. Các câu chữ đã sửa

| Chỗ cũ | Nội dung hiện hành | Vì sao/ảnh hưởng |
|---|---|---|
| Đặt giữ/bỏ TORAI A như chọn lại baseline | B chính/A phụ đã có trong P3 và cả hai đã chạy. Minh xác nhận giữ A ngoài A4. Chỉ nguồn A còn theo grant từng phạm vi. | Không mở lại lựa chọn đã có; ma trận thêm đúng 180 slot A phụ, không nhập A vào A4. |
| SPEC ghi chưa cấp quyền công cụ; CLI chưa tồn tại | Nguồn quyền triển khai/pilot local và CLI hiện hành nằm trong LOG/authorization. Các placeholder không là lệnh chạy chính. | Phiên tiếp nhận không xin lại quyền đã cấp hoặc dùng mô tả lịch sử làm hiện trạng. |
| Trần 3 giờ được hiểu là dự kiến pilot mất 3 giờ | Đó là đề xuất cap chưa đo, chưa được chốt. Hai gói thực tế giữ cùng mốc cap local một giờ, không reset khi nhận tiếp. Generator không tự tái sinh cap 3 giờ như hiện trạng. | Dự toán phải dùng số đo; tăng thời gian không tự chọn cách chấm khi cạn trần. |
| RE3 chỉ là một lô sau | Pha 1 có nghĩa vụ chuẩn bị hợp đồng nguồn/adapter bằng metadata/schema. Đã tạo hợp đồng, nêu chính xác các bước còn thiếu. | Không coi cùng RCAEval là adapter đã tương thích; không bỏ nghĩa vụ nghiên cứu vì chưa mở RE3. |
| Môi trường cũ trong protocol bị hiểu là môi trường đã chạy mới | Môi trường pilot thực được ghi riêng, nguồn cũ giữ dưới trường historical; ngoại lệ 16 luồng chỉ là chẩn đoán. | Không ghi môi trường 1 luồng thành 16 hoặc lấy metadata cũ thay bằng chứng thực chạy. |

Chỉ sửa mô tả hiện hành trong SPEC và hồ sơ; không sửa quyết định khoa học cũ, src hoặc báo cáo lịch sử. Đề xuất dòng sổ chính thức nằm trong `runs/trien-khai-003/de-xuat-so-quyet-dinh.md`, chưa nối DECISIONS/WHY khi chưa được duyệt đúng dòng.

## 3. Đã triển khai và thực chạy

### Nguồn thật và nhãn dev

Worker kiểm runtime mới bằng descriptor đọc lại allowlist baseline, G1 và command native đã pin. Descriptor không tin một bản đồ nguồn thứ hai do runtime tự khai. Mã thành viên được dựng từ đúng G1 dev; t TT từ command main đúng ca, t_ns/guard OB từ allowlist gốc. Các trường file/byte/hash phải khớp trước đọc/cắt và gọi method.

Evaluator đóng snapshot trước, rồi dựng lại nhãn dev từ G1 độc lập với runtime mới. Có kiểm root/fault/cell/alias và đủ ca/seed. Nhãn, case, locator không vào API phương pháp. Đây là liên kết có nguồn gốc; không phải bảo đảm chống người cố tình giả mọi lớp bằng chứng.

`source-original-checks.json` có tám kiểm đạt. `external-code-checks.json` xác nhận ba upstream ngoài repo cùng revision và không có tracked diff. Toàn bộ 93 pin code nền được kiểm trước dùng; không sửa src. Các bản code T-054 thực chạy được giữ và kiểm byte theo job tại `code-version-lineage.json`.

### Hai gói dev local

| Gói cuối | Ca | Công việc | Đầu ra |
|---|---|---|---|
| `pilot-local-007` | TT dev-a5cabe5fa7; OB dev-607751ac0a | Bảy M1-family trên mỗi ca; sáu baseline theo support; B ba seed; A phụ ba seed; C-d3 sau main seal. Tổng 32 slot. | `summary.json`, `sealed-snapshot.json`, `parity-complete.json`; bảng ở `reports/pilot-local-002/`. |
| `pilot-local-008` | TT dev-03d4910932; OB dev-2bfc97b01e | M1/T12 trên mỗi ca; B ba seed TT và M4 OB. Tám slot để kiểm thêm ca và đo biến thiên, không nhân lại toàn ma trận. | `summary.json`, `sealed-snapshot.json`, `parity.json`; bảng ở `reports/pilot-local-003/`. |

40 slot đều có kết cục VERIFIED trong gói cuối, **không đồng nghĩa 40 kết quả OK**. Gói đầu có hai ERROR TT, hai UNSUPPORTED OB và C-d3 UNSUPPORTED_CYCLIC; các trạng thái được giữ. CIRCA một call có hai variant OK, không tính thành hai ca. Các bảng dev dùng một ca mỗi dataset trong từng gói, không phải A4 test 60/34 ca.

Gói đầu xuất 91 dòng mô tả, bốn dòng vùng, hai vị trí N; gói thêm xuất 22 dòng mô tả, bốn dòng vùng. Không có C-e mới trong hai gói. Không cộng các bảng có độ phủ vế khác nhau thành kết quả P7 chính. Không dùng điểm dev này để chọn lại thiết kế.

### Lỗi thật tìm được và sửa tối thiểu

| Điểm | Bằng chứng | Xử lý/giới hạn |
|---|---|---|
| Nguồn quyền TXT bị ép đọc JSON | Pilot001 chưa phát worker đã dừng. | Kiểm byte/hash nguồn quyền, không yêu cầu văn bản quyền là JSON. Giữ lượt hỏng. |
| Kiểm kê môi trường py38 lấy nhầm metadata thư viện từ đường Python 3.12 | Probe prepend khác thứ tự append của worker. | Sửa probe đúng thứ tự nhập; phát DRAIN, giữ sáu vế TT đã VERIFIED. Ba seed B chưa chạy được sửa đúng environment; tiếp nhận cùng mốc/cost cap. Không đổi code phương pháp. |
| C-d3 tìm cạnh trong phần điểm | Main thật chỉ có dich/diem ở dau_vao_cd3; cạnh nằm ở extra.canh. Fixture cũ có gộp sẵn cạnh nên chưa chạm lỗi này. | Đối chiếu helper T-052 rồi nối đúng hai trường đã seal. Chỉ chạy lại C-d3 ở006; main/rank/vùng không đổi. Raw status/blocks/điểm khớp controls cạnh quan sát cùng ca ở T-051. Ca thật là nhánh cyclic, không nhận đã kiểm solver DAG thật. |
| CIRCA thiếu trường window.circa_current | Method đã ghi current đúng trong diagnostics; wrapper không chuyển vào window như worker P3. | Sửa wrapper và thêm guard; chỉ kiểm lại CIRCA ở007. Giữ kết quả/report đầu, khai đã xem nhãn dev. Không sửa rank hoặc công thức. |
| Snapshot có thể nhận ERROR tự gắn VERIFIED mà thiếu phân loại | Lớp envelope riêng không phân xử nguồn lỗi. | Bổ sung kiểm receipt tại snapshot. Receipt tái hiện ERROR dev không dùng được cho test hoặc TIMEOUT. |

Hai lỗi MicroRank/TraceRCA TT không được đổi thành OK. `operation-error-audit.json` xác nhận đúng operation có **0 span N, 210 span A**, theo phép chia end-time của cả hai code. MicroRank kiểm newops rồi ném lỗi; TraceRCA truy cập normal_slo không có khóa. Adapter giữ ERROR. Cửa sổ, nguồn và ERROR khớp bản baseline đã chấm trước. Đây là giả định của bản cài phương pháp về có baseline cho operation, không là kết luận dữ liệu hỏng hoặc cơ chế vật lý của sự cố. Receipt chỉ cho phép tái hiện dev có audit code/đầu vào và native reference; chưa giải quyết policy lỗi test tổng quát.

### Parity và chẩn đoán số học

Gói đầu đối chiếu đủ 32 slot, gồm các trường khoa học và trung gian baseline như phiếu M4, prep TORAI, ba world M1, vùng T12 và trạng thái C-d3. Bỏ ra có khai báo các metadata của driver cũ đã chuyển sang envelope/attempt: run/config ID, cost, source_provenance và nhãn pilot. Không thêm dung sai số để cho qua.

- Một MicroRank OB ở 1 luồng khác một ULP tại một điểm, không đổi thứ tự. Lượt chẩn đoán Minh cấp riêng mất khoảng 11,47 giây, có cùng normalized-input digest; thư viện thực đo 16 luồng và các trường khoa học khớp chính xác bản T-026. Điều này cho thấy đổi chế độ chạy hiện tại có thể tạo sai khác ấy. Chưa xác nhận source thread lịch sử hoặc tự chọn cấu hình chính.
- Gói thêm có M1/T12 trên OB dev-2bfc97b01e khác số thực ở cuối so với nguồn EC2, gồm p và một khóa độ lớn. Các trường rời rạc, thứ tự và vùng trong phần đã đối chiếu không đổi. Chưa xác định riêng cơ chế máy, thư viện hay phép cộng nào tạo lệch. `pilot-local-008/parity.json` giữ từng đường dẫn và giá trị. Không gọi là exact hoặc tự làm tròn để khớp.
- Các dòng khác của hai gói khớp ở những trường được đối chiếu. Điều đó không chứng minh toàn cohort hoặc mọi nhánh đã tương đương. Quy tắc số thực giữa môi trường và lựa chọn luồng vẫn phải được chốt trước G3 theo SPEC.

`numeric-parity-analysis.json` lượng hóa các lệch đã thấy: MicroRank một ULP, M1 tối đa hai ULP, T12 một ULP trên các trường so tương ứng. Đây là mô tả quan sát, không phải cận sai số chung hoặc dung sai đã duyệt. `control-T050-parity.json` có bốn so sánh C-c/C-g trên hai ca gói đủ baseline: toàn bộ output dẫn xuất khớp chính xác T-050, gồm phiếu M4 và graph M1 tương ứng; không gọi lại phương pháp.

## 4. Thời gian và bố trí trước chạy chính

Nguồn số: `runs/trien-khai-003/thoi-gian-va-kich-ban.json#/measured`, tham chiếu từng cost và con trỏ group_cost_samples_s trong cùng file.

- Hai gói có 40 slot trên bốn ca. 42 attempt có cost gồm các lượt sửa giữ lại; tổng khoảng **39,72 phút**. Chẩn đoán luồng riêng khoảng 11,47 giây. Tổng công việc máy khoảng **40 phút**; không tính các kiểm metadata và thời gian người vào tổng method này.
- Từ mốc pilot đầu đến supervisor cuối dừng là **56,16 phút**, gồm khoảng ngắt để kiểm/sửa/nhận tiếp. Cùng mốc cap được giữ qua các lần chuyển plan; không đổi unrun thành TIMEOUT hay tự reset giờ.
- M1 TT hai ca khoảng 118 và 212 giây; T12 TT khoảng 136 và 214 giây. M1 OB khoảng 49 và 51 giây. Đây là lượt cô lập/lạnh của driver hiện tại, đã gồm source/read/cut/compute/receive theo cost attempt. Không dùng một trung bình để khẳng định mọi ca đều có chi phí ấy.

**Chưa có ETA chạy chính đáng tin.** Kịch bản nhân đúng chi phí ca đầu cho 1.342 slot chính và 180 A phụ cho khoảng 24,71 giờ ở một worker. Nếu cả 60 C-e có chi phí bằng M1 main ca mẫu thì thêm khoảng 1,97 giờ. Đây là **CANDIDATE CHƯA KIỂM**, không phải dự báo, cap hay cận trên. Nó chưa dự đoán chi phí solver C-d3 được hỗ trợ và không phản ánh biến thiên ca thứ hai, bundle/cache hoặc song song. Các giả định, lúc sai và quyết định phụ thuộc được ghi trong `#/scenario`.

Ý nghĩa thực tế của phép tính là chưa nên phát toàn ma trận bằng driver lạnh nối tiếp rồi hứa xong qua đêm. SPEC đã dự kiến dùng chung phần chuẩn bị/cache trong bundle; code hiện vẫn khởi worker và reset E4 cache cho từng slot. Scheduler nhiều worker cũng chưa cài. Cần hoàn thiện/đo các phần đã được SPEC giao, rồi mới quyết số worker, cap và lịch. Không chia kịch bản tuần tự cho hai hoặc ba để tự tạo ETA.

Bố trí cơ sở vẫn giữ test/dẫn xuất local. Hai EC2 chỉ nhận TT dev độc lập đủ quyền và có lợi sau đo identity/env/sync/parity; chưa SSH nên chưa xác nhận chúng sẵn sàng. Không có việc cloud đã đo đủ để khẳng định tiết kiệm thời gian. Không phát sinh cloud cost hoặc truyền test.

## 5. RE3 đã chuẩn bị đến đâu

`runs/trien-khai-003/hop-dong-re3.json` và `.md` đối chiếu metadata đã pin với G1: 30 ca, 10 ô, 138.129.790 byte. Chưa tải hay mở telemetry. Hồ sơ schema local đã kiểm không có RE3-OB.

Code hiện có còn các giả định TT: TORAI metric lọc ts-*, BARO/CIRCA/TraceRCA truyền dataset re2-tt, profile M1 chỉ có TT/Nezha. Hợp đồng nêu H1 kiểm schema/đơn vị/inventory phi nhãn; H2 duyệt đúng file rồi kiểm adapter bằng dữ liệu tự sinh; H3 bản cuối khóa và grant RE3 riêng; H4 bảng riêng. Không lấy root metadata làm U, không đổi tên RE3 thành Nezha để chạy, không dùng RE3 làm pilot/chọn thiết kế.

**H0 hợp đồng chuẩn bị đã có; H1–H4 chưa hoàn tất.** Đây là phần còn phải triển khai, không phải lý do bỏ RE3 khỏi nghiên cứu. Src chưa được SPEC cấp sửa cho nhánh này, nên phải trình đúng phạm vi file/hợp đồng trước H2.

## 6. Phần còn thiếu và quyết định bị chặn

| Phần | Loại trạng thái | Thiếu đúng gì / bước tiếp |
|---|---|---|
| Cài và đo bundle/cache M1, prep TORAI và scheduler 2/3 worker | Chưa làm đủ trong công cụ | Giữ đầu ra lạnh làm tham chiếu; dùng cùng nguồn/param, so normalized input/trung gian/output đúng byte hoặc chính sách số đã khóa. Kiểm resume/timeout/budget khi có cache/đồng thời. Đo toàn lô, RSS/đĩa/paging và cold/warm; không tự nhận speedup. |
| C-e và phủ các nhóm giúp/hại/không đổi của SPEC §7 | Chưa đủ bằng chứng mới | Xác minh chứng nhận hỗ trợ lịch sử/A0 từ nguồn hợp lệ, dùng ca đã khai và đối chiếu native. Hai gói hiện không có C-e mới; không chuyển nó thành NO_CAUSE/0 hoặc tự bỏ khỏi nghiên cứu. |
| Chính sách số học và luồng | OPEN cần Minh | Exact case hiện có và các diff đã lưu. Minh chọn phạm vi cấu hình/ngoại lệ và quy tắc số thực trước G3; 16-thread diagnostic không duyệt cấu hình main. Không sửa số để che bất đồng. |
| ERROR/TIMEOUT main, monitor/sleep/clock, cạn trần | OPEN và thiếu triển khai tổng quát | Phân loại có nguồn, pha và chứng cứ; receipt dev không áp test. Minh chọn giữ P3 hay ngoại lệ PENDING/BLOCKED khi cạn trần. Tăng thời gian không giải quyết thay lựa chọn này. |
| Bản loại lỗi và hoán vị ca | OPEN cần Minh | Hai ứng viên ở SPEC §6 chưa được chốt. Không biến bản nhạy thành phép quyết định chính. |
| Nguồn test/nhãn, nguồn A cả cohort, snapshot revision | Chưa có đủ quyền/chứng nhận | Giữ metadata matrix đã khai. Cấp đúng map/source/grant trước phần phụ thuộc; không tự đọc locked hoặc suy grant A dev thành cả cohort. |
| G3 và chạy chính | Chưa được Minh duyệt | Không trình đạt G3 khi các mục trên còn chặn. Giữ WAIT; báo Minh trước main theo yêu cầu. |

Task đã có bằng chứng công cụ và pilot thật; câu hỏi hiệu quả độc lập RQ3b/d chưa được trả lời bằng test. RQ3a, độ đúng vùng ảnh hưởng, các giải thích vật lý, LLM/FlashTicket và H1–H4 RE3 vẫn giữ đúng phạm vi. Không đề nghị nghiệm thu T-054 hoặc gọi mọi câu hỏi đã đóng.

Giữ mọi lượt lỗi và code thực chạy. `code-version-lineage.json`, manifest checkpoint003, freeze005 và mục cuối LOG là điểm tiếp nhận. Các báo cáo trước và bản ghi đầu không sửa. Prompt chuẩn nằm trong LOG để Minh chọn chuyển; không tự gửi hoặc tạo vòng phản biện mới.

Kiểm checkpoint tại `runs/trien-khai-003/validation.json`: PASS trong phạm vi toàn vẹn/liên kết/quyền, không phải G3. Đối chiếu 2.190 file trước phiên: 19 file đổi đúng phạm vi, 2.171 file được giữ nguyên. Prefix LOG giữ byte; STATE chỉ khác dòng T-054. Chín script qua kiểm cú pháp, 93 pin code nền khớp, ba phiên bản code thực chạy khớp job pins. Freeze005 có 107 file và archive khớp byte. Không còn worker/supervisor T-054 đang chạy. Các bất đồng số học vẫn được giữ, không bị validator biến thành PASS khoa học.
