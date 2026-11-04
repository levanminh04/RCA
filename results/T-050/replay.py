"""Phát lại xếp hạng và dựng vùng trên gói đầu vào đã kiểm."""
import hashlib
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from m1 import e7, xep_hang
from m1.kieu import Kenh
from m1_danh_gia.pha2 import giai_ma_json

WORLDS = ("P", "S_lo", "S_hi")


def encode(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, allow_nan=False,
                      separators=(",", ":")).encode("utf-8")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inputs(frame, use_s1=False):
    decoded = giai_ma_json(frame)
    channels = [Kenh(**{k: v for k, v in row.items() if k != "ma"})
                for row in decoded["kenh"]]
    assert [k.ma for k in channels] == [row["ma"] for row in frame["kenh"]]
    return channels, dict(F_I=decoded["F_I"], thuc_the_co_kenh_OK=decoded["co_OK"],
                          khoa_T4c=decoded["m"] if use_s1 else None)


def region(rank, channels, edges, inherited):
    result = {"T": rank["T"]}
    for mode in (1, 2):
        regions = e7.vung(rank["T"], channels, edges, inherited, mode)
        result[f"cach_{mode}"] = {root: sorted(nodes) for root, nodes in regions.items()}
        result[f"hop_cach_{mode}"] = sorted(set().union(*regions.values()))
    return result


def mass(rank, edges):
    nodes = rank["tap_PageRank"]
    score = {node: rank["K_I"][node][0] for node in nodes}
    pi = rank["pi"]
    if not pi:
        assert math.fsum(score.values()) == 0
        return None
    total = math.fsum(score.values())
    v = {node: score[node] / total for node in nodes}
    flows = {}
    for node in nodes:
        targets = sorted({node} | {b for a, b in edges if a == node and b in score})
        weight = math.fsum(score[b] for b in targets)
        weights = {b: score[b] / weight for b in targets} if weight else v
        flows[node] = {b: xep_hang.DAMPING * pi[node] * p for b, p in weights.items() if p}
    update = {b: (1 - xep_hang.DAMPING) * v[b] +
              math.fsum(row.get(b, 0) for row in flows.values()) for b in nodes}
    residual = math.fsum(abs(update[b] - pi[b]) for b in nodes)
    return {"v": v, "flow": flows, "residual_L1": residual}


def run(payload, baseline=None):
    result = {}
    edges = [tuple(edge) for edge in payload["edges"]]
    for world in WORLDS:
        frame = payload["frames"][world]
        channels, kwargs = inputs(frame, use_s1=True)
        s1 = xep_hang.xep(channels, **kwargs)
        checks = payload["state"][world]
        assert sum(tier == 1 for tier in s1["tang"].values()) == checks["N1"]
        assert xep_hang.verdict(s1["tang"], checks["valid_units"]) == checks["V0"]
        if baseline is not None:
            assert encode(s1) == encode(baseline[world]), world
        kwargs["khoa_T4c"] = None
        s0 = xep_hang.xep(channels, **kwargs)
        b = xep_hang.xep(channels, che_do="E6b", canh=edges, **kwargs)
        for rank in (s0, b):
            assert all(rank[k] == s1[k] for k in ("K_I", "K_raw", "tang"))
        if b["trang_thai_E6b"] == "NO_POSITIVE_MASS":
            assert b["blocks"] == s0["blocks"]
        result[world] = {"S1": s1, "S0": s0, "E6b": b, "mass": mass(b, edges), **checks}
        if world == "P":
            result[world]["region"] = {
                name: region(rank, channels, edges, payload["inherited"])
                for name, rank in (("S1", s1), ("S0", s0), ("E6b", b))
            }
    return result
