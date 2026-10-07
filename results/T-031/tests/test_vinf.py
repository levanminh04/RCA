"""T-031 (Q-81, WHY-36, giao thức §6.5): test biến thể CIRCA V∞. Fixture tổng hợp của T-030, không dữ liệu thật."""
import json
import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results' / 'T-030' / 'tests')]
import fixture  # noqa: E402
from p3 import ban_ghi, cua_so, danh_gia as dg, nhan, runner, selector  # noqa: E402
from p3.adapters import circa  # noqa: E402

OUT = ROOT / 'results' / 'T-030' / 'work' / 'test-vinf-runs'
TO = 600


def _khung(hang_roi_doi):
    """Fixture T-030; thêm cột latency của ts-a-service hằng tới 1 ulp trong N rồi (tùy chọn) đổi mức trong A."""
    rng = np.random.default_rng(1)
    m = fixture.metrics(rng)
    tr = fixture.traces(rng)
    t = fixture.T_INJ
    col = 'ts-a-service_latency-90'
    v = np.where(np.arange(len(m)) % 2 == 0, 0.235, 0.23500000000000004)
    if hang_roi_doi:
        v = np.where(m['time'].to_numpy() >= t, 0.95, v)
    m[col] = v
    w, _ = cua_so.cat_ca(m, tr, None, t)
    clean = circa.chuan_bi(w['metric'])
    graph, _ = circa.do_thi([c for c in clean.columns if c != 'time'], w['traces'], t)
    return clean, graph, t, int(clean['time'].max())


class Luat(unittest.TestCase):
    def test_la_hang(self):
        self.assertTrue(circa.la_hang([0.235, 0.23500000000000004] * 50))
        self.assertTrue(circa.la_hang([3.0] * 10))
        self.assertFalse(circa.la_hang([0.235, 0.236] * 50))
        self.assertFalse(circa.la_hang(np.arange(10.0)))

    def test_luat_vinf(self):
        n = [0.235, 0.23500000000000004] * 50
        self.assertEqual(circa.luat_vinf(n, [0.95] * 10), math.inf)
        self.assertEqual(circa.luat_vinf(n, [0.235] * 10), 0.0)
        self.assertIsNone(circa.luat_vinf(np.arange(100.0), [0.95] * 10))


class Cham(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from circa_kien_truc.scoring import score_graph
        cls.goc, cls.vinf = {}, {}
        for doi in (True, False):
            clean, graph, t, cur = _khung(doi)
            cls.goc[doi] = score_graph(clean, graph, t, cur)
            cls.vinf[doi] = circa.cham(clean, graph, t, cur, 'vinf')

    def test_ban_goc_bi_phong(self):
        """Điều kiện của test: bản gốc cho điểm khổng lồ ở cột hằng-rồi-đổi (hiện tượng R1)."""
        self.assertGreater(self.goc[True]['nodes']['ts-a-service_latency']['rht_score'], 1e10)

    def test_inf_va_zero(self):
        self.assertEqual(self.vinf[True]['nodes']['ts-a-service_latency']['rht_score'], 'inf')
        self.assertEqual(self.vinf[True]['nodes']['ts-a-service_latency']['vinf'], 'inf')
        self.assertEqual(self.vinf[False]['nodes']['ts-a-service_latency']['rht_score'], 0.0)
        self.assertEqual(self.vinf[False]['nodes']['ts-a-service_latency']['vinf'], 'zero')

    def test_nut_khac_giu_diem_goc(self):
        for doi in (True, False):
            g, v = self.goc[doi]['nodes'], self.vinf[doi]['nodes']
            self.assertEqual(set(g), set(v))
            for k in g:
                if 'vinf' not in v[k]:
                    self.assertEqual(g[k]['rht_score'], v[k]['rht_score'], k)
                    self.assertEqual(g[k]['regression_route'], v[k]['regression_route'], k)

    def test_khong_doi_thi_thu_hang_rht_giu_nguyen_ngoai_nut_zero(self):
        g = [n for n, _ in self.goc[False]['ranks'] if n != 'ts-a-service_latency']
        v = [n for n, _ in self.vinf[False]['ranks'] if n != 'ts-a-service_latency']
        self.assertEqual(g, v)

    def test_da_lan_inf_len_cha(self):
        """DA gốc cộng điểm con lớn nhất vào cha (rht.py:276–281): cha có con +∞ thì +∞."""
        nodes = self.vinf[True]['nodes']
        da = {n: s for n, s, _ in self.vinf[True]['ranks_da']}
        self.assertEqual(da['ts-a-service_latency'], math.inf)
        n_cha = 0
        con_cua = {k: [c for c, v in nodes.items() if k in v['parents']] for k in nodes}
        for k, cs in con_cua.items():
            if 'ts-a-service_latency' in cs and nodes[k]['rht_score'] != 'inf' and float(nodes[k]['rht_score']) >= 3:
                self.assertEqual(da[k], math.inf, k)
                n_cha += 1
        self.assertGreater(n_cha, 0, 'fixture không có cha nào để kiểm DA')


class BanGhi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = fixture.tao_repo('tvinf', so_ca=2, seed=0, sao_y_het=True)
        cls.al = selector.nap_allowlist(cls.repo / 'allowlist.json')
        cls.ids = sorted(cls.al)
        cls.t = nhan.nap_moc(cls.repo / 'nhan.json')[cls.ids[0]]
        cls.recs = runner.chay_luot(cls.al, cls.ids[0], 'circa', 'a', cls.t, OUT, TO, repo_root=cls.repo,
                                    model='ols_vinf')
        cls.ols = runner.chay_luot(cls.al, cls.ids[0], 'circa', 'a', cls.t, OUT, TO, repo_root=cls.repo, model='ols')

    def test_bon_bien_the(self):
        self.assertEqual([r['variant'] for r in self.recs], circa.bien_the('ols_vinf'))
        self.assertEqual(circa.bien_the('ols_vinf'), ['ols+rht_da', 'ols+rht', 'ols_vinf+rht_da', 'ols_vinf+rht'])
        self.assertTrue(all(r['status'] == 'OK' for r in self.recs))

    def test_ols_trong_luot_vinf_giong_luot_ols(self):
        bo = ('run_id', 'opaque_id', 'cost', 'input_sha256')
        gon = lambda r: json.loads(json.dumps({k: v for k, v in r.items() if k not in bo}))  # noqa: E731
        self.assertEqual([gon(r) for r in self.recs[:2]], [gon(r) for r in self.ols])

    def test_chi_vinf_duoc_inf(self):
        with self.assertRaises(ValueError):
            ban_ghi.tao('circa', 'v', 'ols+rht', 'a', {'status': 'OK', 'items': [('x_a', 'x', (math.inf,))]},
                        None, 'c', [])
        r = ban_ghi.tao('circa', 'v', 'ols_vinf+rht', 'a',
                        {'status': 'OK', 'items': [('x_a', 'x', (math.inf,)), ('y_a', 'y', (1.0,))]}, None, 'c', [])
        self.assertEqual(r['ranking'][0]['key'], ['inf'])
        self.assertEqual(r['entity_ranking'][0]['key'], ['inf'])
        r2 = json.loads(json.dumps(r))
        self.assertEqual(dg.khoi_tu_ban_ghi(r2)[0]['key'], (math.inf,))
        with self.assertRaises(ValueError):
            ban_ghi.tao('circa', 'v', 'ols_vinf+rht', 'a', {'status': 'OK', 'items': [('x_a', 'x', (math.nan,))]},
                        None, 'c', [])
        r3 = dict(r2, variant='ols+rht')
        with self.assertRaises(dg.LoiBanGhi):
            dg.khoi_tu_ban_ghi(r3)

    def test_hoa_inf_cham_duoc(self):
        r = ban_ghi.tao('circa', 'v', 'ols_vinf+rht', 'a',
                        {'status': 'OK', 'items': [('x_a', 'x', (math.inf,)), ('y_a', 'y', (math.inf,)),
                                                   ('z_a', 'z', (2.0,))]}, None, 'c', [])
        c = dg.cham_ca(json.loads(json.dumps(r)), 'y')
        self.assertAlmostEqual(c['hit@1'], 0.5)

    def test_timeout_bon_bien_the(self):
        rs = runner.chay_luot(self.al, self.ids[0], 'circa', 'a', self.t, OUT, 0.5, repo_root=self.repo,
                              model='ols_vinf')
        self.assertEqual([r['variant'] for r in rs], circa.bien_the('ols_vinf'))
        self.assertTrue(all(r['status'] == 'TIMEOUT' for r in rs))


if __name__ == '__main__':
    unittest.main(verbosity=2)
