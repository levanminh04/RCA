"""Bản ghi mỗi lượt (§13) và ánh xạ về thực thể (§8.2). Không có trường nhãn."""
import math

CAM = ('root', 'fault', 'cell', 'case', 'label', 'nhan', 'answer', 'inject_time', 'opaque_id_path')


def thuc_the_metric(col):
    """Tiền tố trước '_' đầu tiên (main.py:560; '-db' không xuất hiện trên RE2-TT)."""
    return col.split('_')[0]


def _khoa(k):
    t = tuple(float(x) for x in (k if isinstance(k, (list, tuple)) else (k,)))
    if not all(math.isfinite(x) for x in t):
        raise ValueError(f'khóa không hữu hạn: {k!r}')
    return t


def xep_thuc_the(items):
    """items: [(item, entity, key)] theo thứ tự gốc của phương pháp.

    Điểm thực thể = khóa cao nhất của các phần tử của nó. Sắp giảm dần theo khóa; hòa khi khóa bằng
    nhau đúng giá trị; trong nhóm hòa giữ thứ tự xuất hiện đầu (chỉ để hiển thị).
    """
    best, first = {}, {}
    for i, (_, ent, key) in enumerate(items):
        k = _khoa(key)
        if ent not in best or k > best[ent]:
            best[ent] = k
        first.setdefault(ent, i)
    ents = sorted(best, key=lambda e: first[e])
    ents = sorted(ents, key=lambda e: best[e], reverse=True)  # sort ổn định
    out, g = [], -1
    for i, e in enumerate(ents):
        if i == 0 or best[e] != best[ents[i - 1]]:
            g += 1
        out.append({'entity': e, 'key': list(best[e]), 'tie_group': g})
    return out


def tao(method, method_version, variant, mode, ket_qua, window, config_id, why_ids,
        seed=None, hashseed=None, detector=None, detector_columns=None, run_id=None, opaque_id=None):
    """Gộp kết quả adapter thành bản ghi §13. opaque_id chỉ để runner nối file; phương pháp không nhận."""
    items = ket_qua.get('items') or []
    status = ket_qua['status']
    if status == 'OK' and not items and not ket_qua.get('blocks'):
        raise ValueError('OK nhưng danh sách rỗng')
    rec = {
        'run_id': run_id, 'opaque_id': opaque_id, 'method': method, 'method_version': method_version,
        'variant': variant, 'mode': mode, 'detector': detector, 'detector_columns': detector_columns,
        'seed': seed, 'hashseed': hashseed, 'config_id': config_id, 'why_ids': list(why_ids),
        'window': window,
        'input_shape': ket_qua.get('input_shape', {}),
        'status': status, 'method_status_raw': ket_qua.get('method_status_raw'), 'error': ket_qua.get('error'),
        'ranking_native': ket_qua.get('ranking_native') or [],
        'ranking': [{'item': it, 'entity': e, 'key': list(_khoa(k))} for it, e, k in items],
        'entity_ranking': xep_thuc_the(items) if items else [],
        'blocks': ket_qua.get('blocks'),
        'sets': {},
        'diagnostics': ket_qua.get('diagnostics', {}),
        'extra': ket_qua.get('extra', {}),
        'cost': {},
        'input_sha256': {},
    }
    if rec['blocks'] is not None:
        rec['entity_ranking'] = [{'entity': e, 'key': list(_khoa(b['key'])), 'tie_group': bi}
                                 for bi, b in enumerate(rec['blocks']) for grp in b['groups'] for e in grp]
    obs = sorted(set(ket_qua.get('observed_entities') or []))
    ret = [r['entity'] for r in rec['entity_ranking']]
    rec['sets'] = {'observed': len(obs), 'observed_entities': obs, 'returned': len(ret)}
    kiem(rec)
    return rec


def kiem(rec):
    """Không trường nhãn; trường bắt buộc có mặt."""
    def walk(d, path=''):
        if isinstance(d, dict):
            for k, v in d.items():
                if k in CAM:
                    raise ValueError(f'bản ghi chứa trường nhãn: {path}{k}')
                walk(v, f'{path}{k}.')
    walk({k: v for k, v in rec.items() if k != 'opaque_id'})
    for k in ('method', 'variant', 'mode', 'status', 'window', 'ranking_native', 'entity_ranking', 'sets'):
        if k not in rec:
            raise ValueError(f'thiếu trường {k}')
