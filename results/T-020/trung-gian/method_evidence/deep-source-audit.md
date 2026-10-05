# Kiểm sâu bài/code: MicroRank và TORAI

Khóa chọn theo seed ở LOG T020 trước đọc giá trị: MicroRank T015 (Codex), TORAI T016 (Claude). Không lựa chọn protocol. Revision code/hashes/AST từng hàm và file:dòng thật nằm trong `runs/deep-source-audit.json`.

## MicroRank

Đã đối chiếu toàn phần công thức trong PDF text T015 với nguồn pinned MicroRank, AST bản tách trong src/microrank/official.py giữ nguyên. Code PageRank: d=.85,alpha=.01,25vòng; mỗi phía normalize max. Prior bất thường dùng nghịch đảo biểu thức hỗn hợp, khác công thức7bài là hỗn hợp cộng nghịch đảo chuẩn hóa; prior code không tổng1. Spectrum Dstar2=ef²/(ep+nf), absent branch1e-7 và top_max+6 không đổi. Gốc handling-time trừ tổng con trực tiếp, không union thời gian con song song. Detector alarmµ+1.5σ/>8trace, partitionµ+σ+50ms; REspanµ+3σ là bản khác. Các file gốc pagerank.py:139,172; online_rca.py:53,84,149; preprocess_data.py:177–225. Nguồn paper: `results/T-015/sources/microrank-paper.txt` và profile §2/§5. Bản adapter T015 chưa là đầy đủ gốc nếu thiếu kind/instance/root.

Đã chép script tính độc lập sang T020 và thêm guard inputfixture/outputpath. `runs/microrank-fixture-001/summary.json`:24so sánh đúng, sai số0. Fixture không mở telemetry; không xác nhận mọi graph/partition của dataset chỉ bằng số học.

## TORAI

[Bài TORAI v1](https://arxiv.org/html/2604.13522v1) §3.2–3.6 dùng severity, GMM/BIC, nhân quả trong cụm và FineGrainer. Code RCAEval ghim `259ea41` severity có4nguồn (trace táchlat/error), chuẩn hóa theo tổng, GMM gán cứng. Hàm trong cụm không dùng trace và fallback severity nếu sốservice RCD không đủ. FineGrainer không có. Đây là khác biệt bài/code, không sửa tiếp ở T020.

Code gốc torai.py:29và81stride15hai lần, nên metric bước nhân quả cócadence225s;47–48concatindex. Bản sửa src/torai/torai_sua.py bỏ lần hai và ghép vị trí; parent-root sẽ tự kiểm hai thay đổi. Không đồng nhất bản sửa với toàn TORAI bài. Default GMM fullcov,max_iter50,randomstate0;γ5,bins5,localizedTrue; rcd alpha.01/.001,bước.1 tới<1. Seed RE không khóa. Chốt áp dụng/WHY và P3 thuộc nguồn quyết định hiện hành, luồng này không đổi trạng thái.

`runs/torai-arithmetic-001.json` kiểm normalization/grouping56components mỗi bản. Sau đó `runs/torai-full-goc-001.json` và `torai-full-sua-001.json` đã chạy full independent S12 bằng bản chép, tách riêng hàm input của harness qua AST; không import TORAI/RCD/RCAEval/causal-learn. Đúng TX2checkoutservice_cpu/1,L10,seed0; fitGaussianMixture thư viện đúng default và tự tính BIC, độc lập Kmeans/chi-square/PCphases. Severity/14BIC/cluster labels/bins/CI/fallback/finalranks khớp original; phép đầu chỉ normalization không được dùng thay fullproof. Có guard output và gitstatus16attempts trongall-replays.json.

MicroRank fixture24checksPASS; additional raw-input replay17/19PASS và2auditboolFAIL do null-root diagnostic definition. Giữ4counter old→new trongmismatches.csv vàgraphrelations equality; xem HANDOFF, không tự đổi trạng thái T015.

## Nguồn đính chính V9 đã kiểm trực tiếp

BARO DataFrame: baro/root_cause_analysis.py:313–314 và RCAEval/e2e/baro.py:50–51 `max(zscores)` có dấu. Dict BR:229–230 `abs(max(post)-median)`. Counterexample giảm trong T013 edge-falling-ranks.json cóa_cpu=-2.6,b_cpu=1.0. Không viết mọi bảnBARO làmaxabs.

CIRCA DA: circa/alg/ci/__init__.py:144,150 xử lý evidencecon theoθ; Model ởcirca/alg/common.py:225 xếp toàn scores. Không cutoff3output và không detector cấp hệ thống. Paper§4.3/codedifferent giữ riêng; pending K1 là correction mô tả.

MicroRank self-time/default và TORAI double-stride/fallback có source AST/needle assertions ởJSON, không chỉ sao prose. Không sửa docs chung, taskcũ, src, dataset hay môi trường.
