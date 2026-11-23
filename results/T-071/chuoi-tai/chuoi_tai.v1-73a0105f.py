#!/usr/bin/env python3
"""Bộ chuỗi lượt tải trên exp-obs (T-071, phương án A của R7). Python 3 thư viện chuẩn.

Chạy một danh sách lượt khai trước, lần lượt, bằng tai_linux.py (start → get chờ xong → receive).
Không sửa tai_linux.py; không phát gì ngoài danh sách; không có lượt bù; không bao giờ gọi `stop` thiếu --tag.

Dùng (chạy nền trên server, không cần laptop giữ kết nối):
  nohup python3 /opt/rca-lab/load/controller/chuoi_tai.py --ke-hoach KHAI.json --sha256 HASH \\
        --kho /srv/rca-lab/runs/t071-e2 > /srv/rca-lab/runs/t071-e2.out 2>&1 &
  python3 chuoi_tai.py ... --chay-kho      # chạy khô: kiểm kế hoạch, tag chưa dùng, in lệnh; không phát tải

Kế hoạch: JSON có mảng `luot` (theo thứ tự), mỗi phần tử {thu_tu, tag, seconds, buoc_tai, multiplier}.
`--sha256` phải bằng sha256 của file kế hoạch (bản đã khóa); lệch thì từ chối.

Nhật ký `<kho>/chuoi.jsonl` (chỉ ghi thêm, fsync từng dòng): mỗi lượt ghi `sap_phat` (tag, lệnh) TRƯỚC khi gọi start,
rồi `phat`, `xong`, `nhan`, `kiem_telemetry`. `<kho>/trang-thai.json` (ghi thay nguyên tử) cho người theo dõi.

Dừng chuỗi (không phát lượt tiếp; lượt đang chạy để chạy hết rồi receive):
  - có `/srv/rca-lab/runs/STOP`, `/srv/rca-lab/load-controller/STOP` (I8) hoặc `<kho>/DUNG` (riêng chuỗi này);
  - commit `/opt/rca-lab` đổi giữa chuỗi (I7), hoặc cây bẩn (tai_linux tự từ chối);
  - lỗi start thuộc loại chung (STOP, cây bẩn, còn container rca-tai- khác, khóa bận) hoặc 2 lượt liền không start được;
  - kiểm telemetry sau lượt thấy 0 mẫu gateway trong cửa sổ lượt (mất quan sát: lỗi nguồn chung).
Lỗi cục bộ một lượt (start lỗi khác, container thoát lỗi, receive lỗi sau 3 lần): ghi `hong`, chuyển lượt kế.

Tiếp nhận sau gián đoạn: chạy lại cùng lệnh. Lượt đã `nhan` thì bỏ qua; lượt đã `sap_phat` nhưng chưa `nhan`
thì không start lại (tag không tái dùng): chờ container xong và receive; nếu container không tồn tại thì ghi `hong`.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request

try:
    import fcntl
except ImportError:  # chỉ để chạy thử trên Windows; trên server luôn có fcntl
    fcntl = None

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
TAI_LINUX = ROOT / 'tai_linux.py'
STOP_FILES = [Path('/srv/rca-lab/runs/STOP'), Path('/srv/rca-lab/load-controller/STOP')]
PROM = 'http://127.0.0.1:9090'
TAG_RE = re.compile('[a-z0-9][a-z0-9-]{0,47}')
LOI_CHUNG = ('STOP exists', 'dirty', 'A rca-tai- container is running', 'Another L1 Linux mutation',
             'Cannot read lab git commit', 'SSH key/known_hosts')
NHIP_GET_S = float(os.environ.get('CHUOI_TAI_NHIP_S', '30'))  # chỉ đổi khi chạy thử bằng tai_linux giả
GRACEFUL_S = 90
QUA_HAN_S = 900  # quá seconds + graceful + 900 s mà container vẫn chạy → stop đúng tag


def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()


class Chuoi:
    def __init__(self, a):
        self.a = a
        self.kho = Path(a.kho)
        self.kho.mkdir(parents=True, exist_ok=True)
        self.log_path = self.kho / 'chuoi.jsonl'
        self.tai_linux = Path(a.tai_linux)
        self.da_ghi = self.doc_nhat_ky()

    # ---- nhật ký -------------------------------------------------------------------------------
    def ghi(self, loai, **chi_tiet):
        dong = json.dumps({'utc': utc(), 'loai': loai, **chi_tiet}, ensure_ascii=False)
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(dong + '\n')
            f.flush()
            os.fsync(f.fileno())
        print(dong, flush=True)

    def trang_thai(self, **o):
        tmp = self.kho / 'trang-thai.json.tmp'
        tmp.write_text(json.dumps({'utc': utc(), 'pid': os.getpid(), **o}, ensure_ascii=False, indent=1),
                       encoding='utf-8')
        os.replace(tmp, self.kho / 'trang-thai.json')

    def doc_nhat_ky(self):
        out = {}
        if self.log_path.exists():
            for l in self.log_path.read_text(encoding='utf-8').splitlines():
                try:
                    d = json.loads(l)
                except ValueError:
                    continue
                if d.get('tag'):
                    out.setdefault(d['tag'], set()).add(d['loai'])
        return out

    # ---- gọi tai_linux --------------------------------------------------------------------------
    def tl(self, *args, timeout=900):
        """Gọi tai_linux.py, trả JSON một dòng của nó (ok/result hoặc ok=false/error)."""
        try:
            p = subprocess.run([sys.executable, str(self.tai_linux), *args], stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, timeout=timeout, check=False, cwd=str(REPO))
        except subprocess.TimeoutExpired:
            return {'ok': False, 'error': 'chuoi_tai: tai_linux timeout ' + ' '.join(args[:1])}
        dong = [l for l in p.stdout.decode('utf-8', 'replace').splitlines() if l.strip()]
        try:
            return json.loads(dong[-1])
        except (IndexError, ValueError):
            return {'ok': False, 'error': f'chuoi_tai: không đọc được JSON (exit {p.returncode})'}

    # ---- kiểm điều kiện -----------------------------------------------------------------------
    def commit(self):
        try:
            c = subprocess.run(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], stdout=subprocess.PIPE,
                               stderr=subprocess.DEVNULL, timeout=30, check=True).stdout.decode().strip()
            ban = subprocess.run(['git', '-C', str(REPO), 'status', '--porcelain', '--', 'load', 'campaigns',
                                  'inventory'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=30,
                                 check=True).stdout.decode().strip()
            return c, bool(ban)
        except (OSError, subprocess.SubprocessError):
            return None, True

    def ly_do_dung(self, commit0):
        for p in STOP_FILES + [self.kho / 'DUNG']:
            if p.exists():
                return 'có file ' + str(p)
        c, ban = self.commit()
        if c != commit0:
            return f'commit /opt/rca-lab đổi giữa chuỗi: {commit0} → {c}'
        if ban:
            return 'cây repo lab bẩn ở load/campaigns/inventory'
        return None

    def kiem_telemetry(self, bat_dau, ket_thuc):
        """Hai truy vấn nhẹ: số mẫu count gateway và job up trong cửa sổ lượt (phát hiện sớm mất quan sát, I11)."""
        dai = max(60, int(ket_thuc - bat_dau))
        q = {
            'mau_gateway': f'sum(count_over_time(http_server_request_duration_seconds_count{{service_name="api-gateway"}}[{dai}s]))',
            'job_up_min': f'min(min_over_time(up[{dai}s]))',
        }
        out = {}
        for k, e in q.items():
            try:
                url = PROM + '/api/v1/query?' + urllib.parse.urlencode({'query': e, 'time': ket_thuc})
                with urllib.request.urlopen(url, timeout=60) as r:
                    res = json.load(r)['data']['result']
                out[k] = float(res[0]['value'][1]) if res else 0.0
            except Exception as ex:
                out[k] = None
                out[k + '_loi'] = type(ex).__name__
            time.sleep(0.3)
        return out

    # ---- một lượt -------------------------------------------------------------------------------
    def lenh_start(self, l):
        args = ['start', '--tag', l['tag'], '--seconds', str(l['seconds'])]
        if l.get('buoc_tai'):
            args += ['--buoc-tai', str(l['buoc_tai']), '--multiplier', str(l['multiplier'])]
        return args

    def cho_xong(self, l):
        han = time.time() + l['seconds'] + GRACEFUL_S + QUA_HAN_S
        loi_lien = 0
        da_stop = False
        while True:
            g = self.tl('get', '--tag', l['tag'], timeout=180)
            if g.get('ok'):
                loi_lien = 0
                st = g['result']['state']
                if not st.get('Running'):
                    return st
                if time.time() > han and not da_stop:
                    s = self.tl('stop', '--tag', l['tag'], timeout=300)  # luôn có --tag (I8)
                    self.ghi('qua_han_stop', tag=l['tag'], ket_qua=s)
                    da_stop = True
            else:
                loi_lien += 1
                self.ghi('get_loi', tag=l['tag'], loi=g.get('error'), lan=loi_lien)
                if loi_lien >= 20:  # tai_linux giấu stderr SSH nên không phân biệt được 'không có container'
                    return None
            time.sleep(NHIP_GET_S)

    def nhan(self, l):
        for lan in range(1, 4):
            r = self.tl('receive', '--tag', l['tag'], timeout=900)
            if r.get('ok'):
                return r
            self.ghi('nhan_loi', tag=l['tag'], loi=r.get('error'), lan=lan)
            time.sleep(2 * NHIP_GET_S)
        return None

    def chay_luot(self, l, da_phat):
        tag = l['tag']
        if not da_phat:
            self.ghi('sap_phat', tag=tag, thu_tu=l['thu_tu'], lenh=['tai_linux.py', *self.lenh_start(l)])
            self.trang_thai(tag=tag, buoc='start', thu_tu=l['thu_tu'])
            r = self.tl(*self.lenh_start(l), timeout=900)
            if not r.get('ok'):
                loi = str(r.get('error'))
                self.ghi('phat_loi', tag=tag, loi=loi)
                g = self.tl('get', '--tag', tag, timeout=180)
                if not g.get('ok'):  # không có container: lượt chưa chạy
                    chung = any(s in loi for s in LOI_CHUNG)
                    self.ghi('hong', tag=tag, ly_do='start lỗi, không có container', loi_chung=chung)
                    return 'loi_chung' if chung else 'hong_start'
            else:
                self.ghi('phat', tag=tag, ket_qua=r['result'])
        else:
            self.ghi('tiep_nhan', tag=tag, ghi_chu='đã sap_phat ở lần chạy trước; không start lại')
        self.trang_thai(tag=tag, buoc='cho_xong', thu_tu=l['thu_tu'])
        st = self.cho_xong(l)
        if st is None:
            self.ghi('hong', tag=tag, ly_do='không đọc được trạng thái container')
            return 'hong'
        self.ghi('xong', tag=tag, state=st)
        self.trang_thai(tag=tag, buoc='receive', thu_tu=l['thu_tu'])
        r = self.nhan(l)
        if r is None:
            self.ghi('hong', tag=tag, ly_do='receive lỗi 3 lần; dữ liệu giữ trên máy tải')
            return 'hong'
        self.ghi('nhan', tag=tag, ket_qua={k: r['result'].get(k) for k in
                                           ('destination', 'hashesMatched', 'outputsManifestSha256')})
        try:
            bd = dt.datetime.fromisoformat(st['StartedAt'][:26].rstrip('Z') + '+00:00').timestamp()
            kt = dt.datetime.fromisoformat(st['FinishedAt'][:26].rstrip('Z') + '+00:00').timestamp()
        except (KeyError, ValueError):
            bd = kt = None
        if bd and kt:
            k = self.kiem_telemetry(bd, kt)
            self.ghi('kiem_telemetry', tag=tag, ket_qua=k)
            if k.get('mau_gateway') == 0.0:
                return 'mat_telemetry'
        bad = st.get('ExitCode') != 0 or st.get('OOMKilled')
        return 'xong_loi_container' if bad else 'xong'

    # ---- chuỗi ------------------------------------------------------------------------------------
    def chay(self, ke_hoach, h):
        commit0, ban = self.commit()
        self.ghi('bat_dau_chuoi', ke_hoach=self.a.ke_hoach, sha256=h, lab_commit=commit0, cay_ban=ban,
                 so_luot=len(ke_hoach), pid=os.getpid())
        hong_lien = 0
        for l in ke_hoach:
            tag = l['tag']
            if 'nhan' in self.da_ghi.get(tag, set()) or 'hong' in self.da_ghi.get(tag, set()):
                self.ghi('bo_qua', tag=tag, ly_do='đã kết thúc ở lần chạy trước')
                continue
            ld = self.ly_do_dung(commit0)
            if ld:
                self.ghi('dung_chuoi', ly_do=ld, truoc_tag=tag)
                self.trang_thai(buoc='dung', ly_do=ld)
                return 2
            kq = self.chay_luot(l, 'sap_phat' in self.da_ghi.get(tag, set()))
            self.ghi('ket_qua_luot', tag=tag, ket_qua=kq)
            if kq in ('loi_chung', 'mat_telemetry'):
                self.ghi('dung_chuoi', ly_do=kq, sau_tag=tag)
                self.trang_thai(buoc='dung', ly_do=kq)
                return 3
            hong_lien = hong_lien + 1 if kq == 'hong_start' else 0
            if hong_lien >= 2:
                self.ghi('dung_chuoi', ly_do='2 lượt liền không start được', sau_tag=tag)
                self.trang_thai(buoc='dung', ly_do='2 lượt liền không start được')
                return 3
        self.ghi('xong_chuoi')
        self.trang_thai(buoc='xong_chuoi')
        return 0

    def chay_kho(self, ke_hoach, h):
        """Không phát tải: kiểm kế hoạch, điều kiện dừng, tag chưa dùng (get chỉ đọc), in đúng lệnh sẽ gọi."""
        commit0, ban = self.commit()
        out = {'che_do': 'chay_kho', 'ke_hoach': self.a.ke_hoach, 'sha256': h, 'lab_commit': commit0,
               'cay_ban': ban, 'ly_do_dung_neu_chay': self.ly_do_dung(commit0), 'luot': []}
        for l in ke_hoach:
            g = self.tl('get', '--tag', l['tag'], timeout=180)
            out['luot'].append({'thu_tu': l['thu_tu'], 'tag': l['tag'],
                                'lenh': ['python3', str(self.tai_linux), *self.lenh_start(l)],
                                'tag_chua_dung_tren_may_tai': not g.get('ok'),
                                'get': g.get('error') if not g.get('ok') else 'CONTAINER ĐÃ TỒN TẠI',
                                'tai_out_ton_tai': (Path('/srv/rca-lab/load-controller/tai-out') / l['tag']).exists(),
                                'da_ghi_nhat_ky': sorted(self.da_ghi.get(l['tag'], set()))})
            time.sleep(0.3)
        out['tong_giay_tai'] = sum(l['seconds'] for l in ke_hoach)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        (self.kho / ('chay-kho-' + dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ') + '.json')
         ).write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding='utf-8')
        return 0


def doc_ke_hoach(path, h):
    raw = Path(path).read_bytes()
    thuc = hashlib.sha256(raw).hexdigest()
    if thuc != h:
        raise SystemExit(f'sha256 kế hoạch {thuc} khác --sha256 {h}; từ chối')
    luot = json.loads(raw)['luot']
    tags = [l['tag'] for l in luot]
    if len(set(tags)) != len(tags):
        raise SystemExit('tag trùng trong kế hoạch')
    for l in luot:
        if not TAG_RE.fullmatch(l['tag']):
            raise SystemExit('tag sai dạng: ' + l['tag'])
        if not (1 <= int(l['seconds']) <= 3600) or not (1 <= int(l.get('multiplier', 1)) <= 3):
            raise SystemExit('seconds/multiplier ngoài giới hạn tai_linux: ' + l['tag'])
        if l.get('buoc_tai') and not (1 <= int(l['buoc_tai']) < int(l['seconds'])):
            raise SystemExit('buoc_tai phải nhỏ hơn seconds: ' + l['tag'])
    if [l['thu_tu'] for l in luot] != sorted(l['thu_tu'] for l in luot):
        raise SystemExit('luot không theo thứ tự thu_tu')
    return luot, thuc


def main():
    # stdout có thể là file với locale C/ANSI (nohup): không để print tiếng Việt làm chết chuỗi giữa chừng
    sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
    ap = argparse.ArgumentParser()
    ap.add_argument('--ke-hoach', required=True)
    ap.add_argument('--sha256', required=True)
    ap.add_argument('--kho', required=True)
    ap.add_argument('--chay-kho', action='store_true')
    ap.add_argument('--tai-linux', default=str(TAI_LINUX))
    a = ap.parse_args()
    luot, h = doc_ke_hoach(a.ke_hoach, a.sha256)
    c = Chuoi(a)
    if a.chay_kho:
        return c.chay_kho(luot, h)
    lock = open(c.kho / 'chuoi.lock', 'a')
    if fcntl:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise SystemExit('chuỗi khác đang chạy trên cùng thư mục kho')
    return c.chay(luot, h)


if __name__ == '__main__':
    sys.exit(main())
