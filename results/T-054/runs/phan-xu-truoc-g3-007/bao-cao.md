# Phân xử trước G3 — checkpoint 007

Ngày 06/11/2026. Codex người làm; Claude phản biện chính thức. Chưa khóa G3 hoặc chạy main.

## Quyền và trạng thái
Minh duyệt triển khai phiên dài bước1–4 như đề xuất. Đề xuất có điều kiện: trình bản vá cụ thể sau phân xử rồi mới sửa lõi. Bản này là kết quả phân xử và đề xuất patch, chưa là phê duyệt patch. Đầu ra ghi trong đúng phạm vi năm file đã trình. Quyền nguyên văn, nguồn/hash trước phiên và checkpoint nằm trong bang-chung.json.

Bước1: đã đọc code, kiểm103pin, xác định phụ thuộc OB và lấy schema90RE3; hợp đồng khoa học/đơn vị chưa chốt. Bước2: chưa cài patch lõi, chưa có kiểm toàn tuyến của patch. Bước3: đã tính lại partition metadata1642vị trí, chưa tạo plan thực thi/chuyển nguồn/SSH. Bước4: chưa đủ căn cứ trình khóa G3. Không gọi checkpoint này là xong toàn gói.

## OB: quan sát, giải thích và đề xuất
FACT: reader p3.nezha::_doc_cua_so bắt mỗi nguồn có5N5A, cùng membership ordinal, rồi dựng DataFrame chung. M1 ca_nezha dùng DataFrame đó. Chuoi kiểm len(timestamp_nguồn)==len(metrics) và zip mọi kênh với cùng tập hàng. SimpleRCA dùng arrays riêng; MicroRank/TraceRCA chỉ dùng spans sau reader. BARO chấm RobustScaler độc lập từng cột sau tiền xử lý đã ghim. Chặn4ca là chặn adapter trước method, không phải kết quả method.

Hai ca thiếuN và hai ca thừa hàng sát biên đều phải giữ mẫu thật trong [t−300,t+300), nhưng không suy cùng nguyên nhân thiếu dữ liệu. Bỏ guard đơn lẻ vẫn không biểu diễn được các cột khác độ dài. Bù/lưới/union hoặc cắt về5hàng thay phân phối đầu vào. Không dịch mốc, bỏ ca, gán0 hoặc pilot method test để chọn phương án.

CANDIDATE: biểu diễn per-source giữ từng timestamp và mẫu thật. Bản rectangular cũ vẫn giữ đường thực thi cũ; layout mới bật rõ ở wrapper T054. Đây là thay đổi hợp đồng adapter và cách đưa input BARO, không tuyên bố sửa thuật toán hay xác nhận lợi ích RCA. ThiếuN thật vẫn dẫn tới thiếu hỗ trợ/NO_EVIDENCE/error theo logic đã khóa, không tự cứu bằng mẫu giả.

## Bản vá cụ thể xin duyệt — chưa áp dụng
1. src/p3/nezha.py: thêm layout source_native opt-in; mặc định legacy giữ guard5N5A. Nhánh mới giữ per-source frame/time/arrays, window/provenance ghi sốN/A thật từng nguồn. Khi rectangular hợp lệ vẫn giữ các trường/đường cũ. Ragged không dựng frame chung giả hoặc fake timestamp.
2. src/m1/adapter.py: ca_nezha nhận layout optional; ragged chuyển thành các record mẫu thật theo source, cùng params.chi_so_hang_metric ánh xạ source→index và thoi_gian_nguon thật. Channel owner giữ ánh xạ hiện hành; không truyền locator/nhãn.
3. src/m1/chuoi.py: hỗ trợ optional chi_so_hang_metric; kiểm index nguyên/duy nhất/trong miền, độ dài thời gian, timestamp thực và owner của cột. Quan sát và N/A mỗi kênh chỉ lấy đúng các hàng nguồn ấy. Thiếu mapping giữ hành vi rectangular cũ. Giữ API7tham số và công thức E1/E2/E4/E5/xếp hạng/vùng.
4. src/p3/adapters/nezha.py: source_native cho BARO gọi kernel và preprocessing đã ghim trên từng source riêng, ghép khóa toàn cục với thứ tự cột khai trước để giữ hòa; SimpleRCA giữ arrays, trace methods giữ spans. Không thêm ngưỡng hỗ trợ mới. Phải kiểm equivalence trước coi tuyến mới hợp lệ.
5. results/T-054/scripts/worker.py: bật layout source_native rõ ràng cho OB tại cả tuyến M1 và baseline; TT không đổi. Ghim lựa chọn layout trong metadata/config/contract mới trước main; không dùng gói103pin cũ cho code mới.
6. tasks/T-054-khoa-g3-chay-p7-a/SPEC.md: lưu bản trước trong output task, bổ sung đúng quyền5file và thay đổi hợp đồng OB/layout; giữ nền/ca/seed/statistics. Không sửa lịch sử T026/T044.
7. docs/WHY.md: nối lý do per-source, phương án khác, bằng chứng code, điều kiện thất bại và giới hạn equivalence; chưa gọi cơ chế đã kiểm.
8. docs/DECISIONS.md: nối nguyên văn quyền phiên dài hiện hành và quyết định patch nếu Minh duyệt. LOG/STATE và outputs T054 tiếp tục theo phạm vi task.

Ảnh hưởng: M1 và toàn vế OB, BARO input dispatch, code/config/source/env binding và package từng host. TT giữ cấu hình, nhưng coreM1 có thêm nhánh nên cần chứng minh mặc định không đổi. Không mở lại nghiệm thu task cũ. Quyền patch không phải quyềnG3/main/telemetryRE3.

## Phép kiểm cần thiết sau duyệt patch
- Fixture per-source:2N5A/3N5A/6N5A/5N6A, thứ tự hàng, ranh giới, missing/nonfinite; giữ đúng mẫu/timestamp không bù/cắt.
- Mapping sai/trùng/chéo owner/out-of-range phải bị bác trước method.
-5N5A: old↔new input, trung gian, cờ, tầng, khóa, hòa, hạng và vùng giữ tương đương; so ca dev hợp lệ đã pin, không chạy rộng lại.
- BARO rectangular↔per-source với hòa, cột constant, preprocessing ffill/nonfinite; kiểm khóa và thứ tự toàn cục, không chỉ điểm cuối. Synthetic feasibility riêng nếu có không thay toàn pipeline.
- Kiểm phần tuyến cloud/nhận mới sau khi source/core/binding đã hợp lệ; dùngEC2 cho phần phù hợp theo kế hoạch. Không chạy method trên4testOB để thử patch.

## RE3: đã làm và phần OPEN
Đã kiểm nguồn metadata theo pin hợp đồng003, lấyfooter90/90parquet tại HF revision đãpin bằng HTTP206exactrange. Tổng1.491.735byte metadata; mỗi footer≤128KiB. Chỉ giữ schema Arrow/names/types/nullability/counts và hash footer; không đọc min/max stats, data pages hay phương pháp. Full LFS hash của cả file chưa được xác minh bằng phầnfooter; không nhận đây là full-source verification. Có5schema metric,1schema trace,1schema log; xem từng schema và tập cột trong bang-chung.json#/RE3/schema_summary.

OPEN: int64 không chứng minh đơn vị timestamp/duration; cần tài liệu/converter nguồn. Cadence/null thực/severity/coverage không suy từ dtype. Inventory từ architecture hoặc metadata service, không lấy4root nhãn; frontend-external chưa tự gộp frontend. Metric profiles phải bao phủ cả5schema; không chọn kênh theo root/fault. TORAI ts-* filter, CIRCA graph và adapter/grant/bảngRE3 riêng chưa cài. Chưa chốt ma trận/số lượt hoặc đếm30ca là30method. Không dùngRE3 để tune/pilot. H1 mới đạt schema, chưa đạt đầy đủ hợp đồngH1/H2.

## Partition và phần còn thiếu của bước3
Tính metadata theo ownerTT đãkhai và5ca chuyển: EC2_1=523supported+2C-einsufficient; EC2_2=749supported+68unsupported; laptop300supported.1642keysduynhất. Đây không phải planthựcthi35/25 hoặc lịch đãkhóa.

Chưa chuyển thêm nguồn hay kiểm máy ở lượt này. Đầu vào cho bước3 sau patch: codepins mới, nguồnOB hợp lệ, inventory/hash remote để chỉ bổ sung phần thiếu, 5TT đúngowner, cận nguồn+output+tạm+lượt hỏng/gói nhận, môi trường/phần parity khác thật. Giữ lô độc lập và ưu tiênEC2; prep→TORAI, M1seal→C-d3. Layout/snapshot/matrix/authority mới phải khớp trước phát. Không dùng nguyên activate006 cho35/25.

## Tiếp nhận chính xác
Đọc bang-chung.json và báo cáo này, rồi patch scope8mục trên. Chờ Minh quyết đúng patch/hợp đồng; tiếp tục phần metadataRE3 có nguồn thích hợp khi không phụ thuộc patch. Khi được phép cài, giữ outputs/checkpoint mới riêng, kiểm synthetic/dev đúng phần đổi rồi hoàn thiện bước3 và hồ sơG3. Giữ main, test method và telemetryRE3 chưa mở. Không chạy lại metadata90footer đãhợp lệ hoặc baseline diện rộng vì đổi phiên.

Lệnh cuối: kiểm manifest007, protected-file pins, diff đúng5file và git diff --check. Có giữ một assertion sai trong phân tích partition: ban đầu dùng slot host thay TT_case_owner; đã sửa phép tính metadata và lưu failure trong bang-chung, không cóplan hoặc method bịphát từ phép tính sai.
