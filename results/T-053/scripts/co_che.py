"""Đọc chênh K trên cùng ca dev và giữ chuỗi bằng chứng cho nhóm quan trọng."""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

from doi_chieu import ROOT, WORLDS, jsonl, read, sha

sys.path[:0] = [str(ROOT / name) for name in ("src","results/T-047/scripts","results/T-045/scripts")]
from m1_danh_gia.pha2 import giai_ma_json, ma_hoa_json
from co_che_t047 import chain_delta, signal_signature, snapshot
from cham_k import sealed_inputs, source


def decode(path):
    return giai_ma_json(read(path))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("seal", type=Path)
    p.add_argument("scored", type=Path)
    p.add_argument("out", type=Path)
    args = p.parse_args()
    seal_hash, seal, inputs = sealed_inputs(args.seal.resolve())
    scored = args.scored.resolve()
    assert read(scored / "command.json")["seal_sha256"] == seal_hash
    names = {
        "selector":"results/T-047/khoi-k.json",
        "scores":"results/T-047/khoi-k/kq.json",
        "native":"results/T-047/runs/b3-k-c1-that-001/ban-ghi.jsonl",
        "mechanism_tool":"results/T-047/scripts/co_che_t047.py",
    }
    pins = read(ROOT / "results/T-047/manifest.json")["outputs"]
    for name in names.values():
        assert sha(ROOT / name) == pins[name]["sha256"], name
    old_law = decode(ROOT / names["selector"])
    new_law = decode(scored / "khoi-k.json")
    old = decode(ROOT / names["scores"])["cau_hinh"]
    new = decode(scored / "kq.json")["cau_hinh"]
    labels = source.nap_nhan(False)
    assert set(old) == set(new)
    changes = {}
    examples = defaultdict(set)
    pair_changes = {}
    important = {"K-R0", "K-E1+E2"}
    for world in WORLDS:
        for state in (old_law,new_law):
            candidate = state["chon_khoi"][world].get("chon")
            if candidate:
                important.add("K-" + candidate)
    for pair, now in new_law["cap"].items():
        prior = old_law["cap"][pair]
        def per_world(row):
            return {w: row["theo_the_gioi"][w]["ket_cuc"] for w in WORLDS}
        a,b = per_world(prior),per_world(now)
        if a != b:
            pair_changes[pair] = dict(before=a, after=b)
            important.update("K-" + x for x in pair.split("|"))
    for cid in sorted(new):
        assert set(old[cid]["ca"]) == set(new[cid]["ca"]) == set(labels)
        cases = {}
        for oid in sorted(labels):
            ca, cb = (table[cid]["ca"][oid]["theo_the_gioi"] for table in (old,new))
            cases[oid] = {w: dict(old=ca[w]["RR"], new=cb[w]["RR"],
                                  delta=cb[w]["RR"]-ca[w]["RR"], old_hit1=ca[w]["hit1"], new_hit1=cb[w]["hit1"])
                          for w in WORLDS}
        changes[cid] = cases
        if cid not in important:
            continue
        for dataset in ("RE2-TT","Nezha-OB"):
            for w in WORLDS:
                allowed = [oid for oid in cases if labels[oid]["dataset"] == dataset]
                for sign in (-1,1):
                    subset = [oid for oid in allowed if sign*cases[oid][w]["delta"] > 0]
                    if subset:
                        oid = max(subset, key=lambda o:(sign*cases[o][w]["delta"],o))
                        examples[cid,oid].add(f"{dataset}/{w}/{'tốt lên' if sign>0 else 'xấu đi'}")
    # Điều kiện đối chứng xét trên nền cũ. Lấy đúng ca cùng chữ ký tín hiệu.
    targets = set(examples)
    old_shots = {}
    controls = {}
    for row in jsonl(ROOT / names["native"]):
        cid,oid = row["config_id"],row["opaque_id"]
        if cid not in important:
            continue
        if (cid,oid) in targets or (changes[cid][oid]["P"]["old_hit1"] == 1
                                   and changes[cid][oid]["P"]["new_hit1"] == 1):
            shot = snapshot(row,names["native"],labels[oid])
            signature = signal_signature(shot,labels[oid])
            if (cid,oid) in targets:
                old_shots[cid,oid] = (shot,signature)
            else:
                key = (cid,json.dumps(signature,sort_keys=True))
                controls.setdefault(key,(oid,shot))
    control_for = {}
    for key,(shot,signature) in list(old_shots.items()):
        cid,oid = key
        matched = controls.get((cid,json.dumps(signature,sort_keys=True)))
        control_for[cid,oid] = matched[0] if matched else None
        if matched:
            control, item = matched
            old_shots[cid,control] = (item,signature)
            examples[cid,control].add(f"đúng cùng điều kiện với {oid}")
    chains = {}
    for path in inputs["that"][0]:
        for row in jsonl(path):
            key = row["config_id"],row["opaque_id"]
            if key not in old_shots:
                continue
            previous, signature = old_shots[key]
            now = snapshot(row,path.relative_to(ROOT).as_posix(),labels[key[1]])
            chains["|".join(key)] = dict(reason=sorted(examples[key]), signature=signature,
                                         matched_control=control_for.get(key),
                                         chain=chain_delta(previous,now,labels[key[1]]["root"]))
    assert len(chains)==len(old_shots)
    with args.out.open("x",encoding="utf-8") as f:
        json.dump(ma_hoa_json(dict(seal_sha256=seal_hash, pair_changes=pair_changes, per_case=changes,
                                   selected=sorted(important), chains=chains)),f,ensure_ascii=False,indent=2)


if __name__ == "__main__":
    main()
