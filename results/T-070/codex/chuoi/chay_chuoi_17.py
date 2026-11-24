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
# Chuỗi 17 (T-070, 24/11 đêm): phương án C — việc vừa sức giao Codex.
chay('CX-34b', 'Bạn là phiên Codex THỨ HAI, độc lập với phiên trước. Chỉ đọc; không sửa file, không SSH, không commit, không subagent. Bước 1 (trước khi mở kết luận phiên trước): tự soát {task} theo đúng prompt gốc ở results/T-070/codex/{ma}-brief.md. Bước 2: đọc results/T-070/codex/{ma}-tin-cuoi.md; với từng điểm ghi ĐÚNG / ĐÚNG MỘT PHẦN / SAI / CHƯA KIỂM ĐƯỢC kèm bằng chứng riêng; nêu riêng lỗi mới. Không tìm cho đủ số lượng. Cuối: bảng (điểm, nguồn, kết luận, CHẶN/KHÔNG CHẶN, sửa tối thiểu). Tiếng Việt, ngắn.'.format(task='phản hồi và bản 2 của T-075', ma='CX-34'))
chay('CX-35', 'Bạn là Codex viết tài liệu đọc dự án (Minh duyệt 23/11 "hai việc nhẹ": sửa README repo lab cho đúng trạng thái, viết hướng dẫn đọc). Phạm vi: chỉ GHI đúng file được nêu; không sửa file khác, không ghi LOG/STATE/SPEC/WHY/DECISIONS/LESSONS, không SSH, không commit, không dùng subagent. Liệt kê file đã tạo/sửa kèm sha256. Tiếng Việt, câu ngắn.\nGHI ĐÚNG HAI FILE: (1) D:/Project/flashticket-rca-lab/README.md (sửa; checkout đang ở main = 1bb40ca, không đổi nhánh, không sửa file khác của repo lab); (2) D:/RCA-flashticket/docs/READING-GUIDE.md (file mới; kế hoạch W0 docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2). README lab: giữ phần giới thiệu ba repo và sơ đồ; sửa bảng thư mục và mục "Trạng thái" theo sự thật hiện tại (đọc git log main, AGENTS.md của repo lab): dịch vụ RCA trực tuyến chế độ (b) đang ở campaigns/online/ (rca-service/ chỉ có README, chưa chuyển); luật cảnh báo W4 ở observability/grafana/provisioning/alerting/t072-luat.yaml; bộ chuỗi tải load/controller/chuoi_tai.py; commit đang chạy trên exp-obs là 1bb40ca (main). Không hứa việc chưa làm; ghi rõ "tên thư mục/dashboard còn mang mã task (t065-…); tái cấu trúc để sau W7 (Minh 23/11)". READING-GUIDE (repo RCA): cho người mới (cô hướng dẫn, Minh) đọc dự án theo thứ tự: mục tiêu (DT18, MRP), kế hoạch giai đoạn 2, STATE, DECISIONS, WHY, cách đọc một task (SPEC/LOG/results), các task giai đoạn 2 T-066…T-075 mỗi task một dòng (làm gì, kết quả chính, file chính), nơi để dữ liệu ngoài git (D:/RCA-archive, data/README.md), repo lab đọc gì. Lấy thông tin từ file thật (docs/STATE.md, LOG các task, results); không viết số từ trí nhớ; số nào đưa vào phải dẫn file. Ngắn, dễ đọc.', 'workspace-write')
chay('CX-35b', 'Bạn là phiên Codex kiểm kỹ thuật độc lập việc {ma} vừa làm. Chỉ đọc; không sửa file, không SSH, không commit, không subagent. Brief: results/T-070/codex/{ma}-brief.md; kết quả: results/T-070/codex/{ma}-tin-cuoi.md. Kiểm: chỉ đúng file được phép bị ghi (so mtime/sha256); nội dung đúng căn cứ, không vượt phạm vi; với code: chạy lại phép thử, kiểm từng ca. Cuối: ĐẠT / CHƯA ĐẠT từng điểm, lỗi còn lại, sửa tối thiểu. Tiếng Việt, ngắn.'.format(ma='CX-35'))
chay('CX-36', 'Bạn là Codex sửa lỗi nhỏ bộ chấm W4 v2 (Minh cho phép "lỗi nhỏ Codex sửa, phiên Codex khác kiểm"). Phạm vi: chỉ GHI đúng file được nêu; không sửa file khác, không ghi LOG/STATE/SPEC/WHY/DECISIONS/LESSONS, không SSH, không commit, không dùng subagent. Liệt kê file đã tạo/sửa kèm sha256. Tiếng Việt, câu ngắn.\nGHI DUY NHẤT file mới trong D:/RCA-flashticket/results/T-072/v2/: cham_offline_v2c.py (chép từ cham_offline_v2_claude.py rồi sửa), thu_ca_gia_v2c.py, ra/thu-ca-gia-v2c.txt. KHÔNG sửa file đã có trong v2/ hay results/T-072/. Căn cứ: results/T-070/codex/CX-33-tin-cuoi.md và CX-33b-tin-cuoi.md: (A) khi khoảng chấm bắt đầu giữa phút, sự cố được đếm vào tử số nhưng phút chứa nó không vào mẫu số — sửa để tử số và mẫu số dùng cùng tập phút đủ điều kiện, vẫn liệt kê sự cố ở phút bị loại; (lỗi riêng CX-33b) xử lý khi lưới ngoại tuyến bị đứt theo đúng mô tả CX-33b. KHÔNG đổi quy tắc đã khóa (quy-tac-*.json), không đụng phần diễn giải "bảo đảm p95" (của Claude T-072), không chấm lại E4. Ca giả bắt buộc: tái hiện ca CX-33 điểm A (đầu khoảng giây 70, Alerting giây 80) trước/sau sửa; ca lưới đứt; giữ đạt các ca giả cũ (chạy lại thu_ca_gia.py, so len(khoang_chay) với số kỳ vọng). Ghi hash code thực chạy vào đầu ra.', 'workspace-write')
chay('CX-36b', 'Bạn là phiên Codex kiểm kỹ thuật độc lập việc {ma} vừa làm. Chỉ đọc; không sửa file, không SSH, không commit, không subagent. Brief: results/T-070/codex/{ma}-brief.md; kết quả: results/T-070/codex/{ma}-tin-cuoi.md. Kiểm: chỉ đúng file được phép bị ghi (so mtime/sha256); nội dung đúng căn cứ, không vượt phạm vi; với code: chạy lại phép thử, kiểm từng ca. Cuối: ĐẠT / CHƯA ĐẠT từng điểm, lỗi còn lại, sửa tối thiểu. Tiếng Việt, ngắn.'.format(ma='CX-36'))
chay('CX-38', 'Bạn là Codex soạn NHÁP SPEC W9a (diễn tập demo) để điều phối và Minh xem; chỉ đọc, KHÔNG ghi file (trả lời trong chat; điều phối lưu). Không subagent. Nguồn: docs/techstack/KE-HOACH-GIAI-DOAN-2.md §8.2 (W9a: kịch bản demo, video, phát lại offline, diễn tập 2 lần; xong khi diễn tập không lỗi); tasks/_MAU/SPEC.md (mẫu); docs/DECISIONS.md (khối 23/11: W8/LLM hoãn — demo KHÔNG có LLM; Q9: E7 được đi trước E6 nếu đủ điều kiện; phương án C: W7 chạy đêm, diễn tập xếp ban ngày giữa các khối); results/T-073/trien-khai-e5.md và e5-ket-qua.md (cách bật dịch vụ chế độ (b), commit E5/P/H, giới hạn live-down, chú thích hash T-064 sai); results/T-072/troi-p95-e2-e4.md (chạy tải ≥ 5 phút trước phần phát hiện, giữ cảnh báo đầu lượt); tasks/T-070-dieu-phoi-giai-doan-2/LICH-MAY.md, HOP-DONG.md (I7, I9, I15); results/T-074/e6-spec-nhap-2.md (hạn bán hiện 2026-12-02; E6 gia hạn). Nháp theo đủ mục mẫu SPEC: mục tiêu, câu hỏi/phép kiểm, đầu vào, đầu ra, phạm vi ghi, các bước (bật lại dịch vụ với vùng ghi mới — commit E5 ghim nguồn t073-e5-001 nên cần nguồn/commit mới hay dùng lại; kịch bản: tải → tiêm ô demo → cảnh báo → ca hiện dashboard → mở phát lại; hoàn tác), kiểm đúng đắn, tiêu chí xong (2 lần không lỗi, định nghĩa "lỗi"), mục lỗi 10/50/99% (luật 21), chi phí giờ máy, rủi ro, việc cần Minh quyết (mỗi việc có đề xuất, lý do, mặt trái). Ghi rõ phần chưa kiểm. Tiếng Việt, ngắn.')
log(su_kien='het_chuoi_17')
