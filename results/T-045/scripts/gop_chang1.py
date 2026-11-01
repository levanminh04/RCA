"""T-045 chặng 1: gộp kết quả hai dataset vào các tệp đầu ra theo tên của SPEC (`t1.json`, `doi-chieu-ks16.json`,
`e3-khong-nhan.json`, `nhom-vong.json`). Mỗi tệp giữ nguyên nội dung các tệp theo dataset dưới khóa của dataset, kèm
nguồn. Không tính lại gì.
Chạy: $PY -B results/T-045/scripts/gop_chang1.py
"""
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parents[1]

GOP = {
    't1.json': {'Nezha-OB': 't1-nezha.json', 'RE2-TT': 't1-re2.json',
                'RE2-TT_kiem_doc_lap_metric_moc_gia': 'runs/b2-t1-re2-mocgia-001/kiem-doc-lap-metric.json'},
    'doi-chieu-ks16.json': {'Nezha-OB': 'doi-chieu-ks16-nezha.json', 'RE2-TT': 'doi-chieu-ks16-re2.json'},
    'e3-khong-nhan.json': {'Nezha-OB': 'e3-khong-nhan-nezha.json', 'RE2-TT': 'e3-khong-nhan-re2.json'},
    'nhom-vong.json': {'Nezha-OB': 'nhom-vong-nezha.json', 'RE2-TT': 'nhom-vong-re2.json'},
}

for ra, phan in GOP.items():
    out = {'nguon': {}, 'ghi_chu': 'gộp nguyên văn các tệp theo dataset của T-045 chặng 1 (scripts/gop_chang1.py)'}
    for k, tep in phan.items():
        p = R / tep
        out['nguon'][k] = {'tep': f'results/T-045/{tep}', 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
        out[k] = json.loads(p.read_text(encoding='utf-8'))
    (R / ra).write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(ra, list(phan))
