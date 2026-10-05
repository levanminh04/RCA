# Bàn giao factual method evidence T020

Không thêm/sửa quyết định, không chọn dataset/phương pháp/protocol. T013 dùng bản đã duyệt R1/N1–3; WHY19/20/Q57 giữ đúng phạm vi candidate của gói. Mọi đầu ra nằm trong method_evidence. Không sửa task cũ/src/data/env, không EC2. Filedownload mới0byte; chỉ đọc primary TORAIv1 HTML qua webtool, không tải binary/dataset hoặc lưufile từweb; transferbytes củawebtool khônginstrumented.

## Bộ ghép

- `07-checklist-doc-nhanh.md`:42đoạn riêng variant/detector, mỗi đoạn<350từ; `method-checklist.csv` giữ inputs/unit/graphrole/cơ chế/default/source/assumption/tính tay/ledger.
- `yeu-cau-hop-nhat.csv`:42hàng từ sáu bảng nguyên16columns +provenance; `header-audit.csv` 0mismatch; mọi chua_kiem giữ nguyên.
- `05-evidence.md`, `label-budget.csv`, `window-parameters.csv`, `runner-leakage.csv`:marker,regime,tuning,normal budget,giây/points/cadence/lookback. Adapter dataset mới chưa kiểm.
- `runtime.csv`:47bản ghi timer thật và dự phóng conditional dataset×seed Q40. GDN chi phí=nseeds*(trainonce/system/seed+inferenceDataset), không nhân train×90ca. `runtime-ledger.csv` chỉ là tổng execution hỗn hợp, không dùng thay chi phí phương pháp.
- `checks-normalized.csv`:gốc/key/query/recompute/match; gồm pool156, root20, T0019, GDN11 và source mismatch4counter/8graphcounts. `checks.csv` là pool156 riêng, không đại diện mọi phép mới.
- `T001-checks.csv`:9đại lượng checked từAST/code và table count. `selected-root-checks.csv`:20lá số khóa riêng củaroot,20PASS. `mismatches.csv` giữ4counter differences.
- `deep-source-audit.md`, `runs/deep-source-audit.json`:18source checks và3revisioncheckPASS; code/paper khác biệt gốc/sửa giữ riêng.
- `independent-script-inventory.csv`:151script nguyên bản đọc toàn source/AST/import/write-site/hash. Text match không tự là numerical runner.12source standalone đã chép/chạy; đúng lý do các script không chạy ở từng hàng.
- `ca-da-chay.csv`, `runs/all-replays.json`:16attempts,12exit0,4retainedfailures; không gọi tất cảexit0 làmethod quality PASS. Tổng subprocess wall78.406s, từng lượt<5phút; gitstatus trước/sau16attempts giống nhau; guard toàn tiến trình cấm ghi ngoài folder này, -B.

## Kiểm độc lập đã chạy

T13 mean/variance/max/candidate/window25DELAY×4 và endpoint/ranks khớp. CIRCA savedarrays272nodes/2176RHT-DA comparisonsPASS; raw→snapshot1088arrays vàparentsPASS; savedgraph6DAGmatch,24cyclic nằm ngoài DAG proof. MicroRank fixture24PASS và root5numeric mathPASS. TORAI full gốc/sửa cùng S12TX2case/window/seed:severity,14BIC,cluster,bins,CI,p-values,fallback,ranks khớp; p-value sai số≤1e-9relative theo SPEC. T17 selftest, normalized tính độc lập và2226comparisonsPASS. T18 NumPy fixedcheckpoint:0ô vượt dung sai, argmax/báođộngkhác0;7run19holdout algebra đã tính lại từ savedarrays. Không đo runtime phương pháp mới; elapsed của scripts là chi phí kiểm.

## Mismatch MicroRank phải giữ đúng nghĩa

Snapshot `results/T-015/runs/tt-local/auth/example.json` có normalaudit missing_parent1326/root0 và anomalyaudit1403/root0. Independent current source `results/T-015/scripts/independent_inputs.py:45–48` dùng unresolved AND nonroot để đếm missing và nhận `<NA>` là explicitroot:0/1326 và0/1403. Archived `runs/source-versions/graph-before-null-audit-fix.py:26` không nhận `<NA>`; current `src/microrank/graph.py:32` có nhận. Mismatch phù hợp khác định nghĩa/phiên bản chẩn đoán null; không tự gán bug xếp hạng hay đổi trạng thái T015.

17/19đối chiếu current input replay khớp:count/SLO/operationidentity, toàn4graphrelations mỗi nhóm,tracecounts đều bằng snapshot. Hai boolauditcomparisonFAIL, cụ thể4counter trongmismatches.csv. `src/microrank/__init__.py:74–90` truyền graph vào PageRank và chỉ lưu audit; graph của đúng ca này đã xác nhận bằng nhau. Không có thêm lượt ranker để tuyên bố benchmark mọi ca hoặc thứ hạng mọi dataset bất biến.

## Các phép không chạy và phạm vi

T13 wholemechanism script trộn independent algebra với code tác giả/detectors và writes task cũ; component/window proof được chạy bằng bản chép độc lập, khôngrerunwhole. T15reference90OBaudit mongtask/data không có local; không EC2/download. T18B3 là data preparation30rawcases×feature/train variants, không standalone numeric inference proof; dùng existing normalized input vàcheckpoint. Script docs/assembly/inventory/EC2/sourcebuilder khác không là calculationrunner; reasons vàactual write sites giữ tronginventory. Không tái học PCdefault/đo method/detector mới hoặc kiểm thích hợpdataset mới. Chưa có normalbudget/calibration chung; PCcyclic proof vàdataset adapter remains chua_kiem.

## Bảo toàn đầu vào

Freeze5772entry:5771hashkhớp, duy nhấtdocs/STATE.md khác do checkpoint luồngroot (reported, không ghi bởi agent này). Toàn old task evidence frozen khớp; manifest/filehash output ở`output-manifest.json`. Giữ originalfailedsourceassert và mechanical attempts; không quy lỗi verifier thành lỗi phương pháp.
