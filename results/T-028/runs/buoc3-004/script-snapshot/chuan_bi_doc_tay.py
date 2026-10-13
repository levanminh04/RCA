"""Prepare source-linked excerpts for human/agent reading, without assigning labels."""
import argparse
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]

def read(p):return json.loads((ROOT/p).read_text(encoding='utf-8'))

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);a=p.parse_args()
    run=ROOT/'results/T-028/runs'/a.run_id
    output=run/'manual-excerpts.json'
    if output.exists():raise RuntimeError('Preserve prior excerpts; do not overwrite')
    selected=read(str((run/'manual-selection.json').relative_to(ROOT)))
    out=[]
    for item in selected:
        r=item['row'];ev=r['evidence'];agg=read(ev['source']['path'])['aggregate']
        split=ev['native_trace_split'];ss={}
        for sid,s in ev['seed_evidence'].items():
            rec=read(s['source']['path'])
            ancestors=set(s['ancestors']['value'] or [])
            before=set(s['certain_before_root'] or [])
            callers=sorted(ancestors & before)
            ss[sid]={
                'status':s['status'],'source':s['source'],
                'O':s['ranking']['O'],'R':s['ranking']['R'],
                'root_key':s['ranking']['entity_keys'].get(r['root']),
                'root_p1':s['ranking']['p_by_k'].get('1',{}).get(r['root']),
                'root_p5':s['ranking']['p_by_k'].get('5',{}).get(r['root']),
                'by_k':s['by_k'],'ancestors':s['ancestors'],
                'certain_before_root':s['certain_before_root'],
                'M5_matching_callers':{e:{'relation':s['caller_relation'][e],
                        'key':s['ranking']['entity_keys'].get(e),
                        'trace':agg['trace_'+split].get(e),
                        'simple_votes':agg['simple_entity_max'].get(e)} for e in callers},
                'CIRCA_root_nodes':s['CIRCA_root_nodes'],
                'CIRCA_full_key':s['ranking']['entity_keys'].get(r['root']),
                'TORAI_root_blocks':s['TORAI_root_blocks'],
                'TORAI_diagnostics':s['native_diagnostics'],
                'root_native_items':[v for v in rec['ranking'] if v['entity']==r['root']],
                'record_diagnostics':rec['diagnostics'],
                'top_entity_items':rec['entity_ranking'][:8],
                'local_nonpositive':s['local_nonpositive']}
        out.append({'dataset':r['dataset'],'method':r['method'],'opaque_id':r['opaque_id'],
                    'root':r['root'],'cell':r['cell'],'fault':r['fault'],
                    'hit1':r['hit@1'],'hit5':r['hit@5'],'requirements':item['requirements'],
                    'source':ev['source'],'mechanisms':r['mechanisms'],
                    'graph_audit':agg['graph_'+split],
                    'root_metric':ev['root_metric_Simple_convention'],
                    'root_trace':ev['root_trace_start_Simple_convention' if split=='start' else 'root_trace_end_context'],
                    'root_log':ev['root_logs_A_Simple_convention'],
                    'root_operations':ev['root_operations_end_native'],'seeds':ss})
    output.write_text(json.dumps(out,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print('source-linked manual excerpts',len(out))

if __name__=='__main__':main()
