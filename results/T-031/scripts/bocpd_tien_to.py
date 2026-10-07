"""T-031 bước 6 (Q-77): đo thời gian BOCPD trên tiền tố T điểm đầu, không chạy đủ 1.441 điểm trên laptop.

Mỗi T một lượt, tiến trình con, giới hạn 3.600 s, đo wall và RSS đỉnh bằng runner.chay_tien_trinh.
Trong tiến trình con: tiền xử lý §7.2 trên CẢ bản ghi (chọn cột Q-67, bỏ cột hằng, ffill, điền 0, min–max,
ffill, điền 0 — `phat_hien.tien_xu_ly_bocpd`, giữ đúng d của ca), rồi lấy T dòng đầu và gọi
`online_changepoint_detection(X, partial(constant_hazard, 50), MultivariateT(dims=d))` như §7.2.
Không chấm phát hiện, không tính điểm đổi, không lưu hay đọc R/maxes: chỉ dùng thời gian và RSS.
Một luồng phụ đọc `MultivariateT.t` (số bước đã xử lý) mỗi 5 s để ghi tiến độ theo thời gian; luồng này không
đổi phép tính.

python bocpd_tien_to.py me <oid> <T1,T2,...>     # tiến trình mẹ (đo)
python bocpd_tien_to.py con <job.json> <out.json>  # tiến trình con (runner gọi)
"""
import json
import sys
import threading
import time

import chung


def con(job_path, out_path):
    import pandas as pd
    from functools import partial
    from baro._bocpd import MultivariateT, constant_hazard, online_changepoint_detection
    from p3.adapters import phat_hien
    job = json.loads(open(job_path, encoding='utf-8').read())
    s0 = time.perf_counter()
    if chung.sha256_file(job['metrics']) != job['sha256']:
        raise chung.selector.LoiRunner('SHA-256 sai')
    m = pd.read_parquet(job['metrics'])
    cot = phat_hien.cot_bocpd(m.columns)
    data = phat_hien.tien_xu_ly_bocpd(m[cot])
    X = data.to_numpy()[:job['T']]
    d = int(data.shape[1])
    s1 = time.perf_counter()
    lik = MultivariateT(dims=d)
    mau, dung = [], threading.Event()
    td = open(job['tien_do'], 'a', encoding='utf-8')

    def theo_doi():
        while not dung.wait(5.0):
            e = time.perf_counter() - s2
            mau.append([round(e, 2), int(lik.t)])
            td.write(f'{e:9.1f}s buoc={lik.t}/{len(X)}\n')
            td.flush()
    s2 = time.perf_counter()
    th = threading.Thread(target=theo_doi, daemon=True)
    th.start()
    online_changepoint_detection(X, partial(constant_hazard, 50), lik)
    s3 = time.perf_counter()
    dung.set()
    th.join()
    td.close()
    out = {'T': int(len(X)), 'T_ban_ghi': int(len(m)), 'd_tho': len(cot), 'd': d,
           'giay_doc_tien_xu_ly': round(s1 - s0, 3), 'giay_goi_bocpd': round(s3 - s2, 3),
           'so_lan_pdf': int(len(X) * (len(X) + 1) // 2), 'mau_tien_do': mau}
    json.dump(out, open(out_path, 'w', encoding='utf-8'))


def me(oid, Ts):
    from p3 import runner
    al, _ = chung.nap()
    f = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['metrics.parquet'])
    L = chung.Luot(f'bocpd-tien-to-{oid}', {'phuong_phap': 'bocpd', 'opaque_id': oid, 'T': Ts})
    rows = []
    for T in Ts:
        d = L.dir / f'T{T}'
        d.mkdir()
        job = {'metrics': f['metrics.parquet'], 'sha256': al[oid]['files']['metrics.parquet']['sha256'], 'T': T,
               'tien_do': str(d / 'tien-do-con.txt')}
        (d / 'job.json').write_text(json.dumps(job, ensure_ascii=False, indent=1), encoding='utf-8')
        ram = chung.ram_trong_gb()
        L.ghi(f'T={T}: bắt đầu; RAM trống {ram} GB')
        cost = runner.chay_tien_trinh('main', [__file__, 'con', str(d / 'job.json'), str(d / 'ket-qua.json')],
                                      chung.TIMEOUT_S, hashseed=0, log_dir=d)
        kq = json.loads((d / 'ket-qua.json').read_text(encoding='utf-8')) if (d / 'ket-qua.json').exists() else None
        trang_thai = 'TIMEOUT' if cost['timed_out'] else ('OK' if kq and cost['exit_code'] == 0 else 'LOI')
        row = {'T': T, 'trang_thai': trang_thai, 'cost': cost, 'ram_truoc_gb': ram, 'ket_qua': kq}
        if trang_thai == 'TIMEOUT':  # cận dưới: bước cuối đã ghi trong tiến độ của con
            try:
                last = (d / 'tien-do-con.txt').read_text(encoding='utf-8').strip().splitlines()[-1]
            except (OSError, IndexError):
                last = None
            row['tien_do_cuoi'] = last
        rows.append(row)
        chung.ghi_json(d / 'luot.json', row)
        L.ghi(f'T={T}: {trang_thai} wall={cost["wall_s"]}s goi={kq and kq["giay_goi_bocpd"]}s d={kq and kq["d"]} '
              f'rss={cost["peak_rss_mb"]}MB')
    chung.ghi_json(L.dir / 'tom-tat.json', {'mo_ta': __doc__.strip(), 'opaque_id': oid, 'luot': rows,
                                            'src_p3_sha256': L.ch['src_p3']['tong']})
    L.xong({'T': Ts, 'trang_thai': [r['trang_thai'] for r in rows]})


if __name__ == '__main__':
    if sys.argv[1] == 'con':
        con(sys.argv[2], sys.argv[3])
    else:
        me(sys.argv[2], [int(x) for x in sys.argv[3].split(',')])
