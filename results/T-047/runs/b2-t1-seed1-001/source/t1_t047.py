"""T1 T-047: bất biến, QT5, C-e/N1, Đ5 D1 và đối chiếu bước 10 T-046."""
import collections
import json
import sys
from pathlib import Path
import adapter_t047 as ad
import luat_c_t047 as lc
import tep_pha1

sys.path[:0] = [str(ad.ROOT/'results/T-045/scripts'), str(ad.ROOT/'results/T-046/scripts')]
import t1_tong_hop as old
import b10_kiem_src as b10
from p3 import nezha


def main():
    base = ad.OUT/'runs'
    paths = {str(i): base/f'b2-t1-seed{i}-001' for i in range(3)}
    paths.update(xao=base/'b2-t1-xao0-001', ce=base/'b2-t1-ce-001')
    data = {}
    for name, path in paths.items():
        tep_pha1.kiem(path)
        data[name] = old.doc(path)
    inv = {name: old.so_luot(data['0'], data[name]) for name in ('1', '2', 'xao')}
    universe = json.loads((ad.ROOT/'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    common, qt, d5 = {}, {}, {}
    for group in ('0', 'ce'):
        for (cid, oid), r in data[group][1].items():
            ds = json.loads((paths[group]/'cases'/oid/'summary.json').read_text(encoding='utf-8'))['dataset']
            case = dict(aliases={}, inventory=universe if ds == 'RE2-TT' else nezha.UNIVERSE)
            summary, _, _ = b10.tom_tat(r, case, 'R0')
            ref = json.loads((ad.ROOT/'results/T-046/runs/b10-kiem-src-001/ca'/f'{oid}.json').read_text(encoding='utf-8'))
            original = ref['cua_so'][('that' if group == '0' else 'ce')+'|R0']['tom_tat']
            diff = {k: [original[k], summary.get(k)] for k in set(original)|set(summary) if original.get(k) != summary.get(k)}
            common[group+'|'+oid] = dict(summary=summary, differences=diff)
            if group == '0':
                qt[oid] = old.soi_ban_ghi.soi(r, False)
                d5[oid] = json.loads((paths[group]/'cases'/oid/'d5.json').read_text(encoding='utf-8'))
    fake = {oid: lc._n1(r) for (_, oid), r in data['ce'][1].items()}
    vd = collections.Counter(r['verdict'] for r in data['ce'][1].values())
    denom = sum(v for k, v in vd.items() if k != 'INSUFFICIENT_EVIDENCE')
    gates = collections.Counter()
    for r in data['ce'][1].values():
        q = old.soi_ban_ghi.soi(r, False)
        gates.update({'phan_vi|'+k: v for k, v in q['cong_phan_vi'].items()})
        gates.update({'dem|'+k: v for k, v in q['dem']['P'].items()})
    out = dict(luot={k: str(v.relative_to(ad.ROOT)) for k,v in paths.items()}, bat_bien=inv,
               theo_ca=qt, doi_chieu_T046=common, D5_D1=d5,
               D5_tong=dict(so_don_vi=sum(x['so_don_vi_dem_OK_P'] for x in d5.values()),
                            so_doi=sum(x['so_doi_quyet_dinh'] for x in d5.values())),
               moc_gia=dict(N1=fake, N1_mean=lc.Fraction(sum(fake.values()), len(fake)), verdict=dict(vd),
                            mau_so=denom, ti_le_CAUSE_FOUND=lc.Fraction(vd['CAUSE_FOUND'],denom) if denom else None,
                            cong=dict(gates)))
    out['PASS'] = (all(v['giong_het'] for v in inv.values()) and not any(x['differences'] for x in common.values())
                   and len(qt)==52 and len(fake)==30)
    ad.ghi(ad.OUT/'t1.json', out)
    print(json.dumps(dict(PASS=out['PASS'], bat_bien={k:v['giong_het'] for k,v in inv.items()},
                          common_differences=sum(bool(x['differences']) for x in common.values()), D5=out['D5_tong'])))
    if not out['PASS']:
        raise SystemExit('STOP T1: xem t1.json và giữ mọi lượt')


if __name__ == '__main__':
    main()
