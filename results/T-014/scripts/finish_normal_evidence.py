"""Keep failed platform comparison separate from same-host arithmetic proof."""
import json,csv
from pathlib import Path
o=Path('D:/RCA-flashticket/results/T-014')
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
d=o/'runs/ec2-2-normal';scores=load(d/'scores.json');rank=sorted(scores,key=lambda x:-x[1])
capture=load(o/'runs/normal-normal-pc-official-capture/capture-status.json')
proof=load(o/'runs/normal-official-independent-linux/comparison.json')
assert proof['pass'] and capture['actual_rht_same_host_repeat_exact']
mismatch=load(o/'runs/normal-ec2-local-mismatch-001.json')
c=dict(mode='normal',status=load(d/'status.json'),shape=[720,275],scored=len(scores),top=rank[0],scores_ge3=sum(v>=3 for k,v in scores),fallback_valueerror=0,direct_rht_matches_snapshot=False,official_same_host_repeat_exact=True,independent_official_linux_pass=True,normal_pc_input_strictly_before_injection=True,normal_score_windows_strictly_before_injection=True,cross_platform_mismatch=mismatch,normal_sanity_verdict='FAIL apparent evidence on pre-injection proxy')
(d/'comparison.json').write_text(json.dumps(c,indent=2))
note='''# Đối chiếu số học của đối chứng bình thường

Code RHT chính thức chạy lại trên cùng EC2, cùng đồ thị và dữ liệu trả đúng từng điểm của 270 metric. Script độc lập trên EC2 kiểm 1080 giá trị trung gian, sai số lớn nhất 2,22e-16. Script chuẩn bị dữ liệu độc lập kiểm 1080 mảng và khớp. Nguồn: runs/normal-normal-pc-official-capture/, runs/normal-official-independent-linux/, paper/followup-normal-official-raw/.

Đối chiếu với laptop KHÔNG ĐẠT tolerance atol=rtol=1e-7: bốn metric khác điểm. ts-auth-service_latency đổi từ 41,9829 trên EC2 thành 287,4143 trên laptop. Ba metric còn lại lệch nhỏ hơn nhưng vẫn vượt tolerance. Lượt thất bại được giữ tại runs/normal-ec2-local-mismatch-001.json và paper/followup-normal-official-score/comparison.json. Không nới sai số để biến thành đạt.

Với auth_latency, cùng thứ tự sáu parent và mảng X/Y giống từng giá trị, nhưng ma trận hồi quy gần suy biến: một singular value khoảng 2,7e-17. Hệ số hồi quy thay đổi lớn giữa hai máy. Điều này phù hợp với nhạy số học của bài toán gần suy biến. Các nguyên nhân khả thi khác gồm thư viện đại số, thứ tự phép cộng/centering và bố trí bộ nhớ; với auth_workload còn có thứ tự parent khác. Chưa cô lập từng yếu tố, nên không quy duy nhất cho hệ điều hành hoặc thứ tự parent. Ghim phiên bản Python/package chưa bảo đảm cùng bản biên dịch và backend đại số.

Kết luận đối chứng lấy điểm chính thức trên EC2: 93/270 điểm >=3, top ts-security-service_mem=957,1627977273204. Không coi top này là nguyên nhân thật. Cả hai cửa sổ đều trước mốc tiêm, nhưng đây chỉ là đại diện bình thường chưa được xác nhận khỏe độc lập. Một ca không cho tỷ lệ báo nhầm của dataset. Kiểm số học đạt không làm phép kiểm âm tính đạt.
'''
(o/'normal-doi-chieu-so-hoc.md').write_text(note,encoding='utf-8')
p=o/'scripts/finalize_followup.py';s=p.read_text(encoding='utf-8')
s=s.replace("p=out/'paper'/('followup-'+mode+'-'+stage)/name;", "p=(out/'runs/normal-official-independent-linux/comparison.json' if mode=='normal' and stage=='score' else out/'paper/followup-normal-official-raw/window-comparison.json' if mode=='normal' else out/'paper'/('followup-'+mode+'-'+stage)/name);")
s=s.replace("line+=' Direct RHT/snapshot, số học độc lập và raw arrays đều PASS. Không có ValueError fallback.' if c['fallback_valueerror']==0 else f\" Node fallback={c['fallback_valueerror']}; đã ghi rõ.\"", "line+=(' Direct RHT/snapshot, số học độc lập và raw arrays đều PASS.' if mode=='permuted' else ' RHT chính thức lặp lại cùng máy khớp từng điểm; số học độc lập trên EC2 và raw arrays PASS. Đối chiếu laptop FAIL ở bốn metric; xem normal-doi-chieu-so-hoc.md.')")
s=s.replace('Nếu lượt mới chưa hoàn tất, chưa có bằng chứng cho kết luận của phép kiểm tương ứng; trạng thái lỗi/timeout trong ngân sách được giữ.', 'Hai lượt mới đều hoàn tất. Chưa cô lập nguyên nhân số học khác giữa laptop và EC2 ở bốn metric gần suy biến; phép đối chiếu này FAIL, không phải chưa chạy. Số chính thức được kiểm độc lập trên EC2. Chưa có full-PC tham chiếu cùng máy cho permutation; fixture cùng máy xác nhận cơ chế nhạy thứ tự, chưa quy hết thay đổi trên ca thật cho nó.')
p.write_text(s,encoding='utf-8')
p=o/'scripts/verify_followup.py';s=p.read_text(encoding='utf-8')
s=s.replace("ck(mode+' direct RHT matches captured snapshot',c['direct_rht_matches_snapshot'])", "ck(mode+' evidence comparison status',c['direct_rht_matches_snapshot'] if mode=='permuted' else c['official_same_host_repeat_exact'] and not c['direct_rht_matches_snapshot'] and len(c['cross_platform_mismatch']['diff'])==4)")
s=s.replace("load(out/'paper'/('followup-'+mode+'-'+stage)/file)['pass']", "load((out/'runs/normal-official-independent-linux/comparison.json' if mode=='normal' and stage=='score' else out/'paper/followup-normal-official-raw/window-comparison.json' if mode=='normal' else out/'paper'/('followup-'+mode+'-'+stage)/file))['pass']")
p.write_text(s,encoding='utf-8')
with (Path('D:/RCA-flashticket/tasks/T-014-ho-so-circa/LOG.md')).open('a',encoding='utf-8') as f:f.write('\n- Đối chứng full normal-PC hoàn tất. RHT chính thức lặp cùng EC2 khớp 270/270; độc lập Linux 1080 phép PASS, raw 1080 PASS. Đối chiếu Windows FAIL bốn metric; giữ mọi lượt lỗi, không nới tolerance. Chi tiết normal-doi-chieu-so-hoc.md. Không còn worker PC chạy.\n')
p=o/'ca-da-chay.csv'
with p.open(encoding='utf-8-sig',newline='') as f:r=csv.reader(f);rows=list(r)
for method,purpose,reason in [('CIRCA-PC RHT','Lặp lại RHT chính thức cùng EC2 trên đồ thị normal đã lưu','a'),('CIRCA-PC RHT và RHT+DA','Đối chiếu adapter trên đồ thị permuted đã học mới','b'),('CIRCA-PC RHT và RHT+DA','Đối chiếu adapter trên đồ thị normal đã học mới; giữ mismatch','b')]:rows.append(['re2tt_ts-order-service_loss_3','data/rcaeval/re2tt_ts-order-service_loss_3/metrics.parquet',method,purpose,reason])
with p.open('w',encoding='utf-8',newline='') as f:csv.writer(f).writerows(rows)
print('Normal evidence and final reporting repaired; cross-platform failure retained.')
