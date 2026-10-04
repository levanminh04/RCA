"""Saved-output validation with independent count/rate/raw-band checks. No network."""
import argparse, collections, csv, hashlib, json, math, pathlib, re, sys
import numpy as np
import pandas as pd
from acquire import ROOT, OUT, DATA, dump, hashcheck
from build_card import HEADINGS

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--read-only',action='store_true');args=parser.parse_args()
    checks={};details={}
    load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
    plan=load(OUT/'download-plan.json');summary=load(OUT/'census-summary.json');source=load(OUT/'sources-audit/ss-summary.json')
    checks['source_metadata_pages_and_hashes']=all(x['valid'] for x in load(OUT/'input-metadata-check.json')['checks'])
    checks['all_618_SS_files_hash_size_match']=all(hashcheck((DATA/e['path']).read_bytes(),e)['valid'] for e in plan['files']) and len(plan['files'])==618
    census=pd.read_csv(OUT/'census-cases.csv');cells=pd.read_csv(OUT/'census-cells.csv')
    checks['census_case_key_unique']=not census.duplicated(['dataset','root','fault','repetition']).any()
    checks['census_sum_all_dimensions']=all(int(cells[cells.dataset==s['dataset']].cases.sum())==s['cases']==len(census[census.dataset==s['dataset']]) for s in summary)
    other=pd.read_csv(OUT/'sources-audit/ss-census.csv')
    checks['independent_census_all_case_names_equal']=set(census['case'])==set(other['case'])
    checks['inventory_no_trace_all_three_SS']=int(census.trace.sum())==0 and all(s['trace_cases']==0 for s in summary)
    cases=load(OUT/'inspection/cases.json');checks['actual_all_245_cases_read']=len(cases)==len(census)==245
    checks['root_parent_runtime_unclaimed']=load(OUT/'inspection/manifest.json')['parent_resolution'] is None and load(OUT/'inspection/manifest.json')['runtime_root_degrees'] is None
    bounds=pd.read_csv(OUT/'inspection/boundaries.csv');bb=bounds[(bounds.modality=='metric')&(bounds.dataset!='RE1-SS')]
    checks['actual_120_symmetric_metric_windows']=(len(bb)==120 and (bb.start_minus_injection==-720).all() and (bb.end_minus_injection==720).all() and (bb.pre_rows==720).all() and (bb.post_rows==721).all())
    qa=load(OUT/'sources-audit/label-audit.json');labels=next(v for v in qa.values() if isinstance(v,list) and v and isinstance(v[0],dict) and 'case' in v[0])
    checks['eight_label_files_seven_unique']=len(labels)==8 and len({x['sha256'] for x in labels})==7 and all(x['hash_matches_tree'] for x in labels)
    checks['one_detail_label_outside_own_log']=sum(not x['indicator_time_in_log_window'] for x in labels)==1 and sum(x['service_message_matches']==1 for x in labels)==7
    e=pd.read_csv(OUT/'inspection/entity-rates.csv');e=e[(~e.is_root)&e.control_rate.notna()&e.post_rate.notna()]
    p=e.groupby(['dataset','case','group','q'],as_index=False).agg(control_mean=('control_rate','mean'),post_mean=('post_rate','mean'),services_increased=('difference',lambda x:int((x>0).sum())))
    q=p.groupby(['dataset','group','q'],as_index=False).agg(cases=('case','nunique'),control_mean=('control_mean','mean'),post_mean=('post_mean','mean'),cases_any_increase=('services_increased',lambda x:int((x>0).sum())))
    saved=pd.read_csv(OUT/'inspection/probe-summary.csv');merged=q.merge(saved,on=['dataset','group','q'],suffixes=('_actual','_saved'),validate='one_to_one')
    checks['probe_summary_reaggregates_exact_counts_and_rates']=len(merged)==len(saved) and all(np.allclose(merged[c+'_actual'],merged[c+'_saved'],rtol=1e-12,atol=1e-12) for c in ['cases','control_mean','post_mean','cases_any_increase'])
    bands=pd.read_csv(OUT/'inspection/channel-bands.csv');raw_check=[]
    for family in ['RE2-SS','RE3-SS']:
        c=next(x for x in cases if x['dataset']==family);m=pd.read_parquet(DATA/c['case']/'metrics.parquet').sort_values('time');pre=m[m.time<c['injection']];ref=pre.iloc[:2*len(pre)//3];ctrl=pre.iloc[2*len(pre)//3:];post=m[m.time>=c['injection']]
        b=bands[bands.case==c['case']]
        for row in b.itertuples():
            vals=ref[row.metric].to_numpy(dtype=float);vals=vals[np.isfinite(vals)]
            med=float(np.median(vals));width=float(np.quantile(np.abs(vals-med),row.q))
            vc=ctrl[row.metric].to_numpy(dtype=float);vp=post[row.metric].to_numpy(dtype=float)
            ok=(math.isclose(med,row.center,rel_tol=1e-12,abs_tol=1e-12) and math.isclose(width,row.band,rel_tol=1e-12,abs_tol=1e-12) and int(((np.abs(vc-med)>width)&np.isfinite(vc)).sum())==row.control_exceed and int(((np.abs(vp-med)>width)&np.isfinite(vp)).sum())==row.post_exceed)
            raw_check.append(ok)
    checks['raw_two_family_all_channel_bands_and_counts']=all(raw_check);details['raw_band_sets_checked']=len(raw_check)
    checks['finite_rates_bounded']=bands[['control_rate','post_rate']].stack().dropna().between(0,1).all() and saved[['control_mean','post_mean']].stack().dropna().between(0,1).all()
    checks['undefined_channel_rates_only_with_zero_denominator']=all(((bands[rate].isna())==(bands[denom]==0)).all() for rate,denom in [('control_rate','control_valid'),('post_rate','post_valid')])
    checks['lineage_all_checks_pass']=load(OUT/'lineage/verification.json')['all_pass']
    ledger=pd.read_csv(OUT/'so-ca-da-nhin.csv',keep_default_na=False);ls=load(OUT/'ledger-summary.json')
    checks['ledger_total_unique_and_inspection_exposure']=len(ledger)==ls['total_rows']==1245 and not ledger.duplicated(['source','case','public_family','public_case']).any() and ls['T019_inspected_cases']==335
    main_source=load(OUT/'runner-source/manifest.json');raw=(OUT/'runner-source/main.py').read_bytes()
    checks['official_runner_blob_verified']=main_source['valid'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==main_source['git_blob']
    # Received payload sizes from each disjoint network manifest, no estimated totals.
    sourcebytes=sum(load(OUT/'sources-audit'/f)['total_bytes'] for f in ['network-manifest.json','architecture-manifest.json','diagram-metadata-manifest.json'])+load(OUT/'sources-audit/diagram-manifest.json')['bytes']
    net=load(OUT/'acquisition/manifest.json')['network_bytes']+load(OUT/'lineage/download-manifest.json')['network_bytes']+sourcebytes+main_source['network_bytes']
    checks['network_payload_below_1GB']=net<=1_000_000_000;details['received_payload_bytes']=net
    card=(OUT/'the-sock-shop.md').read_text(encoding='utf-8')
    checks['card_two_release_blocks_each_ten_sections']=all(card.count('### '+str(i)+'. '+h)==2 for i,h in enumerate(HEADINGS,1))
    checks['card_nine_criteria_each_release']=all(card.count('| '+str(i)+'. ')==2 for i in range(1,10))
    checks['required_four_files_exist']=all((OUT/x).is_file() for x in ['the-sock-shop.md','so-ca-da-nhin.csv','dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md'])
    checks['all_current_JSON_parse']=True
    for f in OUT.rglob('*.json'):load(f)
    links=re.findall(r'\[[^\]]*\]\(([^)]+)\)',card)
    checks['card_local_links_exist']=all((OUT/x).exists() for x in links if not x.startswith(('https:','http:')))
    checks['old_reused_source_snapshots_unchanged']=all(hashlib.sha256(pathlib.Path(x['path']).read_bytes()).hexdigest()==x['sha256'] for x in load(OUT/'input-metadata-check.json')['checks'])
    checks['STATE_initial_other_bytes_preserved']=load(OUT/'state-start.json')['other_bytes_preserved']
    if (OUT/'state-finish.json').exists():checks['STATE_final_other_bytes_preserved']=load(OUT/'state-finish.json')['other_bytes_preserved']
    result={'checks':{k:bool(v) for k,v in checks.items()},'details':details,'all_pass':all(checks.values()),'limits':'No RCA/detector/network or locked data accessed by this verifier.'}
    if not args.read_only:dump(OUT/'final-checks.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2));assert result['all_pass']

if __name__=='__main__':main()
