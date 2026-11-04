"""Báo cáo và bàn giao theo kết quả thật; không tự nghiệm thu hoặc mở G3."""
import hashlib
import json
import time
from datetime import datetime

import adapter_t047 as ad
from m1_danh_gia.pha2 import giai_ma_json as dec


def read(p):
    return dec(json.loads(p.read_text(encoding='utf-8')))


def main():
    root,out = ad.ROOT,ad.OUT
    stamp = datetime.now().astimezone().isoformat(timespec='seconds')
    t1,k,b,table = [read(out/p) for p in ['t1.json','khoi-k.json','do-ben.json','so-sanh-t045.json']]
    post = read(out/'runs/c1-kiem-hau-xu-ly-001/checks.json')
    assert t1['PASS'] and k['STOP'] is None and post['PASS']
    winner = k['chon_khoi']['P']['chon'];chosen=k['cau_hinh']['K-'+winner]
    changed=read(out/'runs/c1-tong-hop-so-001/summary.json')
    automatic = read(out/'runs/b5-c1-co-che-001/co-che-khoi-k.json')
    audit = out/'runs/ket-phien6-001';audit.mkdir(exist_ok=False)
    table_rows=[]
    for cid,c in sorted(table['cau_hinh'].items()):
        table_rows.append('| '+cid[2:]+' | '+' | '.join(f"{float(c['MRR'][name]['gop']):.6f}" for name in
                          ['G0D0_S0','G0D0_S1','G3D1_S0','G3D1_S1'])+' |')
    pair_rows=[]
    for key,worlds in changed['changed_pairs'].items():
        a,z=worlds['P'];pair_rows.append(f'| {key} | {a} → {z} |')
    boot_rows='\n'.join(f'| {cid} | {n}/1000 |' for cid,n in sorted(b['tan_suat_thang'].items(),key=lambda x:-x[1]))
    trait=['runs/c1-method-analysis-e1-e2-001/analysis.md','runs/c1-method-analysis-e3-e5-001/analysis.md']
    for p in trait:assert (out/p).is_file()
    mechanism = dict(automatic, status='ANALYZED_COMPUTATIONAL_PATHS_WITH_OPEN_SCIENTIFIC_QUESTIONS',
        original_FACTS='results/T-047/runs/b5-c1-co-che-001/co-che-khoi-k.json',
        interpretation=[dict(file='results/T-047/'+p,sha256=hashlib.sha256((out/p).read_bytes()).hexdigest()) for p in trait],
        additional_evidence=['results/T-047/runs/c1-method-analysis-e1-e2-001/ce-E1-E3-E5.json',
            'results/T-047/runs/c1-method-analysis-e1-e2-001/raw-api-002/summary.json',
            'results/T-047/runs/c1-method-analysis-e3-e5-001/raw-refine-002/summary.json',
            'results/T-047/runs/c1-method-analysis-e3-e5-001/e5-FI-api-replay.json',
            'results/T-047/runs/c1-tong-hop-so-001/world-scoring.json'],
        scope_conclusion='Đã phân xử đường tính toán quan trọng và điểm dừng luật; không xác nhận cơ chế vật lý chung, hiệu chuẩn hoặc hiệu quả độc lập.',
        OPEN_after_analysis=['nghĩa vận hành của mẫu log có/mất và sự kiện không được thu',
             'tính nhân quả vật lý của kênh giải thích theo quan hệ gọi/E5',
             'tác động riêng G3 và D1, chi tiết tầng/khóa/inherited_by non-P chưa lưu',
             'hiệu chuẩn cổng, độ bền trên dữ liệu độc lập và khả năng chuyển FlashTicket'])
    ad.ghi(out/'co-che-khoi-k.json',mechanism)
    score_table='\n'.join(f"| {name[2:]} | {v['MRR']['P']['gop']:.6f} | {v['MRR']['P']['RE2-TT']:.6f} | {v['MRR']['P']['Nezha-OB']:.6f} | {v['moc_gia']['N1_trung_binh']} |" for name,v in
                         [(cid,k['cau_hinh'][cid]) for cid in ['K-R0','K-'+winner,'K-E1+E2+E3+E5']])
    report=f'''# T-047 — kết quả Phiên 6

Trạng thái: **hoàn tất phần thực nghiệm/hậu xử lý trong phạm vi được duyệt; chờ Claude phản biện và Minh nghiệm thu**. Ghi {stamp}. Không tự đóng task, khóa G3 hoặc cho phép mở test.

## Kết quả chính và mức căn cứ

Luật chọn đã khóa giữ **{winner}** tại P, S_lo và S_hi. Mức HẠI chính h=1 giữ nguyên; h=0,5 và 2 đều chạy lại đủ cặp/bộ chọn và vẫn chọn cùng cấu hình. Không có cờ mặc định phải trình thêm tại lựa chọn chính. Đây là kết cục trên dev, không phải quyết định mới của Minh hoặc xác nhận cơ chế/hiệu quả RCA.

| Cấu hình | MRR dev gộp | RE2-TT | Nezha-OB | N1 trung bình cửa sổ giả |
|---|---|---|---|---|
{score_table}

Nguồn: `khoi-k.json#/chon_khoi`, `#/cau_hinh`, `#/do_nhay_muc_HAI`, `#/mac_dinh_ap`. Có 30 ca RE2-TT và22 Nezha-OB; dữ liệu dev được dùng nhiều lần, số này lạc quan và không độc lập với thiết kế. N1 của cấu hình chọn là {chosen['moc_gia']['N1_trung_binh']} thực thể/cửa sổ; V0 vẫn CAUSE_FOUND ở30/30 cửa sổ giả của cấu hình này. Vế HẠI tương đối không hiệu chuẩn số cảnh báo tuyệt đối và không chứng minh phương pháp đã phân biệt sự cố với biến động nền.

## Kiểm nguồn, cài đặt và lượt chạy

- Đã tự rà SPEC từ nguồn DT18-NV2/NV3, hướng dẫn cô, MRP P6/P7, WHY/DECISIONS/LESSONS và code/đầu ra gốc trước khi dùng nhận xét cũ. SPEC là quyền thực hiện, không là chứng nhận phương pháp đúng. Điểm chặn C1 đã được điều tra bằng raw và Minh duyệt đúng patch; không có mâu thuẫn mới buộc đổi thiết kế trong phần đã kiểm.
- C1 chỉ đổi hai hàm `o_1s`/`tu_tuong_quan` theo patch đã duyệt: tổng bù và thứ tự tính cố định. Nguồn chạy là revision nền cộng C1, metadata ghi hash code thực. Một commit C1/Q-233 đã có; không commit thêm hoặc push. Receipt ở `runs/c1-ap-dung-001/commit.json`. Không sửa SPEC đã khóa, WHY, luật chọn hoặc tham số.
- Hồi quy sau C1: T-044 374, T-045 16, T-046 46 test qua; T-047 sau sửa guard171 test qua. Nguồn JUnit tại `runs/c1-T-044-001/`, `c1-T-045-001/`, `c1-T-046-001/`, `c1-guard-hoi-quy-002/`. Helper luật C giữ hash đã ghim; test qua chỉ xác nhận phạm vi đã kiểm.
- T1 mới đủ238 lượt:52ca×3seed,52ca xáo,30 cửa sổ giả. Các seed/xáo trùng byte. Native52thật/30giả trước-sau C1 giống hệt;82 tóm tắt R0 với T-046 không lệch. D5 D1 có58đơn vị hợp lệ,0đổi cờ khi thời gian quan sát lệch±1%. Nguồn `t1.json`, `runs/c1-delta-that-001/summary.json`, `runs/c1-delta-ce-001/summary.json`.
- K đủ16×52=832 thật và16×30=480 giả. Không bỏ ca hoặc bản ghi lỗi. R0 khớp T1 và K-đủ khớp phần tóm tắt tương ứng T-046, cả thật/giả; không có lệch ở các đại lượng chung cần miễn hoặc đổi tiêu chí. Không nhận là đã chạy lại toàn bộ A/A của T-046 hoặc có toàn bộ native lịch sử để so mọi trường. Nguồn `runs/b3-k-c1-*/kiem-k-pha1.json`.
- Hai hash K đã ghi LOG trước đọc nhãn, kể cả D2. D2 tái lập12/12 baseline. Chấm đúng52ca dev, không dữ liệu khóa/cloud. QT5 đã rà đủ832/480bản: Kthật108groupdom+2toanhoa; giả98groupdom, không lỗi cài đặt chưa giải thích. Có đơn vị hợp lệ trong ca toàn hòa, không gán thành dữ liệu rỗng. Nguồn `runs/c1-qt5-audit-001/summary-corrected-002.json`, `runs/c1-qt5-ce-audit-001/summary.json`, `tai-lap-baseline.json`.

## Luật C, lựa chọn và độ bền

Đủ43cặp ở ba thế giới, dùng cùng helper cho pha2/bootstrap/độ nhạy. N1 lấy tạiP trên cùng tập cửa sổ hợp lệ của hai nhánh, Fraction và dấu > chính xác. UV-6, điều kiện E5 và M+M′ được giữ; `khong_moc_gia` và kết hợp thế giới tính lại. Không áp trần tỷ lệ V0 vào số đếm N1. Kiểm trực tiếp lại43 chênh từ tầng, trung bình từng ô bảng2×2 và bảo toàn mẫu đạt: `runs/c1-kiem-hau-xu-ly-001/checks.json`.

Bootstrap đủ1000 mẫu, seed {b['seed']}, mức chính1, lấy lại ô ghép cặp và dùng đúng helper. Bội số tất cả ca bằng1 tái lập toàn bộ kết quả chính. Giữ mọi mẫu, không bỏ mẫu không chọn được.

| Cấu hình được chọn trong mẫu hợp lệ | Tần suất trên toàn bộ1000mẫu |
|---|---|
{boot_rows}

Còn một mẫu chọn R0, không đạt điều kiện có E1/E2/E5; giữ với mã dừng bước8. 999mẫu có lựa chọn đạt điều kiện; không dùng999 làm mẫu số để làm đẹp tần suất. Không có mẫu C-e chưa kiểm được;109mẫu có cờ trái chiều dataset cần trình theo luật,77mẫu có trái chiều ở cặp liên quan cấu hình thắng. Nguồn `do-ben.json#/loai`, `#/tan_suat_thang`, `#/tan_suat_co`; từng mẫu tại `runs/b6-c1-do-ben-001/samples.jsonl`. Lựa chọn chính còn mong manh theo ô; việc h=0,5/1/2 không đổi cấu hình không xóa giới hạn này. Không đổi h hoặc chọn theo bootstrap.

## Bảng2×2 tạiP

| Cấu hình | G0/D0,S0 | G0/D0,S1 | G3/D1,S0 | G3/D1,S1 |
|---|---|---|---|---|
{chr(10).join(table_rows)}

Nguồn toàn bộ số, từng dataset, từng ca và tương tác: `so-sanh-t045.json#/cau_hinh`. Phục dựng S0 trải thực thể, bỏ độ lớn, sắp/gộp lại; kiểm độc lập bằng tầng/K_I/K_raw trên đủ832bản mới và bằngT4c trên832bản cũ. MRR ôG3/D1,S1 khớp pha2 ở cả16cấu hình. Ở {winner}, thay thang trên G3/D1 tăng1/208; thay gói cổng khi giữS1 tăng1/780; đó là mô tảdev, không tách G3 khỏiD1. S1 không có lợi đồng đều: trên nềnE3+E5 hoặcE1+E3+E5, nó làm MRRgộp giảm trong gói cổng mới. Không dùng bảng chọn lại thang/cổng/lượt. ChỉP có đủ bốn ô.

## Thay đổi kết cục và cơ chế đã kiểm

Có {changed['changed_count']} cặp đổi kết cục so T-045, giống nhau ở ba thế giới:

| Cặp tắt→bật | T-045 → T-047 |
|---|---|
{chr(10).join(pair_rows)}

Nguồn `runs/c1-tong-hop-so-001/summary.json#/changed_pairs`; các bước/reasons/RRtheoô đầy đủ ở `khoi-k.json#/cap`. Không đồng nhất đổi kết cục luật với đổi một cơ chế riêng. Cả gói cổng/thang/vếC-e thay cùng lượt.

Đã trích chuỗi đầy đủ từng ca của15cặp cần đọc (các cặp đổi và đảo tại cấu hình thắng), thêm phân tíchE1/E2 theo52ca; không dừng ở gán cờ. Phân tích người làm có ở:

- `runs/c1-method-analysis-e1-e2-001/analysis.md`: E1/E2, ba cặp thêmE1 đổi kết cục, ca hại/lên/đúng, raw trace→mẫu→G0/G3 ở ba đơn vị; mọi trường chung tái lập. Tương tácE1×E3×E5 trên30cửa sổ giả giữ log/metric/coverage/graph, E1 đổi mẫu/lớp thao tác; replayE5 60/60 nhánh khớp. Lớp không lan làm một số kênh giữF_I, tăngN1; có cả cửa sổ giảm/không đổi. Đây là đường tính, không chứng minh kênh ấy thật sự tự sinh.
- `runs/c1-method-analysis-e3-e5-001/analysis.md`: đủ4cặp×52ca, raw log→Drain→cổng298đơn vị ở4ca không lệch; E5 replay156/156ca khớp. E3 có cả ca làm đối thủ vượt root và ca giúp root qua khóa độ lớn. NEW_OP/STOPPED s=1 là nhánh trực tiếp đã khai, không tự là lỗi bỏphi. Severity/nhãnKHONG_LOI của bộ phân lớp không chứng minh hoạt động lành. E5 có ca root bị hạF_I nhưng thứ hạng vẫn cải thiện nhờ đối thủ hạ nhiều hơn; M5 không bao mọi ca tụt hạng.

`co-che-khoi-k.json` trỏ tới diễn giải và các OPEN; bản trích FACT nguyên gốc vẫn ở `runs/b5-c1-co-che-001/co-che-khoi-k.json`. RR/Hit1/M5 từng ca giống giữa ba thế giới trên832bản, không chỉ cùng MRR trung bình; kênh/khóa số có khác (`runs/c1-tong-hop-so-001/world-*.json`). Không mượn tầng/khóaP thay non-P vốn chưa được native lưu riêng.

Phân loại đã kiểm: các raw/API đã tái dựng khớp cài đặt/adapter; không thấy bằng chứng buộc sửa công thức/SPEC/test. Một số giới hạn nằm ở quy tắc/giả định của phương pháp: novelty/mất mẫu, s=1, giả định kênh giải thích theo cạnh và lớp không lan. Coverage không đổi trong cặp không chứng minh không thiếu thu. Không cộng cờ chồng lấn thành tỷ lệ nguyên nhân, không quy mọi ca sai cho dataset, Drain hoặc E5. Cặp R0→nhiều thành phần không phân xử tác động riêng; giữ chuỗi và giới hạn, không ép nguyên nhân duy nhất.

## Đối chiếu nguồn nghiên cứu và phần còn thiếu

DT18-NV2/NV3 và MRP P6 được hỗ trợ ở phần chọn/kiểm thành phần trên dev: nút là dịch vụ/thành phần, log vàmetric gắn nút, span/thao tác và quan hệ cha-con dùng tính mẫu độc quyềnE1; mẫu cạnhE2 được gán cho bên được gọi; E5 dùng cạnh và nhóm vòng để đổiF_I. Cấu hình chọn cóE1/E2 dùng quan hệ trong phép tính, không chỉ vẽ đồ thị. C-d1/C-d3 đều có dùng đồ thị, không là đối chứng bỏ quan hệ.

Task chưa trả lời xong RQ3a–d, chưa đo lợi ích trên dữ liệu không dùng khi thiết kế, chưa xác nhận vùng ảnh hưởng thật hoặc cơ chế vật lý chung. T1/D2/test qua không thay các bằng chứng ấy. Các nghĩa vụ đối chứng tương đương, T4/T4b mới/hiệu chuẩn, chọnverdictP7, hồ sơG3, dữliệuđộc lập vàFlashTicket vẫn theo các task/gói sau; không tự mở hoặc thu hẹp chúng.

OPEN cụ thể: nghĩa vận hành của mẫu log có/mất; quan hệ nhân quả của các kênh giải thích; vai trò thiếu sự kiện/coverage ở nhóm chưa phân xử; chi tiết non-P chưa lưu; G3gần hằng và hiệu chuẩn; độ bền ngoài52ca/dev. Các câu này ảnh hưởng khóa thiết kế/G3 và khả năng chuyển sangFlashTicket. N1 cao và bootstrap phân tán phải đi cùng đề nghị dùng nềnE1+E2; không coi hai agent cùng ý kiến hoặc nghiệm thu task là xác nhận phương pháp.

## Quyền ghi, lịch sử và bàn giao

Giữ mọi lượt lỗi, trước/sauC1 và dùng lại hợp lệ; không đổi ma trận/luật chọn sau nhìn số. Guard Windows được tái lập47/768 do khác dạng tiền tố đường sauresolve, sửa trong adapter results; sau sửa0/768. Hai lỗiT1 lịch sử thiếu giá trị lúc so nên liên hệ cùng cơ chế chỉ là suy luận hồi tố. Một lượt test lỗi11fixture do thiếu thư mục cha đã giữ; sửa cách gọi, không sửa đáp án. Chi tiết ở LOG.

Có vi phạm ghi cache: lệnh test tạo5file ngoài phạm vi tại.pytest_cache. Đã báo Minh, sao lưu/hash, Minh duyệt dọn và5file đã xóa. Ba thư mục rỗng còn do công cụ chặn xóa với lý do“blocked by policy”; không lách chặn. Receipt `runs/c1-cache-vi-pham-001/cleanup.json`. Không ảnh hưởng số liệu, nhưng không gọi phiên là tuân thủ quyền ghi hoàn toàn.

File được sửa theo quyền: results/T-047, nốiLOG, dòngT047STATE; ngoại lệC1/Q233 đúng duyệt và mộtcommit. Giữ các thay đổi có sẵn ởWHY/DECISIONS/SPEC, không sửa chúng theo diễn giải mới. Khôngcommit thêm/push. Chi phí gồm mọi lượt thử/lỗi/chạy lại và toàn bộ thời gian nền; chỉ loại khoảng chờMinh trước duyệtC1 đã lưu. Trần28800giây; thời gian chốt cuối lấy `runs/chot-phien6-001/result.json`, không reset phần đã chạy.

Kiểm cuối/phạm vi/hash: `runs/ket-phien6-kiem-001/kiem-ban-giao.json`, manifest.json sau chốt. Prompt trung tính theo nguyên văn mẫu ở `prompt-claude-phien6.txt`, Minh chuyển thủ công; chưa tự gửi hoặc ghi phản biện thayClaude. Phần output được đề nghị nghiệm thu trong phạm vi mô tả/kiểm đã làm; task và câu hỏi nghiên cứu vẫn doMinh quyết. Bước tiếp: Claude soát độc lập kết quả, sau đóMinh quyết nghiệm thu/sửa hoặc giao task kế tiếp. Không tự khởi độngtask(2).
'''
    (out/'bao-cao.md').write_text(report,encoding='utf-8')
    ad.ghi(audit/'summary.json',dict(status='COMPLETE_PENDING_REVIEW',T1_PASS=True,T1_main_records=238,
        K_main_records=1312,winner=winner,bootstrap_n=b['n'],changed_pairs=changed['changed_count'],
        computational_path_analysis=True,scientific_mechanism_confirmed=False,Minh_accepted=False,
        report='results/T-047/bao-cao.md',source_report_sha256=hashlib.sha256((out/'bao-cao.md').read_bytes()).hexdigest()))
    with (out/'so-lan-nhin.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(time=stamp,task='T-047',cong_doan='buoc5_9_dien_giai_bao_cao',
                               muc_dich='diễn giải/chốt theo kết quả đã khóa; không chọn lại',
                               sources=['khoi-k.json','do-ben.json','so-sanh-t045.json','co-che-khoi-k.json']),ensure_ascii=False)+'\n')
    state=root/'docs/STATE.md';lines=state.read_bytes().splitlines(keepends=True)
    ids=[i for i,line in enumerate(lines) if line.startswith(b'- **T-047 ')];assert len(ids)==1
    i=ids[0];nl=b'\r\n' if lines[i].endswith(b'\r\n') else b'\n'
    lines[i]=('- **T-047 — chạy khối K lượt thứ hai:** **chờ phản biện Claude, chưa nghiệm thu** (02/11/2026, Phiên6). Codex làm. C1/Q233 một commit, chưa push; T1 mới238lượt đạt; K đủ1312bản ghi, đốichiếuT046/D2 đạt. Luật chọn E1+E2, cả3world vàh0,5/1/2; bootstrap518/1000giữE1+E2,403/1000chọnE2+E5. Đã phân tích chuỗi/counterpart, bảng2×2; không xácnhận hiệuchuẩn/cơchếvậtlý/hiệuquảRCA. [Báo cáo](../results/T-047/bao-cao.md), [LOG](../tasks/T-047-khoi-k-luot-2/LOG.md), [promptClaude](../results/T-047/prompt-claude-phien6.txt). Trầntổng8giờ; giờchốt/hash tại manifest.').encode()+nl
    state.write_bytes(b''.join(lines))
    prompt=(out/'prompt-claude-phien6.txt').read_text(encoding='utf-8')
    with (root/'tasks/T-047-khoi-k-luot-2/LOG.md').open('a',encoding='utf-8') as f:
        f.write(f'''\n## Kết thúc triển khai Phiên6 — {stamp}

1. Đã làm: giữ phần hợp lệ, áp đúngC1/Q233/mộtcommit, hồi quy/pilot, đủT1mới238 vàK1312. T1bấtbiến/82R0T046đạt; KduT04652/30đạt; haihashKtrướcD2/nhãn. D2đạt12/12; đủ43cặp×3world, bộchọn1–8/10, hchính1/độnhạy0.5/2, bootstrap1000seed20261102, bảng2×2đủ16×52 vàphụchồihạngđúng. Lựa chọnchính{winner}; bootstrap518E1E2/403E2E5và1mẫuR0giữmãdừng, khôngđổitiêuchí. Đãđọc15cặptríchchuỗi, phânxửquantrọngE1/E2/E3/E5, ca hại/lên/đúng/counterpart; rawAPI298logđơnvị/4ca và3traceđơnvị khớp, E5replay156ca+60nhánhC-e khớp. Các đườngtínhtoánđượcxácđịnh, cơchếvậtlýchung/hiệuchuẩn/hiệuquảđộclập vẫnOPEN. Khôngxem code/test/đồngthuận làchứngminhRCA.
2. Fileđổi: src/m1/cong.pyđúng2hàmC1 vàdòngQ233đãcommit; kếtquả/scripts/tests/runs/báocáo/manifest/prompt trongresultsT047; nốiLOGnày, đúngdòngT047STATE. WHY/SPEC vàmọithayđổicósẵngiữ nguyên. Vi phạm5filepytestcacheđãbáovàMinhduyệtdọn;5fileđãxóasauhash/sao lưu, thưmụcrỗngcòn vìcôngcụchặnRemove-Item 'blocked by policy', khôngđổicáchđểvượtchặn. Khôngcloud/locked/committhêm/push.
3. Kiểm: JUnitT044374/T04516/T04646 vàT047171qua; T1/K/nhãnhash/gates/metađạt. Guardrace47/768trước,0/768sau; giữ11lỗifixturetestvàmọiworker/pilot/candidatecũ. Kiểmhậu xửlýđộclậpđạt ở runs/c1-kiem-hau-xu-ly-001/checks.json: 43N1tínhlạitừtầng, đủ1000mẫu/bộisố, mẫugốc=main,16bảng2×2/mean/tươngtáckhớp. KiểmtheocathấyRR/Hit1/M5giữgiữa3world cho832bản; kênh/khóasốvẫncókhác, khôngmượnPchothếgiớikhác. BảnchẩnđoánCountersaiđãgiữvàdùngcorrected002; khôngsửađápán/phươngpháp. Kiểmcuốiphạmvi/hash/diff đangchạysau báocáonày, chỉghiPASSnếukếtquảthậtđạt.
4. Phầnđạt: phạmvimôtả/kiểmcàiđặt/chọntrêndev/cơchếtínhtoán/cácgiớihạncầnthiếtcủaT047, đềnghịchờphảnbiện. Phầnthiếu: nghĩa vận hành mẫu logcó/mất; giảđịnhkếthừanhânquảE5; vai tròthiếusựkiện/coverageởnhómchưaphânxử; G3gầnhằng/hiệuchuẩn; táchG3D1; non-Pchi tiết chưa lưu; hiệuquảđộclập/RQ3/G3/FlashTicket vàcáctaskkếtiếp. Bootstrapmongmanh,N1tuyệtđốicao, khôngdùngluậttươngđốilàmchứngnhậnan toàn. Không thêmquyếtđịnhnghiêncứu; Minhchưanghiệmthu, taskchưađóng.

Bước tiếp chínhxác: đọcbao-cao.md, manifest.jsonvà runs/ket-phien6-kiem-001/kiem-ban-giao.json cùngreceiptngânsáchchốt; kiểmcácfilebằnghashtrướcdùnglại. Claudeđọcnguồn/code/đầuragốctrướcbáocáo/kếtluận, phảnbiệnđộclậptheo promptbêndưới; quyềnchỉtrảlờitrongchatvìchưacómộttênfilephảnbiệnđượcMinhduyệt. Minhquyếtnghiệmthu/sửa/giaotasktiếp. Khôngchạylạimethod/T1/KhaymởG3/testnếuchưacóđềxuất/duyệtmới. ĐềxuấtnộidungcommitkếtquảsauMinhduyệtriêng: feat(T-047): lưu khối K G3/D1/S1, độ bền và phân tích cơ chế trên dev. MộtcommitC1/Q233đãcó; pushchờduyệtriêng. KhôngtựgửichoClaude.

Lệnh tiếp của chính phiên này: Python ghim -B results/T-047/scripts/kiem_phien6.py --run results/T-047/runs/ket-phien6-kiem-001 --status COMPLETE_PENDING_REVIEW --scoring-read; nếuđạt thì Python ghim -B results/T-047/scripts/chot_ngan_sach_phien6.py. Môi trườnggiữPYTHONPATHghim/PYTHONDONTWRITEBYTECODE1; testsdùngno:cacheprovidervàvùngtạmtrongresults. Lệnhcuốithực/sốphútcuốisẽđượcscriptchốtghibổsung, khôngresetngânsách.

### Prompt Claude — bàn giao kết quả Phiên6, Minh chuyển thủ công

```text
{prompt.rstrip()}
```
''')
    print(json.dumps(dict(report='results/T-047/bao-cao.md',winner=winner,status='COMPLETE_PENDING_REVIEW')))


if __name__ == '__main__':
    main()
