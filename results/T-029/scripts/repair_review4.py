"""Approved T029 report-only repair; frozen scientific outputs are read-only."""
import argparse
import difflib
import hashlib
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-029'
TASK = ROOT / 'tasks/T-029-p4-han-che-phat-hien'
RUN = OUT / 'runs/review4-repair-001'
LOG = TASK / 'LOG.md'
REPORTS = ['ban-do-han-che-phat-hien.md', 'doc-tay.md', 'dinh-vi.md']


def audit(message):
    with LOG.open('a', encoding='utf-8') as f:
        f.write('\n- ' + datetime.now(timezone(timedelta(hours=7))).isoformat() + ' — Phiên10: ' + message + '\n')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def new(path, value):
    path = Path(path)
    assert not path.exists(), path
    path.parent.mkdir(parents=True, exist_ok=True)
    data = value if isinstance(value, bytes) else (value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')
    path.write_bytes(data)
    audit('Ghi mới ' + path.relative_to(ROOT).as_posix())


def replace_once(text, old, value):
    assert text.count(old) == 1, (old[:120], text.count(old))
    return text.replace(old, value, 1)


def pointer(doc, path):
    for k in path.lstrip('/').split('/') if path else []:
        k = k.replace('~1', '/').replace('~0', '~')
        doc = doc[int(k)] if isinstance(doc, list) else doc[k]
    return doc


def esc(text):
    return text.replace('~', '~0').replace('/', '~1')


def prepare():
    audit('Lệnh có ghi: Python -B -X utf8 -W ignore scripts/repair_review4.py prepare; guard toàn bàn giao trước snapshot/tổng hợp, không detector/ranker.')
    assert not RUN.exists(), 'Không ghi đè lượt cũ'
    handoff = read(OUT / 'runs/handoff-session8-001/manifest.json')
    for p, item in handoff['files'].items():
        assert digest(ROOT / p) == item['sha256'] and (ROOT / p).stat().st_size == item['bytes'], p
    final_path = OUT / 'runs/final-verification-001/verification.json'
    assert digest(final_path) == handoff['final_verification_sha256']
    final = read(final_path)
    for p, h in final['src_p3']['tep'].items():
        assert digest(ROOT / p) == h, p
    RUN.mkdir()
    paths = [OUT / n for n in REPORTS] + [TASK / 'REVIEW-4.md', LOG, ROOT / 'docs/STATE.md']
    before = {}
    for p in paths:
        data = p.read_bytes()
        before[p.relative_to(ROOT).as_posix()] = {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)}
        new(RUN / (p.name + '.before'), data)
    protected = [ROOT / 'AGENTS.md', TASK / 'SPEC.md', TASK / 'REVIEW.md', TASK / 'REVIEW-2.md', TASK / 'REVIEW-3.md', ROOT / 'docs/WHY.md', ROOT / 'docs/DECISIONS.md']
    new(RUN / 'before.json', {'files': before, 'protected': {p.relative_to(ROOT).as_posix(): digest(p) for p in protected}, 'handoff_file_count': len(handoff['files']), 'handoff_manifest_sha256': digest(OUT / 'runs/handoff-session8-001/manifest.json')})
    boc = read(OUT / 'bocpd-can-thiep.json')['cases']
    rows = [x for x in read(OUT / 'theo-ca.json')['rows'] if x['detector'] == 'bocpd']
    grouped = defaultdict(list)
    for row in rows:
        grouped[row['cell']].append(row)

    def intervention(items):
        counts = Counter()
        first = Counter()
        totals = Counter()
        for row in items:
            c = boc[row['opaque_id']]
            delta = c['cp_counts_Nv']['I1'] - c['cp_counts_Nv']['full']
            counts['more' if delta > 0 else 'less' if delta < 0 else 'equal'] += 1
            t = min(c['I1']) - row['t_hat_index']
            first['earlier' if t < 0 else 'later' if t > 0 else 'equal'] += 1
            totals.update(c['cp_counts_Nv'])
        return {'n': len(items), 'Nv_totals': dict(totals), 'Nv_change': {k: counts[k] for k in ('more', 'equal', 'less')}, 'first_change': {k: first[k] for k in ('earlier', 'equal', 'later')}}

    summary = {'intervention': {'all': intervention(rows), 'by_cell': {k: intervention(v) for k, v in sorted(grouped.items())}, 'S': [], 'B2': {'n': sum(x['flags_flat']['B2/5'] is True for x in rows), 'I1_first_earlier': sum(x['flags_flat']['B2/5'] is True and min(boc[x['opaque_id']]['I1']) < x['t_hat_index'] for x in rows)}}, 'coverage': {}, 'coverage_cases': {}, 'B4_equal': []}
    for row in rows:
        if row['first_group'] == 'S':
            c = boc[row['opaque_id']]
            summary['intervention']['S'].append({'opaque_id': row['opaque_id'], 'cell': row['cell'], 'full_first': row['t_hat_index'], 'I1_first': min(c['I1']), 'full_Nv': c['cp_counts_Nv']['full'], 'I1_Nv': c['cp_counts_Nv']['I1']})
    summary['intervention']['S_count'] = len(summary['intervention']['S'])
    ns = read(OUT / 'n-sigma-cot.json')['cases']
    loc = read(OUT / 'dinh-vi.json')['cases']
    for det in ('nsigma', 'nsigma_doi_chung'):
        summary['coverage'][det] = {}
        summary['coverage_cases'][det] = {}
        for oid, c in sorted(ns.items()):
            summary['coverage_cases'][det][oid] = {}
            for var, services in c[det]['E_services'].items():
                active = sum(x['so_cot'] > 0 for x in services.values())
                summary['coverage_cases'][det][oid][var] = {'active': active, 'inactive': len(services) - active, 'root_columns': services[loc[oid]['root']]['so_cot'], 'U': len(services)}
        for var in ('baseline', '5', '10', '20'):
            cs = [x[var] for x in summary['coverage_cases'][det].values()]
            summary['coverage'][det][var] = {'n': len(cs), 'active_min': min(x['active'] for x in cs), 'active_max': max(x['active'] for x in cs), 'inactive_min': min(x['inactive'] for x in cs), 'inactive_max': max(x['inactive'] for x in cs), 'root_without_columns': sum(x['root_columns'] == 0 for x in cs), 'U': cs[0]['U']}
    v7 = read(OUT / 'runs/step5-001/V7.json')
    for oid, c in v7['cases'].items():
        q = c['B4']['60']['2']
        if q['at_first_valid'] and q['control_n'] and int(q['at_first']) * q['control_n'] == q['control_true']:
            summary['B4_equal'].append({'opaque_id': oid, 'true': q['control_true'], 'n': q['control_n'], 'at_first': q['at_first']})
    summary['B4_equal_count'] = len(summary['B4_equal'])
    sources = ['bocpd-can-thiep.json', 'theo-ca.json', 'n-sigma-cot.json', 'dinh-vi.json', 'runs/step5-001/V7.json']
    summary['source_hashes'] = {(OUT / p).relative_to(ROOT).as_posix(): digest(OUT / p) for p in sources}
    summary['source_pointers'] = {'intervention': 'bocpd-can-thiep.json#/cases/<ca>/{full,I1,cp_counts_Nv}; theo-ca.json#/rows', 'coverage': 'n-sigma-cot.json#/cases/<ca>/<det>/E_services/<variant>/<service>/{so_cot,first_after_index}; dinh-vi.json#/cases/<ca>/root', 'B4_equal': 'runs/step5-001/V7.json#/cases/<ca>/B4/60/2'}
    new(RUN / 'summary.json', summary)
    print(json.dumps({'status': 'PREPARED', 'intervention': summary['intervention']['all'], 'coverage': summary['coverage'], 'B4_equal_count': summary['B4_equal_count']}, ensure_ascii=False))


class EditedReport:
    def __init__(self, name):
        self.name = name
        self.text = (RUN / (name + '.before')).read_text(encoding='utf-8')
        rel = re.search(r'\]\(([^)]+\.bindings\.json)\)', self.text.splitlines()[0]).group(1)
        self.binding = read(OUT / rel)
        self.next_id = max(int(x['id']) for x in self.binding['bindings']) + 1
        self.summary = read(RUN / 'summary.json')

    def num(self, ptr):
        value = pointer(self.summary, ptr)
        key = str(self.next_id)
        self.next_id += 1
        text = format(value, '.6g')
        self.binding['bindings'].append({'id': key, 'path': (RUN / 'summary.json').relative_to(ROOT).as_posix(), 'pointer': ptr, 'format': '.6g', 'rendered': text})
        return '<!--v8:' + key + '-->' + text + '<!--/v8-->'

    def save(self):
        old_link = re.search(r'\]\(([^)]+\.bindings\.json)\)', self.text.splitlines()[0]).group(1)
        self.text = replace_once(self.text, '](' + old_link + ')', '](' + RUN.relative_to(OUT).as_posix() + '/' + self.name + '.bindings.json)')
        self.binding['source_hashes'][(RUN / 'summary.json').relative_to(ROOT).as_posix()] = digest(RUN / 'summary.json')
        new(RUN / (self.name + '.bindings.json'), self.binding)
        new(RUN / (self.name + '.diff'), ''.join(difflib.unified_diff((RUN / (self.name + '.before')).read_text(encoding='utf-8').splitlines(True), self.text.splitlines(True), fromfile=self.name + '.before', tofile=self.name)))
        (OUT / self.name).write_text(self.text, encoding='utf-8', newline='\n')
        audit('Sửa đúng báo cáo đã duyệt ' + self.name + '; diff/binding mới ở review4-repair-001; không sửa scalar cũ.')


def direction(report):
    n = report.num
    return ('Khi cắt sau mốc theo I1, báo đầu sớm hơn ở ' + n('/intervention/all/first_change/earlier') + '/' + n('/intervention/all/n') + ' ca, bằng ở ' + n('/intervention/all/first_change/equal') + ' ca và muộn hơn ở ' + n('/intervention/all/first_change/later') + ' ca. Số điểm đổi trong Nv tăng/bằng/giảm so với bản đầy đủ lần lượt ở ' + n('/intervention/all/Nv_change/more') + '/' + n('/intervention/all/Nv_change/equal') + '/' + n('/intervention/all/Nv_change/less') + ' ca; tổng full/I1/I2 là ' + n('/intervention/all/Nv_totals/full') + '/' + n('/intervention/all/Nv_totals/I1') + '/' + n('/intervention/all/Nv_totals/I2') + '. Hai đại lượng phải đọc riêng; các ca ngược chiều chỉ thuộc số điểm đổi nền, không thuộc báo đầu trên mẫu này.')


def apply():
    audit('Lệnh có ghi: Python -B -X utf8 -W ignore scripts/repair_review4.py apply; chỉ ba báo cáo/bảng người làm, binding/diff lượt mới; số nguồn đóng băng.')
    s = read(RUN / 'summary.json')
    for p, h in s['source_hashes'].items():
        assert digest(ROOT / p) == h, p
    for name in REPORTS:
        assert digest(OUT / name) == read(RUN / 'before.json')['files'][(OUT / name).relative_to(ROOT).as_posix()]['sha256'], name
    r = EditedReport(REPORTS[0])
    r.text = replace_once(r.text, 'Báo động đầu thường nằm trước mốc tiêm theo nhãn proxy. BOCPD nhạy với dữ liệu sau mốc qua tiền xử lý; N-Sigma có nhiều báo động nền, nhưng các cờ chưa tách được nguyên nhân thống kê. Bước nhảy telemetry B4 cũng phổ biến ở điểm không báo. Vì vậy bản đồ dưới đây phân biệt bằng chứng can thiệp, liên hệ, đọc tay và phần chưa kiểm.', 'Báo động đầu thường nằm trước mốc tiêm theo nhãn proxy. Trên mẫu đã kiểm, tiền xử lý toàn chuỗi của BOCPD cho báo đầu muộn hơn hoặc bằng so với I1 cắt sau mốc; tổng số điểm đổi nền ít hơn nhưng có ca ngược chiều. B2 cho biết vị trí báo đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý, chưa giải thích sự tồn tại của báo động trước mốc. N-Sigma có nhiều báo động nền, nhưng các cờ chưa tách được nguyên nhân thống kê. B4 mô tả bước nhảy telemetry và cũng phổ biến ở điểm không báo; không dùng riêng cờ này làm lời giải thích. Bản đồ phân biệt bằng chứng can thiệp, liên hệ, đọc tay và phần chưa kiểm.')
    anchor = 'Nguồn bảng: `theo-ca.json#/per_detector/<bộ>/cell/<ô>` và `runs/report-main-001/summary.json#/delay`.'
    p = 'Các ca S của BOCPD có điều kiện theo tiền xử lý toàn chuỗi: cả ' + r.num('/intervention/S_count') + ' ca đều có báo động trước mốc trong I1. Bảng sau giữ từng ca; không đổi phân loại hay số T-025. I1 vẫn nhìn trước bên trong tiền tố, nên đây không là chất lượng online.\n\n| Ca / ô | Báo đầu full | Báo đầu I1 | Điểm đổi Nv full | Điểm đổi Nv I1 |\n|---|---|---|---|---|\n'
    for i, c in enumerate(s['intervention']['S']):
        p += '| ' + c['opaque_id'] + ' / ' + c['cell'].replace('|', ' / ') + ' | ' + ' | '.join(r.num('/intervention/S/' + str(i) + '/' + k) for k in ('full_first', 'I1_first', 'full_Nv', 'I1_Nv')) + ' |\n'
    p += '\nNguồn: `runs/review4-repair-001/summary.json#/intervention/S`; số gốc `bocpd-can-thiep.json#/cases/<ca>/{full,I1,cp_counts_Nv}`.\n\n'
    r.text = replace_once(r.text, anchor, p + anchor)
    r.text = replace_once(r.text, 'Danh sách cờ là đa nhãn, không là thứ tự nguyên nhân trội. D0 ở S có thể do tất cả cờ BOCPD không có miền hợp lệ.', 'Danh sách cờ là đa nhãn ở cấu hình chính, không là thứ tự nguyên nhân trội hoặc số ca đã giải thích. Với nhóm E, D0 là một phần của nhóm chưa giải thích; có cờ chưa đồng nghĩa đã giải thích sự tồn tại của báo động trước mốc. D0 ở S có thể do các cờ BOCPD không có miền hợp lệ, nên phải tách S/E và không gộp D0 ở S thành thất bại báo sớm.')
    r.text = replace_once(r.text, 'Cắt sau mốc làm mất điểm đổi quanh t̂ ở các ca B2.', 'Vị trí báo đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý; cắt sau mốc làm mất điểm đổi quanh t̂ ở các ca B2 nhưng có báo đầu sớm hơn. B2 chưa giải thích vì sao tồn tại báo động trước mốc; chiều can thiệp và điều kiện của S được báo riêng dưới đây.')
    r.text = replace_once(r.text, 'I1 đổi đồng thời bộ cột và min–max; vẫn nhìn dữ liệu sau t̂ trong tiền tố. B2 sai chưa loại look-ahead.', 'I1 đổi bộ cột và min–max, kéo theo số chiều của prior; vẫn nhìn dữ liệu sau t̂ trong tiền tố. B2 sai chưa loại look-ahead; không suy bỏ nhìn trước sẽ giảm báo sai.')
    r.text = replace_once(r.text, 'Có bước median lớn; V7 không cho quy mọi cờ thành lời giải thích.', 'Mô tả bước median lớn. Cờ phổ biến ở điểm không báo và đổi chiều theo ô/độ nhạy; không dùng B4 riêng làm lời giải thích sự tồn tại của báo động trước mốc.')
    r.text = replace_once(r.text, 'Không ép vào cơ chế. S và E phải tách; miền N/A không là cờ âm.', 'Với E, D0 thuộc nhóm chưa giải thích nhưng không bao hết nhóm đó: có cờ cũng chưa chắc đã giải thích. Với S, D0 có thể do miền N/A; không tính thành thất bại báo sớm. Không ép vào cơ chế; N/A không là cờ âm.')
    anchor = '### Số HP theo từng ô'
    block = '### Chiều can thiệp I1: theo ô và tổng gộp\n\n| Ô | Ca | Điểm đổi Nv full | I1 | I2 | Báo đầu I1 sớm / bằng / muộn | Số điểm đổi I1 tăng / bằng / giảm |\n|---|---|---|---|---|---|---|\n'
    for cell in s['intervention']['by_cell']:
        base = '/intervention/by_cell/' + esc(cell)
        block += '| ' + cell.replace('|', ' / ') + ' | ' + r.num(base + '/n') + ' | ' + ' | '.join(r.num(base + '/Nv_totals/' + k) for k in ('full', 'I1', 'I2')) + ' | ' + ' / '.join(r.num(base + '/first_change/' + k) for k in ('earlier', 'equal', 'later')) + ' | ' + ' / '.join(r.num(base + '/Nv_change/' + k) for k in ('more', 'equal', 'less')) + ' |\n'
    block += '\n' + direction(r) + ' Cả ' + r.num('/intervention/B2/I1_first_earlier') + '/' + r.num('/intervention/B2/n') + ' ca B2 chính có báo đầu sớm hơn trong I1. Đây là tác động lên đầu ra detector qua tiền xử lý, không xác nhận nguyên nhân vận hành của báo sớm.\n\nNguồn: `runs/review4-repair-001/summary.json#/intervention`; từng ca gốc ở `bocpd-can-thiep.json#/cases` và bảng B5/I1/I2 cuối báo cáo. I1 không loại nhìn trước bên trong tiền tố.\n\n'
    r.text = replace_once(r.text, anchor, block + anchor)
    old = 'B1 chỉ xét cửa sổ quanh i nằm trong Nv.'
    r.text = replace_once(r.text, old, 'Bằng nhau đúng số chỉ là dấu mô tả để chọn ca đọc tay, không là kiểm định tương đương. Chưa bằng nhau không chứng minh cờ phân biệt; không đặt ngưỡng gần bằng. B4 vẫn giữ trong cờ cấu hình chính để mô tả, không là số ca đã giải thích. ' + old)
    old = 'Không kết luận nhân quả, lan hoặc giá trị đồ thị từ bảng này.'
    r.text = replace_once(r.text, old, 'Mức nền giữ toàn universe, gồm dịch vụ không có cột và không thể báo; chênh lệch với mức nền chưa tách giá trị detector khỏi thông tin tập cột. Coverage từng ca/bộ/độ nhạy được bổ sung ở định vị; không thay mức nền đã khóa. ' + old)
    r.save()
    r = EditedReport(REPORTS[1])
    old = '“Không phân biệt” dùng khi tỉ lệ đúng bằng nhau, không là kiểm định tương đương. B1 không trúng và đối chứng cũng không trúng chỉ cho biết cờ vắng. Với B4 ở cấu hình w60/k2, ca dev-16597725c1 và dev-746fd74313 có cờ ở mọi điểm không báo hợp lệ: không phân biệt, không dùng cờ này để giải thích báo động. Các cấu hình khác vẫn phải xem tỉ lệ cạnh nhau, không tự gọi phân biệt vì chưa bằng đúng số.'
    para = '“Không phân biệt đúng số” là dấu mô tả/chọn ca khi tỉ lệ bằng nhau, không là kiểm định tương đương. B1 không trúng và đối chứng cũng không trúng chỉ cho biết cờ vắng. Với B4 ở cấu hình w60/k2, có ' + r.num('/B4_equal_count') + ' ca có cờ tại báo đầu và mọi điểm không báo hợp lệ: ' + ', '.join(c['opaque_id'] for c in s['B4_equal']) + '. Không dùng riêng cờ này để giải thích báo động. Chưa bằng đúng số không chứng minh phân biệt; mọi cấu hình vẫn phải đọc hai tỉ lệ cạnh nhau. Không đặt ngưỡng gần bằng. Nguồn: `runs/step5-001/V7.json#/cases/<ca>/B4/60/2` và `runs/manual-selection-001/selection.json#/literal_non_discriminating`.'
    r.text = replace_once(r.text, old, para)
    anchor = '## dev-03d4910932 / bocpd'
    para = '## Tổng quan BOCPD trước khi đọc từng ca\n\n' + direction(r) + ' B2 xác nhận vị trí báo đầu phụ thuộc dữ liệu sau mốc qua tiền xử lý, chưa giải thích sự tồn tại báo sớm; I1 vẫn nhìn trước bên trong tiền tố và đổi cả bộ cột/min–max/số chiều prior. Cả ' + r.num('/intervention/S_count') + ' ca S đều có báo trước mốc trong I1; phân loại S của bản đầy đủ có điều kiện theo tiền xử lý toàn chuỗi.\n\nVới E, D0 là một phần nhóm chưa giải thích; có cờ B2/B4 hoặc N1–N3 chưa đồng nghĩa đã giải thích sự tồn tại của báo trước mốc. D0 ở S phải đọc riêng vì có thể do cờ nằm ngoài miền hợp lệ. B4 là mô tả telemetry, không dùng riêng làm lời giải thích. Không đổi cờ, danh sách đọc tay hoặc nhãn P3.\n\nNguồn: `runs/review4-repair-001/summary.json#/intervention`, `bocpd-can-thiep.json#/cases`, `theo-ca.json#/rows`; bảng theo ca/ô ở báo cáo chính và các mục đọc tay phía dưới.\n\n'
    r.text = replace_once(r.text, anchor, para + anchor)
    r.save()
    r = EditedReport(REPORTS[2])
    anchor = '## N-Sigma chính: theo ô'
    para = '## Coverage của mức nền: giữ universe đã khóa\n\nMức nền trên toàn U gồm cả dịch vụ không có cột và không thể báo. Chênh so mức nền chưa tách thông tin tập cột khỏi giá trị detector; không dùng độ lớn chênh đó như tác động riêng của detector. Bảng dưới giữ từng bộ và mức bỏ N2, rồi đầy đủ từng ca. Dịch vụ hết cột vẫn ở U và đồng hạng không báo theo SPEC.\n\n| Bộ / mức | Ca | Có cột: min–max | Không có cột: min–max | Ca root hết cột |\n|---|---|---|---|---|\n'
    names = {'nsigma': 'N-Sigma chính', 'nsigma_doi_chung': 'N-Sigma đối chứng'}
    vars = {'baseline': 'Giữ cột', '5': 'Bỏ N2 mức 5·p0', '10': 'Bỏ N2 mức 10·p0', '20': 'Bỏ N2 mức 20·p0'}
    for det in names:
        for var in vars:
            base = '/coverage/' + det + '/' + var
            para += '| ' + names[det] + ' / ' + vars[var] + ' | ' + r.num(base + '/n') + ' | ' + r.num(base + '/active_min') + '–' + r.num(base + '/active_max') + ' | ' + r.num(base + '/inactive_min') + '–' + r.num(base + '/inactive_max') + ' | ' + r.num(base + '/root_without_columns') + ' |\n'
    for det in names:
        para += '\n### ' + names[det] + ': coverage từng ca\n\nCác cột lần lượt là giữ cột và các mức bỏ N2 đã khai. Root còn cột không có nghĩa root có báo động.\n\n| Ca | Có cột: giữ | Bỏ N2 mức 5·p0 | Bỏ N2 mức 10·p0 | Bỏ N2 mức 20·p0 | Cột root: giữ | Bỏ N2 mức 5·p0 | Bỏ N2 mức 10·p0 | Bỏ N2 mức 20·p0 |\n|---|---|---|---|---|---|---|---|---|\n'
        for oid in s['coverage_cases'][det]:
            base = '/coverage_cases/' + det + '/' + oid
            para += '| ' + oid + ' | ' + ' | '.join(r.num(base + '/' + var + '/' + key) for key in ('active', 'root_columns') for var in vars) + ' |\n'
    para += '\nNguồn: `runs/review4-repair-001/summary.json#/coverage` và `#/coverage_cases`; đếm trực tiếp `n-sigma-cot.json#/cases/<ca>/<bộ>/E_services/<mức>/<dịch-vụ>/so_cot`, nối root chỉ để đánh giá từ `dinh-vi.json#/cases/<ca>/root`. Số không có cột bằng kích thước U trừ số có cột; không loại dịch vụ khỏi U.\n\nKhông bổ sung hoặc thay mức nền. Nếu sau này xét mức nền chỉ hoán vị root giữa dịch vụ có cột nhưng giữ U, phải giữ cùng hạng/khối hòa của quan sát để so trực tiếp. Thu hẹp U là đại lượng khác và cần tính lại cả hạng quan sát. Khi root hết cột, giả định root thuộc nhóm có cột không đúng cho ca đó; không tự loại ca theo nhãn.\n\n'
    r.text = replace_once(r.text, anchor, para + anchor)
    r.save()
    path = TASK / 'REVIEW-4.md'
    text = path.read_text(encoding='utf-8')
    text = replace_once(text, 'D0 chỉ có nghĩa không có cờ chính, không là số ca chưa giải thích.', 'D0 là không có cờ chính; với nhóm E, D0 là một phần của nhóm chưa giải thích, không phải toàn bộ nhóm đó. Có cờ cũng chưa đồng nghĩa đã giải thích sự tồn tại báo trước mốc. D0 ở S phải đọc riêng vì có thể ngoài miền hợp lệ.')
    text = replace_once(text, 'Nếu thật thu hẹp universe về nhóm có cột, hạng nền trung bình là 14,1; đó là phép so khác.', 'Nếu thật thu hẹp universe về nhóm có cột, hạng nền trung bình là 14,1; đó là phép so khác và chỉ so được khi tính lại cả hạng quan sát trong U đã thu hẹp.')
    lines = text.splitlines()
    notes = {'R1': 'Claude đính chính qua phản hồi do Minh cung cấp: prior cố định theo số chiều, không tuyệt đối giống nhau khi đổi bộ cột; giữ kết luận can thiệp qua tiền xử lý.', 'R2': 'Claude đính chính qua phản hồi do Minh cung cấp: B4 không bao giờ bật là sai ở cấp ca; đúng là không bật ở cấu hình chính và cấp gộp. Các ca bằng đúng số đã được đối chiếu trong LOG phiên 9 và phần sửa này.', 'R3': 'Claude đính chính qua phản hồi do Minh cung cấp: đối chứng đủ cột không đúng ở mọi độ nhạy; phạm vi R3 rộng hơn phát biểu ban đầu. Giữ U mới so trực tiếp được với hạng quan sát hiện tại.'}
    for i, line in enumerate(lines):
        for key, note in notes.items():
            if line.startswith('| ' + key + ' |'):
                assert line.endswith('| |')
                lines[i] = line[:-3] + ' ' + note + ' | Minh duyệt sửa 09/10/2026; đã sửa, chờ rà soát độc lập. |'
    while lines and not lines[-1].strip():
        lines.pop()
    text = '\n'.join(lines) + '\n'
    text += '| P1 | Đúng về cần ghi rõ; KHÔNG CHẶN | Tách báo đầu 29/1/0 khỏi số điểm đổi nền 23/3/4. “Đa số” đúng nhưng chưa đủ rõ; ngoại lệ ngược chiều chỉ thuộc số điểm đổi. Nguồn và lệnh ở LOG phiên 9, lượt review4-repair-001/summary.json#/intervention/all. Đã sửa hai đại lượng riêng trong báo cáo chính và đọc tay. | Minh duyệt sửa 09/10/2026; đã sửa, chờ rà soát độc lập. |\n'
    text += '| P2 | Đúng; KHÔNG CHẶN | Sửa câu phủ định quá mạnh về D0: với E, D0 là một phần nhóm chưa giải thích; có cờ chưa chắc đã giải thích sự tồn tại báo sớm. Tách D0 ở S vì miền N/A không là thất bại báo sớm. Đã sửa HP-9, chú giải bảng và đọc tay; giữ nhãn D0/cờ. Nguồn: SPEC Quy tắc chung/Rủi ro, theo-ca.json#/rows; đính chính Claude do Minh cung cấp lưu ở LOG phiên 10. | Minh duyệt sửa 09/10/2026; đã sửa, chờ rà soát độc lập. |\n'
    new(RUN / 'REVIEW-4.md.diff', ''.join(difflib.unified_diff((RUN / 'REVIEW-4.md.before').read_text(encoding='utf-8').splitlines(True), text.splitlines(True), fromfile='REVIEW-4.md.before', tofile='REVIEW-4.md')))
    path.write_text(text, encoding='utf-8', newline='\n')
    audit('Sửa chỉ bảng người làm REVIEW-4: chỉnh P1/P2, ghi đính chính nguồn Claude do Minh cung cấp và Minh duyệt; phần reviewer trước bảng giữ nguyên.')
    new(RUN / 'applied.json', {'status': 'APPLIED', 'reports': {n: digest(OUT / n) for n in REPORTS}, 'review_sha256': digest(path), 'summary_sha256': digest(RUN / 'summary.json'), 'script_sha256': digest(__file__)})
    print(json.dumps({'status': 'APPLIED', 'reports': REPORTS}, ensure_ascii=False))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('phase', choices=['prepare', 'apply'])
    args = ap.parse_args()
    try:
        (prepare if args.phase == 'prepare' else apply)()
    except Exception as exc:
        audit('DỪNG repair_review4 ' + args.phase + ': ' + type(exc).__name__ + ': ' + str(exc) + '; giữ mọi tệp, không ghi đè lượt.')
        raise
