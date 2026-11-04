"""Bảng 2×2 tại P của T-047; chỉ hậu xử lý, không chạy phương pháp.

CLI: --that <lượt K đủ 16×52> --ra <results/T-047/so-sanh-t045.json>.
Kiểm hash pha 1 và dòng LOG trước khi nạp nhãn. Đọc T-045 từng cấu hình,
kiểm mỗi tệp theo manifest; không dùng MRR đã chấm làm đầu vào.
"""
import argparse
import collections
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT / 'src'), str(ROOT / 'results/T-047/scripts'),
                str(ROOT / 'results/T-045/scripts')]
import adapter_t047 as ad
import pha2_khoi_k as pk
import tep_pha1
from m1 import xep_hang
from m1_danh_gia import rr

CELLS = ('G0D0_S0', 'G0D0_S1', 'G3D1_S0', 'G3D1_S1')
PAIRS = {'S1_tru_S0_G0D0': ('G0D0_S0', 'G0D0_S1'),
         'S1_tru_S0_G3D1': ('G3D1_S0', 'G3D1_S1'),
         'G3D1_tru_G0D0_S0': ('G0D0_S0', 'G3D1_S0'),
         'G3D1_tru_G0D0_S1': ('G0D0_S1', 'G3D1_S1')}


def sha_file(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def can_cu_pha1(path, log_text):
    """Không nạp nhãn; kiểm tệp tuần tự và quyền chuyển sang pha 2."""
    path = ad.duong_ra(path)
    meta = tep_pha1.kiem(path)
    line = f"- `{path.relative_to(ROOT).as_posix()}`: `{meta['sha256']}`"
    if line not in log_text:
        raise ValueError('hash pha 1 chưa được ghi LOG; chưa được đọc nhãn')
    if meta['so_ca'] != 52 or meta['so_ban_ghi'] != 16 * 52:
        raise ValueError('bảng 2×2 cần đủ 16 cấu hình × 52 ca thật')
    expected = {'K-' + ('+'.join(c) if c else 'R0')
                for n in range(5) for c in itertools.combinations(('E1', 'E2', 'E3', 'E5'), n)}
    if set(meta['cau_hinh']) != expected:
        raise ValueError('ma trận cấu hình khác khối K đã duyệt')
    return path, meta


def _entities(blocks):
    return [e for b in blocks for g in b['groups'] for e in g]


def kiem_phuc_dung(rec):
    """S0 chiếu từ S1 phải bằng E6a dựng độc lập từ tầng và khóa đã lưu.

    Dùng công thức của xep_hang.xep tại P: (3-tầng, K_I) ở tầng 1,
    (3-tầng, K_raw) ở tầng 2 và (0,0,0,0) ở tầng 3. Không cần
    chạy chuỗi hay đo lại kênh. Thiếu trung gian là OPEN, không suy giá trị.
    """
    ad.kiem_ban_ghi(rec)
    extra = rec.get('extra') or {}
    required = ('tang_P', 'K_I_P', 'K_raw_P')
    if any(not isinstance(extra.get(k), dict) for k in required):
        raise ValueError('OPEN: thiếu tang_P/K_I_P/K_raw_P để kiểm phục dựng S0')
    blocks = rec.get('blocks')
    if not isinstance(blocks, list):
        raise ValueError('OPEN: thiếu blocks S1')
    tang, ki, kr = (extra[k] for k in required)
    entities = _entities(blocks)
    if len(entities) != len(set(entities)) or set(entities) != set(tang) or set(tang) != set(ki) or set(tang) != set(kr):
        raise ValueError('OPEN: tập thực thể của tầng/khóa/blocks không khớp')
    items = []
    for e, t in tang.items():
        if isinstance(t, bool) or t not in (1, 2, 3):
            raise ValueError('OPEN: tầng không hợp lệ')
        for k in (ki[e], kr[e]):
            if not isinstance(k, (list, tuple)) or len(k) != 3 or any(
                    isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) for x in k):
                raise ValueError('OPEN: khóa K_I/K_raw không hợp lệ')
        base = tuple(ki[e] if t == 1 else kr[e] if t == 2 else (0, 0, 0))
        items.append((e, (3 - t,) + base))
    direct = xep_hang._nhom(xep_hang.sap_khoa(items))
    projected = ad.phuc_dung_S0(blocks)
    if projected != direct:
        raise ValueError('OPEN: S0 chiếu từ S1 lệch công thức E6a trên trung gian đã lưu')
    return projected


def _rank_groups(blocks):
    # Các khối E6a có một nhóm hòa; dùng nhóm, không so khóa S0/S1 khác độ dài.
    return tuple(tuple(tuple(sorted(g)) for g in b['groups']) for b in blocks)


def doi_hang(a, b, root):
    """Đổi thứ tự/tập trả về và quan hệ từng thực thể với root, gồm vào/ra hòa."""
    def pos(blocks):
        return {e: (bi, gi) for bi, block in enumerate(blocks)
                for gi, group in enumerate(block['groups']) for e in group}
    pa, pb = pos(a), pos(b)

    def rel(p, e):
        if root not in p:
            return 'root_vang'
        if e not in p:
            return 'vang'
        return 'truoc' if p[e] < p[root] else 'sau' if p[e] > p[root] else 'hoa'
    changes = [{'thuc_the': e, 'truoc': rel(pa, e), 'sau': rel(pb, e)}
               for e in sorted((set(pa) | set(pb)) - {root}) if rel(pa, e) != rel(pb, e)]
    return {'thu_tu_ung_vien_doi': _rank_groups(a) != _rank_groups(b),
            'phan_bo_hang_root_doi': rr.phan_bo(a, root) != rr.phan_bo(b, root),
            'root_vang': {'truoc': root not in pa, 'sau': root not in pb},
            'quan_he_root_doi': changes}


def cham_cau_hinh(cells_by_case, labels, refs=None):
    """Hàm thuần trên bốn ô của cùng tập ca; giữ Fraction tới khi ghi JSON."""
    if not cells_by_case or set(cells_by_case) != set(labels):
        raise ValueError('bốn ô phải dùng cùng tập ca và nhãn')
    case_out, scores = {}, {c: {} for c in CELLS}
    for oid in sorted(cells_by_case):
        cells, label = cells_by_case[oid], labels[oid]
        if set(cells) != set(CELLS):
            raise ValueError('thiếu một trong bốn ô')
        root = label['root']
        for c in CELLS:
            item = cells[c]
            if item.get('status') not in ('OK', 'NO_EVIDENCE', 'ERROR', 'UNSUPPORTED'):
                raise ValueError('trạng thái bản ghi lạ')
            if not isinstance(item.get('blocks'), list):
                raise ValueError('thiếu blocks; không tự đổi thiếu trung gian thành RR=0')
            scores[c][oid] = rr.rr_ca(item['blocks'], root, item['status'] == 'OK')
        delta = {name: scores[b][oid] - scores[a][oid] for name, (a, b) in PAIRS.items()}
        delta['tuong_tac'] = delta['S1_tru_S0_G3D1'] - delta['S1_tru_S0_G0D0']
        case_out[oid] = {'dataset': label['dataset'], 'o': label.get('o'), 'root': root,
                         'RR': {c: scores[c][oid] for c in CELLS},
                         'hang_ky_vong': {c: rr.hang_ky_vong(cells[c]['blocks'], root)
                                         if cells[c]['status'] == 'OK' else None for c in CELLS},
                         'status': {c: cells[c]['status'] for c in CELLS},
                         'chenh_RR': delta,
                         'doi_hang': {name: doi_hang(cells[a]['blocks'], cells[b]['blocks'], root)
                                      for name, (a, b) in PAIRS.items()},
                         'nguon': (refs or {}).get(oid)}
    dataset = sorted({label['dataset'] for label in labels.values()})

    def means(values):
        return {'gop': rr.mrr(values), **{d: rr.mrr(values, {o for o, x in labels.items() if x['dataset'] == d})
                                        for d in dataset}}
    mrr = {c: means(scores[c]) for c in CELLS}
    deltas = {name: {d: mrr[b][d] - mrr[a][d] for d in ('gop', *dataset)}
              for name, (a, b) in PAIRS.items()}
    deltas['tuong_tac'] = {d: deltas['S1_tru_S0_G3D1'][d] - deltas['S1_tru_S0_G0D0'][d]
                           for d in ('gop', *dataset)}
    return {'so_ca': len(labels), 'MRR': mrr, 'chenh_MRR': deltas, 'ca': case_out}


def _iter_records(path):
    with Path(path).open('rb') as f:
        for line, data in enumerate(f, 1):
            if data.strip():
                yield line, json.loads(data)


def _old_manifest():
    path = ROOT / 'results/T-045/manifest.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    return manifest['files'], {'file': path.relative_to(ROOT).as_posix(), 'sha256': sha_file(path)}


def _verified(path, files):
    path = Path(path)
    rel = path.relative_to(ROOT).as_posix()
    if rel not in files or sha_file(path) != files[rel]['sha256']:
        raise ValueError(f'hash T-045 lệch hoặc thiếu manifest: {rel}')
    return path


def old_parts(files):
    """Hash metadata trước khi dùng pk.phan_cua; không ghi lại T-045."""
    out = []
    for run in pk.LUOT_THAT:
        base = pk.RUNS / run
        _verified(base / 'pha1.json', files)
        _verified(base / 'theo-cau-hinh/tach.json', files)
        out.append(pk.phan_cua(run))
    return out


def old_config(cid, parts, files):
    rows, refs, sources = {}, {}, []
    for split in parts:
        if cid not in split:
            raise ValueError(f'T-045 thiếu cấu hình {cid}')
        base = split[cid]
        _verified(base / 'pha1.json', files)
        meta = json.loads((base / 'pha1.json').read_text(encoding='utf-8'))
        source = _verified(base / meta['tep'], files)
        if meta['sha256'] != files[source.relative_to(ROOT).as_posix()]['sha256']:
            raise ValueError('hash tệp tách T-045 khác pha1.json')
        count, local_oids = 0, set()
        for line, rec in _iter_records(source):
            oid = rec['opaque_id']
            if rec['config_id'] != cid or oid in rows:
                raise ValueError('T-045 trùng/lệch cấu hình-ca')
            status = rec.get('status')
            if status not in ('OK', 'NO_EVIDENCE'):
                raise ValueError(f'OPEN: T-045 {cid}/{oid} trạng thái {status}; chưa đủ bốn ô')
            s1 = (rec.get('extra') or {}).get('T4c')
            if not isinstance(rec.get('blocks'), list) or not isinstance(s1, dict) or not isinstance(s1.get('blocks'), list):
                raise ValueError(f'OPEN: T-045 {cid}/{oid} thiếu blocks/T4c.blocks')
            if ad.phuc_dung_S0(s1['blocks']) != rec['blocks']:
                raise ValueError('OPEN: kiểm chiếu S1→S0 trên T-045 không khớp')
            rows[oid] = {'G0D0_S0': {'blocks': rec['blocks'], 'status': status},
                         'G0D0_S1': {'blocks': s1['blocks'], 'status': status}}
            refs[oid] = {'file': source.relative_to(ROOT).as_posix(), 'line': line,
                          'config_id': cid, 'opaque_id': oid,
                          'S0': '/blocks', 'S1': '/extra/T4c/blocks'}
            count += 1
            local_oids.add(oid)
        if count != meta['so_ban_ghi'] or len(local_oids) != meta['so_ca'] or meta['cau_hinh'] != [cid]:
            raise ValueError('metadata tệp tách T-045 không khớp')
        sources.append({'file': source.relative_to(ROOT).as_posix(), 'sha256': meta['sha256']})
    return rows, refs, sources


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--that', required=True)
    ap.add_argument('--ra', required=True)
    args = ap.parse_args()
    output = ad.duong_ra(args.ra)
    if output.exists():
        raise FileExistsError('giữ mọi lượt: chọn đường đầu ra mới, không ghi đè')
    log_text = (ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md').read_text(encoding='utf-8')
    path, meta = can_cu_pha1(args.that, log_text)
    files, mf_source = _old_manifest()
    parts = old_parts(files)
    # Chỉ sau cổng hash+LOG phía trên mới gọi hàm nạp nhãn thật.
    labels = pk.nap_nhan(False)
    if len(labels) != 52 or collections.Counter(x['dataset'] for x in labels.values()) != {'RE2-TT': 30, 'Nezha-OB': 22}:
        raise ValueError('nhãn không khớp 52 ca dev đã duyệt')
    result, old_sources, previous = {}, [], None
    source = path / meta['tep']
    for cid, group in itertools.groupby(_iter_records(source), key=lambda row: row[1]['config_id']):
        if previous is not None and cid <= previous:
            raise ValueError('pha 1 không sắp theo cấu hình; không đọc cả tệp vào RAM')
        previous = cid
        cells, refs = {}, {}
        for line, rec in group:
            oid = rec['opaque_id']
            if oid in cells or oid not in labels:
                raise ValueError('T-047 trùng/khác tập ca dev')
            s0 = kiem_phuc_dung(rec)
            cells[oid] = {'G3D1_S0': {'blocks': s0, 'status': rec['status']},
                           'G3D1_S1': {'blocks': rec['blocks'], 'status': rec['status']}}
            refs[oid] = {'T047': {'file': source.relative_to(ROOT).as_posix(), 'line': line,
                                    'config_id': cid, 'opaque_id': oid, 'S1': '/blocks',
                                    'S0': 'chiếu /blocks, đối chiếu /extra/tang_P + /extra/K_I_P + /extra/K_raw_P'}}
        old, old_refs, used_sources = old_config(cid, parts, files)
        if set(cells) != set(old) or set(cells) != set(labels):
            raise ValueError('bốn ô không cùng 52 ca')
        for oid in cells:
            cells[oid].update(old[oid])
            refs[oid]['T045'] = old_refs[oid]
        result[cid] = cham_cau_hinh(cells, labels, refs)
        old_sources.extend(used_sources)
    if set(result) != set(meta['cau_hinh']):
        raise ValueError('chưa đủ 16 cấu hình trong bảng 2×2')
    out = {'schema': 'T047-so-sanh-2x2-v1', 'the_gioi': 'P', 'cau_hinh': result,
           'nguon': {'T047': {'file': source.relative_to(ROOT).as_posix(), 'sha256': meta['sha256'],
                               'hash_da_ghi_LOG_truoc_nhan': True},
                     'T045_manifest': mf_source, 'T045_records': old_sources,
                     'nhan': [{'file': rel, 'dataset': ds, 'sha256': digest}
                              for rel, (ds, digest) in pk.NHAN.items()]},
           'kiem_phuc_dung': {'T047': 'đối chiếu tất cả 16×52 bản ghi từ tầng và khóa P đã lưu',
                              'T045': 'chiếu T4c.blocks về blocks trên tất cả 16×52 bản ghi'},
           'pham_vi_trung_gian_da_kiem': ['blocks', 'extra.T4c.blocks (T-045)',
                                         'extra.tang_P', 'extra.K_I_P', 'extra.K_raw_P (T-047)'],
           'gioi_han': ['G3 và D1 là một gói; bảng không tách tác động riêng từng cổng.',
                        'Bốn ô chỉ đầy đủ tại P; không tuyên bố đầy đủ tại S_lo/S_hi.',
                        'MRR trên dev tái sử dụng; không xác nhận hiệu quả RCA hoặc cơ chế.',
                        'Không dùng bảng để chọn lại thang, cổng, tham số hay lượt chạy.',
                        'Kiểm trung gian ở đây xác nhận phục dựng thứ hạng; lần theo cơ chế nằm ở co-che-khoi-k.json.']}
    ad.ghi(output, out)
    print(json.dumps({'file': str(output), 'configs': len(result), 'cases_per_config': 52,
                      'reconstruction': 'PASS'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
