"""Summarize only serialized, hash-verified diagnostics; do not run methods."""
from collections import defaultdict, Counter
from datetime import datetime, timezone
import gzip
import json
import math
from pathlib import Path
from simple_runner import ROOT, OUT, sha, write


def read(path):
    path=Path(path)
    if path.suffix=='.gz':
        with gzip.open(path,'rt',encoding='utf-8') as f:return json.load(f)
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    simple=read(OUT/'simple-evaluate-001/evaluation.json');extra=read(OUT/'extra-evaluate-001/summary.json')
    micro=read(OUT/'micro/evaluate-001/summary.json');prior=read(OUT/'micro/prior-evaluate-002/summary.json')
    labels={r['opaque_id']:r for r in read(ROOT/'results/T-026/nhan-dev.json')['cases']}
    chains=[];invalid=[];graph=[];numeric=[]
    for file in ['micro/cached-001/diagnosis-list.json','micro/full-004/diagnosis-list.json','micro/prior-full-002/diagnosis-list.json']:
        doc=read(OUT/file);assert doc['completed'] and not doc['labels_read']
        for row in doc['records']:
            path=ROOT/row['path'];assert sha(path)==row['sha256'];v=read(path);assert not v['labels_read']
            oid=row['opaque_id'];root=labels[oid]['root'];b=row['branch']
            if b=='upstream_rcaeval':
                invalid.append(dict(opaque_id=oid,cell=labels[oid]['cell'],source=row,
                    reasons=v['invalid_reasons'],negative_cell_count=len(v['negative_cells']),
                    negative_examples=v['negative_cells'][:3],main=v['main']))
                continue
            if b=='upstream_graph_only':graph.extend(dict(opaque_id=oid,**g) for g in v['contrast'])
            if b=='repaired_sham':numeric.append(dict(opaque_id=oid,**v['checks']['sham_exact_vs_cached']))
            diagnosis=v['diagnosis'];entity=diagnosis['entities'].get(root)
            detail=None
            if entity:
                op=entity['operation'];detail=dict(operation=op,score=entity['score'],spectrum=v['spectrum'].get(op),
                    rank_min=entity['rank_min'],rank_max=entity['rank_max'])
                groups=v.get('weights_and_counts') or {g:x['official'] for g,x in v.get('groups',{}).items()}
                if groups:detail['weight_and_coverage']={g:dict(weight=q['weights'].get(op),traces=q['tracecounts'].get(op)) for g,q in groups.items()}
            chains.append(dict(opaque_id=oid,branch=b,root=root,cell=labels[oid]['cell'],source=row,counts=v.get('counts'),root_evidence=detail,
                top_entities={s:d for s,d in diagnosis['entities'].items() if d['rank_min']==1},
                interpretation='Root joined only after source diagnosis freeze; no new source-level physical root-cause claim'))
    write(OUT/'micro-mechanism-chains.json',dict(chains=chains,upstream_invalid=invalid,graph_contrasts=graph,numerical_replays=numeric,
        matched_cells=['recommendationservice|cpu_consumed','checkoutservice|exception']))
    costs=[]
    for path in sorted(OUT.rglob('cost.json')):costs.append(dict(path=path.relative_to(ROOT).as_posix(),data=read(path)))
    for path in [OUT/'contracts/full-summary.json',OUT/'contracts/histogram-001/full-summary.json']:
        costs.append(dict(path=path.relative_to(ROOT).as_posix(),data=read(path)['cost']))
    failures=[dict(run='source-contract-001',kind='overbroad source scanner assertion; other RCABench readers reference paired files; corrected Nezha-path claim in002'),
        dict(run='micro/pilot-001',kind='auxiliary repeated-operation list ordering assertion; Counter equality used next, no method change'),
        dict(run='micro/full-001',kind='bitwise numerical replay stricter than existing numeric tolerance; preserved audit and bit/order/weights evidence'),
        dict(run='micro/full-002',kind='root stopped worker to bound storage; future outputs gzip, all existing files preserved; cost not fully sampled at termination'),
        dict(run='micro/full-003',kind='two nonmaximum operations within same service swap by2ULP; service rank/ties/max operation exact; full004 retains every changed position and16ULP AND16eps bound')]
    write(OUT/'cost-and-runs.json',dict(costs=costs,failed_or_stopped=failures,
        uncertainty='Full002 stopped without worker cost-finally; elapsed clock can be reconstructed from invocation/progress/budget-stop, CPU/peak not available. Contracts probe RSS API returned null, not zero. Simultaneous work timings are not speed comparisons.',
        datasets_read='22 allowlisted dev windows only',downloads=0,shared_src_edits=0,commits=0,pushes=0))
    hist=read(OUT/'contracts/histogram-001/full-summary.json');contracts=read(OUT/'contracts/full-summary.json');clock=read(OUT/'contracts/map-and-time-summary.json')
    adjudication=dict(status='maker_complete_awaiting_Claude_review',authority='Q-190',
        decisions_added=['Q-190 execution extension only'],baseline_selected=False,source_scientific_question_closed=False,
        hypotheses=[
          dict(id='H-S1',result='SUPPORTED within matched P3 input',observation='main.py source kernel M0 Top1=15/22 versus frozen M4 S0=7/22',
               consequence='Published program identity and preprocessing are material; M4 alone does not represent every SimpleRCA source branch',
               limit='main.py not default CLI; source window/normal/clock/labels pairing not same as paper',evidence='simple-evaluate-001/evaluation.json#/summary'),
          dict(id='H-S2-duration',result='SUPPORTED interaction with source fusion; not a recommended fix',
               observation=simple['contrasts']['M0 -> M1'],consequence='duration x1000 changes22 score sets and18 root ranks; metric-positive gate suppresses trace while other services receive large absolute trace scores',
               limit='M0 better dev score does not validate wrong units; kernel input assumedns differs converterus',evidence='simple-evaluate-001/mechanism-chains.json#/chains'),
          dict(id='H-S2-log-clock',result='CHANGES scores but does not explain rank gap here',observation=simple['contrasts']['M1 -> M2'],evidence='simple-evaluate-001/evaluation.json#/contrasts'),
          dict(id='H-S3-severity',result='SOURCE CONVERTER LOSS confirmed; raw not wholly missing',observation=hist['counts'],
               consequence='Observed lower/uppercase and unknown policy alter ranks; full author level construction still unproven',evidence='extra-evaluate-001/summary.json#/summary'),
          dict(id='H-S4-TimeStamp',result='SOURCE FIELD INCONSISTENCY confirmed on selected dev rows',observation=clock,
               consequence='TimeStamp projection drops90 selected adservice rows in9cases; T-M0 Top1=16/22, not sufficient to identify paper program',evidence='time-projection-001/*-audit.json'),
          dict(id='H-M1-formula',result='Formula alone does not rescue registered partitions',observation=micro['branches'],
               consequence='Sham remains0/22; mo15c1 worsens6→5 and mo1p50c1 remains8; no universal repair or new winner selected',evidence='micro/evaluate-001/summary.json#/paired'),
          dict(id='H-M2-graph',result='Edge loss affects computation; alone insufficient for Top1 gap',
               observation=dict(groups=len(graph),groups_with_removed_edges=sum(bool(r['removed_edges']) for r in graph),groups_with_added_edges=sum(bool(r['added_edges']) for r in graph)),
               consequence='Same groups/incidence/occurrences, original graph changes MRR but Top1 stays0/22',evidence='micro-mechanism-chains.json#/graph_contrasts'),
          dict(id='H-M2-upstream',result='INVALID weighted spectra on22/22',observation=dict(cases=len(invalid),negative_cells_min=min(r['negative_cell_count'] for r in invalid),negative_cells_max=max(r['negative_cell_count'] for r in invalid)),
               consequence='Pre/post graph and counted-group mismatch creates impossible negative cells; upstream return cannot be a valid performance prediction',
               limit='RCAEval kernel, not original paper program',evidence='micro-mechanism-chains.json#/upstream_invalid'),
          dict(id='H-M3-prior',result='Expression/kind/scope differences real; not enough to fix Top1 on sham',observation=prior['summary'],
               limit='Conditional on sham partition and repaired matrices; not all combinations, not paper reproduction',evidence='micro/prior-evaluate-002/summary.json')],
        remaining=[
          dict(question='Which exact program produced published SimpleRCA0.91 / MicroRank Table3?',classification='MISSING identifying evidence, not lack of local experiments',
               needed=['exact revision+entrypoint+config+cohort and per-case predictions','actual normal inputs and conversion bridge','evaluator aggregation used for tables'],
               why_stop='Several source branches and input contracts remain possible. Matching aggregate accuracy on dev cannot identify historical pipeline. Additional ad hoc variants would not supply provenance.',
               dependent='Direct reproduction, attributing published gap to a single cause, selecting official baseline'),
          dict(question='Severity of112587 rows without a real field?',classification='MISSING measurement',needed=['actual severity from instrumentation/source owner or approved convention with acknowledged uncertainty'],
               why_stop='Keywords or assigning INFO would fabricate labels; two-agent agreement cannot recover the field',dependent='Full severity-based source diagnosis and observation requirements'),
          dict(question='Does a different method or graph improve diagnosis?',classification='NOT YET EVALUATED',needed=['approved design, matched controls and later allowed held-out evaluation'],
               why_stop='T042 contrasts qualify mechanisms on dev; cannot infer generalization or choose new method from the same inspected cases',dependent='P6/P7/G3/RQ3')])
    write(OUT/'phan-xu-bo-sung.json',adjudication)
    lines=['# T-042 — Kết quả nối tiếp theo Q-190','',
      'Đã phân xử thêm được bằng chứng cụ thể. Chênh lệch ban đầu không thể gói thành “không tìm thấy bằng chứng”. Mã nguồn, trường đầu vào, cách ghép điểm và một số lỗi cài đặt thực sự làm đổi kết quả trên cùng22dev. Chưa định danh được chương trình sinh các bảng công bố; không chọn baseline mới, không nghiệm thu hay đóng task.','',
      'Đầu ra trước Q-190 giữ nguyên tại results/T-042/bao-cao.md và manifest.json. Báo cáo này bổ sung và làm rõ những OPEN trước đó: severity có trong phần lớn raw log; cây lời gọi và Eq7 vẫn có thể kiểm được. Quyền nối tiếp ghi ở DECISIONS Q-190, WHY-54 và LOG. SPEC cũ không sửa.','',
      '## Kết quả SimpleRCA','',
      '| Nhánh | Đúng hạng1 native /22 | MRR native | Ý nghĩa |','|---|---:|---:|---|']
    descriptions={'M0':'Hàm main.py; duration literal từ converter; time log native','M1':'M0 đổi duration vềns theo chú thích code','M2':'M1 thêm timestamp datetime cho log','N0-partial':'Metric+trace NezhaRCA, literal duration; không log','N1-partial':'Metric+trace NezhaRCA, physicalns; không log','M4-no-log':'M4 bỏ log, đối chứng phạm vi modality'}
    for b in ['M0','M1','M2','N0-partial','N1-partial','M4-no-log']:
        s=simple['summary'][b];lines.append(f"| {b} | {round(s['native_hit1']*22)} | {s['native_mrr']:.6f} | {descriptions[b]} |")
    lines+=['','M4 S0 trước nối tiếp đúng7/22. M0/M1/M2 đều là nguyên hàm source trên hợp đồng P3, chưa phải pipeline tác giả: main.py là nhánh khác CLI NezhaRCA, nguồn normal/window khác; không mặc nhiên nhận nó là SimpleRCA trong bài. Không chọn giữ sai đơn vị chỉ vì dev cao hơn. Bảng đầy đủ22ca/13ô và kỳ vọng tie: simple-evaluate-001/tables.md; số JSON: evaluation.json#/summary, /by_cell, /rows.','',
      'Duration×1000 đổi điểm22/22 và hạng gốc18/22. Đổi time log làm đổi điểm20/22 nhưng không đổi hạng gốc. Trong main.py, chỉ cần metric>0 là trace bị bỏ khỏi phép ghép; trace của dịch vụ metric=0 vẫn được dùng ở thang thời lượng tuyệt đối. Đây là chuỗi cài đặt xác nhận trong source và số trung gian, không phải nguyên nhân của mọi ca sai.','',
      'Đối chiếu cùng ô checkout exception: dev-b0f8b2e3ac có metric160, log100 và trace256180.5 ở M1, nhưng fusion chỉ190, hạng6. dev-55f99f3e0a có metric0, trace190132.2, log100 nên fusion190202.2, hạng1. Với recommendation cpu_consumed, dev-9b9397a4dc có metric100 nên bỏ trace; dev-515c5f2190 có metric0 nên dùng trace và đúng hạng1. Các pool/ngưỡng/đếm và dịch vụ cao điểm hơn được lưu cho mọi ca tại simple-evaluate-001/mechanism-chains.json#/chains.','',
      '## Log và trường thời gian','',
      f"Probe trên22cửa sổ có{hist['counts']['rows']} lượt dòng log; {hist['counts']['resolved_rows']} có severity thật ở JSON lồng, {hist['counts']['unknown_rows']} thiếu. Đây là lượt dòng theo ca, không phải đếm log vật lý duy nhất của toàn dataset. Converter chỉ lấy chuỗi log và không xuất level; mất trường là hạn chế converter, không được kết luận raw hoàn toàn không có severity. Tất cả outer log làstring nên helper extract_message chưa str-cast tương đương trên đúng miền đã kiểm.", '',
      '| Hợp đồng level | Top1 native /22 | MRR native |','|---|---:|---:|']
    for b in ['L0','L1','L2']:
        s=extra['summary']['level-seed0/'+b];lines.append(f"| {b} | {round(s['native_hit1']*22)} | {s['native_mrr']:.6f} |")
    lines+=['','L0 giữ chữ thực và null; L1 uppercase chữ quan sát, null giữ nguyên; L2 uppercase rồi chỉ dùng dòng có severity. L0/L1: null!=INFO trong kernel bị tính non-INFO; không phải bằng chứng dòng đó là lỗi. L2 thiếu độ phủ, không phải toàn bộ log. Mọi dòng thiếu giữ unknown, không gán INFO. Dùng lại metric/trace N1, chỉ chạy kernel log/vote từ histogram. Ba hash seed cho cùng score/ranks trên66cặpca–hợpđồng; không xác nhận ổn định ngoài miền này.','',
      'Ca checkout exception dev-b0f8b2e3ac: L0 rơi sang fallback non-INFO, xếp gốc hạng4; L1 giữ sự tăng error thật, gốc hạng1. Ca đúng tương ứng dev-55f99f3e0a vẫn hạng1. Ngược lại ở recommendation cpu_consumed dev-515c5f2190, bỏ unknown chuyển nhánh log sang INFO-count reduction và có thể làm gốc mất hạng1. Do đó không cộng các cờ hoặc gọi một hợp đồng level là chân lý. Histograms/các count N/A/service và nhánh source lưu ở contracts/histogram-001 và level-seed*/. Bảng toàn ca/ô: extra-evaluate-001/tables.md.','',
      'Metric có hai trường thời gian không khớp:90hàng đã chọn ở adservice trong9ca nằm ngoài cửa sổ nếu dùng TimeStamp×1e9 của converter;45hàng đổi N/A. Độ lệch lớn nhất khoảng200triệu giây. Không sửa clock. Projection chỉ xét chính hàng đã allowlist, không tìm hàng khác có TimeStamp rơi vào cửa sổ. Native metric audit trước projection khớp bit score/rank cũ. T-M0 tăng15→16ca hạng1; M1 vẫn5; các L vẫn8/10/9. Mâu thuẫn trường là FACT; chưa xác nhận trường nào phản ánh đồng hồ runtime đúng. Kết quả không phải exact author window. Nguồn: contracts/map-and-time-summary.json, metric-time-exceptions.json và time-projection-001/*-audit.json.','',
      '## MicroRank','',
      '| Phép giữ các yếu tố còn lại | Top1 /22 trước→sau | MRR trước→sau |','|---|---:|---:|']
    for a,b in [('cache_sham_dstar2','cache_sham_ochiai'),('cache_md_dstar2','cache_md_ochiai'),('cache_mo15c1_dstar2','cache_mo15c1_ochiai'),('cache_mo1p50c1_dstar2','cache_mo1p50c1_ochiai'),('repaired_sham','upstream_graph_only')]:
        x=micro['branches'][a];y=micro['branches'][b];lines.append(f"| {a} → {b} | {round(x['hit@1']*22)}→{round(y['hit@1']*22)} | {x['mrr']:.6f}→{y['mrr']:.6f} |")
    lines+=['','Dstar2/Ochiai dùng lại88bộ weight/count đã ghim, không chạy lại PageRank. Phép đổi graph giữ đúng nhóm trace, incidence và occurrence; khác cạnh thật do builder cũ reset danh sách cạnh theo dòng. Trên cả22ca đổi graph đơn lẻ không cứu Top1; không dùng đặc tính chung của graph làm nguyên nhân mọi sai.','',
      f"Kernel RCAEval nguyên hàm hoàn tất nhưng INVALID22/22: mỗi ca có{min(r['negative_cell_count'] for r in invalid)}–{max(r['negative_cell_count'] for r in invalid)} ô spectrum âm. Ví dụ pilot: graph anomaly chứa991trace, anomaly_count chỉ94; normal/anomaly đếm chồng94trace. nf âm vì đếm toàn graph với số nhóm nhỏ hơn. Giữ nguyên output native, không dùng điểm INVALID làm prediction hợp lệ hoặc báo accuracy0 như kết quả của thuật toán hợp lệ. Nguồn: micro-mechanism-chains.json#/upstream_invalid; source kernel/line và revision ở micro/*/source-checks.json. Đây là RCAEval, chưa phải chương trình nguyên thủy sinh Table3.", '',
      'Đã đọc trực tiếp ảnh bài và xác nhận Eq7 khác biểu thức prior code. Giữ nguyên ma trận và phép PageRank: kiểm normalization-only, Eq7 cùng coverage-set kind, đổi riêng kind A theo cây identity, đổi cả kind N và đổi scope sang uniqueoperation. Đủ19.080trace–ca sau end split có cây identity đơn gốc/không cycle/không missingparent;58trace có bản lặp, chỉ collapse identity để định kind, giữ occurrence trong graph/scope cho tới phép đổi scope. Có74nhóm–ca cùng operation set nhưng khác cây; không dùng thiếu span.kind làm lý do dừng đại số.','',
      '| Prior | Top1 /22 | MRR |','|---|---:|---:|']
    for b,s in prior['summary'].items():lines.append(f"| {b} | {round(s['hit@1']*22)} | {s['mrr']:.6f} |")
    lines+=['','Tất cả vẫn0/22 ở phân hoạch sham, MRR chỉ đổi rất nhỏ. Kết luận có điều kiện, không phải phủ định prior/đồ thị trên mọi phân hoạch. Các ma trận cố định, vector/weight/spectrum và scope/duplicates lưu tại micro/prior-full-002/; đủ22ca/13ô trong prior-evaluate-002/summary.json. Source graph/operator/order/weights được tự kiểm; một cặp operation không phải max trong shipping đổi thứ tự2ULP, service order/tie/max operation giữ nguyên. Không che khác biệt hoặc sửa manifest cũ.','',
      'Matched-case MicroRank: cùng ô recommendation cpu_consumed, dev-9b9397a4dc ở mo15c1 có gốc không nằm trong anomaly support (ef=nf=1e-7), hạng9; mo1p50c1 đưa gốc vào nhóm có support và lên hạng1. dev-515c5f2190 đúng trong mo15c1, nhưng điều kiện nhóm khác. Đổi prior ở sham vẫn giữ counts/coverage nên không thể thay phần bằng chứng bị detector loại. Toàn bộ root/top intermediate và cặp ca đúng/sai được lưu tại micro-mechanism-chains.json#/chains; không suy duy nhất detector giải thích mọi ca sai.','',
      '## Đã phân xử tới đâu và vì sao dừng thực nghiệm ở đây','',
      'Đã phân biệt được nguồn hạn chế: bất nhất hai trường thời gian và severity không có ở một phần dòng là vấn đề đầu vào; bỏ severity/thiếu bridge pairedfiles và metric wide là converter/adapter; mismatch graph–count là cài đặt RCAEval; gate ghép điểm/scale thời lượng, detector và công thức prior là cách tính/giả định. Các nhóm chồng lấn nên không cộng thành tỷ lệ nguyên nhân. Chưa xác nhận lợi ích của phương pháp đồ thị mới.','',
      'Cặp orig NezhaRCA tốiđa5 với report mặc định ZIP không đồng thời giải thích hàng Table2 Top1=Top5=MRR=.91: report lọc hit trước MRR, nên nếu Top1/Top5 đều làm tròn.91 thì conditionalMRR≥.905/.915≈.989, không thể làm tròn.91. single.py còn đường per-case miss=0; vì thiếu script bảng không kết luận cả artifact hay bài sai. Fixture adapter gốc với sáu pairedfiles không tồn tại trả sáu frame rỗng/ranks[]; đường convert Nezha xuất ba singularfiles, chưa có bridge đã định danh trong caller tương ứng. Nguồn/algebra: source-contract-002/fixtures.json và evaluator-contract.json.','',
      'Phần chưa phân xử được tiếp bằng nguồn đang có là định danh lịch sử chương trình/bộ dữ liệu/cách chấm đã sinh0.91 và Table3. Cần exact revision+entrypoint+config/cohort, normal inputs, bridge conversion, per-case prediction và script tổng hợp của tác giả. Normal riêng trong construct_data không thuộc allowlist; không mở nó. Nhiều biến thể có thể cho cùng số tổng; thêm cấu hình trên22dev không cung cấp provenance này. Không nhận là mọi thí nghiệm có thể nghĩ ra đã hết: các tổ hợp khác hoặc phương pháp mới vẫn có thể nghiên cứu, nhưng chưa phải bằng chứng để xác nhận pipeline công bố hay đủ căn cứ chọn thiết kế.','',
      'Với các giả định cùng56ca/cùngTop1/dev22 là tập con, ngay cả T-M0 đúng16ca thì cận tốt nhất(16+34)/56=.892857<.905, vẫn loại cohort-only cho chính chương trình đó; không đọc34test và không xác nhận giả định cohort tác giả. Con số này không cho phép tự chọn biến thể theo dev.','',
      'Hệ quả FlashTicket: cần ghi severity có schema thống nhất, đơn vị thời gian tường minh và đồng hồ đối chiếu; giữ parent/span identity đủ dựng cây và thông tin nhóm cho mọi bước chấm. Đây là yêu cầu quan sát rút từ thiếu/mất trường đã xác nhận; collector tương lai không khôi phục dữ liệu lịch sử chưa ghi. Dữ liệu đủ để đề xuất kiểm ứng viên có căn cứ, chưa đủ xác nhận lợi ích/khóa thiết kế P6 hay mở G3.','',
      '## Kiểm, chi phí và bàn giao','',
      'Nguồn/revision/AST và manifest được kiểm trước dùng; chỉ22dev, payload RAM; không tải/cài, không mở test/giữngoài, không sửa src/SPEC, không commit/push hoặc gửi Claude. Có132Simple,198severity (3seed×66),110projection,242Micro công thức/graph/native và132prior diagnosis records; số này bao gồm replay/control, không phải814quan sát độc lập. Lượt hợp lệ được dùng lại; mọi lượt hỏng/dừng và lý do ở cost-and-runs.json. Các row/case/ô trung gian giữ đủ.','',
      'Lượt full002 bị dừng để giữ đĩa và tiếp bằng gzip chỉ cho file mới; không xóa/nén thay file cũ. Có giới hạn đo chi phí: RSS probe contracts null; full002 không có cost cuối, giữ clock/progress/checkpoint và nêu thiếu CPU/peak. Đọc timing đang song song không dùng so tốc độ method. Xem cost-and-runs.json và invocation/progress/cost từng lượt.','',
      'Trạng thái: người làm hoàn tất phần nối tiếp, chờ Claude phản biện chính thức. Minh quyết tiếp nhận giới hạn, yêu cầu nguồn tác giả hoặc lập nghiên cứu tiếp; chưa nghiệm thu/đóng câu hỏi. Prompt trung tính theo mẫu ở cuối LOG T-042.']
    (OUT/'bao-cao-bo-sung.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print('report,adjudication,mechanism,cost saved')


if __name__=='__main__':main()
