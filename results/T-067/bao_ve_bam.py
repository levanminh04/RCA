"""Băm danh sách file bảo vệ của T-067 (laptop + ba máy). Chỉ đọc.
Dùng: py -3 -I bao_ve_bam.py <file-ra>   (file ra ghi byte LF, sắp theo đường dẫn)
Phạm vi: results/T-066/bao-ve.tsv (mục '!' = file trong tgz, băm từ tgz);
repo lab trên laptop: campaigns/g1/{l8b-xuat.py,service_graph.py}, campaigns/runner/*.py;
exp-obs: /srv/rca-lab/m1/**, /srv/rca-lab/m1-snapshots/**, /opt/rca-lab cùng các file lab trên;
exp-app, máy tải: /opt/rca-lab cùng các file lab trên."""
import hashlib, sys, tarfile, subprocess, glob, os, base64
RCA = 'D:/RCA-flashticket'; LAB = 'D:/Project/flashticket-rca-lab'
R = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '..', '..')
SCR = os.environ['T067_SSH']  # đường dẫn script r.sh (ssh chỉ đọc)
LAB_GLOBS = ['campaigns/g1/l8b-xuat.py', 'campaigns/g1/service_graph.py', 'campaigns/runner/*.py']
def h(b): return hashlib.sha256(b).hexdigest()
out = []
for i, line in enumerate(open(f'{RCA}/results/T-066/bao-ve.tsv', encoding='utf-8')):
    if i == 0: continue
    p = line.rstrip('\n').split('\t')[1]
    if '!' in p:
        tgz, inner = p.split('!')
        with tarfile.open(tgz) as t:
            out.append((h(t.extractfile(inner).read()), 'laptop:' + p.replace(chr(92), '/')))
    else:
        out.append((h(open(p, 'rb').read()), 'laptop:' + p.replace(chr(92), '/')))
for g in LAB_GLOBS:
    for f in sorted(glob.glob(f'{LAB}/{g}')):
        out.append((h(open(f, 'rb').read()), 'laptop:' + f.replace(chr(92), '/')))
lab = ' '.join(f'/opt/rca-lab/{g}' for g in LAB_GLOBS)
labc = f'for f in {lab}; do if [ -f "$f" ]; then sha256sum "$f"; else echo "THIEU  $f"; fi; done'
cmds = {
 'obs': 'sudo find /srv/rca-lab/m1 /srv/rca-lab/m1-snapshots -type f -print0 | sudo xargs -0 sha256sum; ' + labc,
 'app': labc, 'tai': labc}
for m, c in cmds.items():
    r = subprocess.run([os.environ.get('T067_BASH', 'bash'), SCR, m, c], capture_output=True, check=True)
    for l in r.stdout.decode().splitlines():
        s, p = l.split('  ', 1); out.append((s, f'{m}:{p}'))
out.sort(key=lambda x: x[1])
with open(sys.argv[1], 'wb') as f:
    f.write(''.join(f'{s}  {p}\n' for s, p in out).encode())
print(len(out), 'file')
