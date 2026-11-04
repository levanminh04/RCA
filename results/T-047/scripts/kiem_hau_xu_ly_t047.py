"""Kiểm hậu xử lý từ dữ kiện/đại lượng độc lập; không chạy lại phương pháp."""
import hashlib
import json
from fractions import Fraction

import adapter_t047 as ad
from m1_danh_gia.pha2 import giai_ma_json as dec


def read(p):
    return dec(json.loads(p.read_text(encoding='utf-8')))


def main():
    audit = ad.OUT / 'runs/c1-kiem-hau-xu-ly-001'
    audit.mkdir(exist_ok=False)
    main_result = read(ad.OUT / 'khoi-k.json')
    boot = read(ad.OUT / 'do-ben.json')
    ce = read(ad.OUT / 'khoi-k/ce.json')
    table = read(ad.OUT / 'so-sanh-t045.json')
    core = ('h', 'cap', 'chon_khoi', 'buoc8')
    checks = dict(bootstrap_base_equals_main=all(boot['mau_goc'][k] == main_result[k] for k in core),
                  bootstrap_n_and_seed=boot['n'] == 1000 and boot['seed'] == 20261102,
                  bootstrap_counts_complete=sum(boot['loai'].values()) == 1000,
                  bootstrap_wins_plus_stops=sum(boot['tan_suat_thang'].values()) +
                      sum(v for k,v in boot['loai'].items() if k != 'chon') == 1000,
                  main_h_exact=main_result['h'] == Fraction(1),
                  main_has_graph=bool(set(main_result['chon_khoi']['P']['chon'].split('+')) & {'E1','E2','E5'}),
                  main_no_stop=main_result['STOP'] is None,
                  sensitivity_levels=set(main_result['do_nhay_muc_HAI']) == {'1','1/2','2'},
                  sensitivity_h1_equals_main=all(main_result['do_nhay_muc_HAI']['1'][k] == main_result[k] for k in core),
                  pairs_43=len(main_result['cap']) == 43,
                  matrix16=set(table['cau_hinh']) == set(main_result['cau_hinh']) and len(table['cau_hinh']) == 16)
    ce_checks = {}
    for pair, value in main_result['cap'].items():
        off,on = ['K-' + x for x in pair.split('|')]
        ids = sorted(set(ce[off]) & set(ce[on]))
        valid = [o for o in ids if 'INSUFFICIENT_EVIDENCE' not in (ce[off][o]['verdict'],ce[on][o]['verdict'])]
        n1 = lambda r: sum(t == 1 for t in r['extra']['tang_P'].values())
        delta = Fraction(sum(n1(ce[on][o])-n1(ce[off][o]) for o in valid),len(valid)) if valid else None
        ve = 'CHUA_KIEM_DUOC' if not valid else 'HAI' if delta > 1 else 'KHONG_KICH_HOAT'
        ce_checks[pair] = all(value['theo_the_gioi'][w]['moc_gia']['tang'] == delta and
                             value['theo_the_gioi'][w]['moc_gia']['n'] == len(valid) and
                             value['theo_the_gioi'][w]['moc_gia']['ve'] == ve for w in ('P','S_lo','S_hi'))
    checks['all_43_N1_recomputed_direct_from_tiers'] = all(ce_checks.values())
    table_checks = {}
    for cid,t in table['cau_hinh'].items():
        m = main_result['cau_hinh'][cid]
        ok = t['so_ca'] == 52 and t['MRR']['G3D1_S1'] == m['MRR_phan_so']['P']
        for cell,values in t['MRR'].items():
            for ds,v in values.items():
                ids = [o for o,c in t['ca'].items() if ds == 'gop' or c['dataset'] == ds]
                ok &= v == sum((t['ca'][o]['RR'][cell] for o in ids),Fraction(0)) / len(ids)
        for ds in t['MRR']['G3D1_S1']:
            interaction = (t['MRR']['G3D1_S1'][ds]-t['MRR']['G3D1_S0'][ds]) - (t['MRR']['G0D0_S1'][ds]-t['MRR']['G0D0_S0'][ds])
            ok &= interaction == t['chenh_MRR']['tuong_tac'][ds]
        table_checks[cid] = bool(ok)
    checks['table_all_case_means_and_main_and_interactions'] = all(table_checks.values())
    sample_path = ad.ROOT / boot['tep_mau']
    with sample_path.open(encoding='utf-8') as f:
        rows = [json.loads(x) for x in f if x.strip()]
    checks['all_1000_samples_preserved_and_indexed'] = [r['i'] for r in rows] == list(range(1000))
    weights_ok = all(all(type(v) is int and v >= 0 for v in r['trong_so'].values()) and len(r['trong_so']) == 52 for r in rows)
    checks['all_sample_case_weights_nonnegative_integer'] = weights_ok
    d2 = read(ad.OUT / 'tai-lap-baseline.json')
    checks['D2_12_exact_reproductions'] = d2['dat'] and d2['tong_hop']['so_phuong_phap'] == 12 and d2['tong_hop']['MRR_khop_G2'] == d2['tong_hop']['MRR_khop_KS16'] == 12
    source_files = ['khoi-k.json','do-ben.json','so-sanh-t045.json','tai-lap-baseline.json']
    result = dict(PASS=all(checks.values()),checks=checks,Ce_pairs=ce_checks,table_configs=table_checks,
                  sample_file=boot['tep_mau'],sample_sha256=hashlib.sha256(sample_path.read_bytes()).hexdigest(),
                  sources={n:hashlib.sha256((ad.OUT/n).read_bytes()).hexdigest() for n in source_files},
                  limits='Kiểm phép tính và bảo toàn mẫu; không chứng nhận hiệu chuẩn, cơ chế vật lý hoặc hiệu quả RCA.')
    ad.ghi(audit / 'checks.json',result)
    print(json.dumps(dict(PASS=result['PASS'],failed=[k for k,v in checks.items() if not v])))
    if not result['PASS']:
        raise SystemExit('hậu xử lý chưa đạt; điều tra trước khi bàn giao')


if __name__ == '__main__':
    main()
