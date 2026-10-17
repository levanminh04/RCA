# Dòng quyết định TraceRCA xin Minh duyệt nối

Minh đã duyệt thực hiện đúng `de-xuat-tracerca-path-001.md` ngày 10/10/2026. Chỉ dòng lưu quyết định dưới đây còn chờ Minh duyệt. Đọc lại `docs/DECISIONS.md` ngay trước nối; Q-98 đã có thì dừng trình, không ghi đè.

| Q-98 | 10/10/2026 | Minh duyệt đúng results/T-032/de-xuat-tracerca-path-001.md: chỉ TraceRCA dùng bản code RCAEval revision 259ea41 byte-identical dưới path cha có token rcaeval chữ thường trong ~/rca/T-032; closure ≤5 MiB, kiểm inventory/hash nguồn–đích và actual import, không fallback; fixture và tối đa ba pilot RE2 ERROR/OK/Nezha, mỗi pilot ≤10 phút, tổng ≤30 phút/200 MiB; giữ exact toàn record và mọi lượt cũ, lệch dừng/trình, sau pilot đạt mới đo/dự toán cohort; không sửa SPEC/code chung/package/môi trường/task cũ, không áp path này cho phương pháp khác. Mỗi lúc một việc nặng EC2, TraceRCA chạy trước; cohort MicroRank chỉ sau Minh duyệt riêng và pilot TraceRCA xong; đo tổng mới so trần 8 GiB trước lượt lớn, vượt dừng/trình. | lời duyệt Minh 10/10/2026 trong chat; results/T-032/de-xuat-tracerca-path-001.md |

Ảnh hưởng: thêm đúng một dòng vào DECISIONS để lưu quyền đã có; không đổi tiêu chí, SPEC hoặc WHY. Phiên này vẫn chỉ làm T-032.
