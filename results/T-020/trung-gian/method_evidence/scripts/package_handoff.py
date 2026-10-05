"""Package current evidence, preserving diagnostic mismatches and all run failures."""
from pathlib import Path
import csv,json,math,hashlib,time,subprocess
R=Path('D:/RCA-flashticket');O=R/'results/T-020/trung-gian/method_evidence'
def jr(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def readcsv(p):return list(csv.DictReader(Path(p).open(encoding='utf-8-sig')))
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
records=[]
def scalar(value):
    if value=='True':return True
    if value=='False':return False
    try:return float(value)
    except ValueError:return value
def add(task,source,key,old,new,query,component='',hashvalue='',reason='',tolerance=1e-10):
    match=old==new if not isinstance(old,(int,float)) or not isinstance(new,(int,float)) else math.isclose(float(old),float(new),rel_tol=tolerance,abs_tol=tolerance)
    records.append({'task':task,'source':source,'key':key,'original_value':json.dumps(old,ensure_ascii=False) if isinstance(old,(list,dict)) else old,'recomputed_value':json.dumps(new,ensure_ascii=False) if isinstance(new,(list,dict)) else new,'match':'PASS' if match else 'MISMATCH','query':query,'component_source':component,'reason':reason,'selection_hash':hashvalue,'source_sha256':sha(R/source.split('#')[0]) if (R/source.split('#')[0]).exists() else ''})
for row in readcsv(O/'checks.csv'):
    add(row['task'],row['source'],row['key'],scalar(row['original']),scalar(row['recomputed']),row['reason'],row['component_source'],row['selection_hash'],reason='original independent component pool; sampled='+row['sampled'])
for row in readcsv(O/'selected-root-checks.csv'):
    add(row['task'],row['path'],row['key'],float(row['original_value']),float(row['recomputed_value']),row['query'],hashvalue=row['sampling_hash'],reason=row['reason'])
for row in readcsv(O/'T001-checks.csv'):
    add('T-001','results/T-001/danh-sach-phuong-phap.md',row['key'],float(row['original_value']),float(row['recomputed_value']),row['query'],row['source'],reason='code AST/default or table row count; source document line'+row['document_line'])
oldpath='results/T-015/runs/tt-local/auth/example.json';old=jr(R/oldpath);new=jr(O/'runs/microrank-inputs-002/input-calculation.json')
for group in ['normal','anomaly']:
    for key in ['missing_parent_spans','explicit_root_spans']:
        add('T-015',oldpath,f'/groups/{group}/audit/{key}',old['groups'][group]['audit'][key],new['groups'][group]['audit'][key],'independent_inputs.py:44–48 scoped parent join; count unresolved nonroot vs explicit null root using <NA> sentinel',str(O/'runs/microrank-inputs-002/input-calculation.json'),reason='Diagnostic definition/version difference; archived graph-before-null-audit-fix.py:26 excludes <NA>; current graph.py:32 includes it. No inference of new ranker bug or automatic task status change.')
    for key in ['operation_operation','operation_trace','trace_operation','pr_trace']:
        assert old['groups'][group]['graph'][key]==new['groups'][group]['graph'][key]
        add('T-015',oldpath,f'/groups/{group}/graph/{key}/keys_count',len(old['groups'][group]['graph'][key]),len(new['groups'][group]['graph'][key]),'full dictionary equality then count keys of saved/independently joined graph',str(O/'runs/microrank-inputs-002/input-calculation.json'),reason='Full graph relation equality confirmed for this case; does not validate other cases or rerun RCA ranker')
full=jr(O/'runs/r1s-re2tt5-cham-tinh-tay.json');src='results/T-018/runs/r1s-re2tt5-cham-tinh-tay.json';original=jr(R/src)
for key in ['so_tick_test','so_cot','so_cua_so_val','so_o_vuot_dung_sai_diem','tau_tay','so_bao_dong_code','nut_co_chinh_no_trong_topk','so_lang_gieng_that_trung_binh','iqr_test_duoi_1e-6','iqr_val_duoi_1e-6','cot_hang_trong_tap_hoc']:
    add('T-018',src,key,original[key],full[key],'copied NumPy forward→abs error→median/IQR→4tick mean→max feature/threshold; original checkpoint/normalized arrays held fixed',str(O/'runs/r1s-re2tt5-cham-tinh-tay.json'),reason='No GDN author function or training; torch only loads checkpoint')
with (O/'checks-normalized.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,list(records[0]));w.writeheader();w.writerows(records)
with (O/'mismatches.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,list(records[0]));w.writeheader();w.writerows(r for r in records if r['match']=='MISMATCH')
allruns=jr(O/'runs/all-replays.json');freeze=jr(O/'runs/input-freeze-verification.json')
text='''# Bàn giao factual method evidence T020

Không thêm/sửa quyết định, không chọn dataset/phương pháp/protocol. T013 dùng bản đã duyệt R1/N1–3; WHY19/20/Q57 giữ đúng phạm vi candidate của gói. Mọi đầu ra nằm trong method_evidence. Không sửa task cũ/src/data/env, không EC2. Filedownload mới0byte; chỉ đọc primary TORAIv1 HTML qua webtool, không tải binary/dataset hoặc lưufile từweb; transferbytes củawebtool khônginstrumented.

## Bộ ghép

- `07-checklist-doc-nhanh.md`:42đoạn riêng variant/detector, mỗi đoạn<350từ; `method-checklist.csv` giữ inputs/unit/graphrole/cơ chế/default/source/assumption/tính tay/ledger.
- `yeu-cau-hop-nhat.csv`:42hàng từ sáu bảng nguyên16columns +provenance; `header-audit.csv` 0mismatch; mọi chua_kiem giữ nguyên.
- `05-evidence.md`, `label-budget.csv`, `window-parameters.csv`, `runner-leakage.csv`:marker,regime,tuning,normal budget,giây/points/cadence/lookback. Adapter dataset mới chưa kiểm.
- `runtime.csv`:47bản ghi timer thật và dự phóng conditional dataset×seed Q40. GDN chi phí=nseeds*(trainonce/system/seed+inferenceDataset), không nhân train×90ca. `runtime-ledger.csv` chỉ là tổng execution hỗn hợp, không dùng thay chi phí phương pháp.
- `checks-normalized.csv`:gốc/key/query/recompute/match; gồm pool156, root20, T0019, GDN11 và source mismatch4counter/8graphcounts. `checks.csv` là pool156 riêng, không đại diện mọi phép mới.
- `T001-checks.csv`:9đại lượng checked từAST/code và table count. `selected-root-checks.csv`:20lá số khóa riêng củaroot,20PASS. `mismatches.csv` giữ4counter differences.
- `deep-source-audit.md`, `runs/deep-source-audit.json`:18source checks và3revisioncheckPASS; code/paper khác biệt gốc/sửa giữ riêng.
- `independent-script-inventory.csv`:151script nguyên bản đọc toàn source/AST/import/write-site/hash. Text match không tự là numerical runner.12source standalone đã chép/chạy; đúng lý do các script không chạy ở từng hàng.
- `ca-da-chay.csv`, `runs/all-replays.json`:16attempts,12exit0,4retainedfailures; không gọi tất cảexit0 làmethod quality PASS. Tổng subprocess wall78.406s, từng lượt<5phút; gitstatus trước/sau16attempts giống nhau; guard toàn tiến trình cấm ghi ngoài folder này, -B.

## Kiểm độc lập đã chạy

T13 mean/variance/max/candidate/window25DELAY×4 và endpoint/ranks khớp. CIRCA savedarrays272nodes/2176RHT-DA comparisonsPASS; raw→snapshot1088arrays vàparentsPASS; savedgraph6DAGmatch,24cyclic nằm ngoài DAG proof. MicroRank fixture24PASS và root5numeric mathPASS. TORAI full gốc/sửa cùng S12TX2case/window/seed:severity,14BIC,cluster,bins,CI,p-values,fallback,ranks khớp; p-value sai số≤1e-9relative theo SPEC. T17 selftest, normalized tính độc lập và2226comparisonsPASS. T18 NumPy fixedcheckpoint:0ô vượt dung sai, argmax/báođộngkhác0;7run19holdout algebra đã tính lại từ savedarrays. Không đo runtime phương pháp mới; elapsed của scripts là chi phí kiểm.

## Mismatch MicroRank phải giữ đúng nghĩa

Snapshot `results/T-015/runs/tt-local/auth/example.json` có normalaudit missing_parent1326/root0 và anomalyaudit1403/root0. Independent current source `results/T-015/scripts/independent_inputs.py:45–48` dùng unresolved AND nonroot để đếm missing và nhận `<NA>` là explicitroot:0/1326 và0/1403. Archived `runs/source-versions/graph-before-null-audit-fix.py:26` không nhận `<NA>`; current `src/microrank/graph.py:32` có nhận. Mismatch phù hợp khác định nghĩa/phiên bản chẩn đoán null; không tự gán bug xếp hạng hay đổi trạng thái T015.

17/19đối chiếu current input replay khớp:count/SLO/operationidentity, toàn4graphrelations mỗi nhóm,tracecounts đều bằng snapshot. Hai boolauditcomparisonFAIL, cụ thể4counter trongmismatches.csv. `src/microrank/__init__.py:74–90` truyền graph vào PageRank và chỉ lưu audit; graph của đúng ca này đã xác nhận bằng nhau. Không có thêm lượt ranker để tuyên bố benchmark mọi ca hoặc thứ hạng mọi dataset bất biến.

## Các phép không chạy và phạm vi

T13 wholemechanism script trộn independent algebra với code tác giả/detectors và writes task cũ; component/window proof được chạy bằng bản chép độc lập, khôngrerunwhole. T15reference90OBaudit mongtask/data không có local; không EC2/download. T18B3 là data preparation30rawcases×feature/train variants, không standalone numeric inference proof; dùng existing normalized input vàcheckpoint. Script docs/assembly/inventory/EC2/sourcebuilder khác không là calculationrunner; reasons vàactual write sites giữ tronginventory. Không tái học PCdefault/đo method/detector mới hoặc kiểm thích hợpdataset mới. Chưa có normalbudget/calibration chung; PCcyclic proof vàdataset adapter remains chua_kiem.

## Bảo toàn đầu vào

Freeze5772entry:5771hashkhớp, duy nhấtdocs/STATE.md khác do checkpoint luồngroot (reported, không ghi bởi agent này). Toàn old task evidence frozen khớp; manifest/filehash output ở`output-manifest.json`. Giữ originalfailedsourceassert và mechanical attempts; không quy lỗi verifier thành lỗi phương pháp.
'''
(O/'HANDOFF.md').write_text(text,encoding='utf-8')
deep=(O/'deep-source-audit.md').read_text(encoding='utf-8');start=deep.index('`runs/torai-arithmetic-001.json`');end=deep.index('\n## Nguồn đính chính',start)
deep=deep[:start]+'''`runs/torai-arithmetic-001.json` kiểm normalization/grouping56components mỗi bản. Sau đó `runs/torai-full-goc-001.json` và `torai-full-sua-001.json` đã chạy full independent S12 bằng bản chép, tách riêng hàm input của harness qua AST; không import TORAI/RCD/RCAEval/causal-learn. Đúng TX2checkoutservice_cpu/1,L10,seed0; fitGaussianMixture thư viện đúng default và tự tính BIC, độc lập Kmeans/chi-square/PCphases. Severity/14BIC/cluster labels/bins/CI/fallback/finalranks khớp original; phép đầu chỉ normalization không được dùng thay fullproof. Có guard output và gitstatus16attempts trongall-replays.json.

MicroRank fixture24checksPASS; additional raw-input replay17/19PASS và2auditboolFAIL do null-root diagnostic definition. Giữ4counter old→new trongmismatches.csv vàgraphrelations equality; xem HANDOFF, không tự đổi trạng thái T015.
''' +deep[end:]
(O/'deep-source-audit.md').write_text(deep,encoding='utf-8')
e=(O/'05-evidence.md').read_text(encoding='utf-8');e=e.replace('Số mismatch hiện: 0. Mismatch giữ nguyên và lý do trong bảng, không sửa task cũ.','Pool156 không mismatch; root20 vàT0019 đềuPASS. Các kiểm mới giữ4counter diagnostic MicroRank mismatch trong checks-normalized.csv/mismatches.csv; xemHANDOFF. Không sửa task cũ.')
e=e.replace('`runtime.csv` đếm execution ledger, không coi tất cả ca/lần chạy là benchmark một dataset.','`runtime.csv`47dòng timer gốc và dự phóng conditional theo dataset×seed; `runtime-ledger.csv` là executionledger hỗn hợp, không dùng thay methodcost. GDNtrainonce/system/seed + inferenceDataset, không nhân training theo sốincident.')
(O/'05-evidence.md').write_text(e,encoding='utf-8')
manifest=[{'path':p.relative_to(O).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(O.rglob('*')) if p.is_file() and p.name!='output-manifest.json']
(O/'output-manifest.json').write_text(json.dumps({'files':manifest,'total_bytes':sum(p['bytes'] for p in manifest),'public_download_bytes':0,'scope':str(O)},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'normalized_checks':len(records),'diagnostic_counter_mismatches':sum(x['match']=='MISMATCH' for x in records),'output_files':len(manifest),'total_bytes':sum(x['bytes'] for x in manifest),'runs':len(allruns['records'])}))
