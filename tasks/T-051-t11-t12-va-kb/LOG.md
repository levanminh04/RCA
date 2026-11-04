# Nhật ký T-051

## Phiên 1 — 04/11/2026 — Codex — laptop Windows — người làm

Minh duyệt có điều kiện qua prompt tiếp nhận ngày 04/11. Claude là người phản biện chính thức.

### Phương án tự dựng trước khi mở SPEC T-051

- **Nguồn và câu hỏi.** DT18-NV2/NV3, hướng dẫn cô bước 2–4, MRP §2.3/RQ3b–d, T-043 B2/B4/D8/D19/Đ11 và kế hoạch sau T-047. Trên dev chế độ (a), kiểm xem thứ tự khởi phát có cứu bằng chứng tự sinh bị E5 phân loại sai, cạnh tĩnh có bổ sung quan hệ hữu ích hay nối sai, và lựa chọn của khối K có đổi trong chuỗi hiện tại. Phần đánh giá độc lập, hiệu quả do quan hệ và độ đúng của vùng ảnh hưởng còn OPEN.
- **Đã quyết.** E1-U, E2-C, E5, z+S1, E6a, ε=0,05, α=0,01, G3/D1 trong mã, cạnh quan sát. E3(a), E3b, E6b, E9, T12 tắt ban đầu. Cờ đánh đổi E2 giữ nguyên, đảo chiều PageRank OPEN.
- **Đã quan sát.** T-050 hai manifest xác minh được 378 và 294 đầu ra, không lệch SHA-256. Lượt chạy lại T9 tiếp tục HẠI cho E6b theo chiều gọi. Gói chiếu của T-050 được thiết kế tái lập khóa xếp hạng, dùng đầu ra sau phân loại E5 nên phải lấy thêm dữ liệu theo đơn vị từ seal T-049 để kiểm khả năng tái chạy E5.
- **T11.** Cặp E9 bật/tắt, giữ E5 và cạnh quan sát cố định. Lưu kênh, đề xuất kế thừa, khởi phát của e và toàn bộ B(e), chặn trên cạnh E2, F_I, tầng, khóa và hòa. Phân biệt thiếu khởi phát, đủ nhưng không phủ quyết, đã phủ quyết, và phủ quyết làm đổi hạng. Sau chấm, đối chiếu ca cứu root, ca làm hỏng và ca đủ điều kiện nhưng hạng giữ nguyên.
- **T12.** So cạnh quan sát với hợp cạnh tĩnh trên nền sau T11, giữ E9 cố định. Lưu cạnh mới, nút chỉ có trong kiến trúc, thay đổi SCC/kế thừa và khóa, vùng E7 và C-d1/C-d3. Kiểm đầu vào E1/E2 bất biến. Phân biệt thay đổi do đường quan hệ, do hai phiên bản kiến trúc khác nhau, và do thay đổi vùng mà hạng không đổi. Nhãn root chỉ đo độ chứa sau seal.
- **KB.** Sau T12, giữ chuỗi cố định rồi đảo riêng E1, E2, E3(a), E5. Dùng kết quả ghim cho từng vế khi chứng minh được cùng đầu vào, công thức, cấu hình và khóa; E1 đổi phép tính span, E2 đổi gán cạnh, E3 đổi kênh, E5 đổi phân loại và khóa. Kết cục khác mốc chọn phải trình Minh. Phép đảo đơn lẻ chưa tách tương tác VC × E5.
- **Chấm và lỗi.** Chọn pilot không nhãn, đối chiếu lần lượt kênh, khởi phát, F_I, khóa, hòa, N1/V0, vùng và đối chứng trước ghép nhãn. Seal từng pha 1 trước lấy RR, theo ca/ô và ba thế giới. Giữ C-e đúng cặp mốc giả RE2, báo N1 và V0 theo quy ước đã quyết. Giữ lỗi và thiếu bằng chứng riêng, không quy ERROR thành ca thường hoặc giảm mẫu số tùy tiện.
- **Chi phí và tiêu chí xong.** Một tiến trình laptop. Kiểm nguồn, xác nhận đầu vào và ước lượng chi phí bằng pilot trước khi cam kết chạy đủ. Tiêu chí là tái lập vế nền, truy được kết cục theo cơ chế và luật, chỉ rõ gì chưa phân xử, giữ seal/biên nhận. ETA chưa đo. Nếu cache thiếu hoặc phần chạy lại vượt trần 60 phút thì trình phạm vi và chi phí.

### Đối chiếu sau khi mở SPEC

- Hai hướng cùng yêu cầu T11 → T12 → KB, ba thế giới, seal trước ghép nhãn và tách độ chứa root khỏi độ đúng của vùng. SPEC xác định thêm số cửa sổ, cờ kích hoạt cố định, UV-6/M5, C-d2, luật, độ nhạy và điều kiện dừng. Giữ các yêu cầu đó. Phương án độc lập nhấn mạnh rằng gói chiếu T-050 đã đi qua E5 và chỉ có khóa theo thực thể. SPEC mục 2 đã yêu cầu đối chiếu nguồn T-049 theo từng thế giới. Kiểm 82 cửa sổ/246 thế giới từ seal T6 thấy đủ tập mã `F_I`, chủ kênh có cờ và đầu nhận E2-C nằm trong U. Chạy lại E5 khi E9 tắt và dựng S1 từ m từng đơn vị khớp dữ liệu nguồn. Vì vậy bỏ việc lấy khóa tổng hợp T-050 làm đầu vào phát lại, giữ T-050 làm đối chiếu nền T9. Không bỏ phép đo hay giảm tập ca.
- SPEC T12 có C-d2 làm bất biến và yêu cầu C-d3. Tập đích C-d3 đến từ span gốc A và cờ thô lan ngược ở `chuoi.py`. Khi chỉ thay cạnh tĩnh, có thể giữ đích từ bản ghi native đúng cấu hình nếu kiểm vế cạnh quan sát khớp; C-d3 vẫn phải tính lại trên hợp cạnh. Hai mô hình tĩnh khớp SHA-256 ghim trong KS-16. `E_X` có nhãn root nên chỉ đọc pha chấm.
- Bốn cấu hình KB đúng ID có trong ma trận T-053. Kiểm theo từng cấu hình vẫn cần chứng minh cùng đầu vào, cấu hình và đường số học trước khi dùng lại; nếu E9 hoặc T12 bật, chỉ dùng trung gian trước E5 theo cấu hình và tính lại phần đổi. Cặp VC × E5 vẫn OPEN.
- Sửa nhỏ trong SPEC. Dòng cũ ghi bảng hành động, ngân sách và triển khai chờ duyệt. Dòng mới ghi Minh duyệt có điều kiện theo Q-241. Căn cứ là prompt tiếp nhận ngày 04/11. Phạm vi khoa học và luật giữ nguyên. STATE chưa có mục T-051, nên thêm đúng một dòng cho task này. Mục T-050 giữ lịch sử.
- Công cụ. Trình khởi chạy Python cũ không khởi động được. Dùng Python đóng gói 3.12.14 và thư viện đã cài sẵn từ môi trường py312-pin và T-016-cong-cu, không cài thêm. Phiên bản vá Python khác mốc gốc nên kiểm đường chạy native trên cùng laptop. Lượt `pilot-replay-001` dừng vì so trực tiếp list JSON với tuple của cặp m. So cùng dạng tuần tự hóa và giữ mặc định số thực theo code gốc. `pilot-replay-002` ghi đủ ba cửa sổ 19, 60, 06, chọn từ cấu trúc và loại cửa sổ trước ghép nhãn. Giữ kế hoạch lượt hỏng và các bản ghi sau sửa.

### T11 trước ghép nhãn

- Pilot native 3 cửa sổ, 6 cấu hình, không lệch F_I, m, thứ hạng, V0, vùng và giải thích kế thừa. Thời gian từng cửa sổ ở `results/T-051/pilot-native-001.log` và biên nhận riêng. Lượt chính phát lại đủ 82 cửa sổ trong 46,031 giây. Dự toán cập nhật sau pilot là 15–35 phút cho phần triển khai còn lại gồm T12, kiểm nguồn KB và hồ sơ, với điều kiện T11/T12 không phải trình quyết định và đường C-d3 không vượt dự toán. Chưa đo T12/KB.
- Seal T11 trước ghép nhãn: `results/T-051/t11-001/sealed/seal.json` (0c905c93afd320b289e977a2c7d3e2f9a5a1a8072ba0c13bea057afd2cfd72d5).

### T11 đã chấm, T12 đang kiểm

- T11 trả KHÔNG TÁC DỤNG cả ba thế giới ở ngưỡng chính. Một ca đổi RR, ΔMRR gộp 1/104. C-e có 30 cặp hợp lệ và ΔN1 7/30. δ=0,005 cho GIÚP. Nguồn `results/T-051/t11-001/score/{law,mechanisms,robustness}.json`. Giữ E9 tắt cho T12. Chuỗi vẫn dùng quan hệ qua E1/E2/E5/E7, nên ngoại lệ DT18/MRP cho việc giữ thành phần không áp dụng cho E9.
- Sửa nhỏ SPEC. Bổ sung một câu sau ma trận để làm rõ C-d3 chỉ trên RE2-TT theo Đ12 của đính chính T-043. Bản cũ nêu C-d3 ở P nhưng chưa nói phạm vi dataset. Vế Nezha-OB suy biến do không có span gốc. Giữ C-d1, C-d2 và cả hai cách E7 trên Nezha-OB.
- T12 pilot-001 dừng ở hash kỳ vọng T-039 vì chuỗi chép thiếu ký tự. So lại giá trị bằng Get-FileHash và ghim KS-16, sửa chuỗi cục bộ trong công cụ, giữ log lỗi. Pilot-t12-002 phát lại đủ ba cửa sổ trong 4,032 giây, dùng lại pilot chọn trước ghép nhãn. C-d3 có cả OK và UNSUPPORTED_CYCLIC trên RE2-TT. Pilot native lần 1 truyền cạnh qua khóa cấu hình mà runner không chuyển tiếp. Sửa cách gọi, đưa cạnh vào params_ca theo hợp đồng runner, giữ lượt lỗi. Dùng lại vế tắt từ kiểm native T11 và kiểm C-d1/d2/d3 nền đối chiếu bản gốc, chỉ chạy lại vế bật trong pilot native lần 2. Mục đích kiểm vẫn là cùng đầu vào và khác đúng đồ thị.
- T12 pilot native vế bật khớp đầu vào, phân loại, khóa, vùng và đối chứng ở cả ba cửa sổ. Lượt chính 82 cửa sổ, 47,547 giây. Seal T12 trước ghép nhãn: `results/T-051/t12-001/sealed/seal.json` (c52ac2edac0afa2ce7a191e1d68003ac40026f6e9921787e015fbe59b06773fc).

### T12 đã chấm, chuẩn bị KB

- T12 KHÔNG TÁC DỤNG ở cả ba thế giới. RR root giữ nguyên trên 52 ca; C-e có 30 cặp hợp lệ, ΔN1 −7/10. Có thay đổi phân loại E5, trật tự nhóm, vùng E7 và đối chứng phụ thuộc cạnh. C-d2 bất biến. Giữ cạnh quan sát cho KB theo bảng. E5 và E7 vẫn dùng cạnh quan sát để đáp ứng vai trò đồ thị.
- KB lượt 001 dừng vì dùng blob Git dạng LF so với hash nguồn có CRLF. Hash của bản chụp trước tích hợp T-049 trùng đúng hash ghi trong kế hoạch T-053; Git blob sau đổi cách xuống dòng cũng khớp. Lượt 002 dùng bản chụp byte gốc theo công cụ T-049. Diff đường mã từ revision T-053 tới hiện hành trong src và capture chỉ đổi src/m1/e4.py, bổ sung nhánh phục hồi số học Q-237. So điều kiện phục hồi và đầu vào riêng từng cấu hình. Nếu hợp lệ thì bỏ tính lại telemetry, vẫn chấm riêng bốn cặp theo luật khối K.
- KB lượt 002 kiểm đủ 82 cửa sổ × 5 cấu hình. Mỗi bản ghi đã ghim đúng đầu vào chuẩn hóa, cấu hình, không có ngoại lệ z và đồng nhất vế nền với T12 cạnh quan sát trong ba thế giới. Seal KB trước ghép nhãn: `results/T-051/kb-002/seal.json` (f22ba367a199209f8a9ea4bbd1867b842f1d2a02b7ec45bc9ba6fcb70d5c3bd8).

### Kết thúc phiên

1. Hoàn tất triển khai dev chế độ (a) T11 → T12 → KB theo Q-241. T11/T12 giữ nhánh tắt. KB tái lập GIÚP, TRÁI CHIỀU theo dataset, HẠI, GIÚP theo thứ tự E1/E2/E3(a)/E5 ở cả ba thế giới. Không có kết cục KB đổi phải trình chọn lại. Đề xuất nền Q-241 cho T-052 với cờ E2.
2. File ghi gồm SPEC và LOG T-051, results/T-051, mục Q-241 trong DECISIONS, WHY-75 và đúng dòng T-051 của STATE. Giữ nguyên những thay đổi đã có trước phiên. Lượt fixture đầu bị lỗi quyền thư mục tạm mặc định. Lượt 002 đặt thư mục tạm mới trong results/T-051 và chạy qua 139/139, với ba cảnh báo thư viện. Không mở test hoặc dữ liệu giữ ngoài.
3. Hai pilot native và đối chiếu đầu vào đã qua. Kiểm cuối đọc lại 82 biên nhận và seal cho mỗi bước T11/T12, 410 bản ghi KB, luật ở ba thế giới, N1 tính từ các cặp cửa sổ, cú pháp công cụ và git diff --check. Kiểm cuối lưu tại results/T-051/kiem-cuoi.log. Dự toán 15–35 phút sau pilot đã gồm phần còn lại. Triển khai trên một tiến trình laptop mỗi lượt và trong trần 60 phút thực.
4. Task phân xử việc giữ cấu hình dev và các tác động quan sát được, gồm vết khởi phát → phủ quyết → khóa và cạnh → E5/E7/đối chứng. T11 nhạy δ=0,005, T12 có thay đổi vùng nhưng thiếu nhãn để gọi là cải thiện hay suy giảm vùng ảnh hưởng. KB tái lập trên cùng dữ liệu và nền. Chiều đảo PageRank, VC × E5, revision đồ thị tĩnh, hiệu chuẩn verdict, nhãn vùng, hiệu quả độc lập, chế độ (b), RE3-OB, FlashTicket và G3 còn OPEN. T-052 phụ thuộc Minh quyết nghiệm thu, sau Claude phản biện.

Bước tiếp theo. Minh chuyển prompt dưới đây cho Claude. Claude đọc SPEC, báo cáo và manifest T-051, rồi kiểm kết quả trong phạm vi Minh cấp. Trước nghiệm thu, đề xuất nội dung commit `T-051: ghi kết quả dev T11, T12 và KB` nếu Minh muốn chốt lưu lịch sử riêng. Commit/push cần quyền riêng.

Lệnh cuối khi chốt hồ sơ. Python 3.12.14 đóng gói với `-B results/T-051/manifest_task.py cho_phan_bien`, rồi đối chiếu SHA-256 và tập file trong manifest. Kiểm diff bằng `git diff --check`; xem file thuộc phạm vi bằng `git status --short --untracked-files=normal -- docs/DECISIONS.md docs/WHY.md docs/STATE.md tasks/T-051-t11-t12-va-kb results/T-051`.

## Prompt Claude soát kết quả T-051

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-051, tasks/T-051-t11-t12-va-kb/SPEC.md.
- Công đoạn: soát kết quả.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/KE-HOACH-SAU-T047.md, DT18, hướng dẫn của cô, SPEC T-043 và đính chính, SPEC/LOG T-051 và git diff hiện hành.
- Phản biện và phản hồi trước: chưa có phản biện chính thức T-051.
- Code và kết quả liên quan: results/T-051/bao-cao.md, results/T-051/manifest.json, results/T-051, src/m1, src/m1_danh_gia, seal T-049/T-050/T-053 được dẫn trong hồ sơ, lệnh và môi trường trong LOG.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: soát kết quả.
Kiểm trên đầu ra thật, code và dữ liệu được phép; không tin tóm tắt LOG. Đối chiếu tiêu chí xong với phần mục tiêu nguồn và mức căn cứ cho bước tiếp theo; chạy lại phần rẻ khi trong quyền được duyệt.
Phân biệt hoàn thành task mô tả, xác nhận cơ chế và đủ căn cứ chọn/đánh giá thiết kế. Giới hạn đã khai không tự miễn phép kiểm cần thiết còn làm được.
Chỉ ghi bản phản biện lượt được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ bản cũ; không sửa kết quả thay người làm.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 2 — 04/11/2026 — Codex — laptop Windows — người làm

Minh duyệt sửa gói đính chính sau bản đáp phản biện lượt 1, nguyên văn “duyệt sửa”. Vai trò người làm và phản biện chính thức giữ theo SPEC.

### Phạm vi và câu hỏi của Minh

Bốn file được duyệt gồm bản đính chính mới, LOG này, bổ sung nguồn Q-241 trong DECISIONS và manifest đính chính mới. Giữ báo cáo, manifest, SPEC và các lượt chạy gốc làm lịch sử.

Minh hỏi phần thiếu đo thời gian có nghĩa task còn tồn đọng chưa xong hay không. Trả lời của người làm là có, hồ sơ trước chưa đáp ứng trọn yêu cầu đo chi phí của SPEC. Dòng “hoàn tất triển khai” ở Phiên 1 cần đọc cùng đính chính này. Kết quả T11/T12/KB đã có nhưng báo cáo thiếu phạm vi cạnh, độ nhạy và bằng chứng chi phí. Khoảng pilot đầu → manifest lấy từ mốc file gồm thao tác và chờ của agent, không thay cho phép đo từng công đoạn.

### Tự soát và phản hồi đã kiểm trước quyền sửa

Các số T11/T12/KB và 261 đầu ra, 13 nguồn của manifest gốc khớp SHA-256 khi kiểm ở lượt đáp. Tệp Minh chuyển chứa cả kết luận và prompt nên người làm đã thấy kết luận trước khi tự soát xong. Lượt đáp là đối chiếu trên nguồn gốc. Điểm tự tìm thêm là thiếu phép đo tách đọc/hash, giải nén, hậu xử lý của lượt chính. Biên nhận pilot có RAM đỉnh nhưng chưa báo.

Bảng phản hồi chính thức của người làm đặt trong bản đính chính mới, để cột Minh quyết theo phạm vi “duyệt sửa”. Bản nhận xét của Claude giữ nguyên trong tệp Minh đã chuyển, không tạo bản REVIEW thay Claude.

### Đo bổ sung chi phí

Đọc lại đúng đầu vào đã ghim và gọi lại T11/T12 cùng đường tái sử dụng KB trong bộ nhớ, một tiến trình laptop. So đầu ra với seal gốc. Đo các thao tác đọc/hash, luồng gzip và giải mã dòng, phân tích JSON, xử lý sau nạp và C-d3. Phép đo này thuộc phần đo chi phí đã được SPEC/Q-241 yêu cầu. Kết quả và mã tái lập nằm trong bản đính chính được duyệt, không tạo thêm loại đầu ra. Dự kiến 2–4 phút máy, trong phần ngân sách còn lại của Q-241. Phép đo bổ sung không khôi phục được các mốc công đoạn chưa lưu của lượt cũ.


Lượt đo bổ sung 1 đã đối chiếu T11 và T12, lần lượt 75,618 và 66,885 giây. Kiểm byte KB dừng vì bộ đệm trong bộ nhớ dùng LF còn file gốc ghi CRLF trên Windows. Kiểm file gốc xác nhận 260 dòng CRLF ở ban-ghi.jsonl và một ở mỗi file ce.json, sources.json. Lượt 2 mô phỏng đúng xuống dòng Windows, đồng thời lưu biên nhận ngay sau từng bước để giữ kết quả nếu bước sau dừng. Số chi tiết của lượt đo 1 chưa được lưu nên chỉ giữ trạng thái đã quan sát và thời gian tổng đã in.

Lệnh nối mở Phiên 2 đã ghi thành công nhưng phần in thông báo gặp lỗi mã hóa ký tự ở stdout mặc định của tiến trình. Kiểm đuôi LOG xác nhận mục đã có, không nối lặp.


### Hoàn tất gói đính chính

1. Đã thêm bản đính chính lượt 1 với bảng phản hồi năm điểm, phạm vi cạnh tĩnh, T11 theo dataset/cửa sổ, giới hạn C-e của T12, độ nhạy KB đầy đủ và số C-d2. Nối nguyên văn nguồn quyền Q-241 vào DECISIONS. Ghi nhận kiểm native có cơ chế do Claude báo trong bản Minh chuyển theo phương án được duyệt, kèm giới hạn chưa có biên nhận native bổ sung được ghim trong repo.
2. Đo bổ sung T11 và T12 trên đủ 82 cửa sổ, KB trên 410 bản ghi trong bộ nhớ. T11 khớp toàn bộ trường, T12 khớp khi bỏ trường thời gian C-d3, và ba file dữ liệu KB khớp từng byte sau mô phỏng đúng CRLF. Tổng ba bước là 239,680 giây. Mức RAM đỉnh của cùng tiến trình tới từng bước là 261.156.864, 271.597.568 và 584.794.112 byte. Đây là số của lượt đo bổ sung.
3. Profiler đo được tổng, luồng gzip, JSON và phần xử lý ngoài loader. Phát hiện helper sha được records import trực tiếp chưa được gắn đồng hồ, nên cột hash_read_seconds trong profiler chưa gồm hash nội bộ loader. Giữ biên nhận đó với giới hạn nêu rõ. Đo tách trực tiếp trên đúng 492 lượt file nguồn của ba bước, gồm đọc, SHA-256 trên bộ đệm và giải nén byte. Lượt tách này mất 81,529 giây và khớp mọi hash. Hai lượt đo có điều kiện cache hiện tại nên không cộng chéo cột của chúng, không gọi số mới là phân rã thời gian của lượt cũ.
4. Kiểm cuối qua 261 đầu ra gốc, kiểm tiền tố DECISIONS và LOG theo manifest gốc để bảo toàn nội dung trước phiên, ba bước phát lại, 492 kiểm file và cú pháp hai khối mã tái lập trong đính chính. git diff --check qua. Chỉ bốn file trong gói duyệt có thay đổi của lượt sửa. Hai file fixtures-tmp-002 được phân loại là dữ liệu tạm của fixture trong manifest đính chính, không phải kết quả thực nghiệm cần mang sang máy khác.
5. Hồ sơ báo cáo trước chưa đầy đủ theo SPEC. Bản đính chính đã bổ sung nội dung và phép đo hiện tại. Phân rã thời gian lịch sử chưa lưu của lượt đầu không thể khôi phục và được giữ như sai sót ghi nhận khi nghiệm thu. T11/T12/KB vẫn chỉ hỗ trợ lựa chọn trên dev. Cạnh thông điệp/dữ liệu, chiều đảo PageRank, VC × E5, revision nguồn tĩnh, verdict, nhãn vùng, hiệu quả độc lập, chế độ (b), RE3-OB và FlashTicket còn OPEN. Chờ Claude kiểm gói sửa và Minh nghiệm thu, không tự đóng task.

Bốn file của lượt sửa gồm results/T-051/dinh-chinh-luot-1.md, LOG này, docs/DECISIONS.md và results/T-051/manifest-dap-phan-bien-001.json. Báo cáo và manifest gốc giữ mốc trước đính chính. Dòng STATE hiện vẫn ở bước chờ Claude, phù hợp với giai đoạn này.

Bước tiếp theo. Minh chuyển prompt bên dưới cùng bản đính chính và manifest mới cho Claude. Đề xuất dừng phản biện sau khi không còn phản đối ảnh hưởng lựa chọn dev hoặc phạm vi kết luận. Minh quyết nghiệm thu. Nội dung commit đề xuất khi Minh muốn lưu lịch sử là “T-051: đính chính phạm vi kết luận và bổ sung chi phí sau phản biện lượt 1”.

Lệnh cuối khi chốt. Python -B kiểm manifest đính chính, hash 261 đầu ra gốc, tiền tố hai file đã nối, các khối JSON và mã tái lập. git diff --check. Môi trường đo là Python 3.12.14 đóng gói, PYTHONHASHSEED=0, OPENBLAS_NUM_THREADS=1, PYTHONIOENCODING=utf-8. PYTHONPATH có results/T-051, D:/RCA-ext/envs/py312-pin/Lib/site-packages và D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages. Mã đầy đủ của hai phép đo nằm trong bản đính chính.

## Prompt Claude kiểm gói đính chính lượt 1

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-051, tasks/T-051-t11-t12-va-kb/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043 và đính chính, SPEC/LOG T-051, git diff hiện hành.
- Phản biện và phản hồi trước: bản phản biện lượt 1 của Claude và bản đáp của Codex do Minh chuyển trong chat, LOG T-051.
- Code và kết quả liên quan: results/T-051/bao-cao.md, results/T-051/manifest.json, results/T-051/dinh-chinh-luot-1.md, results/T-051/manifest-dap-phan-bien-001.json, src/m1, src/m1_danh_gia và các seal nguồn được dẫn trong hồ sơ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```


## Phiên 3 — 04/11/2026 — Codex — laptop Windows — người làm

Minh yêu cầu làm nốt phần còn thiếu, nguyên văn “vẫn còn đang chờ gì mà chưa làm nốt, đang chờ gì mà vẫn để open”. Thực hiện kiểm hồi cứu native đã trình ở lượt trước, gồm E9 tắt/bật cửa sổ 55 và T12 bật cửa sổ 43, lưu bản ghi, trung gian và đối chiếu trong results/T-051. Một tiến trình laptop, dự toán 2–4 phút máy. Phạm vi là cùng đầu vào và cấu hình đã ghim, không thay ma trận hay luật chọn. Nối LOG, cập nhật đúng dòng task trong STATE và ghim manifest lượt bổ sung. Đồng thời lập bảng từng vấn đề còn thiếu bằng chứng, kết luận đã có và bước xử lý cụ thể theo nguồn, tránh ghi OPEN chung chung.


### Rà phần còn lại trong lúc kiểm native

Rà lại SPEC và hồ sơ sau đính chính không thấy phép chạy khoa học nào khác còn thiếu trong ma trận T11/T12/KB ngoài ba cấu hình native hồi cứu đang thực hiện. Runner mới ghi đủ record/trace và assert danh sách mismatch rỗng. Không dùng riêng exit code của pilot cũ làm bằng chứng vì pilot_native.py cũ chỉ ghi mismatch mà không assert phần đó.

Đã lập results/T-051/hoan-tat-nguoi-lam.md với bảng kết luận hiện tại, việc tiếp theo, nơi xử lý và phụ thuộc cho từng câu hỏi trước đây ghi OPEN. Nền E9/T12 và khối K đã có lựa chọn cụ thể. Verdict có kết luận chưa chọn được ở WHY-68, nhãn vùng đã gắn P10, đối chứng gắn T-052, (b)/RE3 gắn gói G3 theo Q-211/Q-212. Các giới hạn dữ liệu được ghi thành kết luận về khả năng phân xử. Các phép thăm dò đổi chiều PageRank hoặc tương tác không bị coi là phần T-051 đang chờ chạy. Bảng ghi đề xuất ở đúng mức, không tự đổi quyết định của Minh.


### Kết thúc Phiên 3

1. Đã làm nốt ba cấu hình native hồi cứu, E9 tắt/bật ở cửa sổ 55 và T12 bật ở 43. Đủ ba thế giới có 0 sai khác về F_I, m, khóa/hòa và V0. Ở P còn khớp vùng, kế thừa và các đối chứng của T12. Ca 55 có 2 kênh đổi F_I, ca 43 có 4 kênh đổi. Lưu đủ native.json.gz, input.json, comparison.json, command.json và summary.json trong results/T-051/native-co-tac-dong-001.
2. Tổng lượt native 262,740 giây, khoảng 4,38 phút. Vế E9 tắt 68,703 giây, bật 6,924 giây nhờ dùng lại cache; T12 ca 43 là 186,528 giây. Ca 43 lâu hơn dự toán pilot, đã cập nhật ETA khi chạy. Giữ toàn bộ biên nhận, thời gian và RAM. Một tiến trình laptop.
3. Đã hoàn thiện results/T-051/hoan-tat-nguoi-lam.md. Bảng bàn giao không để OPEN chung mà nêu kết luận, hướng xử lý cụ thể, nơi xử lý, người chịu trách nhiệm và phụ thuộc. Lựa chọn T-051 đã rõ, phần nguồn thiếu bằng chứng giữ đúng giới hạn. T-052 thực hiện đối chứng/G3, P9/P10 thu quan sát và nhãn độc lập, các biến thể thăm dò có câu hỏi và phạm vi riêng. Chưa mở test/dữ liệu giữ ngoài và không tự triển khai task kế tiếp.
4. File viết của lượt này gồm runner kiểm native mới, thư mục và log native, bản tổng kết người làm, LOG này, đúng dòng T-051 của STATE và manifest-dap-phan-bien-002.json. Không sửa báo cáo, seal hoặc manifest lịch sử. Kiểm 261 đầu ra gốc và các tiền tố lịch sử, hash native, trạng thái và schema, số so sánh, cú pháp runner và diff. Phần người làm T-051 có đủ đầu ra hiện có thể kiểm/thu. Còn bước phản biện gói cuối và nghiệm thu. Hai sai lệch thời điểm pilot và ghi thời gian lịch sử vẫn được công khai, không chuyển thành phép chạy còn thiếu.
5. Câu hỏi nguồn. T-051 đã phân xử lựa chọn dev E9/T12/KB theo luật và lần theo tác động từng ca. Hiệu quả độc lập, vùng có nhãn và tác dụng cạnh thông điệp/dữ liệu còn cần bước đánh giá đã gắn trách nhiệm. Không có lựa chọn E9/T12 đang chờ hai bên đề xuất tiếp.

Bước tiếp theo chính xác. Minh có thể chuyển prompt dưới cho Claude đọc bàn giao cuối, native-co-tac-dong-001/summary.json và manifest-dap-phan-bien-002.json, kiểm gói bổ sung. Người làm đề xuất dừng phản biện sau khi không còn phản đối ảnh hưởng tính đúng hoặc phạm vi kết luận. Minh nghiệm thu, sau đó giao T-052 theo kế hoạch. Đề xuất commit khi Minh muốn lưu là “T-051: hoàn tất kiểm native có tác động và bàn giao cuối”.

Lệnh cuối khi chốt. Kiểm hash manifest mới và các hash nguyên gốc, kiểm tiền tố LOG và STATE theo các manifest cũ, giải nén native và đối chiếu record/trace, git diff --check và trạng thái tập file. Lệnh chạy đã thực hiện là Python -B results/T-051/kiem-native-co-tac-dong.py native-co-tac-dong-001. Môi trường và phiên bản thư viện ở command.json.

## Prompt Claude kiểm gói cuối T-051

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: T-051, tasks/T-051-t11-t12-va-kb/SPEC.md.
- Công đoạn: kiểm lại phản hồi và sửa.
- Gói/cổng: P6, chuẩn bị P7, G3 chưa mở.
- Người làm và người phản biện chính thức: Codex là người làm, Claude là người phản biện.
- Tài liệu gốc: AGENTS.md, docs/STATE.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md, docs/KE-HOACH-SAU-T047.md, SPEC T-043 và đính chính, SPEC/LOG T-051, git diff hiện hành.
- Phản biện và phản hồi trước: phản biện lượt 1 của Claude và bản đáp Codex do Minh chuyển, bản đính chính và LOG T-051.
- Code và kết quả liên quan: results/T-051/hoan-tat-nguoi-lam.md, results/T-051/native-co-tac-dong-001, results/T-051/manifest-dap-phan-bien-002.json, các manifest cũ và đính chính T-051 được dẫn trong hồ sơ.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat nếu Minh chưa cấp quyền ghi bản phản biện riêng.

Không sửa ngoài phạm vi trên, không commit. Chưa có quyền ghi rõ ràng thì chỉ đọc và trả lời trong chat. Giữ các bản lượt cũ. Không đọc dữ liệu khóa hoặc chạy thực nghiệm ngoài quyền được duyệt.

Đọc nguồn và đầu ra gốc trước khi đọc kết luận các lượt phản biện/phản hồi. Lập nhận xét độc lập trước, không lấy tóm tắt trong LOG thay bằng chứng trên file thật.
Nguồn đối chiếu: docs/STATE.md, SPEC và LOG nếu có; phần trực tiếp chi phối trong docs/MRP.md, docs/WHY.md, docs/DECISIONS.md, docs/LESSONS.md.
Nguồn đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ và được phép); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.
7. Kiểm cả đạt SPEC và đạt phần mục tiêu nguồn. Nếu chỉ đạt một phần, nêu phần thiếu và quyết định phụ thuộc. Không dùng “chưa kiểm” làm căn cứ đã xác nhận hoặc “ngoài SPEC” để bỏ nghĩa vụ nghiên cứu. Không ép một nguyên nhân vào chỗ chưa biết.
8. Với nhận định quan trọng, hỏi còn nguyên nhân khả thi nào khác giải thích kết quả và bằng chứng có phân xử được không. Trước khi dùng đầu ra cũ, kiểm hash theo manifest phù hợp; lệch thì dừng phần phụ thuộc và báo Minh. Số làm bằng chứng phải có đường dẫn và con trỏ JSON hoặc lệnh đã chạy kèm kết quả.
9. Kiểm tuân thủ quy trình bằng việc thực tế: vai trò, quyền ghi và duyệt phạm vi; nguồn quyết định; tự kiểm; LOG/STATE/bàn giao theo nghĩa vụ của vai trò; tự đổi mục tiêu/tiêu chí/thiết kế; đề nghị chuyển bước khi thiếu căn cứ. Áp dụng luật và quyền có hiệu lực ở thời điểm việc được làm, không tự mở lại task đã đóng. Chỉ báo vi phạm có bằng chứng và ảnh hưởng cụ thể, không chỉ xác nhận đã đọc AGENTS.
10. Sau tự soát, kiểm từng điểm và phản hồi các lượt trước: đúng / đúng một phần / sai / chưa kiểm được, với bằng chứng riêng. Không mặc nhiên đồng ý với bên nào. Nêu phạm vi lỗi rộng/hẹp hơn hoặc mặt trái của đề xuất sửa.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: CHẶN hoặc KHÔNG CHẶN; chặn kết luận/quyết định nào; ở đâu; sai gì;
bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); hậu quả; đề xuất sửa tối thiểu hoặc bằng chứng còn thiếu.
Tiếng Việt, câu ngắn.

Cuối lượt báo:
1. Đã làm gì.
2. File đã thay đổi, hoặc không sửa file nào.
3. Kiểm đã chạy và kết quả.
4. Bất đồng có bằng chứng, câu hỏi mở, phần thiếu và quyết định bị ảnh hưởng; điều cần Minh quyết.

Đề xuất tiếp tục hoặc dừng phản biện, kèm lý do. Nếu không còn phản đối chưa xử lý ảnh hưởng tính đúng, phạm vi kết luận hoặc quyết định đang xin duyệt, đề xuất dừng; không che bất đồng bên kia còn giữ. Có thể thống nhất giới hạn khi thiếu bằng chứng; kết luận phụ thuộc vẫn OPEN. Minh quyết cuối. Hai agent đồng ý không thay bằng chứng khoa học; dừng phản biện không tự duyệt SPEC, đóng task hoặc mở test.

Sau đó soạn prompt bàn giao cho agent đối phương: chép nguyên văn Prompt chung + đúng Khối công đoạn + Khối cổng hiện có trong docs/review-prompt.md, chỉ điền thông tin trung tính. Giữ vai trò; người làm nhận prompt đáp phản biện, người phản biện nhận prompt kiểm độc lập. Vẫn soạn khi đề xuất dừng để Minh chọn gửi hay dừng; không tự gửi.

Công đoạn: người phản biện kiểm lại phản hồi và sửa.
Tự soát yêu cầu và đầu ra gốc trước; sau đó đọc phản biện, phản hồi và các thay đổi được duyệt. Kiểm cả ý kiến phản bác reviewer; không mặc định phản hồi hoặc bản sửa đúng.
Đối chiếu từng điểm với bằng chứng hiện tại, quyền sửa và hậu quả. Có điểm đúng nhưng chưa được Minh duyệt sửa thì ghi đúng trạng thái; không tự coi đã xử lý hoặc ép người làm sửa.
Chỉ ghi bản phản biện lượt mới được Minh cho phép theo tasks/_MAU/REVIEW.md, hoặc trả lời trong chat. Giữ lịch sử, không ghi LOG/STATE hay sửa thay người làm. Nêu bất đồng còn lại và soạn prompt để người làm đáp.

Với từng thành phần, kiểm mục đích và căn cứ: sửa hạn chế P4, đáp ứng DT18 hay nhu cầu kỹ thuật. Có lý do kỹ thuật, phương án khác, bằng chứng dev và điều kiện thất bại không; có dùng mã hạn chế mô tả như bằng chứng cơ chế hoặc chọn theo mức chênh đồ thị trừ không đồ thị không?
Nêu rõ nút/cạnh, ánh xạ log/trace/metric và phép tính thực sự sử dụng cạnh. Lần theo thông tin quan hệ và nhãn trong phương pháp lẫn đối chứng; gọi “không đồ thị” có đúng với thông tin còn giữ không?
Kiểm baseline và đối chứng đủ mạnh, tương đương về tín hiệu/cửa sổ/tập ứng viên/coverage/tiền xử lý/quy tắc chấm/ngân sách chọn cấu hình ở phần không chủ ý thay; yếu tố thay cùng phải giới hạn kết luận.
Phương pháp và đối chứng đã được cài và kiểm đầu vào, trung gian, hành vi trên dev chưa, hay chỉ chạy không lỗi? Không đòi đồ thị phải thắng để khóa.
Code/revision, cấu hình, giả thuyết, độ đo, tập ca/tập ứng viên, cách xử lý ca lỗi/UNSUPPORTED/nhánh dự phòng và bảng diễn giải đã khóa trước test chưa? Có bỏ nhóm khó sau khi nhìn điểm hoặc dùng test để chọn thiết kế không?
Với tự phát hiện, kiểm cả tiền xử lý và ngưỡng có dùng nhãn/mốc tiêm/thông tin tương lai không. Quyền mở test và commit phải có Minh duyệt riêng theo phạm vi; không suy từ đồng thuận review.
```

## Phiên 4 — 04/11/2026 — Codex — Windows — nghiệm thu và bàn giao T-052

### Quyết định của Minh trong phiên

Minh: “nghiệm thu 51, sau đó push lên giúp tôi các phần chưa push, soạn prompt yêu cầu phiên codex mới, nghiên cứu kĩ các kết quả làm được hiện tại, phải đọc hiểu hết các kết quả đã đạt được, có được cái nhìn bao trùm toàn bộ, từ đó đề xuất ra spec cho task t052, các task trước đó có những bài học về viêc sử dụng ec2, yêu cầu agent cần nhắc và cách phân phối hợp lý để đạt thời gian tốt nhất, ec2 nhanh hơn laptop, không quan tâm tiền máy”.

Sau khi được báo lượng file chưa theo dõi và hỏi phạm vi lưu, Minh chọn: “Đẩy hồ sơ và kết quả tổng hợp; giữ trung gian nặng local”. Quyết định lưu ở Q-242–Q-244; không suy quyền soạn SPEC thành quyền chạy T-052.

1. **Đã làm.** Ghi nghiệm thu T-051 trong phạm vi dev đã báo cáo và đính chính; giữ nền Q-241, E9/T12 tắt và cờ E2. Lượt kiểm bổ sung Codex đã đối chiếu nguồn, mã, đầu ra và các ý cũ; không đổi vai trò phản biện chính thức, không ghi Claude đã kiểm gói native cuối. Chuẩn bị commit/push phần hồ sơ, mã và tổng hợp đang chờ theo Q-243/Q-244.
2. **File sửa mới của lượt này.** Chỉ nối docs/DECISIONS.md, nối LOG này, đổi đúng dòng T-051 trong docs/STATE.md. Các báo cáo, SPEC, seal và manifest kết quả lịch sử giữ nguyên byte. Các thay đổi/code/hồ sơ đã có trước phiên được rà riêng trước đưa vào commit theo yêu cầu push.
3. **Kiểm.** Đã đối chiếu STATE/SPEC/LOG với lời nghiệm thu. Lượt kiểm bổ sung trước nghiệm thu xác minh manifest, tính lại RR/độ đo, PageRank, vùng, độ bền và các native đã lưu; không chạy telemetry mới. Fetch xác nhận nhánh local và remote cùng điểm xuất phát. Đã kiểm hash toàn bộ đầu ra gốc T-050/T-051, đầu ra lượt chạy lại T-050 và các đầu ra bất biến của gói T-051 cuối. Đã so tiền tố lịch sử LOG và DECISIONS, kiểm đọc JSON và so tập file đưa vào Git. Dữ liệu khóa và trung gian nặng giữ ngoài Git.
4. **Phạm vi đạt và phần còn thiếu.** T-051 kết thúc phần chọn/mô tả dev T11/T12/KB. Hai sai lệch lịch sử về pilot và đo thời gian vẫn giữ. Hiệu quả độc lập, vùng có nhãn, chiều đảo PageRank, tương tác VC/E5, revision nguồn tĩnh, verdict, chế độ (b), RE3-OB và FlashTicket còn theo nguồn tương ứng; không đóng bằng nghiệm thu. Phiên mới phải đối chiếu toàn cảnh trước đề xuất T-052, không tự chạy lại hoặc mở task đã đóng.

Bước tiếp theo: Minh copy prompt dưới sang phiên Codex mới trong D:/RCA-flashticket. Phiên mới chỉ đọc, tổng hợp và trình SPEC trong chat trước khi được duyệt ghi. Lệnh kiểm gần nhất trước ghi nghiệm thu: git status --porcelain=v1 -uno; git rev-list --left-right --count origin/claude/sweet-hawking-dy078d...HEAD (hai phía bằng 0 sau fetch).

### Prompt phiên Codex mới — nghiên cứu toàn cảnh và đề xuất SPEC T-052

```text
Làm việc trong D:/RCA-flashticket. Đọc AGENTS.md trước.

Minh đã nghiệm thu T-051 ngày 04/11/2026. Quyết định hiện hành ở docs/DECISIONS.md Q-242–Q-244, docs/STATE.md và LOG đóng T-051. Tôi giao phiên Codex mới nghiên cứu kỹ toàn bộ kết quả hiện có, hình thành cái nhìn bao trùm, rồi đề xuất SPEC cho T-052. Không chỉ nối tiếp tóm tắt của phiên trước hoặc điền sẵn một checklist.

Phân loại lượt này là PLAN: đọc, kiểm rẻ chỉ đọc và trình đề xuất trong chat. Chưa tạo/sửa file SPEC/LOG T-052, chưa chạy telemetry/thực nghiệm, chưa khởi động EC2 mới, chưa mở G3/test/dữ liệu giữ ngoài. Codex là người đề xuất SPEC; trình rõ vai trò người làm/người phản biện khi xin duyệt SPEC. Claude vẫn là người phản biện chính thức của T-051. Không tự tạo chat khác hoặc gửi prompt phản biện; Minh chuyển thủ công.

1. Đọc và tự dựng toàn cảnh từ nguồn.
- Đọc AGENTS, STATE, MRP, DECISIONS, WHY, LESSONS, các kế hoạch P6/giai đoạn tới/sau T-047, DT18 và hướng dẫn cô. Phân biệt yêu cầu nguồn, quyết định của Minh, ứng viên và câu hỏi còn mở. Khi nguồn hiện hành và hồ sơ lịch sử khác nhau, lần theo mốc quyết định thay vì chọn câu thuận tiện.
- Theo mục lục task và MRP, đọc hiểu kết quả khoa học đã đạt từ P1/P2 về cơ chế phương pháp/dataset, P3 về baseline và giao thức, P4 về cơ chế hạn chế, P5 về mô hình đồ thị và quan sát. Đọc báo cáo, bảng kết quả, code và trung gian có liên quan của các task đó, không coi task đã đóng là câu hỏi khoa học đã trả lời xong. Đặc biệt lần theo T-022–T-026, T-028–T-034, T-035–T-040 và T-041/T-042 khi chúng chi phối T-052. Kiến thức nền chưa kiểm lại không tự thành bằng chứng.
- Đọc đầy đủ chuỗi M1: T-043 SPEC/đặc tả và mọi đính chính; T-044 cài đặt/fixture; T-045; T-046; T-047; T-048 và T-053; T-049; T-050; T-051. Tự liệt kê hồ sơ, đọc bản gốc và các bổ sung theo thời gian, phân biệt báo cáo tại mốc cũ với quyết định hiện hành. Với T-050/T-051 phải đọc cả đính chính, manifest bổ sung, native và bàn giao cuối, không chỉ bao-cao.md.
- Kiểm hash theo manifest phù hợp trước dùng kết quả. Manifest có thể dẫn tới trung gian giữ local theo Q-244; đọc file thật tại máy khi cần, không gọi file chưa đưa lên remote là file chưa từng tồn tại. Thiếu file hoặc hash lệch thì dừng phần phụ thuộc, báo đúng bằng chứng thiếu. Không đọc data/locked hoặc repo RCA lưu trữ.
- Tự lần theo src/m1/, src/m1_danh_gia/, src/p3/, runner/helper và code chính thức ở revision liên quan khi kết luận phụ thuộc vào chúng. Lần theo quan hệ và nhãn từ đầu vào tới điểm, tập ứng viên, phân loại, hạng và vùng. Đọc code/trung gian trước khi đề xuất tính lại.
- Tự lập nhận xét từ nguồn và đầu ra trước, sau đó kiểm phản biện/phản hồi. Phản biện chỉ lưu qua chat hoặc tóm tắt phải được ghi đúng loại nguồn; không coi lời báo đã kiểm là biên nhận native.

2. Trình bản tổng hợp đủ để chứng minh đã hiểu toàn hệ thống.
- Nêu câu hỏi nguồn nào đã được trả lời tới mức nào; bằng chứng nào hỗ trợ, bác bỏ hoặc chưa phân xử; tác động tới quyết định đang chuẩn bị. Mỗi số có đường dẫn và con trỏ JSON hoặc lệnh/kết quả.
- Giải thích chuỗi M1 hiện hành, nút/cạnh, log/trace/metric, vai trò tính toán thật của đồ thị, các nhánh bỏ quan hệ và quy tắc đơn giản còn giữ thông tin cấu trúc nào. Tách lựa chọn trên dev khỏi khẳng định lợi ích độc lập.
- Lập bản đồ phụ thuộc của T-052: đầu ra còn dùng được, điều kiện tái sử dụng và phép kiểm cần thiết; lỗi/sai lệch đã xử lý; giới hạn đã chấp nhận; phần chưa làm, thiếu dữ kiện hoặc dữ liệu hiện có không thể phân xử. Không ép OPEN thành lỗi mới hoặc dùng ngoài SPEC để bỏ nghĩa vụ nghiên cứu.
- Bắt buộc đọc lại kinh nghiệm dùng máy trong LOG T-047/T-048/T-049/T-050/T-051/T-053 và các nguồn trước có liên quan. Nhắc bài học bằng dẫn chứng, không chỉ nói đã đọc.

3. Tối ưu thời gian và phân phối EC2.
Minh xác nhận EC2 nhanh hơn laptop và không quan tâm tiền máy. Ưu tiên EC2 cho phần tính nặng; mục tiêu là thời gian hoàn tất toàn gói, không tối thiểu hóa chi phí tiền máy. Không mặc định chạy chính trên laptop, hoặc giữ số tiến trình cũ chỉ vì task trước dùng như vậy. Không cần mở phép so tốc độ laptop mới nếu không có quyết định nào phụ thuộc vào nó.
- Đọc số pilot, lịch phân phối và thời gian thật của các task trước; tách số đã đo khỏi ngoại suy. T-048 từng phải cân lại tải; T-053 từng gặp SSH chờ sau khi worker đã xong và đầy đĩa lúc bootstrap; T-049/T-053 từng chọn nhầm môi trường thiếu thư viện. Đọc đúng các LOG để hiểu điều kiện, cách sửa và giới hạn.
- Đề xuất máy/cấu hình và số tiến trình theo CPU/RAM/đĩa, tải thực và vị trí dữ liệu. Chia theo chi phí đo được; dùng laptop làm phần nhẹ/độc lập nếu giảm thời điểm hoàn tất cuối. Giữ các vế một phép so trên cùng máy khi sai khác số thực ảnh hưởng đối chiếu. Không suy hệ số tăng tốc của một lát cắt thành hệ số chung.
- Tận dụng đầu ra/cache/phát lại đã kiểm tương đương. Không chạy lại dữ liệu nặng để tạo lại đầu ra đã hợp lệ; cũng không coi replay khớp chính nó là native parity. Pilot tương lai phải chạm nhánh cơ chế có tác động, có biên nhận ghim trước chấm khi SPEC yêu cầu.
- Preflight đúng instance, Python executable, phiên bản/import/PYTHONPATH, nguồn dev, dung lượng và dữ liệu sẵn có. Môi trường Python laptop từng dùng không khởi động được trong lượt kiểm gần nhất; xác minh trạng thái hiện tại, không giả định đường dẫn trong manifest là môi trường còn chạy được.
- Đề xuất cách chạy tách SSH, lưu PID/timeout/checkpoint/biên nhận, tiếp nhận lại bằng hash và chỉ chạy phần thiếu. Đọc đúng bài học SSH keepalive, theo dõi cả cây tiến trình và phân biệt đang tính với đang chờ kết nối.
- Dự toán cả chuyển dữ liệu, đọc/hash/giải nén, tính, chấm/bootstrap, truy vết, đóng hồ sơ và tự kiểm. Tính thời gian tổng theo nhánh chậm nhất, nêu tài nguyên đỉnh và phương án tránh đầy đĩa. Ghi thời gian từng công đoạn ngay từ đầu khi được triển khai; giữ mọi lượt hỏng. Không tự dọn dữ liệu cũ.
- Tiền máy không là ràng buộc chọn phương án. SPEC vẫn phải nêu thời gian, tài nguyên, mức song song và quyền thực thi cần duyệt theo AGENTS; chỉ đạo này không tự là quyền chạy một thực nghiệm chưa có SPEC.

4. Từ toàn cảnh đó, đề xuất SPEC T-052 trong chat.
Đối chiếu mẫu tasks/_MAU/SPEC.md, mục T-052 trong kế hoạch hiện hành, T-043 A4/B6/B4 và MRP. Xác định phần T13, baseline/đối chứng, vùng trên cấu hình cuối và hồ sơ G3 thực sự cần làm. Giữ C-d2 và các giới hạn đối chứng theo nguồn; không dựng mục tiêu phương pháp phải thắng.

Nêu câu hỏi, phép phân xử, ma trận/cấu hình, tập ca/ứng viên, độ đo/quy tắc chấm, xử lý lỗi/UNSUPPORTED/fallback, trung gian cần lưu, nguồn tái dùng và căn cứ, bước phụ thuộc, lịch phân phối máy, tiêu chí xong, phạm vi ghi, dự toán/trần và rủi ro. Tách phần nghiên cứu được trả lời khỏi phần chỉ đóng hồ sơ. Những quyết định còn cần về verdict, chế độ (b), RE3-OB và G3 phải có phương án có căn cứ để Minh chọn; không chỉ chép danh sách OPEN. Không tự mở test hoặc biến nghiệm thu T-051 thành duyệt G3.

Nếu khối việc không vừa một phiên, đề xuất tách theo phụ thuộc và đầu ra, không giảm kiểm để vừa thời gian. Không mặc định chia task trước khi hiểu khối lượng. Cuối lượt trình: tổng hợp hiểu biết và nguồn đã kiểm; đề xuất SPEC; các lựa chọn còn cần Minh quyết kèm khuyến nghị; báo không sửa file; soạn prompt Claude soát SPEC bằng nguyên văn Prompt chung + khối Soát SPEC + khối G3 trong docs/review-prompt.md. Prompt phản biện chỉ điền thông tin trung tính. Dừng chờ Minh duyệt đúng phạm vi ghi và triển khai.
```
