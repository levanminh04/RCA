# Sổ tìm nguồn 2025–2026 — lượt nguồn đã kết thúc

Đây là phần bàn giao của lượt tìm có giới hạn, chưa phải kết luận chọn dataset. Ngày truy cập: 03/10/2026. K3 là đầu mối; chỉ nguồn chính thức được dùng để xác minh. Chưa tải archive dữ liệu và chưa đọc số đo.

## Phạm vi và tiến độ

Giới hạn trong SPEC: sáu truy vấn, tối đa 12 hồ sơ chính thức và 90 phút tìm nguồn. Đã dùng đủ sáu truy vấn dưới đây, không tìm thêm. Có 11 hồ sơ: bảy đầu mối đầu, LO2v2 và ba đầu mối K3 đọc cuối. Biến thể hệ, revision và snapshot không đếm thành dataset mới. Thời gian từng thao tác web trước checkpoint chưa được lưu thành phép đo; không báo đã tuân thủ giới hạn thời gian bằng một số tự nhớ. Chi phí bước lấy nguồn được lưu riêng trong manifest.

| Mã | Truy vấn đã dùng |
|---|---|
| S1 | microservice root cause analysis dataset benchmark 2025 2026 public traces metrics logs |
| S2 | "TrainTicketTrace" dataset 2026 |
| S3 | "AnoMod" dataset 2026 |
| S4 | "Check Your Trace First" dataset |
| S5 | "2607.13548" OR "2602.09937" microservice dataset root cause |
| S6 | microservice RCA dataset 2025 2026 "FAMOS" "OpenRCA" benchmark public |

Không tìm thêm sau khi ngữ cảnh bị nén. Bước lưu nguồn ở checkpoint chỉ bảo toàn các đầu mối đã đọc, không mở lượt khảo sát mới. Không gọi lượt tìm này là khảo sát đầy đủ mọi dataset công bố trong hai năm.

## Hồ sơ cần tiếp nhận

| Đầu mối | Nguồn chính thức đã nhận diện | Trạng thái và việc còn thiếu |
|---|---|---|
| FSE fault-propagation-aware benchmark | [Bài v2](https://arxiv.org/html/2510.04711v2), [artifact Zenodo](https://zenodo.org/records/19513398) | Bài và bản phát hành có phạm vi khác nhau. Cần đối chiếu artifact rút gọn với benchmark toàn bộ và khóa bản mới hơn nếu có. Không lấy số ca toàn bài làm số ca trong archive. |
| AnoMod | [Bài v1](https://arxiv.org/html/2601.22881v1), [repo](https://github.com/EvoTestOps/AnoMod), [Zenodo](https://zenodo.org/records/18342898) | Trang record không đọc được qua công cụ web ở lượt này. Cần metadata API, revision, giấy phép, schema và nhãn thật. |
| TrainTicketTrace | [Zenodo](https://zenodo.org/records/17811972) | Đã mở record, chưa khóa bài báo tương ứng. Cần phân biệt archive mang tên lỗi với nhãn từng trace/root/time. |
| Check Your Trace First | [Zenodo](https://zenodo.org/records/19335897) | Trang record không đọc được qua công cụ web ở lượt này. Cần metadata API và provenance để xác định đây có phải dataset mới hay bản dùng lại dữ liệu. |
| OpenRCA | [Repo](https://github.com/microsoft/OpenRCA), [bài tác giả](https://netman.aiops.org/wp-content/uploads/2025/05/13411_OpenRCA_Can_Large_Langua.pdf) | Repo đã mở. Cần khóa revision, phân biệt Telecom/Bank/Market và quan hệ với AIOps Challenge. Chưa tải liên kết dữ liệu ngoài repo. |
| OpenRCA 2.0 | [Bài v2](https://arxiv.org/html/2606.27154v2) | Bài đã mở. Cần đối chiếu release chính thức, nguồn dữ liệu gốc và quan hệ với FSE/RCABench/OpenRCA. Không tự coi là bộ độc lập. |
| LO2 | [Bài v1](https://arxiv.org/html/2504.12067v1), [record đã nhận diện](https://zenodo.org/records/14938118) | Cần kiểm record/version mới hơn và phân biệt sample với kho toàn bộ. Chưa kiểm trace có trong release hay chỉ trong mô tả thu thập. |

## Đối chiếu các đầu mối cuối

K3 còn dẫn `arXiv 2607.13548`, `arXiv 2602.09937` và FAMOS `Zenodo 13120167`. Đã lưu ba nguồn chính thức ở run-003: hai bài dùng OpenRCA nên không tạo họ dataset mới; record FAMOS TT công bố 29/07/2024 nên giữ đầu mối ngoài cửa sổ 2025–2026, không tự kéo raw hoặc hệ Mall vào gói. Xem [đối chiếu đầu mối cuối](final-leads.md). Năm công bố bài không tự làm dữ liệu cũ thành dữ liệu mới. RCAEval thuộc T-002; kết quả trùng không đếm thành bộ độc lập mới. Các kết quả tìm trung gian không phải primary source chỉ dùng chỉ đường, không dùng làm bằng chứng thẻ.

## Cách tiếp nhận

Đã có 14 thẻ đủ 10 mục từ run-001/run-002, lineage và bảng task; kiểm độc lập ở `runs/final-check-001/verification.json`. Census nhãn archive và schema số đo vẫn OPEN: record chỉ phát hành gói nén; repo OpenRCA ghim không chứa `record.csv`/`query.csv` thực. Bank bảo toàn tới G3. Không dùng nhãn công bố thay census hoặc nói đã kiểm chất lượng dataset. Lượt nguồn kết thúc; không tìm tiếp sau S6.

