# V6 — Nhãn, cửa sổ và mode b: bằng chứng

T020 không chốt protocol. `window-parameters.csv` giữ giây, điểm, cadence, pre/post, lookback và trigger riêng. `label-budget.csv` tách fit-normal/regime, tune-dev và score-test. `runner-leakage.csv` là audit hồ sơ từng adapter, không tuyên bố b đã hợp lệ chỉ từ chữ ký hàm.

T013 L20 trên ôdelay FSE-OB hiện chỉ có360trước+361sau do giới hạn recording, khác ý định600+600. T014111điểm1s khác111điểm1min;10testpoints tại+291..+300khác+(-4)..+5phút của default. TORAI L10=300s mỗi phía;20logts points15s. GDN model5tick ở1s không bảo đảm5giá trị độc lập. Giữ đủ bình thường thống kê là OPEN, không dùng minimum để gọi calibrated.

`checks.csv` có phép tính từ CSV hoặc thành phần JSON gốc: {13: 10, 14: 11, 15: 97, 16: 24, 17: 5, 18: 9}. Số chọn bằng SHA256 seed20261004 trong pool đại lượng tính lại, mọi aggregate trọng yếu trong pool đều kiểm; không chọn theo kết quả. `numeric-sample-candidates.csv` chứa toàn pool kiểm lại của luồng này; nó không thay inventory tất cả lá số đầu vào của root. Pool156 không mismatch; root20 vàT0019 đềuPASS. Các kiểm mới giữ4counter diagnostic MicroRank mismatch trong checks-normalized.csv/mismatches.csv; xemHANDOFF. Không sửa task cũ.

Giới hạn runtime: `runtime.csv`47dòng timer gốc và dự phóng conditional theo dataset×seed; `runtime-ledger.csv` là executionledger hỗn hợp, không dùng thay methodcost. GDNtrainonce/system/seed + inferenceDataset, không nhân training theo sốincident. Q40 áp total dataset×seed, không10800s mỗi seed. Nếu runtime một seed gần ngân sách thì số seed khả thi cần tính bằng total, không nhân ngân sách theo seed. Dataset mới: adapter và runtime `chua_kiem`; không chạy mới T020.

Nhãn gốc/fault không được fit. Regime normal/fault dùng mốc nhãn ởmodea; GDN lấy normal của dev bằng mốc tiêm cũng là labelbudget thật. Chế độb phải xử lý marker,crop,future-normalization và candidate selection trước đo. Testlabels không chọn threshold/checkpoint; root/path/SLI không truyền vào phương pháp. Đồ thị PC học incident data trongmodea không tự là ròroot nhưng khác normal-only topology. Biên file-centered injection vẫn là đường lộ trongmodeb.
