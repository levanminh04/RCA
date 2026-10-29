"""Append the approved maker handoff, copy exact prompt template, then seal manifest."""
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from simple_runner import ROOT, OUT, read, sha, write


def block(source,heading):
    text=source.split(heading,1)[1]
    return text.split('```text',1)[1].split('```',1)[0].strip('\r\n')


def main():
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    common=block(template,'## Prompt chung')
    fields={
        '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':'T-042; D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md',
        '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>':'soát kết quả',
        '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>':'P3–P4, trọng tâm G2',
        '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':'Codex làm; Claude phản biện',
        '<danh sách đường dẫn và git diff từ commit gốc nếu có>':'D:/RCA-flashticket/tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md và LOG.md; D:/RCA-flashticket/docs/DECISIONS.md, WHY.md; D:/RCA-flashticket/results/T-042/bao-cao.md, doi-chieu.md, phan-xu.json, nguon.json, ke-hoach-chay.json, manifest.json; D:/RCA-flashticket/results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json, manifest.json; bản chưa commit, không có commit gốc riêng',
        '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':'không có phản biện chính thức trước',
        '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':'D:/RCA-flashticket/results/T-042/scripts/ và runs/; D:/RCA-flashticket/results/T-042/runs/continuation-001/plan.json, supplementary-plan.json, cost-and-runs.json, micro-mechanism-chains.json, final-verify-002/checks.json và các diagnosis-list/diagnoses-frozen; src/p3/, src/simplerca/, src/microrank/; nguồn/revision/pin tại nguon.json, source-pins/source-checks/config/invocation từng lượt và manifest; môi trường D:/RCA-ext/envs/T-014-main/Scripts/python.exe, dùng -B, lệnh thực tế và hướng dẫn tại LOG',
        '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':'chỉ trả lời trong chat; chưa có quyền ghi bản phản biện hoặc sửa file trong lượt này'
    }
    for old,new in fields.items():assert old in common;common=common.replace(old,new)
    assert '<mã' not in common
    stage=block(template,'### Soát kết quả');gate=block(template,'### G2 — Baseline và phân tích hạn chế')
    prompt=common+'\n\n'+stage+'\n\n'+gate+'\n'
    dest=OUT/'prompt-claude.txt'
    with dest.open('x',encoding='utf-8') as stream:stream.write(prompt)
    log=ROOT/'tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md'
    text='''

### Kết thúc phần nối tiếp Q-190 — 24/10/2026 — Codex người làm

1. **Đã làm:** tiếp tục theo lời Minh, không dừng ở2×2. Đọc code converter/caller/evaluator đã ghim; kiểm kernel AST không sửa trên22dev; so đơn vị trace, thời gian log/metric, severity, graph/count/formula/prior và cây kind. Dùng lại các trung gian đủ hash và pilot/case hợp lệ. Main.py literal đúng15/22, projection TimeStamp16/22; physicalns5/22; không nhận nhánh tốt hơn là baseline đã chọn. NezhaRCA partial và severity contracts tách rõ. Micro nguyên kernel RCAEval có spectrum không hợp lệ22/22; đổi riêng graph/formula/prior không cứu sham Top1. Có chuỗi trung gian và ca đúng/sai cùng ô, không gán mọi sai cho một cơ chế. Đã lập báo cáo nguồn/mức kết luận tại bao-cao-bo-sung.md và phan-xu-bo-sung.json trong continuation-001.

2. **File thay đổi:** chỉ thêm results/T-042/runs/continuation-001/ (scripts/config/fixture/diagnosis/intermediate/evaluation/report/hash/cost/prompt); nối WHY-54, DECISIONS Q-190 và LOG này; chỉ đổi dòng T-042 trong STATE. SPEC và164file T-042 trước bổ sung giữ nguyên; toàn bộ src, data, kết quả/task khác và tham chiếu hạ tầng không sửa. Q-190 chỉ duyệt thực hiện phần nối tiếp, không quyết chọn phương pháp hoặc nghiệm thu. Không commit/push, tải/cài, mở test/giữ ngoài, ghi ngoài hệ thống hoặc gửi Claude. Hai trợ lý nội bộ hỗ trợ người làm, không thay phản biện chính thức; root tiếp quản khi trợ lý hết usage.

3. **Kiểm:** fixture Simple10, graph/spectrum8, Eq7 toy, contract11 và histogram8 đạt; source/revision/AST hash kiểm trước dùng; raw payload không lưu. Có132Simple,198level,110TimeStamp,242Micro và132prior records (gồm replay/control; không là số quan sát độc lập). Micro evaluator đối chiếu242 vàprior132 với P3; kiểm cuối308native API ordinal ranks đối chiếu P3 đạt, tách khỏi kỳ vọng score ties. Đọc lại đầy đủ JSON/gzip/source scripts, frozen-list hashes và163output cũ đạt; kiểm code chung theo29pin gốc đạt; template prompt common/stage/G2 giữ nguyên ngoài metadata. git diff --check đạt. File set và hash trong manifest bổ sung; không sửa manifest cũ để che control hashes đã đổi theo quyền mới.

   **Lượt hỏng/dừng giữ đầy đủ:** source-contract-001 assertion scanner quá rộng, đã đọc lại đường Nezha và kiểm002; Micro pilot-001 đòi list order không cần cho ranker thay bằng Counter multiplicity; full-001 kiểm bit quá chặt, giữ audit và dùng16ULP AND16eps không floor, giữ service order/tie/max-op exact; full-002 dừng worker vì lưu lượng đĩa rồi tiếp bằng gzip cho output mới; full-003 hai operation không phải max trong cùng shippingservice đổi thứ tự2ULP, ghi đủ vị trí/score tại full-004, service ranking không đổi. Final-verify-001 dùng tie_group sai khi chấm native API; giữ source/failure rồi002 dùng ordinal key rõ ràng, không đổi diagnosis. Một lệnh đọc JSON thiếu encoding và một lệnh tìm wildcard trên PowerShell hỏng; đọc lại đúng UTF-8/thư mục, không ảnh hưởng số. Cost/clock/RSS có giới hạn nêu ở cost-and-runs.json: contracts RSS null; full-002 bị dừng nên không có CPU/peak/cost cuối. Không gọi null là0. Kết quả nặng giữ nguyên; tổng byte thực trong manifest, không xóa/nén thay file cũ.

4. **Câu hỏi nguồn và điều còn mở:** đã xác nhận những khác biệt có tác động, không phải thiếu mọi bằng chứng. Không thể định danh tiếp pipeline lịch sử sinh0.91/Table3 chỉ từ nguồn local và22dev: thiếu exact revision/entrypoint/config/cohort, normal inputs/conversion bridge, per-case predictions và script tổng hợp. Normal ngoài allowlist không được mở. Có thể nghĩ thêm tổ hợp/đổi thuật toán, nhưng không cung cấp provenance để chọn giữa các chương trình tác giả khả dĩ; không coi nó là bắt buộc chạy thêm chỉ để khớp số. Severity thật thiếu ở112587lượt dòng vẫn unknown; không bịa INFO hoặc suy keyword thành level. Kết quả dev chưa xác nhận lợi ích phương pháp đồ thị hoặc tổng quát hóa; P6/P7/G3 và lựa chọn baseline phụ thuộc nguồn/thiết kế/đánh giá được giao tiếp. Dừng thực nghiệm phần nối tiếp ở giới hạn nhận diện này; chưa nghiệm thu/đóng task hay câu hỏi nghiên cứu. Claude chưa phản biện; Minh quyết tiếp nhận giới hạn, yêu cầu nguồn hoặc giao bước sau.

**Bước tiếp theo chính xác:** Minh đọc results/T-042/runs/continuation-001/bao-cao-bo-sung.md, phan-xu-bo-sung.json và manifest.json cùng báo cáo/manifest gốc. Nếu chuyển phiên, giữ SOURCE/Python theo config/pins; xác minh manifest và đọc diagnoses đã có trước, không chạy lại lượt hợp lệ. Claude nhận prompt trung tính bên dưới để tự đọc nguồn gốc và kiểm kết quả; chưa được ghi REVIEW nếu Minh chưa cấp quyền. Người làm chờ Minh/Claude, không tự nghiệm thu hoặc gửi tin. Không có lệnh method còn cần tự chạy.

**Lệnh method/kiểm chính đã thực hiện:** dùng D:/RCA-ext/envs/T-014-main/Scripts/python.exe -B tại D:/RCA-flashticket:
- results/T-042/runs/continuation-001/simple_runner.py fixtures simple-fixtures-001; pilot simple-pilot-001; full simple-full-001.
- source_audit.py; evaluate_simple.py; level_runner.py0/1/2 với PYTHONHASHSEED tương ứng; time_projection.py; evaluate_extra.py.
- micro/driver.py vàdriver_v2.py fixture/cached/pilot/full; driver_v3.py full full-002; driver_v4.py full full-003; driver_v5.py full full-004 vàevaluate evaluate-001, PYTHONHASHSEED=0. Invocation/source snapshots từng run ghi đúngversion.
- micro/prior.py fixtures prior-fixtures-001; prior_v2.py pilot prior-pilot-002; full prior-full-002; evaluate prior-evaluate-002, PYTHONHASHSEED=0. Tất cả từ graph đã lưu, không rawrerun.
- finish_report.py; verify_final.py (lượt002 đạt); finalize_handoff.py. Lệnh cuối cần hoàn tất là kiểm seal bằng final_seal_check.py sau khi manifest/handoff được tạo; script chỉ đọc. Các lệnh lỗi, stdout/stderr/failure và checkpoints giữ ở đúngrun.

**Đề xuất nội dung commit khi Minh yêu cầu:** research: discriminate Nezha-OB baseline source and input contracts (T-042). Chưa commit/push.

### Prompt Claude — soát kết quả T-042 sau phần nối tiếp

Minh chọn chuyển; chưa tự gửi. Prompt được chép nguyên văn ba khối hiện hành, chỉ điền metadata.

```text
'''
    with log.open('a',encoding='utf-8') as stream:stream.write(text+prompt+'```\n')
    state=ROOT/'docs/STATE.md';before=state.read_text(encoding='utf-8-sig');lines=before.splitlines()
    matching=[i for i,line in enumerate(lines) if line.startswith('- **T-042 —')];assert len(matching)==1
    index=matching[0];lines[index]='- **T-042 — Đối chiếu baseline Nezha-OB:** **chờ phản biện** (24/10/2026); Codex làm, Claude phản biện. [Báo cáo bổ sung](../results/T-042/runs/continuation-001/bao-cao-bo-sung.md), [báo cáo gốc](../results/T-042/bao-cao.md), [SPEC](../tasks/T-042-doi-chieu-baseline-nezha-ob/SPEC.md), [LOG/prompt](../tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md). Đã thực hiện phần nối tiếp được Minh duyệt; chưa nghiệm thu, chưa chọn baseline. Giữ kết quả cũ và khóa test; tham chiếu T-042 hạ tầng chờ lượt riêng.'
    after='\n'.join(lines)+'\n';assert sum(x!=y for x,y in zip(before.splitlines(),after.splitlines()))==1
    state.write_text(after,encoding='utf-8',newline='')
    write(OUT/'state-row-change.json',dict(before_T042=before.splitlines()[index],after_T042=lines[index],other_lines_equal=True))
    with (OUT/'bao-cao-bo-sung.md').open('a',encoding='utf-8') as stream:stream.write('\nKiểm cuối bổ sung: final-verify-002/checks.json đạt; lượt001 là lỗi dựng bản ghi của checker, giữ source/failure. Có308kiểm ordinal API độc lập; đây không thay kiểm exact-score ties. Đã soạn prompt Claude và chuyển đúng dòng STATE sang chờ phản biện.\n')
    original=read(ROOT/'results/T-042/manifest.json')
    for row in original['files']:assert sha(ROOT/row['path'])==row['sha256']
    assert sha(ROOT/'results/T-042/manifest.json')==read(OUT/'initial-controls.json')['results/T-042/manifest.json']['sha256']
    assert sha(ROOT/'docs/review-prompt.md')==original['controls']['docs/review-prompt.md']
    for part in [stage,gate]:assert part in prompt
    result=subprocess.run(['git','diff','--check','--','docs/STATE.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md','results/T-042'],cwd=ROOT,capture_output=True,text=True);assert result.returncode==0,(result.stdout,result.stderr)
    files=[dict(path=p.relative_to(ROOT).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(OUT.rglob('*')) if p.is_file() and p.name!='manifest.json']
    controls={name:dict(bytes=(ROOT/name).stat().st_size,sha256=sha(ROOT/name)) for name in read(OUT/'initial-controls.json')}
    controls['docs/review-prompt.md']=dict(bytes=(ROOT/'docs/review-prompt.md').stat().st_size,sha256=sha(ROOT/'docs/review-prompt.md'))
    manifest=dict(schema='T042-Q190-supplement-v1',created_utc=datetime.now(timezone.utc).isoformat(),status='awaiting_review_not_accepted',files=files,
        n_files_excluding_self=len(files),bytes_excluding_self=sum(r['bytes'] for r in files),controls=controls,
        parent_manifest=dict(path='results/T-042/manifest.json',sha256=sha(ROOT/'results/T-042/manifest.json'),science_files_verified=163),
        control_note='Parent controls describe prior timestamp; LOG/WHY/DECISIONS/STATE now updated by Q190. Parent science and SPEC unchanged; do not rewrite parent to hide intended controls changes.',
        write_scope=['results/T-042/runs/continuation-001/','docs/WHY.md append WHY-54','docs/DECISIONS.md append Q-190','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md append','docs/STATE.md T-042 only'],
        tests_opened=False,downloads=0,shared_src_edits=0,commits=0,pushes=0,official_review_performed=False,
        scientific_stop='Missing identifying author program/input/predictions/aggregation; do not interpret this as all imaginable experiments exhausted')
    write(OUT/'manifest.json',manifest)
    for row in manifest['files']:assert sha(ROOT/row['path'])==row['sha256']
    total=sum(p.stat().st_size for p in (ROOT/'results/T-042').rglob('*') if p.is_file());assert total<300*2**20
    print(json.dumps(dict(status='SEALED',files=len(files),total_T042_bytes=total,total_T042_MiB=total/2**20,prompt_template_exact=True,STATE='chờ phản biện'),ensure_ascii=True))


if __name__=='__main__':main()
