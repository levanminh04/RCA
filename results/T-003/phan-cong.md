# Phân công và bàn giao T-003

Cập nhật 03/10/2026. Q-45 giao toàn gói; Q-47 cho kiểm Nezha/Eadro laptop, Deep/LEMMA EC2 mới và ủy quyền bảo toàn; Q-50 tiếp checkpoint với subagent GPT-6.1 Sol high. Người làm Codex, người phản biện Claude; subagent chỉ hỗ trợ người làm, không thay REVIEW độc lập. Lượt đầu Astra theoSPEC/Q48; lượt tiếp nhận hiện GPT-6.1 Sol high theoMinh.

| Nhánh | Phạm vi thực làm | Bằng chứng cuối | Giới hạn bàn giao |
|---|---|---|---|
| T-008 NezhaOB/TT | ToànCSVtải approved, labels/cells, parent/log/clock, graphroot, strictnormal, Duration3q/control | [Thẻ](../T-008/the-dataset.md); file-audit001/evidence002/symptoms003/trace-symptoms002/card-final002/units001/SQLindependent001 | Strictresource calibration0; trace windowngắn, clock haihypothesis, data licenseOPEN |
| T-009 EadroSN/TT | Toàn2ZIP+nested, deduphash/raw, parent2unit, metric/log, graphwhole-file, probe3q/control | [Thẻ](../T-009/the-dataset.md); inspect004summary/independent-summary | Paper/releasecountkhác, aliasSN/clock; chưa codefault/onset/region |
| T-010 DeepTT | Toàn14F/10normal/8graph/5all-log inventorytải, shape/labels/lineage/logcoverage | [Thẻ](../T-010/the-dataset.md); inspect005/006/007/008 | 28.116normalgraphID thiếu spanraw cólog; root/time/resource metric/permission/embeddingOPEN |
| T-011 LEMMAIT | Toànmember4ZIP Preprocessed2ngày; staticNPY/fullCSV/PPTX/mapping/KPI/Cloudbands | [Thẻ](../T-011/the-dataset.md); inspect008/validate001/003/kiem-file/cloud-bands | Original/ngày khácmetadata; PR46case chưa fullmatch; Cloudclock/logmetadata; NC/ND cuốiOPEN |
| T-012 nguồn2025–2026 | 6truyvấn/11hồsơ,14thẻ,34snapshots, lineage/task/license | [Thẻ](../T-012/the-dataset.md); final-check001/search-ledger/final-leads | Source-only, chưa censusarchive; Bank giữG3, độclập chưa đủ3trục |
| T-003 tổnghợp | Thẻ10mục,9tiêuchí,taskmatrix,tựphảnbiện; verification root | [Tổnghợp](the-dataset-ngoai-rcaeval.md), [tiêuchí](bang-tieu-chi.md), [task](task-cham-duoc.md), [tựkiểm](tu-phan-bien-nguon-va-giao-thuc.md) | Root ghim manifest/scopechecks/LOGparent/STATE/promptClaude; subagent khôngsửa shareddocs |

Đã kiểm telemetry theoQ47; không còn trạng thái “chưa quyền đọc” của checkpoint cũ. OPEN do phạmvi/nhãn/clock/provenance, khônglấpgiảđịnh. LEMMA Original/ngày khác khôngtrong4ZIP, T012 ba archive kiểm thật sau REVIEW, Bank chỉ metadata/nhãn; khônggọi toànrawmọiứngviên. OT bỏ phạmvi mới, historygiữ.

OpenRCA Bank/AIOps Bank bảo toàn WHY13/Q49 khôngthayG1. Khôngchọn dataset/split, mởlocked, RCA, commit/push. Claude REVIEW gộpT003 theoQ47, không REVIEW nhánh hay người làm tự REVIEW.

Root cần đối chiếu thẻ/run mới nhất trước manifest: nếu T009 córun sauinspect004, chỉ dùng số đã vào thẻ và được kiểm. T010/T011 sửa vẫn giữ bản cũ. Trạng thái chờphảnbiện/handoff do root cập nhật; không tựđóng task/G1.

