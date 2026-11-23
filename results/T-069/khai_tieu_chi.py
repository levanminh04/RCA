# -*- coding: utf-8 -*-
"""T-069 bước 3 — dựng results/T-069/tieu-chi.json (khai trước khi thu). Chỉ đọc đầu vào; không sửa bộ chấm, đáp án.
Dùng: D:/RCA-flashticket/.venv/Scripts/python.exe -B results/T-069/khai_tieu_chi.py
Hạng cũ từng ô tính bằng chính bộ chấm T-064 (cham_dev3.tim + src/m1_ft/cham.cham_ca_loi/cham_ca_khong_loi), cùng
goc_uu_tien của spec R9 → khớp results/T-064/cham/chon-dev3-d0-v082-r9-A.json (kiểm ở cuối)."""
import datetime as dt, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
R = Path('D:/RCA-flashticket'); T = R / 'results/T-064'; RA = R / 'results/T-069/tieu-chi.json'
LAB = Path('D:/Project/flashticket-rca-lab')
spec_ = importlib.util.spec_from_file_location('cham_dev3_t064', T / 'cham/cham_dev3.py')
C = importlib.util.module_from_spec(spec_); spec_.loader.exec_module(C)
cham = C.cham
SPEC_R9 = json.loads((T / 'cham/spec-dev3-d0-v082-r9.json').read_text(encoding='utf-8'))
C.UU[:] = SPEC_R9.get('goc_uu_tien', [])
BAN = {'V082': 'V082-V066+H8a', 'P7': 'P7'}


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def git_sha(path):
    return subprocess.run(['git', '-C', str(LAB), 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()


tap = C.tap_tu_file('results/T-064/tap-chon-dev3-17.json')
cu_tong = json.loads((T / 'cham/chon-dev3-d0-v082-r9-A.json').read_text(encoding='utf-8'))
nhom2 = {c['ma'] for c in json.loads((T / 'tap-chon-dev2-13.json').read_text(encoding='utf-8'))['ca']}
lich_thu = json.loads((LAB / 'campaigns/schedules/lich-t069-thu.json').read_text(encoding='utf-8'))['chu_ky']
lich_chinh = json.loads((LAB / 'campaigns/schedules/lich-t069.json').read_text(encoding='utf-8'))['chu_ky']
vi_tri_moi = [('lich-t069-thu', i, x) for i, x in enumerate(lich_thu)] + [('lich-t069', i, x) for i, x in enumerate(lich_chinh)]
INJ = {}
src = (LAB / 'faults/injectors/docker/inj3.py').read_text(encoding='utf-8')
ns = {}
exec(src.split('def now()')[0].replace("STATE.mkdir(parents=True, exist_ok=True)", ''), ns)  # chỉ đọc bảng CELLS
CELLS = ns['CELLS']

cap = []; dem_bt = 0
for c in tap:
    o = c['o']
    # ghép theo ô; BINH-THUONG ghép theo thứ tự xuất hiện (tập cũ theo thứ tự lich-2, lịch mới cùng thứ tự)
    cung_o = [v for v in vi_tri_moi if v[2]['o'] == o]
    if o == 'BINH-THUONG':
        vt = cung_o[dem_bt]; dem_bt += 1
    else:
        assert len(cung_o) == 1, o; vt = cung_o[0]
    cu = {}
    for k, b in BAN.items():
        rec, sh, nguon = C.tim(b, c['ma'], 0)
        if c['loai'] == 'loi':
            r = cham.cham_ca_loi(cham.chieu_canh_ve_nut(rec), c['tap_chap_nhan'])
            cu[k] = {'status': rec.get('status'), 'hang_cat': r['hang_cat'], 'hang_ky_vong': r['hang_ky_vong'],
                     'p1': r['p1'], 'p3': r['p3'], 'sha256': sh, 'nguon': nguon}
        else:
            r = cham.cham_ca_khong_loi(rec)
            cu[k] = {'status': rec.get('status'), 'k': r['k'], 'verdict': rec.get('verdict'), 'sha256': sh, 'nguon': nguon}
        # đối chiếu với file chấm đã lưu
        luu = cu_tong['ban'][b]['chon']['ca'][c['ma']]
        for f in ('p1', 'p3', 'hang_ky_vong', 'k'):
            if f in cu[k] and luu.get(f) != cu[k][f]: raise SystemExit(f'lệch file chấm cũ: {b} {c["ma"]} {f}')
        if luu['sha256'] != sh: raise SystemExit(f'lệch sha đầu ra cũ: {b} {c["ma"]}')
    g2 = c['ma'] in nhom2
    cap.append({
        'o': o, 'loai': c['loai'], 'tap_chap_nhan': c.get('tap_chap_nhan'),
        'cu': {'ma': c['ma'], 'nhom_thu': 'thu2 (lich-2)' if g2 else 'thu bù 3 (lich-3)',
               'image': 'arm64-t062-6b21ed55 cả 7 service' if g2 else 'arm64-t062-6b21ed55; Event arm64-t063h3-76b34d5e',
               'dong_bang': 'results/T-063/dong-bang/dong-bang-2.json' if g2 else 'results/T-063/dong-bang/dong-bang-3.json',
               'xac_nhan': 'results/T-063/chay/xac-nhan-ca-2.json' if g2 else 'results/T-063/thu3/xac-nhan-ca-3-sua-sau.json',
               **cu},
        'moi': {'lich': vt[0], 'chu_ky': vt[1], 'multiplier': vt[2].get('multiplier', 1),
                'flash_x3_tai_moc_t': o in ('FLASH-HEALTHY', 'HTTP5-EVENT-FLASH'),
                'image': 'arm64-t067-36a3725d cả 7 service (results/T-067/trien-khai/chuoi-container.json)',
                'can_thiep_inj3': CELLS[o]},
        'cua_so': 'tải 1800 s; t = mốc tải + 600 (sổ load-start); lỗi [t, t+600]; M1 như runner4 (stage tại t+750); chế độ (a) t từ sổ',
    })

tieu_chi = {
    'task': 'T-069 (W3) — V082 không hồi quy trên bản ghim 36a3725',
    'ghi_utc': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
    'trang_thai': 'khai trước: chưa thu ca nào của T-069',
    'nguon_sha256': {p: sha(R / p) for p in [
        'tasks/T-069-v082-ban-ghim/SPEC.md', 'results/T-064/tap-chon-dev3-17.json', 'results/T-064/dap-an-dev3.json',
        'results/T-064/cham/cham_dev3.py', 'src/m1_ft/cham.py', 'results/T-064/cham/spec-dev3-d0-v082-r9.json',
        'results/T-064/cham/chon-dev3-d0-v082-r9-A.json', 'results/T-064/manifest-3.json',
        'results/T-063/chay/dieu-kien-xac-nhan.md', 'results/T-063/chay/xac_nhan_ca.py',
        'results/T-063/thu3/dieu-kien-xac-nhan-3.md', 'results/T-063/thu3/scripts/xac_nhan_ca_3.py']},
    'repo_lab': {'commit': git_sha(LAB), 'inj3_sha256': sha(LAB / 'faults/injectors/docker/inj3.py'),
                 'lich_t069_thu_sha256': sha(LAB / 'campaigns/schedules/lich-t069-thu.json'),
                 'lich_t069_sha256': sha(LAB / 'campaigns/schedules/lich-t069.json'),
                 'runner4_sha256': sha(LAB / 'campaigns/runner/runner4.py')},
    'phia_cu_tong': {k: {'AC@1': cu_tong['ban'][b]['chon']['tong']['AC@1'], 'AC@3': cu_tong['ban'][b]['chon']['tong']['AC@3'],
                         'tong_hang_cat': cu_tong['ban'][b]['chon']['tong']['tong_hang_cat'], 'K': cu_tong['ban'][b]['chon']['K'],
                         'loi_chay': cu_tong['ban'][b]['chon']['loi_chay']} for k, b in BAN.items()},
    'cap_ca': cap,
    'dinh_nghia': {
        'hang': 'hang_cat của src/m1_ft/cham.py::cham_ca_loi trên đầu ra method-output-1.json (bộ chấm T-064 không sửa): hạng kỳ '
                'vọng của nút đáp án trong nhóm đồng hạng, cắt ở 6; vắng, lỗi chạy, thiếu đầu ra = 6. Đáp án A (dap-an-dev3.json).',
        'tut': 'ô lỗi ghép được có hang_cat(V082 mới) > hang_cat(V082 cũ) + 1',
        'doi_hang': 'hang_cat mới khác hang_cat cũ (V082 hoặc P7)',
        'k': 'ô không lỗi: k = 1 khi verdict CAUSE_FOUND (cham_ca_khong_loi)',
        'ghep_duoc': [
            'ca mới đạt đúng điều kiện xác nhận can thiệp mà ca cũ cùng ô đã đạt: ô lich-2 theo results/T-063/chay/dieu-kien-xac-nhan.md '
            '(kèm "Sửa sau 1" Minh đã nhận), script results/T-063/chay/xac_nhan_ca.py --sua-sau-1; ô lich-3 theo '
            'results/T-063/thu3/dieu-kien-xac-nhan-3.md (kèm "Sửa sau 1", "Sửa sau 2"), script xac_nhan_ca_3.py --sua-sau-1 --sua-sau-2. '
            'Script chép nhị phân sang results/T-069/xac-nhan/, chạy trên thư mục dựng từ sổ tiêm của lượt, đầu ra tải, audit Event đầy đủ.',
            'khong_du_du_lieu (thiếu đầu dò, Prometheus mất mẫu, thiếu audit) hoặc không xác nhận → ô không ghép được, ghi lý do, không chấm.',
            'mỗi ca có đầu ra P7 (hoặc lỗi chạy P7 ghi rõ) và V082; V082 phải trung_sha = true, P7 deterministic_repeat = true.'],
        'so_tong': 'AC@1, AC@3, tổng hạng cắt, K tính bằng cham_dev3.py trên tập ca mới (spec results/T-069/cham/spec-moi.json, '
                   'goc_uu_tien → results/T-069/dau-ra/); số cũ của D1–D5 tính lại trên đúng tập ô ghép được.',
    },
    'dieu_kien_dung': {
        'D1': 'AC@3(V082 mới) < AC@3(V082 cũ) trên tập ô lỗi ghép được',
        'D2': 'AC@1(V082 cũ) − AC@1(V082 mới) ≥ 2',
        'D3': 'V082 mới kém P7 mới ở AC@1, hoặc AC@3, hoặc tổng hạng cắt (lớn hơn là kém) trên cùng tập',
        'D4': 'V082 lỗi chạy (status ≠ OK hoặc không ra đầu ra) mà không do hạ tầng (gói ca, đĩa, mạng, Prometheus)',
        'D5': 'K(V082 mới) − K(V082 cũ) ≥ 2 trên tập ô không lỗi ghép được',
        'nghia': 'dừng kết luận, không chuyển W4/W5; không ngắt lượt thu; làm bước 7 trên dữ liệu đã lưu rồi trình Minh',
    },
    'nhom_giai_thich': {
        'a': 'ô V082 đổi hạng xấu đi và P7 cũng xấu đi cùng ô (hệ thống đổi làm mọi phương pháp khó hơn)',
        'b': 'chỉ V082 xấu đi (P7 giữ hoặc tốt lên) → nghi thành phần riêng H5b/H8s1/H8a; xét ở bước 7',
        'c': 'lần thu lặp cho hạng V082 trở về trong [hạng cũ − 1, hạng cũ + 1] → nghiêng nhiễu một lần thu',
        'ghi_chu': 'nhóm là nghiêng về, không là kết luận cơ chế; cơ chế theo bước 7 (luật 15)',
    },
    'quy_tac_lap': {
        'dieu_kien': 'ô lỗi ghép được có hang_cat của V082 hoặc P7 khác phía cũ',
        'toi_da': 4,
        'uu_tien': ['1. ô V082 tụt (theo hang_cat mới − cũ giảm dần)', '2. ô V082 đổi hạng khác (|Δ| giảm dần)',
                    '3. ô chỉ P7 đổi hạng (|Δ| giảm dần)',
                    '4. nếu còn chỗ và D5 xảy ra: ô không lỗi có k V082 đổi 0 → 1', 'đồng hạng: theo thứ tự trong lịch'],
        'lich': 'lượt ngắn riêng campaigns/schedules/lich-t069-lap.json, sau khi chấm lượt chính; cùng hệ số tải và can thiệp',
        'bao_cao': 'báo cả hai lần thu; D1–D5 tính trên lần thu chính; lần lặp chỉ dùng để xếp nhóm (c); không chọn lần đẹp hơn',
    },
    'xu_ly_rieng': {
        'RECREATE-PAY_P7_loi': 'nếu run_m1 (P7) lỗi adapter như ca cũ ebd5ef38 thì runner không chạy gói bổ sung/V082 cho ca đó; '
                               'khi đó sau chu kỳ chạy đúng các lệnh của runner4 (xuat_bo_sung.py --t <t>, cài vào m1/bo-sung/<mã>/, '
                               'lệnh chay_v082, sau_v082.py) trên gói stage đầu tiên (mã gốc). P7 ghi loi-chay.json phía chấm (hạng 6).',
        'stage_lai': 'nếu runner stage lại mã mới (lần 2) thì dùng mã đã cho đầu ra; ghi cả hai mã.',
        'tai_moi_lan': 'ca thử (lich-t069-thu) tính là ca chính thức nếu sau đó không sửa code',
    },
}
RA.parent.mkdir(parents=True, exist_ok=True)
RA.write_bytes((json.dumps(tieu_chi, ensure_ascii=False, indent=1) + '\n').encode('utf-8'))
for x in cap:
    print(x['o'], x['cu']['ma'], {k: x['cu'][k].get('hang_cat', x['cu'][k].get('k')) for k in BAN}, x['moi']['lich'], x['moi']['chu_ky'])
print('sha256', sha(RA))
