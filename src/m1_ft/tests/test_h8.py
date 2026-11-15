# -*- coding: utf-8 -*-
"""Test đơn vị H8-adapter và H8-log (phiên C, T-064). Chạy (môi trường ghim, từ gốc repo):
  PYTHONPATH=D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B src/m1_ft/tests/test_h8.py
Dữ liệu: gói metric thật của ca T-062 a5539fba (không nhãn). Ca tổng hợp ở đây là KIỂM CÀI ĐẶT, không phải bằng chứng hiệu quả."""
import copy, json, sys
from pathlib import Path
sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1 import adapter_flashticket as ad  # noqa: E402
from m1_ft.thanh_phan import h8_adapter as h8a, h8_log  # noqa: E402

CA = ROOT / 'results/T-062/ca/a5539fba/cases/a5539fba'
LOOKBACK = 300.0


def tach(bundles, kenh, svc, t_tach, them_nhan=None):
    """Tách chuỗi (kenh, svc) tại t_tach thành hai container như Prometheus thật: chuỗi cũ giữ điểm có mẫu gốc < t_tach
    và lặp mẫu cuối (mốc gốc cũ) ở các mốc đánh giá sau đó trong lookback; chuỗi mới giữ điểm có mẫu gốc ≥ t_tach."""
    out = copy.deepcopy(bundles)
    b = next(x for x in out if x['channel'] == kenh)
    s = next(x for x in b['result'] if x['metric'].get('service_name') == svc)
    k = ad._labels_key(s['metric'])
    n = next(x for x in b['native_timestamps'] if ad._labels_key(x['metric']) == k)
    nmap = {str(e): v for e, v in n['values']}
    cu_v, cu_n, moi_v, moi_n = [], [], [], []
    last = None
    for e, v in s['values']:
        nt = nmap[str(e)]
        if float(nt) < t_tach:
            cu_v.append([e, v]); cu_n.append([e, nt]); last = (v, nt)
        else:
            moi_v.append([e, v]); moi_n.append([e, nt])
            if last and float(e) - float(last[1]) <= LOOKBACK:
                cu_v.append([e, last[0]]); cu_n.append([e, last[1]])
    m_cu = dict(s['metric'], container_id='aaaa'); m_moi = dict(s['metric'], container_id='bbbb', **(them_nhan or {}))
    b['result'] = [x for x in b['result'] if x is not s] + [{'metric': m_cu, 'values': cu_v}, {'metric': m_moi, 'values': moi_v}]
    b['native_timestamps'] = [x for x in b['native_timestamps'] if x is not n] + [
        {'metric': m_cu, 'values': cu_n}, {'metric': m_moi, 'values': moi_n}]
    return out


def main():
    bundles = json.loads((CA / 'prometheus.json').read_text(encoding='utf-8'))
    inv = json.loads((CA / 'inventory.json').read_text(encoding='utf-8'))
    t = json.loads((CA / 'request.json').read_text(encoding='utf-8'))['t']
    goc = ad.normalize_metrics(bundles, inv)
    # 1. không có nhóm cần nối → trả nguyên (trùng byte)
    moi, cd = h8a.noi_chuoi(bundles, inv, ad._owner)
    assert json.dumps(moi) == json.dumps(bundles) and not cd['nhom_noi'], 'không nhóm nào thì phải trả nguyên'
    # 2. tách cpu và mem của booking-service tại t + 60 → adapter ghim ném; nối lại → đầu ra adapter trùng bản gốc
    gia = tach(tach(bundles, 'cpu', 'booking-service', t + 60), 'mem', 'booking-service', t + 60)
    try:
        ad.normalize_metrics(gia, inv); raise AssertionError('adapter ghim phải ném lỗi trên ca tách')
    except ValueError as e:
        assert 'Multiple runtime series' in str(e)
    noi, cd = h8a.noi_chuoi(gia, inv, ad._owner)
    sau = ad.normalize_metrics(noi, inv)
    for i, ten in enumerate(['rows', 'owners', 'indices', 'clocks', 'coverage', 'aliases']):
        assert json.dumps(sau[i], sort_keys=True) == json.dumps(goc[i], sort_keys=True), f'lệch {ten} sau khi nối'
    assert len(cd['nhom_noi']) == 2 and cd['mat_mau'] == 0 and cd['diem_lap_bo'] > 0, cd
    # 3. chồng lấn trong mốc mẫu gốc → không nối (adapter vẫn ném)
    chong = tach(bundles, 'cpu', 'booking-service', t + 60)
    b = next(x for x in chong if x['channel'] == 'cpu')
    moi_s = [x for x in b['native_timestamps'] if x['metric'].get('container_id') == 'bbbb'][0]
    cu_s = [x for x in b['native_timestamps'] if x['metric'].get('container_id') == 'aaaa'][0]
    moi_s['values'][0][1] = str(float(cu_s['values'][-1][1]) - 1)  # mẫu đầu của chuỗi mới trước mẫu cuối chuỗi cũ
    _, cd3 = h8a.noi_chuoi(chong, inv, ad._owner)
    assert cd3['nhom_khong_noi'] and cd3['nhom_khong_noi'][0]['ly_do'] == 'chong_lan_moc_mau_goc', cd3
    # 4. khác nhãn ngoài nhãn runtime → không nối
    khac = tach(bundles, 'cpu', 'booking-service', t + 60, them_nhan={'host_id': 'may-khac'})
    _, cd4 = h8a.noi_chuoi(khac, inv, ad._owner)
    assert cd4['nhom_khong_noi'][0]['ly_do'] == 'khac_nhan_ngoai_runtime', cd4
    print('H8-adapter OK', {k: (len(v) if isinstance(v, list) else v) for k, v in cd.items()})

    # 5. H8-log-kq: phân loại lại theo outcome; dòng không ghép được thì ném
    logs = [{'timestamp': 1, 'entity': 'a', 'message': 'x', 'severity_raw': 'INFO'},
            {'timestamp': 2, 'entity': 'a', 'message': 'y', 'severity_raw': 'ERROR'},
            {'timestamp': 3, 'entity': 'b', 'message': 'z', 'severity_raw': 'WARN'},
            {'timestamp': 4, 'entity': 'b', 'message': 'w', 'severity_raw': 'INFO'}]
    phu = [dict(logs[0], outcome='UNKNOWN'), dict(logs[1], outcome='RETRY'), dict(logs[2], outcome=None),
           dict(logs[3], outcome='SUCCESS')]
    params = {'ho_so_nguon': {'quy_tac_log': {'loi': ['ERROR', 'FATAL']}}}
    tp = h8_log.LogKetCuc({}); tp.bo_sung = {'log_phu': phu}
    ra = tp.vao([[], [], logs, [], {}, 0, params])[2]
    assert [r['severity_raw'] for r in ra] == ['ERROR', 'INFO', 'WARN', 'INFO'], ra
    assert tp.cd['len_loi'] == 1 and tp.cd['xuong_khong_loi'] == 1 and tp.cd['giu'] == 1, tp.cd
    tp.bo_sung = {'log_phu': phu[:3]}
    try:
        tp.vao([[], [], logs, [], {}, 0, params]); raise AssertionError('phải ném khi thiếu ghép')
    except ValueError:
        pass
    # 6. H8-log-chuoi: ô đóng dấu đầu ô; bản ghi tại t vào ô t (A), tại t − 1 ns vào ô t − 15 (N)
    T = 1000
    phu2 = [{'timestamp': T * 10 ** 9, 'entity': 'svc', 'outcome': 'FAILED'},
            {'timestamp': T * 10 ** 9 - 1, 'entity': 'svc', 'outcome': 'SUCCESS'},
            {'timestamp': (T - 300) * 10 ** 9, 'entity': 'svc', 'outcome': 'SUCCESS'},
            {'timestamp': (T + 300) * 10 ** 9, 'entity': 'svc', 'outcome': 'FAILED'}]  # ngoài lưới, bỏ
    tc = h8_log.LogChuoiKetCuc({}); tc.bo_sung = {'log_phu': phu2}
    bb = tc.bien_doi_bundle([], [None] * 5 + [T, None])
    loi = {e: float(v) for e, v in bb[0]['result'][0]['values']}; ok = {e: float(v) for e, v in bb[1]['result'][0]['values']}
    assert len(loi) == 40 and loi[str(T)] == 1.0 and loi[str(T - 15)] == 0.0 and ok[str(T - 15)] == 1 / 15
    assert ok[str(T - 300)] == 1 / 15 and tc.cd['ban_ghi'] == {'svc': 3}, (loi, ok, tc.cd)
    print('H8-log OK')


main()
