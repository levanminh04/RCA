"""Render C3 from preserved samples and warehouse queries, with OOM history."""
import json,re,statistics
from pathlib import Path
root=Path(__file__).resolve().parent
data=json.loads((root/'so-do-tai-nguyen.json').read_text(encoding='utf8'))
raw=[json.loads(x) for x in (root/'resources-30m-app.jsonl').read_text().splitlines()]
heap=json.loads((root/'memory-heap-history.json').read_text())
def size(text):
 m=re.fullmatch(r'([0-9.]+)\s*([A-Za-z]+)',text.strip())
 return float(m[1])*{'B':1,'kB':1000,'MB':1e6,'GB':1e9,'KiB':1024,'MiB':1024**2,'GiB':1024**3}[m[2]]
groups={}
for row in raw:
 for c in row['docker_stats']:
  if not c['Name'].startswith('flash-ticket-') or '-infra-' in c['Name'] or c['Name']=='flash-ticket-collector': continue
  used,limit=[size(x) for x in c['MemUsage'].split('/')]
  groups.setdefault(c['Name'],[]).append((row['utc'],used,limit))
out=['# C3 — tài nguyên và OOM trong môi trường có agent','',
     '**Không đạt ổn định ở cả hai pha.** Booking bị kernel giết vì chạm giới hạn cgroup 512 MiB lúc 21:04:18Z và 21:40:18Z. Cả hai xảy ra trước lỗi chủ động. Host vẫn còn RAM available. Không dùng hai cửa sổ này làm nền sạch hoặc kết quả dung lượng ổn định.', '',
     'Đây là phép đo 30 phút rảnh + 30 phút tải đọc 1 request/giây theo STEER #3, rút từ SPEC 1 giờ + 1 giờ. Mỗi host có 241 mẫu, bước 15 giây. Hai đầu mút chung dùng cho delta; CPU tính theo khoảng thời gian sau đầu cửa sổ. Dữ liệu gốc và summary giữ nguyên.', '',
     '| Máy/pha | CPU host trung bình | RAM available nhỏ nhất | Tăng kho, GB/giờ | Restart mới | OOM kernel |',
     '|---|---:|---:|---:|---:|---:|']
for role,host in data['hosts'].items():
 for phase,w in host['windows'].items():
  out.append(f"| {role}/{phase} | {w['cpu_mean_percent_machine']:.2f}% | {w['minimum_memory_available_percent']:.2f}% | {w['telemetry_decimal_gb_per_hour']:.4f} | {sum(w['restart_deltas'].values())} | {len(w['kernel_oom_events'])} |")
out+=['','CPU host tính trên toàn máy; Docker CPU 100% tương ứng một logical CPU. GB/giờ là ngoại suy từ tăng byte trong 30 phút, gồm file capture/queue và dữ liệu backend; không phải đo retention ổn định. RAM thực tế khoảng 11,65 GiB app và 10,66 GiB obs, không phải máy 8 GiB của SPEC.', '',
      '## 1. Bộ nhớ từng JVM trước sửa', '',
      'Bảng dùng Docker working set từ sampler, không gọi nó là RSS của tiến trình. Số ở đây bao gồm hoạt động bình thường và hai lần restart; không chỉ lấy đỉnh để bỏ phần lỗi.', '',
      '| Container | Limit MiB | Working set lớn nhất MiB | Tỷ lệ lớn nhất |',
      '|---|---:|---:|---:|']
table=[]
for name,points in sorted(groups.items()):
 maximum=max(points,key=lambda x:x[1]/x[2])
 table.append({'container':name,'limit_bytes':maximum[2],'maximum_working_set_bytes':max(x[1] for x in points),'maximum_percent':100*maximum[1]/maximum[2]})
 out.append(f'| {name} | {maximum[2]/1024**2:.0f} | {max(x[1] for x in points)/1024**2:.2f} | {100*maximum[1]/maximum[2]:.2f}% |')
out+=['', 'RSS trực tiếp lúc 21:46:37Z của booking là 522868 KiB; payment 528496 KiB; discovery 374236 KiB. RSS gồm trang chia sẻ nên có thể khác số charge của cgroup. `memory-before-fix.json` ghi PID1; riêng PID1 Keycloak là shell, hàng đó **không** dùng làm RSS JVM Keycloak. Theo dõi sau sửa đọc đúng tiến trình `java` trong cgroup.', '',
      '## 2. Heap và non-heap của booking', '',
      '| Đại lượng | Nhỏ nhất MiB | Lớn nhất MiB |','|---|---:|---:|']
for name,q in heap['queries'].items():
 series=next(x for x in q['data']['result'] if x['metric'].get('service_name')=='booking-service')
 values=[float(x[1]) for x in series['values']]
 out.append(f'| {name} | {min(values)/1024**2:.2f} | {max(values)/1024**2:.2f} |')
out+=['', 'Nguồn là bốn query Prometheus cố định trong `memory-history.py`; raw matrix ở `memory-heap-history.json`. Bước query 15 giây ở đây chỉ phục vụ mô tả. Đây không phải clock nguồn dùng trong adapter M1.', '',
      'Heap dùng không đạt limit 512 MiB trong các mẫu đã có; non-heap đáng kể. Điều đó phù hợp với việc giới hạn tổng cgroup bao gồm nhiều vùng ngoài heap. Nó chưa chỉ ra phần nào do agent. Không lấy RSS trừ heap used thành số overhead chính xác: heap used/committed, RSS, working set và bộ nhớ native khác nhau.', '',
      'OPEN: chưa có đối chứng cùng máy ARM, cùng JDK/revision/tải và không agent. Thông tin máy 84 dùng 512 MiB không tạo được đối chứng có kiểm soát; không truy cập máy 84. Các giải thích còn lại gồm chi phí instrumentation/class metadata, heap/native/JIT/thread của ứng dụng và khác biệt nền ARM/JDK/thư viện. Cần lượt A/B cùng môi trường được duyệt để định lượng Δagent; đêm nay chỉ xác nhận cấu hình có agent này không vừa cgroup cũ.', '',
      '## 3. Collector và giới hạn quan sát', '',
      'Các chuỗi receiver_refused xuất hiện đầy đủ có delta 0 ở cả hai Collector trong hai pha; xem `so-do-tai-nguyen.json#/hosts/*/windows/*/collector_counter_series`. Không có chuỗi send_failed/enqueue_failed được xuất trong các mẫu này; không đổi sự vắng mặt đó thành số đo drop SDK bằng 0. Queue max và counter thô được giữ theo từng exporter/loại tín hiệu. Collector không đo được span chưa tới receiver.', '',
      '`State.OOMKilled` ở các mẫu có thể là false sau automatic restart. Vì vậy `oom_seen=false` trong summary thô không chứng minh không OOM. Báo cáo tổng hợp bổ sung kernel journal, Docker exit137 và delta restart. Docker event buffer chỉ còn giữ lần OOM sau; journal giữ cả hai lần. Nguồn: `unplanned-oom.json`, raw sampler.', '',
      '## 4. Sửa triển khai theo STEER #4', '',
      'Sau khi C3 kết thúc, `fix-jvm-memory.py` đổi **compose-exp**: booking/payment/event 512→1024 MiB, discovery 384→768 MiB, Keycloak 768→1536 MiB. Các service còn lại dưới mức cần đổi trong mẫu. Giữ `-XX:MaxRAMPercentage=50.0 -Duser.timezone=UTC`. Đây là lệch giới hạn so với compose của nhóm/máy 84 được cung cấp; không sửa repo. Chọn khoảng dư lớn hơn 768 MiB cho các JVM 512 MiB vì non-heap đáng kể và thời gian còn lại cần một cửa sổ ổn định; không coi giới hạn mới là tối ưu.', '',
      'Các container đó và Collector được recreate, log allowlist tạo lại và image Collector ghim lại digest. API được xác nhận ba lần liên tiếp, hoàn tất 21:50:53.940859Z; xem `jvm-memory-fix.json`. Plan v1 giữ nguyên, plan v2 khóa trước M1 và chờ thêm 10 phút ổn định. Monitor mới đọc `memory.events` cgroup, bao gồm `oom_kill`, và RSS đúng tiến trình Java; file `memory-after-fix.jsonl` sẽ là bằng chứng sau sửa. Chưa có phép đo C3 đủ 1h+1h hoặc phép so overhead sau sửa.', '',
      'C3 trả lời được: giới hạn booking 512 MiB không đủ cho cấu hình hiện tại. Chưa trả lời được máy 8 GiB có đủ hoặc chi phí riêng của agent là bao nhiêu. Không đề xuất tăng toàn máy chỉ từ OOM cgroup khi host còn RAM.']
(root/'kiem-bo-nho.md').write_text('\n'.join(out)+'\n',encoding='utf8')
(root/'memory-container-summary.json').write_text(json.dumps(table,indent=2)+'\n',encoding='utf8')
print('Rendered C3 report with',len(table),'JVM containers; both failed phases preserved')
