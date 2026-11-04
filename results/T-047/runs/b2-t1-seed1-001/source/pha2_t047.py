"""Pha 2 T-047. Không đọc nhãn trước khi hash pha 1 đã khớp LOG.

Chấm từng cấu hình; C-e và dấu vết đọc tuần tự. --bootstrap chỉ báo cáo,
giữ 1.000 mẫu kể cả mẫu không chọn được hoặc C-e chưa kiểm được.
"""
import argparse
import collections
import hashlib
import json
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from fractions import Fraction
from itertools import combinations, zip_longest
from pathlib import Path

import numpy as np
import psutil

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts'),
                str(ROOT / 'results/T-045/scripts')]
import adapter_t047 as ad
import luat_c_t047 as lc
import tep_pha1
import pha2_khoi_k as old
from m1_danh_gia import chon_khoi, dau_vet, pha2, rr

BOOTSTRAP_SEED = 20261102
BOOTSTRAP_N = 1000


def now():
    return datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')


def verify_logged(paths, log_text=None):
    """Chỉ pha 1: không chạm D2, nhãn, E_X hoặc số chấm cũ."""
    if log_text is None:
        log_text = (ad.ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md').read_text(encoding='utf-8')
    out = {}
    for name, path in paths.items():
        path = ad.duong_ra(path)
        meta = tep_pha1.kiem(path)
        line = f"- `{path.relative_to(ad.ROOT).as_posix()}`: `{meta['sha256']}`"
        if line not in log_text:
            raise ValueError(f'hash pha 1 chưa ghi LOG: {name}')
        out[name] = meta
    return out


def validate_design(meta):
    expected = {'K-' + chon_khoi.ten(set(c), lc.TP)
                for n in range(5) for c in combinations(lc.TP, n)}
    for name, n in (('that', 52), ('ce', 30)):
        m = meta[name]
        if set(m['cau_hinh']) != expected or m['so_ca'] != n or m['so_ban_ghi'] != n * 16:
            raise ValueError(f'khối K {name} không đủ 16 × {n}')


def verify_derived_source():
    """Chỉ gọi sau verify_logged: tệp E_X cũng được D2 dùng để đối chiếu."""
    rel = 'results/T-043/ks16/dem-sau-ghep-nhan.json'
    manifest = json.loads((ad.ROOT / 'results/T-043/manifest.json').read_text(encoding='utf-8'))
    matches = [x['sha256'] for x in manifest['outputs'] if x['path'] == rel]
    if len(matches) != 1:
        raise ValueError('manifest không có đúng một hash cho nguồn E_X')
    got = hashlib.sha256((ad.ROOT / rel).read_bytes()).hexdigest()
    if got != matches[0]:
        raise ValueError('nguồn E_X/hình dạng baseline lệch manifest T-043')
    return {rel: got}


def parts(path, meta):
    """Dùng lại phần tách hợp lệ; không tin riêng cờ noi_lai_dung_goc."""
    path = ad.duong_ra(path)
    split = path / 'theo-cau-hinh'
    if not split.exists():
        tep_pha1.tach(path)
    audit = json.loads((split / 'tach.json').read_text(encoding='utf-8'))
    if (audit.get('sha256_goc') != meta['sha256'] or not audit.get('noi_lai_dung_goc')
            or sorted(audit['phan']) != sorted(meta['cau_hinh'])):
        raise ValueError('chỉ mục tách không khớp gốc')
    digest = hashlib.sha256()
    out = {}
    for cid in sorted(audit['phan']):
        p = split / cid
        m = tep_pha1.kiem(p)
        if m.get('tach_tu') != meta['sha256'] or m['cau_hinh'] != [cid] or m['so_ca'] != meta['so_ca']:
            raise ValueError('phần tách sai nguồn/ma trận')
        with (p / m['tep']).open('rb') as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b''):
                digest.update(chunk)
        out[cid] = (p, m)
    if digest.hexdigest() != meta['sha256']:
        raise ValueError('nối phần tách không khớp hash gốc')
    return out


def records(part):
    p, m = part
    with (p / m['tep']).open('rb') as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                ad.kiem_ban_ghi(rec)
                yield rec


def stop_reason(result):
    winner = result['chon_khoi']['P']['chon']
    if winner is None:
        return 'buoc7_khong_con_cau_hinh'
    if not (chon_khoi.tap(winner) & set(lc.DO_THI)):
        return 'buoc8_khong_E1_E2_E5'
    return None


def defaults(result):
    ch, b8 = result['chon_khoi'], result['buoc8']['P']
    winner = ch['P']['chon']
    out = []
    stop = stop_reason(result)
    if stop:
        out.append(dict(tinh_huong=stop, hanh_dong='DỪNG, trình Minh'))
    if winner is not None:
        if 'trai_chieu_dataset' in ch['P']['ly_do_trinh_Minh']:
            out.append(dict(tinh_huong='buoc6_trai_chieu_dataset',
                            hanh_dong='giữ cấu hình thắng; gắn cờ; báo MRR từng dataset'))
        for key, label in (('xung_dot', 'buoc8_ket_cuc_dao_mau_thuan'),
                           ('phu_thuoc_quan_sat', 'buoc8_phu_thuoc_quan_sat_khong_it_ca')):
            if b8[key]:
                out.append(dict(tinh_huong=label, thanh_phan=b8[key],
                                hanh_dong='giữ cấu hình thắng; ghi cặp và trạng thái'))
        if ch['P'].get('can_Minh_truoc_task2'):
            out.append(dict(tinh_huong='Ce_chua_kiem_o_thang',
                            cap=ch['P']['cap_Ce_chua_kiem_o_thang'],
                            hanh_dong='trình Minh trước khi dùng làm nền task (2)'))
        for w in ('S_lo', 'S_hi'):
            if ch[w]['chon'] != winner:
                out.append(dict(tinh_huong=f'buoc10_{w}_khac_P', chon_o_the_gioi=ch[w]['chon'],
                                hanh_dong='giữ lựa chọn tại P; ghi phụ thuộc quan sát'))
    contrary = sorted(k for k, v in result['cap'].items()
                      if v['ket_hop']['ket_cuc_P'] == 'TRAI_CHIEU_O')
    if contrary:
        out.append(dict(tinh_huong='luatC_buoc7_trai_chieu_o', cap=contrary,
                        hanh_dong='không là căn cứ loại; ghi cờ'))
    return out


def config_summary(kq, ce, true_parts, labels, event):
    out = {}
    mrr = {w: pha2.mrr_cau_hinh(kq, the_gioi=w) for w in lc.WORLDS}
    for cid, scored in sorted(kq['cau_hinh'].items()):
        ca = scored['ca']
        rp = {oid: c['theo_the_gioi']['P']['RR'] for oid, c in ca.items()}
        cell = {oid: c['o'] for oid, c in ca.items()}
        fake = ce[cid]
        vd = collections.Counter(r['verdict'] for r in fake.values())
        valid = {oid: lc._n1(r) for oid, r in fake.items() if r['verdict'] != 'INSUFFICIENT_EVIDENCE'}
        cd, states = {'C-d1': {}, 'C-d3': {}}, collections.Counter()
        for r in records(true_parts[cid]):
            oid = r['opaque_id']
            for method in cd:
                x = r['extra']['doi_chung'][method]
                cd[method][oid] = rr.rr_ca(x.get('blocks') or [], labels[oid]['root'],
                                         x.get('trang_thai') == 'OK')
                states[f"{method}|{x.get('trang_thai')}"] += 1
        out[cid] = dict(
            MRR={w: {d: float(v) for d, v in mrr[w][cid].items()} for w in lc.WORLDS},
            MRR_phan_so={w: mrr[w][cid] for w in lc.WORLDS}, RR_ca_P=rp,
            RR_o_P=rr.rr_o(rp, cell), ca_M5_P=sum(c['theo_the_gioi']['P']['M5'] for c in ca.values()),
            hit1_P=sum((c['theo_the_gioi']['P']['hit1'] for c in ca.values()), Fraction(0)),
            WORLD_DEPENDENT=sorted(o for o, c in ca.items() if c['WORLD_DEPENDENT']),
            moc_gia=dict(verdict=dict(vd), mau_so=len(valid),
                         N1_tung_cua_so={o: valid.get(o) for o in sorted(fake)},
                         bi_loai=sorted(set(fake) - set(valid)),
                         N1_trung_binh=Fraction(sum(valid.values()), len(valid)) if valid else None,
                         ti_le_CAUSE_FOUND=Fraction(vd['CAUSE_FOUND'], len(valid)) if valid else None),
            doi_chung={m: dict(MRR_gop=rr.mrr(v), **{
                ds: rr.mrr(v, {o for o in ca if ca[o]['dataset'] == ds})
                for ds in sorted({c['dataset'] for c in ca.values()})}) for m, v in cd.items()},
            doi_chung_trang_thai=dict(states))
        event(event='config_summary', config=cid)
    return out


def e5_traces(true_parts, fake_parts, labels, event):
    out = {}
    for cid in sorted(true_parts):
        s = chon_khoi.tap(cid[2:])
        if 'E5' not in s:
            continue
        off = 'K-' + chon_khoi.ten(s - {'E5'}, lc.TP)
        cases, counts = {}, collections.Counter()
        for a, b in zip_longest(records(true_parts[off]), records(true_parts[cid])):
            if a is None or b is None or a['opaque_id'] != b['opaque_id']:
                raise ValueError('cặp dấu vết E5 khác tập/thứ tự ca')
            oid = a['opaque_id']
            x = dau_vet.root_E5_tu_ban_ghi(a, b, labels[oid]['root'])
            cases[oid] = x
            counts['ca'] += 1
            counts['root_mat_kenh'] += int(x['mat_kenh_F_raw'][0] > 0)
            counts['root_het_tu_sinh'] += int(x['mat_kenh_F_raw'][1] > 0 and not x['con_tu_sinh'])
            if x['hang_bo_E5'] is not None and x['hang_bat_E5'] is not None:
                counts['hang_tang'] += int(x['hang_bat_E5'] > x['hang_bo_E5'])
                counts['hang_giam'] += int(x['hang_bat_E5'] < x['hang_bo_E5'])
        for r in records(fake_parts[cid]):
            inherited, total = dau_vet.ty_le_ke_thua_lop_lan(r)
            counts['moc_gia_kenh_lan_ke_thua'] += inherited
            counts['moc_gia_kenh_lan'] += total
        key = off[2:] + '|' + cid[2:]
        out[key] = dict(tong_hop=dict(counts), theo_ca=cases)
        event(event='e5_trace', pair=key)
    return out


def bootstrap(kq, ce, ex, event, sample_sink, seed=BOOTSTRAP_SEED, n=BOOTSTRAP_N):
    ca = next(iter(kq['cau_hinh'].values()))['ca']
    ds = [dict(ma=o, dataset=c['dataset'], o=c['o']) for o, c in sorted(ca.items())]
    base = ad.mau_do_ben(kq, ce, ex, {x['ma']: 1 for x in ds})
    if base != ad.pha2_khoi(kq, ce, ex):
        raise ValueError('mọi bội số 1 không tái lập toàn bộ kết quả chính')
    rng = np.random.default_rng(seed)
    kinds, wins, components, flags = (collections.Counter() for _ in range(4))
    world_wins = {w: collections.Counter() for w in lc.WORLDS}
    event(event='bootstrap_start', seed=seed, n=n, h=1)
    for i in range(n):
        weights = rr.lay_mau_o(ds, rng)
        result = ad.mau_do_ben(kq, ce, ex, weights)
        kind = stop_reason(result) or 'chon'
        kinds[kind] += 1
        winner = result['chon_khoi']['P']['chon']
        for w in lc.WORLDS:
            world_wins[w][result['chon_khoi'][w]['chon'] or 'KHONG_CHON_DUOC'] += 1
        if kind == 'chon':
            wins[winner] += 1
            components.update(chon_khoi.tap(winner))
        ch, b8 = result['chon_khoi']['P'], result['buoc8']['P']
        flags['Ce_chua_kiem'] += bool(ch['cap_Ce_chua_kiem'])
        flags['Ce_chua_kiem_o_thang'] += bool(ch['cap_Ce_chua_kiem_o_thang'])
        flags['trai_chieu_dataset_o_thang'] += 'trai_chieu_dataset' in ch['ly_do_trinh_Minh']
        flags['phu_thuoc_quan_sat_o_thang'] += bool(b8 and b8['phu_thuoc_quan_sat']) or any(
            result['chon_khoi'][w]['chon'] != winner for w in ('S_lo', 'S_hi'))
        flags['xung_dot_buoc8'] += bool(b8 and b8['xung_dot'])
        sample_sink(dict(i=i, trong_so=weights, loai=kind, chon_khoi=result['chon_khoi'],
                         buoc8=result['buoc8']))
        event(event='bootstrap_sample', i=i + 1, n=n)
    return dict(seed=seed, n=n, h=lc.H, mau_goc=base, loai=dict(kinds),
                tan_suat_thang=dict(wins), tan_suat_thanh_phan_bat={x: components[x] for x in lc.TP},
                tan_suat_co=dict(flags), tan_suat_the_gioi={w: dict(x) for w, x in world_wins.items()},
                dien_giai='Độ bền lựa chọn trên dev; không chọn lại, không xác nhận hiệu quả RCA.')


def run(args):
    paths = {name: ad.duong_ra(getattr(args, name)) for name in ('that', 'ce')}
    # Gate này phải đứng trước cả subprocess D2 (D2 cũng đọc nhãn).
    meta = verify_logged(paths)
    validate_design(meta)
    derived_hash = verify_derived_source()
    audit = ad.duong_ra(args.run)
    audit.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    with (audit / 'progress.jsonl').open('x', encoding='utf-8') as progress:
        def event(**value):
            budget_path = ad.OUT / 'runs/ngan-sach.json'
            used = None
            if budget_path.exists():
                b = json.loads(budget_path.read_text(encoding='utf-8'))
                used = b['prior_seconds'] + time.time() - b['start_epoch']
            row = dict(time=now(), seconds=time.monotonic() - started,
                       rss=psutil.Process().memory_info().rss, budget_seconds=used, **value)
            progress.write(json.dumps(row, ensure_ascii=False) + '\n')
            progress.flush()
            if used is not None and used >= b['cap_seconds']:
                raise TimeoutError('DỪNG: tới trần tổng gói chạy')

        event(event='start', inputs={k: str(v.relative_to(ad.ROOT)) for k, v in paths.items()})
        ad.ghi(audit / 'command.json', dict(argv=sys.argv, source_sha256=hashlib.sha256(
            Path(__file__).read_bytes()).hexdigest(), phase1=meta, derived_hash=derived_hash,
            bootstrap_seed=BOOTSTRAP_SEED, bootstrap_n=BOOTSTRAP_N))
        with (ad.OUT / 'so-lan-nhin.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(dict(time=now(), task='T-047', cong_doan='pha2',
                                   muc_dich='D2 rồi chấm/luật C khối K; mức h đã khóa',
                                   hash_pha1={k: m['sha256'] for k, m in meta.items()}), ensure_ascii=False) + '\n')
        d2_path = audit / 'tai-lap-baseline.json'
        command = [sys.executable, '-B', str(ad.ROOT / 'results/T-045/scripts/d2_baseline.py'),
                   '--ra', str(d2_path)]
        event(event='d2_start')
        with (audit / 'd2.stdout').open('xb') as stdout, (audit / 'd2.stderr').open('xb') as stderr:
            result = subprocess.run(command, cwd=ad.ROOT, stdout=stdout, stderr=stderr, check=False)
        if result.returncode:
            raise RuntimeError(f'D2 lỗi, mã thoát {result.returncode}')
        d2 = json.loads(d2_path.read_text(encoding='utf-8'))
        summary = d2.get('tong_hop') or {}
        passed = (d2.get('dat') is True and summary.get('so_phuong_phap') == 12
                  and summary.get('MRR_khop_G2') == summary.get('MRR_khop_KS16') == 12)
        ad.ghi(ad.OUT / 'tai-lap-baseline.json', dict(d2, luot=str(d2_path.relative_to(ad.ROOT))))
        event(event='d2_done', passed=passed)
        if not passed:
            raise RuntimeError('DỪNG: D2 không đạt 12/12')
        labels, ex = old.nap_nhan(False), old.nap_E_X(False)
        # Không nạp toàn tệp K; chỉ mỗi cấu hình qua bộ chấm gốc.
        true_parts, fake_parts = (parts(paths[k], meta[k]) for k in ('that', 'ce'))
        kq, ce = {'cau_hinh': {}}, {}
        for cid, (p, m) in sorted(true_parts.items()):
            kq['cau_hinh'][cid] = pha2.cham(p, m['sha256'], labels)['cau_hinh'][cid]
            event(event='scored', config=cid)
        for cid, part in sorted(fake_parts.items()):
            ce[cid] = {}
            for rec in records(part):
                # Đủ dữ kiện N1, không giữ phần trung gian lớn trong RAM.
                slim = dict(status=rec['status'], verdict=rec['verdict'],
                            extra=dict(tang_P=rec['extra']['tang_P']))
                lc._n1(slim)
                ce[cid][rec['opaque_id']] = slim
            if len(ce[cid]) != 30 or not set(ce[cid]) <= set(kq['cau_hinh'][cid]['ca']):
                raise ValueError('C-e không khớp 30 ca RE2-TT')
            if any(labels[o]['dataset'] != 'RE2-TT' for o in ce[cid]):
                raise ValueError('C-e có ca ngoài RE2-TT')
        ad.ghi(audit / 'kq.json', kq)
        ad.ghi(audit / 'ce.json', ce)
        ad.ghi(ad.OUT / 'khoi-k/kq.json', kq)
        ad.ghi(ad.OUT / 'khoi-k/ce.json', ce)
        main = ad.pha2_khoi(kq, ce, ex)
        out = dict(main, thanh_phan=lc.TP, it_ca=lc.IT_CA, do_thi=lc.DO_THI, delta_d=lc.DD,
                   E_X_so_o={x: len(ex[x]) for x in lc.TP}, mac_dinh_ap=defaults(main),
                   luot={k: str(p.relative_to(ad.ROOT)) for k, p in paths.items()},
                   hash_pha1={k: m['sha256'] for k, m in meta.items()},
                   cau_hinh=config_summary(kq, ce, true_parts, labels, event),
                   dau_vet_E5=e5_traces(true_parts, fake_parts, labels, event),
                   STOP=stop_reason(main))
        ad.ghi(audit / 'khoi-k.json', out)
        ad.ghi(ad.OUT / 'khoi-k.json', out)
        event(event='selection_done', winner=main['chon_khoi']['P']['chon'], stop=out['STOP'])
        if out['STOP']:
            raise RuntimeError('DỪNG, trình Minh: ' + out['STOP'])
        out['do_nhay_muc_HAI'] = ad.do_nhay(kq, ce, ex)
        ad.ghi(audit / 'khoi-k.json', out)
        ad.ghi(ad.OUT / 'khoi-k.json', out)
        event(event='sensitivity_done', h=['1', '1/2', '2'])
        if args.bootstrap:
            with (audit / 'bootstrap-samples.jsonl').open('x', encoding='utf-8') as sink:
                def sample(row):
                    sink.write(json.dumps(pha2.ma_hoa_json(row), ensure_ascii=False) + '\n')
                    sink.flush()
                boot = bootstrap(kq, ce, ex, event, sample)
            boot['tep_mau'] = str((audit / 'bootstrap-samples.jsonl').relative_to(ad.ROOT))
            ad.ghi(audit / 'do-ben.json', boot)
            ad.ghi(ad.OUT / 'do-ben.json', boot)
        event(event='done')
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--that', required=True)
    parser.add_argument('--ce', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--bootstrap', action='store_true')
    args = parser.parse_args()
    try:
        out = run(args)
    except Exception as error:
        print(f'STOP: {type(error).__name__}: {error}', file=sys.stderr, flush=True)
        raise
    print(json.dumps(dict(winner=out['chon_khoi']['P']['chon'], STOP=out['STOP']), ensure_ascii=False), flush=True)


if __name__ == '__main__':
    main()
