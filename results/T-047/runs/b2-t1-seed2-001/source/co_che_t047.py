"""Trích FACT cho bước 5; không tự quy nguyên nhân hoặc xác nhận cơ chế.

Gate hash K thật/C-e + LOG trước nhãn hoặc kết quả đã chấm. Native đọc
tuần tự mỗi cấu hình; snapshot và chuỗi delta giữ riêng từng ca để có thể
đọc cả ca sai và counterpart đúng. Không chạy lại phương pháp.
"""
import argparse
import collections
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts'),
                str(ROOT / 'results/T-045/scripts')]
import adapter_t047 as ad
import luat_c_t047 as lc
import pha2_t047 as evaluator
import pha2_khoi_k as old
import so_sanh_t047 as comparison
from m1_danh_gia import chon_khoi, dau_vet, m5, pha2, rr


def pointer_key(value):
    return str(value).replace('~', '~0').replace('/', '~1')


def positions(blocks):
    return {e: (bi, gi) for bi, b in enumerate(blocks or [])
            for gi, group in enumerate(b['groups']) for e in group}


def before_root(blocks, root):
    p = positions(blocks)
    return sorted(e for e in p if root in p and p[e] < p[root])


def snapshot(rec, source, label=None):
    """Giữ dữ kiện có trong native; thiếu không suy bằng 0 hoặc False."""
    ex = rec.get('extra') or {}
    missing = []
    for field in ('tang_P', 'K_I_P', 'K_raw_P', 'kenh_co', 'don_vi_phan_vi', 'G_N', 'canh'):
        if field not in ex:
            missing.append('/extra/' + field)
    for field in ('blocks', 'coverage', 'inherited_by', 'worlds'):
        if field not in rec:
            missing.append('/' + field)
    units = {}
    for i, unit in enumerate(ex.get('don_vi_phan_vi') or []):
        units[unit['ma']] = dict(value=unit, pointer=f'/extra/don_vi_phan_vi/{i}')
    counted = {}
    for w in lc.WORLDS:
        counted[w] = {}
        for i, unit in enumerate((rec.get('worlds') or {}).get(w, {}).get('don_vi_dem') or []):
            counted[w][unit['ma']] = dict(value=unit, pointer=f'/worlds/{w}/don_vi_dem/{i}')
    channels = {k['ma']: dict(value=k, pointer=f'/extra/kenh_co/{i}')
                for i, k in enumerate(ex.get('kenh_co') or [])}
    blocks = rec.get('blocks')
    tang = ex.get('tang_P')
    rank = {}
    if label is not None:
        root = label['root']
        for w in lc.WORLDS:
            b = blocks if w == 'P' else (rec.get('worlds') or {}).get(w, {}).get('blocks')
            if not isinstance(b, list):
                missing.append('/blocks' if w == 'P' else f'/worlds/{w}/blocks')
                rank[w] = dict(RR=None, hit1=None, expected_rank=None, M5=None)
                continue
            ok = rec.get('status') == 'OK'
            rank[w] = dict(RR=rr.rr_ca(b, root, ok), hit1=rr.hit1_ca(b, root, ok),
                           expected_rank=rr.hang_ky_vong(b, root) if ok else None,
                           M5=(bool(ok and m5.co_M5(b, root, {tuple(x) for x in ex['G_N']}))
                               if 'G_N' in ex else None))
    return dict(source=source, status=rec.get('status'), method_version=rec.get('method_version'),
                config_id=rec['config_id'], opaque_id=rec['opaque_id'], label=label,
                window=rec.get('window'), coverage=rec.get('coverage'), diagnostics=rec.get('diagnostics'),
                sets=rec.get('sets'), verdict=rec.get('verdict'), blocks=blocks,
                worlds={w: dict(blocks=(rec.get('worlds') or {}).get(w, {}).get('blocks'),
                                units=counted[w]) for w in lc.WORLDS}, units=units, channels=channels,
                tang=tang, K_I=ex.get('K_I_P'), K_raw=ex.get('K_raw_P'), inherited_by=rec.get('inherited_by'),
                G_N=ex.get('G_N'), canh=ex.get('canh'), nhom_vong=ex.get('nhom_vong_P'),
                thong_ke_log=ex.get('thong_ke_log'), T4c=ex.get('T4c'), rank=rank,
                N1=sum(t == 1 for t in tang.values()) if isinstance(tang, dict) else None,
                missing=sorted(set(missing)))


def changed_units(a, b, relevant):
    """Liệt kê mọi đơn vị đổi; giữ giá trị chi tiết cho đơn vị của các kênh liên quan."""
    out = []
    for world in ('shared', *lc.WORLDS):
        ua = a['units'] if world == 'shared' else a['worlds'][world]['units']
        ub = b['units'] if world == 'shared' else b['worlds'][world]['units']
        for name in sorted(set(ua) | set(ub)):
            av, bv = ua.get(name), ub.get(name)
            va, vb = av['value'] if av else {}, bv['value'] if bv else {}
            fields = sorted(k for k in set(va) | set(vb) if va.get(k) != vb.get(k) or (k in va) != (k in vb))
            if av is not None and bv is not None and not fields:
                continue
            row = dict(ma=name, world=world, fields=fields,
                       before_pointer=av['pointer'] if av else None,
                       after_pointer=bv['pointer'] if bv else None,
                       before_present=av is not None, after_present=bv is not None,
                       relevant=name in relevant)
            if name in relevant:
                row['values'] = {k: dict(before=va.get(k), after=vb.get(k),
                                         before_present=k in va, after_present=k in vb) for k in fields}
            out.append(row)
    return out


def chain_delta(a, b, root=None):
    """Đầu vào đã lưu → đơn vị/cờ → F_I → khóa → hạng; không suy cơ chế."""
    if root is None:
        entities = {e for snap in (a, b) for e, t in (snap['tang'] or {}).items() if t == 1}
    else:
        entities = {root} | set(before_root(a['blocks'], root)) | set(before_root(b['blocks'], root))
    channels = []
    relevant_units = set()
    for ma in sorted(set(a['channels']) | set(b['channels'])):
        av, bv = a['channels'].get(ma), b['channels'].get(ma)
        va, vb = av['value'] if av else None, bv['value'] if bv else None
        if not any(x is not None and x.get('thuc_the') in entities for x in (va, vb)):
            continue
        relevant_units.update(x['don_vi'] for x in (va, vb) if x is not None and x.get('don_vi'))
        channels.append(dict(ma=ma, before=va, after=vb,
                             before_pointer=av['pointer'] if av else None,
                             after_pointer=bv['pointer'] if bv else None,
                             changed=va != vb))
    keys = {e: {field: dict(before=(a[field] or {}).get(e), after=(b[field] or {}).get(e))
                for field in ('tang', 'K_I', 'K_raw')} for e in sorted(entities)}
    rank = {}
    for w in lc.WORLDS:
        if root is None:
            break
        av, bv = a['rank'][w], b['rank'][w]
        rank[w] = dict(before=av, after=bv,
                       delta_RR=bv['RR'] - av['RR'] if av['RR'] is not None and bv['RR'] is not None else None)
    inherited = {name: [x for x in snap.get('inherited_by') or [] if x.get('thuc_the') in entities]
                 for name, snap in (('before', a), ('after', b))}
    return dict(entities_examined=sorted(entities), rank=rank,
                input=dict(window_changed=a['window'] != b['window'],
                           coverage_changed=a['coverage'] != b['coverage'],
                           span_diagnostics_before=(a.get('diagnostics') or {}).get('span'),
                           span_diagnostics_after=(b.get('diagnostics') or {}).get('span'),
                           pointers=['/window', '/coverage', '/diagnostics/span', '/thong_ke_log']),
                units_changed=changed_units(a, b, relevant_units), channels=channels, entity_keys=keys,
                inherited_by=inherited, graph=dict(G_N_changed=a['G_N'] != b['G_N'],
                                                  canh_changed=a['canh'] != b['canh']),
                N1=dict(before=a['N1'], after=b['N1'],
                        delta=b['N1'] - a['N1'] if a['N1'] is not None and b['N1'] is not None else None),
                missing=dict(before=a['missing'], after=b['missing']),
                status='FACTS_ONLY',
                warning='Kênh vắng trong kenh_co không tự có nghĩa F_raw=0; có thể thiếu/không chấm/khác tập đơn vị.')


def group_case(old_off, old_on, new_off, new_on):
    vals = [s['rank']['P'] for s in (old_off, old_on, new_off, new_on)]
    if any(x['RR'] is None for x in vals):
        return dict(effect='OPEN_RR', correctness='OPEN', delta_old=None, delta_new=None)
    d_old, d_new = vals[1]['RR'] - vals[0]['RR'], vals[3]['RR'] - vals[2]['RR']
    return dict(effect='tut' if d_new < 0 else 'len' if d_new > 0 else 'khong_doi',
                correctness='dung' if vals[3]['hit1'] == 1 else 'hoa_dau' if vals[3]['hit1'] > 0 else 'sai',
                delta_old=d_old, delta_new=d_new, delta_effect=d_new - d_old)


def signal_signature(snap, label):
    """Điều kiện để tìm counterpart; mô tả bản tắt mới, không là cơ chế hay tiêu chí chọn."""
    root = label['root']
    channels = [x['value'] for x in snap['channels'].values() if x['value']['thuc_the'] == root]
    coverage = snap.get('coverage')
    observed = (snap.get('sets') or {}).get('observed_entities')
    return dict(dataset=label['dataset'], loai_loi=label.get('loai_loi'),
                root_in_returned=root in positions(snap['blocks']),
                root_observed=root in observed if isinstance(observed, list) else None,
                root_raw_channel=bool(channels) if '/extra/kenh_co' not in snap['missing'] else None,
                root_intrinsic_channel=any(x.get('F_I') == 1 for x in channels)
                    if '/extra/kenh_co' not in snap['missing'] else None,
                channel_groups=sorted({(x.get('don_vi') or '').split('|', 1)[0] for x in channels}),
                propagation_classes=sorted({x.get('lop') for x in channels if x.get('lop') is not None}),
                has_ancestor_before=snap['rank']['P']['M5'],
                coverage_unsupported=sorted(k for k, v in coverage.items() if v.get('trang_thai') != 'OK')
                    if isinstance(coverage, dict) else None)


def counterparts(rows):
    """Giữ mọi ca; không ép có counterpart khi dữ liệu không có điều kiện tương ứng."""
    out = {}
    for oid, row in sorted(rows.items()):
        candidates = [o for o, x in sorted(rows.items()) if o != oid and x['condition'] == row['condition']]
        out[oid] = dict(same_condition=candidates,
                        dung=[o for o in candidates if rows[o]['group']['correctness'] == 'dung'],
                        sai=[o for o in candidates if rows[o]['group']['correctness'] == 'sai'],
                        hoa_dau=[o for o in candidates if rows[o]['group']['correctness'] == 'hoa_dau'],
                        status='CANDIDATES_TO_READ' if candidates else 'OPEN_NO_MATCH',
                        note='Cùng điều kiện quan sát không xác nhận nguyên nhân chung hoặc độc lập thống kê.')
    return out


def select_pairs(new, previous):
    selected = {}
    for key, value in new['cap'].items():
        prior = previous['cap'].get(key)
        reasons = []
        if prior is None:
            reasons.append('OPEN_thieu_cap_T045')
        else:
            for w in lc.WORLDS:
                if value['theo_the_gioi'][w]['ket_cuc'] != prior['theo_the_gioi'][w]['ket_cuc']:
                    reasons.append('ket_cuc_khac_T045_' + w)
        if reasons:
            selected[key] = reasons
    winner = new['chon_khoi']['P']['chon']
    if winner is not None:
        s = chon_khoi.tap(winner)
        for x in lc.TP:
            key = chon_khoi.ten(s - {x}, lc.TP) + '|' + chon_khoi.ten(s | {x}, lc.TP)
            selected.setdefault(key, []).append('dao_' + x + '_tai_thang')
        key = 'R0|' + winner
        if key in new['cap'] and any(new['cap'][key]['theo_the_gioi'][w]['ket_cuc'] == 'HAI' for w in lc.WORLDS):
            selected.setdefault(key, []).append('R0_den_thang_HAI')
    return selected


def old_part_sources(run_names, files):
    out = []
    for name in run_names:
        base = old.RUNS / name
        comparison._verified(base / 'pha1.json', files)
        comparison._verified(base / 'theo-cau-hinh/tach.json', files)
        out.append(old.phan_cua(name))
    return out


def save_native(parts_by_dataset, files, needed, audit, version, window, labels, event):
    index = {}
    for cid in sorted(needed):
        index[cid] = {}
        for source_parts in parts_by_dataset:
            if cid not in source_parts:
                raise ValueError('OPEN: thiếu native ' + cid)
            base = source_parts[cid]
            if files is not None:
                comparison._verified(base / 'pha1.json', files)
            meta = json.loads((base / 'pha1.json').read_text(encoding='utf-8'))
            source = base / meta['tep']
            if files is not None:
                comparison._verified(source, files)
                if comparison.sha_file(source) != meta['sha256']:
                    raise ValueError('hash native khác metadata')
            for line, rec in comparison._iter_records(source):
                oid = rec['opaque_id']
                if rec['config_id'] != cid or oid in index[cid]:
                    raise ValueError('native trùng cấu hình/ca')
                label = labels[oid] if window == 'that' else None
                src = dict(file=source.relative_to(ad.ROOT).as_posix(), line=line,
                           sha256=meta['sha256'], config_id=cid, opaque_id=oid)
                snap = snapshot(rec, src, label)
                target = audit / 'native' / version / window / cid / (oid + '.json')
                ad.ghi(target, snap)
                index[cid][oid] = target
            event(event='native_extracted', version=version, window=window, config=cid,
                  cases=len(index[cid]))
    return index


def read_snapshot(path):
    return pha2.giai_ma_json(json.loads(Path(path).read_text(encoding='utf-8')))


def run(args):
    paths = {k: ad.duong_ra(getattr(args, k)) for k in ('that', 'ce')}
    # Trước cả khoi-k.json cũ/mới, nhãn hoặc E_X.
    metas = evaluator.verify_logged(paths)
    evaluator.validate_design(metas)
    new_path = ad.duong_ra(args.khoi)
    new = pha2.giai_ma_json(json.loads(new_path.read_text(encoding='utf-8')))
    if new.get('hash_pha1') != {k: m['sha256'] for k, m in metas.items()}:
        raise ValueError('khoi-k T047 không thuộc hai hash đã ghi LOG')
    files, old_manifest = comparison._old_manifest()
    old_path = comparison._verified(ad.ROOT / 'results/T-045/khoi-k.json', files)
    previous = pha2.giai_ma_json(json.loads(old_path.read_text(encoding='utf-8')))
    labels = old.nap_nhan(False)
    selected = select_pairs(new, previous)
    needed = {'K-' + name for key in selected for name in key.split('|')}
    audit = ad.duong_ra(args.run)
    audit.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    with (audit / 'progress.jsonl').open('x', encoding='utf-8') as progress:
        def event(**value):
            row = dict(time=evaluator.now(), seconds=time.monotonic() - start, **value)
            budget_path = ad.OUT / 'runs/ngan-sach.json'
            if budget_path.exists():
                budget = json.loads(budget_path.read_text(encoding='utf-8'))
                row['budget_seconds'] = budget['prior_seconds'] + time.time() - budget['start_epoch']
            progress.write(json.dumps(row, ensure_ascii=False) + '\n')
            progress.flush()
            if budget_path.exists() and row['budget_seconds'] >= budget['cap_seconds']:
                raise TimeoutError('DỪNG: tới trần gói chạy')
        with (ad.OUT / 'so-lan-nhin.jsonl').open('a', encoding='utf-8') as f:
            f.write(json.dumps(dict(time=evaluator.now(), cong_doan='buoc5_trich_FACT',
                                   muc_dich='chuỗi bằng chứng và counterpart; không đổi thiết kế',
                                   hash_pha1={k: m['sha256'] for k, m in metas.items()}), ensure_ascii=False) + '\n')
        event(event='start', pairs=len(selected), configs=len(needed))
        ad.ghi(audit / 'command.json', dict(argv=sys.argv,
            source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            hash_pha1={k: m['sha256'] for k, m in metas.items()}))
        nt, nc = (evaluator.parts(paths[k], metas[k]) for k in ('that', 'ce'))
        true_new = save_native([{c: p for c, (p, _) in nt.items()}], None, needed, audit, 'T047', 'that', labels, event)
        fake_new = save_native([{c: p for c, (p, _) in nc.items()}], None, needed, audit, 'T047', 'ce', labels, event)
        true_old = save_native(old_part_sources(old.LUOT_THAT, files), files, needed, audit, 'T045', 'that', labels, event)
        fake_old = save_native(old_part_sources([old.LUOT_MG], files), files, needed, audit, 'T045', 'ce', labels, event)
        index, missing = {}, []
        for key, reasons in sorted(selected.items()):
            off, on = ('K-' + x for x in key.split('|'))
            groups, case_index = collections.Counter(), {}
            if not (set(true_new[off]) == set(true_new[on]) == set(true_old[off]) == set(true_old[on]) == set(labels)):
                raise ValueError('cặp cơ chế không cùng 52 ca')
            for oid, label in sorted(labels.items()):
                paths4 = dict(old_off=true_old[off][oid], old_on=true_old[on][oid],
                              new_off=true_new[off][oid], new_on=true_new[on][oid])
                snaps = {k: read_snapshot(p) for k, p in paths4.items()}
                group = group_case(**snaps)
                groups[group['effect']] += 1
                groups['ket_qua_' + group['correctness']] += 1
                delta = {name: chain_delta(snaps[a], snaps[b], label['root']) for name, (a, b) in {
                    'T045_bat_tru_tat': ('old_off', 'old_on'), 'T047_bat_tru_tat': ('new_off', 'new_on'),
                    'doi_phien_ban_nhanh_tat': ('old_off', 'new_off'), 'doi_phien_ban_nhanh_bat': ('old_on', 'new_on')}.items()}
                file = audit / 'pairs' / key.replace('|', '__') / (oid + '.json')
                refs = {k: p.relative_to(ad.ROOT).as_posix() for k, p in paths4.items()}
                ad.ghi(file, dict(pair=key, opaque_id=oid, label=label, group=group, native=refs,
                                  chains=delta, status='FACTS_ONLY',
                                  raw_input_lookup=dict(file='results/T-022/allowlist-dev.json' if label['dataset'] == 'RE2-TT'
                                                        else 'results/T-026/allowlist-dev.json', opaque_id=oid)))
                condition = signal_signature(snaps['new_off'], label)
                case_index[oid] = dict(file=file.relative_to(ad.ROOT).as_posix(), group=group, condition=condition)
                for version, snap in snaps.items():
                    if snap['missing']:
                        missing.append(dict(pair=key, opaque_id=oid, branch=version, fields=snap['missing'],
                                            snapshot=refs[version]))
            match = counterparts(case_index)
            # C-e dùng N1/tầng; không gán root thật hoặc đúng/sai RCA vào cửa sổ giả.
            fake_index = {}
            ids = set(fake_new[off])
            if not (ids == set(fake_new[on]) == set(fake_old[off]) == set(fake_old[on])) or len(ids) != 30:
                raise ValueError('cặp C-e cơ chế không cùng 30 cửa sổ')
            for oid in sorted(ids):
                pp = dict(old_off=fake_old[off][oid], old_on=fake_old[on][oid],
                          new_off=fake_new[off][oid], new_on=fake_new[on][oid])
                ss = {k: read_snapshot(p) for k, p in pp.items()}
                file = audit / 'ce-pairs' / key.replace('|', '__') / (oid + '.json')
                ad.ghi(file, dict(pair=key, opaque_id=oid,
                                  native={k: p.relative_to(ad.ROOT).as_posix() for k, p in pp.items()},
                                  N1={k: s['N1'] for k, s in ss.items()},
                                  verdict={k: s['verdict'] for k, s in ss.items()},
                                  chains={name: chain_delta(ss[a], ss[b]) for name, (a, b) in {
                                      'T045_bat_tru_tat': ('old_off', 'old_on'), 'T047_bat_tru_tat': ('new_off', 'new_on'),
                                      'doi_phien_ban_nhanh_tat': ('old_off', 'new_off'),
                                      'doi_phien_ban_nhanh_bat': ('old_on', 'new_on')}.items()}))
                fake_index[oid] = file.relative_to(ad.ROOT).as_posix()
            index[key] = dict(reasons=reasons, counts=dict(groups), cases=case_index, counterparts=match,
                              ce=fake_index, conclusion='OPEN: cần người làm đọc chuỗi, code và raw để diễn giải')
            event(event='pair_done', pair=key, cases=len(case_index), fake_windows=len(fake_index))
        opens = [dict(question='Nguyên nhân thay đổi ở từng cặp quan trọng là gì?',
                      status='OPEN', evidence_needed='Đọc file pair/snapshot, raw theo allowlist và code; kiểm giải thích khác.',
                      dependent='Kết luận cơ chế, phân loại nguồn hạn chế và diễn giải lựa chọn.'),
                 dict(question='Trung gian nào chưa được native ghi?', status='OPEN',
                      evidence_needed=['mẫu N/A và mốc sự kiện của đơn vị bị đổi',
                                       'phi_D1 ở cấu hình K; native không lưu hệ số',
                                       'khối/b/rho và phép hoán vị G3 khi cần phân xử p đổi',
                                       'khoảng span và phần độc quyền E1 khi cần phân xử thay đổi mẫu'],
                      dependent='Chuỗi hiện tại cho nơi đổi giá trị, chưa tự phân xử vì sao giá trị đổi.')]
        out = dict(schema='T047-co-che-facts-v1', status='FACTS_ONLY_NEEDS_INTERPRETATION',
                   selected_pairs=index, missing_native_fields=missing, OPEN=opens,
                   sources=dict(T047=dict(khoi_k=new_path.relative_to(ad.ROOT).as_posix(),
                                          hash_pha1={k: m['sha256'] for k, m in metas.items()}),
                                T045=dict(manifest=old_manifest, khoi_k=old_path.relative_to(ad.ROOT).as_posix())),
                   code_to_read=['src/m1/chuoi.py:437 (D1)', 'src/m1/chuoi.py:464 (G3/E4)',
                                 'src/m1/chuoi.py:555 (E5/xếp hạng)', 'src/m1/e5.py', 'src/m1/xep_hang.py',
                                 'src/m1_danh_gia/m5.py', 'results/T-047/scripts/luat_c_t047.py'],
                   limits=['Chữ ký counterpart là điều kiện quan sát để đọc, không phải matching nhân quả.',
                           'G3/D1/S1 và luật C-e đổi cùng gói; không quy chênh tổng thành cơ chế riêng.',
                           'Cờ thiếu dữ liệu/coverage không tự chứng minh nguyên nhân thuộc dataset.',
                           'Không loại nhóm vì thiếu trung gian; các nhóm đó giữ OPEN ở index.'])
        ad.ghi(audit / 'co-che-khoi-k.json', out)
        ad.ghi(ad.duong_ra(args.ra), out)
        event(event='done', pairs=len(index))
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--that', required=True)
    parser.add_argument('--ce', required=True)
    parser.add_argument('--run', required=True)
    parser.add_argument('--khoi', default=str(ad.OUT / 'khoi-k.json'))
    parser.add_argument('--ra', default=str(ad.OUT / 'co-che-khoi-k.json'))
    run(parser.parse_args())


if __name__ == '__main__':
    main()
