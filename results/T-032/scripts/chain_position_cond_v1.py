"""T-032 việc 1, góc nhìn bổ sung THÊM SAU KHI ĐÃ XEM chain-position-002: tỷ lệ nền chỉ trên thực thể có span.

Lý do: ở RE2-TT các phương pháp metric xếp hạng 68 thực thể, khoảng 42 trong đó không có span (cơ sở dữ liệu...). Thực thể không
có span không thể nằm trên chuỗi gọi và hiếm khi đứng trên root, nên mốc nền tính trên mọi ứng viên làm tỷ số "phía trên" phình.
Bảng này giữ nguyên dữ liệu của units.json, chỉ đổi tập ứng viên: bỏ lớp khong_co_span ở cả thực thể đứng trên root lẫn ứng viên.
Chạy trên EC2, chỉ đọc. Dùng: python chain_position_cond_v1.py <units.json> <thư mục lượt mới>
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

UP = ("goi_truc_tiep", "phia_tren_gian_tiep")
GROUPS = {"phia_tren": UP, "phia_tren_ke_ca_hai_chieu": UP + ("hai_chieu",), "phia_duoi": ("duoc_goi_truc_tiep", "phia_duoi_gian_tiep"),
          "khong_lien_he": ("chung_phia_tren", "roi"), "chung_phia_tren": ("chung_phia_tren",), "roi": ("roi",)}
DRAWS, SEED = 20000, 20261011


def main():
    units_path, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=False)
    units = json.loads(units_path.read_text(encoding="utf-8"))
    rng = np.random.default_rng(SEED)
    summary = {}
    keys = sorted({(u["dataset"], u["method"], u["seed"]) for u in units}, key=lambda k: (k[0], k[1], str(k[2])))
    for dataset, method, seed in keys:
        ok = [u for u in units if (u["dataset"], u["method"], u["seed"]) == (dataset, method, seed) and u.get("status") == "OK" and u.get("root_ranked")]
        if not ok:
            continue
        block = {"units_ok_root_ranked": len(ok), "pairs_above_all": sum(u["n_above"] for u in ok),
                 "pairs_above_without_span": sum(u["above_by_class"].get("khong_co_span", 0) for u in ok), "groups": {}}
        block["pairs_above_with_span"] = block["pairs_above_all"] - block["pairs_above_without_span"]
        block["candidates_with_span"] = sum(u["n_candidates"] - u["candidates_by_class"].get("khong_co_span", 0) for u in ok)
        for name, classes in GROUPS.items():
            observed, expected, total = 0, 0.0, np.zeros(DRAWS, dtype="int64")
            cand_total = 0
            for u in ok:
                n_cand = u["n_candidates"] - u["candidates_by_class"].get("khong_co_span", 0)
                n_above = u["n_above"] - u["above_by_class"].get("khong_co_span", 0)
                good = sum(u["candidates_by_class"].get(c, 0) for c in classes)
                cand_total += good
                observed += sum(u["above_by_class"].get(c, 0) for c in classes)
                if n_above and n_cand:
                    expected += n_above * good / n_cand
                    if good:
                        total += rng.hypergeometric(good, n_cand - good, n_above, size=DRAWS)
            block["groups"][name] = {"observed": observed, "expected": expected, "ratio": (observed / expected) if expected > 0 else None, "candidates": cand_total,
                                     "random_draw_share_ge_observed": float((total >= observed).mean()), "random_draw_share_le_observed": float((total <= observed).mean())}
        # theo ca: ca có thực thể đứng trên root; trong đó ca có ít nhất một thực thể phía trên, và ca mà mọi thực thể đứng trên root đều ở phía trên
        with_above = [u for u in ok if u["n_above"] > 0]
        up_all = GROUPS["phia_tren_ke_ca_hai_chieu"]
        block["cases"] = {"with_above": len(with_above),
                          "with_any_upstream_above": sum(any(u["above_by_class"].get(c, 0) for c in up_all) for u in with_above),
                          "all_above_upstream": sum(sum(u["above_by_class"].get(c, 0) for c in up_all) == u["n_above"] for u in with_above),
                          "top1_is_upstream": sum(any(t["class"] in up_all for t in u["top1_when_root_not_first"]) for u in with_above),
                          "root_has_no_upstream_candidates": sum(sum(u["candidates_by_class"].get(c, 0) for c in up_all) == 0 for u in with_above)}
        summary.setdefault(dataset, {})[method if seed is None else method + "|seed=" + seed] = block
    result = {"schema": "T032-chain-position-cond-v1", "post_hoc": True,
              "reason": "Thêm sau khi xem chain-position-002: mốc nền chỉ trên thực thể có span, để tỷ số không phình vì thực thể không có span.",
              "source": {"path": str(units_path), "sha256": hashlib.sha256(units_path.read_bytes()).hexdigest()}, "draws": DRAWS, "rng_seed": SEED,
              "summary": summary, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for dataset, b in summary.items():
        for name, r in b.items():
            if "seed=1" in name or "seed=2" in name:
                continue
            g = r["groups"]
            line = " | ".join("%s %d/%.1f r=%s p>=%.4f" % (k, g[k]["observed"], g[k]["expected"], None if g[k]["ratio"] is None else round(g[k]["ratio"], 2),
                                                          g[k]["random_draw_share_ge_observed"]) for k in ("phia_tren", "phia_tren_ke_ca_hai_chieu", "phia_duoi", "khong_lien_he"))
            print(dataset, name, "pairs_with_span", r["pairs_above_with_span"], "of", r["pairs_above_all"], "|", line, "| cases", r["cases"], flush=True)


if __name__ == "__main__":
    main()
