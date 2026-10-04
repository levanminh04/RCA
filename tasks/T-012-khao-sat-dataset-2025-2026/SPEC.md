# T-012 — Khảo sát có giới hạn dataset công bố 2025–2026

- **Trạng thái:** được giao triển khai gói 03/10/2026; nguồn/metadata đang làm; telemetry và tải lớn chờ quyền đọc.
- **Người làm:** Codex (subagent hỗ trợ người làm).
- **Người phản biện:** Claude, dự kiến.
- **Thuộc gói MRP:** P2 — **Cổng:** G1.
- **Gói cha:** T-003.

Quyền triển khai gói được Minh giao trực tiếp ngày 03/10/2026: “triển khai toàn bộ task 003 cho tôi, gồm cả các task phụ , sử dụng sub agent với model mạnh nhất nếu cần”. Đây là lệnh EXECUTE, thay giới hạn chỉ đọc của lượt đề xuất. Không suy lệnh này thành quyền chọn dataset/đổi G1/G3/đọc data/locked. Quyền đọc telemetry của ứng viên mới và gói tải lớn đang chờ câu trả lời rõ từ Minh; phần nguồn/metadata/nhãn riêng được làm ngay.

## Mục tiêu

Cung cấp bằng chứng cho tiêu chí MRP §4, RQ1/RQ3a/b/c và G1. Phục vụ DT18-NV2/NV3 và nhận xét của cô về mở rộng dataset trước thiết kế. Không quyết định chọn/bỏ dataset.

## Đầu vào

- D:/RCA-flashticket/AGENTS.md; docs/STATE.md; docs/MRP.md §4, P2 và G1; docs/WHY.md WHY-03/04/06; docs/DECISIONS.md Q-21/31/33/40/41/43/44.
- D:/RCA-flashticket/docs/LESSONS.md; docs/knowledge/K3-dataset-ung-vien.md.
- D:/RCA-flashticket/results/T-002/mau-the-dataset.md; the-rcaeval.md; tasks/T-002-the-dataset-rcaeval/SPEC.md và mục cuối LOG/REVIEW.
- D:/RCA-flashticket/docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và advisor-2026-09-23.md.
- SPEC/LOG gói cha D:/RCA-flashticket/tasks/T-003-the-dataset-ngoai-rcaeval/.
- Biến thể: Các đầu mối K3 (FSE fault propagation, AnoMod, TrainTicketTrace, OpenRCA/2.0, Check Your Trace First, LO2 và các đầu mối công bố 2025–2026 khác); một lượt tìm tối đa 90 phút/sáu truy vấn/12 hồ sơ chính thức. Không đổi danh sách thí nghiệm tự động.
- Nguồn: Nguồn primary: bài tác giả/arXiv/conference và repo/DOI/kho dữ liệu/giấy phép phát hành. K3 chỉ điểm xuất phát.

## Đầu ra

- D:/RCA-flashticket/results/T-012/the-dataset.md: thẻ các biến thể đủ10mục, nguồn/metadata và mức file đã kiểm tách rõ.
- D:/RCA-flashticket/results/T-012/scripts/: mã lấy/kiểm nguồn/metadata/nhãn, kiểm file sau quyền đọc.
- D:/RCA-flashticket/results/T-012/sources/, runs/<run-id>/: snapshot, manifest revision/license/source, số đếm/schema/chi phí/case/graph/symptom/validation khi đã có, giữ lượt hỏng.
- D:/RCA-flashticket/results/T-012/inspection-plan.md: đúng file/mẫu/byte/cách chọn/ngân sách/giới hạn suy rộng và quyền chưa có.

## Phạm vi ghi

- D:/RCA-flashticket/results/T-012/.
- D:/RCA-flashticket/data/ngoai-rcaeval/metadata/T-012/: metadata/nhãn riêng được làm ngay; telemetry chưa được tải/đọc nếu chưa có câu trả lời quyền đọc trong LOG gói cha.
- SPEC này tạo trong gói được giao; LOG của task chỉ thêm; dòng T-012 trong STATE do root cập nhật. Root cập nhật đúng mục dữ liệu và quyết định của gói; subagent không sửa docs/file dùng chung.
- Không cài/sửa môi trường chung; py -3 -B với thư viện chuẩn hoặc đọc môi trường có sẵn. Gói mới cần báo phạm vi trước.

## Các bước

1. Khóa source/revision/biến thể/giấy phép; kiểm bằng script --sources và manifest đối chiếu nguồn.
2. Lấy metadata/nhãn riêng và census; kiểm bằng script --validate-counts, tổng theo ngày/ô/loại và kiểm nhãn mẫu bằng raw label.
3. Lập inspection-plan (chọn trước theo metadata); kiểm bằng bảng coverage theo hệ/ngày/schema/root/fault/repetition và byte dự kiến.
4. Khi quyền đọc được Minh cấp: tải đúng file, hash/CRC/archive member; đọc schema/parent/normal/mapping/graph/nhãn thật. Kiểm bằng số trung gian từng ca và phép tính lại độc lập; phân phối không có trường nào thì báo đúng release.
5. Khảo sát thô tiêu chí7 nếu được phép; kiểm đối chứng/kênh/q/ca/ô, không tạo nhãn lan. Gói giữ ngoài bỏ bước4–5 số đo đến G3, không kết luận thay.
6. Sinh thẻ từ kết quả; script --verify và kiểm diff/links/numbers; LOG bàn giao và prompt chung+G1 nguyên văn (Q44).

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

Đủ biến thể đã liệt kê, nguồn official+revision+license+manifest, thẻ10mục, bảng nhãn/task/coverage và số trỏ artifact. Phần file được phép đã kiểm mức cần cho kết luận; còn phần chưa quyền đọc/giấy phép phải ghi đúng OPEN và không báo hoàn tất kiểm dataset. “Chờ phản biện” chỉ khi đầu ra đáp ứng phạm vi được duyệt; đóng task do Minh.

## Không làm

Không RCA/detector/training/MyRCA; không chọn dataset/dev-test/giữ ngoài; không mở data/locked; không archive cũ; không tự đổi timestamp hoặc lấp nhãn; không commit/push/external messages. Không thêm quy trình/cổng hoặc score tổng.

## Chi phí ước lượng

Metadata/tài liệu dự kiến dưới 25 MB; chưa duyệt archive mới. 60–90 phút nguồn; file thật sẽ được trình đúng release/byte sau khi nhận diện. Giữ mọi lead vượt giới hạn ở bảng chưa đánh giá; không gọi khảo sát exhaustive.
Q40 giới hạn phương pháp3giờ/dataset, không phải quota bỏ phép kiểm dữ liệu. Ghi thời gian từng bước ngay từ đầu; lượt >1giờ/tải >5GB phải chờ Minh đồng ý theo luật8. Hiện ≤2subagent GPT-6Astra hỗ trợ gói, không thêm agent khác.

## Rủi ro và điều chưa chắc

Quyền telemetry/giữ ngoài còn OPEN; thiếu nguồn/giấy phép không tự giải quyết. File trong archive cần tải không coi đã kiểm từ code. K3 chưa xác minh; một ca không suy toàn kho; root/position/fault có thể confound, đồng thời ngoài root không chứng minh propagation. Nếu material conflict ảnh hưởng dùng dữ liệu, dừng phần phụ thuộc và báo Minh; đọc source và mô tả vẫn được.


## Bổ sung được Minh duyệt 03/10/2026 (Q-47)

Thay giới hạn chờ quyền/không EC2 trước đây: dùng EC2 mới 3.26.62.217/key2, /home/ubuntu/rca-t003/{data,scripts,results}/ cho DeepTraLog và bốn ZIP LEMMA IT đã đề xuất; Nezha/Eadro dùng vùng data laptop đã liệt kê. Được tải gói 5,265 GB theo kế hoạch đã trình và cài công cụ giải nén cần thiết; không dùng instance T-007. Codex được giao quyết ứng viên bảo toàn dựa thông tin chung/nhãn/schema/tính độc lập trước số đo, ghi lý do trong WHY trước dùng; các ứng viên còn lại được kiểm số đo theo SPEC. Bộ bảo toàn chỉ metadata/schema/đếm nhãn trước G3. Không chia dev/test hoặc chọn dataset thí nghiệm thay G1. OT (SWaT/WADI) bỏ khỏi phạm vi mới, giữ nguồn lịch sử không xóa. LEMMA xác minh giấy phép trước dùng phần phụ thuộc. Claude phản biện gộp một REVIEW ở task T-003, gồm tất cả nhánh và tổng hợp; không cần REVIEW riêng nhánh. Người làm tự phản biện độc lập, sửa lỗi tự tìm trước bàn giao. Bổ sung phạm vi ghi docs/WHY.md cho lý do bảo toàn được Minh giao quyết; results/task/LOG/STATE/data README và DECISIONS theo phạm vi hiện hành.


## Bổ sung sửa phản biện R1–R4 được Minh giao 03/10/2026

Minh yêu cầu đọc/phản biện review và sửa ngay điểm đồng ý, không dùng subagent nếu không cần. R1 bổ sung data/ngoai-rcaeval/T-012/{anomod,trca,fse}/ trên laptop: tải đúng ba archive record18342898/19335897/19522409,628.411.611byte (kế hoạch đã báo trước); kiểm checksumofficial, toànmember phát hành/census/schema/clock/parent/entity/normal/graph/probe đủ điều kiện. Không giảm thành chỉ nguồn, không suy artifactFSErútgọn thành toànpaper. Các archive/raw khônggit. R3 chỉBank Driveinventory/schema/đếmnhãn táchriêngnếutruycậpđược, khôngđọcsốđo hoặcagentpredictions. Kếtquả/script/nguồn trongresults/T012 vàgói nhưphạmvi trước; cậpnhậtthẻ/bảng/LOG/dataREADME/STATE, bảngphảnhồiREVIEWparent, WHY13giới hạn đúng. KhôngđổiG1/G3/split/đóngtask/commit/push.
