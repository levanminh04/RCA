"""T-062 G1: sinh chỉ mục danh sách sự cố cho TRANG CHÍNH (không đáp án) của dashboard G2, cho một thư mục bất kỳ.

Cùng định dạng và cùng trường với results/T-061/chi-muc.py (Minh duyệt 11/11/2026); khác ở chỗ nhận thư mục làm tham số
thay vì cố định results/T-061/mau. Đọc mọi `<mã>.json` ở đúng thư mục đó (không đệ quy); bỏ qua `*.phat-lai.json`;
dừng nếu một file có khối `phat_lai` (đáp án không được lọt vào trang chính) hoặc tên file khác mã ca.
Nếu truyền thêm manifest (JSON `{"files": {"<tên>": {"sha256": …, "bytes": …}}}` như mau/manifest-mau.json của T-061)
thì chỉ nhận file có trong manifest và kiểm byte.

Ghi `<thư mục>/chi-muc/danh-sach-su-co.json`, mới nhất trước.
Cách dùng: py -3 -B chi-muc-chinh.py <thư mục kết quả 0.2> [manifest.json]
"""
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


def main():
    sys.stdout.reconfigure(encoding='utf-8')
    if len(sys.argv) not in (2, 3):
        raise SystemExit('Cách dùng: chi-muc-chinh.py <thư mục> [manifest.json]')
    thu_muc = Path(sys.argv[1])
    mm = json.load(open(sys.argv[2], encoding='utf-8'))['files'] if len(sys.argv) == 3 else None
    ten_file = sorted(mm) if mm is not None else sorted(f.name for f in thu_muc.glob('*.json')
                                                          if not f.name.endswith('.phat-lai.json'))
    dong = []
    for ten in ten_file:
        b = (thu_muc / ten).read_bytes()
        h = hashlib.sha256(b).hexdigest()
        if mm is not None and (h != mm[ten]['sha256'] or len(b) != mm[ten]['bytes']):
            raise SystemExit(f'{ten} không khớp manifest')
        kq = json.loads(b.decode('utf-8'))
        if 'phat_lai' in kq:
            raise SystemExit(f'{ten} có khối phat_lai (đáp án): không được đưa vào trang chính')
        sc = kq['su_co']
        if ten != sc['ma'] + '.json':
            raise SystemExit(f'{ten}: tên file không khớp mã ca {sc["ma"]}')
        dong.append({
            'ma': sc['ma'], 't_ms': sc['moc']['t_ns'] // 10**6, 't_utc': sc['moc']['t_utc'],
            'trang_thai': sc['trang_thai'], 'ket_luan': sc['ket_luan'], 'ket_luan_hien_thi': sc['ket_luan_hien_thi'],
            'nghi_nguon_hang_1': ', '.join(n['id'] for n in kq['nut'] if n['noi_bat']) or '—',
            'so_thuc_the_quan_sat': kq['do_phu']['so_quan_sat'], 'so_thuc_the_co_hang': kq['do_phu']['so_tra_hang'],
            'file': ten, 'sha256_file': h,
        })
    dong.sort(key=lambda x: x['t_ms'], reverse=True)
    ra = thu_muc / 'chi-muc' / 'danh-sach-su-co.json'
    ra.parent.mkdir(exist_ok=True)
    ra.write_text(json.dumps({'dinh_dang': 'flashticket-rca-danh-sach', 'phien_ban': '0.2', 'su_co': dong},
                             ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{ra}: {len(dong)} sự cố')


if __name__ == '__main__':
    sys.exit(main())
