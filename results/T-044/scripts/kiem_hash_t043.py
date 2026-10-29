"""T-044: kiểm hash T-043 trên bản clone git (SPEC T-044 dòng 44, 86, 118; R1 Minh duyệt 29/10/2026).

Git không lưu thư mục rỗng, nên thư mục của lượt hỏng `runs/khe-open-001` không có trên bản clone.
Script:
- chép results/T-043 vào thư mục tạm;
- chỉ dựng lại thư mục lượt có trong manifest.json#/luot_chay mà không có trên đĩa, và manifest
  không ghi file nào bằng hoặc nằm dưới đường dẫn đó (tức thư mục vốn rỗng);
- chạy nguyên results/T-043/scripts/tao_manifest.py --kiem trên bản sao.
Mọi lệch khác (file thiếu, file thừa, hash lệch, hash đóng băng) vẫn FAIL. Không ghi vào results/T-043.
Chạy: python -B results/T-044/scripts/kiem_hash_t043.py
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
GOC = ROOT / 'results' / 'T-043'


def main():
    m = json.loads((GOC / 'manifest.json').read_text(encoding='utf-8'))
    tep = [x['path'] for x in m['outputs']]
    dung_lai = []
    with tempfile.TemporaryDirectory(prefix='kiem-t043-') as tmp:
        dich = Path(tmp) / 'results' / 'T-043'
        shutil.copytree(GOC, dich)
        for luot in m['luot_chay']:
            rel = luot['duong_dan'].rstrip('/')
            if (dich / rel).exists():
                continue
            day_du = f'results/T-043/{rel}'
            if any(t == day_du or t.startswith(day_du + '/') for t in tep):
                continue  # manifest ghi file ở đây: thiếu thật, để --kiem báo
            (dich / rel).mkdir(parents=True)
            dung_lai.append(rel)
        r = subprocess.run([sys.executable, '-B', str(dich / 'scripts' / 'tao_manifest.py'), '--kiem'],
                           capture_output=True, text=True, encoding='utf-8')
    print(json.dumps({'thu_muc_dung_lai': dung_lai}, ensure_ascii=False))
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    sys.exit(r.returncode)


if __name__ == '__main__':
    main()
