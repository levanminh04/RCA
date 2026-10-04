"""Replace obsolete pending statements in current reports, preserve historical logs."""
from pathlib import Path
o=Path('D:/RCA-flashticket/results/T-014')
p=o/'kiem-tra-va-doi-chieu-spec.md';s=p.read_text(encoding='utf-8')
s=s.replace('Việc học PC riêng trên normal còn chưa kiểm; không thay bằng toy hoặc graphcached để hoàn tất checklist.', 'Đã bổ sung PC học riêng trên 720×275 dữ liệu trước tiêm: 93/270 điểm≥3, nên phép kiểm âm tính FAIL. Bằng chứng tại runs/ec2-2-normal/; số học độc lập trên EC2 PASS, đối chiếu laptop FAIL bốn metric.')
lines=s.splitlines()
for i,line in enumerate(lines):
    if line.startswith('| 6. PC quy môTT/'):
        lines[i]='| 6. PC quy mô TT/chi phí/progress | Default 600×273 xong; bổ sung full permutation và full normal-PC trên EC2₂ đều xong. Permutation FAIL bất biến: 667 cặp endpoint và 258 điểm đổi; host cũng đổi nên chưa quy riêng mọi thay đổi. Normal control FAIL 93/270≥3. Worker cũ+mới+dự phòng=10235,006s; queue không worker tách riêng, không đặt lại ngân sách theo máy. | runs/ec2-2-permuted/; ec2-2-normal/; followup-cost.json; bo-sung-ec2.md |'
    if line.startswith('- PC normal windows'):
        lines[i]='- PC normal windows trên cached fault graph có 76/268≥3. Đã bổ sung full normal-PC riêng: 93/270≥3, không đạt đối chứng âm tính. Lặp RHT cùng EC2 khớp 270 điểm; độc lập Linux 1080 phép PASS và raw 1080 mảng PASS. Đối chiếu laptop FAIL bốn metric; xem normal-doi-chieu-so-hoc.md.'
    if line.startswith('- Architecture same-seed repeat'):
        lines[i]='- Architecture same-seed repeat và đảo cột khớp. PC cached scorer khớp nhưng full PC permutation FAIL; fixture cùng máy xác nhận cơ chế nhạy thứ tự uc_priority=2. Ca thật đổi cả host nên chưa quy riêng mọi thay đổi; bo-sung-ec2.md.'
    if line.startswith('| FullPC normal graph |'):
        lines[i]='| Nhạy số học và permutation giữa hai máy | Full normal-PC đã chạy xong, đối chứng âm tính FAIL 93/270≥3. Bốn điểm khác giữa laptop và EC2; kiểm độc lập cùng EC2 đạt. Full permutation đổi cả host; chưa có lượt PC tham chiếu cùng host trong ngân sách còn lại. | Nếu backend đại số hoặc thứ tự phép cộng làm đổi nghiệm gần suy biến, ghim package chưa đủ; cần tách backend/parent order/centering. Fixture orientation cùng máy xác nhận một cơ chế nhạy thứ tự nhưng chưa replay separating sets của ca thật. |'
p.write_text('\n'.join(lines)+'\n',encoding='utf-8')
p=o/'ho-so-circa-pc.md';s=p.read_text(encoding='utf-8');s=s.replace('FullPC permutation được xếp hàng trên EC2 với4170s gồm cả chờ; kết quả cuối ở `runs/ec2-default-permuted/status.json` và `kiem-tra-va-doi-chieu-spec.md`.', 'Lượt xếp hàng đầu tiên không có worker được giữ trong lịch sử. Lượt bổ sung full PC permutation trên EC2₂ đã xong, không đạt bất biến; xem `bo-sung-ec2.md`.')
s=s.replace('không thay PC học riêng hai cửa sổ normal.', 'không thay PC học riêng hai cửa sổ normal. Phép học riêng đã bổ sung và cũng không đạt đối chứng âm tính: 93/270 điểm≥3.')
p.write_text(s,encoding='utf-8')
print('Current scientific status refreshed; historical LOG untouched.')
