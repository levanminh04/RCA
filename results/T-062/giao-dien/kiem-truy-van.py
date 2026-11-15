"""T-062 G1: chạy mọi truy vấn Infinity của hai dashboard qua /api/ds/query của một Grafana thử (đăng nhập ẩn danh),
thay biến bằng giá trị cho trước, in số dòng / lỗi / vài dòng đầu. Không ghi gì lên máy.

Cách dùng: py -3 -B kiem-truy-van.py <url grafana> <file dashboard> ca=<mã> dv=<thành phần> thu_muc=<thư mục> [t_tu=.. t_den=.. dv_svc=..]
"""
import json
import re
import sys
import urllib.error
import urllib.request


def thay_bien(s, v):
    return re.sub(r'\$\{(\w+)\}', lambda m: v.get(m.group(1), m.group(0)), s)


def chay(base, target, v):
    t = json.loads(thay_bien(json.dumps(target, ensure_ascii=False), v))
    t.setdefault('refId', 'A')
    body = json.dumps({'queries': [t], 'from': 'now-1h', 'to': 'now'}).encode()
    r = urllib.request.Request(base + '/api/ds/query', data=body, headers={'Content-Type': 'application/json'})
    try:
        return json.load(urllib.request.urlopen(r))
    except urllib.error.HTTPError as e:
        return {'http_error': e.code, 'body': e.read().decode()[:500]}


def in_kq(ten, res, n=3):
    if 'http_error' in res:
        print(f'  [{ten}] HTTP {res["http_error"]}: {res["body"]}')
        return
    for k, r in res['results'].items():
        if r.get('error'):
            print(f'  [{ten}] LỖI: {r["error"]}')
        for f in r.get('frames', []):
            names = [x['name'] for x in f['schema']['fields']]
            vals = f.get('data', {}).get('values', [])
            rows = list(zip(*vals)) if vals else []
            print(f'  [{ten}] {len(rows)} dòng; cột {names}')
            for row in rows[:n]:
                print('     ', row)


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    base, f = sys.argv[1], sys.argv[2]
    v = dict(a.split('=', 1) for a in sys.argv[3:])
    d = json.load(open(f, encoding='utf-8'))
    for b in d['templating']['list']:
        if b['type'] == 'query':
            t = dict(b['query']['infinityQuery'], refId='v', datasource=b['datasource'])
            in_kq('biến ' + b['name'], chay(base, t, v))
    for p in d['panels']:
        for t in p.get('targets', []):
            if t.get('datasource', {}).get('uid') == 'infinity-rca':
                in_kq(f'{p["title"]} / {t["refId"]}', chay(base, t, v))


if __name__ == '__main__':
    main()
