"""Validate handoff tables, actual outputs and numeric citations (read only)."""
import ast,csv,json,re,math,hashlib,sys
from pathlib import Path

repo=Path('D:/RCA-flashticket');out=repo/'results/T-014';checks=[]
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def check(name,value,detail=None):checks.append(dict(check=name,pass_=bool(value),detail=detail))
fields='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
with (out/'yeu-cau-dau-vao.csv').open(encoding='utf-8-sig',newline='') as f:
    reader=csv.DictReader(f);rows=list(reader)
    check('input CSV exact 16-column schema',reader.fieldnames==fields)
    check('input CSV nine distinct variants; every cell populated',len(rows)==9 and len({r['bien_the'] for r in rows})==9 and all(all(r[k].strip() for k in fields) for r in rows))
with (out/'ca-da-chay.csv').open(encoding='utf-8-sig',newline='') as f: cases=list(csv.DictReader(f))
allow={p.name for p in (repo/'data/rcaeval').glob('re2tt_*') if p.is_dir()}
check('TT case inventory exactly authorized 30',len(allow)==30)
check('case registry TT allowlist',all(r['ca'] in allow for r in cases if r['ca'].startswith('re2tt_')))
check('all actual non-TT runs in allowed legacy fse-OB',all(r['ca'].startswith(('fse-ob/','fse-ob_')) for r in cases if not r['ca'].startswith('re2tt_')))
check('registry has purpose, source, a/b/c',all(r['file_nguon'] and r['muc_dich'] and r['ly_do'] in ['a','b','c'] for r in cases),len(cases))
inv=load(out/'runs/inventory.json')
check('inventory matches actual 30 permitted directories',set(r['case'] for r in inv)==allow)
check('graph reports 30 with expected identities',{p.stem for p in (out/'graphs').glob('re2tt_*.json')}==allow)
agg=load(out/'graphs/aggregate.json');graphs=[load(p) for p in (out/'graphs').glob('re2tt_*.json')]
check('graph summary independently recounted',agg['unknown_total']==sum(len(g['unknown']) for g in graphs) and agg['call_cyclic_cases']==sum(not g['call_dag'] for g in graphs) and agg['metric_edges_max']==max(g['metric_edges'] for g in graphs))
check('native factory edge/coverage equivalence actually complete',load(out/'runs/native-yaml-equivalence.json')['pass_'])
for kind in ['pc','kien-truc']:
    text=(out/f'ho-so-circa-{kind}.md').read_text(encoding='utf-8-sig')
    check(f'{kind} profile nine numbered sections',re.findall(r'^## (\d+)\.',text,re.M)==list(map(str,range(1,10))))
    check(f'{kind} profile explicit pending WHY and code locations','chờ WHY' in text and 'file:dòng' in text and '§4.3' in text)
for mode,profile in [('example-pc','pc'),('example-architecture','kien-truc')]:
    s=load(out/f'runs/{mode}/snapshot.json');i=load(out/f'runs/{mode}/interpretation.json')
    check(mode+' genuine finite nonempty scoring',bool(s['nodes']) and all(math.isfinite(n['rht_score']) for n in s['nodes'].values()) and len(s['ranks'])==len(s['nodes']))
    text=(out/f'ho-so-circa-{profile}.md').read_text(encoding='utf-8-sig')
    top=s['ranks'][0];check(mode+' numeric top cited in profile',str(top[1]) in text)
    selected_inventory=next(r for r in inv if r['case']==i['case'])
    check(mode+' top independent of input-column order',top[0]!=selected_inventory['processed_columns'][0])
    check(mode+' no exception fallback route',load(out/'runs/regression-route-summary.json')['runs'][mode].get('value_error_fallback',0)==0)
for name in ['compare-example-architecture/comparison.json','compare-example-pc-001/comparison.json','window-example-architecture-002/window-comparison.json','window-example-pc-001/window-comparison.json']:
    check('independent '+name,load(out/'paper'/name)['pass'])
check('normal negative-control failure explicitly reported',load(out/'runs/normal-sanity-explained.json')['sanity_verdict'].startswith('FAIL') and 'không đạt' in (out/'ho-so-circa-kien-truc.md').read_text(encoding='utf-8'))
check('PC adjacency source alignment',load(out/'paper/pc-source-alignment.json').get('pass',False))
parse_errors=[]
for base in [repo/'src/circa_kien_truc',out/'scripts',out/'paper',out/'audit']:
    for p in base.glob('*.py'):
        try:ast.parse(p.read_text(encoding='utf-8-sig'),filename=str(p))
        except SyntaxError as exc:parse_errors.append((str(p),str(exc)))
check('all own source/scripts Python syntax',not parse_errors,parse_errors)
mandatory=['dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md','moi-truong.md','kiem-tra-va-doi-chieu-spec.md','manifest-files.csv','runs/chi-phi-tong.json']
check('mandatory handoff outputs present',all((out/name).is_file() and (out/name).stat().st_size>0 for name in mandatory))
check('authorization exact sentence in LOG','Minh ủy quyền tự duyệt SPEC theo prompt Đợt 1 ngày 04/10/2026' in (repo/'tasks/T-014-ho-so-circa/LOG.md').read_text(encoding='utf-8-sig'))
report=dict(checks=checks,pass_=all(c['pass_'] for c in checks),count=len(checks),failed=[c['check'] for c in checks if not c['pass_']],scope='Handoff consistency, not causal validity; negative control remains scientific FAIL.')
if '--read-only' not in sys.argv:
    (out/'runs/verification-final.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(pass_=report['pass_'],count=len(checks),failed=report['failed']),ensure_ascii=False))
raise SystemExit(0 if report['pass_'] else 1)
