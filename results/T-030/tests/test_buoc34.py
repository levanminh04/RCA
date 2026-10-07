"""T-030 bước 3–4: runner, bản ghi, adapter trên fixture tổng hợp (§11.2, §11.6–11.8, §11.10 phần fixture).

Chạy bằng T-014-main, PYTHONPATH gồm RCAEval, baro, CIRCA. Tạo tiến trình con ở ba môi trường.
"""
import inspect
import json
import re
import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(Path(__file__).parent)]
import fixture  # noqa: E402
from p3 import ban_ghi, danh_gia as dg, nhan, runner, selector, torai_b  # noqa: E402
from p3.adapters import circa, phat_hien, torai  # noqa: E402

OUT = ROOT / 'results' / 'T-030' / 'work' / 'test34-runs'
TO = 600
BO = ('run_id', 'opaque_id', 'cost', 'input_sha256')


def gon(rec):
    r = {k: v for k, v in rec.items() if k not in BO}
    return json.loads(json.dumps(r))


class Chung(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = fixture.tao_repo('t34', so_ca=2, seed=0, sao_y_het=True)
        cls.al = selector.nap_allowlist(cls.repo / 'allowlist.json')
        cls.ids = sorted(cls.al)
        cls.t = nhan.nap_moc(cls.repo / 'nhan.json')[cls.ids[0]]
        cls.cache = {}

    def chay(self, oid, method, mode='a', t=None, **kw):
        key = (oid, method, mode, t, tuple(sorted(kw.items())))
        if key not in self.cache:
            self.cache[key] = runner.chay_luot(self.al, oid, method, mode, self.t if t is None else t, OUT, TO,
                                               repo_root=self.repo, torai_tt=self.repo / 'torai-TT', **kw)
        return self.cache[key]


class Ranker(Chung):
    def test_chay_va_khoa(self):
        for m, kw in [('baro', {}), ('simplerca', {}), ('microrank', {}), ('tracerca', {}), ('circa', {'model': 'ols'}),
                      ('circa', {'model': 'svr'}), ('torai_A', {'seed': 0}), ('torai_B', {'seed': 0})]:
            for r in self.chay(self.ids[0], m, **kw):
                with self.subTest(m=m, v=r['variant']):
                    self.assertEqual(r['status'], 'OK', r.get('error'))
                    ban_ghi.kiem(r)
                    self.assertGreater(r['sets']['observed'], 0)
                    # TraceRCA: operation không có span bất thường cho ji = NaN (support 0) → 'nan_present'
                    self.assertIn(r['diagnostics'].get('key_check', 'pass'), ('pass', 'nan_present'))
                    c = dg.cham_ca(r, 'ts-b-service')
                    self.assertTrue(c['root_trong_tra_ve'])
                    self.assertGreater(r['cost']['wall_s'], 0)
                    self.assertIsNotNone(r['window'])

    def test_doi_locator(self):
        # §11.2: hai ca cùng nội dung, khác thư mục và mã mờ → đầu ra giống hệt
        for m, kw in [('baro', {}), ('simplerca', {}), ('microrank', {}), ('tracerca', {}), ('circa', {'model': 'ols'}),
                      ('torai_B', {'seed': 0})]:
            a = [gon(r) for r in self.chay(self.ids[0], m, **kw)]
            b = [gon(r) for r in self.chay(self.ids[1], m, **kw)]
            with self.subTest(m=m):
                self.assertEqual(a, b)

    def test_lap_lai_torai_seed(self):
        a = gon(self.chay(self.ids[0], 'torai_B', seed=0)[0])
        b = gon(runner.chay_luot(self.al, self.ids[0], 'torai_B', 'a', self.t, OUT, TO, repo_root=self.repo,
                                 torai_tt=self.repo / 'torai-TT', seed=0)[0])
        self.assertEqual(a, b)

    def test_lech_luoi_A(self):
        r = self.chay(self.ids[0], 'torai_A', seed=0)[0]
        # lưới giả bắt đầu ở đầu file + 10 s; mốc ở giây 720 → bin đầu A bắt đầu ở giây 730 = t+10
        self.assertEqual(r['extra']['chuan_bi']['lech_luoi_s'], 10)

    def test_circa_route_va_current(self):
        for r in self.chay(self.ids[0], 'circa', model='svr'):
            self.assertEqual(r['window']['circa_current'], self.t + 299)
            self.assertNotIn('value_error_fallback', r['diagnostics']['regression_routes'])

    def test_timeout(self):
        r = runner.chay_luot(self.al, self.ids[0], 'baro', 'a', self.t, OUT, 0.5, repo_root=self.repo)[0]
        self.assertEqual(r['status'], 'TIMEOUT')
        self.assertEqual(dg.cham_ca(r, 'ts-b-service')['hit@1'], 0.0)

    def test_timeout_bien_the(self):
        for m, kw, want in (('microrank', {}, ['full']), ('circa', {'model': 'ols'}, ['ols+rht_da', 'ols+rht']),
                            ('circa', {'model': 'svr'}, ['svr+rht_da', 'svr+rht'])):
            rs = runner.chay_luot(self.al, self.ids[0], m, 'a', self.t, OUT, 0.5, repo_root=self.repo, **kw)
            self.assertEqual([r['variant'] for r in rs], want)
            self.assertTrue(all(r['status'] == 'TIMEOUT' for r in rs))

    def test_circa_route_tung_nut(self):
        for r in self.chay(self.ids[0], 'circa', model='ols'):
            nodes = r['diagnostics']['nodes']
            self.assertEqual(len(nodes), sum(r['diagnostics']['regression_routes'].values()))
            for v in nodes.values():
                self.assertIn('regression_route', v); self.assertIn('regression_error', v)

    def test_che_do_b_bien_file(self):
        t_hat = fixture.T0 + 1300  # A chỉ còn 141 s tới cuối file
        r = self.chay(self.ids[0], 'baro', mode='b', t=t_hat, detector='nsigma')[0]
        self.assertEqual(r['window']['seconds_A'], 141)
        self.assertEqual(r['window']['rows_A'], 141)
        self.assertEqual(r['mode'], 'b')


class HoanVi(Chung):
    """§11.10 trên fixture: thứ hạng thực thể bất biến ngoài nhóm hòa."""

    def _hoan_vi_repo(self, kieu):
        repo = fixture.tao_repo('t34-' + kieu, so_ca=1, seed=0)
        d = next((repo / 'data' / 'rcaeval').iterdir())
        if kieu == 'dong':
            tr = pd.read_parquet(d / 'traces.parquet').sample(frac=1.0, random_state=3)
            tr.to_parquet(d / 'traces.parquet', index=False)
        else:
            m = pd.read_parquet(d / 'metrics.parquet')
            m[['time'] + [c for c in reversed(m.columns) if c != 'time']].to_parquet(d / 'metrics.parquet', index=False)
        al = json.loads((repo / 'allowlist.json').read_text(encoding='utf-8'))
        for f in al['cases'][0]['files'].values():
            f['sha256'] = selector.sha256_file(repo / f['path'])
        (repo / 'allowlist.json').write_text(json.dumps(al), encoding='utf-8')
        return repo, selector.nap_allowlist(repo / 'allowlist.json')

    def _xep(self, r):
        return [[e['entity'] for e in r['entity_ranking'] if e['tie_group'] == g]
                for g in sorted({e['tie_group'] for e in r['entity_ranking']})]

    def _so(self, a, b):
        self.assertEqual([sorted(g) for g in self._xep(a)], [sorted(g) for g in self._xep(b)])

    def test_hoan_vi_dong_span(self):
        repo, al = self._hoan_vi_repo('dong')
        oid = sorted(al)[0]
        for m in ('microrank', 'tracerca'):
            with self.subTest(m=m):
                a = self.chay(self.ids[0], m)[0]
                b = runner.chay_luot(al, oid, m, 'a', self.t, OUT, TO, repo_root=repo)[0]
                self._so(a, b)

    def test_hoan_vi_cot_metric(self):
        repo, al = self._hoan_vi_repo('cot')
        oid = sorted(al)[0]
        for m, kw in [('baro', {}), ('simplerca', {}), ('circa', {'model': 'ols'})]:
            for a, b in zip(self.chay(self.ids[0], m, **kw),
                            runner.chay_luot(al, oid, m, 'a', self.t, OUT, TO, repo_root=repo, **kw)):
                with self.subTest(m=m, v=a['variant']):
                    self._so(a, b)


class CircaSvrBanSao(unittest.TestCase):
    def test_ols_qua_duong_svr_bang_score_graph(self):
        from sklearn.linear_model import LinearRegression
        from circa_kien_truc.scoring import score_graph
        rng = np.random.default_rng(1)
        m = fixture.metrics(rng)
        tr = fixture.traces(rng)
        from p3 import cua_so
        t = fixture.T_INJ
        w, _ = cua_so.cat_ca(m, tr, None, t)
        clean = circa.chuan_bi(w['metric'])
        graph, _ = circa.do_thi([c for c in clean.columns if c != 'time'], w['traces'], t)
        cur = int(clean['time'].max())
        a = score_graph(clean, graph, t, cur)
        b = circa.cham_svr(clean, graph, t, cur, tao_hoi_quy=LinearRegression, ten_route='linear_regression')
        self.assertEqual(a['ranks'], b['ranks'])
        self.assertEqual(a['ranks_da'], b['ranks_da'])
        self.assertEqual({k: v['regression_route'] for k, v in a['nodes'].items()},
                         {k: v['regression_route'] for k, v in b['nodes'].items()})


class PhatHien(Chung):
    def test_diem_doi_tu_R(self):
        # R (T+1)x(T+1), T = 5. argmax cột 1..5 = [0, 1, 2, 0, 1] → m; |Δ| > 1 ở i=3 (2→0)
        T = 5
        R = np.zeros((T + 1, T + 1))
        for i, a in enumerate([0, 1, 2, 0, 1]):
            R[a, i + 1] = 1.0
        cps, m = phat_hien.diem_doi_tu_R(R)
        self.assertEqual(list(m), [0, 1, 2, 0, 1])
        self.assertEqual(cps, [3])
        self.assertTrue(all(c < T for c in cps))  # không sentinel ở cuối
        R[:, 4] = np.nan
        cps, bad = phat_hien.diem_doi_tu_R(R)
        self.assertIsNone(cps)
        self.assertEqual(bad, 4)

    def test_bocpd_chuoi_nho(self):
        rng = np.random.default_rng(0)
        T = 120
        t = np.arange(fixture.T0, fixture.T0 + T)
        x = np.r_[rng.normal(0, 0.05, 60), rng.normal(1, 0.05, 60)]
        m = pd.DataFrame({'time': t, 'ts-a_latency-50': x, 'ts-b_error': rng.normal(0, 0.05, T),
                          'ts-a_cpu': rng.normal(0, 1, T), 'rabbitmq_x_error': x})
        r = phat_hien.bocpd(m)
        self.assertEqual(r['detector_columns'], ['ts-a_latency-50', 'ts-b_error'])
        self.assertEqual(r['status'], 'OK')
        self.assertTrue(all(fixture.T0 + 1 <= a < fixture.T0 + T for a in r['alarms']))
        self.assertTrue(any(abs(a - (fixture.T0 + 60)) <= 3 for a in r['alarms']), r['alarms'])

    def test_nsigma_khoi_dong_va_bo_trung(self):
        T = 300
        t = np.arange(fixture.T0, fixture.T0 + T)
        base = np.tile([0.0, 1.0], T // 2)
        a, b = base.copy(), base.copy()
        a[50] = b[50] = 100.0     # trước startsfrom: không đánh giá
        a[150] = b[150] = 100.0   # hai cột cùng lúc: một báo động sau bỏ trùng
        a[200] = np.inf           # inf → NaN → ffill
        m = pd.DataFrame({'time': t, 'ts-a_latency-50': a, 'ts-b_error': b})
        r = phat_hien.nsigma(m)
        self.assertEqual(r['alarms'], [fixture.T0 + 150])

    def test_luot_rca(self):
        r = phat_hien.luot_rca([10, 20, 309, 310, 700])
        self.assertEqual((r['t_hat'], r['thong_bao']), (10, [10, 310, 700]))

    def test_khong_nhan_vao_bo_phat_hien(self):
        # §11.8: hàm bộ phát hiện chỉ nhận bảng metric; job không có mốc, nhãn, đường dẫn ngoài file dữ liệu
        self.assertEqual(list(inspect.signature(phat_hien.bocpd).parameters), ['metrics'])
        self.assertEqual(list(inspect.signature(phat_hien.nsigma).parameters), ['metrics', 'tap_cot'])
        r1 = self.chay(self.ids[0], 'nsigma', mode='b', t=None)[0]
        job = json.loads((OUT / r1['run_id'] / 'job.json').read_text(encoding='utf-8'))
        self.assertNotIn('t', job)
        self.assertEqual(set(job), {'kind', 'method', 'files', 'tap_cot'})
        # đổi nhãn/mốc phía evaluator: báo động không đổi, chỉ điểm chấm đổi
        s1 = dg.cham_phat_hien(r1['times'], r1['alarms'], fixture.T_INJ, r1['bat_dau_danh_gia'])
        s2 = dg.cham_phat_hien(r1['times'], r1['alarms'], fixture.T_INJ + 120, r1['bat_dau_danh_gia'])
        self.assertEqual(s1['bao_dong_dau'], s2['bao_dong_dau'])
        r2 = runner.chay_luot(self.al, self.ids[0], 'nsigma', 'b', 12345, OUT, TO, repo_root=self.repo)[0]
        self.assertEqual(r1['alarms'], r2['alarms'])


class TraceRCAKhongNaN(unittest.TestCase):
    def test_khoa_khop_chinh_thuc(self):
        from p3.adapters import tracerca
        rng = np.random.default_rng(0)
        t = fixture.T0 + 100
        rows = []
        for i in range(400):
            sec = fixture.T0 + i // 2
            for op, svc in (('opA', 'ts-a-service'), ('opB', 'ts-b-service'), ('opC', 'ts-c-service')):
                d = int(rng.normal(1000, 10))
                if sec >= t and i % (3 if op == 'opA' else 5 if op == 'opB' else 7) == 0:
                    d = 5000
                rows.append((f'{i}{op}', f'{i}{op}s', svc, None, op, None, sec * 1_000_000, d))
        sp = pd.DataFrame(rows, columns=['traceID', 'spanID', 'serviceName', 'methodName', 'operationName',
                                         'parentSpanID', 'startTime', 'duration'])
        r = tracerca.chay(sp, t)
        self.assertEqual(r['diagnostics']['key_check'], 'pass')
        self.assertEqual(r['ranking_native'], r['extra']['ranks_chinh_thuc'])
        self.assertEqual(r['ranking_native'][0], 'ts-a-service_opA')


class RoNhan(unittest.TestCase):
    def test_khong_doc_nhan_ngoai_runner(self):
        src = ROOT / 'src' / 'p3'
        for f in src.rglob('*.py'):
            s = f.read_text(encoding='utf-8')
            if f.name in ('nhan.py',):
                continue
            with self.subTest(f=f.name):
                self.assertNotIn('nhan-dev', s)
                if f.parent.name == 'adapters' or f.name in ('worker.py', 'cua_so.py', 'torai_b.py', 'ban_ghi.py'):
                    self.assertIsNone(re.search(r'\bnhan\b\s*(import|\.)|from \.\.? import .*\bnhan\b', s))

    def test_ban_ghi_cam_truong_nhan(self):
        with self.assertRaises(ValueError):
            ban_ghi.tao('m', 'v', 'x', 'a', {'status': 'OK', 'items': [('a_cpu', 'a', (1.0,))], 'extra': {'root': 'a'}},
                        {}, 'c', [])


class TenCotTT(unittest.TestCase):
    def test_chuan_hoa(self):
        # luật §6.6 bỏ '/api/v1/' nhưng giữ phương thức HTTP đứng trước
        self.assertEqual(torai_b.chuan_hoa_op('POST /api/v1/aservice/do'), 'POST-aservice-do')
        self.assertEqual(torai_b.chuan_hoa_op('GET /api/v1/cservice/x/{id}'), 'GET-cservice-x-id')
        self.assertEqual(torai_b.chuan_hoa_op('/api/v1/a_b//c '), 'a-b-c')
        self.assertEqual(torai_b.chuan_hoa_op('calc_value'), 'calc-value')
        self.assertEqual(torai_b.chuan_hoa_op('find ts-b-mongo.x'), 'find-ts-b-mongo.x')

    def test_span_http_lay_service_con(self):
        tr = pd.DataFrame({'traceID': ['t'] * 4, 'spanID': ['1', '2', '3', '4'], 'parentSpanID': [None, '1', None, '3'],
                           'serviceName': ['ui', 'a', 'ui', 'ui'], 'operationName': ['GET', 'POST /api/v1/x', 'PUT', 'q'],
                           'startTime': [1, 2, 3, 4]})
        cot, nhieu = torai_b.ten_cot(tr)
        self.assertEqual(list(cot), ['a_GET', 'a_POST-x', 'ui_PUT', 'ui_q'])
        self.assertEqual(nhieu, 0)

    def test_so_theo_ten_cot(self):
        idx = pd.Index([0, 15], name='time')
        mau = pd.DataFrame({'x': [1.0, np.nan], 'y': [2.0, 2.0]}, index=idx)
        mine = pd.DataFrame({'x': [1.0, 0.0], 'z': [5.0, 5.0]}, index=idx)
        r = torai_b.so_theo_ten_cot(mine, mau)
        self.assertEqual((r['so_o'], r['o_trung']), (6, 2))  # x: 2 ô trùng (NaN coi 0); y, z: 4 ô sai


class ToraiANRong(unittest.TestCase):
    """REVIEW T-030 R3: chế độ (b), báo động đầu trước bin đầu file tác giả → nửa N rỗng."""

    def test_n_rong(self):
        g = pd.DataFrame({'time': range(10, 300, 15), 'x': 0})  # lưới 15 s lệch 10 s như fixture
        m = pd.DataFrame({'time': range(0, 300)})
        for t in (3, 10):
            info = torai.chuan_bi_A(m, g, g, g, t)[-1]
            self.assertIsNone(info['N_phu'])
            self.assertEqual(info['A_phu'], [10, 310])
        info = torai.chuan_bi_A(m, g, g, g, 11)[-1]
        self.assertEqual((info['N_phu'], info['A_phu']), ([10, 25], [25, 310]))


if __name__ == '__main__':
    unittest.main(verbosity=2)
