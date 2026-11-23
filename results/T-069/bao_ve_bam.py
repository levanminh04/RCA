"""T-069 — băm danh sách bảo vệ (laptop + ba máy). Chỉ đọc. Dựa theo results/T-067/bao_ve_bam.py (bản đó không sửa).
Dùng: <python> -I bao_ve_bam.py <file-bao-ve> <file-lab-exp-app>     (biến môi trường T069_SSH = script r.sh)
Ra hai file, byte LF, sắp theo đường dẫn:
  <file-bao-ve>: phải trùng byte trước/sau trên mọi đường dẫn đã có ở lần trước:
    - results/T-066/bao-ve.tsv (mục '!' = file trong tgz, băm từ tgz);
    - phía cũ T-064 (đầu ra d0 P7 và V082, R9, bộ chấm, đáp án, tập chọn, manifest-3, hồ sơ chọn) và file ngoài T-064
      mà manifest-3 ghi (trừ docs/*), src/m1_ft/;
    - results/T-067/** ; điều kiện và script xác nhận của T-063 dùng lại;
    - repo lab trên laptop: campaigns/g1/{l8b-xuat.py,service_graph.py}, campaigns/runner/*.py;
    - exp-obs: /srv/rca-lab/m1/**, /srv/rca-lab/m1-snapshots/**, /opt/rca-lab/campaigns/{g1,runner} như trên;
    - máy tải: /opt/rca-lab cùng các file lab trên.
  <file-lab-exp-app>: HEAD và mọi file git của /opt/rca-lab trên exp-app (đổi theo checkout của bước 2; khác biệt
    phải đúng bằng git diff --name-only giữa hai commit).
"""
import hashlib, sys, tarfile, subprocess, glob, os, json
sys.stdout.reconfigure(encoding='utf-8')
RCA = 'D:/RCA-flashticket'; LAB = 'D:/Project/flashticket-rca-lab'
SCR = os.environ['T069_SSH']
BASH = os.environ.get('T069_BASH', 'bash')
LAB_GLOBS = ['campaigns/g1/l8b-xuat.py', 'campaigns/g1/service_graph.py', 'campaigns/runner/*.py']
T064_TIEN_TO = ['kiem/nhan-luot5/', 'kiem/nhan-r9/', 'cham/dau-ra-dev2/P7/', 'cham/dau-ra-dev3/P7/', 'cham/cham_dev3.py',
                'cham/chon-dev3-d0-v082-r9-A.', 'cham/chon-dev3-d0-v082-r9-B.', 'cham/spec-dev3-d0-v082-r9.json',
                'dap-an-dev3.json', 'dap-an-dev3-B.json', 'tap-chon-dev3-17.json', 'tieu-chi-chon.md', 'ho-so-chon.md',
                'cau-hinh-de-xuat.json', 'bien-the/V082-V066+H8a/cau-hinh.json', 'bien-the/P7/']
T063 = ['results/T-063/chay/dieu-kien-xac-nhan.md', 'results/T-063/chay/xac_nhan_ca.py',
        'results/T-063/thu3/dieu-kien-xac-nhan-3.md', 'results/T-063/thu3/scripts/xac_nhan_ca_3.py']


def h(b): return hashlib.sha256(b).hexdigest()


def hf(p): return h(open(p, 'rb').read())


out = []
for i, line in enumerate(open(f'{RCA}/results/T-066/bao-ve.tsv', encoding='utf-8')):
    if i == 0: continue
    p = line.rstrip('\n').split('\t')[1]
    if '!' in p:
        tgz, inner = p.split('!')
        with tarfile.open(tgz) as t:
            out.append((h(t.extractfile(inner).read()), 'laptop:' + p.replace(chr(92), '/')))
    else:
        out.append((hf(p), 'laptop:' + p.replace(chr(92), '/')))
m3 = json.load(open(f'{RCA}/results/T-064/manifest-3.json', encoding='utf-8'))
t064 = sorted(k for k in m3['file'] if any(k.startswith(x) for x in T064_TIEN_TO))
rel = [f'results/T-064/{k}' for k in t064] + ['results/T-064/manifest-3.json']
rel += sorted(k for k in m3['ngoai_T064'] if not k.startswith('docs/'))
rel += sorted(p.replace(chr(92), '/')[len(RCA) + 1:] for p in glob.glob(f'{RCA}/src/m1_ft/*.py'))
rel += sorted(p.replace(chr(92), '/')[len(RCA) + 1:] for p in glob.glob(f'{RCA}/results/T-067/**', recursive=True) if os.path.isfile(p))
rel += T063
for r in sorted(set(rel)):
    out.append((hf(f'{RCA}/{r}'), f'laptop:{RCA}/{r}'))
for g in LAB_GLOBS:
    for f in sorted(glob.glob(f'{LAB}/{g}')):
        out.append((hf(f), 'laptop:' + f.replace(chr(92), '/')))
lab = ' '.join(f'/opt/rca-lab/{g}' for g in LAB_GLOBS)
labc = f'for f in {lab}; do if [ -f "$f" ]; then sha256sum "$f"; else echo "THIEU  $f"; fi; done'
cmds = {'obs': 'sudo find /srv/rca-lab/m1 /srv/rca-lab/m1-snapshots -type f -print0 | sudo xargs -0 sha256sum; ' + labc,
        'tai': labc}
for m, c in cmds.items():
    r = subprocess.run([BASH, SCR, m, c], capture_output=True, check=True)
    for l in r.stdout.decode().splitlines():
        s, p = l.split('  ', 1); out.append((s, f'{m}:{p}'))
out.sort(key=lambda x: x[1])
with open(sys.argv[1], 'wb') as f:
    f.write(''.join(f'{s}  {p}\n' for s, p in out).encode())
r = subprocess.run([BASH, SCR, 'app', 'cd /opt/rca-lab && echo "HEAD  $(git rev-parse HEAD)" && git ls-files -z | xargs -0 sha256sum'],
                   capture_output=True, check=True)
lines = sorted(r.stdout.decode().splitlines())
with open(sys.argv[2], 'wb') as f:
    f.write(''.join(l + '\n' for l in lines).encode())
print(len(out), 'file bảo vệ;', len(lines), 'dòng lab exp-app')
