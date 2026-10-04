"""Build current sample cards/report strictly from saved audit artifacts."""
import collections,csv,datetime,hashlib,json,pathlib
BASE=pathlib.Path(__file__).resolve().parents[1]
def load(p): return json.loads((BASE/p).read_text(encoding='utf-8'))
def n(v): return f'{v:,}'.replace(',','.')
def utc(v): return datetime.datetime.fromtimestamp(v,datetime.timezone.utc).isoformat()

def main():
    sums=load('runs/inspect-008/summaries.json'); archives=load('runs/inspect-008/archives.json');final=load('runs/inspect-008/summary.json')
    compare=load('runs/validate-001/validation.json');link=load('runs/validate-003/validation.json')
    root='i-078923fb30cac1ede'; types={}; details=[];duplicates=[]
    for kind in ['Product_Review','Cloud_Computing']:
        subset=[x for x in sums if kind in x['archive']]; csvs=[x for x in subset if 'rows' in x]; arrays=[x for x in subset if 'cases' in x]
        typ={'csv_files':len(csvs),'csv_rows':sum(x['rows'] for x in csvs),'csv_ragged':sum(x['ragged'] for x in csvs),
             'invalid_utf8_files':sum(bool(x.get('invalid_utf8_bytes')) for x in csvs),'invalid_utf8_bytes':sum(x.get('invalid_utf8_bytes',0) for x in csvs),
             'npy_files':len(arrays),'npy_constant_columns':sum(c['constant'] for x in arrays for case in x['cases'] for c in case['columns']),
             'npy_nonfinite_values':sum(c['nonfinite'] for x in arrays for case in x['cases'] for c in case['columns']),
             'member_bytes':sum(m['bytes'] for a in archives if kind in a['path'] for m in a['members']),
             'zip_bytes':sum(a['zip_bytes'] for a in archives if kind in a['path']),
             'metric_cases':[],'log_feature_cases':[],'structured_csv_fields':sorted({k for x in csvs if x['member'].endswith('_structured.csv') for k in x['header']})}
        groups=collections.defaultdict(list)
        for x in arrays:
            target='metric_cases' if 'Metrics Data' in x['archive'] else 'log_feature_cases'
            for case in x['cases']:
                typ[target].append({k:case[k] for k in ['kpi','entities','features','shape','time_min','time_max','time_count','deltas']})
                for col in case['columns']:
                    groups[(case['kpi'],col['name'],col['sha256'])].append(x['member'])
                    if 'descriptive_bands' in col:
                        b=col['descriptive_bands']
                        for q in b.get('q',[]):
                            ref,control,fault=b['counts']; ec,ef=q['exceed']
                            details.append([kind,x['member'],case['kpi'],col['name'],col['name']==root,q['q'],b.get('median'),q['band'],q['zero_band'],ref,control,fault,ec,ef,ec/control if control else '',ef/fault if fault else ''])
        duplicates.extend([{'dataset':kind,'kpi':k[0],'entity_or_feature':k[1],'vector_sha256':k[2],'members':v} for k,v in groups.items() if len(set(v))>1])
        types[kind]=typ
    for b in link['log_bands']:
        for q in b['q']:
            ref,control,fault=b['counts'];ec,ef=q['exceed'];details.append(['Cloud_Computing','CSV hourly log rate','all events/hour',b['entity'],b['entity']==root,q['q'],b['median'],q['band'],q['zero_band'],ref,control,fault,ec,ef,ec/control if control else '',ef/fault if fault else ''])
    with (BASE/'cloud-descriptive-bands.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['dataset','member','kpi_or_channel','entity_or_feature','root_attached_after_measurement','q','reference_median','band','zero_band','reference_n','control_n','fault_n','control_exceed','fault_exceed','control_fraction','fault_fraction']);w.writerows(details)
    result={'scope':final['coverage'],'integrity':final,'datasets':types,'kpi_comparison_count':len(compare['comparisons']),
            'kpi_comparison_nonmatches':len(compare['comparison_errors']),'linkage':link['linkage'],
            'duplicate_numeric_vectors':duplicates,'descriptive_band_rows':len(details),
            'license_exact':'OPEN; internal noncommercial inspection only; WHY-14',
            'claims':'No raw–processed equivalence, actual trace graph, propagation labels, healthy normal ground truth, or release-wide quality claim'}
    (BASE/'file-inspection-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    pr=types['Product_Review'];cc=types['Cloud_Computing']
    report=f'''# LEMMA — kiểm bốn ZIP IT đã duyệt Q-47

**Đã kiểm toàn bộ member trong đúng hai ngày mẫu; chưa kiểm Original hoặc các ngày còn lại.** Không RCA, detector, training hoặc chia dữ liệu. LEMMA không phải bộ bảo toàn; không mở Bank/locked. Giấy phép cuối còn OPEN, việc kiểm nội bộ phi thương mại theo WHY-14 không là quyền chia sẻ payload gốc/phái sinh.

## Dữ liệu thực đã đọc và mức kiểm

Bốn ZIP cộng {n(pr['zip_bytes']+cc['zip_bytes'])} byte. File gốc nằm trên EC2 mới `/home/ubuntu/rca-t003/data/lemma/`; kết quả kiểm trong repo. [Download manifest](runs/download-001/manifest.json) và [phép so LFS độc lập của root](../T-003/runs/lemma-independent-hash-001/result.json) xác nhận đúng byte/SHA-256 public revision. Không dùng hash tự tính làm bằng chứng duy nhất về nguồn.

[inspect-008](runs/inspect-008/summary.json) tái dùng CRC/summary hợp lệ của inspect-007 và inspect-002, bổ sung schema khác. Có {n(final['crc_checked_members'])} file không phải directory đều đọc tới EOF/CRC đạt, {n(final['bytes_uncompressed'])} byte khai báo member, {n(sum(t['csv_rows'] for t in types.values()))} dòng CSV và {n(sum(t['npy_files'] for t in types.values()))} NPY được parse. Không giải nén nguyên cây; CSV đọc luồng, mỗi lần chỉ một NPY. Byte member là dữ liệu đã đi qua decompressor, không là nhu cầu ổ đĩa khi streaming.

| Mẫu | CSV / dòng | NPY | Member byte | UTF-8 lỗi / file | CSV ragged |
|---|---|---:|---:|---|---:|
| PR20211203 | {n(pr['csv_files'])} / {n(pr['csv_rows'])} | {pr['npy_files']} | {n(pr['member_bytes'])} | {n(pr['invalid_utf8_bytes'])} / {pr['invalid_utf8_files']} | {pr['csv_ragged']} |
| Cloud20240124 | {n(cc['csv_files'])} / {n(cc['csv_rows'])} | {cc['npy_files']} | {n(cc['member_bytes'])} | {n(cc['invalid_utf8_bytes'])} / {cc['invalid_utf8_files']} | {cc['csv_ragged']} |

Tất cả NPY ở mẫu dùng object dtype chứa pickle. [Bộ đọc an toàn](scripts/safe_npy.py) diễn giải một tập opcode thành đối tượng inert (không hoạt động), không import/gọi globals của payload, không pickle.load, không allow_pickle=True. Mọi primitive array có shape×itemsize khớp byte, order C, endian nhỏ và dtype f8/i8/i4 được kiểm trước đọc. GLOBAL ngoài whitelist và shape sai bị chặn trong tự kiểm. Surrogateescape giữ nguyên byte CSV không giải được UTF-8; chỉ đếm lỗi, không thay dữ liệu bằng ký tự khác. Giữ lỗi decoder/schema trước ở inspect-002/005; không gọi lỗi UTF-8 là CRC hỏng.

## Schema và nối nguồn tín hiệu

Metric NPY chứa dict theo KPI, các trường `KPI_*` hoặc `jaeger_*`, `Pod_Name`/`Node_Name`, `Sequence`, `time`. PR có cả hai kiểu khóa; không dùng loader chung cố định field cho mọi file. Processed log NPY là entity×time×feature; Cloud dict phẳng, PR dict lồng. Cloud golden/PCA có 15 entity; PR golden/frequency có 89/132 entity. CSV log có LineId, Time, Content, EventId, EventTemplate, ParameterList; template có EventId, EventTemplate, Occurrence. Đây là schema thực của mẫu, không thay schema Original.

Nối tên chính xác theo [validation linkage](runs/validate-003/validation.json), phân biệt metric, log CSV và log feature NPY; filename cung cấp entity provenance, không chứng minh body có ID service. Cloud đủ 15 metric entity/15 structured log filename, giao 15. PR số thực lưu trong file-inspection-summary.json; mapping p2n có 302 pod→node nhưng không là graph gọi dịch vụ. Raw→processed và pod→service selector mọi ngày vẫn OPEN.

Không ZIP mẫu nào chứa bảng span/parent; CSV log không có cột trace/span ID. Không tính unique-parent/graph degree từ processed log hoặc sơ đồ kiến trúc. ID có thể nằm trong payload nhưng không có hợp đồng span/parent để ghép được xác minh; không kết luận Original thiếu trace hoặc root cô lập.

## Nhãn và clock: nguồn khác nhau không được trộn

Cloud PPTX slide4–7 trong [labels](runs/inspect-008/labels.json) xác định AP host ip-10-1-100-109, instance i-078923fb30cac1ede; cause là API /api/cpu_stress/ chiếm một trong bốn CPU. Nó ghi bug 2024-01-24 03:10Z và failure time 03:10:51Z; đây là nhãn narrative của scenario, không phải onset đã được phát hiện độc lập từ số đo. Metric/log dùng UTC; nhãn PPTX này đã có Z, không dịch thêm chín giờ. JSON riêng có epoch thành09:10:51Z, lệch sáu giờ với PPTX; giữ xung đột, không sửa JSON và không dùng epoch đó đặt cửa sổ kiểm.

PR PPTX mô tả external NFS disk full, địa chỉ192.168.57.153, nối MongoDB-v1, rồi ảnh hưởng ratings. README gọi root MongoDB-v1; phải phân biệt entity nhãn benchmark và nguyên nhân vận hành ngoài cluster. Mẫu có mapping pod MongoDB, nhưng không suy NFS hiện diện trong metric/trace hoặc chấm pod thay storage mà chưa chốt đơn vị. PPTX có ví dụ Jaeger ngày khác; không đếm chúng thành span thật ngày20211203. Mốc tiêm/normal/recovery đáng tin cho PR vẫn OPEN.

NPY time là epoch giây; PR KPI CSV epoch microsecond và Cloud KPI CSV epoch giây. Giữ unit gốc, chuyển chỉ trong phép nối kiểm. Cadence thực và gap theo từng case nằm trong summaries.json, không lấy lịch source thay chất lượng file. Node/pod PR preprocessing giao thời gian, loại entity thiếu điểm và điền NaN theo code nguồn; không thấy NaN trong output không chứng minh raw không thiếu. Số nonfinite và constant theo kênh nằm trong file-inspection-summary.json/summaries.json.

## Kiểm KPI độc lập và giới hạn release

[validate-001](runs/validate-001/validation.json) đọc lại ba KPI CSV, group theo label/second, tự tính trung bình rồi so từng điểm với cột KPI cuối của mọi Sequence. Cloud 14/14 case khớp tất cả shared seconds, không missing/mismatch. PR 46/46 case không nối đầy đủ hoặc khác giá trị: kpi.csv chỉ có label ratings; NPY có thêm reviews/reviews-v2/reviews-v3. Ví dụ node ratings có63.976 điểm ghép, 37.938 điểm thiếu, 63.974 điểm khác; chênh lớn nhất104.261. Không sửa dữ liệu hoặc giả định CSV là nguồn trực tiếp của mọi NPY. Cần tác giả/nguồn preprocessing giải thích KPI khác, provenance, release hoặc lỗi exporter. Phép Cloud đạt và shape/byte kiểm an toàn là đối chứng cho logic reader, nhưng không thay xác minh PR.

Cloud log-feature NPY lưu KPI_Label ratings.book-info... dù metric/KPI CSV cùng archive ghi scenario8_app_request. Đây là metadata không khớp, không tự kết luận numeric payload thuộc PR. Cloud PCA chỉ kết thúc trước injection, không có fault segment để dùng như feature phủ toàn sự cố. Numeric vector trùng giữ tại duplicate_numeric_vectors; cột metric Cloud Error/Latency thường dùng chung số đo, không được đếm là hai lần lặp độc lập.

## Normal và mô tả tiêu chí7

Cloud PPTX ghi thu48h, lỗi giữa kỳ sau24h; đồng thời ghi có 502 trước lỗi. Vì vậy trước injection là **tham chiếu theo timeline nguồn**, không có nhãn healthy từng điểm. Chia hai nửa12h đầu làm tham chiếu và đối chứng,24h sau bug làm đoạn sự cố; không dùng root chọn SLI. Đây là phép mô tả P2, không detector/dev/test.

[cloud-descriptive-bands.csv](cloud-descriptive-bands.csv) ghi mọi entity/kênh/q=.95/.99/.995, median tham chiếu, band tuyệt đối, zero band, số mẫu và tử/mẫu đối chứng/sự cố. Metric từng giây; log CSV dùng số event/giờ UTC đầy đủ, bỏ giờ cắt qua biên, mỗi nửa chỉ11 mẫu nên q log thô. Log feature golden có đoạn sau lỗi; PCA denominator sau lỗi0 được giữ trống, không gọi0% bất thường. Root gắn sau khi tính. Không OR các kênh, không regex mức lỗi làm nhãn vùng. PR không tính band normal vì thiếu mốc normal được xác minh và KPI không khớp; dùng tùy ý phần đầu sẽ đóng OPEN bằng giả định.

Co-occurrence ngoài root có thể do workload chung, nhiễu, threshold zero, recovery chưa biết, hoặc preprocessing. Không xem vượt band là nhãn ảnh hưởng/lan truyền thật. Nhãn vùng và bất thường từng trace vẫn thiếu; RQ3c hoặc đánh giá graph cần nguồn bổ sung.

## Chi phí, tự phản biện và tiếp nhận

Download 27,540s; full initial audit 200,284s; correction inspect-007 135,206s; schema supplement008 2,824s tái dùng kết quả. Lượt004 dừng tối ưu giữ progress/console, không ghi2,824s như thời gian toàn scan. MaxRSS lớn nhất audit hoàn tất khoảng901.348KiB. Các bước kiểm chạy có chồng thời gian; đây là chi phí quan sát trên EC2, không benchmark method hoặc dự báo adapter toàn release. Lượt lỗi/interrupt không xóa. Không tải lại ZIP; script --reuse-run chỉ tái dùng summary cùng archive/member CRC đạt và giữ đếm byte lỗi đã có.

Tự phản biện: (1) parse object có thực thi payload không — không, reader whitelist/inert và hostileselfcheck; (2) CRC đạt là chất lượng schema đạt không — không, lỗi parser giữ riêng; (3) metric/NPY log entity có bị trộn không — đã sửa, validate-003 là bản đúng; (4) một ngày là census release không — không; (5) PR KPI mismatch có thể do parser không — Cloud toàn bộ so khớp, PR vẫn cần nguồn riêng; (6) normal24h nguồn có sạch không — chưa; (7) metadata Cloud ratings có làm log payload thuộcPR không — chưa chứng minh. Không dùng dữ liệu này kết luận graph thắng/thua.

Chạy lại đọc source offline và builder local; audit EC2 dùng `inspect_files.py --data /home/ubuntu/rca-t003/data/lemma --results <new-run> --reuse-run <saved-run>`. Giữ run mới, không đè. Toàn release và Original không nằm trong bốn ZIP được duyệt; kế hoạch mở rộng cần đúng quyền/byte trước làm. G1 do Minh quyết, Claude review gộp T003.
'''
    example='\nVí dụ từ đúng CSV kết quả, q=.99 ở file Latency/cpu_usage; đây là từng kênh, không là kết luận trung bình toàn hệ:\n\n| Kênh/entity | Vượt band đối chứng | Vượt band sau bug |\n|---|---|---|\n'
    for name in [root,'i-03e386f9757915c39','i-04a5da0032591b1f6','Latency']:
        row=next(x for x in details if x[1]=='20240124/Latency/pod_level_data_cpu_usage.npy' and x[3]==name and x[5]==.99)
        example+=f'| {name} | {n(row[12])}/{n(row[10])} ({100*row[14]:.2f}%) | {n(row[13])}/{n(row[11])} ({100*row[15]:.2f}%) |\n'
    example+='\nCPU tại root thay đổi rõ ở kênh này; CPU các entity khác và KPI Latency không cùng có tỷ lệ vượt tăng. Không dùng ví dụ này chứng minh lan truyền hoặc phủ mọi kênh. Trung bình KPI theo giây có thể che các request tail; đây là khả năng giải thích, chưa được kiểm từ request outcome/route trong task.\n'
    report=report.replace('Co-occurrence ngoài root',example+'\nCo-occurrence ngoài root')
    (BASE/'kiem-file.md').write_text(report,encoding='utf-8')
    cards='# LEMMA-RCA — thẻ IT sau kiểm mẫu Q-47\n\nNguồn: [xác minh nguồn và độc lập](xac-minh-nguon-va-doc-lap.md). File thật: [báo cáo kiểm](kiem-file.md), [summary](file-inspection-summary.json). Chỉ kiểm Preprocessed PR20211203 và Cloud20240124; Original và ngày khác chỉ metadata. OT bỏ theo Q-47. Bank bảo toàn theo Q-49; LEMMA không giữ ngoài.\n'
    for kind,title,date in [('Product_Review','Product Review','20211203'),('Cloud_Computing','Cloud Computing','20240124')]:
        t=types[kind];l=next(x for x in link['linkage'] if x['dataset']==kind);cloud=kind=='Cloud_Computing'
        label=('PPTX xác định AP instance i-078923fb30cac1ede, bug lúc 03:10Z và failure time 03:10:51Z ngày 24/01/2024. Đây là nhãn theo tác giả, không phải onset đã kiểm độc lập. Epoch JSON riêng lệch sáu giờ.' if cloud else 'README gọi root MongoDB-v1. PPTX mô tả nguyên nhân external NFS đầy đĩa, nối MongoDB rồi ảnh hưởng ratings. Giữ riêng entity nhãn benchmark và nguyên nhân vận hành ngoài cluster; chưa thay pod bằng storage hoặc ngược lại.')
        normal=('Nguồn ghi 24 h trước bug, nhưng cũng ghi có 502 trước lỗi. Phần này là tham chiếu theo timeline, không có nhãn healthy từng điểm. PPTX có UTCZ nên không dịch chín giờ thêm; không áp quy tắc này để sửa JSON. Cloud PCA log feature kết thúc trước injection.' if cloud else 'KPI CSV dùng epoch microsecond, NPY dùng epoch giây và log UTC. Mốc injection/normal/recovery của ngày mẫu chưa xác minh; không lấy một phần đầu tùy ý làm normal. Ví dụ Jaeger trong PPTX có ngày khác, không là span thật của mẫu.')
        quality=('14/14 Sequence KPI case khớp phép tính trung bình CSV theo label/second, không thiếu hoặc khác điểm. Cloud log-feature NPY lưu KPI_Label ratings.book-info... trong khi metric/KPI CSV ghi scenario8_app_request. Chưa xác nhận vì sao metadata này khác; không suy numeric payload thuộc PR.' if cloud else '46/46 Sequence case không nối đầy đủ hoặc khác giá trị so kpi.csv. CSV chỉ có ratings; NPY thêm reviews/reviews-v2/reviews-v3. Ví dụ node ratings: 63.976 điểm ghép, 37.938 điểm thiếu, 63.974 điểm khác. Cần giải thích provenance/KPI hoặc exporter; không tự sửa release.')
        bands=('Đã tính q=.95/.99/.995, độ lệch tuyệt đối so median 12 h tham chiếu,12 h đối chứng và 24 h sau bug. Log CSV dùng event/giờ UTC đầy đủ, bỏ giờ cắt biên; q log chỉ có 11 mẫu mỗi nửa nên thô. Tử/mẫu và zero band từng entity/kênh ở cloud-descriptive-bands.csv; PCA sau lỗi có denominator 0 nên tỷ lệ để trống. Root gắn sau tính, không chọn SLI theo root.' if cloud else 'Chưa có normal/mốc lỗi được xác minh và KPI provenance còn khác. Không tính band bằng một phần thời gian chọn tùy ý. Chất lượng toàn mẫu đã kiểm; cần nguồn mốc và normal để phép mô tả có ý nghĩa.')
        cards+=f"""
# {title} — Original và Preprocessed

## 1. Danh tính, nguồn và phạm vi

LEMMA-RCA, Zheng và cộng sự; [paper v4](https://arxiv.org/html/2406.05375v4), [code tác giả](https://github.com/lemma-rca/rca_baselines), [Original](https://huggingface.co/datasets/Lemma-RCA-NEC/{kind}_Original), [Preprocessed](https://huggingface.co/datasets/Lemma-RCA-NEC/{kind}_Preprocessed). Revision khóa tại [manifest](runs/source-final-001/manifest.json). Original/Preprocessed chung lineage. License NC/ND chính xác còn OPEN; kiểm nội bộ phi thương mại theo WHY-14 không cấp quyền chia sẻ payload phái sinh. Đã kiểm toàn bộ member hai ZIP metric/log ngày {date}; các ngày khác và Original chỉ metadata.

## 2. Bảng tiêu chí MRP1–9

| Tiêu chí | Kết quả đúng phạm vi mẫu |
|---|---|
| 1. Công khai/tải/license | Byte/LFS SHA public revision khớp; license cuối OPEN. |
| 2. Root/time | Nhãn và clock theo mục3/5; không suy mốc tiêm thành onset đã kiểm. |
| 3. Trace cha–con | ZIP mẫu không có span table; parent/degree Original OPEN. |
| 4. Metric/log | {t['npy_files']} NPY, {n(t['csv_rows'])} CSV rows; chất lượng kiểm từng file. |
| 5. Root/vị trí | Có mapping entity; không có trace graph để đo bậc root. |
| 6. Nhóm lỗi | {'API infinite loop gây CPU contention' if cloud else 'External storage disk full ảnh hưởng database'}; một scenario chưa phủ mọi nhóm. |
| 7. Triệu chứng ngoài root | {'Đã có mô tả theo từng kênh/q kèm đối chứng' if cloud else 'Normal/mốc lỗi và KPI lineage chưa đủ'}; không nhãn vùng. |
| 8. Normal học ngưỡng | {'Có timeline 24 h trước lỗi, chưa nhãn healthy' if cloud else 'OPEN, không dùng phần đầu tùy ý'}. |
| 9. Độc lập | Raw/processed chung lineage; PR/Cloud chưa đủ coi hai bộ độc lập; không census raw reuse xuyên bộ. |

## 3. Nhãn, ca và khả năng phân xử

{label} Một ngày mẫu không là census root×fault×repetition toàn release. Nguồn có 4 PR/6 Cloud date token; không coi chúng là incident count. Sơ đồ PPTX không thay trace graph. Bậc root và confound vị trí–loại lỗi vẫn OPEN.

## 4. Schema và chất lượng ba nguồn tín hiệu

NPY object dict dùng KPI_* hoặc jaeger_*, Sequence/time và Pod_Name/Node_Name. Log NPY có layout entity×time×feature; CSV structured có LineId, Time, Content, EventId, EventTemplate, ParameterList. Static reader không thực thi pickle. Có {n(t['npy_nonfinite_values'])} nonfinite và {n(t['npy_constant_columns'])} constant column occurrences, kể cả KPI/alias; {n(t['invalid_utf8_bytes'])} byte không giải được UTF-8 trong {t['invalid_utf8_files']} CSV; {t['csv_ragged']} ragged rows. Encoding khác có thể giải thích, chưa gọi file hỏng. Cadence/gap/unit và từng kênh xem summaries; preprocessing có thể che missing raw.

Metric có {len(l['metric_entities'])} tên entity; structured log có {len(l['log_entities'])} tên file; giao chính xác {len(l['exact_overlap'])}; log-feature NPY có {len(l['log_feature_entities'])} entity. Ba tập giữ riêng. {'Root instance có trong cả metric/log.' if cloud else 'p2n có 302 pod→node, không là graph gọi dịch vụ.'} Không cột trace/span ID trong CSV; ID trong payload và khả năng ghép parent chưa có hợp đồng được xác minh. Không suy Original thiếu trace.

## 5. Normal và thời gian

{normal} Cadence là FACT file, tách khỏi lịch nguồn. Injection, narrative failure time và recovery là ba loại thông tin khác; không tự sửa clock/nhãn.

## 6. Mô tả thô triệu chứng ngoài root

{bands} Co-occurrence có thể do workload chung, nhiễu, threshold zero hoặc preprocessing. Không OR các kênh, không regex mức lỗi làm nhãn vùng, không kết luận propagation từ vượt band. Đây là mô tả P2, chưa chọn detector hoặc chia dev/test.

## 7. Task nào chấm được?

Ranking root là CANDIDATE theo đúng đơn vị nhãn sau chốt mapping. {'Cloud có label instance trực tiếp.' if cloud else 'PR cần giữ khác biệt pod MongoDB và storage cause.'} Time detection cần giao thức và interval nhãn phù hợp, không gọi onset đã verified. Không nhãn vùng/trace thật để chấm segmentation hoặc trace anomaly. Không RCA/baseline/training chạy trong task.

## 8. Rò nhãn, provenance và G1

Không đưa date/PPTX/root vào đầu vào phương pháp. Case-dependent KPI/metric selector code nguồn chưa là adapter an toàn cho chế độ tự phát hiện. {quality} Vector trùng giữ ở summary, không đếm alias thành lặp. Không chia Original/Preprocessed cùng ca sang hai phía. Chưa chọn dataset thí nghiệm.

## 9. Kích thước và chi phí

Hai ZIP mẫu {n(t['zip_bytes'])} byte; {n(t['member_bytes'])} byte member được stream. Toàn kho Original PR 53.633.808.946byte/Cloud 33.002.132.069byte theo [census](runs/run-001/count-summary.json), chưa tải. Full audit 200,284s, correction 135,206s, bổ sung schema 2,824s tái dùng kết quả; không gọi 2,824s là toàn scan. Xem kiem-file cho RAM/lượt lỗi/interrupt và giới hạn dự báo chi phí.

## 10. OPEN và owner

Tác giả: exact license, {'JSON/PPTX time và Cloud log-feature KPI_Label' if cloud else 'PR KPI provenance và mốc normal/injection'}. Codex/Minh: nguồn Original/parent, phủ ngày khác, đúng unit ranking; mở rộng cần quyền và byte cụ thể trước làm. Minh: chọn G1/thí nghiệm; Claude review gộp T003. Không xem kiểm một ngày là kiểm toàn release hoặc đáp ứng mọi tiêu chí G1.
"""
    (BASE/'the-dataset.md').write_text(cards,encoding='utf-8')
    print(json.dumps({'datasets':{k:{j:v for j,v in t.items() if not isinstance(v,(list,dict))} for k,t in types.items()},'band_rows':len(details)},ensure_ascii=False))

if __name__=='__main__': main()
