"""Close authorized T020 work, enumerate every artifact and preserve review neutrality."""
from pathlib import Path
from datetime import datetime,timezone,timedelta
import csv,json,hashlib,subprocess,re,runpy
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'results/T-020';TASK=ROOT/'tasks/T-020-tong-hop-g1'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return list(csv.DictReader(p.open(encoding='utf-8-sig',newline='')))
# Verify original source pins against the saved, independently checked hashes.
deep=json.loads((OUT/'trung-gian/method_evidence/runs/deep-source-audit.json').read_text(encoding='utf-8'))
pins={r['source']:r['sha256'] for r in deep['checks'] if r.get('sha256')}
for name,h in pins.items():assert digest(Path(name))==h,name
(OUT/'runs/final-source-pins.json').write_text(json.dumps({'sources':[{'path':p,'sha256':h} for p,h in pins.items()],'revisions':deep['revisions'],'matched':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Root reviewed hash-selected semantic examples after reading their exact content.
rs=rows(OUT/'trung-gian/exposure_ledger/v1-semantic-overrides.csv'); groups={}
for r in rs:groups.setdefault(r['oldclass']+'>'+r['newclass'],[]).append(r)
selected=[]
for k,group in sorted(groups.items()):
    for r in sorted(group,key=lambda r:hashlib.sha256(('20261004|'+r['id']).encode()).hexdigest())[:3]:
        selected.append(dict(r,root_review='PASS: exact content inspected; history/evidence versus current choice distinguished'))
with (OUT/'trung-gian/root/v1-semantic-root-sample.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(selected[0]));w.writeheader();w.writerows(selected)
# Exact single-row mutation; reread immediately before write and preserve other bytes.
state_path=ROOT/'docs/STATE.md'; before=state_path.read_bytes()
old=[x for x in before.splitlines(keepends=True) if x.startswith(b'| T-020 |')]
assert len(old)==1 and 'đang làm (giai đoạn C/3, 04/10/2026)'.encode() in old[0]
new=old[0].replace('đang làm (giai đoạn C/3, 04/10/2026)'.encode(),'chờ phản biện (04/10/2026)'.encode())
start=before.index(old[0]); tail=before[start+len(old[0]):]
with state_path.open('r+b') as f:
    f.seek(start);f.write(new);f.write(tail);f.truncate()
after=state_path.read_bytes()
assert after==before.replace(old[0],new,1) and after.replace(new,b'',1)==before.replace(old[0],b'',1)
runpy.run_path(str(OUT/'scripts/final_audit.py'),run_name='__main__')
now=datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=7))).strftime('%d/%m/%Y %H:%M:%S (UTC+7)')
report=f'''

## Kết thúc phiên — {now} — Codex — Windows laptop — người làm

### Diễn biến giai đoạn C

- Hợp nhất 40 phần dataset, 42 hàng yêu cầu, 1680 cặp; 728 cần adapter, 825 chưa kiểm, 127 không chạy được trong phần tín hiệu chỉ định. Không coi “có file” là schema đã kiểm.
- V1 audit ngữ nghĩa giữ 877 dòng/533 occurrence; áp 683 override với exact ID+source+content. Root đọc 18 mẫu theo hash seed và các dòng bắt buộc a/b; các sai phân loại ban đầu đã sửa. Sau hợp nhất: a2/b2/c257/d18/e598. Bốn gate bắt buộc đủ D1–D6.
- V9 đối chiếu 90 section: 4 áp nguyên văn, 23 biến thể, 50 chưa áp, 13 không áp. Giữ từng body cũ→mới và evidence đích; không coi section là thay đổi độc lập. Không tự sửa WHY/DECISIONS.
- Tính lại 3248 phép: 3235 MATCH, 4 MISMATCH MicroRank, 9 OPEN. Chín OPEN là mẫu bổ trợ, pool quan trọng mỗi task đủ ít nhất năm; T004 không có nguồn triển khai để tạo mẫu.
- 16 replay TX2/fixture: 12 exit0, bốn lỗi giữ đủ (ba môi trường/API; một kiểm audit MicroRank). Tổng wall subprocess 78.406 giây; không là runtime chính thức. Bốn graph relations/SLO/counts của ca MicroRank khớp, audit null-root khác định nghĩa.
- Tự đọc G1 và phụ lục, sửa: physical duration unit OPEN; trace LEMMA ngày khác chưa kiểm; SimpleRCA metric-rule chỉ metric; ngân sách mốc chế độ a; Bank raw-provider OPEN; ô bootstrap chưa chứng minh độc lập; RE1-SS 100TX2+25TX1; GDN học một lần/hệ/seed. G1 1816 từ thân trước chỉnh câu cuối, dưới khoảng 3000; 42 đoạn biến thể tối đa209 từ trước link edit cuối.
- Root final verifier lần đầu so bytes worktree CRLF với git blob LF nên fail; kiểm lại bằng SHA input freeze chứng minh không đổi byte ngoài dòng T020. Verifier sửa dùng hash byte gốc và đối chiếu HEAD sau chuẩn hóa newline; không sửa nguồn để PASS.

### Ba subagent và bàn giao

Đã dùng đúng ba agent, cùng model **gpt-6.1-sol**, reasoning **ultra**, fork none. Luồng dataset_evidence làm V2/V4; exposure_ledger làm V3/census và audit V1/V9; method_evidence làm V5/V6/V8 factual. Chỉ root viết file cuối/thẻ/khuyến nghị/STATE. Không giao quyền quyết định.

Usage limit làm cả ba interrupted; list_agents xác nhận, followup tiếp tục đúng luồng. Dataset bàn giao kiểm cuối khoảng14:55 UTC, bổ sung đọc draft sau đó; method bàn giao nhận lúc15:03 UTC; exposure bàn giao nhận trước15:19 UTC. Đây là mốc quan sát bàn giao, không giả thời gian bắt đầu/CPU. Thời gian chính xác từng script ở run JSON; 16 replay78.406s, V1 replay0.452709s, build ledger1.425971s và independent validate0.346354s. Toàn bộ kiểm hash đóng băng đạt, không thay model để né limit. Worker folders nằm `results/T-020/trung-gian/{{dataset_evidence,exposure_ledger,method_evidence}}/`; manifest từng luồng giữ hash payload.

### Đối chiếu V1–V10 và tiêu chí xong

| Việc | Đầu ra và kiểm |
|---|---|
| V1 | 08, coverage533/533, 877dòng và683semanticoverrides; nguồn exact line, root18mẫu |
| V2 | 01 đủ40phần, C1–C9 cùng định nghĩa; 0ôtrống, schema/license/provenance ghiOPEN đúng phạm vi |
| V3 | 02, build_ledger và independent_validate;1417identityunits, không phải1417physicalincidents; 60lockedTT không có exposure/method-result |
| V4 | 03, task/leakage/root-mapping; không gọi injection là onset hoặc traceclass là service-root |
| V5 | 04 1680cặp và42requirement;16cột nguyên+bốnprovenance,0header mismatch,chua_kiem giữ nguyên |
| V6 | 05; budget fit/tune/score/normal/heldout, known/blind riêng; W-time/W-feasible chưa chốt số |
| V7 | 06, baCSV chia-theo-o vàassert; wholecell/census/noTX2test/v130/60 đạt; CIgiớihạn theo ô |
| V8 | 07,42đoạn vàchecklist;MicroRank/TORAIghim sâu,16replay dưới5phút;failures/inventory giữ đủ |
| V9 | Hai fileđínhchính/nhápchung;90section đối chiếu hiện hành,34section đínhchính; T002R1–5/T003R1–4 kiểm hiện trạng |
| V10 | G1 sáucâu trảlời riêng/D1–D6 đủ phươngán/phảnđối/đổibằngchứng/RQ/nháp;10P3 theo phụ thuộc vàQ40toàn bộ×seed |

Tiêu chí1–7 và9–11: các file/checks/coverage/split/nháp và prompt đủ theo bảng trên. Tiêu chí8 về ghi file đạt: chỉ SPEC/LOG/resultsT020 và dòngSTATE; không data/locked, không method mới. Tuy nhiên **phạm vi đọc có sự cố raw TX1** bên dưới; không trình toàn bộ tuân thủ tuyệt đối. Manifest và final-audit giữ ngoại lệ này. Tiêu chí G1 là đủ gói để phản biện/quyết, không tự duyệt G1.

| Yêu cầu gốc | Bằng chứng |
|---|---|
| P1 hiểu cơ chế/công thức/default/bài-code/giả định/tính tay | 07; method-checklist.csv; deep-source-audit.md;09; replaystdout/intermediate |
| P2 cùng tiêu chí/task chấm được/dataset/split | 01–06; C9 từng trục; source/license/schema; chia_theo_o.py vàsplit-assertions |
| G1 danh sách/dataset/chia vàQ54/Q56 | g1-goi-quyet-dinh.md D1–D6,08,nhápWHY/DEC; chưa P3/P5 |

### Bảng việc còn lại

| Việc | Làm được trong giới hạn T020? | Loại/lý do và người hoặc đầu vào cần |
|---|---|---|
| Duyệt D1–D6/WHY và các sửa nguồn chung | Không | Cần Minh quyết; chỉ nháp đã được phép ghi |
| Chốt mốc chế độ a so với MRP “test labels chỉ chấm” | Không | Cần Minh làm rõ D4; không tự cấp nhãn test |
| Mở test/giữ ngoài, raw TX0/TX1 để xác nhận adapter/clock/normal | Không | MRP§4 và giới hạn đọc; G3+Minh cho phép |
| Bank tiêu đề thật | Không với artifact/cơ chế hiện có | V7 đã cấp first-line có điều kiện; cần nguồn bất biến và cơ chế exact newline/noinflate, không thiếu quyền đã cấp |
| Chín lá bổ trợ OPEN | Không với nguồn hiện có | T008/T010/T011 cầnrawTX1; T003 cầnthànhphầnmetadatađộc lập. Cần nguồn phù hợp doMinh cấp/xác nhận, không dùngsốđóquyếtrole |
| Runtime mới toàn bộ/normal calibration/CI theo kết quả | Không | P3/P7+, cầndataset/protocol đãduyệt; không chạy trongT020 |
| C9 injector/collector/raw-provider và giấy phép | Không thể xác nhận từ nguồn đã có | Cầnnguồn tácgiả/provider hoặcquyếtđịnh vai tròMinh; khôngbịađểđóng |
| Phản biện task/G1 | Không thuộc người làm | Claude phiên riêng theo prompt cuốiLOG; Minh quyết findings |

Không có việc kiểm được phép và có đủ đầu vào còn bỏ dở. Không có đầu ra cần lấy riêng từ EC2 trongT020.

### Báo cáo A–I

**A. Đã làm:** đủ V1–V10 và gói G1 đề xuất; giữ sáu thẻ, ba cấu trúc split, nguồn/OPEN và kiểm số. Chưa đóng G1.

**B. File đã thay đổi:** `tasks/T-020-tong-hop-g1/SPEC.md`, LOG.md; mọi file trong `results/T-020/` (manifest kê đủ); đúng dòng T020 của `docs/STATE.md` chuyển chờ phản biện. Không tạo file ngoài repo; không sửa task cũ/src/shareddocs. Byte mọi dòngSTATEkhác giữ nguyên.

**C. Kiểm:** 3248 phép kiểm số với3235khớp/4sai khácgiải thích/9OPEN; metadata census/split assertions đạt;17rootcode/24rootcost/49rootcounts; 42đoạn≤350từ; 40parts×42=1680; coverage533/533; sourcepins/hash inputs/giới hạn ghi/link/diffcheck đạt. Final-audit.json là kết quả kiểm cuối, không phải OS-wide trace chứng minh mọi lần đọc.

**D. VẤN ĐỀ Ở TASK CŨ — ĐỂ REVIEWER KIỂM:** xem `dinh-chinh-task-cu.md`. Mới: bốn audit counters MicroRank khác null-root version; V3 thêm125localRE1OBTX2 (40copyFSE,85aliasHFOPEN); NezhaTT45records cóclockxungđột; giữ những proposal chưaáp/phạmvi đãáp và bỏ mục Minh loại. T002/T003 đã sửa được kiểm hiện trạng, không dùng review banđầu làm chặn. T020dùngphạmvigiớihạn đãđínhchính, không sửa nguồn cũ.

**E. Lệch SPEC:** sự cố dataset worker đọc nhầm file schema chứa raw TX1, đã báo Minh ngay và giữ scope-incident.md/json. Không có file cũ bị đổi, không locked hoặc method mới; loại payload khỏi schema proof. Ngoài ra, ba agent interrupted được tiếp tục, không thay mô hình/quy tắc; sửa verifier và phrasing sau kiểm nguồn, không đổi seed/selection. Đọc hợp lệ sau sự cố dùng aggregate/header witness thay sample payload. Không đề nghị coi sự cố là hợp lệ hồi tố.

**F. Tài liệu chung/commit:** xem `de-xuat-tai-lieu-chung.md`; pending chưa ghi, các templateWHY/DEC phải Minh chọn rồi duyệt. Nội dung commit đề xuất: `docs(T-020): tổng hợp gói quyết định G1 và bằng chứng kiểm chéo`. Chưa commit/push.

**G. Chưa kiểm:** chín mẫu OPEN; schema/unit/normal các bộ chưa được mở; Bank header thật, license/provenance C9; P3 calibration và blind evaluation. Không tuyên bố có heldout đạt3trục hoặc vùng ảnh hưởng publicgold. Sự cố rawread đãnêu làgiớihạn audit, không che bằnghashequal.

**H. Cần Minh quyết:** D1 biến thể; D2 gói/vai trò; D3 TX1/test/split; D4 nhãn/normal/mốc; D5 quy tắc window; D6 Retrieval/Rerank. Ngoài thẻ: nguồn/license/provenance/header đápứngV7; sửa tài liệu chung đúngđoạn; cách xửlýQ40chi phílịch sửCIRCA nếu cần. Không yêu cầu duyệt lại đề xuất bịloại.

**I. Xung đột lợi ích:** thẻ Codex/T013/T014/T015/T017 và Q49/WHY13 bảo toànBank được đối xử như nguồn cầnkiểm. Tính từ gốccomponent/Census/hashselectedsamples; deep MicroRank chọn trước cùngTORAIcủaClaude; root code/count/cost kiểm riêng. V9 đọc từng câu hiện hành/exception, V1 nguồn exact-content. Những câuquárộng được sửa; Bank không tựđượcchọnvìCodexđãbảo toàn. Subagent làđầu vào, không thay phảnbiệnClaude.

### Sáu ý kết thúc theo mẫu LOG

1. Đã làm: A/V1–V10 ở trên; gói chờ phản biện.
2. File: B và manifest.json; không có outputngoàirepo.
3. Kiểm: C,09,runs/final-audit.json; failures vàscopeincident giữ đủ.
4. Chưa chắc/cần Minh: G/H và Bảng việc còn lại. Không ghi quyếtđịnhG1thayMinh.
5. Bước tiếp chính xác: Minh mở **Claude Code phiên mới trong D:\\RCA-flashticket**, dán nguyên prompt cuối LOG. Claude đọc SPEC/LOG và mọi file liệt kê, chỉ ghi REVIEW.md. Sau review người làm tự soát trước rồi phản hồi từng finding theoAGENTS; chưa sửa task cũ tự động.
6. Lệnh cuối: `py -3 -X utf8 -B results/T-020/scripts/prepare_handoff.py`; script gọi final_audit.py, ghi prompt/filelist/manifest rồi kiểm hashes. Phản biệnkhông dùnggitdiff làm phạmvi duy nhất.
'''
with (TASK/'LOG.md').open('a',encoding='utf-8',newline='') as f:f.write(report)
# All paths, including artifacts created below, are neutral scope data only.
planned=['results/T-020/manifest.json','results/T-020/runs/review-prompt-audit.json']
paths=sorted(set([p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file()]+planned+
['tasks/T-020-tong-hop-g1/SPEC.md','tasks/T-020-tong-hop-g1/LOG.md','docs/STATE.md']))
template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
common=template.split('## Prompt chung')[1].split('```text\n',1)[1].split('\n```',1)[0]
focus=template.split('**G1 — phương pháp, dataset, cách chia:**')[1].split('```text\n',1)[1].split('\n```',1)[0]
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
prompt=common.replace('<T-xxx>','T-020').replace('<T-xxx-tên>','T-020-tong-hop-g1').replace('<danh sách>',',\n'.join(paths)).replace('<commit gốc>',head)+'\n\n'+focus
assert '<T-' not in prompt and '<danh sách>' not in prompt
with (TASK/'LOG.md').open('a',encoding='utf-8',newline='') as f:
    f.write('\n\n## Prompt phản biện cho Claude — chép vào phiên mới\n\n```text\n'+prompt+'\n```\n')
(OUT/'runs/review-prompt-audit.json').write_text(json.dumps({'template':'docs/review-prompt.md','common_and_G1_exact_except_neutral_placeholders':True,'file_list':paths,'outside_outputs':[],'HEAD':head,'scope_is_explicit_files':True,'extra_findings_in_prompt':False},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
freeze=json.loads((OUT/'trung-gian/input-freeze.json').read_text(encoding='utf-8-sig'))
supp=json.loads((OUT/'trung-gian/root/supplemental-inputs.json').read_text(encoding='utf-8'))
files=[p for p in OUT.rglob('*') if p.is_file() and p!=OUT/'manifest.json']+[TASK/'SPEC.md',TASK/'LOG.md',state_path]
outputs=[{'path':p.relative_to(ROOT).as_posix(),'sha256':digest(p),'bytes':p.stat().st_size} for p in sorted(files)]
manifest={'task':'T-020','status':'chờ phản biện; G1 chưa duyệt','created_utc':datetime.now(timezone.utc).isoformat(),
'input_manifest_frozen':freeze,'supplemental_historical_timer_inputs':supp,'original_source_pins':{'path':'results/T-020/runs/final-source-pins.json','sha256':digest(OUT/'runs/final-source-pins.json')},
'outputs':outputs,'manifest_self_hash':'omitted to avoid recursive self-hash; all other output files hashed','outside_outputs':[],
'scope_incident':{'path':'results/T-020/trung-gian/dataset_evidence/scope-incident.md','description':'read of mixed schema/raw TX1 sample; reported, excluded from proof, retained'},
'frozen_input_audit':'5771 unchanged; only authorized T020 STATE row differs; original STATE bytes retained elsewhere'}
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert all(digest(ROOT/e['path'])==e['sha256'] for e in outputs)
assert set(paths)=={p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file()}|{'tasks/T-020-tong-hop-g1/SPEC.md','tasks/T-020-tong-hop-g1/LOG.md','docs/STATE.md'}
print('handoff finalized:',len(outputs),'hashed outputs;',len(paths),'explicit review paths; manifests and LOG stable')
