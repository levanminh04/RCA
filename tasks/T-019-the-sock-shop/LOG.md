# Nhật ký T-019

Chỉ người làm ghi thêm; Claude chỉ ghi REVIEW.md.

## Phiên 1 — 04/10/2026 — Codex — Windows 11 laptop Minh — người làm

**Mở phiên:** Intent EXECUTE. Đã đọc AGENTS, STATE, LESSONS, review-prompt, mẫu SPEC/LOG, MRP §2–7, WHY, DECISIONS và nguồn DT18/advisor. HEAD mở phiên: `93f13d4c4a966428177e2acc287d96bc89303e92`. Cây làm việc có output task khác; không sửa. Chưa có SPEC/LOG T019 hay dòng STATE T019. STATE có phần prose cũ; prompt Minh giao T019 rõ và cho chèn dòng này, không sửa phần prose chung.

**Quyết định của Minh trong phiên:**
- Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026
- Chưa ghi DECISIONS vì prompt cấm ghi; sẽ đề xuất nguyên văn trong results/T-019/de-xuat-tai-lieu-chung.md.

**Khối task — nguyên văn:**

<task>
Thư mục task: tasks/T-019-the-sock-shop/. Thư mục kết quả: results/T-019/.

Đầu vào:
- results/T-002/: thẻ, mẫu thẻ, script, public-metadata.
- tasks/T-002-the-dataset-rcaeval/: SPEC, LOG, REVIEW.
- results/T-003/bang-tieu-chi.md.
- data/rcaeval/re2ss_orders_loss_2 và data/rcaeval/re3ss_carts_f1_1.
- Trong D:\RCA-ext\data\: fse-ss, torai-SS, RE1-SS.

Yêu cầu:
1. Thẻ theo đúng mẫu results/T-002/mau-the-dataset.md, đủ 10 mục và đủ 9 tiêu chí của MRP §4.
2. Census nhãn trên toàn bộ release, lấy từ metadata công khai: root × loại lỗi × lần lặp.
   - Lập danh sách file của từng ca: ca nào có trace, có log, có metric.
   - Không suy ra từ 2 ca mẫu.
3. Kiểm file thật, tổng dung lượng tải tối đa 1 GB:
   - schema;
   - quan hệ span cha–con;
   - liên kết giữa log và trace;
   - dữ liệu bình thường;
   - biên file quanh mốc tiêm, vì đây là một đường lộ mốc tiêm (T-006 mục 2.3);
   - vị trí service gốc trong đồ thị.
   Đọc 8 file root_cause.txt của RE3-SS và mô tả chúng chứa loại nhãn gì.
4. Sổ ca đã nhìn:
   - fse-ss, torai-SS và RE1-SS đã được chạy phương pháp ở T-006. Xác định chúng trùng với ca nào của RE2-SS hoặc RE1-SS, bằng mốc tiêm, hash hoặc so nội dung.
   - Làm tương tự giữa fse-ob, torai-OB và RE2-OB. T-007 đã chạy đủ 90 ca RE2-OB.
   - Mục đích: G1 cần biết ca nào không được dùng làm test.
5. Tiêu chí 7 (triệu chứng xuất hiện ngoài service gốc): chỉ ước lượng thô như T-002 mục 6.

Edge case tối thiểu phải có trong SPEC (bạn tự tìm thêm):
- Ca thiếu file.
- Trace rỗng.
- Nhãn trùng.
- Tên service khác nhau giữa các nguồn.
- Mốc tiêm nằm ngoài cửa sổ dữ liệu.
- Revision Hugging Face khác nhau giữa các file.

Không dùng EC2. Được ghi thêm: data/T-019/ (ngoài git); D:\RCA-ext\work\T-019\.
</task>

**Diễn biến:**
- Đọc input: hai mẫu SS có file thật; metadata T002 tree gồm 2.815 entries. Đếm sơ bộ RE2-SS 90 ca/270 file, RE3-SS 30 ca/98 file, RE1-SS 125 ca/250 file. Không trace ở cả ba trong tree ghim; cần kiểm census/hash độc lập trước kết luận thẻ.
- Viết SPEC kỹ trước triển khai. Impact map: chỉ SPEC/LOG T019, results T019, cache data/work T019, và một dòng STATE T019. Không thay lựa chọn dataset hay source chung.
- Tự phản biện SPEC trước tải: đối chiếu các lỗi yêu cầu; thêm rõ clock/band0/hash git-blob/identity nội dung/concurrency, phép không làm và kết luận yếu. Bản ghi results/T-019/tu-phan-bien-spec.md. Không thay quyết định vật chất.
- Kiểm metadata: cả tám snapshot source T002 khớp SHA256 manifest; hợp ba trang tree bằng hf-tree.json, revision ghim đúng. Census độc lập ra RE1 125/25 ô/lặp5; RE2 90/30 ô/lặp3; RE3 30/9 ô/lặp3–4. Collision khóa nhãn =0. Files và từng ca ở census/file-inventory.
- Kế hoạch tải TRƯỚC tải: nguồn https://huggingface.co/datasets/phamquiluan/RCAEval/resolve/afeacb11bcc94dadfd1c8f483ee4377b2b8b614e/; toàn RE1/2/3-SS 149.245.189 byte, tái dùng bảy file mẫu khớp hash 2.315.466 byte, tải mới 146.929.723 byte, data/T-019/. Manifest/plan results/T-019/download-plan.json. Ghi hash theo LFS-SHA256 hoặc git-blob-SHA1 sau tải. Đã được prompt Minh cho trần1GB, không xin lại.
- Kế hoạch tải nhánh lineage TRƯỚC tải: cùng nguồn/revision HF trên, 180 file RE2-OB chỉ metric/inject, 14.215.893 byte; D:/RCA-ext/work/T-019/lineage/re2ob/. Plan results/T-019/lineage/download-plan.json. Không trace/log OB.
- Kế hoạch nguồn nhánh audit TRƯỚC tải: HF metadata/info/tree revision afeacb11bcc94dadfd1c8f483ee4377b2b8b614e (~0,7MB), RCAEval GitHub metadata/code revision259ea4167160256a74ad30004aa3d96a998c846e (~1MB), Sock Shop upstream metadata/README/architecture (~0,2MB; pin SHA trước file). Trần nhánh3MB, chỉ source không telemetry. Manifest cụ thể do nhánh lưu trước file. Tổng kế hoạch root+lineage+source dưới165MB.
- Kiểm môi trường: Python .venv đã có pandas/pyarrow/numpy; requests thiếu (lệnh import thất bại, không sửa môi trường). Dùng urllib chuẩn cho acquisition, không cài package mới.
- Acquisition SS hoàn thành 618/618 file, toàn size/hash khớp nguồn ghim; tải146.929.723 byte, bảy file verified reuse; có progress mỗi25file, thời gian khoảng147s. Manifest results/T-019/acquisition/manifest.json. Toàn metadata/file thực xác nhận không trace, không thực hiện phép parent trên dữ liệu không tồn tại.
- Nhánh source đã pin Sock Shop9dff06fae4981921caec6a62393a6ebfce4b3e3f; kế hoạch bổ sung trước tải: internal-docs/design.md1.500 byte và deploy/docker-compose/docker-compose.yml3.757 byte; nằm trong3MB. Chỉ cạnh cấu hình, không dùng như trace runtime.
- Kế hoạch nguồn trước tải tiếp: metadata repo/commit/tree chính thức microservices-demo/microservices-demo.github.io tối đa100KB, lấy SHA rồi ghi manifest trước Architecture.png tối đa500KB (dự kiến<200KB). Cạnh cấu hình chỉ hỗ trợ mô tả tĩnh; không mặc định đúng deployment RCAEval. Cộng trong trần3MB nhánh source.
- Đã chèn duy nhất dòng T019 STATE bằng splice byte với OS lock; kiểm byte ngoài dòng giữ nguyên ở state-start.json. Lệnh sau mutation báo lỗi in tiếng Việt cp1252 (không lỗi sửa STATE); giữ record, sửa encoding stdout của script T019, không ghi lại STATE.
- Kế hoạch hình trước tải: assets/Architecture.png258.735byte; docrepo revision1ae9f90384364b961fe6bfb6c796ddba328c6ad8, Git-blob nguồn ở sources-audit/diagram-download-plan.json. Đây là hình architecture nguồn, chưa bằng chứng deployment runtime SS.
- Inspection lượt1 đã đọc đủ245ca, có progress từng25ca; lỗi serialization numpy.bool lúc ghi nhãn sau cases/schema. Giữ partial/progress và snapshot code trong inspection-001-failed/. Sửa ép bool Python; chạy lại vì bảng bands chưa được ghi, không giả hoàn thành. Không tải lại payload.
- Inspection lượt2 hoàn thành245ca/618hash trong219,421s; có cases/schema/boundaries,8nhãn, bands/entity/case/cell/summary. Peak working set quan sát329.355.264byte ở tiến trình reader; máy có nhiều phiên khác, không dùng wall time này làm benchmark RCA. Nguồn inspection/manifest.json và resources-snapshot.json.
- Source audit hoàn thành: census độc lập khớp, không trace;8rootcause/7nội dung unique, một nhãn frontend_f2_2 ngoài cửa sổ own log và không match; bảy nhãn match message,4timestamp lệch1s. Kiến trúc source chỉ bậc liên hệ tĩnh, không suy hướng/runtime. Nhánh tải652.287byte; quét77file T000–012 và đọc sâu các nhận định liên quan, không tuyên bố audit toàn RCA/phương pháp cũ. Source-report và manifest đủ file.
- Lineage hoàn thành:405cặp so metric,400full-content,5cặp finite-time sau loại hàng nulltime; local fseSS=RE1SS100byte-identical. RE2SS90 qua toraiSS; RE1SS100non-disk qua fseSS; RE2OB90 T007 direct và toraiOB. RE1SS25disk T006 chỉ census metadata, T019 đọc metric, chưa thấy RCA direct. Ledger910dòng;180OBfile14215893byte hashPASS;1695source+6archive before/after giữhash. Không sửa nguồn cũ.
- Kế hoạch nguồn trước tải cuối: main.py chính thức RCAEval tại GitHub revision259ea4167160256a74ad30004aa3d96a998c846e,26.309byte, Git-blob81c7e30b9e97fca400dee2779f549faa0dbdee89 từ tree đã ghim. Chỉ đọc/định vị đường SLI; không chạy/import runner. results/T-019/runner-source/ giữ plan/source/hash. Nằm trong tổng1GB.
- Kiểm cuối phần được phép: tách constant và all-null bằng đọc metric nhẹ245ca, không đổi khảo sát. Probe loại20cặpca/kênh thiếu30điểm reference; nhómerror ngoài root thiếu23ca RE2 (69bộca/nhóm/q), có danh sách và lý do. Ghi exclusions, sổ thêm245SS+90OB metric-readT019; final ledger1245row không là1245incident.
- Source runner26.309byte khớp blob; main.py:283/:341–363/:415 giữ bằng chứng service từ path→SLI→method. Không import/chạy. Tổng byte mạng thực161.824.212, không retry payload; cache replay618file bằng --run mới, toànhashPASS/0byte mạng. Không mất lượt cũ.
- Tự soát thẻ: sốsource/probe/census đúng; cụ thể hóa path artifact, thêm lệnh --run/cache verified cho tái lập. Không thêm scope/phương pháp. SPEC chỉ append mục Thay đổi trong lúc làm; mọi lựa chọn G1 vẫnOPEN.
- Rà final-checks lượt1 phát hiện rates cóNaN (195ô tỷ lệ kênh không xác định vì mẫu số0), không phải giá trị ngoài[0,1]. Giữ failedchecks và tổng hợp trước sửa trong inspection-summary-001-before-paired/. Bổ sung phép kiểm NaN chỉ khi denominator0 và so cùng entity có cả hai tỷ lệ hữu hạn. Nhómerror RE2 thật62ca hợp lệ (trước sửa67ca có schema),84bộca/nhóm/q bị thiếu; bands/rates raw không đổi. Giữ lý do thiếu reference/control/post từng ca; không biến missing thành0 hoặc chọn threshold theo kết quả.
- Final-checks sau sửaPASS: census độc lập,618SShash,245caseread,120metric±720,8nhãn/7unique/1outside,465bộband/count tính lại từ2rawcase, táiaggregate mọi nhóm/ô, ledger1245unique, network161824212byte,10mục+9TCmỗiRE2/RE3, oldsnapshotsunchanged và initialSTATEotherbytespreserved. Không RCA/detector, khôngmạngmớiởverifier.


## Kết thúc phiên — 04/10/2026


**A. Đã làm.** Hoàn tất thẻ RE2-SS/RE3-SS đủ10mục/9tiêu chí, RE1-SS ngắn; census245SSca, kiểm618file và8nhãn chi tiết; sổ ca đã nhìn SS/OB, đính chính và nháp tài liệu chung. Hai subagent hỗ trợ độc lập; Claude chưa phản biện.

**B. File đã thay đổi, kể cả ngoài repo.** tasks/T-019-the-sock-shop/SPEC.md và LOG.md; mọi file results/T-019/ liệt kê trong output-files.csv/artifact-manifest.json;618file data/T-019/ ngoài git;180file D:/RCA-ext/work/T-019/lineage/re2ob/ (đầy đủ path ở lineage/outside-files.csv). docs/STATE.md chỉ dòngT019. Không sửa file task cũ, môi trường/src hoặc nguồn chung khác. Không commit/push.

**C. Kiểm tra đã chạy và kết quả.** Census độc lập/hash/parser/schema/biên/nhãn PASS; metadata toànSS khôngtrace. RE2=90ca/5root/30ô; RE3=30ca/3root/9ô. Cả120ca RE2/3 có metric±720s quanh tiêm. Lineage405cặp:400fullmetric,5finite-time sau bỏ nulltime. Sổ1245hàng quan hệ/exposure, không phải1245incident. Kiểm band/count465bộ từ2rawcase và táiaggregate toàn summary PASS. Tải161.824.212byte, cache replay0byte. Kiểm final/state/handoff được ghi riêng; mọi lượt hỏng giữ lại.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** T003 dòng19 dẫn hồ sơ Sock Shop về T002 trong khi SPEC/thẻ T002 chỉ có bốn TT/OB và schema hai mẫuSS. T019 đã bổ sung hồ sơ riêng; đề xuất sửa referral, chưa sửa cũ. Không chứng minh sai số mới ở T002. Bổ sung nguồn: HF bảngF5SS lệch prose/GitHub/tree; một root_cause front-end_f2_2 trùng ca trước và ngoài cửa sổ own log. Đây là lỗi nguồn nhãn, không tự là lỗi người làm task cũ. Bằng chứng/đoạn sửa tối thiểu ở dinh-chinh-task-cu.md.

**E. Chỗ lệch khỏi SPEC và lý do.** Không vượt phạm vi. Bổ sung tách constant/all-null, finite paired rates và --run/cache verified để tránh mẫu số0 và tái lập ghi đè. SPEC chỉ ghi thêm mục Thay đổi trong lúc làm. Lượt serialization lỗi và tổng hợp trước sửa được giữ. Không đổi q/band/raw hay lựa chọn nghiên cứu.

**F. Đề xuất cho tài liệu chung.** Nháp nguyên văn DECISIONS về ủy quyền, README dữ liệu/modalities/lệnh dựng và thông tin G1 về exposure/biên/nhãn ở de-xuat-tai-lieu-chung.md. Không tự ghi WHY/lựa chọn dataset.

**G. Phần chưa kiểm và lý do.** Parent/log-trace/root runtime degree không có đầu vào trace; mapping kiến trúc sang deployment OPEN. Onset/end/normal sạch/vùng ảnh hưởng/code-line không có nhãn/source độc lập; mô tả giả định và điều kiện sai trong thẻ mục10. Không chạy RCA/detector theo prompt.

**H. Cần Minh quyết.** Cho Claude phản biện T019. Tại tổng hợp G1, quyết dùng/không dùngSS, kịch bản graph kiến trúc, cách dùng nhãn và chia dữ liệu sau khi xét sổ exposure. Nếu ghi nguồn chung hoặc sửa referral cũ, Minh duyệt riêng bản nháp. Task này không tự quyết các mục đó.

**Kết thúc phiên đủ6ý theo mẫu:**
1. Đã làm: xem A; toàn phần được phép và khả thi đã kiểm, status chờ Claude.
2. File thay đổi: xem B, output-files.csv và toàn danh sách dưới; nguồn cũ giữ hash trong phạm vi có baseline.
3. Kiểm tra: xem C/final-checks.json/handoff-checks.json; không chạy RCA/detector.
4. Điều chưa chắc/cần Minh: xem G/H; chưa chọn dataset/chia hoặc dùng nhãn detail lỗi.
5. Bước tiếp theo chính xác: Minh mở phiên Claude, dán nguyên prompt cuối này; Claude đọc SPEC/LOG và mọi file liệt kê, ghi đúng tasks/T-019-the-sock-shop/REVIEW.md. Kiểm read-only rẻ: `.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py --read-only`; không chạy runner nguồn.
6. Lệnh cuối cùng dự kiến sau ghi LOG: `py -3 -X utf8 -B results/T-019/handoff.py verify`; lệnh kiểm diff trước đó: `git diff --check -- docs/STATE.md tasks/T-019-the-sock-shop results/T-019`. Không dùng diff làm phạm vi phản biện; danh sách file dưới đầy đủ cả cache và file ngoài repo.

## Prompt phản biện cho Claude — T-019

```text
Bạn là người phản biện độc lập cho task T-019 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-019-the-sock-shop/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-019-the-sock-shop/SPEC.md, tasks/T-019-the-sock-shop/LOG.md, các file đầu ra: tasks/T-019-the-sock-shop/SPEC.md, tasks/T-019-the-sock-shop/LOG.md, deliverables under results/T-019/; complete paths and scopes for outputs, data/T-019/ and D:/RCA-ext/work/T-019/ are results/T-019/output-files.csv; downloaded-file hashes are in results/T-019/file-inventory.csv,
và kết quả `git diff 93f13d4c4a966428177e2acc287d96bc89303e92` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```


## Bổ sung đóng gói bàn giao — 04/10/2026

Kiểm đóng gói lượt1 báo trailing spaces ở README nguồn nguyên bản và dòng placeholder của prompt nguyên văn. Giữ source/prompt nguyên trạng, chỉ kiểm whitespace văn bản do T019 viết ngoài code fence; giữ failedchecks trong handoff-checks-001-failed.json. Không thay số liệu hoặc phạm vi. Prompt mới cuối LOG thay bản trước về danh sách file (có thêm record lượt kiểm hỏng); cả hai bản cũ/mới được giữ theo luật append-only.


**A. Đã làm.** Hoàn tất thẻ RE2-SS/RE3-SS đủ10mục/9tiêu chí, RE1-SS ngắn; census245SSca, kiểm618file và8nhãn chi tiết; sổ ca đã nhìn SS/OB, đính chính và nháp tài liệu chung. Hai subagent hỗ trợ độc lập; Claude chưa phản biện.

**B. File đã thay đổi, kể cả ngoài repo.** tasks/T-019-the-sock-shop/SPEC.md và LOG.md; mọi file results/T-019/ liệt kê trong output-files.csv/artifact-manifest.json;618file data/T-019/ ngoài git;180file D:/RCA-ext/work/T-019/lineage/re2ob/ (đầy đủ path ở lineage/outside-files.csv). docs/STATE.md chỉ dòngT019. Không sửa file task cũ, môi trường/src hoặc nguồn chung khác. Không commit/push.

**C. Kiểm tra đã chạy và kết quả.** Census độc lập/hash/parser/schema/biên/nhãn PASS; metadata toànSS khôngtrace. RE2=90ca/5root/30ô; RE3=30ca/3root/9ô. Cả120ca RE2/3 có metric±720s quanh tiêm. Lineage405cặp:400fullmetric,5finite-time sau bỏ nulltime. Sổ1245hàng quan hệ/exposure, không phải1245incident. Kiểm band/count465bộ từ2rawcase và táiaggregate toàn summary PASS. Tải161.824.212byte, cache replay0byte. Kiểm final/state/handoff được ghi riêng; mọi lượt hỏng giữ lại.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** T003 dòng19 dẫn hồ sơ Sock Shop về T002 trong khi SPEC/thẻ T002 chỉ có bốn TT/OB và schema hai mẫuSS. T019 đã bổ sung hồ sơ riêng; đề xuất sửa referral, chưa sửa cũ. Không chứng minh sai số mới ở T002. Bổ sung nguồn: HF bảngF5SS lệch prose/GitHub/tree; một root_cause front-end_f2_2 trùng ca trước và ngoài cửa sổ own log. Đây là lỗi nguồn nhãn, không tự là lỗi người làm task cũ. Bằng chứng/đoạn sửa tối thiểu ở dinh-chinh-task-cu.md.

**E. Chỗ lệch khỏi SPEC và lý do.** Không vượt phạm vi. Bổ sung tách constant/all-null, finite paired rates và --run/cache verified để tránh mẫu số0 và tái lập ghi đè. SPEC chỉ ghi thêm mục Thay đổi trong lúc làm. Lượt serialization lỗi và tổng hợp trước sửa được giữ. Không đổi q/band/raw hay lựa chọn nghiên cứu.

**F. Đề xuất cho tài liệu chung.** Nháp nguyên văn DECISIONS về ủy quyền, README dữ liệu/modalities/lệnh dựng và thông tin G1 về exposure/biên/nhãn ở de-xuat-tai-lieu-chung.md. Không tự ghi WHY/lựa chọn dataset.

**G. Phần chưa kiểm và lý do.** Parent/log-trace/root runtime degree không có đầu vào trace; mapping kiến trúc sang deployment OPEN. Onset/end/normal sạch/vùng ảnh hưởng/code-line không có nhãn/source độc lập; mô tả giả định và điều kiện sai trong thẻ mục10. Không chạy RCA/detector theo prompt.

**H. Cần Minh quyết.** Cho Claude phản biện T019. Tại tổng hợp G1, quyết dùng/không dùngSS, kịch bản graph kiến trúc, cách dùng nhãn và chia dữ liệu sau khi xét sổ exposure. Nếu ghi nguồn chung hoặc sửa referral cũ, Minh duyệt riêng bản nháp. Task này không tự quyết các mục đó.

**Kết thúc phiên đủ6ý theo mẫu:**
1. Đã làm: xem A; toàn phần được phép và khả thi đã kiểm, status chờ Claude.
2. File thay đổi: xem B, output-files.csv và toàn danh sách dưới; nguồn cũ giữ hash trong phạm vi có baseline.
3. Kiểm tra: xem C/final-checks.json/handoff-checks.json; không chạy RCA/detector.
4. Điều chưa chắc/cần Minh: xem G/H; chưa chọn dataset/chia hoặc dùng nhãn detail lỗi.
5. Bước tiếp theo chính xác: Minh mở phiên Claude, dán nguyên prompt cuối này; Claude đọc SPEC/LOG và mọi file liệt kê, ghi đúng tasks/T-019-the-sock-shop/REVIEW.md. Kiểm read-only rẻ: `.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py --read-only`; không chạy runner nguồn.
6. Lệnh cuối cùng dự kiến sau ghi LOG: `py -3 -X utf8 -B results/T-019/handoff.py verify`; lệnh kiểm diff trước đó: `git diff --check -- docs/STATE.md tasks/T-019-the-sock-shop results/T-019`. Không dùng diff làm phạm vi phản biện; danh sách file dưới đầy đủ cả cache và file ngoài repo.

## Prompt phản biện cho Claude — T-019

```text
Bạn là người phản biện độc lập cho task T-019 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-019-the-sock-shop/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-019-the-sock-shop/SPEC.md, tasks/T-019-the-sock-shop/LOG.md, các file đầu ra: tasks/T-019-the-sock-shop/SPEC.md, tasks/T-019-the-sock-shop/LOG.md, deliverables under results/T-019/; complete paths and scopes for outputs, data/T-019/ and D:/RCA-ext/work/T-019/ are results/T-019/output-files.csv; downloaded-file hashes are in results/T-019/file-inventory.csv,
và kết quả `git diff 93f13d4c4a966428177e2acc287d96bc89303e92` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```


## Phiên phản hồi phản biện — 04/10/2026

- Mở phiên: Codex, thiết bị Windows 11/laptop tại D:/RCA-flashticket, vai trò người làm T-019, bước 7 — phản hồi phản biện. HEAD vẫn là mốc mở task ghi ở phần đầu LOG.
- Minh yêu cầu trong phiên này: “đã có review t 019, đọc agent.md và workflow trước rồi **kiểm chứng từng góp ý rồi ghi phản hồi vào bảng cuối REVIEW và LOG**”. Intent: EXECUTE phản hồi; không phải lệnh sửa các đầu ra khoa học hay bản bàn giao.
- Phạm vi ghi phiên này: chỉ thêm LOG và điền bảng “Phản hồi của người làm” cuối REVIEW; để trống cột “Minh quyết”. Theo workflow ở docs/review-prompt.md, chưa sửa file nào khác, kể cả STATE. Không đổi người làm/người phản biện của SPEC; REVIEW ghi ngoại lệ Minh cho phép phiên Codex khác phản biện.
- Đã đọc AGENTS.md, STATE, SPEC, cuối LOG và workflow bước 7. Lệch trình tự: lượt đọc gộp đã mở REVIEW trước khi ghi tự soát. Không gọi lượt tự soát của người làm sau đó là chưa biết finding; nhánh hỗ trợ riêng được giao chỉ đọc đầu ra, không đọc REVIEW. Đây là ghi nhận trung thực, không khôi phục được điều kiện trước khi biết góp ý.
- Kiểm R1 trước khi thêm bất kỳ dòng LOG nào: 925 đường dẫn manifest đều tồn tại; 923 mục có hash, chỉ LOG lệch. Manifest ghi LOG 158.173 byte, hiện tại 28.111 byte; inventory vẫn đủ. Prompt cuối hiện tại không bằng prompt_for(inventory()), trong khi handoff-checks.json lưu all_pass=true. Các hash khoa học/dữ liệu còn khớp. Chưa xác lập ai/phiên nào đổi LOG hoặc thời điểm đổi; không suy từ sai khác hiện tại rằng lượt kiểm ban đầu không hợp lệ.
- Không chạy handoff.py build/verify vì hai lệnh này ghi file; chỉ import định nghĩa với Python -B và tự tính trên bộ file hiện tại. Không tải hoặc chạy RCA/detector. Sẽ kiểm lại đầu ra khoa học rẻ bằng verify_final.py --read-only, rồi ghi kết luận cho từng góp ý và đề xuất sửa tối thiểu theo file.


### Kết quả tự soát và kiểm chứng — bước 7

**Tự soát sau khi người làm đã biết finding:** đọc lại SPEC, thẻ, tiêu chí xong, tài liệu tái lập, đính chính, báo cáo lineage; lần theo code khảo sát/kiểm và bảng nguồn. Không có điểm khoa học mới để thêm N1. Vắng trace chỉ đúng release ghim; parent/join/bậc runtime không bị gán 0. Khảo sát dùng nhãn tiêm theo phạm vi mô tả của SPEC, gắn root sau phép tính; không có RCA/detector nhận nhãn. Drift, workload, collector và OR nhiều kênh vẫn là các nguyên nhân khác có thể giải thích tỷ lệ ngoài root. Root_cause không bị nâng thành onset/code-line/vùng ảnh hưởng. Exposure không đồng nghĩa hiệu quả phương pháp hoặc một recording mới độc lập.

**Nhánh tự soát riêng chưa đọc REVIEW:** subagent independent_outputs chỉ đọc, không ghi file, không tải/chạy phương pháp. Không tìm thấy lỗi khoa học mới. Kiểm độc lập các CSV/JSON: 22.572 cờ root khớp entity/root; đủ 90 RE2 và 30 RE3 có root entity; 68.532 đối chiếu số đếm nhóm một kênh và 22.461 chênh lệch paired không lệch; tái tổng hợp 36 dòng summary không lệch. Không thấy metric/log/injection cùng byte giữa các ca trong inventory và không thấy cửa sổ metric trùng giữa 245 ca. Đây không phải chứng minh độc lập khoa học nếu clock/provenance bị đổi mà không khai báo. Phạm vi tự soát: thẻ/khảo sát/exposure, không tái lập toàn phương pháp hoặc mở telemetry mới. Subagent cũng chạy verifier chỉ đọc trước khi nhận tin root đã chạy; hai lượt đều PASS, không có file đầu ra mới.

**Kiểm của người làm:** `.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py --read-only` đạt 27/27. Tính lại 465 bộ band/count từ hai ca raw và táiaggregate, hash/size 618 file SS, census/nhãn/biên/sổ exposure đều đạt. Tổng tải cũ vẫn 161.824.212 byte; phiên phản hồi tải 0 byte. Không gọi build/verify của handoff.py vì chúng có thao tác ghi.

**R1 — Đúng, KHÔNG CHẶN.** Trước khi mở mục phiên mới trong LOG, kiểm trực tiếp 925 path/923 hash cho đúng kết quả reviewer: không thiếu path; duy nhất LOG không khớp, 158.173 byte trong manifest so với 28.111 byte hiện tại lúc mở phiên. Prompt cuối so với `prompt_for(inventory())` không khớp, nhưng bản handoff-checks.json lưu cả hai phép kiểm đạt và all_pass=true. Nội dung Prompt chung + G1 vẫn khớp nguồn mẫu ngoài phần điền danh sách file; bản hiện tại dẫn danh sách đầy đủ qua output-files.csv. Vì vậy lỗi hẹp ở chứng cứ bàn giao cho LOG hiện tại, không phải mất inventory, prompt làm neo reviewer hay sai số khoa học. Thêm phản hồi vào LOG tất nhiên tiếp tục đổi hash LOG; không dùng PASS cũ để chứng nhận bản có phản hồi này.

Chưa đủ bằng chứng xác lập phiên/người/thời điểm làm LOG khác bản manifest; file hiện tại hoặc lời dẫn không tự chứng minh nguyên nhân. Có thể có chỉnh rút gọn sau bàn giao hoặc bản lưu thuộc trạng thái trước, nhưng đó chỉ là CANDIDATE. Không tuyên bố lượt kiểm ban đầu sai. Không sửa/khôi phục LOG theo suy đoán. Đồng ý sửa chứng cứ bàn giao sau khi Minh quyết bản LOG nguồn; ưu tiên giữ bản hiện tại có lịch sử phản hồi, thay vì cố dựng lại bản cũ không có nguồn kiểm chứng.

### Đề xuất sửa gom theo file — CHƯA LÀM, cần Minh quyết R1

- `results/T-019/artifact-manifest.json`: bản cũ chứa byte/hash LOG không còn đúng. Sau khi Minh chọn LOG nguồn và duyệt sửa R1, cập nhật byte/hash/danh sách cho bộ bàn giao ở trạng thái mới; không dùng hash cũ để xác nhận bản mới. Trước cập nhật giữ bản cũ tại `results/T-019/handoff-before-R1/artifact-manifest.json` theo luật giữ lượt chạy.
- `results/T-019/handoff-checks.json`: bản cũ all_pass=true chỉ là chứng cứ trạng thái cũ, không xác nhận LOG hiện tại. Sau cùng cập nhật kết quả kiểm theo bộ manifest/prompt tương ứng; chỉ ghi PASS nếu các phép kiểm thực đạt. Giữ nguyên bản cũ tại `results/T-019/handoff-before-R1/handoff-checks.json` trước khi cập nhật.
- `results/T-019/tieu-chi-xong.md`, dòng tiêu chí 8: cũ “Đạt khi bàn giao:LOG6ý/A–H/prompt nguyên văn/all-fileinventory; chỉ dòngT019 STATE; khôngcommit/push” → nháp mới “Inventory và nội dung LOG đủ; chứng cứ hash/prompt của LOG hiện tại có giới hạn R1. Chỉ xác nhận lại bản bàn giao sau khi manifest và phép kiểm tương ứng được cập nhật.” Nếu bản kiểm mới đạt thì ghi trạng thái thực cùng đường dẫn bản mới. Không cần sửa thẻ hoặc các bảng khoa học vì R1.
- Đề xuất trên có thể thêm các bản lưu cũ vào inventory/prompt của lần đóng gói được duyệt; đó là phần đồng bộ của cùng bản bàn giao, không đề xuất một cổng hay vòng review mới. Phiên hiện tại chưa tạo các thư mục/bản lưu này và chưa sửa bất kỳ file kết quả nào.

### Kết thúc phiên phản hồi — đủ sáu ý theo mẫu

1. **Đã làm:** đọc luật/workflow; kiểm chứng R1 bằng file thật trước khi thêm LOG; tự soát có ghi rõ lệch trình tự, có một nhánh chưa đọc REVIEW; điền R1 “đúng — KHÔNG CHẶN” vào bảng cuối REVIEW. Không có finding khoa học mới N1. Để trống “Minh quyết”.
2. **File đã thay đổi:** chỉ `tasks/T-019-the-sock-shop/REVIEW.md` (thêm một dòng trong bảng người làm) và `tasks/T-019-the-sock-shop/LOG.md` (chỉ ghi thêm). Không đổi nội dung reviewer phía trên bảng. Không ghi kết quả, dữ liệu, môi trường, file ngoài repo hoặc STATE; workflow bước 7 yêu cầu chưa sửa file nào khác. Không commit/push.
3. **Kiểm tra và kết quả:** R1 được xác nhận; prompt mẫu/common+G1 chỉ khác phần điền danh sách; inventory đủ; khoa học 27/27 PASS, các kiểm hỗ trợ mô tả ở trên. Kiểm cuối chỉ đọc sẽ đối chiếu prefix LOG/bản reviewer trước bảng và hash toàn bộ file baseline ngoài hai file được phép; không chạy phép kiểm bàn giao có ghi.
4. **Điều chưa chắc/cần Minh quyết:** chưa biết nguyên nhân/người/thời điểm LOG đổi. R1 không chặn khoa học nhưng PASS cũ không xác nhận LOG hiện tại. Minh quyết có sửa R1 theo đề xuất gom file ở trên và chọn bản LOG nguồn; chưa có quyết định sửa trong phiên này. Không có quyết định mới về dataset/dev/test, phương pháp hoặc nhãn.
5. **Bước tiếp theo chính xác:** Minh đọc dòng R1 cuối `tasks/T-019-the-sock-shop/REVIEW.md` và mục đề xuất theo file trong LOG này. Khi Minh duyệt nội dung/phạm vi sửa R1, người làm giữ các bản kiểm cũ, cập nhật bộ chứng cứ cho LOG được chấp thuận và kiểm trạng thái thực; không chạy lại RCA. Trước khi duyệt, không chạy `handoff.py build/verify` vì có ghi kết quả. STATE giữ nguyên theo phạm vi workflow phiên phản hồi.
6. **Lệnh cuối cùng của phiên:** `py -3 -X utf8 -B -` với đoạn kiểm chỉ đọc qua stdin: so hash file baseline ngoài REVIEW/LOG, xác nhận prefix LOG giữ nguyên toàn 28.111 byte lúc mở phiên, prefix reviewer phía trên bảng không đổi, và cột “Minh quyết” trống. Các số hash chỉ dùng trong phép kiểm/baseline của công cụ, không rải trong văn bản. Lệnh verifier khoa học trước đó: `.venv/Scripts/python.exe -X utf8 -B results/T-019/verify_final.py --read-only`.


## Phiên sửa R1 đã được Minh duyệt — 04/10/2026 — Codex — Windows 11/laptop — người làm

**Mở phiên:** đã đọc lại AGENTS, STATE, SPEC, REVIEW, cuối LOG và workflow. HEAD không đổi so với mốc mở task. Kiểm đầu vào hiện tại: đủ 925 đường dẫn của bản bàn giao cũ; ngoài LOG, các hash có ghi đều còn khớp. Thẻ và số liệu giữ nguyên; không có lý do chạy lại phương pháp.

**Quyết định của Minh trong phiên:** Minh nói nguyên văn “chốt đề xuất”, sau bản tóm tắt: giữ manifest/kết quả kiểm cũ; cập nhật danh sách file, dung lượng và hash theo LOG hiện tại; kiểm hồ sơ bàn giao và cập nhật tiêu chí hoàn thành. Đây là quyền sửa R1, không phải đóng task hay chọn dataset. Ghi quyết định trong LOG của task; không ghi nguồn chung bị cấm trong phạm vi T-019.

**Phạm vi và ảnh hưởng đã duyệt:** cập nhật artifact-manifest.json, handoff-checks.json, tieu-chi-xong.md, đồng bộ output-files.csv và chỉ thêm LOG. Tạo đúng hai bản giữ lịch sử trong results/T-019/handoff-before-R1/. Tổng bảy file mới/đổi; không sửa thẻ, số liệu, code, REVIEW, dữ liệu, file ngoài repo hoặc STATE. Nội dung cũ trong LOG giữ nguyên; prompt mới sẽ chứa nguyên văn mẫu chung + G1 và mọi đường dẫn của bộ bàn giao đã bổ sung hai bản giữ lịch sử. Việc cập nhật chỉ xác nhận bản LOG ở cuối lượt sửa này, không hợp thức hóa bản LOG cũ hoặc suy nguyên nhân nó từng lệch.

**Diễn biến:**
- Đã giữ bản artifact-manifest.json và handoff-checks.json trước sửa tại handoff-before-R1/, kiểm byte/hash bản sao khớp nguồn. Hai bản này là chứng cứ lịch sử, không phải chứng nhận cho LOG hiện tại.
- Sẽ cập nhật TC8, danh sách, byte/hash và prompt tương ứng; dùng kiểm bàn giao đã có. Không gọi handoff.py build() vì hàm đó chép lại báo cáo phiên cũ; chỉ dùng inventory/prompt_for và verify để giữ đúng tình trạng đã có REVIEW/R1. Không sửa code kiểm, không chạy RCA/detector, không tải dữ liệu hoặc tái tính kết quả khoa học.


- Đã cập nhật đúng dòng TC8 theo R1. Danh sách bộ bàn giao có thêm hai bản lịch sử; nội dung khoa học, dữ liệu, script và REVIEW giữ nguyên. Kết quả kiểm cuối trỏ tới manifest/check hiện hành, không trỏ hai bản cũ.
- Hoàn tất phần LOG trước khi chốt hash: báo cáo và prompt dưới thuộc lượt sửa R1 đã duyệt. Sau khi hash LOG, không thêm dòng để tránh tự làm chứng cứ vừa sửa lệch trở lại.

**A. Đã làm.** Thực hiện sửa chứng cứ bàn giao R1 theo “chốt đề xuất” của Minh: giữ hai bản cũ, đồng bộ danh sách/byte/hash/prompt với LOG hiện tại và cập nhật TC8. Không coi đây là một lượt phương pháp RCA.

**B. File đã thay đổi.** Bảy file: tasks/T-019-the-sock-shop/LOG.md; results/T-019/{artifact-manifest.json,handoff-checks.json,output-files.csv,tieu-chi-xong.md}; hai file giữ lịch sử results/T-019/handoff-before-R1/{artifact-manifest.json,handoff-checks.json}. Không ghi file ngoài repo hoặc dữ liệu. REVIEW, STATE, SPEC, code, thẻ và bảng số liệu không đổi trong lượt sửa này. LOG chỉ ghi thêm; không commit/push.

**C. Kiểm tra.** Hai bản lịch sử đã kiểm khớp byte/hash với nguồn trước sửa. Kiểm bàn giao cuối bằng handoff.py verify; kết quả từng mục và all_pass ở handoff-checks.json hiện hành. Chỉ coi sửa R1 đạt khi kiểm cuối đạt toàn bộ; không dùng PASS của hai bản lịch sử. Kiểm sau đó chỉ đọc so hash baseline, prefix LOG và dòng TC8 để xác nhận đúng phạm vi. Đây là kiểm file/prompt và nguồn code có sẵn, không tính lại kết quả khoa học hoặc chạy RCA/detector.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** Không có finding mới. Đính chính T003 và giới hạn nhãn nguồn đã nằm trong dinh-chinh-task-cu.md, không sửa lại ở lượt đóng gói này. R1 là sự không khớp chứng cứ bàn giao T019, không phải sai số khoa học.

**E. Chỗ lệch khỏi SPEC và lý do.** Không mở rộng công việc khoa học. Thêm hai bản giữ lịch sử và đồng bộ danh sách/prompt theo đề xuất R1 đã duyệt; không sửa SPEC, không thay code kiểm. Dùng inventory/prompt_for và đóng manifest trực tiếp, không gọi build() để tránh chép lại báo cáo phiên cũ như thể chưa có REVIEW.

**F. Đề xuất tài liệu chung.** Không có đề xuất mới. Các nháp chung cũ giữ nguyên. Quyết định sửa R1 được ghi nguyên lời trong mục phiên này; không thêm lựa chọn nghiên cứu hoặc ghi nguồn chung bị cấm.

**G. Phần chưa kiểm và lý do.** Không xác định nguyên nhân/người/thời điểm LOG từng khác bản cũ; sửa này không khôi phục lịch sử theo suy đoán. Các OPEN khoa học trong thẻ giữ nguyên. Không có phép chạy RCA hay detector nào cần thiết để xử lý R1.

**H. Cần Minh quyết.** Quyền sửa R1 đã có; không xin lại quyền đó. Việc đóng T019/chọn dataset và các lựa chọn G1 vẫn thuộc Minh; lượt sửa này không tự đóng task hoặc commit/push.

**Kết thúc phiên đủ6ý theo mẫu:**
1. Đã làm: xử lý R1 đã duyệt, lưu bản cũ và đồng bộ hồ sơ theo LOG hiện tại; chỉ kết thúc lượt sửa khi kiểm bàn giao cuối đạt.
2. File thay đổi: bảy file nêu ở B. Các byte LOG cũ, REVIEW, số liệu khoa học và nguồn chung được kiểm bảo toàn; không đổi dữ liệu hoặc file ngoài repo.
3. Kiểm tra: nguồn bản sao khớp hash; trạng thái kiểm bản hiện hành ở results/T-019/handoff-checks.json. Bản lưu cũ chỉ chứng minh trạng thái cũ, không chứng nhận LOG mới.
4. Điều chưa chắc/cần Minh: nguyên nhân sai khác LOG cũ chưa xác lập; không ảnh hưởng sửa R1. Không còn phải quyết lại quyền sửa R1, không tự quyết đóng task hoặc dataset.
5. Bước tiếp theo chính xác: xem dòng TC8 trong results/T-019/tieu-chi-xong.md và all_pass của results/T-019/handoff-checks.json để xét hồ sơ T019. Không thêm vòng phản biện hoặc chạy phương pháp chỉ vì sửa chứng cứ bàn giao.
6. Lệnh cuối cùng sẽ chạy: py -3 -X utf8 -B - với đoạn kiểm chỉ đọc qua stdin đối chiếu mọi hash/size, prefix LOG, TC8, hai bản lịch sử và phạm vi file. Lệnh kiểm bàn giao ngay trước đó: py -3 -X utf8 -B results/T-019/handoff.py verify. Không sửa LOG sau khi chốt manifest.

## Prompt phản biện cho Claude — T-019

```text
Bạn là người phản biện độc lập cho task T-019 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-019-the-sock-shop/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-019-the-sock-shop/SPEC.md, tasks/T-019-the-sock-shop/LOG.md, các file đầu ra: 
- D:/RCA-flashticket/tasks/T-019-the-sock-shop/SPEC.md
- D:/RCA-flashticket/tasks/T-019-the-sock-shop/LOG.md
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_4/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_4/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_4/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_3/metrics.parquet
- D:/RCA-flashticket/results/T-019/acquire.py
- D:/RCA-flashticket/results/T-019/acquisition/manifest.json
- D:/RCA-flashticket/results/T-019/acquisition/progress.jsonl
- D:/RCA-flashticket/results/T-019/acquisition-cache-replay-001/manifest.json
- D:/RCA-flashticket/results/T-019/acquisition-cache-replay-001/progress.jsonl
- D:/RCA-flashticket/results/T-019/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/bao-cao-cuoi.md
- D:/RCA-flashticket/results/T-019/build_card.py
- D:/RCA-flashticket/results/T-019/card-measurements.json
- D:/RCA-flashticket/results/T-019/census-cases.csv
- D:/RCA-flashticket/results/T-019/census-cells.csv
- D:/RCA-flashticket/results/T-019/census-summary.json
- D:/RCA-flashticket/results/T-019/de-xuat-tai-lieu-chung.md
- D:/RCA-flashticket/results/T-019/dinh-chinh-task-cu.md
- D:/RCA-flashticket/results/T-019/download-plan.json
- D:/RCA-flashticket/results/T-019/file-inventory.csv
- D:/RCA-flashticket/results/T-019/final-checks.json
- D:/RCA-flashticket/results/T-019/finalize_evidence.py
- D:/RCA-flashticket/results/T-019/handoff-before-R1/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/handoff-before-R1/handoff-checks.json
- D:/RCA-flashticket/results/T-019/handoff-checks-001-failed.json
- D:/RCA-flashticket/results/T-019/handoff-checks.json
- D:/RCA-flashticket/results/T-019/handoff.py
- D:/RCA-flashticket/results/T-019/input-metadata-check.json
- D:/RCA-flashticket/results/T-019/inspect_files.py
- D:/RCA-flashticket/results/T-019/inspection/boundaries.csv
- D:/RCA-flashticket/results/T-019/inspection/cases.json
- D:/RCA-flashticket/results/T-019/inspection/channel-bands.csv
- D:/RCA-flashticket/results/T-019/inspection/channel-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection/entity-rates.csv
- D:/RCA-flashticket/results/T-019/inspection/exclusions-summary.json
- D:/RCA-flashticket/results/T-019/inspection/hash-recheck.json
- D:/RCA-flashticket/results/T-019/inspection/manifest.json
- D:/RCA-flashticket/results/T-019/inspection/paired-entity-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-cases.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-cells.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-summary.csv
- D:/RCA-flashticket/results/T-019/inspection/progress.jsonl
- D:/RCA-flashticket/results/T-019/inspection/quality-refinement.json
- D:/RCA-flashticket/results/T-019/inspection/resources-snapshot.json
- D:/RCA-flashticket/results/T-019/inspection/root-cause-labels.json
- D:/RCA-flashticket/results/T-019/inspection/schemas.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/cases.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/failure.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/progress.jsonl
- D:/RCA-flashticket/results/T-019/inspection-001-failed/schemas.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/script-after-bool-fix.py
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/failed-final-checks-001.json
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-cases.csv
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-cells.csv
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-summary.csv
- D:/RCA-flashticket/results/T-019/ledger-summary.json
- D:/RCA-flashticket/results/T-019/lineage/all-T006-run-commands.json
- D:/RCA-flashticket/results/T-019/lineage/check_lineage.py
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/public-metric-comparisons.json
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/public-time-inventory.json
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/so-ca-da-nhin.csv
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/summary.json
- D:/RCA-flashticket/results/T-019/lineage/download-manifest.json
- D:/RCA-flashticket/results/T-019/lineage/download-plan.json
- D:/RCA-flashticket/results/T-019/lineage/input-file-final-hashes.json
- D:/RCA-flashticket/results/T-019/lineage/local-file-manifest.json
- D:/RCA-flashticket/results/T-019/lineage/local-fse-RE1-SS-overlap.csv
- D:/RCA-flashticket/results/T-019/lineage/outside-files.csv
- D:/RCA-flashticket/results/T-019/lineage/progress.log
- D:/RCA-flashticket/results/T-019/lineage/public-metric-comparisons.json
- D:/RCA-flashticket/results/T-019/lineage/public-time-inventory.json
- D:/RCA-flashticket/results/T-019/lineage/report.md
- D:/RCA-flashticket/results/T-019/lineage/run-manifest.json
- D:/RCA-flashticket/results/T-019/lineage/run-members.csv
- D:/RCA-flashticket/results/T-019/lineage/so-ca-da-nhin.csv
- D:/RCA-flashticket/results/T-019/lineage/source-file-integrity.json
- D:/RCA-flashticket/results/T-019/lineage/summary.json
- D:/RCA-flashticket/results/T-019/lineage/verification.json
- D:/RCA-flashticket/results/T-019/output-files.csv
- D:/RCA-flashticket/results/T-019/runner-source/main.py
- D:/RCA-flashticket/results/T-019/runner-source/manifest.json
- D:/RCA-flashticket/results/T-019/runner-source/plan.json
- D:/RCA-flashticket/results/T-019/so-ca-da-nhin.csv
- D:/RCA-flashticket/results/T-019/sources-audit/architecture-edges.csv
- D:/RCA-flashticket/results/T-019/sources-audit/architecture-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/architecture-root-positions.csv
- D:/RCA-flashticket/results/T-019/sources-audit/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/audit_labels.py
- D:/RCA-flashticket/results/T-019/sources-audit/audit_metadata.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_architecture.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_diagram.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_diagram_metadata.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_sources.py
- D:/RCA-flashticket/results/T-019/sources-audit/diagram-download-plan.json
- D:/RCA-flashticket/results/T-019/sources-audit/diagram-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/diagram-metadata-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/label-audit.json
- D:/RCA-flashticket/results/T-019/sources-audit/network-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/prior-task-relevance-scan.json
- D:/RCA-flashticket/results/T-019/sources-audit/scan_prior_tasks.py
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/Architecture.png
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/hf-info.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/hf-pinned-info.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/rcaeval-tree.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-docs-commit.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-docs-repository.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-docs-tree.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-commit.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-design.md
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-docker-compose.yml
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-README.md
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-repository.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-tree.json
- D:/RCA-flashticket/results/T-019/sources-audit/source-report.md
- D:/RCA-flashticket/results/T-019/sources-audit/source-reuse-checks.json
- D:/RCA-flashticket/results/T-019/sources-audit/ss-cells.csv
- D:/RCA-flashticket/results/T-019/sources-audit/ss-census.csv
- D:/RCA-flashticket/results/T-019/sources-audit/ss-files.csv
- D:/RCA-flashticket/results/T-019/sources-audit/ss-summary.json
- D:/RCA-flashticket/results/T-019/sources-audit/validation.json
- D:/RCA-flashticket/results/T-019/sources-audit/verify_sources_audit.py
- D:/RCA-flashticket/results/T-019/state-finish.json
- D:/RCA-flashticket/results/T-019/state-start.json
- D:/RCA-flashticket/results/T-019/state_row.py
- D:/RCA-flashticket/results/T-019/tai-lap.md
- D:/RCA-flashticket/results/T-019/the-sock-shop.md
- D:/RCA-flashticket/results/T-019/tieu-chi-xong.md
- D:/RCA-flashticket/results/T-019/tu-phan-bien-spec.md
- D:/RCA-flashticket/results/T-019/verify_final.py,
và kết quả `git diff 93f13d4c4a966428177e2acc287d96bc89303e92` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```


## Phiên đóng task — 04/10/2026 — Codex — Windows 11/laptop — người làm

**Mở phiên:** đọc AGENTS, STATE, SPEC, cuối LOG và kiểm bộ bàn giao R1 còn đủ file/hash, all_pass=true. Minh hỏi task đã đóng chưa; người làm trả lời chưa. Minh sau đó nói nguyên văn “DUYỆT”. USER_CONFIRMED: Minh duyệt đóng T-019, không phải duyệt commit/push hoặc chọn dataset.

**Diễn biến:** giữ bản manifest/check trước đóng tại results/T-019/handoff-before-close/; hai bản sao đúng byte. Đọc STATE ngay trong khóa file, thay chính xác duy nhất dòng T-019 thành “Xong (04/10/2026), chưa commit”; đọc lại và xác nhận phần ngoài dòng đó giữ nguyên. Nguồn trạng thái là Minh duyệt và dòng STATE, cập nhật hồ sơ dẫn xuất sau nguồn này. Không sửa SPEC, REVIEW, code, thẻ, bảng số liệu, dữ liệu hoặc nguồn chung khác.

Hồ sơ đóng task sẽ được đồng bộ với LOG cuối; chỉ kiểm file/hash/prompt. Phép kiểm trạng thái dùng “đã đóng theo Minh” thay cho “chờ phản biện” của giai đoạn trước. Code handoff.py giữ nguyên; hàm verify của nó được dùng qua stdin với đúng mệnh đề trạng thái thay theo giai đoạn đóng, không bỏ kiểm trạng thái. Bản trước đóng giữ lại phép kiểm “chờ phản biện” đúng tại thời điểm cũ. Không chạy RCA/detector và không tải dữ liệu.


**A. Đã làm.** Minh duyệt đóng T-019 ngày 04/10/2026. STATE đã chuyển đúng dòng T019 sang Xong, chưa commit. R1 đã sửa đạt trước đó; giữ nguyên phần nghiên cứu, phản biện và phản hồi.

**B. File thay đổi.** Đúng dòng T019 của docs/STATE.md; thêm LOG; đồng bộ results/T-019/{artifact-manifest.json,handoff-checks.json,output-files.csv,tieu-chi-xong.md}; tạo hai bản lịch sử results/T-019/handoff-before-close/{artifact-manifest.json,handoff-checks.json}. Tổng tám file mới/đổi. Không sửa SPEC, REVIEW, code, nguồn chung khác, thẻ, số liệu, dữ liệu hoặc file ngoài repo.

**C. Kiểm tra.** Bản trước đóng đủ hash/size và all_pass=true; hai bản sao đúng byte. STATE đọc ngay trước/sau trong khóa; ngoài dòngT019 giữ nguyên. Kiểm cuối file/hash/prompt và xác nhận STATE đã đóng theo Minh; trạng thái thực từng mục trong handoff-checks.json. Không chạy lại khoa học hoặc thuật toán.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** Không có finding mới. Đính chính và giới hạn nhãn trong các tài liệu T019 trước đó giữ nguyên.

**E. Chỗ lệch khỏi SPEC và lý do.** SPEC mô tả bước bàn giao ở trạng thái chờ phản biện; nay Minh đã duyệt đóng theo AGENTS mục5 bước9. Phép kiểm trạng thái phải kiểm Xong thay vì chờ phản biện. Dùng cùng hàm kiểm có sẵn qua stdin, chỉ thay mệnh đề trạng thái trong bộ nhớ và ghi rõ giai đoạn trong kết quả; không sửa code file hoặc bỏ phép kiểm trạng thái.

**F. Đề xuất tài liệu chung.** Không có đề xuất mới; quyết định duyệt đóng được ghi nguyên lời trong LOG, các nháp chung cũ giữ nguyên theo phạm vi task.

**G. Phần chưa kiểm.** Những OPEN dữ liệu/G1 trong thẻ giữ nguyên, không bị nâng thành DECIDED bởi việc đóng task. Không còn việc được giao nào của T019 chưa hoàn tất.

**H. Cần Minh quyết.** T019 đã đóng, không cần duyệt đóng lại. Chưa có quyền commit/push. Đề xuất nội dung commit khi Minh yêu cầu: docs: hoàn tất thẻ Sock Shop T-019 và xử lý R1. Không tự chọn dataset/chia test hoặc đóng G1.

**Kết thúc phiên đủ6ý theo mẫu:**
1. Đã làm: đóng task theo “DUYỆT” của Minh; cập nhật một dòng STATE và hồ sơ bàn giao, giữ các bản lịch sử.
2. File thay đổi: tám file ở B. LOG chỉ ghi thêm, các dòng STATE khác giữ nguyên; REVIEW và số liệu không đổi.
3. Kiểm tra: xem C và handoff-checks.json bản đóng. Kiểm cuối chỉ đọc đối chiếu hash/size, phạm vi file, prefix LOG, bản lịch sử và STATE ngoài dòng T019.
4. Điều chưa chắc/cần Minh: không còn việc cần quyết để đóng T019. Các quyết định G1 và quyền commit/push là việc riêng, chưa thực hiện.
5. Bước tiếp theo chính xác: dùng thẻ và sổ ca T019 làm đầu vào tổng hợp G1. Nếu Minh yêu cầu kiểm bản đóng, dùng khối Python dưới với py -3 -X utf8 -B -, vì handoff.py verify gốc chỉ kiểm giai đoạn chờ phản biện. Không mở thêm vòng review hoặc chạy RCA để đóng task.
6. Lệnh cuối cùng sẽ chạy: py -3 -X utf8 -B - với kiểm chỉ đọc sau khi chốt manifest. Lệnh kiểm trạng thái đóng ngay trước là cùng lệnh stdin chạy khối dưới; sau chốt hash không thêm LOG để tránh làm lệch bản bàn giao.

Khối kiểm trạng thái đóng (các phép kiểm khác giữ nguyên; ghi handoff-checks.json):

```python
import sys, inspect
sys.path.insert(0, 'results/T-019')
import handoff
source = inspect.getsource(handoff.verify)
old = next(line for line in source.splitlines() if "checks['STATE_row_waiting_review']=" in line)
new = "    checks['STATE_row_closed_by_Minh']=any(x.startswith('| T-019 |') and 'Xong (04/10/2026), chưa commit' in x for x in (ROOT/'docs/STATE.md').read_text(encoding='utf-8').splitlines()) and 'Minh sau đó nói nguyên văn “DUYỆT”' in log"
source = source.replace(old, new)
source = source.replace("dump(OUT/'handoff-checks.json',result);", "result['task_stage']='closed'; result['status_verification']='STATE closed row and Minh approval in LOG; other checks unchanged'; dump(OUT/'handoff-checks.json',result);")
exec(compile(source, 'T019-closed-stage-from-existing-verifier', 'exec'), handoff.__dict__)
handoff.verify()
```

Prompt mẫu và inventory dưới được giữ để kiểm literal/phạm vi bàn giao; không yêu cầu mở một lượt phản biện mới khi task đã đóng.

## Prompt phản biện cho Claude — T-019

```text
Bạn là người phản biện độc lập cho task T-019 của repo D:\RCA-flashticket.
Đọc AGENTS.md trước. Bạn chỉ được ghi đúng một file: tasks/T-019-the-sock-shop/REVIEW.md, theo mẫu tasks/_MAU/REVIEW.md.
Không sửa file nào khác, không commit.

Đọc: tasks/T-019-the-sock-shop/SPEC.md, tasks/T-019-the-sock-shop/LOG.md, các file đầu ra: 
- D:/RCA-flashticket/tasks/T-019-the-sock-shop/SPEC.md
- D:/RCA-flashticket/tasks/T-019-the-sock-shop/LOG.md
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_checkoutservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_currencyservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_emailservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_productcatalogservice_socket_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_cpu_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_delay_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_disk_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_loss_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_mem_3/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_1/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_1/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_2/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_2/metrics.parquet
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_3/inject_time.txt
- D:/RCA-ext/work/T-019/lineage/re2ob/re2ob_recommendationservice_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_carts_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_catalogue_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_orders_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_payment_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_cpu_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_delay_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_disk_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_loss_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_5/inject_time.txt
- D:/RCA-flashticket/data/T-019/re1ss_user_mem_5/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_carts_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_catalogue_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_orders_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_payment_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_cpu_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_delay_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_disk_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_loss_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_mem_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re2ss_user_socket_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_4/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f1_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_4/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f3_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_4/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_4/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_carts_f4_4/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f1_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_1/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_2/root_cause.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f2_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_front-end_f3_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f1_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f3_3/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_1/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_1/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_1/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_2/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_2/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_2/metrics.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_3/inject_time.txt
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_3/logs.parquet
- D:/RCA-flashticket/data/T-019/re3ss_orders_f4_3/metrics.parquet
- D:/RCA-flashticket/results/T-019/acquire.py
- D:/RCA-flashticket/results/T-019/acquisition/manifest.json
- D:/RCA-flashticket/results/T-019/acquisition/progress.jsonl
- D:/RCA-flashticket/results/T-019/acquisition-cache-replay-001/manifest.json
- D:/RCA-flashticket/results/T-019/acquisition-cache-replay-001/progress.jsonl
- D:/RCA-flashticket/results/T-019/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/bao-cao-cuoi.md
- D:/RCA-flashticket/results/T-019/build_card.py
- D:/RCA-flashticket/results/T-019/card-measurements.json
- D:/RCA-flashticket/results/T-019/census-cases.csv
- D:/RCA-flashticket/results/T-019/census-cells.csv
- D:/RCA-flashticket/results/T-019/census-summary.json
- D:/RCA-flashticket/results/T-019/de-xuat-tai-lieu-chung.md
- D:/RCA-flashticket/results/T-019/dinh-chinh-task-cu.md
- D:/RCA-flashticket/results/T-019/download-plan.json
- D:/RCA-flashticket/results/T-019/file-inventory.csv
- D:/RCA-flashticket/results/T-019/final-checks.json
- D:/RCA-flashticket/results/T-019/finalize_evidence.py
- D:/RCA-flashticket/results/T-019/handoff-before-close/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/handoff-before-close/handoff-checks.json
- D:/RCA-flashticket/results/T-019/handoff-before-R1/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/handoff-before-R1/handoff-checks.json
- D:/RCA-flashticket/results/T-019/handoff-checks-001-failed.json
- D:/RCA-flashticket/results/T-019/handoff-checks.json
- D:/RCA-flashticket/results/T-019/handoff.py
- D:/RCA-flashticket/results/T-019/input-metadata-check.json
- D:/RCA-flashticket/results/T-019/inspect_files.py
- D:/RCA-flashticket/results/T-019/inspection/boundaries.csv
- D:/RCA-flashticket/results/T-019/inspection/cases.json
- D:/RCA-flashticket/results/T-019/inspection/channel-bands.csv
- D:/RCA-flashticket/results/T-019/inspection/channel-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection/entity-rates.csv
- D:/RCA-flashticket/results/T-019/inspection/exclusions-summary.json
- D:/RCA-flashticket/results/T-019/inspection/hash-recheck.json
- D:/RCA-flashticket/results/T-019/inspection/manifest.json
- D:/RCA-flashticket/results/T-019/inspection/paired-entity-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-cases.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-cells.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection/probe-summary.csv
- D:/RCA-flashticket/results/T-019/inspection/progress.jsonl
- D:/RCA-flashticket/results/T-019/inspection/quality-refinement.json
- D:/RCA-flashticket/results/T-019/inspection/resources-snapshot.json
- D:/RCA-flashticket/results/T-019/inspection/root-cause-labels.json
- D:/RCA-flashticket/results/T-019/inspection/schemas.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/cases.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/failure.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/progress.jsonl
- D:/RCA-flashticket/results/T-019/inspection-001-failed/schemas.json
- D:/RCA-flashticket/results/T-019/inspection-001-failed/script-after-bool-fix.py
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/failed-final-checks-001.json
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-cases.csv
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-cells.csv
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-exclusions.csv
- D:/RCA-flashticket/results/T-019/inspection-summary-001-before-paired/probe-summary.csv
- D:/RCA-flashticket/results/T-019/ledger-summary.json
- D:/RCA-flashticket/results/T-019/lineage/all-T006-run-commands.json
- D:/RCA-flashticket/results/T-019/lineage/check_lineage.py
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/public-metric-comparisons.json
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/public-time-inventory.json
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/so-ca-da-nhin.csv
- D:/RCA-flashticket/results/T-019/lineage/compare-run001/summary.json
- D:/RCA-flashticket/results/T-019/lineage/download-manifest.json
- D:/RCA-flashticket/results/T-019/lineage/download-plan.json
- D:/RCA-flashticket/results/T-019/lineage/input-file-final-hashes.json
- D:/RCA-flashticket/results/T-019/lineage/local-file-manifest.json
- D:/RCA-flashticket/results/T-019/lineage/local-fse-RE1-SS-overlap.csv
- D:/RCA-flashticket/results/T-019/lineage/outside-files.csv
- D:/RCA-flashticket/results/T-019/lineage/progress.log
- D:/RCA-flashticket/results/T-019/lineage/public-metric-comparisons.json
- D:/RCA-flashticket/results/T-019/lineage/public-time-inventory.json
- D:/RCA-flashticket/results/T-019/lineage/report.md
- D:/RCA-flashticket/results/T-019/lineage/run-manifest.json
- D:/RCA-flashticket/results/T-019/lineage/run-members.csv
- D:/RCA-flashticket/results/T-019/lineage/so-ca-da-nhin.csv
- D:/RCA-flashticket/results/T-019/lineage/source-file-integrity.json
- D:/RCA-flashticket/results/T-019/lineage/summary.json
- D:/RCA-flashticket/results/T-019/lineage/verification.json
- D:/RCA-flashticket/results/T-019/output-files.csv
- D:/RCA-flashticket/results/T-019/runner-source/main.py
- D:/RCA-flashticket/results/T-019/runner-source/manifest.json
- D:/RCA-flashticket/results/T-019/runner-source/plan.json
- D:/RCA-flashticket/results/T-019/so-ca-da-nhin.csv
- D:/RCA-flashticket/results/T-019/sources-audit/architecture-edges.csv
- D:/RCA-flashticket/results/T-019/sources-audit/architecture-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/architecture-root-positions.csv
- D:/RCA-flashticket/results/T-019/sources-audit/artifact-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/audit_labels.py
- D:/RCA-flashticket/results/T-019/sources-audit/audit_metadata.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_architecture.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_diagram.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_diagram_metadata.py
- D:/RCA-flashticket/results/T-019/sources-audit/capture_sources.py
- D:/RCA-flashticket/results/T-019/sources-audit/diagram-download-plan.json
- D:/RCA-flashticket/results/T-019/sources-audit/diagram-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/diagram-metadata-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/label-audit.json
- D:/RCA-flashticket/results/T-019/sources-audit/network-manifest.json
- D:/RCA-flashticket/results/T-019/sources-audit/prior-task-relevance-scan.json
- D:/RCA-flashticket/results/T-019/sources-audit/scan_prior_tasks.py
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/Architecture.png
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/hf-info.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/hf-pinned-info.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/rcaeval-tree.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-docs-commit.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-docs-repository.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-docs-tree.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-commit.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-design.md
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-docker-compose.yml
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-README.md
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-repository.json
- D:/RCA-flashticket/results/T-019/sources-audit/snapshots/sock-shop-tree.json
- D:/RCA-flashticket/results/T-019/sources-audit/source-report.md
- D:/RCA-flashticket/results/T-019/sources-audit/source-reuse-checks.json
- D:/RCA-flashticket/results/T-019/sources-audit/ss-cells.csv
- D:/RCA-flashticket/results/T-019/sources-audit/ss-census.csv
- D:/RCA-flashticket/results/T-019/sources-audit/ss-files.csv
- D:/RCA-flashticket/results/T-019/sources-audit/ss-summary.json
- D:/RCA-flashticket/results/T-019/sources-audit/validation.json
- D:/RCA-flashticket/results/T-019/sources-audit/verify_sources_audit.py
- D:/RCA-flashticket/results/T-019/state-finish.json
- D:/RCA-flashticket/results/T-019/state-start.json
- D:/RCA-flashticket/results/T-019/state_row.py
- D:/RCA-flashticket/results/T-019/tai-lap.md
- D:/RCA-flashticket/results/T-019/the-sock-shop.md
- D:/RCA-flashticket/results/T-019/tieu-chi-xong.md
- D:/RCA-flashticket/results/T-019/tu-phan-bien-spec.md
- D:/RCA-flashticket/results/T-019/verify_final.py,
và kết quả `git diff 93f13d4c4a966428177e2acc287d96bc89303e92` nếu có.
Nguồn đối chiếu đề tài: docs/reference/sources/DT18-de-tai-va-nhiem-vu.md và docs/reference/sources/advisor-2026-09-23.md.

Nhiệm vụ: tìm lỗi ảnh hưởng tới (1) tính đúng của lập luận, phương pháp hoặc kết quả,
hoặc (2) độ khớp với DT18 và hướng dẫn của cô.
Kiểm cụ thể: đầu ra có đạt "Tiêu chí xong" trong SPEC không; có ghi ra ngoài "Phạm vi ghi" không;
số trong văn bản có khớp file kết quả không (chạy lại nếu rẻ); có nhãn nào lọt vào phương pháp không;
có lựa chọn nào thiếu lý do trong docs/WHY.md không; có lặp sai lầm nào trong docs/LESSONS.md không.

Bổ sung yêu cầu phản biện:
1. Phân biệt yêu cầu của DT18/cô, quyết định của Minh, đề xuất và ứng viên. Đối chiếu các câu “chọn”, “sẽ”, “dùng để” với thời điểm bằng chứng phải có. Tìm trường hợp kế hoạch nói chọn sau thực nghiệm nhưng đã cam kết cơ chế trước đó.
2. Kiểm lập luận trong WHY, không chỉ kiểm có mục “tại sao”. Tìm phương án đối lập giả và kết luận mạnh hơn bằng chứng. Khi nêu lỗi, xét cả đoạn có thể phản bác finding đó.
3. Khi tính đúng phụ thuộc vào phương pháp hoặc benchmark được dẫn, đọc bài/code chính thức ở revision liên quan. Lần theo phần chọn đầu vào, tiền xử lý, dùng nhãn, xử lý ngoại lệ và lưu kết quả. Không mặc định code chính thức hoặc bản mới nhất cho kết quả hợp lệ.
4. Lần theo thông tin đồ thị và nhãn từ đầu vào → đặc trưng → điểm bất thường → tập ứng viên → xếp hạng. Với đối chứng “không đồ thị”, xác định thông tin cấu trúc còn lại và phạm vi kết luận phép so sánh thực sự hỗ trợ.
5. Phân biệt lỗi đã xảy ra, mâu thuẫn thiết kế và nguy cơ chưa kiểm. Không biến OPEN thành lỗi chỉ vì chưa hoàn thành công việc thuộc gói sau. Không yêu cầu làm xong P4 ngay tại G0.
6. Mỗi finding ghi rõ bước chịu ảnh hưởng, bằng chứng, hậu quả và sửa tối thiểu. Không tìm cho đủ số lượng. Không đề xuất thêm quy trình, cổng hoặc phép kiểm “cho chắc”. Không chạy thực nghiệm mới hay mở dữ liệu khóa ngoài phạm vi được phép.

Không báo: chính tả, văn phong, đề xuất thêm quy trình, thêm phép kiểm "cho chắc".
Nếu không có lỗi đáng kể, nói thẳng là không có. Không cần tìm cho đủ số lượng.

Mỗi điểm: mức CHẶN hoặc KHÔNG CHẶN; ở đâu; sai gì; bằng chứng (trích dẫn, số, phản ví dụ, lệnh đã chạy); đề xuất sửa ngắn.
Tiếng Việt, câu ngắn.

Danh sách phương pháp có phủ đủ các họ không; hồ sơ kỹ thuật có đúng với bài và code gốc không
(kiểm ngẫu nhiên ít nhất 2 phương pháp); dataset đã chọn có phân xử được RQ1, RQ3 không;
cách chia dev/test có lộ đáp án không; có đường nào để nhãn lọt vào phương pháp không.
```
