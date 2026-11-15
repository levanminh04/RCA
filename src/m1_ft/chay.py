# -*- coding: utf-8 -*-
"""M1-FT: chạy M1 bản P7 (`src/m1`, chỉ đọc, import nguyên) với các thành phần thích nghi FlashTicket bật/tắt bằng cấu hình.

Hợp đồng (T-064 SPEC "Đầu ra", `results/T-064/hop-dong-dau-ra.md`):
- `cau_hinh_ft = {"thanh_phan": [{"ma": "<mã>", "tham_so": {...}}, ...]}`; danh sách rỗng ⇒ gọi thẳng
  `m1.chuoi.chay(*inputs)` và trả nguyên bản ghi P7 (phép kiểm tương đương: trùng SHA trên 9 ca T-062).
- Mỗi thành phần là một lớp trong `THANH_PHAN` với tối đa ba móc, áp theo thứ tự khai:
    `vao(inputs) -> inputs`        biến đổi đầu vào 7 tham số (vd. thêm cột metric, lọc thao tác nền);
    `ngu_canh()`                   context manager thay tạm hàm nội bộ của `m1` trong lúc chạy (khôi phục sau);
    `ra(rec, inputs, ctx) -> rec`  hậu xử lý bản ghi (vd. xếp hạng cạnh). Chỉ thêm khóa dưới `extra.m1_ft`
                                   hoặc sửa thứ hạng/verdict theo quy tắc đã ghi trong sổ biến thể.
- Không nhận nhãn, tên ca, đường dẫn (luật cứng 6): chỉ 7 tham số của M1 cộng cấu hình thành phần.
"""
import contextlib
import copy
import hashlib
import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from m1 import chuoi, e4, hop_dong  # noqa: E402  (cùng cách import với runner ghim T-058 trên exp-obs)

PHIEN_BAN_FT = 'M1-FT-0'
THANH_PHAN = {}  # mã -> lớp; các module thành phần tự đăng ký qua `dang_ky`


def dang_ky(cls):
    if cls.ma in THANH_PHAN:
        raise ValueError(f'trùng mã thành phần {cls.ma}')
    THANH_PHAN[cls.ma] = cls
    return cls


class ThanhPhan:
    ma = None

    def __init__(self, tham_so):
        self.tham_so = dict(tham_so or {})

    def vao(self, inputs):
        return inputs

    @contextlib.contextmanager
    def ngu_canh(self):
        yield {}

    def ra(self, rec, inputs, ctx):
        return rec


def canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def sha_cau_hinh(cau_hinh_ft):
    return hashlib.sha256(canonical(cau_hinh_ft).encode()).hexdigest()


def sha_ma_nguon():
    """sha256 của cây mã đã dùng (src/m1 + src/m1_ft, file .py theo thứ tự tên)."""
    h = hashlib.sha256()
    for goc in ('m1', 'm1_ft'):
        for p in sorted((_SRC / goc).rglob('*.py')):
            if '__pycache__' in p.parts or 'tests' in p.parts:
                continue
            h.update(p.relative_to(_SRC).as_posix().encode() + b'\0' + p.read_bytes() + b'\0')
    return h.hexdigest()


def tao_thanh_phan(cau_hinh_ft):
    _nap_module_thanh_phan()
    ds = []
    for muc in (cau_hinh_ft or {}).get('thanh_phan', []):
        if muc['ma'] not in THANH_PHAN:
            raise ValueError(f"thành phần lạ: {muc['ma']}")
        ds.append(THANH_PHAN[muc['ma']](muc.get('tham_so')))
    return ds


def _nap_module_thanh_phan():
    import importlib
    goi = _SRC / 'm1_ft' / 'thanh_phan'
    if goi.exists():
        for p in sorted(goi.glob('*.py')):
            if p.stem != '__init__':
                importlib.import_module(f'm1_ft.thanh_phan.{p.stem}')


def can_bo_sung(cau_hinh_ft):
    """Tập khóa đầu vào bổ sung mà cấu hình cần (vd. {'span_phu'})."""
    return {k for tp in tao_thanh_phan(cau_hinh_ft) if hasattr(tp, 'can_bo_sung') for k in tp.can_bo_sung()}


def dung_lai_metric(inputs, bundles, kenh_them=None):
    """Dựng lại metric + tham số nguồn từ bundle bằng `m1.adapter_flashticket.normalize_metrics` (code ghim), cho phép
    khai thêm kênh (tên → lớp của `m1.kenh.LOP_HUONG`). Bất biến nguồn/mốc/chỉ số hàng do adapter bảo đảm."""
    from m1 import adapter_flashticket as ad
    spans, metrics, logs, inventory, aliases, t, params = inputs
    goc = ad.CHANNELS
    ad.CHANNELS = dict(goc, **(kenh_them or {}))
    try:
        rows, owners, indices, clocks, coverage, m_alias, md = ad.normalize_metrics(bundles, inventory)
    finally:
        ad.CHANNELS = goc
    p = dict(params)
    p['nguon_metric'], p['chi_so_hang_metric'], p['thoi_gian_nguon'] = owners, indices, clocks
    p['coverage'] = {**{k: v for k, v in params['coverage'].items() if not k.startswith('metric:')}, **coverage}
    if kenh_them:
        ho = copy.deepcopy(params['ho_so_nguon'])
        ho['kenh_metric']['bang'] = dict(ho['kenh_metric']['bang'], **kenh_them)
        p['ho_so_nguon'] = ho
    return [spans, rows, logs, inventory, dict(aliases, **m_alias), t, p], md


def _duong_ong_metric(ds, vao, bo_sung):
    """Thành phần khai `kenh_moi()` (kênh lấy từ gói bổ sung) và/hoặc `bien_doi_bundle(bundles, vao)`; metric dựng lại
    đúng một lần sau mọi biến đổi. Không thành phần nào khai: trả nguyên đầu vào."""
    cs = [tp for tp in ds if hasattr(tp, 'kenh_moi') or hasattr(tp, 'bien_doi_bundle')]
    if not cs:
        return vao
    bundles = copy.deepcopy(bo_sung['bundles'])
    kenh = {}
    for tp in cs:
        if hasattr(tp, 'kenh_moi'):
            km = tp.kenh_moi()
            kenh.update(km)
            bundles += [copy.deepcopy(b) for b in bo_sung.get('bundles_bo_sung', []) if b['channel'] in km]
    for tp in ds:  # H8-adapter (phiên C): nối chuỗi container trước mọi biến đổi khác; vắng thì không làm gì
        if hasattr(tp, 'bien_doi_goi_ghim'):
            bundles = tp.bien_doi_goi_ghim(bundles, vao[3], nhan='duong_ong')
    for tp in cs:
        if hasattr(tp, 'bien_doi_bundle'):
            bundles = tp.bien_doi_bundle(bundles, vao)
    moi, md = dung_lai_metric(vao, bundles, kenh)
    for tp in cs:
        tp.chan_doan_metric = {'unmapped': len(md.get('unmapped_series', [])), 'empty': md.get('empty_queries', [])}
    return moi


def chay(inputs, cau_hinh_ft=None, ban=None, bo_sung=None):
    """inputs = [spans, metrics, logs, inventory, aliases, t, params] (như method-input.json của P7).
    bo_sung: đầu vào kỹ thuật thêm (không nhãn), vd. {'span_phu': bo_sung.span_phu(...)}; chỉ thành phần cần mới đọc."""
    ds = tao_thanh_phan(cau_hinh_ft)
    for tp in ds:
        if hasattr(tp, 'bo_sung'):
            tp.bo_sung = bo_sung
    chuoi.CACHE = e4.CacheCong()  # như runner ghim: mỗi lần chạy một cache mới
    if not ds:
        return chuoi.chay(*inputs)
    vao = copy.deepcopy(inputs)
    vao = _duong_ong_metric(ds, vao, bo_sung or {})
    for tp in ds:
        vao = tp.vao(vao)
    ctxs = {}
    with contextlib.ExitStack() as st:
        for tp in ds:
            ctxs[tp.ma] = st.enter_context(tp.ngu_canh())
        rec = chuoi.chay(*vao)
    for tp in ds:
        rec = tp.ra(rec, vao, ctxs.get(tp.ma))
    ft = rec.setdefault('extra', {}).setdefault('m1_ft', {})
    ft.update({'ban': ban, 'phien_ban': PHIEN_BAN_FT, 'cau_hinh_sha256': sha_cau_hinh(cau_hinh_ft),
               'ma_nguon_sha256': sha_ma_nguon(), 'thanh_phan_bat': [tp.ma for tp in ds]})
    rec['variant'] = ban or rec.get('variant')
    if rec.get('status') == 'OK':
        hop_dong.kiem_ban_ghi(rec)
    json.dumps(rec, allow_nan=False)
    return rec
