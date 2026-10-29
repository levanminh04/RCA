# Khảo sát sâu K1–K6 cho kế hoạch giai đoạn tới

- **Ngày:** 23/10/2026. **Người soạn:** Claude, phiên khảo sát theo việc A10 và Phụ lục P3 của [KE-HOACH-GIAI-DOAN-TOI.md](KE-HOACH-GIAI-DOAN-TOI.md). Minh cho phép dùng subagent (M-40).
- **Quyền tạo file:** lời Minh ngày 23/10/2026: "duyệt ghi tài liệu sâu đó soạn prompt cho codex yêu cầu phản biện, rà soát sâu . yêu cầu codex phải kiểm chứng các tài liệu mà bạn đã tuyên bố". Khi được hỏi nội dung file, Minh chọn "Báo cáo + trả lời + prompt".
- **Trạng thái:**
  - Đây là khảo sát tài liệu. Không đề xuất nào đã được thử trên dữ liệu.
  - Mọi mã KS-xx là [ĐX], chưa duyệt, trừ: KS-07 đã duyệt cùng E-04 (M-44 trong KE-HOACH); KS-10, KS-11, KS-14, KS-16 được đưa vào SPEC M1 làm ứng viên để thử (M-48 trong KE-HOACH). Trạng thái từng mã ở mục 3.
  - Đã qua phản biện và kiểm lại của Codex ngày 23/10/2026; các sửa ghi ở Phụ lục C. Prompt lượt đầu ở Phụ lục B.
- **Quan hệ với tài liệu khác:** file này không thay KE-HOACH, MRP, WHY, DECISIONS. Đề xuất sửa nằm ở mục 3, chờ Minh duyệt theo Luật 0.
- **Cách làm:**
  - Claude đọc trực tiếp các nguồn repo mà Phụ lục P3 yêu cầu.
  - Sáu subagent chỉ đọc khảo sát song song: K1 phần A (đồ thị gọi/trace/topology); K1 phần B (nhân quả, thời gian, benchmark); K2; K3; K4; K5.
  - Claude tổng hợp và tự kiểm lại các điểm ảnh hưởng cao.
- **Nhãn:**
  - [GỐC]: subagent báo đã đọc thân bài, bảng, mã hoặc tài liệu chính thức.
  - [THỨ CẤP]: chỉ đọc abstract, trang hội nghị, blog, diễn đàn hoặc bài khác dẫn lại.
  - [SUY LUẬN]: suy luận của subagent hoặc của Claude.
  - [TÍNH]: số tự tính, có giả định.
  - [ĐÃ KIỂM]: Claude tự kiểm lại trong phiên, trên file repo hoặc tài liệu chính thức.
  - Phần lớn [GỐC] là do subagent đọc. Claude chỉ kiểm lại những điểm có nhãn [ĐÃ KIỂM].

---

## 1. Tóm tắt: nên đổi gì, xếp theo mức ảnh hưởng

1. **Baseline trên Nezha-OB lệch xa số công bố, chưa có giải thích** [ĐÃ KIỂM].
   - Bài SimpleRCA báo Top@1 0,91 trên Nezha-OB, 56 ca (`results/T-017/so-cong-bo.csv`). Repo đo 0,318 trên 22 ca dev.
   - MicroRank cũng lệch: bài Nezha báo 41,07% (`results/T-026/runs/session-005/published-reference.json`, hash khớp), repo đo 0/22. T-026 ghi "chưa có nguyên nhân xác nhận".
   - Theo bài SimpleRCA, Nezha-OB có 0% ca Type III (`results/T-017/type-i-ii.md`). Tỷ lệ này theo luật của tác giả. T-017 ghi luật chưa đủ đặc tả để tái tạo, và tỷ lệ không xác nhận độ khó hay quan hệ nhân quả.
   - Hệ quả: mục tiêu "Nezha-OB: cải thiện" (D.1) có thể đặt sai chỗ. Các hạn chế P4 rút từ bộ này, ví dụ lỗi return 0/4, có thể do adapter hoặc giao thức. Không dùng tỷ lệ Type để kết luận về chỗ cho đồ thị: G2-H06 ghi ở 5/6 ca trễ mạng Nezha-OB, root đứng đầu theo span phía gọi. Đây là dấu hiệu thông tin quan hệ có thể hữu ích, chưa phải bằng chứng phương pháp đồ thị sẽ thắng.
   - Đề xuất KS-15; xem thêm Phụ lục A.1 và A.3.
2. **Khả năng phân xử của dev còn hạn chế; cần xác định theo từng cơ chế và độ đo.**
   - Tỷ lệ Type III theo luật của tác giả: RE2-TT 17%, Nezha-OB 0% [ĐÃ KIỂM số trong `results/T-017/type-i-ii.md`].
   - RE2-TT: max call depth 5, phủ 39% service. Nezha-OB: max call depth 2 [GỐC, SimpleRCA v2 Bảng 1, §6.1.2]. Bài dùng max call depth làm chỉ báo cho độ phức tạp nhân quả tiềm năng; đó không phải độ sâu lan đã xác nhận của từng ca.
   - Trên RE2-TT dev30, TORAI B có Hit@3 = 1,0. Vì vậy ở độ đo top-3, phần cải thiện chỉ còn là xếp lại trong top-3. TORAI B không chạy được trên Nezha-OB (`results/T-034/goi-g2.md` §2.4).
   - Trên benchmark có max call depth 7 (1.430 ca Train Ticket), Top@1 của MicroRCA là 0,37, BARO 0,36, SimpleRCA 0,28 [GỐC, FSE 2026 Hình 9].
   - WHY-03 ghi: RE2-TT không cho khái quát sang topology khác, nhưng vẫn kiểm được một cách dùng quan hệ trên các vị trí đang có ("chưa biết" khác "không được", SL21). G2-H06 ghi dấu hiệu ở span phía gọi trong 5/6 ca trễ mạng Nezha-OB.
   - Hệ quả: nếu dev có ít ca phân xử được cho một cơ chế, tiêu chí bác bỏ của cơ chế đó ở D.2 có thể bác nhầm; KS-16 đếm trước. Thêm dataset là ứng viên để Minh cân nhắc. Lập luận "FlashTicket có lợi thế thông tin nên sẽ vượt" yếu. Điều quyết định là loại lỗi và điểm mù, không phải lượng thông tin.
3. **Quy tắc ban đầu của E-04 không phải phép kiểm không thua (non-inferiority, NI). Thống kê phải gom theo ô.**
   - Theo FDA, ICH E9 và EMA, kết luận NI đòi khoảng tin cậy (CI) nằm trọn phía tốt của biên.
   - Power với Δ_MRR = 0,05 khoảng 0,11 (n = 30) và 0,19 (n = 60) [TÍNH, giả định ở Phụ lục C].
   - TORAI B so với BARO: p = 0,0195 nếu kiểm theo ca, p = 0,1875 nếu kiểm theo ô [ĐÃ KIỂM, `results/T-024/cham-a.json`; hash khớp `results/T-024/work/danh-sach-tep-cuoi.json:15`].
   - Ngày 23/10/2026 Minh duyệt E-04 theo bản sửa KS-07 (M-44), rồi làm rõ cách đọc thành hai câu hỏi báo đồng thời (M-45).
4. **Không dùng được "nhiệt độ 0" ở L5 với Claude hiện hành** [ĐÃ KIỂM].
   - Từ phiên bản API `2026-10-21`, mọi model trả lỗi 400 khi request có `temperature`, `top_p` hoặc `top_k`.
   - Có ba bài báo LLM xếp lại hoặc tổng hợp ứng viên thắng BARO trên RCAEval. Phần còn thiếu: chưa bài nào vừa ẩn tên service vừa báo phương sai; đối chứng thay agent bằng luật chỉ có ở GALA+ và chỉ chạy trên OB. Lợi ích chưa tách được giữa LLM và các thành phần khác (xem K2).
5. **Nhánh H (đồ thị gộp cảnh báo) có nhiều tiền lệ và rẻ. Với nhánh G (đồ thị quyết định báo động): công nghiệp có bộ phát hiện dựa trên cấu trúc trace theo endpoint (CRISP, Uber); chưa thấy công cụ dùng điểm toàn hệ tổng hợp trên đồ thị phụ thuộc như G.**
   - Một cách hiểu ví dụ "PageRank anomaly" (AnomRank) thuộc kiểu G; chưa có căn cứ đây là thuật toán cô định nhắc. Đây là một rủi ro khi bảo vệ.
   - Đề xuất nâng H (KS-13) mâu thuẫn với M-20; Minh quyết. Giải thích G và H ở Phụ lục A.4.
6. **Mô-đun phương pháp:**
   - E5 có hai cách cài, bằng chứng ngược nhau.
   - E9 hạ xuống thành phép phủ quyết.
   - Thêm: tín hiệu cấu trúc trace; trạng thái "ngừng sau mốc"; cạnh thông điệp lấy từ span link; dung sai lệch đồng hồ.
   - Thêm hai đối chứng.
7. **Đính chính hạ tầng:**
   - Chaos Monkey đã có bản 4.0.0 hỗ trợ Boot 4.
   - OTel agent 3.0 đổi tên thuộc tính `db.*` và `messaging.*`.
   - 4/5 service dùng PostgreSQL [ĐÃ KIỂM]. SMTP là cạnh mù.
   - Synthetics không cần endpoint công khai.
8. **Chống thiên lệch trên FlashTicket cần thêm luật**, gồm việc lọc tín hiệu của công cụ tiêm lỗi khỏi đầu vào RCA (luật cứng 6).
9. **Phương án B của C-15 có rủi ro đo được.** Sửa đúng 3 ca đã thấy trên 60 ca test làm Hit@1 tăng 0,05, bằng đúng Δ.

Không đề xuất đổi AGENTS hay DECISIONS. Các đề xuất bổ sung cho file kế hoạch, hoặc cho các đoạn sửa MRP/WHY đã duyệt hướng ở bảng C.1.

---

## 2. Phát hiện theo từng câu

### K1. Phương pháp RCA dùng đồ thị, 2023–2026

| Phương pháp | Điểm đáng chú ý cho kế hoạch | Nguồn | Nhãn, tin cậy |
|---|---|---|---|
| Benchmark FSE 2026 (bài của SimpleRCA) | Dataset cũ phần lớn Type I/II. Bộ mới có max call depth 7 (chỉ báo, chưa phải độ sâu lan của từng ca): đồ thị chỉ ngang BARO; SimpleRCA cao nhất Top@5 (0,80). Thất bại do: thành phần không giám sát (DB); mất tín hiệu (PodKill); giả định gãy | https://arxiv.org/html/2510.04711v2 Bảng 2, 3, Hình 9, §6.2.4 | [GỐC]; cao. Bản công khai là artifact rút gọn 10 ca, 8 ca dùng được (`results/T-012/the-dataset.md`, mục FSE); bộ đầy đủ 1.430 ca chưa thấy công khai |
| CRISP (ATC 2022) | Thuật toán đường găng (con kết thúc cuối, cắt span chồng, dung sai lệch đồng hồ 1 ms). Phần con vượt khoảng của cha bị cắt: việc bất đồng bộ chạy sau khi cha kết thúc không lên đường găng; lời gọi bất đồng bộ được chờ xong có thể nằm trên đường găng; con song song kết thúc sớm có thể không. CRISP cũng phát hiện bất thường bằng autoencoder trên vector đường găng theo endpoint ở Uber. Dùng làm bộ chấm RCA thì yếu: MRR 24,83% trên RE2-OB | PDF ATC'22 §5.1–5.2; RCLAgent (arXiv 2605.14866) Bảng I | [GỐC]; cao |
| TraceDiag (FSE 2023 industry) | Gần nhất với E1 → E5 → E7: thời gian độc quyền/bao gồm, tỉa đồ thị, phân bổ Shapley kiểu Budhathoki. Không so baseline đơn giản; ít ca | https://arxiv.org/abs/2310.18740 Bảng 6–7 | [GỐC]; trung bình |
| PetShop (CLeaR 2024) | Quy tắc Traversal theo mã tác giả (commit `2e96f93`, `_traversal_rca`, `_score_potential_root_causes`): ứng viên là nút bất thường không có nút nguyên nhân (predecessor trong đồ thị nhân quả) nào bất thường, **và** có đường gồm toàn nút bất thường nối tới nút mục tiêu; điểm là tổng điểm bất thường lớn nhất trên các đường đó. Nút nguyên nhân thường ứng với phía được gọi (phụ thuộc) [SUY LUẬN]. Khi có đồ thị: ở top-1 (Bảng 8), Traversal bằng hoặc hơn phân bổ phản thực tế ở 6/6 ô; ở top-3 (Bảng 3), Traversal thua phản thực tế ở 2/3 ô latency (0,57 so với 0,71; 0,79 so với 0,86). Phân bổ đạt 0 ở top-1 với lỗi availability. Mọi phương pháp đều "tìm ra" root ngay trong đoạn bình thường | https://arxiv.org/html/2311.04806v2 Bảng 3, 8 | [GỐC]; cao |
| PRISM (arXiv 2601.21359) | Không đồ thị: root bất thường cả nội bộ lẫn bên ngoài. Điều kiện về thứ tự điểm quan sát được (nội bộ của root lớn hơn nội bộ lớn nhất của thành phần bị ảnh hưởng) đúng ở 66,5% ca. Với DELAY, thứ tự "nội bộ trước" chỉ đúng 27,4% | Bảng 2, 11, 15; phụ lục D.2 | [GỐC]; thấp–trung bình |
| MicroDig (TSC 2024) | Nút mức lời gọi cộng nút service; MRR cao nhất trên benchmark sâu (0,48) | DOI 10.1109/TSC.2024.3402172 | [THỨ CẤP]; trung bình |
| TraceContrast (ICSE 2024) | So mẫu đường gọi giữa trace thường và trace bất thường. Mạnh nhất nhóm trace không LLM trên RE2-OB (MRR 45,79%, theo bên thứ ba) | researchr ICSE 2024; RCLAgent Bảng I | [THỨ CẤP]; trung bình |
| DiagMLP (arXiv 2501.02766) | Thay GNN trong Eadro/TVDiag bằng MLP, giữ tiền xử lý: kết quả ngang hoặc hơn | Bảng IV | [GỐC]; trung bình–cao |
| Groot (ASE 2021) | Đồ thị service ngây thơ: top-1 3%; bỏ cả luật động và luật có điều kiện: 33%; bản đủ: 78%. Chất lượng cạnh quan trọng hơn thuật toán lan | https://ar5iv.labs.arxiv.org/html/2108.00344 | [GỐC]; trung bình |
| "Where RCA Fails" (arXiv 2609.36686) | Tách lỗi "không lấy được root" khỏi "lấy được nhưng xếp thấp". RCAEval đã có `--report-decomposition`, `--report-chance` | arXiv; README RCAEval | [GỐC] qua K2; trung bình |
| GNN có giám sát (DynaCausal, CHASE, Eadro) | Cần nhãn root khi train. RE2 chỉ 5 root nên dễ học "service hay là root" | arXiv 2510.22613, 2406.19711 | [GỐC]; thấp–trung bình |

**Đề xuất cho D.2** (KS-10, KS-11):

- **E1.**
  - Thêm dung sai lệch đồng hồ theo CRISP.
  - Trước lượt 1, đếm tỷ lệ span có con chạy song song lệch pha. Nếu tỷ lệ thấp, E1 gần trùng phép trừ hợp khoảng con.
  - Báo lợi ích theo từng loại lỗi.
- **E5.** Có hai ứng viên, bằng chứng ngược nhau. Minh chọn, hoặc giữ cả hai:
  - Quy tắc Traversal trên đồ thị quan sát: không có nút nguyên nhân bất thường, và có đường toàn nút bất thường tới nút mục tiêu (định nghĩa đầy đủ ở bảng K1, dòng PetShop). PetShop so trực tiếp: ở top-1 bằng hoặc hơn phân bổ ở 6/6 ô; ở top-3 thua ở 2/3 ô latency. Đủ để là ứng viên, chưa đủ để chọn.
  - Phân bổ Shapley trên topology đã tỉa. TraceDiag chạy trong sản xuất, nhưng không so với baseline đơn giản.
  - Nếu chọn Traversal, phải tách rõ phần E5 thêm so với C-d.
- **E9.**
  - Chỉ dùng làm phép phủ quyết có dung sai: ít nhất hai lần chu kỳ lấy mẫu cộng độ lệch đồng hồ.
  - Tắt với lỗi mạng.
  - Trên Nezha (1 điểm mỗi phút), ghi "thiếu dữ liệu".
- **Thêm E3b: tín hiệu cấu trúc trace**, nhắm vào lỗi return.
  - [ĐÃ KIỂM] `statusCode` rỗng trên RE2-TT: `results/T-002/local-inspection/run-002/summary.json#/re2tt` ghi `n_spans` 22.834.238, `status_nonnull` 0 (hash khớp `results/T-002/handoff-manifest.json`).
  - Mẫu RE2-OB có giá trị; không suy ra toàn bộ RE2-OB. Nezha: chưa kiểm.
- **Ghi chú 6 ở D.2.** Tách hai trạng thái "chưa từng quan sát" và "ngừng sau mốc".
- **E8.** Cạnh RabbitMQ lấy từ span link; không ghép consumer vào đường găng HTTP.
- **E6b.** Chạy sau E4 và E5.
- **Loại trừ GNN có giám sát.**
- **D.5.**
  - Thêm C-g: bộ chấm cục bộ mạnh cộng đúng bước đồ thị của chuỗi.
  - Thêm C-h (tùy chọn): baseline kiểu PRISM.
  - Viết cụ thể C-d bằng Traversal.
  - Viết C-a kèm danh sách quan hệ còn giữ ở từng bước: đặc trưng, điểm, tập ứng viên, xếp hạng. Kiểu DiagMLP "bỏ đồ thị, giữ tiền xử lý" chỉ đo phần đóng góp của bước bị bỏ phía sau, vì tiền xử lý vẫn mang quan hệ (E1 dùng cha–con, E2 dùng cạnh). Ví dụ, chưa chốt: C-a0 không giữ cha–con và cạnh; C-a1 giữ cha–con ở E1, bỏ cạnh dịch vụ.

### K2. LLM ở các khâu trung gian

**Phát hiện:**

- **Tách mẫu log.**
  - LILAC đạt GA 92,7 và FGA 92,4; Drain đạt 84,3 và 55,4. Trung bình khoảng 280 lần gọi LLM mỗi dataset [GỐC, arXiv 2310.01796 Bảng 1].
  - **Chưa có bằng chứng tách mẫu tốt hơn thì RCA tốt hơn.** Với phát hiện bất thường, yếu tố quyết định là tính phân biệt giữa log bình thường và log lỗi [GỐC, arXiv 2305.15897].
- **Trích phụ thuộc từ code.** Code2DFD đạt F1 cạnh 0,87 [GỐC, arXiv 2412.08352 Bảng 5b]. Agent GPT-4o đạt F1 0,604 cho toàn kiến trúc [THỨ CẤP, ESEM 2026]. Hai số khác độ đo (F1 cạnh so với F1 tổng kiến trúc), không so trực tiếp.
- **Agent điều tra.**
  - Con số 11,34% của OpenRCA đang bị tranh luận [GỐC, issue #23 của microsoft/OpenRCA].
  - OpenRCA 2.0: AnySvc (nêu đúng ít nhất một service gốc) trung bình 76,0% trên 11 model; Path Reachability 61,5%; Exact Match 20,7% [GỐC, arXiv 2606.27154 §3.2].
  - Một bài khác (arXiv 2608.21310) báo Acc@1 90,0% cho một cấu hình trên RCABench, chi phí tới 4,64 USD mỗi ca. Bài này ghi phần lớn ca sai của Sonnet là nguyên nhân bịa ngoài schema [GỐC].
  - Hai số 76,0% và 90,0% khác độ đo và tập đánh giá, không ghép thành một khoảng.
- **LLM xếp lại.**
  - GALA+ đạt AC@1 74,44 so với 14,44 của BARO (RE2-OB), và 73,33 so với 66,67 (RE2-TT) [GỐC, arXiv 2608.08968 Bảng 1]. GALA+ không chỉ xếp lại: nó gộp BARO với STRIX (chấm cấu trúc trace và đồ thị) và có bước điều tra theo đồ thị.
  - Ablation (§5.3.3), mỗi lần thay một thành phần: bỏ STRIX, OB 74,44 → 35,56, TT 73,33 → 68,89; thay agent hợp nhất bằng RRF hoặc agent tổng hợp bằng đếm ngưỡng, OB còn 63,33 (chưa chạy trên TT). Các thành phần đều có đóng góp trong cấu hình được đo; chưa chia được tỷ trọng giữa trace, đồ thị và LLM [GỐC].
  - Kết quả là trung bình 3 lượt (§8), không báo độ phân tán; dấu ± chỉ có ở RQ5 (5 seed, 30 ca OB). Bài không ẩn tên service [GỐC].
  - McNemar (§5.3.1) tính trên kết quả đa số phiếu theo từng sự cố qua 3 lượt, kiểm định nhị thức chính xác một phía; cặp bất đồng 27/4 (OB) và 35/12 (TT) [GỐC].
  - Câu "mồi nhử được xếp đầu ở 21–42% ca" (bài trên Research Square, rs-11401166): chỉ đọc được tiêu đề, chưa kiểm; không dùng làm căn cứ.
- **LLM chấm lời giải thích.** GALA: SURE-Score tương quan Spearman ρ = 0,92 với 3 SRE trên 20 mẫu; bản tham chiếu được sinh có đưa nhãn đúng [GỐC]. Số κ = 0,92 ở arXiv 2601.22208 là độ khớp khi gán taxonomy lỗi cho 30 reasoning trace, không phải chấm lời giải thích.
- **Giá** [ĐÃ KIỂM]: Sonnet 5.5 là 2/10 USD mỗi triệu token (vào/ra); Haiku 5.5 là 0,10/0,50 USD khi prompt ≤ 100k token (trên mức đó 0,50/2,50); Batch rẻ hơn 50%.
- **Grafana Assistant.** Không ghim được model; chưa tìm thấy cam kết tái lập kết quả [GỐC].

**Đề xuất (KS-12):**

- **L1.** Thêm đường gốc Drain có regex che ID. Đo độ mịn của mẫu và tính phân biệt.
- **L2.** Trích tĩnh trước. LLM chỉ làm bước hai, chạy 3–5 lần.
- **L5.**
  - Bỏ "nhiệt độ 0". Thay bằng: ghim model ID và header phiên bản API; chạy N ≥ 5 lần; báo độ lệch chuẩn.
  - Có năm đối chứng: phương pháp chính đứng riêng; bộ xếp lại bằng luật trên cùng gói bằng chứng; LLM chỉ thấy tên ứng viên; có mồi nhử; lệch mốc ±2 phút.
- **L6.** Chấm hai tầng:
  - kiểm tự động rằng mỗi khẳng định trỏ tới một ID bằng chứng có thật;
  - LLM-judge thuộc họ model khác, được hiệu chỉnh với người trên 50–100 mẫu.
- **So với Grafana Assistant:** chỉ so định tính.
- **Sửa một câu ở D.3:** "LLM kém khi tự đào telemetry thô" đổi thành "agent tự đào telemetry đắt, khó tái lập, hay suy luận không có căn cứ".

### K3. Đồ thị trong báo động và gom cảnh báo

**Phát hiện:**

- **CNSS** là "Calibrated Nonparametric Scan Statistics" (AAAI 2022). Nó quét các đồ thị con liên thông, có hiệu chỉnh [GỐC, https://arxiv.org/abs/2206.12786]. Chưa thử trên dữ liệu IT.
- **ART.** Đồ thị nằm trong bộ phát hiện; được đo theo ca, không theo số báo giả mỗi giờ [GỐC].
- **Gom cảnh báo theo topology có nhiều tiền lệ.**
  - GRLIA: NMI 0,83–0,91 [GỐC, Bảng IV].
  - DiLink: F1 0,963 [GỐC, Bảng 2].
  - Dynatrace gom sự kiện theo đồ thị nhân quả [GỐC].
  - GitLab sinh `inhibit_rules` từ khai báo phụ thuộc [GỐC, số tự công bố].
- **G:** công nghiệp có bộ phát hiện dựa trên cấu trúc trace theo endpoint (CRISP, Uber). Chưa thấy công cụ dùng điểm toàn hệ tổng hợp trên đồ thị phụ thuộc như G. Warden (Microsoft) phát hiện ở mức hệ thống mà không dùng đồ thị [GỐC].
- **Grafana.** IRM chỉ có trên Cloud. Inhibition ở Grafana 13 là API beta, chưa có giao diện [GỐC].
- **Dữ liệu.** RCAEval mỗi ca chỉ một lỗi, nên không đo được việc gộp nhầm hai sự cố.

**Đề xuất (KS-13):**

- Nâng nhánh H thành một task nhỏ, làm sau khi Mô-đun B chạy trên dev.
  - H0: sinh inhibition từ đồ thị P5.
  - H1: gom theo nhãn tự sinh/kế thừa của B.
  - Đo: tỷ lệ nén; số sự cố bị nén mất (phải bằng 0); số lần gộp nhầm.
  - Thêm kịch bản hai lỗi chồng thời gian.
- Thêm phép quét đồ thị con kiểu CNSS cho "vùng ảnh hưởng".
- Giữ G hoãn.
- Trả lời hội đồng bằng phân loại GAD (Ma và cộng sự, TKDE 2021).

### K4. Cách đánh giá

**Phát hiện:**

- **Độ đo.**
  - Với một root, AC@k = Hit@k [GỐC, RCAEval §4.2].
  - RCAEval, FSE 2026 và Eadro đều không có kiểm định hay CI.
  - Cách xử lý ca lỗi làm lệch số: TraceRCA đạt 0,700 khi tính ca lỗi là trượt, 0,808 khi loại ca lỗi [TÍNH].
- **Phép kiểm.** Theo Urbano (SIGIR 2019), t-test và permutation giữ đúng mức α; Wilcoxon thì không [GỐC].
- **Dữ liệu repo.** 21/30 ca có chênh lệch RR bằng 0 [ĐÃ KIỂM].
- **Biên NI.**
  - FDA ghi rằng thiết kế kém tạo "bias toward the alternative" [GỐC, https://www.fda.gov/media/78504/download §III.C].
  - ICH E9 ghi rằng suy ra NI từ một kiểm định không có ý nghĩa là "inappropriate" [GỐC].
- **Đặc tính của quy tắc điểm ước lượng** [TÍNH, giả định ở Phụ lục C]: với MRR và n = 60, một phương pháp kém thật 0,10 vẫn qua khoảng 14% số lần. Số 32% cho Hit@1 chưa tái lập.
- **Cỡ mẫu FlashTicket** [TÍNH, Phụ lục C]: với tỷ lệ thành công của **một** phương pháp p = 0,7, 60 sự cố cho nửa độ rộng ±0,14–0,16; muốn ±0,10 cần 113–145 sự cố. Các số này đã nhân hệ số thiết kế 1,4–1,8 (3 lần lặp mỗi ô, ICC 0,2–0,4). ICC là giả định để xét độ nhạy, chưa được ước lượng. Đây không phải cỡ mẫu cho chênh giữa hai phương pháp.
- **Phát hiện bất thường.** Point-adjust biến điểm ngẫu nhiên thành SOTA (Kim, AAAI 2022). Theo SRE, cảnh báo được đánh giá bằng precision, recall, detection time và reset time [GỐC].

**Đề xuất:** KS-07 (đã duyệt cùng E-04), KS-08, KS-09.

### K5. Hạ tầng

- **OTel Java agent.**
  - Bản 2.32.0 (03/10/2026) là bản ứng viên của 3.0. Bản 3.0 đổi tên `db.*` và `messaging.*`; Hibernate mặc định tắt [GỐC].
  - Issue #14906 về hỗ trợ Boot 4 đã đóng. Issue #20199 xác nhận span tạo bình thường trên Boot 4.0.8 [GỐC].
  - Khóa MDC của agent là `trace_id`, còn B16 dùng `traceId`.
  - Agent không có instrumentation cho Jakarta Mail.
- **Tiêm lỗi.**
  - Chaos Monkey v4.0.0 (06/02/2026) build với Boot 4.0.2 [GỐC]. Chọn được tới package, class, method qua `watchedCustomServices`; tiêm latency và exception; tài liệu không có tiêm giá trị trả về. Chạy với Boot 4.1.1: chưa kiểm.
  - Toxiproxy v2.13.0 có token.
  - Pumba không có bản Windows.
  - chaosd chạy được không cần Kubernetes.
  - FIS tính 0,10 USD mỗi action-phút ở khu vực thường. Cấu hình mặc định trên interface chính của host chưa bảo đảm nhắm đúng cạnh giữa hai container cùng máy. FIS cho đặt `Interface`, lọc theo `Sources` (IP/CIDR) và `TrafficType`, và dùng SSM document tùy biến; tiêm đúng cạnh container bằng các cách này: chưa kiểm [GỐC + SUY LUẬN].
- **FlashTicket** [ĐÃ KIỂM `services/*/pom.xml`]. Booking, event, payment, ticket dùng JPA với PostgreSQL. User dùng MongoDB. Ticket và user có SMTP.
- **Grafana Cloud.**
  - Investigations có trong gói Free.
  - Chỉ 3 người xem hoạt động mỗi tháng.
  - Dữ liệu vượt hạn mức bị bỏ, không tính tiền [THỨ CẤP, 2023].
  - Knowledge Graph đòi nhãn môi trường trên mọi metric: `deployment.environment.name`, rồi `deployment.environment`; thiếu thì ghi "unknown". `service.namespace` không được ghi là bắt buộc. Định danh host để tính phí App O11y dùng một trong `k8s.node.name`, `host.id`, `grafana.host.id`. Host ngoài Kubernetes cần Node Exporter. Trang prerequisites vừa liệt kê host bare metal vừa ghi metric hạ tầng hiện thu từ Kubernetes, nên mức hỗ trợ Docker/VM chưa rõ [GỐC].
  - Synthetics có private probe.
- **Collector, Tempo, OTel Demo.**
  - servicegraph connector ở mức alpha; `store.ttl` mặc định 2 s [GỐC].
  - Tempo 3.1.1. OTel Demo 3.1.0; tránh 3.0.0.
  - Chưa tìm thấy dataset RCA có ground truth thu từ OTel Demo chạy Docker compose.
- **Thêm.**
  - H1 trên service khung không kiểm được span DB và AMQP.
  - Gửi dữ liệu song song lên Grafana Cloud ngay từ H2.
  - Không dùng laptop cho lượt cần mốc thời gian chính xác.

**Đề xuất:** KS-01 đến KS-06.

### K6. Khía cạnh kế hoạch chưa xét

Phần này là [SUY LUẬN], trừ chỗ có ghi nguồn.

**Phương pháp:**
1. Chất lượng cạnh có thể đáng đầu tư hơn thuật toán lan (Groot: 3% so với 78%).
2. "Mất tín hiệu" là điểm mù lớn nhất của benchmark mới, nhưng chưa có kịch bản cho nó.
3. Lỗi mạng làm đảo thứ tự bất thường, và chưa có nhánh riêng cho loại lỗi này.

**Dữ liệu và đánh giá:**

4. Một hệ của bên thứ ba có telemetry giàu sẽ tách được "lợi thế thông tin" khỏi "thiên lệch tự thiết kế". Ví dụ: bảng phụ OTel Demo. Việc này liên quan C-07; Minh quyết.
5. RE2-OB có mã trạng thái span và được nhiều bài 2025–2026 dùng [ĐÃ KIỂM]. Thêm nó là quyết định cấp G1. G1 đã loại RE2-OB vì mức tiếp xúc TX2: repo đã chạy phương pháp trên gần như toàn bộ 90 ca (`results/T-021/goi-g1.md:116`; `results/T-015/ca-da-chay.csv`). Vì vậy bộ này chỉ làm dev hoặc tái lập, không làm kiểm độc lập.
6. Kịch bản FlashTicket nên sắp theo trục phân xử: độ sâu root, loại cạnh, loại lỗi, điểm mù.
7. Khai trước một họ giả thuyết chính, để giới hạn số phép so sánh.
8. Báo thời gian chạy từng mô-đun.

**Hạ tầng:**

9. Lọc tín hiệu của công cụ tiêm lỗi khỏi đầu vào RCA (luật cứng 6): `chaos_monkey_*`, container Pumba, Toxiproxy, flagd, `feature_flag.*`.
10. Ghim phiên bản Docker Engine, agent và chế độ semconv.

**Demo:**

11. Grafana Cloud chỉ lưu 14 ngày. Nếu demo đọc trực tiếp dữ liệu còn trên Cloud thì phải thu dữ liệu trong 14 ngày trước buổi bảo vệ. Chỉ 3 người xem hoạt động mỗi tháng.
12. Flame graph đường găng là cách trình bày giải thích rẻ, hợp DT18.

**Bảo vệ:**

13. Câu "SimpleRCA đã 83% thì cần đồ thị làm gì": trả lời bằng tỷ lệ Type III và số trên benchmark có call depth lớn (FSE 2026).
14. Câu "LLM có bịa không": dùng các độ đo "đúng nhưng không có căn cứ" và Evidence Closure Rate.

---

## 3. Đề xuất sửa file (mẫu Luật 0 mục 3)

**Trạng thái ngày 23/10/2026:** KS-07 đã duyệt cùng E-04 (M-44 trong KE-HOACH). KS-10, KS-11, KS-14, KS-16 được đưa vào SPEC M1 làm ứng viên để thử, mỗi ứng viên có ba kết cục: giúp thì giữ, hại thì bỏ, không đủ ca để phân xử thì giữ lại và kiểm trên FlashTicket (M-48 trong KE-HOACH); D.2, D.5, D.7 của KE-HOACH chưa sửa. Các mã khác chưa duyệt.

| Mã | File, mục | Sửa gì | Vì sao | Ảnh hưởng |
|---|---|---|---|---|
| KS-01 | KE-HOACH Phần B dòng Chaos Monkey; D.9(b); D.8.7 | "Không tìm thấy xác nhận hỗ trợ Spring Boot 4" → "Có v4.0.0 (06/02/2026), build với Boot 4.0.2; với 4.1.1 chưa kiểm". Lý do dùng cờ lỗi trong code đổi thành: Chaos Monkey tiêm được latency và exception tới mức method, nhưng không thấy tiêm giá trị trả về sai; lỗi Saga và Boot 4.1.1 chưa kiểm | Dữ kiện cũ đã sai | D.9(b) giữ, đổi lý do; Chaos Monkey là phương án tiêm latency/exception |
| KS-02 | Phần B dòng Java agent; D.8.3 (H0, H1) | Thêm #14906, #20199, 2.32.0 là bản ứng viên của 3.0, đổi tên `db.*`/`messaging.*`, khóa MDC. H0: ghim agent và chế độ semconv. H1: ứng dụng thử có JPA, Mongo, AMQP, Lettuce (nơi đặt chờ duyệt); kiểm 6 điểm | Tên thuộc tính đổi làm lệch dữ liệu giữa các đợt | H0, H1, H4, B16 |
| KS-03 | Phần B; D.9 | Thêm dữ kiện PostgreSQL, MongoDB, SMTP. Mỗi cặp service→DB một proxy. Thêm mock SMTP, kịch bản cạnh mù SMTP, kịch bản mất tín hiệu | Dùng chung proxy thì đáp án sai | Danh mục kịch bản |
| KS-04 | D.8.2; D.8.3 | Synthetics dùng private probe. Ghi rõ xử lý khi vượt hạn mức; 3 người xem; điều kiện Knowledge Graph (nhãn môi trường bắt buộc; `service.namespace` không bắt buộc; mức hỗ trợ ngoài Kubernetes chưa rõ, như mục K5); IRM chỉ có trên Cloud; inhibition là API beta. H7 chạy cùng H2 | Dữ kiện mới | Thứ tự các bước H |
| KS-05 | D.8.1 | servicegraph ở mức alpha, đổi tên `service_graph`; tăng `store.ttl`; cạnh thông điệp lấy từ span link; không dùng `db.statement` làm dimension; gắn định danh host bằng một trong `host.id`, `grafana.host.id` (hoặc `k8s.node.name` nếu có Kubernetes), khớp `hostId` của B16 | Mất cạnh thông điệp; vượt 10.000 chuỗi | Bộ dựng P5; E8 |
| KS-06 | D.10 | Ghim OTel Demo 3.1.0; đếm lại số cờ; ghi rõ chưa tìm thấy dataset RCA có ground truth chạy Compose | Dữ kiện đã đổi | H2, H3 |
| KS-07 | D.1 (E-04); C-08 | Kết luận theo CI, báo đồng thời hai câu: (1) không thua quá Δ (cận dưới > −Δ, là điều kiện E-04); (2) khác 0 (hơn, kém, chưa phân biệt). Quy tắc điểm ước lượng chỉ là "tiêu chí thực dụng khai trước"; baseline đối chứng TORAI B; Hit@1 chỉ để mô tả; thêm mục "khi không đạt biên". **Đã duyệt (M-44), làm rõ cách đọc (M-45)** | Quy tắc cũ không phải NI; power khoảng 0,11–0,19 với n = 30–60 (giả định ở Phụ lục C) | Cách viết kết luận P7 |
| KS-08 | D.6; A4; C-15 | Phép kiểm chính: sign-flip chính xác theo ô. Phép nhạy: theo ca. McNemar là phép phụ. Bỏ Wilcoxon. Bootstrap theo ô kèm cảnh báo ít cụm. Wilson chỉ dùng cho tỷ lệ nhị phân của các đơn vị độc lập; độ đo có hòa, chênh MRR và dữ liệu theo ô tính theo giao thức A4. Sign-flip theo ô chỉ chính xác khi dấu chênh của từng ô hoán đổi được dưới H0. Thêm Retrieval@K/Rerank@1, Chance; phân tầng theo Type và độ sâu; hai cách xử lý ca lỗi. Phát hiện: thêm reset time và precision theo sự cố; cấm point-adjust. Ghi sổ số lần xem test | p 0,020 so với 0,188 [ĐÃ KIỂM] | Giao thức đánh giá; WHY-06 |
| KS-09 | D.9 | Thêm luật (6)–(14): tách vai; phân tích mù; khóa giao thức bằng hash; lọc theo tác động; công bằng thông tin; ngân sách chỉnh như nhau; kịch bản từ postmortem; đối chứng dương và âm; lọc tín hiệu của công cụ tiêm | FDA; FSE 2026; luật cứng 6 | Chiến dịch lớn hơn |
| KS-10 | D.2 | E1, E5, E9, E3b, ghi chú 6, E8, E6b như mục K1 | K1 | SPEC M1 |
| KS-11 | D.5 | Thêm C-g, C-h; viết C-d bằng Traversal; viết C-a kèm danh sách quan hệ còn giữ ở từng bước (xem mục K1) | Tách được lợi ích của bước đồ thị | Thêm 1–2 cấu hình |
| KS-12 | D.3; C-05 | Đổi điều kiện ghim model; bỏ nhiệt độ 0; sửa L1, L2, L5, L6; Assistant chỉ so định tính; lưu prompt và phản hồi | API trả lỗi 400 [ĐÃ KIỂM] | P8, L5 |
| KS-13 | D.4, D.4.1; C-01 | H0/H1 thành task nhỏ; thêm phép quét kiểu CNSS; G hoãn; dùng lập luận GAD. **Thứ tự phụ thuộc** (không làm ngay): H0 cần bộ luật cảnh báo và đồ thị P5, không cần RCA; H1 cần Mô-đun B chạy được; đo gộp nhầm cần hạ tầng H3 và kịch bản hai lỗi. M-20 vẫn giữ. Chi tiết ở Phụ lục D.2 | Tiền lệ H dày | **Mâu thuẫn M-20** |
| KS-14 | D.7 | Thêm TraceDiag, PetShop, "Where RCA Fails", DiagMLP, TraceContrast, MicroDig, PRISM, OpenRCA 2.0, OTel messaging semconv, CNSS, GRLIA, DiLink, Urbano 2019, FDA NI. Đọc FSE 2026 trước; hạ Eadro, Murphy, Sage | K1–K4 | A2 |
| KS-15 | Phần F (thêm A11) | Task đối chiếu Nezha-OB với số công bố, trước SPEC M1. Chi tiết ở Phụ lục A.1 | 0,318 so với 0,91 [ĐÃ KIỂM] | Mục tiêu Nezha-OB; hạn chế P4 |
| KS-16 | Phần F (thêm A12) | Đếm trên dev, chỉ đọc: một quy tắc mô tả kiểu Type do repo đặt mới, ghi rõ khác "Type theo tác giả" vì luật của tác giả không tái tạo được; độ sâu gọi, tỷ lệ con song song lệch pha, số ca dịch vụ gọi đứng trên root, hình dạng xếp hạng | Biết trước tiêu chí có phân xử được không | Tiêu chí lượt 1 và 5 |
| KS-17 | Phần E (thêm E-15) | **Hoãn.** Quyết sau KS-15 và KS-16. Bảng phương án (giữ nguyên, RE2-OB, benchmark FSE 2026, bảng phụ OTel Demo) ở Phụ lục D | Bản đầu chỉ liệt kê lựa chọn, không phân tích, và bỏ sót G1 (T-021) và T-012 | Cấp G1; tải phải trình dung lượng trước |

---

## 4. Những điều chưa kiểm được

- **SimpleRCA bản FSE:** công cụ không đọc được PDF. Số lấy từ arXiv v2, khớp `so-cong-bo.csv`.
- **Benchmark FSE 2026:** bản công khai là artifact rút gọn (Zenodo 19522409, 91 MB): 10 ca, 8 ca dùng được, mỗi ô một lần; phạm vi license của dữ liệu thô còn OPEN (`results/T-012/the-dataset.md`, mục FSE). Bộ đầy đủ 1.430 ca chưa thấy công khai.
- **Chỉ đọc được abstract:** LagRCA, MicroDig, ShapleyIQ, Murphy, Sleuth, COLA, ProAlert, AirAlert.
- **Số RCAEval Bảng 6** dùng ở Phụ lục A.2: Codex đã đối chiếu nguồn gốc (BARO hàng metric 0,67, multi-source 0,69; CIRCA metric 0,32, multi-source 0,06). Claude chưa mở lại.
- **Nezha có ghi mã trạng thái span không:** chưa rõ.
- **Cần đăng nhập mới kiểm được:** Knowledge Graph trên Docker; PDC, FIS và private probe có trong gói Free không; quota và tín dụng của các tài khoản.
- **Luật cấm chạy thử:** Chaos Monkey với Boot 4.1.x; ChaosBlade với Java 21; Pumba với Docker 29; model 3–8B trên laptop.
- **Số của K4:** power, xác suất 14%, nửa độ rộng CI và cỡ mẫu đã tính lại theo công thức ở Phụ lục C; Codex tính lại khớp. Chưa tái lập: số 32% cho Hit@1; kết luận "Bayesian signed-rank cho kết luận sai hướng".
- **Bài trên Research Square (rs-11401166)**, nguồn của câu "mồi nhử được xếp đầu ở 21–42% ca": chỉ đọc được tiêu đề.
- **Chính sách ngừng model** (Sonnet 4.5 ngừng 30/11/2026, theo K2): chưa kiểm.

## 5. Subagent và thời gian

- 6/6 subagent. Bắt đầu 06:31, đủ kết quả khoảng 06:58 ngày 23/10/2026.
- Thời gian từng subagent: 13,0 / 13,6 / 15,0 / 17,0 / 18,0 / 20,7 phút.
- Khoảng 1,29 triệu token, 486 lượt gọi công cụ.
- Không dùng máy thực nghiệm, không tải dữ liệu.

## 6. Tác dụng phụ ngoài repo (Luật 0 mục 8)

- WebFetch tự lưu khoảng 23 MB cache (14 PDF và vài file văn bản) vào `C:\Users\84583\.claude\projects\D--RCA-flashticket\3c64cd3a-6a39-41a6-a9d0-c33fb927b66c\tool-results\`.
- Đây là thư mục dữ liệu phiên của Claude Code, không do agent chủ ý ghi.
- Cách hoàn tác: xóa thư mục đó. Minh quyết.

---

## Phụ lục A. Trả lời câu hỏi của Minh, lượt 2 (23/10/2026)

### A.1 Task đối chiếu Nezha-OB trước SPEC M1 (KS-15) cụ thể làm gì?

**Mục đích.** Tìm vì sao baseline của repo trên Nezha-OB thấp hơn nhiều số công bố, trước khi thiết kế P6 dựa trên bộ này.

**Một dữ kiện mới [TÍNH].** Riêng việc khác tập ca không đủ giải thích chênh lệch của SimpleRCA, với điều kiện: 22 ca dev là tập con của 56 ca bài dùng, và hai bên cùng cách chấm Top@1.
- Dev có 22 ca, SimpleRCA đúng khoảng 7 ca (0,318 × 22).
- Nếu đúng cả 34 ca còn lại, tổng cũng chỉ là 41/56 = 0,732. Vẫn thấp hơn 0,91.
- Vậy loại được giải thích "chỉ do khác tập ca". Nguyên nhân còn lại (bản cài, đầu vào, giao thức, phiên bản dữ liệu) chưa xác định; chưa kết luận lỗi thuộc adapter.
- Với MicroRank thì khác: T-026 đã chỉ ra khác tập ca vẫn có thể giải thích về mặt số học. Phản ví dụ này nằm trong `results/T-026/cham-a.md`; file lệch hash với manifest nên chỉ dùng làm chỉ dẫn. Số công bố ở `results/T-026/runs/session-005/published-reference.json` (hash khớp).

**Bước 1. Chỉ đọc, không chạy.** Lập bảng khác biệt giữa bài và repo theo năm điểm:
1. **Dữ liệu:** bài dùng bản Nezha nào, tiền xử lý nào. Repo dùng bản trong thẻ `results/T-008/the-dataset.md`.
2. **Đơn vị và tập ứng viên:** bài chấm ở mức service hay pod. Repo dùng alias, U = 10, 16 kênh pod + 5 kênh front, loại kênh Node* (Q-85).
3. **Đầu vào của SimpleRCA:** bài dùng luật cảnh báo trên metric, log, trace. Repo dùng bản M4 cài theo mô tả của bài, có chỗ bài để ngỏ (T-017, WHY-17). So với mã tác giả mà T-017 đã lưu.
4. **Cửa sổ và mốc:** cửa sổ của bài so với giao thức V2 của repo. Nền ở Nezha ngắn.
5. **Quy tắc chấm:** hòa và ca lỗi. Bài có Top@1 = Top@3 = Top@5 = 0,91, gợi ý mỗi ca hoặc trúng ngay hoặc không có ứng viên nào bị cảnh báo [SUY LUẬN].

Đầu ra: bảng khác biệt, các giả thuyết nguyên nhân và dự đoán kiểm được cho từng giả thuyết.

**Bước 2. Chỉ làm khi Minh duyệt SPEC; chỉ trên 22 ca dev, không mở 34 ca test.**
- Chạy mã tác giả SimpleRCA đúng tiền xử lý của bài.
- Sau đó đổi từng yếu tố một (kênh, cửa sổ, đơn vị ứng viên) để thấy yếu tố nào làm điểm tụt.
- Có thể làm tương tự cho MicroRank.
- Chi phí: bài báo ghi SimpleRCA khoảng 5 s mỗi ca, nên 22 ca chỉ vài phút trên laptop.

**Kết quả dẫn tới quyết định:**
- **(a) Lỗi do adapter của repo:** sửa adapter. Chạy lại mọi baseline Nezha-OB theo quy tắc sửa lỗi cài đặt. Xem lại các hạn chế P4 rút từ Nezha-OB, ví dụ G2-H07 (lỗi return).
- **(b) Do giao thức repo chọn có chủ đích:** giữ nguyên, ghi rõ khác bài. Viết lại mục tiêu "cải thiện Nezha-OB".
- **(c) Do dữ liệu hoặc phiên bản:** ghi giới hạn.

Theo AGENTS mục 5, task này cần SPEC được duyệt, có người làm và người phản biện.

### A.2 Baseline trên RE2-TT có lệch so với bài gốc không?

**Trả lời ngắn:** không thấy lệch lớn. Nhưng đây chưa phải tái lập: repo chỉ có 30 ca dev, bài dùng đủ 90 ca, và cấu hình khác nhau.

| Phương pháp | Repo dev30, Hit@1 = AC@1 [khoảng bootstrap] | Số công bố trên RE2-TT, 90 ca | Nhận xét |
|---|---|---|---|
| BARO | 0,700 [0,47; 0,90] | RCAEval Bảng 6: 0,67 (hàng metric; bản repo chỉ dùng metric theo `results/T-013/ho-so-baro.md`) và 0,69 (hàng multi-source); SimpleRCA Bảng 2: 0,67 | Khớp trong khoảng |
| SimpleRCA | 0,833 [0,67; 1,00] | 0,80 (SimpleRCA Bảng 2; `so-cong-bo.csv`) | Khớp trong khoảng |
| TraceRCA | 0,700 [0,50; 0,87]; thứ tự gốc của hàm cho 0,533 | 0,66 (RCAEval Bảng 6) | Khớp; nhạy với thứ tự (WHY-32) |
| MicroRank | 0,067 [0,00; 0,20], 4 ca ERROR | 0,16 (RCAEval Bảng 6) | Thấp hơn nhưng nằm trong khoảng; repo dùng bản đã sửa đầu vào |
| CIRCA | 0,533, dùng đồ thị kiến trúc | RCAEval Bảng 6: 0,32 (metric), 0,06 (multi-source) | Không so được: RCAEval dùng PC, repo dùng đồ thị kiến trúc (Q-62) |
| TORAI B | 0,867 | Không có số cho bản B. Bản gốc khớp số công bố trên torai-OB/SS (`results/T-006/kiem-dung-dan.md` §7) | Chưa có mốc trên TT |

- **Nguồn số repo:** `results/T-034/goi-g2.md` §2.1 và §2.7 [ĐÃ KIỂM]. Số RCAEval Bảng 6: Codex đã đối chiếu nguồn gốc (BARO hàng metric 0,67, multi-source 0,69; CIRCA metric 0,32, multi-source 0,06). Claude chưa mở lại.
- **Kiểm số học [TÍNH].** Với BARO, SimpleRCA, TraceRCA, MicroRank, số đúng cần có ở 60 ca còn lại để khớp số công bố đều hợp lý: lần lượt khoảng 0,66 (theo hàng metric 0,67 của BARO); 0,78; 0,64; 0,21. Điều này trái ngược với Nezha-OB ở A.1.
- **Theo loại lỗi, BARO lệch so với README RCAEval (Avg@5):** cpu +0,147; socket +0,17; loss −0,073 (`results/T-024/cham-a.json#/methods/baro/summaries/dev30/grouped/fault`, hash khớp; số README ở `docs/knowledge/K4-ho-thuat-toan.md:112`). Tập ca và phân bố loại lỗi khác nhau, nên chỉ là tham khảo.

### A.3 Đã có phương án xử lý độ lệch trên Nezha-OB chưa?

**Chưa.** Tình trạng trong repo [ĐÃ KIỂM]:
- **MicroRank:** T-026 ghi lệch so với Bảng 3 của bài Nezha (41,07%; `results/T-026/runs/session-005/published-reference.json`, hash khớp) và nêu bốn khả năng: nền ngắn, tải đổi, cấu trúc/coverage, khác tập ca. Kết luận "chưa có nguyên nhân xác nhận" (`results/T-026/cham-a.md`; file lệch hash với manifest, chỉ dùng làm chỉ dẫn). Không có task xử lý tiếp.
- **SimpleRCA:** `published-reference.json` ghi Bảng 3 của bài Nezha không có BARO, SimpleRCA, TraceRCA (`#/other_T026_methods_in_table`). Tức là lúc đó T-026 chưa so với số 0,91 của bài FSE 2026, dù T-017 đã ghi số này. `goi-g2.md` §2.7 chỉ ghi SimpleRCA "chưa tái lập số công bố", lấy lý do test RE2-TT đang khóa; không nhắc Nezha-OB.
- **Danh sách OPEN** của Q-149 (duyệt G2) không có mục này.
- **T-041:** không thấy nhắc trong `results/T-041/*.md` khi tìm theo từ khóa.

KS-15 là đề xuất đầu tiên để xử lý.

### A.4 Nhánh G và nhánh H là gì?

Chuỗi giám sát trả lời hai câu:
1. **Khi nào có sự cố?** Tức là quyết định báo động.
2. **Cái gì gây ra?** Tức là chẩn đoán và xếp hạng nguyên nhân.

**Kế hoạch hiện tại.** Luật cảnh báo Grafana trả lời câu 1. Ví dụ: "tỷ lệ lỗi 5xx của booking trên 5% trong 2 phút thì báo". Đồ thị chỉ dùng cho câu 2 (Mô-đun A, B, C, D).

**Nhánh G: đồ thị tham gia trả lời câu 1.**
- **Cách làm:** mỗi chu kỳ, Mô-đun A, B tính điểm bất thường cho từng service, có trừ phần kế thừa từ phía dưới. Các điểm này được gộp thành một điểm cho cả hệ. Vượt ngưỡng (học từ đoạn bình thường) thì báo động. G thay hoặc bổ sung luật Grafana.
- **Ví dụ:** DB của booking chậm làm booking, payment, gateway cùng chậm. G thấy một nguồn tự sinh ở cạnh booking→DB và báo một lần.
- **Phải đo:** báo giả mỗi giờ, độ trễ, số lần bỏ sót; so với luật Grafana.
- **Tiền lệ:** có trong nghiên cứu (ART, AnomRank, CNSS). Trong công nghiệp có bộ phát hiện dựa trên cấu trúc trace theo endpoint (CRISP, Uber); chưa thấy công cụ dùng điểm toàn hệ tổng hợp trên đồ thị phụ thuộc như G.
- **Rủi ro:** điểm thành phần vốn đã nhiễu (BOCPD, N-Sigma báo trước mốc), nên dễ báo giả.

**Nhánh H: luật Grafana vẫn mở sự cố, đồ thị dùng để gom cảnh báo.**
- **Cách làm:** khi nhiều luật cùng kêu (booking chậm, payment chậm, gateway 5xx, DB chậm), đồ thị gom chúng thành một sự cố. Nó chỉ ra cảnh báo nào là gốc (DB) và cảnh báo nào là hệ quả, rồi nén thông báo hệ quả.
- **H0:** sinh sẵn luật nén từ đồ thị P5. Ví dụ: "khi cảnh báo của DB đang kêu thì không gửi cảnh báo cùng loại của booking".
- **H1:** khi có sự cố, dùng nhãn tự sinh/kế thừa của Mô-đun B để gom.
- **Tiền lệ:** Dynatrace, Alertmanager inhibition, GitLab, GRLIA, DiLink.
- **Phải đo:** tỷ lệ nén; số sự cố bị nén mất (phải bằng 0); số lần gộp nhầm hai sự cố.

**Quan hệ với RCA.** Cả hai nhánh dùng lại Mô-đun A, B. H rẻ hơn G. M-20 hoãn cả hai; KS-13 đề xuất nâng H.

### A.5 Quyết định E-04 ngày 23/10/2026

- **Lời Minh:** "duyệt E-04". Khi được hỏi duyệt bản nào, Minh chọn "E-04 sửa theo KS-07".
- **Nội dung đã duyệt:**
  - Giữ Δ_MRR = 0,05 và Δ_Hit@1 = 2/30 (4/60).
  - Khai trước baseline đối chứng là TORAI B.
  - Kết luận theo vị trí CI: trọn trên −Δ là không thua; chứa cả −Δ và 0 là chưa phân xử; cận trên dưới 0 là kém. (Cách đọc ban đầu; đã làm rõ ở M-45, xem dưới.)
  - Quy tắc điểm ước lượng chỉ là tiêu chí thực dụng, báo kèm.
  - Hit@1 chỉ để mô tả.
- **Nơi ghi:** M-44 và D.1 của KE-HOACH.
- **Làm rõ ngày 23/10/2026 (M-45), sau phản biện Codex:** báo đồng thời hai câu, và hai câu có thể cùng đúng.
  - (1) Không thua quá Δ: cận dưới của CI lớn hơn −Δ là đạt E-04; ngược lại là chưa chứng minh được.
  - (2) Khác 0: CI trọn trên 0 là hơn; trọn dưới 0 là kém; chứa 0 là chưa phân biệt.
  - Xem D.1 của KE-HOACH.

---

## Phụ lục B. Prompt cho Codex phản biện file này

- **Gồm:** Prompt chung, khối "Soát kết quả" và khối G3 của `docs/review-prompt.md`, chép nguyên văn.
- **Khối thêm:** "Khối yêu cầu của Minh" theo lời Minh ngày 23/10/2026. Khối này là ngoại lệ đối với AGENTS §9 và Q-44, chỉ dùng cho lượt này. Tiền lệ là M-29; C-10 vẫn không duyệt.
- **Quyền ghi của Codex:** chỉ trả lời trong chat. Minh muốn lưu bản phản biện thì sửa dòng "Phạm vi ghi" trước khi dán.

```text
Bạn thực hiện một lượt đánh giá độc lập trong repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Giữ đúng vai trò và phạm vi đã được Minh duyệt.

Thông tin lượt này:
- Task hoặc đề xuất: docs/KHAO-SAT-SAU-K1-K6.md (báo cáo khảo sát sâu K1–K6 theo việc A10 và Phụ lục P3 của docs/KE-HOACH-GIAI-DOAN-TOI.md, Claude soạn ngày 23/10/2026 bằng 6 subagent; gồm đề xuất KS-01…KS-17 và Phụ lục A trả lời câu hỏi của Minh). Kèm phần sửa docs/KE-HOACH-GIAI-DOAN-TOI.md ngày 23/10/2026 ghi quyết định E-04 (xem Phần Z và git diff). Ngoài task, chưa có mã T.
- Công đoạn: soát kết quả.
- Gói/cổng: P6–P10, trước SPEC M1; G2 đã duyệt (Q-149), G3 chưa mở. Loại đề xuất: báo cáo khảo sát tài liệu, đề xuất sửa kế hoạch và ghi quyết định.
- Người làm và người phản biện chính thức: ngoài task; vai trò dự kiến: Claude soạn khảo sát, Codex phản biện.
- Tài liệu gốc: docs/KHAO-SAT-SAU-K1-K6.md; docs/KE-HOACH-GIAI-DOAN-TOI.md (Phần A là lời Minh; Phụ lục P3 là đề bài khảo sát); các nguồn web và file repo được dẫn trong docs/KHAO-SAT-SAU-K1-K6.md; docs/MRP.md; docs/WHY.md; docs/DECISIONS.md; docs/LESSONS.md; docs/knowledge/K1-phuong-phap-rca.md; docs/knowledge/K4-ho-thuat-toan.md; results/T-034/goi-g2.md; results/T-034/bang-baseline.json; results/T-017/; results/T-024/cham-a.json, cham-a.md; results/T-026/cham-a.md; results/T-002/the-rcaeval.md; D:/Project/flash-ticket-platform (chỉ đọc: services/*/pom.xml, docs/architecture/aws-runtime-baseline.md, B16-observability-baseline.md). docs/DECISIONS.md, docs/STATE.md và docs/KE-HOACH-GIAI-DOAN-TOI.md có thay đổi chưa commit (git status, git diff).
- Phản biện và phản hồi trước: chưa có phản biện cho docs/KHAO-SAT-SAU-K1-K6.md. Prompt phản biện kế hoạch ở Phụ lục P2 của docs/KE-HOACH-GIAI-DOAN-TOI.md; phản biện của Codex ngày 22/10/2026 nằm trong chat, không có file.
- Code và kết quả liên quan: không có code mới. Manifest results/T-034/runs/manifest-cuoi-007/manifest.json; danh sách file cuối T-024 tại results/T-024/work/danh-sach-tep-cuoi.json. Được đọc bài, tài liệu và mã chính thức trên web nếu môi trường cho phép; được chạy lệnh chỉ đọc và phép tính nhỏ không ghi file.
- Phạm vi ghi được Minh cho phép trong lượt này: chỉ trả lời trong chat.

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

Khối yêu cầu của Minh cho lượt này (lời Minh ngày 23/10/2026: "soạn prompt cho codex yêu cầu phản biện, rà soát sâu . yêu cầu codex phải kiểm chứng các tài liệu mà bạn đã tuyên bố"). Khối này là ngoại lệ Minh yêu cầu cho lượt này đối với AGENTS §9 và Q-44:
1. Phản biện và rà soát sâu toàn bộ docs/KHAO-SAT-SAU-K1-K6.md và phần sửa E-04 trong docs/KE-HOACH-GIAI-DOAN-TOI.md.
2. Kiểm chứng các nguồn mà tài liệu đã dẫn: mở từng nguồn (URL, file repo, dòng, bảng, mục) được dùng làm căn cứ, đối chiếu khẳng định và số liệu với nguồn. Với mỗi khẳng định đã kiểm, ghi: khớp / lệch / không tìm thấy / không truy cập được, kèm mức bạn đã đọc (nguồn gốc hay chỉ tóm tắt). Kiểm cả nhãn nguồn và mức tin cậy mà tài liệu tự gán.
3. Các số có nhãn [TÍNH] hoặc [ĐÃ KIỂM]: tính lại khi rẻ và trong quyền được phép, ghi lệnh và kết quả.
4. Nguồn nào không truy cập được (ví dụ không có mạng) thì ghi rõ là chưa kiểm, không suy đoán nội dung.
```

---

## Phụ lục C. Đính chính sau phản biện Codex (23/10/2026)

- **Căn cứ:** bản phản biện Codex (R1–R8), bản kiểm lại của Codex, và hai lượt đáp của Claude (N1–N4), đều ngày 23/10/2026, trong chat.
- **Lời duyệt của Minh:** "Duyệt P-A (đoạn mới cho D.1 E-04, thêm M-45 ở Phần A và một dòng Phần Z của KE-HOACH) và P-B (sửa đúng các vị trí đã liệt kê trong docs/KHAO-SAT-SAU-K1-K6.md, thêm Phụ lục C và dòng lịch sử). Giữ hai câu N3. Không sửa file khác, không commit."
- **Phụ lục B** giữ nguyên làm lịch sử, vì đó là prompt đã dùng.

### C.1 Câu cũ → câu mới

| # | Vị trí | Câu cũ (tóm tắt) | Câu mới (tóm tắt) | Căn cứ |
|---|---|---|---|---|
| 1 | §1 mục 1 | "Trên bộ này đồ thị gần như không có chỗ để giúp" | Bỏ. Tỷ lệ Type theo luật của tác giả, không tái tạo được; thêm G2-H06 (5/6 ca trễ mạng có dấu hiệu ở span phía gọi) | R3 |
| 2 | §1 mục 2 | "Tỷ lệ Type III…"; "độ sâu lan 2–4" | "theo luật của tác giả"; "RE2-TT max call depth 5, phủ 39%; Nezha-OB max call depth 2" | R3; bảng nguồn Codex |
| 3 | §1 mục 3 | "Power … chỉ khoảng 0,1–0,3 [TÍNH, K4]"; "duyệt E-04 … (M-44)" | "khoảng 0,11 (n = 30) và 0,19 (n = 60), giả định ở C.2"; thêm M-45 | N1; R1 |
| 4 | §1 mục 4 | "Chưa bài nào có đủ đối chứng" | Nêu cụ thể phần thiếu: ẩn tên, phương sai; đối chứng luật chỉ ở GALA+ trên OB | R7 |
| 5 | §1 mục 5; K3; A.4 | "G gần như không có tiền lệ công nghiệp"; "PageRank anomaly của cô, ở dạng gốc AnomRank" | "Có bộ phát hiện theo cấu trúc trace/endpoint (CRISP, Uber); chưa thấy điểm toàn hệ như G"; "một cách hiểu … chưa có căn cứ đó là ý cô" | R4; bảng nguồn |
| 6 | Bảng K1, CRISP | "độ trễ bất đồng bộ không lên đường găng" | Chỉ phần vượt khoảng cha bị cắt; lời gọi được chờ xong có thể nằm trên đường găng; thêm phần phát hiện của CRISP | R4 |
| 7 | Bảng K1, PetShop; đề xuất E5 | "Traversal bằng hoặc hơn"; "Traversal thắng" | Top-1: bằng hoặc hơn ở 6/6 ô; top-3: thua 2/3 ô latency; ứng viên, chưa chọn | R5 |
| 8 | Bảng K1, PRISM | "Tiên đề chỉ đúng 66,5%" | "Điều kiện thứ tự điểm quan sát đúng ở 66,5% ca" | Bảng nguồn |
| 9 | Bảng K1, Groot | "bỏ luật cạnh động: 33%" | "bỏ cả luật động và luật có điều kiện: 33%" | Bảng nguồn |
| 10 | Đề xuất E3b | Dẫn `results/T-002/the-rcaeval.md:111, 117` | Dẫn `summary.json#/re2tt` (hash khớp) | Luật cứng 4 |
| 11 | Đề xuất D.5; KS-11 | "C-a theo kiểu DiagMLP: bỏ đồ thị, giữ tiền xử lý" | Ghi quan hệ còn giữ ở từng bước; C-a0/C-a1 chỉ là ví dụ | R6 |
| 12 | K2, trích phụ thuộc | 0,87 so với 0,604 | Ghi rõ F1 cạnh so với F1 tổng kiến trúc | Bảng nguồn |
| 13 | K2, agent | "đúng service ở 76–90% ca" | Tách AnySvc 76,0% (OpenRCA 2.0) và Acc@1 90,0% (bài khác) | R7 |
| 14 | K2, LLM xếp lại | Chỉ có số GALA+ chính | Thêm ablation theo dataset; trung bình 3 lượt; không ẩn tên | R7; kiểm lại Codex |
| 15 | K2, mồi nhử | "mồi nhử … 21–42% [THỨ CẤP]" | Chưa kiểm, không dùng làm căn cứ | R7 |
| 16 | K2, chấm lời giải thích | "κ 0,92 … 20–30 mẫu" | Tách ρ 0,92 (GALA, 20 mẫu) và κ 0,92 (taxonomy, 30 trace) | R7 |
| 17 | K2, giá | "Haiku 5.5 là 0,10/0,50 USD" | Thêm điều kiện prompt ≤ 100k token | Bảng nguồn |
| 18 | K2, Grafana Assistant | "không cam kết tái lập" | "chưa tìm thấy cam kết tái lập" | Bảng nguồn |
| 19 | K4 | Đặc tính 14%, 32% | 14% kèm giả định; 32% chưa tái lập | N1 |
| 20 | K4 | "Bayesian signed-rank cho kết luận sai hướng" | Bỏ khỏi phát hiện; chuyển sang §4 | Codex lượt 1 |
| 21 | K4 | "113–145 sự cố" | Ghi rõ là tỷ lệ của một phương pháp; ICC là giả định độ nhạy | N1; kiểm lại Codex |
| 22 | K5, Chaos Monkey | Chỉ có bản và Boot | Thêm chọn tới method, latency/exception, không có giá trị trả về | R8 |
| 23 | K5, FIS | "không tạo được lỗi trên cạnh giữa hai container" | Hạn chế thuộc document dựng sẵn; document tùy biến chưa thử | R8 |
| 24 | K5, Knowledge Graph | "cần nhãn môi trường, `service.namespace` và `grafana.host.id`" | Nhãn môi trường bắt buộc; `service.namespace` không bắt buộc; một trong ba định danh host; mức hỗ trợ ngoài K8s chưa rõ | R8; kiểm lại Codex |
| 25 | K5; KS-06 | "Không có dataset OTel Demo … Compose" | "Chưa tìm thấy dataset RCA có ground truth …" | Bảng nguồn |
| 26 | K6 mục 11 | "phải thu dữ liệu demo trong 14 ngày" | Thêm điều kiện: demo đọc dữ liệu còn trên Cloud | Kiểm lại Codex |
| 27 | KS-01 | "không làm được lỗi trả giá trị sai, lỗi theo thao tác, lỗi Saga" | Làm được latency/exception tới method; không thấy giá trị trả về; Saga, Boot 4.1.1 chưa kiểm | R8 |
| 28 | KS-04, KS-05 | "điều kiện Knowledge Graph"; "gắn host id" | Đồng bộ với dòng 24 | Kiểm lại Codex |
| 29 | KS-07; A.5 | Ba mục CI loại trừ nhau | Hai câu báo đồng thời (M-45) | R1 |
| 30 | KS-08 | "CI dùng Wilson" | Wilson chỉ cho tỷ lệ nhị phân độc lập; điều kiện chính xác của sign-flip | R2 |
| 31 | KS-16 | "Type" | Quy tắc mô tả mới, tách khỏi "Type theo tác giả" | R3 |
| 32 | §4 | "Claude chỉ tính lại hai giá trị p" | Liệt kê số đã tính lại và chưa tái lập; thêm mồi nhử, McNemar của GALA+ | Tổng hợp |
| 33 | A.1 | "Vậy phải có khác biệt ở bản cài…"; dẫn `cham-a.md:596` | Ghi điều kiện của 41/56; chỉ loại "chỉ do khác tập ca"; dẫn JSON khớp hash | R3; luật cứng 4 |
| 34 | A.2 | BARO "0,69"; CIRCA "0,06"; kiểm số học "0,68; …" | BARO 0,67 (metric, khớp bản repo) và 0,69 (multi-source); CIRCA 0,32 và 0,06; kiểm số học "0,66; 0,78; 0,64; 0,21" | Bảng nguồn |
| 35 | A.2, A.3 | Dẫn `T-024/cham-a.md`, `T-026/cham-a.md` | Dẫn `T-024/cham-a.json` và `T-026/…/published-reference.json` (hash khớp) | Luật cứng 4 |

**Ngoài danh sách P-B:** ba chỗ (dòng "Chưa có phản biện" ở đầu file; trích dẫn `results/T-026/cham-a.md:594–596` ở §1 mục 1; câu "Số RCAEval Bảng 6 … Claude chưa mở lại" ở §4 và A.2) đã được sửa theo P-C, xem C.3.

### C.2 Công thức của các số ở K4 và D.1

- **Dữ liệu:** `results/T-024/cham-a.json#/methods/*/per_case/*` (trường `rr`, `label.cell`); hash khớp `results/T-024/work/danh-sach-tep-cuoi.json`.
- **SD của chênh RR theo ca trên dev30:** TORAI B − SimpleRCA 0,3631; TORAI B − BARO 0,3204.
- **Nửa độ rộng CI 95% theo ca:** 1,96 · SD / √n.
  - n = 60: 0,092 (cặp SimpleRCA), 0,081 (cặp BARO).
  - n = 30: 0,130 và 0,115.
- **Xác suất điểm ước lượng dưới −Δ khi chênh thật bằng 0:** Φ(−Δ / SE).
  - n = 60: 0,143 (cặp SimpleRCA), 0,113 (cặp BARO).
  - Xác suất một phương pháp kém thật 0,10 vẫn qua có cùng giá trị, do đối xứng.
- **Power của câu (1) khi chênh thật bằng 0:** Φ(Δ / SE − 1,96). n = 30: 0,114; n = 60: 0,186.
- **Theo ô (10 ô, t₉ = 2,262), trên dev30:** 2,262 · SD(trung bình ô) / √10 cho 0,151 (cặp SimpleRCA) và 0,207 (cặp BARO).
- **Cỡ mẫu cho một tỷ lệ:** n = 1,96² · p(1 − p) / E² = 80,7, với p = 0,7 và E = 0,10.
  - Hệ số thiết kế = 1 + (m − 1) · ICC, với m = 3 và ICC = 0,2–0,4, cho 1,4–1,8. Nhân vào được 112,9–145,2.
  - Nửa độ rộng với n = 60: 1,96 · √(p(1 − p) · hệ số / 60) = 0,137–0,156.
- **Giả định:** xấp xỉ chuẩn; các ca độc lập (trừ dòng tính theo ô); SD lấy từ một cặp baseline, còn SD của phương pháp mới chưa biết; ICC chỉ là giả định để xét độ nhạy.
- **Lệnh:** `py -3 -I -c`, chỉ đọc JSON, không ghi file (23/10/2026). Codex tính lại bằng `py -3 -B -` và ra cùng kết quả.

### C.3 Đính chính lượt 2 (P-C)

- **Căn cứ:** lượt kiểm lại mới nhất của Codex (hai điểm: khả năng phân xử của dev; FIS) và phản hồi của Claude (N5), ngày 23/10/2026, trong chat.
- **Lời duyệt của Minh:** "Duyệt P-C: sửa đúng các vị trí đã liệt kê trong docs/KHAO-SAT-SAU-K1-K6.md (gồm ba chỗ cũ ngoài P-B), thêm C.3 vào Phụ lục C và một dòng lịch sử. Không sửa file khác, không commit."

| # | Vị trí | Câu cũ (tóm tắt) | Câu mới (tóm tắt) | Căn cứ |
|---|---|---|---|---|
| 1 | §1 mục 2 | "Dataset dev quá nông để phân xử lợi ích của đồ thị"; "TORAI B đã có Hit@3 = 1,0. Mọi lợi ích còn lại chỉ có thể là xếp lại trong top-3"; "benchmark lan sâu"; "tiêu chí bác bỏ … có thể bác nhầm" | "Khả năng phân xử của dev còn hạn chế; cần xác định theo từng cơ chế và độ đo"; call depth chỉ là chỉ báo; Hit@3 = 1,0 chỉ thuộc RE2-TT dev30 và độ đo top-3, TORAI B không chạy trên Nezha-OB; thêm WHY-03 và G2-H06; bác nhầm chỉ khi ít ca phân xử được (KS-16); thêm dataset là ứng viên | Codex lượt 2, điểm 1; WHY-03; SL21 |
| 2 | Bảng K1, FSE 2026 | "Bộ mới lan sâu 7 tầng" | "Bộ mới có max call depth 7 (chỉ báo, chưa phải độ sâu lan của từng ca)" | Codex lượt 2, điểm 1 |
| 3 | K6 mục 13 | "số trên benchmark lan sâu" | "số trên benchmark có call depth lớn (FSE 2026)" | Codex lượt 2, điểm 1 |
| 4 | KS-17, cột lý do | "Dev nông" | "Khả năng phân xử của dev còn hạn chế" | Codex lượt 2, điểm 1 |
| 5 | K5, FIS | "Các SSM document dựng sẵn chạy tc trên interface của host (mặc định `eth0`), nên không nhắm được cạnh giữa hai container cùng máy" | "Cấu hình mặc định … chưa bảo đảm nhắm đúng cạnh; FIS cho đặt `Interface`, lọc `Sources`, `TrafficType`, dùng document tùy biến; chưa kiểm" | Codex lượt 2, điểm 2 |
| 6 | K2, GALA+; §4 | §4: "McNemar … chưa kiểm chắc" | K2 thêm: McNemar trên đa số phiếu theo sự cố qua 3 lượt, nhị thức chính xác một phía, cặp bất đồng 27/4 và 35/12; xóa dòng ở §4 | GALA+ §5.3.1 (Claude và Codex đều đã đọc) |
| 7 | Bảng K1, PetShop; đề xuất E5 | "nút bất thường mà cha không bất thường" | Quy tắc đầy đủ theo mã tác giả: không có nút nguyên nhân bất thường **và** có đường toàn nút bất thường tới mục tiêu; điểm là tổng lớn nhất trên đường; ghi chú chiều cạnh [SUY LUẬN] | N5; mã PetShop commit `2e96f93` |
| 8 | Đầu file, Trạng thái | "Chưa có phản biện. Prompt cho Codex ở Phụ lục B." | "Đã qua phản biện và kiểm lại của Codex ngày 23/10/2026; các sửa ghi ở Phụ lục C. Prompt lượt đầu ở Phụ lục B." | Ba chỗ cũ ngoài P-B |
| 9 | §1 mục 1 | "bài Nezha báo 41% … `results/T-026/cham-a.md:594–596` ghi …" | "bài Nezha báo 41,07% (`published-reference.json`, hash khớp) … T-026 ghi …" | Ba chỗ cũ ngoài P-B; luật cứng 4 |
| 10 | §4; A.2 | "Số RCAEval Bảng 6 … do subagent đọc, Claude chưa mở lại" | "Codex đã đối chiếu nguồn gốc (BARO 0,67 metric, 0,69 multi-source; CIRCA 0,32, 0,06). Claude chưa mở lại" | Ba chỗ cũ ngoài P-B; phản biện lượt 1 của Codex |
| 11 | C.1, câu cuối | "Chưa sửa vì ngoài danh sách P-B …" | Ghi ba chỗ đó đã sửa theo P-C, trỏ tới C.3 | — |

### C.4 Đính chính lượt 3 (P-D)

- **Căn cứ:** câu hỏi của Minh ngày 23/10/2026: KS-17 có tổng hợp bằng chứng, lợi ích, phần thiếu và việc phát sinh của từng lựa chọn chưa, hay là đề xuất mù; và nhánh H gom cảnh báo kiểu gì khi chưa có RCA và hạ tầng. Claude trả lời: KS-17 là đề xuất mù, bỏ sót quyết định G1 (`results/T-021/goi-g1.md`) và thẻ dataset benchmark FSE ở T-012. KS-13 không nêu chuỗi phụ thuộc.
- **Lời duyệt của Minh:** "Duyệt P-D: sửa đúng các vị trí đã liệt kê trong docs/KHAO-SAT-SAU-K1-K6.md (KS-17 hoãn, KS-13 thêm thứ tự phụ thuộc, đính chính benchmark FSE theo T-012, ghi lý do G1 loại RE2-OB), thêm Phụ lục D, mục C.4 và một dòng lịch sử. Không sửa file khác, không commit."

| # | Vị trí | Câu cũ (tóm tắt) | Câu mới (tóm tắt) | Căn cứ |
|---|---|---|---|---|
| 1 | KS-17 | "Hỏi Minh: có thêm bộ lan sâu (FSE 2026), RE2-OB, hoặc bảng phụ OTel Demo?" | "Hoãn. Quyết sau KS-15 và KS-16. Bảng phương án ở Phụ lục D" | Đề xuất mù; bỏ sót T-021 và T-012 |
| 2 | KS-13 | "H0/H1 thành task nhỏ; …" (không nêu phụ thuộc) | Thêm thứ tự phụ thuộc: H0 cần bộ luật cảnh báo và đồ thị P5; H1 cần Mô-đun B; đo gộp nhầm cần hạ tầng H3; M-20 vẫn giữ | Câu cũ dễ đọc thành "làm ngay" |
| 3 | Bảng K1, dòng FSE 2026 | "Chưa thấy URL dataset" | "Bản công khai là artifact rút gọn 10 ca, 8 ca dùng được (T-012); bộ đầy đủ 1.430 ca chưa thấy công khai" | `results/T-012/the-dataset.md`, mục FSE |
| 4 | §4 | "Benchmark FSE 2026: chưa thấy URL, license, dung lượng" | Artifact Zenodo 19522409, 91 MB, 10 ca, 8 dùng được; license dữ liệu thô OPEN; bộ đầy đủ chưa thấy công khai | Như trên |
| 5 | K6 mục 5 | "Thêm nó là quyết định cấp G1" | Thêm: G1 đã loại RE2-OB vì TX2; chỉ làm dev hoặc tái lập | `results/T-021/goi-g1.md:116`; `results/T-015/ca-da-chay.csv` |
| 6 | Mới | — | Phụ lục D: bảng bốn phương án cho KS-17 và chuỗi phụ thuộc của nhánh H | — |

---

## Phụ lục D. Phân tích phương án KS-17 và chuỗi phụ thuộc nhánh H (23/10/2026)

Nhãn: [REPO] là dữ kiện trong file repo; [GỐC] là nguồn gốc đã đọc; [SUY LUẬN] là suy luận.

### D.1 Phương án dữ liệu cho KS-17

| Phương án | Bằng chứng đã có | Lợi ích | Phần thiếu | Việc phát sinh |
|---|---|---|---|---|
| **0. Giữ nguyên:** dev RE2-TT và Nezha-OB; RE3-OB giữ ngoài | Q-61, Q-68 [REPO]. WHY-03: vẫn kiểm được một cách dùng quan hệ trên 5 vị trí của RE2-TT [REPO] | Không phát sinh việc. Giữ test sạch: 60 ca RE2-TT ở TX1, RE3-OB ở TX0 | RE2-TT có 5 root ở vị trí cố định, không khái quát được sang topology khác. Nezha-OB lệch số công bố chưa giải thích (KS-15). Khả năng phân xử theo từng cơ chế chưa đếm (KS-16) | Không |
| **A. RE2-OB** (90 ca) | TX2 (`results/T-021/goi-g1.md:116`) [REPO]. Dữ liệu từng nằm trên EC2 của T-015; máy local chỉ có 1 ca mẫu (`data/README.md:17`) [REPO]. Có `statusCode` trong mẫu (T-002; file khớp manifest T-020) [REPO]. Type III 13% (`results/T-017/type-i-ii.md`) [REPO]. Nhiều bài 2025–2026 dùng: GALA+, RCLAgent, DynaCausal [GỐC] | So được với số công bố của nhiều bài. Có mã trạng thái, hữu ích cho E3b. Dùng chung adapter RE2 | TX2 nên không làm kiểm độc lập được. Cùng 6 loại lỗi tài nguyên và mạng như RE2-TT. Cùng nhóm và công cụ thu với RE2-TT, không độc lập theo tiêu chí 9 | Lấy lại dữ liệu (dung lượng chưa kiểm, phải trình trước). Chạy lại 6 baseline. Dòng DECISIONS mới sửa Q-61, Q-68 |
| **B. Benchmark FSE 2026** | Artifact công khai Zenodo 19522409, 91 MB: 10 ca, 2 ca có marker invalid, 8 ca dùng được; 11 service gốc; 8 mã lỗi; mỗi ô một lần; có parent span, metric, log, trace Parquet; tên ca và `injection.json` lộ nhãn; phạm vi license dữ liệu thô OPEN; cùng upstream TT với OpenRCA 2.0 (`results/T-012/the-dataset.md`, mục FSE) [REPO]. Bộ đầy đủ 1.430 ca chưa thấy công khai [GỐC] | Lỗi đa dạng: container kill, exception, request delay, bandwidth, response replace. Có ca nhiều root. Bài có số baseline trên bộ đầy đủ | 8 ca, không lặp: không đủ để thống kê hay làm dev. Ca nhiều root cần quy tắc chấm mới | Adapter Parquet mới. Quy tắc chấm nhiều root. Bộ đầy đủ phải xin tác giả (việc bên ngoài, Minh quyết). Thực tế chỉ dùng được làm ca minh họa |
| **C. Bảng phụ OTel Demo** (nhóm tự tiêm) | OTel Demo 3.1.0 có cờ lỗi với đáp án rõ, cần khoảng 6 GB RAM (mục K5) [GỐC]. T-012 có thẻ OpenRCA 2.0 trên OTel Demo, chạy Kubernetes, chưa phát hành [REPO]. C-07 ghi OTel Demo là sân thử, không vào bảng chính [REPO] | Telemetry giàu như FlashTicket (kind, DB, Kafka). Dùng được khi FlashTicket chưa sẵn (M-06). Hệ không do nhóm thiết kế. Hạ tầng H2–H3 đằng nào cũng phải dựng | Nhóm tự tiêm và gán nhãn, không độc lập. Cờ lỗi viết để demo, có thể quá dễ. Chưa có số baseline công bố trong cùng điều kiện | Danh mục kịch bản khai trước. Adapter sang định dạng 6 baseline (cũng cần cho FlashTicket, C-06). Giờ máy chưa ước lượng. Lọc `flagd` và `feature_flag.*` khỏi đầu vào RCA (luật cứng 6) |

**Khuyến nghị [SUY LUẬN]:**
- Chưa quyết KS-17. Làm KS-15 và KS-16 trước; cả hai chỉ đọc và rẻ.
- Kết quả của hai việc đó cho biết có cần thêm dữ liệu không, và cần loại nào.
- A chỉ thêm ca dev và giúp so với tài liệu. B hiện chỉ đủ làm ca minh họa. C trùng phần lớn với việc hạ tầng đã có trong kế hoạch.

### D.2 Chuỗi phụ thuộc của nhánh H

Nhánh H không làm ngay. Không gom cảnh báo được khi chưa có cảnh báo; H1 còn cần RCA.

| Phần | Cần gì | Trạng thái 23/10/2026 |
|---|---|---|
| Có cảnh báo để gom | Bộ luật cảnh báo đang chạy. Trên FlashTicket hoặc OTel Demo: hạ tầng bước H3 (Grafana alerting). Trên dữ liệu công khai: phát lại luật trên metric đã lưu (RE2-TT chế độ b), không cần hạ tầng | Chưa có; bộ luật là phần nghiên cứu phát hiện ở D.4 của KE-HOACH |
| Đồ thị phụ thuộc | Bộ dựng P5 | Có (T-035; nguồn tĩnh T-036 đến T-039) |
| **H0:** sinh luật nén từ đồ thị | Đồ thị P5 + bộ luật cảnh báo. Không cần RCA | Chờ bộ luật |
| **H1:** gom theo nhãn tự sinh/kế thừa | Mô-đun B (một phần RCA) chạy được | Chờ RCA |
| Đo gộp nhầm hai sự cố | Hạ tầng thật và kịch bản hai lỗi chồng thời gian | Chờ H3 và FlashTicket hoặc OTel Demo |

**Thứ tự nếu Minh quyết làm H:**
1. Soạn bộ luật cảnh báo.
2. Chạy H0 offline: phát lại trên RE2-TT, đo tỷ lệ nén và số sự cố bị bỏ sót.
3. Khi Mô-đun B chạy được: làm H1.
4. Khi có hạ tầng: đo gộp nhầm.

M-20 vẫn có hiệu lực; Minh có thể giữ H ở trạng thái hoãn. Giá trị của H là có câu trả lời cho hội đồng về "đồ thị tham gia báo động"; H không phải phần lõi DT18 yêu cầu [SUY LUẬN].

---

## Lịch sử

| Ngày | Người sửa | Nội dung | Căn cứ |
|---|---|---|---|
| 23/10/2026 | Claude | Tạo file: báo cáo khảo sát K1–K6, Phụ lục A (trả lời lượt 2, quyết định E-04), Phụ lục B (prompt Codex) | Lời Minh 23/10/2026 ở đầu file; lựa chọn "Báo cáo + trả lời + prompt" |
| 23/10/2026 | Claude | Sửa theo P-B sau phản biện Codex: 35 vị trí liệt kê ở Phụ lục C.1; thêm Phụ lục C (câu cũ → mới, công thức) | Lời Minh 23/10/2026 duyệt P-A và P-B (M-45 trong KE-HOACH) |
| 23/10/2026 | Claude | Sửa theo P-C sau lượt kiểm lại của Codex: 10 vị trí và câu cuối C.1, liệt kê ở Phụ lục C.3 | Lời Minh 23/10/2026 duyệt P-C (chép ở C.3) |
| 23/10/2026 | Claude | Sửa theo P-D: KS-17 hoãn, KS-13 thêm thứ tự phụ thuộc, đính chính benchmark FSE theo T-012, ghi lý do G1 loại RE2-OB (liệt kê ở C.4); thêm Phụ lục D | Lời Minh 23/10/2026 duyệt P-D (chép ở C.4) |
