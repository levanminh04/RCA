"""E3 — log theo mẫu Drain (SPEC T-043 B2 E3; đặc tả v1 §5, §7.3; Đ15; dinh-chinh-cai-dat.md CĐ4).

- Chuỗi vào Drain: Nezha-OB theo quy tắc chung (khóa `log`; nếu `log` là JSON có `message` kiểu chuỗi thì dùng
  `message`); RE2-TT dùng `message` nguyên văn (CĐ4.1).
- Che token theo thứ tự UUID → IP → HEX → NUM, ranh giới không dính chữ hoặc số; không che chuỗi trong ngoặc
  (đổi thiết kế, CĐ4.3); tắt phần che sẵn của drain3.
- Một Drain chung cho mọi thực thể, học trên dòng N quan sát được theo thứ tự (mốc, thực thể, nội dung) (CĐ4.4;
  Đ15 điểm 5). drain3 0.9.11: độ sâu 4, ngưỡng 0,4, max_children 100, max_clusters không giới hạn, extra_delimiters
  rỗng, parametrize_numeric_tokens True (CĐ4.5–4.6).
- Lớp của cặp (thực thể, mẫu) theo phiếu ở N (Đ15 điểm 3): không phiếu → không xác định; n_lỗi >= n_không → lỗi;
  còn lại thường. Mẫu đã biết của thực thể: có ít nhất một dòng N của thực thể (Đ15 điểm 5).
- Khớp dòng A (CĐ4.2), chỉ trên mẫu đã biết của thực thể: (a) 'hoan_toan' như Drain.match(fallback); (b) 'nguong'
  như Drain.tree_search; (c) 'nguong_cung_lop' như (b) nhưng chỉ xét mẫu cùng lớp với dòng. Không khớp: ô mẫu mới.
"""
import json
import re

from drain3.drain import Drain

_UUID = re.compile(r'(?<![A-Za-z0-9])[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
                   r'(?![A-Za-z0-9])')
_IP = re.compile(r'(?<![A-Za-z0-9])(?:\d{1,3}\.){3}\d{1,3}(?::\d{1,5})?(?![A-Za-z0-9])')
_HEX = re.compile(r'(?<![A-Za-z0-9])(?:0[xX][0-9a-fA-F]+|(?=[0-9a-fA-F]*[0-9])(?=[0-9a-fA-F]*[a-fA-F])[0-9a-fA-F]{8,})'
                  r'(?![A-Za-z0-9])')
_NUM = re.compile(r'(?<![A-Za-z0-9])[+-]?\d+(?:\.\d+)?(?![A-Za-z0-9])')

LOI, KHONG_LOI, UNKNOWN = 'LOI', 'KHONG_LOI', 'UNKNOWN'


def che_token(msg):
    s = _UUID.sub('<UUID>', msg)
    s = _IP.sub('<IP>', s)
    s = _HEX.sub('<HEX>', s)
    return _NUM.sub('<NUM>', s)


def chuoi_vao_drain_nezha(cot_log):
    """CĐ4.1: lấy `log` của JSON ngoài; nếu `log` giải mã được thành object có `message` kiểu chuỗi thì dùng
    `message`, không thì dùng `log`; JSON ngoài không giải mã được thì dùng nguyên chuỗi. Không gọi tên dịch vụ."""
    try:
        ngoai = json.loads(cot_log)
    except (TypeError, ValueError):
        return cot_log
    if not isinstance(ngoai, dict) or not isinstance(ngoai.get('log'), str):
        return cot_log
    log = ngoai['log']
    try:
        trong = json.loads(log)
    except (TypeError, ValueError):
        return log
    if isinstance(trong, dict) and isinstance(trong.get('message'), str):
        return trong['message']
    return log


def lop_dong_tu_khoa(noi_dung, tu_khoa):
    """RE2-TT: bộ từ khóa SimpleRCA, không phân biệt hoa thường, tìm chuỗi con (src/simplerca/core.py:22, 87)."""
    rx = re.compile('|'.join(re.escape(x) for x in tu_khoa), re.IGNORECASE)
    return LOI if rx.search(noi_dung or '') else KHONG_LOI


def _lop_dong(d, quy_tac):
    if d.get('lop') is not None:
        return d['lop']
    if quy_tac['kieu'] == 'tu_khoa':
        return lop_dong_tu_khoa(d['noi_dung'], quy_tac['tu_khoa'])
    from m1.kenh import chuan_hoa_severity
    return chuan_hoa_severity(d.get('severity_raw'), quy_tac)


def _la(drain, tokens):
    """Nút lá của cây tiền tố cho chuỗi token, như Drain.tree_search của drain3 0.9.11 (không chấm)."""
    n = len(tokens)
    cur = drain.root_node.key_to_child_node.get(str(n))
    if cur is None:
        return None
    if n == 0:
        return cur
    depth = 1
    for tok in tokens:
        if depth >= drain.max_node_depth or depth == n:
            break
        nxt = cur.key_to_child_node.get(tok)
        if nxt is None:
            nxt = cur.key_to_child_node.get(drain.param_str)
        if nxt is None:
            return None
        cur = nxt
        depth += 1
    return cur


def _khop(drain, tokens, ung_vien, khop, sim_th):
    """Khớp một dòng A với tập mẫu ứng viên (mẫu đã biết của thực thể, có thể lọc theo lớp)."""
    if not ung_vien:
        return None
    la = _la(drain, tokens)
    trong_la = sorted(set(la.cluster_ids) & ung_vien) if la is not None else []
    if khop == 'hoan_toan':
        c = drain.fast_match(trong_la, tokens, 1.0, True) if trong_la else None
        if c is None:  # full_search_strategy="fallback": mọi mẫu cùng số token
            cung_do_dai = sorted(set(drain.get_clusters_ids_for_seq_len(len(tokens))) & ung_vien)
            c = drain.fast_match(cung_do_dai, tokens, 1.0, True) if cung_do_dai else None
        return c
    return drain.fast_match(trong_la, tokens, sim_th, False) if trong_la else None


def hoc_va_dem(dong_N, dong_A, tham_so_E3, quy_tac):
    """dong_*: [{'moc', 'thuc_the', 'noi_dung', 'lop' (LOI | KHONG_LOI | UNKNOWN | None), 'severity_raw'?}].
    Trả cặp (thực thể, mã mẫu) với lớp, phiếu, số dòng N/A; số dòng A vào ô mẫu mới theo thực thể."""
    khop = tham_so_E3['khop']  # CĐ5: không có mặc định; chuoi._kiem_params kiểm trước
    if khop not in ('hoan_toan', 'nguong', 'nguong_cung_lop'):
        raise ValueError(f'cách khớp lạ: {khop}')
    sim_th = float(tham_so_E3['sim_th'])
    drain = Drain(depth=int(tham_so_E3['do_sau']), sim_th=sim_th, max_children=100, max_clusters=None,
                  extra_delimiters=(), parametrize_numeric_tokens=True)
    cap = {}
    biet = {}
    for d in sorted(dong_N, key=lambda x: (x['moc'], x['thuc_the'], x['noi_dung'])):
        cl, _ = drain.add_log_message(che_token(d['noi_dung']))
        e, cid = d['thuc_the'], cl.cluster_id
        biet.setdefault(e, set()).add(cid)
        c = cap.setdefault((e, cid), {'n_N': 0, 'n_A': 0, 'phieu_loi': 0, 'phieu_khong': 0, 'unknown_N': 0,
                                      'unknown_A': 0, 'loi_xac_dinh_N': 0, 'loi_xac_dinh_A': 0})
        c['n_N'] += 1
        lop = _lop_dong(d, quy_tac)
        if lop == LOI:
            c['phieu_loi'] += 1
            c['loi_xac_dinh_N'] += 1
        elif lop == KHONG_LOI:
            c['phieu_khong'] += 1
        else:
            c['unknown_N'] += 1
    for k, c in cap.items():
        if c['phieu_loi'] + c['phieu_khong'] == 0:
            c['lop'] = 'khong_xac_dinh'
        elif c['phieu_loi'] >= c['phieu_khong']:
            c['lop'] = 'loi'
        else:
            c['lop'] = 'thuong'
    mau_moi = {}
    for d in sorted(dong_A, key=lambda x: (x['moc'], x['thuc_the'], x['noi_dung'])):
        e = d['thuc_the']
        tokens = drain.get_content_as_tokens(che_token(d['noi_dung']))
        lop = _lop_dong(d, quy_tac)
        ung = set(biet.get(e, set()))
        if khop == 'nguong_cung_lop' and lop != UNKNOWN:
            can = 'loi' if lop == LOI else 'thuong'
            ung = {cid for cid in ung if cap[(e, cid)]['lop'] == can}
        cl = _khop(drain, tokens, ung, khop, sim_th)
        if cl is None:
            mau_moi[e] = mau_moi.get(e, 0) + 1
            continue
        c = cap[(e, cl.cluster_id)]
        c['n_A'] += 1
        if lop == LOI:
            c['loi_xac_dinh_A'] += 1
        elif lop == UNKNOWN:
            c['unknown_A'] += 1
    mau = {cl.cluster_id: cl.get_template() for cl in drain.clusters}
    return {'cap': cap, 'mau_moi': mau_moi, 'mau': mau, 'thuc_the_N': sorted(biet)}
