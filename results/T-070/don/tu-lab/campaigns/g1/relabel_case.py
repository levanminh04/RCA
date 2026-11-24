#!/usr/bin/env python3
"""One-off relabel of an existing V082 display case (T-068): change exactly two JSON values.

    <du-lieu>/<variant>/<case>.json            #/nguon_ca
    <du-lieu>/<variant>/chi-muc.json           #/su_co/<row of case>/nguon
chi-muc-ban.json is not touched. Both files are checked before anything is written; if the index row or the
case file is missing, or the case file has no `nguon_ca`, nothing is written. Old files are copied to
<file>.bak-<label> first (never overwritten). Files are rewritten with the same serializer as the G1 exporter
(json.dumps ensure_ascii=False, compact separators, trailing newline); the script verifies that only the two
declared values differ after rewrite.

    sudo python3 -B campaigns/g1/relabel_case.py --ca 7ffb2305 --nguon t066 [--ban V082-V066+H8a]
        [--du-lieu /srv/rca-lab/rca-results/t065-l11-001/du-lieu] [--thu]   (--thu: check only, write nothing)
"""
import argparse
import copy
import json
import os
import pathlib
import shutil
import sys


def dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '\n'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ca', required=True)
    ap.add_argument('--nguon', required=True)
    ap.add_argument('--ban', default='V082-V066+H8a')
    ap.add_argument('--du-lieu', default='/srv/rca-lab/rca-results/t065-l11-001/du-lieu')
    ap.add_argument('--thu', action='store_true')
    a = ap.parse_args()
    if not (a.ca.isalnum() and a.nguon.isalnum()):
        sys.exit('mã ca / nhãn không hợp lệ')
    d = pathlib.Path(a.du_lieu) / a.ban
    f_ca, f_idx = d / (a.ca + '.json'), d / 'chi-muc.json'
    if not f_ca.is_file() or not f_idx.is_file():
        sys.exit(f'thiếu file: {f_ca if not f_ca.is_file() else f_idx}; không ghi gì')
    raw_ca, raw_idx = f_ca.read_bytes(), f_idx.read_bytes()
    ca, idx = json.loads(raw_ca), json.loads(raw_idx)
    rows = [i for i, x in enumerate(idx['su_co']) if x['ma'] == a.ca]
    if len(rows) != 1:
        sys.exit(f'chỉ mục có {len(rows)} dòng mã {a.ca}; cần đúng 1; không ghi gì')
    if 'nguon_ca' not in ca:
        sys.exit('file ca không có nguon_ca; không ghi gì')
    if dump(ca).encode() != raw_ca or dump(idx).encode() != raw_idx:
        sys.exit('file hiện tại không theo đúng cách tuần tự hóa của bộ xuất; không ghi gì')
    r = rows[0]
    old = {'nguon_ca': ca['nguon_ca'], 'chi_muc_nguon': idx['su_co'][r]['nguon']}
    new_ca, new_idx = copy.deepcopy(ca), copy.deepcopy(idx)
    new_ca['nguon_ca'] = a.nguon
    new_idx['su_co'][r]['nguon'] = a.nguon
    # chỉ hai giá trị khác
    chk_ca, chk_idx = copy.deepcopy(new_ca), copy.deepcopy(new_idx)
    chk_ca['nguon_ca'] = ca['nguon_ca']
    chk_idx['su_co'][r]['nguon'] = idx['su_co'][r]['nguon']
    assert chk_ca == ca and chk_idx == idx
    report = {'ca': a.ca, 'ban': a.ban, 'dong_chi_muc': r, 'cu': old, 'moi': a.nguon, 'thu': a.thu}
    if not a.thu:
        for f in (f_ca, f_idx):
            bak = f.with_name(f.name + '.bak-' + a.nguon)
            if bak.exists():
                sys.exit(f'đã có bản sao {bak}; không ghi đè; dừng')
        for f in (f_ca, f_idx):
            shutil.copy2(f, f.with_name(f.name + '.bak-' + a.nguon))
        for f, obj in ((f_ca, new_ca), (f_idx, new_idx)):
            tmp = f.with_name(f.name + '.tmp')
            tmp.write_text(dump(obj), encoding='utf-8')
            shutil.copymode(f, tmp)
            os.replace(tmp, f)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    main()
