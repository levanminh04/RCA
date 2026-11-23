"""T-073 E5 S4-6: chuỗi chuẩn hóa của 11 luật (uid, expr, ngưỡng, for, noData/execErr, nhãn, receiver) từ t072-luat.yaml.
Cùng dạng với hàm JS chạy trên /api/v1/provisioning/alert-rules (ghi trong LOG); so sha256 hai bên. Ngưỡng nguyên viết dạng số nguyên (YAML 8.0 = JSON 8)."""
import hashlib, json, sys, yaml
def giay(v):
    v = str(v); return int(v[:-1]) * {'s': 1, 'm': 60, 'h': 3600}[v[-1]]
d = yaml.safe_load(open(sys.argv[1], encoding='utf-8'))
out = []
for g in d['groups']:
    for r in g['rules']:
        a = next(x for x in r['data'] if x['refId'] == 'A'); c = next(x for x in r['data'] if x['refId'] == 'C')
        ev = c['model']['conditions'][0]['evaluator']
        out.append([r['uid'], g['name'], a['model']['expr'], ev['type'], [int(x) if float(x).is_integer() else x for x in ev['params']], giay(r['for']), r['noDataState'], r['execErrState'],
                    sorted(r['labels'].items()), r['notification_settings']['receiver']])
out.sort()
s = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
print(len(out), hashlib.sha256(s.encode()).hexdigest())
