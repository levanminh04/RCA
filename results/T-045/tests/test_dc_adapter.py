"""ĐC1, ĐC2 (results/T-045/dinh-chinh-cai-dat.md): parquet RE2-TT mang metadata pandas kiểu `string`, nên giá trị
rỗng đọc ra là pd.NA. Ca giả sinh trong thư mục tạm, cùng đường đọc `p3.selector` như test_adapter của T-044."""
import hashlib
import json
from pathlib import Path

import pandas as pd
import pyarrow.parquet as pq

ROOT = Path(__file__).resolve().parents[3]
HOP_DONG = json.loads((ROOT / 'results' / 'T-043' / 'hop-dong.json').read_text(encoding='utf-8'))
U = ['A', 'F', 'R']
T = 1000
US = 10 ** 6


def _sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _ca(tmp_path):
    d = tmp_path / 'data' / 'rcaeval' / 're2tt_gia_na'
    d.mkdir(parents=True)
    s = lambda v: pd.array(v, dtype='string')  # noqa: E731
    tr = pd.DataFrame({'traceID': s(['t1', 't1', 't1']), 'spanID': s(['a', 'b', 'c']),
                       'parentSpanID': s([pd.NA, 'a', 'b']), 'serviceName': s(['F', 'A', 'R']),
                       'operationName': s(['F.h', 'A.h', 'R.h']),
                       'startTime': [(T + 10) * US, (T + 10) * US + 100, (T + 10) * US + 200],
                       'duration': [5000, 4000, 3000]})
    tr.to_parquet(d / 'traces.parquet', index=False)
    pd.DataFrame({'time': list(range(T - 300, T + 300)), 'R_cpu': [1.0] * 600}).to_parquet(d / 'metrics.parquet',
                                                                                       index=False)
    lg = pd.DataFrame({'timestamp': pd.array([T - 100, T + 100, T + 101], dtype='Int64'),
                       'container_name': s(['F', 'R', 'R']), 'message': s(['INFO ok', pd.NA, 'ERROR failed'])})
    lg.to_parquet(d / 'logs.parquet', index=False)
    files = {k: {'path': f'data/rcaeval/re2tt_gia_na/{k}', 'sha256': _sha(d / k)}
             for k in ('traces.parquet', 'metrics.parquet', 'logs.parquet')}
    p = tmp_path / 'allowlist.json'
    p.write_text(json.dumps({'so_ca': 1, 'cases': [{'opaque_id': 'dev-0a1b2c3d4e', 'case_dir':
                                                    'data/rcaeval/re2tt_gia_na', 'files': files}]}), encoding='utf-8')
    return p, d


def test_tien_de_parquet_string_co_NA(tmp_path):
    # tiền đề của ĐC1, ĐC2: đọc lại parquet ra kiểu `string`, giá trị rỗng là pd.NA (như 30/30 ca RE2-TT dev)
    _, d = _ca(tmp_path)
    tr = pq.read_table(d / 'traces.parquet').to_pandas()
    assert str(tr['parentSpanID'].dtype) == 'string' and tr['parentSpanID'][0] is pd.NA
    lg = pq.read_table(d / 'logs.parquet').to_pandas()
    assert str(lg['message'].dtype) == 'string' and lg['message'][1] is pd.NA


def test_DC1_parent_NA_la_span_goc(tmp_path):
    from m1 import adapter, span
    from p3 import selector
    p, _ = _ca(tmp_path)
    ca = adapter.ca_re2tt(selector.nap_allowlist(p), 'dev-0a1b2c3d4e', T, tmp_path, HOP_DONG, U)
    by = {x['spanID']: x for x in ca['spans']}
    assert by['a']['parentSpanID'] == '' and by['b']['parentSpanID'] == 'a'
    prep = span.chuan_bi(ca['spans'], t=T * US, tau=1000)
    assert prep['chan_doan']['goc'] == 1 and prep['chan_doan']['mo_coi'] == 0


def test_DC1_rong_nhan_NA():
    from m1 import adapter
    assert adapter._rong(pd.NA) and adapter._rong(None) and adapter._rong(float('nan')) and adapter._rong('')
    assert not adapter._rong('a') and not adapter._rong('<NA>')
