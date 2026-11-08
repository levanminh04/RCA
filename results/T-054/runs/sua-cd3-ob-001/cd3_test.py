"""C-d3 bổ sung cho 34 ca Nezha-OB test (laptop; Minh duyệt 08/11/2026). Không chạy lại M1.

Mỗi ca: lấy job.json + result.json M1 đã VERIFIED của main-013-v2 (đường dẫn từ phan-tich-nhom.json, kiểm hash
result với verified.json); đọc lại trace qua đúng bộ đọc/adapter đã ghim; dựng span A gốc hai cách:
  - cu  (không wrapper): phải tái lập đúng dau_vao_cd3 đã lưu (dich, so_span_goc_A) → kiểm phép dựng;
  - moi (wrapper "root"): tập đích sửa; gọi doi_chung.cd3 với canh/diem đã lưu.
Chấm sau cùng bằng exact_score (T-052) với root từ bảng đã ghép nhãn sau seal (phan-tich-nhom.json#/cases).
Đây là SỬA SAU KHI ĐÃ XEM TEST, không phải phép kiểm độc lập.
"""
import hashlib
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

RUN = Path(__file__).resolve().parent
sys.path.insert(0, str(RUN))
import lane  # noqa: E402

PT = lane.GOC / 'results/T-054/reports/p7a-013-v2/phan-tich-nhom.json'


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def log_exposure(event, **kw):
    with open(RUN / 'exposure.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps(dict(event=event, utc=datetime.now(timezone.utc).isoformat(), **kw), ensure_ascii=False) + '\n')


def main():
    t0 = time.perf_counter()
    pt = json.loads(PT.read_text(encoding='utf-8'))
    ids = sorted(k.split('|', 1)[1] for k in pt['trung_gian_theo_ca'] if k.startswith('Nezha-OB|'))
    assert len(ids) == 34
    first = lane.GOC / pt['trung_gian_theo_ca']['Nezha-OB|' + ids[0]]['M1']['result']
    job0 = json.loads((first.parent / 'job.json').read_text(encoding='utf-8'))
    lane.them_pythonpath(job0['pythonpath'])
    log_exposure('READ_OB_TEST_TRACE_START', n_case=34, grant='Minh 08/11/2026 gói C-d3 OB; main-grant test_grant')
    out = {'schema': 'T054-SUA-CD3-TEST-1', 'note': 'Sửa adapter sau khi đã xem test; không phải phép kiểm độc lập.',
           'cases': {}}
    contract = None
    for oid in ids:
        rp = lane.GOC / pt['trung_gian_theo_ca']['Nezha-OB|' + oid]['M1']['result']
        att = rp.parent
        job = json.loads((att / 'job.json').read_text(encoding='utf-8'))
        ver = json.loads((att / 'verified.json').read_text(encoding='utf-8'))
        rs = sha(rp)
        assert rs in json.dumps(ver), 'result.json không khớp verified.json: ' + oid
        assert job['slot']['arm'] == 'M1' and job['slot']['opaque_id'] == oid and job['slot']['dataset'] == 'Nezha-OB'
        rec = json.loads(rp.read_text(encoding='utf-8'))['records'][0]
        if contract is None:
            contract = json.loads((lane.GOC / job['m1_contract']['path']).read_text(encoding='utf-8'))
        t1 = time.perf_counter()
        res = {'result_sha256': rs, 'job_sha256': sha(att / 'job.json')}
        for mode, sua in (('cu', False), ('moi', True)):
            data, n = lane.doc_ca(job['source'], oid, job['inventory'], contract, str(lane.GOC), sua=sua)
            params = lane.params_m1(job['config'], data)
            spans_A, cd = lane.spans_A_goc(data, job['t'], params)
            r = lane.cd3_tu_luu(rec['extra'], spans_A)
            r.update(n_span_doi_root=n, chan_doan={k: cd[k] for k in ('goc', 'mo_coi', 'so_span')})
            res[mode] = json.loads(lane.dump(r))
        luu = rec['extra']['dau_vao_cd3']
        res['cu_tai_lap_luu'] = (res['cu']['dich'] == luu['dich'] and res['cu']['so_span_goc_A'] == luu['so_span_goc_A'])
        res['giay'] = round(time.perf_counter() - t1, 2)
        out['cases'][oid] = res
        print(oid, res['cu_tai_lap_luu'], res['moi']['cd3']['trang_thai'], res['moi']['dich'], res['giay'], flush=True)
    log_exposure('READ_OB_TEST_TRACE_END', n_case=len(out['cases']))
    # chấm: chỉ sau khi đã có đầu ra phi nhãn ở trên
    out_path = RUN / 'cd3-test-phi-nhan.json'
    out_path.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
    log_exposure('LABEL_USE_FOR_SCORING', source='results/T-054/reports/p7a-013-v2/phan-tich-nhom.json#/cases',
                 phi_nhan_sha256=sha(out_path))
    sys.path.insert(0, str(lane.GOC / 'results/T-052/scripts'))
    from bang_doc_lap import exact_score
    from m1_danh_gia.pha2 import giai_ma_json

    def ban_ghi(raw):
        # như worker (bản ghi C-d3) rồi như cham.describe (giải mã JSON đã seal)
        return giai_ma_json(json.loads(lane.dump(dict(raw, method='C-d3', variant='cd3', mode='a', seed=None,
                                                       status=raw['trang_thai']))))

    # kiểm đường chấm trên TT: tính lại C-d3 từ dau_vao_cd3 đã lưu của M1 TT, chấm, so tables.json
    from fractions import Fraction
    from m1 import doi_chung
    tables = json.loads((lane.GOC / 'results/T-054/reports/main-013-v2/tables.json').read_text(encoding='utf-8'))
    tt_rows = {r['opaque_id']: r for r in tables['rows'] if r['dataset'] == 'RE2-TT' and r['arm'] == 'C-d3'}
    kiem_tt = {'n': 0, 'khop': 0, 'lech': []}
    for key, v in pt['trung_gian_theo_ca'].items():
        ds, oid = key.split('|', 1)
        if ds != 'RE2-TT' or oid not in tt_rows:
            continue
        ex = json.loads((lane.GOC / v['M1']['result']).read_text(encoding='utf-8'))['records'][0]['extra']
        d = dict(ex['dau_vao_cd3'])
        d.setdefault('canh', ex['canh'])
        raw = json.loads(lane.dump(doi_chung.cd3(d['canh'], {e: Fraction(*p) for e, p in d['diem'].items()}, d['dich'])))
        s = exact_score(ban_ghi(raw), pt['cases']['RE2-TT'][oid]['root'])
        kiem_tt['n'] += 1
        ok = Fraction(s['RR']) == Fraction(*tt_rows[oid]['metrics']['RR']['phan_so'])
        kiem_tt['khop'] += ok
        if not ok:
            kiem_tt['lech'].append(oid)
    cham = {}
    for oid, res in out['cases'].items():
        c = pt['cases']['Nezha-OB'][oid]
        raw = res['moi']['cd3']
        rec = ban_ghi(raw)
        try:
            s = exact_score(rec, c['root'])
            sc = {'RR': float(s['RR']), 'Hit5_Q': float(s['Hit5_Q']), 'status': s['status']}
        except Exception as e:  # ghi nguyên lỗi, không đoán
            sc = {'ERROR': f'{type(e).__name__}: {e}'}
        cham[oid] = dict(sc, cell=c['cell'], fault=c['fault'], trang_thai=raw['trang_thai'])
    (RUN / 'cd3-test-cham.json').write_text(json.dumps({'schema': 'T054-SUA-CD3-CHAM-1', 'phi_nhan_sha256': sha(out_path),
                                                       'kiem_duong_cham_TT': kiem_tt, 'cases': cham}, ensure_ascii=False, indent=1, sort_keys=True), encoding='utf-8')
    print('tong_giay', round(time.perf_counter() - t0, 1))


if __name__ == '__main__':
    main()
