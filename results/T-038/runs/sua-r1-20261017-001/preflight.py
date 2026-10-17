from pathlib import Path
import hashlib, json, shutil, subprocess, socket, datetime
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'results/T-038'; HERE=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
 before=HERE/'before';before.mkdir(exist_ok=False)
 m=load(BASE/'manifest.json'); bad=[]
 for r in m['files']:
  p=ROOT/r['path']
  if not p.exists() or sha(p)!=r['sha256']:bad.append(r['path'])
 save(HERE/'initial-manifest-check.json',dict(files=len(m['files']),mismatches=bad))
 assert not bad,bad
 originals=[]
 for p in BASE.rglob('*'):
  if p.is_file() and not p.is_relative_to(HERE):
   originals.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p),bytes=p.stat().st_size))
 save(HERE/'before-files.json',originals)
 for p in list(BASE.glob('*'))+list((BASE/'do-thi').glob('*'))+[BASE/'doi-chieu/index.json']:
  if p.is_file():
   dest=before/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 protected=[]
 for folder in ['docs','src/do_thi','src/do_thi_tinh','tasks/T-038-p5b-trainticket','tasks/T-040-p5b-tong-hop']:
  for p in (ROOT/folder).rglob('*'):
   if p.is_file():protected.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)))
 for p in [ROOT/'AGENTS.md', ROOT/'results/T-035/manifest.json',ROOT/'results/T-036/manifest.json',ROOT/'results/T-036/runs/doi-chieu-smtp-001/manifest.json']:
  protected.append(dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p)))
 for rel in ['tasks/T-038-p5b-trainticket/LOG.md','tasks/T-038-p5b-trainticket/REVIEW.md','docs/STATE.md']:
  p=ROOT/rel;dest=before/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 save(HERE/'protected-before.json',protected)
 (HERE/'git-status-before.txt').write_bytes(subprocess.check_output(['git','status','--short'],cwd=ROOT))
 (HERE/'git-diff-before.patch').write_bytes(subprocess.check_output(['git','diff','--no-ext-diff'],cwd=ROOT))
 notes=[
  dict(id='N1',status='FACT',blocking=True,observation='Root graph has 166 entity edges, 343 operation edges and 509 records; root projection has 121 edges and entity-only 44, summing to 165. SMTP was not propagated to these derived files.',evidence=['before/results/T-038/do-thi/thuc-the.json','before/results/T-038/do-thi/thao-tac.json','before/results/T-038/do-thi/chieu-thao-tac.json','before/results/T-038/do-thi/chi-thuc-the.json']),
  dict(id='N2',status='FACT',blocking=True,observation='Root engine.pinned_api uses historical R1 code plus live-code hash assertion; assemble uses historical part-document and does not add SMTP. It cannot reproduce current output with current common pin.',evidence=['before/results/T-038/engine.py']),
  dict(id='N3',status='OPEN',blocking=False,observation='Original part-document inventories support components, but adds only five non-Java relations. Supporting configuration relation completeness needs direct source inspection; no assertion of semantic completeness.',evidence=['results/T-038/runs/trien-khai-001/coverage/build_part_document.py'])]
 save(HERE/'independent-before-review.json',dict(review_or_candidate_conclusions_read=False,observations=notes))
 log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md'
 with log.open('a',encoding='utf-8') as f:
  f.write('\n\n## Phiên 3 — 17/10/2026 — Codex — '+socket.gethostname()+' — vai trò: người làm kiểm/đáp và sửa\n\n')
  f.write('Phân loại EXECUTE. Minh giao gói xử lý dứt điểm R1, đồng bộ phiên bản, kiểm đủ graph dev và bàn giao T-040. Quyền: results/T-038/ trừ nguồn/lịch sử; nối LOG; chỉ bảng phản hồi REVIEW; chỉ dòng T-038 STATE. Không đổi vai trò lịch sử, SPEC, quyết định, shared code hay kết quả task khác; không raw/test/heldout/archive, tải/EC2/RCA mới/subagent/chat/commit/push. Lời giao lưu tại authorization.txt của run sửa. Không xin lại quyền trong gói.\n\n')
  f.write('Tự soát trước khi đọc kết luận REVIEW/candidate: N1 CHẶN — graph166/343 đã thêm SMTP nhưng phép chiếu121 + entity-only44 chỉ phủ165; N2 CHẶN — runner gốc vẫn ghim R1, không tái lập bản SMTP; N3 OPEN — inventory support có nút nhưng năm relation non-Java không bảo vệ được độ đủ quan hệ cấu hình, cần đọc nguồn. Bằng chứng độc lập: runs/sua-r1-20261017-001/independent-before-review.json; before/ giữ byte trước. Đã kiểm manifest hiện hành không lệch; không đổi expected hash. Cần kiểm candidate từ nguồn và kiểm nhận vào bản chính thức.\n')
 print(json.dumps(dict(ok=True,originals=len(originals),manifest_files=len(m['files'])),ensure_ascii=False),flush=True)
if __name__=='__main__':main()
