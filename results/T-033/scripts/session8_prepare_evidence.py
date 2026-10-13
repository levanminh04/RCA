"""Laptop metadata setup for EC2 synthesis, preserve all previous outputs."""
from session8_control import ROOT,OPEN,read,write,sha,stamp
import ast
inp=read(OPEN/'rest-input.json');inv=read(ROOT/'results/T-033/runs/session8-extraction-001/artifact-inventory.json')
inp['pins'].update(inv['files']);inp['selected_case_ids']=sorted({v['opaque_id'] for v in inp['locator']['core']})
write(OPEN/'evidence-input.json',inp)
src=ROOT/'results/T-033/scripts/session8_evidence.py';ast.parse(src.read_text())
s=(ROOT/'results/T-033/scripts/session8_inventory.py').read_text().replace("['session7-manual-pilot-001','session7-manual-rest-001']","['session8-evidence-001']")
(ROOT/'results/T-033/scripts/session8_inventory_evidence.py').write_text(s,encoding='utf-8',newline='\n')
s=(ROOT/'results/T-033/scripts/session8_receive.py').read_text().replace('session8-extraction-001','session8-evidence-receive-001').replace('session8-receive-inventory-001','session8-evidence-inventory-001').replace('session8_inventory.py','session8_inventory_evidence.py').replace("v.startswith('runs/session7-manual-')","v.startswith('runs/session8-evidence-001/')").replace('session8-receive-stream-001.timer.json','session8-evidence-stream-001.timer.json')
(ROOT/'results/T-033/scripts/session8_receive_evidence.py').write_text(s,encoding='utf-8',newline='\n')
with (ROOT/'tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md').open('a',encoding='utf-8',newline='\n') as f:
 f.write('\n- '+stamp()+': preflight/source/raw89/native/env mới PASS sau một lượt SSH sandbox chặn có timer. Pilot v2 một ca PASS, 7 đường/31 điểm; scalar/time/post_indices/NaN/flags/CP/theta/source-after/readback kiểm exact nguồn. Rest29 PASS, 203 đường/937 điểm và kiểm exact cùng schema. Không gọi detector. Nhận40file/17215895byte, hash hai đầu PASS; automatic approval review lần đầu chặn egress vì chưa xác minh payload/đích, đối chiếu README storage mục3 và public provenance trước retry cùng hành động; lần tiếp được phép và đạt. Giữ mọi lần lỗi/file/timer.\n- Tiếp lập chuỗi scalar+contrast+log text từ dữ liệu đã lưu, chưa diễn giải/nhận hoàn tất RQ2 hoặc task. Tất cả tính toán tổng hợp trên EC2 có ledger/timer, không thay tham số hay khóa nhóm/điểm.\n')
print('PASS evidence input pins',len(inp['pins']))
