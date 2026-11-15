"""T-061: lớp phát lại — ghép đáp án vào kết quả RCA đã chuyển đổi, CHỈ ở bước trình bày.

Thứ tự bắt buộc (PLAN-TRIEN-KHAI §5.2–5.3; gói C2 đã duyệt 11/11/2026):
1. Đọc danh sách ca của đợt từ bản ghi phát lượt đã ghim (`m1-launch-record.json`, chỉ dùng `/ids`), kiểm hash theo
   manifest lượt chạy. Không đọc file kế hoạch mà bản ghi đó trỏ tới.
2. Kiểm đủ đợt: không trùng mã; tập mã = tập mẫu trong manifest mẫu; byte từng mẫu khớp manifest mẫu; mã ca trong
   mẫu và thư mục nguồn M1 ghi trong `nguon.file_m1` đều trùng mã.
3. Chỉ khi cả đợt đạt mới mở nguồn đáp án (kế hoạch có vai trò ca, sổ tiêm lỗi đã nhận; kiểm hash theo manifest
   lượt chạy) và THÊM khối `phat_lai` vào từng mẫu. Mọi trường khác giữ nguyên.

Bộ chuyển đổi (`chuyen-doi.py`) không import và không gọi file này.

Cách dùng (trong results/T-061):
  py -3 -B phat-lai.py --dot <m1-launch-record.json> --thu-muc-mau mau --manifest-mau mau/manifest-mau.json
     --ke-hoach <m1-execution-plan-v2.json> --so <ledger-received.jsonl> --manifest <artifacts-sha256.json>
     --goc-manifest <thư mục gốc của manifest>
"""
import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True


class LoiDot(Exception):
    """Đợt không đạt kiểm; chưa mở nguồn đáp án."""


def doc_da_kiem(path, manifest, goc):
    m = json.load(open(manifest, encoding='utf-8'))
    rel = Path(os.path.relpath(path, goc)).as_posix()
    muc = m['files'].get(rel)
    b = Path(path).read_bytes()
    if muc is None or muc['sha256'] != hashlib.sha256(b).hexdigest() or muc['bytes'] != len(b):
        raise LoiDot(f'Không khớp manifest lượt chạy: {rel}')
    return rel, hashlib.sha256(b).hexdigest(), b


def kiem_dot(ids, thu_muc_mau, manifest_mau):
    """Kiểm đủ đợt trước khi mở bất kỳ nguồn đáp án nào. Trả {mã: (đường dẫn mẫu, sha256, nội dung)}."""
    if len(ids) != len(set(ids)):
        raise LoiDot(f'Danh sách ca có mã trùng: {sorted(i for i in set(ids) if ids.count(i) > 1)}')
    mm = json.load(open(manifest_mau, encoding='utf-8'))['files']
    co_trong_manifest = {Path(k).stem for k in mm}
    if set(ids) != co_trong_manifest:
        raise LoiDot(f'Đợt và manifest mẫu lệch: thiếu {sorted(set(ids) - co_trong_manifest)}, '
                     f'thừa {sorted(co_trong_manifest - set(ids))}')
    out = {}
    for ma in ids:
        p = Path(thu_muc_mau) / f'{ma}.json'
        if not p.exists():
            raise LoiDot(f'Thiếu mẫu của ca {ma}')
        b = p.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        if mm[p.name]['sha256'] != h or mm[p.name]['bytes'] != len(b):
            raise LoiDot(f'Mẫu {p.name} đã đổi sau khi băm')
        kq = json.loads(b.decode('utf-8'))
        nguon_ma = Path(kq['nguon']['file_m1']).parent.name
        if kq['su_co']['ma'] != ma or nguon_ma != ma:
            raise LoiDot(f'Mã ca của {p.name} không khớp nguồn ({kq["su_co"]["ma"]}, {nguon_ma})')
        out[ma] = (p, h, kq)
    return out


def dap_an(ma, ke_hoach, su_kien):
    ca = [c for c in ke_hoach['planned_cases'] if c['opaque_id'] == ma]
    if len(ca) != 1:
        raise SystemExit(f'Không có đúng một ca {ma} trong kế hoạch')
    ca = ca[0]
    bat_dau = [e for e in su_kien if e.get('opaque_id') == ma and e.get('event') == 'intervention_start']
    if not bat_dau:
        return {'thanh_phan_tiem': None, 'ho_loi': None, 'moc_xac_nhan_utc': None,
                'vai_tro_ke_hoach': ca.get('operator_only_role')}
    if len(bat_dau) != 1:
        raise SystemExit(f'Ca {ma} có nhiều sự kiện bắt đầu tiêm')
    e = bat_dau[0]
    return {'thanh_phan_tiem': e['component'], 'ho_loi': e['fault_family'],
            'moc_xac_nhan_utc': e['confirmed']['utc'], 'vai_tro_ke_hoach': ca.get('operator_only_role')}


def nhan_xet(kq, da):
    if da['thanh_phan_tiem'] is None:
        return (f'Đáp án: không có lỗi được tiêm trong cửa sổ này (kế hoạch: "{da["vai_tro_ke_hoach"]}"). '
                f'Kết luận M1: {kq["su_co"]["ket_luan"]}.')
    tp = da['thanh_phan_tiem']
    nut = {n['id']: n for n in kq['nut']}
    if tp not in nut:
        vt = 'không có trong các thực thể M1 quan sát'
    else:
        n = nut[tp]
        vt = f'vai trò dự đoán "{n["vai_tro"]}", ' + (f'hạng {n["hang"]}' if n['hang'] else 'không có hạng')
    return f'Đáp án: {tp}, họ lỗi {da["ho_loi"]}. Trong dự đoán M1, {tp}: {vt}.'


def main(argv=None):
    sys.stdout.reconfigure(encoding='utf-8')
    ap = argparse.ArgumentParser()
    for x in ('--dot', '--thu-muc-mau', '--manifest-mau', '--ke-hoach', '--so', '--manifest', '--goc-manifest'):
        ap.add_argument(x, required=True)
    a = ap.parse_args(argv)
    try:
        r_dot, h_dot, b_dot = doc_da_kiem(a.dot, a.manifest, a.goc_manifest)
        ids = json.loads(b_dot.decode('utf-8'))['ids']
        mau = kiem_dot(ids, a.thu_muc_mau, a.manifest_mau)
    except LoiDot as ex:
        print(f'Dừng trước khi mở nguồn đáp án: {ex}')
        return 2
    # chỉ tới đây mới mở nguồn đáp án
    r1, h1, b1 = doc_da_kiem(a.ke_hoach, a.manifest, a.goc_manifest)
    r2, h2, b2 = doc_da_kiem(a.so, a.manifest, a.goc_manifest)
    ke_hoach = json.loads(b1.decode('utf-8'))
    su_kien = [json.loads(x) for x in b2.decode('utf-8').splitlines() if x.strip()]
    for ma in ids:
        p, h_kq, kq = mau[ma]
        da = dap_an(ma, ke_hoach, su_kien)
        out = dict(kq)
        out['phat_lai'] = {
            'canh_bao': 'Bản phát lại: đáp án ghép SAU khi kết quả cả đợt đã băm; không dùng để chẩn đoán trực tuyến.',
            'nguon_dap_an': [r1, r2], 'sha256_dap_an': {r1: h1, r2: h2}, 'sha256_ket_qua_truoc_ghep': h_kq,
            'thanh_phan_tiem': da['thanh_phan_tiem'], 'ho_loi': da['ho_loi'],
            'moc_xac_nhan_utc': da['moc_xac_nhan_utc'], 'nhan_xet': nhan_xet(kq, da)}
        ra = p.with_name(f'{ma}.phat-lai.json')
        with open(ra, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(out, f, ensure_ascii=False, indent=1, allow_nan=False)
            f.write('\n')
        print(f'{ra}: {out["phat_lai"]["nhan_xet"]}')
    print(f'Đợt {r_dot} (sha256 {h_dot[:12]}…): {len(ids)} ca, đủ và khớp hash trước khi ghép.')


if __name__ == '__main__':
    sys.exit(main())
