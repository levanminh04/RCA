"""T-014: kiểm scorer CIRCA gốc với cùng đồ thị và dữ liệu RCAEval.

Hai ca được chọn trước khi chạy: fse-ob/cartservice_cpu/1 và
fse-ob/cartservice_mem/1; không chọn theo thứ hạng. Không gọi main.py,
không đưa tên ca/nhãn vào scorer. Kho dữ liệu và thư viện chỉ đọc.
"""
from __future__ import annotations

import csv
from datetime import datetime, timedelta
import importlib
import inspect
import json
import os
from pathlib import Path
import sys
import time
import traceback

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.dont_write_bytecode = True
sys.path.insert(0, "D:/RCA-ext/work/T-014/CIRCA")

OUT = Path(__file__).resolve().parent
PROGRESS = OUT / "progress.log"


def log(message):
    line = f"{datetime.now().isoformat()} {message}"
    print(line, flush=True)
    with PROGRESS.open("a", encoding="utf-8") as stream:
        stream.write(line + "\n")


def write_json(name, value):
    (OUT / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")


log("START imports; machine shared: elapsed is diagnostic only")
import networkx as nx
import numpy as np
import pandas as pd
from RCAEval.classes.data import CaseData, MemoryDataLoader
from RCAEval.classes.graph import MemoryGraph, Node
from RCAEval.graph_construction.pc import pc_default
from RCAEval.graph_heads.rht import RHTScorer, rht
from RCAEval.io.time_series import preprocess
from circa.alg.ci import RHTScorer as OriginalRHT
from circa.model.case import CaseData as OriginalCaseData
from circa.model.data_loader import MemoryDataLoader as OriginalLoader
from circa.model.graph import MemoryGraph as OriginalGraph, Node as OriginalNode

log("IMPORTS_OK original RHT imported without optional R/pgmpy dependencies")


def data_for_case(relative):
    path = Path("D:/RCA-ext/data/fse-ob") / relative / "simple_data.csv"
    df = pd.read_csv(path).drop(columns=["time.1"], errors="ignore")
    df = df.loc[:, ~df.columns.str.endswith("_latency-50")]
    df = df.replace([np.inf, -np.inf], np.nan).ffill().fillna(0)
    inject_time = int((path.parent / "inject_time.txt").read_text().strip())
    df = pd.concat([df[df.time < inject_time].tail(300), df[df.time >= inject_time].head(300)], ignore_index=True)
    df = df.rename(columns={c: c.replace("_latency-90", "_latency") for c in df if c.endswith("_latency-90")})
    times = df.time
    df = preprocess(df, dataset="fse-ob", dk_select_useful=False)
    df["time"] = times
    return df, inject_time, path


def graph_from_adj(adj, columns, node_class):
    nodes = [node_class(*name.split("_")[:2]) for name in columns]
    graph = nx.DiGraph()
    for a in range(len(adj)):
        for b in range(len(adj)):
            if adj[a, b] == adj[b, a] == 0:
                continue
            if adj[a, b] == adj[b, a] == -1:
                graph.add_edge(nodes[b], nodes[a])
            elif adj[a, b] == 1 and adj[b, a] == -1:
                graph.add_edge(nodes[b], nodes[a])
            elif adj[a, b] == -1 and adj[b, a] == 1:
                graph.add_edge(nodes[a], nodes[b])
            else:
                raise ValueError((a, b, int(adj[a, b]), int(adj[b, a])))
    return graph.reverse(), nodes


def loader_for(df, loader_class):
    out_data = {}
    for name in df:
        if name == "time":
            continue
        entity, metric = name.split("_")[:2]
        out_data.setdefault(entity, {})[metric] = list(zip(df.time, df[name]))
    return loader_class(out_data)


def score(klass, case_class, loader_class, node_class, graph_class, adj, df, inject_time, keep_isolates=False):
    columns = [c for c in df if c != "time"]
    graph, nodes = graph_from_adj(adj, columns, node_class)
    if keep_isolates:
        graph.add_nodes_from(nodes)
    mem_graph = graph_class(graph)
    context = case_class(loader_for(df, loader_class), sli=nodes[0], detect_time=inject_time, interval=timedelta(seconds=1))
    scores = klass().score(mem_graph, context, current=inject_time + 300)
    values = {f"{node.entity}_{node.metric}": value.score for node, value in scores.items()}
    return values, graph, context


rows = []
summary = []
for relative in ("cartservice_cpu/1", "cartservice_mem/1"):
    stem = relative.replace("/", "_")
    case_result = {"case": "fse-ob/" + relative, "selection_rule": "first repetition of cartservice CPU and MEM; fixed before new outcomes", "labels_given_to_method": False}
    try:
        df, inject_time, source = data_for_case(relative)
        columns = [c for c in df if c != "time"]
        log(f"{stem} PC_BEGIN shape={df.shape}")
        started = time.perf_counter()
        adj = pc_default(df.drop(columns=["time"]))
        log(f"{stem} PC_END diagnostic_seconds={time.perf_counter()-started:.3f}")
        write_json(stem + "_graph.json", {"node_names": columns, "adj": adj.astype(int).tolist()})
        rows.append([case_result["case"], str(source), "CIRCA-PC/RCAEval default", "original scorer comparison on new graph with recorded intermediate values", "b"])
        values, graph, context = score(RHTScorer, CaseData, MemoryDataLoader, Node, MemoryGraph, adj, df, inject_time)
        official_wrapper = dict(rht(adj, inject_time, df))
        original, original_graph, original_context = score(OriginalRHT, OriginalCaseData, OriginalLoader, OriginalNode, OriginalGraph, adj, df, inject_time)
        original_all, _, _ = score(OriginalRHT, OriginalCaseData, OriginalLoader, OriginalNode, OriginalGraph, adj, df, inject_time, keep_isolates=True)
        repeat, _, _ = score(OriginalRHT, OriginalCaseData, OriginalLoader, OriginalNode, OriginalGraph, adj, df, inject_time)
        rows.extend([
            [case_result["case"], str(source), "CIRCA-original/RHT same PC and 1s context", "compare every metric score to RCAEval copied scorer", "b"],
            [case_result["case"], str(source), "CIRCA-original/RHT keep graph isolates", "candidate coverage diagnostic; explicit changed graph membership", "b"],
            [case_result["case"], str(source), "CIRCA-original/RHT same PC repeat", "repeat scores on fixed input", "a"],
        ])
        old_path = Path("D:/RCA-ext/work/T-006/l4-circa-fse-ob-len10-lan1/output/results") / (stem + ".json")
        old_ranks = json.loads(old_path.read_text())["0"]
        names = set(values)
        case_result.update({
            "source": str(source), "old_result": str(old_path), "raw_pc_columns": columns,
            "num_pc_columns": len(columns), "num_scored": len(values), "num_graph_edges": graph.number_of_edges(),
            "is_dag": nx.is_directed_acyclic_graph(graph),
            "graph_isolates_omitted": sorted(set(columns) - names),
            "original_isolate_scores": {k: original_all[k] for k in sorted(set(original_all) - names)},
            "same_candidate_set_original": names == set(original),
            "max_score_diff_original_rcaeval": max((abs(original[k]-values[k]) for k in names), default=0),
            "max_score_diff_rht_function": max((abs(official_wrapper[k]-values[k]) for k in names), default=0),
            "repeat_exact_scores": original == repeat,
            "old_rank_same_candidates": set(old_ranks) == names,
            "old_rank_same_order_except_exact_ties": all(values[a] >= values[b] for a,b in zip(old_ranks,old_ranks[1:])),
            "context": {"interval_seconds": 1, "train_points": context.train_window, "test_points": context.test_window,
                        "loaded_start_offset": -120, "loaded_end_offset": 300, "train_offset": [-120,-10], "test_offset": [291,300]},
            "original_scores": original, "rcaeval_scores": values,
        })
        log(f"{stem} SCORES_END diff={case_result['max_score_diff_original_rcaeval']} isolates={case_result['graph_isolates_omitted']}")
    except Exception as error:
        case_result.update({"error": type(error).__name__ + ": " + str(error), "traceback": traceback.format_exc()})
        log(f"{stem} FAILED {case_result['error']}")
    write_json(stem + "_comparison.json", case_result)
    summary.append(case_result)

# Synthetic graph-empty/isolation/parser checks do not consume dataset labels.
times = np.arange(-300, 300)
toy = pd.DataFrame({"a_cpu": 1+np.sin(times/9), "b_cpu": 2+np.cos(times/11), "time": times})
empty_result = rht(np.zeros((2,2)), 0, toy)
toy_graph, _ = graph_from_adj(np.array([[0,-1,0],[-1,0,0],[0,0,0]]), ["a_cpu", "b_cpu", "c_cpu"], Node)
bad = toy.rename(columns={"a_cpu":"cpu"})
try:
    rht(np.zeros((2,2)), 0, bad)
    parser_error = None
except Exception as error:
    parser_error = type(error).__name__ + ": " + str(error)
write_json("synthetic.json", {"empty_pc_ranks": empty_result, "graph_nodes_with_c_isolate": sorted(f"{n.entity}_{n.metric}" for n in toy_graph.nodes), "malformed_no_underscore_error": parser_error})
write_json("summary.json", summary)
with (OUT / "cases.csv").open("w",encoding="utf-8-sig",newline="") as stream:
    writer=csv.writer(stream); writer.writerow(["ca", "file_nguon", "phuong_phap", "muc_dich", "ly_do"]);writer.writerows(rows)
log("DONE; audit scores compared, synthetic empty graph and parser tested")
