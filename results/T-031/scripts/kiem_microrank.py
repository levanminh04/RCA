"""T-031 bước 5–6 cho MicroRank sau lời Minh "1 duyệt" (giữ 4 ca ERROR là trượt, nhánh đi tiếp).

Trên 3 ca pilot: hash seed 1 so với bản ghi hash seed 0 của bước 2. Trên ca trung vị dưới: cửa sổ bình thường
t' = t0 + 360 (§11.9) và hoán vị dòng span (§11.10). Không dùng nhãn, không in thứ hạng.

python kiem_microrank.py <tom-tat microrank hash seed 0 (dem-loi-microrank.json của lượt)> <ca-pilot.json>
"""
import json
import shutil
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import chung
from p3 import runner
from kiem_ca_that import ban_ghi, ban_sao, so_nhom, tom_ban_ghi, TP


def main(p0, p_pilot):
    al, moc = chung.nap()
    d0 = json.loads(open(p0, encoding='utf-8').read())
    run0 = {r['opaque_id']: Path(p0).parent / 'luot' / r['run_id'] for r in d0['ca'] if r.get('run_id')}
    pilot = json.loads(open(p_pilot, encoding='utf-8').read())['chon']['microrank']
    L = chung.Luot('kiem-microrank')
    out = {'mo_ta': __doc__.strip(), 'run': L.dir.name, 'hash_seed_1': {}}
    for vt, x in pilot.items():
        oid = x['opaque_id']
        r1 = runner.chay_luot(al, oid, 'microrank', 'a', moc[oid], L.dir / 'luot', chung.TIMEOUT_S, hashseed=1)[0]
        r0 = ban_ghi(run0[oid])[0]
        out['hash_seed_1'][oid] = dict(so_nhom(r0, r1), wall_s=r1['cost']['wall_s'])
        L.ghi(f'hash seed 1 {oid}: {out["hash_seed_1"][oid]}')
    oid = pilot['trung_vi_duoi']['opaque_id']
    f = chung.selector.chon_ca(al, oid, chung.ROOT, tep=['metrics.parquet'])
    t0 = int(pd.read_parquet(f['metrics.parquet'], columns=['time'])['time'].min())
    recs = runner.chay_luot(al, oid, 'microrank', 'a', t0 + TP, L.dir / 'luot', chung.TIMEOUT_S, hashseed=0)
    out['binh_thuong'] = {'opaque_id': oid, 'binh_thuong': tom_ban_ghi(recs), 'cua_so_that': tom_ban_ghi(ban_ghi(run0[oid]))}
    L.ghi(f'binh thuong {oid}: {out["binh_thuong"]["binh_thuong"]}')
    dich = chung.OUT / 'work' / 'hoan-vi' / f'microrank-dong-{oid}'
    if dich.exists():
        shutil.rmtree(dich)
    al2, man = ban_sao(al, oid, 'dong', dich, np.random.default_rng(20261006))
    r2 = runner.chay_luot(al2, oid, 'microrank', 'a', moc[oid], L.dir / 'luot', chung.TIMEOUT_S, repo_root=dich, hashseed=0)[0]
    shutil.rmtree(dich)
    out['hoan_vi_dong'] = {'opaque_id': oid, 'manifest_ban_sao': man, 'so_sanh': so_nhom(ban_ghi(run0[oid])[0], r2)}
    L.ghi(f'hoan vi {oid}: {out["hoan_vi_dong"]["so_sanh"]}')
    chung.ghi_json(chung.OUT / 'kiem-microrank.json', out)
    L.xong({'xong': True})


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
