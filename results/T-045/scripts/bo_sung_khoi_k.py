"""T-045: bổ sung vào `khoi-k.json` số ca đúng bị hỏng và ca được sửa của từng cặp luật C ở thế giới P (SPEC T-045 đầu ra
4), từ kết quả chấm đã lưu `khoi-k/kq.json`. Ca đúng: Hit@1 = 1 ở cấu hình tắt; bị hỏng: Hit@1 < 1 ở cấu hình bật. Ca
được sửa: Hit@1 < 1 ở cấu hình tắt và = 1 ở cấu hình bật. Kèm danh sách mã ca và số theo dataset. Không đổi trường cũ.
Chạy: $PY -B results/T-045/scripts/bo_sung_khoi_k.py results/T-045/khoi-k.json
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1_danh_gia import pha2  # noqa: E402


def main(p):
    p = Path(p)
    d = json.loads(p.read_text(encoding='utf-8'))
    kq = pha2.giai_ma_json(json.loads((p.with_suffix('') / 'kq.json').read_text(encoding='utf-8')))
    out = {}
    for k in d['cap']:
        a, b = k.split('|')
        ta, tb = kq['cau_hinh']['K-' + a]['ca'], kq['cau_hinh']['K-' + b]['ca']
        hong = sorted(o for o in ta if ta[o]['theo_the_gioi']['P']['hit1'] == 1 and tb[o]['theo_the_gioi']['P']['hit1'] < 1)
        sua = sorted(o for o in ta if ta[o]['theo_the_gioi']['P']['hit1'] < 1 and tb[o]['theo_the_gioi']['P']['hit1'] == 1)
        out[k] = {'hong': len(hong), 'sua': len(sua), 'ca_hong': hong, 'ca_sua': sua,
                  'theo_dataset': {ds: {'hong': sum(1 for o in hong if ta[o]['dataset'] == ds),
                                        'sua': sum(1 for o in sua if ta[o]['dataset'] == ds)} for ds in ('RE2-TT', 'Nezha-OB')}}
    d['ca_hong_sua_P'] = out
    p.write_text(json.dumps(d, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for k in ('R0|E1', 'R0|E2', 'R0|E3', 'R0|E5', 'R0|E1+E2', 'E1+E2|E1+E2+E3', 'E1+E2|E1+E2+E5'):
        print(k, out[k]['hong'], out[k]['sua'], out[k]['theo_dataset'])


if __name__ == '__main__':
    main(sys.argv[1])
