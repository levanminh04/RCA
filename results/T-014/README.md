# T-014 — CIRCA PC và kiến trúc

Đọc hai hồ sơ: [CIRCA-PC](ho-so-circa-pc.md) và [CIRCA kiến trúc](ho-so-circa-kien-truc.md). Mỗi hồ sơ giải thích từ đầu vào tới điểm xếp hạng, có ví dụ kiểm độc lập và điều kiện áp dụng. Scorer tham chiếu chung là linearRHT; RHT+DA được kiểm riêng. Đây là lựa chọn cho hồ sơ P1, chờWHY, chưa chốtP3.

Các file bàn giao:

- [Yêu cầu đầu vào](yeu-cau-dau-vao.csv), [ca đã chạy](ca-da-chay.csv), [môi trường](moi-truong.md).
- [Kiểm và đối chiếu SPEC](kiem-tra-va-doi-chieu-spec.md), [đính chính task cũ](dinh-chinh-task-cu.md), [nháp tài liệu chung](de-xuat-tai-lieu-chung.md).
- [Ví dụ PC](paper/vi-du-pc.md), [ví dụ kiến trúc](paper/vi-du-kien-truc.md), [DA và thứ tự SCC](paper/crossseed-pc.md), [đối chứng trước mốc](paper/normal-pretrace-verification.md).
- [Bộ dựng/scorer](../../src/circa_kien_truc/README.md), [toàn bộ file đã tạo](manifest-files.csv), [chi phí](runs/chi-phi-tong.json), [nguồn tải](download-sources.csv).

Graph canonical seed0 ở graphs/; lượt đầu thiếuhashseed giữ riêng. Runs/ giữ mọi lượt hỏng, timeout, tiếnđộ và intermediate snapshots. Audit/ giữ điều tra cũ và phép so backend/scorer; paper/ giữ nguồn và script độc lập. Manifest ghi cả file ngoài repo và EC2; đó là phạm vi đầu ra, không dùng gitdiff để thu hẹp review.

PC mặc định đã chạy xong ở273biến. Normalcontrol chưa đạt: không coi ranking bình thường là root có nghĩa. Chênh số công bố còn phần giao thức chưa phân xử; không chọn biến thể từ accuracy và không gọi toàn task đã tái lập sốpaper.


Kiểm tiếp theo chỉ dẫn Minh: [bổ sungEC2₂](bo-sung-ec2.md). Đây là trạng thái hiện hành của permutation/fullnormalPC; cáclogquaymáy cũ đượcgiữ.
