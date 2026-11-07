"""T13: chấm bản gọn đã seal và hợp nhất các nguồn kiểm hợp lệ."""
import copy
import gzip
import json
import time
from collections import Counter
from fractions import Fraction

from common import ROOT, RUN, digest, dump, pin, read, save, timing
from bang_doc_lap import exact_score
from thong_ke import counts
from m1 import doi_chung
from m1_danh_gia import pha2
from p3 import danh_gia


def groups(blocks):
    return [b['groups'] for b in blocks]


def main():
    start = time.perf_counter()
    seal = read(RUN / 'prepared-seal.json')
    pin(seal['output']['path'], seal['output'])
    # Chỉ đọc nhãn sau kiểm seal trên.
    previous = pha2.giai_ma_json(read('results/T-052/ket-qua-dev-doc-lap-001.json'))
    labels = previous['labels']
    regions = read('results/T-052/vung-ce-va-vi-tri-001.json')
    pos = {r['opaque_id']: r for r in regions['real']}
    tables = {w: {d: copy.deepcopy(previous['worlds'][w][d]['per_case']) for d in ('RE2-TT','Nezha-OB')}
              for w in ('P','S_lo','S_hi')}
    raw_controls = read('results/T-050/doi-chung-003.json')
    m52 = read('results/T-052/manifest.json')
    pin('results/T-050/doi-chung-003.json', next(r for r in m52['upstream_inputs_verified'] if r['path'] == 'results/T-050/doi-chung-003.json'))
    source_controls = {r['opaque_id']: r for r in raw_controls['rows']}
    m51 = read('results/T-051/manifest.json')
    record_map, proofs = {}, []
    with gzip.open(ROOT / seal['output']['path'], 'rt', encoding='utf-8') as stream:
        for line in stream:
            package = json.loads(line)
            j, name, rec = package['job'], package['configuration'], package['record']
            oid, ds = j['opaque_id'], j['dataset']
            if j['window'] != 'that': continue
            record_map[name, oid] = rec
            for w in tables:
                r = dict(rec, blocks=rec['worlds'][w]['blocks'])
                scored = exact_score(r, labels[oid]['root'])
                if name in tables[w][ds]:
                    assert scored['RR'] == tables[w][ds][name][oid]['RR'], (name, oid, w)
                tables[w][ds].setdefault(name, {})[oid] = scored
                if name == 'M1':
                    tables[w][ds].setdefault('T12-on', {})[oid] = exact_score(
                        dict(status=rec['status'], blocks=rec['T12_on'][w]['blocks']), labels[oid]['root'])
            if name != 'M1': continue
            for ctrl, r in rec['controls'].items():
                # Trạng thái gốc giữ nguyên; lỗi/không hỗ trợ không bị bỏ khỏi mẫu số.
                tables['P'][ds].setdefault(ctrl, {})[oid] = exact_score(
                    {'status': r['trang_thai'], 'blocks': r['blocks']}, labels[oid]['root'])
            ctrl = source_controls[oid]
            rankings, sources = {}, {}
            for method, ref in ctrl['sources'].items():
                pin(ref['path'], ref)
                r = read(ref['path'])
                sources[method] = r
                rankings[method] = None if r['status'] == 'ERROR' else [g for b in danh_gia.khoi_tu_ban_ghi(r) for g in b['groups']]
            cc = doi_chung.cc(rankings)
            simple = sources['simplerca']
            votes = {r['entity']: int(r['key'][0]) for r in simple['entity_ranking']}
            cg = doi_chung.cg(votes, rankings['simplerca'], [tuple(e) for e in rec['extra']['canh']])
            for ctrl_name, new in (('C-c',cc),('C-g',cg)):
                old = ctrl[ctrl_name]
                assert new['trang_thai'] == old['trang_thai'] and dump(new['blocks']) == dump(old['blocks']), (oid,ctrl_name)
                tables['P'][ds].setdefault(ctrl_name,{})[oid] = exact_score(
                    {'status': new['trang_thai'], 'blocks': new['blocks']}, labels[oid]['root'])
            proofs.append({'opaque_id': oid, 'graph': 'prepared M1 N-union-A, T12 off',
                           'C-c_blocks_exact': True, 'C-g_blocks_exact': True})
    output, mechanisms = {}, []
    for w, datasets in tables.items():
        output[w] = {}
        for ds, table in datasets.items():
            n = 30 if ds == 'RE2-TT' else 22
            assert all(len(r) == n for r in table.values())
            cells = {o: labels[o]['cell'] for o in table['M1']}
            bootstrap = danh_gia.bootstrap(table, cells)
            summary = {name: {'n':len(rows),'MRR':sum((r['RR'] for r in rows.values()),Fraction(0))/n,
                       'metrics':{k:sum(r[k] for r in rows.values())/n for k in danh_gia.DO_DO_BOOT},
                       'status':Counter(r['status'] for r in rows.values())} for name,rows in table.items()}
            pairs = {}
            for name, rows in table.items():
                if name == 'M1':continue
                a,b={o:r['RR'] for o,r in table['M1'].items()},{o:r['RR'] for o,r in rows.items()}
                delta={o:a[o]-b[o] for o in a}
                pairs[name]={'mean_delta':sum(delta.values())/n,'delta_RR':delta,'counts':counts(delta,cells,a,b)}
            stratified={}
            for field in ('fault','cell','N_position_p75','N_position_p90'):
                values={o:(pos[o][field]['group'] if field.startswith('N_') else labels[o][field]) for o in cells}
                stratified[field]={}
                for group in sorted(set(values.values())):
                    chosen=[o for o in values if values[o]==group]
                    stratified[field][group]={name:{'n':len(chosen),'MRR':sum((r[o]['RR'] for o in chosen),Fraction(0))/len(chosen)} for name,r in table.items()}
            output[w][ds]={'summary':summary,'pairs_M1_minus':pairs,'bootstrap':bootstrap,
                           'groups':stratified,'per_case':table}
            if w == 'P':
                for name in ('bo-E1','bo-E2','bo-E5','C-a0','C-a1'):
                    for oid,delta in pairs[name]['delta_RR'].items():
                        if delta == 0:continue
                        base,other=record_map['M1',oid],record_map[name,oid]
                        root=labels[oid]['root']
                        candidates=[o for o,d in pairs[name]['delta_RR'].items() if d>=0 and o!=oid and
                                    labels[o]['fault']==labels[oid]['fault'] and labels[o]['root']==root]
                        good=sorted(candidates)[0] if delta<0 and candidates else None
                        mechanisms.append({'configuration':name,'opaque_id':oid,'dataset':ds,'delta_RR':delta,
                          'root':root,'matched_control_same_root_fault':good,
                          'M1_root_channels':[k for k in base['extra']['kenh_co'] if k['thuc_the']==root],
                          'other_root_channels':[k for k in other['extra']['kenh_co'] if k['thuc_the']==root],
                          'M1_tier':base['extra']['tang_P'].get(root),'other_tier':other['extra']['tang_P'].get(root),
                          'M1_top_blocks':base['blocks'][:3],'other_top_blocks':other['blocks'][:3],
                          'limit':'Mô tả can thiệp tính toán; không xác nhận nguyên nhân vật lý hoặc triệt tiêu nhiễu.'})
    save(ROOT/'results/T-052/ket-qua-dev.json',{'status':'DEV_T13_SCORED_NOT_G3_APPROVED',
         'worlds':output,'labels':labels,'controls_graph_parity':proofs,'mechanism_traces':mechanisms,
         'regions_ce_source':'results/T-052/vung-ce-va-vi-tri-001.json',
         'prepared_seal':{'path':'results/T-052/runs/trien-khai-001/prepared-seal.json','sha256':digest(RUN/'prepared-seal.json')},
         'scope':{'P':'six baselines, M1, three ablations, C-a0/a1, C-d1/2/3, C-c/C-g, T12-on',
                  'S_lo_S_hi':'M1, three ablations, C-a0/a1, T12-on and fixed baseline results; C-d/C-c/C-g only P'},
         'source_control_limit':'C-d3 OB chỉ giữ mô tả lịch sử NO_TARGET; không có lượt C-d3 mới trên OB.'})
    save(RUN/'score-all-summary.json',timing('score_all',start,PASS=True,real_cases=52,
         native_windows=82,prepared_records=492,graph_control_checks=len(proofs),bootstrap_B=10000,seed=20261005))


if __name__=='__main__':main()
