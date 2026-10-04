# Báo cáo cuối T-019 — 04/10/2026

**A. Đã làm.** Hoàn tất thẻ RE2-SS/RE3-SS đủ10mục/9tiêu chí, RE1-SS ngắn; census245SSca, kiểm618file và8nhãn chi tiết; sổ ca đã nhìn SS/OB, đính chính và nháp tài liệu chung. Hai subagent hỗ trợ độc lập; Claude chưa phản biện.

**B. File đã thay đổi, kể cả ngoài repo.** tasks/T-019-the-sock-shop/SPEC.md và LOG.md; mọi file results/T-019/ liệt kê trong output-files.csv/artifact-manifest.json;618file data/T-019/ ngoài git;180file D:/RCA-ext/work/T-019/lineage/re2ob/ (đầy đủ path ở lineage/outside-files.csv). docs/STATE.md chỉ dòngT019. Không sửa file task cũ, môi trường/src hoặc nguồn chung khác. Không commit/push.

**C. Kiểm tra đã chạy và kết quả.** Census độc lập/hash/parser/schema/biên/nhãn PASS; metadata toànSS khôngtrace. RE2=90ca/5root/30ô; RE3=30ca/3root/9ô. Cả120ca RE2/3 có metric±720s quanh tiêm. Lineage405cặp:400fullmetric,5finite-time sau bỏ nulltime. Sổ1245hàng quan hệ/exposure, không phải1245incident. Kiểm band/count465bộ từ2rawcase và táiaggregate toàn summary PASS. Tải161.824.212byte, cache replay0byte. Kiểm final/state/handoff được ghi riêng; mọi lượt hỏng giữ lại.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** T003 dòng19 dẫn hồ sơ Sock Shop về T002 trong khi SPEC/thẻ T002 chỉ có bốn TT/OB và schema hai mẫuSS. T019 đã bổ sung hồ sơ riêng; đề xuất sửa referral, chưa sửa cũ. Không chứng minh sai số mới ở T002. Bổ sung nguồn: HF bảngF5SS lệch prose/GitHub/tree; một root_cause front-end_f2_2 trùng ca trước và ngoài cửa sổ own log. Đây là lỗi nguồn nhãn, không tự là lỗi người làm task cũ. Bằng chứng/đoạn sửa tối thiểu ở dinh-chinh-task-cu.md.

**E. Chỗ lệch khỏi SPEC và lý do.** Không vượt phạm vi. Bổ sung tách constant/all-null, finite paired rates và --run/cache verified để tránh mẫu số0 và tái lập ghi đè. SPEC chỉ ghi thêm mục Thay đổi trong lúc làm. Lượt serialization lỗi và tổng hợp trước sửa được giữ. Không đổi q/band/raw hay lựa chọn nghiên cứu.

**F. Đề xuất cho tài liệu chung.** Nháp nguyên văn DECISIONS về ủy quyền, README dữ liệu/modalities/lệnh dựng và thông tin G1 về exposure/biên/nhãn ở de-xuat-tai-lieu-chung.md. Không tự ghi WHY/lựa chọn dataset.

**G. Phần chưa kiểm và lý do.** Parent/log-trace/root runtime degree không có đầu vào trace; mapping kiến trúc sang deployment OPEN. Onset/end/normal sạch/vùng ảnh hưởng/code-line không có nhãn/source độc lập; mô tả giả định và điều kiện sai trong thẻ mục10. Không chạy RCA/detector theo prompt.

**H. Cần Minh quyết.** Cho Claude phản biện T019. Tại tổng hợp G1, quyết dùng/không dùngSS, kịch bản graph kiến trúc, cách dùng nhãn và chia dữ liệu sau khi xét sổ exposure. Nếu ghi nguồn chung hoặc sửa referral cũ, Minh duyệt riêng bản nháp. Task này không tự quyết các mục đó.
