"""Record the agreed response and metadata candidate without granting main."""
import json
from pathlib import Path
from activate import ROOT,RUN,pin
from bien_nhan import atomic,digest,read_pin


def put(path,text):path.write_text(text.strip()+'\n',encoding='utf-8',newline='')


def main():
    base=RUN/'pre-review-001'
    for host in ('ec2_1','ec2_2'):assert read_pin(pin(RUN/(host+'-after-review-environment.json')))['PASS']
    cost=read_pin(pin(RUN/'cost-scenario.json'));models=cost['pipeline_scenarios']
    hours=[row['total_seconds']/3600 for row in models]
    response='''# Codex đáp phản biện Claude về chuẩn bị013

## Kết luận và quyền

Đã tự soát nguồn và entry trước khi đọc kết luận Claude; mục mở lượt đáp nằm trong LOG. Nhận cả hai finding chính. Không còn phản đối về cách xử lý: sửa ứng viên theo F1(a), bổ sung F2. Chưa gọi metadata sau sửa là đã được Claude kiểm; Claude đề nghị kiểm phần này trước khi dừng. Không khóa G3, mở test, chỉ định evaluator theo quyền cuối, chạy main hoặc commit.

Minh cho phép ghi có điều kiện khi Codex kiểm độc lập đồng ý; đã lưu nguyên văn review tại `claude-review-013-001.txt`, quyền/rationale trong DECISIONS/WHY. Đã giữ nguyên gói Claude kiểm và các tài liệu ghim ở `pre-review-001/`, với ánh xạ `preservation.json`. Manifest mới nhận diện bản sửa; không dùng pin gói cũ để xin duyệt bản mới.

| Điểm | Phản hồi của Codex | Xử lý | Minh quyết |
|---|---|---|---|
| F1: số worker và cách dùng số đo chồng | Đúng về thiếu căn cứ thông lượng và nguy cơ bất đối xứng wall-clock. Nhận phương án(a). | Cả hai EC2 một worker trong ứng viên; laptop giữ tối đa hai theo RAM và nhóm. Không đổi600s/C-d360s. | Quyền khóa/chạy vẫn chờ lời duyệt cuối. |
| F2: thiếu local/chuyển/nhận/chấm | Đúng. Dự toán cũ chỉ có TT cloud nên không đủ mô tả toàn chuỗi. | Đã thêm kịch bản từng nhóm local và toàn chuỗi, nguồn cũ có pin; không chạy thêm method. | Xét cùng hồ sơ duyệt cuối, không coi kịch bản là ETA. |

## F1 — bằng chứng và giới hạn lập luận

Đọc lại event/cost r2: bảy job cộng475,39giây trong khoảng239,93giây với hai worker, khớp quan sát Claude (`review-evidence.json#/F1`). Ba vế nặng trên EC2_1 có wall121,78/126,58/113,96giây; các vế đo đơn khác trên EC2_2 khoảng65–69giây. Đây chưa là đối chiếu cùng vế/cùng máy ở một và hai worker. Giữ cả hai giải thích: tranhCPU hoặc khác chi phí vế. Không quy cơ chế riêng khi chưa phân xử.

Sửa một worker mỗi EC2 là lựa chọn ứng viên giảm bất đối xứng đồng thời trước G3. Không dựa vào khẳng định chắc chắn “tổng thời gian không đổi”, vì hai nửa test có thể khác chi phí, và local có thể là đường găng. Không dùng câu “số worker không đổi đầu ra” cho cả trạng thái TIMEOUT: ngưỡng wall-clock và tranh chấp có thể làm trạng thái khác. Những giới hạn này không làm Codex phản đối phương án(a); chúng là cách ghi chính xác căn cứ của lựa chọn.

Giữ600giây là giữ ngân sách wall-clock ứng viên của giao thức, không chứng minh mọi ca test xong trước600giây. DEV và fixture cho bằng chứng thực thi/pha/phân loại, không cho cận trên toàn cohort. Không tăng ngưỡng sau điểm test. Đã ghi căn cứ, phương án và điều kiện thất bại trong WHY; quyền khóa các số vẫn nằm ở lần duyệt cuối.

## F2 — toàn chuỗi có điều kiện

`cost-scenario.json` thay kịch bản cũ, giữ bản cũ ở `pre-review-001/`. Dùng số đo cũ đã kiểm hash ở pilot007/004, timing OB T052 và chi phí cloud013; không cần quay lại số đo T024 khác tuyến khi cùng driver T054 đã có các nhóm CIRCA/MicroRank/A. Với mỗi nhóm local, dùng max DEV quan sát để tính proxy, không nhận đó là phân phối chi phí cohort.

| Phần | Kịch bản lặp proxy DEV | Giới hạn |
|---|---:|---|
| EC2_1, một worker |6,90giờ | Một số vế chỉ có wall khi chạy chồng; dùng làm proxy, không gọi số đo một worker. |
| EC2_2, một worker |6,95giờ | Ngoại suy từ ít ca và có M1 C-e làm proxy. |
| Laptop, tính tuần tự |6,08giờ | Đã gồm742job, cả180A; hai worker không tự chia đôi do RAM/nhóm/ràoA. |
| Toàn chuỗi, kịch bản cơ sở |9,12giờ | Có chuyển đi, max ba queue, nhận, hash/giải nén/verify và proxy chấm. |
| Toàn chuỗi, độ nhạy chậm |18,34giờ | Nhân2 chi phí phương pháp/chấm, network1MiB/s và output4lần thay vì kịch bản cơ sở2MiB/s. |

Không gọi9–18giờ là khoảng tin cậy hoặc cận trên. Network và hash/I/O là giả định tốc độ; đã giữ số staging DEV cũ như quan sát, không suy thành tốc độ đảm bảo. Dung lượng trả về được dựng lại theo nhóm của phân lô mới và mẫu DEV storage011, giữ fallback. Chưa đọc byte test để tính thời gian.

**Chấm toàn cohort chưa được đo.** Kịch bản chấm dùng lần report fixture cũ thành công dưới timeout120giây cho28slot, ngoại suy theo1640/28 và thêm độ nhạy×2. Đây là proxy chưa kiểm về quan hệ tuyến tính, không là số đo7030giây hay cận trên cho evaluator thật. Số ô, hạng/hòa, Fraction/bootstrap, lượng seal và audit lỗi đọc lại nguồn có thể làm sai proxy. Không chạy lại scientific method hoặc mở test để lấp chỗ này. Trạng thái đó được giữ trong `cost-scenario.json#/uncertainty` và phải khai khi Minh duyệt lượt dài.

Đường găng giữa các queue được lấy max, không cộng ba queue. Chi phí ngoài queue được cộng riêng. Khi chạy thật được cấp, agent đo từng pha; WAIT_RESOURCE có thể cần resume thủ công, thời gian chờ người không nằm trong dự toán. Không trần cộng dồn hoặc retry mới được tạo ở lượt đáp này.

## Các điểm còn lại của Claude

Đồng ý giữ OPEN về OB lệch mẫu, ca A thiếuN và H1 RE3. D1/D4 giới hạn diễn giải vẫn giữ; C-e giữ ngoại lệ đúng phép, không quy sai khác cho OS/BLAS đã được chứng minh. Giới hạn graph và phần DT18/cô còn lại không đổi. Main chưa trả lời RQ3b/RQ3d.

Việc chỉ định Codex làm quản lý nguồn/evaluator đã là mục riêng trong đề nghị duyệt cuối, chưa được xem là quyền hiện tại. Commit chưa được Minh duyệt nên giữ chưa commit/push; SPEC cho khóa byte/provenance trước khi có commit và nói commit theo quyền riêng. Không thêm commit thành cổng bắt buộc để thay một quyết định chưa có.

## Kiểm sửa và bước tiếp

`metadata-revision-check.json`:106pin code không đổi,1640slot và2support giữ nguyên; cấu hình/seed/source/window/env không đổi. Job chỉ đổi protocol_ref và hash phụ thuộc C-d3 theo protocol mới. EC2_1 đổi2→1worker; EC2_2 vẫn1, laptop vẫn2tối đa. Validator và ghép ma trận đạt. Hai EC2 đã nhận/kiểm metadata mới, nguồn byte test chưa được chuyển; biên nhận `ec2_*-after-review-environment.json`. Dùng lại101fixture mỗi máy và đối chiếuDEV đã có vì mã thực thi không đổi; không rerun phương pháp vì đổi gói.

Đề xuất Claude kiểm ngắn diff metadata, kịch bản chi phí và nguồn ghi quyền của lượt này theo đề nghị của Claude. Nếu không còn phản đối thì đề xuất dừng phản biện chuẩn bị. Minh quyết khóa/chạy riêng theo `de-nghi-duyet-main.md` và manifest mới. Hai bên thống nhất cách sửa không thay bằng chứng khoa học hoặc tự nghiệm thu T054/G3.
'''
    put(RUN/'review-response.md',response)
    report=(base/'bao-cao.md').read_text(encoding='utf-8')
    report=report.replace('# Chuẩn bị main 013 — chờ Claude kiểm và Minh duyệt chạy','# Chuẩn bị main 013 — đã đáp review, chờ kiểm metadata sửa')
    report=report.replace('Codex là người làm, Claude là người phản biện.','Codex là người làm, Claude là người phản biện. Claude đã kiểm bản trước sửa, không có finding CHẶN; hai finding vận hành được đáp tại `review-response.md`.')
    report=report.replace('| 448 | 2 | 2 |','| 448 | 2 | 1 |')
    report=report.replace('bản cài013 này chưa được Claude kiểm','metadata sửa sau phản biện chưa được Claude kiểm')
    a=report.index('Chạy chính dài hơn1giờ');z=report.index('## D1–D4/R3',a)
    report=report[:a]+'''Sau phản biện, ứng viên dùng một worker trên mỗi EC2. Không dùng số chồng rồi chia2 như thông lượng đã xác minh; H1 tranhCPU và H2 vế nặng còn chưa phân xử. `review-response.md` và WHY ghi lý do giữ method600giây/C-d360giây là ngân sách ứng viên, không bảo đảm mọi ca hoàn tất. Mã/slot/config/seed/source/window/env không đổi theo `metadata-revision-check.json`; job chỉ đổi pin protocol và phụ thuộc. Hai EC2 đã kiểm metadata/môi trường mới, xem `ec2_*-after-review-environment.json`.

Chạy chính dài hơn1giờ, chờ Minh duyệt riêng. `cost-scenario.json` hiện gồm local, chuyển/nhận/hash/verify/chấm. Proxy tuần tự: EC2_1=6,90giờ, EC2_2=6,95giờ, local=6,08giờ. Hai kịch bản toàn chuỗi9,12/18,34giờ có giả định về cost/network/I/O/output, không là ETA hoặc cận trên đã kiểm. Chấm fullcohort chưa được đo; proxy dựa vào timeout120giây của report fixture thành công28slot, ngoại suy1640/28, nên giữ OPEN về tính tuyến tính/bootstrap/audit lỗi. Lượt chậm hoặc phải chờ RAM/người có thể vượt kịch bản. Không tự đặt trần tổng, retry hoặc tắt máy.

'''+report[z:]
    report+='''\n\nBản Claude đã kiểm được giữ ở pre-review-001; manifest mới ghim metadata sau sửa. Năm wrapper và ba helper thực thi không đổi, nên các phép kiểm trên code được dùng lại; không nhận Claude đã kiểm bản metadata mới.\n'''
    put(RUN/'bao-cao.md',report)
    proposal=(base/'de-nghi-duyet-main.md').read_text(encoding='utf-8')
    proposal=proposal.replace('Trạng thái: đề nghị sau Claude kiểm, chưa có quyền chạy.','Trạng thái: đã đáp phản biện bản gốc, metadata sửa đang chờ Claude kiểm; chưa có quyền chạy.')
    proposal=proposal.replace('phân lô30/30 và policy trong hồ sơ.','phân lô30/30, một worker trên mỗi EC2 và policy trong hồ sơ. Laptop tối đa hai worker theo RAM/nhóm, TORAI A sau non-A của laptop.')
    proposal+='''\n\nKhi duyệt lượt dài: kịch bản toàn chuỗi trong cost-scenario.json khoảng9,1/18,3giờ dưới các giả định đã khai; không phải ETA/cận trên, chấm fullcohort chưa đo. Bản Minh xét phải là manifest sau đáp review, không pin gói trước sửa. Chỉ định quản lý nguồn/evaluator và các quyền ở trên chỉ có hiệu lực từ lời duyệt cuối đúng gói.\n'''
    put(RUN/'de-nghi-duyet-main.md',proposal)
    grant=read_pin(pin(base/'grant-template.json'))
    grant['approved_candidate_protocol_sha256']=digest(RUN/'protocol-candidate.json')
    grant['approved_source_bundle_sha256']=digest(RUN/'source-bundle.json')
    atomic(RUN/'grant-template.json',grant)
    atomic(RUN/'readiness.json',dict(preparation_complete_by_codex=True,
          claude_review_of_original_implementation='NO_BLOCKING_FINDINGS_TWO_OPERATIONAL_FINDINGS',
          metadata_revision_review='PENDING_CLAUDE',g3=False,test_grant=False,main_started=False,score_started=False,commit_push=False,
          response=pin(RUN/'review-response.md'),revision=pin(RUN/'metadata-revision-check.json'),
          candidate=pin(RUN/'protocol-candidate.json'),bundle=pin(RUN/'source-bundle.json')))
    dossier=ROOT/'results/T-054/ho-so-g3.md';text=dossier.read_text(encoding='utf-8')
    text=text.replace('chờ Claude kiểm bản cài và Minh duyệt chạy.','đã đáp hai finding vận hành của Claude, chờ kiểm metadata sau sửa và Minh duyệt chạy.')
    text=text.replace('Claude đã góp ý và thống nhất phần kế hoạch trước triển khai, chưa kiểm các output013 mới.','Claude đã kiểm bản013 trước sửa, không có finding CHẶN. Codex nhận F1(a)/F2; một worker mỗi EC2 và dự toán toàn chuỗi nằm trong metadata sau sửa, còn chờ Claude kiểm phần đổi này.')
    text+='''\n\n[Phản hồi và kiểm sửa](runs/chuan-bi-main-013/review-response.md): bản trước sửa ở pre-review-001. Candidate hiện một worker/EC2, laptop tối đa hai. Không đổi code/slot/config/seed/source/window/env. Dự toán9,1/18,3giờ là kịch bản chưa kiểm; chấm toàn cohort chưa đo. Grant vẫnfalse, chưa mở test/main.\n'''
    put(dossier,text)
    runbook=ROOT/'results/T-054/runbook.md';text=runbook.read_text(encoding='utf-8')
    text=text.replace('448job+2support,2worker','448job+2support,1worker')
    text+='''\n\nSau đáp review: xem review-response.md và manifest mới. Cả hai EC2 một worker, không dùng worker2 của bản trước sửa. WAIT_RESOURCE khi không có active có thể làm supervisor thoát; agent kiểm RAM/PID/token rồi resume cùng plan trong quyền main đã cấp, không tự đóng ứng dụng Minh hoặc retry slot hỏng. Dự toán toàn chuỗi có giả định; quyền cuối phải chỉ đúng bản metadata đã được kiểm lại.\n'''
    put(runbook,text)
    spec=ROOT/'tasks/T-054-khoa-g3-chay-p7-a/SPEC.md';text=spec.read_text(encoding='utf-8')
    text=text.replace('chuẩn bị013 theo Minh duyệt đã có output, chờ Claude kiểm bản cài và Minh duyệt','chuẩn bị013 đã đáp review; bản gốc được Claude kiểm, metadata sửa chờ kiểm lại và Minh duyệt')
    text=text.replace('EC2_1=448job+2support/2worker','EC2_1=448job+2support/1worker')
    at=text.index('\n',text.index('**Đầu ra chuẩn bị013, chờ phản biện bản cài:**'))
    note='''\n\n**Đáp review013 theo quyền ghi có điều kiện 07/11/2026:** nhận F1(a)/F2; ứng viên hiện một worker mỗi EC2, laptop tối đa hai theo RAM/nhóm và A sau non-A. Giữ mã thực thi và toàn bộ slot/config/seed/source/window/env, tái ghim protocol/plan/contract/packet/manifest và hồ sơ; không chạy lại method. Bản gốc Claude đã kiểm giữ ở pre-review-001; metadata sau sửa chờ Claude kiểm. Dự toán toàn chuỗi nằm trong cost-scenario, là kịch bản chưa kiểm, không khẳng định tổng thời gian không đổi hoặc mọi test xong trong600giây. G3/test/nguồn/chuyển/main/chấm/chỉ định quản lý nguồn/evaluator và commit chưa được cấp.\n'''
    text=text[:at]+note+text[at:];spec.write_bytes(text.replace('\r\n','\n').replace('\n','\r\n').encode('utf-8'))
    state=ROOT/'docs/STATE.md';lines=state.read_text(encoding='utf-8').splitlines()
    for i,line in enumerate(lines):
        if line.startswith('- **T-054'):
            lines[i]='- **T-054 — đã đáp review013, chờ Claude kiểm metadata sửa.** Codex làm, Claude phản biện. Nhận F1(a)/F2: ứng viên một worker/EC2, bổ sung dự toán toàn chuỗi; code/ma trận giữ nguyên. Bản gốc và mọi lượt giữ lại; chưa G3/test/main/chấm/commit. [Phản hồi](../results/T-054/runs/chuan-bi-main-013/review-response.md), [LOG](../tasks/T-054-khoa-g3-chay-p7-a/LOG.md).'
    state.write_bytes(('\r\n'.join(lines)+'\r\n').encode('utf-8'))
    log='''\n\n### Kết quả đáp Claude và sửa metadata013, 07/11/2026\n\nĐồng ý F1 về căn cứ worker/thông lượng/biên wall-clock; nhận F1(a) và F2. Đã tự kiểm7job cộng475,39giây trong239,93giây; không xác nhận tranhCPU hay vế vốn nặng, không khẳng định đổi worker giữ nguyên TIMEOUT/tổngthời gian. Ghi WHY trước áp dụng. Một worker/EC2 là CANDIDATE trình khóa, không ghi rằng Minh đã duyệt chạy. Nguồn quyền có điều kiện và bản Claude nguyên văn đã lưu; bản013 gốc giữ ở pre-review-001 cùng ánh xạ preservation.\n\nĐổi metadata: EC2_1 từ2→1worker;1640job+2support, case/config/seed/source/window/env không đổi.106pin mã thực thi giữ nguyên. Validator/union/phụ thuộc đạt; chỉ job.protocol_ref và main_dependency rehash. Hai EC2 đã stage/kiểm metadata+môi trường mới trong vùng013, không chuyển test. Vì code và tuyến một worker đã có bằng chứng, dùng lại fixture/DEV hợp lệ; không chạy lại method.\n\nF2 dùng cost pilot007/004, timingOB T052, cloud013 và storage011 sau kiểm hash. Proxy tuần tự cloud6,90/6,95giờ, local6,08giờ; toàn chuỗi9,12/18,34giờ dưới giả định. Phần chấm fullcohort chưa đo: proxy scale timeout120s của fixture report28slot thành công, không phải số đo full1640slot. Hrank/bootstrap/audit lỗi/network/RAM/đợi người có thể làm sai kịch bản; giữ OPEN và owner trong cost-scenario. Phép đọc cost đầu có lỗi chuẩn hóa prefix manifest012, đã giữ biên nhận và sửa trước sinh số; không có lượt method nào.\n\nĐã đổi SPEC, ho-so-g3/runbook, bao-cao/de-nghi, WHY/DECISIONS và đúng dòngSTATE theo nguồn hợp lệ; không đổi mã phương pháp/wrapper/helper thực thi, AGENTS/MRP/LESSONS hoặc data/private. Phản hồi ở review-response.md; grant mẫu vẫnfalse. Không còn phản đối cách xử lý hai finding; chưa nhận Claude đã kiểm metadata mới hoặc G3 đã đạt. Câu hỏi nguồn RQ3b/RQ3d chưa có điểm test; giới hạn OB/A/RE3 giữ nguyên. Chủ nguồn/evaluator và quyền dài/chuyển/chấm vẫn nằm trong đề nghị duyệt cuối; commit không tự thêm thành điều kiện trước main, chưa commit/push.\n\nBước tiếp: Claude kiểm ngắn phần metadata/dự toán/nguồn quyền sau sửa rồi đề nghị dừng hoặc nêu bất đồng; Minh quyết. Nếu dừng và Minh duyệt đúng manifest mới theo de-nghi-duyet-main.md, Codex mới ghi nguồn lời duyệt/grant thật và chạy theo runbook. Prompt bàn giao trung tính ở runs/chuan-bi-main-013/prompt-claude-after-review.txt để Minh chuyển thủ công, không tự gửi. Lệnh triển khai cuối: stage_review.py, cả hai host PASS; lệnh kiểm kết thúc dự kiến: verify_manifest.py --documents và kiểm bảo toàn bản trước sửa. Đề xuất commit khi Minh duyệt: T054: address preparation013 review and align EC2 worker policy; chưa commit/push.\n'''
    with (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab')as f:f.write(log.encode('utf-8'))
    # Exact common/stage/gate blocks, only neutral placeholders filled.
    template=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8')
    def block(title):
        s=template.index(title);a=template.index('```text',s)+len('```text\n');b=template.index('```',a);return template[a:b]
    common=block('## Prompt chung')
    fills={
      '<mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn>':'T-054, D:/RCA-flashticket/tasks/T-054-khoa-g3-chay-p7-a/SPEC.md; bản đáp và metadata checkpoint013 sau review',
      '<soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa>':'kiểm lại phản hồi và sửa',
      '<gói, cổng hiện tại; ngoài task thì ghi loại đề xuất>':'P7, chuẩn bị G3(a)',
      '<tên theo SPEC; ngoài task thì ghi vai trò dự kiến>':'Codex làm, Claude phản biện theo SPEC',
      '<danh sách đường dẫn và git diff từ commit gốc nếu có>':'D:/RCA-flashticket/AGENTS.md; docs/STATE.md; SPEC/LOG T-054; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; hai nguồn đề tài theo mẫu; results/T-054/{ho-so-g3,runbook}.md; runs/chuan-bi-main-013/metadata-after-review.patch và pre-review-001/preservation.json',
      '<đường dẫn theo thứ tự thời gian; không có thì ghi không có>':'các mục trao đổi trong LOG T-054; results/T-054/runs/chuan-bi-main-013/claude-review-013-001.txt, review-response.md',
      '<đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng>':'D:/RCA-flashticket/results/T-054/runs/chuan-bi-main-013/{manifest.json,pre-review-001/,metadata-revision-check.json,review-evidence.json,cost-scenario.json,prepared/,protocol-candidate.json,dispatch-contract.json,main-packet.json,grant-template.json,de-nghi-duyet-main.md}; các ref gốc từ chúng. Lệnh chỉ đọc từ repo: D:/RCA-ext/envs/T-014-main/Scripts/python.exe -X utf8 -B results/T-054/runs/chuan-bi-main-013/verify_manifest.py --documents',
      '<chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác>':'chỉ đọc và trả lời trong chat; không ghi file, không SSH, không chạy lại thực nghiệm/kích hoạt/main hoặc mở dữ liệu khóa, không commit/push'}
    for old,new in fills.items():assert old in common;common=common.replace(old,new)
    put(RUN/'prompt-claude-after-review.txt',common+'\n'+block('### Kiểm lại phản hồi và sửa')+'\n'+block('### G3 — Khóa thiết kế trước khi mở test'))
    print(json.dumps(dict(PASS=True,pipeline_hours=hours,docs_updated=True,grant_flags_remain_false=True)))


if __name__=='__main__':main()
