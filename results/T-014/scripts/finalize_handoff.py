"""Close only after the bounded EC2 attempt has a terminal status."""
import json,re,csv
from pathlib import Path
repo=Path('D:/RCA-flashticket');out=repo/'results/T-014';log=repo/'tasks/T-014-ho-so-circa/LOG.md'
status_path=out/'runs/ec2-default-permuted/status.json'
if not status_path.exists():raise SystemExit('EC2 permutation still pending; do not close handoff.')
status=json.loads(status_path.read_text());cost=json.loads((out/'runs/chi-phi-tong.json').read_text())
if status['complete']:
    summary='FullPC permutation đã hoàn tất; so sánh graph/score theo identity ở runs/pc-full-permutation-comparison.json.'
elif not (status_path.parent/'progress.jsonl').exists():
    summary=f"Full PC permutation chưa khởi worker: chờ EC2 có job khác tới hết {status['elapsed']:.3f} giây ngân sách. Chỉ parent theo dõi ps/free, không chạy song song hai tiến trình nặng."
else:
    summary=f"FullPC permutation không hoàn tất trong{status['elapsed']:.3f}s (gồm chờ/pause); giữ progress/partial/error, không gọi scorer permutation là PC discovery permutation."
report=f'''# Báo cáo cuối T-014 — 04/10/2026

**A. Đã làm.** Viết hai hồ sơ CIRCA đủ chín mục. Dựng đồ thị kiến trúc từ trace trước mốc và kiểm schema của 30 ca dev. Hai ví dụ được tính lại độc lập từ dữ liệu gốc tới từng điểm số. PC mặc định chạy trên EC2 với 600×273 đầu vào và trả 270 điểm; kiến trúc trả 272 điểm. Dùng linear RHT làm tham chiếu chung, chạy DA riêng để kiểm cơ chế. Đây là lựa chọn P1, chờ WHY, chưa chốt P3.

**B. File đã thay đổi.** SPEC/LOG của T-014; results/T-014/; bốn file src/circa_kien_truc/; đúng dòng T-014 của STATE. Ngoài repo: D:/RCA-ext/work/T-014/ và D:/RCA-ext/envs/T-014-main/. Trên EC2: /home/ubuntu/rca/T-014/, gồm đúng một ca dev, script, cache, thư mục tạm và kết quả. Mỗi file có một dòng trong manifest-files.csv. Không sửa task cũ, tài liệu quyết định chung hoặc môi trường/source dùng chung. Không commit hay push.

**C. Kiểm tra đã chạy và kết quả.** Kiến trúc/PC khớp 2176/2160 thành phần số học và 1088/1080 mảng raw. CIRCA gốc trên cùng graph/context khớp 272 điểm RHT/DA trong tolerance; đảo parents chủ động cũng khớp. Native YAML/factory khớp 30/30 ca. Đổi hashseed làm đổi cạnh của 24 graph kiến trúc cyclic; trên PC cùng graph, RHT không đổi vượt tolerance nhưng DA đổi 25/270 điểm. Fixtures kiểm graph rỗng, singular, constant, alpha/depth, parser và fallback đã có đầu ra. **Đối chứng bình thường không đạt:** kiến trúc có 60/270 điểm≥3; PC dùng graph fault lưu sẵn có 76/268, chưa thay full normal-PC. PC mặc định mất 1796,269 giây; RHT 0,832 giây; RSS quan sát khoảng 5,2 GB. Thời gian có instrumentation trên máy dùng chung, không phải benchmark sạch. {summary} Accounting PC gồm toàn bộ reservation kiểm khác là {cost['PC_dataset_accounting_with_full_other_reservation_seconds']:.3f} giây≤10800. Audit fseOB chỉ có timer từng khối; tổng chính xác để null.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** Có năm điểm: parser tên không có underscore gây lỗi/fallback; phạm vi hashseed T006 chỉ bốn ca; PC cô lập mất ứng viên và có thể trả rank rỗng; directed PC bị đảo hướng; mô tả “chỉ khác graph/DA” thiếu SVR, cửa sổ và coverage. Đã triển khai fixtures, so scorer/graph và factorial trên 25 ca MEM được phép. Bằng chứng, hệ quả và đoạn cũ→mới ở dinh-chinh-task-cu.md. K1 cần tách cutoff trong lời mô tả paper khỏi output code. Không tự sửa số/file cũ. Đã census tài liệu T000–T012 và đọc sâu phần CIRCA/chấm liên quan; không tuyên bố đã audit mọi artifact của mọi phương pháp.

**E. Chỗ lệch khỏi SPEC và lý do.** Các thay đổi ghi nối cuối SPEC: metadata T002 cho 29 mốc thiếu; chuẩn tiền xử lý runner; kiểm MEM25/factorial; pause/resume đúng worker của T014; đổi cách kiểm YAML sau lỗi harness; giữ graph thiếu hashseed rồi dựng canonical seed0; thêm full PC permutation khi default xong; thêm so scorer gốc và đảo parents. Không đổi thiết kế P3 theo accuracy hoặc đọc ca TT ngoài danh sách.

**F. Đề xuất cho tài liệu chung.** de-xuat-tai-lieu-chung.md có nháp nguyên văn cho DECISIONS, WHY, STATE và K1: ủy quyền, scorer chung, mapping/coverage, thông tin cửa sổ vào metric membership, và cutoff paper/code. Đính chính T001/T005/T006 chờ Minh quyết. Chưa sửa file chung hay thêm quy trình/cổng.

**G. Phần chưa kiểm và lý do.** Chưa tái lập giao thức sinh số MEM công bố 0,74: R-linear đạt 0,864; SVR 0,960; linear+DA 0,856; SVR+DA 0,864. Backend/hướng/coverage đổi cùng nhau nên chưa quy toàn khoảng lệch cho một nguyên nhân. R userspace đã chạy được. Full normal-PC, full permutation nếu status chưa complete, và alpha/depth toàn TT còn thiếu bằng chứng vì máy/ngân sách. Graph cached và toy không thay các phép kiểm đó. Runtime sạch, calibration, prevalence và toàn factory Oracle chưa được kiểm. Timer/byte tải còn thiếu được ghi cụ thể, không điền số giả. Giả định, khi nào sai và phép phân xử nằm ở kiem-tra-va-doi-chieu-spec.md.

**H. Cần Minh quyết.** Duyệt hoặc sửa nháp tài liệu chung. Sau phản biện G1, chọn regressor/DA, candidate coverage và timing cửa sổ cho P3. Nếu cần kiểm tiếp giao thức công bố hoặc học lại PC, Minh quyết phạm vi/ngân sách theo Q40; không tự reset ngân sách bằng task mới. Chưa cần mở test hoặc đổi thiết kế đồ thị.
'''
(out/'bao-cao-cuoi.md').write_text(report,encoding='utf-8')
proposal='''
## Trạng thái phép kiểm EC2 cuối

'''+summary+f" Tổng các defaultattempt (tính cả chờ)={cost['default_total_seconds']:.3f}s; capdepth0={cost['capped_PC_actual_seconds']:.3f}s. Trạng thái terminal được copyback cùngqueue/progress. Không còn worker T014 chạy sau bàn giao.\n"
p=out/'kiem-tra-va-doi-chieu-spec.md'
text=p.read_text(encoding='utf-8').replace('cần task/phạmvi/ngânsách riêng đượcMinh giao sauG1.','Minh quyết phépkiểm tiếp phù hợpQ40; nếu vượtQ40 cần ngoại lệ rõ, không resetngânsách theo task.')
if '## Trạng thái phép kiểm EC2 cuối' not in text:p.write_text(text+proposal,encoding='utf-8')
template=(repo/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
common=re.search(r'## Prompt chung.*?```text\n(.*?)\n```',template,re.S).group(1)
g1=re.search(r'\*\*G1 — phương pháp, dataset, cách chia:\*\*\n```text\n(.*?)\n```',template,re.S).group(1)
files='results/T-014/manifest-files.csv (mọi file mỗi dòng gồm scope task/results/source/outside_work/outside_environment/ec2, và dòng STATE T014); results/T-014/README.md; ho-so-circa-pc.md; ho-so-circa-kien-truc.md; yeu-cau-dau-vao.csv; ca-da-chay.csv; dinh-chinh-task-cu.md; de-xuat-tai-lieu-chung.md; moi-truong.md; kiem-tra-va-doi-chieu-spec.md; bao-cao-cuoi.md; mọi file paper/, audit/, graphs/, runs/, scripts/ trong manifest; src/circa_kien_truc/__init__.py, builder.py, scoring.py, README.md; mọi file D:/RCA-ext/work/T-014/ và D:/RCA-ext/envs/T-014-main/ trong manifest; mọi file /home/ubuntu/rca/T-014/ trên EC2 trong manifest. Nguồn code: CIRCA D:/RCA-ext/work/T-014/CIRCA revision0215e1880096aa02a305c697f1c23cac4600ebd2; RCAEval D:/RCA-ext/src/RCAEval revision259ea4167160256a74ad30004aa3d96a998c846e. Cách chạy: results/T-014/moi-truong.md và scripts/verify_outputs.py --read-only'
common=common.replace('<T-xxx>','T-014').replace('<T-xxx-tên>','T-014-ho-so-circa').replace('<danh sách>',files).replace('<commit gốc>','93f13d4c4a966428177e2acc287d96bc89303e92')
closing='''

## Kết thúc phiên — 04/10/2026 — Codex người làm

1. Đã làm gì: xem đầy đủ báo cáo A–H dưới; phần P1 khả thi đã triển khai, không chuyển OPEN thành DECIDED.
2. File đã thay đổi: SPEC/LOG, results/T014, src/circa_kien_truc, dòng STATE T014, ownwork/env/EC2; fullfilemanifest ở results/T-014/manifest-files.csv.
3. Kiểm tra đã chạy và kết quả: số học/raw/source/builder/cached-repeat PASS theo phạmvi, negativecontrol FAIL; sources và tiêu chí ở verification-final/scope-and-sources/đốichiếuSPEC.
4. Điều chưa chắc/cần Minh quyết: giao thức côngbố và phép kiểm chưa hoàn tất do máy/ngânsách; nhápcommon vàP3CANDIDATE ở F/G/H.
5. Bước tiếp theo chính xác: Minh mở phiên Claude phảnbiện, đọc SPEC/LOG và mọi file trong manifest; chỉ ghi tasks/T-014-ho-so-circa/REVIEW.md. Đọc results/T-014/moi-truong.md trước chạy nhẹ. Lệnh kiểm nhẹ: D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-014/scripts/verify_outputs.py --read-only; không tự chạy lạiPC haymởdatamới. SauREVIEW, người làm phản hồi đúngbước7.
6. Lệnh cuối cùng trước ghi kết thúc: D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-014/scripts/verify_outputs.py. Các lệnh bàn giao tiếp theo đã định: update_state.py 'chờ phản biện (04/10/2026)', check_scope_sources.py, verify_outputs.py, manifest_files.py; chúng chỉ ghi kếtquảkiểm/dòngSTATE/manifest, không rerunphươngpháp.

'''+report+'''

## Prompt phản biện cho Claude — 04/10/2026

```text
'''+common+'\n\n'+g1+'\n```\n'
with log.open('a',encoding='utf-8') as f:f.write(closing)
print('Wrote A–H, six-item session close, and exact common/G1 review prompt. STATE transition is next.')
