"""T-025 bước 4: chốt danh sách bản ghi đưa vào evaluator, ghi `bao-dong.json` và `ban-ghi-dua-vao-cham.json`.

Không đọc nhãn. Mỗi đối số `<loai>:<nhom>=<thư mục lượt>` với loai ∈ {bo_phat_hien, rca}. Lấy mọi `ban-ghi-*.json`
trong `luot/*/` của thư mục lượt. Một ca có nhiều bản ghi cùng (phương pháp, biến thể, seed) → dừng (phải chọn trước,
không chọn theo kết quả).

python chot.py bo_phat_hien:bocpd=runs/bocpd-ec2-001 ... rca:bocpd=runs/rca-bocpd-001 ... [ra=<thư mục>]
ra: thư mục ghi hai tệp (tương đối với results/T-025); mặc định results/T-025 (bản chốt). Chạy khô ghi vào work/.
"""
import json
import sys
from pathlib import Path

import chung


def main(args):
    items, bao_dong, khoa = [], {}, set()
    nguon = {}
    ra = chung.OUT
    for a in [x for x in args if x.startswith('ra=')]:
        ra = chung.OUT / a.split('=', 1)[1]
        ra.mkdir(parents=True, exist_ok=True)
    for a in [x for x in args if not x.startswith('ra=')]:
        lk, d = a.split('=', 1)
        loai, nhom = lk.split(':')
        d = chung.OUT / d
        nguon[lk] = {'thu_muc': d.relative_to(chung.ROOT).as_posix(),
                     'src_p3_sha256': json.loads((d / 'cau-hinh.json').read_text(encoding='utf-8'))['src_p3']['tong'],
                     'xong': (d / 'ket-thuc.json').exists()}
        for p in sorted(d.glob('luot/*/ban-ghi-*.json')):
            r = json.loads(p.read_text(encoding='utf-8'))
            k = (loai, nhom, r['opaque_id'], r['method'], r.get('variant'), r.get('seed'))
            if k in khoa:
                raise SystemExit(f'bản ghi trùng: {k}')
            khoa.add(k)
            items.append({'loai': loai, 'nhom': nhom, 'opaque_id': r['opaque_id'], 'method': r['method'],
                          'variant': r.get('variant'), 'seed': r.get('seed'), 'status': r['status'],
                          'duong_dan': p.relative_to(chung.ROOT).as_posix(), 'sha256': chung.sha256_file(p)})
            if loai == 'bo_phat_hien':
                kq_p = p.parent / 'ket-qua.json'
                kq = json.loads(kq_p.read_text(encoding='utf-8'))['ket_qua'] if kq_p.exists() else {}
                bao_dong.setdefault(nhom, {})[r['opaque_id']] = {
                    'run_id': r['run_id'], 'method': r['method'], 'tap_cot': r.get('tap_cot'), 'status': r['status'],
                    'error': r.get('error'), 'alarms': r.get('alarms'), 'chi_so': kq.get('chi_so'),
                    'bat_dau_danh_gia': r.get('bat_dau_danh_gia'), 'luot_rca': r.get('luot_rca'),
                    'diagnostics': r.get('diagnostics'), 'input_shape': r.get('input_shape'),
                    'detector_columns': r.get('detector_columns'),
                    'cost': {k: (r.get('cost') or {}).get(k) for k in ('wall_s', 'peak_rss_mb', 'timed_out', 'exit_code')}}
    hp = chung.hash_p3()['tong']
    al = chung.nap_allowlist()
    thieu = {nhom: sorted(set(al) - set(v)) for nhom, v in bao_dong.items()}
    chung.ghi_json(ra / 'bao-dong.json', {
        'mo_ta': 'Báo động thô chế độ (b) từng ca, từng bộ phát hiện (§7.2–7.5). BOCPD: điểm đổi tính lại từ R '
                 '(m[i] = argmax R[:, i+1]) và điểm đổi maxes gốc (đối chiếu, không chấm). t̂ = luot_rca.t_hat. '
                 'Không có nhãn.', 'tao_luc_utc': chung.bay_gio(), 'src_p3_sha256': hp, 'ca_thieu': thieu,
        'bo_phat_hien': bao_dong})
    chung.ghi_json(ra / 'ban-ghi-dua-vao-cham.json', {
        'mo_ta': 'Mọi bản ghi đưa vào evaluator T-025; chốt trước lượt evaluator đầu tiên (SPEC bước 4).',
        'tao_luc_utc': chung.bay_gio(), 'src_p3_sha256': hp, 'nguon': nguon, 'so_ban_ghi': len(items),
        'ban_ghi': items})
    print(json.dumps({'so_ban_ghi': len(items), 'ca_thieu': thieu, 'src_p3': hp[:16]}, ensure_ascii=False))


if __name__ == '__main__':
    main(sys.argv[1:])
