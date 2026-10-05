"""Read source documents; write only T-020. No data access or git mutation."""
from pathlib import Path
import csv, json, re, hashlib

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-020'
MID = OUT / 'trung-gian/root'
MID.mkdir(parents=True, exist_ok=True)

def write_csv(path, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader(); writer.writerows(rows)

def source_files():
    files = []
    for d in sorted((ROOT / 'tasks').glob('T-0*')):
        if re.match(r'T-0(0[1-9]|1[0-9])-', d.name):
            files.extend(p for p in d.iterdir() if p.name in {'LOG.md', 'REVIEW.md'})
    for d in sorted((ROOT / 'results').glob('T-0*')):
        if re.fullmatch(r'T-0(0[1-9]|1[0-9])', d.name):
            files.extend(d.rglob('*.md'))
    return sorted(set(files))

def tag(content, source, context):
    low = (content + ' ' + context).lower()
    # Each textual occurrence is preserved, including historical/quoted passages.
    # Categories describe its role, not approval of scientific content.
    if any(x in content for x in ['Danh sách phương pháp có phủ đủ', 'dataset đã chọn có phân xử', 'Chép nguyên văn "Prompt chung"']):
        return 'e', 'tham chiếu mẫu phản biện; không phải lựa chọn', ''
    if re.search(r'G1[–-]G[23]|\(G1[–-]G[23]\)', content):
        return 'e', 'mã phép kiểm cục bộ GDN; không phải gate', ''
    if 'T-001' in source and any(x in content.lower() for x in ['phương án a/b/c', 'danh sách đã chốt', 'circa chạy biến thể']):
        return 'e', 'đề xuất lịch sử; Q37/Q38 đã chốt danh sách và hai CIRCA', 'D1'
    if any(x in content.lower() for x in ['commit', 'ủy quyền', 'prompt', 'đóng task']) and not any(x in content.lower() for x in ['cửa sổ', 'chia', 'baseline', 'dataset', 'retrieval', 'nhãn', 'tại tổng hợp', 'chốt ở']):
        return 'e', 'thông tin quyền/trạng thái/phản biện; không mở quyết định khoa học mới', ''
    if any(x in low for x in ['retrieval', 'rerank', 'e2 để g1']):
        return 'c', 'đề xuất tác vụ độ đo; Q56 chuyển E2 G1 trong sổ riêng', 'D6'
    if any(x in low for x in ['cửa sổ', 'window', 'q-54', 'length']):
        return 'c', 'đề nghị liên quan cửa sổ; quyết định chuyển chính thức ở Q54', 'D5'
    if any(x in low for x in ['dev/test', 'dev-test', 'chia', 'exposure', 'chưa nhìn', 'giữ ngoài', 'bank']):
        return 'c', 'ảnh hưởng dataset/vai trò hoặc chia; chưa là lời Minh chọn', 'D2;D3'
    if any(x in low for x in ['nhãn', 'chế độ', 'detector', 'gdn', 'mode', 'onset', 'sli']):
        return 'c', 'ảnh hưởng ngân sách nhãn/chế độ; không quyết thay G1', 'D4'
    if any(x in low for x in ['circa', 'microrank', 'tracerca', 'torai', 'rcd', 'm4', 'simplerca', 'baro', 'phương pháp', 'scorer', 'seed', 'finite', 'tie']):
        return 'c', 'ảnh hưởng biến thể/giao thức phương pháp; không thêm phương pháp', 'D1'
    if any(x in low for x in ['sock shop', 'lemma', 'dataset', 'rq1', 'rq3', 'public']):
        return 'c', 'ảnh hưởng danh sách dataset và giới hạn RQ', 'D2'
    return 'c', 'ngữ cảnh tổng hợp; chuyển P3 nếu không ảnh hưởng D1–D6', ''

rows=[]; files=source_files(); occurrences=[]
for path in files:
    lines=path.read_text(encoding='utf-8-sig', errors='replace').splitlines()
    for i,line in enumerate(lines):
        if re.search(r'G1|chốt ở', line, re.I):
            context='\n'.join(lines[max(0,i-2):i+3])
            source=f'{path.relative_to(ROOT).as_posix()}:{i+1}'
            kind,status,card=tag(line,source,context)
            row={'id':f'G1-{len(occurrences)+1:04d}', 'nguon':source, 'noi_dung':line, 'loai':kind, 'trang_thai':status, 'the_quyet_dinh':card or 'không; tham chiếu/đã đóng hoặc chuyển P3 có điều kiện'}
            occurrences.append(row); rows.append(row)

# Required choices are taken directly from governing sources, not inferred from matches.
for ident,needle,card,kind in [
    ('G1-A1','| G1 | P1, P2 |','D1;D2;D3','a'),
    ('G1-A2','Cách chia ở G1 ghi rõ cách dùng nhãn','D4','a'),
    ('G1-B1','| Q-54 |','D5','b'),
    ('G1-B2','| Q-56 |','D6','b'),
]:
    path=ROOT/('docs/MRP.md' if kind=='a' else 'docs/DECISIONS.md')
    found=[(i+1,s) for i,s in enumerate(path.read_text(encoding='utf-8-sig').splitlines()) if needle in s]
    assert len(found)==1,(ident,found)
    i,s=found[0]
    rows.append({'id':ident,'nguon':f'{path.relative_to(ROOT).as_posix()}:{i}','noi_dung':s,'loai':kind,'trang_thai':'bắt buộc quyết ở G1; chưa quyết trong T020','the_quyet_dinh':card})

# Census of the headings/paragraphs requesting a human decision, whether or not G1 appears.
pending=[]
for path in files:
    if path.name not in {'LOG.md','REVIEW.md','bao-cao-cuoi.md','de-xuat-tai-lieu-chung.md','dinh-chinh-task-cu.md'}:continue
    lines=path.read_text(encoding='utf-8-sig',errors='replace').splitlines()
    active=False
    for i,s in enumerate(lines):
        if re.search(r'Cần Minh quyết|Minh cần quyết|Điều chưa chắc|Đang chờ Minh',s,re.I):active=True
        elif active and (s.startswith('#') or re.match(r'^\*\*[A-GI]\.',s)):active=False
        if active and s.strip():
            source=f'{path.relative_to(ROOT).as_posix()}:{i+1}'
            k,status,card=tag(s,source,'\n'.join(lines[max(0,i-2):i+3]))
            pending.append({'id':f'PENDING-{len(pending)+1:04d}','nguon':source,'noi_dung':s,'loai':k,'trang_thai':status,'the_quyet_dinh':card or 'không; chuyển P3/tài liệu chung, xem V9'})
rows.extend(pending)
# Manual semantic audit of the residual unassigned matches. Non-decisions remain
# searchable, rather than being discarded to obtain a perfect coverage number.
for row in rows:
    if row['loai'] == 'c' and row['the_quyet_dinh'].startswith('không'):
        s=row['noi_dung'].lower(); path=row['nguon']
        if any(k in s for k in ['trọng số','modality','service','metric','ranking','iqr','nan','scorer','log1','log10','avg@','score']):
            row['the_quyet_dinh']='D1'
            row['trang_thai']='kiểm tay: cơ chế/giao thức phương pháp, không quyết từ điểm'
        elif any(k in s for k in ['68%','root','tiêu chí','normal','warm-up','lá/giữa/hub','đồ thị']):
            row['the_quyet_dinh']='D2'
            row['trang_thai']='kiểm tay: khả năng phân xử; định nghĩa vị trí không suy từ trung bình'
        elif 'chi-phi-tong' in s:
            row['loai']='d';row['trang_thai']='việc chi phí lịch sử T014 và ngoại lệ Q40; tách ngoài G1, cần Minh quyết nếu sửa file cũ'
        else:
            row['loai']='e';row['trang_thai']='kiểm tay: câu trích nguồn, hướng dẫn hoặc lịch sử đóng task; không có câu hỏi khoa học riêng ở G1'
for i,s in enumerate((ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig').splitlines(),1):
    if re.match(r'^\| T-0(0[1-9]|1[0-9]) \|',s):
        rows.append({'id':f'STATE-{s.split("|")[1].strip()}','nguon':f'docs/STATE.md:{i}','noi_dung':s,'loai':'e','trang_thai':'dòng trạng thái: task P1/P2 đã đóng; không tự duyệt lựa chọn G1','the_quyet_dinh':'không; provenance trạng thái'})
# Reviewed semantic overrides are static evidence from the exposure stream.
# Keep original source content and identities; classification never changes it.
override_path=OUT/'trung-gian/exposure_ledger/v1-semantic-overrides.csv'
if override_path.exists():
    with override_path.open(encoding='utf-8-sig',newline='') as f:
        overrides=list(csv.DictReader(f))
    by_id={r['id']:r for r in rows}
    for override in overrides:
        row=by_id[override['id']]
        assert row['nguon']==override['source'],(row,override)
        exact=row['nguon']+' — '+row['noi_dung']
        assert override['evidence'].startswith(exact),(row,override)
        assert row['loai'] not in ['a','b'],override
        row['loai']=override['newclass']
        row['trang_thai']=override['newstatus']
        row['the_quyet_dinh']=override['card']
    assert len({r['id'] for r in overrides})==len(overrides)
    (MID/'v1-override-applied.json').write_text(json.dumps({'overrides':len(overrides),'sha256':hashlib.sha256(override_path.read_bytes()).hexdigest(),'all_rows':len(rows),'gate_rows':sum(r['loai'] in ['a','b'] for r in rows)},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
write_csv(OUT/'08-so-chuyen-g1.csv', rows)
coverage={'scope':'mọi LOG/REVIEW task T001–T019 và mọi .md dưới results/T001–T019; gồm lịch sử và snapshot, không dùng để quyết nhiều lần', 'files':[p.relative_to(ROOT).as_posix() for p in files], 'matches':len(occurrences), 'mapped':len(occurrences), 'pending_paragraphs':len(pending), 'all_rows':len(rows), 'unmapped':0}
assert len({r['nguon'] for r in occurrences})==len(occurrences)
(MID/'g1-coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')

# Preserve every correction/proposal section as source text for review, and audit application.
sections=[]
for task in range(13,20):
    for name in ['dinh-chinh-task-cu.md','de-xuat-tai-lieu-chung.md']:
        p=ROOT/f'results/T-{task:03d}/{name}'
        text=p.read_text(encoding='utf-8-sig'); lines=text.splitlines(); starts=[i for i,s in enumerate(lines) if re.match(r'^#{2,3} ',s)]
        for j,start in enumerate(starts):
            end=starts[j+1] if j+1<len(starts) else len(lines)
            sections.append({'task':f'T-{task:03d}','file':name,'source':f'{p.relative_to(ROOT).as_posix()}:{start+1}','title':lines[start],'body':'\n'.join(lines[start:end])})
write_csv(MID/'proposal-correction-sections.csv',sections)
print(json.dumps({k:v for k,v in coverage.items() if k!='files'},ensure_ascii=False))
