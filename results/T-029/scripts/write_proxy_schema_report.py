"""Write SPEC P1/P2 report from frozen JSON; never read raw telemetry."""
import hashlib
import json
import time
from collections import defaultdict
from pathlib import Path

from report_support import Report, esc
from resume_step7 import ROOT, OUT, log, read, sha, write, now

RUN = OUT / 'runs/report-proxy-schema-001'
SOURCE = 'results/T-029/nhan-proxy-va-schema.json'
AGG = 'results/T-029/runs/report-proxy-schema-001/aggregate.json'
VERIFY = 'results/T-029/runs/report-proxy-schema-001/check.json'


def build_aggregate(source):
    cases = source['P1']['cases']
    groups = defaultdict(list)
    for oid, row in cases.items():
        groups[row['cell']].append(oid)
    na_cases = [o for o, r in cases.items() if any(
        m['unavailable_count'] for v in r['by_Nv'].values()
        for m in v['minutes_after_injection'])]
    rows = [m for r in cases.values() for v in r['by_Nv'].values()
            for m in v['minutes_after_injection']]
    first_windows = next(iter(cases.values()))['by_Nv']['bocpd']['minutes_after_injection']
    full_windows = [m for m in first_windows if not m['partial_minute']]
    result = {
        'case_count': len(cases), 'Nv_count': len(next(iter(cases.values()))['by_Nv']),
        'minute_rows': len(rows), 'full_minutes_per_case_Nv': len(full_windows),
        'last_partial_seconds': next(iter(cases.values()))['by_Nv']['bocpd']['minutes_after_injection'][-1]['seconds'],
        'na_case_count': len(na_cases), 'na_case_ids': na_cases,
        'rows_with_NA': sum(r['unavailable_count'] > 0 for r in rows),
        'zero_eligible_rows': sum(r['eligible_count'] == 0 for r in rows),
        'minute_labels': [m['minute'] for m in full_windows], 'cell_summary': {}, 'P2': {},
    }
    for cell, ids in sorted(groups.items()):
        group = {}
        for nv in ('bocpd', 'nsigma_and_nsigma_control'):
            w = [m for o in ids for m in cases[o]['by_Nv'][nv]['minutes_after_injection'][:-1]]
            group[nv] = {
                'cases': len(ids), 'case_ids': ids,
                'full_minute_rows': len(w),
                'minimum_ratio': min(m['ratio'] for m in w if m['ratio'] is not None),
                'maximum_ratio': max(m['ratio'] for m in w if m['ratio'] is not None),
                'rows_with_NA': sum(m['unavailable_count'] > 0 for m in w),
                'zero_outside_rows': sum(m['outside_count'] == 0 for m in w),
            }
        result['cell_summary'][cell] = group
    for det, data in source['P2'].items():
        varying = [r['column'] for r in data['presence_by_column']
                   if any(c['present'] < c['n'] for c in r['by_root'].values())]
        all_present = [r['column'] for r in data['presence_by_column']
                       if all(c['present'] == c['n'] for c in r['by_root'].values())]
        result['P2'][det] = {
            'case_count': len(data['cases']),
            'union_count': len(data['presence_by_column']),
            'varying_count': len(varying), 'all_present_count': len(all_present),
            'varying_columns': varying, 'all_present_columns': all_present,
            'perfect_count': len(data['perfect_partition_columns']),
            'groups': {},
        }
        for field, groups in data['by_group'].items():
            result['P2'][det]['groups'][field] = {
                name: {'n': row['n'], 'column_min': min(row['column_counts']),
                       'column_max': max(row['column_counts']),
                       'd_min': min(row['d']), 'd_max': max(row['d'])}
                for name, row in groups.items()
            }
    partial = [c for c in result['P2']['bocpd']['varying_columns'] if c.endswith('latency-50')]
    result['partial_latency_columns'] = {'column_count': len(partial), 'columns': partial}
    absent_counts = [g['absent_column_counts'][col]
                     for det, data in source['P2'].items()
                     for groups in data['by_group'].values()
                     for g in groups.values()
                     for col in result['P2'][det]['all_present_columns']]
    assert set(absent_counts) == {0}
    result['always_present_absent_count'] = max(absent_counts)
    return result


def independent_check(source, aggregate):
    """Verify aggregation through stored case rows and T-025 column sets."""
    checks = 0
    def check(condition):
        nonlocal checks
        assert condition
        checks += 1
    p1 = source['P1']['cases']
    check(aggregate['case_count'] == len(p1))
    n_rows = n_na = n_zero = 0
    cases_na = set()
    for oid, case in p1.items():
        for nv, data in case['by_Nv'].items():
            full = [m for m in data['minutes_after_injection'] if not m['partial_minute']]
            last = [m for m in data['minutes_after_injection'] if m['partial_minute']]
            check(len(full) == aggregate['full_minutes_per_case_Nv'])
            check(len(last) == 1 and last[0]['seconds'] == aggregate['last_partial_seconds'])
            for minute in data['minutes_after_injection']:
                n_rows += 1
                n_na += minute['unavailable_count'] > 0
                n_zero += minute['eligible_count'] == 0
                if minute['unavailable_count']:
                    cases_na.add(oid)
                eligible = []
                outside = []
                for column in case['root_columns']:
                    low = data['q01'][column]
                    high = data['q99'][column]
                    median = minute['median_by_column'][column]
                    if low is not None and high is not None and median is not None:
                        eligible.append(column)
                        if median < low or median > high:
                            outside.append(column)
                check(set(eligible) == set(minute['eligible_columns']))
                check(set(outside) == set(minute['outside_columns']))
                check(minute['ratio'] == (len(outside) / len(eligible) if eligible else None))
    check(n_rows == aggregate['minute_rows'])
    check(n_na == aggregate['rows_with_NA'])
    check(n_zero == aggregate['zero_eligible_rows'])
    check(sorted(cases_na) == sorted(aggregate['na_case_ids']))
    for cell, cell_stats in aggregate['cell_summary'].items():
        ids = [o for o in p1 if p1[o]['cell'] == cell]
        for nv, stats in cell_stats.items():
            minutes = [m for o in ids for m in p1[o]['by_Nv'][nv]['minutes_after_injection']
                       if not m['partial_minute']]
            check(stats['cases'] == len(ids))
            check(stats['full_minute_rows'] == len(minutes))
            check(stats['minimum_ratio'] == sorted(m['ratio'] for m in minutes)[0])
            check(stats['maximum_ratio'] == sorted(m['ratio'] for m in minutes)[-1])
            check(stats['rows_with_NA'] == sum(bool(m['unavailable_count']) for m in minutes))
            check(stats['zero_outside_rows'] == sum(m['outside_count'] == 0 for m in minutes))
    alarms = read(ROOT / 'results/T-025/bao-dong.json')['bo_phat_hien']
    for det, schema in source['P2'].items():
        columns = {o: set(alarms[det][o]['detector_columns']) for o in schema['cases']}
        union = set().union(*columns.values())
        varying = sorted(c for c in union if any(c not in cols for cols in columns.values()))
        all_present = sorted(c for c in union if all(c in cols for cols in columns.values()))
        agg = aggregate['P2'][det]
        check(agg['union_count'] == len(union))
        check(agg['varying_columns'] == varying)
        check(agg['all_present_columns'] == all_present)
        perfect = []
        for incidence in schema['presence_by_column']:
            col = incidence['column']
            statuses = []
            for root, counts in incidence['by_root'].items():
                ids = [o for o in schema['cases'] if schema['cases'][o]['root'] == root]
                presence = [col in columns[o] for o in ids]
                check(counts == {'present': sum(presence), 'n': len(ids)})
                statuses.append('all' if all(presence) else 'none' if not any(presence) else 'mixed')
            is_perfect = 'mixed' not in statuses and len(set(statuses)) > 1
            check(is_perfect == incidence['perfect_binary_root_partition'])
            if is_perfect:
                perfect.append(col)
        check(agg['perfect_count'] == len(perfect))
        for field, groups in agg['groups'].items():
            for name, stats in groups.items():
                ids = [o for o, row in schema['cases'].items() if row[field] == name]
                vals = [schema['cases'][o] for o in ids]
                check(stats['n'] == len(vals))
                check(stats['column_min'] == min(len(columns[o]) for o in ids))
                check(stats['column_max'] == max(len(columns[o]) for o in ids))
                check(stats['d_min'] == sorted(row['d'] for row in vals)[0])
                check(stats['d_max'] == sorted(row['d'] for row in vals)[-1])
                for col, absent in schema['by_group'][field][name]['absent_column_counts'].items():
                    check(absent == sum(col not in columns[o] for o in ids))
    primary = source['P2']['bocpd']['by_group']
    ns = source['P2']['nsigma']['by_group']
    control = source['P2']['nsigma_doi_chung']['by_group']
    for field, groups in primary.items():
        for group, row in groups.items():
            for col, n in row['absent_column_counts'].items():
                check(ns[field][group]['absent_column_counts'][col] == n)
                check(control[field][group]['absent_column_counts'][col] == n)
    latency = [x['column'] for x in source['P2']['bocpd']['presence_by_column']
               if x['column'].endswith('latency-50')
               and any(v['present'] < v['n'] for v in x['by_root'].values())]
    check(latency == aggregate['partial_latency_columns']['columns'])
    check(len(latency) == aggregate['partial_latency_columns']['column_count'])
    for det, data in source['P2'].items():
        for col in aggregate['P2'][det]['all_present_columns']:
            check(all(row['absent_column_counts'][col] == aggregate['always_present_absent_count']
                      for groups in data['by_group'].values() for row in groups.values()))
    return {'status': 'PASS', 'checks': checks, 'raw_read': False,
            'source_hashes': {SOURCE: sha(ROOT / SOURCE),
                              'results/T-025/bao-dong.json': sha(ROOT / 'results/T-025/bao-dong.json')},
            'method': 'Independent stored-q/median eligibility reconstruction; group and incidence counts from T-025 column sets; summary ranges from saved per-case rows.'}


def display_label(name):
    return name.replace('ts-', '').replace('-service', '').replace('|', ' / ')


def main():
    log('Lệnh có ghi: T-014-main Python -B -W ignore scripts/write_proxy_schema_report.py; chỉ đọc JSON đóng băng, ghi report-proxy-schema-001 và nhan-proxy-va-schema.md. Không raw/SSH/rerun.')
    assert not RUN.exists(), 'Giữ lượt cũ; không ghi đè report run.'
    RUN.mkdir(parents=True)
    started = time.perf_counter()
    write(RUN/'invocation.json', {'started_at': now(),
          'command': 'T-014-main Python -B -W ignore results/T-029/scripts/write_proxy_schema_report.py',
          'script_sha256': sha(Path(__file__)), 'source_sha256': sha(ROOT/SOURCE),
          'scope': ['nhan-proxy-va-schema.md', 'runs/report-proxy-schema-001/']})
    source = read(ROOT / SOURCE)
    aggregate = build_aggregate(source)
    check = independent_check(source, aggregate)
    write(RUN / 'aggregate.json', aggregate)
    write(RUN / 'check.json', check)
    r = Report('nhan-proxy-va-schema.md', RUN)
    n = r.num
    integer = lambda path, ptr: n(path, ptr, 'd')
    a = lambda ptr: integer(AGG, ptr)
    s = lambda ptr: integer(SOURCE, ptr)
    text = []
    add = text.append
    add('# Nhãn proxy và schema — C5, HP-12 và HP-13\n')
    add('Thời lượng lỗi D vẫn **OPEN**. Nguồn tác giả đã khảo sát mô tả mốc tiêm và hai đoạn trước/sau; chưa thấy D hoặc mốc kết thúc độc lập. T-029 giữ nguyên số P/R/F1 của T-025. Tỉ lệ metric dưới đây chỉ mô tả telemetry, không xác định lúc lỗi thật bắt đầu hay kết thúc.\n')
    add('Schema (cấu trúc tập cột) thay đổi theo ca và liên hệ với một số nhóm nhãn. Có ' +
        a('/P2/bocpd/perfect_count') + ' cột BOCPD, ' + a('/P2/nsigma/perfect_count') +
        ' cột N-Sigma chính và ' + a('/P2/nsigma_doi_chung/perfect_count') +
        ' cột N-Sigma đối chứng tách hoàn toàn các nhóm root theo điều kiện đã khóa. Kết quả này không phủ nhận thông tin nhãn một phần hoặc thông tin trong tổ hợp schema. Không đưa dấu vắng vào phương pháp.\n')
    add('Mức bằng chứng: **HP-12** là khảo sát nguồn và liên hệ metric với nhãn proxy; chưa có nhãn thời lượng độc lập. **HP-13** là số đếm chính xác và liên hệ với nhãn; chưa tách nguyên nhân tạo schema, chưa có can thiệp vào schema. Cả hai không chứng minh quan hệ nhân quả hoặc “lan”.\n')
    add('## P1 — Nguồn thời lượng và quy tắc đo\n')
    add('Nguồn JSON: `nhan-proxy-va-schema.json#/P1/source_duration`, `runs/proxy-002/manifest.json` và `runs/proxy-002/verification.json`.\n')
    add('| Nguồn tác giả đã khảo sát | Thông tin đọc trực tiếp | Kết luận được phép |\n|---|---|---|')
    add('| [Bài RCAEval, phần Telemetry Data Collection Process](https://arxiv.org/html/2412.17015v2#S3.SS3) | Cho hệ thống chạy bình thường, rồi tiêm lỗi và thu telemetry bất thường. | Đoạn này không nêu thời lượng sau tiêm. Không suy D từ thời lượng thu hoặc từ file. |')
    add('| [README repository RCAEval](https://github.com/phamquiluan/RCAEval/blob/259ea4167160256a74ad30004aa3d96a998c846e/README.md) | `inject_time.txt` chứa mốc tiêm; phần cấu trúc file không nêu end time. | Xác nhận mốc tiêm, chưa xác nhận mốc hết lỗi. |')
    add('| [README dataset RCAEval](https://huggingface.co/datasets/phamquiluan/RCAEval/blob/afeacb11bcc94dadfd1c8f483ee4377b2b8b614e/README.md) | Chia normal trước mốc và faulty sau mốc; dữ liệu thiếu được giữ null khi lưu. | Đây là quy ước proxy. Null không là quan sát bình thường hoặc bằng chứng hết lỗi. |')
    add('| Khảo sát tree repository và primary search đã lưu trong JSON nguồn | Chưa thấy script tiêm lỗi hoặc thông tin D trong phạm vi đã khảo sát. | “Chưa thấy trong nguồn đã khảo sát”; không khẳng định mọi nguồn đều thiếu. |\n')
    first = next(iter(source['P1']['cases']))
    base = '/P1/cases/' + first + '/by_Nv/'
    add('Dùng mọi cột của dịch vụ root, không chọn theo loại lỗi. Mỗi cột so median của đoạn sau mốc với khoảng q01–q99 của Nv. Hai Nv là [' +
        s(base+'bocpd/Nv_half_open/0') + ', ' + s(base+'bocpd/Nv_half_open/1') + ') cho BOCPD và [' +
        s(base+'nsigma_and_nsigma_control/Nv_half_open/0') + ', ' + s(base+'nsigma_and_nsigma_control/Nv_half_open/1') +
        ') cho cả hai N-Sigma. Raw metrics được dùng trực tiếp; quantile/median bỏ NaN khi còn quan sát, không điền trước cho P1.\n')
    add('Cột thiếu q01/q99 ở Nv hoặc thiếu median của phút ghi N/A. Tỉ lệ = số cột ngoài khoảng / số cột đủ dữ liệu. Báo cạnh đó đủ/tổng và tên cột thiếu; không có cột đủ thì tỉ lệ N/A. Có ' +
        a('/case_count') + ' ca, ' + a('/Nv_count') + ' Nv và ' + a('/minute_rows') +
        ' dòng Nv–đoạn. Mỗi ca/Nv có ' + a('/full_minutes_per_case_Nv') +
        ' phút đầy đủ, sau đó một đoạn cuối chỉ ' + a('/last_partial_seconds') +
        ' giây; đoạn cuối không được coi là phút đầy đủ. ' + a('/na_case_count') +
        ' ca có cột N/A, trên ' + a('/rows_with_NA') + '/' + a('/minute_rows') +
        ' dòng; ' + a('/zero_eligible_rows') + ' dòng không còn cột đủ.\n')
    add('### Coverage và cột thiếu theo ca\n')
    add('Nguồn: `nhan-proxy-va-schema.json#/P1/cases/<mã>/by_Nv/<Nv>/minutes_after_injection`; đủ/tổng áp ở cả hai Nv và mọi đoạn của ca vì coverage không đổi trong các JSON đã lưu.\n')
    add('| Ca | Ô | Đủ/tổng | Cột thiếu | Lý do |\n|---|---|---|---|---|')
    for oid, row in source['P1']['cases'].items():
        ptr = '/P1/cases/' + oid
        windows = [m for v in row['by_Nv'].values() for m in v['minutes_after_injection']]
        assert len({m['eligible_count'] for m in windows}) == 1
        assert len({tuple(m['unavailable_columns']) for m in windows}) == 1
        m = windows[0]
        missing = ', '.join('`'+c+'`' for c in m['unavailable_columns']) or 'Không'
        reasons = ', '.join(sorted({why for v in m['unavailable_reasons_by_column'].values() for why in v})) or 'Đủ dữ liệu'
        add('| `'+oid+'` | '+display_label(row['cell'])+' | '+s(ptr+'/by_Nv/bocpd/minutes_after_injection/0/eligible_count')+
            '/'+s(ptr+'/total_root_columns')+' | '+missing+' | '+reasons+' |')
    add('\nN/A của các cột được liệt kê đến từ Nv thiếu quan sát. Median sau mốc có thể đã xuất hiện, nhưng thiếu khoảng tham chiếu vẫn làm phép so N/A. Không chuyển N/A thành False hoặc giảm tử số trên mẫu số tổng.\n')
    add('### Tỉ lệ từng phút, đầy đủ từng ca và hai Nv\n')
    add('Mỗi ô là **ngoài/đủ**, chính là tử và mẫu của `ratio`; đọc coverage ở bảng trên. Bảng giữ mọi đoạn và mọi ca để tránh chọn ca theo kết quả. Nguồn: `nhan-proxy-va-schema.json#/P1/cases/<mã>/by_Nv/<Nv>/minutes_after_injection/<chỉ số>` → `outside_count`, `eligible_count`, `ratio`.\n')
    labels = ['Phút '+a('/minute_labels/'+str(i)) for i in range(12)]
    add('| Ca / Nv | '+' | '.join(labels)+' | Cuối '+a('/last_partial_seconds')+' giây |')
    add('|---|'+'---|'*13)
    for oid, row in source['P1']['cases'].items():
        for nv, data in row['by_Nv'].items():
            cells = []
            for i, m in enumerate(data['minutes_after_injection']):
                ptr = '/P1/cases/'+oid+'/by_Nv/'+nv+'/minutes_after_injection/'+str(i)
                cells.append(s(ptr+'/outside_count')+'/'+s(ptr+'/eligible_count'))
            add('| `'+oid+'` / '+('BOCPD' if nv=='bocpd' else 'N-Sigma')+' | '+' | '.join(cells)+' |')
    add('\n### Theo ô trước khi diễn giải\n')
    add('Phạm vi tỉ lệ lấy trên các phút đầy đủ của mọi ca trong ô; không gồm đoạn cuối ngắn. Đây là phạm vi mô tả, không là ngưỡng chấm lại. Nguồn: `runs/report-proxy-schema-001/aggregate.json#/cell_summary`, kiểm độc lập từ P1 đã lưu.\n')
    add('| Ô | Nv | Ca | Phút đủ | Min–max tỉ lệ | Phút có N/A | Phút không cột ngoài |\n|---|---|---|---|---|---|---|')
    for cell, data in aggregate['cell_summary'].items():
        for nv in data:
            ptr='/cell_summary/'+esc(cell)+'/'+nv
            add('| '+display_label(cell)+' | '+('BOCPD' if nv=='bocpd' else 'N-Sigma')+' | '+a(ptr+'/cases')+' | '+a(ptr+'/full_minute_rows')+' | '+
                n(AGG,ptr+'/minimum_ratio')+'–'+n(AGG,ptr+'/maximum_ratio')+' | '+a(ptr+'/rows_with_NA')+' | '+a(ptr+'/zero_outside_rows')+' |')
    add('\nTỉ lệ thay đổi khi chọn Nv khác, nhất là trong một số ca order/travel. Nó phụ thuộc phân vị nền, số cột đủ và cấu tạo metric. Tỉ lệ thấp không chứng minh lỗi đã hết; tỉ lệ cao không chứng minh lỗi còn kéo dài. Một sự cố kéo dài có thể ít đổi metric đang đo, còn tải hoặc drift có thể làm metric nằm ngoài khoảng khi sự cố đã hết.\n')
    add('### Giá trị tham chiếu q01–q99 theo ca\n')
    add('Nguồn: `nhan-proxy-va-schema.json#/P1/cases/<mã>/by_Nv/<Nv>/q01` và `/q99`. q01–q99 là các quantile mô tả theo SPEC; không là ngưỡng mới. Bảng ghi cả hai Nv và giữ N/A để truy vết tử/mẫu số ở trên.\n')
    add('| Ca | Cột root | BOCPD q01–q99 | N-Sigma q01–q99 |\n|---|---|---|---|')
    for oid, row in source['P1']['cases'].items():
        for col in row['root_columns']:
            pieces=[]
            for nv in row['by_Nv']:
                ptr='/P1/cases/'+oid+'/by_Nv/'+nv
                pieces.append(n(SOURCE,ptr+'/q01/'+esc(col),'.12g')+'–'+n(SOURCE,ptr+'/q99/'+esc(col),'.12g'))
            add('| `'+oid+'` | `'+col+'` | '+' | '.join(pieces)+' |')
    add('\n**Trả lời C5 về proxy:** dữ liệu và tác giả chưa xác nhận độc lập giả định “lỗi kéo dài tới cuối file”. Theo thiết kế khóa, D vẫn OPEN và không chấm lại P/R/F1. Số gốc chỉ là chất lượng trong quy ước injection-regime (chế độ nhãn dựa trên mốc tiêm), chưa là chất lượng trên sự kiện thật có onset và kết thúc độc lập.\n')
    add('## P2 — Cột vắng và số chiều\n')
    add('`column_count` là số cột detector nhận; d là số chiều sau tiền xử lý. BOCPD bỏ cột hằng nên hai số khác nhau; N-Sigma giữ tập cột của mình. Cột tồn tại nhưng toàn NaN ở Nv khác với cột vắng khỏi schema. P1 đo trường hợp trước; P2 đo trường hợp sau.\n')
    add('Nguồn: `nhan-proxy-va-schema.json#/P2/<bộ>/cases`, `/by_group`, `/presence_by_column`. `audit_cot` và `detector_columns` của T-025 đã đối chiếu độc lập.\n')
    add('| Bộ | Ca | Union cột | Cột biến thiên | Cột luôn có | Cột tách hoàn toàn root |\n|---|---|---|---|---|---|')
    for det in source['P2']:
        ptr='/P2/'+det
        add('| '+det+' | '+' | '.join(a(ptr+'/'+k) for k in ('case_count','union_count','varying_count','all_present_count','perfect_count'))+' |')
    add('\nĐiều kiện tách hoàn toàn: trong mỗi root, một cột phải có ở mọi ca hoặc vắng ở mọi ca; đồng thời trạng thái phải khác giữa ít nhất hai root. Một dấu có/vắng nhị phân chỉ tách nhóm root, không nhất thiết xác định từng root. `perfect_partition_columns` rỗng ở mọi bộ.\n')
    add('### Số cột và d theo ca\n')
    add('Nguồn: `nhan-proxy-va-schema.json#/P2/<bộ>/cases/<mã>`. Mọi ca được giữ.\n')
    add('| Ca | Ô | BOCPD cột/d | N-Sigma cột/d | Đối chứng cột/d |\n|---|---|---|---|---|')
    for oid,row in source['P1']['cases'].items():
        vals=[]
        for det in source['P2']:
            ptr='/P2/'+det+'/cases/'+oid
            vals.append(s(ptr+'/column_count')+'/'+s(ptr+'/d'))
        add('| `'+oid+'` | '+display_label(row['cell'])+' | '+' | '.join(vals)+' |')
    add('\n### Số cột và d theo root, loại lỗi, ô\n')
    add('Nguồn: `runs/report-proxy-schema-001/aggregate.json#/P2/<bộ>/groups`; min–max từ từng ca, không suy cơ chế từ trung bình nhóm. Các d cụ thể vẫn ở bảng theo ca.\n')
    for field,title in (('root','Root'),('fault','Loại lỗi'),('cell','Ô')):
        add('#### '+title+'\n')
        add('| Nhóm | Ca | BOCPD cột / d | N-Sigma cột / d | Đối chứng cột / d |\n|---|---|---|---|---|')
        for group in source['P2']['bocpd']['by_group'][field]:
            vals=[]
            for det in source['P2']:
                ptr='/P2/'+det+'/groups/'+field+'/'+esc(group)
                vals.append(a(ptr+'/column_min')+'–'+a(ptr+'/column_max')+' / '+a(ptr+'/d_min')+'–'+a(ptr+'/d_max'))
            add('| '+display_label(group)+' | '+a('/P2/bocpd/groups/'+field+'/'+esc(group)+'/n')+' | '+' | '.join(vals)+' |')
        add('')
    add('### Bảng chéo cột vắng\n')
    add('Mỗi ô là **ca vắng/tổng ca trong nhóm**. Các cột biến thiên chung có cùng số vắng ở cả ba bộ; bảng hiển thị một lần và ghi phạm vi áp dụng. Cột thêm của đối chứng ghi riêng. Cột luôn có không được bỏ khỏi kiểm: danh sách đầy đủ ở `aggregate.json#/P2/<bộ>/all_present_columns`; mọi số vắng của chúng bằng ' +
        n(AGG,'/always_present_absent_count','d') + ' theo bảng nguồn.\n')
    primary=set(aggregate['P2']['bocpd']['varying_columns'])
    varying=aggregate['P2']['nsigma_doi_chung']['varying_columns']
    control=source['P2']['nsigma_doi_chung']
    for field,title in (('root','Root'),('fault','Loại lỗi'),('cell','Ô')):
        add('#### Cột vắng theo '+title.lower()+'\n')
        add('Nguồn: `nhan-proxy-va-schema.json#/P2/nsigma_doi_chung/by_group/'+field+'`; cột chung đã kiểm trùng `/P2/bocpd/by_group` và `/P2/nsigma/by_group`.\n')
        groups=list(control['by_group'][field])
        add('| Cột | Tập | '+' | '.join(display_label(g) for g in groups)+' |')
        add('|---|---|'+'---|'*len(groups))
        for col in varying:
            vals=[]
            for group in groups:
                ptr='/P2/nsigma_doi_chung/by_group/'+field+'/'+esc(group)
                vals.append(s(ptr+'/absent_column_counts/'+esc(col))+'/'+s(ptr+'/n'))
            add('| `'+col+'` | '+('Cả ba' if col in primary else 'Đối chứng')+' | '+' | '.join(vals)+' |')
        add('')
    add('### Liên hệ một phần, chưa phải kênh tách hoàn toàn\n')
    partial=aggregate['partial_latency_columns']['columns']
    add('Các cột latency sau có mặt ít hơn trong nhóm order: '+', '.join('`'+c+'`' for c in partial)+'. Tổng cộng '+
        a('/partial_latency_columns/column_count')+' cột, mỗi cột vắng ở '+
        s('/P2/bocpd/by_group/root/ts-order-service/absent_column_counts/'+esc(partial[0]))+'/'+
        s('/P2/bocpd/by_group/root/ts-order-service/n')+' ca order và không vắng ở các root khác trong mẫu. Trong từng ô order/disk và order/loss, mỗi cột vắng ở '+
        s('/P2/bocpd/by_group/cell/'+esc('ts-order-service|disk')+'/absent_column_counts/'+esc(partial[0]))+'/'+
        s('/P2/bocpd/by_group/cell/'+esc('ts-order-service|disk')+'/n')+' ca. Đây là liên hệ một phía trong dev: dấu vắng gợi ý nhóm order nhưng dấu có không xác định root. Nó chưa đạt định nghĩa tách hoàn toàn đã khóa, vì ca order còn lẫn có/vắng.\n')
    add('Thiết kế dev không giao chéo đầy đủ root và loại lỗi: auth/train chỉ có cpu, delay; order/travel chỉ có disk, loss; route chỉ có mem, socket. Vì vậy, liên hệ theo root hoặc theo loại lỗi có thể do ô được chọn, chế độ tải, cấu hình thu hoặc hành vi metric theo sự cố. Không quy riêng biến đổi số chiều cho root, loại lỗi hoặc cơ chế detector. Không suy nguyên nhân thiếu cột từ các bảng chéo.\n')
    add('**Trả lời C5 về schema:** số cột và sự vắng thay đổi giữa ca; đã báo theo root/loại lỗi/ô và ca. Chưa có cột đơn tách hoàn toàn root theo quy tắc SPEC, nhưng tồn tại liên hệ một phần. Việc kiểm này không chứng minh schema an toàn với mọi cách dùng; task giữ dấu vắng ngoài phương pháp và không khảo sát classifier dựa trên schema.\n')
    add('**C6:** README dataset mô tả null khi metric không được quan sát; đó là giải thích định dạng lưu. Chưa thấy tác giả nêu liên hệ schema–root cụ thể hoặc xác nhận thời lượng lỗi kéo dài tới cuối file trong nguồn đã khảo sát. Tài liệu nền `docs/knowledge/K2-du-lieu.md` cũng giữ giới hạn injection target/onset độc lập; đây là ghi chú của dự án, không thay lời tác giả.\n')
    add('## Kiểm số và giới hạn sử dụng\n')
    add('Kiểm độc lập báo cáo chạy trên JSON đã lưu: ' + integer(VERIFY,'/checks') +
        ' phép đạt; nguồn và hash ở `runs/report-proxy-schema-001/check.json`. Đối chiếu quy tắc N/A từ q01/q99 và median, bảng chéo từ tập cột T-025, và phạm vi d từ dòng theo ca. Không chạy lại P1/P2 hoặc đọc raw. Binding V8 ghi từng số và con trỏ JSON.\n')
    add('HP-12 và HP-13 chỉ áp cho RE2-TT dev trong giao thức đang dùng. D, onset thật, nền sạch, clock tuyệt đối và mức khái quát sang dữ liệu khác còn OPEN. Không thay số T-025, không đổi ngưỡng, không đưa đề xuất thiết kế P5/P6 vào báo cáo này.\n')
    r.save('\n'.join(text))
    write(RUN/'manifest.json', {'status':'PASS', 'completed_at':now(),
          'seconds':time.perf_counter()-started, 'checks':check['checks'],
          'bindings':len(r.bindings), 'script_sha256':sha(Path(__file__)),
          'outputs': {p.relative_to(ROOT).as_posix():sha(p)
                      for p in [OUT/'nhan-proxy-va-schema.md', RUN/'aggregate.json',
                                RUN/'check.json', RUN/'nhan-proxy-va-schema.md.bindings.json']}})
    log('Hỗ trợ P1/P2: báo cáo nhan-proxy-va-schema.md và binding đã ghi; kiểm độc lập PASS '+str(check['checks'])+' phép, không raw hoặc rerun. Tiếp theo chỉ kiểm lại aggregate mới/binding và đọc toàn MD trước báo root.')
    print(json.dumps({'status':'PASS','checks':check['checks'],'bindings':len(r.bindings)}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        log('DỪNG báo cáo P1/P2: '+type(error).__name__+': '+str(error)+'. Giữ lượt; báo root trước sửa/chạy tiếp.')
        if RUN.exists() and not (RUN/'manifest.json').exists():
            write(RUN/'failure.json',{'status':'STOP','time':now(),
                  'error':type(error).__name__+': '+str(error),'script_sha256':sha(Path(__file__))})
        raise
