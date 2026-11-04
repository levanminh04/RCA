"""Hai chuỗi trọng điểm: raw trace→mẫu→G0/G3→native; không whole M1."""
import json
import hashlib

import adapter_t047 as ad
import giai_thich_lech_c1 as raw_api
from m1 import chuoi, cong, e4, span
from m1_danh_gia.pha2 import giai_ma_json as dec


def read(p):
    return dec(json.loads(p.read_text(encoding='utf-8')))


def main():
    out = ad.OUT / 'runs/c1-method-analysis-e1-e2-001/raw-api-002'
    out.mkdir(exist_ok=False)
    loader = raw_api.RawInputs()
    targets = [('dev-1ac905bc95', 'K-E2+E5', 'op|currencyservice|hipstershop.CurrencyService/Carry'),
               ('dev-6c9afc9822', 'K-E1+E2', 'canh|checkoutservice|emailservice'),
               ('dev-63c30faf34', 'K-E1+E3', 'op|recommendationservice|/hipstershop.RecommendationService/ListRecommendations')]
    results = []
    for oid, cid, ma in targets:
        base = ad.OUT / 'runs/b3-k-c1-that-001/cases' / oid / 'phase1'
        meta = read(base / 'pha1.json')
        assert hashlib.sha256((base / meta['tep']).read_bytes()).hexdigest() == meta['sha256']
        records = [json.loads(line) for line in (base / meta['tep']).read_text(encoding='utf-8').splitlines()]
        rec = next(r for r in records if r['config_id'] == cid)
        config = next(c for c in read(base / 'tham-so.json')['configs'] if c['config_id'] == cid)
        ts = config['tham_so_E4']
        before = read(ad.OUT / 'runs/b5-c1-co-che-001/native/T045/that' / cid / (oid + '.json'))['units'][ma]['value']
        after = next(u for u in rec['extra']['don_vi_phan_vi'] if u['ma'] == ma)
        if ma.startswith('op|'):
            raw = loader.one(oid, rec, ma)
            if 'E1' in cid[2:].split('+'):
                case, provenance = loader.cache[(oid, rec['window']['A'][0])]
                t = rec['window']['A'][0]
                rows = [s for s in case['spans'] if s['start_us'] * 1000 >= rec['window']['N'][0]
                        and (s['start_us'] + s['duration_us']) * 1000 < rec['window']['A'][1]]
                prep = span.chuan_bi(rows,t=t/1000,tau=1000,tinh_CP=False)
                assert not prep['loi']
                _, owner, operation = ma.split('|',2)
                sample = span.mau_thao_tac(prep,'U')[(owner,operation)]
                raw.update(N=sample['N'],A=sample['A'],mN=[int(v*1000) for v in sample['moc_N']],
                           mA=[int(v*1000) for v in sample['moc_A']],E1='U')
        else:
            first = next(u['ma'] for u in rec['extra']['don_vi_phan_vi'] if u['ma'].startswith('op|'))
            raw0 = loader.one(oid, rec, first)
            case, provenance = loader.cache[(oid, rec['window']['A'][0])]
            t = rec['window']['A'][0]
            rows = [s for s in case['spans'] if s['start_us'] * 1000 >= rec['window']['N'][0]
                    and (s['start_us'] + s['duration_us']) * 1000 < rec['window']['A'][1]]
            prep = span.chuan_bi(rows, t=t / 1000, tau=1000, tinh_CP=False)
            assert not prep['loi']
            _, a, b = ma.split('|')
            sample = span.mau_canh(prep)[(a, b)]
            raw = dict(N=sample['N'], A=sample['A'], mN=[int(v * 1000) for v in sample['moc_N']],
                       mA=[int(v * 1000) for v in sample['moc_A']], t_ns=t,
                       bounds=cong.bien_phia(rec['coverage']['trace'], t), provenance=provenance,
                       source='trace', span_diagnostics=prep['chan_doan'])
        def gate(d):
            return cong.p_theo_G3(raw['N'],raw['mN'],raw['A'],raw['mA'],raw['t_ns'],*raw['bounds'],d,ts,ma)
        directions = ('len','xuong') if 'E3' in cid[2:].split('+') and ma.startswith('op|') else ('len',)
        outputs = {name: chuoi._gon_pv(ma, e4.cham_phan_vi(raw['N'], raw['A'], ts['m_span'], ts,
                              huong_cham=directions, ham_p=ham)) for name,ham in [('G0',None),('G3',gate)]}
        fields = ['n_N','n_A','trang_thai','h','r_len_N','r_len_A','p_len','e_len','F_raw_len']
        if 'xuong' in directions:
            fields += ['l','r_xuong_N','r_xuong_A','p_xuong','e_xuong','F_raw_xuong']
        differences = {name: {k:[expected.get(k), outputs[name].get(k)] for k in fields
                              if expected.get(k) != outputs[name].get(k)}
                       for name, expected in [('G0',before),('G3',after)]}
        result = dict(oid=oid,config=cid,unit=ma,raw=raw,params=ts,native={'G0':before,'G3':after},
                      recomputed=outputs,differences=differences,
                      G3_intermediates=raw_api.audit_intermediates(cong,raw['N'],raw['mN'],raw['A'],raw['mA'],raw['t_ns'],raw['bounds']),
                      PASS=not any(differences.values()),scope='đúng cặp raw/API của đơn vị, không hiệu chuẩn hoặc thực nghiệm thiết kế khác')
        ad.ghi(out / (oid + '.json'), result)
        results.append({k:result[k] for k in ['oid','config','unit','differences','PASS']})
        print(oid,ma,{d:{'G0':[before.get('p_'+d),before.get('F_raw_'+d)],'G3':[after.get('p_'+d),after.get('F_raw_'+d)]} for d in directions},differences,flush=True)
    ad.ghi(out / 'summary.json',dict(cases=results,PASS=all(r['PASS'] for r in results)))
    if not all(r['PASS'] for r in results):
        raise SystemExit('chưa tái lập; không công nhận giải thích API')


if __name__ == '__main__':
    main()
