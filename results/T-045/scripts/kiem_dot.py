"""T-045: kiểm một đợt chạy song song (`chay_song_song.py`) trong lúc chạy và khi xong. Không đọc nhãn, không đếm verdict.

- Tiến độ: số đơn vị xong, lỗi, bỏ qua, chờ RAM, theo lượt; bộ điều phối còn sống không; dự báo thời gian còn lại.
- Đối chiếu tham chiếu: ca `dev-03d4910932`, `dev-12a1a88069` ở lượt T1 seed 0 so với `runs/b1-r0-re2-003` (code đã
  sửa, chạy riêng); ca `dev-03d4910932` ở lượt khối K so với sha256 bản chẩn đoán ngoài repo `867733d0…` (16 cấu
  hình, cùng ngữ nghĩa ĐC1–ĐC3).
- Đối chiếu chéo trong đợt: bản ghi T1-R0 giống nhau ở seed 0, 1, 2 và lượt xáo (theo ca); bản ghi K-R0 của lượt khối
  K giống bản ghi T1-R0 cùng ca sau khi bỏ `config_id`, `variant` (cùng mã nội dung cấu hình), cả cửa sổ thật và mốc giả.
- Lượt đã ghép: `m1_danh_gia.pha2.doc` (hash, đủ và không trùng bản ghi; không đọc nhãn).
Chạy: $PY -B results/T-045/scripts/kiem_dot.py --dot d17-002 [--ra <json>]
"""
import argparse
import collections
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from m1_danh_gia import pha2  # noqa: E402
import chay_song_song as css  # noqa: E402

RUNS = ROOT / 'results/T-045/runs'
CHEO_R0 = [('b2-t1-re2-seed0-001', 'b2b-k16-re2-001', 'K-R0'),
           ('b2-t1-re2-mocgia-001', 'b2b-k16-re2-mocgia-001', 'K-R0'),
           ('b2-t1-re2-seed0-001', 'b4-t4-re2-001', 'T4-e0.05-a0.01'),
           ('b2-t1-re2-mocgia-001', 'b4-t4-re2-mocgia-001', 'T4-e0.05-a0.01'),
           ('b2-t1-nezha-seed0-001', 'b4-t4-nezha-001', 'T4-e0.05-a0.01'),
           ('b2-t1-nezha-seed0-001', 'b5-k16-nezha-001', 'K-R0')]
K16_THAM_CHIEU = {'dev-03d4910932': '867733d0057766c0762b66bc1d12bf00fe2fef48b524b6a2c3ef07a3173a926f'}


def doc_ca(L, o):
    d = RUNS / L / 'ca' / o
    if not (d / 'pha1.json').exists():
        return None
    meta = json.loads((d / 'pha1.json').read_text(encoding='utf-8'))
    du = (d / meta['tep']).read_bytes()
    return meta['sha256'], [json.loads(x) for x in du.decode('utf-8').splitlines() if x]


def bo_ten(r):
    return json.dumps({k: v for k, v in r.items() if k not in ('config_id', 'variant')}, sort_keys=True,
                      ensure_ascii=False)


def con_song(pid):
    out = subprocess.run(['tasklist', '/FI', f'PID eq {pid}', '/NH'], capture_output=True, text=True).stdout
    return str(pid) in out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dot', required=True)
    ap.add_argument('--ra', default=None)
    a = ap.parse_args()
    dot = RUNS / a.dot
    ev = [json.loads(x) for x in (dot / 'progress.jsonl').read_text(encoding='utf-8').splitlines() if x]
    bd = next(e for e in ev if e['su_kien'] == 'bat_dau')
    nguon = json.loads((dot / 'nguon.json').read_text(encoding='utf-8'))
    dv = [e for e in ev if e['su_kien'] == 'don_vi']
    kq = {'dot': a.dot, 'bat_dau': bd['t'], 'su_kien_cuoi': ev[-1]['su_kien'], 'thoi_diem_cuoi': ev[-1]['t'],
          'dieu_phoi_con_song': con_song(nguon['pid']), 'DUNG': (dot / 'DUNG').read_text(encoding='utf-8').strip()
          if (dot / 'DUNG').exists() else None,
          'don_vi': {'tong': bd['so_don_vi'], 'xong': len(dv), 'dat': sum(1 for e in dv if e['kiem'] == 'dat'),
                     'loi': [e for e in dv if e['kiem'] != 'dat'],
                     'bo_qua_DUNG': sum(1 for e in ev if e['su_kien'] == 'bo_qua_DUNG'),
                     'cho_ram': sum(1 for e in ev if e['su_kien'] == 'cho_ram')},
          'ngoai_le': [e for e in ev if e['su_kien'].startswith('ngoai_le')],
          'pha_A_xong': any(e['su_kien'] == 'pha_A_xong' for e in ev),
          'ghep': {e['luot']: e['rc'] for e in ev if e['su_kien'] == 'ghep'}}
    ram = [e['ram_trong_gib'] for e in dv if 'ram_trong_gib' in e]
    kq['ram_trong_gib_thap_nhat'] = min(ram) if ram else None
    # dự báo: giây trung bình theo loại đơn vị (khối K / còn lại), nhân số đơn vị còn lại, chia số tiến trình
    luot = {L: (s, arg, n, ds) for L, s, arg, n, ds in css.TAT_CA_LUOT.values()}
    so_ca = {ds: len(css.ca_cua(ds)) for ds in ('RE2-TT', 'Nezha-OB')}
    tg = collections.defaultdict(list)
    for e in dv:
        n = luot.get(e['luot'], ('', [], 1, ''))[2]
        tg['K' if n > 1 else 'khac'].append(e['giay'])
    da = collections.Counter(e['luot'] for e in dv)
    con = {'K': 0, 'khac': 0}
    for L, (s, arg, n, ds) in luot.items():
        if L in bd['luot']:
            con['K' if n > 1 else 'khac'] += so_ca[ds] - da.get(L, 0)
    tb = {k: (sum(v) / len(v) if v else None) for k, v in tg.items()}
    if all(tb.get(k) for k in ('K', 'khac')):
        kq['du_bao_con_lai_phut'] = round((con['K'] * tb['K'] + con['khac'] * tb['khac']) / bd['so_tien_trinh'] / 60, 1)
    kq['giay_trung_binh'] = {k: (round(v, 1) if v else None) for k, v in tb.items()}
    # tham chiếu
    tc = {}
    for o in ('dev-03d4910932', 'dev-12a1a88069'):
        x, ref = doc_ca('b2-t1-re2-seed0-001', o), doc_ca('b1-r0-re2-003', o)
        if x and ref:
            tc[f'T1 seed0 {o} = b1-r0-re2-003'] = x[0] == ref[0]
    for o, h in K16_THAM_CHIEU.items():
        x = doc_ca('b2b-k16-re2-001', o)
        if x:
            tc[f'K16 {o} = bản chẩn đoán'] = x[0] == h
    kq['tham_chieu'] = tc
    # chéo trong đợt
    ca = css.ca_re2()
    seeds = ['b2-t1-re2-seed0-001', 'b2-t1-re2-seed1-001', 'b2-t1-re2-seed2-001', 'b2-t1-re2-xao0-001']
    cheo = collections.Counter()
    lech = []
    for o in ca:
        r = {L: doc_ca(L, o) for L in seeds}
        co = [L for L in seeds if r[L]]
        if len(co) >= 2:
            ok = len({r[L][0] for L in co}) == 1
            cheo['T1_seed_xao_giong' if ok else 'T1_seed_xao_lech'] += 1
            if not ok:
                lech.append(['T1 seed/xáo', o, {L: r[L][0][:12] for L in co}])
    # cấu hình cùng mã nội dung với T1-R0 phải cho bản ghi trùng T1-R0 sau khi bỏ config_id, variant
    for T1, K, cid in CHEO_R0:
        for o in css.ca_cua('Nezha-OB' if 'nezha' in K else 'RE2-TT'):
            t, k = doc_ca(T1, o), doc_ca(K, o)
            if t and k:
                kr0 = [x for x in k[1] if x['config_id'] == cid]
                ok = len(kr0) == 1 and bo_ten(kr0[0]) == bo_ten(t[1][0])
                cheo[f'{cid} = T1-R0 ({K})' if ok else f'{cid} khác T1-R0 ({K})'] += 1
                if not ok:
                    lech.append([f'{cid} vs T1-R0', K, o])
    kq['cheo'] = dict(cheo)
    kq['cheo_lech'] = lech
    # lượt đã ghép
    gh = {}
    for L in kq['ghep']:
        try:
            meta = json.loads((RUNS / L / 'pha1.json').read_text(encoding='utf-8'))
            tep = RUNS / L / meta['tep']
            if tep.stat().st_size <= 100 * 2 ** 20:
                m, recs = pha2.doc(RUNS / L, meta['sha256'])
                gh[L] = {'dat': True, 'cach': 'pha2.doc', 'so_ban_ghi': len(recs), 'sha256': meta['sha256'][:16],
                         'status': dict(collections.Counter(r['status'] for r in recs))}
            else:  # tệp lớn (khối K khoảng 0,9 GB): kiểm theo dòng để không giành RAM của đợt đang chạy
                h, khoa, st = hashlib.sha256(), set(), collections.Counter()
                with open(tep, 'rb') as f:
                    for dong in f:
                        h.update(dong)
                        if dong.strip():
                            r = json.loads(dong)
                            khoa.add((r['config_id'], r['opaque_id']))
                            st[r['status']] += 1
                n = sum(st.values())
                cfg, ca = {c for c, _ in khoa}, {o for _, o in khoa}
                dat = (h.hexdigest() == meta['sha256'] and n == meta['so_ban_ghi'] == len(khoa)
                       == len(cfg) * len(ca) and sorted(cfg) == sorted(meta['cau_hinh']) and len(ca) == meta['so_ca'])
                gh[L] = {'dat': dat, 'cach': 'theo_dong', 'so_ban_ghi': n, 'sha256': meta['sha256'][:16],
                         'status': dict(st)}
        except Exception as ex:
            gh[L] = {'dat': False, 'loi': f'{type(ex).__name__}: {ex}'}
    kq['luot_da_ghep'] = gh
    kq['dat_tat_ca'] = (not kq['don_vi']['loi'] and not kq['ngoai_le'] and kq['DUNG'] is None
                        and all(tc.values()) and not lech and all(v['dat'] for v in gh.values()))
    s = json.dumps(kq, ensure_ascii=False, indent=1)
    if a.ra:
        Path(a.ra).write_text(s + '\n', encoding='utf-8')
    print(s)


if __name__ == '__main__':
    main()
