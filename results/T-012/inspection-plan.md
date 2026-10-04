# Phạm vi kiểm T-012 sau Q-47

Bản kế hoạch nguồn trước REVIEW giữ trong LOG/runs. Theo Q-51 và SPEC bổ sung, đã tải toàn ba archive628.411.611byte, không lấy một ca mẫu đại diện. [Downloadplan](runs/review-sources-001/download-plan.json), [AnoModfull](runs/anomod-file-inspect-003/validation.json), [AnoModfollowup](runs/anomod-followup-002/validation.json), [FSEfull](runs/fse-file-inspect-003/validation.json), [TRCAfullCRC](runs/trca-inventory-001/validation.json), [TRCAreuse](runs/trca-reuse-001/result.json).

Bank: chỉDriveinventory/centraldirectory và inflate record.csv bằngexactrange; [census](runs/bank-label-reproduce-002/census.json). KhôngfullZIPtelemetry. TrainTicketTrace26,9GB/LO2large vẫnscope nguồn; giới hạn budget/scope, không gọi không thể kiểm. OpenRCA2 không publicarchive ghim trong nguồn đãđọc; chủnguồn release quyết dữ kiện còn thiếu.

Tái lập: inspect_review_archives.py --kind fse/anomod/inventory --archive <path> --run <mới>; inspect_anomod_followup.py --run <mới>; fetch_bank_labels.py --run <mới>. inspect_trca_reuse.py --run <mới>. Reuse1165byte-identicalCSV dùng lại semanticT008 thayđọc lặp; kiểmgraph/parent/normal/clock/probe đúnglineage. Bản cards hiện dùng write_review_cards.py --run <mới> --baseline runs/cards-review-002/previous-card-set.md; build_metadata_cards.py làcheckpoint nguồn cũ, không ghiđè thẻ hiện tại.
