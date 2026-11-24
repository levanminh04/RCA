# Chuỗi Codex tự động (T-070, Minh duyệt 22/11: hai phiên Codex phản biện lẫn nhau, lỗi nhỏ Codex sửa và phiên khác kiểm).
import json, pathlib, subprocess, time, datetime, shutil
D = pathlib.Path('D:/RCA-flashticket/results/T-070/codex')
NK = D / 'chuoi' / 'nhat-ky.jsonl'
CMD = [shutil.which('codex.cmd') or shutil.which('codex') or 'codex.cmd','exec','-C','D:/RCA-flashticket','--add-dir','D:/Project/rca-lab-wt','--add-dir','D:/Project/flashticket-rca-lab','--add-dir','D:/RCA-ext/src/RCAEval','-m','gpt-6.2-astra','-c','model_reasoning_effort="high"','--json']
def now(): return datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def log(**k):
    with NK.open('a',encoding='utf-8') as f: f.write(json.dumps({'utc':now(),**k},ensure_ascii=False)+'\n')
def xong(ma):
    p = D/f'{ma}.jsonl'
    return p.exists() and '"turn.completed"' in p.read_text(encoding='utf-8',errors='replace')
def tin_cuoi(ma):
    msgs=[]
    for l in (D/f'{ma}.jsonl').read_text(encoding='utf-8',errors='replace').splitlines():
        try: d=json.loads(l)
        except: continue
        it=d.get('item') or {}
        if d.get('type')=='item.completed' and it.get('type') in ('agent_message','assistant_message'): msgs.append(it.get('text',''))
    s = msgs[-1] if msgs else ''
    (D/f'{ma}-tin-cuoi.md').write_text(s,encoding='utf-8'); return s
def het_usage(ma):
    t=(D/f'{ma}.jsonl').read_text(encoding='utf-8',errors='replace').lower()
    return any(x in t for x in ('usage limit','rate limit reached','quota exceeded','insufficient_quota','you\'ve hit your'))
KHONG_SUBAGENT = ('Yêu cầu của Minh (22/11): KHÔNG dùng subagent hay agent con; tự làm toàn bộ trong phiên này. '
                  'Đọc có chọn lọc (grep, đọc đúng đoạn cần), không đọc lại toàn bộ file lớn khi không cần.\n\n')
def chay(ma, brief, che_do='read-only'):
    if xong(ma):
        tin_cuoi(ma); log(viec=ma, su_kien='bo_qua_da_xong'); return
    if not brief.startswith('Yêu cầu của Minh (22/11): KHÔNG dùng subagent'): brief = KHONG_SUBAGENT + brief
    (D/f'{ma}-brief.md').write_text(brief,encoding='utf-8')
    log(viec=ma, su_kien='bat_dau', che_do=che_do)
    with (D/f'{ma}.jsonl').open('w',encoding='utf-8') as out:
        r=subprocess.run(CMD+['-s',che_do,'-'],input=brief,text=True,encoding='utf-8',stdout=out,stderr=subprocess.STDOUT)
    if not xong(ma):
        (D/'HET-USAGE.txt').write_text(f'{now()} {ma}: Codex dừng (rc={r.returncode}); nghi hết usage hoặc lỗi. Báo Minh đổi tài khoản Codex rồi chạy lại từ {ma}.\n',encoding='utf-8')
        log(viec=ma, su_kien='dung', rc=r.returncode); raise SystemExit(2)
    tin_cuoi(ma); log(viec=ma, su_kien='xong', rc=r.returncode)
# Chuỗi 22 (T-070, 24/11): kiểm lại T-072 v2e + WHY-110; chờ chuỗi 21 xong.
while not any('het_chuoi_21' in l for l in NK.read_text(encoding='utf-8').splitlines()): time.sleep(30)
chay('CX-44', (D/'CX-44-brief.md').read_text(encoding='utf-8'))
chay('CX-44b', 'Bạn là phiên Codex THỨ HAI, độc lập với phiên trước. Chỉ đọc; không sửa file, không SSH, không commit, không subagent. Bước 1 (trước khi mở kết luận phiên trước): tự soát {task} theo đúng prompt gốc ở results/T-070/codex/{ma}-brief.md. Bước 2: đọc results/T-070/codex/{ma}-tin-cuoi.md; với từng điểm ghi ĐÚNG / ĐÚNG MỘT PHẦN / SAI / CHƯA KIỂM ĐƯỢC kèm bằng chứng riêng; nêu riêng lỗi mới. Không tìm cho đủ số lượng. Cuối: bảng (điểm, nguồn, kết luận, CHẶN/KHÔNG CHẶN, sửa tối thiểu, loại: lỗi nhỏ Codex sửa được ngay / cần người làm / cần Minh). Tiếng Việt, ngắn.'.format(task='bộ chấm v2e và chữ WHY-110 của T-072', ma='CX-44'))
log(su_kien='het_chuoi_22')
