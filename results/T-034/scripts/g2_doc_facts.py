"""T-034: số chỉ dùng trong văn xuôi của gói G2 (ngoài các số đã đăng ký cho bản đồ).

Phần dẫn xuất (đếm ô, gộp theo loại lỗi, gộp lớp vị trí) được ghi ra `<lượt>/g2-dan-xuat.json` kèm cách suy và nguồn,
rồi số trong văn bản trỏ vào file đó. Không có số nào được viết tay.
"""
import json
from collections import defaultdict

from g2_lib import ROOT, load

BL = "results/T-034/bang-baseline.json"
CP = "results/T-032/runs/chain-position-002/summary.json"
CS = "results/T-032/runs/call-slow-001/summary.json"
PX = "results/T-032/phan-xu-caller-root.json"
MAIN = ["baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"]
TAG = {"RE2-TT_dev30": "re2", "RE2-TT_dev19": "re19", "Nezha-OB_main": "nz"}


def derive(run):
    bl = load(BL)["ranking_mode_a"]
    cells, by_fault, by_root = {}, {}, {}
    for coh, doc in bl.items():
        cells[coh], by_fault[coh], by_root[coh] = {}, {}, {}
        for m in MAIN:
            bc = doc["methods"][m]["by_cell"]
            cells[coh][m] = {"n_cells": len(bc), "cells_all_right": sum(1 for v in bc.values() if abs(v["hit@1_sum"] - v["n"]) < 1e-12),
                             "cells_none_right": sum(1 for v in bc.values() if v["hit@1_sum"] == 0)}
            f, r = defaultdict(lambda: {"n": 0, "hit1_sum": 0.0}), defaultdict(lambda: {"n": 0, "hit1_sum": 0.0})
            for c, v in bc.items():
                service, fault = c.split("|")
                for table, key in ((f, fault), (r, service)):
                    table[key]["n"] += v["n"]
                    table[key]["hit1_sum"] += v["hit@1_sum"]
            by_fault[coh][m], by_root[coh][m] = dict(f), dict(r)
    cp = load(CP)["summary"]
    chain = {}
    for ds, methods in cp.items():
        for m, v in methods.items():
            if isinstance(v, dict) and "above_by_class" in v:
                chain[f"{ds}|{m}"] = {"pairs_above": v["pairs_above"], "upstream": v["above_by_class"]["goi_truc_tiep"] + v["above_by_class"]["phia_tren_gian_tiep"]}
    both = {m: {"pairs_above": sum(chain[f"{ds}|{m}"]["pairs_above"] for ds in ("RE2-TT", "Nezha-OB")), "upstream": sum(chain[f"{ds}|{m}"]["upstream"] for ds in ("RE2-TT", "Nezha-OB"))}
            for m in ("microrank_full", "baro", "simplerca", "tracerca")}
    out = {"schema": "T034-g2-dan-xuat-v1",
           "cells": {"source": BL, "pointer": "/ranking_mode_a/<cohort>/methods/<m>/by_cell", "derivation": "cells_all_right: số ô có hit@1_sum = n; cells_none_right: số ô có hit@1_sum = 0", "values": cells},
           "by_fault": {"source": BL, "derivation": "cộng n và hit@1_sum của các ô cùng loại lỗi", "values": by_fault},
           "by_root": {"source": BL, "derivation": "cộng n và hit@1_sum của các ô cùng root", "values": by_root},
           "chain": {"source": CP, "pointer": "/summary/<dataset>/<m>/above_by_class", "derivation": "upstream = goi_truc_tiep + phia_tren_gian_tiep (không gồm hai_chieu); both = cộng hai dataset",
                     "values": chain, "both": both}}
    path = run / "g2-dan-xuat.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return str(path.relative_to(ROOT)).replace("\\", "/")


def register(F, run):
    A = F.add
    DX = derive(run)
    doc = load(DX)
    for coh, tag in TAG.items():
        for m in MAIN:
            A(f"dx.{tag}.{m}.cells", DX, f"/cells/values/{coh}/{m}/n_cells")
            A(f"dx.{tag}.{m}.full", DX, f"/cells/values/{coh}/{m}/cells_all_right")
            A(f"dx.{tag}.{m}.zero", DX, f"/cells/values/{coh}/{m}/cells_none_right")
            for fault in doc["by_fault"]["values"][coh][m]:
                A(f"dx.{tag}.{m}.f.{fault}.n", DX, f"/by_fault/values/{coh}/{m}/{fault}/n")
                A(f"dx.{tag}.{m}.f.{fault}.h1", DX, f"/by_fault/values/{coh}/{m}/{fault}/hit1_sum")
            for root in doc["by_root"]["values"][coh][m]:
                short = root.replace("ts-", "").replace("-service", "").replace("service", "")
                A(f"dx.{tag}.{m}.r.{short}.n", DX, f"/by_root/values/{coh}/{m}/{root}/n")
                A(f"dx.{tag}.{m}.r.{short}.h1", DX, f"/by_root/values/{coh}/{m}/{root}/hit1_sum")
    for key in doc["chain"]["values"]:
        ds, m = key.split("|", 1)
        tag = ("re2" if ds == "RE2-TT" else "nz") + "." + m.replace("|seed=", "_s")
        A(f"ch.{tag}.pairs", DX, f"/chain/values/{key}/pairs_above")
        A(f"ch.{tag}.up", DX, f"/chain/values/{key}/upstream")
    for m in doc["chain"]["both"]:
        A(f"ch.both.{m}.pairs", DX, f"/chain/both/{m}/pairs_above")
        A(f"ch.both.{m}.up", DX, f"/chain/both/{m}/upstream")
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        A(f"cs.{tag}.n", CS, f"/summary/{ds}/n_cases")
        A(f"cs.{tag}.edge", CS, f"/summary/{ds}/cases_with_edge_to_root")
        A(f"cs.{tag}.ge05", CS, f"/summary/{ds}/cases_max_to_root_slow_share_after_ge_0_5")
        A(f"cs.{tag}.ge02", CS, f"/summary/{ds}/cases_max_to_root_slow_share_after_ge_0_2")
        A(f"cs.{tag}.before", CS, f"/summary/{ds}/slow_share_before_median_all_root_edges")
        A(f"cs.{tag}.top", CS, f"/summary/{ds}/cases_to_root_exceeds_every_other_edge")
    px = load(PX)["dem_theo_dataset_phuong_phap"]
    for key, v in px.items():
        ds, m = key.split("|")
        tag = ("re2" if ds == "RE2-TT" else "nz") + "." + m
        for k, short in (("don_vi_trong_cohort", "units"), ("sai_hang_1_OK", "sai"), ("co_M5_o_k1_hoac_k5", "m5")):
            if k in v:
                A(f"m5.{tag}.{short}", PX, f"/dem_theo_dataset_phuong_phap/{key}/{k}")
    # bảng baseline: vài số đọc thêm
    for det in ("bocpd", "nsigma"):
        A(f"bl.det.{det}.tp", BL, f"/detection_mode_b/{det}/windows/tp")
        A(f"bl.det.{det}.fp", BL, f"/detection_mode_b/{det}/windows/fp")
    A("bl.g.n", BL, "/table_G_run_point/rows/baro[bocpd]/n")
    BD = "results/T-034/ban-do-g2.json"
    A("map.rows", BD, "/rows", op="len")
    A("v3.required", BD, "/v3/required")
    A("v3.covered", BD, "/v3/covered")
    A("v3.ledger", BD, "/v3/ledger_rows")
    A("v3.status", BD, "/v3/status")
    for grp, short in (("E-gần", "near"), ("E-xa", "far"), ("S", "s")):
        A(f"bl.g.baro_bocpd.{short}.n", BL, f"/table_G_run_point/rows/baro[bocpd]/by_event_group/{grp}/n")
        A(f"bl.g.baro_bocpd.{short}.that", BL, f"/table_G_run_point/rows/baro[bocpd]/by_event_group/{grp}/points/t_hat/hit@1")
        A(f"bl.g.baro_bocpd.{short}.a", BL, f"/table_G_run_point/rows/baro[bocpd]/by_event_group/{grp}/points/a/hit@1")
    return F
