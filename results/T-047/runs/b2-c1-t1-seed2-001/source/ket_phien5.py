"""Ghi báo cáo trung thực ở điểm dừng T1; không sửa nguồn ngoài quyền."""
import hashlib
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET
from datetime import datetime,timedelta,timezone
from pathlib import Path
import adapter_t047 as ad
import tep_pha1


def main():
    stamp=datetime.now(timezone(timedelta(hours=7))).isoformat(timespec='seconds')
    root=ad.ROOT;out=ad.OUT
    t1=json.loads((out/'t1.json').read_text(encoding='utf-8'))
    diag=json.loads((out/'runs/t1-xao-dieu-tra-002/summary.json').read_text(encoding='utf-8'))
    proposal=json.loads((out/'runs/de-xuat-c1-003/kiem-ung-vien.json').read_text(encoding='utf-8'))
    junit=ET.parse(out/'runs/hoi-quy-cuoi-phien5-001/junit.xml').getroot()
    total=sum(int(x.get('tests',0)) for x in junit.iter('testsuite'))
    lines=[]
    for x in diag:
        if x['oid']=='dev-03d4910932':continue
        a,b=x['versions']['original'],x['versions']['shuffled']
        lines.append(f"| `{x['oid']}` | {a['b']} → {b['b']} | {a['p']:.12g} → {b['p']:.12g} |")
    table='\n'.join(lines)
    correction=f'''# C1 — T1 không bất biến theo xáo hàng

Trạng thái: **CHẶN bước 3 trở đi; chưa sửa src, chưa duyệt ứng viên.** Ghi {stamp}.

## Quan sát và chuỗi bằng chứng

T1 đã đủ 238 lượt cấu hình–ca chính. Seed 0/1/2 trùng byte. Xáo hàng lệch đúng hai trường `p_len` trên 52 ca; các trường còn lại, gồm cờ, tầng và thứ hạng, trùng. Nguồn: `t1.json#/bat_bien`; `runs/b2-t1-xao0-001/so-xao-chan-doan-001.json#/ca_lech` và hai tệp `different-*.json`.

Cả hai trường thuộc `metric|ts-admin-travel-service_latency-90`. Các cặp (mốc, giá trị) N/A giữ nguyên, chỉ hoán vị thứ tự. Raw đã kiểm hash qua allowlist; chẩn đoán không đọc nhãn chấm.

| Ca | Độ dài khối b | p gốc → p xáo |
|---|---|---|
{table}

Nguồn số: `runs/t1-xao-dieu-tra-002/summary.json` và từng ca, `#/versions/original`, `#/versions/shuffled`. N có hai mức 0,235 và 0,23500000000000004. Thứ tự thêm ô vào dict theo thứ tự hàng đi qua `o_1s`; `tu_tuong_quan` dùng `list(o.values())` và cộng các cặp theo thứ tự dict. Sai số trung bình/phương sai trên chuỗi gần hằng khuếch đại khi chuẩn hóa thành rho; rho làm đổi b, số khối, rồi không gian chia khối và p. Sắp lại theo thời gian phục hồi b/p gốc ở cả hai ca. Ca đối chiếu cùng đơn vị `dev-03d4910932` có biến thiên rõ hơn: b và p không đổi giữa hai thứ tự. Xem `#/versions/sorted_shuffled` và ca đối chiếu trong cùng thư mục.

**Phân loại đã xác nhận:** lỗi tất định số học/thứ tự xử lý trong cài đặt G3, tại `src/m1/cong.py` hàm `o_1s`, `tu_tuong_quan`. Không có bằng chứng adapter đổi tập mẫu: chẩn đoán kiểm cùng cặp mẫu và ghép mốc đúng. Không phải đổi ngẫu nhiên seed; ba seed đã trùng đầu ra và G3 khóa seed theo mã đơn vị/hướng. Không nới tiêu chí T1 vì hiện cờ/hạng chưa đổi: p/b đã thay đổi thực sự và SPEC yêu cầu bất biến.

**OPEN riêng:** ý nghĩa thống kê và độ ổn định của G3 trên chuỗi gần hằng ở mức độ chính xác máy. Sửa thứ tự không xác nhận hiệu chuẩn G3, không giải quyết câu hỏi có nên đặt điều kiện gần hằng. Không tự thêm epsilon hoặc sàn phương sai.

## Đề xuất sửa tối thiểu — chưa áp dụng

Patch cụ thể: `runs/de-xuat-c1-003/de-xuat.patch`; bản nguồn dự kiến `cong-proposed.py`. Chỉ hai hàm:

1. `o_1s`: gom mẫu theo ô; tổng `math.fsum` trên dãy giá trị đã sắp; xuất ô theo thời gian tăng (chỉ số ô N giảm).
2. `tu_tuong_quan`: mảng và các cặp rho dùng cùng thứ tự chỉ số ô đã khóa, thay vì thứ tự chèn dict.

Giữ công thức trung bình/phương sai/rho, điều kiện phương sai bằng 0, ngưỡng rho, giới hạn b, số hoán vị, seed, cửa sổ, G3/D1/S1, h, ma trận và luật chọn. Tổng bù tránh mất số hạng nhỏ khi nhiều mẫu chung một ô. Không làm tròn dữ liệu hoặc đặt ngưỡng gần hằng.

Ứng viên riêng đã qua 3 phép kiểm: hoán vị chuỗi gần hằng; nhiều mẫu chung ô với đáp án tổng biết trước; điều kiện ít ô/phương sai bằng 0. Đã kiểm bản patch trong namespace tách rời trên hai đơn vị lỗi và một đơn vị đối chiếu: cùng cặp mẫu, b/p bất biến và khớp bản gốc hiện lưu. Nguồn: `runs/ung-vien-tat-dinh-002/junit.xml`, `runs/de-xuat-c1-003/kiem-ung-vien.json`. **Chưa kiểm tích hợp toàn chuỗi hoặc mọi đơn vị/dev. Không gắn ứng viên vào M1 đang dùng.** `src` vẫn nguyên byte.

## Bản đồ ảnh hưởng xin Minh duyệt

| File/phạm vi | Thay đổi đề nghị | Tác động và lý do |
|---|---|---|
| `src/m1/cong.py` | Áp đúng patch C1 ở trên | Mọi phép G3 có thể chịu ảnh hưởng số học; mặc định G0/D0 không gọi tệp này. Cần hồi quy và chạy lại bằng code có đính chính. |
| `results/T-047/` | Giữ mọi lượt; bổ sung test, metadata hash nguồn thực, lượt mới, T1 và K/hậu xử lý | Không gắn số cũ với code đã sửa; không dùng lại kết quả chỉ vì từng PASS. Phần không phụ thuộc sửa được giữ sau kiểm hash. |
| `tasks/T-047-khoi-k-luot-2/LOG.md` | Chỉ nối lời duyệt thật, phạm vi C1, hash, kiểm và bàn giao | Giữ lịch sử và căn cứ đổi nguồn chạy từ c298188e sang c298188e cộng patch C1. |
| Dòng T-047 trong `docs/STATE.md` | Cập nhật bước làm theo kết quả thật | Không tự nghiệm thu hoặc đóng task. |
| `docs/DECISIONS.md` | Đề nghị một dòng Q-233, nếu mã còn trống, ghi nguyên văn lời duyệt thật và phạm vi C1/ngân sách Minh quyết | Đây là quyền bổ sung cần duyệt riêng; chưa ghi dòng này. Không sửa quyết định cũ. |

Không sửa SPEC đã khóa, WHY hoặc manifest T-043–T-046. Đề nghị duyệt đính chính cài đặt C1 làm ngoại lệ nguồn code: nguồn gốc c298188e cộng patch đã duyệt, không gọi là byte nguyên bản c298188e. Nguồn src của T-046 cũ kiểm bằng `git show c298188e`, kết quả cũ vẫn kiểm theo manifest cũ; nguồn mới và patch ghi hash tại T-047. Metadata mới phải ghi rõ nguồn thực, không chỉ mang revision cũ.

Sau khi được duyệt: kiểm cài đặt mặc định/adapter và ứng viên đã tích hợp; chạy thử đo thời gian/RAM; chạy lại phần T1 bị phụ thuộc vào G3 đã sửa rồi mới K. Đối chiếu T-046 phải giải thích lệch do C1 nếu có, không tự đổi tiêu chí hoặc coi mọi lệch là hợp lệ. Nếu xuất hiện mâu thuẫn SPEC hoặc cần đổi công thức/ma trận/tham số, dừng phần phụ thuộc trình Minh.

Chi phí dự báo CHƯA KIỂM: sửa/hồi quy/đo lại khoảng 15–25 phút; T1 khoảng 60–85 phút; K khoảng 2–3 giờ; cơ chế/độ bền/độ nhạy/bảng/báo cáo khoảng 45–75 phút. Tổng còn lại khoảng 4–5,5 giờ nếu không có lỗi mới; có thể vượt phần còn lại của trần 7 giờ. Đề nghị Minh quyết quyền sửa và, nếu muốn duyệt cùng gói chạy tiếp, **trần tổng 8 giờ**, tính cả mọi lượt đã chạy, không phải thêm 8 giờ mới. Chưa tự nới trần. Nếu chỉ duyệt sửa và giữ 7 giờ, phải đo/dự báo lại trước lượt nặng; dự báo vượt thì dừng.

## Phần nghiên cứu và nghĩa vụ còn lại

Đã có bằng chứng cài đặt về bất biến hash seed và một lỗi theo thứ tự hàng, Đ5 D1, QT5 và đối chiếu R0 thật/C-e với T-046. Chưa có K, D2 mới, lựa chọn khối, bootstrap hay bảng 2×2. Không trả lời xong câu hỏi chọn thành phần, RQ3 hoặc lợi ích RCA. Lỗi cài đặt này không tự chứng minh phương pháp sai về hiệu quả, cũng không được bỏ vì hạng hiện chưa đổi.
'''
    (out/'dinh-chinh-cai-dat.md').write_text(correction,encoding='utf-8')
    report=f'''# T-047 — báo cáo Phiên 5 tại điểm dừng T1

Trạng thái: **chưa hoàn tất; dừng trước khối K để trình C1 và quyền sửa src**. {stamp}.

- Đã tự rà SPEC với DT18, hướng dẫn của cô, MRP và nguồn quyết định; không mặc định SPEC đúng. Bước0/manifest hợp lệ được dùng lại. Pilot hai dataset đạt; thực hiện đủ T1, không đọc nhãn chấm.
- T1: 52 ca × 3 seed, 52 ca xáo hàng, 30 cửa sổ giả. Seed1/2 trùng seed0; xáo trượt tại hai p-value. Đối chiếu {len(t1['doi_chieu_T046'])} tóm tắt R0 thật/C-e với bước10 T-046 không lệch. Đ5 D1 có {t1['D5_tong']['so_don_vi']} đơn vị hợp lệ, {t1['D5_tong']['so_doi']} đổi cờ khi T lệch±1%. Nguồn: `t1.json#/bat_bien`, `#/doi_chieu_T046`, `#/D5_tong`.
- Hồi quy T-047 cuối phiên: {total}/{total} qua trên dữ liệu giả, không thay kết quả T1. JUnit: `runs/hoi-quy-cuoi-phien5-001/junit.xml`. Bộ cũ và helper bước0 giữ nguyên hash; nguồn chứng cứ ở `kiem-helper.json`, `runs/phien5-tiep-nhan-001/kiem-tiep-nhan.json`.
- QT5: đọc 12 ca tỷ trọng một nhóm>90%, đếm đơn vị/cổng/trạng thái và so ca cùng dataset không cờ; chưa thấy lỗi bỏ nhóm đầu vào. Đây là giải thích tỷ trọng đã ghi, không xác nhận bất thường thật. `runs/b2-t1-seed0-001/qt5-phan-xu.json` và LOG.
- Usage ngắt phần soạn/rà, tiến trình T1 vẫn chạy. Seed2-001 gặp một guard trước nạp; giữ hai ca hoàn tất và dùng lại trong seed2-002 sau kiểm hash/config/seed. Nguồn lỗi guard cụ thể còn OPEN; nó chưa tạo bản ghi phương pháp sai. Mọi ca T1 cuối đã đủ. Không gọi lỗi đó là đã được giải thích hoàn toàn.
- C1 có chuỗi raw → thứ tự tổng → trung bình/phương sai/rho → b → p, kèm đối chiếu. Chi tiết, patch chưa áp dụng và bản đồ ảnh hưởng ở [đính chính](dinh-chinh-cai-dat.md). Không sửa src, h, ma trận hoặc luật chọn.

Phần đã đạt: kiểm cài đặt R0 trên dev và chẩn đoán lỗi tất định thật. Phần chưa đạt: tiêu chí T1 bất biến, K/D2/chọn khối/cơ chế khối/độ bền/độ nhạy/bảng2×2. DT18-NV2/NV3 và MRP P6 chỉ được hỗ trợ ở phần kiểm cài đặt; chưa có bằng chứng chọn khối mới hay hiệu quả RCA. Những nghĩa vụ của task(2), task(3), T4/T4b mới và RQ3/G3 giữ OPEN theo SPEC.

File đổi: chỉ `results/T-047/`, nối LOG và dòng T-047 của STATE. Giữ mọi thay đổi có sẵn; chưa sửa src/SPEC/WHY/DECISIONS, chưa commit/push. Đề xuất commit sau khi Minh duyệt phạm vi và xử lý điểm chặn: `feat(T-047): thêm driver, T1 và chẩn đoán bất biến G3`; chưa thực hiện.
'''
    (out/'bao-cao.md').write_text(report,encoding='utf-8')
    paths=[out/'runs'/name for name in ['b2-t1-seed0-001','b2-t1-seed1-001','b2-t1-seed2-002','b2-t1-xao0-001','b2-t1-ce-001']]
    hashes=tep_pha1.ghi_log(paths)
    with (out/'so-lan-nhin.jsonl').open('a',encoding='utf-8') as f:
        f.write(json.dumps(dict(time=stamp,session=5,kind='T1_khong_nhan_va_chan_doan',
            sources=['t1.json','runs/b2-t1-xao0-001/so-xao-chan-doan-001.json','runs/t1-xao-dieu-tra-002',
                     'runs/b2-t1-seed0-001/qt5-phan-xu.json','runs/de-xuat-c1-003'],
            labels_read=False,decision='STOP trước K; chỉ đề xuất C1, chưa áp dụng'),ensure_ascii=False)+'\n')
    # Chỉ thay một dòng STATE, giữ nguyên byte các dòng khác.
    p=root/'docs/STATE.md';ls=p.read_bytes().splitlines(keepends=True);ids=[i for i,x in enumerate(ls) if x.startswith(b'- **T-047 ')]
    assert len(ids)==1;i=ids[0];nl=b'\r\n' if ls[i].endswith(b'\r\n') else b'\n'
    ls[i]=('- **T-047 — chạy khối K lượt thứ hai:** **dừng trước K: T1 xáo hàng trượt, chờ Minh duyệt C1/quyền sửa src** (02/11/2026, Phiên 5). Codex làm, Claude phản biện. Đủ T1; ba seed trùng hash, xáo lệch hai p-value; cờ/hạng hiện không đổi. Đã lần theo lỗi thứ tự số học G3, chuẩn bị patch chưa áp dụng; 152/152 test giả qua không thay T1. Usage không làm mất đầu ra; mọi lượt và hai ca seed2 dùng lại được giữ. Chưa đọc nhãn chấm/chạy K/chọn khối. [Báo cáo](../results/T-047/bao-cao.md), [đề xuất C1](../results/T-047/dinh-chinh-cai-dat.md), [LOG](../tasks/T-047-khoi-k-luot-2/LOG.md).').encode()+nl
    p.write_bytes(b''.join(ls))
    # Prompt chép nguyên các khối; chỉ điền thông tin trung tính.
    template=(root/'docs/review-prompt.md').read_text(encoding='utf-8')
    def block(header):return template.split(header,1)[1].split('```text\n',1)[1].split('\n```',1)[0]
    common=block('## Prompt chung')
    values=['T-047; tasks/T-047-khoi-k-luot-2/SPEC.md', 'soát kết quả', 'P6, chuẩn bị G3',
        'Codex làm; Claude phản biện',
        'SPEC T-047; docs/STATE.md; docs/WHY.md; docs/DECISIONS.md; git diff từ c298188e; results/T-047/bao-cao.md; results/T-047/dinh-chinh-cai-dat.md',
        'LOG T-047 theo thứ tự thời gian; các nhận xét trong chat Minh chuyển kèm nếu có',
        'src/m1, src/m1_danh_gia tại c298188e; manifest T-043–T-046; results/T-047/manifest.json; scripts/tests/runs của T-047; patch tại runs/de-xuat-c1-003; môi trường và lệnh trong LOG và command.json/JUnit từng lượt',
        'chỉ trả lời trong chat']
    fields=re.findall(r'<[^>\n]+>',common)
    assert len(fields)==len(values),(fields,len(values))
    for key,value in zip(fields,values):common=common.replace(key,value,1)
    prompt=common+'\n\n'+block('### Soát kết quả')+'\n\n'+block('### G3 — Khóa thiết kế trước khi mở test')
    (out/'prompt-claude-phien5.txt').write_text(prompt+'\n',encoding='utf-8')
    with (root/'tasks/T-047-khoi-k-luot-2/LOG.md').open('a',encoding='utf-8') as f:
        f.write(f'''\n### Kết thúc Phiên 5 tại điểm chặn — {stamp}

1. Đã làm: tiếp sau usage, giữ kết quả hợp lệ, hoàn tất 238 lượt T1 chính và pilot; tự rà code/nguồn, helper/adapter/driver, Đ5 D1, kiểm trung gian, đối chiếu T-046 và chẩn đoán C1. T1 không đạt bất biến xáo hàng; dừng trước K. Không thêm hoặc đổi quyết định nghiên cứu.
2. File đổi: scripts/tests/runs, kiem-helper giữ nguyên, t1.json, so-lan-nhin.jsonl, dinh-chinh-cai-dat.md, bao-cao.md, prompt-claude-phien5.txt và manifest/kiểm bàn giao trong results/T-047; chỉ nối LOG này, chỉ dòng T-047 trong STATE. Không sửa src/SPEC/WHY/DECISIONS hoặc dữ liệu; giữ các thay đổi có sẵn. Không cloud/commit/push.
3. Kiểm: hash cũ và nguồn bước0 khớp; seed0/1/2 trùng byte; R0 thật/C-e khớp {len(t1['doi_chieu_T046'])} tóm tắt T-046; xáo lệch đúng2 trường p ở2ca. Đ5 D1 {t1['D5_tong']['so_don_vi']} đơn vị, {t1['D5_tong']['so_doi']} đổi quyết định. Cuối phiên {total}/{total} test giả qua; ứng viên C1 riêng qua3 test và3 đơn vị thật, chưa tích hợp. Lượt lỗi/test trượt/các bản patch trước đều giữ. Báo cáo và đính chính chứa con trỏ nguồn; không coi test qua là T1 qua.
4. OPEN/chờ Minh: quyền sửa src C1 và ngoại lệ nguồn code c298188e cộng patch, dòng Q-233 nếu duyệt; quyết ngân sách vì chạy lại T1/K có thể vượt phần còn lại trần7giờ. Đề nghị trần tổng8giờ, chưa nới. Lỗi guard duy nhất trước nạp còn chưa giải thích cụ thể. Ý nghĩa G3 trên chuỗi gần hằng chưa xác nhận. Chưa có K, D2 mới, chọn khối, cơ chế khối, bootstrap, độ nhạy hay2×2; không trả lời xong RQ3, hiệu chuẩn hoặc hiệu quả RCA. Hai agent hỗ trợ chỉ là người làm phụ, chưa có phản biện chính thức của Claude.

Bước tiếp theo chính xác: đọc báo cáo/đính chính C1 và patch runs/de-xuat-c1-003/de-xuat.patch; chờ Minh duyệt phần ngoài quyền. Không chạy K với T1 đang trượt. Nếu được duyệt, áp đúng patch src, cập nhật metadata nguồn T-047 theo hash code thực và ghi đúng lời duyệt/phạm vi; giữ mọi kết quả cũ. Kiểm mặc định/hồi quy và pilot đo lại; kiểm dự báo trong trần Minh cho phép trước chạy T1 mới, rồi K và các bước còn lại nếu đạt. Không tự thêm epsilon/sàn phương sai hoặc đổi G3/D1/S1/h/ma trận/luật chọn. Nguồn T-046 cũ kiểm src bằng git show c298188e khi C1 đã được phép; không sửa manifest cũ. Chưa có quyền đổi tiêu chí so T-046 nếu sau sửa vẫn lệch chưa giải thích.

Lệnh kiểm cuối: scripts/kiem_ket_phien5.py (kiểm phạm vi/hash/diff/JUnit, manifest và dừng tiến trình; sẽ ghi output sau mục này). Mọi tiến trình phương pháp đã dừng sau T1; không có tự động chạy K. Nội dung commit đề xuất sau khi Minh duyệt phạm vi: feat(T-047): thêm driver, T1 và chẩn đoán bất biến G3. Chưa commit/push.

### Prompt Claude — bàn giao Phiên 5, Minh chuyển thủ công

```text
{prompt}
```
''')
    print(json.dumps(dict(status='STOP_C1',T1_PASS=t1['PASS'],tests=total,hashes_logged=len(hashes))))


if __name__=='__main__':main()
