#!/usr/bin/env python3
"""T-068 phương án A — bước 0 rà soát (chỉ đọc gói trace, không ghi vào chỗ gốc).

Một ca: kiểm hash trace theo manifest đã cho, cắt cửa sổ theo l8b-xuat.py:135–160
(start >= lo, end < hi, tính trên ns và trên us đã chuẩn hóa; bỏ trùng (traceId, spanId);
alias discovery-server -> config-discovery; phía A khi end >= lo + 300 s), rồi:
- đếm thuộc tính DB / RabbitMQ / kind / status trong cửa sổ;
- kiểm chéo: số quan hệ cha–con khác chủ theo cặp (nguồn, đích) và phía N/A so với
  tổng `canh_thao_tac` của file ca (gộp theo chủ thao tác); số span theo chủ so với n_N/n_A của `thao_tac`.

Dùng:
  py -3 -I ra_soat.py --ca X --file-ca <ca.json> --trace <raw-traces.jsonl> --sha <sha256> --out <json>
  py -3 -I ra_soat.py --ca X --file-ca <ca.json> --tgz <X.tgz> --tgz-sha <sha256> --out <json>
"""
import argparse
import collections
import hashlib
import io
import json
import sys
import tarfile

ALIAS = {'discovery-server': 'config-discovery'}
KIND = {'SPAN_KIND_INTERNAL': 1, 'SPAN_KIND_SERVER': 2, 'SPAN_KIND_CLIENT': 3, 'SPAN_KIND_PRODUCER': 4,
        'SPAN_KIND_CONSUMER': 5}
KEYS = ('db.system', 'db.system.name', 'db.name', 'db.namespace', 'server.address', 'messaging.system',
        'messaging.destination.name', 'messaging.operation', 'messaging.operation.type',
        'messaging.rabbitmq.destination.routing_key')


def av(attrs):
    out = {}
    for x in attrs or []:
        v = x.get('value') or {}
        out[x['key']] = next(iter(v.values()), None) if v else None
    return out


def sha_file(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


class Hashing(io.RawIOBase):
    def __init__(self, f):
        self.f, self.h = f, hashlib.sha256()

    def readable(self):
        return True

    def readinto(self, b):
        d = self.f.read(len(b))
        self.h.update(d)
        b[:len(d)] = d
        return len(d)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ca', required=True)
    ap.add_argument('--file-ca', required=True)
    ap.add_argument('--trace')
    ap.add_argument('--sha')
    ap.add_argument('--tgz')
    ap.add_argument('--tgz-sha')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    case = json.load(open(a.file_ca, encoding='utf-8'))
    w = case['cua_so_ms']
    lo, hi, t = w[0] * 10**6, w[1] * 10**6, (w[0] + 300000) * 10**6
    res = {'ca': a.ca, 'cua_so_ms': w, 'hash': {}}
    tar = None
    if a.tgz:
        got = sha_file(a.tgz)
        res['hash']['tgz'] = {'mong_doi': a.tgz_sha, 'thuc': got, 'khop': got == a.tgz_sha}
        tar = tarfile.open(a.tgz, 'r:gz')
        man = json.load(tar.extractfile(f'cases/{a.ca}/manifest.json'))
        exp = man['files']['raw-traces.jsonl']['sha256']
        raw = Hashing(tar.extractfile(f'cases/{a.ca}/raw-traces.jsonl'))
        res['hash']['manifest_trong_goi_cua_so_s'] = man.get('method_window_seconds')
    else:
        exp = a.sha
        raw = Hashing(open(a.trace, 'rb'))
    spans, meta = {}, {}
    total = dup = 0
    for line in io.TextIOWrapper(io.BufferedReader(raw, 1 << 20), encoding='utf-8'):
        if not line.strip():
            continue
        for rs in json.loads(line).get('resourceSpans', []):
            svc = av(rs.get('resource', {}).get('attributes'))['service.name']
            owner = ALIAS.get(svc, svc)
            for sc in rs.get('scopeSpans', []):
                for s in sc.get('spans', []):
                    total += 1
                    st, en = int(s['startTimeUnixNano']), int(s['endTimeUnixNano'])
                    if st < lo or en >= hi:
                        continue
                    su, du = st // 1000, en // 1000 - st // 1000
                    if su * 1000 < lo or (su + du) * 1000 >= hi:
                        continue
                    key = (s['traceId'].lower(), s['spanId'].lower())
                    if key in spans:
                        dup += 1
                        continue
                    p = (s.get('parentSpanId') or '').lower()
                    k = s.get('kind')
                    k = KIND.get(k, k)
                    code = (s.get('status') or {}).get('code')
                    spans[key] = (owner, p, 'A' if (su + du) * 1000 >= t else 'N')
                    at = av(s.get('attributes'))
                    meta[key] = (k, code in (2, 'STATUS_CODE_ERROR'), {x: at[x] for x in KEYS if x in at}, s['name'])
    got = raw.h.hexdigest()
    res['hash']['raw_traces'] = {'mong_doi': exp, 'thuc': got, 'khop': got == exp}
    res['so_span_goi'] = total
    res['so_span_cua_so'] = len(spans)
    res['so_trung'] = dup
    # Kiểm chéo cạnh liên dịch vụ.
    pair = collections.Counter()
    same = collections.Counter()
    for key, (o, p, ph) in spans.items():
        par = spans.get((key[0], p)) if p else None
        if par is None:
            continue
        if par[0] != o:
            pair[(par[0], o, ph)] += 1
        else:
            same[ph] += 1
    owner_of = {x['id']: x['chu'] for x in case['thao_tac']}
    want = collections.Counter()
    want_same = collections.Counter()
    for e in case['canh_thao_tac']:
        s, d = owner_of[e['source']], owner_of[e['target']]
        for ph in 'NA':
            if s != d:
                want[(s, d, ph)] += e['so_' + ph]
            else:
                want_same[ph] += e['so_' + ph]
    want = +want
    lech = sorted({k for k in set(pair) | set(want) if pair[k] != want[k]})
    res['kiem_cheo_canh'] = {'so_cap_trace': len({k[:2] for k in pair}), 'so_cap_file_ca': len({k[:2] for k in want}),
                             'tong_trace': sum(pair.values()), 'tong_file_ca': sum(want.values()),
                             'cung_chu_trace': dict(same), 'cung_chu_file_ca': dict(want_same),
                             'lech': [[*k, pair[k], want[k]] for k in lech][:30], 'so_lech': len(lech)}
    per_owner = collections.Counter((o, ph) for (o, _, ph) in spans.values())
    want_owner = collections.Counter()
    for x in case['thao_tac']:
        want_owner[(x['chu'], 'N')] += x['n_N']
        want_owner[(x['chu'], 'A')] += x['n_A']
    want_owner = +want_owner
    res['kiem_cheo_span_theo_chu'] = {'lech': [[*k, per_owner[k], want_owner[k]] for k in sorted(set(per_owner) | set(want_owner))
                                               if per_owner[k] != want_owner[k]]}
    # Thuộc tính.
    kinds = collections.Counter(m[0] for m in meta.values())
    err = collections.Counter((spans[k][0], m[0]) for k, m in meta.items() if m[1])
    db = collections.Counter()
    mq = collections.Counter()
    key_count = collections.Counter()
    for k, (kd, e, at, name) in meta.items():
        for x in at:
            key_count[x] += 1
        o = spans[k][0]
        if 'db.system' in at or 'db.system.name' in at:
            db[(o, kd, at.get('db.system') or at.get('db.system.name'), at.get('db.name') or at.get('db.namespace'),
                at.get('server.address'))] += 1
        if 'messaging.system' in at or kd in (4, 5):
            mq[(o, kd, at.get('messaging.system'), at.get('messaging.destination.name'), at.get('messaging.operation'),
                at.get('messaging.rabbitmq.destination.routing_key'), name)] += 1
    res['kind'] = {str(k): v for k, v in sorted(kinds.items(), key=lambda x: str(x[0]))}
    res['loi_theo_chu_kind'] = [[*k, v] for k, v in sorted(err.items(), key=str)]
    res['so_span_co_khoa'] = dict(sorted(key_count.items()))
    res['db'] = [[*k, v] for k, v in sorted(db.items(), key=lambda x: -x[1])]
    res['rabbitmq'] = [[*k, v] for k, v in sorted(mq.items(), key=lambda x: -x[1])]
    res['classes'] = sorted(case.get('classes') or {})
    with open(a.out, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
        f.write('\n')
    ok = res['hash']['raw_traces']['khop'] and res['hash'].get('tgz', {'khop': True})['khop'] and not lech
    print(a.ca, 'hash', res['hash']['raw_traces']['khop'], 'lech_canh', len(lech), 'lech_chu',
          len(res['kiem_cheo_span_theo_chu']['lech']), 'span', len(spans), 'mq', sum(mq.values()))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
