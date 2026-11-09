"""T-056: dựng yêu cầu đếm tín hiệu cho từng EC2 từ job/result M1 đã VERIFIED (không nhãn trong yêu cầu)."""
import glob
import json
from pathlib import Path

REPO = Path('D:/RCA-flashticket')
OUT = REPO / 'results/T-056/runs/yeu-cau-001'
SRC = {
    'RE2-TT': [REPO / 'results/T-054/runs/chuan-bi-main-013-v2/received-main-002/{h}/results/T-054/runs/main-013-v2/queue'],
    'RE3-OB': [Path('D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received/{h}/results/T-054/runs/re3-ban-cuoi-001/queue')],
}
DATA_ROOT = {'RE2-TT': '/home/ubuntu/rca-p7/T-054/checkpoint013/data-root', 'RE3-OB': '/home/ubuntu/rca-p7/T-055/data-root'}
OUT.mkdir(parents=True, exist_ok=False)
for h in ('ec2_1', 'ec2_2'):
    req = {'keywords': ['ERROR', 'FAIL', 'EXCEPTION'], 'cases': {}}
    for ds, pats in SRC.items():
        for pat in pats:
            for jf in glob.glob(str(Path(str(pat).format(h=h)) / '*/attempt-*/job.json')):
                j = json.loads(Path(jf).read_bytes())
                s = j['slot']
                if s['arm'] != 'M1' or s['view'] != 'main':
                    continue
                rec = json.loads((Path(jf).parent / 'result.json').read_bytes())['records'][0]
                cols = sorted({k['don_vi'].split('|', 1)[1] for k in rec['extra'].get('kenh_co', [])
                               if k['don_vi'].startswith('metric|')})
                s_by = {k['don_vi'].split('|', 1)[1] + '|' + k['huong']: k['s'] for k in rec['extra'].get('kenh_co', [])
                        if k['don_vi'].startswith('metric|')}
                req['cases'][s['opaque_id']] = {'dataset': ds, 'data_root': DATA_ROOT[ds], 't': j['t'],
                                                'files': {n: v['path'] for n, v in j['source']['files'].items()},
                                                'metric_cols': cols, 'm1_s': s_by}
    (OUT / f'{h}.json').write_text(json.dumps(req, sort_keys=True), encoding='utf-8')
    print(h, {ds: sum(1 for c in req['cases'].values() if c['dataset'] == ds) for ds in SRC})
