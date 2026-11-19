#!/usr/bin/env python3
"""T-068 A bước 0: gộp results/T-068/a/ra-soat/<ca>.json thành bảng tóm tắt (in JSON)."""
import collections
import json
import pathlib
import sys

D = pathlib.Path(__file__).resolve().parent / 'ra-soat'
rows = []
tong = collections.Counter()
for p in sorted(D.glob('*.json')):
    r = json.loads(p.read_text(encoding='utf-8'))
    kinds_db = collections.Counter(x[1] for x in r['db'] for _ in [0])
    db_kind = collections.Counter()
    for x in r['db']:
        db_kind[x[1]] += x[-1]
    mq = collections.Counter()
    for x in r['rabbitmq']:
        mq[x[1]] += x[-1]
    dbnames = collections.Counter()
    for x in r['db']:
        dbnames[(x[2], x[3])] += x[-1]
    owners = sorted({x[0] for x in r['db']} | {x[0] for x in r['rabbitmq']})
    row = {'ca': r['ca'], 'hash_trace': r['hash']['raw_traces']['khop'], 'hash_tgz': r['hash'].get('tgz', {}).get('khop'),
           'span_cua_so': r['so_span_cua_so'], 'trung': r['so_trung'],
           'lech_canh': r['kiem_cheo_canh']['so_lech'], 'lech_span_chu': len(r['kiem_cheo_span_theo_chu']['lech']),
           'cap_lien_dv': r['kiem_cheo_canh']['so_cap_trace'],
           'db_theo_kind': {str(k): v for k, v in db_kind.items()},
           'db_he_ten': {f'{a}/{b}': v for (a, b), v in sorted(dbnames.items(), key=str)},
           'mq_theo_kind': {str(k): v for k, v in sorted(mq.items(), key=str)},
           'span_loi': sum(x[-1] for x in r['loi_theo_chu_kind']),
           'chu_ngoai_classes': [o for o in owners if o not in r['classes']],
           'db_name_ngoai_classes': sorted({x[3] for x in r['db'] if x[3] and x[3] not in r['classes']}),
           'classes_co_user_db': 'user_db' in r['classes'], 'classes_co_broker': 'broker' in r['classes']}
    rows.append(row)
    tong['ca'] += 1
    tong['hash_dat'] += bool(row['hash_trace']) and row['hash_tgz'] in (None, True)
    tong['kiem_cheo_dat'] += row['lech_canh'] == 0 and row['lech_span_chu'] == 0
    tong['khong_mq'] += not r['rabbitmq']
json.dump({'tong': tong, 'ca': rows}, sys.stdout, ensure_ascii=False, indent=1)
print()
