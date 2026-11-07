"""Hồi quy công thức và chế độ chấm, bằng mẫu tổng hợp."""
import json
import math
import sys
from contextlib import ExitStack
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

from m1 import e4
from m1_danh_gia import pha2

from cham import SIZES, WORLDS, doi_thang


def oracle_z(normal, anomalous):
    ordered = sorted(map(float, normal))

    def quantile(q):
        index = (len(ordered) - 1) * q
        left = math.floor(index)
        right = math.ceil(index)
        if left == right:
            return ordered[left]
        return (1 - (index - left)) * ordered[left] + (index - left) * ordered[right]

    median = quantile(0.5)
    iqr = quantile(0.75) - quantile(0.25)
    scale = iqr if iqr >= 10 * sys.float_info.epsilon else 1.0
    return median, iqr, scale, (max(anomalous) - median) / scale, (median - min(anomalous)) / scale


def kiem_z():
    for normal, anomalous in (
        ([2.0] * 11, [1.0, 3.0]),
        ([0.0, 1.0, 2.0, 7.0], [-5.0, 30.0]),
        ([0.0, 2**-53], [-1.0, 2.0]),
        ([0.0, 2**-47], [-1.0, 2.0]),
    ):
        actual = e4.diem_z(normal, anomalous)
        fields = ("med_N", "IQR", "c", "z_len", "z_xuong")
        for key, expected in zip(fields, oracle_z(normal, anomalous), strict=True):
            assert math.isclose(actual[key], expected, rel_tol=1e-14, abs_tol=0)
        assert actual["huu_han"]
        assert e4.diem_z(normal[::-1], anomalous[::-1]) == actual
    with e4.np.errstate(over="ignore"):
        extreme = e4.diem_z([1e308] * 11, [-1e308] + [1.5e308] * 20)
    assert math.isfinite(extreme["z_len"])
    assert math.isinf(extreme["z_xuong"]) and not extreme["huu_han"]
    return {"ordinary_cases": 4, "extreme": "finite_up_nonfinite_down"}


def kiem_luat_c():
    old, new, cells = {}, {}, set()
    for (dataset, size), cell_count in zip(SIZES.items(), (12, 11), strict=True):
        for i in range(size):
            cell_index = i % cell_count
            cell = f"{dataset}-{cell_index}"
            oid = f"{dataset}-{i}"
            cells.add(cell)
            base = {"dataset": dataset, "o": cell}
            rr_old = dict.fromkeys(WORLDS, Fraction(1, 2))
            rr_new = dict(rr_old)
            if cell_index < 3:
                rr_new.update(P=Fraction(1), S_hi=Fraction(0))
            old[oid] = dict(base, theo_the_gioi={w: {"RR": rr_old[w]} for w in WORLDS})
            new[oid] = dict(base, theo_the_gioi={w: {"RR": rr_new[w]} for w in WORLDS})

    scored = {"cau_hinh": {"E4": {"ca": old}, "z": {"ca": new}}}
    result = doi_thang(scored, "E4", "z", cells)
    native = {w: d["ket_cuc"] for w, d in result["theo_the_gioi"].items()}
    assert native == {"P": "GIUP", "S_lo": "KHONG_TAC_DUNG", "S_hi": "HAI"}
    for world in result["theo_the_gioi"].values():
        assert world["so_o_E_X"] == 23
        assert world["UV6"] == world["dieu_kien_E5"] == "KHONG_AP"
        assert world["moc_gia"] is None
    assert result["ket_hop"]["ket_cuc_dung"] == "KHONG_DU_CA"
    block = pha2.ket_cuc_cap(scored, "E4", "z", cells, "doi_thang", "khoi_K")
    assert block["ket_hop"]["ket_cuc_dung"] == "GIUP"
    from m1_danh_gia import luat_c

    def outcome(total, re2, nz, positive, negative):
        summary = {"dMRR": {"gop": total, "RE2-TT": re2, "Nezha-OB": nz},
                   "P": positive, "M": negative, "P_phay": 0, "M_phay": 0, "so_o_E_X": 23}
        return luat_c.ket_cuc_tu_tong_hop(summary)

    assert outcome(Fraction(-2, 100), 0, Fraction(-1, 10), 0, 3)["buoc"] == 1
    assert outcome(Fraction(-2, 100), Fraction(1, 10), Fraction(-1, 10), 1, 3)["buoc"] == 2
    assert outcome(Fraction(-2, 100), 0, Fraction(-1, 10), 1, 3)["buoc"] == 3
    for margin in (Fraction(1, 100), Fraction(-1, 100)):
        assert outcome(margin, 0, 0, 1, 1)["ket_cuc"] == "KHONG_TAC_DUNG"
    fake = {"cau_hinh": {
        cid: {"ca": {"a": {"verdict": "INSUFFICIENT_EVIDENCE"}}} for cid in ("E4", "z")
    }}
    assert pha2.dem_moc_gia(fake, "E4", "z")[:2] == ((0, 0), (0, 0))
    return {"worlds": native, "luat_C": "KHONG_DU_CA", "khoi_K": "GIUP",
            "order_and_strict_boundaries": "PASS", "ce_zero_denominator": "PASS"}





def so_hai_may(first, second):
    """Đối chiếu cùng lát cắt, chỉ loại metadata lệnh, thời gian và máy."""
    from chay import read, sha

    def load(folder):
        meta = read(folder / "kiem.json")
        command = read(folder / "command.json")
        plan = command["plan"]
        files = ("ban-ghi.jsonl", "trung-gian.jsonl")
        hashes = ("phase1_sha256", "intermediate_sha256")
        for filename, key in zip(files, hashes, strict=True):
            if sha(folder / filename) != meta[key]:
                raise ValueError(f"Hash lệch: {folder / filename}")
        return command, plan, meta, (folder / name for name in files)

    ca, pa, ma, fa = load(first)
    cb, pb, mb, fb = load(second)
    if pa != pb or ca["configs"] != cb["configs"] or ca["script_sha256"] != cb["script_sha256"]:
        raise ValueError("Lát cắt, công cụ hoặc cấu hình khác nhau")
    expected = [(j["opaque_id"], cid, j["window"]) for j in pa["jobs"] for cid in pa["configs"]]
    differences = []
    with ExitStack() as stack:
        streams = [stack.enter_context(f.open(encoding="utf-8")) for f in (*fa, *fb)]
        count = 0
        for raw_a, trace_a, raw_b, trace_b in zip(*streams, strict=True):
            a, ta, b, tb = map(json.loads, (raw_a, trace_a, raw_b, trace_b))
            oid, cid, window = expected[count]
            for native, trace in ((a, ta), (b, tb)):
                if ((native["opaque_id"], native["config_id"]) != (oid, cid)
                        or (trace["opaque_id"], trace["config_id"], trace["window"]) != expected[count]):
                    raise ValueError(f"Lệch thứ tự hoặc thiếu bản ghi: {expected[count]}")
            native_fields = sorted(k for k in a.keys() | b.keys() if a.get(k) != b.get(k))
            trace_fields = sorted(k for k in ta["trace"].keys() | tb["trace"].keys()
                                  if ta["trace"].get(k) != tb["trace"].get(k))
            decision = so_truong_quyet_dinh(a, ta, b, tb)
            numeric = so_nguong_va_khoa(a, b, ca["configs"][cid]["tham_so_E4"]["alpha"])
            if numeric["qua_nguong"]:
                decision.append("p_crosses_alpha")
            if native_fields or trace_fields or decision or ta["effective_sha256"] != tb["effective_sha256"]:
                differences.append({"case": oid, "config": cid, "window": window,
                                    "native": native_fields, "trace": trace_fields, "decision": decision,
                                    "numeric": numeric,
                                    "effective_equal": ta["effective_sha256"] == tb["effective_sha256"]})
            count += 1
    if count != len(expected):
        raise ValueError(f"Thiếu bản ghi: {count}/{len(expected)}")
    return {"records": count, "differences": differences,
            "wall_seconds": [ma["wall_seconds"], mb["wall_seconds"]],
            "python": [ca["python"], cb["python"]], "versions": [ca["versions"], cb["versions"]]}


def phat_lai(ranking, score_overrides, s1):
    """Chạy lại E6a với cờ, tập thực thể và đường gán kênh đã cố định."""
    from dataclasses import replace

    from m1 import xep_hang
    from m1.kieu import Kenh

    ranking = pha2.giai_ma_json(ranking)
    channels = []
    unused = set(score_overrides)
    for raw in ranking["kenh"]:
        entry = dict(raw)
        key = entry.pop("ma")
        channel = Kenh(**entry)
        if key in score_overrides:
            score = score_overrides[key]
            if not channel.co or not math.isfinite(score):
                raise ValueError(f"Điểm replay không hợp lệ: {key}")
            exact = score if isinstance(score, Fraction) else None
            channel = replace(channel, s=float(score), s_q=exact)
            unused.remove(key)
        channels.append(channel)
    if unused:
        raise ValueError("Không tìm thấy kênh replay")
    if s1 and ranking["m"] is None:
        raise ValueError("Thiếu m gốc để replay S1")
    return xep_hang.xep(channels, F_I=ranking["F_I"], thuc_the_co_kenh_OK=ranking["co_OK"],
                       che_do="E6a", khoa_T4c=ranking["m"] if s1 else None)






def doi_co_va_tang(reference, candidate):
    """So điều kiện của phép đổi điểm trước khi tính N1 hoặc V0."""
    def extract(native, trace):
        ranks = trace["xep"]
        if native["status"] not in ("OK", "NO_EVIDENCE") or len(ranks) < len(WORLDS):
            return None
        per_world = {}
        for world, rank in zip(WORLDS, ranks[:3], strict=True):
            per_world[world] = {
                "channels": sorted((k["ma"], k["F_raw"], rank["F_I"].get(k["ma"]),
                                    k["hop_le"], k["trang_thai"]) for k in rank["kenh"]),
                "layers": rank["ket_qua"]["tang"],
                "eligible": rank["co_OK"],
                "count_channel_scores": {
                    k["ma"]:(k["s"],k["s_q"]) for k in rank["kenh"]
                    if k["don_vi"] not in trace["phan_vi"]
                },
            }
        return {
            "status": native["status"],
            "count_calculations": trace.get("dem", []),
            "units": {u["ma"]: (u["hop_le"], u["F_raw_len"], u["F_raw_xuong"])
                      for u in native["extra"]["don_vi_phan_vi"]},
            "assignments": [g["gan"] for g in trace["gan_canh"]],
            "worlds": per_world,
        }
    left, right = extract(*reference), extract(*candidate)
    if left is None or right is None:
        return {"comparable": False, "reason": "native_error_or_missing_intermediate"}
    fields = sorted(key for key in left if left[key] != right[key])
    return {"comparable": not fields, "differences": fields}


def so_truong_quyet_dinh(a, ta, b, tb):
    """Tách chênh số thực khỏi chênh thứ tự, hòa, cờ và độ hợp lệ."""
    from chay import ROOT, read
    from m1 import xep_hang
    from p3 import nezha

    fields = [key for key in ("status", "verdict", "window", "sets", "classes")
              if a.get(key) != b.get(key)]
    if a["status"] not in ("OK", "NO_EVIDENCE") or b["status"] not in ("OK", "NO_EVIDENCE"):
        return fields + ["native_error"]
    pair = doi_co_va_tang((a, ta["trace"]), (b, tb["trace"]))
    fields += pair.get("differences", [])
    for world in WORLDS:
        x, y = a["worlds"][world], b["worlds"][world]
        if x["thu_tu"] != y["thu_tu"] or [v["groups"] for v in x["blocks"]] != [
            v["groups"] for v in y["blocks"]
        ]:
            fields.append(f"order_or_tie.{world}")

    def verdicts(native, detail):
        trace = detail["trace"]
        u = set(read(ROOT / "results/T-022/mappings/universe-re2tt-dev.json")["U"]
                if detail["dataset"] == "RE2-TT" else nezha.UNIVERSE)
        if len(trace["don_vi_the_gioi"]) < 3:
            return None
        result = {}
        for world, rank, units in zip(WORLDS, trace["xep"][:3], trace["don_vi_the_gioi"][:3], strict=True):
            valid = sum(x["cham"].get("hop_le", False) and x["don_vi"]["thuc_the"] in u
                        for x in units["don_vi"])
            layers = rank["ket_qua"]["tang"]
            result[world] = [sum(layer == 1 for layer in layers.values()), xep_hang.verdict(layers, valid)]
        if result["P"][1] != native["verdict"]:
            raise ValueError("V0 suy lại khác verdict native")
        return result

    if verdicts(a, ta) != verdicts(b, tb):
        fields.append("N1_or_V0")
    return sorted(set(fields))





def doi_chieu_khoa(rank, entity, unit_m=None):
    """Khóa và kênh đóng góp của thực thể, giữ phân số của phương pháp."""
    from m1.kieu import Kenh
    from m1.xep_hang import khoa_q

    rank = pha2.giai_ma_json(rank)
    tier = rank["ket_qua"]["tang"].get(entity)
    if tier is None:
        return None
    channels = []
    for row in rank["kenh"]:
        if row["thuc_the"] != entity:
            continue
        channel = Kenh(**{k: v for k, v in row.items() if k != "ma"})
        if channel.co and (tier != 1 or rank["F_I"].get(channel.ma) == 1):
            channels.append(channel)
    max_score, count, total = khoa_q(channels)
    key = (max_score, count, total)
    m_channels=None
    if rank["m"] is not None:
        magnitude = rank["m"].get(entity, (0.0, 0.0))[int(tier == 1)]
        key = (max_score, magnitude, count, total)
        if unit_m is not None:
            observed=max((unit_m.get(k.don_vi,0.0) for k in channels),default=0.0)
            if observed != magnitude:
                raise ValueError("Kênh đóng góp m không tái lập khóa")
            m_channels=[k.ma for k in channels if unit_m.get(k.don_vi,0.0)==magnitude]
    rendered=next(block["key"] for block in rank["ket_qua"]["blocks"]
                  if any(entity in group for group in block["groups"]))
    return {
        "tier": tier, "key": key, "rendered_key": rendered, "m_channels":m_channels,
        "max_channels": [k.ma for k in channels if k.s_chinh_xac == max_score],
        "channels": [k.ma for k in channels],
    }


def so_nguong_va_khoa(a, b, alpha):
    delta_p = delta_key = 0.0
    crosses = []
    for world in WORLDS:
        left, right = (record.get("worlds", {}).get(world, {}) for record in (a, b))
        lkey = {tuple(tuple(g) for g in block["groups"]): block["key"] for block in left.get("blocks", [])}
        rkey = {tuple(tuple(g) for g in block["groups"]): block["key"] for block in right.get("blocks", [])}
        for group in lkey.keys() & rkey.keys():
            delta_key = max([delta_key] + [abs(x - y) for x, y in zip(lkey[group], rkey[group], strict=True)])
    pv = [r.get("extra", {}).get("don_vi_phan_vi", []) for r in (a, b)]
    pairs = [("phan_vi", *pv)]
    for world in WORLDS:
        left, right = (r.get("worlds", {}).get(world, {}).get("don_vi_dem", []) for r in (a, b))
        pairs.append((world, left, right))
    for scope, left, right in pairs:
        la, lb = ({u["ma"]: u for u in units} for units in (left, right))
        for unit in sorted(la.keys() & lb.keys()):
            for direction in ("len", "xuong"):
                field = f"p_{direction}"
                x, y = la[unit].get(field), lb[unit].get(field)
                if x is not None and y is not None:
                    delta_p = max(delta_p, abs(x - y))
                    if (x < alpha) != (y < alpha):
                        crosses.append([scope, unit, direction, x, y])
    return {"max_abs_delta_p": delta_p, "max_abs_delta_key": delta_key, "qua_nguong": crosses}


def oracle_phan_vi(normal, anomalous, minimum, params, directions, result, z):
    """Kiểm độc lập tỷ phần/cờ/điểm trên mẫu hữu hạn thực đã đưa vào chuỗi."""
    normal = sorted(float(x) for x in normal if x is not None and math.isfinite(float(x)))
    anomalous = sorted(float(x) for x in anomalous if x is not None and math.isfinite(float(x)))
    if result["n_N"] != len(normal) or result["n_A"] != len(anomalous):
        raise ValueError("Oracle cỡ mẫu lệch")
    if result["trang_thai"] != "OK":
        return {"checked": False, "status": result["trang_thai"]}
    if min(len(normal), len(anomalous)) < minimum:
        raise ValueError("Oracle hỗ trợ mẫu lệch")
    checked = {}
    for direction, threshold, compare in (
        ("len", result["h"], lambda value, bound: value > bound),
        ("xuong", result["l"], lambda value, bound: value < bound),
    ):
        ra = Fraction(sum(compare(x, threshold) for x in anomalous), len(anomalous))
        rn = Fraction(sum(compare(x, threshold) for x in normal), len(normal))
        raw = max(Fraction(0), ra - rn)
        if float(ra) != result[f"r_{direction}_A"] or float(rn) != result[f"r_{direction}_N"]:
            raise ValueError("Oracle tỷ phần vượt biên lệch")
        p = result[f"p_{direction}"]
        flag = direction in directions and p is not None and p < params["alpha"] and raw > 0
        used = raw if direction in directions and p is not None and p < params["alpha"] else Fraction(0)
        if result[f"F_raw_{direction}"] != int(flag) or result[f"e_{direction}_q"] != used:
            raise ValueError("Oracle cờ hoặc điểm E4 lệch")
        if not 0 <= result[f"e_{direction}"] <= 1 or not math.isfinite(result[f"e_{direction}"]):
            raise ValueError("Oracle miền E4 lệch")
        checked[direction] = {"r_A": ra, "r_N": rn, "raw": raw,
                              "r_A_one": ra == 1, "e_one": used == 1}
    expected = oracle_z(normal, anomalous)
    native = tuple(z[k] for k in ("med_N", "IQR", "c", "z_len", "z_xuong"))
    if all(math.isfinite(value) for value in native + expected):
        if not all(math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-14) for a, b in zip(native, expected)):
            raise ValueError("Oracle công thức z lệch")
        checked["z"] = "finite_formula_match"
    else:
        checked["z"] = "nonfinite_requires_native_exception_analysis"
    return checked


def oracle_dem(args, kwargs, result):
    if result["trang_thai"] != "OK":
        return
    n_normal, n_anomalous, t_normal, t_anomalous, params = args
    lam = Fraction(n_normal) * Fraction(t_anomalous) / Fraction(t_normal)
    if result["nhan"] in ("NEW_OP", "STOPPED"):
        direction = "len" if result["nhan"] == "NEW_OP" else "xuong"
        if result[f"e_{direction}"] != 1 or result[f"F_raw_{direction}"] != 1:
            raise ValueError("Oracle nhánh trực tiếp lệch")
        return
    directions = kwargs.get("huong_cham", ("len", "xuong"))
    for direction, difference, denominator in (
        ("len", n_anomalous-lam, max(n_anomalous, 1)),
        ("xuong", lam-n_anomalous, max(lam, 1)),
    ):
        raw = max(Fraction(0), difference/denominator)
        flag = direction in directions and result[f"p_{direction}"] < params["alpha"] and difference > 0
        expected = raw if flag else Fraction(0)
        if result[f"F_raw_{direction}"] != int(flag) or result[f"e_{direction}_q"] != expected:
            raise ValueError("Oracle điểm đếm lệch")
        if not math.isfinite(result[f"e_{direction}"]) or not 0 <= result[f"e_{direction}"] <= 1:
            raise ValueError("Oracle miền điểm đếm lệch")


def read_run(folder):
    """Kiểm đủ hash trước trả iterator pha 1 và dấu vết của lượt."""
    from chay import read, sha
    command, metadata = read(folder / "command.json"), read(folder / "kiem.json")
    if "success" in metadata and not metadata["success"]:
        raise ValueError(f"Controller lỗi {folder}")
    for filename, key in (("ban-ghi.jsonl", "phase1_sha256"),
                          ("trung-gian.jsonl", "intermediate_sha256")):
        if sha(folder / filename) != metadata[key]:
            raise ValueError(f"Hash lệch {folder / filename}")
    expected = [(job["opaque_id"], cid, job["window"])
                for job in command["plan"]["jobs"] for cid in command["plan"]["configs"]]

    def pairs():
        count = 0
        with (folder/"ban-ghi.jsonl").open(encoding="utf-8") as f, (
            folder/"trung-gian.jsonl").open(encoding="utf-8") as g:
            for a, b in zip(f, g, strict=True):
                record, detail = json.loads(a), json.loads(b)
                key = (record["opaque_id"], record["config_id"], detail["window"])
                if count >= len(expected) or key != expected[count]:
                    raise ValueError("Thiếu, trùng hoặc lệch thứ tự lượt")
                count += 1
                yield record, detail
        if count != len(expected):
            raise ValueError("Lượt thiếu bản ghi")
    return command, metadata, pairs


def compare_cache(first, second):
    ca, ma, fa = read_run(first)
    cb, mb, fb = read_run(second)
    if ca["configs"] != cb["configs"] or ca["plan"] != cb["plan"] or ca["script_sha256"] != cb["script_sha256"]:
        raise ValueError("Hai lượt cache khác nguồn hoặc kế hoạch")
    differences = []
    for (a, da), (b, db) in zip(fa(), fb(), strict=True):
        if a != b or da != db:
            differences.append([a["opaque_id"],a["config_id"],da["window"]])
    return {"native_and_intermediate_exact": not differences, "differences": differences,
            "wall_off": ma["wall_seconds"], "wall_on": mb["wall_seconds"],
            "time_ratio": ma["wall_seconds"]/mb["wall_seconds"],
            "cache_off_sha256": ma, "cache_on_sha256": mb}


def historical_common(record, old):
    """Báo tất cả trường chung lệch, kiểm riêng thứ tự/hòa và cờ trước diễn giải."""
    fields = [key for key in record.keys() | old.keys()
              if key not in ("config_id", "variant") and record.get(key) != old.get(key)]
    decision = [key for key in ("status", "verdict", "window", "sets", "classes", "OBS_DEPENDENT")
                if record.get(key) != old.get(key)]
    if record["status"] not in ("OK", "NO_EVIDENCE") or old["status"] not in ("OK", "NO_EVIDENCE"):
        return {"fields": fields,"decision": decision + ["non_OK"]}
    for world in WORLDS:
        a, b = record["worlds"][world], old["worlds"][world]
        if a["thu_tu"] != b["thu_tu"] or [x["groups"] for x in a["blocks"]] != [x["groups"] for x in b["blocks"]]:
            decision.append(f"order_or_tie.{world}")
        key_fields = ("trang_thai", "nhan", "F_raw_len", "F_raw_xuong", "n_N", "n_A", "T_N", "T_A")
        def counts(rows):
            return {u["ma"]: {k: u.get(k) for k in key_fields} for u in rows}
        if counts(a["don_vi_dem"]) != counts(b["don_vi_dem"]):
            decision.append(f"count_flags.{world}")
    if record["extra"]["tang_P"] != old["extra"]["tang_P"]:
        decision.append("tang_P")
    def quantiles(native):
        return {u["ma"]: {k:u[k] for k in ("trang_thai","hop_le","F_raw_len","F_raw_xuong")}
                for u in native["extra"]["don_vi_phan_vi"]}
    if quantiles(record) != quantiles(old):
        decision.append("quantile_flags")
    def flagged(native):
        return {w: sorted((c["ma"],c["F_I"],c["don_vi"],c["thuc_the"],c["huong"])
                          for c in native["extra"]["kenh_co_the_gioi"][w]) for w in WORLDS}
    if flagged(record) != flagged(old):
        decision.append("flagged_channels_or_assignment")
    return {"fields": sorted(fields), "decision": sorted(set(decision)),
            "numeric": so_nguong_va_khoa(record, old, 0.01)}


def mechanism_case(e4_record, e4_detail, z_record, z_detail, z0_record, z0_detail, root):
    from chay import dump
    from m1_danh_gia import rr

    gates = doi_co_va_tang((e4_record,e4_detail["trace"]),(z_record,z_detail["trace"]))
    output = {"gate_check":gates,"worlds":{}}
    if not gates["comparable"]:
        output["OPEN"] = "Ngoại lệ đổi cờ/tầng, không diễn giải như chỉ đổi điểm"
        return output
    invalid_scale=[]
    for unit,detail in z_detail["trace"]["phan_vi"].items():
        if "z" not in detail:
            continue
        values=detail["z"]
        fields=("med_N","IQR","c","z_len","z_xuong")
        if (not all(isinstance(values[k],(int,float)) and math.isfinite(values[k]) for k in fields)
                or values["IQR"] < 0 or values["c"] <= 0):
            invalid_scale.append(unit)
    output["invalid_scale"]=invalid_scale
    if invalid_scale:
        output["OPEN"]="Trung gian chuẩn hóa z không hợp lệ, giữ native và dừng diễn giải công thức phụ thuộc"
        return output
    for index,world in enumerate(WORLDS):
        base=e4_detail["trace"]["xep"][index]
        zrank=z_detail["trace"]["xep"][index]
        z0rank=z0_detail["trace"]["xep"][index]
        for native,s1 in ((base,True),(zrank,True),(z0rank,False)):
            replay=phat_lai(native,{},s1=s1)
            if json.loads(dump(replay)) != native["ket_qua"]:
                raise ValueError(f"Replay native lệch {world}")
        pv=e4_detail["trace"]["phan_vi"]
        e4_m=e4_detail["trace"].get("don_vi_the_gioi",[])
        z_m=z_detail["trace"].get("don_vi_the_gioi",[])
        e4_m=e4_m[index]["m"] if len(e4_m)>=3 else None
        z_m=z_m[index]["m"] if len(z_m)>=3 else None
        forward,saturated,unsaturated,revert,extreme={},{},{},{},{}
        details={}
        for channel in base["kenh"]:
            unit,direction=channel["don_vi"],channel["huong"]
            if channel["F_raw"] != 1 or channel["trang_thai"] != "OK" or unit not in pv:
                continue
            z=pv[unit]["z"]
            score=z[f"z_{direction}"]
            if not isinstance(score,(int,float)) or not math.isfinite(score):
                raise ValueError("z không hữu hạn trên cặp được coi cùng cờ")
            key=channel["ma"]
            forward[key]=score
            flag=pv[unit]["e4"][f"r_{direction}_A"]==1
            (saturated if flag else unsaturated)[key]=score
            exact=pha2.giai_ma_json(pv[unit]["e4"][f"e_{direction}_q"])
            revert[key]=exact
            z_source=z_detail["trace"]["phan_vi"][unit]
            if pv[unit]["mau_sha256"] != z_source["mau_sha256"]:
                raise ValueError("Hai vế khác mẫu đầu vào")
            extrema=z_source.get("A_extrema",pv[unit].get("A_extrema"))
            if extrema and len(extrema["max2"])>1:
                value=extrema["max2"][-2] if direction=="len" else extrema["min2"][1]
                extreme[key]=(value-z["med_N"])/z["c"] if direction=="len" else (z["med_N"]-value)/z["c"]
            details[key]={"unit":unit,"direction":direction,"r_A_one":flag,
                          "E4":exact,"z":score,"sample_sha256":pv[unit]["mau_sha256"]}
        full=phat_lai(base,forward,True)
        back=phat_lai(zrank,revert,True)
        if json.loads(dump(full)) != zrank["ket_qua"] or json.loads(dump(back)) != base["ket_qua"]:
            raise ValueError("Đổi lại toàn bộ điểm phân vị không tái lập vế đối xứng")
        replays={
            "E4_S1":base["ket_qua"],"E4_S0":phat_lai(base,{},False),
            "z_S1":zrank["ket_qua"],"z_S0":z0rank["ket_qua"],
            "sat_only":phat_lai(base,saturated,True),"non_sat_only":phat_lai(base,unsaturated,True),
            "z_remove_one_A_extreme":phat_lai(zrank,extreme,True),
        }
        root_rr={name:rr.rr_ca(value["blocks"],root) for name,value in replays.items()}
        def relation(ranking,a,b):
            place={entity:i for i,block in enumerate(ranking["blocks"]) for group in block["groups"] for entity in group}
            if a not in place or b not in place:
                return None
            return (place[a]>place[b])-(place[a]<place[b])
        flips=[]
        entities=base["ket_qua"]["tang"].keys()
        for rival in sorted(e for e in entities if e!=root):
            before=relation(base["ket_qua"],root,rival)
            after=relation(zrank["ket_qua"],root,rival)
            if before==after:
                continue
            a0,b0=doi_chieu_khoa(base,root,e4_m),doi_chieu_khoa(base,rival,e4_m)
            a1,b1=doi_chieu_khoa(zrank,root,z_m),doi_chieu_khoa(zrank,rival,z_m)
            if any(x is None for x in (a0,b0,a1,b1)):
                continue
            tied_max=a0["key"][0]==b0["key"][0]
            first_before=next((i for i,(x,y) in enumerate(zip(a0["rendered_key"][1:],b0["rendered_key"][1:])) if x!=y),None)
            first_after=next((i for i,(x,y) in enumerate(zip(a1["rendered_key"][1:],b1["rendered_key"][1:])) if x!=y),None)
            winning=None if after==0 else (a1 if after<0 else b1)
            losing_before=None if after==0 else (b0 if after<0 else a0)
            losing_after=None if after==0 else (b1 if after<0 else a1)
            pv_max=[key for key in winning["max_channels"] if key in details] if winning else []
            count_max=[key for key in losing_before["max_channels"] if key not in details] if losing_before else []
            count_max_after=[key for key in losing_after["max_channels"] if key not in details] if losing_after else []
            pv_max_after=[key for key in losing_after["max_channels"] if key in details] if losing_after else []
            revert_winners={key:revert[key] for key in pv_max}
            revert_group={key:revert[key] for key in winning["channels"] if key in revert} if winning else {}
            local=phat_lai(zrank,revert_winners,True) if revert_winners else zrank["ket_qua"]
            local_group=phat_lai(zrank,revert_group,True) if revert_group else zrank["ket_qua"]
            pair_units={key:details[key] for key in set(a0["channels"]+b0["channels"]) if key in details}
            flips.append({
                "rival":rival,"before_relation":before,"after_relation":after,
                "transition":"became_tied" if after==0 else ("left_tie" if before==0 else "strict_reversal"),
                "tier_root":a0["tier"],"tier_rival":b0["tier"],"E4_max_tied":tied_max,
                "E4_max_rendered_tied":a0["rendered_key"][1]==b0["rendered_key"][1],
                "first_key_before":first_before,"first_key_after":first_after,
                "root_E4":a0,"rival_E4":b0,"root_z":a1,"rival_z":b1,
                "saturation_in_pair":any(x["r_A_one"] for x in pair_units.values()),
                "sat_only_relation":relation(replays["sat_only"],root,rival),
                "non_sat_only_relation":relation(replays["non_sat_only"],root,rival),
                "winning_pv_max":pv_max,"opposing_E4_count_max":count_max,
                "opposing_z_count_max":count_max_after,"opposing_z_PV_max":pv_max_after,
                "cross_type_max_competition":bool(pv_max and count_max_after and first_after==0 and a0["tier"]==b0["tier"]),
                "pure_count_opponent":bool(count_max_after and not pv_max_after),
                "revert_winning_pv_relation":relation(local,root,rival),
                "revert_winning_PV_group_relation":relation(local_group,root,rival),
                "channels":pair_units,
            })
        output["worlds"][world]={"RR":root_rr,"flips":flips,
                                 "replay_exact":True,"PV_count":len(forward),
                                 "saturated_PV_count":len(saturated)}
    return output


def without_backend_p_and_m(record):
    """Chỉ dùng để định vị chênh, mọi số khác và nhóm hòa vẫn được giữ."""
    import copy
    value=copy.deepcopy(record)
    value["config_id"]=value["variant"]="R0"

    def blocks(rows):
        for block in rows:
            key=block["key"]
            if len(key)!=5:
                raise ValueError("Không phải khóa S1 của B0")
            key[2]=None

    blocks(value["blocks"])
    for row in value["entity_ranking"]:
        if len(row["key"])!=5:
            raise ValueError("Khóa entity không phải S1")
        row["key"][2]=None
    extra=value["extra"]
    blocks(extra["blocks_P"])
    blocks(extra["T4c"]["blocks"])
    extra["T4c"]["m_don_vi"]={k:None for k in extra["T4c"]["m_don_vi"]}
    extra["T4c"]["m_thuc_the"]={k:[None,None] for k in extra["T4c"]["m_thuc_the"]}
    for unit in extra["don_vi_phan_vi"]:
        for direction in ("len","xuong"):
            unit[f"p_{direction}"]=None
    for world in WORLDS:
        blocks(value["worlds"][world]["blocks"])
        for unit in value["worlds"][world]["don_vi_dem"]:
            for direction in ("len","xuong"):
                unit[f"p_{direction}"]=None
    return value


class CacheMagnitude:
    """Memo cho hàm m thuần túy. Cờ và việc chọn m theo thực thể vẫn tính lại."""

    def __init__(self):
        self.values={}
        self.hits=0
        self.misses=0

    def wrap(self, native, kind):
        import hashlib
        import numpy as np

        def evaluate(*args):
            try:
                if kind == "phan_vi":
                    arrays=[np.asarray(values,dtype="<f8") for values in args]
                    key=(kind,*((array.shape,hashlib.sha256(array.tobytes()).digest()) for array in arrays))
                else:
                    key=(kind,*((type(value).__module__,type(value).__qualname__,Fraction(value)) for value in args))
            except (TypeError,ValueError,OverflowError):
                return native(*args)
            if key in self.values:
                self.hits+=1
                return self.values[key]
            self.misses+=1
            result=native(*args)
            self.values[key]=result
            return result
        return evaluate


def export_closed_controller(source, run_id):
    """Xuất nguyên byte native và phép chiếu N1/V0, giữ trung gian đầy đủ tại nguồn."""
    import hashlib
    import inspect
    from chay import OUT, read, dump, sha

    status=read(source/"kiem.json")
    command=read(source/"command.json")
    if not status["success"] or status["jobs"]!=len(status["finished"]):
        raise ValueError("Nguồn export chưa hoàn tất")
    target=(OUT/"runs"/run_id).resolve()
    if target.parent!=(OUT/"runs").resolve():
        raise ValueError("Đường export ngoài T-048")
    target.mkdir()
    bundle=target.parent/f"{run_id}-000";bundle.mkdir()
    jobs=command["plan"]["jobs"]
    by_job={}
    metadata={}
    configs=None
    for child in status["finished"]:
        folder=source.parent/child
        cmd,meta,pairs=read_run(folder)
        if len(cmd["plan"]["jobs"])!=1:
            raise ValueError("Nguồn không phải một cửa sổ/child")
        job=cmd["plan"]["jobs"][0]
        key=(job["opaque_id"],job["window"])
        if key in by_job:
            raise ValueError("Nguồn trùng cửa sổ")
        by_job[key]=(folder,cmd,meta,pairs)
        metadata[child]=meta
        if configs is None:
            configs=cmd["configs"]
        if configs!=cmd["configs"]:
            raise ValueError("Nguồn khác cấu hình")
    if set(by_job)!={(j["opaque_id"],j["window"]) for j in jobs}:
        raise ValueError("Nguồn thiếu cửa sổ")
    count=0
    with (bundle/"ban-ghi.jsonl").open("xb") as native,(
        bundle/"trung-gian.jsonl").open("x",encoding="utf-8",newline="\n") as thin:
        for job in jobs:
            folder,cmd,meta,pairs=by_job[(job["opaque_id"],job["window"])]
            reconstructed=[]
            for index,(record,detail) in enumerate(pairs()):
                reconstructed.append(dump(record).encode()+b"\n")
                states=detail["trace"]["world_state"]
                projected={w:{k:states[w][k] for k in ("N1","V0","valid_units")} for w in WORLDS}
                if projected["P"]["V0"]!=record["verdict"]:
                    raise ValueError("V0 chiếu khác native")
                row={k:v for k,v in detail.items() if k!="trace"}
                row["trace"]={"world_state":projected}
                row["original_child"]=folder.name
                row["original_row"]=index
                thin.write(dump(row)+"\n")
                count+=1
            original=(folder/"ban-ghi.jsonl").read_bytes()
            if b"".join(reconstructed)!=original:
                raise ValueError("Native khi xuất không trùng byte nguồn")
            native.write(original)
    exported={
        "plan":command["plan"],"configs":configs,"source_controller":str(source),
        "source_child_by_window":{o+"|"+w:folder.name for (o,w),(folder,_,_,_) in by_job.items()},
        "source_native_metadata":metadata,"intermediate_projection":"N1/V0 and valid units only",
        "full_intermediate_location":"source_controller sibling child directories",
        "producer_source":inspect.getsource(export_closed_controller),
    }
    (bundle/"command.json").write_text(dump(exported)+"\n",encoding="utf-8")
    (bundle/"kiem.json").write_text(dump({
        "records":count,"phase1_sha256":sha(bundle/"ban-ghi.jsonl"),
        "intermediate_sha256":sha(bundle/"trung-gian.jsonl"),
        "source_closed":True,"projection":True,
    })+"\n",encoding="utf-8")
    (target/"command.json").write_text(dump({"source":str(source),"plan":command["plan"],
                                           "export_bundle":bundle.name})+"\n",encoding="utf-8")
    (target/"kiem.json").write_text(dump({"success":True,"jobs":1,"finished":[bundle.name],
        "source_jobs":len(jobs),"source_status":status,"source_full_intermediates_retained":True})+"\n",encoding="utf-8")
    return target


if __name__ == "__main__":
    print(json.dumps({"z": kiem_z(), "luat_C": kiem_luat_c()}, ensure_ascii=False))
