"""Chấm khối K đã đóng hash. Mọi đầu ra ghi trong results/T-053."""
import argparse
from collections import Counter, defaultdict
from fractions import Fraction
import gzip
import hashlib
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/T-053"
LOG = ROOT / "tasks/T-053-kiem-z-chay-lai-k/LOG.md"
sys.path[:0] = [str(ROOT / p) for p in ("src", "results/T-047/scripts", "results/T-045/scripts")]

from m1 import chuoi, hop_dong, xep_hang
from m1_danh_gia import pha2
import luat_c_t047 as lc
import pha2_khoi_k as source
import pha2_t047 as old


SIZES = {"RE2-TT": 30, "Nezha-OB": 22}
MODE = {"cong_phan_vi": "G3", "cong_dem": "D1", "thang": "E4+T4c"}


def local_path(value):
    path = (ROOT / value).resolve()
    if not path.is_relative_to(OUT.resolve()):
        raise ValueError(f"Đường dẫn ngoài T-053: {path}")
    return path


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def emit(handle, row):
    handle.write(json.dumps(pha2.ma_hoa_json(row), ensure_ascii=False, allow_nan=False) + "\n")


def save(path, row):
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        emit(handle, row)


def records(path):
    open_binary = gzip.open if path.suffix == ".gz" else Path.open
    with open_binary(path, "rb") as handle:
        for line in handle:
            yield json.loads(line)


def records_in(paths):
    for path in paths:
        yield from records(path)


def dev_ids():
    paths = {"RE2-TT": "results/T-022/allowlist-dev.json",
             "Nezha-OB": "results/T-026/allowlist-dev.json"}
    manifest = read(ROOT / "results/T-048/manifest.json")
    pinned = {row["path"]: row["sha256"] for row in manifest["files"]}
    out = {}
    for dataset, rel in paths.items():
        path = ROOT / rel
        if sha(path) != pinned[rel]:
            raise ValueError(f"Allowlist lệch hash: {rel}")
        ids = {row["opaque_id"] for row in read(path)["cases"]}
        if len(ids) != SIZES[dataset]:
            raise ValueError(f"Sai số ca dev: {dataset}")
        out[dataset] = ids
    return out


def sealed_inputs(path):
    seal_hash = sha(path)
    required = f"- `{path.relative_to(ROOT).as_posix()}`: `{seal_hash}`"
    if required not in LOG.read_text(encoding="utf-8").splitlines():
        raise ValueError("Hash seal pha 1 chưa ghi trong LOG T-053")
    document = read(path)
    inputs = {}
    for kind in ("that", "ce"):
        native, traces = [], []
        for spec in document[kind]:
            record, trace = local_path(spec["path"]), local_path(spec["trace"])
            if sha(record) != spec["sha256"] or sha(trace) != spec["trace_sha256"]:
                raise ValueError(f"Hash pha 1 lệch: {kind} {record}")
            native.append(record)
            traces.append(trace)
        if len(native) != (52 if kind == "that" else 30) or len(set(native)) != len(native):
            raise ValueError(f"Sai danh sách tệp cửa sổ: {kind}")
        inputs[kind] = (native, traces)
    return seal_hash, document, inputs


def inspect_source(paths, trace_paths, ids, config_ids, output=None):
    """Kiểm tích ca × cấu hình, thu N1/V0 và giữ đúng trường của bộ chấm."""
    traces = {}
    if trace_paths:
        for row in records_in(trace_paths):
            key = row["config_id"], row["opaque_id"]
            if key in traces:
                raise ValueError(f"Dấu vết trùng: {key}")
            traces[key] = {world: {field: state[field] for field in ("N1", "V0", "valid_units")}
                           for world, state in row["trace"]["world_state"].items()}
    states, ce, projections = {}, defaultdict(dict), defaultdict(list)
    for rec in records_in(paths):
        cid, oid = rec["config_id"], rec["opaque_id"]
        key = cid, oid
        if cid not in config_ids or oid not in ids or key in states:
            raise ValueError(f"Bản ghi ngoài ma trận hoặc trùng: {key}")
        if (rec["method_version"] != chuoi.PHIEN_BAN_CHE_DO
                or rec["extra"]["che_do"] != MODE
                or rec["status"] not in ("OK", "NO_EVIDENCE")):
            raise ValueError(f"Bản ghi sai chế độ hoặc lỗi native: {key}")
        hop_dong.kiem_ban_ghi(rec)
        world_states = {}
        for world in pha2.WORLDS:
            blocks = rec["blocks"] if world == "P" else rec["worlds"][world]["blocks"]
            # E6a dùng 3 - tầng làm phần đầu của khóa ở mọi thế giới.
            if any(block["key"][0] not in (0, 1, 2) for block in blocks):
                raise ValueError(f"Khóa E6a không hợp lệ: {key}, {world}")
            n1 = sum(len(group) for block in blocks if block["key"][0] == 2 for group in block["groups"])
            if world == "P":
                v0 = rec["verdict"]
            else:
                v0 = "CAUSE_FOUND" if n1 else None
            if trace_paths:
                state = traces[key][world]
                expected_v0 = xep_hang.verdict({"tier1": 1} if n1 else {}, state["valid_units"])
                if state["N1"] != n1 or state["V0"] != expected_v0 or (v0 is not None and v0 != expected_v0):
                    raise ValueError(f"N1/V0 native và dấu vết lệch: {key}, {world}")
                v0 = expected_v0
            world_states[world] = {"N1": n1, "V0": v0}
        states[key] = world_states
        slim = {"status": rec["status"], "verdict": rec["verdict"],
                "extra": {"tang_P": rec["extra"]["tang_P"]}}
        if lc._n1(slim) != world_states["P"]["N1"]:
            raise ValueError(f"Tầng P khác blocks: {key}")
        ce[cid][oid] = slim
        if output:
            fields = ("opaque_id", "config_id", "status", "verdict", "blocks")
            projected = {field: rec[field] for field in fields}
            projected["extra"] = {k: rec["extra"][k] for k in ("G_N", "kenh_co_the_gioi")}
            projected["worlds"] = {w: {"blocks": rec["worlds"][w]["blocks"]} for w in pha2.WORLDS}
            projections[cid].append(projected)
    expected = {(cid, oid) for cid in config_ids for oid in ids}
    if set(states) != expected or (trace_paths and set(traces) != expected):
        raise ValueError("Ma trận hoặc dấu vết thiếu hoặc dư")
    if output:
        for cid, rows in projections.items():
            part = output / cid
            part.mkdir(parents=True)
            data = part / "ban-ghi.jsonl"
            with data.open("x", encoding="utf-8", newline="\n") as handle:
                for row in sorted(rows, key=lambda row: row["opaque_id"]):
                    emit(handle, row)
            save(part / "pha1.json", {"tep": data.name, "sha256": sha(data),
                "so_ban_ghi": len(rows), "so_ca": len(rows), "cau_hinh": [cid]})
    return states, dict(ce)


def summarize(rows, world, scored=None):
    v0 = Counter(row[world]["V0"] or "CHUA_CO_TRUNG_GIAN" for row in rows)
    valid_n1 = [row[world]["N1"] for row in rows
                if row[world]["V0"] not in (None, "INSUFFICIENT_EVIDENCE")]
    out = {"n": len(rows), "V0": dict(v0), "N1_n_hop_le": len(valid_n1),
           "N1_tong_hop_le": sum(valid_n1),
           "N1_trung_binh_hop_le": Fraction(sum(valid_n1), len(valid_n1)) if valid_n1 else None}
    if scored is not None:
        values = [case["theo_the_gioi"][world] for case in scored]
        h1 = sum((v["hit1"] for v in values), Fraction(0))
        h5 = math.fsum(v["do"]["hit@5"] for v in values)
        n = len(values)
        out.update(MRR=sum((v["RR"] for v in values), Fraction(0)) / n,
                   Hit1=h1 / n, Hit3=math.fsum(v["do"]["hit@3"] for v in values) / n,
                   Hit5=h5 / n, NDCG5=math.fsum(v["do"]["ndcg@5"] for v in values) / n,
                   Retrieval5=h5 / n, Rerank1_K5=float(h1) / h5 if h5 else None,
                   sum_Hit1=h1, sum_Hit5=h5, M5=sum(v["M5"] for v in values))
    return out


def report_metrics(kq, states, labels):
    out = {}
    for cid, cfg in sorted(kq["cau_hinh"].items()):
        true = cfg["ca"]
        detail = {kind: {oid: rows for (c, oid), rows in states[kind].items() if c == cid}
                  for kind in ("that", "ce")}
        aggregate = {}
        for kind, rows in detail.items():
            groups = defaultdict(list)
            for oid in sorted(rows):
                groups["gop", "gop"].append(oid)
                groups["dataset", labels[oid]["dataset"]].append(oid)
                groups["o", labels[oid]["o"]].append(oid)
            aggregate[kind] = {}
            for (scope, key), ids in sorted(groups.items()):
                aggregate[kind].setdefault(scope, {})[key] = {
                    w: summarize([rows[o] for o in ids], w,
                                 [true[o] for o in ids] if kind == "that" else None)
                    for w in pha2.WORLDS}
        out[cid] = {"theo_ca": detail, "tong_hop": aggregate}
    return out


def run(args):
    path = local_path(args.seal)
    seal_hash, seal, inputs = sealed_inputs(path)
    ids = dev_ids()
    config_ids = {"K-" + b for _, b, _, _ in lc.cac_cap().values()} | {"K-R0"}
    out = local_path(args.out)
    out.mkdir(parents=True, exist_ok=False)
    states, _ = inspect_source(*inputs["that"], set.union(*ids.values()), config_ids, out / "pham-vi-cham")
    fake_states, ce = inspect_source(*inputs["ce"], ids["RE2-TT"], config_ids)
    # Kiểm lại sau khi phân tách và trước khi mở nhãn.
    if sealed_inputs(path) != (seal_hash, seal, inputs):
        raise ValueError("Seal pha 1 thay đổi khi chuẩn bị chấm")
    source_paths = [Path(mod.__file__) for mod in (lc, old)]
    t047 = read(ROOT / "results/T-047/manifest.json")
    pinned = {}
    for file in source_paths:
        rel = file.relative_to(ROOT).as_posix()
        pinned[rel] = sha(file)
        if pinned[rel] != t047["outputs"][rel]["sha256"]:
            raise ValueError(f"Nguồn bộ chọn lệch manifest: {rel}")
    t048 = read(ROOT / "results/T-048/manifest.json")
    for rel, expected in t048["source_sha256"].items():
        if rel.startswith("src/"):
            pinned[rel] = sha(ROOT / rel)
            if pinned[rel] != expected:
                raise ValueError(f"Nguồn bộ chấm lệch manifest: {rel}")
    derived = old.verify_derived_source()
    save(out / "command.json", {"argv": sys.argv, "seal": seal, "seal_sha256": seal_hash,
         "script_sha256": sha(Path(__file__)), "derived_source_sha256": derived, "source_sha256": pinned,
         "bootstrap_seed": old.BOOTSTRAP_SEED, "bootstrap_n": old.BOOTSTRAP_N,
         "t0_source": source.NHAN})
    save(out / "so-lan-nhin.json", {"cong_doan": "pha2", "seal_sha256": seal_hash,
         "muc_dich": "Ghép nhãn dev, chạy bộ chọn K, độ nhạy và độ bền"})
    labels, ex = source.nap_nhan(False), source.nap_E_X(False)
    if set(labels) != set.union(*ids.values()) or len({x["o"] for x in labels.values()}) != 23:
        raise ValueError("T0 lệch tập ca hoặc số ô")
    if any(labels[oid]["dataset"] != d for d, group in ids.items() for oid in group):
        raise ValueError("Nhãn khác tập dataset dev")
    kq = {"cau_hinh": {}}
    for cid in sorted(config_ids):
        part = out / "pham-vi-cham" / cid
        part_hash = read(part / "pha1.json")["sha256"]
        kq["cau_hinh"][cid] = pha2.cham(part, part_hash, labels)["cau_hinh"][cid]
    save(out / "kq.json", kq)
    save(out / "chi-so.json", report_metrics(kq, {"that": states, "ce": fake_states}, labels))
    main = lc.danh_gia_khoi(kq, ce, ex)
    save(out / "khoi-k.json", dict(main, STOP=old.stop_reason(main), mac_dinh_ap=old.defaults(main),
         E_X={c: sorted(cells) for c, cells in ex.items()}))
    save(out / "do-nhay.json", {str(h): lc.danh_gia_khoi(kq, ce, ex, h=h)
                               for h in (Fraction(1, 2), Fraction(2))})
    with (out / "bootstrap-samples.jsonl").open("x", encoding="utf-8", newline="\n") as samples, (
        out / "bootstrap-progress.jsonl"
    ).open("x", encoding="utf-8", newline="\n") as progress:
        def event(**fields):
            emit(progress, fields)
            progress.flush()

        def sample(row):
            emit(samples, row)
            samples.flush()

        result = old.bootstrap(kq, ce, ex, event, sample)
    save(out / "do-ben.json", result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seal", required=True)
    parser.add_argument("--out", required=True)
    run(parser.parse_args())
