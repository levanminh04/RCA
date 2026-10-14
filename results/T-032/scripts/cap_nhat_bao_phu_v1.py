#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""T-032, phiên 12 — cập nhật trạng thái đọc trong bao-phu-nhom.json.

Chỉ đổi các trường trạng thái đọc; danh mục nhóm, đơn vị, cặp đối chứng và điều kiện ghép giữ nguyên.
Tự kiểm: sau khi bỏ các trường được phép đổi, nội dung cũ và mới phải bằng nhau.

Dùng: python3 -B -X utf8 cap_nhat_bao_phu_v1.py <bao-phu-nhom.json cũ> <ke-hoach-doc-tay.json> <file ra>
"""
import copy
import hashlib
import json
import sys

old_path, plan_path, out_path = sys.argv[1:4]
raw = open(old_path, 'rb').read()
old = json.loads(raw.decode('utf-8'))
plan = json.load(open(plan_path, encoding='utf-8'))
new = copy.deepcopy(old)

read_units = {p['unit_id']: p for p in plan['don_vi_doc']}
gplan = {g['group_id']: g for g in plan['nhom']}
ALLOWED_TOP = {'status', 'reading_update'}
ALLOWED_GROUP = {'reading_status', 'coverage_after_reading', 'reading_units'}
ALLOWED_UNIT = {'reading_status'}
ALLOWED_PAIR = {'reading_status'}

new['status'] = 'CATALOG_LOCKED_READING_DONE_PHIEN_12'
new['reading_update'] = {
    'at': 'phiên 12, 11/10/2026',
    'previous_sha256': hashlib.sha256(raw).hexdigest(),
    'rule': plan['quy_tac'],
    'n_units_read_by_hand': len(read_units),
    'doc': 'results/T-032/doc-tay.md',
    'table': 'results/T-032/doi-chieu-dung-sai.json',
    'note': 'Chỉ các trường reading_status, coverage_after_reading, reading_units, status và reading_update được đổi so với bản đã khóa. mechanism_established giữ false ở mọi nhóm: kết luận cơ chế nằm trong báo cáo, không gắn theo nhóm cờ.'}
for g in new['groups']:
    gp = gplan[g['group_id']]
    g['reading_units'] = [{'wrong_unit_id': r['don_vi_sai_doc'], 'path_signature': r['duong_di'],
                           'n_units_same_signature': r['so_don_vi_cung_duong_di'],
                           'control_unit_id': (r['doi_chung_doc'] or {}).get('unit_id'),
                           'control_same_cell': (r['doi_chung_doc'] or {}).get('cung_o'),
                           'missing_control_reason': r['ly_do_thieu_doi_chung']} for r in gp['doc_tay']]
    g['reading_status'] = 'đã đọc %d/%d đơn vị sai (mỗi đường đi một đơn vị); các đơn vị còn lại chỉ có trong bảng tự động' % (
        len(gp['doc_tay']), gp['so_don_vi_sai'])
    g['coverage_after_reading'] = 'Bảng tự động phủ mọi đơn vị của nhóm; đọc tay phủ %d đường đi. Không suy cơ chế cả nhóm từ đơn vị đại diện.' % gp['so_duong_di_khac_nhau']
for u in new['units']:
    u['reading_status'] = 'đã đọc tay (phiên 12)' if u['unit_id'] in read_units else 'chỉ có trong bảng tự động (phiên 12)'
reads = {(r['don_vi_sai_doc'], g['k']) for g in plan['nhom'] for r in g['doc_tay']}
for p in new['counterpart_pairs']:
    p['reading_status'] = 'đã đọc đơn vị sai và đối chứng đầu tiên (phiên 12)' if (p['wrong_unit_id'], p['k']) in reads else 'chỉ có trong bảng tự động (phiên 12)'


def strip(d):
    d = copy.deepcopy(d)
    for k in ALLOWED_TOP:
        d.pop(k, None)
    for g in d['groups']:
        for k in ALLOWED_GROUP:
            g.pop(k, None)
    for u in d['units']:
        for k in ALLOWED_UNIT:
            u.pop(k, None)
    for p in d['counterpart_pairs']:
        for k in ALLOWED_PAIR:
            p.pop(k, None)
    return d


assert strip(old) == strip(new), 'nội dung ngoài các trường trạng thái đọc đã bị đổi'
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    json.dump(new, f, ensure_ascii=False, indent=1)
    f.write('\n')
print('OK: chỉ trường trạng thái đọc đổi; nhóm', len(new['groups']), 'đơn vị', len(new['units']), 'đã đọc', len(read_units),
      'cặp đã đọc', sum(1 for p in new['counterpart_pairs'] if p['reading_status'].startswith('đã đọc')))
