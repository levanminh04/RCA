# -*- coding: utf-8 -*-
"""Lô 5 — dựng ở ổ C (biến môi trường L5_W) vì ổ D còn ~4,8 GB.
Lô 5 (WHY-96): dựng thư mục gốc kiểu /opt/flash-ticket-rca trên laptop cho phần d = 0 (ngoài repo, D:/RCA-ext/m1ft-l5),
từ gói ca và gói bổ sung đã có trong repo; đối chiếu hash gói bổ sung với exp-obs (file hash truyền vào)."""
import hashlib, json, pathlib, shutil, sys, tarfile
REPO = pathlib.Path('.'); import os; W = pathlib.Path(os.environ['L5_W']); GOC = W / 'goc'; BS = W / 'bo-sung'
remote = {}
for l in open(sys.argv[1], encoding='utf-8'):
    h, p = l.split(); remote[p] = h
R = REPO / 'results/T-064'
dev2 = [c['ma'] for c in json.load(open(R / 'tap-chon-dev2-13.json', encoding='utf-8'))['ca']]
t062 = open(R / 'kiem/ca-t062-9.txt').read().split()
moi5 = ['86dea661', '659a9dfb1ab0', '1e5a3dc5', '7d1ee32f', '0a45b2e0']
CAN_DU = ('raw-traces.jsonl', 'request.json', 'prometheus.json', 'inventory.json', 'raw-logs.jsonl')  # 5 ca thu bù 3
CAN_GON = ('request.json', 'prometheus.json', 'inventory.json')  # 22 ca cũ: bản chạy trên laptop không cần trace/log
def sha(p): return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
bao = {'goi': {}, 'bo_sung': {}}
for tap, ids, nguon_tgz, nguon_bs, remote_dir in (
        ('dev2', dev2, 'results/T-063/thu2/ca/{i}.tgz', 'results/T-063/thu2/ca/{i}/prometheus-bo-sung.json', 'bo-sung-dev2'),
        ('dev3', moi5, 'results/T-063/thu3/thu/ca/{i}.tgz', 'results/T-063/thu3/thu/ca/{i}/prometheus-bo-sung.json', 'bo-sung-dev3'),
        ('t062', t062, None, 'results/T-063/ca-t062-bo-sung/{i}/prometheus-bo-sung.json', 'bo-sung')):
    for i in ids:
        if nguon_tgz:
            with tarfile.open(nguon_tgz.format(i=i)) as tf:
                for m in tf.getmembers():
                    if m.isfile() and (m.name == f'outputs/{i}/method-input.json' or
                                       (m.name.startswith(f'cases/{i}/') and m.name.split('/')[-1] in (CAN_DU if tap == 'dev3' else CAN_GON))):
                        tf.extract(m, GOC, filter='data')
        else:
            for sub, names in (('outputs', ('method-input.json',)), ('cases', CAN_GON)):
                for n in names:
                    s = REPO / 'results/T-062/ca' / i / sub / i / n
                    if s.exists():
                        d = GOC / sub / i / n; d.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(s, d)
        assert (GOC / 'outputs' / i / 'method-input.json').exists(), i
        b = REPO / nguon_bs.format(i=i); h = sha(b); hr = remote.get(f'{remote_dir}/{i}/prometheus-bo-sung.json')
        assert hr == h, (i, h, hr)
        d = BS / tap / i / 'prometheus-bo-sung.json'; d.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(b, d)
        bao['bo_sung'][f'{tap}/{i}'] = h
shutil.copyfile(REPO / 'results/T-058/dem-2026-11-10/m1-p7-config.json', GOC / 'm1-p7-config.json')
print(json.dumps({'so_ca': len(bao['bo_sung']), 'khop_exp_obs': True}, ensure_ascii=False))
(W / 'dung-goc.json').write_text(json.dumps(bao, ensure_ascii=False, indent=1), encoding='utf-8')
