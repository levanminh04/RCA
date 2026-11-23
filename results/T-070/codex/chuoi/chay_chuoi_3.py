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
    if het_usage(ma) or not xong(ma):
        (D/'HET-USAGE.txt').write_text(f'{now()} {ma}: Codex dừng (rc={r.returncode}); nghi hết usage hoặc lỗi. Báo Minh đổi tài khoản Codex rồi chạy lại từ {ma}.\n',encoding='utf-8')
        log(viec=ma, su_kien='dung', rc=r.returncode); raise SystemExit(2)
    tin_cuoi(ma); log(viec=ma, su_kien='xong', rc=r.returncode)
# Chuỗi 3 (T-070, 22/11 ~19:2xZ): Codex kiểm độc lập bản sửa S4-6/S4-7 của T-073 (sau CX-16b).
KT2 = ('Bạn là phiên Codex kiểm độc lập bản sửa thứ hai của hướng dẫn E5 (người sửa: Claude T-073). Chỉ đọc; không sửa file, không SSH, không commit. '
       'So D:/RCA-flashticket/results/T-073/trien-khai-e5.truoc-t073-2.md với trien-khai-e5.md (diff). Lỗi gốc cần sửa: results/T-070/codex/CX-16b-tin-cuoi.md '
       '(S4-6 Test theo từng integration; S4-7 dashboard lưu trữ chưa chỉ commit chứa provider tạm) và giới hạn live-down (results/T-070/hop-nhat-cx13-16.md mục 1). '
       'Tự soát trước khi đọc LOG T-073. Kiểm: (1) S4-6 đúng với mã Grafana của phiên bản đang ghim (đọc mã thật nếu có trong repo/worktree, nêu rõ nếu không kiểm được); '
       '(2) cách kiểm dashboard lưu trữ mới có thực sự kiểm được điều tiêu chí W5 yêu cầu (dashboard hiện hành, lưu trữ, phát lại khi đổi nguồn JSON) hay chỉ kiểm file; nếu thu hẹp tiêu chí thì CHẶN; '
       '(3) thứ tự S4 và hoàn tác §5 chạy được trên code thật ở worktree D:/Project/rca-lab-wt/T-073-e5 (git -C ... diff, status); I7 ở mọi lần đổi checkout; '
       '(4) không đổi nội dung khoa học (N, tiêu chí, ô PAUSE-PAYMENT, hash hai file khóa results/T-073/khai-truoc-e5.json, khoa-boc-e5.json theo LOG T-073); '
       '(5) có ghi ra ngoài phạm vi không (git -C D:/RCA-flashticket status --short). Mỗi điểm: ĐẠT / CHƯA ĐẠT, CHẶN/KHÔNG CHẶN, bằng chứng file:dòng, sửa tối thiểu. '
       'Cuối: kết luận có đủ để trình Minh duyệt commit E5 không. Tiếng Việt, ngắn.')
chay('CX-17', KT2)
log(su_kien='het_chuoi_3')
