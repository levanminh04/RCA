"""Publish terminal evidence, not a successful-looking checklist, for resumed T014."""
import json,csv,re,hashlib,subprocess
from pathlib import Path
from datetime import datetime
root=Path('D:/RCA-flashticket');out=root/'results/T-014';log=root/'tasks/T-014-ho-so-circa/LOG.md'
statuses={mode:json.loads((out/'runs'/('ec2-2-'+mode)/'status.json').read_text()) for mode in ['permuted','normal']}
cost=json.loads((out/'runs/followup-cost.json').read_text());assert cost['under_limit']
comparisons={mode:json.loads((out/'runs'/('ec2-2-'+mode)/'comparison.json').read_text()) if statuses[mode]['complete'] else None for mode in statuses}
independent={}
for mode,c in comparisons.items():
    if c:
        for stage,name in [('score','comparison.json'),('raw','window-comparison.json')]:
            p=(out/'runs/normal-official-independent-linux/comparison.json' if mode=='normal' and stage=='score' else out/'paper/followup-normal-official-raw/window-comparison.json' if mode=='normal' else out/'paper'/('followup-'+mode+'-'+stage)/name);independent[mode+'_'+stage]=json.loads(p.read_text());assert independent[mode+'_'+stage]['pass']
old=json.loads((out/'runs/chi-phi-tong-truoc-tiep-tuc.json').read_text());old['historical_accounting_included_queue_seconds']=old['PC_dataset_accounting_with_full_other_reservation_seconds']
old['budget_policy_current']='Minh requested continuation after proposal to count actual worker wall; queue without worker excluded, no reset by host; reserved900s retained'
old['PC_dataset_accounting_with_full_other_reservation_seconds']=cost['total_with_reservation_seconds'];old['PC_dataset_under_3h_with_reservation']=cost['under_limit'];old['followup']=cost
old['excluded_historical_queue_seconds']=4171.454560293
old['audit_fseOB']['followup_factor_scoring_seconds']=json.loads((out/'audit/graph-factor-summary.json').read_text())['elapsed_diagnostic_seconds']
(out/'runs/chi-phi-tong.json').write_text(json.dumps(old,indent=2))
sentences=[]
for mode in ['permuted','normal']:
    s=statuses[mode];c=comparisons[mode]
    if c:
        events=[json.loads(x) for x in (out/'runs'/('ec2-2-'+mode)/'progress.jsonl').read_text().splitlines()];pc=next(r['pc_elapsed'] for r in events if r.get('event')=='PC_end')
        if mode=='permuted':line=f"Đảo cột/học lại PC: hoàn tất {pc:.3f}s; {c['changed_endpoint_pair_count']} cặp endpoint đổi, {c['changed_score_count']} điểm đổi vượt tolerance; cùng candidate={c['candidate_set_identical']}."
        else:line=f"Full normal-PC học trên {c['shape'][0]}×{c['shape'][1]} điểm/cột trước tiêm: hoàn tất {pc:.3f}s; {c['scores_ge3']}/{c['scored']} điểm≥3, top {c['top'][0]}={c['top'][1]:.8g}."
        line+=(' Direct RHT/snapshot, số học độc lập và raw arrays đều PASS.' if mode=='permuted' else ' RHT chính thức lặp lại cùng máy khớp từng điểm; số học độc lập trên EC2 và raw arrays PASS. Đối chiếu laptop FAIL ở bốn metric; xem normal-doi-chieu-so-hoc.md.')
    else:line=f"{mode}: đã khởi worker và chạy {s['active_wall_seconds']:.3f}s; chưa hoàn tất, timeout={s.get('timeout')}. Chưa có đồ thị/điểm đầy đủ để kết luận phép kiểm này."
    sentences.append(line)
summary='\n\n'.join(sentences)
text=f'''# Bổ sung T-014 trên EC2 thứ hai — 04/10/2026

Minh yêu cầu tiếp tục hai phép kiểm còn thiếu trên một ca dev đã chọn trước khi xem điểm. Máy 3.26.62.217 có 2 vCPU, RAM 7,6 GiB, không có swap. Nguồn code, dữ liệu và phiên bản thuật toán khớp. Python cùng phiên bản 3.12.3, nhưng bản biên dịch khác máy trước. Phép đối chiếu này đồng thời đổi thứ tự cột và đổi máy. Nếu kết quả khác, chưa thể quy riêng cho thứ tự cột khi chưa có lượt tham chiếu trên cùng máy. Đây là kiểm một ca, không phải benchmark 30 ca.

{summary}

Nguồn từng khối: `runs/ec2-2-permuted/status.json`, `progress.jsonl`, `comparison.json` (nếu hoàn tất); tương tự ở `ec2-2-normal/`. Script: `ec2_followup.py`, `compare_followup.py`; tính lại điểm và chuẩn bị dữ liệu độc lập ở `paper/followup-*/`. Mọi lượt lỗi, timeout và log dựng môi trường đều được giữ.

Ngân sách thực tế: thời gian tiến trình cũ {cost['old_worker_wall_seconds']:.3f}s + tiến trình mới {cost['new_worker_wall_seconds']:.3f}s + dự phòng {cost['reservation_seconds']:.0f}s = {cost['total_with_reservation_seconds']:.3f}s ≤10800s. Thời gian chờ lịch sử 4171,455s không có tiến trình tính toán được ghi riêng. Trước đây phần này bị tính vào ngân sách, dẫn tới bàn giao thiếu. Không đặt lại ngân sách khi đổi máy. Nguồn: `runs/followup-cost.json`; cách tính cũ giữ ở `chi-phi-tong-truoc-tiep-tuc.json`.

Như đối chứng kiến trúc, dữ liệu trước mốc tiêm là một proxy (đại diện) cho bình thường, chưa được xác nhận độc lập là hoàn toàn khỏe. Phương pháp luôn xếp hạng khi có điểm; score≥3 không tự chứng minh có nguyên nhân sự cố. Không chỉnh cửa sổ, alpha hoặc độ sâu để làm đối chứng đạt. Nếu lượt PC bình thường timeout, đồ thị đã học từ sự cố không thay thế được phép kiểm này.

Điều tra MEM25 bổ sung: trên cùng đồ thị R-pcalg, giữ hoặc bỏ nút cô lập đều cho Avg5=0,864 ở chiều gốc, và 0,896 khi đảo chiều. Tách được tác động của chiều cạnh trong điều kiện này: +0,032. Bỏ nút cô lập không đổi điểm tổng trong nhóm này. Chưa tái lập mốc 0,740, nên không quy hết khoảng lệch 0,148 cho một lỗi. Số công bố có hai chữ số thập phân; 0,148 là chênh với số hiển thị, không phải số gốc của bài chính xác tới ba chữ số. Nguồn: `audit/graph-factor-summary.json`, `graph-factor-verification.json`.

**Cơ chế nhạy thứ tự đã kiểm riêng.** Trên cùng máy, fixture bốn node có cùng skeleton và separating sets theo tên nhưng chỉ đảo thứ tự node cho hai hướng khác nhau. Với `uc_priority=2`, code ưu tiên collider đã được định hướng trước, trong khi danh sách triple được duyệt theo chỉ số node. `stable=True` chỉ điều chỉnh bước xóa cạnh skeleton, không bảo đảm quy tắc xử lý xung đột này bất biến theo thứ tự. Rule tính tay độc lập khớp kết quả hàm chính thức. Đây là cơ chế đã xác nhận; không phải replay toàn bộ separating sets của ca Train Ticket, nên chưa quy riêng mọi cặp đổi hướng cho nó. Nguồn: `paper/orientation-order-fixture.json`; causal-learn0.1.3.8 `PC.py:25–26,111–116`, `UCSepset.py:40–42,95–111`, `GraphClass.py:92–107`.
'''
(out/'bo-sung-ec2.md').write_text(text,encoding='utf-8')
pcp=out/'ho-so-circa-pc.md';ptext=pcp.read_text(encoding='utf-8')
ptext+='\n\n**Bổ sung kiểm EC2₂ (04/10, trạng thái hiện hành).** '+summary.replace('\n\n',' ')+' Chi phí và giới hạn đối chiếu host ở `bo-sung-ec2.md`; bằng chứng từngkhối ở `runs/ec2-2-permuted/`, `runs/ec2-2-normal/`, `paper/followup-*/`. Các nhận xét chưakiểm trong đoạn trước là trạng thái trước khi Minh yêu cầu tiếp tục; trạng thái hiện hành của hai phép kiểm là đoạn này.\n'
pcp.write_text(ptext,encoding='utf-8')
csvpath=out/'yeu-cau-dau-vao.csv'
with csvpath.open(encoding='utf-8-sig',newline='') as f:r=csv.DictReader(f);fields=r.fieldnames;rows=list(r)
for row in rows:
    if row['bien_the'].startswith('PC-'):
        row['ghi_chu']=re.sub(r'normal-PC graph học riêng chua_kiem:[^;]*;', '',row['ghi_chu'])
        row['ghi_chu']+='; kiểm tiếp EC2₂: '+summary.replace('\n\n',' ')+' nguồn bo-sung-ec2.md'
with csvpath.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
(out/'kiem-tra-va-doi-chieu-spec.md').write_text((out/'kiem-tra-va-doi-chieu-spec.md').read_text(encoding='utf-8')+'\n\n## Kiểm bổ sung theo chỉ dẫn tiếp tục của Minh\n\n'+summary+'\n\nNguồn/trạng thái hiện hành: bo-sung-ec2.md; runs/followup-cost.json. Các ghi thiếu ngân sách ở bảng trước là trạng thái lịch sử trước việc sửa accounting queue. Giới hạn3hactual vẫn giữ. Kiểmfactor MEM25 đã làm thêm; independentrecount100config PASS.\n',encoding='utf-8')
(out/'moi-truong.md').write_text((out/'moi-truong.md').read_text(encoding='utf-8')+'\n\n## EC2 thứ hai: môi trường kiểm tiếp\n\nPython3.12.3portable được copy từT015 chỉđọc sangT014/python; uv vàenv/source/wheels/cache/tmp đều riêng trongT014.36gói ghim ởrequirements-followup.txt, version thuậttoán trùngEC2₁, networkx2.5 cho hàmrht trựctiếp; adapter snapshot local2.8.8 đượcso tới từngscore. Khôngapt/admin/hệthống. Chạy ec2_followup_setup.sh, ec2_followup.py preflight/supervisor. Sourcegitarchive đúngrevision,5criticalfile vàrawSHA khớp. WheelPyPI giữ compressedfile/metadata/SHA/byte, retryreuse; inventory gắn host3.26.62.217. Cáclượtsetup lỗi giữnguyên. Ngân sáchmethod táchqueueno-worker sauMinhyêucầutiếptục; không tăngtrần3hactual. Xem bo-sung-ec2.md vàenvironment-ec2-2.json.\n',encoding='utf-8')
(out/'README.md').write_text((out/'README.md').read_text(encoding='utf-8')+'\n\nKiểm tiếp theo chỉ dẫn Minh: [bổ sungEC2₂](bo-sung-ec2.md). Đây là trạng thái hiện hành của permutation/fullnormalPC; cáclogquaymáy cũ đượcgiữ.\n',encoding='utf-8')
report=f'''# Báo cáo cuối T-014 — bổ sung 04/10/2026

**A. Đã làm.** Hai hồ sơ đủ chín mục. Bộ dựng đồ thị kiến trúc đã kiểm trên schema của 30 ca dev. Hai ví dụ được tính lại độc lập tới từng điểm số. PC mặc định ở quy mô 273 cột đã chạy xong. Bổ sung hai phép kiểm trên cùng một ca bằng EC2 thứ hai. {summary}

**B. File đã thay đổi.** SPEC/LOG, results/T-014/, src/circa_kien_truc/ (từ lượt trước), đúng dòng T-014 của STATE. Ngoài repo: D:/RCA-ext/work/T-014/ và môi trường T-014-main. Trên hai EC2, chỉ ghi ~/rca/T-014/; máy thứ hai có runtime, source, env, wheel, cache, thư mục tạm, script và một ca dev. Manifest ghi từng file và máy. File nháp 2B tạo nhầm tại D:/RCA-flasicket/results/T-014/scripts/placeholder.txt đã được báo và xóa; còn các thư mục rỗng, không còn file ngoài phạm vi. Không commit/push.

**C. Kiểm và kết quả.** Bộ dựng native khớp 30/30 ca. Ví dụ kiến trúc khớp 2176 phép số học và 1088 mảng dữ liệu; PC khớp 2160 phép và 1080 mảng. Các kiểm seed/hash, SCC/DA, đồ thị rỗng, suy biến, cột hằng, alpha và độ sâu có bằng chứng. Hai lượt PC bổ sung có trạng thái ở A. Đối chứng kiến trúc không đạt: 60/270 điểm≥3. Source, dữ liệu và phiên bản được ghim; phạm vi ghi được kiểm. Tổng thời gian thực tế cộng dự phòng {cost['total_with_reservation_seconds']:.3f}s≤10800s; thời gian chờ không có worker báo riêng. Thời gian trên máy dùng chung có đo tiến độ là số chẩn đoán. Điều tra trên đồ thị R đã lưu: 75 lượt chấm mới mất 11,906s; đếm độc lập 100 cấu hình đạt.

Kiểm định hướng cùng máy chỉ đổi node order tái hiện khác biệt của `uc_priority=2`, rule độc lập khớp. Full permutation không đạt bất biến; không sửa thứ tự/cấu hình để che khác biệt và không dùng cached scorer PASS thay kết luận này. Chi tiết ở bo-sung-ec2.md.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM.** N1: parser và nhánh dự phòng; N2: kiểm hashseed ở T-006 chỉ gồm bốn ca; N3: mất nút cô lập hoặc trả thứ hạng rỗng; N4: đảo chiều cạnh PC có hướng; N5: mô tả khác biệt thiếu SVR, cửa sổ và tập ứng viên. Đã triển khai fixture, scorer gốc, R/pcalg và điều tra ô MEM25. Kiểm bổ sung tách chiều và coverage trên cùng đồ thị R: 0,864/0,896 theo hướng; bỏ nút cô lập không đổi điểm tổng. Chưa quy toàn bộ khoảng lệch 0,148 cho một yếu tố. K1 cần phân biệt ngưỡng trong bài và trong code. Bằng chứng, hệ quả và đề xuất đoạn cũ→mới ở dinh-chinh-task-cu.md; không sửa file task cũ.

**E. Lệch SPEC và lý do.** Các điều chỉnh trước được giữ nối cuối SPEC. Theo yêu cầu tiếp tục của Minh, sửa cách tính ngân sách để tách thời gian chờ không có worker; chuyển sang EC2 thứ hai với môi trường riêng, giữ trần ba giờ thực tế. Bổ sung hai lượt PC và phép tách yếu tố trên đồ thị đã lưu. Không đổi ca, alpha hoặc độ sâu theo điểm. Các lỗi dựng môi trường được giữ log; chuyển sang kiểm đủ phụ thuộc theo bản freeze và pip check. Không sửa code thuật toán.

**F. Đề xuất tài liệu chung.** de-xuat-tai-lieu-chung.md có nguyên văn nháp DECISIONS, WHY, STATE và K1; thêm yêu cầu tiếp tục của Minh và cách tính ngân sách. Lựa chọn P3 vẫn là CANDIDATE/chờ WHY. Không chọn RHT/DA hoặc chiều cạnh từ điểm chính xác.

**G. Phần chưa kiểm và lý do.** Chưa xác định giao thức nguyên vẹn sinh số công bố MEM=0,740. Đã dựng R/pcalg không cần admin, thử cấu hình từ prior work và ghi giả thuyết, bằng chứng, các nguyên nhân khác. Không mở dữ liệu ngoài danh sách cho phép để lấp khoảng trống. Kiểm alpha/độ sâu trên toàn Train Ticket, calibration, tỷ lệ báo nhầm và benchmark 30 ca thuộc P3/P4 hoặc đã hết ngân sách chẩn đoán. Hai lượt mới đều hoàn tất. Chưa cô lập nguyên nhân số học khác giữa laptop và EC2 ở bốn metric gần suy biến; phép đối chiếu này FAIL, không phải chưa chạy. Số chính thức được kiểm độc lập trên EC2. Chưa có full-PC tham chiếu cùng máy cho permutation; fixture cùng máy xác nhận cơ chế nhạy thứ tự, chưa quy hết thay đổi trên ca thật cho nó. Chưa có runtime trên máy độc lập, chi phí tiền riêng của task và metadata tải nén cho một số gói đầu; không bịa số. Giả định, khi nào sai và phép phân xử ở kiem-tra-va-doi-chieu-spec.md.

**H. Cần Minh quyết.** Duyệt nháp tài liệu chung và lựa chọn P3 sau phản biện G1. Các phép kiểm còn khả thi trong trần đã được làm; phần giới hạn và hệ quả ghi ở bo-sung-ec2.md và đối chiếu SPEC. Nếu cần kiểm ngoài trần hoặc dữ liệu được phép, cần chốt phạm vi riêng; không đặt lại ngân sách theo máy hay task.
'''
(out/'bao-cao-cuoi.md').write_text(report,encoding='utf-8')
with log.open('a',encoding='utf-8') as f:
    f.write('\n\n## Kết thúc lượt tiếp tục — '+datetime.now().isoformat(timespec='seconds')+'\n\n1. Đã làm: báo cáoA–H bên dưới.\n2. File: toàn bộfile/host theo manifest; source/statephạmvi riêngT014.\n3. Kiểm: report/verification/followup/progress; phânbiệt PASSsốhọc và FAILnegativecontrol.\n4. Chưa chắc: protocolpaper vàcácgiớihạn tạiG/H; khôngđiềnOPENthànhDECIDED.\n5. Bước tiếp theo: ClaudeđọcSPEC/LOG/manifest vàmoi-truong; lệnhnhẹ verify_outputs.py --read-only; ghiREVIEW.md duy nhất.\n6. Lệnhcuối tínhtoán: compare_followup.py, independent_scores.py, independent_window.py; các lệnhbàn giao kế: stateupdate/chkscope/verify/promptcheck/manifest.\n\n'+report)
template=(root/'docs/review-prompt.md').read_text(encoding='utf-8-sig');common=re.search(r'## Prompt chung.*?```text\n(.*?)\n```',template,re.S).group(1);g1=re.search(r'\*\*G1 — phương pháp, dataset, cách chia:\*\*\n```text\n(.*?)\n```',template,re.S).group(1)
files='SPEC và LOG; results/T-014/manifest-files.csv liệt kê mọi file trongresults/T-014/ (README, haiho-so, yeu-cau-dau-vao.csv, ca-da-chay.csv, dinh-chinh-task-cu.md, de-xuat-tai-lieu-chung.md, moi-truong.md, kiem-tra-va-doi-chieu-spec.md, bao-cao-cuoi.md, bo-sung-ec2.md, paper/audit/graphs/runs/scripts/requirements vànguồn tải); src/circa_kien_truc/__init__.py,builder.py,scoring.py,README.md; mọi file D:/RCA-ext/work/T-014/, D:/RCA-ext/envs/T-014-main/ trongmanifest; mọi file /home/ubuntu/rca/T-014/ trênEC2₁13.239.30.70 vàEC2₂3.26.62.217 trongmanifest (scopeec2/ec2_2). NguồnCIRCA0215e1880096aa02a305c697f1c23cac4600ebd2 vàRCAEval259ea4167160256a74ad30004aa3d96a998c846e; cáchdựng/chạy ởmoi-truong.md; toàn fileđầura gồm các fileđãgiữ từlượt trước vàlượt tiếp tục'
common=common.replace('<T-xxx>','T-014').replace('<T-xxx-tên>','T-014-ho-so-circa').replace('<danh sách>',files).replace('<commit gốc>','93f13d4c4a966428177e2acc287d96bc89303e92')
with log.open('a',encoding='utf-8') as f:f.write('\n\n## Prompt phản biện cho Claude — 04/10/2026\n\n```text\n'+common+'\n\n'+g1+'\n```\n')
print(json.dumps(dict(statuses=statuses,total_budget=cost['total_with_reservation_seconds'],comparisons_complete={k:v is not None for k,v in comparisons.items()})))
