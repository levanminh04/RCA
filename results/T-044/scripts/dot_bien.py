"""Phép đột biến (SPEC T-044 bước 7, tiêu chí 6): mỗi đột biến thay đúng một chỗ trong bản sao tạm của `src/`, chạy
toàn bộ test, ghi số phép trượt. Không sửa repo, không commit đột biến. Lượt đối chứng không đột biến phải xanh.

    python -B results/T-044/scripts/dot_bien.py results/T-044/runs/dot-bien-001
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PY = sys.executable

DOT_BIEN = [
    ('D01-dao-lop-lan', 'src/m1/e5.py', "        if c.lop == 'lan_nguoc':", "        if c.lop == 'lan_xuoi':",
     'E5: đảo quy tắc lan ngược và lan xuôi'),
    ('D02-bo-cat-con-E1', 'src/m1/span.py', "        cat, v = cat_con((s['start'], s['end']), khoang, tau)",
     "        cat, v = list(khoang), 0", 'E1-U: bỏ cắt con về khoảng của cha'),
    ('D03-doi-khoa-hoa', 'src/m1/xep_hang.py', "    return (max(s), len(s), sum(s, Fraction(0)))",
     "    return (max(s), sum(s, Fraction(0)), len(s))", 'Khóa K: đổi chỗ số kênh và tổng điểm'),
    ('D04-bo-duyet-list-truong-cam', 'src/m1/hop_dong.py', "    elif isinstance(obj, (list, tuple)):",
     "    elif isinstance(obj, ()):", 'Bộ kiểm trường cấm: không duyệt list, tuple'),
    ('D05-doi-delta-luat-C', 'src/m1_danh_gia/luat_c.py', "DELTA = Fraction(1, 100)", "DELTA = Fraction(2, 100)",
     'Luật C: δ = 0,02 thay 0,01'),
    ('D06-ro-ma-mo-vao-params', 'src/m1/runner.py', "    p['config_id'] = cau_hinh['config_id']",
     "    p['config_id'] = cau_hinh['config_id'] + '@' + ca['opaque_id']", 'Pha 1: đưa mã mờ vào params'),
    ('D07-m1-import-bo-danh-gia', 'src/m1/chuoi.py', "from m1.kieu import Kenh",
     "from m1.kieu import Kenh\nfrom m1_danh_gia import rr as _rr  # noqa: F401", 'src/m1 import bộ đánh giá'),
    ('D08-doc-duong-dan-nhan', 'src/m1/runner.py', "class LoiRoNhan(ValueError):",
     "NHAN = 'results/T-022/nhan-dev.json'\n\n\nclass LoiRoNhan(ValueError):", 'Pha 1 trỏ tới file nhãn'),
    ('D09-bo-tau-CRISP', 'src/m1/span.py', "    if c[0] > d[0] or not (c[1] - tau < d[0]):",
     "    if c[0] > d[0] or not (c[1] < d[0]):",
     'E1-CP: bỏ dung sai τ của happensBefore'),
    ('D10-nhom-vong-mac-dinh-ke-canh', 'src/m1/e5.py',
     "def phan_loai(kenh, canh, bat=True, doc_nhom_vong='co_vong',",
     "def phan_loai(kenh, canh, bat=True, doc_nhom_vong='ke_canh',", 'E5: cách đọc nhóm vòng mặc định A thay C′'),
    ('D11-E7-any-thay-all', 'src/m1/e7.py', "                if all(k.ma in gt",
     "                if any(k.ma in gt", 'E7 cách 1: "mọi kênh có giải thích" thành "một kênh"'),
    ('D12-E9-bien-2-o', 'src/m1/e9.py', "    if all(b - kp_e > 2 * o_s + tau for b in kp_B):",
     "    if all(b - kp_e >= 2 * o_s for b in kp_B):", 'E9: bỏ τ và lấy cả biên đúng 2 ô'),
    ('D13-lambda-dao', 'src/m1/e4.py', "    lam = Fraction(n_N) * Fraction(T_A) / Fraction(T_N)  # chính xác theo T đã cho",
     "    lam = Fraction(n_N) * Fraction(T_N) / Fraction(T_A)",
     'Đơn vị đếm: λ dùng T đảo'),
    ('D14-damping', 'src/m1/xep_hang.py', "DAMPING = 0.85", "DAMPING = 0.80", 'E6b: hệ số tắt dần 0,80'),
    ('D15-bien-cong-chinh-xac', 'src/m1/e4.py', "    if n <= n_exact_max:", "    if n < n_exact_max:",
     'E4: n = 100 chuyển sang xấp xỉ'),
    ('D16-dao-the-gioi', 'src/m1/quan_sat.py', "'S_lo': (Tm['N'], Tc['A']), 'S_hi': (Tc['N'], Tm['A'])",
     "'S_lo': (Tc['N'], Tm['A']), 'S_hi': (Tm['N'], Tc['A'])", 'Ba thế giới: đổi S_lo và S_hi'),
    ('D17-E3-hoan-toan-thanh-nguong', 'src/m1/e3.py',
     "        c = drain.fast_match(trong_la, tokens, 1.0, True) if trong_la else None",
     "        c = drain.fast_match(trong_la, tokens, sim_th, False) if trong_la else None",
     'E3 cách khớp (a): dùng ngưỡng thay khớp hoàn toàn'),
    ('D18-tang-bo-E5', 'src/m1/xep_hang.py',
     "        tang[e] = 1 if K_I[e][1] > 0 else (2 if K_raw[e][1] > 0 else 3)",
     "        tang[e] = 1 if K_raw[e][1] > 0 else 3", 'Tầng: bỏ tầng kế thừa'),
    ('D19-bo-sap-kenh-E5', 'src/m1/e5.py',
     "    co = sorted((k for k in kenh if k.co), key=lambda k: k.ma)  # thứ tự chuẩn: đầu ra không phụ thuộc thứ tự vào",
     "    co = [k for k in kenh if k.co]", 'E5: bỏ thứ tự chuẩn (chỉ lộ khi xáo hàng, chạy với M1_XAO=1)'),
    ('D20-metric-khong-khai-dung-metrics-time', 'src/m1/chuoi.py',
     "            ng = nguon_cua.get(cot)\n", "            ng = nguon_cua.get(cot, 'metric')\n",
     'Chuỗi: cột metric không khai nguồn vẫn được chấm'),
    ('D21-chuoi-mac-dinh-ke-canh', 'src/m1/chuoi.py', "doc_nhom_vong=tham_so_E5.get('doc_nhom_vong', 'co_vong')",
     "doc_nhom_vong=tham_so_E5.get('doc_nhom_vong', 'ke_canh')", 'Chuỗi: thiếu tham_so_E5 thì dùng cách đọc A'),
    # sau phản biện lượt 1 (LOG T-044, mục "Phản hồi phản biện lượt 1 và gói sửa")
    ('D22-luat-C-bo-boi-so-o', 'src/m1_danh_gia/luat_c.py', "        k = boi[o]\n", "        k = 1\n",
     'Luật C: P, M đếm mỗi ô một lần dù ô được lấy k lần'),
    ('D23-M5-bo-boi-so', 'src/m1_danh_gia/pha2.py',
     "            them['M5'] = (sum(_w(trong_so, o) * tat[o]['theo_the_gioi'][w]['M5'] for o in tat),",
     "            them['M5'] = (sum(tat[o]['theo_the_gioi'][w]['M5'] for o in tat),", 'Cờ M5 nhánh tắt: bỏ bội số'),
    ('D24-UV6-bo-boi-so', 'src/m1_danh_gia/uv6.py', "        w = c.get('trong_so', 1)\n", "        w = 1\n",
     'UV-6: bỏ bội số'),
    ('D25-moc-gia-bo-boi-so', 'src/m1_danh_gia/pha2.py', "    n = sum(_w(trong_so, o) for o, _, _ in giu)\n",
     "    n = len(giu)\n", 'Mốc giả: mẫu số không theo bội số'),
    ('D26-bo-coverage-metric', 'src/m1/chuoi.py',
     "            qs[ng_s] = _nguon(ng_s, [m for m in tg[ng_s]['moc'] if lo_ns <= m < hi_ns])\n",
     "            pass\n", 'Chuỗi: không xuất trạng thái quan sát của nguồn metric'),
    ('D27-WD-cap-dau-bang', 'src/m1_danh_gia/the_gioi.py',
     "            if qp != qw:\n",
     "            if qw == 'truoc' or qp != qw:\n",
     'WORLD_DEPENDENT: lấy mọi thực thể đứng trước root, kể cả thực thể đã đứng trước ở P'),
    # sau phản biện lượt 2 (LOG T-044, mục "Phản hồi phản biện lượt 2 và gói sửa")
    ('D28-MRR-so-thuc', 'src/m1_danh_gia/pha2.py', "            kq['MRR_the_gioi'][w] = m\n",
     "            kq['MRR_the_gioi'][w] = {k: float(v) for k, v in m.items()}\n", 'Pha 2: MRR đổi sang số thực'),
    ('D29-o-boi-so-0', 'src/m1_danh_gia/rr.py', "    return {o: tong[o] / dem[o] for o in tong if dem[o] != 0}",
     "    return {o: tong[o] / dem[o] for o in tong}", 'RR_o: ô bội số 0 vẫn chia'),
    ('D30-buoc8-bo-PTQS', 'src/m1_danh_gia/chon_khoi.py',
     "        v = _kc_ptqs(v)",
     "        v = _kc(v)", 'Bước 8: đọc kết cục tại P của cặp phụ thuộc quan sát'),
    ('D31-T12-thieu-khoa-thanh-ERROR', 'src/m1/chuoi.py',
     "        if not isinstance(ct, dict) or 'revision' not in ct or 'canh' not in ct:",
     "        if not isinstance(ct, dict):", 'T12: thiếu khóa con của canh_tinh không ra UNSUPPORTED'),
    ('D32-bo-thong-ke-log', 'src/m1/chuoi.py', "                  'thong_ke_log': thong_ke_log,",
     "                  'thong_ke_log': None,", 'Bản ghi bỏ thống kê severity và cặp Drain'),
    ('D33-WD-hoa-thanh-sau', 'src/m1_danh_gia/the_gioi.py', "    return 'hoa'\n", "    return 'sau'\n",
     'WORLD_DEPENDENT: coi hòa là đứng sau'),
    ('D34-WD-bo-thuc-the-vang', 'src/m1_danh_gia/the_gioi.py',
     "        for e in sorted((set(vP) | set(vw)) - {root}):", "        for e in sorted((set(vP) & set(vw)) - {root}):",
     'WORLD_DEPENDENT: chỉ xét thực thể có ở cả hai thế giới'),
    ('D35-trang-thai-metric-chi-khi-co-hang', 'src/m1/chuoi.py', "    for ng_s in sorted(tg):\n",
     "    for ng_s in (sorted(tg) if metrics else []):\n", 'Chuỗi: không xuất trạng thái nguồn metric khi không có hàng'),
    # lượt 3 (S12, S13, S16)
    ('D36-ma-kenh-bo-don-vi', 'src/m1/kieu.py', "        return f'{self.thuc_the}|{self.don_vi}|{self.ten}|{self.huong}'",
     "        return f'{self.thuc_the}|{self.ten}|{self.huong}'", 'Mã kênh: bỏ đơn vị (mã cũ thực thể|tên|hướng)'),
    ('D37-E5-bo-kiem-trung-ma', 'src/m1/e5.py', "    if len(set(ma_all)) != len(ma_all):",
     "    if False:", 'E5: không báo lỗi khi hai kênh trùng mã'),
    ('D38-E7-tra-theo-ten', 'src/m1/e7.py',
     "    gt = {x['ma'] for x in inherited_by if x['trang_thai'] in ('de_xuat', 'ap_dung')}",
     "    gt = {k.ma for k in co if any(x['thuc_the'] == k.thuc_the and x['kenh'] == k.ten and x['huong'] == k.huong"
     " and x['trang_thai'] in ('de_xuat', 'ap_dung') for x in inherited_by)}", 'E7: tra giải thích theo tên kênh'),
    ('D39-WD-cap-kenh-manh-nhat', 'src/m1_danh_gia/the_gioi.py',
     "        return [x['ma'] for x in kd] if kd else manh(w, e)", "        return manh(w, e)",
     'WORLD_DEPENDENT: cặp luôn lấy kênh mạnh nhất, bỏ kênh đổi'),
    ('D40-WD-bo-phan-khoa', 'src/m1_danh_gia/the_gioi.py',
     "            return {'chi_so': i, 'ten': ten[i] if i < len(ten) else f'k{i}'}", "            return None",
     'WORLD_DEPENDENT: không ghi phần khóa phân định'),
    ('D41-UV6-ky-vong-bo-boi-so', 'src/m1_danh_gia/uv6.py',
     "                x['tang_ca_loi_ma'] += w * max(Fraction(0), bat - tat)",
     "                x['tang_ca_loi_ma'] += max(Fraction(0), bat - tat)", 'UV-6 báo kèm: bỏ bội số'),
    # E1-CP và bước 5 (Minh duyệt 30/10/2026)
    ('D42-E1CP-bo-con-da-chon', 'src/m1/span.py',
     "            khac = [e for i, e in enumerate(tat_ca) if i not in (j, k)]  # gồm cả con đã chọn",
     "            khac = [e for i, e in enumerate(tat_ca) if i in con_lai and i != j]",
     'E1-CP: kiểm vùng chồng lấn chỉ với con còn lại'),
    ('D43-E1CP-bien-dong', 'src/m1/span.py', "    return not any(lo < x < hi for e in khac for x in e)",
     "    return not any(lo <= x <= hi for e in khac for x in e)", 'E1-CP: biên đóng'),
    ('D44-buoc5-ket-cuc-P', 'src/m1_danh_gia/chon_khoi.py',
     "                if v is not None and _kc_ptqs(v) == 'KHONG_DU_CA':",
     "                if v is not None and _kc(v) == 'KHONG_DU_CA':", 'Bước 5: đọc kết cục tại P của cặp phụ thuộc quan sát'),
    # lượt 4 (dinh-chinh-cai-dat.md C6)
    ('D45-E4-ty-le-so-thuc', 'src/m1/e4.py', "    rA_len, rA_xuong = ty_le_vuot_q(XA, ng['h'], ng['l'])",
     "    rA_len, rA_xuong = ty_le_vuot(XA, ng['h'], ng['l'])", 'E4 phân vị: tỷ lệ vượt của A tính bằng số thực'),
    ('D46-E4-lambda-so-thuc', 'src/m1/e4.py', "    lam = Fraction(n_N) * Fraction(T_A) / Fraction(T_N)  # chính xác theo T đã cho",
     "    lam = n_N * T_A / T_N", 'E4 đếm: λ tính bằng số thực'),
    ('D47-khoa-tong-so-thuc', 'src/m1/xep_hang.py', "    return (max(s), len(s), sum(s, Fraction(0)))",
     "    return (max(s), len(s), Fraction(math.fsum(float(x) for x in s)))", 'Khóa: Σs cộng bằng số thực'),
    ('D48-z-giu-co-vo-han', 'src/m1/chuoi.py',
     "                            kq[f'F_raw_{d}'], kq[f'e_{d}'], kq[f'e_{d}_q'] = 0, 0.0, Fraction(0)",
     "                            kq[f'e_{d}'], kq[f'e_{d}_q'] = z[f'z_{d}'], None", 'Nhánh z: giữ cờ và điểm không hữu hạn'),
    ('D49-T4c-log-so-thuc', 'src/m1/e4.py', "    return _log1p_q(abs(mA - mN) / max(abs(mN), r_u))",
     "    return math.log(1 + float(abs(mA - mN)) / float(max(abs(mN), r_u)))", 'T4c: log tính trên số thực'),
    ('D50-bo-kiem-JSON', 'src/m1/chuoi.py', "        json.dumps(rec, allow_nan=False)",
     "        json.dumps(rec, allow_nan=True)", 'Chuỗi: không chặn bản ghi có giá trị không hữu hạn'),
    ('D51-bo-kiem-gia-tri-bat-tat', 'src/m1/chuoi.py',
     "        if not any(v is x if isinstance(x, bool) else (isinstance(v, str) and v == x) for x in cho_phep):",
     "        if False:", 'Chuỗi: không kiểm giá trị của bat_tat'),
    ('D52-bo-pi-goc', 'src/m1/chuoi.py',
     "                  'E6b_pi': ({w: dict(sorted(xh_w[w]['pi'].items())) for w in WORLDS} if E6 == 'b' else None),",
     "                  'E6b_pi': None,", 'Bản ghi bỏ π gốc của E6b'),
    ('D53-bo-kiem-so-moc', 'src/m1/chuoi.py',
     "        if tg[ng_s]['trang_thai'] == 'OK' and len(tg[ng_s]['moc']) != len(metrics):  # mốc ghép theo hàng (S24)",
     "        if False:", 'Chuỗi: không kiểm số mốc của nguồn metric'),
    ('D54-map-boi-so-thua', 'src/m1_danh_gia/rr.py', "        raise ValueError(f'map bội số thiếu ca {ma}')",
     "        return Fraction(1)", 'Bội số: ca thiếu trong map tự lấy 1'),
    ('D55-pha2-bo-kiem-du-tich', 'src/m1_danh_gia/pha2.py', "    if len(cap) != len(cfg) * len(ca):",
     "    if False:", 'Pha 2: không kiểm đủ tích cấu hình × ca'),
    ('D56-pha2-bo-kiem-so-dong', 'src/m1_danh_gia/pha2.py', "    if len(recs) != meta.get('so_ban_ghi'):",
     "    if False:", 'Pha 2: không kiểm số dòng thật với metadata'),
    ('D57-E7-luon-dung-vung', 'src/m1/chuoi.py', "    E7 = params.get('doi_chung') not in DOI_CHUNG_KHONG_E7",
     "    E7 = True", 'C-a0, C-a1 vẫn dựng vùng E7'),
    ('D58-chon-bo-kiem-cap', 'src/m1_danh_gia/chon_khoi.py', "    if sorted(can - set(cap)):",
     "    if False:", 'Luật chọn khối: không kiểm đủ cặp'),
    ('D59-chon-bo-kiem-du-cau-hinh', 'src/m1_danh_gia/chon_khoi.py', '    if set(MRR) != du:\n',
     '    if False:\n', 'Luật chọn khối: không kiểm đủ 2^n cấu hình (G1)'),
    ('D60-chon-bo-kiem-it-ca-do-thi', 'src/m1_danh_gia/chon_khoi.py', "    for nhan_ds, ds_tp in (('it_ca', it_ca), ('do_thi', do_thi)):\n        if isinstance(ds_tp, str) or not set(ds_tp) <= set(thanh_phan):\n",
     "    for nhan_ds, ds_tp in (('it_ca', it_ca), ('do_thi', do_thi)):\n        if False:\n", 'Luật chọn khối: không kiểm it_ca, do_thi (G1)'),
    ('D61-buoc8-thieu-cap-bo-qua', 'src/m1_danh_gia/chon_khoi.py', "            raise ValueError(f'thiếu cặp cho bước 8: {k}')",
     '            continue', 'Bước 8: thiếu cặp thì bỏ qua (G1)'),
    ('D62-luat-C-nhan-so-thuc', 'src/m1_danh_gia/luat_c.py', '    if isinstance(x, bool) or not isinstance(x, (Fraction, int)):',
     '    if False:', 'Luật C: nhận số thực (G2)'),
    ('D63-boi-so-khong-nguyen', 'src/m1_danh_gia/rr.py', '    if isinstance(w, bool) or not isinstance(w, (int, Fraction)) or w < 0 or Fraction(w).denominator != 1:',
     '    if isinstance(w, bool) or Fraction(w) < 0:', 'Bội số: nhận chuỗi, số không nguyên (G2)'),
    ('D64-uv6-hit1-so-thuc', 'src/m1_danh_gia/uv6.py', '            if isinstance(c[k], bool) or not isinstance(c[k], (int, Fraction)):',
     '            if False:', 'UV-6: nhận Hit@1 số thực (G2)'),
    ('D65-luat-C-E_X-ngoai-ds', 'src/m1_danh_gia/luat_c.py', '    if isinstance(E_X, str) or not set(E_X) <= set(o_cua.values()):',
     '    if False:', 'Luật C: không kiểm E_X thuộc tập ô (G3)'),
    ('D66-luat-C-ma-ca-trung', 'src/m1_danh_gia/luat_c.py', "        if c['ma'] in o_cua:",
     '        if False:', 'Luật C: không kiểm mã ca trùng (G3)'),
    ('D67-pha2-bo-kiem-nhan', 'src/m1_danh_gia/pha2.py', '        if thanh_phan != mong:',
     '        if False:', 'Pha 2: không kiểm nhãn thành phần của cặp (G4)'),
    ('D68-buoc8-PTQS-khong-it-ca', 'src/m1_danh_gia/chon_khoi.py', "        if isinstance(v, dict) and v['phu_thuoc_quan_sat'] and x not in it_ca:",
     '        if False:', 'Bước 8: thành phần không ít ca đọc như ít ca (G5, Q1)'),
    ('D69-ma-noi-dung-bo-doi-chung', 'src/m1/runner.py', '    if doi_chung is not None:',
     '    if False:', 'Mã nội dung không gồm doi_chung (G6)'),
    ('D70-bo-kiem-trung-ma-don-vi', 'src/m1/chuoi.py', '    if len(set(ma_dv)) != len(ma_dv):',
     '    if False:', 'Chuỗi: không kiểm trùng mã đơn vị (S27)'),
    ('D71-verdict-ngoai-U', 'src/m1/chuoi.py', " if kq.get('hop_le') and u['thuc_the'] in set(U))",
     " if kq.get('hop_le'))", 'Verdict đếm cả phép chấm ngoài U (S28, Q2)'),
    ('D72-nguong-tran', 'src/m1/e4.py', '    h = min(q_hi + eps * abs(q_hi), MAX_THUC)',
     '    h = q_hi + eps * abs(q_hi)', 'E4: ngưỡng trên có thể tràn (S29)'),
    ('D73-STOPPED-moi-huong', 'src/m1/e4.py', "    if n_A == 0 and n_N >= ts['count_min'] and 'xuong' in huong_cham:",
     "    if n_A == 0 and n_N >= ts['count_min']:", 'STOPPED cả ở hướng không chấm (S30, Q5)'),
    ('D74-nhanh-z-khong-kiem', 'src/m1/chuoi.py', "    if not isinstance(params.get('nhanh_z', False), bool):",
     '    if False:', 'Chuỗi: không kiểm kiểu nhanh_z (S31)'),
    ('D75-tham-so-E4-khong-kiem', 'src/m1/chuoi.py', '    if not isinstance(t4, dict) or set(t4) != set(TS_E4_KHOA):',
     '    if False:', 'Chuỗi: không kiểm khóa tham_so_E4 (S31)'),
    ('D76-params-ca-doi-chung', 'src/m1/runner.py', "    if 'doi_chung' in rieng:",
     '    if False:', 'Runner: params_ca được mang doi_chung (S31)'),
    ('D77-E1CP-con-long', 'src/m1/span.py', '    if c[0] > d[0] or not (c[1] - tau < d[0]):',
     '    if not (c[1] - tau < d[0]):', 'E1-CP: nhận con bắt đầu trong khoảng của nút đang xét (S32, Q3)'),
    ('D78-bo-khong-moc-gia', 'src/m1_danh_gia/pha2.py', '    if moc_gia is not None:  # vế mốc giả',
     '    if False:  # vế mốc giả', 'Pha 2: không báo kèm kết cục khi chưa áp mốc giả (S33)'),
    ('D79-E6b-bo-khoa-phu', 'src/m1/xep_hang.py', 'items.append((e, (p,) + tuple(K_I[e]) + tuple(K_raw[e])))',
     'items.append((e, (p,)))', 'E6b: không dùng K_I, K_raw phá hòa π (N01)'),
    ('D80-nhom-hoa-khoa-chinh-xac', 'src/m1/xep_hang.py', '        if blocks and cu == _thuc(k):',
     '        if blocks and cu_q == tuple(k):', 'Gộp hòa theo khóa chính xác thay khóa ghi ra (ngược K07; S35)'),
    ('D81-E6b-khong-lam-tron', 'src/m1/xep_hang.py', 'p = _lam_tron_12(pi.get(e, 0.0))',
     'p = pi.get(e, 0.0)', 'E6b: không làm tròn π 12 chữ số (N02)'),
    ('D82-CP-tau-le', 'src/m1/span.py', '    if c[0] > d[0] or not (c[1] - tau < d[0]):',
     '    if c[0] > d[0] or not (c[1] - tau <= d[0]):', 'E1-CP: happensBefore không chặt (N22)'),
    ('D83-CP-LFC-hoa', 'src/m1/span.py', 'tat_ca = sorted(cat, key=lambda x: (x[1], x[0]))',
     'tat_ca = sorted(cat, key=lambda x: (x[1], -x[0]))', 'E1-CP: hòa LFC chọn con bắt đầu sớm (N24)'),
    ('D84-C-giup-ge', 'src/m1_danh_gia/luat_c.py', "if dM['gop'] > delta and t['P'] > t['M']",
     "if dM['gop'] >= delta and t['P'] > t['M']", 'Luật C: GIÚP khi ΔMRR = δ (N30)'),
    ('D85-C-ktd-lt', 'src/m1_danh_gia/luat_c.py', "if abs(dM['gop']) <= delta:",
     "if abs(dM['gop']) < delta:", 'Luật C: |ΔMRR| = δ không là KHÔNG TÁC DỤNG (N31)'),
    ('D86-C-P-ge-M', 'src/m1_danh_gia/luat_c.py', "t['P'] > t['M'] and not",
     "t['P'] >= t['M'] and not", 'Luật C: GIÚP khi P = M (N33)'),
    ('D87-C-trai-chieu-ge', 'src/m1_danh_gia/luat_c.py', 'if any(dM[a] > dd[a] for a in ds) and any(dM[b] < -dd[b] for b in ds):',
     'if any(dM[a] >= dd[a] for a in ds) and any(dM[b] <= -dd[b] for b in ds):', 'Luật C: TRÁI CHIỀU tại biên (N34)'),
    ('D88-C-PM-moi-o', 'src/m1_danh_gia/luat_c.py', '        if o in E_X:\n',
     '        if True:\n', 'Luật C: P, M đếm cả ô ngoài E_X (N36)'),
    ('D89-C-buoc4-truoc-3', 'src/m1_danh_gia/luat_c.py', "    if dM['gop'] < -delta:\n",
     "    if dM['gop'] < -delta and t['so_o_E_X'] >= O_TOI_THIEU:\n", 'Luật C: KHÔNG ĐỦ CA trước HẠI gộp (N37)'),
    ('D90-moc-gia-le', 'src/m1_danh_gia/moc_gia.py', 'elif tang > NGUONG:',
     'elif tang >= NGUONG:', 'Mốc giả: HẠI khi tăng đúng 0,1 (N39)'),
    ('D91-moc-gia-khong-phan-xu-lt', 'src/m1_danh_gia/moc_gia.py', 'if 1 - r_t <= NGUONG:',
     'if 1 - r_t < NGUONG:', 'Mốc giả: biên không phân xử được (N40)'),
    ('D92-CK-hoa-MRR-thap', 'src/m1_danh_gia/chon_khoi.py', 'thang = min(gan, key=lambda c: (len(tap(c)), -MRR[c],',
     'thang = min(gan, key=lambda c: (len(tap(c)), MRR[c],', 'Chọn khối: hòa số thành phần chọn MRR thấp (N42)'),
    ('D93-CK-thu-tu-ten', 'src/m1_danh_gia/chon_khoi.py', 'thang = min(gan, key=lambda c: (len(tap(c)), -MRR[c], _khoa_thu_tu(tap(c), thanh_phan, thu_tu)))',
     'thang = min(gan, key=lambda c: (len(tap(c)), -MRR[c], sorted(tap(c))))', 'Chọn khối: thứ tự theo tên (N43)'),
    ('D94-CK-luot2-bo-co-dinh', 'src/m1_danh_gia/chon_khoi.py', '            if c2 in co_dinh:\n',
     '            if True:\n', 'Bước 5: không cần c thêm x thuộc tập cố định (N44)'),
    ('D95-B8-tat-KTD-xung-dot', 'src/m1_danh_gia/chon_khoi.py', "out['nhat_quan' if v in ('HAI', 'KHONG_TAC_DUNG') else 'xung_dot'].append(x)",
     "out['nhat_quan' if v in ('HAI',) else 'xung_dot'].append(x)", 'Bước 8: tắt với KHÔNG TÁC DỤNG là xung đột (N47)'),
    ('D96-CK-trai-chieu-gan-a', 'src/m1_danh_gia/chon_khoi.py', "gan_co = {k.split('|')[1] for k in co_trai_chieu}",
     "gan_co = {k.split('|')[0] for k in co_trai_chieu}", 'Chọn khối: cờ TRÁI CHIỀU gắn cho a (N48)'),
    ('D97-CK-bo-R0-HAI', 'src/m1_danh_gia/chon_khoi.py', "if c != 'R0' and _la_hai(cap_cua('R0', c) or ''):",
     'if False:', 'Lượt một: bỏ loại vì (R0, c) HẠI (N49)'),
    ('D98-buoc5-moi-thanh-phan', 'src/m1_danh_gia/chon_khoi.py', '        for x in it_ca:\n',
     '        for x in thanh_phan:\n', 'Bước 5: áp cho mọi thành phần (K03)'),
    ('D99-pha2-bo-kiem-trung', 'src/m1_danh_gia/pha2.py', '    if len(set(cap)) != len(cap):\n',
     '    if False:\n', 'Pha 2: không kiểm bản ghi trùng (N51)'),
    ('D100-pha2-bo-so-ca', 'src/m1_danh_gia/pha2.py', "    if 'so_ca' in meta and meta['so_ca'] != len(ca):\n",
     '    if False:\n', 'Pha 2: không kiểm số ca với metadata (N52)'),
    ('D101-cache-bo-huong', 'src/m1/e4.py', 'tuple(sorted(float(x) for x in A)), huong,',
     'tuple(sorted(float(x) for x in A)),', 'E4: khóa cache không có hướng (N14)'),
    ('D102-NEW_OP-gt', 'src/m1/e4.py', "    if n_N == 0 and n_A >= ts['count_min'] and 'len' in huong_cham:",
     "    if n_N == 0 and n_A > ts['count_min'] and 'len' in huong_cham:", 'NEW_OP: biên count_min (N12)'),
    ('D103-PII01-pv-le', 'src/m1/e4.py', '        qua = p < alpha\n',
     '        qua = p <= alpha\n', 'PII-01 đơn vị phân vị: p ≤ α (N07)'),
    ('D104-PII01-dem-le', 'src/m1/e4.py', 'qua = (d in huong_cham) and p < alpha and cheng > 0',
     'qua = (d in huong_cham) and p <= alpha and cheng > 0', 'PII-01 đơn vị đếm: p ≤ α (N08)'),
    ('D105-UV6-sua-bang-0', 'src/m1_danh_gia/uv6.py', "if ma and c['hit1_tat'] < 1 and c['hit1_bat'] == 1:",
     "if ma and c['hit1_tat'] == 0 and c['hit1_bat'] == 1:", 'UV-6: ca được sửa cần Hit@1 tắt = 0 (N55)'),
    ('D106-lan-xuoi-chi-lop-giai-thich', 'src/m1/e5.py', "                    if b == e:\n                        for ch in theo_e[a]:\n                            _them(B, a, ch, [a, e], 'lan_xuoi')",
     "                    if b == e:\n                        for ch in theo_e[a]:\n                            if ch.lop in GIAI_THICH_LAN_NGUOC:\n                                _them(B, a, ch, [a, e], 'lan_xuoi')", 'E5: lan xuôi chỉ do bên gọi lớp lan ngược/không lan (N19)'),
    ('D107-E9-chi-nguoi-dau', 'src/m1/e5.py', '[ch.khoi_phat for _, ch, _, _ in B]',
     '[B[0][1].khoi_phat]', 'E9: chỉ xét bên giải thích đầu (N18)'),
    ('D108-mrr-tong-0', 'src/m1_danh_gia/rr.py', "        raise ValueError('tổng trọng số của các ca được chọn bằng 0')",
     '        return Fraction(0)', 'MRR: tổng bội số 0 trả 0 (K01)'),
    ('D109-e5-duong-set', 'src/m1/e5.py', '    ke = {v: sorted({y for x, y in canh if x == v and y in S}) for v in S}',
     '    ke = {v: list({y for x, y in canh if x == v and y in S}) for v in S}', 'E5: đường phụ thuộc hash seed (K09)'),
    ('D110-E3-sap-chi-theo-moc', 'src/m1/e3.py', "for d in sorted(dong_N, key=lambda x: (x['moc'], x['thuc_the'], x['noi_dung'])):",
     "for d in sorted(dong_N, key=lambda x: x['moc']):", 'E3: log trùng mốc theo thứ tự vào (K17)'),
    ('D111-khong-moc-gia-nhan-X', 'src/m1_danh_gia/pha2.py', "            khong_mg[w] = luat_c.ap_dung(ds, rt, rb, E_X, thanh_phan=thanh_phan, moc_gia=None, trong_so=trong_so,\n                                         delta_d_co_dinh=delta_d_co_dinh, **them)['ket_cuc']",
     "            khong_mg[w] = luat_c.ap_dung(ds, rt, rb, E_X, thanh_phan='X', moc_gia=None, trong_so=trong_so,\n                                         delta_d_co_dinh=delta_d_co_dinh)['ket_cuc']", 'khong_moc_gia bỏ điều kiện riêng E5, E3 (S34; lỗi của lượt 5)'),
    ('D112-gop-khong-dem', 'src/m1/xep_hang.py', '                dem.append(e)',
     '                pass', 'Không đếm lần gộp khóa ghi ra (S35)'),
    ('D113-chon-bo-the-gioi', 'src/m1_danh_gia/chon_khoi.py', "        cap = {k: v['theo_the_gioi'][the_gioi] for k, v in cap.items()}",
     '        pass', 'Luật chọn khối ở S_lo, S_hi vẫn đọc kết cục tại P (S36)'),
    ('D114-mrr-cau-hinh-bo-boi-so', 'src/m1_danh_gia/pha2.py', "        m = {'gop': rr.mrr(r, None, trong_so)}",
     "        m = {'gop': rr.mrr(r, None, None)}", 'MRR gộp của cấu hình bỏ bội số (S37)'),
    ('D115-lay-mau-gop-dataset', 'src/m1_danh_gia/rr.py', '        o_ds = sorted(o for o, x in ds_cua_o.items() if x == d)',
     '        o_ds = sorted(ds_cua_o)', 'Lấy mẫu ô gộp hai dataset (S37)'),
    ('D116-lay-mau-khong-sap', 'src/m1_danh_gia/rr.py', '        o_ds = sorted(o for o, x in ds_cua_o.items() if x == d)',
     '        o_ds = [o for o, x in ds_cua_o.items() if x == d]', 'Lấy mẫu ô theo thứ tự đầu vào (S37)'),
    ('D117-cache-khong-theo-ca', 'src/m1/runner.py', '        chuoi.CACHE = e4.CacheCong()\n',
     '', 'Pha 1 không làm mới cache theo ca (S38)'),
    ('D118-bo-kiem-gia-tri-E4', 'src/m1/chuoi.py', "            not (0 < t4['alpha'] < 1 and 0 <= t4['epsilon'] < 1 and 0 < t4['q_lo'] < t4['q_hi'] < 1):",
     '            False:', 'Chuỗi: không kiểm khoảng giá trị tham_so_E4 (S39)'),
    ('D119-bo-do-ca', 'src/m1_danh_gia/pha2.py', "                         'do': danh_gia.do_ca(rr.phan_bo(b, root), ok)}",
     "                         'do': {}}", 'Pha 2 không lưu đủ độ đo (S42)'),
    ('D120-moc-gia-giu-ERROR', 'src/m1_danh_gia/pha2.py', "if 'INSUFFICIENT_EVIDENCE' not in (a, b) and None not in (a, b)]",
     "if 'INSUFFICIENT_EVIDENCE' not in (a, b)]", 'Mốc giả giữ cặp có bản ghi lỗi trong mẫu số (X02; PII-13)'),
    ('D121-T4c-mKI-bo-FI', 'src/m1/chuoi.py', 'max(b, m) if F_I_P.get(k.ma, 1) == 1 else b)',
     'max(b, m))', 'T4c: phần K_I của m không theo F_I (X04)'),
    ('D122-M5-luon-dung-P', 'src/m1_danh_gia/pha2.py', "'M5': ok and m5.co_M5(b, root, G_N),",
     "'M5': ok and m5.co_M5(_blocks(rec, 'P'), root, G_N),", 'M5 ở S_lo, S_hi dùng khối của P (X05)'),
    ('D123-E2VC-canh-yeu', 'src/m1/chuoi.py', 'best = max(phu, key=lambda x: (diem[x], x))',
     'best = min(phu, key=lambda x: (diem[x], x))', 'E2-VC lấy cạnh điểm thấp nhất (X08)'),
    ('D124-WD-theo-ky-vong', 'src/m1_danh_gia/the_gioi.py', 'vals = {w: tuple(sorted(d.items())) for w, d in pb.items()}',
     'vals = {w: rr.hang_ky_vong(blocks_theo_the_gioi[w], root) for w in pb}', 'WORLD_DEPENDENT theo hạng kỳ vọng (X10)'),
    ('D125-dich-Cd3-phia-N', 'src/m1/chuoi.py', "for s in prep['spans'].values() if s['phia'] == 'A']",
     "for s in prep['spans'].values() if s['phia'] == 'N']", 'Đích C-d3 lấy span phía N (X13)'),
    ('D126-G_N-cha-o-A', 'src/m1/chuoi.py', "if s['cha'] is not None and s['phia'] == 'N' and sp[s['cha']]['phia'] == 'N'",
     "if s['cha'] is not None and s['phia'] == 'N'", 'G_N nhận cạnh có span cha thuộc A (X14)'),
    ('D127-o_s-5s', 'src/m1/chuoi.py', 'o_s_ns = 10 * NS',
     'o_s_ns = 5 * NS', 'Ô E9 5 giây (X16)'),
    ('D128-e9-canh-E2-mot-chieu', 'src/m1/e5.py', 'dung_canh_E2 = any((p[i], p[i + 1]) in canh_E2 or (p[i + 1], p[i]) in canh_E2',
     'dung_canh_E2 = any((p[i], p[i + 1]) in canh_E2', 'E9: cạnh E2 chỉ xét một chiều (X26)'),
]
XAO = {'D19-bo-sap-kenh-E5': '1'}
# chỉ bị bắt bởi phép quét tĩnh (test_tinh.py), không đổi hành vi; không tính vào số đột biến hành vi (C7)
KIEM_TINH = ('D07-m1-import-bo-danh-gia', 'D08-doc-duong-dan-nhan')


def chay(goc, ra, ma, xao):
    env = dict(os.environ, PYTHONHASHSEED='0', PYTHONIOENCODING='utf-8', M1_KET_QUA=str(ra / f'{ma}.json'))
    env.pop('M1_XAO', None)
    if xao:
        env['M1_XAO'] = xao
    t0 = time.perf_counter()
    p = subprocess.run([PY, '-B', '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '-W', 'ignore'],
                       cwd=goc / 'results' / 'T-044' / 'tests', env=env, capture_output=True, text=True, timeout=900,
                       encoding='utf-8', errors='replace')  # Windows: không dùng cp1252 mặc định
    (ra / f'{ma}.txt').write_text(p.stdout + p.stderr, encoding='utf-8')
    kq = json.loads((ra / f'{ma}.json').read_text(encoding='utf-8'))
    truot = sorted(r['test'] for r in kq if r['ket_qua'] != 'passed')
    return {'so_phep': len(kq), 'so_truot': len(truot), 'truot': truot, 'exit': p.returncode,
            'giay': round(time.perf_counter() - t0, 2), 'M1_XAO': xao}


def main():
    ra = Path(sys.argv[1]).resolve()
    ra.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        goc = Path(td)
        (goc / 'results').mkdir()
        shutil.copytree(ROOT / 'results' / 'T-043', goc / 'results' / 'T-043',
                        ignore=shutil.ignore_patterns('runs'))
        for d in ('tests', 'fixture'):
            shutil.copytree(ROOT / 'results' / 'T-044' / d, goc / 'results' / 'T-044' / d)
        out = {}
        for ma, tep, cu, moi, mo_ta in [('D00-doi-chung', None, None, None, 'không đột biến')] + DOT_BIEN:
            if (goc / 'src').exists():
                shutil.rmtree(goc / 'src')
            shutil.copytree(ROOT / 'src', goc / 'src', ignore=shutil.ignore_patterns('__pycache__'))
            if tep:
                p = goc / tep
                s = p.read_text(encoding='utf-8')
                if s.count(cu) != 1:
                    raise SystemExit(f'{ma}: chuỗi cũ xuất hiện {s.count(cu)} lần trong {tep}')
                p.write_text(s.replace(cu, moi), encoding='utf-8')
            r = chay(goc, ra, ma, XAO.get(ma))
            r.update({'tep': tep, 'cu': cu, 'moi': moi, 'mo_ta': mo_ta,
                      'bi_bat': (r['so_truot'] > 0) if tep else None})
            out[ma] = r
            print(ma, r['so_truot'], 'trượt /', r['so_phep'], flush=True)
    dc = out['D00-doi-chung']
    tong = {'buoc': 'SPEC T-044 bước 7, tiêu chí 6', 'lenh': 'python -B results/T-044/scripts/dot_bien.py <thư mục>',
            'doi_chung_xanh': dc['so_truot'] == 0, 'so_dot_bien': len(DOT_BIEN),
            'so_bi_bat': sum(1 for k, v in out.items() if v['bi_bat']),
            'kiem_tinh': list(KIEM_TINH), 'so_dot_bien_hanh_vi': len(DOT_BIEN) - len(KIEM_TINH),
            'so_bi_bat_hanh_vi': sum(1 for k, v in out.items() if v['bi_bat'] and k not in KIEM_TINH),
            'so_bi_bat_dung_mot_phep': sum(1 for k, v in out.items() if v['bi_bat'] and v['so_truot'] == 1),
            'song_sot': sorted(k for k, v in out.items() if v['bi_bat'] is False), 'chi_tiet': out}
    (ra / 'tong-hop.json').write_text(json.dumps(tong, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print('đối chứng xanh:', tong['doi_chung_xanh'], '| bị bắt:', tong['so_bi_bat'], '/', tong['so_dot_bien'],
          '| sống sót:', tong['song_sot'])


if __name__ == '__main__':
    main()
