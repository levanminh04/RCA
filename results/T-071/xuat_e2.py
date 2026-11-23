#!/usr/bin/env python3
"""T-071 — xuất dữ liệu E2 trên exp-obs sau khi chuỗi xong (thư viện chuẩn). Chỉ đọc Prometheus (qua xuat_chuoi.py,
khúc ≤ 600 s, nghỉ 0,3 s) và file tai-out; ghi vào THU_MUC_RA (chưa tồn tại).

Dùng: python3 xuat_e2.py KHAI.json THU_MUC_RA
Mỗi lượt (theo thứ tự khai): cửa sổ [StartedAt − 600 s, FinishedAt + 300 s] (bieu-thuc.json#/xuat_cho_T071/cach_xuat);
  xuat/<tag>/          xuat_chuoi.py với bieu-thuc.json (chuỗi luật)
  xuat-doc-lap/<tag>/  xuat_chuoi.py với chuoi-phan-loai.json (chuỗi độc lập)
  luot/<tag>/          state.json, run.json, summary.json, outputs.sha256 (chép từ tai-out), k6-phut.json (k6_phut.py)
Ghi tiến độ từng bước vào THU_MUC_RA/tien-do.jsonl.
"""
import datetime as dt
import json
import pathlib
import re
import shutil
import subprocess
import sys

HERE = pathlib.Path(__file__).resolve().parent
TAI_OUT = pathlib.Path('/srv/rca-lab/load-controller/tai-out')
khai, ra = json.load(open(sys.argv[1], encoding='utf-8')), pathlib.Path(sys.argv[2])
ra.mkdir()
(ra / 'xuat').mkdir()
(ra / 'xuat-doc-lap').mkdir()


def ts(s):
    m = re.fullmatch(r'(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(\.\d+)?Z', s)
    return dt.datetime.fromisoformat(m.group(1) + '+00:00').timestamp() + (float('0' + m.group(2)) if m.group(2) else 0)


def iso(t):
    return dt.datetime.fromtimestamp(t, dt.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')


def ghi(**o):
    with open(ra / 'tien-do.jsonl', 'a', encoding='utf-8') as f:
        f.write(json.dumps({'utc': iso(dt.datetime.now(dt.timezone.utc).timestamp()), **o}, ensure_ascii=False) + '\n')


for l in khai['luot']:
    tag = l['tag']
    src = TAI_OUT / tag
    st = json.load(open(src / 'state.json'))
    a, b = ts(st['StartedAt']) - 600, ts(st['FinishedAt']) + 300
    d = ra / 'luot' / tag
    d.mkdir(parents=True)
    for n in ('state.json', 'run.json', 'summary.json', 'outputs.sha256'):
        shutil.copy2(src / n, d / n)
    ghi(tag=tag, buoc='bat_dau', cua_so=[iso(a), iso(b)])
    r = subprocess.run([sys.executable, '-I', str(HERE / 'k6_phut.py'), str(src / 'raw.json'), str(d / 'k6-phut.json')],
                       capture_output=True, text=True)
    ghi(tag=tag, buoc='k6_phut', rc=r.returncode, out=r.stdout.strip()[-300:], err=r.stderr.strip()[-300:])
    for spec, goc in (('bieu-thuc.json', 'xuat'), ('chuoi-phan-loai.json', 'xuat-doc-lap')):
        r = subprocess.run([sys.executable, '-I', str(HERE / 'xuat_chuoi.py'), str(HERE / spec), iso(a), iso(b),
                            str(ra / goc / tag)], capture_output=True, text=True)
        ghi(tag=tag, buoc=goc, rc=r.returncode, err=r.stderr.strip()[-300:],
            khuc_loi=sum(json.loads(x)['khuc_loi'] for x in r.stdout.splitlines() if x.startswith('{')))
ghi(buoc='xong')
