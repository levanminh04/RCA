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
# Chuỗi 4 (T-070, 22/11 ~19:2xZ): Codex kiểm độc lập bản sửa lượt 3 của T-073 (sau CX-17).
KT3 = ('Bạn là phiên Codex kiểm độc lập bản sửa lượt 3 của hướng dẫn E5 (người sửa: Claude T-073). Chỉ đọc; không sửa file, không SSH, không commit. '
       'So D:/RCA-flashticket/results/T-073/trien-khai-e5.truoc-t073-3.md với trien-khai-e5.md (diff); đọc patch/commit dự kiến ở D:/RCA-flashticket/results/T-073/commit-e5/ '
       'và diff worktree D:/Project/rca-lab-wt/T-073-e5 so với ecdeed2. Lỗi cần sửa: results/T-070/codex/CX-17-tin-cuoi.md (S4-7 phải thực sự mở sáu dashboard lưu trữ khi nguồn E5 hoạt động; '
       '§5 hoàn tác chạy trọn có deleteContactPoints thật; S4-6 dẫn health 13.3.0). Tự soát yêu cầu W5 (docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2, tasks/T-073-w5-rca-truc-tuyen/SPEC.md) trước khi đọc LOG T-073. '
       'Kiểm: (1) mỗi patch áp được lên đúng commit cha dự kiến (git apply --check trên bản sao tạm ngoài repo hoặc đọc kỹ ngữ cảnh), nội dung provider/deleteContactPoints đúng cú pháp provisioning Grafana 13; '
       '(2) chuỗi đổi checkout S4 và §5: mỗi lần đổi có I7, thứ tự không để Grafana ở trạng thái dở, hoàn tác đưa về đúng ecdeed2-tương đương (11 luật W4, một integration T-072, dashboard nguồn t065-l11-001); '
       '(3) S4-7 kiểm đúng tiêu chí W5, không thu hẹp; (4) không đổi khoa học (N 25 phút, tiêu chí, ô PAUSE-PAYMENT, hash hai file khóa theo LOG T-073); '
       '(5) phạm vi ghi; (6) mọi điểm mới. Mỗi điểm: ĐẠT/CHƯA ĐẠT, CHẶN/KHÔNG CHẶN, bằng chứng file:dòng, sửa tối thiểu. Cuối: đủ để trình Minh duyệt commit E5 chưa. Tiếng Việt, ngắn.')
chay('CX-18', KT3)
log(su_kien='het_chuoi_4')
