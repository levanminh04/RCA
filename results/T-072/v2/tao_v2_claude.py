# Tạo results/T-072/v2/cham_offline_v2_claude.py từ cham_offline_v2.py (Codex) — không sửa file Codex.
import pathlib
V2 = pathlib.Path(r'D:\RCA-flashticket\results\T-072\v2')
s = (V2 / 'cham_offline_v2.py').read_bytes().decode('utf-8')


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:80], s.count(a))
    s = s.replace(a, b)


rep('"""T-072 — bộ chấm offline', '"""T-072 — bộ chấm offline. Bản v2_claude = v2 của Codex (CX-24) + phần quy_ve / Pending / ca đầu khoảng của\nClaude T-072 (đáp CX-19 F5). File v2 của Codex giữ nguyên.\n\nT-072 — bộ chấm offline')

rep("""                # PHAN CUA CLAUDE T-072: chưa sửa
                if ok:""", """                # Pending (Claude T-072, v2_claude): giữ nguyên. tp = bước đúng đầu tiên của dãy đúng liên tiếp; Alerting khi
                # t - tp >= for_s. Khớp Grafana (Normal->Pending ở lần đánh giá đúng đầu tiên) trên 4 luật thử E3 (lệch -4 s, pha).
                # Dãy đúng ngay từ bước đầu lưới: lịch sử trước lưới không thấy -> quy_ve gắn cờ 'pending-tu-dau-luoi'.
                if ok:""")

rep("""# PHAN CUA CLAUDE T-072: chưa sửa
def quy_ve(sus, phut, t_dau):
    for s in sus:
        m = s['t_hat'] // 60 * 60
        s['lop'] = phut.lop(m)
        s['co'] = []
        if any(c.get('tp') == t_dau for c in s['canh_bao']):
            s['lop'] = 'dang-chay-luc-bat-dau'
""", '''def quy_ve(sus, phut, t_dau, bat_dau=None):
    """Quy sự cố về phút theo quy-tac-gom.json#/quy_ve_phut (Claude T-072, v2_claude; sửa CX-19 F5).

    - Lớp = lớp của phút chứa t̂ sự cố (t̂ = lúc vào Alerting), như cũ.
    - bat_dau = đầu khoảng chấm (giờ hiệu lực hoặc mốc khai trước), epoch giây. Sự cố có t̂ < bat_dau: còn cháy tại
      bat_dau (t_het None hoặc t_het > bat_dau; khoảng nửa mở) -> 'dang-chay-luc-bat-dau'; đã hết -> 'truoc-khoang'.
      Cả hai không vào tử số. bat_dau = None -> không xét. (Bản cũ so tp với bước đầu lưới xuất: sai nghĩa quy tắc, bỏ.)
    - Cờ 'pending-truoc-khoang': có cảnh báo vào Pending trước bat_dau nhưng Alerting từ bat_dau trở đi (vẫn đếm theo t̂).
    - Cờ 'pending-tu-dau-luoi': dãy đúng bắt đầu ngay bước đầu lưới t_dau; offline không thấy lịch sử trước lưới nên
      t̂ offline có thể muộn hơn Grafana; phải đối chiếu lịch sử trạng thái Grafana.
    """
    for s in sus:
        m = s['t_hat'] // 60 * 60
        s['lop'] = phut.lop(m)
        s['co'] = []
        if bat_dau is not None and s['t_hat'] < bat_dau:
            s['lop'] = 'dang-chay-luc-bat-dau' if (s['t_het'] is None or s['t_het'] > bat_dau) else 'truoc-khoang'
        elif bat_dau is not None and any(c.get('tp') is not None and c['tp'] < bat_dau for c in s['canh_bao']):
            s['co'].append('pending-truoc-khoang')
        if any(c.get('tp') == t_dau for c in s['canh_bao']):
            s['co'].append('pending-tu-dau-luoi')
''')

rep("""        if lops - {s['lop']}:""", """        if lops - {phut.lop(m)}:  # so với lớp của phút (không với lớp đầu khoảng), v2_claude""")

rep("""def cham(bt, du, ng, phut):
    kcs = danh_gia(bt, du, ng)
    luoi = sorted(du.luoi)
    sus = quy_ve(gom(kcs), phut, luoi[0] if luoi else 0)""", """def cham(bt, du, ng, phut, bat_dau=None):
    kcs = danh_gia(bt, du, ng)
    luoi = sorted(du.luoi)
    sus = quy_ve(gom(kcs), phut, luoi[0] if luoi else 0, bat_dau)""")
rep("    pk = phut.so_phut(KHOE, luoi)",
    "    pk = phut.so_phut(KHOE, [t for t in luoi if bat_dau is None or t // 60 * 60 >= bat_dau])  # chỉ phút trọn từ bat_dau")

rep("""    def ca(ten, chens, ky_vong, phut=None, bo=None):
        d = du_nen()
        for c in chens:
            chen(d, c)
        if bo:
            bo(d)
        kq = cham(bt, d, ng, Phut(phut))
        got = [(s['loai'], s['lop'], s['t_hat'] - T0) for s in kq['su_co']]
        if got != ky_vong:
            sai.append({'ca': ten, 'ky_vong': ky_vong, 'duoc': got})
        return kq""", """    def ca(ten, chens, ky_vong, phut=None, bo=None, bat_dau=None, co=None, so_khoang=None):
        d = du_nen()
        for c in chens:
            chen(d, c)
        if bo:
            bo(d)
        kq = cham(bt, d, ng, Phut(phut), None if bat_dau is None else T0 + bat_dau)
        got = [(s['loai'], s['lop'], s['t_hat'] - T0) for s in kq['su_co']]
        if got != ky_vong:
            sai.append({'ca': ten, 'ky_vong': ky_vong, 'duoc': got})
        if co is not None and [sorted(s['co']) for s in kq['su_co']] != co:
            sai.append({'ca': ten + '/co', 'ky_vong': co, 'duoc': [sorted(s['co']) for s in kq['su_co']]})
        if so_khoang is not None and len(kq['khoang_chay']) != so_khoang:
            sai.append({'ca': ten + '/so-khoang', 'ky_vong': so_khoang, 'duoc': len(kq['khoang_chay'])})
        return kq""")

rep("""    # PHAN CUA CLAUDE T-072: chưa sửa
    ca('dang-chay-luc-bat-dau', [f'{P}|booking|{T0}|120|0.5'], [('he-thong', 'dang-chay-luc-bat-dau', 60)])""",
    """    # Ca đầu khoảng (Claude T-072, v2_claude; thay ca cũ "Pending ở t0 -> đang cháy", sai nghĩa quy tắc, CX-19 F5).
    ca('dung-tu-dau-luoi-khong-bat-dau', [f'{P}|booking|{T0}|120|0.5'], [('he-thong', 'chua-phan-loai', 60)],
       co=[['pending-tu-dau-luoi']], so_khoang=1)
    ca('pending-truoc-alerting-sau-bat-dau', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)],
       bat_dau=1030, co=[['pending-truoc-khoang']], so_khoang=1)
    ca('alerting-dung-bat-dau-van-dem', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)],
       bat_dau=1060, co=[['pending-truoc-khoang']], so_khoang=1)
    ca('pending-dung-bat-dau-khong-co', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'chua-phan-loai', 1060)],
       bat_dau=1000, co=[[]], so_khoang=1)
    ca('dang-chay-luc-bat-dau', [f'{P}|booking|{T0+1000}|300|0.5'], [('he-thong', 'dang-chay-luc-bat-dau', 1060)],
       bat_dau=1100, co=[[]], so_khoang=1)
    ca('het-truoc-bat-dau', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'truoc-khoang', 1060)], bat_dau=1200, co=[[]])
    ca('het-dung-bat-dau-nua-mo', [f'{P}|booking|{T0+1000}|120|0.5'], [('he-thong', 'truoc-khoang', 1060)],
       bat_dau=1120, co=[[]])
    kq_ms = ca('mau-so-sau-bat-dau', [], [], phut={'khoang': [[T0, T0 + 7300, KHOE]]}, bat_dau=1200)
    if kq_ms['ty_le_khoe_x1']['phut_khoe_x1'] != 101:
        sai.append({'ca': 'mau-so-sau-bat-dau', 'duoc': kq_ms['ty_le_khoe_x1']['phut_khoe_x1']})
    ca('mat-do-dung-mot-khoang', ['tin-hieu/t072-mat-do||%d|120|none' % (T0 + 4000)], [('quan-sat', 'chua-phan-loai', 4060)],
       so_khoang=1)""")

rep("    ap.add_argument('--chen', action='append', default=[])",
    "    ap.add_argument('--chen', action='append', default=[])\n"
    "    ap.add_argument('--bat-dau', help='đầu khoảng chấm: epoch giây hoặc YYYY-mm-ddTHH:MM:SSZ (v2_claude)')")
rep("""        if a.lenh == 'cham' and not a.nguong:""", """        bat_dau = None
        if a.bat_dau:
            import datetime as _dt
            bat_dau = (int(a.bat_dau) if a.bat_dau.isdigit()
                       else int(_dt.datetime.fromisoformat(a.bat_dau.replace('Z', '+00:00')).timestamp()))
        if a.lenh == 'cham' and not a.nguong:""")
rep("""            out = cham(bt, du, ng, phut)
            out.update({'nguong': ng, 'chen': a.chen, 'dau_vao_sha256': dauvao})""", """            out = cham(bt, du, ng, phut, bat_dau)
            out.update({'nguong': ng, 'chen': a.chen, 'bat_dau_khoang': bat_dau, 'dau_vao_sha256': dauvao})""")
(V2 / 'cham_offline_v2_claude.py').write_bytes(s.encode('utf-8'))
print('ok')
