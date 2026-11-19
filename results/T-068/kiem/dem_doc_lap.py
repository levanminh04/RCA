"""T-068 (phương án A, service-graph-5) — kiểm độc lập file đồ thị dịch vụ bằng cách đọc thẳng trace gốc.

Viết riêng, không import service_graph.py. Khác bộ dựng ở chỗ:
- gói .tgz đọc bằng lệnh `tar -xzOf` ngoài (bộ dựng dùng tarfile);
- cửa sổ lọc một lần trên ns: giữ span khi lo <= start và end < hi, phía A khi end >= lo + 300 s
  (lo, hi, t là bội của 1000 ns nên tương đương phép lọc hai lần ns/us của l8b-xuat.py);
- phân vị hạng gần nhất tính bằng số nguyên: chỉ số = -(-p*n // 100) - 1;
- kỳ vọng dựng thành bảng (nguồn, đích, loại) rồi so từng trường.
Bản 19/11 (sửa theo phản biện): mọi cạnh, kể cả cha–con, phải có hai đầu thuộc classes; span của dịch vụ ngoài
classes, cạnh cha–con có đầu ngoài classes, span DB không phải CLIENT tính vào "không vẽ"; kiểm chéo với file ca
đếm mọi cặp cha–con khác chủ (cả cặp không vẽ); nút chú thích phải có link tới panel 3 và không đặt var-dv/var-op.

Dùng:
  py -3 -I dem_doc_lap.py --du-lieu D --do-thi G --nguon-trace nguon-trace.json [--cap ban/ca ...] [--lech-cua-so-ms X]
--lech-cua-so-ms dùng cho đối chứng âm (kỳ vọng tính trên cửa sổ dịch đi X ms, phải báo lệch).
In JSON tóm tắt; mã thoát 1 nếu có lệch.
"""
import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import parse_qs, urlparse

MAU = {'tu_sinh': '#E02F44', 'ke_thua': '#FF9830', 'binh_thuong': '#8E8E8E'}
GOP = {'postgresql': 'postgresql-shared-instance', 'redis': 'cache', 'mongodb': 'mongodb-instance'}
LOAI_CANH = {'span_cha_con', 'db', 'rabbitmq_gui', 'rabbitmq_nhan'}
KHONG_MQ = 'trace của ca không có span RabbitMQ'


def doc_trace(nguon, ca):
    goi = nguon['goi']
    if goi.endswith('.tgz'):
        b = Path(goi).read_bytes()
        assert hashlib.sha256(b).hexdigest() == nguon['sha_ngoai'], f'{ca}: hash tgz'
        del b
        man = json.loads(subprocess.run(['tar', '-xzOf', goi, f'cases/{ca}/manifest.json'], check=True,
                                        capture_output=True).stdout)
        du_lieu = subprocess.run(['tar', '-xzOf', goi, f'cases/{ca}/raw-traces.jsonl'], check=True,
                                 capture_output=True).stdout
    else:
        man = json.loads((Path(goi) / 'manifest.json').read_text(encoding='utf-8'))
        du_lieu = (Path(goi) / 'raw-traces.jsonl').read_bytes()
        if nguon.get('sha_ngoai'):
            assert hashlib.sha256(du_lieu).hexdigest() == nguon['sha_ngoai'], f'{ca}: hash raw ngoài'
    sha = hashlib.sha256(du_lieu).hexdigest()
    assert sha == man['files']['raw-traces.jsonl']['sha256'], f'{ca}: hash raw theo manifest gói'
    return du_lieu, sha


def tach_span(du_lieu, w):
    lo, hi = w[0] * 1000000, w[1] * 1000000
    moc = lo + 300 * 10**9
    ds = {}
    for dong in du_lieu.splitlines():
        if not dong.strip():
            continue
        for khoi in json.loads(dong).get('resourceSpans', []):
            ten = None
            for x in khoi.get('resource', {}).get('attributes', []):
                if x['key'] == 'service.name':
                    ten = x['value']['stringValue']
            chu = 'config-discovery' if ten == 'discovery-server' else ten
            for pham in khoi.get('scopeSpans', []):
                for s in pham.get('spans', []):
                    bd, kt = int(s['startTimeUnixNano']), int(s['endTimeUnixNano'])
                    if not (lo <= bd and kt < hi):
                        continue
                    k = s['traceId'].lower() + ':' + s['spanId'].lower()
                    if k in ds:
                        continue
                    tt = {}
                    for x in s.get('attributes', []):
                        v = list((x.get('value') or {}).values())
                        tt[x['key']] = v[0] if v else None
                    ds[k] = {'chu': chu, 'cha': s['traceId'].lower() + ':' + (s.get('parentSpanId') or '').lower()
                             if s.get('parentSpanId') else None,
                             'phia': 'A' if kt >= moc else 'N', 'kind': s.get('kind'),
                             'loi': (s.get('status') or {}).get('code') in (2, 'STATUS_CODE_ERROR'),
                             'tg': kt - bd, 'tt': tt}
    return ds


def pv(ds, p):
    if not ds:
        return None
    ds = sorted(ds)
    return round(ds[-(-p * len(ds) // 100) - 1] / 10**6, 3)


def ky_vong(ca, ds):
    lop = ca.get('classes') or {}
    bang = defaultdict(lambda: {'N': [], 'A': [], 'lN': 0, 'lA': 0, 'ct': Counter()})
    chu_span = defaultdict(lambda: {'N': 0, 'A': 0, 'lN': 0, 'lA': 0})
    khong_ve = 0
    co_mq = False
    cha_con_tat_ca = Counter()
    for s in ds.values():
        trong = s['chu'] in lop
        if trong:
            c = chu_span[s['chu']]
            c[s['phia']] += 1
            c['l' + s['phia']] += s['loi']
        else:
            khong_ve += 1
        cha = ds.get(s['cha']) if s['cha'] else None
        if cha and cha['chu'] != s['chu']:
            cha_con_tat_ca[(cha['chu'], s['chu'], s['phia'])] += 1
            if cha['chu'] in lop and trong:
                o = bang[(cha['chu'], s['chu'], 'span_cha_con')]
                o[s['phia']].append(s['tg'])
                o['l' + s['phia']] += s['loi']
            else:
                khong_ve += 1
        tt = s['tt']
        he = tt.get('db.system') or tt.get('db.system.name')
        ms = tt.get('messaging.system')
        if ms == 'rabbitmq':
            co_mq = True
        if he and s['kind'] not in (3, 'SPAN_KIND_CLIENT'):
            khong_ve += 1
            continue
        if (he or ms or s['kind'] in (4, 5, 'SPAN_KIND_PRODUCER', 'SPAN_KIND_CONSUMER')) and not trong:
            khong_ve += 1
            continue
        if he:
            ten = tt.get('db.name')
            dich = ten if ten in lop else GOP.get(he.lower())
            if dich is None or dich not in lop or dich == s['chu']:
                khong_ve += 1
                continue
            o = bang[(s['chu'], dich, 'db')]
        elif ms or s['kind'] in (4, 5, 'SPAN_KIND_PRODUCER', 'SPAN_KIND_CONSUMER'):
            k = {'SPAN_KIND_PRODUCER': 4, 'SPAN_KIND_CONSUMER': 5}.get(s['kind'], s['kind'])
            if ms == 'rabbitmq' and 'broker' in lop and k == 4:
                o = bang[(s['chu'], 'broker', 'rabbitmq_gui')]
            elif ms == 'rabbitmq' and 'broker' in lop and k == 5:
                o = bang[('broker', s['chu'], 'rabbitmq_nhan')]
            else:
                khong_ve += 1
                continue
        else:
            continue
        o[s['phia']].append(s['tg'])
        o['l' + s['phia']] += s['loi']
    return bang, chu_span, khong_ve, co_mq, cha_con_tat_ca


def kiem_link(ca, g, chu_thich):
    loi = []
    if any('detail__url' in e for e in g['canh']):
        loi.append('cạnh có link')
    dv = {x for x in ca.get('services') or [] if not x.startswith('__')}
    w = ca['cua_so_ms']
    for n in g['nut']:
        q = parse_qs(urlparse(n.get('detail__url', '')).query, keep_blank_values=True)
        if chu_thich and not q:
            loi.append(f'nút chú thích thiếu link {n["id"]}')
            continue
        if chu_thich and ('var-dv' in q or 'var-op' in q):
            loi.append(f'nút chú thích đặt var-dv/var-op {n["id"]}')
        if not q:
            if n['id'] in dv:
                loi.append(f'nút dịch vụ thiếu link {n["id"]}')
            continue
        if n['id'] not in dv and not chu_thich:
            loi.append(f'nút không phải dịch vụ có link {n["id"]}')
        muon = {'var-ban': [g['ban']], 'var-ca': [g['ca']], 'from': [str(w[0])], 'to': [str(w[1] - 1)]}
        if any(q.get(k) != v for k, v in muon.items()):
            loi.append(f'link sai bản/ca/cửa sổ {n["id"]}')
        if chu_thich and 'viewPanel=panel-3' not in n['detail__url']:
            loi.append('nút chú thích không mở bảng trạng thái')
        if not chu_thich and q.get('var-dv') != [n['id']]:
            loi.append(f'link sai dịch vụ {n["id"]}')
    return loi


def kiem(ca, g, ds, sha_ca, sha_raw):
    loi = []
    if g.get('nguon_file_sha256') != sha_ca:
        loi.append('nguon_file_sha256 khác file ca')
    if ca.get('trang_thai_chay') != 'OK' or not ca.get('ranking_rows'):
        if g.get('trang_thai') != 'khong_co_dau_ra' or not any(n['title'] == 'không có đầu ra' for n in g['nut']):
            loi.append('ca lỗi chạy không hiện "không có đầu ra"')
        if any(e['detail__loai'] != 'chu_thich' for e in g['canh']) or any(n['id'][:2] != '__' for n in g['nut']):
            loi.append('ca lỗi chạy có nút/cạnh dữ liệu')
        return loi + kiem_link(ca, g, True)
    if (g.get('nguon_trace') or {}).get('sha256_raw_traces') != sha_raw:
        loi.append('nguon_trace sai hash')
    bang, chu_span, khong_ve, co_mq, cha_con_tat_ca = ky_vong(ca, ds)
    lop = ca.get('classes') or {}
    co = {}
    for e in g['canh']:
        k = (e['source'], e['target'], e['detail__loai'])
        if e['detail__loai'] not in LOAI_CANH:
            loi.append(f'loại cạnh lạ {k}')
        if k in co:
            loi.append(f'cạnh trùng {k}')
        co[k] = e
        if not ({e['source'], e['target']} <= set(lop)):
            loi.append(f'cạnh tới đích ngoài classes {k}')
    if set(co) != set(bang):
        loi.append(f'tập cạnh lệch: thừa {sorted(set(co) - set(bang))[:3]} thiếu {sorted(set(bang) - set(co))[:3]}')
    for k in set(co) & set(bang):
        e, o = co[k], bang[k]
        muon = {'detail__so_N': len(o['N']), 'detail__so_A': len(o['A']), 'detail__loi_N': o['lN'],
                'detail__loi_A': o['lA'], 'detail__p50_N_ms': pv(o['N'], 50), 'detail__p50_A_ms': pv(o['A'], 50),
                'detail__p95_N_ms': pv(o['N'], 95), 'detail__p95_A_ms': pv(o['A'], 95)}
        sai = [f for f, v in muon.items() if e.get(f) != v]
        if sai:
            loi.append(f'số lệch {k}: {sai}')
        if f'nền {len(o["N"])} · sự cố {len(o["A"])}' != e['mainstat']:
            loi.append(f'nhãn số lệch {k}')
    # Kiểm chéo với file ca (cùng tiêu chí bộ dựng dừng).
    chu = {t['id']: t['chu'] for t in ca['thao_tac']}
    tc = Counter()
    for e in ca['canh_thao_tac']:
        if chu[e['source']] != chu[e['target']]:
            tc[(chu[e['source']], chu[e['target']], 'N')] += e['so_N']
            tc[(chu[e['source']], chu[e['target']], 'A')] += e['so_A']
    if +tc != +cha_con_tat_ca:
        loi.append('trace khác canh_thao_tac của file ca')
    hang = {r['entity']: (r['hang'], r['lop']) for r in ca['ranking_rows']}
    nut_muon = set(hang) | set(chu_span) | {x for k in bang for x in k[:2]}
    nut = {n['id']: n for n in g['nut']}
    if set(nut) != nut_muon:
        loi.append(f'tập nút lệch: thừa {sorted(set(nut) - nut_muon)} thiếu {sorted(nut_muon - set(nut))}')
    for i, n in nut.items():
        h = hang.get(i)
        if h and (n['mainstat'] != f'#{h[0]}' or n['color'] != MAU[h[1]] or n['detail__lop'] != h[1]):
            loi.append(f'màu/hạng lệch {i}')
        c = chu_span.get(i)
        if c and (n.get('detail__span_N'), n.get('detail__span_A'), n.get('detail__loi_N'), n.get('detail__loi_A')) != \
                (c['N'], c['A'], c['lN'], c['lA']):
            loi.append(f'số span nút lệch {i}')
    ghi = {x['muc']: x for x in g.get('ghi_chu', [])}
    if co_mq == ('RabbitMQ' in ghi):
        loi.append('ghi chú RabbitMQ sai')
    if 'broker' in nut and (KHONG_MQ in nut['broker']['title']) == co_mq:
        loi.append('tiêu đề broker sai')
    if sum(x['so'] for x in g.get('ghi_chu', []) if x['muc'] == 'không vẽ') != khong_ve:
        loi.append(f'số span không vẽ lệch (kỳ vọng {khong_ve})')
    return loi + kiem_link(ca, g, False)


def main():
    sys.stdout.reconfigure(encoding='utf-8', newline='\n')  # -I bỏ qua PYTHONIOENCODING; Windows mặc định cp1252, CRLF
    sys.stderr.reconfigure(encoding='utf-8', newline='\n')
    ap = argparse.ArgumentParser()
    ap.add_argument('--du-lieu', required=True)
    ap.add_argument('--do-thi', required=True)
    ap.add_argument('--nguon-trace', required=True)
    ap.add_argument('--cap', nargs='*')
    ap.add_argument('--lech-cua-so-ms', type=int, default=0)
    a = ap.parse_args()
    du, dt = Path(a.du_lieu), Path(a.do_thi)
    nguon = json.loads(Path(a.nguon_trace).read_text(encoding='utf-8'))
    if a.cap:
        cap = [tuple(x.split('/')) for x in a.cap]
    else:
        idx = json.loads((du / 'chi-muc-ban.json').read_text(encoding='utf-8'))
        cap = [(v['ban'], c) for v in idx['ban'] for c in v['cac_ca']]
    theo_ca = defaultdict(list)
    for b, c in cap:
        theo_ca[c].append(b)
    ket, tong = {}, Counter()
    for c, bans in theo_ca.items():
        ds = sha_raw = None
        for b in bans:
            raw = (du / b / f'{c}.json').read_bytes()
            ca = json.loads(raw)
            g = json.loads((dt / b / f'{c}.json').read_text(encoding='utf-8'))
            if ds is None and ca.get('trang_thai_chay') == 'OK' and ca.get('ranking_rows'):
                du_lieu, sha_raw = doc_trace(nguon[c], c)
                w = [x + a.lech_cua_so_ms for x in ca['cua_so_ms']]
                ds = tach_span(du_lieu, w)
                del du_lieu
            loi = kiem(ca, g, ds, hashlib.sha256(raw).hexdigest(), sha_raw)
            tong['cap'] += 1
            tong['dat'] += not loi
            tong['khong_co_dau_ra'] += g.get('trang_thai') == 'khong_co_dau_ra'
            for e in g['canh']:
                tong['canh_' + e['detail__loai']] += 1
            if loi:
                ket[f'{b}/{c}'] = loi
        print(c, 'xong', file=sys.stderr, flush=True)
    print(json.dumps({'tong': tong, 'loi': ket}, ensure_ascii=False, indent=1))
    sys.exit(1 if ket else 0)


if __name__ == '__main__':
    main()
