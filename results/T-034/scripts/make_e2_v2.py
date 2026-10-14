"""Tạo e2_bocpd_log_v2.py từ e2_bocpd_log.py bằng các phép thay có kiểm (chỉ thêm phần đo và so, không đổi phép tính)."""
import ast
import sys
from pathlib import Path

src = Path(sys.argv[1])
dst = Path(sys.argv[2])
s = src.read_text(encoding="utf-8")


def rep(old, new):
    global s
    assert s.count(old) == 1, ("không tìm thấy đúng một lần", old[:60])
    s = s.replace(old, new, 1)


rep('"""T-034 E2: BOCPD của BARO với posterior và chuẩn hóa hoàn toàn trong miền log.\n',
    '"""T-034 E2 (bản v2): BOCPD của BARO với posterior và chuẩn hóa hoàn toàn trong miền log.\n\n'
    'Bản v2 khác bản v1 (e2_bocpd_log.py, giữ nguyên cho lượt e2-001) ở phần ĐO và SO, không ở phép tính:\n'
    '  - tách các trạng thái vùng bình thường (R gốc >= 1e-290) theo lịch sử dòng dõi: dòng dõi từng xuống dưới ngưỡng chuẩn hóa\n'
    '    (R < 2,2e-308) hay chưa. Lý do: lượt e2-001 cho thấy trạng thái đi qua vùng dưới chuẩn hóa rồi lớn lên lại mang sai số làm tròn\n'
    '    lớn trong bản gốc; gộp chúng với trạng thái sạch làm tiêu chí 1e-9 mất nghĩa (thiết kế, Mục nối 2);\n'
    '  - thêm chế độ determinism để kiểm bản gốc chạy lại có trùng bản lưu từng bit không, theo cấu hình luồng BLAS.\n'
    'Hàm log_run, LogLikelihood, quy tắc m/CP, fixture và dung sai đã khai giữ nguyên từng dòng.\n')

rep('def compare_full(R, logR, times=None, slices=()):\n',
    'def lineage_dipped(R):\n'
    '    """dipped[r, t] = True nếu dòng dõi của trạng thái (r, t) từng có R gốc < TINY ở một cột trước đó (kể cả bằng 0)."""\n'
    '    T = R.shape[1] - 1\n'
    '    dipped = np.zeros(R.shape, dtype=bool)\n'
    '    for t in range(1, T + 1):\n'
    '        dipped[1:t + 1, t] = dipped[0:t, t - 1] | (R[0:t, t - 1] < TINY)\n'
    '    return dipped\n\n\n'
    'def compare_full(R, logR, times=None, slices=()):\n')

rep('    out["normal_zone_states"] = int(normal[:, 1:].sum())\n',
    '    out["normal_zone_states"] = int(normal[:, 1:].sum())\n'
    '    dipped = lineage_dipped(R)\n'
    '    clean = normal & ~dipped\n'
    '    dirty = normal & dipped\n'
    '    err_clean = np.where(clean, err, 0.0)\n'
    '    err_dirty = np.where(dirty, err, 0.0)\n'
    '    out["normal_zone_states_lineage_never_subnormal"] = int(clean[:, 1:].sum())\n'
    '    out["normal_zone_states_lineage_was_subnormal"] = int(dirty[:, 1:].sum())\n'
    '    out["posterior_log_abs_error_max_lineage_never_subnormal"] = float(err_clean[:, 1:].max())\n'
    '    out["posterior_log_abs_error_max_lineage_was_subnormal"] = float(err_dirty[:, 1:].max())\n'
    '    bad = dirty & (err > 1e-9)\n'
    '    out["states_error_gt_1e-9_lineage_was_subnormal"] = int(bad[:, 1:].sum())\n'
    '    out["states_error_gt_1e-9_lineage_never_subnormal"] = int((clean & (err > 1e-9))[:, 1:].sum())\n'
    '    out["max_log_mass_of_states_error_gt_1e-9"] = (float(np.max(np.where(bad, np.where(finite_log, logR, -np.inf), -np.inf)[:, 1:]))\n'
    '                                                    if bad[:, 1:].any() else None)\n')

rep('    sham["pass"] = bool(sham["m_equal_stored"] and sham["cp_flags_equal_stored"] and sham["R_relative_error_max_normal_zone"] <= 1e-9 and sham["R_all_finite"])\n',
    '    dipped_stored = lineage_dipped(R_stored) | lineage_dipped(R)\n'
    '    clean = normal & ~dipped_stored\n'
    '    dirty = normal & dipped_stored\n'
    '    rel_all = np.zeros_like(R)\n'
    '    rel_all[normal] = np.abs(R[normal] - R_stored[normal]) / R_stored[normal]\n'
    '    sham["R_relative_error_max_lineage_never_subnormal"] = float(rel_all[clean].max()) if clean.any() else 0.0\n'
    '    sham["R_relative_error_max_lineage_was_subnormal"] = float(rel_all[dirty].max()) if dirty.any() else 0.0\n'
    '    sham["normal_zone_states_lineage_never_subnormal"] = int(clean.sum())\n'
    '    sham["normal_zone_states_lineage_was_subnormal"] = int(dirty.sum())\n'
    '    # tiêu chí đã khai trong thiết kế (giữ nguyên): m, CP trùng tuyệt đối; R lệch tương đối <= 1e-9 trên mọi phần tử >= 1e-290\n'
    '    sham["pass"] = bool(sham["m_equal_stored"] and sham["cp_flags_equal_stored"] and sham["R_relative_error_max_normal_zone"] <= 1e-9 and sham["R_all_finite"])\n'
    '    # báo riêng (Mục nối 2, sau khi đã thấy lượt e2-001): phần bắt buộc m/CP; và tiêu chí R chỉ trên dòng dõi chưa từng dưới chuẩn hóa\n'
    '    sham["pass_m_cp_exact"] = bool(sham["m_equal_stored"] and sham["cp_flags_equal_stored"] and sham["R_all_finite"])\n'
    '    sham["pass_R_1e-9_lineage_never_subnormal"] = bool(sham["R_relative_error_max_lineage_never_subnormal"] <= 1e-9)\n')

rep('               "interpretable": bool(sham["pass"]), "wall_s_total"',
    '               "interpretable": bool(sham["pass"]), "interpretable_by_m_cp_exact": bool(sham["pass_m_cp_exact"]), "wall_s_total"')

DET = r'''    if mode == "determinism":
        npz_path, out_json, baro_root = Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4]
        nb, bocpd_sha = load_native(baro_root)
        z = np.load(npz_path, allow_pickle=False)
        X = z["X"]
        T, d = X.shape
        t0 = time.perf_counter()
        nat = nb.MultivariateT(dims=d)
        stored_pdf = z["predictive_density"]
        first_pdf_diff, pdf_bit_equal_rows, pdf_rel_max = None, 0, 0.0
        R = np.zeros((T + 1, T + 1))
        R[0, 0] = 1
        hazard = partial(nb.constant_hazard, HAZARD_LAM)
        for t, x in enumerate(X):                      # chép đúng vòng lặp gốc để soi density từng bước
            predprobs = nat.pdf(x)
            row = stored_pdf[t, : t + 1]
            if np.array_equal(predprobs, row):
                pdf_bit_equal_rows += 1
            else:
                if first_pdf_diff is None:
                    j = int(np.flatnonzero(predprobs != row)[0])
                    first_pdf_diff = {"step": int(t), "run_length": j, "now": float(predprobs[j]), "stored": float(row[j])}
                ok = row > 0
                pdf_rel_max = max(pdf_rel_max, float(np.max(np.abs(predprobs[ok] - row[ok]) / row[ok])))
            H = hazard(np.array(range(t + 1)))
            R[1:t + 2, t + 1] = R[0:t + 1, t] * predprobs * (1 - H)
            R[0, t + 1] = np.sum(R[0:t + 1, t] * predprobs * H)
            R[:, t + 1] = R[:, t + 1] / np.sum(R[:, t + 1])
            nat.update_theta(x, t=t)
        m, cps = m_and_cps(R)
        res = {"schema": "T034-E2-determinism-v1", "npz": str(npz_path), "npz_sha256": sha(npz_path), "T": int(T), "d": int(d),
               "environment": environment(bocpd_sha, baro_root), "wall_s": round(time.perf_counter() - t0, 3),
               "pdf_rows_bit_equal_stored": pdf_bit_equal_rows, "pdf_rows": int(T), "pdf_first_difference": first_pdf_diff,
               "pdf_relative_difference_max": pdf_rel_max,
               "R_bit_equal_stored": bool(np.array_equal(R, z["R"])), "R_bit_equal_fraction": float((R == z["R"]).mean()),
               "m_equal_stored": bool(np.array_equal(m, z["m"])), "R_sha256": hashlib.sha256(np.ascontiguousarray(R).tobytes()).hexdigest()}
        try:
            from threadpoolctl import threadpool_info
            res["threadpools"] = threadpool_info()
        except Exception as exc:                        # pragma: no cover
            res["threadpools"] = repr(exc)
        out_json.parent.mkdir(parents=True, exist_ok=True)
        out_json.write_text(json.dumps(res, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(json.dumps({k: v for k, v in res.items() if k not in ("environment", "threadpools")}, ensure_ascii=False), flush=True)
        return

    assert mode == "chain"
'''
rep('    assert mode == "chain"\n', DET)
ast.parse(s)
dst.write_text(s, encoding="utf-8")
print("đã ghi", dst, len(s))
