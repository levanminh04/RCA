"""T-034 K3: dựng bản đồ hạn chế hợp nhất `ban-do-g2.json` từ nguồn T-028, T-029, T-032, T-033 và kết quả E1/E2. Chỉ đọc nguồn.

Mỗi dòng G2-Hn: mã gốc, phương pháp, dataset, chế độ, hiện tượng, trạng thái của câu "vì sao", mức bằng chứng (thang WHY-51),
loại nguồn hạn chế (D dữ liệu / G giao thức / A bản cài hoặc đầu vào tự dựng / M cách tính của phương pháp), giải thích khác,
lời tác giả, RQ bị ảnh hưởng; các con số kèm (file, con trỏ JSON); và bảng theo ô.

Bảng theo ô (root × loại lỗi) được suy ra tại đây từ bảng theo đơn vị của T-032 (`doi-chieu-dung-sai.json`,
`can-thiep-tinh-toan.json`) và bảng HP theo ô của T-029; cách suy ghi trong trường `derivation`.

Dùng: python g2_ban_do.py <thư mục lượt> <hai-phep-kiem.json hoặc '-'>
"""
import json
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g2_lib import Facts, ROOT, load, resolve, sha  # noqa: E402
import g2_extra_facts  # noqa: E402
from g2_ban_do_rows import EXCLUDED, ROWS  # noqa: E402

T28 = "results/T-028/runs/phan-hoi-review-001/summary-tables.json"
T29S = "results/T-029/runs/report-main-001/summary.json"
T29R = "results/T-029/runs/review4-repair-001/summary.json"
T32 = "results/T-032/"
R32 = "results/T-032/runs/"
SUP = "results/T-032/runs/bo-sung-toan-dien-20261012-001/"
T33 = "results/T-033/runs/bo-sung-toan-dien-20261012-001/t33/"
UNITS = T32 + "doi-chieu-dung-sai.json"
EFFECT = T32 + "can-thiep-tinh-toan.json"
LEVELS = {"CT": "can thiệp", "ĐC": "đo cơ chế", "LĐ": "liên hệ có đối chứng", "MT": "mô tả", "CK": "chưa kiểm"}


def mech_idx(dataset, method, k, group_field="overall", group=None):
    rows = load(T28)["mechanism_tables"]
    hits = [i for i, r in enumerate(rows) if r["dataset"] == dataset and r["method"] == method and r["k"] == k and r["group_field"] == group_field
            and (group is None or r["group"] == group)]
    assert len(hits) == 1, (dataset, method, k, group_field, group, len(hits))
    return hits[0]


def cells_ranking(dataset, methods, interventions=()):
    """Theo ô: số ca, số ca sai hạng 1 (OK), số không OK, cờ T-028 ở k=1, và tác dụng phép đổi lên các ca sai (root lên hạng 1 tính bi quan)."""
    units = load(UNITS)["don_vi"]
    effect = {u["unit_id"]: u for u in load(EFFECT)["tac_dung_theo_don_vi"]}
    out = {}
    for method in methods:
        table = defaultdict(lambda: {"n": 0, "sai_hang_1_OK": 0, "khong_OK": 0, "co_k1": Counter(), "phep_doi": defaultdict(lambda: {"ca_sai_co_ket_qua": 0, "sai_thanh_hang_1": 0})})
        seen = set()
        for u in units:
            if u["dataset"] != dataset or u["method"] != method:
                continue
            key = u["opaque_id"]
            first = key not in seen
            seen.add(key)
            cell = table[u["cell"]]
            wrong = bool(u["t028"]["sai_o_k1_theo_ca"])
            if first:                                    # TORAI có 3 seed: đếm theo ca
                cell["n"] += 1
                if u["trang_thai_nguon"] != "OK":
                    cell["khong_OK"] += 1
                elif wrong:
                    cell["sai_hang_1_OK"] += 1
                for flag in u["t028"]["co"]["1"]:
                    cell["co_k1"][flag] += 1
                e = effect.get(u["unit_id"], {})
                for name, getter in interventions:
                    rank = getter(e)
                    if wrong and rank is not None:
                        cell["phep_doi"][name]["ca_sai_co_ket_qua"] += 1
                        cell["phep_doi"][name]["sai_thanh_hang_1"] += int(rank[1] == 1)
        out[method] = {c: {"n": v["n"], "sai_hang_1_OK": v["sai_hang_1_OK"], "khong_OK": v["khong_OK"], "co_k1": {f: v["co_k1"].get(f, 0) for f in ("M1", "M2", "M3", "M4", "M5", "M6", "M0")},
                           "phep_doi": {k: dict(x) for k, x in v["phep_doi"].items()}} for c, v in sorted(table.items())}
    return out


def g(key, *path):
    def getter(e):
        cur = e.get(key)
        for p in path:
            if cur is None:
                return None
            cur = cur.get(p)
        if isinstance(cur, dict):
            cur = cur.get("hang_root")
        return cur
    return getter


def cells_hp(codes):
    hp = load(T29S)["HP_cells"]
    return {code: hp[code] for code in codes if code in hp}


def register_facts(F, run, with_extra=True):
    """Đăng ký mọi số dùng trong bản đồ vào sổ F; ghi hai file dẫn xuất nhỏ vào thư mục lượt."""
    A = F.add

    # ----------------------------------------------------------------------------------------------------------------- số của từng dòng
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        for m in ("baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"):
            i = mech_idx(ds, m, 1)
            A(f"t28.{tag}.{m}.sai", T28, f"/mechanism_tables/{i}/n_wrong_OK")
            A(f"t28.{tag}.{m}.dung", T28, f"/mechanism_tables/{i}/n_correct_OK")
            A(f"t28.{tag}.{m}.khongok", T28, f"/mechanism_tables/{i}/n_non_OK")
            A(f"t28.{tag}.{m}.n", T28, f"/mechanism_tables/{i}/n_cohort")
            for code in ("M1", "M2", "M3", "M4", "M5", "M6", "M0"):
                A(f"t28.{tag}.{m}.{code}", T28, f"/mechanism_tables/{i}/multi/{code}")
                A(f"t28.{tag}.{m}.{code}.primary", T28, f"/mechanism_tables/{i}/primary/{code}")
    # H1 MicroRank bộ chia
    P = R32 + "microrank-partition-001/collect-001/summary.json"
    for br in ("mo15", "mo1p50"):
        A(f"h1.{br}.evaluable", P, f"/summary/all/{br}/evaluable")
        A(f"h1.{br}.hit1", P, f"/summary/all/{br}/hit1/{br}")
        A(f"h1.{br}.native", P, f"/summary/all/{br}/hit1/native")
        A(f"h1.{br}.pairs", P, f"/summary/all/{br}/pairs_above_root_native/n")
        A(f"h1.{br}.gone", P, f"/summary/all/{br}/pairs_above_root_native/gone")
        A(f"h1.{br}.up", P, f"/summary/all/{br}/root_effect/tăng hạng")
        for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
            A(f"h1.{br}.{tag}.hit1", P, f"/summary/{ds}/{br}/hit1/{br}")
            A(f"h1.{br}.{tag}.evaluable", P, f"/summary/{ds}/{br}/evaluable")
    A("h1.share.native", P, "/summary/RE2-TT/mo15/abnormal_share/native/median")
    A("h1.share.mo15", P, "/summary/RE2-TT/mo15/abnormal_share/mo15/median")
    D13 = R32 + "tong-hop-phien-13-001/derived-013.json"
    A("h1.fake.median", D13, "/kt1/fake_all/median")
    A("h1.fake.n", D13, "/kt1/n_cases")
    A("h1.fake.noroot", D13, "/kt1/fake_noroot/median")
    A("h1.real.noroot", D13, "/kt1/real_noroot/median")
    # H2, H3
    C = R32 + "microrank-core-aprime-c1-002/summary.json"
    for br, key in (("c1", "c1"), ("w", "w_unit")):
        A(f"h2.{br}.n", C, f"/summary/{key}/all/n")
        A(f"h2.{br}.hit1", C, f"/summary/{key}/all/hit1/{key}")
        A(f"h2.{br}.native", C, f"/summary/{key}/all/hit1/native")
        A(f"h2.{br}.pairs", C, f"/summary/{key}/all/entity_pairs_above_root_native/n")
        A(f"h2.{br}.gone", C, f"/summary/{key}/all/entity_pairs_above_root_native/no_longer_above")
        A(f"h2.{br}.up", C, f"/summary/{key}/all/effect_on_root/tăng hạng")
        A(f"h2.{br}.down", C, f"/summary/{key}/all/effect_on_root/giảm hạng")
    # H4
    S = R32 + "slow-call-flag-link-001/summary.json"
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        A(f"h4.{tag}.n", S, f"/summary/{ds}/tracerca/groups/above_upstream_measurable/main/n")
        A(f"h4.{tag}.wait", S, f"/summary/{ds}/tracerca/groups/above_upstream_measurable/main/ge_0.5")
    A("h4.right.n", S, "/summary/RE2-TT/tracerca/groups/not_above_upstream_measurable_root_rank1_cases/main/n")
    A("h4.right.wait", S, "/summary/RE2-TT/tracerca/groups/not_above_upstream_measurable_root_rank1_cases/main/ge_0.5")
    TD = R32 + "tracerca-core-td-001/summary.json"
    A("h4.td.re2.before", TD, "/summary/by_dataset/RE2-TT/cases_with_caller_above_root/native")
    A("h4.td.re2.after", TD, "/summary/by_dataset/RE2-TT/cases_with_caller_above_root/t_d")
    A("h4.td.nz.before", TD, "/summary/by_dataset/Nezha-OB/cases_with_caller_above_root/native")
    A("h4.td.nz.after", TD, "/summary/by_dataset/Nezha-OB/cases_with_caller_above_root/t_d")
    A("h4.td.hit1.native", TD, "/summary/all/hit1/native")
    A("h4.td.hit1.td", TD, "/summary/all/hit1/t_d")
    A("h4.td.n", TD, "/summary/all/n")
    A("h4.up.fake", D13, "/kt2/upstream_of_root/fake_median")
    A("h4.up.real", D13, "/kt2/upstream_of_root/real_median")
    A("h4.unrel.fake", D13, "/kt2/unrelated/fake_median")
    A("h4.unrel.real", D13, "/kt2/unrelated/real_median")
    # H5
    SC = R32 + "tracerca-score-contrast-001/summary.json"
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        A(f"h5.{tag}.pairs", SC, f"/summary/{ds}/tr1/pairs_above_root_native/n")
        A(f"h5.{tag}.tr1.gone", SC, f"/summary/{ds}/tr1/pairs_above_root_native/gone")
        A(f"h5.{tag}.ts.still", SC, f"/summary/{ds}/ts/pairs_above_root_native/still_above")
        A(f"h5.{tag}.right", SC, f"/summary/{ds}/tr1/native_right/n")
        A(f"h5.{tag}.right.lose", SC, f"/summary/{ds}/tr1/native_right/lose_rank1")
    # H6 nguồn cũ và mã tác giả
    L = SUP + "closure-ledger-review-001.json"
    A("h6.pairs", L, "/h6_pair_audit/listed_pairs")
    A("h6.cases", L, "/h6_pair_audit/listed_cases")
    A("h6.oldpairs", L, "/h6_pair_audit/old_relation_pairs")
    for i, tag in enumerate(("re2.t1", "re2.t3", "nz.t1", "nz.t3")):
        for k in ("pairs", "above", "tie", "below", "above_with_caller_fallback", "tie_with_both_fallback"):
            A(f"h6.author.{tag}.{k}", L, f"/h6_pair_audit/author_aggregates/{i}/{k}")
    A("h6.frontend.multi", L, "/pattern_candidate/frontend_multi_service_best")
    A("h6.frontend.cases", L, "/pattern_candidate/Nezha_old_relation_cases")
    # H7
    RS = R32 + "root-signal-location-001/summary.json"
    A("h7.nd.n", RS, "/summary/by_dataset_fault/Nezha-OB|network_delay/n_cases")
    A("h7.nd.own", RS, "/summary/by_dataset_fault/Nezha-OB|network_delay/positions/own_d/root_first")
    A("h7.nd.in", RS, "/summary/by_dataset_fault/Nezha-OB|network_delay/positions/in_u/root_first")
    A("h7.re2.ownu", RS, "/summary/by_dataset/RE2-TT/positions/own_u/root_first")
    A("h7.re2.ownd", RS, "/summary/by_dataset/RE2-TT/positions/own_d/root_first")
    A("h7.re2.n", RS, "/summary/by_dataset/RE2-TT/positions/own_u/n_root_has_spans")
    A("h7.nz.ownu", RS, "/summary/by_dataset/Nezha-OB/positions/own_u/root_first")
    A("h7.nz.n", RS, "/summary/by_dataset/Nezha-OB/positions/own_u/n_root_has_spans")
    A("h7.re2.inu", RS, "/summary/by_dataset/RE2-TT/positions/in_u/root_first")
    A("h7.re2.inn", RS, "/summary/by_dataset/RE2-TT/positions/in_u/n_root_has_spans")
    A("h7.nz.inu", RS, "/summary/by_dataset/Nezha-OB/positions/in_u/root_first")
    A("h7.nz.inn", RS, "/summary/by_dataset/Nezha-OB/positions/in_u/n_root_has_spans")
    RF = R32 + "root-signal-by-fault-001/summary.json"
    for m in ("baro", "simplerca", "tracerca"):
        A(f"h7.nd.{m}", RF, f"/by_dataset_fault/Nezha-OB|network_delay/{m}_rank1")
    # H8
    A("h8.n", RF, "/by_dataset_fault/Nezha-OB|return/cases")
    A("h8.norank", RF, "/by_dataset_fault/Nezha-OB|return/no_signal_any_channel")
    for m in ("baro", "simplerca", "tracerca"):
        A(f"h8.{m}", RF, f"/by_dataset_fault/Nezha-OB|return/{m}_rank1")
    A("h8.logvote", RF, "/by_dataset_fault/Nezha-OB|return/root_log_vote")
    FN = SUP + "t32/findings.json"
    for i in range(4):
        A(f"h8.log.{i}.placebo", FN, f"/response/return/{i}/log_keywords/placebo/error_keywords")
        A(f"h8.log.{i}.early", FN, f"/response/return/{i}/log_keywords/early/error_keywords")
        A(f"h8.log.{i}.late", FN, f"/response/return/{i}/log_keywords/late/error_keywords")
    # H9
    SD = R32 + "simplerca-decomposition-002/summary.json"
    A("h9.pairs", SD, "/summary/all/wrong_at_1/entity_pairs_above_root")
    A("h9.metric", SD, "/summary/all/wrong_at_1/pairs_decided_by_metric_alone")
    S1 = R32 + "simplerca-s1-001/summary.json"
    A("h9.s1.re2.pairs", S1, "/summary/by_dataset/RE2-TT/pairs_above_root_native")
    A("h9.s1.re2.gone", S1, "/summary/by_dataset/RE2-TT/pairs_no_longer_above")
    A("h9.s1.re2.native", S1, "/summary/by_dataset/RE2-TT/hit1/native")
    A("h9.s1.re2.changed", S1, "/summary/by_dataset/RE2-TT/hit1/changed")
    A("h9.s1.re2.optimistic", S1, "/summary/by_dataset/RE2-TT/hit1_optimistic_on_ties/changed")
    # H10
    B2 = R32 + "baro-b2-001/summary.json"
    A("h10.pairs", B2, "/summary/by_dataset/RE2-TT/pairs_above_root_native")
    A("h10.gone", B2, "/summary/by_dataset/RE2-TT/pairs_no_longer_above")
    A("h10.native", B2, "/summary/by_dataset/RE2-TT/hit1/native")
    A("h10.changed", B2, "/summary/by_dataset/RE2-TT/hit1/changed")
    A("h10.lose", B2, "/summary/by_dataset/RE2-TT/native_hit_at_1/loses_hit1")
    A("h10.nz.native", B2, "/summary/by_dataset/Nezha-OB/hit1/native")
    A("h10.nz.changed", B2, "/summary/by_dataset/Nezha-OB/hit1/changed")
    A("h10.nz.lose", B2, "/summary/by_dataset/Nezha-OB/native_hit_at_1/loses_hit1")
    B1 = R32 + "baro-b1-001/summary.json"
    A("h10.b1.same", B1, "/summary/all/b1_effect_on_root/không đổi")
    A("h10.b1.n", B1, "/summary/all/n")
    A("h10.b1.added", B1, "/summary/all/cases_root_has_added_column")
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        A(f"h10.{tag}.wrong", B2, f"/summary/by_dataset/{ds}/native_wrong_at_1/n")
        A(f"h10.{tag}.fixed", B2, f"/summary/by_dataset/{ds}/native_wrong_at_1/becomes_hit1")
    # H11, H12
    MC = R32 + "metric-chain-001/summary.json"
    A("h11.mem", MC, "/summary/RE2-TT/baro/above_kind_by_trend_group/mem/trôi nền")
    BT = R32 + "baseline-trend-001/summary.json"
    A("h11.memall", BT, "/summary/winning_columns/baro/above_root|ca sai hạng 1/by_kind/mem")
    CP = R32 + "chain-position-002/summary.json"
    A("h12.pairs", CP, "/summary/RE2-TT/baro/pairs_above")
    A("h12.nospan", CP, "/summary/RE2-TT/baro/above_by_class/khong_co_span")
    A("h12.roi", CP, "/summary/RE2-TT/baro/above_by_class/roi")
    A("h12.chung", CP, "/summary/RE2-TT/baro/above_by_class/chung_phia_tren")
    A("h12.up.latency", MC, "/summary/RE2-TT/baro/above_position_by_kind/phia_tren/latency")
    # H13–H15
    K2 = R32 + "circa-laptop-k2-001/collect-001/summary.json"
    A("h13.huge", K2, "/summary/k2_cases_with_huge_node/n")
    A("h13.n", K2, "/summary/n_cases")
    A("h13.da", K2, "/summary/k2_cases_with_huge_node/hit1/native_da")
    A("h13.k2", K2, "/summary/k2_cases_with_huge_node/hit1/k2_rht")
    A("h13.hugek2", K2, "/summary/k2_all/node_counts_total/huge_k2")
    A("h13.clean.n", K2, "/summary/k2_cases_without_huge_node/n")
    A("h13.clean.native", K2, "/summary/k2_cases_without_huge_node/hit1/native_rht")
    A("h13.clean.k2", K2, "/summary/k2_cases_without_huge_node/hit1/k2_rht")
    A("h13.clean.da", K2, "/summary/k2_cases_without_huge_node/hit1/native_da")
    A("h13.rht", K2, "/summary/k2_cases_with_huge_node/hit1/native_rht")
    A("h13.da.down", K2, "/summary/da_effect_on_root/giảm hạng")
    A("h13.da.up", K2, "/summary/da_effect_on_root/tăng hạng")
    A("h13.da.same", K2, "/summary/da_effect_on_root/không đổi")
    A("h15.raise", K2, "/summary/k2_all/node_counts_total/regression_raises_score")
    A("h15.reg", K2, "/summary/k2_all/node_counts_total/native_route_linear_regression")
    for key, tag in (("native111_late", "n111"), ("long291_late", "l291"), ("early111_late", "e111"), ("strided111_offset0", "s0"), ("strided111_offset1", "s1"), ("strided111_offset2", "s2")):
        A(f"h15.{tag}", FN, f"/circa/fixed_parent_group_diagnostic/at_least8_parents/{key}/median_of_case_ratio_medians")
    A("h15.nodes", FN, "/circa/fixed_parent_group_diagnostic/at_least8_parents/native111_late/n_nodes")
    # H16, H17
    TL = R32 + "torai-log-contrast-001/summary.json"
    A("h16.wrong", TL, "/summary/tl1/native_wrong/n")
    A("h16.fixed", TL, "/summary/tl1/native_wrong/becomes_hit1")
    A("h16.lose", TL, "/summary/tl1/native_hit1/loses_hit1")
    TB = R32 + "torai-block-decomposition-001/summary.json"
    A("h17.units", TB, "/summary/n_units")
    A("h17.rcd", TB, "/summary/all_units_root_block_branch/rcd")
    A("h17.fallback", TB, "/summary/all_units_root_block_branch/du_phong")
    A("h17.don", TB, "/summary/all_units_root_block_branch/don")
    TRC = R32 + "trace-root-census-001/summary.json"
    A("d5.orphan", TRC, "/cases/14/after_traces/with_orphan")
    A("d5.n", TRC, "/cases/14/after_traces/n")
    A("d5.gate", TRC, "/cases/14/gate/pass")
    # H19 dữ liệu
    KN = T32 + "kha-nang-do-trace.json"
    A("d.nz.ok", KN, "/theo_dataset/Nezha-OB/theo_muc/đo được")
    A("d.nz.no", KN, "/theo_dataset/Nezha-OB/theo_muc/không đo được")
    A("d.re2.part", KN, "/theo_dataset/RE2-TT/theo_muc/đo được một phần")
    A("d.re2.no", KN, "/theo_dataset/RE2-TT/theo_muc/không đo được")
    A("d.nz.n", KN, "/theo_dataset/Nezha-OB/so_ca")
    A("d.re2.n", KN, "/theo_dataset/RE2-TT/so_ca")
    A("d4.tracerca.hit1", D13, "/kt8/tracerca_hit1")
    # T-029 phát hiện
    A("hp.i1.earlier", T29R, "/intervention/all/first_change/earlier")
    A("hp.i1.equal", T29R, "/intervention/all/first_change/equal")
    A("hp.i1.later", T29R, "/intervention/all/first_change/later")
    A("hp.i1.n", T29R, "/intervention/all/n")
    A("hp.nv.full", T29R, "/intervention/all/Nv_totals/full")
    A("hp.nv.i1", T29R, "/intervention/all/Nv_totals/I1")
    A("hp.nv.i2", T29R, "/intervention/all/Nv_totals/I2")
    for det in ("bocpd", "nsigma", "nsigma_doi_chung"):
        A(f"hp.delay.{det}.median", T29S, f"/delay/{det}/median")
        A(f"hp.delay.{det}.zero", T29S, f"/delay/{det}/zero")
    FS = T33 + "fast-summary-001.json"
    for d in ("30", "60", "120", "300", "600"):
        A(f"k7.d{d}", FS, f"/bocpd_post_any_byD/{d}")
    EN = T33 + "engine-final-summary-001.json"
    A("k3.slots", EN, "/counts/PASS")
    A("k3.shams", EN, "/expected_native_shams")
    A("k3.interv", EN, "/expected_interventions")
    LS = T33 + "log-semantics-summary-001.json"
    for code in ("200", "500", "503"):
        A(f"k5.http{code}", LS, f"/all_HTTP_status_counts_in_union_regions/{code}")
    BS = T33 + "backend-status-summary-001.json"
    A("k5.app1", BS, "/application_status_literal_counts/1")
    A("k5.app0", BS, "/application_status_literal_counts/0")

    # dẫn xuất từ 240 slot của T-033: tổng CP và số ca đổi tập CP theo nhánh
    slots = load(EN)["slots"]
    derived33 = {"source": EN, "pointer": "/slots", "derivation": "theo nhánh: tổng CP_count; số ca có CP_set_added hoặc CP_set_removed khác rỗng; tổng native_CP_count",
                 "branches": {}}
    for s in slots:
        if s["branch"] == "native_sham":
            continue
        b = derived33["branches"].setdefault(s["branch"], {"cases": 0, "cp_total": 0, "native_cp_total": 0, "cases_cp_set_changed": 0})
        b["cases"] += 1
        b["cp_total"] += s["CP_count"]
        b["native_cp_total"] += s["native_CP_count"]
        b["cases_cp_set_changed"] += int(bool(s["CP_set_added"]) or bool(s["CP_set_removed"]))
    # theo ô, cho hai nhánh nén (G2-H23): ghép ca với ô bằng results/T-029/nhan-proxy-va-schema.json#/P1/cases/<ca>/cell
    cell_of = {k: v["cell"] for k, v in load("results/T-029/nhan-proxy-va-schema.json")["P1"]["cases"].items()}
    derived33["by_cell_derivation"] = ("theo ô (results/T-029/nhan-proxy-va-schema.json#/P1/cases/<ca>/cell) và nhánh nén: số ca; tổng native_CP_count; tổng CP_count; "
                                      "số ca có CP_set_added hoặc CP_set_removed khác rỗng")
    derived33["by_cell"] = {}
    for s in slots:
        if s["branch"] not in ("compressed_row", "compressed_calendar"):
            continue
        c = derived33["by_cell"].setdefault(cell_of[s["opaque_id"]], {}).setdefault(s["branch"], {"cases": 0, "cp_total": 0, "native_cp_total": 0, "cases_cp_set_changed": 0})
        c["cases"] += 1
        c["cp_total"] += s["CP_count"]
        c["native_cp_total"] += s["native_CP_count"]
        c["cases_cp_set_changed"] += int(bool(s["CP_set_added"]) or bool(s["CP_set_removed"]))
    for br in ("compressed_row", "compressed_calendar"):
        assert sum(v[br]["cp_total"] for v in derived33["by_cell"].values()) == derived33["branches"][br]["cp_total"]
        assert sum(v[br]["cases"] for v in derived33["by_cell"].values()) == derived33["branches"][br]["cases"]
    # theo ô, cho đường độ nhạy theo D (G2-H24): tính lại từ thời điểm điểm đổi của bản gốc đã lưu theo ca và mốc tiêm của giao thức
    LAB = "results/T-022/nhan-dev.json"
    inject = {c["opaque_id"]: c["inject_time"] for c in load(LAB)["cases"]}
    derived33["bocpd_post_any_by_cell_derivation"] = ("theo ô: số ca có ít nhất một phần tử của `native_alarm_times` (" + EN + "#/slots, nhánh compressed_row) nằm trong đoạn [mốc, mốc + D], "
                                                     "mốc = inject_time của " + LAB + " (nhãn chỉ dùng để chấm và phân tích); D = 30, 60, 120, 300, 600 giây. "
                                                     "Tổng 10 ô được kiểm bằng " + FS + "#/bocpd_post_any_byD")
    derived33["bocpd_post_any_by_cell"] = {}
    for s in slots:
        if s["branch"] != "compressed_row":
            continue
        t0 = inject[s["opaque_id"]]
        c = derived33["bocpd_post_any_by_cell"].setdefault(cell_of[s["opaque_id"]], {"cases": 0, "30": 0, "60": 0, "120": 0, "300": 0, "600": 0})
        c["cases"] += 1
        for d in (30, 60, 120, 300, 600):
            c[str(d)] += int(any(t0 <= x <= t0 + d for x in s["native_alarm_times"]))
    for d in (30, 60, 120, 300, 600):
        assert sum(v[str(d)] for v in derived33["bocpd_post_any_by_cell"].values()) == load(FS)["bocpd_post_any_byD"][str(d)], d
    assert sum(v["cases"] for v in derived33["bocpd_post_any_by_cell"].values()) == 30
    ns = load(FS)["nsigma"]["nsigma"]["rows"]
    derived33["nsigma_rolling_first_post_relation"] = dict(Counter(r["rolling_first_post_relation"] for r in ns))
    derived33["nsigma_source"] = {"path": FS, "pointer": "/nsigma/nsigma/rows", "derivation": "đếm rolling_first_post_relation trên 30 ca, bộ cột chính"}
    (run / "t033-dan-xuat.json").write_text(json.dumps(derived33, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    DR = str((run / "t033-dan-xuat.json").relative_to(ROOT)).replace("\\", "/")
    for br in derived33["branches"]:
        A(f"k3.{br}.cp", DR, f"/branches/{br}/cp_total")
        A(f"k3.{br}.changed", DR, f"/branches/{br}/cases_cp_set_changed")
        A(f"k3.{br}.cases", DR, f"/branches/{br}/cases")
    A("k3.native.cp", DR, "/branches/prior_df4/native_cp_total")
    A("k3.cell.routemem.native", DR, "/by_cell/ts-route-service|mem/compressed_row/native_cp_total")
    A("k3.cell.routemem.row", DR, "/by_cell/ts-route-service|mem/compressed_row/cp_total")
    A("k3.cell.routemem.calendar", DR, "/by_cell/ts-route-service|mem/compressed_calendar/cp_total")
    for rel in ("earlier", "equal", "later"):
        A(f"k2.roll.{rel}", DR, f"/nsigma_rolling_first_post_relation/{rel}")

    # dẫn xuất từ T-032: số ca root không được dịch vụ nào gọi
    ca = load(KN)["ca"]
    reasons = Counter((c["dataset"], c["muc_do_duoc"], c.get("ly_do") or c.get("giai_thich_muc", "")[:60]) for c in ca)
    no_caller = sum(1 for c in ca if c["muc_do_duoc"] == "không đo được" and c.get("ly_do_phien_10") == "root không được dịch vụ nào gọi trong trace")
    few_calls = sum(1 for c in ca if c["muc_do_duoc"] == "không đo được" and c.get("ly_do_phien_10") == "cạnh gọi tới root có dưới 20 lời gọi ở một phía mốc")
    assert no_caller + few_calls == sum(1 for c in ca if c["muc_do_duoc"] == "không đo được")
    derived32 = {"source": KN, "pointer": "/ca", "derivation": "trong các ca mức 'không đo được': đếm theo trường ly_do_phien_10", "canh_duoi_20_loi_goi": few_calls,
                 "root_khong_duoc_goi": no_caller, "khong_do_duoc": sum(1 for c in ca if c["muc_do_duoc"] == "không đo được"), "n": len(ca),
                 "ly_do": {" | ".join(k): v for k, v in reasons.items()}}
    derived32["by_cell_derivation"] = "theo dataset và ô (root|fault): số ca; số ca theo trường muc_do_duoc"
    derived32["by_cell"] = {}
    for c in ca:
        e = derived32["by_cell"].setdefault(c["dataset"], {}).setdefault(c["root"] + "|" + c["fault"], {"cases": 0, "đo được": 0, "đo được một phần": 0, "không đo được": 0})
        e["cases"] += 1
        e[c["muc_do_duoc"]] += 1
    assert sum(v["không đo được"] for t in derived32["by_cell"].values() for v in t.values()) == derived32["khong_do_duoc"]
    assert sum(v["cases"] for t in derived32["by_cell"].values() for v in t.values()) == len(ca)
    (run / "t032-dan-xuat.json").write_text(json.dumps(derived32, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    D32 = str((run / "t032-dan-xuat.json").relative_to(ROOT)).replace("\\", "/")
    A("d2.nocaller", D32, "/root_khong_duoc_goi")
    A("d2.fewcalls", D32, "/canh_duoi_20_loi_goi")
    A("d2.unmeasurable", D32, "/khong_do_duoc")
    A("d2.n", D32, "/n")

    if with_extra:
        g2_extra_facts.register(F)
    return F


def main():
    run = ROOT / sys.argv[1]
    run.mkdir(parents=True, exist_ok=True)
    e_path = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != "-" else None
    F = register_facts(Facts(), run, with_extra=bool(e_path))
    EN = T33 + "engine-final-summary-001.json"
    # ----------------------------------------------------------------------------------------------------------------- các dòng G2-Hn
    rows = ROWS
    ranking_cells = {
        "G2-H01": [("RE2-TT", ["microrank_full"]), ("Nezha-OB", ["microrank_full"])],
        "G2-H02": [("RE2-TT", ["microrank_full"]), ("Nezha-OB", ["microrank_full"])],
        "G2-H03": [("RE2-TT", ["tracerca"]), ("Nezha-OB", ["tracerca"])],
        "G2-H04": [("RE2-TT", ["tracerca"]), ("Nezha-OB", ["tracerca"])],
        "G2-H05": [("RE2-TT", ["tracerca"]), ("Nezha-OB", ["tracerca"])],
        "G2-H06": [("Nezha-OB", ["baro", "simplerca", "tracerca"])],
        "G2-H07": [("Nezha-OB", ["baro", "simplerca", "tracerca", "microrank_full"])],
        "G2-H08": [("RE2-TT", ["simplerca"]), ("Nezha-OB", ["simplerca"])],
        "G2-H09": [("RE2-TT", ["baro"]), ("Nezha-OB", ["baro"])],
        "G2-H10": [("RE2-TT", ["baro", "simplerca"])],
        "G2-H11": [("RE2-TT", ["baro"]), ("Nezha-OB", ["baro"])],
        "G2-H12": [("RE2-TT", ["circa_ols_da"])],
        "G2-H13": [("RE2-TT", ["circa_ols_da"])],
        "G2-H14": [("RE2-TT", ["torai_B"])],
        "G2-H15": [("RE2-TT", ["torai_B"])],
        "G2-H16": [("RE2-TT", ["microrank_full", "tracerca"]), ("Nezha-OB", ["tracerca", "simplerca"])],
        "G2-H17": [("RE2-TT", ["baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"]), ("Nezha-OB", ["baro", "simplerca", "microrank_full", "tracerca"])],
        "G2-H18": [("RE2-TT", ["baro", "microrank_full", "circa_ols_da", "torai_B", "tracerca"]), ("Nezha-OB", ["baro", "simplerca", "microrank_full", "tracerca"])],
    }
    interventions = {
        "microrank_full": [("chia trace theo bài gốc (mo15)", g("chia_theo_bai_goc", "mo15")), ("chia trace theo bài gốc (mo1p50)", g("chia_theo_bai_goc", "mo1p50")),
                           ("đếm riêng (M-C1)", g("C1_dem_rieng")), ("trọng số đơn vị (A′)", g("A_phay_trong_so_don_vi")), ("cờ theo phần chưa phủ (M-D)", g("MD_co_theo_phan_chua_phu"))],
        "tracerca": [("cờ theo phần chưa phủ (T-D)", g("TD_co_theo_phan_chua_phu")), ("bước xếp hạng theo lời văn (to_p)", g("buoc_xep_hang_bai_goc_to_p"))],
        "baro": [("thang độ lệch chuẩn (B-2)", g("B2_thang_do_lech_chuan")), ("không lọc cột hằng (B-1)", g("B1_khong_loc_cot_hang"))],
        "simplerca": [("đếm theo cột (S-1)", g("S1_dem_theo_cot"))],
        "circa_ols_da": [("bỏ mọi cạnh, RHT (K-2)", lambda e: (e.get("CIRCA") or {}).get("K2_khong_canh_RHT"))],
        "torai_B": [("bỏ nguồn log, seed 0 (tl1)", lambda e: (e.get("tl1") or {}).get("hang_root_seed0"))],
    }
    hp_cells = {"G2-H20": ["HP-6"], "G2-H21": ["HP-5", "HP-7", "HP-8"], "G2-H22": ["HP-1", "HP-2", "HP-3", "HP-4"]}
    d0 = load(T29S)["D0"]
    out_rows = []
    for r in rows:
        r = dict(r)
        r["muc_nghia"] = LEVELS[r["muc"]]
        missing = [fid for fid in r.get("fact_ids", []) if fid not in F.items]
        assert not missing, (r["id"], missing)
        r["so_van_ban"] = r["so"]
        r["so"] = {fid: F.items[fid] for fid in r.get("fact_ids", [])}
        r["trang_thai"] = re.findall(r"Đã xác lập|Đã loại|Chưa phân xử", r["vi_sao"])
        assert r["trang_thai"], r["id"]
        cells = {}
        if r["id"] in ranking_cells:
            for dataset, methods in ranking_cells[r["id"]]:
                table = {}
                for m in methods:
                    table.update(cells_ranking(dataset, [m], interventions.get(m, [])))
                cells[dataset] = table
            r["theo_o"] = {"kind": "xep_hang", "derivation": "theo ca (TORAI gộp 3 seed theo ca): n; sai hạng 1 trong các ca OK (hạng bi quan khi hòa); không OK; cờ T-028 ở k=1; "
                           "với mỗi phép đổi của T-032: trong các ca sai có kết quả ở nhánh đổi, số ca root lên hạng 1 (bi quan). Nguồn: " + UNITS + "#/don_vi và " + EFFECT + "#/tac_dung_theo_don_vi",
                           "tables": cells}
        elif r["id"] in hp_cells:
            tables = cells_hp(hp_cells[r["id"]])
            if r["id"] == "G2-H21":
                tables["HP-9 (D0)"] = d0
            r["theo_o"] = {"kind": "phat_hien", "derivation": "số cờ đúng / cặp hợp lệ / tổng / N/A theo ô và bộ phát hiện, nguyên từ " + T29S + "#/HP_cells và /D0", "tables": tables}
        elif r["id"] == "G2-H19":
            src = str((run / "t032-dan-xuat.json").relative_to(ROOT)).replace("\\", "/")
            r["theo_o"] = {"kind": "bang_khac", "phu_luc": "C", "source": src,
                           "derivation": load(src)["by_cell_derivation"] + ". Nguồn gốc: " + load(src)["source"] + "#/ca",
                           "cells": {ds: sorted(t) for ds, t in load(src)["by_cell"].items()}}
        elif r["id"] == "G2-H24":
            src = str((run / "t033-dan-xuat.json").relative_to(ROOT)).replace("\\", "/")
            r["theo_o"] = {"kind": "bang_khac", "phu_luc": "C", "source": src,
                           "derivation": load(src)["bocpd_post_any_by_cell_derivation"], "cells": sorted(load(src)["bocpd_post_any_by_cell"])}
        elif r["id"] == "G2-H23":
            src = str((run / "t033-dan-xuat.json").relative_to(ROOT)).replace("\\", "/")
            r["theo_o"] = {"kind": "bang_khac", "phu_luc": "C", "source": src,
                           "derivation": load(src)["by_cell_derivation"] + ". Nguồn gốc: " + EN + "#/slots", "cells": sorted(load(src)["by_cell"])}
        elif r["id"] == "G2-H26":
            src = "results/T-029/a-so-b.json"
            doc = load(src)["by_detector"]["bocpd"]
            r["theo_o"] = {"kind": "bang_khac", "phu_luc": "C", "source": src,
                           "derivation": "Hit@1 theo ô, nguyên từ " + src + "#/by_detector/bocpd/<phương pháp>/by_cell/<ô>/points: a (tại mốc tiêm), t_hat_plus (báo động đầu sau mốc), t_hat (báo động đầu)",
                           "methods": ["baro", "circa_ols_da", "torai_B"], "cells": sorted(doc["baro"]["by_cell"])}
        elif r["id"] == "G2-H25":
            src = "results/T-029/nhan-proxy-va-schema.json"
            doc = load(src)["P2"]["bocpd"]["by_group"]["cell"]
            r["theo_o"] = {"kind": "bang_khac", "phu_luc": "C", "source": src,
                           "derivation": "theo ô, nguyên từ " + src + "#/P2/bocpd/by_group/cell/<ô>: column_counts (số cột BOCPD nhận, từng ca), d (số chiều sau tiền xử lý, từng ca)",
                           "cells": {c: len(v["case_ids"]) for c, v in sorted(doc.items())}}
        else:
            r["theo_o"] = {"kind": "khong_tach_o", "reason": r.get("ly_do_khong_tach_o", "nguồn chỉ có số theo dataset hoặc theo ca đã nêu; không có bảng theo ô")}
        out_rows.append(r)

    # kiểm nhất quán: tổng theo ô phải bằng số của T-028
    checks = []
    for ds, tag in (("RE2-TT", "re2"), ("Nezha-OB", "nz")):
        for m in ("baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"):
            t = cells_ranking(ds, [m])[m]
            tot = {"n": sum(v["n"] for v in t.values()), "sai": sum(v["sai_hang_1_OK"] for v in t.values()), "khongok": sum(v["khong_OK"] for v in t.values())}
            ok = tot["n"] == F.value(f"t28.{tag}.{m}.n") and tot["sai"] == F.value(f"t28.{tag}.{m}.sai") and tot["khongok"] == F.value(f"t28.{tag}.{m}.khongok")
            checks.append({"dataset": ds, "method": m, "from_cells": tot, "t028": [F.value(f"t28.{tag}.{m}.n"), F.value(f"t28.{tag}.{m}.sai"), F.value(f"t28.{tag}.{m}.khongok")], "equal": ok})
    assert all(c["equal"] for c in checks), [c for c in checks if not c["equal"]]

    # V3: mọi mã gốc phải có mặt
    required = ([f"HP-{i}" for i in range(1, 15)] + [f"M{i}" for i in range(0, 7)] + [f"H{i}" for i in range(1, 18)] + [f"D{i}" for i in range(1, 8)]
                + [f"T-032:KT{i}" for i in range(1, 17)] + [f"T-033:K{i}" for i in range(1, 8)])
    ledger_ids = [(q["task"], q["id"], q["parent_question"]) for q in load(SUP + "closure-ledger.json")["questions"]]
    covered = defaultdict(list)
    for r in out_rows:
        for code in r["ma_goc"]:
            covered[code].append(r["id"])
    excluded = EXCLUDED
    for x in excluded:
        covered[x["ma"]].append("KHÔNG ĐƯA VÀO: " + x["ly_do"][:60])
    missing = [c for c in required if c not in covered]
    ledger_missing = [f"{t}:{p}" for t, _i, p in ledger_ids if f"{'T-032' if t == 'T032' else 'T-033'}:{p}" not in covered]
    v3 = {"required": len(required), "covered": len([c for c in required if c in covered]), "missing": missing, "ledger_rows": len(ledger_ids),
          "ledger_parent_questions_missing": sorted(set(ledger_missing)), "status": "PASS" if not missing and not ledger_missing else "FAIL",
          "coverage": {c: covered[c] for c in required}}
    out = {"schema": "T034-ban-do-g2-v1", "generated": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "thang_muc": LEVELS,
           "loai_nguon": {"D": "dữ liệu hoặc thiếu đầu vào", "G": "giao thức đánh giá", "A": "bản cài, adapter hoặc đầu vào do ta dựng", "M": "giả định hoặc cách tính của phương pháp"},
           "luu_y": "Các dòng có thể chồng nhau trên cùng một ca; không cộng thành tỷ lệ nguyên nhân. Mọi số là trên dev (30 ca RE2-TT, 22 ca Nezha-OB).",
           "rows": out_rows, "khong_dua_vao": excluded, "v3": v3, "kiem_tong_theo_o": checks,
           "sources": {p: sha(p) for p in sorted({v["path"] for v in F.items.values()})}}
    (run / "ban-do-g2.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (run / "so-lieu-ban-do.json").write_text(json.dumps(F.items, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("rows", len(out_rows), "facts", len(F.items), "V3", v3["status"], "missing", missing, v3["ledger_parent_questions_missing"])


if __name__ == "__main__":
    main()
