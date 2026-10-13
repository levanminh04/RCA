"""Tạo bản V8 mới; giữ nguyên verifier và kết quả V8 lượt đầu."""
from pathlib import Path
import ast
from repair_reports import ROOT, OUT, log

old=OUT/'scripts/verify_reports.py'
new=OUT/'scripts/verify_reports_v2.py'
assert not new.exists()
text=old.read_text(encoding='utf-8')
text=text.replace("    bindings=[p for p in OUT.rglob('*.md.bindings.json')]", """    # Tên metric được truy về chính detector_columns, không loại mọi hậu tố số.
    metric_source='results/T-025/bao-dong.json'
    metric_doc=read(ROOT/metric_source); metric_refs={}
    for det,cases in metric_doc['bo_phat_hien'].items():
        for oid,case in cases.items():
            for j,name in enumerate(case['detector_columns']):
                metric_refs.setdefault(name,{'path':metric_source,'pointer':'/bo_phat_hien/'+det+'/'+oid+'/detector_columns/'+str(j)})
    decisions_path='docs/DECISIONS.md'; decisions_text=(ROOT/decisions_path).read_text(encoding='utf-8')
    decision_codes=set(re.findall(r'^\\| (Q-\\d+) \\|',decisions_text,re.M))
    named_occurrences=[]
    bindings=[p for p in OUT.rglob('*.md.bindings.json')]
    ck('binding_file_count',len(bindings)==5)
""")
anchor="        for identifier in sorted(identifiers,key=len,reverse=True):scrub=scrub.replace(identifier,' FLAG ')"
insert="""        def metric_name(m):
            name=m.group(0);ref=metric_refs.get(name)
            ck('metric_identifier_source',ref is not None,{'report':report.name,'name':name})
            if ref is None:return name
            ck('metric_identifier_value',resolve(metric_doc,ref['pointer'])==name,name)
            named_occurrences.append({'report':report.name,'name':name,**ref})
            return ' METRIC_NAME '
        scrub=re.sub(r'(?<![\\w-])ts-[A-Za-z0-9_-]+_(?:latency|error)-\\d+(?![\\w-])',metric_name,scrub)
        def decision_code(m):
            code=m.group(0);ok=code in decision_codes
            ck('decision_identifier_source',ok,code)
            if ok:named_occurrences.append({'report':report.name,'name':code,'path':decisions_path,'locator':'table row '+code})
            return ' DECISION_CODE ' if ok else code
        scrub=re.sub(r'\\bQ-\\d+\\b',decision_code,scrub)
        def run_code(m):
            name=m.group(0);path=OUT/'runs'/name;ok=path.is_dir() and any(path.iterdir())
            ck('run_identifier_source',ok,name)
            if ok:named_occurrences.append({'report':report.name,'name':name,'path':path.relative_to(ROOT).as_posix(),'locator':'preserved run directory'})
            return ' RUN_CODE ' if ok else name
        scrub=re.sub(r'\\bmanual-evidence-\\d+\\b',run_code,scrub)
"""
assert text.count(anchor)==1;text=text.replace(anchor,insert+anchor)
text=text.replace("        scrub=re.sub(r'\\b(?:latency|error)-(?:50|90)\\b',' METRIC_NAME ',scrub)\n",'')
oldtable="""        table_cols=None; malformed=[]
        for line_no,line in enumerate(text.splitlines(),1):
            if line.startswith('|'):
                columns=len(re.split(r'(?<!\\\\)\\|',line))-2
                if table_cols is None:table_cols=columns
                elif columns!=table_cols:malformed.append(line_no)
            else:table_cols=None
        ck('markdown_table_shape',not malformed,{'report':report.name,'lines':malformed})"""
newtable="""        table_cols=None; malformed=[]; blocks=[]; block=[]
        for line_no,line in enumerate(text.splitlines(),1):
            if line.startswith('|'):
                columns=len(re.split(r'(?<!\\\\)\\|',line))-2
                if table_cols is None:table_cols=columns
                elif columns!=table_cols:malformed.append(line_no)
                block.append((line_no,line))
            else:
                table_cols=None
                if block:blocks.append(block);block=[]
        if block:blocks.append(block)
        # Bắt cả hàng w bị tách khỏi header bởi ghi chú, lỗi width đơn thuần bỏ sót.
        for block in blocks:
            if len(block)<2 or not re.fullmatch(r'\\|(?:\\s*:?-+:?\\s*\\|)+',block[1][1]):malformed.append(block[0][0])
        ck('markdown_table_shape',not malformed,{'report':report.name,'lines':sorted(set(malformed))})"""
assert oldtable in text;text=text.replace(oldtable,newtable)
text=text.replace("'source_hashes':{p:sha(ROOT/p) for p in cache},", "'source_hashes':{p:sha(ROOT/p) for p in set(cache)|{metric_source,decisions_path}},'classified_names':named_occurrences,")
ast.parse(text)
log('Lệnh có ghi: T014-main Python -B -X utf8 -W ignore scripts/prepare_v8_repair.py. Tạo verify_reports_v2.py từ verifier cũ; giữ nguyên verify_reports.py và V8-reports-001. Phân loại metric bằng giá trị/con trỏ detector_columns T025, Q-code bằng dòng DECISIONS thực, run-code bằng lượt cũ có thật; không bỏ số định lượng chưa nguồn. Kiểm bảng nhận cả hàng bị ghi chú tách khỏi header. AST PASS; chưa chạy V8 mới.')
new.write_text(text,encoding='utf-8')
print(new.relative_to(ROOT).as_posix())
