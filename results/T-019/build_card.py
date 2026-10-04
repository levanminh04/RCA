"""Build the card only from saved measurements and source audits."""
import collections, csv, json, pathlib
import pandas as pd
from acquire import OUT, dump

HEADINGS=[
'Danh tính, nguồn và phạm vi đã kiểm',
'Bảng chung tiêu chí 1–9',
'Nhãn, số ca và khả năng phân xử',
'Schema thật và chất lượng ba nguồn tín hiệu',
'Dữ liệu bình thường và mốc thời gian',
'Ước lượng thô triệu chứng lan — tiêu chí 7',
'Task nào chấm được bằng nhãn hiện có?',
'Rò nhãn và thông tin phục vụ G1',
'Kích thước và chi phí — tách khỏi khả năng phân xử',
'Những điều còn mở']

def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join(['---']*len(headers))+'|']+['| '+' | '.join(str(x).replace('|',' / ').replace('\n',' ') for x in row)+' |' for row in rows])

def span(values):
    return f'{min(values):g}–{max(values):g}' if min(values)!=max(values) else f'{min(values):g}'

def main():
    summaries=json.loads((OUT/'census-summary.json').read_text()); sm={x['dataset']:x for x in summaries}
    cases=json.loads((OUT/'inspection/cases.json').read_text());bounds=pd.read_csv(OUT/'inspection/boundaries.csv')
    cells=pd.read_csv(OUT/'census-cells.csv');probes=pd.read_csv(OUT/'inspection/probe-summary.csv'); channels=pd.read_csv(OUT/'inspection/channel-bands.csv')
    qa=json.loads((OUT/'sources-audit/label-audit.json').read_text()); labels=qa['labels'] if 'labels' in qa else qa.get('rows',qa.get('records',[]))
    if not labels:
        # Locate list by schema instead of relying on an audit's prose summary.
        labels=next(v for v in qa.values() if isinstance(v,list) and v and isinstance(v[0],dict) and 'case' in v[0])
    rootrows=[]
    for x in labels:
        rootrows.append([x['case'],x['indicator_kind'],x['offset_seconds'],x['service_message_matches'],x['indicator_time_in_log_window']])
    chunks=['# Thẻ Sock Shop của họ RCAEval — T-019\n',
'Ngày kiểm: 04/10/2026. P2 phục vụ G1, RQ1/RQ3 và câu của cô “vì sao dùng hoặc không dùng Sock Shop”. Thẻ mô tả bằng chứng; không chọn hoặc loại dataset, không chia dev/test.\n',
'**FACT metadata và file thật:** toàn ba biến thể SS tại revision ghim không có trace. Không có span để kiểm parent (cha–con), không ghép log–trace và không đo bậc root runtime (lúc chạy). Đây là giới hạn release, không phải phần chờ quyền. Đồ thị kiến trúc nguồn chỉ là bằng chứng tĩnh; không thay thế đồ thị quan sát.\n',
'Nguồn chính: [HF dataset](https://huggingface.co/datasets/phamquiluan/RCAEval), [bài RCAEval v2](https://arxiv.org/html/2412.17015v2), [code RCAEval](https://github.com/phamquiluan/RCAEval). Revision, hash và URL file nằm trong [download-plan.json](download-plan.json), [input-metadata-check.json](input-metadata-check.json), [source manifests](sources-audit/network-manifest.json). HF HEAD được kiểm vẫn bằng revision ghim; không trộn file giữa revision.\n',
'Trạng thái: FACT nguồn công bố khác FACT metadata/file thật; USER_CONFIRMED là phạm vi Minh giao trong SPEC/LOG; không có quyết định DECIDED chọn dataset. CANDIDATE là khả năng cần kiểm. OPEN nêu đầu vào và người cần giải quyết. Số đo không tự là bằng chứng nhân quả.\n']
    measured=[]
    for ds in ['RE2-SS','RE3-SS']:
        s=sm[ds];cc=[c for c in cases if c['dataset']==ds];n=len(cc);bb=bounds[bounds.dataset==ds];mm=bb[bb.modality=='metric'];ll=bb[bb.modality=='log'];pp=probes[probes.dataset==ds]
        total_log=sum(c['log']['rows'] for c in cc);total_metric=sum(c['metric_rows'] for c in cc)
        direct=sum(bool(c['log']['direct_id_columns']) for c in cc);keyed=sum(c['log']['keyed_or_spring_context_rows'] for c in cc);hexn=sum(c['log']['hex16or32_rows'] for c in cc)
        invalid=[c['case'] for c in cc if c['metric_time_outside']]
        schema_num=len({c['metric_schema_id'] for c in cc});mshape=span([c['metric_columns'] for c in cc])
        chunks.append(f'\n## {ds}\n')
        chunks.append(f'\n### 1. {HEADINGS[0]}\n')
        chunks.append(table(['Mục','Nội dung'],[
            ['Hệ/biến thể','Sock Shop; RCAEval '+ds],
            ['Tác giả và nguồn công bố','Pham et al.; bài v2 §3, HF/code của tác giả. RE2: stress-ng cho tài nguyên/socket, tc cho mạng. RE3: sửa mã nguồn. Prometheus/cAdvisor/Istio và Vector/Loki/Elasticsearch; Jaeger được nguồn mô tả cho bộ benchmark, nhưng không có trace SS phát hành.'],
            ['Giấy phép','FACT nguồn: HF card và README tác giả khai báo dữ liệu MIT; code có LICENSE MIT, cần giữ notice. Không suy license từ chỉ công khai. Snapshot và phạm vi nguồn ở sources-audit/source-report.md.'],
            ['Tổng ca / ca có / ca được phép / thực kiểm',f'{s["cases"]} metadata / {n} ca local đã hash / {n} ca được phép / {n} ca thực đọc toàn metric, log, injection'+('; đủ 8 file nhãn chi tiết' if ds=='RE3-SS' else '')],
            ['Chỉ kiểm metadata','Không có ca SS ở trạng thái metadata-only sau task. Nguồn ngoài SS không mở telemetry ngoài metric OB phục vụ lineage; không mở RE2-TT ngoài dev hoặc dữ liệu khóa.'],
            ['Tái lập','acquire.py plan/acquire → inspect_files.py → build_card.py; lệnh và môi trường trong tai-lap.md. Census/file inventory, acquisition/manifest.json và inspection/manifest.json là kết quả gốc.']]))
        chunks.append('\nGiới hạn: khác tên hệ không chứng minh độc lập; khai báo Jaeger của toàn benchmark không bảo đảm SS có dữ liệu Jaeger. Giấy phép nguồn không tự xác nhận mọi quyền bên thứ ba.\n')
        chunks.append(f'\n### 2. {HEADINGS[1]}\n')
        chunks.append(table(['Tiêu chí MRP §4','Kết quả và trạng thái','Phạm vi/nguồn','Giới hạn / nguyên nhân khác'],[
            ['1. Công khai/tải/license','FACT: toàn file đọc được, hash đúng; nguồn khai báo MIT','acquisition/manifest.json; sources-audit/source-report.md','Truy cập xác nhận ngày kiểm; license công bố không là kiểm quyền bên thứ ba.'],
            ['2. Root và thời điểm','FACT: tên ca có root/fault/repeat; inject_time.txt cho lúc tiêm','census-cases.csv; inspection/cases.json','Tiêm khác onset quan sát; nhãn chỉ báo RE3 có giới hạn ở mục3.'],
            ['3. Parent trace','FACT: không có file trace ở toàn release','file-inventory.csv; census-summary.json','Không kiểm được parent/linkage/runtime graph; kịch bản graph kiến trúc là CANDIDATE riêng.'],
            ['4. Metric/log',f'FACT: {n}/{n} ca có cả hai, đều đọc được','inspection/cases.json; inspection/schemas.json','ID-like trong payload chưa là request join; metric/log có không đồng nghĩa mọi root hiện đủ tín hiệu.'],
            ['5. Root/vị trí',f'FACT: {len(s["roots"])} root; vị trí runtime OPEN, liên hệ kiến trúc nguồn ở mục3','census-cells.csv; sources-audit/architecture-root-positions.csv','Danh tính/root và topology có thể confound; hình tĩnh không pin deployment RCAEval.'],
            ['6. Nhóm lỗi','FACT nguồn: tài nguyên + mạng; không code fault ở RE2' if ds=='RE2-SS' else 'FACT nguồn: code fault f1–f4; không tài nguyên/mạng trong RE3','census-cells.csv; source report','Một biến thể riêng không đủ ba nhóm. Nhãn fault không chứng minh biểu hiện ở mỗi modality.'],
            ['7. Ngoài root','FACT khảo sát dải metric 3q với control, theo từng ca/ô/kênh','inspection/probe-summary.csv; inspection/probe-cases.csv; inspection/probe-cells.csv','Đồng thời vượt dải có thể do tải/drift/collector/OR nhiều kênh; chưa là lan truyền nhân quả.'],
            ['8. Normal',f'FACT: {span(mm.pre_rows.tolist())} điểm metric trước tiêm, nhịp {span(mm.median_step.tolist())} s','inspection/boundaries.csv','Không có nhãn healthy độc lập; đủ khảo sát hiện tại chưa bảo đảm đủ học mọi phương pháp.'],
            ['9. Bộ độc lập','FACT: RE1/2/3 cùng họ RCAEval; không tạo thêm bộ độc lập chỉ bằng SS','sources-audit/source-report.md; lineage/report.md','Tác giả/công cụ/collector cần so toàn bảng G1; khác testbed với TT/OB chưa đáp ứng cả ba trục.']]))
        chunks.append(f'\n### 3. {HEADINGS[2]}\n')
        own=cells[cells.dataset==ds]
        chunks.append(table(['Root','Loại lỗi gốc','Nhóm theo nguồn','Số ca','Lần lặp'],[[r.root,r.fault,'tài nguyên' if r.fault in ['cpu','mem','disk','socket'] else ('mạng' if r.fault in ['delay','loss'] else 'mã nguồn'),r.cases,str(r.repetitions)] for r in own.itertuples()]))
        chunks.append(f'\nFACT metadata: {s["cases"]} ca, {len(s["roots"])} root, {len(s["faults"])} mã lỗi, {s["cells"]} ô đã có; không có collision khóa root×fault×repeat. Nguồn: census-summary.json/census-cases.csv. Không suy ô không xuất hiện là file bị mất.\n')
        if ds=='RE3-SS':
            chunks.append('FACT nguồn: HF bảng README ghi f1–f5 cho SS, nhưng prose F5 nói riêng OB; README GitHub ghi f1–f4. FACT release: chỉ f1–f4. Giữ cả hai lời nguồn và census; không tự thêm ca f5. f1 là sai giá trị tham số, f2 thiếu tham số, f3 thiếu lời gọi, f4 sai giá trị trả về theo paper; loại lỗi không chỉ định dòng code thực của từng ca.\n')
            chunks.append('\n**Tám root_cause.txt đã đọc:** mỗi file một dòng CSV, sáu trường: giờ ngắn, timestamp nanosecond, service, message, pod, host. Bốn file carts là WARN “POST not supported”; bốn file front-end là access log HTTP500. Không chứa dòng sửa mã, stack trace, nhãn từng span/trace hay vùng ảnh hưởng.\n')
            chunks.append(table(['Ca','Loại chỉ báo','Timestamp nhãn − injection (s)','Message ghép own log','Trong cửa sổ log?'],rootrows))
            chunks.append('\nFACT: 8 file chỉ có 7 nội dung byte khác nhau. Nhãn front-end_f2_2 trùng f2_1; timestamp ngoài ca f2_2 và message không khớp log ca đó. Bảy file còn lại khớp service+message một hàng/ca; ba timestamp floor khớp chính xác, bốn lệch 1 s. Nguồn sources-audit/label-audit.json, inspection/root-cause-labels.json. CANDIDATE: có thể chép lại nhãn ca cũ hoặc sai clock/export/association; chưa có lịch sử annotation để phân xử. Không coi tám file là tám nhãn chỉ báo hợp lệ, không thay nhãn tiêm bằng timestamp hàng log.\n')
        chunks.append('\n**Vị trí root:** runtime có mặt và bậc vào/ra đều OPEN vì không có span. Không báo root “cô lập” hay bậc0 từ việc vắng trace. Hình kiến trúc Sock Shop công khai có Front-end nối Order/Payment/User/Catalogue/Cart bằng nét không mũi tên; Order→Shipping→Queue→Queue-Master có mũi tên. Với liên hệ tĩnh bỏ User bên ngoài và icon DB: front-end bậc không hướng5; orders2; carts/catalogue/payment/user1. Nguồn sources-audit/architecture-edges.csv và sources-audit/architecture-root-positions.csv; hình đã hash trong sources-audit/diagram-manifest.json; không đặt ngưỡng hub. Đây là FACT trên hình nguồn; áp dụng sang deployment RCAEval là CANDIDATE — chưa kiểm. Tên Cart/Order/User được giữ mapping nguồn; dịch tên sang carts/orders/user chưa xác nhận deployment. Vì cạnh front-end không có hướng, không tự báo in/out-degree cho nó.\n')
        chunks.append(f'\n### 4. {HEADINGS[3]}\n')
        chunks.append(table(['Nguồn','Phạm vi','Schema/chất lượng thực','Giới hạn'],[
            ['Trace','0 file / '+str(n)+' ca','Không có span; tổng span và mẫu số parent không xác định','Không phải trace rỗng; không có trace file. Không ghép ID với span.'],
            ['Metric',f'{n}/{n}; {total_metric:,} hàng',f'{mshape} cột; {schema_num} schema khác; time int64 epoch-second, các KPI double; '+f'{sum(c["metric_nulls"] for c in cc):,} null; {sum(c["metric_infinite"] for c in cc):,} infinite; duplicate time '+str(sum(c['metric_duplicate_time'] for c in cc)),'KPI theo entity_suffix; cpu/mem/diskio/socket/workload/error/latency-50/90. Đơn vị KPI chi tiết không có metadata chuẩn trong parquet; không tự suy ms/%/MB.'],
            ['Log',f'{n}/{n}; {total_log:,} hàng','timestamp int64 epoch-second; container_name/message string; direct trace/span ID column '+str(direct)+' ca; keyed/Spring context rows '+str(keyed)+', hex16/32-like rows '+str(hexn),'Regex rộng có false positive như request/user ID, không là join. RE3 Spring context chứa ID-like thật nhưng thiếu trace phát hành; không thấy ID-key không chứng minh payload hoàn toàn không có ID.']]))
        chunks.append('\nParent: total span/root/reference/unique-parent/missing/ambiguous/resolve đều N/A, không gán0% hoặc100%. Schema/null/constant/all-null và tên entity từng ca ở inspection/cases.json, inspection/schemas.json; refinement tách hằng khỏi all-null ở inspection/quality-refinement.json. Mẫu số log-ID là số hàng log của biến thể; không phải tỷ lệ trace coverage. Metric hằng có thể do normal, lỗi thu thập hoặc workload không chạy.\n')
        chunks.append(f'\n### 5. {HEADINGS[4]}\n')
        chunks.append(table(['Nguồn','Biên đầu so injection (s)','Biên cuối (s)','Midpoint − injection (s)','Pre/post rows'],[
            ['Metric',span(mm.start_minus_injection.tolist()),span(mm.end_minus_injection.tolist()),span(mm.midpoint_minus_injection.tolist()),span(mm.pre_rows.tolist())+' / '+span(mm.post_rows.tolist())],
            ['Log',span(ll.start_minus_injection.tolist()),span(ll.end_minus_injection.tolist()),span(ll.midpoint_minus_injection.tolist()),span(ll.pre_rows.tolist())+' / '+span(ll.post_rows.tolist())]]))
        chunks.append(f'\nInjection nằm trong mọi cửa sổ metric; ca ngoài cửa sổ: {len(invalid)}. Toàn {n} ca có metric biên đối xứng ±720 s; bỏ file nhãn vẫn có thể suy mốc tiêm bằng midpoint. Biên log đọc riêng ở boundaries.csv; biên hàng không chứng minh cơ chế exporter và midpoint không là onset. Nguồn không có nhãn healthy riêng/onset/end/affected region đã xác minh.\n')
        chunks.append('\nKhảo sát dùng 2/3 đầu pre làm reference, 1/3 cuối pre làm control, post từ injection; không gọi đây là normal sạch đã được xác nhận. Warm-up, drift, tải biến đổi, lỗi trước đó hoặc clock làm giả định sạch sai. Nguồn telemetry/lịch sử tải độc lập mới kiểm được giả định đó; G1 chốt giao thức, không lấp unknown bằng phần đầu file.\n')
        chunks.append('\nĐối chiếu nguồn: paper §3.3 nói 10 phút bình thường; file metric thực có 720 s (12 phút) trước tiêm. Giữ cả hai, không sửa lời nguồn hay cắt dữ liệu để khớp. Có thể mô tả giao thức chung khác phạm vi xuất file/phiên chạy; thiếu converter/deployment gốc để phân xử. Số ca của biến thể khớp bảng README; số lặp thực theo ô ở mục3.\n')
        chunks.append(f'\n### 6. {HEADINGS[5]}\n')
        chunks.append('Khảo sát mô tả theo T002 mục6. Với mọi kênh số: median reference, dải phân vị q của |x−median|, xét vượt dải ở control/post. Không chọn SLI bằng root; root gắn sau phép tính tất cả entity. Kênh có <30 điểm hữu hạn bị bỏ và giữ mẫu số; band0 tách riêng, không chia0. Không chạy detector/RCA, không tạo nhãn lan.\n')
        rows=[]
        for r in pp[pp['group'].isin(['all_metrics','latency90','cpu','mem','error'])].itertuples():
            rows.append([r.group,r.q,r.cases,f'{100*r.control_mean:.3f}%',f'{100*r.post_mean:.3f}%',r.cases_any_increase])
        chunks.append(table(['Nhóm tín hiệu','q','Ca hợp lệ','Control ngoài root','Post ngoài root','Ca có entity post > control'],rows))
        chunks.append('\nTỷ lệ trên chỉ dùng entity có tỷ lệ xác định ở cả control và post, lấy cùng entity cho hai cửa sổ; trung bình trong từng ca rồi trung bình ca hợp lệ. Không gộp thành phần trăm hàng hay tỷ lệ ca “lan”. Cột cuối chỉ bất kỳ tăng dương, chưa có ngưỡng mức tăng ý nghĩa. Tách theo ô ở inspection/probe-cells.csv và ca ở inspection/probe-cases.csv; từng kênh, band, mẫu số ở inspection/channel-bands.csv; tỷ lệ entity ở inspection/entity-rates.csv. Entity không tính cặp được lưu ở inspection/paired-entity-exclusions.csv.\n')
        flat=channels[(channels.dataset==ds)&channels.flat_band]
        chunks.append(f'\nCó {len(flat):,} bộ (ca,kênh,q) band0 trong {len(channels[channels.dataset==ds]):,} bộ kiểm; giữ band0 và null trong artifacts. Không thể gọi toàn dòng OR là bằng chứng lan: nhiều kênh làm OR tăng, mem có thể drift, workload và collector thay đổi cũng tạo đồng biến. Nhìn latency/error/cpu/mem riêng và control để tránh chép một số trung bình. Không thấy thay đổi ở metric không chứng minh log/trace không lan. Không có trace để kiểm thông tin lan theo cạnh.\n')
        ex=pd.read_csv(OUT/'inspection/probe-exclusions.csv');cx=pd.read_csv(OUT/'inspection/channel-exclusions.csv')
        chunks.append(f'\nCa/kênh không tính được: {len(ex[ex.dataset==ds])} bộ (ca,nhóm,q) không có entity ngoài root đủ tỷ lệ ở cả hai cửa sổ và {len(cx[cx.dataset==ds])} cặp (ca,kênh) không đủ30điểm hữu hạn reference. Danh sách, lý do và kênh ứng viên ở inspection/probe-exclusions.csv và inspection/channel-exclusions.csv; không biến vắng error-channel hay mất số đo thành “không có triệu chứng”.\n')
        chunks.append(f'\n### 7. {HEADINGS[6]}\n')
        chunks.append(table(['Task đánh giá','Nhãn cần / thực có','Chấm được đến đâu','Giới hạn'],[
            ['Xếp hạng root',f'{n}/{n} service root theo tên ca; injection theo file','MRR/Hit@k và NDCG theo relevance một root có điều kiện giao thức G1','Không root operation/span và không nhãn vùng; sổ ca đã nhìn phải được xét ở G1.'],
            ['Phát hiện theo thời gian','Có injection; chưa onset/end quan sát','Chỉ phép chấm gắn khoảng tiêm nếu G1/P7 định nghĩa, xử lý biên lộ nhãn','Không báo F1 tự phát hiện từ cửa sổ đã căn tiêm hoặc gọi độ trễ từ onset.'],
            ['Vùng ảnh hưởng','Không có ground truth (nhãn chuẩn) tập thành phần bị ảnh hưởng','Không chấm Precision/Recall/F1 vùng','Root và khảo sát dải ngoài root không là vùng thật.'],
            ['Bất thường từng trace','Không trace và không nhãn từng trace','Không chấm trace-level','Một dòng root_cause log không là nhãn từng trace hoặc kết quả RCA.']]))
        chunks.append('\nKhả năng huấn luyện giám sát, checkpoint, chuyển hệ và adapter còn tùy ngân sách nhãn/giao thức G1; không suy đủ học từ tổng số ca. Nhãn test chỉ để chấm theo MRP.\n')
        chunks.append(f'\n### 8. {HEADINGS[7]}\n')
        chunks.append('- Root/fault/repeat nằm ở tên thư mục; injection ở inject_time.txt; RE3 nhãn chi tiết còn có service/pod/host/message/time. Chỉ dùng census/chấm, không đưa đường dẫn hoặc nhãn vào phương pháp.\n- Biên metric toàn release này đối xứng quanh injection. Đổi tên/bỏ inject_time không loại đường suy mốc; chưa chạy detector nên chưa chứng minh có detector khai thác. Giải pháp giao thức phải chốt G1, không tự thêm cách cắt.\n- Runner chính thức đã kiểm đúng revision: runner-source/main.py:283 lấy service từ đường dẫn; :341–363 chọn SLI (chỉ báo chất lượng dịch vụ), có nhánh dùng service đó; :415 truyền sli vào phương pháp. URL/revision/hash ở runner-source/manifest.json. Chỉ đọc code, không chạy/import runner. Không có adapter mới trong T019 để tuyên bố đã loại rò.\n- [Sổ ca đã nhìn](so-ca-da-nhin.csv): toàn90 RE2-SS đã có kết quả RCA T006 qua torai-SS; 100 RE1-SS non-disk qua fse-ss. RE1 25disk ở T006 chỉ census metadata; T019 đã đọc metric, chưa thấy RCA trực tiếp trong manifests đã kiểm. T007 đã chạy đủ90 RE2-OB; fse-ob không có bản ghi chung với RE2-OB theo clock/nội dung kiểm, không tự là độc lập khoa học. T019 đọc số đo SS và OB metric, không chạy phương pháp.\n- Sổ phân biệt full metric-content, cùng dữ liệu hữu hạn thời gian sau bỏ hàng time-null, local byte-identical, và chưa xác lập; không đồng nhất time-only với identity. Sources tên khác không tạo test mới. Không tự chia dev/test hoặc đánh dấu ca được phép test.\n- Chia theo ô và bảo toàn theo WHY04/MRP là phương án G1; chưa chọn trong task. RCAEval SS/TT/OB cùng họ collector/injector/tác giả, không đủ bộ độc lập chỉ từ khác hệ.\n')
        chunks.append(f'\n### 9. {HEADINGS[8]}\n')
        chunks.append(table(['Mục','Giá trị / nguồn','Giới hạn'],[
            ['Toàn file SS biến thể',f'{s["bytes"]:,} byte / census-summary.json','Đây là bytes các file Parquet/text công khai, không archive và không logical uncompressed.'],
            ['Đã có trên máy',f'{s["files"]} file verified cho {n} ca ở data/T-019/','acquisition/manifest.json; data ngoài git.'],
            ['RAM/thời gian kiểm','inspection/manifest.json; inspection/resources-snapshot.json','Peak working set lấy trong lượt2, không tổng RAM laptop; tám phiên khác có thể làm wall time thay đổi.'],
            ['Chi phí adapter','CANDIDATE — chưa kiểm','Chưa viết/chạy adapter RCA do phạm vi cấm. Thiếu trace đòi kịch bản tĩnh riêng; không suy chi phí RCA từ inspection.']]))
        chunks.append(f'\n### 10. {HEADINGS[9]}\n')
        chunks.append(table(['OPEN','Vì sao/giả định và khi sai','Đầu vào/người giải quyết','Kết luận phụ thuộc'],[
            ['Root runtime degree/parent/log-trace','Release không có trace; giả định hình tĩnh tương ứng sai khi version/deployment/workload khác','Trace mới hoặc xác nhận deployment từ tác giả; Minh chốt G1 kịch bản','RQ1 theo vị trí và đồ thị quan sát RQ3d.'],
            ['Onset/end/normal sạch','File chỉ injection, cửa sổ đã căn tiêm; pre có thể warm-up/drift','Nguồn timeline/load độc lập và giao thức G1/P7','RQ3a tự phát hiện và delay.'],
            ['Nhãn vùng và lan causal','Không ground truth vùng; đồng biến do tải/collector/drift cũng có thể giải thích','Thiết kế P4/G3 theo kế hoạch, không mở test mới trong T019','RQ3c, giải thích lợi ích đồ thị.'],
            ['Nhãn detail RE3 lỗi association','Một duplicate ngoài cửa sổ; chỉ báo log không mã nguồn/onset','Tác giả xác minh annotation; Minh quyết cách dùng nhãn ở G1','Chấm indicator sâu, không ảnh hưởng census root theo tên.'],
            ['Đơn vị KPI/alias/deployment','Parquet thiếu unit chuẩn; labels nguồn dùng tên khác; chưa pin deployment SS RCAEval','Cấu hình thu thập/biến đổi từ tác giả hoặc source tương ứng','Mapping đồ thị/thời gian/self-time và adapter.'],
            ['Test/dev/baseline/label budget','Task bị cấm chọn/chạy phương pháp; sổ ghi exposure thay quyết định','Minh tại tổng hợp G1','P3/P7 hợp lệ, không coi dữ liệu đổi tên là chưa nhìn.']]))
        chunks.append('\nBằng chứng đủ cho census, file quality, nhãn, biên và khảo sát metric của release này. Chưa phân xử hiệu quả phương pháp đồ thị, nhân quả lan hay topology runtime. Thiếu trace có thể do phạm vi thu thập/instrumentation/phát hành; không chứng minh hệ Sock Shop không thể tạo trace. Không kết luận thắng/thua hoặc chọn thay Minh.\n')
        measured.append({'dataset':ds,'cases':n,'metric_rows':total_metric,'log_rows':total_log,'metric_columns_range':mshape,'metric_schemas':schema_num,'keyed_context_rows':keyed,'hex16or32_rows':hexn,'flat_channel_q_sets':len(flat)})
    s=sm['RE1-SS'];chunks.append('\n## RE1-SS — ghi ngắn\n')
    chunks.append(f'FACT toàn metadata/file: {s["cases"]} ca =5root×5fault×5lặp, {s["cells"]} ô; {s["metric_cases"]} metric+injection, log0/trace0. Tổng{s["bytes"]:,}byte. Đây là corpus metric, không đáp ứng trace TC3. Schema/biên được kiểm đủ125ca, census-summary.json và inspection/boundaries.csv theo artifacts. CANDIDATE kịch bản graph từ kiến trúc; không coi là trace benchmark.\n')
    chunks.append('Sổ lineage xác nhận local fse-ss100ca byte-identical RE1-SS local, nhưng chuyển Parquet HF có loại dòng thiếu time ở user_mem_1 và catalogue_disk_3 (disk không ở fse). Phần finite-time khớp với tolerance ghi manifest; không nói bản HF bảo toàn mọi dòng metric. T006 đã RCA100ca qua fse-ss;25disk chưa có evidence RCA trực tiếp. Không chọn/chia test.\n')
    chunks.append('\n## Kết quả gốc và phần cần Minh quyết\n')
    chunks.append('Đính chính task cũ ở dinh-chinh-task-cu.md; nội dung cần ghi tài liệu chung ở de-xuat-tai-lieu-chung.md. G1 quyết dùng/không dùng SS, kịch bản trace hay kiến trúc, phạm vi nhãn và cách chia sau khi xét sổ đã nhìn. Không có phương pháp RCA hoặc detector nào chạy trong T019.\n')
    (OUT/'the-sock-shop.md').write_text('\n'.join(chunks),encoding='utf-8')
    dump(OUT/'card-measurements.json',measured)

if __name__=='__main__':main()
