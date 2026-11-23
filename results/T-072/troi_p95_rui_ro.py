# -*- coding: utf-8 -*-
"""T-072 — ước lượng thô (mô hình, suy luận) tần suất p95 cửa sổ 5 phút vượt ngưỡng do số ít request chậm.
Giả định: N = 72 request/5 phút (đo), request chậm độc lập (Poisson), mọi request chậm nằm trong bucket (0,1; 0,25];
p95 histogram_quantile = 0,1 + 0,15·(k − 0,05·N)/k khi k request > 0,1 s. k_min = số request chậm ít nhất để p95 > θ.
Đọc troi-p95-e2-e4.json (tỷ lệ request > 0,1 s theo lượt) và nguong.json. Ghi troi-p95-rui-ro.json."""
import json, math, pathlib
G = pathlib.Path(__file__).parent
d = json.loads((G / 'troi-p95-e2-e4.json').read_text(encoding='utf-8'))
ng = json.loads((G / 'nguong.json').read_text(encoding='utf-8'))['nguong']
N = 72
def p_ge(lam, k):
    return 1 - sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k))
out = {'gia_dinh': __doc__, 'route': {}}
for r in ('payment', 'ticket'):
    th = ng[f'theta_p95_{r}']
    kmin = next(k for k in range(1, N) if k > 0.05 * N and 0.1 + 0.15 * (k - 0.05 * N) / k > th)
    x1 = [l['route'][r]['ty_le_tren_0_1'] for l in d['luot'] if l['tag'].endswith('x1')]
    e2 = [l['route'][r]['ty_le_tren_0_1'] for l in d['luot'] if l['khoang'] == 'e2' and l['tag'].endswith('x1')]
    e4 = [l['route'][r]['ty_le_tren_0_1'] for l in d['luot'] if l['khoang'] == 'e4' and l['tag'].endswith('x1')]
    o = {'nguong': th, 'k_min_request_cham_5ph': kmin, 'theo_ty_le': {}}
    for ten, f in (('tb_e2_x1', sum(e2) / len(e2)), ('tb_e4_x1', sum(e4) / len(e4)), ('max_luot_x1', max(x1)), ('min_luot_x1', min(x1))):
        lam = N * f; p = p_ge(lam, kmin)
        o['theo_ty_le'][ten] = {'ty_le_tren_0_1': round(f, 5), 'lambda_5ph': round(lam, 3), 'p_cua_so': p, 'ky_vong_moi_6_gio_72_cua_so': round(72 * p, 4)}
    out['route'][r] = o
(G / 'troi-p95-rui-ro.json').write_text(json.dumps(out, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
for r, o in out['route'].items():
    print(r, 'k_min', o['k_min_request_cham_5ph'], {k: (v['ty_le_tren_0_1'], v['lambda_5ph'], '%.2e' % v['p_cua_so'], v['ky_vong_moi_6_gio_72_cua_so']) for k, v in o['theo_ty_le'].items()})
