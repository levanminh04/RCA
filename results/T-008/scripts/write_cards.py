"""Write dataset cards from saved inspection evidence, preserve old card."""
import argparse,collections,json,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];R=ROOT/'results/T-008';parser=argparse.ArgumentParser();parser.add_argument('--run',required=True);args=parser.parse_args();OUT=R/'runs'/args.run;OUT.mkdir(exist_ok=False)
if (R/'the-dataset.md').exists():shutil.copyfile(R/'the-dataset.md',OUT/'previous-card.md')
audit=json.loads((R/'runs/evidence-002/summary.json').read_text());source=json.loads((R/'runs/run-001/summary.json').read_text());trace=json.loads((R/'runs/trace-symptoms-002/result.json').read_text());full=json.loads((R/'runs/file-audit-001/summary.json').read_text());leak=json.loads((R/'runs/sampling-leakage-001/result.json').read_text())
cards=[]
for ds,title in [('OB','Online Boutique'),('TT','Train Ticket')]:
    a=audit['datasets'][ds];s=source[ds];positions=[r for r in audit['root_windows'] if r['dataset']==ds];perroot=collections.defaultdict(collections.Counter)
    for r in positions:
        if r['clock_interpretation']=='text_as_utc':perroot[r['root']][r['position']]+=1
    normal=a['normal_trace_windows'];c=[r for r in trace['calibration'] if r['dataset']==ds];results=[r for r in trace['results'] if r['dataset']==ds];groups=[g for g in trace['groups'] if g['dataset']==ds]
    totals=collections.defaultdict(collections.Counter)
    for x in results:
        key=(x['date'],x['clock'],x['q'],x['outside_root']);totals[key]['samples']+=x['n'];totals[key]['exceed']+=x['exceed']
    text=f'''# Nezha {title} — thẻ đã kiểm file trong phạm vi

## 1. Danh tính, nguồn và phạm vi đã kiểm

Nezha FSE 2023, nhóm Guangba Yu và cộng sự. Nguồn chính: [README ghim](sources/README.md), [bài](sources/FSE2023_Nezha.pdf), [manifest nguồn/revision](runs/run-001/manifest.json). Stack công bố OTel/Tempo, Promtail/Loki, cAdvisor/Istio/Node Exporter/Prometheus. Công cụ lỗi code Byteman/Hypno/Failpoint; công cụ CPU/network cụ thể chưa khóa từ nguồn đã kiểm, không suy từ tên lỗi.

Repo LICENSE MIT; artifact Zenodo ghi other-open. Chưa xác nhận phạm vi license riêng của dữ liệu và quan hệ phiên bản artifact; công khai không tự chứng minh mọi quyền. Tải ghim Git revision, byte và Git blob hash khớp [download](runs/download-001/manifest.json), không chạy code RCA tác giả.

Trong biến thể này đã đọc toàn {a['files']} CSV được đề xuất, {a['bytes']} byte, {a['rows']} hàng CSV tính theo file (không phải unique incident/span), gồm construct/rca trên hai ngày. Không lấy kết quả phương pháp. Quyền Q47; OpenRCA Bank giữ ngoài là bộ khác. [File audit](runs/file-audit-001/summary.json) không parse error; thẻ này không đại diện release khác hoặc phần ngoài inventory.

## 2. Bảng chung tiêu chí MRP §4

| Tiêu chí | Bằng chứng và giới hạn |
|---|---|
| 1. Công khai/giấy phép | Tải thành công, revision/hash khớp. Repo MIT; license data/artifact cần giữ đúng scope, chưa chốt thay tác giả. |
| 2. Root/time | {s['events']} record tiêm, {s['root_count']} service gốc; thời điểm tiêm không phải onset; clock và bản ghi trùng xem mục5. |
| 3. Cha–con | {a['trace_files']} trace CSV đã đọc; parent scoped trace_id+span_id, root sentinel riêng. Số theo mục4; duplicate/ambiguous không tự resolve. |
| 4. Metric/log/liên kết | {a['metric_files']} resource metric CSV và log có ID; linkage thật theo từng file. Cột TimeStamp có vấn đề ở OB, không sửa dữ liệu. |
| 5. Root/vị trí | Đếm từng root tại cửa sổ quanh tiêm và hai cách hiểu clock; không kết luận bằng graph trung bình. |
| 6. Lỗi | Nhãn nguyên bản nhiều nhóm; không tự tạo nhóm thiếu hoặc suy biểu hiện từ tên nhãn. |
| 7. Triệu chứng ngoài root | Đã khảo sát Duration theo pod+operation, q/control, xem mục6. Vượt ngưỡng không là nhãn vùng hoặc bằng chứng nhân quả. |
| 8. Normal | Trace construct có cửa sổ ngắn; resource metric construct trùng fault ở nhiều file. Strict mask không đủ train/control. |
| 9. Độc lập | Nhóm/collector/công cụ/reuse đối chiếu [ma trận](../T-012/independence-matrix.md); TT/OB cùng họ không tự là hai bộ độc lập. |

## 3. Ca, root, loại lỗi, lần lặp và vị trí

Record tiêm/cell/root lấy từ [labels](runs/run-001/labels.json), [cells](runs/run-001/cells.json), [summary](runs/run-001/summary.json), không đếm CSV thành ca. Loại lỗi: `{json.dumps(s['fault_counts'],ensure_ascii=False)}`. Giữ lặp từng root×fault/date trong cells; không cộng hai cách hiểu clock thành hai lần lặp.

Graph là quan hệ gọi parent→child giữa service suy từ pod theo alias tên nguồn; không có bằng chứng đủ cạnh message/data-dependency. Dùng toàn minute-file chạm injection±60s, không gọi đó là interval sự cố. Root không thấy không gọi cô lập. [Từng ca/cả hai clock](runs/evidence-002/summary.json).

| Root | Vị trí quan sát trong từng cửa sổ, text hiểu UTC |
|---|---|
'''
    for root,count in sorted(perroot.items()):text+=f'| {root} | `{dict(count)}` |\n'
    text+=f'''
## 4. Trace, metric, log và liên kết

Parent counts (đơn vị hàng span theo file): `{a['span_parent']}`. Mẫu số không-root {a['nonroot_denominator']}; resolved duy nhất {a['span_parent'].get('unique_resolved_within_file',0)}, ambiguous {a['span_parent'].get('ambiguous_within_file',0)}. {a['duplicate_span_keys']} khóa span trùng theo file. Boundary file/lấy mẫu có thể giải thích missing, không tự gọi lỗi tracing. [SQL kiểm độc lập](runs/independent-check-001/result.json) đối chiếu first/last trace mỗi phase/date, toàn bộ census do file-audit thực hiện.

Log cùng tên phút: `{a['log_join']}`. Khớp (TraceID,SpanID) duy nhất khác có ID khác ghép được clock giữa metric/log/trace. Metric clock TimeStamp−Time text: `{a['metric_timestamp_minus_text_seconds']}`; không tự sửa. [Schema/kênh/cadence/gap/NaN/constant từng file](runs/file-audit-001/summary.json). Counts overlap giữa normal/fault không là observations độc lập.

## 5. Dữ liệu bình thường, nhãn và mốc thời gian

Root từ pod→service trong labels/cells; inner-service mapping riêng không thay root service. Nhãn có inject_time và inject_timestamp, injection chưa phải onset. Một số TT lệch text/epoch; giữ từng record và hai clock hypotheses trong evidence/trace-symptoms, không đoán timezone hoặc chữa nhãn. Timestamp metric OB có độ lệch lớn so Time text đã kiểm; ghép nguồn phải chọn clock có bằng chứng ở bước dùng sau, không chọn vì kết quả đẹp.

### Dữ liệu bình thường

README gọi construct_data fault-free, nhưng toàn họ có {len(audit['identical_normal_fault_paths'])} path normal/fault khớp SHA256, gồm resource metric. Do đó không dùng cả construct metric để học clean threshold. Cửa sổ trace normal trong biến thể:

'''
    for n in normal:text+=f"- `{n['path']}`: {n['rows']} span rows, start {n['start']}, end {n['end']}; không tự mở rộng phút ngoài bounds.\n"
    text+=f'''
Metric strict trace bounds không đủ chia ≥2 điểm reference và ≥2 control trên các ngày. [symptoms-003](runs/symptoms-003/result.json) đã kiểm và không sinh calibration hợp lệ; không phải bỏ kiểm do chi phí. symptoms-001 và 002 giữ lại cùng cảnh báo invalid/limited, không dùng kết luận. Trace normal đủ nhiều span để khảo sát Duration nhưng chỉ cửa sổ ngắn, load/recovery/correlation chưa chứng minh sạch/đủ học ngưỡng cho toàn nhiệm vụ.

## 6. Khảo sát triệu chứng ngoài root

Đã kiểm toàn trace normal/fault theo pod+operation, raw Duration (đối chiếu [units](runs/units-001/result.json) với End−Start, đơn vị µs), chronological first half normal reference/second half control, median absolute deviations q=.95/.99/.995; root ghép sau đo. [Kết quả/từng ca/kênh/q/control](runs/trace-symptoms-002/result.json). Không OR qua operation/kênh hoặc gọi exceedance là propagation. Ref n thấp nhất {min(x['reference_n'] for x in c)}, cao nhất {max(x['reference_n'] for x in c)}; tail có ít mẫu phải đọc n/control ngay cùng số, các span không là quan sát độc lập.

Hai clock có thể phân bổ span khác ca. Interval đến lần tiêm kế tiếp chỉ là cửa sổ mô tả; interval cuối đến hết file không là fault duration. Operation/pod không có normal reference được đếm missing, không zero-score. Thay đổi load, mix operations, lỗi trước chưa recovery và capture boundaries đều có thể gây/che exceedance ngoài root. Vì vậy kết quả hỗ trợ khảo sát thô trên scope, không chứng minh vùng ảnh hưởng hoặc tiêu chí7 đạt mọi ca.

## 7. Task chấm được

| Task | Nhãn và giới hạn |
|---|---|
| Ranking nguyên nhân | Chấm service root theo record tiêm, sau giải clock/mapping/cửa sổ và giao thức G1; nhãn inner-service là task khác. |
| Phát hiện theo thời gian | Trace/log bị cắt theo tiêm, thiếu negative coverage giữa các lần tiêm: không chấm P/R/F1 phát hiện liên tục công bằng từ corpus này riêng lẻ. Metric lưu theo ngày là phạm vi khác; cần giải clock, normal và protocol trước chấm. Injection không phải onset. |
| Vùng ảnh hưởng | Không có nhãn vùng thật đã xác minh; chỉ mô tả vùng nghi ngờ/chứa root khi task sau định nghĩa. |
| Trace anomaly | Không thấy nhãn từng trace trực tiếp; không tự gán mọi trace sau tiêm là anomalous. |

## 8. Rò nhãn và thông tin phục vụ G1

[Kiểm độc lập toàn 101 record](runs/sampling-leakage-001/result.json): trên cả bốn ngày, trace/log/traceid rca_data có đúng các file phút [phút nhãn tiêm, +1, +2], không có các minute-file giữa các lần tiêm. Tổng mỗi modality là 303 = 3×101. Construct chỉ có một trace-file mỗi ngày. Đây là điều kiện chọn khi thu/xuất dữ liệu, không chỉ là cách T008 chọn mẫu. Tên file và việc file tồn tại mang thông tin suy từ nhãn; đổi tên không khôi phục negative coverage bị thiếu. Trace/log phù hợp chấm ranking có điều kiện biết trước cửa sổ, chưa hỗ trợ benchmark tự phát hiện liên tục không biết trước thời điểm từ corpus này riêng lẻ. Không gọi thiếu file là healthy sample hoặc gán trace trong cửa sổ là anomalous.

Toàn họ Nezha có 112 file resource rca được file-audit ghi bounds Time text, mỗi file có cadence/gap trong [bounds từng file](runs/sampling-leakage-001/result.json); đây là file theo service/ngày, không phải 303 minute-file trên. Bounds không chứng minh toàn thời gian là normal; TimeStamp và text có lệch nên không nhập chung clock. Nhãn/tên/path/time và root-derived SLI chỉ dùng census/chấm; adapter chưa có, không claim đã loại mọi rò nhãn. Cùng testbed/stack khác ngày không tự chứng minh độc lập.

## 9. Chi phí và cách dựng lại

Download/hash toàn họ mất 287.828s, whole CSV audit 88.219s; thời gian từng lượt trong manifest/summary, không phải thời gian toàn công việc. Không giải nén file raw. [Plan tải](runs/download-plan-001/plan.json), script `../T-003/scripts/download_verified.py`; kiểm bằng `scripts/inspect_files.py --run <mã_mới>`, `scripts/inspect_trace_symptoms.py --run <mã_mới>` cần run mới nếu chạy lại (không ghi đè). Data không vào git; kết quả/script/manifest giữ repo. Không xóa source sau khảo sát.

## 10. Kết luận phạm vi, phần chưa kiểm và dữ kiện cần

Có root injection và ba nguồn thực, parent/log join đã kiểm toàn file trong inventory, graph/cost/cadence/clock từng file có kết quả. Chưa có onset/end/nhãn vùng hoặc nhãn trace thật để tự suy task; đó là thiếu bằng chứng nhãn, không phải mặc định public dataset phải đủ. Normal resource không đủ bằng chứng sạch, cần timeline/recovery/normal capture bổ sung từ tác giả hoặc giao thức sau có căn cứ. Độ lệch clock và tham chiếu source license cần giải trước dùng kết luận chấm. Không chọn dataset thí nghiệm, không chia dev/test, không RCA/MyRCA. T003 tự phản biện độc lập trước Claude, merged REVIEW tại parent.
'''
    cards.append(text)
(R/'the-dataset.md').write_text('\n---\n\n'.join(cards),encoding='utf-8');print('Wrote two cards, 10 sections each')
