"""Kiểm wrapper (3 trường hợp span) và kiểm driver: chế độ cũ phải tái lập đúng bản ghi dev-ob-001 đã lưu.

Chạy từ gốc repo bằng python môi trường đã ghim:
D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B results/T-054/runs/sua-cd3-ob-001/kiem_wrapper.py
"""
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lane  # noqa: E402

_JOB0 = json.loads((lane.GOC / 'results/T-054/runs/cai-ob-source-native-008/dev-ob-001/job.json').read_text(encoding='utf-8'))
lane.them_pythonpath(_JOB0['pythonpath'])
from m1 import span  # noqa: E402

RUN = Path(__file__).resolve().parent
out = {'schema': 'T054-SUA-CD3-KIEM-WRAPPER-1', 'checks': {}}


def check(name, ok, **info):
    out['checks'][name] = dict(PASS=bool(ok), **info)


# 1) ba trường hợp span qua wrapper + lõi đã ghim
rows = [
    {'traceID': 't', 'spanID': 'a', 'parentSpanID': 'root', 'owner': 'x', 'operation': 'op', 'start_us': 0, 'duration_us': 10},
    {'traceID': 't', 'spanID': 'b', 'parentSpanID': 'a', 'owner': 'y', 'operation': 'op', 'start_us': 1, 'duration_us': 5},
    {'traceID': 't', 'spanID': 'c', 'parentSpanID': 'zz', 'owner': 'z', 'operation': 'op', 'start_us': 2, 'duration_us': 3},
]
cu = span.chuan_bi(rows, t=0, tau=1)
moi_data, n = lane.chuan_hoa_root({'spans': rows})
moi = span.chuan_bi(moi_data['spans'], t=0, tau=1)
check('root_thanh_goc', moi['spans'][('t', 'a')]['cha'] is None and not moi['spans'][('t', 'a')]['mo_coi']
      and cu['spans'][('t', 'a')]['mo_coi'], n_doi=n, cu_mo_coi=cu['chan_doan']['mo_coi'], moi_mo_coi=moi['chan_doan']['mo_coi'],
      cu_goc=cu['chan_doan']['goc'], moi_goc=moi['chan_doan']['goc'])
check('parent_that_giu', moi['spans'][('t', 'b')]['cha'] == ('t', 'a'))
check('parent_thieu_van_mo_coi', moi['spans'][('t', 'c')]['mo_coi'] and moi['spans'][('t', 'c')]['cha'] is None)
check('chi_doi_dung_truong', n == 1 and [dict(r) for r in moi_data['spans']][1:] == rows[1:]
      and {k: v for k, v in moi_data['spans'][0].items() if k != 'parentSpanID'} ==
      {k: v for k, v in rows[0].items() if k != 'parentSpanID'})

# 2) driver chế độ cũ tái lập bản ghi dev-ob-001 (laptop, cùng config/env)
ref_dir = lane.GOC / 'results/T-054/runs/cai-ob-source-native-008/dev-ob-001'
job = json.loads((ref_dir / 'job.json').read_text(encoding='utf-8'))
ref = json.loads((ref_dir / 'result.json').read_text(encoding='utf-8'))
contract = json.loads((lane.GOC / job['m1_contract']['path']).read_text(encoding='utf-8'))
data, _ = lane.doc_ca(job['source'], job['slot']['opaque_id'], job['inventory'], contract, str(lane.GOC), sua=False)
params = lane.params_m1(job['config'], data)
raw = lane.chay_m1(data, job['t'], params)
a = json.loads(lane.dump(raw))
b = ref['records'][0]
check('driver_cu_tai_lap_dev_ob_001', a == b, n_keys=len(b),
      khac=[k for k in sorted(set(a) | set(b)) if a.get(k) != b.get(k)][:10])

out['PASS'] = all(c['PASS'] for c in out['checks'].values())
(RUN / 'kiem-wrapper.json').write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
print(json.dumps(out, ensure_ascii=False, sort_keys=True))
