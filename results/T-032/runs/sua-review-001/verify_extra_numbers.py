from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
T032 = REPO / 'results/T-032'


def read(p):
    return json.loads(p.read_text(encoding='utf-8'))


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


checks = []
def check(label, reported, actual, pointer):
    checks.append({'label': label, 'reported': reported, 'actual': actual,
                   'source': pointer, 'pass': reported == actual})


pins = read(HERE / 'truoc-sua.json')['old_manifest_checks']
for rel in ('results/T-032/doi-chieu-dung-sai.json', 'results/T-032/can-thiep-tinh-toan.json'):
    pin = next(x for x in pins if x['path'] == rel)
    check('source unchanged ' + rel, pin['expected'], sha(REPO / rel), 'truoc-sua.json /old_manifest_checks')
slow_rel = 'results/T-032/runs/call-slow-001/summary.json'
pin = read(T032 / 'can-thiep-tinh-toan.json')['nguon_da_dung'][slow_rel]['sha256']
check('call-slow source manifest', pin, sha(REPO / slow_rel), 'can-thiep-tinh-toan.json /nguon_da_dung')
assert all(x['pass'] for x in checks)

doc = (T032 / 'doc-tay.md').read_text(encoding='utf-8')
line = next(x for x in doc.splitlines() if x.startswith('10. **`dev-db293894ab`'))
reported = re.search(r'ca này (\d+) lời gọi chậm, (\d+) nằm trong span của root \((\d+)%\); ở `dev-12a1a88069` (\d+) lời gọi chậm, (\d+) nằm trong span của root \((\d+)%\)', line)
assert reported
reported = [int(x) for x in reported.groups()]
slow = read(REPO / slow_rel)
for j, cid in enumerate(('dev-db293894ab', 'dev-12a1a88069')):
    i, case = next((i, c) for i, c in enumerate(slow['cases']) if c['opaque_id'] == cid)
    key = next(k for k, v in case['edges_to_root'].items() if v['caller'] == 'ts-seat-service')
    edge = case['edges_to_root'][key]
    actual = [edge['n_slow_after'], edge['slow_inside_callee_span'],
              round(100 * edge['slow_inside_callee_span'] / edge['n_slow_after'])]
    check(cid + ' slow/inside/rounded percent', reported[j*3:j*3+3], actual,
          slow_rel + f' /cases/{i}/edges_to_root/{key}')

ids = ['dev-4e68956051', 'dev-4f8a844308', 'dev-98bc73c499',
       'dev-a505ab3f65', 'dev-b8bd0abf60', 'dev-ba831dbeb8']
units = read(T032 / 'doi-chieu-dung-sai.json')['don_vi']
huge = []
for cid in ids:
    i, unit = next((i, u) for i, u in enumerate(units) if u['method'] == 'circa_ols_da' and u['opaque_id'] == cid)
    row = unit['chi_tiet']['nut_cuc_lon']
    check(cid + ' one huge node, seven parents', [1, 'ts-admin-travel-service_latency', 7],
          [len(row), row[0]['nut'], row[0]['so_cha']], f'doi-chieu-dung-sai.json /don_vi/{i}/chi_tiet/nut_cuc_lon')
    huge.append(row[0])
line = next(x for x in doc.splitlines() if x.startswith('1. **Sáu đơn vị cùng đường đi'))
patterns = [('y_train_do_lech_chuan', r'độ lệch chuẩn của y ở đoạn train từ ([\d,e.+-]+) tới ([\d,e.+-]+)'),
            ('rht', r'điểm RHT từ ([\d,e.+-]+) tới ([\d,e.+-]+)'),
            ('rht_khong_canh', r'không có cha có điểm từ ([\d,]+) tới ([\d,]+)')]
for field, pattern in patterns:
    matches = re.search(pattern, line)
    assert matches, field
    for label, text, actual in zip(('min', 'max'), matches.groups(),
                                  (min(x[field] for x in huge), max(x[field] for x in huge))):
        reported = float(text.replace(',', '.'))
        mantissa = text.lower().split('e')[0]
        digits = len(mantissa.split(',')[1]) if ',' in mantissa else 0
        rounded = float(f'{actual:.{digits}e}') if 'e' in text.lower() else round(actual, digits)
        check(field + ' ' + label + ' rounded as written', reported, rounded,
              'doi-chieu-dung-sai.json /don_vi filter(method=circa_ols_da, opaque_id in six stated cases) /chi_tiet/nut_cuc_lon/0/' + field)

result = {'n_checks': len(checks), 'n_mismatch': sum(not c['pass'] for c in checks),
          'checks': checks, 'doc_sha256': sha(T032 / 'doc-tay.md'),
          'scope': 'Only the two slow-call edges and six stated CIRCA extreme-node summaries; no physical-cause attribution.'}
(HERE / 'kiem-so/kiem-so-bo-sung.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k != 'checks'}, ensure_ascii=False, indent=2))
assert not result['n_mismatch']
