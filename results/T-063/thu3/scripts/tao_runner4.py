# -*- coding: utf-8 -*-
"""T-063 thu3 — sinh runner4.py từ results/T-063/chay/runner3.py (không sửa runner3). Mỗi phép thay có assert.
Dùng: py -3 -B results/T-063/thu3/scripts/tao_runner4.py  → results/T-063/thu3/scripts/runner4.py
Khác runner3 (lý do: results/T-063/thu3/KE-HOACH.md §7, runner4-diff.md):
 1. bộ tiêm ~/inj3.py thay ~/inj2.py (ô thu bù 3, đầu dò queue/pool);
 2. bậc tải theo từng chu kỳ: khóa "multiplier" trong lịch → tai_linux --multiplier (cả lượt, không --buoc-tai);
 3. sổ/nhật ký/trạng thái tên thu3 (so-thu3.jsonl, nhat-ky-3.jsonl, trang-thai-3.json), mốc thu3-begin/thu3-end, tag t3-;
 4. RCA_PHASE (giây, mặc định 600) CHỈ cho chạy thử ngắn; tải dài 3×PHASE; lượt chính không đặt biến này;
 5. lịch mặc định ~/rca-dieu-phoi/lich-3.json.
Logic chu kỳ, đầu dò t−240/t+60/t+330/hoi+60, bao_dam_sach, thử lại tải, stage lại khi M1 lỗi: giữ nguyên.
"""
import ast
from pathlib import Path

R = Path(__file__).resolve().parents[4]
s = (R / 'results/T-063/chay/runner3.py').read_text(encoding='utf-8')


def thay(cu, moi, n=1):
    global s
    assert s.count(cu) == n, (s.count(cu), cu[:80])
    s = s.replace(cu, moi)


thay('"""T-063 bộ chạy bản 3 — chạy TRÊN exp-obs', '"""T-063 bộ chạy bản 4 (thu bù 3; sinh bằng results/T-063/thu3/scripts/tao_runner4.py từ runner3.py) — chạy TRÊN exp-obs')
thay("CHAY = OUTR / 'chay'; SO = OUTR / 'tiem-loi/so-thu2.jsonl'; CA = OUTR / 'ca'",
     "CHAY = OUTR / 'chay'; SO = OUTR / 'tiem-loi/so-thu3.jsonl'; CA = OUTR / 'ca'")
thay('PHASE = 600\n', "PHASE = int(os.environ.get('RCA_PHASE', '600'))  # chỉ chạy thử ngắn mới đặt; lượt chính = 600\n")
thay("open(CHAY / 'nhat-ky-2.jsonl', 'a'", "open(CHAY / 'nhat-ky-3.jsonl', 'a'")
thay("p = CHAY / 'trang-thai-2.json'", "p = CHAY / 'trang-thai-3.json'")
thay("cmd = f'python3 ~/inj2.py {op} {cell}'", "cmd = f'python3 ~/inj3.py {op} {cell}'")
thay("ssh('app', 'python3 ~/inj2.py ensure', timeout=60)", "ssh('app', 'python3 ~/inj3.py ensure', timeout=60)", n=2)
thay("""def start_load(tag, flash=False, seconds=1800):
    extra = ['--buoc-tai', 600, '--multiplier', 3] if flash else []""",
     """def start_load(tag, flash=False, seconds=None, mult=1):
    seconds = seconds or 3 * PHASE
    extra = ['--buoc-tai', PHASE, '--multiplier', 3] if flash else (['--multiplier', mult] if mult > 1 else [])""")
thay("log('load started', tag=tag, flash=flash, out=", "log('load started', tag=tag, flash=flash, mult=mult, out=")
thay("ledger('thu2-begin', lich=", "ledger('thu3-begin', phase_s=PHASE, lich=")
thay("cell = it['o']; oid = secrets.token_hex(4); tag = 't2-' + oid;",
     "cell = it['o']; mult = int(it.get('multiplier', 1)); oid = secrets.token_hex(4); tag = 't3-' + oid;")
thay("ledger('cycle-begin', i=i, opaque_id=oid, cell=cell, load_tag=tag)",
     "ledger('cycle-begin', i=i, opaque_id=oid, cell=cell, load_tag=tag, multiplier=mult)")
thay("S = start_load(tag, flash=flash)", "S = start_load(tag, flash=flash, mult=mult)", n=2)
thay("if cell in ('BINH-THUONG', 'FLASH-HEALTHY'):", "if cell in ('BINH-THUONG', 'FLASH-HEALTHY', 'BINH-THUONG-X3'):")
thay("ledger('thu2-end'); state(phase='XONG')", "ledger('thu3-end'); state(phase='XONG')")
thay("lich = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--lich' else BASE / 'lich-2.json'",
     "lich = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--lich' else BASE / 'lich-3.json'")
thay("Dùng (trên exp-obs, thư mục ~/rca-dieu-phoi): nohup setsid python3 -B runner3.py thu --lich lich-2.json > chay/runner3.out 2>&1 &",
     "Dùng (trên exp-obs): RCA_DP_OUT=~/rca-dieu-phoi/thu3 setsid -f nohup python3 -B runner4.py thu --lich lich-3.json > thu3-runner4.out 2>&1 < /dev/null")
thay("- Tiêm: ~/inj2.py trên exp-app (results/T-063/tiem-loi/inj2.py).", "- Tiêm: ~/inj3.py trên exp-app (results/T-063/thu3/scripts/inj3.py).")
thay('"""Lỗi từ inj2 (ssh', '"""Lỗi từ inj3 (ssh')
thay("RuntimeError(f'inj2 {op}: '", "RuntimeError(f'inj3 {op}: '")
assert "inj2" not in s
ast.parse(s)
(R / 'results/T-063/thu3/scripts/runner4.py').write_text(s, encoding='utf-8', newline='\n')
print('runner4.py OK')
