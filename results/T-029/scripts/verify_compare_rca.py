"""Independent inspection of G source records, grouping, seed means and deltas."""
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
import time

import bocpd_features as bf
from p3.danh_gia import cham_ca

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def main():
    bf.audit('Lệnh có ghi: T014-main Python -B -W ignore verify_compare_rca.py; kiểm output G đã ghi, không chạy ranker.')
    start = time.perf_counter()
    output = read(bf.OUT / 'a-so-b.json')
    a = read(bf.ROOT / 'results/T-024/cham-a.json')
    b = read(bf.ROOT / 'results/T-025/cham-b.json')
    groups = read(bf.ROOT / 'results/T-025/cham/phan-tich-b.json')['theo_ca']
    ids = sorted(c['opaque_id'] for c in read(bf.ROOT / 'results/T-022/allowlist-dev.json')['cases'])
    metrics = ('hit@1', 'hit@5')
    point_names = ('a', 't_hat_plus', 't_hat')
    bkeys = {'baro':'baro:native', 'circa_ols_rht':'circa:ols+rht',
             'circa_ols_da':'circa:ols+rht_da', 'torai_B':'torai_B'}
    checks, failures = [], []
    def check(name, actual, expected, numeric=False):
        okay = math.isclose(actual, expected, abs_tol=1e-12, rel_tol=0) if numeric else actual == expected
        checks.append({'name':name,'pass':okay})
        if not okay:
            failures.append({'name':name,'actual':sorted(actual) if isinstance(actual,set) else actual,
                             'expected':sorted(expected) if isinstance(expected,set) else expected})
    def aggregate(table, rows, prefix):
        check(prefix+'/n',table['n'],len(rows))
        check(prefix+'/ids',set(table['case_ids']),{r['opaque_id'] for r in rows})
        for p in point_names:
            for k in metrics:
                expected = sum(r['points'][p][k] for r in rows)/len(rows) if rows else None
                check(prefix+'/'+p+'/'+k,table['points'][p][k],expected,numeric=bool(rows))
        for delta in ('a_to_tplus','tplus_to_first'):
            for k in metrics:
                expected = sum(r['signed_deltas'][delta][k] for r in rows)/len(rows) if rows else None
                check(prefix+'/'+delta+'/'+k,table['signed_deltas'][delta][k],expected,numeric=bool(rows))
    for path, expected in output['source_hashes'].items():
        check('sourceSHA/'+path,bf.digest(bf.ROOT/path),expected)
    check('row_count',output['row_count'],240)
    check('frozenchecks',len(output['verification']['checks']),960)
    check('frozenmismatches',output['verification']['mismatches'],0)
    row_count = 0
    high_counts, non_ok = {}, Counter()
    for det, methods in output['by_detector'].items():
        for method, table in methods.items():
            rows = table['per_case']; prefix = det+'/'+method
            row_count += len(rows)
            check(prefix+'/ids',sorted(r['opaque_id'] for r in rows),ids)
            for row in rows:
                oid = row['opaque_id']; key = prefix+'/'+oid
                th = row['t_hat']; inj = row['t_hat_plus']-row['t_hat_plus_index']+720
                expected_group = 'S' if th >= inj else 'E-gần' if groups[oid][det]['A_chua_moc'] else 'E-xa'
                check(key+'/group',row['group'],expected_group)
                check(key+'/A_chua_moc',row['A_chua_moc'],groups[oid][det]['A_chua_moc'])
                for p in point_names:
                    point = row['points'][p]
                    seeds = point['per_seed']
                    check(key+'/'+p+'/seedset',set(seeds),{'0','1','2'} if method=='torai_B' else {'single'})
                    for seed, val in seeds.items():
                        record = read(bf.ROOT / val['source_record'])
                        scored = cham_ca(record,row['root'])
                        check(key+'/'+p+'/'+seed+'/status',val['status'],record['status'])
                        check(key+'/'+p+'/'+seed+'/oid',record['opaque_id'],oid)
                        if p != 'a': check(key+'/'+p+'/'+seed+'/detector',record['detector'],det)
                        if record['status']!='OK': non_ok[det+'/'+method+'/'+p]+=1
                        for k in metrics:
                            check(key+'/'+p+'/'+seed+'/'+k,val[k],scored[k])
                            if record['status']!='OK': check(key+'/'+p+'/'+seed+'/'+k+'/nonOKzero',val[k],0.)
                        nodes = (record.get('diagnostics') or {}).get('nodes') or {}
                        high = sorted(n for n,v in nodes.items() if float(v.get('rht_score',0))>1e10)
                        check(key+'/'+p+'/'+seed+'/highnodes',val['circa_nodes_gt_1e10'],high)
                    for k in metrics:
                        mean = sum(v[k] for v in seeds.values())/len(seeds)
                        check(key+'/'+p+'/'+k+'/seedmean',point[k],mean,numeric=True)
                        if p=='a': check(key+'/'+p+'/'+k+'/frozen',point[k],a['methods'][method]['per_case'][oid][k])
                        if p=='t_hat': check(key+'/'+p+'/'+k+'/frozen',point[k],b['theo_bo_phat_hien'][det][bkeys[method]]['ca'][oid][k])
                    check(key+'/'+p+'/highflag',point['circa_any_node_gt_1e10'],any(v['circa_nodes_gt_1e10'] for v in seeds.values()))
                for k in metrics:
                    check(key+'/windowdelta/'+k,row['signed_deltas']['a_to_tplus'][k],row['points']['t_hat_plus'][k]-row['points']['a'][k])
                    check(key+'/eventdelta/'+k,row['signed_deltas']['tplus_to_first'][k],row['points']['t_hat'][k]-row['points']['t_hat_plus'][k])
                if method=='torai_B':
                    for seed in ('0','1','2'):
                        for k in metrics:
                            d=row['signed_deltas_by_seed'][seed]
                            check(key+'/'+seed+'/windowdelta/'+k,d['a_to_tplus'][k],row['points']['t_hat_plus']['per_seed'][seed][k]-row['points']['a']['per_seed'][seed][k])
                            check(key+'/'+seed+'/eventdelta/'+k,d['tplus_to_first'][k],row['points']['t_hat']['per_seed'][seed][k]-row['points']['t_hat_plus']['per_seed'][seed][k])
            aggregate(table['all30'],rows,prefix+'/all30')
            for field, tablekey in (('cell','by_cell'),('group','by_event_group')):
                check(prefix+'/'+tablekey+'/keys',set(table[tablekey]),{r[field] for r in rows})
                for group, agg in table[tablekey].items(): aggregate(agg,[r for r in rows if r[field]==group],prefix+'/'+tablekey+'/'+group)
            if method=='torai_B':
                for seed, agg in table['by_seed_on_30_cases'].items():
                    perseed=[{**r,'points':{p:r['points'][p]['per_seed'][seed] for p in point_names},'signed_deltas':r['signed_deltas_by_seed'][seed]} for r in rows]
                    aggregate(agg,perseed,prefix+'/seed'+seed)
            if method.startswith('circa'):
                c=table['circa_threshold']; high_counts[prefix]={}
                check(prefix+'/threshold',c['threshold'],1e10)
                for p in point_names:
                    expected=[r['opaque_id'] for r in rows if r['points'][p]['circa_any_node_gt_1e10']]
                    check(prefix+'/'+p+'/highids',c['high_case_ids_by_point'][p],expected)
                    check(prefix+'/'+p+'/highcount',c['high_count_by_point'][p],len(expected))
                    high_counts[prefix][p]=len(expected)
                paired=[r for r in rows if all(not r['points'][p]['circa_any_node_gt_1e10'] for p in point_names)]
                aggregate(c['paired_no_node_exceeds_at_any_point'],paired,prefix+'/paired')
                check(prefix+'/paired_bycell/keys',set(c['paired_by_cell']),{r['cell'] for r in paired})
                for cell, agg in c['paired_by_cell'].items(): aggregate(agg,[r for r in paired if r['cell']==cell],prefix+'/paired/'+cell)
    check('actual_rows',row_count,240)
    result={'status':'FAIL' if failures else 'PASS','rows':row_count,'source_files_checked':len(output['source_hashes']),
            'checks':checks,'check_count':len(checks),'mismatch_count':len(failures),'mismatches':failures,
            'circa_high_counts_by_point':high_counts,'nonOK_records':dict(non_ok),'seconds':time.perf_counter()-start,
            'script_sha256':bf.digest(__file__),'output_sha256':bf.digest(bf.OUT/'a-so-b.json'),
            'method':'Reads source records anew; checks scores, seed aggregation, frozen numbers, signed deltas, partitions and node thresholds. Does not call compare_rca.'}
    bf.write_json(bf.OUT/'runs/compare-rca-001/verification.json',result)
    print(json.dumps({k:result[k] for k in ('status','rows','source_files_checked','check_count','mismatch_count','seconds')}))
    if failures: raise RuntimeError('G independent checks failed; preserve output and report')

if __name__=='__main__':
    try: main()
    except Exception as e:
        bf.audit('DỪNG verify_compare_rca.py: '+type(e).__name__+': '+str(e)+'; giữ output và báo root.')
        raise
