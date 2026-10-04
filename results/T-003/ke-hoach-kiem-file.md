# Phạm vi kiểm đã thực hiện và giới hạn suy rộng

Q-47 đã duyệt bố trí hai máy, tải gói, bỏ OT, giao chọn ứng viên bảo toàn và gộp phản biện. Q-50 dùng GPT-6.1 Sol high cho các nhánh tiếp nhận. Các dòng chờ quyền trong checkpoint/SPEC gốc là lịch sử; bổ sung Q-47 của SPEC quy định phạm vi hiện hành. Không mở data/locked/, không chạy RCA/MyRCA, không chọn dataset thí nghiệm hoặc chia dev/test.

| Nhánh | File và cách chọn trước số đo | Mức kiểm thực | Giới hạn |
|---|---|---|---|
| Nezha OB/TT | Toàn 1.165 CSV construct/rca của bốn ngày tại revision ghim; không chọn ca theo biểu hiện | Toàn CSV/schema/clock/parent/log-ID/metric; census nhãn; graph theo từng root và hai cách hiểu clock; normal và khảo sát trace theo kênh | Một revision/bốn ngày; hai clock là giả thuyết, không tăng incident. Metric construct trùng fault không là clean normal; trace normal ngắn. |
| Eadro TT/SN | Hai ZIP record7615394, gồm mọi archive lồng; chọn toàn release đã trình | CRC/hash toàn member; 32 biểu diễn, 19 phiên raw duy nhất; parent strict và identity, metric/log, alias, graph và q theo ca/kênh | Nested trùng không là lặp mới. 117 nhãn tiêm không là nhãn onset/trace/vùng. Clock và alias còn giới hạn. |
| DeepTraLog TT | Toàn F01–F14, normal và đủ8part graph; thêm5part all-log khi normal lineage chưa đầy đủ | CRC/parse toàn phần duyệt, nhãn từng trace, edges E×2, raw↔graph↔log theo ID và từng label | Không thấy root service/injection/region gold. Log có ID không thay span gốc hoặc chứng minh thời gian/normal sạch. |
| LEMMA Product Review | Preprocessed metric/log ngày20211203, theo file đã trình từ metadata | Toàn member hai ZIP; CSV/NPY/PPTX, nhãn/entity/clock, KPI arithmetic và nối modality | Không đại diện Original, các ngày/root/fault khác. Root benchmark MongoDB khác nguyên nhân vận hành NFS; normal/mốc tiêm PR chưa xác minh. |
| LEMMA Cloud | Preprocessed metric/log ngày20240124, theo file đã trình từ metadata | Toàn member hai ZIP; CSV/NPY/PPTX, KPI arithmetic, root mapping và q theo timeline nguồn | Một scenario; trước lỗi không nhãn healthy từng điểm, JSON/PPTX khác clock, PCA không phủ đoạn lỗi. |
| Lượt2025–2026 | Sáu truy vấn theo giới hạn SPEC, hồ sơ nguồn chính thức/release cố định | 14 thẻ nguồn/metadata, bài/README/record/license/version và lineage | Không tải payload trong nhánh này; modality/nhãn công bố chưa thành chất lượng file, census thực còn OPEN. Không gọi không tải vì scope là không thể kiểm. |

[Thẻ và index](the-dataset-ngoai-rcaeval.md), [byte thực](dung-luong-tai-va-giai-nen.md), [nguồn toàn gói](source-manifest.json). LEMMA chỉ bốn ZIP IT, không tải toàn Original hoặc OT. Toàn member của mẫu không đồng nghĩa toàn dataset. Mở rộng cần chỉ rõ file/byte/quyền; không âm thầm giảm mức kiểm các file đã được duyệt.

## Giữ ngoài và phụ thuộc

Theo ủy quyền Minh, Codex chọn bảo toàn OpenRCA Bank cùng AIOps Bank chung lineage trước số đo; [lý do/phương án](bao-toan-openrca-bank.md), WHY-13. Chỉ nguồn/metadata/schema công bố; nhãn census thực chưa có trong scope. Không xem telemetry hoặc predictions Bank. Chất lượng, normal, parent, triệu chứng và độc lập injector/collector còn OPEN; chấp nhận rủi ro để còn phép đánh giá ngoài thiết kế. Chưa là lựa chọn thí nghiệm cuối G1. Các mẫu số đo đã đọc của các bộ khác không còn trạng thái chỉ metadata; không đổi tên hoặc chọn bản phái sinh cùng ca làm giữ ngoài độc lập.

LEMMA: exact license NC/ND còn khác nguồn. WHY-14 ghi trước tải rằng kiểm nội bộ phi thương mại nằm trong quyền hẹp chung của hai khai báo; không chia sẻ payload/adapted data hoặc chọn license thay tác giả. Thiếu license rõ của các bộ khác được ghi đúng trong thẻ; công khai không thay giấy phép. Không gửi yêu cầu tác giả trong task.

## Máy và dựng lại

- Laptop Nezha: D:/RCA-flashticket/data/ngoai-rcaeval/nezha/{online-boutique,train-ticket}/.
- Laptop Eadro: D:/RCA-flashticket/data/ngoai-rcaeval/eadro/{social-network,train-ticket}/.
- EC2 mới Deep: /home/ubuntu/rca-t003/data/deeptralog/; Lemma: /home/ubuntu/rca-t003/data/lemma/.
- Script/kết quả EC2: /home/ubuntu/rca-t003/{scripts,results}/; bản review trong results/T-010 và T-011.
- Metadata/nguồn trong results/T-008–T-012/runs/ theo manifest; không chuyển telemetry vào vùng metadata hoặc data/locked/.

Lệnh dựng lại và revision/hash chính xác ở [data README](../../data/README.md). Python sẵn có; LEMMA dùng môi trường kiểm riêng và static reader object NPY, không thực thi pickle. Không sửa môi trường RCA chung. Mỗi lượt dùng run-id mới; giữ lỗi/partial/interrupt. Không chạy lại acquisition/full scan chỉ để hoàn thiện bảng khi kết quả hợp lệ đã có.

## Thứ tự thực tế và tự kiểm

Thông tin chung → ghi bảo toàn/WHY → kiểm quyền hẹp LEMMA → tải/hash → CRC/schema → census/clock/parent/entity → khảo sát khi có tham chiếu đủ căn cứ → tự đối chiếu độc lập → tổng hợp. Nezha/Eadro và Deep/LEMMA làm song song khi không phụ thuộc. Nguồn2025–2026 và self-audit song song; root chịu trách nhiệm cuối, không dùng lời agent thay file.

Tự kiểm đã sửa lỗi thực: normal metric Nezha trùng fault, mask phút vượt normal trace, missing-reference sai đơn vị; Deep graph E×2 khác kỳ vọng2×E; LEMMA alias schema/encoding và tập entity NPY log lẫn metric. Lượt lỗi giữ nguyên, kết luận dùng lượt đúng chỉ rõ trong thẻ. [Tự phản biện](tu-phan-bien-doc-lap.md) ghi lỗi, phép kiểm và giới hạn; không biến triệu chứng thành ground truth vùng.

Claude phản biện gộp một REVIEW tại T-003. Minh quyết đóng task và lựa chọn G1; không tự commit/push, xóa dữ liệu hoặc Stop EC2.
