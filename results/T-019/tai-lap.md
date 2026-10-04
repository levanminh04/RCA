# Tái lập T-019

Đứng tại `D:/RCA-flashticket`. Không dùng EC2, không cài gói mới, không chạy runner/RCA/detector. `.venv` có Python3.12.10, pandas3.0.6, numpy2.5.3, pyarrow25.0.1; phiên kiểm này dùng môi trường có sẵn. Nhánh lineage dùng envpy312: Python3.12.10/pandas3.0.6/numpy1.26.4/pyarrow25.0.1. Hai môi trường chỉ đọc, không cập nhật.

## Census và dựng cache SS

Metadata của T002 được hash/ghép ba trang trước khi dùng. Lệnh plan tạo census/inventory; nếu cần giữ một lượt plan cũ thì sao lưu nó trong vùng T019 trước khi chạy. Không mặc định metadata HEAD thay revision ghim.

```powershell
py -3 -X utf8 -B results/T-019/acquire.py plan
# Ghi source/revision/byte của download-plan.json vào LOG trước khi tải theo quyền task.
py -3 -X utf8 -B results/T-019/acquire.py acquire --run acquisition-replay-001
```

Tên `--run` phải mới. Script giữ manifest/progress của lượt cũ, dùng lại từng cache file `data/T-019/` hoặc mẫu `data/rcaeval/` chỉ sau hash. Nếu cache không có: SS tối đa149.245.189byte. Không lấy dữ liệu từ data/locked/repo lưu trữ. Nguồn/revision từng file trong download-plan.json; kiểm LFS-SHA256 hoặc Git-blob-SHA1 theo định dạng nguồn. Cache SS file không thay nội dung khi hash khớp.

## Kiểm file và khảo sát mô tả

```powershell
.venv/Scripts/python.exe -X utf8 -B results/T-019/inspect_files.py --run inspection-replay-001
```

Tên lượt mới; đọc từng ca, progress mỗi25ca. Parent/linkage N/A vì metadata và file SS không có trace. Probe là khảo sát dải mô tả bằng mốc tiêm, không detector. So kết quả lượt mới với `inspection/` đã bàn giao; không chép đè lượt cũ. Script hiện đã tách metric hằng khỏi all-null; phiên inspection gốc dùng số gộp, đã được bổ sung đọc metric nhẹ bởi finalize_evidence.py và lưu số gộp cũ, số mới trong quality-refinement.json. Snapshot script reader lúc chạy gốc ở `inspection-001-failed/script-after-bool-fix.py`; hash execution ở inspection/manifest.json. Snapshot lưu sau sửa bool là code của lượt thành công, không phải code bị lỗi serialization.

Rà cuối cũng loại entity không có tỷ lệ xác định ở một trong control/post khỏi phép so cặp. Channel/entity rates gốc giữ nguyên; `inspection-summary-001-before-paired/` giữ tổng hợp trước sửa và failed-final-checks. Script reader hiện cùng quy tắc paired với thẻ cuối; nhánh postprocessor lưu `paired-entity-exclusions.csv`. Nhóm error RE2 có62ca hợp lệ, không phải67ca chỉ có schema/kênh. Thiếu28ca được ghi theo84bộ(ca,q), gồm vắng kênh và mất toàn số đo ở cửa sổ. Không biến missing thành tỷ lệ0.

Các bước lắp sổ/thẻ từ output đã bàn giao:

```powershell
.venv/Scripts/python.exe -X utf8 -B results/T-019/finalize_evidence.py
.venv/Scripts/python.exe -X utf8 -B results/T-019/build_card.py
.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py
```

Các lệnh này cập nhật output cuối của T019; chỉ người làm được ghi. Reviewer muốn chỉ đọc dùng verify_final.py `--read-only`. Việc chạy file gốc runner-source/main.py bị cấm trong task; source này chỉ để kiểm đường SLI.

## Lineage và source

Lệnh và lịch sử hai lượt compare có trong `lineage/report.md`. Trước tải14.215.893byte OB phải ghi plan. `lineage/outside-files.csv` đủ180path ngoài repo; toàn source local trước/sau1695file+6archive đã kiểm giữ hash. Lượt hiện tại đủ evidence, không cần chạy lại phương pháp để chứng minh exposure. Source audit652.287byte và runner-source26.309byte ghim riêng; scripts/manifests tại `sources-audit/` và `runner-source/`. Script source còn một số endpoint HEAD để khám phá metadata; kiểm revision trong manifest trước so, không biến HEAD mới thành nguồn cùng revision.

## Lượt hỏng được giữ

`inspection-001-failed/`: progress đủ245ca, cases/schema valid trước lỗi serialize numpy.bool ở nhãn; code snapshot sau sửa bool. Không dùng nó thay bảng probe. Lỗi in cp1252 của state_row.py xảy ra sau khi byte STATE đã sửa và verify; state-start.json chứng minh chỉ dòngT019 đổi. Lệnh reader hiện dùng `-X utf8` để đọc/in UTF8 ổn định. Hai lỗi khám phá read-only của nhánh lineage được ghi trong report; không cài hoặc sửa môi trường.
