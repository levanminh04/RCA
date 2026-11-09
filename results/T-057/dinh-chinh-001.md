# Đính chính 001 — hồ sơ G4 (T-057)

Claude (người làm), 09/11/2026. Sau phản biện G4 lượt 1 của Codex (R1–R4, chat) và rà soát thêm của người làm (N1–N9). Minh cho phép ghi khi không còn mâu thuẫn với Codex (LOG phiên 3).

Giữ nguyên `ho-so-g4.md` (đã ghim trong `manifest.json`, `manifest-002.json`). File này thay các đoạn nêu dưới đây. **Không đổi số xếp hạng, A4, bảng chính hay CI nào.** Không chạy phương pháp, không đọc dữ liệu thô.

Nguồn mới: [`maxz-dev-002.json`](maxz-dev-002.json) (dev TT từ bản native T-053), [`truy-vet-han-che-002.json`](truy-vet-han-che-002.json) (cờ M5 gốc), [`b0-re3-nhan-002.json`](b0-re3-nhan-002.json). Soát số: [`soat-so-002.json`](soat-so-002.json).

## Đ1 (R1) — RQ3d trên TT và RE3: MRR bằng nhau không có nghĩa "không có ca khác nhau"

Thay câu ở §0 ("Trên RE2-TT và RE3-OB, M1 bằng C-a0 (Δ = 0 ở cả hai bộ)"), dòng RQ3d bảng §3 và đoạn sau bảng §5.2 ("Không phân xử được giữa (a) và (b) … không còn ca nào để tách tác dụng của quan hệ") bằng:

- Trên RE2-TT và RE3-OB, MRR gộp của M1 và C-a0 bằng nhau, nhưng ca khác nhau có tồn tại: TT 2 thắng / 56 hòa / 2 thua (`PT#/so_cap/RE2-TT|M1-C-a0|RR`), RE3 1 thắng / 28 hòa / 1 thua (`R#/so_cap/M1-C-a0|rr`). Giúp và hại bù nhau.
- Ở TT, bốn ca khác nhau có cơ chế đã lần (C07, T-054 §7.2): E1 giúp `327a`, E5 giúp `e9dc`; E1 hại `7a22`, `5e8f`.
- **Không phân xử được** giữa (a) "tín hiệu cục bộ thường đủ" và (b) "thành phần quan hệ chưa hiệu quả". Lý do: số ca khác nhau quá ít (4 ca TT, 2 ca RE3) và theo hai chiều, nên không tách được tác dụng ròng; Hit@5 chạm trần. Dữ liệu phân xử được cần nhiều ca mà quy tắc đơn giản thất bại (FlashTicket, P10). Không dùng kết quả này để kết luận TT/RE3 "không cần quan hệ".

## Đ2 (R2) — Max-z kênh hẹp trên dev TT: có dữ liệu, điều kiện đã xuất hiện

Thay dòng "Dev TT: bản ghi dev không có độ rộng kênh — Không đủ dữ liệu" ở bảng §5.3, dòng "Max-z trên dev TT" ở §12, dòng H14 ở §14 bằng:

- Bản native T-053 (`results/T-053/runs/k-dong-pha1-001/seal.json#/that`, cấu hình `K-E1+E2+E5`) có độ rộng kênh ở 30/30 ca TT; hash seal khớp; RR root tính lại khớp T-052 30/30 ([`maxz-dev-002.json`](maxz-dev-002.json)`#/kiem`). T-052 chỉ bỏ trường này khi tạo bản gọn.
- Theo đúng tiêu chí H8: dev TT có 4 ca sai, **3/4 ca sai thỏa điều kiện mô tả H8** (`dev-14372e1209`, `dev-20acb4402d`, `dev-a915aa2424`); 10/26 ca đúng có root thắng bằng kênh hẹp (`#/TT_dev`).
- Điều kiện này đã xuất hiện trên dev ở cả hai bộ (TT 3/4, OB 2/5 ca sai). Số này **chưa** xác nhận nguồn vật lý của kênh cực trị, cũng chưa chứng minh một khóa thay thế tốt hơn.
- **Bỏ đề xuất H14** (chạy lại M1 trên 30 ca dev TT): không cần.
- Câu "Dev TT: KHÔNG ĐỦ DỮ LIỆU" ở `maxz-dev.json#/TT_dev` và LOG phiên 2 (B5) bị thay bởi đính chính này.

## Đ3 (R3) — Dòng G2-H17: tách hai đại lượng

Thay dòng G2-H17 và câu "Đối thủ phía trên root ở ca sai" ở bảng §6, cùng dòng tương ứng ở bảng §5.1, bằng hai đại lượng riêng ([`truy-vet-han-che-002.json`](truy-vet-han-che-002.json)):

| Đại lượng | TT C-a0 → M1 | OB C-a0 → M1 | RE3 C-a0 → M1 |
|---|---|---|---|
| A. Ở ca sai, thực thể đứng đầu là bên gọi trực tiếp của root (theo `extra/canh`) | 1 → 0 | 8 → 0 | 1 → 1 |
| B. Cờ M5 gốc (`src/m1_danh_gia/m5.py`: có thực thể phía trên root theo `G_N` chắc chắn đứng trước root) | 1 → 0 | **10 → 0** | **3 → 2** |

- B ở OB C-a0 theo loại lỗi: network_delay 8, cpu_consumed 1, cpu_contention 1; cả 10 ca có bên gọi trực tiếp đứng trước root (`#/dai_luong_B_M5_goc/Nezha-OB|C-a0`).
- B ở RE3: C-a0 có 2 ca có bên gọi trực tiếp, 1 ca chỉ gián tiếp; M1 2 ca (`428c`, `cde8`), đều có bên gọi trực tiếp.
- A ở OB C-a0: 8 ca = 7 network_delay + 1 cpu_contention (`#/dai_luong_A_doi_thu_dung_dau`). Số "8 ca" ở §5.1 không thuộc riêng nhóm trễ mạng.
- Bảng §6 cột "Đối thủ phía trên root ở ca sai: OB 8 → 0; TT 1 → 0; RE3 2 → 1" đếm cả gián tiếp theo `extra/canh`; dòng G2-H17 dùng đại lượng B.
- M5 giảm là quan sát; không tự chứng minh cơ chế lan.

## Đ4 (N3) — G4-Q6: M1 được chọn thế nào

Thay gạch đầu tiên của §4 câu 6 bằng:

- Gói E1+E2+E5 do **bộ chọn khối K** của T-053 trả theo luật khai trước (`results/T-053/bao-cao.md:11`, `:143`, `:147`). Minh chốt nền và chấp nhận cờ TRÁI CHIỀU theo dataset của E2 (Q-237, Q-239; nền cuối Q-242). Không phải chọn theo MRR dev gộp.
- Độ bền chọn thấp: trong 1.000 mẫu bootstrap, gói thắng chỉ thắng 249 mẫu; "không có bằng chứng lựa chọn ổn định duy nhất trên dev" (`results/T-053/bao-cao.md:162`).
- Số MRR dev gộp 52 ca (M1 0,904; C-a0 0,847; C-d2 0,909) đúng, nhưng chỉ là mô tả. C-a0 dev TT 0,983 > M1 0,928, còn OB dev 0,662 < 0,873.

## Đ5 (N4) — Root là nút nguồn: sự kiện theo code, chưa là nguyên nhân

Thay câu "E2 không gán bằng chứng cho nút không có bên gọi" ở §10 (điều kiện M1 làm kém) bằng:

"Sự kiện theo code: E2-C gán bằng chứng cạnh cho bên nhận, và frontend không có bên gọi trong `canh` (`dinh-chinh-004.md` Đ13 của T-054), nên frontend không có kênh E2. Việc điều này gây MRR thấp ở 6 ca root frontend **chưa kiểm**; T-054 giữ nó ở mục câu hỏi mở (`results/T-054/reports/p7a-013-v2/bao-cao.md:306`). Phân xử cần so ca frontend với ca root lá có điều kiện tương ứng, trên trung gian đã lưu."

## Đ6 (N6) — §0, "Cơ chế đọc được"

Thay "Có cơ chế đủ chuỗi đầu vào → trung gian → đầu ra cho: E2 ở lỗi trễ mạng OB (C08), E1 ở lỗi CPU, và điều kiện làm khóa xếp max-z sai ở 8/14 ca sai" bằng:

"E2 ở lỗi trễ mạng OB: cơ chế tính toán có trung gian (C08); định vị vật lý chưa phân xử. E1 ở lỗi CPU OB: quan sát trung gian ở 2 ca; phần tác dụng của E1 giảm từ +0,130 còn +0,079 khi bỏ 4 ca D1 (C02). Max-z kênh hẹp: điều kiện có ở 8/14 ca sai trên test, và ở dev (TT 3/4, OB 2/5 ca sai); cũng giúp root ở nhiều ca đúng."

## Đ7 (N7) — §8

Thay "Cùng chiều: … C-d2 và mọi baseline trên cả hai bộ" bằng "… C-d2 và mọi baseline chạy được trên cả hai bộ (CIRCA, TORAI B không hỗ trợ OB)".

## Đ8 (N1) — §1, bổ sung kiểm bản nhận RE3

Thêm sau gạch "Hash": "Bản nhận RE3 ngoài repo khớp biên nhận T-055: hai archive, snapshot, aggregate-plan; 420/420 slot (verified.json, result.json, vân tay job) ([`b0-re3-nhan-002.json`](b0-re3-nhan-002.json)). Lượt kiểm 001 sai phép kiểm (so job.json theo byte), giữ nhưng không dùng."

## Đ9 (N2) — dòng CIRCA RE3 trong `so-cong-bo.json`

`so-cong-bo.json#/bang/RE3-OB/circa` có n = 60, gộp 30 bản RHT+DA và 30 bản RHT; không đại diện một cấu hình CIRCA. Dùng `R#/bang_theo_ve_P/circa` (RHT+DA, MRR 0,917) và `R#/bang_theo_ve_P/circa_rht_aux` (RHT, 0,878). Hồ sơ không dùng dòng gộp.

## Đ10 (R3, nối với Đ3) — §5.1, dòng "C-a0 sai 15 ca OB, ở 8 ca …"

Giữ số; đổi nhãn thành "đại lượng A (thực thể đứng đầu là bên gọi trực tiếp)" và thêm "cờ M5 gốc: 10 → 0".

## Phần không đổi

Bảng §2, A4, các CI và T/H/T, kết luận "M1 không hơn rõ baseline mạnh ở bộ nào", sổ C-15 B, các OPEN khác ở §12, đề xuất §14 trừ H14.
