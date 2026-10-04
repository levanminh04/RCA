"""Offline final artifact checks; never opens locked data or executes a method.

Scientific scope and unresolved findings are separate from technical integrity.
Use a fresh run ID; previous successful and failed runs are retained.
"""
import argparse,ast,csv,datetime,hashlib,json,re,subprocess,sys
from pathlib import Path
import verify_outputs as legacy

R=Path(__file__).resolve().parents[3];B=R/'results/T-003'
TASKS=['T-008','T-009','T-010','T-011','T-012']
def read(p):return json.loads((R/p).read_text(encoding='utf-8-sig'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rel(p):return p.relative_to(R).as_posix()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def main():
    a=argparse.ArgumentParser();a.add_argument('--run',required=True);args=a.parse_args()
    if not re.fullmatch(r'[a-zA-Z0-9_-]+',args.run):raise ValueError('bad run ID')
    out=B/'runs'/args.run;out.mkdir(parents=True,exist_ok=False)
    checks=[];sources=[];source_errors=[];manifests=[]
    for task in TASKS:
        base=R/'results'/task
        for p in sorted((base/'runs').rglob('*manifest.json')):
            # These are source snapshot manifests, not telemetry acquisitions or file catalogs.
            m=json.loads(p.read_text(encoding='utf-8-sig'))
            rows=m.get('sources',m.get('items',[])) if isinstance(m,dict) else []
            if not rows or 'download' in p.parent.name:continue
            if not any(isinstance(x,dict) and x.get('url') for x in rows):continue
            manifests.append(dict(task=task,path=rel(p),sha256=digest(p),revision=m.get('revision',m.get('github_revision')),dataset_revisions=m.get('dataset_revisions',{})))
            for item in rows:
                if not isinstance(item,dict):continue
                row=dict(item,task=task,manifest=rel(p))
                if not all(k in item for k in ('path','bytes','sha256')):
                    source_errors.append(row);continue
                candidates=[(p.parent/item['path']).resolve(),(base/item['path']).resolve(),(R/item['path']).resolve()]
                found=next((q for q in candidates if base in q.parents and q.is_file()),None)
                ok=found is not None and found.stat().st_size==item['bytes'] and digest(found)==item['sha256']
                checks.append(dict(kind='source_hash',path=rel(found) if found else item['path'],ok=ok,manifest=rel(p)))
                if found:row['repository_path']=rel(found)
                sources.append(row)
    unified=dict(stage='approved inspection and bounded source survey',telemetry_read_for_approved_candidates=True,
        bank_measurements_read=False,manifests=manifests,sources=sources,retained_source_failures=source_errors)
    save(B/'source-manifest.json',unified)
    expected={'T-008':2,'T-009':2,'T-010':1,'T-011':2,'T-012':14}
    for task,n in expected.items():
        p=R/'results'/task/'the-dataset.md';t=p.read_text(encoding='utf-8-sig')
        sections={str(i):len(re.findall(r'^## '+str(i)+r'\. ',t,re.M)) for i in range(1,11)}
        checks.append(dict(kind='card_sections',task=task,counts=sections,ok=all(v==n for v in sections.values())))
    for task in ['T-003',*TASKS]:
        for p in (R/'results'/task).glob('*.md'):
            report=legacy.links(p);checks.append(dict(kind='links',**report,ok=not report['missing_local_links']))
        for p in (R/'results'/task/'scripts').glob('*.py'):
            try:ast.parse(p.read_text(encoding='utf-8-sig'));ok=True
            except SyntaxError:ok=False
            checks.append(dict(kind='python_syntax',path=rel(p),ok=ok))
    checks.extend(dict(kind='independent_raw_label_census',**x) for x in legacy.census('T-008')+legacy.census('T-009'))
    for p in ['results/T-009/runs/inspect-004/validation.json','results/T-010/runs/inspect-005/validation.json','results/T-010/runs/inspect-008/validation.json']:
        v=read(p);checks.append(dict(kind='branch_validation',path=p,ok=v['ok']))
    nz=read('results/T-008/runs/units-001/result.json')
    save(out/'nezhaduration-source.json',nz)
    checks.append(dict(kind='nezha_duration_unit',ok=sum(x['rows'] for x in nz['files'])==4180244 and all(x['microsecond_match_within_one_us']==x['rows'] and x['invalid']==x['negative_span_duration']==0 for x in nz['files'])))
    sql=read('results/T-008/runs/independent-check-001/result.json')
    checks.append(dict(kind='nezha_independent_sql_parent',ok=sql['passed'] and len(sql['checks'])==12))
    bands=list(csv.DictReader((R/'results/T-011/cloud-descriptive-bands.csv').open(encoding='utf-8-sig',newline='')))
    balances=True;grouped={}
    for x in bands:
        for segment in ('control','fault'):
            n=int(x[segment+'_n']);e=int(x[segment+'_exceed']);f=x[segment+'_fraction']
            balances &= 0<=e<=n and ((not f and n==0) or (n>0 and abs(float(f)-e/n)<1e-12))
        k=tuple(x[c] for c in ('member','kpi_or_channel','entity_or_feature'))
        grouped.setdefault(k,[]).append(x)
    monotone=True
    for group in grouped.values():
        group.sort(key=lambda x:float(x['q']))
        monotone &= len(group)==3 and all(float(b['band'])>=float(a['band']) and int(b['fault_exceed'])<=int(a['fault_exceed']) and int(b['control_exceed'])<=int(a['control_exceed']) for a,b in zip(group,group[1:]))
    checks.append(dict(kind='lemma_q_numerators_and_monotonicity',rows=len(bands),ok=len(bands)==807 and balances and monotone))
    # Run the safe subset hostile-input and shape checks on the actual current reader.
    c=subprocess.run([sys.executable,'-B',str(R/'results/T-011/scripts/safe_npy.py')],capture_output=True,text=True)
    checks.append(dict(kind='inert_npy_reader_selfcheck',ok=c.returncode==0,stdout=c.stdout,stderr=c.stderr))
    lm=read('results/T-011/runs/validate-001/validation.json')['comparisons']
    cloud=[x for x in lm if x['dataset']=='Cloud_Computing'];pr=[x for x in lm if x['dataset']=='Product_Review']
    checks.append(dict(kind='lemma_kpi_scope_counts',cloud_cases=len(cloud),pr_cases=len(pr),ok=len(cloud)==14 and len(pr)==46 and all(x['missing']==x['mismatches']==0 for x in cloud) and all(x['missing'] or x['mismatches'] for x in pr)))
    linkage=read('results/T-011/runs/validate-003/validation.json')['linkage']
    checks.append(dict(kind='lemma_nonempty_linkage',ok=len(linkage)==2 and all(x['metric_entities'] and x['log_entities'] for x in linkage)))
    resources=read('results/T-003/runs/resources-final-001/summary.json')
    checks.append(dict(kind='download_total',ok=resources['download_bytes']==5477786503))
    # Review repairs: validate current additions instead of relying on old PASS.
    review=read('results/T-003/runs/review-propagation-001/resources.json')
    checks.append(dict(kind='current_payload_and_failure_accounting',ok=review['verified_payload_bytes']==6106198114 and review['logical_member_bytes']==41126769584 and review['retained_failed_download_bytes']==335055240))
    for branch in ['fse-file-inspect-003','anomod-file-inspect-003','anomod-followup-002','trca-inventory-001']:
        v=read('results/T-012/runs/'+branch+'/validation.json');checks.append(dict(kind='new_archive_validation',run=branch,ok=v['ok']))
    fc=read('results/T-012/runs/fse-file-inspect-003/cases.json');valid=[x for x in fc if not x['invalid_marker']]
    checks.append(dict(kind='fse_actual_label_census',ok=len(fc)==10 and len(valid)==8 and len({r for c in valid for r in c['roots']})==11 and len({c['injection']['fault_type'] for c in valid})==8))
    balances=all(sum(p['trace']['parent'].values())==p['trace']['rows'] and all(0<=p['log'][k]<=p['log']['rows'] for k in ('with_trace','trace_matches','span_matches')) for c in fc for p in c['phases'].values())
    checks.append(dict(kind='fse_parent_and_linkage_denominators',ok=balances))
    for branch in ['fse-file-inspect-003','anomod-followup-002']:
        bands=read('results/T-012/runs/'+branch+'/descriptive-bands.json');groups={};ok=True
        for x in bands:
            k=(x['case'],x['channel'],x['entity'],x['feature'],json.dumps(x.get('tags',[]),sort_keys=True));groups.setdefault(k,[]).append(x)
            if x['status']=='descriptive_only':ok &= 0<=x['control_exceed']<=x['control_n'] and 0<=x['fault_exceed']<=x['fault_n'] and x['reference_n']>=2
        for g in groups.values():
            g.sort(key=lambda x:x['q']);ok &= len(g)==3
            if g[0]['status']=='descriptive_only':ok &= all(b['band']>=a['band'] and b['fault_exceed']<=a['fault_exceed'] and b['control_exceed']<=a['control_exceed'] for a,b in zip(g,g[1:]))
        checks.append(dict(kind='review_bands_numerators_q',run=branch,rows=len(bands),ok=ok))
    trca=read('results/T-012/runs/trca-reuse-001/result.json');checks.append(dict(kind='trca_full_input_reuse',ok=trca['csv_files']==trca['exact_nezha_matches']==1165 and len(trca['labels'])==4 and all(x['same_bytes'] for x in trca['labels'])))
    bank=list(csv.DictReader((R/'results/T-012/runs/bank-label-reproduce-002/record.csv').open(encoding='utf-8-sig')))
    checks.append(dict(kind='bank_label_only_independent_census',ok=len(bank)==136 and len({x['component'] for x in bank})==14 and len({x['reason'] for x in bank})==8 and len({x['datetime'][:10] for x in bank})==9 and len({(x['component'],x['reason']) for x in bank})==52))
    leak=read('results/T-008/runs/sampling-leakage-001/result.json');checks.append(dict(kind='nezha_injection_conditioned_inventory',ok=len(leak['groups'])==4 and all(m['matches'] for g in leak['groups'] for m in g['modalities'].values())))
    for p in ['results/T-012/runs/download-review-001/manifest.json','results/T-012/runs/download-review-002/manifest.json']:
        for item in read(p)['items']:
            if item['status']!='ok':continue
            data=R/'data/ngoai-rcaeval/T-012'/item['path'];actual=digest(data);checks.append(dict(kind='local_new_payload_hash',path=str(data.relative_to(R)),ok=data.stat().st_size==item['actual_bytes'] and actual==item['sha256']))
    records=[]
    for task in ['T-003',*TASKS]:
        for p in sorted((R/'results'/task).rglob('*')):
            if p.is_file() and out not in p.parents and '__pycache__' not in p.parts:
                records.append(dict(path=rel(p),bytes=p.stat().st_size,sha256=digest(p)))
    save(out/'artifact-manifest.json',dict(files=records,source_manifest_sha256=digest(B/'source-manifest.json')))
    report=dict(ok=all(x['ok'] for x in checks),technical_integrity_only=True,checks=checks,
        scientific_scope=['Nezha four released days all CSV plus selection leakage audit','Eadro two ZIP including all nested members','Deep raw/normal/graph plus conditional all-log and fault catalog','LEMMA two preprocessed dates only; Original metadata','2025–2026 bounded source survey plus full AnoMod/TRCA/FSE reduced archives; Bank label/metadata only'],
        remaining_research_limits=['license/source conflicts','injection not independently verified onset','missing root/region/trace labels vary by corpus','Bank file quality and independence of injector/collector unverified','LEMMA Original and other dates not inspected'],
        package_closed=False,reviewer='Claude merged T-003; Minh decides closure',created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    save(out/'verification.json',report)
    print(json.dumps(dict(ok=report['ok'],checks=len(checks),failed=[x for x in checks if not x['ok']],source_snapshots=len(sources),retained_source_failures=len(source_errors),artifacts=len(records)),ensure_ascii=False))
    raise SystemExit(0 if report['ok'] else 1)
if __name__=='__main__':main()
