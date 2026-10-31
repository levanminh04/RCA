"""T-044: băm bản ghi của bộ ca tất định (scripts/tat_dinh.py) sau khi bỏ các trường gói sửa phản biện lượt 1 mới thêm
(coverage của nguồn metric, extra.kenh_co_the_gioi; từ lượt 2 thêm extra.thong_ke_log; từ lượt 3 thêm `ma` của
extra.kenh_co và `ma`, `don_vi`, `giai_thich_ma` của inherited_by). Chạy trên cây code cũ (git archive eccdfd77,
9206eaa6 cho lượt 2, 253dbe46 cho lượt 3) và cây hiện tại rồi so:
giống nhau thì gói sửa không đổi phần còn lại của bản ghi (khối, thứ hạng, verdict, kênh...).

    python -B results/T-044/scripts/so_ban_ghi_truoc_sau.py <gốc repo> > <ra>.json
"""
import sys, json, hashlib, importlib.util
goc = sys.argv[1]
sys.argv = ['x']
spec = importlib.util.spec_from_file_location('td', goc + '/results/T-044/scripts/tat_dinh.py')
td = importlib.util.module_from_spec(spec); spec.loader.exec_module(td)
out = {}
for ma_ca, spans, metrics, logs, them in td._ca():
    for ten, ch in td.CAU_HINH.items():
        td.chuoi.CACHE = td.e4.CacheCong()
        rec = td.chuoi.chay(spans, metrics, logs, td.U, {}, 1000, td._params(ten, ch, them))
        rec['coverage'] = {k: v for k, v in rec['coverage'].items() if k in ('trace', 'log')}
        rec['extra'].pop('kenh_co_the_gioi', None)
        rec['extra'].pop('thong_ke_log', None)
        rec['extra'].pop('E6b_pi', None)  # lượt 4 (S23)
        # lượt 3 (S12): mã kênh gồm đơn vị
        for k in rec['extra'].get('kenh_co') or []:
            k.pop('ma', None)
        for x in rec.get('inherited_by') or []:
            for f in ('ma', 'don_vi', 'giai_thich_ma'):
                x.pop(f, None)
        # hai danh sách này sắp theo mã kênh, mà mã đổi ở lượt 3: so theo nội dung, không theo thứ tự
        for ds, gan in ((rec['extra'].get('kenh_co'), lambda v: rec['extra'].__setitem__('kenh_co', v)),
                        (rec.get('inherited_by'), lambda v: rec.__setitem__('inherited_by', v))):
            if ds:
                gan(sorted(ds, key=lambda x: json.dumps(x, sort_keys=True, ensure_ascii=False)))
        s = json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
        out[f'{ma_ca}|{ten}'] = hashlib.sha256(s.encode()).hexdigest()
print(json.dumps(out, sort_keys=True))
