"""Write the approved task status and copy the exact neutral Claude review prompt."""
import hashlib,json,re,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[3];B=R/'results/T-003'
def load(p):return (R/p).read_text(encoding='utf-8-sig')
def append(p,t):
    with (R/p).open('a',encoding='utf-8') as f:f.write(t)
def main():
    text=load('docs/review-prompt.md')
    common=re.search(r'## Prompt chung.*?```text\n(.*?)\n```',text,re.S).group(1)
    g1=re.search(r'\*\*G1 — phương pháp, dataset, cách chia:\*\*\s*```text\n(.*?)\n```',text,re.S).group(1)
    title='T-003-the-dataset-ngoai-rcaeval'
    outputs='results/T-003/, results/T-008/, results/T-009/, results/T-010/, results/T-011/, results/T-012/, SPEC.md và LOG.md của các nhánh T-008–T-012, data/README.md, docs/MRP.md, docs/WHY.md, docs/DECISIONS.md và docs/LESSONS.md'
    prompt=common.replace('<T-xxx-tên>',title).replace('<T-xxx>','T-003').replace('<danh sách>',outputs).replace('<commit gốc>','HEAD')+'\n\n'+g1+'\n'
    (B/'prompt-claude.md').write_text(prompt,encoding='utf-8')
    assert all(s in prompt for s in ('Bổ sung yêu cầu phản biện:','6. Mỗi finding','(kiểm ngẫu nhiên ít nhất 2 phương pháp)'))
    state=load('docs/STATE.md')
    statuses={'T-003':'Chờ phản biện gộp Claude (03/10); đã tự phản biện và kiểm toàn gói',
        'T-008':'Đã kiểm toàn CSV bốn ngày; chờ phản biện trong T-003 (03/10)',
        'T-009':'Đã kiểm hai ZIP và toàn nested; chờ phản biện trong T-003 (03/10)',
        'T-010':'Đã kiểm raw/normal/graph/all-log; chờ phản biện trong T-003 (03/10)',
        'T-011':'Đã kiểm bốn ZIP IT mẫu; Original metadata; chờ phản biện trong T-003 (03/10)',
        'T-012':'Đã hoàn tất khảo sát nguồn có giới hạn, 14 thẻ; chờ phản biện trong T-003 (03/10)'}
    lines=state.splitlines()
    for i,line in enumerate(lines):
        for task,status in statuses.items():
            if line.startswith('| '+task+' |'):
                cells=line.split('|');cells[6]=' '+status+' ';lines[i]='|'.join(cells)
        if line.startswith('**T-003** đã ghi checkpoint'):
            lines[i]='**T-003** hoàn thiện phạm vi Q-47/Q-50; Claude phản biện gộp tại parent, prompt cuối LOG. Bank là ứng viên bảo toàn metadata trước G3 theo WHY-13, chưa chốt tập thí nghiệm G1. T-004 chưa triển khai.'
        if line.startswith('- T-003:'):
            lines[i]='- T-003: chờ Claude REVIEW rồi Minh quyết; exact license/clock/lineage còn OPEN theo thẻ. EC2 mới và dữ liệu còn giữ, chưa Stop/xóa.'
    (R/'docs/STATE.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    append('tasks/T-008-the-dataset-nezha/LOG.md','''

### Kết thúc nhánh Nezha trong gói Q-47/Q-50 — 03/10/2026
Đã hoàn tất thẻ hai hệ, whole-CSV audit/label/root-window/parent/log/clock và khảo sát Duration đúng phạm vi. Bản kết luận dùng evidence-002, trace-symptoms-002, symptoms-003, card-final-002; không dùng normal metric trùng fault làm clean reference. Units-001 kiểm4.180.244span và independent-check-001 SQL12file đạt. Các q/span tương quan, clock haihypothesis và normalngắn còn giới hạn đúng trong thẻ; không RCA hoặc suy nhãn vùng.
File cập nhật gồm scripts/kết quả/thẻ trong results/T008 và LOG, inspection-plan đã ghi trạng tháiQ47 và giữ kếhoạchlịchsử. Root kiểm cuối toàngói trong results/T003/runs/final-002; không sửa REVIEW. ChờClaude reviewgộp parent, khôngđóngtask hoặcG1. Bước tiếp: đọc promptcuốiLOGparent và kếtquả hiệnhành, không chạy lại download/audit hợp lệ. Lệnh cuối nhánh: py -3 -B results/T-008/scripts/write_cards.py --run card-final-002; kiểm gói tiếp ởparent. Chưacommit/push.
''')
    report='''

## Kết thúc thực hiện T-003 và T-008–T-012 — 03/10/2026, Codex

1. Đã làm: tiếp checkpoint, chạy lại nhánh chưa hoàn tất bằng GPT-6.1 Sol high theo Q-50; tái dùng acquisition và kiểm hợp lệ. Hoàn tất phạm vi file Nezha/Eadro/Deep (gồm all-log conditional), toàn member bốn ZIP LEMMA IT mẫu, khảo sát nguồn 2025–2026 có giới hạn và tổng hợp. Bảo toàn Bank cùng AIOps Bank lineage trước số đo theo ủy quyền, WHY-13/Q-49; chưa chốt tập thí nghiệm G1. Tự phản biện đã tìm và sửa lỗi trước bàn giao; báo cáo ở results/T-003/tu-phan-bien-doc-lap.md. Claude phản biện gộp một REVIEW parent.
2. File thay đổi của gói: results/T-003 và T-008–T-012; SPEC sáu task có bổ sung Q-47 đã duyệt ở lượt trước, LOG sáu task; data/README.md; DECISIONS Q-47–50; WHY-13/14; STATE chỉ dòng và mục của gói. Dữ liệu laptop/EC2 ở đúng vùng duyệt, không vào git. Không sửa AGENTS/MRP/LESSONS/review-prompt hoặc task khác trong lượt hoàn thiện này; giữ các diff có trước. Không commit/push, xóa dữ liệu hoặc Stop EC2.
3. Kiểm: final-002 đạt 251 check và 155 snapshot nguồn đúng byte/SHA; hai lỗi lấy nguồn lịch sử giữ nguyên. Đủ thẻ 10 mục, link/script/label census, parent SQL, Duration, branch validation, KPI và q balances đạt. Final-001 giữ lỗi link trước khi tạo báo cáo tự phản biện. Các lỗi normal/bounds/count của Nezha, shape cạnh Deep và schema/entity LEMMA đã sửa, chứng cứ từng lượt trong báo cáo tự phản biện. Eadro ước lượng giải nén cũ bỏ GZip, không là cận trên toàn nested; báo cáo cuối dùng file thật và tách duplicate. Payload 5.477.786.503 byte, nguồn resources-final-001. Postflight SSH máy mới đạt; còn 35.260.207.104 byte đĩa. Streaming không lưu toàn 34.662.558.791 byte nội dung logical ra đĩa. git diff --check đạt whitespace, có cảnh báo LF/CRLF của file đã thay trước.
4. OPEN: exact license/clock/alias/normal/provenance từng thẻ; Deep thiếu nhãn root/onset/vùng và một phần span normal; LEMMA Original/ngày khác ngoài bốn ZIP mẫu, PR normal/KPI và Cloud clock/metadata; T-012 source-only và Bank quality/injector/collector/census thực. Owner, đầu vào cần và kết luận bị giới hạn nằm trong thẻ/bảng. Không gọi không làm vì scope/chi phí là không thể kiểm. Task chờ phản biện; Minh quyết sửa, đóng task và lựa chọn G1. EC2/data giữ để review/tái lập, chưa tự dọn.

Bước tiếp: Minh mở phiên Claude mới tại D:/RCA-flashticket, dán nguyên prompt dưới; bản copy ở results/T-003/prompt-claude.md. Claude đọc AGENTS/SPEC/LOG và đầu ra, chỉ ghi tasks/T-003-the-dataset-ngoai-rcaeval/REVIEW.md. Không tải lại hoặc mở Bank/locked. Người làm phản hồi sau REVIEW theo quy trình, Minh quyết.

Lệnh kiểm cuối trước handoff: py -3 -B results/T-003/scripts/verify_final.py --run final-002; SSH read-only df/du/free và git diff --check. Sau handoff chỉ pin lại manifest/kiểm file cuối vì vừa thêm LOG/status/prompt; không nghiên cứu thêm. Baseline HEAD và file set nằm trong scope-files.json. Đề xuất commit khi Minh yêu cầu/duyệt: docs: complete external dataset evidence and merged review handoff. Chưa commit/push.

Theo AGENTS §5a.2, checkpoint đã ghi ngay sau nén; đề nghị phiên Claude mới dùng prompt dưới. Không cần làm lại phần đã kiểm. PASS kỹ thuật không đóng các OPEN khoa học.

## Prompt Claude phản biện gộp T-003

```text
'''
    append('tasks/T-003-the-dataset-ngoai-rcaeval/LOG.md',report+prompt+'```\n')
    files=[R/'docs'/x for x in ['STATE.md','DECISIONS.md','WHY.md']]+[R/'data/README.md']
    for directory in sorted((R/'tasks').glob('T-*')):
        if directory.name.split('-')[1] in ['003','008','009','010','011','012']:
            files.extend(directory/x for x in ['SPEC.md','LOG.md'])
    scope=dict(stage='final handoff',baseline_head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip(),
        controlled_files=[dict(path=p.relative_to(R).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in files],
        result_directories=['results/T-003/','results/T-008/','results/T-009/','results/T-010/','results/T-011/','results/T-012/'],
        preserved_unrelated_changes=True,no_commit_or_push=True)
    (B/'scope-files.json').write_text(json.dumps(scope,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(dict(prompt_exact=True,controlled_files=len(files),status='waiting merged Claude review')))
if __name__=='__main__':main()
