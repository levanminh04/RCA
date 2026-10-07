"""CIRCA đồ thị kiến trúc (§6.5, WHY-30). RHT + DA (θ = 3) làm chính, kèm RHT-only cùng lượt.

Mô hình: 'ols' gọi `src/circa_kien_truc/scoring.score_graph` nguyên trạng (LinearRegression);
'svr' dùng `RHTScorer(regressor=ANMRegressor(regressor=SVR(kernel="sigmoid")))` của RCAEval,
không sửa code (K-SVR1). Route hồi quy từng nút ghi như scoring.py:44–57 cho cả hai mô hình.
Đồ thị gọi dựng từ span có startTime >= t-300 và kết thúc < t (D3). `current` = điểm quan sát
thật cuối cùng của metric trong A (D3). Builder chạy với PYTHONHASHSEED do runner đặt.
"""
import copy
import os
import sys
from datetime import timedelta

import networkx as nx

from ..ban_ghi import thuc_the_metric
from ..cua_so import doi_ten_latency, tien_xu_ly_main, US
from . import LoiRunner, loi

CIRCA_SRC = 'D:/RCA-ext/work/T-014/CIRCA'
VERSION = 'src/circa_kien_truc + RCAEval 259ea41 RHT/DA; CIRCA 0215e18'
MO_HINH = ('svr', 'ols')


def chuan_bi(metric_win):
    """Như T-014 run_examples.py:13–16, nhưng cắt trước (D1): tiền xử lý main.py, đổi tên, preprocess."""
    from RCAEval.io.time_series import preprocess
    raw = doi_ten_latency(tien_xu_ly_main(metric_win))
    clean = preprocess(raw.copy(), dataset='re2-tt')
    clean['time'] = raw['time'].to_numpy()
    return clean


def do_thi(columns, spans, t, circa_src=CIRCA_SRC):
    from circa_kien_truc import build_graph, service_calls
    st = spans['startTime'].astype('int64')
    en = st + spans['duration'].astype('int64')
    pre = spans.loc[(st >= (t - 300) * US) & (en < t * US)]
    calls, rep_calls = service_calls(pre, t)
    graph, rep = build_graph(columns, calls, circa_src, retain_isolates=True)
    return graph, {'calls': {k: v for k, v in rep_calls.items()}, 'graph': {
        k: rep[k] for k in ('metric_nodes', 'metric_edges', 'dag', 'call_dag', 'meta_dag', 'nontrivial_scc')},
        'call_edges': rep['call_edges'], 'spans_do_thi': int(len(pre))}


def _svr():
    from sklearn.svm import SVR
    return SVR(kernel='sigmoid')


def cham_svr(frame, graph, detect_time, current, da_threshold=3, tao_hoi_quy=_svr, ten_route='svr_regression'):
    """Bản của score_graph với hồi quy SVR(sigmoid) bọc ANMRegressor; còn lại giữ nguyên dòng lệnh.
    `tao_hoi_quy` chỉ để test: với LinearRegression phải cho đúng đầu ra của score_graph."""
    from RCAEval.classes.graph import Node, MemoryGraph
    from RCAEval.classes.data import CaseData, MemoryDataLoader
    from RCAEval.graph_heads.rht import RHTScorer, DAScorer, ANMRegressor
    from circa_kien_truc.builder import metric_mapping
    mapped = {r['column']: r for r in metric_mapping(graph.nodes)}
    if any(r['status'] != 'mapped' for r in mapped.values()):
        raise ValueError('Unmapped metric in scoring graph')
    nodes = {name: Node(mapped[name]['service'], mapped[name]['metric']) for name in graph.nodes}
    converted = nx.DiGraph(); converted.add_nodes_from(nodes.values())
    converted.add_edges_from((nodes[a], nodes[b]) for a, b in graph.edges)
    mg = MemoryGraph(converted); byname = {v: k for k, v in nodes.items()}
    raw = {}
    for name, node in nodes.items():
        if name in frame:
            raw.setdefault(node.entity, {})[node.metric] = list(zip(frame.time, frame[name]))
    if not nodes:
        return dict(nodes={}, da={}, ranks=[], ranks_da=[])
    case = CaseData(MemoryDataLoader(raw), sli=nodes[sorted(nodes)[0]], detect_time=detect_time,
                    interval=timedelta(seconds=1))
    series = case.load_data(mg, current)
    scorer = RHTScorer(regressor=ANMRegressor(regressor=tao_hoi_quy()))
    scores = scorer.score(mg, case, current)
    snaps = {}
    for node, score in scores.items():
        parents = list(mg.parents(node)); px, tx, py, ty = scorer.split_data(series, node, parents, case)
        route, err = ('no_effective_parents', None) if len(px) == 0 else (ten_route, None)
        if len(px):
            try:
                m = tao_hoi_quy().fit(px, py); m.predict(px); m.predict(tx)
            except ValueError as exc:
                route, err = 'value_error_fallback', str(exc)
        snaps[byname[node]] = dict(rht_score=float(score.score), regression_route=route, regression_error=err,
                                   parents=[byname[p] for p in parents if p in series])
    da_scorer = DAScorer(threshold=da_threshold)
    adjusted = da_scorer.score(mg, case, current, copy.deepcopy(scores))
    ranks = sorted([[byname[n], float(s.score)] for n, s in scores.items()], key=lambda x: (-x[1], x[0]))
    ranks_da = sorted([[byname[n], float(s.score), list(s.key)] for n, s in adjusted.items()],
                      key=lambda x: tuple(-v for v in x[2]) + (x[0],))
    return dict(nodes=snaps, ranks=ranks, ranks_da=ranks_da)


def cham(frame, graph, t, current, mo_hinh):
    if mo_hinh == 'ols':
        from circa_kien_truc.scoring import score_graph
        s = score_graph(frame, graph, t, current)
        nodes = {k: dict(rht_score=v['rht_score'], regression_route=v['regression_route'],
                         regression_error=v['regression_error'], parents=v['parents']) for k, v in s['nodes'].items()}
        return dict(nodes=nodes, ranks=s['ranks'], ranks_da=s['ranks_da'])
    if mo_hinh == 'svr':
        return cham_svr(frame, graph, t, current)
    raise ValueError(mo_hinh)


def chay(metric_win, spans, t, mo_hinh):
    """Trả danh sách hai kết quả: [RHT+DA, RHT-only] từ cùng một lượt."""
    if mo_hinh not in MO_HINH:
        raise LoiRunner(f'mô hình CIRCA lạ: {mo_hinh}')
    shape = {'metric_cols': int(metric_win.shape[1] - 1), 'metric_cols_after_preprocess': None, 'spans': int(len(spans))}
    try:
        clean = chuan_bi(metric_win)
        shape['metric_cols_after_preprocess'] = int(clean.shape[1] - 1)
        graph, grep = do_thi([c for c in clean.columns if c != 'time'], spans, t)
        A = clean[clean['time'] >= t]
        if A.empty:
            raise ValueError('không có điểm quan sát trong A')
        current = int(A['time'].max())
        snap = cham(clean, graph, t, current, mo_hinh)
    except Exception as exc:  # noqa: BLE001
        r = loi(exc); r['input_shape'] = shape
        return [dict(r, variant=f'{mo_hinh}+rht_da'), dict(r, variant=f'{mo_hinh}+rht')]
    routes = {}
    for v in snap['nodes'].values():
        routes[v['regression_route']] = routes.get(v['regression_route'], 0) + 1
    diag = {'regression_routes': routes, 'value_error_fallback_nodes': sorted(
        [k for k, v in snap['nodes'].items() if v['regression_route'] == 'value_error_fallback']),
        'graph': grep['graph'], 'calls': grep['calls'], 'spans_do_thi': grep['spans_do_thi'],
        'hashseed': os.environ.get('PYTHONHASHSEED'), 'circa_current': current,
            'nodes': snap['nodes']}
    obs = sorted({thuc_the_metric(n) for n in snap['nodes']})
    da_items = [(n, thuc_the_metric(n), tuple(k)) for n, _, k in snap['ranks_da']]
    rht_items = [(n, thuc_the_metric(n), (s,)) for n, s in snap['ranks']]
    base = {'method_status_raw': None, 'error': None, 'observed_entities': obs, 'input_shape': shape,
            'diagnostics': diag, 'extra': {'call_edges': grep['call_edges']}}
    return [dict(base, variant=f'{mo_hinh}+rht_da', status='OK' if da_items else 'NO_EVIDENCE',
                 items=da_items, ranking_native=[n for n, *_ in snap['ranks_da']]),
            dict(base, variant=f'{mo_hinh}+rht', status='OK' if rht_items else 'NO_EVIDENCE',
                 items=rht_items, ranking_native=[n for n, _ in snap['ranks']])]
