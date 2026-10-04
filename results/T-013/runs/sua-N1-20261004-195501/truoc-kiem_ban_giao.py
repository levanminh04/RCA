"""Read and verify every owned output and neutral reviewer prompt."""
import json,csv,ast,subprocess,hashlib,sys,re
from pathlib import Path
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013';TASK=ROOT/'tasks/T-013-ho-so-baro'
def no_constant(v):raise ValueError('Nonstandard JSON constant '+v)
files=sorted(OUT.rglob('*')); files=[p for p in files if p.is_file()]
issues=[];parse_counts={'json':0,'csv':0,'python':0,'npz':0,'markdown':0};verified=[]
required=['ho-so-baro.md','ho-so-bocpd.md','ho-so-nsigma-phat-hien.md','vi-du-tinh-tay.md','cua-so-va-che-do-b.md','yeu-cau-dau-vao.csv','ca-da-chay.csv','dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md','moi-truong.md','manifest.json','kiem-tra.json','doi-chieu-moc.json','doi-chieu-tieu-chi.md']
assert all((OUT/p).is_file() for p in required)
for p in files:
    suffix=p.suffix
    if suffix=='.json':
        try:json.loads(p.read_text(encoding='utf-8-sig'),parse_constant=no_constant)
        except Exception as e:issues.append({'file':str(p),'error':str(e)})
        parse_counts['json']+=1
    elif suffix=='.csv':
        with p.open(encoding='utf-8-sig',newline='') as f:
            rows=list(csv.reader(f)); assert rows and all(len(r)==len(rows[0]) for r in rows)
        parse_counts['csv']+=1
        if p.name.endswith('-metric.csv'):
            import math
            h=rows[0];si=h.index('score');oi=h.index('official_score')
            for r in rows[1:]:
                if r[si] and r[oi]:assert abs(float(r[si])-float(r[oi]))<=1e-10*max(1,abs(float(r[oi])))
    elif suffix=='.py':ast.parse(p.read_text(encoding='utf-8-sig'));parse_counts['python']+=1
    elif suffix=='.npz':
        import numpy as np
        with np.load(p,allow_pickle=False) as x:
            if 'independent' in x:assert np.max(np.abs(x['independent']-x['official']))<=1e-10
        parse_counts['npz']+=1
    elif suffix=='.md':
        t=p.read_text(encoding='utf-8-sig');parse_counts['markdown']+=1
        if p.name.startswith('ho-so-'):assert all(re.search(r'^## '+str(i)+r'\.',t,re.M) for i in range(1,10))
    verified.append(str(p.relative_to(ROOT)).replace('\\','/'))
# Old failed partial JSON can contain NaN: retain originals, document their status.
assert not issues,issues
with (OUT/'yeu-cau-dau-vao.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.reader(f))
header='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
assert rows[0]==header and len(rows)==7
s=json.loads((OUT/'kiem-tra.json').read_text(encoding='utf-8'));assert s['status']=='complete'
selected={r['case'] for r in s['selection']['selected']}
with (OUT/'ca-da-chay.csv').open(encoding='utf-8-sig',newline='') as f:ledger=list(csv.DictReader(f))
assert all(r['ca'] in selected|{'synthetic'} and r['ly_do'] in {'a','b','c'} for r in ledger)
old=json.loads((OUT/'trung-gian/cua-so-cu.json').read_text(encoding='utf-8'));assert abs(old['difference']-.256)<1e-10
sources={}
for name,expected in [('baro','e35f4ec'),('RCAEval','259ea41')]:
    d=Path('D:/RCA-ext/src')/name
    head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=d,text=True).strip()
    status=subprocess.check_output(['git','status','--short'],cwd=d,text=True).strip();assert head.startswith(expected) and not status
    sources[name]={'head':head,'status':status}
# Validate neutral prompt only after it has been appended.
log=(TASK/'LOG.md').read_text(encoding='utf-8');review=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
if '## Prompt phản biện cho Claude' in log:
    common=review.split('## Prompt chung',1)[1].split('```text\n',1)[1].split('```',1)[0]
    g1=review.split('**G1 — phương pháp, dataset, cách chia:**',1)[1].split('```text\n',1)[1].split('```',1)[0]
    actual=log.split('## Prompt phản biện cho Claude',1)[1]
    assert g1 in actual
    inventory=json.loads((OUT/'danh-sach-file.json').read_text(encoding='utf-8'))
    assert set(inventory['result_outputs'])==set(verified)
    all_paths=inventory['task_outputs']+inventory['result_outputs']+inventory['external_outputs']
    file_list='\n'+'\n'.join('- '+p for p in all_paths)
    expected=common.replace('<T-xxx>','T-013').replace('<T-xxx-tên>','T-013-ho-so-baro')
    expected=expected.replace('<danh sách>',file_list).replace('<commit gốc>','93f13d4c4a966428177e2acc287d96bc89303e92')
    assert expected.rstrip() in actual
    assert all(v in actual for v in verified),[v for v in verified if v not in actual]
    assert 'D:/RCA-ext/work/T-013/metrics-selected.npz' in actual
    assert 'D:/RCA-ext/work/T-013/metrics-selected.json' in actual
    request=Path('C:/Users/84583/.codex/attachments/2f6c5735-a241-4299-bd8c-25d4034a97de/Pasted text.txt').read_text(encoding='utf-8-sig')
    task_block=re.search(r'^<task>\r?\n.*?^</task>',request,re.M|re.S).group(0)
    corrected=log.split('**Khối task đúng nguyên văn, thay cho bản trích dư ở đầu LOG:**',1)[1]
    assert task_block in corrected
    state=(ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig')
    assert '| T-013 | Hồ sơ BARO và bộ phát hiện | P1 | Codex | Claude | chờ phản biện (04/10/2026) | `tasks/T-013-ho-so-baro/` |' in state
    assert json.loads((OUT/'trung-gian/kiem-adapter.json').read_text(encoding='utf-8'))['status']=='pass'
diff=subprocess.check_output(['git','diff','--check','--','docs/STATE.md','tasks/T-013-ho-so-baro','results/T-013'],cwd=ROOT,text=True)
assert not diff
result={'status':'pass','result_files_read':len(files),'parse_counts':parse_counts,'checks_in_mechanism_summary':len(s['checks']),'input_csv_columns':len(header),'input_csv_rows':len(rows)-1,'ledger_rows':len(ledger),'method_cases':sorted(selected),'code_sources_unchanged':sources,'scope':'only T013 authored paths and exactly one own STATE row; unrelated concurrent changes not claimed as ours','git_diff_check':'pass','handoff_prompt_verbatim_and_inventory_complete':'## Prompt phản biện cho Claude' in log,'issues':issues}
(OUT/'kiem-ban-giao.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
