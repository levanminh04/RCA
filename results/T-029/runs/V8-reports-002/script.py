"""V8 độc lập: từng scalar, quét số không gắn nguồn, kiểm tổng hợp/miền."""
import hashlib
import json
import re
import statistics
import time
from collections import Counter
from pathlib import Path
from datetime import datetime, timezone, timedelta

ROOT=Path(__file__).resolve().parents[3]; OUT=ROOT/'results/T-029'; LOG=ROOT/'tasks/T-029-p4-han-che-phat-hien/LOG.md'
def now():return datetime.now(timezone(timedelta(hours=7))).isoformat()
def read(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def log(s):
    with LOG.open('a',encoding='utf-8') as f:f.write('\n- '+now()+' — V8: '+s+'\n')
def resolve(doc,ptr):
    for token in ptr.lstrip('/').split('/') if ptr else []:
        token=token.replace('~1','/').replace('~0','~')
        doc=doc[int(token)] if isinstance(doc,list) else doc[token]
    return doc
def render(v,s):
    if v is None:return 'N/A'
    if isinstance(v,bool):return 'Đúng' if v else 'Sai'
    return str(v) if s=='str' else format(v,s)

def main():
    log('Lệnh có ghi: T-014-main Python -B -W ignore verify_reports.py; V8 kiểm riêng các báo cáo cuối theo từng marker/JSON, quét mọi số không marker; kiểm độc lập số tổng hợp main và V7. Không gọi lại detector/ranker hoặc ghi đè lượt cũ.')
    st=time.perf_counter(); i=1
    while (OUT/f'runs/V8-reports-{i:03d}').exists():i+=1
    run=OUT/f'runs/V8-reports-{i:03d}';run.mkdir()
    failures=[]; counts=Counter(); cache={}; per_report={}
    def ck(name,ok,detail=None):
        counts[name]+=1
        if not ok:failures.append({'check':name,'detail':detail})
    theo=read(OUT/'theo-ca.json'); ns=read(OUT/'n-sigma-cot.json'); v7=read(OUT/'runs/step5-001/V7.json'); summary=read(OUT/'runs/report-main-001/summary.json')
    rows=theo['rows']; flags=set(rows[0]['flags_flat']); identifiers=set(flags)|{'Hit@1','Hit@5','hit@1','hit@5'}
    interval_keys=set(next(iter(ns['cases'].values()))['nsigma']['history'])
    # Tên metric được truy về chính detector_columns, không loại mọi hậu tố số.
    metric_source='results/T-025/bao-dong.json'
    metric_doc=read(ROOT/metric_source); metric_refs={}
    for det,cases in metric_doc['bo_phat_hien'].items():
        for oid,case in cases.items():
            for j,name in enumerate(case['detector_columns']):
                metric_refs.setdefault(name,{'path':metric_source,'pointer':'/bo_phat_hien/'+det+'/'+oid+'/detector_columns/'+str(j)})
    decisions_path='docs/DECISIONS.md'; decisions_text=(ROOT/decisions_path).read_text(encoding='utf-8')
    decision_codes=set(re.findall(r'^\| (Q-\d+) \|',decisions_text,re.M))
    named_occurrences=[]
    bindings=[p for p in OUT.rglob('*.md.bindings.json')]
    ck('binding_file_count',len(bindings)==5)

    expected={'ban-do-han-che-phat-hien.md','doc-tay.md','dinh-vi.md','nhan-proxy-va-schema.md','a-so-b.md'}
    ck('report_set',{read(p)['report'].split('/')[-1] for p in bindings}==expected)
    for p in bindings:
        d=read(p); report=ROOT/d['report']; text=report.read_text(encoding='utf-8')
        matches=list(re.finditer(r'<!--v8:(\d+)-->(.*?)<!--/v8-->',text,re.S)); ids=[m.group(1) for m in matches]; by={x['id']:x for x in d['bindings']}
        ck('unique_markers',len(ids)==len(set(ids))==len(by),report.name)
        ck('marker_ids',set(ids)==set(by),report.name)
        for path,h in d['source_hashes'].items():ck('scalar_source_hash',sha(ROOT/path)==h,path)
        for m in matches:
            b=by.get(m.group(1))
            if not b:continue
            if b['path'] not in cache:cache[b['path']]=read(ROOT/b['path'])
            val=resolve(cache[b['path']],b['pointer']); expected_text=render(val,b['format'])
            ck('scalar_value',m.group(2)==expected_text==b['rendered'],{'report':report.name,'id':b['id'],'pointer':b['pointer'],'actual':m.group(2),'expected':expected_text})
        # Số trong tên mã, hậu tố metric, nguồn và định nghĩa cấu hình không là số đo.
        # Chỉ loại chúng sau khi nhận diện rõ; không bỏ mọi inline-code hoặc mọi digit.
        scrub=re.sub(r'<!--v8:\d+-->.*?<!--/v8-->',' ',text,flags=re.S)
        scrub=re.sub(r'\]\([^\n)]*\)','](SOURCE)',scrub)
        reference_spans=re.findall(r'`([^`]+)`',scrub)
        for ref in reference_spans:
            if re.search(r'(?:\.json|\.md|\.py|\.parquet|results/|runs/|#/)',ref):scrub=scrub.replace('`'+ref+'`',' SOURCE ')
        def metric_name(m):
            name=m.group(0);ref=metric_refs.get(name)
            ck('metric_identifier_source',ref is not None,{'report':report.name,'name':name})
            if ref is None:return name
            ck('metric_identifier_value',resolve(metric_doc,ref['pointer'])==name,name)
            named_occurrences.append({'report':report.name,'name':name,**ref})
            return ' METRIC_NAME '
        scrub=re.sub(r'(?<![\w-])ts-[A-Za-z0-9_-]+_(?:latency|error)-\d+(?![\w-])',metric_name,scrub)
        def decision_code(m):
            code=m.group(0);ok=code in decision_codes
            ck('decision_identifier_source',ok,code)
            if ok:named_occurrences.append({'report':report.name,'name':code,'path':decisions_path,'locator':'table row '+code})
            return ' DECISION_CODE ' if ok else code
        scrub=re.sub(r'\bQ-\d+\b',decision_code,scrub)
        def run_code(m):
            name=m.group(0);path=OUT/'runs'/name;ok=path.is_dir() and any(path.iterdir())
            ck('run_identifier_source',ok,name)
            if ok:named_occurrences.append({'report':report.name,'name':name,'path':path.relative_to(ROOT).as_posix(),'locator':'preserved run directory'})
            return ' RUN_CODE ' if ok else name
        scrub=re.sub(r'\bmanual-evidence-\d+\b',run_code,scrub)
        for identifier in sorted(identifiers,key=len,reverse=True):scrub=scrub.replace(identifier,' FLAG ')
        for interval in interval_keys:
            ck('interval_key',all(interval in f['history'] for ds in ns['cases'].values() for f in ds.values()),interval)
            scrub=scrub.replace(interval,' HISTORY_INTERVAL ')
        # Các caption N2 mức x·p0 phải khớp key độ nhạy có thật trong JSON.
        for level in ('5','10','20'):
            ck('caption_N2_key',all('N2/'+level in r['flags_flat'] for r in rows),level)
            scrub=re.sub(r'(?<!\d)'+level+r'\s*[·×]\s*p0',' N2_LEVEL ',scrub)
        scrub=re.sub(r'dev-[0-9a-f]{10}\b',' CASE ',scrub)
        scrub=re.sub(r'\bT-\d{3}\b|\bHP-\d+\b',' ID ',scrub)
        scrub=re.sub(r'§\s*\d+(?:\.\d+)*(?:[–-]\s*\d+(?:\.\d+)*)?',' SOURCE_SECTION ',scrub)
        scrub=re.sub(r'\b(?:N|B|C|I|P|V|G|Q)\d+(?:[–-](?:N|B|C|I|P|V|G|Q)?\d+)?\b',' CODE ',scrub)
        # Cấu hình w/k và quantile là tên đã có ở các JSON nguồn.
        scrub=re.sub(r'\b(?:w(?:15|30|60)|k(?:2|3|5)|q(?:01|99)|p0)\b',' CONFIG ',scrub)
        remnants=[]
        for match in re.finditer(r'(?<![\w])[-+]?\d+(?:\.\d+)*(?:[eE][+-]?\d+)?(?![\w])',scrub):
            remnants.append(scrub[max(0,match.start()-60):match.end()+60].replace('\n',' '))
        ck('unbound_numeric_literals',not remnants,{'report':report.name,'contexts':remnants[:80],'count':len(remnants)})
        # Số cột bảng, có xét dấu | đã escape và inline code (nguồn không trong cell).
        table_cols=None; malformed=[]; blocks=[]; block=[]
        for line_no,line in enumerate(text.splitlines(),1):
            if line.startswith('|'):
                columns=len(re.split(r'(?<!\\)\|',line))-2
                if table_cols is None:table_cols=columns
                elif columns!=table_cols:malformed.append(line_no)
                block.append((line_no,line))
            else:
                table_cols=None
                if block:blocks.append(block);block=[]
        if block:blocks.append(block)
        # Bắt cả hàng w bị tách khỏi header bởi ghi chú, lỗi width đơn thuần bỏ sót.
        for block in blocks:
            if len(block)<2 or not re.fullmatch(r'\|(?:\s*:?-+:?\s*\|)+',block[1][1]):malformed.append(block[0][0])
        ck('markdown_table_shape',not malformed,{'report':report.name,'lines':sorted(set(malformed))})
        per_report[report.name]={'scalar_count':len(matches),'unbound_numeric_count':len(remnants),'sha256':sha(report),'binding_sha256':sha(p)}
    # Tính lại thống kê main bằng biểu thức tối giản, không import script viết báo cáo.
    for det in ('bocpd','nsigma','nsigma_doi_chung'):
        chosen=[r for r in rows if r['detector']==det]; delay=sorted(r['delay_seconds'] for r in chosen if r['delay_seconds'] is not None)
        q=summary['delay'][det]
        ck('main_delay',q=={'n':len(delay),'minimum':delay[0],'median':(delay[14]+delay[15])/2,'maximum':delay[-1],'zero':delay.count(0)},det)
        for cell,q in summary['D0'][det].items():ck('main_D0',q=={'n':sum(x['cell']==cell for x in chosen),'count':sum(x['cell']==cell and x['D0'] for x in chosen)},det+'/'+cell)
        for flag,q in summary['sensitivity_changes'][det].items():
            expected_changes=[{'opaque_id':x['opaque_id'],'cell':x['cell'],'base':x['flags_flat'][q['base']],'variant':x['flags_flat'][flag]} for x in chosen if x['flags_flat'][q['base']]!=x['flags_flat'][flag]]
            ck('main_sensitivity',q['changes']==expected_changes and q['changed_count']==len(expected_changes) and q['n']==len(chosen),det+'/'+flag)
        for code,dets in summary['HP_cells'].items():
            if det not in dets:continue
            flag={'HP-1':'N1/2.0','HP-2':'N2/10','HP-3':'N3/10','HP-4':'N4','HP-5':'B1','HP-6':'B2/5','HP-7':'B3/5','HP-8':'B4/w30/k3'}[code]
            for cell,q in dets[det].items():
                vs=[x['flags_flat'][flag] for x in chosen if x['cell']==cell]
                ck('main_HP',q=={'true':vs.count(True),'valid':len(vs)-vs.count(None),'total':len(vs),'NA':vs.count(None)},code+'/'+det+'/'+cell)
        if det=='bocpd':continue
        for group,q in summary['NS_descriptive'][det].items():
            fs=[ns['cases'][x['opaque_id']][det] for x in chosen if group=='all' or x['cell']==group]
            ck('main_NS_group',q['n']==len(fs) and q['r_obs_min']==min(f['r_obs'] for f in fs) and q['r_obs_max']==max(f['r_obs'] for f in fs),det+'/'+group)
            for kind,a in q['types'].items():
                den=sum(f['N5_types'][kind]['mau_so_cot_giay'] for f in fs);num=sum(f['N5_types'][kind]['so_bao_cot_giay'] for f in fs)
                ck('main_N5',a=={'alarm_column_seconds':num,'column_seconds':den,'rate':num/den if den else None},det+'/'+group+'/'+kind)
            for j,a in enumerate(q['minutes']):
                den=sum(f['N6_minutes'][j]['so_giay'] for f in fs);num=sum(f['N6_minutes'][j]['so_giay_bao'] for f in fs)
                ck('main_N6',a['alarm_seconds']==num and a['seconds']==den and a['rate']==num/den,det+'/'+group+'/'+str(j))
    for flag,scopes in v7['aggregate'].items():
        for scope,groups in scopes.items():
            for group,q in groups.items():
                parts=[]
                for oid,c in v7['cases'].items():
                    if scope!='all' and c[scope]!=group:continue
                    parts.append(c['B1'] if flag=='B1' else c['B4'][flag.split('/')[1][1:]][flag.split('/')[2][1:]])
                den=sum(p['control_n'] for p in parts); num=sum(p['control_true'] for p in parts);first=[p['at_first'] for p in parts if p['at_first_valid']]
                fr=sum(first)/len(first) if first else None
                ck('V7_counts',q['nonalarm_n']==den and q['nonalarm_true']==num and q['at_first_n']==len(first) and q['at_first_true']==sum(first),flag+'/'+scope+'/'+group)
                ck('V7_rates',q['at_first_rate']==fr and q['nonalarm_rate']==num/den and q['rates_exactly_equal']==(fr is not None and fr==num/den),flag+'/'+scope+'/'+group)
                if flag!='B1':
                    a=summary['V7_direction'][scope][group]['variants'][flag]; delta=fr-num/den if fr is not None else None
                    ck('main_V7_direction',a['difference']==delta and a['direction']==(None if delta is None else '+' if delta>0 else '-' if delta<0 else '='),flag+'/'+scope+'/'+group)
    result={'status':'PASS' if not failures else 'FAIL','time':now(),'wall_s':time.perf_counter()-st,'reports':per_report,'check_counts':dict(counts),'mismatch_count':len(failures),'mismatches':failures,
            'script_sha256':sha(__file__),'source_hashes':{p:sha(ROOT/p) for p in set(cache)|{metric_source,decisions_path}},'classified_names':named_occurrences,
            'literal_policy':'All empirical numeric appearances require binding. Recognized task/HP/case IDs, metric names, source locations and protocol keys are classified explicitly; N2 captions and history labels checked against original JSON keys. No equivalence/significance threshold added.'}
    (run/'verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (run/'script.py').write_bytes(Path(__file__).read_bytes())
    log('Ghi '+run.relative_to(ROOT).as_posix()+'/verification.json và snapshot script; '+result['status']+', '+str(len(failures))+' lệch, '+str(sum(x['scalar_count'] for x in per_report.values()))+' giá trị scalar. Lượt hỏng giữ nguyên nếu có.')
    print(json.dumps({'status':result['status'],'reports':per_report,'counts':dict(counts),'mismatches':failures[:8]},ensure_ascii=True))
    if failures:raise SystemExit(1)
if __name__=='__main__':main()
