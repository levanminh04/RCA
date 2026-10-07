"""Evaluator P3 (§7.4–7.5, §8, §10). Chỉ chạy sau khi đầu ra đã ghi ra file; là nơi duy nhất đọc nhãn.

Biểu diễn thứ hạng thực thể: danh sách khối theo thứ tự của phương pháp. Mỗi khối có `key`
(khóa xếp hạng thật, so đúng giá trị) và `groups` (danh sách nhóm hòa bên trong khối, theo thứ
tự cố định). Các khối liền nhau cùng `key` là hòa ở cấp khối: chỉ hoán vị cả khối (TORAI, §8.4).
Phương pháp khác: mỗi nhóm hòa là một khối một nhóm, các khối có khóa khác nhau.
"""
import math
from fractions import Fraction
from math import comb

import numpy as np

KS = (1, 3, 5, 10)
TRANG_THAI = ('OK', 'NO_EVIDENCE', 'ERROR', 'TIMEOUT', 'UNSUPPORTED')


class LoiBanGhi(Exception):
    """Bản ghi không chấm được (khóa không hữu hạn, trùng thực thể...): lỗi runner, sửa trước bảng."""


def _khoa(k):
    t = tuple(float(x) for x in (k if isinstance(k, (list, tuple)) else [k]))
    if not all(math.isfinite(x) for x in t):
        raise LoiBanGhi(f'khóa không hữu hạn: {k!r}')
    return t


def khoi_tu_ban_ghi(rec):
    """Khối từ bản ghi: dùng `blocks` nếu có (TORAI), không thì nhóm `entity_ranking` theo tie_group."""
    if rec.get('blocks') is not None:
        blocks = [{'key': _khoa(b['key']), 'groups': [list(g) for g in b['groups']]} for b in rec['blocks']]
    else:
        blocks = []
        for row in rec.get('entity_ranking') or []:
            k = _khoa(row['key'])
            if blocks and blocks[-1]['tie_group'] == row['tie_group']:
                if blocks[-1]['key'] != k:
                    raise LoiBanGhi('cùng tie_group nhưng khóa khác')
                blocks[-1]['groups'][0].append(row['entity'])
            else:
                if blocks and blocks[-1]['key'] == k:
                    raise LoiBanGhi('hai tie_group liền nhau cùng khóa')
                blocks.append({'key': k, 'tie_group': row['tie_group'], 'groups': [[row['entity']]]})
    seen = [e for b in blocks for g in b['groups'] for e in g]
    if len(seen) != len(set(seen)):
        raise LoiBanGhi('thực thể trùng trong thứ hạng')
    for a, b in zip(blocks, blocks[1:]):
        if b['key'] > a['key']:
            raise LoiBanGhi('khối không giảm dần theo khóa')
    return blocks


def phan_bo_hang(blocks, root):
    """Phân bố chính xác (Fraction) của hạng root khi thứ tự trong nhóm hòa ngẫu nhiên đều
    và các khối cùng khóa hoán vị đều. Root vắng: {}."""
    pos, i = 0, 0
    while i < len(blocks):
        j = i
        while j + 1 < len(blocks) and blocks[j + 1]['key'] == blocks[i]['key']:
            j += 1
        sg = blocks[i:j + 1]
        sizes = [sum(len(g) for g in b['groups']) for b in sg]
        hit = [n for n, b in enumerate(sg) if any(root in g for g in b['groups'])]
        if hit:
            jb = hit[0]
            others = [s for n, s in enumerate(sizes) if n != jb]
            s = len(sg)
            # dp[m][w]: số tập con m khối khác (đứng trước khối root) có tổng cỡ w
            dp = [dict() for _ in range(s)]
            dp[0][0] = 1
            for size in others:
                for m in range(s - 1, 0, -1):
                    for w, c in list(dp[m - 1].items()):
                        dp[m][w + size] = dp[m].get(w + size, 0) + c
            c_truoc, g = 0, None
            for grp in sg[jb]['groups']:
                if root in grp:
                    g = len(grp)
                    break
                c_truoc += len(grp)
            dist = {}
            for m in range(s):
                tong = comb(s - 1, m)
                for w, c in dp[m].items():
                    p = Fraction(c, tong) / s
                    for q in range(1, g + 1):
                        r = pos + w + c_truoc + q
                        dist[r] = dist.get(r, 0) + p / g
            return dist
        pos += sum(sizes)
        i = j + 1
    return {}


def do_ca(dist, ok=True):
    """Độ đo một ca (kỳ vọng) và cận lạc quan/bi quan cho độ đo đơn điệu theo hạng."""
    out = {}
    if not ok or not dist:
        for k in range(1, 11):
            out[f'hit@{k}'] = 0.0
        out.update({'rr': 0.0, 'ndcg@5': 0.0, 'avg@5': 0.0, 'rank_min': None, 'rank_max': None,
                    'opt': None, 'pes': None})
        return out
    items = sorted(dist.items())
    for k in range(1, 11):
        out[f'hit@{k}'] = float(sum(p for r, p in items if r <= k))
    out['rr'] = float(sum(p / r for r, p in items))
    out['ndcg@5'] = float(sum(float(p) / math.log2(1 + r) for r, p in items if r <= 5))
    out['avg@5'] = sum(out[f'hit@{k}'] for k in range(1, 6)) / 5
    rmin, rmax = items[0][0], items[-1][0]
    out['rank_min'], out['rank_max'] = rmin, rmax

    def tai(r):
        d = {f'hit@{k}': float(r <= k) for k in range(1, 11)}
        d['rr'] = 1 / r
        d['ndcg@5'] = 1 / math.log2(1 + r) if r <= 5 else 0.0
        d['avg@5'] = sum(d[f'hit@{k}'] for k in range(1, 6)) / 5
        return d
    out['opt'], out['pes'] = tai(rmin), tai(rmax)
    return out


def cham_ca(rec, root):
    ok = rec['status'] == 'OK'
    if rec['status'] not in TRANG_THAI:
        raise LoiBanGhi(f'trạng thái lạ: {rec["status"]}')
    dist = phan_bo_hang(khoi_tu_ban_ghi(rec), root) if ok else {}
    d = do_ca(dist, ok)
    d['status'] = rec['status']
    d['root_trong_tra_ve'] = bool(dist)
    return d


def tong_hop(per_case):
    """per_case: {oid: kết quả cham_ca}. Bảng chính: trung bình; Rerank@1 là tỉ số gộp."""
    vals = list(per_case.values())
    n = len(vals)
    if n == 0:
        return {}
    out = {'n': n, 'trang_thai': {s: sum(v['status'] == s for v in vals) for s in TRANG_THAI}}
    for k in ('hit@1', 'hit@3', 'hit@5', 'avg@5', 'rr', 'ndcg@5'):
        out[k if k != 'rr' else 'mrr'] = sum(v[k] for v in vals) / n
    for K in (5, 10):
        out[f'retrieval@{K}'] = sum(v[f'hit@{K}'] for v in vals) / n
        den = sum(v[f'hit@{K}'] for v in vals)
        out[f'rerank@1(K={K})'] = None if den == 0 else sum(v['hit@1'] for v in vals) / den
    for side in ('opt', 'pes'):
        b = {}
        for k in ('hit@1', 'hit@3', 'hit@5', 'avg@5', 'rr', 'ndcg@5', 'hit@10'):
            b[k] = sum((v[side] or {}).get(k, 0.0) for v in vals) / n
        b['mrr'] = b.pop('rr')
        b['retrieval@5'], b['retrieval@10'] = b['hit@5'], b.pop('hit@10')
        out['can_' + ('lac_quan' if side == 'opt' else 'bi_quan')] = b
    return out


def theo_nhom(per_case, nhan, truong):
    nhom = {}
    for oid, v in per_case.items():
        nhom.setdefault(nhan[oid][truong], {})[oid] = v
    return {g: tong_hop(d) for g, d in sorted(nhom.items())}


def muc_ngau_nhien(rec, root, universe):
    """§8.7: theo ca trên tập quan sát O của phương pháp; kèm trên U."""
    O = rec.get('sets', {}).get('observed_entities') or []
    out = {}
    for k in (1, 3, 5, 10):
        out[f'O_hit@{k}'] = (min(k, len(O)) / len(O)) if (O and root in O) else 0.0
        out[f'U_hit@{k}'] = (min(k, len(universe)) / len(universe)) if root in universe else 0.0
    out['O_size'] = len(O)
    out['root_trong_O'] = root in O
    return out


def bon_tap(rec, universe):
    """§8.1: inventory U, tập quan sát, tập chấm (U), tập trả về (đếm riêng thực thể ngoài U)."""
    ret = [e for b in khoi_tu_ban_ghi(rec) for g in b['groups'] for e in g] if rec['status'] == 'OK' else []
    O = rec.get('sets', {}).get('observed_entities') or []
    return {'inventory': len(universe), 'quan_sat': len(O), 'quan_sat_ngoai_U': sorted(set(O) - set(universe)),
            'cham': len(universe), 'tra_ve': len(ret), 'tra_ve_ngoai_U': sorted(set(ret) - set(universe))}


def bang_rcaeval(recs, nhan, max_k=10):
    """§8.6: Evaluator RCAEval trên thứ tự gốc; bỏ trùng như main.py:560–571; ca không OK = rỗng."""
    from RCAEval.benchmark.evaluation import Evaluator
    from RCAEval.classes.graph import Node
    ev = Evaluator(max_k=max_k)
    for oid, rec in sorted(recs.items()):
        ranks = (rec.get('ranking_native') or []) if rec['status'] == 'OK' else []
        s = [Node(x.split('_')[0].replace('-db', ''), 'unknown') for x in ranks]
        s = ([s[0]] + [s[i] for i in range(1, len(s)) if s[i] not in s[:i]]) if s else []
        ev.add_case(ranks=s, answer=Node(nhan[oid]['root'], 'unknown'),
                    n_candidates=len(rec.get('sets', {}).get('observed_entities') or []) or None)
    out = {f'AC@{k}': ev.accuracy_service(k) for k in (1, 3, 5)}
    out['Avg@5'] = ev.average_service(5)
    for K in (5, 10):
        out[f'retrieval_service({K})'] = ev.retrieval_service(K)
        out[f'rerank_service(1,{K})'] = ev.rerank_service(1, K)
    out['n'] = ev.num
    return out


DO_DO_BOOT = ('hit@1', 'hit@3', 'hit@5', 'avg@5', 'rr', 'ndcg@5', 'hit@10')


def bootstrap(bang, o_cua, B=10_000, seed=20261005, alpha=0.05):
    """§8.8: lấy lại ô có hoàn lại, mỗi ô mang mọi ca của nó; ghép cặp giữa các phương pháp.

    bang: {phương pháp: {oid: kết quả cham_ca (đã trung bình theo seed nếu nhiều seed)}}.
    o_cua: {oid: ô}. Trả khoảng phân vị cho từng phương pháp và hiệu từng cặp.
    """
    methods = sorted(bang)
    oids = sorted(o_cua)
    for m in methods:
        if set(bang[m]) != set(oids):
            raise ValueError(f'bootstrap: {m} không đủ ca')
    cells = sorted(set(o_cua.values()))
    idx_cell = {c: [i for i, o in enumerate(oids) if o_cua[o] == c] for c in cells}
    rng = np.random.default_rng(seed)
    draw = rng.integers(0, len(cells), size=(B, len(cells)))
    # ma trận đếm số lần mỗi ca được lấy trong từng mẫu
    W = np.zeros((B, len(oids)))
    for ci, c in enumerate(cells):
        cnt = (draw == ci).sum(axis=1)
        for i in idx_cell[c]:
            W[:, i] += cnt
    tot = W.sum(axis=1)
    samples = {}
    for m in methods:
        s = {}
        for k in DO_DO_BOOT:
            v = np.array([bang[m][o][k] for o in oids])
            s[k] = W @ v / tot
        h1 = W @ np.array([bang[m][o]['hit@1'] for o in oids])
        for K in (5, 10):
            hk = W @ np.array([bang[m][o][f'hit@{K}'] for o in oids])
            with np.errstate(invalid='ignore', divide='ignore'):
                s[f'rerank@1(K={K})'] = np.where(hk > 0, h1 / np.where(hk > 0, hk, 1), np.nan)
        samples[m] = s

    def khoang(x):
        ok = x[~np.isnan(x)]
        lo, hi = (np.percentile(ok, [100 * alpha / 2, 100 * (1 - alpha / 2)]) if len(ok) else (None, None))
        return {'lo': None if lo is None else float(lo), 'hi': None if hi is None else float(hi),
                'n_na': int(np.isnan(x).sum())}
    out = {'B': B, 'seed': seed, 'don_vi': 'ô', 'n_o': len(cells), 'phuong_phap': {}, 'hieu': {}}
    for m in methods:
        out['phuong_phap'][m] = {k: khoang(v) for k, v in samples[m].items()}
    for a in range(len(methods)):
        for b in range(a + 1, len(methods)):
            ma, mb = methods[a], methods[b]
            out['hieu'][f'{ma} - {mb}'] = {k: khoang(samples[ma][k] - samples[mb][k]) for k in samples[ma]}
    return out


# ---------- chế độ (b): chấm phát hiện và thành công chung (§7.4–7.5) ----------

def cham_phat_hien(times, alarms, t_inj, bat_dau_danh_gia, w=60):
    """times: mảng thời điểm của bản ghi (nhịp đều); alarms: thời điểm báo động thô;
    bat_dau_danh_gia: chỉ số đầu tiên bộ phát hiện đánh giá (N-Sigma 100, BOCPD 1).
    Nhãn proxy (chỉ ở đây): bất thường = [t_inj, cuối file]."""
    times = np.asarray(times, dtype=np.int64)
    alarms = np.unique(np.asarray(alarms, dtype=np.int64))
    if len(alarms) and not np.isin(alarms, times).all():
        raise LoiBanGhi('báo động ngoài lưới thời gian của bản ghi')
    t0, T = int(times[0]), len(times)
    eval_mask = np.arange(T) >= bat_dau_danh_gia
    if len(alarms) and (alarms < int(times[bat_dau_danh_gia])).any():
        raise LoiBanGhi('báo động ở điểm bộ phát hiện chưa đánh giá')
    n_win = (T + w - 1) // w
    tp = fp = fn = tn = 0
    n_cat_ngang = 0
    bo = 0
    for k in range(n_win):
        lo, hi = k * w, min((k + 1) * w, T)
        if hi - lo < w or not eval_mask[lo:hi].all():
            bo += 1
            continue
        a, b = t0 + lo, t0 + hi
        duong = bool(((alarms >= a) & (alarms < b)).any())
        nhan_duong = a >= t_inj
        if a < t_inj < b:
            n_cat_ngang += 1
        if duong and nhan_duong:
            tp += 1
        elif duong:
            fp += 1
        elif nhan_duong:
            fn += 1
        else:
            tn += 1
    eval_times = times[eval_mask]
    normal_eval_s = int((eval_times < t_inj).sum())
    sai = int((alarms < t_inj).sum())
    dung = alarms[alarms >= t_inj]
    return {'cua_so': {'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'bo': bo, 'cat_ngang_moc': n_cat_ngang},
            'phat_hien_ca': bool(len(dung)), 'bao_dong_sai': sai, 'giay_binh_thuong_danh_gia': normal_eval_s,
            'do_tre_s': None if not len(dung) else int(dung[0] - t_inj),
            'bao_dong_dau': None if not len(alarms) else int(alarms[0])}


def thanh_cong_chung(t_hat, t_inj, rec_rca, root, k):
    """Báo động đầu ghép đúng (t_hat >= t_inj) và RCA tại đó xếp root trong top-k (quy tắc hòa §8.4)."""
    if t_hat is None or t_hat < t_inj or rec_rca is None:
        return 0.0
    return cham_ca(rec_rca, root)[f'hit@{k}']


def audit_cot(cot_moi_ca):
    """§10: số cột, cột vắng so với hợp các ca. cot_moi_ca: {oid: danh sách cột metric}."""
    hop = sorted(set().union(*map(set, cot_moi_ca.values()))) if cot_moi_ca else []
    return {'hop': len(hop), 'ca': {oid: {'so_cot': len(c), 'vang': sorted(set(hop) - set(c))}
                                    for oid, c in sorted(cot_moi_ca.items())}}
