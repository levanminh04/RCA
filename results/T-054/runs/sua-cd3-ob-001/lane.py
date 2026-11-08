"""T-054 luồng C-d3 OB (Minh duyệt 08/11/2026). Không sửa file đã ghim; chỉ nạp chúng.

Wrapper: chuẩn hóa dấu span gốc Nezha `ParentID = "root"` thành parent rỗng NGAY SAU adapter đã ghim
(`src/m1/adapter.py::ca_nezha`), trước khi spans vào lõi M1. Ngoài trường `parentSpanID` của span mang đúng
giá trị "root", mọi thứ giữ nguyên.

Đường đọc dữ liệu giống `results/T-054/scripts/worker.py` nhánh M1 Nezha-OB (ob_selection + patch chon_ca,
layout source_native). Phép dựng tập span gốc trong A sao đúng `src/m1/chuoi.py` dòng 296–307 và 617.
"""
import copy
import json
import os
import sys
from pathlib import Path
from unittest.mock import patch

GOC = Path(os.environ.get('T054_ROOT', Path(__file__).resolve().parents[4]))
for p in (GOC / 'src', GOC / 'results/T-054/scripts'):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from bien_nhan import fingerprint  # noqa: E402
from nguon import source_row  # noqa: E402

DAU_GOC = 'root'


def them_pythonpath(ds):
    """Như worker.setup: nối pythonpath của job (thư viện phụ, vd drain3) sau src."""
    for p in ds:
        if p not in sys.path:
            sys.path.append(p)


def chuan_hoa_root(data):
    """Trả bản sao data, đổi parentSpanID == 'root' thành ''. Đếm số span đổi."""
    out = dict(data)
    spans, n = [], 0
    for s in data['spans']:
        if s['parentSpanID'] == DAU_GOC:
            s = dict(s, parentSpanID='')
            n += 1
        spans.append(s)
    out['spans'] = spans
    return out, n


def doc_ca(row, opaque_id, inventory, contract, data_root, sua):
    """Đọc một ca OB như worker; sua=True áp wrapper."""
    from m1 import adapter
    from p3 import nezha
    files = source_row(row, data_root)
    selection = {'opaque_id': opaque_id, 'view': 'main', 't_ns': row['t_ns'],
                 'trace_guard_s': row['trace_guard_s'],
                 'files': {k: dict(row['files'][k], absolute_path=v) for k, v in files.items()},
                 'universe': inventory, 'aliases': dict(nezha.POD_ALIASES)}
    with patch('m1.adapter.nezha.chon_ca', return_value=selection):
        data = adapter.ca_nezha({}, opaque_id, data_root, contract, inventory=inventory, layout='source_native')
    n = 0
    if sua:
        data, n = chuan_hoa_root(data)
    return data, n


def params_m1(config, data):
    from m1 import runner, chuoi
    params = runner._params(config, data)
    params['tach_cd3'] = True
    chuoi._kiem_params(params)
    return params


def chay_m1(data, t, params):
    """Chạy chuỗi M1 đúng như worker (CACHE mới, kiểm bản ghi theo hợp đồng)."""
    from m1 import chuoi, e4, hop_dong
    args = [data['spans'], data['metrics'], data['logs'], data['inventory'], data['aliases'], t, params]
    chuoi.CACHE = e4.CacheCong()
    raw = chuoi.chay(*args)
    hop_dong.kiem_ban_ghi(raw)
    return raw


def spans_A_goc(data, t, params):
    """Sao chuoi.py 296–307 (miền span, alias, chuan_bi) và 617 (span A, parent None nếu gốc không mồ côi)."""
    from m1 import chuoi, span
    aliases = data['aliases']
    he_span = chuoi._he_so_ns(params['don_vi_thoi_gian']['spans.start_us'])
    t_ns = int(round(t * chuoi.NS))
    lo_ns, hi_ns = t_ns - 300 * chuoi.NS, t_ns + 300 * chuoi.NS
    rows = []
    for r in data['spans']:
        st = r['start_us'] * he_span
        en = (r['start_us'] + r['duration_us']) * he_span
        if st >= lo_ns and en < hi_ns:
            rows.append(dict(r, owner=chuoi._alias(aliases, r['owner'])))
    prep = span.chuan_bi(rows, t=t_ns / he_span, tau=10 ** 6 / he_span, tinh_CP=False)
    if prep['loi']:
        raise RuntimeError('span lỗi: ' + str(prep.get('ly_do')))
    return [{'parent': None if (s['cha'] is None and not s['mo_coi']) else 'co', 'chu': s['chu']}
            for s in prep['spans'].values() if s['phia'] == 'A'], prep['chan_doan']


def cd3_tu_luu(extra, spans_A):
    """C-d3 từ trung gian đã lưu của bản ghi M1 + span A dựng lại."""
    from fractions import Fraction
    from m1 import doi_chung
    lan_nguoc = sorted({k['thuc_the'] for k in extra['kenh_co'] if k['lop'] == 'lan_nguoc'})
    dich = doi_chung.dich_cd3(spans_A, lan_nguoc)
    diem = {e: Fraction(*v) for e, v in extra['dau_vao_cd3']['diem'].items()}
    kq = doi_chung.cd3([tuple(e) for e in extra['canh']], diem, dich)
    return {'dich': dich, 'so_span_goc_A': sum(1 for s in spans_A if s['parent'] is None),
            'lan_nguoc': lan_nguoc, 'cd3': kq}


def dump(o):
    from fractions import Fraction

    def f(x):
        if isinstance(x, Fraction):
            return [x.numerator, x.denominator]
        if isinstance(x, (set, tuple)):
            return list(x)
        raise TypeError(type(x))
    return json.dumps(o, ensure_ascii=False, sort_keys=True, default=f)
