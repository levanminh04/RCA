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
# Chuỗi 5 (T-070): phản biện kết quả W4 — hai phiên Codex lần lượt, độc lập (Minh 22/11).
chay('CX-19', (D/'CX-19-brief.md').read_text(encoding='utf-8'))
PB = ('Bạn là phiên Codex THỨ HAI, độc lập với phiên trước. Chỉ đọc; không sửa file, không SSH, không commit. '
      'Bước 1 (trước khi mở kết luận phiên trước): tự soát {task} theo đúng prompt gốc ở results/T-070/codex/{ma}-brief.md, '
      'tìm lỗi ảnh hưởng tính đúng. Bước 2: đọc kết luận phiên trước ở results/T-070/codex/{ma}-tin-cuoi.md; với từng điểm của phiên trước '
      'ghi ĐÚNG / ĐÚNG MỘT PHẦN / SAI / CHƯA KIỂM ĐƯỢC kèm bằng chứng riêng (file:dòng, lệnh); phản bác nếu đề xuất không hợp lý; nêu riêng các lỗi '
      'mới mà phiên trước chưa thấy. Không tìm cho đủ số lượng. Cuối: bảng (điểm, nguồn: phiên 1/mới, kết luận, CHẶN/KHÔNG CHẶN, sửa tối thiểu, '
      'loại: lỗi nhỏ sửa được ngay / cần người làm / cần Minh). Tiếng Việt, ngắn.')
chay('CX-19b', PB.format(task='kết quả W4 (T-071, T-072)', ma='CX-19'))
log(su_kien='het_chuoi_5')
