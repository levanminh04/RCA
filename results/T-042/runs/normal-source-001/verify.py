"""Output/file-set verification and read-only final seal; no telemetry/method calls."""
import sys, json, gzip, math, hashlib, subprocess, re
from pathlib import Path
R=Path('D:/RCA-flashticket');B=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):
    p=Path(p)
    with (gzip.open(p,'rt',encoding='utf-8') if p.suffix=='.gz' else p.open(encoding='utf-8-sig')) as f:return json.load(f)
def output(p,v):
    with Path(p).open('x',encoding='utf-8') as f:json.dump(v,f,ensure_ascii=False,indent=2);f.write('\n')
CONTROLS=['docs/DECISIONS.md','docs/WHY.md','docs/STATE.md','tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md']
def check():
    before=read(B/'before.json');checks={};bad=[]
    for p,h in before['old_results'].items():
        if sha(R/p)!=h['sha256']:bad.append(p)
    assert not bad,bad;checks['old_results_unchanged']=len(before['old_results'])
    for p,h in before['control_before'].items():
        if p not in CONTROLS:assert sha(R/p)==h['sha256'],p
    checks['unrelated_controls_unchanged']=True
    for p in ('docs/DECISIONS.md','docs/WHY.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md'):
        assert (R/p).read_bytes().startswith((B/'before'/p).read_bytes()),p
    old=(B/'before/docs/STATE.md').read_bytes().decode('utf-8');new=(R/'docs/STATE.md').read_bytes().decode('utf-8')
    remove=lambda s:''.join(x for x in s.splitlines(keepends=True) if not x.startswith('- **T-042 '))
    assert remove(old)==remove(new)
    old=(B/'before/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md').read_text(encoding='utf-8-sig');new=(R/'tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md').read_text(encoding='utf-8-sig')
    o=next(x for x in old.splitlines() if x.startswith('- **Trạng thái:**'));n=next(x for x in new.splitlines() if x.startswith('- **Trạng thái:**'))
    assert new.split('## Bổ sung đã được Minh duyệt',1)[0].strip()==old.replace(o,n,1).strip()
    checks['only_approved_control_edits']=True
    parsed=0
    for p in B.rglob('*'):
        if p.is_file() and (p.suffix=='.json' or p.name.endswith('.json.gz')):read(p);parsed+=1
        if p.is_file() and p.suffix=='.py':compile(p.read_text(encoding='utf-8-sig'),str(p),'exec')
    checks['json_parsed']=parsed
    frozen=read(B/'full-001/diagnoses-frozen.json');assert frozen['completed'] and len(frozen['records'])==66 and not frozen['labels_read']
    counts={};baselines=0
    for row in frozen['records']:
        p=R/row['path'];assert sha(p)==row['sha256'];v=read(p);assert not v['labels_read'] and not v['raw_payload_saved']
        assert v['status']=='OK';counts[v['method']]=counts.get(v['method'],0)+1
        assert sha(R/v['baseline']['path'])==v['baseline']['sha256'];baselines+=1
    assert counts=={'M4':22,'MAIN':22,'MICRO':22};checks['frozen_records_and_baselines_checked']=66
    e=read(B/'evaluate-003/evaluation.json');assert e['independent_metrics']=='PASS' and len(e['cases'])==66
    for method in counts:
        for side in ('old','normal_source'):
            rows=[x[side] for x in e['cases'] if x['method']==method];s=e['summary'][method][side]
            for key,src in [('hit@1','hit@1'),('mrr','rr'),('native_hit1','native_hit1'),('native_mrr','native_mrr')]:
                assert math.isclose(s[key],sum(x[src] for x in rows)/22,rel_tol=1e-14,abs_tol=0)
    assert e['summary']['M4']['normal_source']['trang_thai']['NO_EVIDENCE']==2
    checks['paired_summaries_checked']=True
    m=read(B/'mechanism-summary.json');assert m['M4']['usable_metric_before']==3630 and m['M4']['usable_metric_after']==0
    assert m['MAIN']['native_CPU_network_fallback_pools']==440 and m['MAIN']['fallback_alert_counts']=={'0':440}
    assert m['MICRO']['partition_counts_changed']==22
    f=read(B/'F2-stable-001/summary.json');assert f['case_channel_pairs']==3630 and f['input_counts_times_minmax_match_old'] and f['all_normalized_within_Cauchy_bound']
    assert f['max_abs_delta_over_std']<=math.sqrt(5)*(1+1e-14)
    checks['mechanism_and_stable_F2_checked']=True
    for name in ('prepare-001','fixtures-001','pilot-001','full-001'):
        assert read(B/name/'invocation.json')['script_sha256']==sha(B/'run.py')
        assert sha(B/name/'source-at-start.py')==sha(B/'run.py')
    assert read(B/'evaluate-003/invocation.json')['script_sha256']==sha(B/'evaluate.py')
    checks['actual_run_scripts_match_snapshots']=True
    # All referenced published comparison files still match their owner manifests.
    m34=read(R/'results/T-034/runs/manifest-cuoi-007/manifest.json');pin34={x['path']:x for x in m34['files']}
    p='results/T-034/bang-baseline.json';assert sha(R/p)==pin34[p]['sha256']
    sources=read(R/'results/T-042/nguon.json');relevant=[x for x in sources['checks'] if isinstance(x,dict) and 'path' in x and (str(x['path']).endswith('so-cong-bo.csv') or str(x['path']).endswith('fse26-pages.txt'))]
    for x in relevant:
        p=Path(x['path']);p=p if p.is_absolute() else R/p
        expected=x.get('expected_sha256',x.get('sha256'));assert expected and sha(p)==expected,x
    checks['T034_baseline_pin_checked']=True;checks['additional_publication_checks_from_T042']=len(relevant)
    diff=subprocess.run(['git','diff','--check'],cwd=R,capture_output=True,text=True,encoding='utf-8')
    assert diff.returncode==0,diff.stdout+diff.stderr;checks['git_diff_check']='PASS'
    checks['new_output_bytes_before_seal']=sum(p.stat().st_size for p in B.rglob('*') if p.is_file());assert checks['new_output_bytes_before_seal']<20_000_000
    checks['status']='PASS';checks['no_method_or_raw_data_read']=True
    folder=B/'verification-001';folder.mkdir(exist_ok=False);output(folder/'checks.json',checks)
    print(json.dumps(checks,ensure_ascii=False))
def seal():
    m=read(B/'manifest.json')
    for x in m['files']:
        p=R/x['path'];assert p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],x['path']
    for p,h in m['controls'].items():assert sha(R/p)==h['sha256'],p
    found={p.relative_to(R).as_posix() for p in B.rglob('*') if p.is_file() and p!=B/'manifest.json'}
    assert found=={x['path'] for x in m['files']}
    assert sum((R/x['path']).stat().st_size for x in m['files'])+(B/'manifest.json').stat().st_size<=20_000_000
    assert read(B/'verification-001/checks.json')['status']=='PASS'
    print(json.dumps(dict(status='PASS',sealed_files=len(m['files']),bytes_including_manifest=sum((R/x['path']).stat().st_size for x in m['files'])+(B/'manifest.json').stat().st_size,controls_checked=len(m['controls']),state='awaiting_review_not_accepted'),ensure_ascii=False))
if __name__=='__main__':
    {'check':check,'seal':seal}[sys.argv[1]]()
