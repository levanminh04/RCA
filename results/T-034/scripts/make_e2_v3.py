"""Tạo e2_bocpd_log_v3.py từ e2_bocpd_log_v2.py bằng các phép thay có kiểm.

Bản v3 chỉ thêm phần đo và một tham chiếu độc lập trên chuỗi thật (thiết kế, Mục nối 3); log_run, LogLikelihood, quy tắc m/CP,
fixture F1–F3 và dung sai đã khai không đổi.
Dùng: python make_e2_v3.py <v2> <v3>
"""
import ast
import sys
from pathlib import Path

s = Path(sys.argv[1]).read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert s.count(old) == 1, ("không tìm thấy đúng một lần", old[:70])
    s = s.replace(old, new, 1)


rep('"""T-034 E2 (bản v2): BOCPD của BARO với posterior và chuẩn hóa hoàn toàn trong miền log.\n',
    '"""T-034 E2 (bản v3): BOCPD của BARO với posterior và chuẩn hóa hoàn toàn trong miền log.\n\n'
    'Bản v3 thêm vào bản v2 (thiết kế, Mục nối 3; viết sau khi lượt e2-001 cho thấy m và CP khác bản gốc ở một chuỗi):\n'
    '  - tham chiếu độc lập trên chuỗi thật: đệ quy TUYẾN TÍNH như mã gốc nhưng bằng số thực mở rộng 80 bit (np.longdouble trên x86 Linux),\n'
    '    không dùng logsumexp; nếu trùng m và CP với bản miền log thì khác biệt với bản gốc không do cách cài miền log;\n'
    '  - khối lượng nằm ở trạng thái bị underflow ảnh hưởng (bằng 0, dưới chuẩn hóa, hoặc dòng dõi từng dưới chuẩn hóa), cột đầu tiên\n'
    '    khối lượng đó vượt 1e-12, sai số của trạng thái sạch trước cột đó, và các đoạn phân kỳ (khoảng cách biến thiên toàn phần > 1e-6);\n'
    '  - lớp "underflow_downstream" cho các chỗ m khác nằm trong đoạn phân kỳ do underflow mở đầu.\n')

rep('def log_run(X, hazard_function, likelihood, tick=None):\n',
    'def extended_linear_run(X, hazard_function, likelihood, tick=None):\n'
    '    """Tham chiếu độc lập: cùng đệ quy tuyến tính với online_changepoint_detection gốc, nhưng R là số thực mở rộng (np.longdouble).\n'
    '    Mật độ là exp của logpdf tính ở độ chính xác mở rộng. Không lấy exp float64: ở fixture F2 chính pdf float64 đã về 0 ở vài\n'
    '    trạng thái (lượt e2-fixtures-ec2-002-v3 và 003-v3 không đạt vì thế). Không có logsumexp."""\n'
    '    LD = np.longdouble\n'
    '    T = len(X)\n'
    '    R = np.zeros((T + 1, T + 1), dtype=LD)\n'
    '    R[0, 0] = 1\n'
    '    for t, x in enumerate(X):\n'
    '        predprobs = np.exp(likelihood.logpdf(x).astype(LD))\n'
    '        H = hazard_function(np.array(range(t + 1)))\n'
    '        R[1:t + 2, t + 1] = R[0:t + 1, t] * predprobs * (1 - H).astype(LD)\n'
    '        R[0, t + 1] = np.sum(R[0:t + 1, t] * predprobs * H.astype(LD))\n'
    '        R[:, t + 1] = R[:, t + 1] / np.sum(R[:, t + 1])\n'
    '        likelihood.update_theta(x, t=t)\n'
    '        if tick:\n'
    '            tick(t)\n'
    '    return R\n\n\n'
    'def extended_available():\n'
    '    return bool(np.finfo(np.longdouble).tiny < np.longdouble("1e-4000"))\n\n\n'
    'def log_run(X, hazard_function, likelihood, tick=None):\n')

# khối lượng ở trạng thái bị ảnh hưởng, sai số sạch trước cột đầu tiên có khối lượng đáng kể
rep('                                                    if bad[:, 1:].any() else None)\n',
    '                                                    if bad[:, 1:].any() else None)\n'
    '    affected = zero | denorm | (reach & dipped)\n'
    '    aff = np.full(T + 1, -np.inf)\n'
    '    for t in range(1, T + 1):\n'
    '        ac = affected[:, t]\n'
    '        if ac.any():\n'
    '            aff[t] = logsumexp(logR[ac, t])\n'
    '    over = np.flatnonzero(aff > np.log(1e-12))\n'
    '    first_aff = int(over[0]) if len(over) else None\n'
    '    out["first_column_affected_mass_gt_1e-12"] = first_aff\n'
    '    out["columns_affected_mass_gt_1e-12"] = int(len(over))\n'
    '    out["affected_mass_log_max"] = float(aff.max()) if np.isfinite(aff.max()) else None\n'
    '    out["affected_mass_log_max_column"] = int(np.argmax(aff)) if np.isfinite(aff.max()) else None\n'
    '    lim = first_aff if first_aff is not None else T + 1\n'
    '    out["posterior_log_abs_error_max_clean_before_affected_mass"] = float(err_clean[:, 1:lim].max()) if lim > 1 else 0.0\n'
    '    out["clean_states_before_affected_mass"] = int(clean[:, 1:lim].sum())\n')

rep('    out["total_variation_max_column"] = int(np.argmax(tv[1:])) + 1\n',
    '    out["total_variation_max_column"] = int(np.argmax(tv[1:])) + 1\n'
    '    big = tv > 1e-6\n'
    '    windows = []\n'
    '    t = 1\n'
    '    while t <= T:\n'
    '        if big[t]:\n'
    '            a = t\n'
    '            while t + 1 <= T and big[t + 1]:\n'
    '                t += 1\n'
    '            mass_a = float(np.exp(aff[a])) if np.isfinite(aff[a]) else 0.0\n'
    '            windows.append({"first_column": int(a), "last_column": int(t), "tv_first": float(tv[a]), "affected_mass_first": mass_a,\n'
    '                            "tv_max": float(tv[a:t + 1].max()), "underflow_initiated": bool(mass_a >= 0.5 * tv[a])})\n'
    '        t += 1\n'
    '    out["divergence_windows_tv_gt_1e-6"] = windows\n'
    '    out["columns_tv_gt_1e-6"] = int(big[1:].sum())\n'
    '    in_underflow_window = np.zeros(T + 3, dtype=bool)\n'
    '    for w in windows:\n'
    '        if w["underflow_initiated"]:\n'
    '            in_underflow_window[w["first_column"]: w["last_column"] + 2] = True\n')

rep('    classes = {"underflow": 0, "rounding_or_near_tie": 0, "other": 0}\n',
    '    classes = {"underflow": 0, "underflow_downstream": 0, "rounding_or_near_tie": 0, "other": 0}\n')
rep('        if native_value_at_log_map == 0 or native_value_at_log_map < TINY:\n'
    '            kind = "underflow"\n'
    '        elif min(gap_nat[i], gap_log[i]) <= NEAR_TIE:\n'
    '            kind = "rounding_or_near_tie"\n',
    '        if native_value_at_log_map == 0 or native_value_at_log_map < TINY or bool(affected[r_log, t]):\n'
    '            kind = "underflow"\n'
    '        elif min(gap_nat[i], gap_log[i]) <= NEAR_TIE:\n'
    '            kind = "rounding_or_near_tie"\n'
    '        elif in_underflow_window[t]:\n'
    '            kind = "underflow_downstream"\n')
rep('              "native_zero_count_by_column": zero.sum(axis=0), "native_subnormal_count_by_column": denorm.sum(axis=0),\n',
    '              "native_zero_count_by_column": zero.sum(axis=0), "native_subnormal_count_by_column": denorm.sum(axis=0), "affected_mass_log": aff,\n')

# fixture F4: kiểm chính tham chiếu mở rộng bằng tham chiếu mpmath (chỉ khi longdouble là 80 bit)
rep('    result["pass"] = bool(result["F1"]["pass"] and result["F2"]["pass"] and result["F3"]["pass"])\n',
    '    if extended_available():\n'
    '        with np.errstate(all="ignore"):\n'
    '            E2x = extended_linear_run(f2, hazard, LogLikelihood(nb.MultivariateT(dims=f2.shape[1])))\n'
    '            E3x = extended_linear_run(dummy, hazard, ScriptedLikelihood(f3))\n'
    '        with np.errstate(divide="ignore"):\n'
    '            l2 = np.log(E2x).astype(float)\n'
    '            l3 = np.log(E3x).astype(float)\n'
    '        x2 = compare_to_reference(l2, ref2, 1e-6, 1e-9)\n'
    '        x3 = compare_to_reference(l3, ref3, 1e-9, 1e-12)\n'
    '        f4_checks = {"F2: tham chiếu mở rộng trùng mpmath về MAP và CP": x2["m_equal_where_reference_gap_clear"] and x2["cp_equal"],\n'
    '                     "F2: |log R_mr - log R_tc| trong dung sai của F2": x2["within_tolerance"],\n'
    '                     "F3: tham chiếu mở rộng trùng mpmath về MAP và CP": x3["m_equal_all"] and x3["cp_equal"],\n'
    '                     "F3: |log R_mr - log R_tc| trong dung sai của F3": x3["within_tolerance"],\n'
    '                     "F3: tham chiếu mở rộng trùng bản miền log về MAP": bool(np.array_equal(m_and_cps(E3x)[0], m_and_cps(logR3)[0]))}\n'
    '        result["F4"] = {"status": "OK", "longdouble_log10_tiny": float(np.log10(np.finfo(np.longdouble).tiny)), "F2": x2, "F3": x3,\n'
    '                        "checks": f4_checks, "pass": all(f4_checks.values())}\n'
    '    else:\n'
    '        result["F4"] = {"status": "UNAVAILABLE", "reason": "np.longdouble trên máy này không phải số thực mở rộng 80 bit", "checks": {}, "pass": None}\n'
    '    result["pass"] = bool(result["F1"]["pass"] and result["F2"]["pass"] and result["F3"]["pass"] and result["F4"]["pass"] is not False)\n')
rep('        for name in ("F1", "F2", "F3"):\n'
    '            print(name, "PASS" if result[name]["pass"] else "FAIL", json.dumps(result[name]["checks"], ensure_ascii=False), flush=True)\n',
    '        for name in ("F1", "F2", "F3", "F4"):\n'
    '            verdict = "KHÔNG ÁP DỤNG" if result[name]["pass"] is None else ("PASS" if result[name]["pass"] else "FAIL")\n'
    '            print(name, verdict, json.dumps(result[name]["checks"], ensure_ascii=False), flush=True)\n')

# lượt chuỗi: thêm tham chiếu mở rộng
rep('    result, arrays = compare_full(R, logR, times, sorted(slices))\n',
    '    ext = {"status": "UNAVAILABLE"}\n'
    '    m_ext = None\n'
    '    if extended_available():\n'
    '        def tick_ext(step):\n'
    '            if step % 100 == 0 or step == T - 1:\n'
    '                note(stage="extended", step=int(step))\n'
    '        t0 = time.perf_counter()\n'
    '        with np.errstate(all="ignore"):\n'
    '            R_ext = extended_linear_run(X, hazard, LogLikelihood(nb.MultivariateT(dims=d)), tick_ext)\n'
    '        m_ext, cps_ext = m_and_cps(R_ext)\n'
    '        m_l, cps_l = m_and_cps(logR)\n'
    '        m_n, cps_n = m_and_cps(R)\n'
    '        reach_e = np.arange(T + 1)[:, None] <= np.arange(T + 1)[None, :]\n'
    '        reach_e[:, 0] = False\n'
    '        sel = reach_e & (logR >= -10000.0) & (R_ext > 0)\n'
    '        dlog = np.abs(np.log(R_ext[sel]).astype(float) - logR[sel])\n'
    '        ext = {"status": "OK", "dtype": str(R_ext.dtype), "longdouble_log10_tiny": float(np.log10(np.finfo(np.longdouble).tiny)),\n'
    '               "m_equal_log_domain": bool(np.array_equal(m_ext, m_l)), "cp_equal_log_domain": cps_ext == cps_l,\n'
    '               "m_equal_native": bool(np.array_equal(m_ext, m_n)), "cp_equal_native": cps_ext == cps_n, "cp": [int(i) for i in cps_ext],\n'
    '               "m_differences_vs_log_domain": int((m_ext != m_l).sum()), "m_differences_vs_native": int((m_ext != m_n).sum()),\n'
    '               "max_abs_log_difference_vs_log_domain": float(dlog.max()), "states_compared_logR_ge_-10000": int(sel.sum()),\n'
    '               "states_not_compared": int((reach_e & ~sel).sum()), "exact_zero_reachable_states": int((reach_e & (R_ext == 0)).sum()),\n'
    '               "tolerance_abs_log": 1e-8, "wall_s": round(time.perf_counter() - t0, 3)}\n'
    '        ext["pass"] = bool(ext["m_equal_log_domain"] and ext["cp_equal_log_domain"] and ext["max_abs_log_difference_vs_log_domain"] <= 1e-8)\n'
    '        note(stage="extended_done", **{k: v for k, v in ext.items() if k != "cp"})\n'
    '        del R_ext\n'
    '    result, arrays = compare_full(R, logR, times, sorted(slices))\n')
rep('               "comparison_native_vs_log": result, "lineage_cross_check": lineage_checks,\n',
    '               "comparison_native_vs_log": result, "extended_reference": ext, "lineage_cross_check": lineage_checks,\n')
rep('    arrays.update(m_stored=m_stored, cp_flags_stored=cp_stored, times=times, log_normalizer=log_norm)\n',
    '    arrays.update(m_stored=m_stored, cp_flags_stored=cp_stored, times=times, log_normalizer=log_norm)\n'
    '    if m_ext is not None:\n'
    '        arrays["m_extended"] = m_ext\n')
rep('"schema": "T034-E2-chain-v1"', '"schema": "T034-E2-chain-v3"')
ast.parse(s)
Path(sys.argv[2]).write_text(s, encoding="utf-8")
print("đã ghi", sys.argv[2], len(s))
