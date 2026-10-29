"""T-044: băm bản ghi của bộ ca tất định (scripts/tat_dinh.py) sau khi bỏ các trường gói sửa phản biện lượt 1 mới thêm
(coverage của nguồn metric, extra.kenh_co_the_gioi; từ lượt 2 thêm extra.thong_ke_log). Chạy trên cây code cũ (git archive eccdfd77, hoặc 9206eaa6 cho lượt 2) và cây hiện tại rồi so:
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
        s = json.dumps(rec, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
        out[f'{ma_ca}|{ten}'] = hashlib.sha256(s.encode()).hexdigest()
print(json.dumps(out, sort_keys=True))
