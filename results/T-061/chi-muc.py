"""T-061: sinh file chỉ mục danh sách sự cố cho panel danh sách (Infinity).

Chỉ đọc các mẫu đã băm trong mau/manifest-mau.json (kiểm byte từng mẫu); không đọc bản phát lại hay nguồn đáp án.
Ghi mau/chi-muc/danh-sach-su-co.json (thư mục con: không lẫn vào manifest mẫu và kiểm đợt của lớp phát lại).
Mỗi dòng là một sự cố, mới nhất trước. Trường lấy thẳng từ JSON định dạng; `nghi_nguon_hang_1` = các nút `noi_bat`.
Cách dùng (trong results/T-061, sau bam-mau.py): py -3 -B chi-muc.py
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
GOC = Path(__file__).resolve().parent
MAU = GOC / 'mau'


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    mm = json.load(open(MAU / 'manifest-mau.json', encoding='utf-8'))['files']
    dong = []
    for ten, muc in sorted(mm.items()):
        b = (MAU / ten).read_bytes()
        if hashlib.sha256(b).hexdigest() != muc['sha256'] or len(b) != muc['bytes']:
            raise SystemExit(f'Mẫu {ten} không khớp manifest mẫu')
        kq = json.loads(b.decode('utf-8'))
        sc = kq['su_co']
        dong.append({
            'ma': sc['ma'], 't_ms': sc['moc']['t_ns'] // 10**6, 't_utc': sc['moc']['t_utc'],
            'trang_thai': sc['trang_thai'], 'ket_luan': sc['ket_luan'], 'ket_luan_hien_thi': sc['ket_luan_hien_thi'],
            'nghi_nguon_hang_1': ', '.join(n['id'] for n in kq['nut'] if n['noi_bat']) or '—',
            'so_thuc_the_quan_sat': kq['do_phu']['so_quan_sat'], 'so_thuc_the_co_hang': kq['do_phu']['so_tra_hang'],
            'file': ten, 'sha256_file': muc['sha256'],
        })
    dong.sort(key=lambda x: x['t_ms'], reverse=True)
    ra = MAU / 'chi-muc' / 'danh-sach-su-co.json'
    ra.parent.mkdir(exist_ok=True)
    ra.write_text(json.dumps({'dinh_dang': 'flashticket-rca-danh-sach', 'phien_ban': '0.2', 'su_co': dong},
                             ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{ra}: {len(dong)} sự cố')


if __name__ == '__main__':
    sys.exit(main())
