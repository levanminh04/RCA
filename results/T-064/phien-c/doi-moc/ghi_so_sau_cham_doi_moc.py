# -*- coding: utf-8 -*-
"""Phiên C — ghi sổ `sau_cham` cho V052–V059 (dời mốc), chỉ thêm dòng. Nguồn: phien-c/cham/doi-moc.json, kiem-lo-doi-moc.json."""
import datetime, json, pathlib
R = pathlib.Path('results/T-064')
so = (R / 'so-bien-the.jsonl').read_text(encoding='utf-8')
if '"vai_tro_sau": "do_nhay_moc_sau_cham"' in so: raise SystemExit('đã ghi')
C = json.loads((R / 'phien-c/cham/doi-moc.json').read_text(encoding='utf-8'))
K = json.loads((R / 'phien-c/cham/kiem-lo-doi-moc.json').read_text(encoding='utf-8'))
CHA = {'V052': 'P7', 'V055': 'P7', 'V058': 'P7', 'V059': 'P7', 'V053': 'V032', 'V056': 'V032', 'V054': 'V041', 'V057': 'V041'}
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); dong = []
for ma in [b for b in C['ban'] if b.startswith('V05')]:
    cha = CHA[ma[:4]]; cap = C['cap'][f'{cha} -> {ma}']
    x = {'loai': 'sau_cham', 'utc': now, 'ma': ma, 'vai_tro_sau': 'do_nhay_moc_sau_cham', 'doi_chieu_d0': cha, 'phien': 'C'}
    for tap, ten in (('dev2', 'tap_B_13'), ('t062', 'khong_hoi_quy_T062')):
        b = C['ban'][ma][tap]; c = cap[tap]
        x[ten] = {'tong': b['tong'], 'K': b['K'], 'bang_canh': b['bang_canh'], 'so_voi_d0': c['so_voi'], 'dK': c['dK'],
                  'tut_qua_2_bac': c['tut_qua_2_bac'],
                  'ca_doi': {m: {k: v for k, v in d.items() if k not in ('_sha_khac',)} for m, d in c['doi'].items() if set(d) - {'_sha_khac', 'o'}}}
    x['kiem_lo'] = K['ban'][ma]
    x['nguon'] = ['phien-c/cham/doi-moc.json', 'phien-c/cham/kiem-lo-doi-moc.json', 'phien-c/doi-moc/bang-o.md']
    dong.append(x)
with open(R / 'so-bien-the.jsonl', 'a', encoding='utf-8', newline='\n') as f:
    for x in dong: f.write(json.dumps(x, ensure_ascii=False) + '\n')
print('ghi', len(dong), now)
