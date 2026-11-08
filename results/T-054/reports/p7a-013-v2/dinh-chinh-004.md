# Đính chính 004 — báo cáo P7(a) main013-v2 (R10: vì sao C-d3 OB kém M1 ở 4 ca)

Ngày 08/11/2026. Claude, người làm phần chạy/chấm/báo cáo T-054. Phản biện R10 của Codex (chat, do Minh chuyển). Minh cho phép ghi khi không còn mâu thuẫn với Codex.
Không ghi đè `bao-cao.md`, `dinh-chinh-001.md` … `dinh-chinh-003.md`. Không chạy phương pháp, không đọc thêm dữ liệu test thô. Chỉ đọc đầu ra đã lưu và nhãn đã ghép sau seal (dùng để chấm, như Đ12).

## Đ13 — Thay câu "chưa lần" ở Đ12 (đính chính 003)

Thay câu "Vì sao C-d3 trượt ở 4 ca chưa lần (chưa đọc khối C-d3 từng ca)." bằng nội dung dưới đây.

**Quy tắc chọn ứng viên** (`src/m1/doi_chung.py:105–120`):
- Đồ thị `H` chỉ gồm thực thể có điểm bất thường (`diem`). Cạnh đảo chiều: bên được gọi → bên gọi.
- Ứng viên là nút có bậc vào 0 trong `H`, tức không gọi bên nào có điểm bất thường.
- Ứng viên chỉ có điểm khi đi qua ít nhất một cạnh tới đích. Nút trùng đích mà không có đường tới đích khác thì không có điểm.
- Cả hai điều khớp code PetShop ở revision được dẫn (`code/baseline_anomaly_traversal.py`, commit `2e96f937`): ứng viên là nút bất thường không có predecessor bất thường trong đồ thị đảo; điểm chỉ tính trên `nx.all_simple_paths(ứng viên, đích)`, rỗng khi ứng viên trùng đích, nên ứng viên đó không có trong kết quả. Không phải lỗi wrapper.

**Quan sát từng ca** (nguồn: `runs/sua-cd3-ob-001/cd3-test-phi-nhan.json#/cases/<ca>/moi/cd3`; `extra.canh`, `extra.dau_vao_cd3.diem` của `result.json` M1 theo `phan-tich-nhom.json#/trung_gian_theo_ca/Nezha-OB|<ca>/M1/result`; root từ `phan-tich-nhom.json#/cases/Nezha-OB/<ca>/root`):

| Ca | Root | Root có điểm | Root là ứng viên | Bên được gọi của root có điểm | RR C-d3 / M1 |
|---|---|---|---|---|---|
| `4dbcb97712` | frontend | có | không | productcatalogservice | 0 / 0,5 |
| `739318ce25` | recommendationservice | có | không | productcatalogservice | 0 / 1 |
| `88dc4b2c47` | frontend | có | không | checkoutservice, recommendationservice, shippingservice | 0 / 0,25 |
| `f92f6a18c4` | recommendationservice | có | không | productcatalogservice | 0 / 1 |

- Ở 6 ca OK còn lại, root có điểm, là ứng viên, và không có bên được gọi có điểm. 5 ca RR 1; `fd2c49f3cc` RR 0,25 (root là ứng viên nhưng xếp thứ tư).
- Đích của cả 10 ca là `frontend`.

**Suy luận (xác định bằng code, không cần giả định thêm):**
- Ở cả 4 ca, root mất tư cách ứng viên trước bước cộng điểm đường đi, vì root gọi ít nhất một bên có điểm bất thường. Đây là lý do đủ cho RR 0.
- Hai ca root `frontend` có thêm một lý do đủ, độc lập: root trùng đích. `frontend` không có bên gọi trong `canh` của hai ca này (đã đếm: 0 bên gọi), nên không có đường qua cạnh tới đích. Dù không bên được gọi nào có cờ, `frontend` vẫn không có điểm. Hệ quả chung: với đích `frontend`, C-d3 không thể xếp đúng ca có root `frontend`. Trong 34 ca OB test có 6 ca root `frontend` (2 OK, 4 NO_TARGET; đếm từ `cd3-test-cham.json` ghép root ở `phan-tich-nhom.json`).

**Chưa biết:** vì sao các bên được gọi ở bảng trên có điểm bất thường. Dữ liệu đã lưu không phân xử được đó là lan truyền thật (ví dụ trễ quay ngược qua cạnh gọi) hay bất thường không liên quan. Không quy về một trong hai.

## Trạng thái

- A4, bảng chính và số C-d3 OB ở Đ12 không đổi. Không chạy lại phương pháp.
- C-d3 OB vẫn là sửa sau khi đã xem test (C-15 B), mức mô tả.

## Đ14 — Thay mục "Trạng thái" của đính chính 003 (N9)

Minh duyệt sửa N9 (08/11/2026). Thay hai dòng cuối của mục "Trạng thái" ở `dinh-chinh-003.md` bằng:

- `src/m1/adapter.py` vẫn còn lỗi; chỉ sửa khi có lượt chạy Nezha-OB mới, kèm ghim lại pin (DECISIONS, mục "mốc sửa adapter Nezha"; WHY-79 cập nhật).
- TORAI A tạm hoãn vô thời hạn: 6/180 slot VERIFIED, 174 BLOCKED (DECISIONS; `runs/torai-a-v3-001/HOAN-TORAI-A.md`).

## Đ15 — Vì sao bên được gọi có cờ (thay đoạn "Chưa biết" ở Đ13; Minh duyệt 08/11/2026)

Câu này nói về **lớp phát hiện bất thường của M1**. `diem` mà C-d3 dùng là điểm kênh M1, thế giới P (`src/m1/chuoi.py:615`). M1 và C-d3 dùng cùng cờ. Khác ở bước sau: C-d3 loại root khi root gọi bên có cờ; M1 không loại, nên M1 vẫn xếp root đứng đầu ở `739318ce25`, `f92f6a18c4`.

**Cách đọc** (`runs/sua-cd3-ob-001/r10_kenh.py` → `r10-kenh.txt`): mỗi ca, liệt kê kênh có cờ `F_I=1` (`extra.kenh_co`) của root và của bên được gọi có điểm; khởi phát sớm nhất; số kênh cạnh đi từ root.

**Quan sát:**
- `739318ce25`, `f92f6a18c4` (recommendationservice, cpu_contention): productcatalogservice có cờ trên cạnh `recommendationservice → productcatalogservice`, khởi phát cùng giây với root.
- `88dc4b2c47` (frontend, exception): recommendationservice có cờ trên cạnh `frontend → recommendationservice`; checkoutservice có cờ một kênh operation; shippingservice có điểm nhưng không kênh nào `F_I=1`.
- `4dbcb97712` (frontend, exception): productcatalogservice có cờ một kênh operation; root không có thời điểm khởi phát (chỉ kênh metric).

**Suy luận:** ở 3/4 ca, ít nhất một cờ của bên được gọi nằm trên cạnh do chính root gọi. E2-C gán cờ cạnh cho bên nhận (`src/m1/e2.py:38–41`). Khi root chậm (CPU bị tranh chấp), thời gian cuộc gọi đo ở phía root tăng và cờ rơi vào bên được gọi. Đây là cơ chế gán, không cần bên được gọi hỏng thật.

**Còn chưa phân xử, và vì sao:** (1) các cờ operation của bên được gọi (`4dbcb97712`, `88dc4b2c47`): dữ liệu đã lưu chỉ có cờ và khởi phát, không có thời lượng phía server tách khỏi phía client. Giải thích khả thi: lỗi lan truyền thật, hoặc bất thường không liên quan. Phân xử cần span server của bên được gọi trong cửa sổ — phải đọc lại trace test, cần Minh duyệt. (2) Cùng giây khởi phát không phân biệt thứ tự; độ phân giải không đủ. Kết luận phụ thuộc: chỉ mức mô tả C-d3 OB; không đổi A4.
