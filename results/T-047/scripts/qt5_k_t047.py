"""Phân xử cờ QT5 trên native K có sẵn, không nhãn hoặc chạy lại M1."""
import argparse
import collections
import hashlib
import json
import math
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts'), str(ROOT / 'results/T-045/scripts')]
import adapter_t047 as ad
import tep_pha1
import soi_ban_ghi as soi


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def flags(q):
    out = {k: q[k] for k in ('diem_lon_hon_1e6', 'toan_hoa', 'so_nguong_cuc_lon',
           'cot_metric_chua_khai_nguon', 'nguon_metric_unsupported', 'coverage_unsupported') if q.get(k)}
    if (q.get('nhom_chiem') or 0) > .9:
        out['nhom_chiem'] = q['nhom_chiem']
    return out


def extract(rec, line, source, ds):
    q = soi.soi(rec, False)
    ex = rec['extra']
    pv = ex['don_vi_phan_vi']
    counted = rec['worlds']['P']['don_vi_dem']
    by_unit = {u['ma']: dict(u, kind='phan_vi', pointer=f'/extra/don_vi_phan_vi/{i}') for i, u in enumerate(pv)}
    by_unit.update({u['ma']: dict(u, kind='dem', pointer=f'/worlds/P/don_vi_dem/{i}') for i, u in enumerate(counted)})
    channels = []
    groups, intrinsic, valid, raw_units = (collections.Counter() for _ in range(4))
    states = collections.Counter()
    for ma, unit in by_unit.items():
        group = soi.nhom_cua_ma(ma)
        states[group + '|' + unit['trang_thai']] += 1
        if unit['trang_thai'] == 'OK':
            valid[group] += 1
        if unit.get('F_raw_len') or unit.get('F_raw_xuong'):
            raw_units[group] += 1
    missing_units, bad_scores = [], []
    for i, channel in enumerate(ex['kenh_co']):
        group = soi.nhom_cua_ma(channel['don_vi'])
        groups[group] += 1
        if channel['F_I'] == 1:
            intrinsic[group] += 1
        ma = channel['don_vi']
        unit = by_unit.get(ma)
        if unit is None:
            missing_units.append(ma)
        if not math.isfinite(channel['s']) or not 0 <= channel['s'] <= 1:
            bad_scores.append(channel['ma'])
        channels.append(dict(channel, group=group, pointer=f'/extra/kenh_co/{i}',
                             unit_status=unit.get('trang_thai') if unit else None,
                             unit_pointer=unit.get('pointer') if unit else None))
    thresholds = [dict(ma=u['ma'], field=k, value=u[k]) for u in pv for k in ('h', 'l')
                  if u.get(k) is not None and (not math.isfinite(u[k]) or abs(u[k]) > soi.NGUONG_LON)]
    tang = ex['tang_P']
    raw_keys, intrinsic_keys = ex['K_raw_P'], ex['K_I_P']
    zero_keys = all(all(x == 0 for x in v) for v in intrinsic_keys.values())
    dominant = sorted(g for g, n in groups.items() if n == max(groups.values())) if groups else []
    tier_fact = dict(tiers=dict(collections.Counter(str(t) for t in tang.values())),
                     returned=rec['sets']['returned'], observed=rec['sets']['observed'],
                     intrinsic_all_zero=zero_keys,
                     all_tier3=bool(tang) and all(t == 3 for t in tang.values()),
                     blocks=rec['blocks'] if q.get('toan_hoa') else None,
                     K_raw=raw_keys if q.get('toan_hoa') else None,
                     K_I=intrinsic_keys if q.get('toan_hoa') else None)
    ratio = q['nhom_chiem']
    explanation = {}
    if 'nhom_chiem' in flags(q):
        explanation['nhom_chiem'] = dict(status='FACT', dominant_groups=dominant,
            numerator=max(groups.values()), denominator=sum(groups.values()), ratio=ratio,
            definition='số kênh có F_raw=1 theo tiền tố đơn vị; không phải điểm, không phải F_I hay tỷ lệ RCA đúng',
            facts='các nhóm còn lại được tách trạng thái OK/LOW_SUPPORT/NO_DATA, số đơn vị có cờ và F_I bên dưới',
            inference='một nhóm cung cấp phần lớn kênh có cờ tại cấu hình/cửa sổ này',
            OPEN='chưa phân xử tín hiệu của nhóm là bất thường thật/nhiễu; không quy nguyên nhân RCA từ group dominance')
    if q.get('toan_hoa'):
        explanation['toan_hoa'] = dict(status='FACT' if zero_keys and tier_fact['all_tier3'] else 'OPEN',
            definition='một khối trả về hơn một thực thể',
            mechanism='mọi thực thể tầng 3 và K_I=0 nên E6a trả một khối hòa' if zero_keys and tier_fact['all_tier3'] else
                      'khối đầu/khoá cần đọc thêm; không mặc định toàn hòa là dữ liệu thiếu',
            OPEN='chưa phân xử vì sao các phép có cỡ mẫu hợp lệ không tạo cờ; không xác nhận cửa sổ bình thường')
    for key in set(flags(q)) - {'nhom_chiem', 'toan_hoa'}:
        explanation[key] = dict(status='OPEN', evidence='xem native details và đơn vị; chưa tự coi là giới hạn đã biết')
    return dict(dataset=ds, config_id=rec['config_id'], opaque_id=rec['opaque_id'],
                source=dict(file=source, line=line), flags=flags(q), status=rec['status'],
                unit_states=dict(states), valid_units=dict(valid), raw_flag_units=dict(raw_units),
                raw_flag_channels=dict(groups), intrinsic_channels=dict(intrinsic),
                dominant_groups=dominant, ratio=ratio,
                channel_count_equals_qt5=sum(groups.values()) == q['kenh_co'],
                group_counts_equal_qt5=dict(groups) == q['kenh_co_theo_nhom'],
                missing_channel_units=sorted(set(missing_units)), out_of_range_scores=bad_scores,
                thresholds=thresholds, coverage={k: v.get('trang_thai') for k, v in rec['coverage'].items()},
                tier_fact=tier_fact, channels=channels if flags(q) else [],
                units={ma: u for ma, u in by_unit.items()} if flags(q) else {},
                classification=explanation, blocking=bool(missing_units or bad_scores or thresholds)
                    or any(x.get('status') == 'OPEN' for k, x in explanation.items() if k not in ('nhom_chiem',)))


def audit(path, out):
    path = ad.duong_ra(path)
    meta = tep_pha1.kiem(path)
    qpath = path / 'kiem-k-pha1.json'
    checked = json.loads(qpath.read_text(encoding='utf-8'))
    if checked['phase1']['sha256'] != meta['sha256']:
        raise ValueError('QT5 index không khớp hash pha1')
    ds = {x['oid']: x['dataset'] for x in checked['cases']}
    rows = {}
    source = path / meta['tep']
    with source.open('rb') as f:
        for line, b in enumerate(f, 1):
            if b.strip():
                rec = json.loads(b)
                x = extract(rec, line, source.relative_to(ROOT).as_posix(), ds[rec['opaque_id']])
                rows[(x['config_id'], x['opaque_id'])] = x
    wanted = {(x['config_id'], x['oid']): x['flags'] for x in checked['QT5_can_doc']}
    found = {k: x['flags'] for k, x in rows.items() if x['flags']}
    if wanted != found:
        raise ValueError('tái lập cờ QT5 khác index')
    flagged, counts = {}, collections.Counter()
    for (cid, oid), row in rows.items():
        if not row['flags']:
            continue
        counts.update(row['flags'].keys())
        candidates = [x for (c, o), x in sorted(rows.items())
                      if c == cid and x['dataset'] == row['dataset'] and not x['flags']]
        # Hai đối chiếu cùng cấu hình/dataset gần nhất về số đơn vị hợp lệ; không chọn theo nhãn/hạng.
        candidates.sort(key=lambda x: (abs(sum(x['valid_units'].values()) - sum(row['valid_units'].values())), x['opaque_id']))
        row['counterparts'] = [{k: x[k] for k in ('dataset', 'config_id', 'opaque_id', 'source', 'flags',
            'unit_states', 'valid_units', 'raw_flag_units', 'raw_flag_channels', 'intrinsic_channels', 'ratio', 'coverage', 'tier_fact')}
            for x in candidates[:2]]
        row['counterpart_rule'] = 'cùng dataset+cấu hình, không cờ; gần nhất số đơn vị hợp lệ; không matching nhân quả'
        row['counterpart_status'] = 'FACT_AVAILABLE' if candidates else 'OPEN_NO_UNFLAGGED_SAME_DATASET_CONFIG'
        name = cid + '__' + oid
        file = out / 'records' / path.name / (name + '.json')
        ad.ghi(file, row)
        flagged[name] = dict(flags=row['flags'], dataset=row['dataset'], file=file.relative_to(ROOT).as_posix(),
                            dominant_groups=row['dominant_groups'], blocking=row['blocking'],
                            counterparts=[x['opaque_id'] for x in row['counterparts']])
    return dict(phase1=meta, phase1_source=source.relative_to(ROOT).as_posix(),
                QT5_index=dict(file=qpath.relative_to(ROOT).as_posix(), sha256=sha(qpath)),
                records=len(rows), flagged_records=len(flagged), flag_type_counts=dict(counts), flagged=flagged,
                all_counts_match_QT5=all(x['group_counts_equal_qt5'] and x['channel_count_equals_qt5'] for x in rows.values()),
                blocking=[name for name, x in flagged.items() if x['blocking']],
                dataset_config_groups={dsname: {cid: dict(flagged=sum(bool(x['flags']) for (c, _), x in rows.items()
                    if c == cid and x['dataset'] == dsname), total=sum(1 for (c, _), x in rows.items()
                    if c == cid and x['dataset'] == dsname)) for cid in meta['cau_hinh']}
                    for dsname in sorted(set(ds.values()))})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', action='append', required=True)
    parser.add_argument('--out', required=True)
    a = parser.parse_args()
    out = ad.duong_ra(a.out)
    out.mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    results = {Path(p).name: audit(p, out) for p in a.run}
    old = ad.OUT / 'runs/c1-k-trung-gian-001/qt5-phan-xu-002.json'
    prior = json.loads(old.read_text(encoding='utf-8'))
    ad.ghi(out / 'summary.json', dict(schema='T047-K-QT5-native-audit-v1',
        runs=results, source_code=dict(file='results/T-045/scripts/soi_ban_ghi.py', sha256=sha(soi.__file__)),
        prior_audit=dict(file=old.relative_to(ROOT).as_posix(), sha256=sha(old),
            scope=prior['scope'], reuse='states/raw_group_counts chỉ dùng khi khớp native mới; intrinsic=null không là kết quả FI'),
        scoring_labels_read=False, M1_rerun=False, seconds=time.monotonic()-start,
        conclusion='Phân xử tính toán cờ và trạng thái đầu vào; không xác nhận cơ chế hay hiệu quả RCA.',
        OPEN=['Cờ group dominance không cho biết bất thường thật hay nhiễu; việc này cần phân tích/nhãn đúng pha.',
              'Toàn hòa có thể là phép hợp lệ không tạo cờ; không coi đây là bằng chứng ca không lỗi.']))
    print(json.dumps({k: dict(flagged=v['flagged_records'], types=v['flag_type_counts'], blocking=v['blocking'])
                      for k, v in results.items()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
