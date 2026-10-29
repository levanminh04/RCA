"""Kiểm tĩnh (SPEC T-044 tiêu chí 4; luật cứng 6): src/m1 không import m1_danh_gia, không đọc đường dẫn nhãn."""
import ast
import inspect
from pathlib import Path

from conftest import ROOT

M1 = ROOT / 'src' / 'm1'
CAM_CHUOI = ('nhan-dev', 'nhan.json', 'nap_moc', 'data/locked', 'm1_danh_gia', 'ground_truth')


def _tep():
    return sorted(M1.rglob('*.py'))


def test_khong_import_bo_danh_gia(ma):
    ma('tinh-import')
    xau = []
    for p in _tep():
        cay = ast.parse(p.read_text(encoding='utf-8'))
        for n in ast.walk(cay):
            if isinstance(n, ast.Import):
                ten = [a.name for a in n.names]
            elif isinstance(n, ast.ImportFrom):
                ten = [n.module or ''] + [f'{n.module}.{a.name}' for a in n.names]
            else:
                continue
            for t in ten:
                if t.startswith('m1_danh_gia') or t in ('p3.nhan',) or t.endswith('.nhan') and t.startswith('p3'):
                    xau.append((p.name, t))
    assert not xau, xau


def _hang_chuoi_trong_ma(cay):
    """Hằng chuỗi trong mã, bỏ docstring (docstring được phép nhắc tên để giải thích luật)."""
    doc = set()
    for n in ast.walk(cay):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and n.body:
            d = n.body[0]
            if isinstance(d, ast.Expr) and isinstance(d.value, ast.Constant) and isinstance(d.value.value, str):
                doc.add(id(d.value))
    return [n.value for n in ast.walk(cay)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in doc]


def test_khong_doc_duong_dan_nhan(ma):
    ma('tinh-duong-dan')
    xau = []
    for p in _tep():
        for s in _hang_chuoi_trong_ma(ast.parse(p.read_text(encoding='utf-8'))):
            xau += [(p.name, c) for c in CAM_CHUOI if c in s]
    assert not xau, xau


def test_api_bay_tham_so(ma):
    """hop-dong.json#/vao/tham_so_duy_nhat: spans, metrics, logs, inventory, aliases, t, params."""
    from m1 import chuoi
    from conftest import T043, _doc
    ma('tinh-api')
    ts = list(inspect.signature(chuoi.chay).parameters)
    assert ts == _doc(T043 / 'hop-dong.json')['vao']['tham_so_duy_nhat']
