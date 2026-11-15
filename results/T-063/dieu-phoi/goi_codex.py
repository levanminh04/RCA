# -*- coding: utf-8 -*-
"""Gọi một lượt Codex theo brief, nhận biết hết hạn mức, chờ tới giờ hồi rồi gọi tiếp (T-063 bước 1).

Cách dùng (từ D:/RCA-flashticket):
    py -3 results/T-063/dieu-phoi/goi_codex.py --ten L1 --brief results/T-062/codex/L1-brief.md \
        --thu-muc results/T-062/codex [--toi-da 8] [--effort high]

Đầu ra trong --thu-muc (mọi giờ là UTC):
    <ten>-lan<k>.log        stdout+stderr nguyên văn của lần gọi thứ k (giữ mọi lần)
    <ten>-ketqua.md         thông điệp cuối của Codex (-o)
    <ten>-su-kien.jsonl     sự kiện: bat_dau, ket_thuc(rc), het_han_muc(giờ hồi), cho, goi_tiep, xong, loi
    <ten>-trang-thai.json   trạng thái hiện tại (dang_chay / cho_han_muc / xong / loi / dung) — phiên điều phối đọc file này

Nguyên tắc:
- Brief truyền qua stdin dạng byte UTF-8 (không qua đường ống PowerShell, tránh lỗi mã hóa đã gặp ở T-062).
- Hết hạn mức: đọc "try again at <giờ>" trong log (giờ địa phương của máy), chờ tới giờ đó + 5 phút,
  rồi `codex exec resume <session id>` với lời nhắc làm tiếp theo checkpoint của nhánh. Không đọc được giờ thì thử lại sau 30 phút.
- rc != 0 không do hạn mức: dừng ở trạng thái `loi` để phiên điều phối xem, không tự lặp.
- Có file D:/RCA-overnight/STOP: dừng ở ranh giới (trước lần gọi kế tiếp / trong lúc chờ), trạng thái `dung`.
- Biến môi trường CODEX_GIA_LAP=<đường dẫn script .py>: thay codex bằng script giả (chỉ dùng cho phép thử mô phỏng).
"""
import argparse, datetime as dt, json, os, re, shutil, subprocess, sys, time
from pathlib import Path

STOP = Path('D:/RCA-overnight/STOP')
RE_HAN = re.compile(r"(hit your usage limit|usage limit|rate limit reached|quota exceeded)", re.I)
RE_GIO = re.compile(r"try again at\s+(?:(?P<ngay>[A-Z][a-z]{2,8}\.? \d{1,2}(?:st|nd|rd|th)?,? \d{4}),?\s+)?(?P<gio>\d{1,2}:\d{2}\s*[AP]M)", re.I)
RE_SID = re.compile(r"session id:\s*([0-9a-f-]{36})", re.I)

LOI_TIEP = ("Lượt trước của bạn dừng giữa chừng vì hết hạn mức. Hạn mức đã hồi. "
            "Làm tiếp đúng nhiệm vụ trong brief ban đầu: đọc checkpoint của nhánh (đường dẫn ghi trong brief), "
            "kiểm đầu ra đã có, không làm lại phần đã có đầu ra hợp lệ, cập nhật checkpoint rồi tiếp tục tới khi xong. "
            "Cuối lượt viết báo cáo ngắn theo mẫu trong brief.")


def bay_gio():
    return dt.datetime.now(dt.timezone.utc)


def iso(t):
    return t.strftime('%Y-%m-%dT%H:%M:%SZ')


def gio_hoi(text, now_utc):
    """Trả về thời điểm hồi (UTC) đọc từ thông báo, hoặc None."""
    ms = list(RE_GIO.finditer(text))
    if not ms:
        return None
    m = ms[-1]
    gio = dt.datetime.strptime(m.group('gio').replace(' ', '').upper(), '%I:%M%p').time()
    local_now = now_utc.astimezone()  # múi giờ của máy (thông báo Codex theo giờ địa phương)
    tz = local_now.tzinfo
    if m.group('ngay'):
        s = re.sub(r'(st|nd|rd|th),?', ',', m.group('ngay')).replace('.', '').replace(',,', ',')
        s = re.sub(r',?\s+', ' ', s).strip()
        d = dt.datetime.strptime(s, '%b %d %Y' if len(s.split()[0]) == 3 else '%B %d %Y').date()
        cand = dt.datetime.combine(d, gio, tz)
    else:
        cand = dt.datetime.combine(local_now.date(), gio, tz)
        if cand < local_now - dt.timedelta(minutes=2):
            cand += dt.timedelta(days=1)
    return cand.astimezone(dt.timezone.utc)


class Nhanh:
    def __init__(self, a):
        self.a = a
        self.d = Path(a.thu_muc)
        self.d.mkdir(parents=True, exist_ok=True)
        self.ev = self.d / f'{a.ten}-su-kien.jsonl'
        self.st = self.d / f'{a.ten}-trang-thai.json'

    def ghi(self, loai, **kw):
        rec = {'t': iso(bay_gio()), 'ten': self.a.ten, 'su_kien': loai, **kw}
        with open(self.ev, 'a', encoding='utf-8') as f:
            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
        print(json.dumps(rec, ensure_ascii=False), flush=True)

    def trang_thai(self, tt, **kw):
        rec = {'cap_nhat': iso(bay_gio()), 'ten': self.a.ten, 'trang_thai': tt, 'pid': os.getpid(),
               'brief': self.a.brief, **kw}
        tmp = self.st.with_suffix('.tmp')
        tmp.write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding='utf-8')
        os.replace(tmp, self.st)

    def lenh(self, sid):
        gl = os.environ.get('CODEX_GIA_LAP')
        if gl:
            base = [sys.executable, gl]
        else:
            exe = shutil.which('codex.cmd') or shutil.which('codex')
            if not exe:
                raise SystemExit('không tìm thấy codex')
            base = [exe]
        if self.a.che_do == 'sandbox':
            che_do = ['-c', 'sandbox_mode="workspace-write"', '-c', 'approval_policy="never"',
                      '-c', 'sandbox_workspace_write.network_access=true',
                      '-c', 'sandbox_workspace_write.writable_roots=[' + ','.join(f'"{w}"' for w in self.a.ghi_them) + ']']
        else:
            che_do = ['--dangerously-bypass-approvals-and-sandbox']
        common = ['--skip-git-repo-check'] + che_do + ['-m', self.a.model,
                  '-c', f'model_reasoning_effort={self.a.effort}', '-o', str(self.d / f'{self.a.ten}-ketqua.md')]
        if sid:
            if getattr(self, 'dung_brief_khi_tiep', False):
                self.dung_brief_khi_tiep = False  # lần đầu tiếp phiên: gửi brief bổ sung; các lần sau (hết hạn mức) gửi lời nhắc làm tiếp
                return base + ['exec', 'resume', sid] + common + ['-'], Path(self.a.brief).read_bytes()
            return base + ['exec', 'resume', sid] + common + ['-'], LOI_TIEP.encode('utf-8')
        return base + ['exec', '-C', self.a.cwd] + common + ['-'], Path(self.a.brief).read_bytes()

    def chay(self):
        sid = self.a.tiep_phien
        self.dung_brief_khi_tiep = bool(sid)
        for k in range(1, self.a.toi_da + 1):
            if STOP.exists():
                self.ghi('dung', ly_do='STOP'); self.trang_thai('dung'); return 3
            cmd, stdin = self.lenh(sid)
            log = self.d / f'{self.a.ten}-lan{k}.log'
            self.ghi('bat_dau', lan=k, resume=sid, log=log.name)
            self.trang_thai('dang_chay', lan=k, log=log.name, session=sid)
            t0 = time.time()
            with open(log, 'wb') as fo:
                p = subprocess.run(cmd, input=stdin, stdout=fo, stderr=subprocess.STDOUT, cwd=self.a.cwd)
            text = log.read_bytes().decode('utf-8', 'replace')
            m = RE_SID.findall(text)
            if m:
                sid = m[0] if sid is None else sid
            han = RE_HAN.search(text[-4000:]) is not None
            self.ghi('ket_thuc', lan=k, rc=p.returncode, giay=round(time.time() - t0, 1), session=sid, het_han_muc=han)
            if not han:
                if p.returncode == 0:
                    self.ghi('xong', lan=k); self.trang_thai('xong', lan=k, session=sid); return 0
                self.ghi('loi', lan=k, rc=p.returncode); self.trang_thai('loi', lan=k, rc=p.returncode, session=sid, log=log.name)
                return 1
            now = bay_gio()
            hoi = gio_hoi(text, now)
            cho_den = (hoi + dt.timedelta(minutes=self.a.them_phut)) if hoi else now + dt.timedelta(minutes=30)
            self.ghi('het_han_muc', lan=k, gio_hoi=iso(hoi) if hoi else None, cho_den=iso(cho_den))
            self.trang_thai('cho_han_muc', lan=k, gio_hoi=iso(hoi) if hoi else None, cho_den=iso(cho_den), session=sid)
            while bay_gio() < cho_den:
                if STOP.exists():
                    self.ghi('dung', ly_do='STOP'); self.trang_thai('dung'); return 3
                time.sleep(min(60, max(1, (cho_den - bay_gio()).total_seconds())))
            self.ghi('goi_tiep', lan_ke=k + 1, session=sid)
        self.ghi('loi', ly_do=f'quá {self.a.toi_da} lần'); self.trang_thai('loi', ly_do='qua_so_lan'); return 2


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--ten', required=True)
    ap.add_argument('--brief', required=True)
    ap.add_argument('--thu-muc', required=True)
    ap.add_argument('--cwd', default='D:/RCA-flashticket')
    ap.add_argument('--model', default='gpt-6.1-sol')
    ap.add_argument('--effort', default='high')
    ap.add_argument('--toi-da', type=int, default=8)
    ap.add_argument('--them-phut', type=float, default=5, help='chờ thêm sau giờ hồi')
    ap.add_argument('--che-do', choices=['sandbox', 'full'], default='sandbox',
                    help='sandbox: workspace-write + mạng + thư mục ghi thêm; full: bỏ sandbox')
    ap.add_argument('--ghi-them', nargs='*', default=['D:/Project/flash-ticket-platform'])
    ap.add_argument('--tiep-phien', help='session id Codex để tiếp (brief làm lời nhắn tiếp theo)')
    sys.exit(Nhanh(ap.parse_args()).chay())


if __name__ == '__main__':
    main()
