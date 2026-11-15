# Hợp đồng đầu ra M1-FT → giao diện (T-064 ↔ T-065), bản 1 — 12/11/2026 21:20Z

Mục đích: T-065 dựng G-a/G-b/G-c ngay trên đầu ra P7 mà không phải làm lại khi T-064 có biến thể. Bản này do Claude (người làm T-064) khai; Codex (người làm T-065) có thể đề nghị bổ sung qua báo cáo, Claude ghi bản 2 nếu đổi.

## 1. Đầu ra gốc của một lần chạy

- Một lần chạy = một **bản** (`ban`) × một **ca** (mã mờ). Đầu ra gốc là `method-output-<lần>.json` cùng **lược đồ của P7** (`src/m1`, `method_version` `M1-T046-1`): `method`, `method_version`, `variant`, `config_id`, `mode`, `status`, `verdict`, `entity_ranking[] {entity, key, tie_group}`, `window`, `region`, `sets`, `coverage`, `diagnostics`, `extra` (gồm `extra.canh`, `extra.kenh_co`, `extra.don_vi_phan_vi`, `extra.tang_P`), `inherited_by`, `evidence_refs`, `why_ids`.
- M1-FT **giữ nguyên mọi khóa trên** (cùng ý nghĩa). Bản tắt mọi thay đổi phải trùng SHA với P7.
- M1-FT chỉ **thêm** khóa mới dưới `extra.m1_ft` (bản P7 không có khóa này):
  ```json
  "extra": { "m1_ft": {
      "ban": "<mã biến thể trong results/T-064/so-bien-the.jsonl>",
      "cau_hinh_sha256": "<sha256 file cấu hình>",
      "ma_nguon_sha256": "<sha256 cây src/m1_ft + src/m1 đã dùng>",
      "thanh_phan_bat": ["H6-...", "H8-..."],
      "nut": [ {"entity": "booking_db", "loai": "service|db|cache|broker|ha_tang|khac"} ],
      "canh_xep_hang": [ {"nguon": "...", "dich": "...", "loai": "goi|db|cache|message|...", "hang": 1, "tie_group": 0, "diem": 0.0, "nguon_xac_minh": "span_cha_con|server.address|db|span_link"} ],
      "chu_thich": { "<khóa thành phần>": "..." }
  } }
  ```
  Khóa nào chưa có thì vắng mặt (không ghi `null` giả). `canh_xep_hang` chỉ có ở biến thể H1.
- `verdict`, `entity_ranking`, `tie_group` có cùng nghĩa như P7. Giao diện **không** tự xếp lại hay chấm điểm.

## 2. Nơi đặt

- Repo: `results/T-064/bien-the/<ban>/<ca>/method-output-1.json` (và `-2` cho lần chạy lặp kiểm SHA). P7 trên 9 ca T-062: `results/T-062/ca/<ca>/outputs/<ca>/method-output-1.json` (nguồn hiện hành của bản 6).
- Trên `exp-obs` cho Infinity: T-065 tự quyết bố cục dưới `/opt/flash-ticket-obs/rca-ket-qua/<thư mục con mới>/`, nhưng phải có **chiều bản**: mỗi chỉ mục ca mang `ban` (P7 = `p7`), để G-c chọn P7 hoặc M1-FT cho cùng một ca. Phiên bản, `cau_hinh_sha256`, cửa sổ `[t−300, t+300)` hiển thị ở trang ca.

## 3. Chỉ mục bản

T-064 sẽ ghi `results/T-064/ban-xuat/chi-muc-ban.json`: danh sách `{ban, mo_ta, cau_hinh_sha256, ma_nguon_sha256, trang_thai: "thu|de_xuat|thay_the", cac_ca: [...]}`. Trước khi có, T-065 dùng một mục giả lập duy nhất `{ban: "p7", trang_thai: "khoa_P7"}` dựng từ đầu ra P7 hiện có (đánh dấu rõ là P7).

## 4. Không đổi

Không đưa đáp án/nhãn vào đầu ra phương pháp. Bản phát lại có đáp án vẫn tách như bản 6.
