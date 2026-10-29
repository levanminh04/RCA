"""Adapter dữ liệu dev → API M1 (dinh-chinh-cai-dat.md CĐ11, CĐ4.1, CĐ5, CĐ12; Đ9 v1.1, Đ19) trên bộ dữ liệu tổng hợp
nhỏ do test sinh trong thư mục tạm, đi đúng đường đọc của src/p3 (selector, nezha). Không đọc data/ của repo."""
import calendar
import csv
import hashlib
import json
from datetime import datetime, timezone

import pandas as pd
import pytest

from conftest import T043, _doc, FIXTURE

HOP_DONG = _doc(T043 / 'hop-dong.json')
U_S = ['A', 'B', 'F', 'I', 'R', 'X']


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ---------------------------------------------------------------- RE2-TT

def _re2(tmp_path, t=1000):
    import sinh_trace_S
    spans, _ = sinh_trace_S.sinh('S1', t=t, mau=FIXTURE['trace_mau_S'])
    rows = [{'traceID': s['traceID'], 'spanID': s['spanID'], 'parentSpanID': s['parentSpanID'] or None,
             'serviceName': s['owner'], 'operationName': s['operation'], 'startTime': s['start_us'],
             'duration': s['duration_us']} for s in spans]
    # hai span ngoài miền: F của trace tính trên toàn file
    rows.append({'traceID': 'ngoai1', 'spanID': 'a', 'parentSpanID': None, 'serviceName': 'F',
                 'operationName': 'F.handle', 'startTime': (t - 650) * 10 ** 6, 'duration': 5000})
    rows.append({'traceID': 'ngoai2', 'spanID': 'a', 'parentSpanID': None, 'serviceName': 'F',
                 'operationName': 'F.handle', 'startTime': (t + 650) * 10 ** 6, 'duration': 7000})
    d = tmp_path / 'data' / 'rcaeval' / 're2tt_gia_1'
    d.mkdir(parents=True)
    pd.DataFrame(rows).to_parquet(d / 'traces.parquet', index=False)
    m = []
    for x in range(t - 720, t + 721):
        v = 10 + 0.1 * (x % 7) if x < t else 50.0
        m.append({'time': x, 'R_cpu': float('nan') if x == t + 3 else v, 'A_latency-90': 5.0 + 0.01 * (x % 3)})
    pd.DataFrame(m).to_parquet(d / 'metrics.parquet', index=False)
    lg = [{'timestamp': t - 500, 'container_name': 'F', 'message': 'INFO ngoai mien'},
          {'timestamp': t - 100, 'container_name': 'F', 'message': 'INFO request accepted'},
          {'timestamp': t + 100, 'container_name': 'R', 'message': 'ERROR request failed'}]
    pd.DataFrame(lg).to_parquet(d / 'logs.parquet', index=False)
    files = {k: {'path': f'data/rcaeval/re2tt_gia_1/{k}', 'sha256': _sha(d / k)}
             for k in ('traces.parquet', 'metrics.parquet', 'logs.parquet')}
    al = {'so_ca': 1, 'cases': [{'opaque_id': 'dev-0123456789', 'case_dir': 'data/rcaeval/re2tt_gia_1',
                                 'files': files}]}
    p = tmp_path / 'allowlist.json'
    p.write_text(json.dumps(al), encoding='utf-8')
    return p, spans, rows


def test_adapter_re2tt(ma, tmp_path):
    from p3 import selector
    from m1 import adapter, runner
    import sinh_trace_S
    ma('adapter-re2tt')
    t = 1000
    p, spans, rows = _re2(tmp_path, t)
    allow = selector.nap_allowlist(p)
    ca = adapter.ca_re2tt(allow, 'dev-0123456789', t, tmp_path, HOP_DONG, U_S)
    assert len(ca['spans']) == len(spans)  # hai span ngoài miền bị cắt như cua_so.cat_span
    en = [r['startTime'] + r['duration'] for r in rows]
    pc = ca['params_ca']
    assert pc['coverage']['trace'] == {'khoang': [[min(en) * 1000, max(en) * 1000]], 'r_ns': 1000}
    assert pc['coverage']['metric'] == {'khoang': [[(t - 720) * 10 ** 9, (t + 720) * 10 ** 9]], 'r_ns': 10 ** 9}
    assert pc['coverage']['log'] == {'khoang': [[(t - 500) * 10 ** 9, (t + 100) * 10 ** 9]], 'r_ns': 10 ** 9}
    assert len(ca['metrics']) == 600 and ca['metrics'][0]['time'] == t - 300
    assert next(r for r in ca['metrics'] if r['time'] == t + 3)['R_cpu'] is None
    assert [l['message'] for l in ca['logs']] == ['INFO request accepted', 'ERROR request failed']
    assert pc['nguon_metric'] == {'A_latency-90': 'metric', 'R_cpu': 'metric'}
    assert pc['thoi_gian_nguon'] == {'metric': 'metrics.time'}
    assert pc['ho_so_nguon']['kenh_metric']['bang'] == HOP_DONG['kenh']['RE2-TT']['metric_theo_hau_to']
    assert pc['don_vi_thoi_gian'] == {'spans.start_us': 'us', 'metrics.time': 's', 'logs.timestamp': 's'}
    assert 'data/rcaeval/re2tt_gia_1' in ca['chuoi_cam']
    # chạy pha 1 trên ca của adapter: cpu của R có cờ (S1, E1-U)
    ch = [{'config_id': 'C1', 'bat_tat': dict(runner.R0, E1='U'), 'tham_so_E4': dict(runner.TS_HOP_DONG)}]
    h = runner.pha1([ca], {'dev-0123456789': t}, ch, tmp_path / 'l')
    rec = json.loads((tmp_path / 'l' / 'ban-ghi.jsonl').read_text(encoding='utf-8').splitlines()[0])
    assert rec['status'] == 'OK' and rec['error'] is None and h['so_ban_ghi'] == 1
    assert any(k['don_vi'] == 'metric|R_cpu' for k in rec['extra']['kenh_co'])
    assert rec['extra']['blocks_P'][0]['groups'][0] == ['R']
    # trạng thái quan sát của nguồn metric (đặc tả v1 dòng 73; Đ19 điểm 3–4)
    assert rec['coverage']['metric']['trang_thai'] == 'OK'
    # mã mờ, case_dir hay đường dẫn tệp lọt vào params thì pha 1 từ chối (CĐ12)
    ch2 = [dict(ch[0], tham_so_E3={'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4, 'ghi_chu': 're2tt_gia_1/x'})]
    assert 're2tt_gia_1' in ca['chuoi_cam']
    with pytest.raises(runner.LoiRoNhan):
        runner.pha1([ca], {'dev-0123456789': t}, ch2, tmp_path / 'l2')


def test_adapter_re2tt_hash_sai(ma, tmp_path):
    from p3 import selector
    from m1 import adapter
    ma('adapter-re2tt-hash')
    p, _, _ = _re2(tmp_path)
    allow = selector.nap_allowlist(p)
    f = tmp_path / 'data' / 'rcaeval' / 're2tt_gia_1' / 'logs.parquet'
    f.write_bytes(f.read_bytes() + b'x')
    with pytest.raises(selector.LoiRunner):
        adapter.ca_re2tt(allow, 'dev-0123456789', 1000, tmp_path, HOP_DONG, U_S)


# ---------------------------------------------------------------- Nezha-OB

PODS = {'adservice': 'adservice-5f6585d649-fnmft', 'cartservice': 'cartservice-579f59597d-wc2lz',
        'checkoutservice': 'checkoutservice-578fcf4766-9csqn', 'currencyservice': 'currencyservice-cf787dd48-vpjrd',
        'emailservice': 'emailservice-55fdc5b988-f6xth', 'frontend': 'frontend-579b9bff58-t2dbm',
        'paymentservice': 'paymentservice-9cdb6588f-554sm',
        'productcatalogservice': 'productcatalogservice-668d5f85fb-wckp8',
        'recommendationservice': 'recommendationservice-6cfdd55578-gfj6q',
        'shippingservice': 'shippingservice-7b598fc7d-lmggd'}


def _tg(ns):
    s, frac = divmod(ns, 10 ** 9)
    return datetime.fromtimestamp(s, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S') + f'.{frac:09d}'


def _ghi_csv(p, cot, rows):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(cot)
        w.writerows(rows)


def _nezha(tmp_path):
    from p3 import nezha
    t_s = calendar.timegm((2022, 8, 22, 10, 0, 0))
    t = t_s * 10 ** 9
    base = tmp_path / 'data' / 'ngoai-rcaeval' / 'nezha' / 'online-boutique' / 'rca_data' / '2022-08-22'
    rel0 = 'data/ngoai-rcaeval/nezha/online-boutique/rca_data/2022-08-22'
    files = []
    # metric: 11 nguồn, mỗi nguồn 10 dòng trong miền (5 N, 5 A) cộng 2 dòng ngoài miền
    for k, (ident, fname, chans) in enumerate(
            [('Frontend', 'front_service.csv', nezha.FRONT_CHANNELS)] +
            [(pod, f'{pod}_metric.csv', nezha.RESOURCE_CHANNELS) for pod in PODS.values()]):
        lech = (k + 1) * 10 ** 8
        rows = []
        for j in [-1] + list(range(10)) + [10]:
            x = t - 300 * 10 ** 9 + j * 60 * 10 ** 9 + lech
            vals = []
            for i, c in enumerate(chans):
                v = 1.0 + 0.01 * ((j + i) % 5)
                if ident == PODS['cartservice'] and c == 'CpuUsage(m)' and j >= 5:
                    v = 9.0
                vals.append('' if (k == 1 and i == 0 and j == 2) else repr(v))
            rows.append([f'{_tg(x)} +0000 UTC m=+{j + 100}.5', ident] + vals)
        cot = ['Time', 'ServiceName' if fname == 'front_service.csv' else 'PodName'] + list(chans)
        _ghi_csv(base / 'metric' / fname, cot, rows)
        files.append(f'{rel0}/metric/{fname}')
    # trace: ba file phút, mỗi request một span frontend và một span cartservice; có khe giữa file
    span_cot = ['TraceID', 'SpanID', 'ParentID', 'PodName', 'OperationName', 'StartTimeUnixNano', 'EndTimeUnixNano',
                'Duration']
    log_cot = ['TimeUnixNano', 'Timestamp', 'PodName', 'Log', 'TraceID', 'SpanID']
    for ten, (a, b) in (('09_59', (-55, -5)), ('10_00', (3, 57)), ('10_01', (63, 117))):
        rows, lrows = [], []
        for i, s in enumerate(range(a, b, 2)):
            st = t + s * 10 ** 9
            d_us = 2000 + (300 if s >= 0 else 0)
            tid = f'{ten}-{i}'
            rows.append([tid, 'p', 'khong-resolve', PODS['frontend'], 'hipstershop.Frontend/Get', st,
                         st + d_us * 1000 + 17, d_us])
            rows.append([tid, 'c', 'p', PODS['cartservice'], 'hipstershop.CartService/GetCart', st + 100_000,
                         st + 100_000 + (d_us - 500) * 1000, d_us - 500])
            x = st + 500_000
            sev = 'error' if (s >= 0 and i % 2 == 0) else ' info '
            inner = json.dumps({'severity': sev, 'message': f'request {i} done in {d_us} us'})
            lrows.append([x, _tg(x).replace(' ', 'T') + 'Z', PODS['cartservice'], json.dumps({'log': inner}),
                          tid, 'c'])
        _ghi_csv(base / 'trace' / f'{ten}_trace.csv', span_cot, rows)
        _ghi_csv(base / 'log' / f'{ten}_log.csv', log_cot, lrows)
        files += [f'{rel0}/trace/{ten}_trace.csv', f'{rel0}/log/{ten}_log.csv']
    fm = {}
    for rel in files:
        pth = tmp_path / rel
        fm[rel] = {'path': rel, 'sha256': _sha(pth), 'bytes': pth.stat().st_size}
    al = {'dataset': 'Nezha-OB', 'so_ca': 1,
          'cases': [{'opaque_id': 'dev-abcdef0123', 't_ns': t, 'trace_guard_s': 41, 'files': fm}]}
    p = tmp_path / 'allowlist-nezha.json'
    p.write_text(json.dumps(al), encoding='utf-8')
    return p, t


def test_adapter_nezha(ma, tmp_path):
    from p3 import nezha
    from m1 import adapter, runner
    ma('adapter-nezha')
    p, t = _nezha(tmp_path)
    allow = nezha.nap_allowlist(p)
    ca = adapter.ca_nezha(allow, 'dev-abcdef0123', tmp_path, HOP_DONG)
    pc = ca['params_ca']
    assert ca['t'] * 10 ** 9 == t and ca['inventory'] == nezha.UNIVERSE
    assert len(ca['metrics']) == 10 and len(pc['nguon_metric']) == 165
    assert len(pc['thoi_gian_nguon']) == 11 and all(len(v) == 10 for v in pc['thoi_gian_nguon'].values())
    assert pc['nguon_metric']['frontend_FrontSuccessRate-pct'] == 'metric:front_service'
    assert pc['nguon_metric']['frontend_CpuUsage-m'] == 'metric:frontend'
    assert pc['phan_hoach_NA_da_kiem'] == {k: True for k in pc['thoi_gian_nguon']}
    assert not any('/' in v for v in pc['nguon_metric'].values())
    # F trace, log: một khoảng mỗi file phút (ba file, có khe), r = 1 ns
    assert len(pc['coverage']['trace']['khoang']) == 3 and pc['coverage']['trace']['r_ns'] == 1
    k0 = pc['coverage']['trace']['khoang']
    assert all(a[1] < b[0] for a, b in zip(k0, k0[1:]))
    # coverage khai theo từng nguồn metric, khóa là mã nguồn trung tính, khoảng từ cột Time của file nguồn
    assert {k for k in pc['coverage'] if k.startswith('metric')} == set(pc['thoi_gian_nguon'])
    for k in pc['thoi_gian_nguon']:
        assert pc['coverage'][k]['r_ns'] == 1 and len(pc['coverage'][k]['khoang']) == 1
        a, b = pc['coverage'][k]['khoang'][0]
        assert a <= min(pc['thoi_gian_nguon'][k]) and max(pc['thoi_gian_nguon'][k]) <= b
    lg = ca['logs'][0]
    assert lg['message'].startswith('request 0 done') and lg['severity_raw'] in ('error', ' info ')
    assert pc['ho_so_nguon']['quy_tac_log']['kieu'] == 'severity'
    assert pc['don_vi_thoi_gian'] == {'spans.start_us': 'us', 'metrics.time': 'ns', 'logs.timestamp': 'ns'}
    assert any(x.endswith('10_00_trace.csv') for x in ca['chuoi_cam'])
    ch = [{'config_id': 'C1', 'bat_tat': dict(runner.R0, E1='U', E3=True), 'tham_so_E4': dict(runner.TS_HOP_DONG)}]
    runner.pha1([ca], {'dev-abcdef0123': ca['t']}, ch, tmp_path / 'l')
    rec = json.loads((tmp_path / 'l' / 'ban-ghi.jsonl').read_text(encoding='utf-8').splitlines()[0])
    assert rec['error'] is None and rec['status'] in ('OK', 'NO_EVIDENCE')
    assert rec['diagnostics']['cot_metric_chua_khai_nguon'] == []
    assert rec['diagnostics']['nguon_metric_unsupported'] == []
    assert rec['coverage']['trace']['trang_thai'] == 'OK'
    assert all(rec['coverage'][k]['trang_thai'] == 'OK' for k in pc['thoi_gian_nguon'])
    assert any(k['don_vi'] == 'metric|cartservice_CpuUsage-m' for k in rec['extra']['kenh_co'])
    # tên file phút (mang phút tiêm) lọt vào params thì pha 1 từ chối (CĐ12)
    ch2 = [dict(ch[0], tham_so_E3={'khop': 'hoan_toan', 'sim_th': 0.4, 'do_sau': 4, 'x': '10_00_trace.csv'})]
    with pytest.raises(runner.LoiRoNhan):
        runner.pha1([ca], {'dev-abcdef0123': ca['t']}, ch2, tmp_path / 'l2')
