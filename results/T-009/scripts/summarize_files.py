"""Independently summarize inspected members and build ten-section cards."""
import argparse,collections,json,re,zipfile,io,csv,statistics,tarfile
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--run',required=True);a=ap.parse_args();base=Path('results/T-009');run=base/'runs'/a.run
load=lambda n:json.loads((run/(n+'.json')).read_text(encoding='utf-8'))
raw=load('raw-sessions');inv=load('nested-inventory');labels=load('labels-all');sym=load('symptom-metrics')
canonical={}
for r in sorted(raw,key=lambda x:(x['origin']!='outer',x['origin'],x['case'])):canonical.setdefault((r['dataset'],Path(r['case']).name),r)
duplicates=[]
for x in inv:
    if x['origin']=='outer':continue
    matches=[y for y in inv if y['dataset']==x['dataset'] and y['origin']=='outer' and y['member'].endswith(x['member'].removeprefix('data/'))]
    for y in matches:
        assert x['sha256']==y['sha256'],(x['member'],'nested mismatch')
        duplicates.append(dict(dataset=x['dataset'],outer=y['member'],nested=x['origin']+'::'+x['member'],sha256=x['sha256'],bytes=x['bytes']))
summaries={};cards=[];rootrows=[]
for ds,title,published in [('SN','SocialNetwork',72),('TT','Train Ticket',162)]:
    rr=[r for (d,_),r in canonical.items() if d==ds];counts=collections.Counter()
    for r in rr:counts.update(r['trace']['counts'])
    fs={}
    for l in labels:
        if l['dataset']!=ds:continue
        session=Path(l['member']).name.replace('.fault-','.').removesuffix('.json')
        for f in l['label'].get('faults',[]):fs.setdefault((session,json.dumps(f,sort_keys=True)),f)
    cells=collections.Counter();roots=set()
    for (sess,_),f in fs.items():
        root=f['name'].removeprefix('dockercomposemanifests_').removesuffix('_1') if ds=='TT' else f['name'].removeprefix('socialnetwork-').removesuffix('-1');cells[(root,f['fault'])]+=1;roots.add(root)
        r=canonical[(ds,sess)];pairs={(e['parent'],e['child']) for e in r['trace']['service_edges']};rootrows.append(dict(dataset=ds,session=sess,root=root,fault=f['fault'],root_present=root in r['trace']['services'],whole_file_in_degree=len({u for u,v in pairs if v==root}),whole_file_out_degree=len({v for u,v in pairs if u==root}),scope='whole-file raw graph after exact span identity dedup; not injection time graph',alias_verified=root!='nginx-thrift'))
    metrics=[m for r in rr for m in r.get('metrics',[])];logs=[m for r in rr for m in r.get('logs',[])];services={s for r in rr for s in r['trace']['services']}
    qrows=[]
    for q in (.95,.99,.995):
        pp=[x for x in sym if x['dataset']==ds and x['q']==q];ctl=[x for x in pp if x['regime']=='normal-control'];outside=[]
        for x in pp:
            if x['regime']!='injection':continue
            f=x['label'];root=f['name'].removeprefix('dockercomposemanifests_').removesuffix('_1') if ds=='TT' else f['name'].removeprefix('socialnetwork-').removesuffix('-1')
            if root!='nginx-thrift' and x['service']!=root:outside.append(x)
        qrows.append(dict(q=q,outside_channel_period_rows=len(outside),outside_exceed=sum(x['exceed'] for x in outside),outside_points=sum(x['n'] for x in outside),outside_zero_band_rows=sum(x['zero_band'] for x in outside),control_exceed=sum(x['exceed'] for x in ctl),control_points=sum(x['n'] for x in ctl),control_zero_band_rows=sum(x['zero_band'] for x in ctl)))
    invalid=sum(x['nonfinite_or_invalid'] for m in metrics for x in m['channels'].values());constant=sum(x['constant'] for m in metrics for x in m['channels'].values());logcounts=collections.Counter()
    for m in logs:logcounts.update(m['counts'])
    s=dict(unique_raw_sessions=len(rr),representations=sum(r['dataset']==ds for r in raw),trace_counts=dict(counts),unique_trace_id_sum_by_session=sum(r['trace']['trace_ids'] for r in rr),metric_files=len(metrics),metric_rows=sum(m['rows'] for m in metrics),metric_invalid=invalid,metric_duplicate_timestamp=sum(m['duplicate_timestamp'] for m in metrics),constant_channel_files=constant,log_counts=dict(logcounts),label_events=len(fs),roots=len(roots),cells=len(cells),repetition_histogram=dict(collections.Counter(cells.values())),duplicate_nested_members=sum(x['dataset']==ds for x in duplicates),q_summary=qrows)
    summaries[ds]=s
    faulttable='\n'.join(f'| {root} | {fault} | {n} |' for (root,fault),n in sorted(cells.items()))
    degree_table='\n'.join(f"| {x['root']} | {x['session']} | {x['whole_file_in_degree']} | {x['whole_file_out_degree']} | {'có' if x['root_present'] else 'vắng'} |" for x in rootrows if x['dataset']==ds and x['fault']=='cpu_load')
    qtable='\n'.join(f"| {x['q']} | {x['outside_exceed']} / {x['outside_points']} | {x['control_exceed']} / {x['control_points']} | {x['outside_zero_band_rows']} |" for x in qrows)
    def c(k):return counts[k]
    cards.append(f'''# Eadro {title} — thẻ đã kiểm toàn release đã tải

## 1. Danh tính, nguồn và phạm vi đã kiểm

FACT: paper Eadro (2023), Cheryl Lee và cộng sự; Chaosblade; Jaeger, cAdvisor/Prometheus/InfluxDB và Fluentd/Elasticsearch/Kibana theo [nguồn đã lưu](runs/run-001/source_claims.json). [Repository](https://github.com/BEbillionaireUSD/Eadro), [Zenodo](https://zenodo.org/records/7615394). Revision/URL/hash nguồn ở [manifest metadata](runs/run-001/manifest.json); checksum ZIP ở [download](runs/download-001/manifest.json). Giấy phép dữ liệu/code OPEN: nguồn đã lưu không có điều khoản rõ; truy cập công khai và yêu cầu trích dẫn không thay giấy phép.

Q-47 cho đọc số đo bộ này; bộ Bank bảo toàn không bị mở. Đã tải hai ZIP Eadro; biến thể này có {len(rr)} phiên raw duy nhất, {s['representations']} bản biểu diễn đã đọc. Toàn member lớp ngoài và mọi nested TAR/XZ/GZIP được đọc, CRC ZIP đạt; [inventory](runs/{a.run}/nested-inventory.json) giữ hash từng file. {s['duplicate_nested_members']} member raw/label nested trùng hash bản ngoài, không cộng thành ca mới. [Kết quả](runs/{a.run}/summary.json), [tính lại độc lập](runs/{a.run}/independent-summary.json). Chạy `py -3 -B results/T-009/scripts/inspect_files.py --data data/ngoai-rcaeval/eadro --out results/T-009/runs/<id-mới>`, rồi `summarize_files.py --run <id>`; không RCA.

## 2. Bảng chung tiêu chí 1–9

| Tiêu chí | FACT và giới hạn |
|---|---|
| 1. Công khai/giấy phép | ZIP tải/hash/CRC được; điều khoản sử dụng OPEN. |
| 2. Root/thời điểm | {len(fs)} nhãn tiêm, {len(roots)} root; chỉ injection, không onset thật. |
| 3. Trace cha–con | Raw Jaeger đầy references; trùng bản export và clock là giới hạn có thật. |
| 4. Metric/log | Đọc {len(metrics)} CSV metric và log mọi phiên raw; nguồn và ID ghép tách mục 4. |
| 5. Root/vị trí | Bậc raw từng root ở mục 3; graph theo injection chưa hợp lệ khi clock chưa rõ. |
| 6. Loại lỗi | CPU load/network delay/network loss; chưa có code fault trong release nhãn. |
| 7. Ngoài root | Đã probe metric ba q, đối chứng riêng; chưa là bằng chứng lan nhân quả. |
| 8. Normal | Có normal riêng và metric thực; warm-up/load cleanliness không được bảo đảm bởi tên. |
| 9. Độc lập | Nhóm tác giả/công cụ/stack có nguồn; cùng Train Ticket hoặc khác tên không đủ quyết độc lập. |

## 3. Nhãn, số ca và khả năng phân xử

FACT: {len(fs)} sự kiện, {len(roots)} root, {len(cells)} ô root×fault; mỗi ô đúng một lần trong release đã tải. Paper công bố {published}, giữ cả hai số. Archive “all” trùng raw/label lớp ngoài theo hash nên không cung cấp lần lặp thứ hai. Phiên chứa nhiều sự kiện, không lấy số phiên thay số sự kiện.

| Root | Nhãn fault gốc | Sự kiện |
|---|---|---|
{faulttable}

| Root | Phiên chính root (cpu_load) | Bậc vào | Bậc ra | Có trong trace |
|---|---|---|---|---|
{degree_table}

Hướng cạnh parent service→child service, bỏ self-edge, union trong toàn file raw sau gộp span trùng nội dung. [Bậc đủ mọi ca/ô](runs/{a.run}/root-degree-whole-file.json). Đây là graph file; không tự gọi graph đúng khoảng tiêm. Root vắng không được gọi cô lập. SN `nginx-thrift`→`nginx-web-server` vẫn là alias CANDIDATE; không dùng thay root đã xác minh.

## 4. Schema thật và chất lượng ba nguồn tín hiệu

FACT toàn {len(rr)} phiên raw duy nhất: {c('spans')} dòng span, {s['unique_trace_id_sum_by_session']} trace-ID cộng theo phiên (không khẳng định ID độc lập liên phiên). Jaeger: traceID/spanID/processes.serviceName/startTime/duration (microsecond theo schema và độ lớn)/tags/references CHILD_OF. Tổng {c('root_no_CHILD_OF')} span không có CHILD_OF; {c('parent_references')} reference cần cha. Khóa `(traceID,spanID)` trong phiên: {c('parent_unique')} tìm một dòng cha, {c('parent_missing')} thiếu, {c('parent_ambiguous')} nhiều dòng. Khi gộp bản span **giống hệt nội dung và service**, {c('parent_unique_identity')} reference tìm một identity; {c('parent_conflicting_identity')} xung đột. {c('duplicate_keys')} dòng trùng khóa; {c('conflicting_span_keys')} khóa có nội dung xung đột. Hai mẫu số/tỷ lệ không bị trộn. Trùng có thể do export nhiều trace lặp, không tự là mất dữ liệu.

Metric: timestamp epoch giây + bảy cột CPU/memory/rx/tx; {s['metric_rows']} dòng trong {len(metrics)} CSV, invalid/nonfinite {invalid}, timestamp trùng {s['metric_duplicate_timestamp']}, {constant} cặp file×kênh hằng. Delta/cadence/gap riêng từng file ở [raw-sessions](runs/{a.run}/raw-sessions.json); tên rx_bytes không đủ xác định raw byte hay rate, đơn vị/biến đổi nguồn OPEN. Không tự chuẩn hóa/sửa giá trị.

Log JSON map service→list text; {logcounts['lines']} dòng. Không cột trace_id riêng; payload `Span reported` có {logcounts['payload_trace_id']} dòng ID, {logcounts['trace_matches']} ghép trace và {logcounts['span_matches']} ghép scoped span. Parser tìm đúng cấu trúc báo span, không coi regex khác là ID. SN phần đã đọc không thấy cấu trúc này; không suy mọi log thiếu ID. Level/timestamp/order theo file được giữ. Clock log chỉ tính UTC **giả định**, không khẳng định timezone nguồn.

## 5. Bình thường và mốc thời gian

Normal nested đã được đọc. SN có ba phiên faults=[]; TT có hai nhãn faults=[] lớp ngoài và thêm raw trong TT-no-fault.txz ngày 20/4 không có label riêng: phần thứ ba là CANDIDATE normal theo tổ chức release. Normal thứ ba này không vào phép probe khi thiếu nhãn riêng. Nhãn start/duration/end là khoảng tiêm, không ground truth onset/recovery.

Trace có timestamp lịch sử và lệch biểu kiến so metric/nhãn/log. Raw SN nhiều span nằm khoảng 8 giờ sau metric; TT cũng có trace từ thời gian trước phiên. [Khoảng thời gian từng nguồn](runs/{a.run}/raw-sessions.json) giữ số gốc; chưa có nguồn xác nhận timezone/cách export. Không dịch 8 giờ để làm graph hoặc claim trace/log đồng bộ. Graph theo injection ở root-positions vì vậy không được diễn giải bậc 0 là cô lập.

## 6. Ước lượng thô triệu chứng ngoài root — tiêu chí 7

FACT mô tả metric: reference là phiên có nhãn no-fault đầu tiên theo session, control là các phiên có nhãn no-fault còn lại; mỗi service×kênh dùng median reference và quantile tuyến tính của độ lệch tuyệt đối, `abs(x-median)>band`; không epsilon, giữ zero-band/missing. Root chỉ gắn sau đo tất cả service/kênh; ba sự kiện `nginx-thrift` không vào tổng ngoài-root do alias chưa xác minh. [Toàn bảng từng ca/kênh/q](runs/{a.run}/symptom-metrics.json) giữ nhãn/ô phục vụ mô tả, không vào phương pháp.

| q | Điểm vượt band ngoài root / điểm hợp lệ | Điểm vượt control / điểm hợp lệ | Cặp ca×kênh ngoài root có band=0 |
|---|---|---|---|
{qtable}

Tổng điểm là phép cộng mô tả, không OR service, không nhãn lan/vùng và không điểm detector. Drift/load, kênh hằng, scale khác giữa phiên hoặc lỗi đo cũng giải thích exceedance. Control được báo để không gọi mọi exceedance là fault. Độ nhạy theo ca/ô còn thấy trong bảng đầy đủ; không kết luận nhân quả từ đồng thời.

## 7. Task chấm được

Ranking root theo service: có nhãn riêng, cần giải quyết alias/clock và giao thức G1; không RCA. Phát hiện thời gian: chỉ injection-regime, onset/end triệu chứng thật không có. Vùng ảnh hưởng: không nhãn tập bị ảnh hưởng; probe không thay nhãn. Không có nhãn bất thường từng trace. Không dùng root label để chọn SLI; chưa chọn ngân sách học/dev/test.

## 8. Rò nhãn, độc lập và G1

Tên file/ca/fault label/mốc tiêm dùng census/chấm, phải loại khỏi đầu vào phương pháp. `align.py` tạo cửa sổ trượt một giây rồi shuffle split, có thể tạo overlap train/test; chưa chứng minh paper dùng chính lệnh đó. Hard-code topology trong util.py khác graph quan sát ở đây. Cùng stack/hệ giữa Eadro và Nezha/RCAEval không tự quyết reuse; hash nested Eadro chỉ chứng minh trùng nội bộ. Chưa chia dev/test hay chọn dataset thay Minh.

## 9. Dung lượng và chi phí

ZIP {78753809 if ds=='SN' else 48923113} byte; byte/MD5/SHA256 và thời gian tải ở download-001. Inspection streaming toàn hai ZIP trong {load('summary')['elapsed_seconds']} giây; không giải nén payload ra đĩa, không cài môi trường. [Inventory](runs/{a.run}/nested-inventory.json) có byte/hash cuối của từng member; tổng representation có trùng, không là dung lượng ca độc lập. RAM đỉnh chưa đo; runtime parsing không thay chi phí RCA hoặc adapter. [Byte file cuối chính xác](runs/{a.run}/logical-member-sizes.json) tách outer/nested và raw duplicate; không gồm TAR header/padding hoặc intermediate container. Đây là dung lượng logical nếu giải nén hết, không là disk đã ghi.

## 10. OPEN và giới hạn

Giấy phép: tác giả/nguồn điều khoản cần làm rõ trước dùng ngoài inspection. Clock/export trace và alias SN: cần nguồn xác minh, Minh quyết cách dùng; không tự sửa. Bình thường sạch/đại diện tải, onset và nhãn vùng không được release chứng minh. Chọn dataset/split/ngân sách nhãn là G1 của Minh. Đã kiểm toàn file trong release tải và giữ lượt hỏng; các thiếu nhãn/nguồn thật không được gọi đã giải quyết nhờ kiểm metadata.
''')
(run/'independent-summary.json').write_text(json.dumps(dict(datasets=summaries,duplicate_member_pairs=duplicates),indent=2),encoding='utf-8')
(run/'root-degree-whole-file.json').write_text(json.dumps(rootrows,indent=2),encoding='utf-8')
old=base/'the-dataset.md';backup=run/'card-before-update.md'
if not backup.exists():backup.write_bytes(old.read_bytes())
old.write_text('\n\n---\n\n'.join(cards),encoding='utf-8')
assert len(re.findall(r'^## [0-9]+\.',old.read_text(encoding='utf-8'),flags=re.M))==20
print(json.dumps(summaries))
