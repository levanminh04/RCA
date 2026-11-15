"""T-062 G1: sinh chỉ mục cho trang phát lại (có đáp án) của dashboard G2.

Đọc mọi file `<mã>.phat-lai.json` (định dạng 0.2 + khối `phat_lai`, do results/T-061/phat-lai.py sinh)
trong thư mục được truyền vào; ghi `<thư mục>/chi-muc/danh-sach-phat-lai.json`.
Chỉ dùng cho thư mục phát lại. Trang chính (không đáp án) đọc `chi-muc/danh-sach-su-co.json` của T-061 (`chi-muc.py`).

Mỗi dòng: thông tin của chỉ mục T-061 + đáp án + vai trò/hạng M1 của các thành phần trong tập chấp nhận.
Đáp án T-062 (results/T-062/e2.py) là root khai trước (với lỗi trên tuyến: cạnh có hướng, T-059) và tập chấp nhận
mức nút; `thanh_phan_tiem` chỉ là phần tử đầu của tập. File T-061 không có các khóa mới: lùi về [thanh_phan_tiem].
Trường cũ dap_an_thanh_phan / m1_vai_tro_cua_dap_an / m1_hang_cua_dap_an giữ nguyên nghĩa (chỉ phần tử đầu) trong giai
đoạn chuyển; dashboard mới đọc trường mới (phản biện G1 lượt 1–3, F1′).
Đây là hiển thị, không phải chấm điểm: chấm vẫn bằng script trên file đã băm.

Cách dùng: py -3 -B chi-muc-phat-lai.py <thư mục chứa *.phat-lai.json>
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
VAI_TRO = {'nghi_nguon': 'nghi là nguồn', 'bi_keo_theo': 'bị kéo theo',
           'binh_thuong': 'bình thường', 'thieu_du_lieu': 'thiếu dữ liệu'}


def mo_ta_trong_tap(ten, nut):
    """Vai trò/hạng M1 của một thành phần trong tập chấp nhận. Không bao giờ in #None."""
    n = nut.get(ten)
    if n is None:
        return f'{ten}: M1 không quan sát'
    vt, h = n.get('vai_tro'), n.get('hang')
    if vt in ('nghi_nguon', 'bi_keo_theo') and h is not None:
        return f'{ten}: #{h} {VAI_TRO[vt]}'
    if vt == 'binh_thuong':
        if h is None:
            return f'{ten}: bình thường'
        nhom = n.get('so_dong_hang')
        return f'{ten}: bình thường (M1 xếp hạng #{h}' + (f', nhóm {nhom} thành phần)' if nhom else ')')
    if vt == 'thieu_du_lieu':
        return f'{ten}: thiếu dữ liệu, không có hạng'
    return f'{ten}: {VAI_TRO.get(vt, vt)}' + (f' #{h}' if h is not None else '')


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) != 2:
        raise SystemExit('Cách dùng: chi-muc-phat-lai.py <thư mục phát lại>')
    thu_muc = Path(sys.argv[1])
    dong = []
    for f in sorted(thu_muc.glob('*.phat-lai.json')):
        b = f.read_bytes()
        kq = json.loads(b.decode('utf-8'))
        sc, pl = kq['su_co'], kq.get('phat_lai')
        if pl is None:
            raise SystemExit(f'{f.name}: không có khối phat_lai')
        if f.name != sc['ma'] + '.phat-lai.json':
            raise SystemExit(f'{f.name}: tên file không khớp mã ca {sc["ma"]}')
        dap = pl.get('thanh_phan_tiem')
        nut = next((n for n in kq['nut'] if n['id'] == dap), None) if dap else None
        nut_id = {n['id']: n for n in kq['nut']}
        # Phân biệt khóa không tồn tại (file T-061) với tập rỗng/null hợp lệ (ca không tiêm).
        tap = (pl['tap_chap_nhan'] or []) if 'tap_chap_nhan' in pl else ([dap] if dap else [])
        root = pl['root_khai_truoc'] if 'root_khai_truoc' in pl else dap
        dong.append({
            'ma': sc['ma'], 't_ms': sc['moc']['t_ns'] // 10**6, 't_utc': sc['moc']['t_utc'],
            'trang_thai': sc['trang_thai'], 'ket_luan': sc['ket_luan'], 'ket_luan_hien_thi': sc['ket_luan_hien_thi'],
            'nghi_nguon_hang_1': ', '.join(n['id'] for n in kq['nut'] if n['noi_bat']) or '—',
            'so_thuc_the_quan_sat': kq['do_phu']['so_quan_sat'], 'so_thuc_the_co_hang': kq['do_phu']['so_tra_hang'],
            'dap_an_thanh_phan': dap or '—',
            'dap_an_ho_loi': pl.get('ho_loi') or '—',
            'dap_an_co_tiem': bool(dap),
            'm1_vai_tro_cua_dap_an': (VAI_TRO.get(nut['vai_tro'], nut['vai_tro']) if nut
                                      else ('M1 không quan sát thành phần này' if dap else '—')),
            'm1_hang_cua_dap_an': (nut['hang'] if nut and nut['vai_tro'] in ('nghi_nguon', 'bi_keo_theo') else None),
            'dap_an_root': root or '—',
            'dap_an_tap': tap,
            'm1_trong_tap': '; '.join(mo_ta_trong_tap(a, nut_id) for a in tap) or '—',
            'hang_tot_nhat_e2': pl.get('hang_tot_nhat') if 'hang_tot_nhat' in pl else None,
            'hang_tot_nhat_e2_hien_thi': ('— (không có tập chấp nhận)' if not tap else
                                          '— (file không có trường hang_tot_nhat)' if 'hang_tot_nhat' not in pl else
                                          'không có hạng' if pl['hang_tot_nhat'] is None else f"#{pl['hang_tot_nhat']}"),
            'nhan_xet': pl.get('nhan_xet'),
            'file': f.name, 'sha256_file': hashlib.sha256(b).hexdigest(),
        })
    dong.sort(key=lambda x: x['t_ms'], reverse=True)
    ra = thu_muc / 'chi-muc' / 'danh-sach-phat-lai.json'
    ra.parent.mkdir(exist_ok=True)
    ra.write_text(json.dumps({'dinh_dang': 'flashticket-rca-danh-sach-phat-lai', 'phien_ban': '0.2', 'su_co': dong},
                             ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{ra}: {len(dong)} sự cố')


if __name__ == '__main__':
    sys.exit(main())
