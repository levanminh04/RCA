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
# Chuỗi 19 (T-070, 24/11): chờ Codex hồi usage (22:43Z) rồi chạy theo ưu tiên: SQL E6 → bộ chấm v2d → nháp W9a.
import datetime as _dt
while _dt.datetime.now(_dt.timezone.utc) < _dt.datetime(2026,11,23,22,44,tzinfo=_dt.timezone.utc): time.sleep(30)
chay('CX-39', (D/'CX-39-brief.md').read_text(encoding='utf-8'))
chay('CX-39b', 'Bạn là phiên Codex THỨ HAI, độc lập với phiên trước. Chỉ đọc; không sửa file, không SSH, không commit, không subagent. Bước 1 (trước khi mở kết luận phiên trước): tự soát {task} theo đúng prompt gốc ở results/T-070/codex/{ma}-brief.md. Bước 2: đọc results/T-070/codex/{ma}-tin-cuoi.md; với từng điểm ghi ĐÚNG / ĐÚNG MỘT PHẦN / SAI / CHƯA KIỂM ĐƯỢC kèm bằng chứng riêng; nêu riêng lỗi mới. Không tìm cho đủ số lượng. Cuối: bảng (điểm, nguồn, kết luận, CHẶN/KHÔNG CHẶN, sửa tối thiểu) và kết luận. Tiếng Việt, ngắn.'.format(task='bộ SQL và nháp E6 bản 4 của T-074', ma='CX-39'))
chay('CX-40', (D/'CX-40-brief.md').read_text(encoding='utf-8'))
chay('CX-40b', 'Bạn là phiên Codex THỨ HAI, độc lập với phiên trước. Chỉ đọc; không sửa file, không SSH, không commit, không subagent. Bước 1 (trước khi mở kết luận phiên trước): tự soát {task} theo đúng prompt gốc ở results/T-070/codex/{ma}-brief.md. Bước 2: đọc results/T-070/codex/{ma}-tin-cuoi.md; với từng điểm ghi ĐÚNG / ĐÚNG MỘT PHẦN / SAI / CHƯA KIỂM ĐƯỢC kèm bằng chứng riêng; nêu riêng lỗi mới. Không tìm cho đủ số lượng. Cuối: bảng (điểm, nguồn, kết luận, CHẶN/KHÔNG CHẶN, sửa tối thiểu) và kết luận. Tiếng Việt, ngắn.'.format(task='bộ chấm v2d và chữ WHY-110 của T-072', ma='CX-40'))
chay('CX-38', 'Bạn là Codex soạn NHÁP SPEC W9a (diễn tập demo) để điều phối và Minh xem; chỉ đọc, KHÔNG ghi file (trả lời trong chat; điều phối lưu). Không subagent. Nguồn: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2 (W9a: kịch bản demo, video, phát lại offline, diễn tập 2 lần; xong khi diễn tập không lỗi); tasks/_MAU/SPEC.md (mẫu); docs/DECISIONS.md (khối 23/11: W8/LLM hoãn — demo KHÔNG có LLM; Q9: E7 được đi trước E6 nếu đủ điều kiện; phương án C: W7 chạy đêm, diễn tập xếp ban ngày giữa các khối); results/T-073/trien-khai-e5.md và e5-ket-qua.md (cách bật dịch vụ chế độ (b), commit E5/P/H, giới hạn live-down, chú thích hash T-064 sai); results/T-072/troi-p95-e2-e4.md (chạy tải ≥ 5 phút trước phần phát hiện, giữ cảnh báo đầu lượt); tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md, HOP-DONG.md (I7, I9, I15); results/T-074/e6-spec-nhap-2.md (hạn bán hiện 2026-12-02; E6 gia hạn). Nháp theo đủ mục mẫu SPEC: mục tiêu, câu hỏi/phép kiểm, đầu vào, đầu ra, phạm vi ghi, các bước (bật lại dịch vụ với vùng ghi mới — commit E5 ghim nguồn t073-e5-001 nên cần nguồn/commit mới hay dùng lại; kịch bản: tải → tiêm ô demo → cảnh báo → ca hiện dashboard → mở phát lại; hoàn tác), kiểm đúng đắn, tiêu chí xong (2 lần không lỗi, định nghĩa "lỗi"), mục lỗi 10/50/99% (luật 21), chi phí giờ máy, rủi ro, việc cần Minh quyết (mỗi việc có đề xuất, lý do, mặt trái). Ghi rõ phần chưa kiểm. Tiếng Việt, ngắn.')
log(su_kien='het_chuoi_19')
