"""T-071 — thử luồng chuoi_tai.py bằng tai_linux giả và Prometheus giả. Không SSH, không tải.

Dùng: python3 thu_chuoi.py CHUOI_TAI.py TAI_GIA.py THU_MUC_THU   (THU_MUC_THU phải chưa tồn tại)
Tạo repo git tạm trong THU_MUC_THU (chuoi_tai kiểm commit/cây sạch). Mỗi ca in ĐẠT/SAI và chi tiết.
Thoát 1 nếu có ca sai.
"""
import hashlib
import http.server
import json
import os
import pathlib
import shutil
import subprocess
import sys
import re
import threading
import urllib.parse

sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")

C, T, W = map(os.path.abspath, sys.argv[1:4])
W = pathlib.Path(W)
W.mkdir()
repo = W / 'repo'
(repo / 'load/controller').mkdir(parents=True)
shutil.copy(C, repo / 'load/controller/chuoi_tai.py')
shutil.copy(T, repo / 'load/controller/tai_gia.py')


def git(*a):
    subprocess.run(['git', '-C', str(repo), *a], check=True, capture_output=True)


git('init', '-q')
git('config', 'core.autocrlf', 'false')
git('add', '-A')
git('-c', 'user.email=t@t', '-c', 'user.name=t', 'commit', '-qm', 't')
C = str(repo / 'load/controller/chuoi_tai.py')
T = str(repo / 'load/controller/tai_gia.py')

MODE = {'v': 'ok', 'n': 0, 'mau_ms': None}  # mau_ms: danh sách timestamp (ms) mẫu gateway; None = mỗi khúc 100


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        MODE['n'] += 1
        if MODE['v'] == 'loi':
            self.send_response(500)
            self.end_headers()
            return
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        expr, t = q['query'][0], float(q['time'][0])
        m = re.search(r'\[(\d+)ms\]', expr)
        if 'count_over_time' in expr and MODE['mau_ms'] is not None:
            # đúng ngữ nghĩa Prometheus: mẫu trong (t − L, t]
            L = int(m.group(1))
            tm = round(t * 1000)
            v = str(sum(1 for s in MODE['mau_ms'] if tm - L < s <= tm))
        else:
            v = '0' if MODE['v'] == 'zero' else ('100' if 'count_over_time' in expr else '1')
        MODE.setdefault('ms', []).append(bool(m))
        b = json.dumps({'status': 'success', 'data': {'resultType': 'vector',
                                                      'result': [{'metric': {}, 'value': [0, v]}]}}).encode()
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b)


srv = http.server.HTTPServer(('127.0.0.1', 0), H)
threading.Thread(target=srv.serve_forever, daemon=True).start()
PROM = f'http://127.0.0.1:{srv.server_port}'


def kh(name, secs=(3600, 1800, 3600)):
    p = W / name
    p.write_text(json.dumps({'luot': [
        {'thu_tu': i + 1, 'tag': f't-{c}', 'seconds': s, 'buoc_tai': 600 if s == 1800 else 0,
         'multiplier': 3 if s == 1800 else 1} for i, (c, s) in enumerate(zip('abc', secs))]}))
    return str(p), hashlib.sha256(p.read_bytes()).hexdigest()


KH = kh('kh.json')
KH1 = kh('kh1.json', (1, 1, 1))


def run(kho, kb, extra=(), env=None, plan=KH, on_line=None):
    e = dict(os.environ, PYTHONIOENCODING='utf-8', CHUOI_TAI_NHIP_S='0.01', CHUOI_TAI_PROM=PROM,
             CHUOI_TAI_STOP=str(W / 'STOP'), FAKE_DIR=str(W / ('f-' + kho)), FAKE_KB=json.dumps(kb), **(env or {}))
    p = subprocess.Popen([sys.executable, C, '--ke-hoach', plan[0], '--sha256', plan[1], '--kho', str(W / kho),
                          '--tai-linux', T, *extra], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=e,
                         text=True, encoding='utf-8')
    ev = []
    for line in p.stdout:
        try:
            d = json.loads(line)
        except ValueError:
            continue
        ev.append(d)
        if on_line:
            on_line(d)
    rc = p.wait()
    return rc, ev, p.stderr.read()


def kq(ev):
    return [(d.get('tag'), d.get('ket_qua')) for d in ev if d['loai'] == 'ket_qua_luot']


def loai(ev):
    return [d['loai'] for d in ev]


def goi(kho):
    f = W / ('f-' + kho) / 'goi.log'
    return f.read_text().splitlines() if f.exists() else []


SAI = []


def ca(ten, dk, chi_tiet):
    if not dk:
        SAI.append(ten)
    print(('ĐẠT ' if dk else 'SAI ') + ten + ' | ' + chi_tiet, flush=True)


# 1 bình thường
rc, ev, _ = run('k1', {})
ca('01 bình thường: 3 lượt xong, 3 kiem_dat, 0 stop',
   rc == 0 and kq(ev) == [('t-a', 'xong'), ('t-b', 'xong'), ('t-c', 'xong')] and loai(ev).count('kiem_dat') == 3
   and not [x for x in goi('k1') if x.startswith('stop')], f'rc={rc} {kq(ev)}')
kd = [d for d in ev if d['loai'] == 'kiem_dat'][0]['ket_qua']
ca('01b kiểm theo khúc ≤ 600 s: lượt 3600 s (07:57:34–08:57:37) → 7 khúc', kd['so_khuc'] == 7, json.dumps(kd)[:160])

# 2 Prometheus lỗi → chưa kiểm được, dừng trước lượt kế; chạy lại thiếu cờ → từ chối; có cờ → kiểm lại, đi tiếp
MODE['v'] = 'loi'
rc, ev, _ = run('k2', {})
ca('02 prom lỗi → chua_kiem_duoc, dừng, không start t-b',
   rc == 3 and kq(ev) == [('t-a', 'chua_kiem_duoc')] and not [x for x in goi('k2') if 'start --tag t-b' in x],
   f'rc={rc} {kq(ev)}')
MODE['v'] = 'ok'
rc, ev, err = run('k2', {})
ca('02b chạy lại thiếu --tiep-sau-dung → từ chối, không ghi gì', rc != 0 and not ev and 'tiep-sau-dung' in err, f'rc={rc}')
rc, ev, _ = run('k2', {}, ('--tiep-sau-dung', 'thử'))
ca('02c có cờ → kiểm lại t-a, không start lại t-a, đi hết',
   rc == 0 and kq(ev)[0] == ('t-a', 'xong') and sum('start --tag t-a' in x for x in goi('k2')) == 1,
   f'rc={rc} {kq(ev)}')

# 3 0 mẫu gateway
MODE['v'] = 'zero'
rc, ev, _ = run('k3', {})
MODE['v'] = 'ok'
ca('03 0 mẫu gateway → mat_telemetry, dừng', rc == 3 and kq(ev) == [('t-a', 'mat_telemetry')], f'rc={rc} {kq(ev)}')

# 4, 5 chết sau 'xong' (trước kiểm) / sau 'kiem_dat' (trước nhận): cắt nhật ký của một lượt chạy tốt
rc, ev, _ = run('k45', {})
lines = (W / 'k45/chuoi.jsonl').read_text(encoding='utf-8').splitlines()
for so, mark in (('04', 'xong'), ('05', 'kiem_dat')):
    kho = 'k' + so
    (W / kho).mkdir()
    shutil.copytree(W / 'f-k45', W / ('f-' + kho))
    cut = next(i for i, l in enumerate(lines) if json.loads(l)['loai'] == mark and json.loads(l).get('tag') == 't-a')
    (W / kho / 'chuoi.jsonl').write_text('\n'.join(lines[:cut + 1]) + '\n', encoding='utf-8')
    n0 = len(goi(kho))
    rc, ev, _ = run(kho, {})
    moi = goi(kho)[n0:]
    tn = [d for d in ev if d['loai'] == 'tiep_nhan' and d['tag'] == 't-a']
    can = 'can_kiem' if mark == 'xong' else 'can_nhan'
    kiem_lai = 'kiem_dat' in [d['loai'] for d in ev if d.get('tag') == 't-a']
    ca(f'{so} chết sau {mark} → tiếp {can}, không start lại, kiểm lại={mark == "xong"}, receive',
       rc == 0 and bool(tn) and tn[0]['buoc'] == can and not any('start --tag t-a' in x for x in moi)
       and kiem_lai == (mark == 'xong') and any('receive --tag t-a' in x for x in moi),
       f'rc={rc} buoc={tn[0]["buoc"] if tn else None}')

# 6 get lỗi kéo dài → chưa xác minh, không 'hong'; chạy lại khi get đã tốt → tiếp chờ, không start lại
rc, ev, _ = run('k6', {'t-a': 'get_loi'})
ca('06 get lỗi 20 lần → chua_xac_minh, dừng, không hong',
   rc == 3 and kq(ev) == [('t-a', 'chua_xac_minh')] and 'hong' not in loai(ev)
   and loai(ev).count('get_loi') == 20, f'rc={rc} {kq(ev)}')
rc, ev, _ = run('k6', {}, ('--tiep-sau-dung', 'get đã tốt'))
ca('06b chạy lại → tiếp can_cho, xong, không start lại',
   rc == 0 and kq(ev)[0] == ('t-a', 'xong') and sum('start --tag t-a' in x for x in goi('k6')) == 1,
   f'rc={rc} {kq(ev)}')

# 7 Running mãi sau stop → cần can thiệp, giữ tag, dừng; stop đúng một lần và có --tag
rc, ev, _ = run('k7', {'t-a': 'treo'}, plan=KH1, env={'CHUOI_TAI_QUA_HAN_S': '-200', 'CHUOI_TAI_SAU_STOP_S': '0.3'})
st = [x for x in goi('k7') if x.startswith('stop')]
ca('07 treo → stop --tag t-a một lần, can_can_thiep, dừng, không hong',
   rc == 3 and kq(ev) == [('t-a', 'can_can_thiep')] and st == ['stop --tag t-a'] and 'hong' not in loai(ev),
   f'rc={rc} {kq(ev)} {st}')


# 8 STOP xuất hiện khi đang chờ lượt
def tao_stop(d):
    if d['loai'] == 'phat' and d['tag'] == 't-a':
        (W / 'STOP').write_text('x')


rc, ev, _ = run('k8', {'t-a': 'cham'}, on_line=tao_stop)
(W / 'STOP').unlink()
ca('08 STOP khi chờ → dung, dừng, tag giữ (không hong)',
   rc == 3 and kq(ev) == [('t-a', 'dung')] and 'hong' not in loai(ev), f'rc={rc} {kq(ev)}')

# 9 lỗi cục bộ: start lỗi không container; start lỗi có container; receive lỗi
rc, ev, _ = run('k9', {'t-a': 'start_loi', 't-b': 'start_loi_co_container', 't-c': 'nhan_loi'})
ca('09 lỗi cục bộ đi tiếp; t-c chưa kết thúc được báo cuối',
   rc == 1 and kq(ev) == [('t-a', 'hong_start'), ('t-b', 'xong'), ('t-c', 'nhan_chua_duoc')]
   and ev[-1]['loai'] == 'xong_chuoi' and ev[-1]['tag_chua_ket_thuc'] == ['t-c'], f'rc={rc} {kq(ev)}')
rc, ev, _ = run('k9', {})
ca('09b chạy lại (không cần cờ vì lần trước xong_chuoi) → chỉ receive t-c',
   rc == 0 and kq(ev) == [('t-c', 'xong')] and [d['tag'] for d in ev if d['loai'] == 'bo_qua'] == ['t-a', 't-b'],
   f'rc={rc} {kq(ev)}')

# 10 container exit 1 vẫn kiểm và nhận
rc, ev, _ = run('k10', {'t-b': 'exit1'})
ca('10 exit 1 → xong_loi_container, vẫn kiểm + nhận, đi tiếp',
   rc == 0 and kq(ev)[1] == ('t-b', 'xong_loi_container') and loai(ev).count('nhan') == 3, f'rc={rc} {kq(ev)}')

# 11, 12 lỗi chung; 2 lượt liền lỗi start
rc, ev, _ = run('k11', {'t-a': 'start_chung'})
ca('11 lỗi chung → dừng', rc == 3 and kq(ev) == [('t-a', 'loi_chung')], f'rc={rc} {kq(ev)}')
rc, ev, _ = run('k12', {'t-a': 'start_loi', 't-b': 'start_loi'})
ca('12 2 lượt liền lỗi start → dừng', rc == 3 and len(kq(ev)) == 2 and ev[-1]['loai'] == 'dung_chuoi',
   f'rc={rc} {kq(ev)}')

# 13 lỗi I/O giữa chuỗi → loi_noi_bo ghi vào nhật ký, rc 4
(W / 'k13').mkdir()
(W / 'k13/trang-thai.json.tmp').mkdir()
rc, ev, _ = run('k13', {})
ca('13 I/O lỗi → loi_noi_bo, rc 4', rc == 4 and 'loi_noi_bo' in (W / 'k13/chuoi.jsonl').read_text(encoding='utf-8'),
   f'rc={rc}')

# 14 kế hoạch khác trên cùng kho; 15 sai sha256
rc, ev, err = run('k1', {}, plan=KH1)
ca('14 kho đã dùng kế hoạch khác → từ chối', rc != 0 and 'kế hoạch khác' in err, f'rc={rc}')
rc, ev, err = run('k15', {}, plan=(KH[0], '00'))
ca('15 sai sha256 → từ chối', rc != 0 and 'từ chối' in err, f'rc={rc}')


# 16 DUNG khi t-a đang chạy: t-a chạy hết (kiểm + nhận), chuỗi dừng trước t-b (tạo ở 'phat' để không đua thứ tự)
def tao_dung(d):
    if d['loai'] == 'phat' and d['tag'] == 't-a':
        (W / 'k16/DUNG').write_text('x')


rc, ev, _ = run('k16', {}, on_line=tao_dung)
ca('16 DUNG → dừng trước t-b', rc == 2 and kq(ev) == [('t-a', 'xong')], f'rc={rc} {kq(ev)}')


def lam_ban(d):
    if d['loai'] == 'ket_qua_luot' and d['tag'] == 't-a':
        (repo / 'load/x.txt').write_text('x')


rc, ev, _ = run('k17', {}, on_line=lam_ban)
(repo / 'load/x.txt').unlink()
ca('17 cây bẩn → dừng trước t-b', rc == 2 and kq(ev) == [('t-a', 'xong')], f'rc={rc} {kq(ev)}')

# 19 start lỗi ở bước docker run và get cũng lỗi → chưa xác minh, không hong, dừng
rc, ev, _ = run('k19', {'t-a': 'start_get_loi'})
ca('19 start + get cùng lỗi → chua_xac_minh, không hong, không start t-b',
   rc == 3 and kq(ev) == [('t-a', 'chua_xac_minh')] and 'hong' not in loai(ev)
   and not [x for x in goi('k19') if 'start --tag t-b' in x], f'rc={rc} {kq(ev)}')


# 20, 21 chết ngay sau `hong` (trước dung_chuoi): khôi phục chốt loi_chung / đếm 2 lượt liền từ nhật ký
def cat_sau(kho_goc, kho, n_hong):
    ls = (W / kho_goc / 'chuoi.jsonl').read_text(encoding='utf-8').splitlines()
    idx = [i for i, l in enumerate(ls) if json.loads(l)['loai'] == 'hong'][n_hong - 1]
    (W / kho).mkdir()
    (W / kho / 'chuoi.jsonl').write_text('\n'.join(ls[:idx + 1]) + '\n', encoding='utf-8')


rc, ev, _ = run('k20g', {'t-a': 'start_chung'})
cat_sau('k20g', 'k20', 1)
rc, ev, _ = run('k20', {})
ca('20 chết sau hong(loi_chung), chạy lại không cờ → dừng, không start t-b',
   rc == 3 and ev[-1]['loai'] == 'dung_chuoi' and 'khôi phục' in ev[-1]['ly_do']
   and not [x for x in goi('k20') if x.startswith('start')], f'rc={rc} {ev[-1].get("ly_do")}')
rc, ev, _ = run('k20', {}, ('--tiep-sau-dung', 'đã xử lý STOP'))
ca('20b có cờ → bỏ qua t-a (hong), chạy t-b, t-c', rc == 0 and kq(ev) == [('t-b', 'xong'), ('t-c', 'xong')],
   f'rc={rc} {kq(ev)}')
rc, ev, _ = run('k21g', {'t-a': 'start_loi', 't-b': 'start_loi'})
cat_sau('k21g', 'k21', 2)
rc, ev, _ = run('k21', {})
ca('21 chết sau hong thứ 2 liền, chạy lại không cờ → dừng, không start t-c',
   rc == 3 and '2 lượt liền' in ev[-1].get('ly_do', '') and 'khôi phục' in ev[-1]['ly_do']
   and not [x for x in goi('k21') if x.startswith('start')], f'rc={rc} {ev[-1].get("ly_do")}')

# 22 cửa sổ đếm mẫu đúng (StartedAt, FinishedAt]: StartedAt = …34.017283858 → mẫu ở …34.017 ngoài, …34.018 trong;
#    FinishedAt = …36.200 → mẫu ở …36.200 trong, …36.201 ngoài
BD = 1794988654017  # 2026-11-18T07:57:34.017Z (ms)
KT = 1794992256200  # 2026-11-18T08:57:36.200Z (ms)
for so, mau, mong in (('22a', [KT + 1], 'mat_telemetry'), ('22b', [KT], 'xong'),
                      ('22c', [BD], 'mat_telemetry'), ('22d', [BD + 1], 'xong')):
    MODE['mau_ms'] = mau
    MODE['ms'] = []
    rc, ev, _ = run('k' + so, {}, plan=KH1)
    ca(f'{so} một mẫu ở {mau[0] - (KT if mau[0] >= KT else BD):+d} ms so với '
       f'{"FinishedAt" if mau[0] >= KT else "StartedAt"} → {mong}',
       kq(ev)[:1] == [('t-a', mong)] and all(MODE['ms']), f'rc={rc} {kq(ev)[:1]}')
MODE['mau_ms'] = None

# 23 bản ghi `xong` thiếu mốc giờ: get lại lấy mốc; vẫn thiếu → chưa kiểm được nhưng vẫn receive, dừng trước t-b
rc, ev, _ = run('k23', {'t-a': 'thieu_moc_1'})
ca('23 thiếu mốc lần đầu → get lại, xong_bo_sung_moc, kiem_dat, đi tiếp',
   rc == 0 and 'xong_bo_sung_moc' in loai(ev) and kq(ev)[0] == ('t-a', 'xong'), f'rc={rc} {kq(ev)}')
rc, ev, _ = run('k23b', {'t-a': 'thieu_moc'})
ca('23b thiếu mốc mãi → chua_kiem_duoc, vẫn receive t-a, không start t-b',
   rc == 3 and kq(ev) == [('t-a', 'chua_kiem_duoc')] and any('receive --tag t-a' in x for x in goi('k23b'))
   and 'nhan' in loai(ev) and not [x for x in goi('k23b') if 'start --tag t-b' in x], f'rc={rc} {kq(ev)}')
rc, ev, _ = run('k23b', {}, ('--tiep-sau-dung', 'mốc đã có'))
ca('23c chạy lại có cờ → kiểm lại t-a, không receive lại t-a',
   rc == 0 and kq(ev)[0] == ('t-a', 'xong') and 'bo_qua_nhan' in loai(ev)
   and sum('receive --tag t-a' in x for x in goi('k23b')) == 1, f'rc={rc} {kq(ev)}')

# 18 khóa (chỉ khi có fcntl)
try:
    import fcntl
    (W / 'k18').mkdir()
    lk = open(W / 'k18/chuoi.lock', 'a')
    fcntl.flock(lk, fcntl.LOCK_EX | fcntl.LOCK_NB)
    rc, ev, err = run('k18', {})
    ca('18 khóa bận → từ chối, không ghi nhật ký', rc != 0 and 'đang chạy' in err
       and not (W / 'k18/chuoi.jsonl').exists(), f'rc={rc}')
except ImportError:
    print('BỎ 18 khóa (máy này không có fcntl)')

print('prom_goi', MODE['n'])
print('TONG', 'ĐẠT' if not SAI else 'SAI: ' + ', '.join(SAI))
sys.exit(1 if SAI else 0)
