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
# 1. chạy lại CX-13, CX-14 (lần 1 hỏng do Codex hết usage; giữ *.hong-het-usage-1.jsonl); CX-15 đã xong
for ma in ('CX-13','CX-14'):
    if not xong(ma): chay(ma, (D/f'{ma}-brief.md').read_text(encoding='utf-8'))
for ma in ('CX-13','CX-14','CX-15'):
    while not xong(ma):
        p=D/f'{ma}.jsonl'
        if p.exists() and het_usage(ma):
            (D/'HET-USAGE.txt').write_text(f'{now()} {ma}: nghi Codex hết usage. Báo Minh đổi tài khoản.\n',encoding='utf-8'); raise SystemExit(2)
        time.sleep(60)
    tin_cuoi(ma); log(viec=ma, su_kien='da_co')
# 2. vòng B: phiên Codex thứ hai, độc lập trước rồi phản biện phiên một
PB = ('Bạn là phiên Codex THỨ HAI, độc lập với phiên trước. Chỉ đọc; không sửa file, không SSH, không commit. '
      'Bước 1 (trước khi mở kết luận phiên trước): tự soát {task} theo đúng prompt gốc ở results/T-070/codex/{ma}-brief.md, '
      'tìm lỗi ảnh hưởng tính đúng. Bước 2: đọc kết luận phiên trước ở results/T-070/codex/{ma}-tin-cuoi.md; với từng điểm của phiên trước '
      'ghi ĐÚNG / ĐÚNG MỘT PHẦN / SAI / CHƯA KIỂM ĐƯỢC kèm bằng chứng riêng (file:dòng, lệnh); phản bác nếu đề xuất không hợp lý; nêu riêng các lỗi '
      'mới mà phiên trước chưa thấy. Không tìm cho đủ số lượng. Cuối: bảng (điểm, nguồn: phiên 1/mới, kết luận, CHẶN/KHÔNG CHẶN, sửa tối thiểu, '
      'loại: lỗi nhỏ sửa được ngay / cần người làm / cần Minh). Tiếng Việt, ngắn.')
for ma,task in (('CX-13','T-066'),('CX-14','T-068'),('CX-15','T-074 W6 bản 3')):
    chay(ma+'b', PB.format(task=task, ma=ma))
# 3. lỗi nhỏ: Codex sửa trien-khai-e5.md theo CX-11/CX-12, phiên khác kiểm
FIX = ('Bạn là Codex sửa lỗi nhỏ (Minh duyệt 22/11: "nếu có lỗi nhỏ thì có thể cho codex sửa và phiên khác kiểm"). '
       'CHỈ được sửa một file: D:/RCA-flashticket/results/T-073/trien-khai-e5.md. Không sửa file nào khác, không SSH, không commit, không chạy lệnh thay đổi máy. '
       'Trước khi sửa, chép nguyên file sang D:/RCA-flashticket/results/T-073/trien-khai-e5.truoc-cx16.md (giữ bản cũ). '
       'Sửa đúng các điểm sau (nguồn: results/T-070/codex/CX-11-tin-cuoi.md mục CHẶN và KHÔNG CHẶN; CX-12-tin-cuoi.md dòng T-073): '
       '(1) chuyển kiểm K8 xuống sau S4-8, trước khi tiêm; (2) kiểm HEAD, cây sạch và đủ job I7 (chuoi_tai|runner4|tai_linux|stage_b|orchestrator|inj3) ngay trước mỗi lần đổi checkout, kể cả hoàn tác; '
       '(3) tách inj3 ensure/verify ra khỏi bước "chỉ đọc" S4-1 thành bước riêng có ghi là thay đổi trạng thái; (4) thêm bước chụp sha256 và dòng cuối của /srv/rca-lab/runs/t072-e3-01/webhook.jsonl trước khi bấm Test ở S4; '
       '(5) ghi cách quan sát ca mới (trang sự cố refresh rỗng: phải mở lại/làm mới trang; ghi giờ thấy ca) và thêm bước kiểm dashboard lưu trữ; (6) ghi ô đã bốc: PAUSE-PAYMENT (hạt 32323232, LOG T-073). '
       'Không đổi nội dung khoa học (N, tiêu chí, ô). Cuối: liệt kê từng thay đổi (đoạn cũ → mới) và sha256 file mới.')
chay('CX-16', FIX, 'workspace-write')
KT = ('Bạn là phiên Codex kiểm bản sửa, độc lập với phiên sửa. Chỉ đọc. So D:/RCA-flashticket/results/T-073/trien-khai-e5.truoc-cx16.md với trien-khai-e5.md (diff), '
      'đối chiếu yêu cầu ở results/T-070/codex/CX-16-brief.md và lỗi gốc ở CX-11-tin-cuoi.md. Kiểm: đủ 6 điểm; không đổi nội dung khoa học; không sửa file nào khác '
      '(git -C D:/RCA-flashticket status --short results/T-073 và các thư mục khác); thứ tự S4 mới chạy được trên code thật (trien-khai, inj3.py, orchestrator.py). '
      'Cuối: ĐẠT / CHƯA ĐẠT từng điểm, lỗi còn lại. Tiếng Việt, ngắn.')
chay('CX-16b', KT)
log(su_kien='het_chuoi')
