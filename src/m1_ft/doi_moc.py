# -*- coding: utf-8 -*-
"""Kiểm độ nhạy mốc (T-064 SPEC bước 6, §7): dựng lại 7 tham số M1 từ gói ca với mốc dời t' = t + d.

Vì sao dựng lại thay vì chỉ đổi `inputs[5]`: `method-input.json` của P7 chỉ chứa span/log trong [t−300, t+300) của t
gốc; đổi riêng `inputs[5]` thì cửa sổ [t'−300, t'+300) của M1 hụt |d| giây ở một đầu. Gói ca (`cases/<id>/`, bộ đóng
gói ghim T-058 `stage-m1.py`) chứa dữ liệu thô [t−600, t+600) → dựng lại bằng **đúng** đường của runner ghim
(`run-m1.py`): `m1.adapter_flashticket.adapt(..., t')`, tham số = cấu hình khóa P7 + `params_ca` của adapter, cùng
các phép kiểm trường cấm và rò giá trị. Với d = 0, đường này phải cho `method-input.json` trùng byte bản đã lưu
(phép kiểm `--dung-lai-dau-vao --doi-t 0`).

Không đọc sổ tiêm lỗi hay nhãn. Mốc dời chỉ là t + d (d do người chạy khai, không suy từ nhãn).
"""
import copy
import hashlib
import json
import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
from m1 import chuoi, hop_dong  # noqa: E402
from m1.adapter_flashticket import adapt, jsonl  # noqa: E402

NS = 10 ** 9
CAM_CHUOI = ['/var/lib/flash-ticket-ledger', 'so-tiem-loi.jsonl', 'fault_service', 'injected_service',
             'injection_start', 'scenario_name']  # như danh sách `forbidden` của run-m1.py ghim


def _canonical(x):
    return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def dung_dau_vao(case_dir, ma_ca, t_moi, cau_hinh_p7, bien_doi=None):
    """→ (inputs, chan_doan). `case_dir` = <goc>/cases/<id>; `cau_hinh_p7` = dict cấu hình khóa (m1-p7-config.json).
    Ném SystemExit khi hash gói lệch, cửa sổ M1 vượt khỏi gói, hoặc có trường/giá trị cấm."""
    case = Path(case_dir)
    man = json.loads((case / 'manifest.json').read_text(encoding='utf-8'))
    for ten, mong in man['files'].items():
        p = case / ten
        if p.parent.resolve() != case.resolve():
            raise SystemExit('đầu vào ngoài danh sách của gói ca')
        if hashlib.sha256(p.read_bytes()).hexdigest() != mong['sha256']:
            raise SystemExit('hash gói ca lệch: ' + ten)
    lo_goi, hi_goi = man['pack_window_seconds']
    if not (lo_goi <= t_moi - 300 and t_moi + 300 <= hi_goi):
        raise SystemExit(f'cửa sổ M1 [t\'−300, t\'+300] vượt gói ca {man["pack_window_seconds"]}')
    inventory = json.loads((case / 'inventory.json').read_text(encoding='utf-8'))
    bundles = json.loads((case / 'prometheus.json').read_text(encoding='utf-8'))
    if bien_doi is not None:  # H8-adapter: biến đổi gói metric ghim trước adapter (vd. nối chuỗi container)
        bundles = bien_doi(bundles, inventory)
    conv = adapt(jsonl([case / 'raw-traces.jsonl']), jsonl([case / 'raw-logs.jsonl']), bundles, inventory, t_moi)
    params = copy.deepcopy(cau_hinh_p7)
    if set(params) & set(conv['params_ca']):
        raise SystemExit('adapter ghi đè tham số khóa')
    params.update(conv['params_ca'])
    chuoi._kiem_params(params)
    inputs = [conv['spans'], conv['metrics'], conv['logs'], conv['inventory'], conv['aliases'], t_moi, params]
    cam = [ma_ca, str(case), str(case.parent)] + CAM_CHUOI
    if hop_dong.vi_pham_truong_cam(inputs):
        raise SystemExit('trường cấm trong đầu vào dựng lại')
    if hop_dong.vi_pham_gia_tri(params, conv['aliases'], inventory, cam):
        raise SystemExit('giá trị cấm trong đầu vào dựng lại')
    ser = _canonical(inputs)
    if any(c in ser for c in cam):
        raise SystemExit('mã ca/đường dẫn lọt vào giá trị đầu vào')
    cov = params['coverage']
    lo, hi = (t_moi - 300) * NS, (t_moi + 300) * NS

    def _phu(c):  # nguồn có phủ trọn cửa sổ M1 không (theo khoảng thời gian adapter ghi)
        k = c.get('khoang') or []
        return bool(k) and min(a for a, _ in k) <= lo and max(b for _, b in k) + (c.get('r_ns') or 0) >= hi

    chan_doan = {'input_sha256': hashlib.sha256((ser + '\n').encode()).hexdigest(),
                 'goi_ca_cua_so': man['pack_window_seconds'], 't_moi': t_moi,
                 'nguon_khong_phu_tron': sorted(k for k, c in cov.items() if not _phu(c)),
                 'adapter': {'so_span': len(conv['spans']), 'so_log': len(conv['logs']),
                             'so_hang_metric': len(conv['metrics']),
                             'parent_missing_in_window': conv['chan_doan_adapter']['trace']['parent_missing_in_window'],
                             'unmapped_series': len(conv['chan_doan_adapter']['metric']['unmapped_series'])}}
    return inputs, chan_doan, ser
