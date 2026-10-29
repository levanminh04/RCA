"""Assemble report from frozen outputs; no telemetry or method execution."""
import gzip, json, math, zipfile
from collections import Counter
import run as t
B=t.BASE;R=t.ROOT

def main():
    e=t.read(B/'evaluate-003/evaluation.json');f=t.read(B/'F2-stable-001/summary.json')
    chains=t.read(B/'evaluate-003/mechanism-chains.json.gz')['chains']
    source=t.read(R/'results/T-017/sources/download-manifest.json');pins={x['file']:x for x in source}
    ziprel='zenodo/rcabench-platform-feat-fse26.zip';zp=t.sr.SOURCE/ziprel;assert t.sha(zp)==pins[ziprel]['sha256']
    with zipfile.ZipFile(zp) as z:
        member=next(n for n in z.namelist() if n.endswith('cli/dataset_transform/make_nezha.py'));data=z.read(member)
    t.write(B/'source-contract.json',dict(converter=dict(path=str(zp),sha256=t.sha(zp),member=member,member_sha256=t.hashlib.sha256(data).hexdigest(),normal_lines=[537,584],A_lines=[479,495],metric_clock_lines=[153,177],duration_line=225),
          known=dict(normal_source='construct_data/<date>, minute from first unsorted glob log filename',A='inject through next inject minus60s, closed; final inject+10min',
                     our_N='same source/minute but P3 Time/end/half-open representation, front165 channels retained',
                     omitted='Node converter values are filtered out before MAIN; no Node causal claim',
                     not_identified='MAIN absolute normal_metric file and six-parquet bridge/actual published program'),
          health='Normal naming/source README is not proof of health; no assertion that whole construct_data is fault-free'))
    m4=[x for x in chains if x['method']=='M4'];main=[x for x in chains if x['method']=='MAIN'];micro=[x for x in chains if x['method']=='MICRO']
    fallback=[p for x in main for v in x['services'].values() for p in v['new_metric']['pools'] if p['fallback_to_incident']]
    ns=[]
    for rel in ('full-001/normal-2022-08-22-audit.json','pilot-001/normal-2022-08-23-audit.json'):
        x=t.read(B/rel);ns.append(dict(day=x['day'],metric_channels=len(x['channels']),finite_count_histogram=x['metric_n_finite_histogram'],spans=x['spans'],logs=x['logs'],
                 trace_log_hulls_s={v['kind']:(v['last_ns']-v['first_ns'])/t.NS for v in x['sources'].values() if v['kind']!='metric'}))
    mechanism=dict(normal=ns,M4=dict(cases=len(m4),case_channels=22*165,usable_metric_before=sum(x['usable_metric_before'] for x in m4),usable_metric_after=sum(x['usable_metric_after'] for x in m4),
                                  trace_vote_changes=sum(v['old']['trace']!=v['new']['trace'] for x in m4 for v in x['services'].values()),unchanged_A_logs=True),
                   MAIN=dict(native_CPU_network_fallback_pools=len(fallback),fallback_alert_counts=dict(Counter(x['alerts'] for x in fallback)),fallback_before=sum(x['fallback_old'] for x in main),
                             A_trace_components_unchanged=True,latency_pool='five cross-metric values at one time; not five independent normal timestamps'),
                   MICRO=dict(sufficient_normal_operations_all22=True,partition_counts_changed=sum((x['counts_old']['normal'],x['counts_old']['anomaly'])!=(x['counts_new']['normal'],x['counts_new']['anomaly']) for x in micro),
                              spectrum_all_nonnegative=True,claim='N changes SLO/trace partition/weighted spectrum; rank1 remains wrong. Does not isolate origin of every error.'),
                   hypothesis=dict(HN='No evidence of a general rescue by this normal source: MAIN worsens, MICRO rank1 unchanged, M4 metrics become unavailable; source/duration/coverage intertwined',
                                   HF2='Within-N differences observed; recovery cause not identified; nominal previous-end offset is not observed recovery'))
    t.write(B/'mechanism-summary.json',mechanism)
    interpretations=[dict(id='H-N',status='MIXED_NOT_SUFFICIENT_EXPLANATION',observation=e['summary'],mechanism='mechanism-summary.json',
                         supported='The choice of normal source/minute affects intermediate signals and ranks under fixed A.',
                         not_supported='Replacing P3 N with this minute universally repairs OB or identifies N contamination as cause.',
                         missing='Exact author metric normal/config/bridge; separation of source, duration, sample size, coverage and health.'),
                     dict(id='H-F2',status='DRIFT_OBSERVED_RECOVERY_OPEN',observation='F2-stable-001/summary.json',
                         supported='Early/late statistics differ on the same five-sample dev N.',not_supported='Differences caused by preceding fault recovery.',
                         alternatives=['workload change','ordinary variability','observation cadence/rounding','recovery'],missing='Observed recovery boundary/clean reference and controlled matched comparison; no test permission inferred.'),
                     dict(id='H-HISTORY',status='OPEN',missing='Actual published revision/entrypoint/cohort, exact normal_metric and conversion bridge, predictions and aggregation script',
                         next='A source-window contrast needs permission and exact neighboring injection timestamps; not executed under Q191.')]
    t.write(B/'phan-xu.json',dict(hypotheses=interpretations,task_status='awaiting_review_not_accepted',new_baseline_selected=False))
    lines=['# Đổi nguồn normal N trên Nezha-OB — T-042, Q-191','',
    'Đã thực hiện gói Minh duyệt: chỉ đổi N trên22ca dev, giữ A300 và các phương pháp/cấu hình. Kết quả không hỗ trợ nhận định rằng chỉ thay N bằng construct_data sẽ khắc phục độ lệch OB. Có tác động thật, gồm mất kênh do thiếu mẫu và kích hoạt fallback; chưa xác định normal có sạch hơn hoặc chương trình sinh bảng công bố.',
    '', '## Kết quả và cách đọc','',
    'Top1/MRR chính dùng kỳ vọng hòa của evaluator P3; “native” là thứ tự trả về thực tế, cùng mẫu số22. Hai độ đo được tách vì M4 mất metric tạo nhiều hòa. Không so hai quy tắc như cùng một số.',
    '', '| Phương pháp | Top1 kỳ vọng cũ → N mới | MRR cũ → N mới | Top1 native cũ → N mới | ΔTop1 kỳ vọng, điểm % |',
    '|---|---:|---:|---:|---:|']
    for m,s in e['summary'].items():
        a,b=s['old'],s['normal_source'];lines.append(f"| {m} | {a['hit@1']:.6f} → {b['hit@1']:.6f} | {a['mrr']:.6f} → {b['mrr']:.6f} | {round(a['native_hit1']*22)}/22 → {round(b['native_hit1']*22)}/22 | {s['delta']['hit@1']*100:+.3f} |")
    lines += ['', 'Nguồn số: evaluate-003/evaluation.json#/summary; từng ô ở /by_cell, từng ca ở /cases và evaluate-003/tables.md. M4 có20ca OK và2ca NO_EVIDENCE khi chấm; không bỏ2ca ấy. MAIN vàMicro có22caOK. “OK” ở đây là có đầu ra, không xác nhận phương pháp đúng hoặc nguồn normal sạch.',
    '', '## Đầu vào thực và phần khác converter','',
    '26file được ghim từ manifest tải T008, tổng41.268.767byte; không tải thêm. Mỗi ngày11metric,1log,1trace. Chỉ decode giá trị trong hai phút UTC được duyệt. Giữ165kênh và clock Time của P3; không thêm Node, không dùng TimeStamp. Trace giữ start>=low vàend<high, log/metric [low,high). Converter dùng TimeStamp, trace-start và biên đóng; các khác biệt ấy không bị giấu thành “tái lập tác giả”. A và membership từngmethod giữ nguyên; fingerprint trong input-audit.json mỗi ca. N ngày23 nằm sau một số ca nên bộ bọc Micro truyền nhóm nguồn trực tiếp, không dịch timestamp.',
    '', '| Ngày | Mẫu hữu hạn/kênh metric | Span N | Log N | Hull trace / log, giây |','|---|---:|---:|---:|---|']
    for n in ns:lines.append(f"| {n['day']} | 1 trên cả165kênh | {n['spans']} | {n['logs']} | {n['trace_log_hulls_s']['trace']:.3f} / {n['trace_log_hulls_s']['log']:.3f} |")
    lines += ['', 'Miền danh nghĩa một phút chỉ giữ phần capture thực có trong file, không dời file hay kéo thêm phút cho đủ dữ liệu. Không coi tên construct_data/normal là chứng minh khỏe. Hồ sơ T008 đã cảnh báo metric trùng byte với cây lỗi; điều đó không tự chứng minh hai miền chọn ở đây nhiễm lỗi. MAIN còn dùng normal_metric ở đường dẫn riêng trong source adapter; nguồn chính xác của file lịch sử ấy vẫn OPEN.',
    '', '## Chuỗi cơ chế và đối chiếu ca đúng/sai','',
    '**M4:** một mẫu < min_normal_metric=2 → toàn3.630kênh–ca metric unavailable → phiếu metric bằng0; log A giữ nguyên,16phiếu trace trong220service–ca đổi vì N khác. Đây là mất thông tin do độ phủ đầu vào kết hợp quy tắc đủ mẫu, không phải chứng minh normal sạch hơn.',
    '', '- Ca dev-3e27669440 (adservice CPU): root metric32→0, trace1→1, tổng33→1; frontend giữ trace+log=2. Root từ hạng1 xuống2. Cùng điều kiện mất metric nhưng dev-7d3c2fe6d1 (shipping CPU) vẫn hạng1 vì trace root còn1, các service khác0.',
    '- Ca dev-1ac905bc95 (frontend return): root giữ log1, các phiếu metric của đối thủ bị mất; root từ vị trí5–6 lên1. Đây là cải thiện nhờ loại bớt bằng chứng cạnh tranh, chưa xác nhận metric cũ là triệu chứng sai hay nền mới tốt hơn.',
    '- Ca dev-2bfc97b01e (checkout network): root metric16→0, không có phiếu log/trace → cả phương pháp abstain. Không chấm một root được ưu tiên ngẫu nhiên thành đúng.',
    '', '**MAIN M0:** CPU/network chỉ1N/pool → fallback lấy A tính ngưỡng. Có440pool fallback (trước0), cả440không phát cảnh báo. Pool latency vẫn đủ5giá trị nhờ gộp nhiều metric tại một thời điểm; không phải5mốc normal độc lập. Trace A và score trace không đổi; lognormal và fusion giữ nguyên quy tắc gốc.',
    '', '- Ca dev-2bfc97b01e: CPU root trước1alert×100, sau fallback0; latency sau1alert×20. Score root100→20, hạng1→5. Trong cùng cấu hình fallback, dev-9b9397a4dc (recommendation CPU) lại có10alert latency×20, score metric100→200 và hạng2→1. Vì vậy không gán mọi ca tăng/giảm cho một lá cờ fallback.',
    '', '**MicroRank repaired sham:** SLO/nhóm trace thay đổi ở22/22ca; đủ operation và std N, không fill. Hai nhóm vẫn rời nhau, A không đổi; weights, spectrum và phép ef²/(ep+nf) đã kiểm. Top1 vẫn0, MRR giảm khoảng0,708điểm%. Điều này loại lời giải “chỉ đổi nguồn N này là đủ cứu sham”, không bác bỏ mọi nguồn N hay mọi bản MicroRank.',
    '', '- dev-27252dca60:100trace bất thường thay94, root productcatalog từhạng3 xuống4. Operation ReadCatalog của root có mean/std3,56/5,05ms→3,50/4,39ms; score root đại diện299,297→124,488, trong khi cartservice đạt136,231 và các đối thủ khác còn cao hơn.',
    '- dev-8ecd9880ed: nhóm bất thường180→437 trên cùng751trace; checkout hạng9→8, vẫn thấp hơn các service khác. N có tác động nhưng không đủ làm root dẫn đầu. Không dùng “Top1 không đổi” để nói mọi trung gian không đổi.',
    '', 'Nguồn đầy đủ cho mọi ca đúng/sai và đối thủ: evaluate-003/mechanism-chains.json.gz#/chains; số tổng hợp tại mechanism-summary.json. Các ví dụ minh họa chuỗi đã lưu, không thay bảng toàn13ô và22ca.',
    '', '## Kiểm đầu–cuối N và giới hạn hồi phục','',
    f"Đã so hai mẫu đầu/cuối trên3.630kênh–ca, bỏ mẫu giữa theo kế hoạch. Thống kê chuẩn hóa xác định ở{f['defined_normalized']}, còn{f['undefined_normalized']}không xác định vì phương sai0/thiếu. Median |delta|/std5={f['median_abs_delta_over_std']:.6f}, P90={f['p90_abs_delta_over_std']:.6f}. Có{f['positive_delta']}delta dương, {f['negative_delta']}âm, {f['zero_delta']}bằng0 theo giá trị binary64. Không coi mỗi dấu khác0 là thay đổi vật lý; có kênh chênh ở độ chính xác lưu số.",
    '', 'Nguồn dùng trong kết luận là F2-stable-001/summary.json và /cases/*.json.gz. F2 NumPy ban đầu được giữ để truy vết;5kênh gần hằng vượt cận Cauchy do làm tròn mean, nên đã tính lại riêng thống kê bằng hữu tỷ chính xác của cùng binary64, không floor/epsilon, không rerun method. Counts/timestamp/minmax toàn3.630khớp; mọi trị chuẩn hóa sau sửa nằm trongsqrt5. Không dùng F2-summary cũ để diễn giải độ lớn.',
    '', 'Trace/log so hai nửa150giây trong N đã lưu ở F2.json.gz mỗi ca; phần thiếu một nửa được ghi UNAVAILABLE_HALF tại evaluate-003/F2-summary.json#/summary/trace_log_half_availability. Không suy kênh vắng thành khỏe.',
    '', 'Bảy cặp kề trong danh sách dev cách497–551giây, N bắt đầu17–71giây sau kết thúc danh nghĩa180giây của ca trước. Đây không phải toàn lịch tiêm và không có nhãn hồi phục quan sát. Kiểm đã xác nhận có sự thay đổi trong N, chưa phân biệt hồi phục, tải, biến thiên bình thường và cadence. H-F2 giữ OPEN về nguyên nhân.',
    '', '## Đáp phản biện và đính chính','',
    '| Điểm | Đánh giá sau tự kiểm | Xử lý và phần còn lại |','|---|---|---|',
    '| F1 | Đúng một phần; chặn kết luận hết đường phân xử | Đã ghi rõ N/A converter đã biết, trình và chạy N-only sau Q191. Fixture nguồn cũ đã có thông tin nhưng báo cáo chưa làm rõ. Không còn nói mọi normal phải xin tác giả; exact metric-normal/bridge vẫn thiếu. |',
    '| F2 | Ứng viên hợp lý; chưa xác nhận recovery | Đã kiểm đầu–cuối N đúng phạm vi; có biến động, chưa có chuỗi xác nhận hồi phục lỗi trước. Không dùng RE2-TT điểm cao để coi nền chắc sạch. |',
    '| F3 | Đúng một phần, không chặn | Đính chính M0 là literal Duration theo converter; main chia1000, NezhaRCA chia1e6. Hệ quả ngưỡng100giây chỉ thuộc nhánh sau. M0 vẫn không là toàn bộ pipeline lịch sử. |',
    '', 'So RE2-TT đúng: repo Hit1=0,833333/MRR=0,891111; bài FSE Top1=0,80/MRR=0,85. Chênh tương ứng3,33/4,11điểm%, khác tập ca; không dùng0,80 làm MRR công bố. Prior không đổi counts vẫn có thể đổi weights/spectrum/hạng; phản ví dụ cũ dev-8ecd9880ed hạng9→8 đã lưu. Có thể nhận ưu tiên N đáng làm sớm hơn, không nhận phép prior tất định vô ích.',
    '', 'Bổ sung bảng đối chiếu nguồn: converter có N một phút construct_data, A tới nextinject−60s (ca cuối+10phút); default CLI và MAIN khác đường, normal_metric/bridge còn thiếu; converter giữ Node không chứng minh MAIN dùng Node. Source-contract.json ghi pin và vị trí code. Giữ báo cáo/kết quả cũ làm lịch sử, bản này là đính chính và bổ sung hiện hành của lượt Q191.',
    '', '## Câu hỏi nguồn, hệ quả và bước tiếp','',
    'RQ1/P3: đã định lượng tác động của gói lựa chọn N trên cùng A, tách lỗi code/giao thức/thiếu đầu vào. RQ2/P4: xác nhận chuỗi thiếu mẫu→mất phiếu hoặc fallback trong điều kiện cụ thể; chưa xác nhận nền nhiễm lỗi hoặc nguyên nhân duy nhất của khoảng lệch công bố. DT18/cô được đáp ứng ở phân tích trường hợp hiệu quả/hạn chế, chưa là đánh giá phương pháp đồ thị hoặc hoàn tất RQ2.',
    '', 'Đối với FlashTicket: cần ghi nguồn và miền normal, đếm mẫu hữu hạn/độ phủ operation, phân biệt unavailable với khỏe, và công khai fallback trước xếp hạng. Muốn ước lượng theo thời gian phải thu đủ nhiều mốc normal đại diện tại nhịp đo thật; một số giá trị gộp khác loại không thay nhiều mốc độc lập. Collector tương lai không thể phục hồi một normal_metric lịch sử chưa được công bố. Quan hệ có thể giúp phân biệt tín hiệu cạnh tranh, nhưng phép này không chứng minh lợi ích đồ thị hoặc chọn cơ chế P6.',
    '', 'Không nói đã hết phép phân xử. Phần A theo converter chưa kiểm vì Q191 giữ A300. Phép tiếp theo cần đúng thời điểm tiêm liên kề để dựng [inject,nextinject−60s], quyền đọc miền bổ sung nếu chạm vùng khóa, và đối chứng A-only trên cùng N. Không tự lấy ca dev kế tiếp làm ca tiêm kế toàn lịch. Exact metric-normal/bridge/config/per-case output vẫn cần nguồn gốc. Các kết luận P6/P7 phụ thuộc; chưa chọn baseline, mở G3/test hoặc nghiệm thu.',
    '', '## Kiểm, chi phí và trạng thái','',
    'prepare:1282output cũ khớp manifest,26raw normal khớp hash. Fixture explicit N/A đạt2kiểm; pilot replay M4/main cũ và Micro explicit split khớp chính xác. Full dùng lại pilot, freeze66record trước nhãn. Evaluator P3 và phép tính độc lập khớp; trợ lý nội bộ kiểm độc lập22M4/22MAIN/22Micro từ output đãfreeze. Không thay phản biện Claude.',
    '', 'Giữ2lượt tổng hợp hỏng evaluate-001/002 và source/failure; evaluate-003 đạt. Không method rerun. F2 stable chỉ đọc lại metricN đã được duyệt, không chạy method. Nhánh runner Micro NO_EVIDENCE chưa được tổng quát hóa: nó sẽ dừng lô ở trạng thái khôngok ngoài missingbaseline; nhánh này không kích hoạt ở22ca hiện tại. Không gọi runner này đã kiểm trên mọi đầu vào khả dĩ.',
    '', 'Lượt method đầy đủ khoảng261giây, pilot khoảng12giây; F2 stable khoảng6giây. Peak RSS đo sau mỗi ca khoảng456MiB, không là đỉnh liên tục. Tổng byte/file cuối và wall từnglượt tại manifest/cost. Không tải/cài, không test, không sửa src/data/kết quả cũ, không commit/push/gửi Claude. Trạng thái: chờ phản biện; chưa nghiệm thu/đóng task.']
    (B/'bao-cao.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    t.write(B/'cost-and-runs.json',dict(runs={name:t.read(B/name/'cost.json') for name in ('pilot-001','full-001','F2-stable-001')},
             failed_evaluation_runs=['evaluate-001','evaluate-002'],successful_evaluation='evaluate-003',
             source_method_diagnoses=66,baseline_replays_only_pilot=True,raw_payload_saved=False,F2_extra_method_runs=0,
             measurement_limits='RSS sampled after cases, stdout/stderr for method runs; F2 stable stdout/stderr not separately captured, exit0 and progress/summary retained'))
    print('Report and source/hypothesis/mechanism/cost outputs written from frozen results.')
if __name__=='__main__':main()
