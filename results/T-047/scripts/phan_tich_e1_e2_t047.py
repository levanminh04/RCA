"""FACT từng ca E1/E2 và nối với kết cục; người làm phải đọc trước diễn giải."""
import collections
import hashlib
import json
from pathlib import Path

import adapter_t047 as ad
import co_che_t047 as mech
import so_sanh_t047 as cmp
from m1_danh_gia.pha2 import giai_ma_json as dec

PAIRS = ['E2+E5|E1+E2+E5', 'E3+E5|E1+E3+E5', 'E3|E1+E3',
         'E2|E1+E2', 'E1|E1+E2', 'R0|E1+E2']


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def read(p):
    return dec(json.loads(p.read_text(encoding='utf-8')))


def main():
    out = ad.OUT / 'runs/c1-method-analysis-e1-e2-001'
    out.mkdir(exist_ok=False)
    new = read(ad.OUT / 'khoi-k.json')
    files, mf = cmp._old_manifest()
    oldp = cmp._verified(ad.ROOT / 'results/T-045/khoi-k.json', files)
    old = read(oldp)
    native = ad.OUT / 'runs/b5-c1-co-che-001/native'
    configs = {'K-' + c for p in PAIRS for c in p.split('|')}
    ids = sorted(p.stem for p in (native / 'T047/that/K-E1+E2').glob('*.json'))
    if len(ids) != 52:
        raise ValueError('cần đủ native trước khi đọc')
    result = {p: dict(cases={}, effects=collections.Counter(), outcomes={}) for p in PAIRS}
    for oid in ids:
        cache = {(version, cid): read(native / version / 'that' / cid / (oid + '.json'))
                 for version in ('T045', 'T047') for cid in configs}
        for pair in PAIRS:
            off, on = ('K-' + c for c in pair.split('|'))
            ss = {name: cache[(v, cid)] for name, v, cid in
                  [('old_off', 'T045', off), ('old_on', 'T045', on), ('new_off', 'T047', off), ('new_on', 'T047', on)]}
            label = ss['new_off']['label'];root = label['root']
            group = mech.group_case(**ss)
            chains = {name: mech.chain_delta(ss[a], ss[b], root) for name, a, b in
                      [('T045', 'old_off', 'old_on'), ('T047', 'new_off', 'new_on'),
                       ('off_old_to_new', 'old_off', 'new_off'), ('on_old_to_new', 'old_on', 'new_on')]}
            sources = {}
            for name, v, cid in [('old_off', 'T045', off), ('old_on', 'T045', on),
                                  ('new_off', 'T047', off), ('new_on', 'T047', on)]:
                p = native / v / 'that' / cid / (oid + '.json')
                sources[name] = dict(file=p.relative_to(ad.ROOT).as_posix(), sha256=digest(p), native_source=ss[name]['source'])
            facts = dict(pair=pair, opaque_id=oid, label=label, group=group, chains=chains,
                         source=sources, condition=mech.signal_signature(ss['new_off'], label),
                         root_state={name: dict(rank=s['rank'], tier=s['tang'].get(root),
                                  K_I=s['K_I'].get(root), K_raw=s['K_raw'].get(root),
                                  channels=[c['value'] for c in s['channels'].values() if c['value']['thuc_the'] == root])
                                     for name,s in ss.items()}, status='FACTS_ONLY')
            p = out / 'cases' / pair.replace('|', '__') / (oid + '.json')
            ad.ghi(p, facts)
            r = result[pair]
            r['cases'][oid] = dict(file=p.relative_to(ad.ROOT).as_posix(), label=label, group=group,
                                   condition=facts['condition'], rank={k: s['rank']['P'] for k,s in ss.items()})
            r['effects'][group['effect']] += 1
            r['effects']['ket_qua_' + group['correctness']] += 1
    for pair, row in result.items():
        row['counterparts'] = mech.counterparts(row['cases'])
        row['effects'] = dict(row['effects'])
        row['outcomes'] = {name: {w: {k: cap.get(k) for k in ['ket_cuc', 'buoc', 'ly_do_hai_rieng',
                            'dMRR', 'P', 'M', 'P_phay', 'M_phay', 'UV6', 'dieu_kien_E5']}
                            | {'C_e': {k: cap['moc_gia'].get(k) for k in ['ve','tang','n']}}
                            for w,cap in src['cap'][pair]['theo_the_gioi'].items()}
                            for name,src in [('T045',old),('T047',new)]}
    ad.ghi(out / 'facts.json', dict(pairs=result, old_manifest=mf, source_khoi_sha256=digest(ad.OUT/'khoi-k.json'),
                                  status='FACTS_ONLY_NEEDS_INTERPRETATION', no_M1_rerun=True))
    print(json.dumps({p:r['effects'] for p,r in result.items()}))


if __name__ == '__main__':
    main()
