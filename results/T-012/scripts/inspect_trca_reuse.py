"""Compare complete TRCA input bytes against inspected, pinned Nezha inputs."""
import argparse,collections,hashlib,json,zipfile
from pathlib import Path
B=Path(__file__).resolve().parents[1];ROOT=B.parents[1];O=None
def main():
    global O
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);a=p.parse_args();O=B/'runs'/a.run
    O.mkdir(exist_ok=False);members=json.loads((B/'runs/trca-inventory-001/members.json').read_text());nz=json.loads((ROOT/'results/T-008/runs/download-001/manifest.json').read_text())['items'];lookup={x['path']:x for x in nz};rows=[];labels=[]
    for m in members:
        n=m['name']
        if not m['regular'] or not n.startswith('TRCA/datasets/'):continue
        tail=n[len('TRCA/datasets/'):];phase,date,*rest=tail.split('/');system='online-boutique' if date.startswith('2022') else 'train-ticket';phase_map={'failure-free':'construct_data','failure-impacted':'rca_data'}
        if phase not in phase_map:raise ValueError('unrecognized phase')
        key='/'.join([system,phase_map[phase],date,*rest]);other=lookup.get(key)
        if n.endswith('.csv'):rows.append(dict(member=n,nezha_path=key,bytes=m['bytes'],sha256=m['sha256'],nezha_match=bool(other and other['sha256']==m['sha256'] and other['actual_bytes']==m['bytes']),quality_reused_from='results/T-008/runs/file-audit-001/summary.json' if other else None))
        elif n.endswith('fault_list.json'):
            p=ROOT/'results/T-008/sources/labels'/Path(n).name;labels.append(dict(member=n,source=str(p.relative_to(ROOT)).replace('\\','/'),same_bytes=p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256']))
    with zipfile.ZipFile(ROOT/'data/ngoai-rcaeval/T-012/trca/attempt-002/TRCA.zip') as z:(O/'README.md').write_bytes(z.read('TRCA/README.md'))
    result=dict(csv_files=len(rows),exact_nezha_matches=sum(x['nezha_match'] for x in rows),unmatched=[x for x in rows if not x['nezha_match']],labels=labels,rows=rows,all_telemetry_identical=all(x['nezha_match'] for x in rows),reuse_means_not_independent=True)
    (O/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('rows','unmatched')},indent=2))
if __name__=='__main__':main()
