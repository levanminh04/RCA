# Mô phỏng nhánh lỗi của runner2 (theo REVIEW T-063 R1/R3), trong bộ nhớ: không tải, không tiêm, không SSH.
import json, queue, types, sys
src = open('results/T-063/chay/runner2.py', encoding='utf-8').read()
ns = {'__name__': 'mo_phong'}; exec(compile(src, 'runner2.py', 'exec'), ns)
class Plan:
    def read_text(self, **k): return json.dumps({'chu_ky': [{'o': 'PAUSE-PAYMENT'}, {'o': 'BINH-THUONG'}]})
    def read_bytes(self): return self.read_text().encode()
class T:
    def __init__(self, **k): pass
    def start(self): pass
def chay(inj):
    ev = []
    ns.update(Path=lambda p: Plan(), log=lambda *a, **k: None, state=lambda **k: None, ledger=lambda e, **k: ev.append(e),
              stopped=lambda: False, wait_until=lambda *a: None, start_load=lambda *a, **k: 100000, finish_load=lambda *a: None,
              ssh=lambda *a, **k: '', M1Q=queue.Queue(), inj=inj,
              threading=types.SimpleNamespace(Thread=T, enumerate=lambda: []), time=types.SimpleNamespace(sleep=lambda *a: None, time=lambda: 0))
    ns['chay_lich']('x'); return ev
# A: stop và cleanup đều lỗi, verify báo bẩn
def a(op, cell='-', seconds=None):
    if op in ('stop', 'cleanup'): raise RuntimeError('mất SSH khi phục hồi')
    if op == 'verify': return {'op': 'verify', 'sach': op != 'verify' or a.lan == 0, 'con_lai': [] if a.lan == 0 else ['pause:payment']}
    if op == 'start': a.lan = 1
    return {'op': op}
a.lan = 0
evA = chay(a)
print('A cycle-begin', evA.count('cycle-begin'), '| run-abort-dirty', 'run-abort-dirty' in evA, '| sự kiện', evA)
