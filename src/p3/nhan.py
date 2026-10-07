"""Đọc nhan-dev.json theo hai vai tách bạch (§3, §4).

- nap_moc: runner chế độ (a) chỉ lấy mốc tiêm. Không trả root, loại lỗi, ô, tên ca.
- nap_nhan: chỉ evaluator gọi, sau khi đầu ra đã ghi ra file.
"""
import json

TRUONG_NHAN = ('root', 'fault', 'cell', 'nhom_vi_tri_p75', 'inject_time')


def _doc(path):
    with open(path, encoding='utf-8') as f:
        doc = json.load(f)
    cases = doc['cases']
    if doc.get('so_ca') != len(cases):
        raise ValueError('nhãn: so_ca không khớp')
    return cases


def nap_moc(path):
    out = {}
    for c in _doc(path):
        t = c['inject_time']
        if not isinstance(t, int):
            raise ValueError('mốc tiêm phải là giây nguyên')
        out[c['opaque_id']] = t
    return out


def nap_nhan(path):
    return {c['opaque_id']: {k: c[k] for k in TRUONG_NHAN} for c in _doc(path)}
