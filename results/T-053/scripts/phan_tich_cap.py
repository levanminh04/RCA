"""Phân tích bốn vế và đối chứng theo chữ ký tín hiệu, chỉ ghi đầu ra T-053."""
import argparse
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / name) for name in ('src', 'results/T-053/scripts', 'results/T-047/scripts', 'results/T-045/scripts')]
parser = argparse.ArgumentParser(description='Đối chiếu các cặp quan trọng bằng bốn vế E4/z bật/tắt')
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
import gzip, json
from pathlib import Path
from collections import defaultdict
from m1_danh_gia.pha2 import giai_ma_json, ma_hoa_json
from cham_k import sealed_inputs, source
from doi_chieu import ROOT, read, sha
base = ROOT / 'results/T-053'
out = base / 'runs/k-cham-001'
seal_hash, seal, inputs = sealed_inputs(base / 'runs/k-dong-pha1-001/seal.json')
old_manifest = read(ROOT / 'results/T-047/manifest.json')['outputs']
for name in ('results/T-047/khoi-k/kq.json', 'results/T-047/khoi-k.json'):
    assert sha(ROOT / name) == old_manifest[name]['sha256']
old = giai_ma_json(read(ROOT / 'results/T-047/khoi-k/kq.json'))['cau_hinh']
new = giai_ma_json(read(out / 'kq.json'))['cau_hinh']
law = giai_ma_json(read(out / 'khoi-k.json'))
labels = source.nap_nhan(False)
pairs = [('E1+E2', 'E1+E2+E5'), ('E1+E5', 'E1+E2+E5'), ('E2+E5', 'E1+E2+E5'), ('E1+E2+E5', 'E1+E2+E3+E5'), ('R0', 'E1+E2'), ('R0', 'E1+E2+E5')]
needed = {'K-' + c for pair in pairs for c in pair}

def profile(rec, oid, table=new):
    root = labels[oid]['root']
    extra = rec['extra']
    entities = {root}
    for block in rec['blocks'][:3]:
        for group in block['groups']:
            entities.update(group)
    channels = [c for c in extra['kenh_co'] if c['thuc_the'] in entities]
    selected = []
    for entity in sorted(entities):
        values = [c for c in channels if c['thuc_the'] == entity]
        chosen = values if entity == root else sorted(values, key=lambda c: -c['s'])[:4]
        selected.extend(sorted(chosen, key=lambda c: c['ma']))
    units = {c['don_vi'] for c in selected}
    pv = {u['ma']: u for u in extra['don_vi_phan_vi'] if u['ma'] in units}
    count = {u['ma']: u for u in rec['worlds']['P']['don_vi_dem'] if u['ma'] in units}
    root_ch = [c for c in extra['kenh_co'] if c['thuc_the'] == root]
    score = table[rec['config_id']]['ca'][oid]['theo_the_gioi']['P']
    condition = dict(dataset=labels[oid]['dataset'], fault=labels[oid]['loai_loi'], observed=root in rec['sets']['observed_entities'], raw=bool(root_ch), intrinsic=any((c['F_I'] == 1 for c in root_ch)), groups=sorted({c['don_vi'].split('|')[0] for c in root_ch}), classes=sorted({c['lop'] for c in root_ch}), M5=score['M5'])
    return dict(root=root, root_tier=extra['tang_P'].get(root), keys={e: dict(raw=extra['K_raw_P'].get(e), intrinsic=extra['K_I_P'].get(e), tier=extra['tang_P'].get(e)) for e in entities}, blocks=rec['blocks'], channels=selected, PV=pv, counts=count, inherited=[x for x in rec['inherited_by'] if x['thuc_the'] in entities], condition=condition, units=sorted(units), status=rec['status'])
profiles = {}
locations = {}
for path in inputs['that'][0]:
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            rec = json.loads(line)
            cid = rec['config_id']
            oid = rec['opaque_id']
            if cid in needed:
                profiles[cid, oid] = profile(rec, oid)
                locations[cid, oid] = dict(path=path.relative_to(ROOT).as_posix(), line=line_no)
targets = defaultdict(lambda: defaultdict(set))
summary = {}

def rr(table, cid, oid):
    return table['K-' + cid]['ca'][oid]['theo_the_gioi']['P']['RR']
for a, b in pairs:
    key = a + '|' + b
    changed = {}
    tp = set(b.split('+')) - set(a.split('+')) if a != 'R0' else set(b.split('+'))
    ex = set().union(*(set(law['E_X'][t]) for t in tp))
    for oid, lab in labels.items():
        vals = [rr(table, cid, oid) for table, cid in ((old, a), (old, b), (new, a), (new, b))]
        d0, d1 = (vals[1] - vals[0], vals[3] - vals[2])
        changed[oid] = dict(dataset=lab['dataset'], cell=lab['o'], RR=vals, delta_E4=d0, delta_z=d1, delta_effect=d1 - d0, in_E_X=lab['o'] in ex)
    for dataset in ('RE2-TT', 'Nezha-OB'):
        eligible = [oid for oid in labels if labels[oid]['dataset'] == dataset]
        for field in ('delta_z', 'delta_effect'):
            for sign in (-1, 1):
                candidates = [oid for oid in eligible if sign * changed[oid][field] > 0]
                if candidates:
                    oid = max(candidates, key=lambda o: (sign * changed[o][field], o))
                    targets[key][oid].add(dataset + '/' + field + ('/positive' if sign > 0 else '/negative'))
    controls = {}
    for oid in list(targets[key]):
        eligible = [o for o in labels if labels[o]['dataset'] == labels[oid]['dataset']]
        condition = profiles['K-' + a, oid]['condition']
        candidates = [o for o in eligible if o != oid and profiles['K-' + a, o]['condition'] == condition and (new['K-' + a]['ca'][o]['theo_the_gioi']['P']['hit1'] == 1) and (new['K-' + b]['ca'][o]['theo_the_gioi']['P']['hit1'] == 1)]
        candidates.sort(key=lambda o: (labels[o]['o'] != labels[oid]['o'], o))
        control = candidates[0] if candidates else None
        controls[oid] = control
        if control:
            targets[key][control].add('correct_matched_control_for/' + oid)
    summary[key] = dict(per_case=changed, controls=controls)
frames = {}
old_ids = sorted(new)
for key, case_ids in targets.items():
    for oid in case_ids:
        for cid in ('K-' + x for x in key.split('|')):
            frame_key = cid + '|' + oid
            if frame_key in frames:
                continue
            old_path = ROOT / f'results/T-047/runs/b3-k-c1-that-001/cases/{oid}/phase1/records/{old_ids.index(cid):05d}.json'
            rel = old_path.relative_to(ROOT).as_posix()
            assert sha(old_path) == old_manifest[rel]['sha256']
            rec = read(old_path)
            assert rec['config_id'] == cid and rec['opaque_id'] == oid
            frames[frame_key] = dict(old=profile(rec, oid, old), new=profiles[cid, oid], native_old=dict(path=rel), native_new=locations[cid, oid])
required = {tuple(key.split('|', 1)) for key in frames}
for path in inputs['that'][1]:
    with gzip.open(path, 'rt', encoding='utf-8') as f:
        for line_no, line in enumerate(f, 1):
            row = json.loads(line)
            cid, oid = (row['config_id'], row['opaque_id'])
            if (cid, oid) not in required:
                continue
            frame = frames[cid + '|' + oid]
            units = set(frame['old']['units']) | set(frame['new']['units'])
            frame['samples'] = {u: v for u, v in row['trace']['phan_vi'].items() if u in units}
            frame['input_sha256'] = row['trace']['normalized_input_sha256']
            frame['trace_source'] = dict(path=path.relative_to(ROOT).as_posix(), line=line_no)
for key, case_ids in targets.items():
    summary[key]['examples'] = {oid: dict(reasons=sorted(reasons), frames=[cid + '|' + oid for cid in ('K-' + x for x in key.split('|'))]) for oid, reasons in case_ids.items()}
doc = dict(seal_sha256=seal_hash, pairs=summary, frames=frames, notes=['Chọn ví dụ theo thay đổi RR toàn bộ ca; giữ cờ in_E_X riêng cho luật', 'Đối chứng đúng ghép cùng chữ ký tín hiệu trên vế tắt dưới z; thiếu đối chứng ghi null', 'Frame đầu vào và trung gian là quan sát; quy nguyên nhân cần đọc code và xét giải thích khác'])
raw = json.dumps(ma_hoa_json(doc), ensure_ascii=False).encode()
path = args.out.resolve()
assert path.is_relative_to(base.resolve())
with path.open('xb') as stream:
    stream.write(raw)
print('PAIRED ANALYSIS', len(frames), 'frames', len(pairs), 'pairs')
