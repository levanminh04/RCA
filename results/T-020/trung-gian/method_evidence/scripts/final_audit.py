"""Pinned numeric/default checks, script inventory and immutable input hashes."""
from pathlib import Path
import ast,csv,hashlib,json,re,time,unicodedata
R=Path('D:/RCA-flashticket');O=R/'results/T-020/trung-gian/method_evidence';t0=time.monotonic()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def jr(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def table_rows(text):return [x for x in text.splitlines() if x.startswith('| ') and not x.startswith('|---')][1:]
def writecsv(name,rows):
    with (O/name).open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,list(rows[0]));w.writeheader();w.writerows(rows)
p=R/'results/T-001/danh-sach-phuong-phap.md';s=p.read_text(encoding='utf-8');rows=[]
def add(key,expected,actual,source,query,line):
    rows.append({'task':'T-001','document':str(p),'document_line':line,'key':key,'original_value':expected,'recomputed_value':actual,'match':'PASS' if expected==actual else 'MISMATCH','source':source,'query':query,'source_sha256':sha(source.split('#')[0]),'reason':'structural count/default from original table or pinned code, not prose score copied'})
main=s.split('**Phương pháp RCA có hồ sơ đầy đủ (5):**')[1].split('**CIRCA hai biến thể**')[0]
ctrl=s.split('**Biến thể đối chứng, không có hồ sơ riêng (3):**')[1].split('**Bộ phát hiện')[0]
add('full_RCA_profiles',5,len(table_rows(main)),str(p),'count actual table data rows in §8.1',205)
add('control_variants',3,len(table_rows(ctrl)),str(p),'count actual control table data rows in §8.1',220)
candidates=s.split('### 3a.')[1].split('### 3b.')[0]
add('RCA_candidates',11,len(re.findall(r'^\|\s*\d+\s*\|',candidates,re.M)),str(p),'count numbered source rows §3a, not detector rows',100)
code=Path('D:/RCA-ext/src/RCAEval/RCAEval/e2e/microrank.py');tree=ast.parse(code.read_text());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='pageRank');defaults=dict(zip([x.arg for x in f.args.args][-len(f.args.defaults):],map(ast.literal_eval,f.args.defaults)))
add('MicroRank_damping',.85,defaults['d'],str(code),'AST pageRank default d',64)
add('MicroRank_call_edge_alpha',.01,defaults['alpha'],str(code),'AST pageRank default alpha',64)
calls=[x for x in ast.walk(tree) if isinstance(x,ast.Call) for k in x.keywords if k.arg=='top_max' and isinstance(k.value,ast.Constant)]
topvalues=[k.value.value for x in calls for k in x.keywords if k.arg=='top_max'];offsets=[x.comparators[0].right.value for x in ast.walk(tree) if isinstance(x,ast.Compare) and isinstance(x.left,ast.Name) and x.left.id=='index' and len(x.comparators)==1 and isinstance(x.comparators[0],ast.BinOp) and isinstance(x.comparators[0].left,ast.Name) and x.comparators[0].left.id=='top_max']
assert set(topvalues)=={5} and offsets==[6]
add('MicroRank_max_operations',11,topvalues[0]+offsets[0],str(code),'AST explicit top_max=5 + cutoff index<top_max+6',64)
code=Path('D:/RCA-ext/src/baro/baro/anomaly_detection.py');tree=ast.parse(code.read_text());f=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='nsigma');defaults=dict(zip([x.arg for x in f.args.args][-len(f.args.defaults):],map(ast.literal_eval,f.args.defaults)))
add('N-Sigma_detector_sigma',3,defaults['k'],str(code),'AST nsigma default k',83)
add('N-Sigma_detector_warmup_points',100,defaults['startsfrom'],str(code),'AST nsigma default startsfrom',83)
haz=[x.args[1].value for x in ast.walk(tree) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id=='partial' and isinstance(x.args[0],ast.Name) and x.args[0].id=='constant_hazard']
assert len(haz)==1;add('BOCPD_hazard_points',50,haz[0],str(code),'AST partial(constant_hazard,50)',83)
writecsv('T001-checks.csv',rows)

# Complete source-script inventory excludes historical snapshots in runs backups.
executed={
'results/T-013/scripts/kiem_cua_so_delay.py':'copied full25case/4window arithmetic EXECUTED; runs/all-replays.json run1',
'results/T-014/paper/independent_scores.py':'copied saved architecture snapshot272nodes/2176checks PASS; run2',
'results/T-015/scripts/independent_math.py':'copied fixture24checks + independently replayed selected TX2 graphs; run3, selected-root-checks.csv',
'results/T-016/scripts/tinh_lai_s9.py':'copied pure saved cell total arithmetic EXECUTED; run4',
'results/T-016/scripts/tinh_tay.py':'copied full exact S12 TX2 case goc/sua; no author/harness import; run5/6',
'results/T-017/scripts/independent_example.py':'copied normalized selected TX2 input+selftest EXECUTED; run7',
'results/T-018/scripts/tinh_tay_gdn.py':'copied full NumPy fixedcheckpoint exact existing arrays EXECUTED; run8'}
executed.update({
'results/T-014/paper/independent_window.py':'copied full selected TX2 raw-to-array; retry existing T014-main env PASS1088arrays and parents; first missingpyarrow run retained',
'results/T-014/scripts/check_graph_independent.py':'copied saved graph DAG projection PASS6;24cyclic explicitly outside DAG proof; first oldnetworkx API failure retained',
'results/T-015/scripts/independent_inputs.py':'copied full selected TX2 auth raw input; compatible env17/19checks match,2audit aggregations mismatch old saved classification. No graph/count/statistic mismatch; exact4counter differences in checks-normalized.csv. Both failed attempts retained.',
'results/T-017/scripts/compare_example.py':'copied compare every intermediate PASS2226 after independent_example replay',
'results/T-018/scripts/phan_tich_gdn.py':'copied7run19holdout saved-array normalization/statistics, no training or author function; run13'})
inventory=[]
for task in range(13,19):
    folders=[R/f'results/T-{task:03d}/scripts']+([R/'results/T-014/paper',R/'results/T-014/audit'] if task==14 else [])
    for folder in folders:
        for path in sorted(folder.glob('*.py')):
            rel=path.relative_to(R).as_posix();text=path.read_text(encoding='utf-8-sig');norm=unicodedata.normalize('NFD',text.lower());norm=''.join(x for x in norm if unicodedata.category(x)!='Mn').replace('đ','d');candidate=any(x in norm for x in ['independent','doc lap','tinh lai','tinh tay','arithmetic'])
            try:
                tree=ast.parse(text);imports=[ast.unparse(x) for x in ast.walk(tree) if isinstance(x,(ast.Import,ast.ImportFrom))];writes=[{'line':x.lineno,'call':ast.unparse(x)[:240]} for x in ast.walk(tree) if isinstance(x,ast.Call) and ((isinstance(x.func,ast.Attribute) and x.func.attr in ['write_text','write_bytes','mkdir','save','dump','to_csv','to_parquet']) or isinstance(x.func,ast.Name) and x.func.id=='open')]
                parsed=True
            except SyntaxError as e:imports=[];writes=[];parsed=False
            if rel in executed:state='EXECUTED_WITH_DIAGNOSTIC_MISMATCH' if rel.endswith('/independent_inputs.py') else 'EXECUTED';reason=executed[rel]
            elif rel=='results/T-014/paper/independent_window.py':state='NOT_REPLAYED';reason='CLI opens raw selected TrainTicket parquet via inventory before reconstructing snapshot arrays; outside this replay input allowlist (saved arrays only). Raw-to-window source audit delegated to dataset_evidence, scope of RHT comparison explicitly retained.'
            elif rel in ['results/T-013/scripts/kiem_co_che.py','results/T-013/scripts/kiem_sua_phan_bien.py','results/T-013/scripts/kiem_lap_lai.py','results/T-013/scripts/kiem_bo_sung.py']:
                state='COMPONENT_REPLAY';reason='Whole script combines independent math with official BARO/N-Sigma/BOCPD detector calls and old-task writes. Did not replay those calls; scalar algebra/fixture queries checked in selected-root-checks.csv, full mean/variance/max/window decomposition replayed copied R1.'
            elif rel=='results/T-015/scripts/validate_reference_counts_ob.py':state='NOT_REPLAYED_MISSING_LOCAL_INPUT';reason='Script expects task/data/<90OBcase>/traces.parquet. results/T-015/data does not exist locally; original script runs on EC2 mirror and original66.81s proof is saved. No EC2 access or data downloads allowed; no substitute/new90case raw scan.'
            elif rel=='results/T-018/scripts/chuan_bi_gdn.py':state='INDEPENDENT_DATA_PREPARATION_NOT_NUMERIC_RUNNER';reason='Rebuilds train/test/19holdout matrices across30raw dev cases and4feature/train variants in external work/data; separate dataset preparation adapter. This replay uses existing normalized matrices and fixed checkpoint, verifies all inference/normalization quantities; no broad raw30case reconstruction or data writes authorized in this stream.'
            elif rel=='results/T-013/scripts/kiem_ket_qua_cu.py':state='NOT_REPLAYED_BROAD_RAW_SOURCE_AUDIT';reason='Scans every toraiOB simple_metrics.csv and old task report/tar members. Not standalone same-input formula replay; opens cases outside exact1TORAI/25DELAY/1TT replay allowlist. Existing aggregate original JSON/CSV queries preserved; no new broad raw audit.'
            elif candidate and any(w in norm for w in ['ssh','ec2','paramiko']):state='NOT_REPLAYED';reason='Contains EC2/network process or remote execution handling; T020 forbids EC2 and fresh method execution. Source inventory only; saved outputs queried where used.'
            elif candidate and any(w in rel for w in ['lap-','tom_tat','write_','final','handoff','cap_nhat','viet_','tong_hop','summar','hoan_tat','ban_giao']):state='NOT_CALCULATION_RUNNER';reason='Report/assembly/validation writer; writes old task/docs or depends on those paths. Not an independent numerical runner; table values queried directly from original results instead.'
            elif candidate:state='NOT_REPLAYED';reason='Mechanism/source/builder/reproduction diagnostic; not the designated standalone independent numeric runner. Contains original task/path assumptions. No new method/detector run; retained original source/hash/import/write inventory, independent designated runner coverage recorded.'
            else:state='NOT_INDEPENDENT_NUMERIC_RUNNER';reason='Source preparation/adapter/method runner/inventory/document writer; excluded from independent numeric replay.'
            inventory.append({'task':f'T-{task:03d}','path':rel,'bytes':path.stat().st_size,'sha256':sha(path),'whole_source_read':True,'AST_parsed':parsed,'independent_candidate_by_text':candidate,'replay_state':state,'reason':reason,'imports':json.dumps(imports,ensure_ascii=False),'write_sites':json.dumps(writes,ensure_ascii=False)})
writecsv('independent-script-inventory.csv',inventory)
freeze=jr(R/'results/T-020/trung-gian/input-freeze.json');verified=[]
for row in freeze['inputs']:
    p=R/row['path'];verified.append({'path':row['path'],'expected':row['sha256'],'actual':sha(p) if p.exists() else None,'match':p.exists() and sha(p)==row['sha256']})
(O/'runs/input-freeze-verification.json').write_text(json.dumps({'inputs':verified,'all_match':all(x['match'] for x in verified)},ensure_ascii=False,indent=2),encoding='utf-8')
(O/'runs/final-audit-summary.json').write_text(json.dumps({'T001_checks':len(rows),'T001_all_passed':all(x['match']=='PASS' for x in rows),'scripts_inventory':len(inventory),'independent_candidates':sum(x['independent_candidate_by_text'] for x in inventory),'designated_copied_script_sources_executed':len(executed),'freeze_all_match':all(x['match'] for x in verified),'elapsed_seconds':time.monotonic()-t0},indent=2),encoding='utf-8')
print((O/'runs/final-audit-summary.json').read_text())
