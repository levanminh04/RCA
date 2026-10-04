# Dữ liệu

Thư mục `data/` không đưa vào git, trừ file này. Mỗi bộ dữ liệu có trong đây phải có một mục bên dưới, đủ để dựng lại trên máy mới: nguồn, revision, cách lấy, kích thước, cách kiểm.

`data/locked/` chứa dữ liệu chưa ai nhìn, để dành cho tập test hoặc dataset giữ ngoài, và file chứa nhãn của chúng. Không đọc nội dung trước cổng G3 (AGENTS luật cứng 1). Tính hash để kiểm toàn vẹn thì được, vì không đọc nội dung.

## RCAEval — revision `afeacb11bcc94dadfd1c8f483ee4377b2b8b614e`

- **Nguồn:** Hugging Face `phamquiluan/RCAEval`, giấy phép MIT.
- **Cách có:** chép ngày 02/10/2026 từ lần tải trước (20–27/09/2026), theo Q-21.
  - Trước khi chép, từng file đã được so với hash SHA-256 mà Hugging Face công bố cho đúng revision trên: 287/287 file khớp, cộng `cases.parquet` khớp.
  - Sau khi chép, so lại bản chép với bản gốc: 287/287 giống hệt.
- **Còn thiếu:** file `inject_time.txt` của 89 ca, tổng 890 byte, chưa tải. Thời điểm tiêm lỗi vẫn có trong `cases.parquet`.

| Thư mục | Nội dung | Kích thước |
|---|---|---|
| `rcaeval/` | 30 ca RE2-TT từng làm tập dev ở v1; 5 ca mẫu: `re1ob_productcatalogservice_cpu_3`, `re2ob_productcatalogservice_loss_1`, `re2ss_orders_loss_2`, `re3ss_carts_f1_1`, `re3tt_ts-route-service_f2_1` | 642 MB |
| `locked/rcaeval-re2tt-60/` | 60 ca RE2-TT chưa ai nhìn từng ca (tập final của v1) | khoảng 1,3 GB |
| `locked/rcaeval-metadata/cases.parquet` | Mục lục 735 ca RCAEval, **có nhãn service gốc của mọi ca**, kể cả 60 ca bị khóa | 29 KB |

Mỗi ca có `metrics.parquet`, `traces.parquet`, `logs.parquet` (riêng một ca RE2-TT không có log). Vài ca mẫu có thêm `inject_time.txt`.

**Lưu ý:** mang dữ liệu về **không** có nghĩa là đã chọn RE2-TT làm dataset chính. Việc chọn dataset và cách chia dev/test là của P2, duyệt ở G1. Nếu G1 không dùng 60 ca bị khóa làm test thì chuyển chúng ra ngoài `locked/`.

**Lấy lại trên máy mới:** dùng `huggingface_hub.snapshot_download(repo_id="phamquiluan/RCAEval", repo_type="dataset", revision="afeacb11bcc94dadfd1c8f483ee4377b2b8b614e", allow_patterns=[...])`, với danh sách thư mục ca như bảng trên. Lệnh này chưa chạy thử trong repo này.

## T-003 — Nezha đã tải theo Q-47

- Laptop: `data/ngoai-rcaeval/nezha/online-boutique/` và `train-ticket/`, construct/rca đủ bốn ngày trong inventory; không phải tập test/Bank bảo toàn.
- Nguồn/revision/từngfile: `results/T-008/runs/download-plan-001/plan.json`; actualbytes/SHA256/Gitblob trong `results/T-008/runs/download-001/manifest.json`. Tổng1165file/3.038.134.642byte,0downloaderror. Khôngđưadata vàogit.
- Dựnglại: `py -3 -B results/T-003/scripts/download_verified.py --plan results/T-008/runs/download-plan-001/plan.json --data data/ngoai-rcaeval/nezha --results results/T-008/runs --run download-NEW --workers 6`. Run-id mới; giữ partial/lượt hỏng.
- Không coi tên construct_data đủ chứng minh mọi metric bình thường:122path trùngbyte với rca_data. Xem thẻT008 và fileaudit/evidence002. Không xóa source sau khảo sát nếu Minh chưa duyệt.

## T-003 — Eadro, DeepTraLog và LEMMA IT theo Q-47

Dữ liệu phục vụ kiểm thẻ, chưa phải lựa chọn dataset thí nghiệm. Chỉ giữ Bank ở mức thông tin chung theo WHY-13; không tải/đọc telemetry Bank, không mở data/locked/. OT (SWaT/WADI) bỏ khỏi phạm vi mới.

| Bộ | Nơi dữ liệu thực | Kế hoạch có URL/revision | Hash/byte thực |
|---|---|---|---|
| Eadro | laptop data/ngoai-rcaeval/eadro/{social-network,train-ticket}/ | results/T-009/runs/download-plan-001/plan.json | results/T-009/runs/download-001/manifest.json; Zenodo MD5 đã đối chiếu |
| DeepTraLog raw/normal/graph | EC2 /home/ubuntu/rca-t003/data/deeptralog/ | results/T-010/runs/download-plan-001/plan.json | results/T-010/runs/download-002/manifest.json; Git blob đối chiếu revision |
| DeepTraLog all-log conditional | cùng vùng Deep trên EC2 | results/T-010/runs/download-plan-alllog-001/plan.json | results/T-010/runs/download-003/manifest.json; Git blob khớp |
| LEMMA mẫu | EC2 /home/ubuntu/rca-t003/data/lemma/ | results/T-011/runs/download-plan-001/plan.json | results/T-011/runs/download-001/manifest.json; LFS SHA-256 kiểm độc lập ở results/T-003/runs/lemma-independent-hash-001/result.json |

EC2 mới: ubuntu@3.26.62.217, key2 riêng tại D:/RCA-ext/keys/key2.pem; không dùng instance T-007. Nội dung key không lưu repo. Script/kết quả remote trong /home/ubuntu/rca-t003/{scripts,results}/; bản review ở results/T-010 và T-011. CSV/ZIP nguồn còn giữ; kiểm streaming, không giải nén nguyên cây. Deep có ZIP ghép là bản trung gian, không phải file tải thứ hai. Không tự xóa hoặc Stop/terminate sau khảo sát.

Dựng lại Eadro trên laptop (run-id mới):

```powershell
py -3 -B results/T-009/scripts/download_archives.py --plan results/T-009/runs/download-plan-001/plan.json --data data/ngoai-rcaeval/eadro --results results/T-009/runs --run download-NEW --workers 2
```

Dựng lại Deep trên Linux sau chép script và đúng plan lên EC2 (mỗi lệnh run-id riêng, không đè):

```text
python3 /home/ubuntu/rca-t003/scripts/download_archives.py --plan /home/ubuntu/rca-t003/results/deep-plan.json --data /home/ubuntu/rca-t003/data/deeptralog --results /home/ubuntu/rca-t003/results --run deep-download-NEW --workers 3
```

`deep-plan.json` phải là bản nguyên trạng của plan base hoặc plan all-log trong bảng; ghi hash và copy provenance khi dựng. LEMMA dùng cùng CLI downloader chuẩn trong results/T-003/scripts/download_verified.py hoặc downloader lưu ở EC2, với --plan bản nguyên trạng results/T-011/runs/download-plan-001/plan.json, --data /home/ubuntu/rca-t003/data/lemma và run-id mới. Plan LEMMA byte/URL ghim revision; sau tải phải đối chiếu SHA-256 với lfs_sha256 của đúng path/dataset trong results/T-011/runs/run-001/inventory.csv. Không dùng SHA tự tính đơn lẻ thay xác minh nguồn. Lệnh dựng lại trên máy mới chưa chạy lần thứ hai; các acquisition thực đã chạy và manifest nêu trên là bằng chứng.

LEMMA chỉ Preprocessed metric/log PR20211203 và Cloud20240124; Original/các ngày khác metadata-only. Exact license NC/ND còn mâu thuẫn; kiểm nội bộ phi thương mại theo WHY-14, không chia sẻ payload/phái sinh hoặc coi có quyền thương mại. Giấy phép Eadro/Deep còn giới hạn đúng như thẻ; công khai không thay điều khoản dùng.

Tổng payload dataset cả gói5.477.786.503byte, gồm all-log213.216.632byte. Kích thước member logical, duplicate, thời gian và nhu cầu streaming ở results/T-003/dung-luong-tai-va-giai-nen.md và runs/resources-final-001/summary.json. Lượt lỗi/partial/interrupt được giữ. Script kiểm tái lập riêng nằm ở results/T-008–T-011/scripts/; dùng run-id mới, không chạy phương pháp RCA.


## T-003 — bổ sung sau REVIEW (04/10, Q-51)

Dùng khảo sát thẻ và nhãn/schema, chưa chạy RCA hoặc chọn datasetG1. Dữ liệu giữ lại, không tự xóa.

| Archive | Đường dẫn laptop | Nguồn/hash |
|---|---|---|
| AnoMod | data/ngoai-rcaeval/T-012/anomod/AnoMod.zip | results/T-012/runs/download-review-001/manifest.json |
| FSE reduced | data/ngoai-rcaeval/T-012/fse/FSE_26_RCA_dataset_study_reviewer.tar.gz | cùng manifest |
| TRCA đủ checksum | data/ngoai-rcaeval/T-012/trca/attempt-002/TRCA.zip | results/T-012/runs/download-review-002/manifest.json |
| TRCA bị thiếu byte, giữ lượt hỏng | data/ngoai-rcaeval/T-012/trca/TRCA.zip | download-review-001 statuserror, không dùng làm dataset |

Plan ghimURL/MD5/byte tại results/T-012/runs/review-sources-001/download-plan.json; TRCA dùng trca-retry-plan.json. Dựng lại ba archive bằng `py -3 -B results/T-009/scripts/download_archives.py --plan results/T-012/runs/review-sources-001/rebuild-plan.json --data data/ngoai-rcaeval/T-012 --results results/T-012/runs --run download-NEW --workers 3`. Dùngrun-id mới; khôngđè bản đanggiữ. Isolated Parquet reader: py -3 -m pip install --target data/ngoai-rcaeval/T-012/python-packages --no-deps pyarrow==23.0.1 tzdata==2025.2. Môi trường ignored, khôngcommit data.

Bank: không cófullZIP local; inventory/range label là results/T-012/runs/bank-metadata-001 và bank-label-reproduce-002, nhãn8.668byte. Replay fetch_bank_labels.py --run <mới>, đóng response nếu serverkhông206exactrange; khôngfallback fullZIP. Chỉ pinmutableDriveid/size/modified/directoryhash/labelhash, chưawholearchivehash. Chưa mởBankmeasurements/data/locked.

Tổng payload gói hiện6.106.198.114byte; transfercó lượt lỗi6.441.253.354byte, metadata/range/env giữriêng. Logical giải nén41.126.769.584byte tính representation, khôngđĩastream cần. [Snapshot](../results/T-003/runs/review-propagation-001/resources.json).
