"""T-030 bước 2: evaluator (§11.4, §11.5, §7.4–7.5). Đáp án tính tay hoặc liệt kê vét cạn độc lập."""
import itertools
import math
import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from p3 import danh_gia as dg  # noqa: E402


def rec_tu_nhom(nhom, status='OK'):
    """nhom: danh sách (khóa, [thực thể]) theo thứ tự giảm dần."""
    er = []
    for i, (k, ents) in enumerate(nhom):
        for e in ents:
            er.append({'entity': e, 'key': [k], 'tie_group': i})
    return {'status': status, 'entity_ranking': er,
            'ranking_native': [f'{e}_m' for _, ents in nhom for e in ents],
            'sets': {'observed_entities': [e for _, ents in nhom for e in ents]}}


def vet_can(blocks, root):
    """Phân bố hạng bằng liệt kê mọi hoán vị hợp lệ (độc lập với DP)."""
    sgs, i = [], 0
    while i < len(blocks):
        j = i
        while j + 1 < len(blocks) and blocks[j + 1]['key'] == blocks[i]['key']:
            j += 1
        sgs.append(blocks[i:j + 1]); i = j + 1
    choices = []
    for sg in sgs:
        opts = []
        for perm in itertools.permutations(range(len(sg))):
            inner_opts = [list(itertools.product(*[list(itertools.permutations(g)) for g in sg[b]['groups']]))
                          for b in perm]
            for combo in itertools.product(*inner_opts):
                opts.append([e for blk in combo for g in blk for e in g])
        choices.append(opts)
    dist, total = {}, 0
    for combo in itertools.product(*choices):
        order = [e for part in combo for e in part]
        total += 1
        if root in order:
            r = order.index(root) + 1
            dist[r] = dist.get(r, 0) + 1
    return {r: Fraction(c, total) for r, c in dist.items()}


class HangVaHoa(unittest.TestCase):
    def test_khong_hoa(self):
        r = dg.cham_ca(rec_tu_nhom([(9, ['a']), (8, ['b']), (7, ['c'])]), 'c')
        self.assertEqual((r['hit@1'], r['hit@3']), (0.0, 1.0))
        self.assertAlmostEqual(r['rr'], 1 / 3)
        self.assertAlmostEqual(r['ndcg@5'], 1 / math.log2(4))
        self.assertAlmostEqual(r['avg@5'], 3 / 5)

    def test_nhom_hoa(self):
        r = dg.cham_ca(rec_tu_nhom([(9, ['a']), (5, ['b', 'c', 'd']), (1, ['e'])]), 'c')
        self.assertAlmostEqual(r['hit@3'], 2 / 3)
        self.assertAlmostEqual(r['hit@1'], 0.0)
        self.assertAlmostEqual(r['rr'], (1 / 2 + 1 / 3 + 1 / 4) / 3)
        self.assertEqual((r['rank_min'], r['rank_max']), (2, 4))
        self.assertEqual(r['opt']['hit@3'], 1.0)
        self.assertEqual(r['pes']['hit@3'], 0.0)

    def test_hoa_dau_va_cuoi(self):
        r = dg.cham_ca(rec_tu_nhom([(5, ['x', 'y'])]), 'x')
        self.assertAlmostEqual(r['hit@1'], 0.5)
        r = dg.cham_ca(rec_tu_nhom([(5, ['a']), (1, ['x', 'y', 'z', 'w', 'v', 'u'])]), 'x')
        self.assertAlmostEqual(r['hit@5'], 4 / 6)
        self.assertAlmostEqual(r['hit@10'], 1.0)

    def test_root_vang_danh_sach_ngan(self):
        r = dg.cham_ca(rec_tu_nhom([(1, ['a'])]), 'z')
        self.assertTrue(all(r[f'hit@{k}'] == 0 for k in range(1, 11)))
        self.assertEqual(r['rr'], 0.0)
        self.assertFalse(r['root_trong_tra_ve'])

    def test_trang_thai(self):
        for s in ('NO_EVIDENCE', 'ERROR', 'TIMEOUT', 'UNSUPPORTED'):
            r = dg.cham_ca({'status': s}, 'a')
            self.assertEqual(r['hit@1'], 0.0)
            self.assertEqual(r['status'], s)
        with self.assertRaises(dg.LoiBanGhi):
            dg.cham_ca({'status': 'LA'}, 'a')
        t = dg.tong_hop({'1': dg.cham_ca(rec_tu_nhom([(1, ['a'])]), 'a'), '2': dg.cham_ca({'status': 'ERROR'}, 'a')})
        self.assertEqual(t['hit@1'], 0.5)  # ca lỗi ở mẫu số
        self.assertEqual(t['trang_thai']['ERROR'], 1)

    def test_trung_thuc_the_khong_huu_han(self):
        with self.assertRaises(dg.LoiBanGhi):
            dg.cham_ca(rec_tu_nhom([(2, ['a']), (1, ['a'])]), 'a')
        with self.assertRaises(dg.LoiBanGhi):
            dg.cham_ca(rec_tu_nhom([(float('nan'), ['a'])]), 'a')
        with self.assertRaises(dg.LoiBanGhi):
            dg.cham_ca(rec_tu_nhom([(1, ['a']), (2, ['b'])]), 'a')  # không giảm dần

    def test_khoa_tuple(self):
        # CIRCA DA: cùng score khác index -> không hòa
        rec = {'status': 'OK', 'entity_ranking': [
            {'entity': 'a', 'key': [5.0, -1.0, 2.0], 'tie_group': 0},
            {'entity': 'b', 'key': [5.0, -2.0, 9.0], 'tie_group': 1}]}
        self.assertEqual(dg.cham_ca(rec, 'a')['hit@1'], 1.0)

    def test_torai_hai_khoi(self):
        rec = {'status': 'OK', 'blocks': [{'key': [0.5], 'groups': [['A'], ['B']]},
                                          {'key': [0.5], 'groups': [['C'], ['D']]}]}
        r = dg.cham_ca(rec, 'A')
        self.assertAlmostEqual(r['rr'], 2 / 3)
        self.assertAlmostEqual(r['hit@1'], 1 / 2)

    def test_dp_khop_vet_can(self):
        rnd = random.Random(7)
        n_cmp = 0
        for _ in range(300):
            blocks, name = [], 0
            key = 10
            for _b in range(rnd.randint(1, 5)):
                if rnd.random() < 0.5:
                    key -= 1
                groups = []
                for _g in range(rnd.randint(1, 2)):
                    groups.append([f'e{name + i}' for i in range(rnd.randint(1, 2))]); name += len(groups[-1])
                blocks.append({'key': (float(key),), 'groups': groups})
            ents = [e for b in blocks for g in b['groups'] for e in g]
            for root in ents + ['khong_co']:
                self.assertEqual(dg.phan_bo_hang(blocks, root), vet_can(blocks, root))
                n_cmp += 1
        self.assertGreater(n_cmp, 1000)

    def test_rerank_khong_don_dieu(self):
        a = dg.cham_ca(rec_tu_nhom([(9, ['r'])]), 'r')
        b = dg.cham_ca(rec_tu_nhom([(9, ['a', 'b', 'c', 'd'])] + [(5, ['r', 'x'])]), 'r')
        t = dg.tong_hop({'1': a, '2': b})
        self.assertAlmostEqual(t['rerank@1(K=5)'], 2 / 3)

    def test_doi_chieu_rcaeval_khong_hoa(self):
        rnd = random.Random(3)
        recs, nhan, per = {}, {}, {}
        ents = [f'ts-s{i}' for i in range(15)]
        for c in range(40):
            order = ents[:]; rnd.shuffle(order); order = order[:rnd.randint(3, 15)]
            rec = rec_tu_nhom([(100 - i, [e]) for i, e in enumerate(order)])
            if c % 9 == 0:
                rec['status'] = 'ERROR'
            root = rnd.choice(ents)
            oid = f'c{c}'
            recs[oid], nhan[oid] = rec, {'root': root}
            per[oid] = dg.cham_ca(rec, root)
        ours = dg.tong_hop(per)
        theirs = dg.bang_rcaeval(recs, nhan)
        for k in (1, 3, 5):
            self.assertAlmostEqual(ours[f'hit@{k}'], theirs[f'AC@{k}'])
        self.assertAlmostEqual(ours['avg@5'], theirs['Avg@5'])
        for K in (5, 10):
            self.assertAlmostEqual(ours[f'retrieval@{K}'], theirs[f'retrieval_service({K})'])
            self.assertAlmostEqual(ours[f'rerank@1(K={K})'], theirs[f'rerank_service(1,{K})'])


class NgauNhien(unittest.TestCase):
    def test_ky_vong_hit(self):
        O = [f'e{i}' for i in range(13)]
        rec = {'sets': {'observed_entities': O}}
        U = O + [f'u{i}' for i in range(55)]
        for k in (1, 3, 5, 10):
            want = dg.muc_ngau_nhien(rec, 'e4', U)[f'O_hit@{k}']
            self.assertAlmostEqual(want, min(k, 13) / 13)
            hits = []
            for seed in range(4000):
                o = O[:]; random.Random(seed).shuffle(o)
                hits.append(o.index('e4') < k)
            m, se = np.mean(hits), np.std(hits, ddof=1) / math.sqrt(len(hits))
            self.assertLess(abs(m - want), 4 * se + 1e-12)
        self.assertEqual(dg.muc_ngau_nhien(rec, 'u1', U)['O_hit@5'], 0.0)
        self.assertAlmostEqual(dg.muc_ngau_nhien(rec, 'u1', U)['U_hit@5'], 5 / 68)


class Bootstrap(unittest.TestCase):
    def setUp(self):
        self.o_cua = {f'c{i}': f'o{i // 3}' for i in range(30)}
        rnd = random.Random(1)
        self.bang = {}
        for m in ('m1', 'm2'):
            self.bang[m] = {}
            for oid in self.o_cua:
                rank = rnd.randint(1, 8)
                self.bang[m][oid] = dg.cham_ca(rec_tu_nhom([(100 - i, [f'x{i}']) for i in range(8)]), f'x{rank - 1}')

    def test_tat_dinh_va_ghep_cap(self):
        a = dg.bootstrap(self.bang, self.o_cua, B=500)
        b = dg.bootstrap(self.bang, self.o_cua, B=500)
        self.assertEqual(a, b)
        bang = {'m1': self.bang['m1'], 'm1b': self.bang['m1']}
        d = dg.bootstrap(bang, self.o_cua, B=500)['hieu']['m1 - m1b']['hit@1']
        self.assertEqual((d['lo'], d['hi']), (0.0, 0.0))

    def test_gia_tri_hang(self):
        bang = {'m': {o: dg.cham_ca(rec_tu_nhom([(1, ['a'])]), 'a') for o in self.o_cua}}
        k = dg.bootstrap(bang, self.o_cua, B=200)['phuong_phap']['m']['hit@1']
        self.assertEqual((k['lo'], k['hi']), (1.0, 1.0))

    def test_rerank_na(self):
        bang = {'m': {o: dg.cham_ca({'status': 'ERROR'}, 'a') for o in self.o_cua}}
        k = dg.bootstrap(bang, self.o_cua, B=100)['phuong_phap']['m']['rerank@1(K=5)']
        self.assertEqual(k['n_na'], 100)


class PhatHien(unittest.TestCase):
    def setUp(self):
        self.t0 = 1_000_000_000
        self.times = np.arange(self.t0, self.t0 + 1441)
        self.t_inj = self.t0 + 720

    def test_nsigma(self):
        with self.assertRaises(dg.LoiBanGhi):
            dg.cham_phat_hien(self.times, [self.t0 + 50], self.t_inj, 100)
        al = [self.t0 + 130, self.t0 + 700, self.t0 + 730, self.t0 + 731, self.t0 + 1300]
        r = dg.cham_phat_hien(self.times, al, self.t_inj, 100)
        # cửa sổ 60 s: 0,1 bỏ (chưa đánh giá đủ); 24 bỏ (1 điểm). Còn 2..23: 22 cửa sổ.
        c = r['cua_so']
        self.assertEqual(c['bo'], 3)
        self.assertEqual(c['tp'] + c['fp'] + c['fn'] + c['tn'], 22)
        self.assertEqual((c['tp'], c['fp']), (2, 2))  # [720,780) và [1260,1320); [120,180) và [660,720)
        self.assertEqual(r['bao_dong_sai'], 2)       # +130, +700
        self.assertEqual(r['giay_binh_thuong_danh_gia'], 620)
        self.assertEqual(r['do_tre_s'], 10)
        self.assertTrue(r['phat_hien_ca'])

    def test_bocpd_mau_so(self):
        r = dg.cham_phat_hien(self.times, [], self.t_inj, 1)
        self.assertEqual(r['giay_binh_thuong_danh_gia'], 719)
        self.assertEqual(r['cua_so']['bo'], 2)
        self.assertIsNone(r['do_tre_s'])

    def test_thanh_cong_chung(self):
        rec = rec_tu_nhom([(2, ['r']), (1, ['x'])])
        self.assertEqual(dg.thanh_cong_chung(self.t_inj - 1, self.t_inj, rec, 'r', 1), 0.0)
        self.assertEqual(dg.thanh_cong_chung(self.t_inj + 5, self.t_inj, rec, 'r', 1), 1.0)
        self.assertEqual(dg.thanh_cong_chung(None, self.t_inj, rec, 'r', 1), 0.0)


class Audit(unittest.TestCase):
    def test_cot_vang(self):
        a = dg.audit_cot({'1': ['a', 'b'], '2': ['a']})
        self.assertEqual(a['hop'], 2)
        self.assertEqual(a['ca']['2']['vang'], ['b'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
