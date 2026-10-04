# Đối chứng normal với trace trước pseudo-mốc

Snapshot `runs/normal-normal-architecture-pretrace/snapshot.json` có270 scored metrics. Graph trace được dựng ở pseudo detect=1706071469, trước mốc tiêm thật=1706071770. Script độc lập dùng dictionary `(traceID,spanID)` từ raw trace đã lọc startTime<1706071469×10⁶, không gọi service_calls/builder. Nó có37472 span và20 service call edges; counts và edges khớp graph report. Các span hai đầu đều lấy trong tập trước pseudo-mốc. Chi tiết ở `paper/normal-pretrace-verification.json`.

Train t_d thật−421…−311; test t_d thật−10…−1. Không chứa điểm sau tiêm. Metric preprocessing của lượt này dùng toàn720 điểm trước **mốc tiêm thật**, gồm300 điểm sau pseudo-mốc. Vì vậy “strict” ở đây xác nhận **trace trước pseudo-mốc** và scoring windows trước injection; không tuyên bố mọi lựa chọn candidate/constant đã chỉ dùng train trước pseudo-mốc.

Independent OLS/RHT/DA2160 checks PASS, max absolute error=2.2204460492503131e-16; raw resampling/parent1080 array checks PASS, error0. Kết luận dựa actual report errors và source hashes, không dựa bool numerically_verified tự gán. Graph/nodes/effective parents/arrays/RHT ranks của snapshot cũ và mới giống nhau ở ca này; cutoff chặt hơn đã được kiểm từ raw thay vì suy từ sự giống nhau.

Vẫn có60/270 score≥3, top `ts-security-service_mem` score823.72419999532769. Đó là kết quả negative control của ca này. Các khả năng khác gồm drift/warmup, normal reference chưa phủ test, model misspecification, residual scale nhỏ hoặc pre-injection chưa hoàn toàn healthy. Kiểm này không chốt calibration hay tỷ lệ false positive toàn dataset. Projection trace/meta→metric của graph vẫn cần bằng chứng riêng; script này chỉ kiểm cutoff/call edges/raw arrays/scoring.
