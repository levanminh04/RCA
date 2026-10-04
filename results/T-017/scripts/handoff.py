"""Validate and inventory T017 only; append neutral review prompt after state edit."""
import argparse,ast,csv,hashlib,inspect,json,re,subprocess,sys,unittest,io
from pathlib import Path
from datetime import datetime,timezone,timedelta
from contextlib import redirect_stdout
import numpy,pandas,pyarrow
from simplerca import diagnose
R=Path('D:/RCA-flashticket');O=R/'results/T-017';T=R/'tasks/T-017-simplerca'
W=Path('D:/RCA-ext/work/T-017');E=Path('D:/RCA-ext/envs/T-017-simple')
HEAD='93f13d4c4a966428177e2acc287d96bc89303e92'
def dump(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def paths():
    return sorted([p for base in (T,O,R/'src/simplerca',W,E) for p in base.rglob('*') if p.is_file()],key=lambda p:str(p).lower())
def inventory():
    cached={};cache_time=0
    if (O/'inventory-files.csv').exists():
        cache_time=(O/'inventory-files.csv').stat().st_mtime_ns
        with (O/'inventory-files.csv').open(encoding='utf-8') as f:cached={x['absolute_path']:x for x in csv.DictReader(f)}
    rows=[]
    for p in paths():
        circular=p in (O/'inventory-files.csv',O/'runs/handoff-check.json')
        stat=p.stat();old=cached.get(str(p));external=not p.is_relative_to(R)
        reusable=external and old and str(stat.st_size)==old['bytes'] and stat.st_mtime_ns<=cache_time and (not old.get('mtime_ns') or str(stat.st_mtime_ns)==old['mtime_ns'])
        digest='self-reference' if circular else old['sha256'] if reusable else sha(p)
        rows.append([str(p),stat.st_size,digest,'outside repo' if external else 'repo',stat.st_mtime_ns])
    # Include the inventory itself, with no recursive hash.
    if not (O/'inventory-files.csv').exists():rows.append([str(O/'inventory-files.csv'),'self-reference','self-reference','repo','self-reference'])
    with (O/'inventory-files.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f);w.writerow(['absolute_path','bytes','sha256','location','mtime_ns']);w.writerows(rows)
    return rows
def validation(tests=False):
    checks={};files=paths()
    for p in files:
        if p.is_relative_to(R) and p.suffix=='.py':ast.parse(p.read_text(encoding='utf-8'),filename=str(p))
    checks['all_own_python_parse']=True
    for p in (O/'ho-so-simplerca.md',O/'vi-du-tinh-tay.md',O/'type-i-ii.md',O/'doi-chieu-code.md',O/'kiem-dung-dan.md',O/'moi-truong.md',O/'ca-da-chay.csv',O/'dinh-chinh-task-cu.md',O/'de-xuat-tai-lieu-chung.md',O/'tieu-chi-xong.csv'):
        assert p.is_file() and p.stat().st_size>0,str(p)
    checks['required_outputs_exist']=True
    with (O/'yeu-cau-dau-vao.csv').open(encoding='utf-8',newline='') as f:rows=list(csv.reader(f))
    expected='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
    assert rows[0]==expected and len(rows)==12 and all(len(x)==16 and all(x) for x in rows)
    checks['input_csv_16_columns_11_rows']=True
    summary=json.loads((O/'runs/run-dev-004/summary.json').read_text(encoding='utf-8'))
    allowed=json.loads((O/'allowlist.json').read_text(encoding='utf-8'))
    assert len(summary)==30 and set(x['case'] for x in summary)==set(allowed)
    assert all(x['status']!='failed' for x in summary)
    source_files={path:data for x in summary for path,data in x['source_hashes'].items()}
    for path,meta in source_files.items():
        p=Path(path)
        assert p.is_relative_to(W/'injection') or (p.parent.name in allowed and p.resolve().parent.parent==(R/'data/rcaeval').resolve())
        assert p.stat().st_size==meta['bytes'] and sha(p)==meta['sha256'],path
    checks['source_hashes_unchanged_files']=len(source_files)
    checks['core_signature_measurements_only']=list(inspect.signature(diagnose).parameters)
    assert all(x not in inspect.signature(diagnose).parameters for x in ('root','case','fault_type','path','inject_time','graph'))
    indep=ast.parse((O/'scripts/independent_example.py').read_text(encoding='utf-8'))
    imports=[n.module or '' for n in ast.walk(indep) if isinstance(n,ast.ImportFrom)]+[a.name for n in ast.walk(indep) if isinstance(n,ast.Import) for a in n.names]
    assert all('simplerca' not in x for x in imports)
    checks['independent_no_main_import']=True
    for p in (O/'ho-so-simplerca.md',):
        for file,num in re.findall(r'`(src/simplerca/[^:`]+):(\d+)`',p.read_text(encoding='utf-8')): assert 1<=int(num)<=len((R/file).read_text(encoding='utf-8').splitlines())
    checks['parameter_line_references_exist']=True
    if tests:
        stream=io.StringIO();suite=unittest.defaultTestLoader.discover(str(R/'src/simplerca/tests'))
        result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
        (O/'runs/final-unit-tests.txt').write_text(stream.getvalue(),encoding='utf-8')
        assert result.wasSuccessful() and result.testsRun==16
        independent=subprocess.run([sys.executable,str(O/'scripts/independent_example.py'),'--self-test'],capture_output=True,text=True,encoding='utf-8')
        (O/'runs/final-independent-self-test.txt').write_text(independent.stdout+independent.stderr,encoding='utf-8')
        assert independent.returncode==0
        checks['unit_tests']=16;checks['independent_self_test']=independent.stdout.strip()
    return checks
def source_notes():
    import shutil
    for name in ('fse-new-artifact-local-check.json','fse-new-artifact-code-comparison.json','fse-artifact-result-filter-check.json','zip-inventory.json','static-syntax-check.json'):
        p=W/'sources-audit'/name
        if p.exists():shutil.copy2(p,O/'sources'/name)
    code=json.loads((O/'sources/git-blob-verification.json').read_text(encoding='utf-8'))
    assert len(code)==70 and all(x['git_blob_matches'] for x in code)
    downloads=json.loads((O/'sources/download-manifest.json').read_text(encoding='utf-8'))
    inject=json.loads((O/'sources/injection-manifest.json').read_text(encoding='utf-8'))
    provenance={'initial_head':HEAD,'current_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),'device':'Windows11 laptop i5-1240P/16GB, concurrent sessions','task':'T-017','self_spec_authorization':'Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026','download_estimate_logged_before_fetch_bytes':30000000,'source_download_manifest_bytes':sum(x['bytes'] for x in downloads),'arxiv_pdf_additional_bytes':(W/'2510.04711v2.pdf').stat().st_size,'injection_remote_bytes':sum(x['bytes'] for x in inject if x['source'].startswith('https:')),'data_telemetry_download_bytes':0,'data_locked_opened':False,'official_timing':False,'packages':{n:{'version':m.__version__,'path':m.__file__} for n,m in [('numpy',numpy),('pandas',pandas),('pyarrow',pyarrow)]},'revision_source':'sources/download-manifest.json','initial_scope_accident':'sources/T-017 empty directory removed; no files/residual','common_docs_written':'only T017 STATE row; other common content drafts in de-xuat-tai-lieu-chung.md','raw_telemetry_source_hashes':'runs/run-dev-004/summary.json','all_created_file_paths':'inventory-files.csv'}
    dump(O/'runs/provenance.json',provenance)
def review_prompt():
    text=(R/'docs/review-prompt.md').read_text(encoding='utf-8')
    common=re.search(r'## Prompt chung[\s\S]*?```text\n([\s\S]*?)\n```',text).group(1)
    g1=re.search(r'\*\*G1 — phương pháp, dataset, cách chia:\*\*\s*```text\n([\s\S]*?)\n```',text).group(1)
    # Every file is enumerated literally, including environment/source scratch.
    output_paths=paths()
    if O/'runs/handoff-check.json' not in output_paths:output_paths.append(O/'runs/handoff-check.json')
    listing='\n'+ '\n'.join('- '+str(p) for p in sorted(output_paths,key=lambda p:str(p).lower()))
    filled=common.replace('<T-xxx>','T-017').replace('<T-xxx-tên>','T-017-simplerca').replace('<danh sách>',listing).replace('<commit gốc>',HEAD)
    assert '<' not in filled
    return filled+'\n\n'+g1,{'common_template_exact_after_neutral_fill':True,'g1_block_exact':True,'every_output_listed':True,'uses_git_diff_as_output_scope':False}
def finalize():
    state=json.loads((O/'runs/state-edit-check.json').read_text(encoding='utf-8'))
    assert state['status']=='PASS' and state['other_content_byte_identical']
    checks=validation()
    report='''A. Đã làm: cài SimpleRCA M4 độc lập, hồ sơ9mục, TypeI/II/tỷ lệ PDF riêng, audit3revision/license/artifact và30dev;25/30đúng hạng1. Không gọi đây là tái lập full0,80.
B. File đã thay đổi: tasks/T-017-simplerca/SPEC.md, LOG.md; src/simplerca/; results/T-017/; đúng dòngT017 trong docs/STATE.md. Ngoài repo: D:/RCA-ext/work/T-017/ và envs/T-017-simple/. Mọi file liệt kê trong inventory-files.csv và prompt dưới. Thư mục sources/T-017 tạo nhầm đã gỡ rỗng, không còn. Các thay đổi task khác trong status thuộc phiên khác.
C. Kiểm tra:16tests;12nhóm độc lập;2226so sánh ví dụ khớp;repeat/permutation2ca;30output khôngfallback, đủ tổngđiểm;guard30ca/89file, alias/collision, log-count độc lập và3ngưỡng đạt. Hai normal-control thực không đạt abstention; đã giữ và không sửa ngưỡng. Hash119nguồn gồm telemetry+metadata không đổi.
D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM: T001 nhầm CLIorig với lớpSimpleRCA riêng; luậtType bị khái quát chỉlog; thiếu nhánh preprocessingRE3SS. Đã triển khai static/source/PDF audit và nháp sửa trong dinh-chinh-task-cu.md; không sửa task cũ. Không phát hiện lỗi mới khác có bằng chứng trong phần liên quan.
E. Chỗ lệch khỏi SPEC: đổi nguồn mốc vì thiếu metadata, giữfailed001/002; sửa regexgộpDB vàrerun004; bổ sung collision/path/log kiểm rẻ; đính chính lỗiđếm17→16cột. Mọi thay đổi ghi thêm cuốiSPEC. Không thay thiết kế theo nhãn.
F. Đề xuất tài liệu chung: nhápDECISIONS quyền tựSPEC, WHY các quy ướcM4 vàLESSONS lỗialias tại de-xuat-tai-lieu-chung.md. Không ghi các filechung.
G. Chưa kiểm: full90RE2TT(60khóa); exactprogram/table2 và outputsdevtácgiả(chưa có nguồn); exactTypeclassifier(bài thiếu luật); durationphysicalunit/latencysemantic(chưa cómetadata); costchínhthức(máy dùngchung); generality/P4(ngoài task). Giảđịnh/khi sai/cáchkiểm ởkiem-dung-dan.md. Normal-control bấtlợi là đã kiểm, không gán chưa kiểm.
H. Cần Minh quyết: xử lý bađínhchínhT001, nhápWHY/DECISIONS/LESSONS và phạmvi dùngSimpleRCAM4 tạiG1. Chưa cần mởlocked hoặc chọn tham sốP3 trongtask. Mâu thuẫnEadroSN0,94vs0,96 trongPDF cầncount/configgốc nếu muốn giải quyết. Không commit/push; đề xuất commit khiMinhduyệt: “Hoàn thành hồ sơ và bản cài SimpleRCA M4 T017”.'''
    prompt,neutral=review_prompt()
    tail='\n\n**Kết thúc phiên — 04/10/2026:**\n1. Đã làm gì: xem báo cáo A–H dưới.\n2. File đã thay đổi: đúng phạm vi T017 và một dòng STATE; mọi file ngoài repo được liệt kê.\n3. Kiểm tra đã chạy và kết quả: xem C; evidence tại runs/handoff-check.json và các run bảo toàn.\n4. Điều chưa chắc hoặc cần Minh quyết: xem G/H; không thay tài liệu chung.\n5. Bước tiếp theo chính xác: Minh mở phiên Claude riêng, dán nguyên prompt cuối LOG; Claude đọc SPEC/LOG/output thật, chỉ ghi tasks/T-017-simplerca/REVIEW.md. Không chạy lại kết quả hợp lệ, không mở locked.\n6. Lệnh cuối cùng đã chạy trước bàn giao: py -3 results/T-017/scripts/handoff.py --finalize; sau đó chỉ verify inventory và mở hồ sơ để đọc.\n\n**Báo cáo cuối A–H:**\n'+report+'\n\n## Prompt phản biện cho Claude\n\n```text\n'+prompt+'\n```\n'
    with (T/'LOG.md').open('a',encoding='utf-8') as f:f.write(tail)
    checks.update(neutral);checks['STATE_T017_only']=True
    checks['status']='PASS';checks['time_local']=datetime.now(timezone(timedelta(hours=7))).isoformat()
    dump(O/'runs/handoff-check.json',checks)
    inventory()
    print(json.dumps(checks,ensure_ascii=False,indent=2))
def verify_inventory():
    with (O/'inventory-files.csv').open(encoding='utf-8') as f:rows=list(csv.DictReader(f))
    assert set(x['absolute_path'] for x in rows)==set(map(str,paths()))
    for row in rows:
        if row['sha256']=='self-reference':continue
        p=Path(row['absolute_path']);stat=p.stat()
        assert stat.st_size==int(row['bytes']),str(p)
        if row['location']=='outside repo':assert str(stat.st_mtime_ns)==row['mtime_ns'],str(p)
        else:assert sha(p)==row['sha256'],str(p)
    check=json.loads((O/'runs/handoff-check.json').read_text(encoding='utf-8'))
    print(json.dumps({'inventory_files':len(rows),'outside_repo_files':sum(x['location']=='outside repo' for x in rows),'all_repo_hashes_match':True,'external_unchanged_since_full_hash_pass':True,'handoff_status':check['status']},ensure_ascii=False))
ap=argparse.ArgumentParser();ap.add_argument('--prepare',action='store_true');ap.add_argument('--finalize',action='store_true');ap.add_argument('--verify',action='store_true');a=ap.parse_args()
if a.prepare:source_notes();dump(O/'runs/pre-handoff-check.json',validation(tests=True));inventory();print('pre-handoff PASS')
if a.finalize:finalize()
if a.verify:verify_inventory()
