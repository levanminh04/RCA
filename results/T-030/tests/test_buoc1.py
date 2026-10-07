"""T-030 bước 1: selector (§11.1) và cắt cửa sổ (§11.3). Fixture tổng hợp, đáp án tính tay."""
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
WORK = ROOT / 'results' / 'T-030' / 'work'
WORK.mkdir(parents=True, exist_ok=True)

from p3 import selector, cua_so  # noqa: E402


def _tao_repo(tmp):
    d = Path(tmp) / 'data' / 'rcaeval' / 'caX'
    d.mkdir(parents=True)
    (d / 'metrics.parquet').write_bytes(b'metric-bytes')
    lk = Path(tmp) / 'data' / 'locked' / 'caY'
    lk.mkdir(parents=True)
    (lk / 'metrics.parquet').write_bytes(b'locked')
    sha = selector.sha256_file(d / 'metrics.parquet')
    al = {'so_ca': 1, 'cases': [{'opaque_id': 'dev-0123456789', 'case_dir': 'data/rcaeval/caX',
                                 'files': {'metrics.parquet': {'path': 'data/rcaeval/caX/metrics.parquet',
                                                               'bytes': 12, 'sha256': sha}}}]}
    p = Path(tmp) / 'al.json'
    p.write_text(json.dumps(al), encoding='utf-8')
    return p, al


class Selector(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=WORK)
        self.path, self.raw = _tao_repo(self.tmp.name)
        self.al = selector.nap_allowlist(self.path)

    def tearDown(self):
        self.tmp.cleanup()

    def _al_voi(self, rel, sha='0' * 64):
        al = json.loads(json.dumps(self.raw))
        al['cases'][0]['files']['metrics.parquet'].update(path=rel, sha256=sha)
        p = Path(self.tmp.name) / 'al2.json'
        p.write_text(json.dumps(al), encoding='utf-8')
        return selector.nap_allowlist(p)

    def test_hop_le(self):
        out = selector.chon_ca(self.al, 'dev-0123456789', self.tmp.name)
        self.assertTrue(out['metrics.parquet'].endswith('metrics.parquet'))

    def test_ma_sai_dang(self):
        for bad in ['dev-012345678', 'DEV-0123456789', 'dev-012345678g', '../dev-0123456789', None, 7]:
            with self.assertRaises(selector.LoiRunner):
                selector.chon_ca(self.al, bad, self.tmp.name)

    def test_ngoai_allowlist(self):
        with self.assertRaises(selector.LoiRunner):
            selector.chon_ca(self.al, 'dev-aaaaaaaaaa', self.tmp.name)

    def test_locked_traversal_tuyet_doi(self):
        for rel in ['data/locked/caY/metrics.parquet', 'data/rcaeval/../locked/caY/metrics.parquet',
                    'data/rcaeval/./caX/metrics.parquet', '/data/rcaeval/caX/metrics.parquet',
                    'C:/x/metrics.parquet', 'data\\rcaeval\\caX\\metrics.parquet', 'other/caX/metrics.parquet',
                    'DATA/LOCKED/caY/metrics.parquet']:
            al = self._al_voi(rel)
            with self.assertRaises(selector.LoiRunner, msg=rel):
                selector.chon_ca(al, 'dev-0123456789', self.tmp.name)

    def test_hash_sai(self):
        al = self._al_voi('data/rcaeval/caX/metrics.parquet', sha='f' * 64)
        with self.assertRaises(selector.LoiRunner):
            selector.chon_ca(al, 'dev-0123456789', self.tmp.name)

    def test_allowlist_trung_ma(self):
        al = json.loads(json.dumps(self.raw))
        al['cases'].append(al['cases'][0]); al['so_ca'] = 2
        p = Path(self.tmp.name) / 'al3.json'; p.write_text(json.dumps(al), encoding='utf-8')
        with self.assertRaises(selector.LoiRunner):
            selector.nap_allowlist(p)


T = 1_000_000_000  # mốc tổng hợp (giây)


class CatCuaSo(unittest.TestCase):
    def test_metric_bien(self):
        m = pd.DataFrame({'time': np.arange(T - 400, T + 400), 'a_cpu': 1.0})
        w = cua_so.cat_metric(m, T)
        self.assertEqual(w['time'].min(), T - 300)
        self.assertEqual(w['time'].max(), T + 299)
        self.assertEqual(len(w), 600)

    def test_span_bien(self):
        us = cua_so.US
        rows = [
            ('vao_dau', (T - 300) * us, 10),            # bắt đầu đúng t-300: vào
            ('truoc', (T - 300) * us - 1, 10),          # bắt đầu trước t-300: bỏ, dù kết thúc trong cửa sổ
            ('ket_thuc_sat', (T + 299) * us, us - 1),   # kết thúc t+300-1µs: vào
            ('ket_thuc_dung', (T + 299) * us, us),      # kết thúc đúng t+300: bỏ
            ('vuot', (T + 200) * us, 200 * us),         # bắt đầu trong cửa sổ, kết thúc sau t+300: bỏ
            ('A', T * us, 5),                           # đầu A
        ]
        tr = pd.DataFrame(rows, columns=['spanID', 'startTime', 'duration'])
        w = cua_so.cat_span(tr, T)
        self.assertEqual(sorted(w['spanID']), sorted(['vao_dau', 'ket_thuc_sat', 'A']))

    def test_log_bien(self):
        lg = pd.DataFrame({'timestamp': [T - 301, T - 300, T - 1, T, T + 299, T + 300], 'container_name': 's', 'message': 'x'})
        w = cua_so.cat_log(lg, T)
        self.assertEqual(w['timestamp'].tolist(), [T - 300, T - 1, T, T + 299])

    def test_cat_ca_thieu_du_lieu(self):
        # file chỉ có từ T-100 tới T+50: ghi độ dài thực, không kéo dài
        m = pd.DataFrame({'time': np.arange(T - 100, T + 51), 'a_cpu': 1.0})
        d, info = cua_so.cat_ca(m, None, None, T)
        self.assertEqual((info['rows_N'], info['rows_A']), (100, 51))
        self.assertEqual((info['seconds_N'], info['seconds_A']), (100, 51))

    def test_mo_c_khong_nguyen(self):
        m = pd.DataFrame({'time': [T], 'a_cpu': [1.0]})
        with self.assertRaises(ValueError):
            cua_so.cat_metric(m, T + 0.5)

    def test_o_trong_dau_cua_so_d1(self):
        # cột a: NaN ở 2 điểm đầu cửa sổ, có giá trị 7 trước t-300.
        t = np.arange(T - 310, T + 310)
        a = np.full(len(t), np.nan); a[t < T - 300] = 7.0; a[t >= T - 298] = 1.0
        b = np.where(t % 2 == 0, np.inf, 2.0)  # inf -> NaN -> ffill trong cửa sổ, điểm đầu là inf
        m = pd.DataFrame({'time': t, 'x_a': a, 'x_b': b, 'x_latency-50': 0.0})
        w = cua_so.tien_xu_ly_main(cua_so.cat_metric(m, T))
        self.assertEqual(w['x_a'].iloc[:2].tolist(), [0.0, 0.0])   # bản này điền 0
        self.assertNotIn('x_latency-50', w)
        d1 = cua_so.dem_d1(m, T)
        # main.py: x_a 2 ô đầu nhận 7; x_b ô đầu (T-300 chẵn -> inf) nhận 2 từ T-301 thay cho 0
        self.assertEqual(d1['o_khac'], 3)
        self.assertEqual(d1['cot_co_o_khac'], 2)
        self.assertTrue(d1['cat_theo_dong_trung_cat_theo_thoi_gian'])

    def test_doi_ten(self):
        d = pd.DataFrame({'time': [1], 's_latency-90': [1.0], 's_cpu': [2.0]})
        self.assertEqual(list(cua_so.doi_ten_latency(d).columns), ['time', 's_latency', 's_cpu'])

    def test_chi_ts(self):
        d = pd.DataFrame({'time': [1, 2], 'ts-a_cpu': [1.0, 2.0], 'istio_x': [3.0, 4.0]})
        self.assertEqual(sorted(cua_so.tien_xu_ly_main(d, chi_ts=True).columns), ['time', 'ts-a_cpu'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
