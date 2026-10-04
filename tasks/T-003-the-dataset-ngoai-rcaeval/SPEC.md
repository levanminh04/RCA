# T-003 — Gói thẻ dataset ngoài RCAEval

- **Trạng thái:** được Minh giao thực hiện toàn bộ gói ngày 03/10/2026; chưa chọn dataset hoặc quyền đọc telemetry.
- **Người làm:** Codex.
- **Người phản biện:** Claude, dự kiến.
- **Thuộc gói MRP:** P2 — **Cổng:** G1.

Quyền triển khai gói được Minh giao trực tiếp ngày 03/10/2026: “triển khai toàn bộ task 003 cho tôi, gồm cả các task phụ , sử dụng sub agent với model mạnh nhất nếu cần”. Đây là lệnh EXECUTE, thay giới hạn chỉ đọc của lượt đề xuất. Không suy lệnh này thành quyền chọn dataset/đổi G1/G3/đọc data/locked. Quyền đọc telemetry của ứng viên mới và gói tải lớn đang chờ câu trả lời rõ từ Minh; phần nguồn/metadata/nhãn riêng được làm ngay.

## Mục tiêu

Cung cấp đủ thẻ/bằng chứng cho Minh chọn dataset tại G1 theo cùng MRP§4/mẫu T002. Phục vụ DT18-NV2/NV3, nhận xét cô mở rộng dataset trước hạn chế/thiết kế, RQ1 và khả năng đánh giá RQ3a/b/c. T003 là gói tổng hợp; công việc một phiên tách T008–T012, không âm thầm giảm mức kiểm.

## Đầu vào

- D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md §4, P2 và G1; docs/WHY.md WHY-03/04/06; docs/DECISIONS.md Q-21/31/33/40/41/43/44.
- D:/RCA-flashticket/docs/LESSONS.md; docs/knowledge/K3-dataset-ung-vien.md.
- D:/RCA-flashticket/results/T-002/mau-the-dataset.md; the-rcaeval.md; tasks/T-002-the-dataset-rcaeval/SPEC.md và mục cuối LOG/REVIEW.
- D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md.
- Các SPEC và kết quả T008–T012; T002 chỉ đọc. DataREADME/review-prompt hiện hành. Published metadata không thay file thật.

## Đầu ra

- results/T-003/the-dataset-ngoai-rcaeval.md: thẻ hợp nhất theo10mục, dẫn source/result mỗi nhánh.
- results/T-003/bang-tieu-chi.md:9tiêu chí cho đủ ngoài RCAEval; đối chiếu RCAEval dẫn thẻT002 và cảnh báo review chưa Minhchốt.
- results/T-003/task-cham-duoc.md:dataset×task×nhãn×unit×phạmvi×limit.
- results/T-003/ke-hoach-kiem-file.md và phan-cong.md: task phụ, dependency, danh sách mẫu/byte/ngân sách/quyền đọc, phiên hoàn thành/chưa đủ.
- results/T-003/source-manifest.json và runs/:ghép manifest nhánh, thời gian/byte/checks/handoff, scripts/verify_outputs.py, snapshots sources khi cần.
- Kết quả khảo sát2025–2026 và lý do độc lập từng cặp; không thêm score/chọn dataset.

## Phạm vi ghi

- D:/RCA-flashticket/tasks/T-003-the-dataset-ngoai-rcaeval/SPEC.md (tạo theo gói giao), LOG.md (chỉ thêm).
- D:/RCA-flashticket/tasks/T-008-the-dataset-nezha/SPEC.md và LOG.md; results/T-008/; vùng data cụ thể theo SPEC nhánh.
- D:/RCA-flashticket/tasks/T-009-the-dataset-eadro/SPEC.md và LOG.md; results/T-009/; vùng data cụ thể theo SPEC nhánh.
- D:/RCA-flashticket/tasks/T-010-the-dataset-deeptralog/SPEC.md và LOG.md; results/T-010/; vùng data cụ thể theo SPEC nhánh.
- D:/RCA-flashticket/tasks/T-011-the-dataset-lemma-rca/SPEC.md và LOG.md; results/T-011/; vùng data cụ thể theo SPEC nhánh.
- D:/RCA-flashticket/tasks/T-012-khao-sat-dataset-2025-2026/SPEC.md và LOG.md; results/T-012/; vùng data cụ thể theo SPEC nhánh.
- D:/RCA-flashticket/results/T-003/.
- D:/RCA-flashticket/data/ngoai-rcaeval/metadata/T-003/; telemetry chưa quyền đọc mặc định không tải/đọc.
- D:/RCA-flashticket/data/README.md:thêm đúng mục dữ liệuT003 vàtaskphụ gồm nguồn/revision/byte/lệnhdựnglại/quyềnđọc.
- D:/RCA-flashticket/docs/STATE.md:chỉ dòngT003,T008–T012 và mục đang làm/chờMinh của gói, không sửa trạng tháiT002/task khác.
- D:/RCA-flashticket/docs/DECISIONS.md:thêm nguyênlời yêu cầu triểnkhaiQ45; câu trả lờiMinh phát sinh ghi đúng nguyêný, không suy lựa chọndataset.
- Không thay AGENTS/MRP/WHY/LESSONS/K3/mẫuthẻ/T002; không thay requirements/venvchung.

## Các bước

1. Ghi nguồn授权/phancong và trạng thái gói trước dữ liệu; kiểm danh sách task và phạmvi so SPEC.
2. Song song metadataNezha/Eadro và DeepTraLog/LEMMA với hai subagentGPT-6Astra; root tìm2025–2026. Kiểm manifest/labelcounts/raw source từng nhánh.
3. Sau metadata, chốt file/mẫu/byte cần đọc; không chờ tìm kiếm mới để làm nhánh đã có. Quyền đọc giữ ngoài/tảilớn là dependency phải có trả lờiMinh, không suy từ elapsedtime.
4. Kiểm file thật đúng quyền đọc theo SPECnhánh:label/time/parent/metric/log/link/root positions/normal/symptom/independence/cost. Kiểm lệnhscriptnhánh và sốtừngca/ô/q; không chạyRCA.
5. Tổng hợp đủ9tiêu chí và ma trậnchấm, mọi số có nguồn, OPENowner và limits. Kiểm bằng py -3 -B results/T-003/scripts/verify_outputs.py.
6. Tựsoát độc lập, hoàn tấtLOG/STATE/phạmvidiff; promptClaude chép nguyênmẫu+G1. Không tựđóngG1/commit/push.

## Kiểm đúng đắn

- Giữ đủ 10 mục mẫu thẻ T-002. Mỗi số có source snapshot/result path; FACT nguồn và FACT file không trộn. Đối chiếu công bố với đếm label/release, giữ cả hai nếu lệch.
- Census metadata/nhãn toàn release nếu lấy riêng được; root × fault × repetition/date, nhãn lỗi/thiếu/trùng. Pod/container→service cần mapping có nguồn.
- Khi Minh cho đọc telemetry: phủ mọi hệ/revision/ngày/schema; ít nhất một ca thực sự có từng root để mô tả vị trí; chọn theo metadata trước nhìn số đo. Các ô dùng so lần lặp phải kiểm đủ lặp; nếu khả thi ưu tiên toàn phần được phép. Muốn nói về nhiều root/fault, phủ ít nhất hai root và hai loại lỗi khi thực có; thiếu tầng thì nêu giới hạn, không tạo ca giả.
- Trace: sentinel root riêng, khóa (trace_id,span_id), tử/mẫu unique-parent, missing/ambiguous; graph cha→con giữa entity, bậc root tại chính ca nó là root; root vắng trace không tự gọi cô lập. So entity metric/log/trace và alias cụ thể.
- Metric/log: đơn vị/clock/cadence/gap/NaN/constant/duplicate; ID có cột/có giá trị/có trong payload/ghép được tách riêng. Published schema không thay schema file.
- Normal: normal riêng hoặc phần trước lỗi với nguồn giải thích, warmup và lỗi trước chưa đủ recovery. Injection≠onset/end. Kiểm biên file/order/path có lộ nhãn; không tự sửa clock/nhãn.
- Khảo sát thô tiêu chí 7 chỉ trên telemetry đã được Minh cho đọc: q=.95/.99/.995 trên độ lệch tuyệt đối so median bình thường, tách tham chiếu/đối chứng; không epsilon. Tách kênh/ca/ô, zero band/missing và số mẫu; không dùng OR tổng hoặc regex làm nhãn lan/vùng. Root gắn sau, không chọn SLI theo root. Đây là mô tả P2, không chọn detector/thiết kế phương pháp (WHY-03/P2).
- Bảng task: root label chấm ranking theo đúng entity; injection chỉ injection-regime nếu đủ interval và xử lý rò, không onset thật; nhãn vùng thật mới chấm vùng; nhãn trace riêng không suy root/time.
- Độc lập: nhóm tác giả + công cụ tiêm + stack + reuse raw. Cùng hệ không đủ, khác tên không đủ.
- Mọi thứ kiểm được với chi phí được duyệt phải làm; nếu không vừa phiên thì checkpoint/tách, không tự giảm mẫu. Phần chỉ metadata do chưa quyền đọc phải có owner Minh và kết luận phụ thuộc. Không gọi “không làm vì ngân sách” là “không thể kiểm”.

## Tiêu chí xong

Mọi ứng viên MRP ngoàiRCAEval có thẻ10mục, sources+revision+license+counts và taskmatrix; tất cả phần kiểm được và đượcphép đãlàm. Phần metadata-only theo giữngoài ghi rõ giới hạn; không coi code/schema côngbố là kiểmfile. Không báo gói xong nếu phầnMinh đãgiao vẫn còn và chưa có quyếtđịnhgiới hạn. Chờphảnbiện sau tựkiểm; task đóng bởiMinh.

## Không làm

KhôngRCA/MyRCA/thiết kếdetector/training; khôngchọn/bỏdataset/dev-test/holdout; khôngdata/locked/archivecũ; khôngcommit/push/external messages; không sửaT002 hoặc phonggópý thànhquyếtđịnh.

## Chi phí ước lượng

Nguồn/metadata2–4giờ tổnglàmviệc,nhiều nhánh song song, dự kiến≤100MB và lưu≤300MB; không cài môi trường/EC2. Cácnhánh kiểmfilethật1–4giờlàmviệc/nhánh chưađo,sốbyte ởSPECnhánh; LEMMA toànraw86,6GB cộnggiảinén khôngthíchhợp56,8GB trống. Khôngduyệt tải toànLEMMA. Tải>5GB/lượt>1giờ cầnMinhcho phép; Q40 chỉáp dụngkhi chạy phươngpháp,vốnngoàitasknày.

## Rủi ro và điều chưa chắc

Giữngoài chưa chọn: metadata/schema/nhãnriêng làmngay; telemetry chờMinh, đọc1mẫu cũngmấtđiềukiệnchỉmetadata. LEMMAlicenseNCvsND giữOPENdừngdùngdữliệuphụthuộc; Eadro/Deeplicense cầnxácminh. STATE T002cũ cógiảithích cuốiLOG, khôngtựđóng/sửa. SockShop cònthiếuphạmviG1nhưngnằmngoàiT003, nêukhoảngtrốngkhôngtựthêm. K3chưađượcxácminh; phươngánschema/mẫu/chi phí chưa kiểm phải cóđiềukiệnsai vàowner.


## Bổ sung được Minh duyệt 03/10/2026 (Q-47)

Thay giới hạn chờ quyền/không EC2 trước đây: dùng EC2 mới 3.26.62.217/key2, /home/ubuntu/rca-t003/{data,scripts,results}/ cho DeepTraLog và bốn ZIP LEMMA IT đã đề xuất; Nezha/Eadro dùng vùng data laptop đã liệt kê. Được tải gói 5,265 GB theo kế hoạch đã trình và cài công cụ giải nén cần thiết; không dùng instance T-007. Codex được giao quyết ứng viên bảo toàn dựa thông tin chung/nhãn/schema/tính độc lập trước số đo, ghi lý do trong WHY trước dùng; các ứng viên còn lại được kiểm số đo theo SPEC. Bộ bảo toàn chỉ metadata/schema/đếm nhãn trước G3. Không chia dev/test hoặc chọn dataset thí nghiệm thay G1. OT (SWaT/WADI) bỏ khỏi phạm vi mới, giữ nguồn lịch sử không xóa. LEMMA xác minh giấy phép trước dùng phần phụ thuộc. Claude phản biện gộp một REVIEW ở task T-003, gồm tất cả nhánh và tổng hợp; không cần REVIEW riêng nhánh. Người làm tự phản biện độc lập, sửa lỗi tự tìm trước bàn giao. Bổ sung phạm vi ghi docs/WHY.md cho lý do bảo toàn được Minh giao quyết; results/task/LOG/STATE/data README và DECISIONS theo phạm vi hiện hành.
