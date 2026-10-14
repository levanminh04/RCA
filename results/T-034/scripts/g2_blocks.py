"""T-034: các khối bảng sinh tự động cho `goi-g2.md` và `hai-phep-kiem.md`.

Mỗi hàm trả về Markdown. Mọi con số trong bảng là một chỗ giữ `{{mã}}` do `Facts.ref(file, con trỏ)` cấp, nên đi qua cùng
đường kiểm V4 như số trong văn xuôi. Không hàm nào tự tính số: phép dẫn xuất (nếu có) nằm trong JSON nguồn đã ghi cách suy.
"""
BL = "results/T-034/bang-baseline.json"
HK = "results/T-034/hai-phep-kiem.json"
BD = "results/T-034/ban-do-g2.json"
T25 = "results/T-025/phat-hien.json"
MAIN = ["baro", "simplerca", "microrank_full", "tracerca", "circa_ols_da", "torai_B"]
SHORT = {"baro": "BARO", "simplerca": "SimpleRCA", "microrank_full": "MicroRank", "tracerca": "TraceRCA", "circa_ols_da": "CIRCA", "torai_B": "TORAI B"}
COHORT = {"RE2-TT_dev30": "RE2-TT", "RE2-TT_dev19": "RE2-TT", "Nezha-OB_main": "Nezha-OB"}


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def cell_name(cell):
    service, fault = cell.split("|")
    return service.replace("ts-", "").replace("-service", "").replace("service", "") + " / " + fault


def k2_rank(F, load, cohort, methods=MAIN):
    base = f"/ranking_mode_a/{cohort}/methods"
    doc = load(BL)["ranking_mode_a"][cohort]["methods"]
    rows = []
    for m in methods:
        r = lambda key, spec=".3f": F.ref(BL, f"{base}/{m}/{key}", spec)
        status = ", ".join(f"{st}: " + F.ref(BL, f"{base}/{m}/status/{st}") for st in doc[m]["status"])
        if set(doc[m]["status"]) == {"UNSUPPORTED"}:
            rows.append([SHORT[m], status] + ["không chạy được"] + [""] * 8)
            continue
        ci = "[" + F.ref(BL, f"{base}/{m}/bootstrap95/hit@1/lo", ".2f") + "; " + F.ref(BL, f"{base}/{m}/bootstrap95/hit@1/hi", ".2f") + "]"
        rows.append([SHORT[m], status, r("hit@1"), ci, r("hit@3"), r("hit@5"), r("mrr"), r("ndcg@5"), r("avg@5"), r("retrieval@5"), r("rerank@1(K=5)")])
    return table(["Phương pháp", "Trạng thái (số ca)", "Hit@1", "Khoảng bootstrap của Hit@1", "Hit@3", "Hit@5", "MRR", "NDCG@5", "Avg@5", "Retrieval@5", "Rerank@1 (K=5)"], rows)


def k2_cell(F, load, cohort, methods=MAIN):
    base = f"/ranking_mode_a/{cohort}/methods"
    doc = load(BL)["ranking_mode_a"][cohort]["methods"]
    cells = list(doc[methods[0]]["by_cell"])
    rows = []
    for c in cells:
        row = [cell_name(c), F.ref(BL, f"{base}/{methods[0]}/by_cell/{c}/n")]
        for m in methods:
            st = doc[m]["by_cell"][c]["status"]
            if set(st) == {"UNSUPPORTED"}:
                row.append("—")
                continue
            mark = "".join(f" ({k}: " + F.ref(BL, f"{base}/{m}/by_cell/{c}/status/{k}") + ")" for k in st if k != "OK")
            row.append(F.ref(BL, f"{base}/{m}/by_cell/{c}/hit@1_sum", ".3g") + mark)
        rows.append(row)
    return table(["Ô (root / loại lỗi)", "Số ca"] + [SHORT[m] for m in methods], rows)


def k2_det(F, load):
    names = {"bocpd": "BOCPD", "nsigma": "N-Sigma (bộ cột chính)", "nsigma_doi_chung": "N-Sigma (bộ cột đối chứng)"}
    rows = []
    for det, name in names.items():
        b = f"/detection_mode_b/{det}"
        r = lambda key, spec="": F.ref(BL, f"{b}/{key}", spec)
        rows.append([name, r("precision", ".3f"), r("recall", ".3f"), r("f1", ".3f"), r("false_alarms") + " / " + r("normal_seconds_evaluated") + " giây",
                     r("false_alarms_per_normal_hour", ".1f"), r("delay_from_injection_s/trung_vi", ".0f") + " (" + r("delay_from_injection_s/min") + "–" + r("delay_from_injection_s/max") + ")",
                     r("cases_first_alarm_at_or_after_injection") + "/" + r("n_cases")])
    return table(["Bộ phát hiện", "Precision", "Recall", "F1", "Báo động trên đoạn bình thường theo nhãn proxy", "Mỗi giờ bình thường", "Độ trễ từ mốc tiêm, giây: trung vị (nhỏ nhất–lớn nhất)",
                  "Ca có báo động đầu ở hoặc sau mốc"], rows)


def k2_det_cell(F, load):
    doc = load(T25)["bo_phat_hien"]
    cells = list(doc["bocpd"]["theo_o"])
    rows = []
    for c in cells:
        rows.append([cell_name(c), F.ref(T25, f"/bo_phat_hien/bocpd/theo_o/{c}/n")] + [F.ref(T25, f"/bo_phat_hien/{d}/theo_o/{c}/bao_dong_dau_dung") for d in ("bocpd", "nsigma")])
    return table(["Ô (root / loại lỗi)", "Số ca", "BOCPD: ca có báo động đầu ở hoặc sau mốc", "N-Sigma: ca có báo động đầu ở hoặc sau mốc"], rows)


def k2_modeb(F, load):
    rows = []
    for ranker, name in (("baro:native", "BARO"), ("circa:ols+rht_da", "CIRCA"), ("torai_B", "TORAI B")):
        for det, dname in (("bocpd", "BOCPD"), ("nsigma", "N-Sigma")):
            b = f"/mode_b_rca_at_first_alarm/{ranker}[{det}]"
            gkey = {"baro:native": "baro", "circa:ols+rht_da": "circa_ols_da", "torai_B": "torai_B"}[ranker]
            g = f"/table_G_run_point/rows/{gkey}[{det}]/points"
            rows.append([name + " + " + dname, F.ref(BL, b + "/cases_first_alarm_correct") + "/" + F.ref(BL, b + "/n"), F.ref(BL, b + "/joint_success/hit@1", ".3f"), F.ref(BL, b + "/joint_success/hit@5", ".3f"),
                         F.ref(BL, g + "/a/hit@1", ".3f"), F.ref(BL, g + "/t_hat_plus/hit@1", ".3f"), F.ref(BL, g + "/t_hat/hit@1", ".3f")])
    return table(["Ghép", "Ca có báo động đầu đúng", "Thành công chung Hit@1", "Thành công chung Hit@5", "Hit@1 khi chạy tại mốc tiêm", "Hit@1 tại báo động đầu sau mốc", "Hit@1 tại báo động đầu"], rows)


def k2_author(F, load):
    rows_doc = load(BL)["diagnostic_branches_not_baseline"]["tracerca_author_code_latency_only"]["rows"]
    base = "/diagnostic_branches_not_baseline/tracerca_author_code_latency_only/rows"
    rows = []
    for i, r in enumerate(rows_doc):
        st = ", ".join(f"{k}: " + F.ref(BL, f"{base}/{i}/status/{k}") for k in r["status"])
        rows.append([r["dataset"], r["latency_unit"], F.ref(BL, f"{base}/{i}/feature_selection_threshold", ".0f"), F.ref(BL, f"{base}/{i}/n"), st,
                     F.ref(BL, f"{base}/{i}/hit1_pessimistic"), F.ref(BL, f"{base}/{i}/hit1_expected", ".3g"), F.ref(BL, f"{base}/{i}/hit1_optimistic"),
                     F.ref(BL, f"{base}/{i}/root_default_minus1")])
    return table(["Dataset", "Đơn vị thời lượng", "Ngưỡng chọn đặc trưng", "Số ca (mẫu số)", "Trạng thái", "Ca hạng 1, bi quan", "Ca hạng 1, kỳ vọng khi hòa", "Ca hạng 1, lạc quan",
                  "Ca root nhận điểm mặc định"], rows)


def k2_mrsplit(F, load):
    base = "/diagnostic_branches_not_baseline/microrank_paper_split/summary"
    rows = []
    for ds in ("RE2-TT", "Nezha-OB"):
        for br, name in (("mo15", "`mo15`: luật của bài"), ("mo1p50", "`mo1p50`: luật chia nhóm trong mã của tác giả")):
            b = f"{base}/{ds}/{br}"
            rows.append([ds, name, F.ref(BL, b + "/cases"), F.ref(BL, b + "/evaluable"), F.ref(BL, b + "/hit1/native"), F.ref(BL, b + f"/hit1/{br}")])
    return table(["Dataset", "Nhánh bộ chia", "Số ca", "Ca xét được", "Ca hạng 1, bản thư viện (trên các ca xét được)", "Ca hạng 1, sau khi thay bộ chia"], rows)


# ------------------------------------------------------------------------------------------------------------ K3
def k3_summary(F, load):
    rows = []
    for r in load(BD)["rows"]:
        state = "; ".join(dict.fromkeys(r["trang_thai"]))
        rows.append([r["id"], r["ten"], r["che_do"], r["muc"], r["loai_nguon"], state, ", ".join(r["ma_goc"])])
    return table(["Mã", "Hạn chế", "Chế độ", "Mức cao nhất", "Loại nguồn", "Trạng thái của câu “vì sao”", "Mã gốc"], rows)


def k3_rows(F, load):
    out = []
    for r in load(BD)["rows"]:
        sub = "; ".join(f"{name} — {level}" for name, level in r["muc_nguon_con"])
        if r["theo_o"]["kind"] == "xep_hang":
            cell = "Phụ lục A, các bảng " + "; ".join(f"{ds} / {SHORT[m]}" for ds, t in r["theo_o"]["tables"].items() for m in t) + "."
        elif r["theo_o"]["kind"] == "phat_hien":
            cell = "Phụ lục B, các cột " + ", ".join(r["theo_o"]["tables"]) + "."
        elif r["theo_o"]["kind"] == "bang_khac":
            cell = "Phụ lục C, bảng của " + r["id"] + "."
        else:
            cell = "Không tách theo ô: " + r["theo_o"]["reason"] + "."
        out.append("\n".join([
            f"#### {r['id']} — {r['ten']}", "",
            f"- **Phương pháp; dataset; chế độ:** {r['phuong_phap']}; {r['dataset']}; {r['che_do']}.",
            f"- **Mã gốc:** {', '.join(r['ma_goc'])}.",
            f"- **Hiện tượng:** {r['hien_tuong']}",
            f"- **Số:** {r['so_van_ban']}",
            f"- **Vì sao:** {r['vi_sao']}",
            f"- **Mức bằng chứng cao nhất:** {r['muc']} ({r['muc_nghia']}). Nguồn con: {sub}.",
            f"- **Loại nguồn hạn chế:** {r['loai_nguon']}.",
            f"- **Giải thích khác còn lại:** {r['giai_thich_khac']}",
            f"- **Tác giả có nêu không:** {r['tac_gia']}",
            f"- **Ảnh hưởng tới:** {r['rq']}.",
            f"- **Số ca theo ô:** {cell}"]))
    return "\n\n".join(out)


def k3_excluded(F, load):
    return "\n".join(f"- `{x['ma']}`: {x['ly_do']}" for x in load(BD)["khong_dua_vao"])


def k3_p4(F, load):
    """Năm đầu ra của P4 (MRP §5) → dòng bản đồ, theo loại nguồn và mức đã ghi ở từng dòng."""
    rows = load(BD)["rows"]
    confirmed = [r["id"] for r in rows if r["muc"] in ("CT", "ĐC")]
    impl = [r["id"] for r in rows if any(x in r["loai_nguon"] for x in ("A", "D", "G"))]
    method = [r["id"] for r in rows if "M" in r["loai_nguon"]]
    open_ = [r["id"] for r in rows if "Chưa phân xử" in r["vi_sao"]]
    return "\n".join([
        "1. **Hạn chế đã xác nhận và điều kiện** (mức của dòng là CT hoặc ĐC; mức đó thuộc phần nào thì ghi ở trường “Vì sao”): " + ", ".join(confirmed) + ". Điều kiện của từng dòng ghi ở trường “Vì sao” và “Giải thích khác”.",
        "2. **Thuộc bản cài, đầu vào do ta dựng, giao thức hoặc thiếu dữ liệu** (loại A, G, D): " + ", ".join(impl) + ".",
        "3. **Thuộc giả định hoặc cách tính của phương pháp** (loại M): " + ", ".join(method) + ".",
        "4. **Quan hệ giữa dịch vụ có thể bổ sung thông tin gì:** mục 5 (ứng viên), không phải bằng chứng đồ thị đã giúp.",
        "5. **Câu chưa trả lời** (dòng còn phần “chưa phân xử”): " + ", ".join(open_) + "; chi tiết và nơi phân xử ở mục 6."])


def appendix_a(F, load):
    doc = load(BD)
    seen, out = set(), []
    for i, r in enumerate(doc["rows"]):
        if r["theo_o"]["kind"] != "xep_hang":
            continue
        for ds, tables in r["theo_o"]["tables"].items():
            for m, t in tables.items():
                if (ds, m) in seen:
                    continue
                seen.add((ds, m))
                base = f"/rows/{i}/theo_o/tables/{ds}/{m}"
                flags = [f for f in ("M1", "M2", "M3", "M4", "M5", "M6", "M0") if any(c["co_k1"][f] for c in t.values())]
                interventions = []
                for c in t.values():
                    for name in c["phep_doi"]:
                        if name not in interventions:
                            interventions.append(name)
                rows = []
                for c, v in t.items():
                    row = [cell_name(c), F.ref(BD, f"{base}/{c}/n"), F.ref(BD, f"{base}/{c}/sai_hang_1_OK"), F.ref(BD, f"{base}/{c}/khong_OK")]
                    row += [F.ref(BD, f"{base}/{c}/co_k1/{f}") for f in flags]
                    for name in interventions:
                        if name in v["phep_doi"]:
                            row.append(F.ref(BD, f"{base}/{c}/phep_doi/{name}/sai_thanh_hang_1") + "/" + F.ref(BD, f"{base}/{c}/phep_doi/{name}/ca_sai_co_ket_qua"))
                        else:
                            row.append("—")
                    rows.append(row)
                out.append(f"**{ds} / {SHORT[m]}**\n\n" + table(["Ô", "Số ca", "Sai hạng 1 (chạy được)", "Không chạy được"] + [f"Cờ {f}" for f in flags] + [f"Phép đổi: {n}" for n in interventions], rows))
    return "\n\n".join(out)


def appendix_b(F, load):
    doc = load(BD)
    out = []
    for i, r in enumerate(doc["rows"]):
        if r["theo_o"]["kind"] != "phat_hien":
            continue
        for code, t in r["theo_o"]["tables"].items():
            dets = list(t)
            cells = list(t[dets[0]])
            rows = []
            for c in cells:
                row = [cell_name(c)]
                for d in dets:
                    b = f"/rows/{i}/theo_o/tables/{code}/{d}/{c}"
                    if "valid" in t[d][c]:
                        row.append(F.ref(BD, b + "/true") + "/" + F.ref(BD, b + "/valid"))
                    else:
                        row.append(F.ref(BD, b + "/count") + "/" + F.ref(BD, b + "/n"))
                rows.append(row)
            out.append(f"**{code}** (thuộc {r['id']})\n\n" + table(["Ô"] + [{"bocpd": "BOCPD", "nsigma": "N-Sigma", "nsigma_doi_chung": "N-Sigma đối chứng"}.get(d, d) for d in dets], rows))
    return "\n\n".join(out)


def appendix_c(F, load):
    """Bảng theo ô của G2-H26 (bảng G, ghép với BOCPD), G2-H23 (hai nhánh nén; tổng theo ô nằm trong file dẫn xuất của lượt) và G2-H25 (số cột, số chiều)."""
    out = []
    rows = {r["id"]: r for r in load(BD)["rows"]}
    t = rows["G2-H19"]["theo_o"]
    for ds, cells in t["cells"].items():
        body = []
        for c in cells:
            b = f"/by_cell/{ds}/{c}"
            body.append([cell_name(c)] + [F.ref(t["source"], b + "/" + k) for k in ("cases", "đo được", "đo được một phần", "không đo được")])
        out.append(f"**G2-H19 — Mức đo được việc “dịch vụ gọi chờ root”, theo ô, {ds}:** số ca ở từng mức. Đây là khả năng quan sát, không phải nhãn lan.\n\n"
                   + table(["Ô", "Số ca", "Đo được (có điều kiện)", "Đo được một phần", "Không đo được"], body))
    t = rows["G2-H24"]["theo_o"]
    body = []
    for c in t["cells"]:
        b = f"/bocpd_post_any_by_cell/{c}"
        body.append([cell_name(c), F.ref(t["source"], b + "/cases")] + [F.ref(t["source"], f"{b}/{d}") for d in (30, 60, 120, 300, 600)])
    out.append("**G2-H24 — Số ca BOCPD có ít nhất một điểm đổi trong D giây sau mốc tiêm, theo ô.** Bảng mô tả theo mốc tiêm; D không phải thời điểm hết lỗi và bảng không cho biết lúc sự cố bắt đầu có tác động.\n\n"
               + table(["Ô", "Số ca", "D = `30`", "D = `60`", "D = `120`", "D = `300`", "D = `600`"], body))
    t = rows["G2-H26"]["theo_o"]
    body = []
    for c in t["cells"]:
        line = [cell_name(c), F.ref(t["source"], f"/by_detector/bocpd/baro/by_cell/{c}/n")]
        for m in t["methods"]:
            line.append(" / ".join(F.ref(t["source"], f"/by_detector/bocpd/{m}/by_cell/{c}/points/{pt}/hit@1", ".2f") for pt in ("a", "t_hat_plus", "t_hat")))
        body.append(line)
    out.append("**G2-H26 — Hit@1 theo ô khi ghép với BOCPD:** tại mốc tiêm / tại báo động đầu sau mốc / tại báo động đầu. Mỗi ô chỉ có ba ca; điểm giữa chọn nhờ nhãn mốc.\n\n"
               + table(["Ô", "Số ca"] + [SHORT[m] for m in t["methods"]], body))
    t = rows["G2-H23"]["theo_o"]
    body = []
    for c in t["cells"]:
        b = f"/by_cell/{c}"
        body.append([cell_name(c), F.ref(t["source"], b + "/compressed_row/cases"), F.ref(t["source"], b + "/compressed_row/native_cp_total"),
                     F.ref(t["source"], b + "/compressed_row/cp_total"), F.ref(t["source"], b + "/compressed_calendar/cp_total"),
                     F.ref(t["source"], b + "/compressed_row/cases_cp_set_changed"), F.ref(t["source"], b + "/compressed_calendar/cases_cp_set_changed")])
    out.append("**G2-H23 — Bỏ hàng lặp, theo ô:** tổng số điểm đổi của BOCPD trên các ca của ô, và số ca có tập điểm đổi khác bản gốc. Số điểm đổi không phải thước đo chất lượng; mỗi ô chỉ có ba ca.\n\n"
               + table(["Ô", "Số ca", "Tổng điểm đổi, bản gốc", "Nén, hazard theo hàng", "Nén, hazard theo thời gian", "Ca đổi tập điểm đổi (theo hàng)", "Ca đổi tập điểm đổi (theo thời gian)"], body))
    t = rows["G2-H25"]["theo_o"]
    body = []
    for c, n in t["cells"].items():
        base = f"/P2/bocpd/by_group/cell/{c}"
        body.append([cell_name(c), F.ref(t["source"], base + "/n"),
                     ", ".join(F.ref(t["source"], f"{base}/column_counts/{i}") for i in range(n)),
                     ", ".join(F.ref(t["source"], f"{base}/d/{i}") for i in range(n))])
    out.append("**G2-H25 — Schema theo ô (đầu vào của BOCPD):** số cột bộ phát hiện nhận và số chiều sau tiền xử lý, từng ca. Bảng mô tả; không tách được ảnh hưởng của schema lên kết quả.\n\n"
               + table(["Ô", "Số ca", "Số cột nhận (từng ca)", "Số chiều sau tiền xử lý (từng ca)"], body))
    return "\n\n".join(out)


# ------------------------------------------------------------------------------------------------------------ E1, E2
AUTHOR = {"above": "trên", "below": "dưới", "tie": "hòa"}
CLASS = {"doi_ca_hai_con_bang_chung": "đổi; cả hai còn tập được chấm", "khong_doi_ca_hai_con_bang_chung": "không đổi; cả hai còn tập được chấm",
         "khong_doi_root_khong_co_tap": "không đổi; root không có tập nào được giữ", "khong_doi_ca_hai_khong_co_tap": "không đổi; cả hai không có tập nào được giữ",
         "doi_do_mat_bang_chung": "đổi vì một bên mất mọi tập được chấm", "khong_co_quan_he": "nhánh không có đặc trưng hữu ích"}


def e1_pairs(F, load, branch):
    pairs = load(HK)["E1"]["pairs"]
    rows = []
    for i, p in enumerate(pairs):
        if p["branch"] != branch:
            continue
        b = f"/E1/pairs/{i}"
        if "relation_all" not in p:
            rows.append([p["dataset"], p["opaque_id"], p["root"], p["caller"], "không có quan hệ (" + p["status"] + ")", "—", "—", "—", "—", "—", CLASS[p["class"]]])
            continue
        size = F.ref(HK, b + "/caller_deciding_all_size") if p["caller_deciding_all_size"] is not None else "—"
        rows.append([p["dataset"], p["opaque_id"], p["root"], p["caller"], p["relation_all"], p["relation_singleton"],
                     F.ref(HK, b + "/root_score_all", ".1f") + " → " + F.ref(HK, b + "/root_score_singleton", ".1f"),
                     F.ref(HK, b + "/caller_score_all", ".1f") + " → " + F.ref(HK, b + "/caller_score_singleton", ".1f"), size,
                     AUTHOR.get((p["author_thr1"] or {}).get("relation"), "không có bằng chứng") + " / " + AUTHOR.get((p["author_thr3"] or {}).get("relation"), "không có bằng chứng"), CLASS[p["class"]]])
    return table(["Dataset", "Ca", "Root", "Dịch vụ gọi", "Quan hệ, chấm qua mọi tập", "Quan hệ, chỉ tập một dịch vụ", "Điểm root (mọi tập → một dịch vụ)", "Điểm dịch vụ gọi (mọi tập → một dịch vụ)",
                  "Cỡ tập quyết định điểm dịch vụ gọi", "Mã tác giả, ngưỡng chọn đặc trưng một / ba (root so với dịch vụ gọi)", "Phân loại"], rows)


def e2_chains(F, load):
    chains = load(HK)["E2"]["chains"]
    rows = []
    for label, c in chains.items():
        b = f"/E2/chains/{label}"
        r = lambda key, spec="": F.ref(HK, f"{b}/{key}", spec)
        rows.append([c["case"], {"PF": "chuỗi tiền tố, mặt nạ tiền tố, thang toàn bản ghi (PF)", "FF": "tiền xử lý trên cả bản ghi (FF)"}[c["branch"]], r("T"), r("d"),
                     r("sham/R_bit_equal_stored"), r("comparison/native_exact_zero_states"), r("comparison/native_subnormal_states"),
                     r("extended_reference/max_abs_log_difference_vs_log_domain", "e"), r("comparison/m_differences"), r("reading/cp_count_native") + " / " + r("reading/cp_count_log"),
                     r("comparison/total_variation_max", "e"), r("reading/first_alarm_unchanged")])
    return table(["Ca", "Nhánh", "Số điểm", "Số chiều", "Bản giữ nguyên trùng bản lưu từng bit", "Trạng thái bị bản gốc cho bằng không", "Trạng thái dưới chuẩn hóa", "Lệch log lớn nhất so với tham chiếu mở rộng",
                  "Số điểm MAP khác", "Số điểm đổi (bản gốc / miền log)", "Khoảng cách biến thiên toàn phần lớn nhất", "Báo động đầu giữ nguyên"], rows)
