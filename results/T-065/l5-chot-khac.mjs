import fs from 'node:fs/promises';
const base='results/T-065',out=base+'/kiem/003-trinh-duyet',task='tasks/T-065-giao-dien-grafana';
const read=async p=>(await fs.readFile(p,'utf8')).replace(/^\uFEFF/,'');
const json=async p=>JSON.parse(await read(p));
const write=async(p,s)=>fs.writeFile(p,s.trimEnd()+'\n');
const append=async(p,s)=>fs.appendFile(p,'\n\n'+s.trim()+'\n');
const now=new Date().toISOString(),audit=await json(out+'/khac-audit.json');
if(!Object.values(audit.checks).every(Boolean))throw Error('Audit chưa đạt');
for(const file of ['BAN-GIAO-L5.md','codex/L5-prompt-tiep-nhan.md','kiem/003-trinh-duyet/BAO-CAO.md','XONG.md']){
 const dest=file.replace(/\.md$/,'-truoc-audit-khac.md');
 try{await fs.copyFile(base+'/'+file,base+'/'+dest,1);}catch(e){if(e.code!=='EEXIST')throw e;}
}
const auditText=`# Rà nhóm khac trong lớp hiển thị — T-065 L5

Cập nhật ${now}. Chỉ phân tích dữ liệu đã lưu. Không chạy lại M1 hoặc sửa đầu ra.

FACT: khac-audit.json#/inventory có 1.997 dòng ca/service/thao tác trên 22 ca P7, tương ứng 131 khóa service + tên thao tác. Không cộng ba bản thành các mẫu độc lập. Bộ audit kiểm hash dữ liệu L4 trước khi đọc.

Chọn hai ca 5fb8208f (dev2) và a5539fba (T-062) bằng thuật toán phủ tên, không dùng nhãn lỗi, hạng hoặc cờ. Hai luồng raw khớp hash theo manifest gốc. Có 491 span ví dụ phủ đủ 131 khóa tên. Nguồn: khac-audit.json#/sources, /samples, /checks và khac-audit-plan.json.

| Scope raw của span ví dụ | Số khóa service + tên | Thuộc tính quan sát |
|---|---:|---|
| io.opentelemetry.hibernate-6.0 | 68 | kind=1; thread.id, thread.name |
| io.opentelemetry.spring-data-1.8 | 60 | kind=1; code.function, code.namespace, thread.id, thread.name |
| io.opentelemetry.methods | 3 | kind=1; code.function, code.namespace, thread.id, thread.name |

Đầu vào → xử lý → đầu ra: các ví dụ không có messaging.system, db.system/db.system.name hoặc http.*; scope không khớp scheduling/quartz. Hàm xuat-du-lieu.mjs::kind vì thế rơi vào nhánh cuối trả khac. l4-raw.mjs dùng cùng hàm khi bổ sung metadata dev. Cả 491 ví dụ đều tái phân loại thành khac như dữ liệu xuất. Tên như SELECT hoặc Transaction.commit không được dùng để tự gán SQL.

Nhóm khac là nhánh dự phòng của bộ phân loại hiển thị. Nhóm này chứa các scope đủ cụ thể để giải thích loại instrumentation. Nó không đồng nghĩa mất thao tác, thiếu trace, không chấm M1 hoặc service khỏe. Không dùng nhóm này để suy nguyên nhân sự cố. Trạng thái và cờ M1 độc lập với nhãn loai, được giữ nguyên.

CANDIDATE: có thể thêm mô tả scope Hibernate/Spring Data/method bên cạnh khac nếu cần tên dễ đọc hơn. Căn cứ là metadata raw, không suy từ tên hàm. Mặt trái: tăng số nhóm và cần giữ ranh giới giữa span ORM/repository với lời gọi SQL thực. Phương án giữ khac kèm thông tin chi tiết hiện tại vẫn trung thực. Lượt này giữ nguyên nhãn và dashboard; không thêm quyết định thiết kế nghiên cứu.

Giới hạn: đã phủ mọi khóa service + tên hiện thuộc khac bằng ví dụ đã lưu. Chưa đọc lại mọi span của toàn bộ 22 ca để khẳng định mọi lần xuất hiện có cùng scope/thuộc tính. Hai raw stream được đọc hết để kiểm hash; chỉ các span ví dụ được phân tích metadata chi tiết. Bằng chứng đủ cho phần rà nhóm của P3, chưa xác nhận lợi ích của nhãn mới. Không cần chạy lại toàn bộ export/M1. Span link vẫn chưa có dữ liệu và chưa hỗ trợ.

Lệnh: node results/T-065/l5-khac-audit.mjs. Dùng lại khac-audit.json ở lượt tiếp, không chạy lại chỉ vì đổi phiên.`;
await write(out+'/khac-audit.md',auditText);
const remaining=`1. Kiểm Chrome sau UI-04: bảng panel 7/phát lại, panel 28/snapshot, panel 31–35 và ảnh dòng cuối panel 24. Dùng lại API 12/12 và dữ liệu đã khớp. Không chạy lại API hoặc M1 khi nguồn không đổi.
2. V041/2e2a5541: bấm chính → phát lại → chính sau UI-04, đọc đủ bảng hai cột và chụp ảnh. Dev V041/19b17e22: xác nhận chỉ có giới hạn chưa cấp đáp án. Kết quả T-062 6/6 trước sửa giữ làm lịch sử, không thay ảnh sau sửa.
3. Query Inspector cho 10 quan sát lịch sử e8661e0a: P7/event-service panel 31/32/33; V032/event-service panel 31/32/33; V041/api-gateway panel 31/32/33/35. Có 7 tổ hợp service/panel duy nhất; cửa sổ [1794444870000,1794445469999] ms. Lấy biểu thức từ doi-chieu-rong-snapshot.json. Lưu request/response hiện tại và ảnh. Giữ 10 lượt cũ loại (iii) nếu thiếu request/response đúng thời điểm cũ; không suy nguyên nhân lịch sử từ phép kiểm hiện tại.
4. G-c vẫn chờ bản M1-FT đề xuất cuối theo SPEC và điều phối. Không tự nâng V032 hoặc V041 thành bản cuối.`;
const latest=`## ${now} — rà khac xong, quyền Chrome chưa khả dụng

Lượt 08:39 đã đọc prompt/checkpoint, chuyển status dang_chay và ghi mở LOG, rồi bị ngắt trước thao tác UI. Lượt tiếp có @Chrome đã đọc lại trạng thái và thử ba đường trên cùng browser 3: binding cũ, getTab(217961015), listTabs. Cả ba trả Local browser access is unavailable for this chat trước khi truy cập trang. Đã dừng UI sau ba lần; không đổi cơ chế điều khiển. Bằng chứng: kiem/003-trinh-duyet/ket-noi-Chrome-tiep-UI04.json. Timestamp là giờ lập biên bản, không giả giờ riêng từng lệnh.

OPEN: chưa xác định vì sao quyền điều khiển local browser của chat không khả dụng. Cần một kết nối Chrome hoạt động để tiếp phần UI. SSH, listener và máy hoạt động không phân xử nguyên nhân cấp quyền chat. Không ghi lỗi này thành lỗi Grafana hoặc kết quả khoa học.

Rà khac đã xong: 1.997 dòng, 131 khóa tên; 491 span ví dụ từ hai raw stream khớp hash, phủ 131/131 tên. Scope Hibernate 68, Spring Data 60, methods 3. Xem khac-audit.md/json. Không đổi nhãn, hạng, cờ hoặc M1. P3 đạt phần rà và kiểm message; span link giữ chưa hỗ trợ vì chưa có dữ liệu.

Không có thao tác Chrome trong lượt này. Dùng lại 66 trang, 162 link, 72 thao tác, 36 service và 36 graph. Pair 18 đã xong. Phần còn lại:

${remaining}

Máy cuối 08:42:36Z: STOP=false, runner3=0, 310.9 MiB/768 MiB, restart=0, cùng StartedAt 04:15:16Z. Listener 13000 vẫn ở PID 24712; tunnel riêng session 30562 giữ để tiếp. Không có job kiểm/M1 nền. Không đổi file máy chủ, src/docs/T-064 hoặc STATE; chỉ results/T-065 và nối LOG.

Đề nghị tiếp phần Chrome khi kết nối hoạt động, dùng tab bàn giao hoặc mở tab riêng theo URL trong status. API chỉ trả lời phần dữ liệu, không thay bằng chứng ảnh/bấm còn thiếu. Không nghiệm thu G-a/G-c hoặc đóng RQ5.`;
await append(base+'/CHECKPOINT.md',latest);
await append(out+'/BAO-CAO.md',latest);
let handoff=await read(base+'/BAN-GIAO-L5.md');
handoff=handoff.replace(/^# Bàn giao L5 — .*$/m,'# Bàn giao L5 — '+now)
 .replace('rà khac còn cần đối chiếu P3','rà khac đã xong tại khac-audit.json')
 .replace('| P3 | Một phần |Message có cờ qua3 bản đã kiểm; rà nhóm khac theo L4; span link chưa có dữ liệu |','| P3 | Đạt phần rà/kiểm | Message qua ba bản đã kiểm; khac-audit phủ 131 tên bằng 491 ví dụ. Span link chưa có dữ liệu, giữ chưa hỗ trợ. |')
 .replace('4. Rà nhóm khac theo P3/L4 nếu còn trong yêu cầu, phân biệt kiểu thao tác dựa thuộc tính span. Span link chưa có dữ liệu, giữ chưa hỗ trợ.','4. Rà khac đã xong. Dùng lại khac-audit.json/md; không đọc lại raw hoặc đổi nhãn. Span link giữ chưa hỗ trợ.');
await write(base+'/BAN-GIAO-L5.md',handoff+'\n\n'+latest);
await write(base+'/XONG.md',`# T-065 L5 — một phần, chờ kết nối Chrome

Dùng lại 66 trang, 162 link đủ kiểm, 72 thao tác, 36 service và 36 graph. Editor Loki đã đọc lại; luồng LOW_SUPPORT → chi tiết đạt 7/7. Rà khac hoàn tất: 1.997 dòng/131 tên, 491 span ví dụ từ hai nguồn raw khớp hash. Không đổi nhãn hoặc M1.

Ba lần truy cập Chrome sau tin có @Chrome đều báo quyền local browser không khả dụng. Lỗi và thứ tự ở kiem/003-trinh-duyet/ket-noi-Chrome-tiep-UI04.json. Đã dừng UI. Máy/tunnel hoạt động, không restart.

Còn kiểm Chrome UI-04, phát lại, Inspector và ảnh cuối panel 24. G-c phụ thuộc bản cuối. Chưa nghiệm thu. Tiếp theo BAN-GIAO-L5.md, CHECKPOINT.md mục cuối và codex/L5-prompt-tiep-nhan.md. Không chạy lại mẫu đã đạt.`);
await write(base+'/codex/L5-prompt-tiep-nhan.md',`Đọc AGENTS.md, tiếp T-065: Codex người làm, Claude phản biện. Đọc results/T-065/codex/L5-brief.md, CHECKPOINT.md mục cuối, BAN-GIAO-L5.md và prompt này. Dùng Chrome đã đăng nhập của Minh qua @Chrome. Chỉ ghi trong quyền L5; không ghi STATE/src/T-064/docs, không commit/push.

HIỆN TRẠNG ${now}: usage đã hồi, nhưng Chrome trả Local browser access is unavailable for this chat qua ba lần: binding cũ, getTab(217961015), listTabs browser 3. Đã dừng UI, không đổi cơ chế điều khiển. Bằng chứng: kiem/003-trinh-duyet/ket-noi-Chrome-tiep-UI04.json. Chưa xác định nguyên nhân quyền chat. Thử kết nối mới khi @Chrome được cấp lại; không lặp nhiều vòng cùng lỗi.

DÙNG LẠI, KHÔNG CHẠY LẠI: 66/66 trang (22 mỗi bản), 162/162 link đủ kiểm (72 Tempo/54 Loki/36 Prometheus), 72 thao tác, 36 service, 18 cặp và 12 lần đổi bản. Editor Loki V032/00eaea92 đã đọc đạt. Graph 36 đủ bằng chứng, 54 ảnh/khung: hai ảnh cũ và 34 graph bổ sung. Node/cạnh/màu/radius khớp; hợp khung không thiếu node. sau-tien-do.json pair18 đã xong; không quay pair13. Không chạy M1/export/API 12 slot lại nếu nguồn không đổi.

Rà khac đã XONG. Dùng lại khac-audit.json/md; không đọc raw lại. Có 1.997 dòng/131 tên và 491 span ví dụ phủ 131/131 từ hai raw khớp hash. Scope Hibernate 68, Spring Data 60, methods 3. Quy tắc hiển thị trả khac, không đổi nhãn/hạng/cờ. Đây không là bằng chứng thiếu trace hoặc lợi ích của nhãn mới. Span link chưa có dữ liệu, giữ chưa hỗ trợ.

Tab bàn giao 217961015 ở V041/19b17e22/event-service/GET (LOW_SUPPORT); URL đầy đủ trong L5-trang-thai.json. Nếu tab mất, mở tab mới riêng và giữ tab Minh. Khởi tạo L5Browser mới từ l5-browser.mjs; l5-cua-adapter.mjs xử lý chọn đúng text và chờ link khớp. Không dùng binding cũ, không cần L5Deep.advance nữa. Menu graph mở chi tiết trong tab mới: không focus panel24 ở tab View graph cũ.

Tunnel riêng: session30562/PID24712, bind127.0.0.1:13000 đến Grafana exp-obs. Kiểm Get-NetTCPConnection -LocalPort 13000 -State Listen trước khi tạo thêm. Máy cuối08:42:36Z: STOP=false, runner3=0, 310.9MiB/768MiB, restart0, cùng StartedAt04:15:16Z. Chạy & results/T-065/l5-may.ps1 -Nhom 'L5 UI04 con lai' trước nhóm nặng và tôn trọng hai STOP. Không đọc khóa/env hoặc in credential.

VIỆC CÒN LẠI:
${remaining}

Ảnh ui04-low-support-detail.png cắt dòng Giới hạn metric cuối, DOM đủ chín dòng. Chỉ bổ sung ảnh View panel24 hoặc cuộn đến dòng cuối, không kiểm lại số. Giữ mọi ảnh cũ và lượt lỗi. Graph lớn đã có ảnh pan, không chụp lại. Nếu công cụ trả JPEG, lưu.jpg và tạo PNG mới, không ghi đè.

Trước khi làm đổi status dang_chay, kiểm hash đúng file theo manifest. Lưu từng bước và checkpoint. Sau cùng: node results/T-065/l5-tong-hop.mjs; rồi manifest, kiểm diff/tập file và soạn prompt Claude chuẩn từ docs/review-prompt.md. L5 vẫn một phần, chưa nghiệm thu. Không đóng RQ5 hoặc tự chọn bản cuối.`);
await append(out+'/loi-va-sua.md',`## ${now} — quyền Chrome của chat chưa khả dụng

Ba lần thử trước thao tác trang cùng lỗi local browser access. Đã dừng sau ba lần; không có sửa UI hoặc quan sát mới trên trang. Chưa xác định nguyên nhân. Xem ket-noi-Chrome-tiep-UI04.json.

Rà khac cục bộ đạt; không thay nhãn hoặc phương pháp. Không chạy lại API/M1. Giữ 10 panel loại (iii) lịch sử và toàn bộ ảnh/DOM cũ. Phần Chrome UI-04/phát lại/Inspector chưa làm được.`);
const template=(await read('docs/review-prompt.md')).replaceAll('\r\n','\n');
const block=h=>{const v=template.split(h+'\n')[1]?.match(/\x60\x60\x60text\n([\s\S]*?)\n\x60\x60\x60/)?.[1];if(!v)throw Error(h);return v;};
const values=['T-065, L5; tasks/T-065-giao-dien-grafana/SPEC.md và results/T-065/codex/L5-brief.md','soát kết quả','Chiến dịch M1-FlashTicket, nhánh giao diện sau G4','Codex người làm; Claude người phản biện và điều phối','tasks/T-065-giao-dien-grafana/SPEC.md, LOG.md; results/T-065/codex/L5-brief.md; results/T-064/ban-xuat/chi-muc-ban.json','tasks/T-065-giao-dien-grafana/REVIEW.md và LOG.md','results/T-065/BAN-GIAO-L5.md, CHECKPOINT.md, manifest.json, kiem/003-trinh-duyet/, l5-khac-audit.mjs, các script l5-* và grafana-l4/','Chỉ đọc và nhận xét trong chat; ghi file phản biện khi Minh cho phép đúng vị trí theo SPEC'];
let i=0;const common=block('## Prompt chung').replace(/<[^>]+>/g,()=>values[i++]);if(i!==values.length)throw Error('Prompt fields');
const prompt=[common,block('### Soát kết quả'),block('### G4 — Kết quả')].join('\n\n');await write(base+'/prompt-ban-giao.md',prompt);
const state=await json(base+'/codex/L5-trang-thai.json');
Object.assign(state,{trang_thai:'mot_phan',cap_nhat:now,buoc:'cho_Chrome_UI04_khac_audit_xong',ly_do:'Ba lần truy cập Chrome trong chat đều bị chặn trước thao tác trang; rà khac đã hoàn tất. Chi tiết trong BAN-GIAO-L5.md.',khac_audit:{rows:1997,names:131,samples:491,raw_sources:2,passed:true}});
await write(base+'/codex/L5-trang-thai.json',JSON.stringify(state,null,2));
await append(task+'/LOG.md',`## L5 — ${now} — Codex, laptop Minh, người làm — rà khac xong, Chrome bị chặn

1. Đọc lại prompt/checkpoint sau ngắt. Thử ba đường Chrome rồi dừng UI vì cùng lỗi trước truy cập trang. Rà 1.997 dòng khac/131 tên, 491 span ví dụ từ hai raw khớp hash, phủ 131/131. Lần theo raw → kind → nhãn khac. Không sửa nhãn/M1. Dùng lại mẫu 66 trang/162 link/36 graph.
2. File mới/đổi chỉ results/T-065 và nối LOG: script audit, kết quả, biên bản kết nối, báo cáo/checkpoint/status, hai prompt và manifest. Không đổi máy chủ, src/docs/T-064/STATE. Không commit/push.
3. Cú pháp script audit đạt; hai raw hash khớp, ba check audit đạt. Máy STOP=false, runner3=0, 310.9MiB/768MiB, restart0. Kiểm cú pháp/diff/hash cuối thực hiện ngay sau phần chốt. Mẫu UI cũ không đổi trong lượt.
4. P3 đạt phần rà; G-a và các mục UI-04 bị kết nối chặn, G-c chờ bản cuối. T-065 thêm bằng chứng giao diện DT18, không khẳng định lợi ích RCA hoặc đóng RQ5. Không thêm/đổi quyết định nghiên cứu. Đề nghị tiếp phần thiếu khi Chrome hoạt động, không thay bằng API hoặc coi brief đã xong.

Bước tiếp: đọc BAN-GIAO-L5/CHECKPOINT mục ${now}, thử kết nối @Chrome, kiểm máy, rồi chỉ làm UI-04/phát lại/Inspector. Lệnh cuối đã chạy: node results/T-065/l5-khac-audit.mjs. Lệnh chốt cuối: node results/T-065/l5-tong-hop.mjs manifest. Tunnel PID24712/session30562 giữ; không job kiểm nền. Đề xuất commit khi có duyệt riêng: test(t065): bổ sung audit khac và bàn giao L5; chưa commit/push.

### Prompt độc lập cho Claude

${prompt}`);
console.log(JSON.stringify({utc:now,audit_checks:audit.checks,status:'mot_phan',connection_attempts:3}));
