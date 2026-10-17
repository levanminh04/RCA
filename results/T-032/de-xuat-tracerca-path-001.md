# TraceRCA: phân loại ngoại lệ khác theo đường dẫn — CHƯA DUYỆT

## Chỗ và bằng chứng

`src/p3/adapters/__init__.py:18–33` kiểm traceback thuộc phương pháp bằng chuỗi `rcaeval` và `os.path.normcase(path)`. Trên Windows, normcase hạ chữ thường; trên Linux, normcase giữ nguyên. Source và bản chuyển đã khớp hash.

Ca RE2 dev-03d4910932 có bản đóng băng ERROR với `KeyError: 'ts-order-other-service_getMore ts.orders'`, hash được khóa trong `results/T-024/ban-ghi-dua-vao-cham.json#/records`. Native EC2 ném đúng KeyError tại `~/rca/T-025/src/RCAEval/RCAEval/e2e/tracerca.py:59`, nhưng adapter gọi `loi(exc)` không nhận ra token `rcaeval`; nó ném `LoiRunner` thay vì trả ERROR. Bằng chứng: `runs/tracerca-re2-error-first-001/check.json#/traceback` và `capture/capture-start.json#/sources/native`. Kiểm stdlib POSIX/Windows ngày 10/10 cho cùng path: token_matches Linux=false, Windows=true. Chưa có ban-ghi phát lại hợp lệ cho ca này; không dùng trung gian làm cơ chế.

Hậu quả: giữ nguyên path EC2 hiện có không đáp ứng hợp đồng ERROR nguồn, dù native/code/input không đổi. Fixture mới đã giữ ngoại lệ thật và PASS, nhưng so original–observed cùng Linux không phát hiện khác Windows này. TraceRCA dừng phần phát lại phụ thuộc; phần coverage không gọi TraceRCA, BARO và các phương pháp độc lập tiếp tục.

## Đề xuất tối thiểu, không đổi thuật toán

1. Trong `~/rca/T-032/` tạo bản code RCAEval revision 259ea41 dưới path có token **rcaeval chữ thường**. Chỉ chép closure mã Python phương pháp cần import; bỏ tests, dữ liệu, .git, cache và khóa. Không đổi byte code adapter/native hay code/môi trường task cũ. Có inventory/hash từng file và kiểm nguồn–đích.
2. Chỉ launcher/replay TraceRCA của T-032 trỏ PYTHONPATH sang bản code này; verifier kiểm actual import mới, cùng revision/hash. Không thay packages/Python/parameters/tolerance.
3. Giữ fixture/pilot hỏng và pilot Nezha cũ. Chạy fixture mới và RE2 ERROR/OK để kiểm đúng phân loại nguồn và khớp tuyệt đối toàn record; Nezha pilot cũ cần kiểm thích hợp với đường import mới trước reuse. Nếu lệch: dừng, không sửa điểm/status để khớp.
4. Sau các pilot đạt mới đo/dự toán cohort. Các phương pháp khác chưa được áp đổi path này. Không sửa SPEC hay luật phân loại ngoại lệ dùng chung trong phiên này.

**Dự toán ứng viên, chưa đo inventory đầy đủ:** code closure ≤5 MiB; mỗi pilot guard ≤10 phút, tối đa ba pilot tổng ≤30 phút, ≤200 MiB trung gian mới. Nếu closure hoặc lượt pilot vượt dự toán thì checkpoint/dừng/trình Minh. Toàn bộ nằm trong ngân sách T-032 8 GiB và giờ máy đã duyệt; không chạy cohort trước đo đủ.

Phương án khác: Minh duyệt sửa bộ nhận diện source trong adapter (ảnh hưởng code dùng chung/nhiều phương pháp) hoặc phát lại laptop Windows nguyên môi trường nguồn (cần ngoại lệ EC2-only và còn phải exact). Đề nghị chọn bản code có path chữ thường để giữ nguyên byte/phạm vi phương pháp. Đây là CANDIDATE; chưa thực hiện.
