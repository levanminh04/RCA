# -*- coding: utf-8 -*-
"""Lô 5 (WHY-96): chạy phần d = 0 trên laptop, song song N tiến trình, môi trường ghim py312-pin.
Dùng: py -3 chay_laptop.py <file việc "bản d tập ca"> <số luồng>   (biến môi trường L5_W = thư mục gốc đã dựng)
Luật 21: một cặp lỗi chỉ ghi dòng lỗi; chạy lại bỏ qua cặp đã có summary.json; có file <L5_W>/DUNG thì không phát cặp mới."""
import concurrent.futures as cf, datetime, os, pathlib, subprocess, sys
W = pathlib.Path(os.environ['L5_W']); REPO = pathlib.Path(__file__).resolve().parents[4]
PY = 'D:/RCA-ext/envs/py312-pin/Scripts/python.exe'
ENV = dict(os.environ, PYTHONPATH='D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages', PYTHONDONTWRITEBYTECODE='1',
           PYTHONIOENCODING='utf-8')
viec = [l.split() for l in open(sys.argv[1], encoding='utf-8') if l.strip()]
log = open(W / ('log-' + pathlib.Path(sys.argv[1]).stem + '.txt'), 'a', encoding='utf-8')

def mot(v):
    b, d, tap, i = v
    ra = W / 'out' / tap / f'd{d}' / b
    if (ra / i / 'summary.json').exists(): return f'BO-QUA {b} {i}'
    if (W / 'DUNG').exists(): return f'DUNG {b} {i}'
    cfg = REPO / 'results/T-064/bien-the' / b / 'cau-hinh.json'
    if not cfg.exists(): cfg = REPO / 'results/T-064/phien-c/kiem-laptop/cau-hinh-rong.json'  # P7: cấu hình rỗng
    cmd = [PY, '-B', str(REPO / 'src/m1_ft/chay_ca.py'), '--id', i, '--cau-hinh', str(cfg), '--ban', b, '--ra', str(ra),
           '--goc', str(W / 'goc'), '--bo-sung', str(W / 'bo-sung' / tap / '{id}' / 'prometheus-bo-sung.json')]
    r = subprocess.run(cmd, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    out = (r.stdout.strip().splitlines() or [''])[-1] + ((' | ' + r.stderr.strip().splitlines()[-1]) if r.returncode else '')
    return f'{datetime.datetime.now(datetime.UTC):%H:%M:%SZ} rc={r.returncode} {b} {tap} {i} {out[:300]}'

with cf.ThreadPoolExecutor(int(sys.argv[2])) as ex:
    for s in ex.map(mot, viec):
        print(s, file=log, flush=True)
print('XONG', file=log, flush=True)
