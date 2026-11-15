import fs from 'node:fs/promises';

const base = 'results/T-065';
const task = 'tasks/T-065-giao-dien-grafana';
const report = `${base}/kiem/003-trinh-duyet`;
const stamp = new Date().toISOString();
const read = async file => (await fs.readFile(file, 'utf8')).replace(/^\uFEFF/, '');
const write = (file, text) => fs.writeFile(file, text.trimEnd() + '\n');
const append = (file, text) => fs.appendFile(file, '\n\n' + text.trim() + '\n');
const archivedPrompt = `${base}/codex/prompt-ban-giao-L4.md`;
try { await fs.copyFile(`${base}/prompt-ban-giao.md`, archivedPrompt, 1); } catch (error) { if (error.code !== 'EEXIST') throw error; }

const template = (await read('docs/review-prompt.md')).replaceAll('\r\n', '\n');
function section(heading) {
  const content = template.split(heading + '\n')[1];
  const block = content?.match(/```text\n([\s\S]*?)\n```/)?.[1];
  if (!block) throw Error(`Thiếu khối prompt ${heading}`);
  return block;
}
const values = [
  `T-065, L5. ${task}/SPEC.md và ${base}/codex/L5-brief.md`,
  'soát kết quả',
  'Chiến dịch M1-FlashTicket, phần tích hợp giao diện sau G4',
  'Codex làm T-065. Claude phản biện và điều phối',
  `${task}/SPEC.md, ${task}/LOG.md, ${base}/codex/L5-brief.md, results/T-064/ban-xuat/chi-muc-ban.json`,
  `${task}/REVIEW.md và ${task}/LOG.md`,
  `${base}/BAN-GIAO-L5.md, ${base}/manifest.json, ${base}/CHECKPOINT.md, ${report}/BAO-CAO.md, ${base}/thay-doi-may.md và các script l5-*`,
  `Chỉ nhận xét trong chat và ghi file phản biện nếu Minh duyệt đúng vị trí theo ${task}/SPEC.md`
];
let index = 0;
const common = section('## Prompt chung').replace(/<[^>]+>/g, () => values[index++]);
if (index !== values.length) throw Error(`Sai số trường prompt: ${index}`);
const prompt = [common, section('### Soát kết quả'), section('### G4 — Kết quả')].join('\n\n');
await write(`${base}/prompt-ban-giao.md`, prompt);
await write(`${base}/XONG.md`, `# T-065 L5 — đạt một phần\n\nĐã triển khai cây Grafana lồng có 7 dashboard RCA. Sáu dashboard cũ giữ UID và bốn JSON lưu trữ giữ hash. Chrome đã đối chiếu đủ 66 trang và ảnh.\n\nĐã chốt 39 trong 162 liên kết của mẫu sâu, gồm 16 Tempo, 16 Loki và 7 Prometheus. Đang dở ở liên kết Prometheus thứ 40. Quyền Chrome của chat chưa khôi phục sau lần gián đoạn hạn mức.\n\nTệp tiếp nhận: BAN-GIAO-L5.md, CHECKPOINT.md và kiem/003-trinh-duyet/sau-tien-do.json. Kết quả chi tiết xem kiem/003-trinh-duyet/BAO-CAO.md.\n`);
await append(`${base}/CHECKPOINT.md`, `## ${stamp} — L5 tiếp nhận sau gián đoạn hạn mức\n\n- Đã đọc lại L5-brief.md. Xác minh 66 bản đối chiếu và 66 PNG, 8 service, 16 thao tác, 39 liên kết. Hai lần đổi bản giữ ca, cửa sổ và service.\n- Rà API cùng cửa sổ. 14 Loki rỗng có bằng chứng truy vấn. 10 quan sát panel rỗng ở e8661e0a vẫn loại (iii) vì API có dữ liệu. Ứng viên UI-03 dựng tại grafana-l5/ui03/, đang chờ kiểm lại Chrome trước khi triển khai.\n- Tab L5 chính 217960284. Tab Explore Prometheus 217960455 mở lúc 05:21:24Z, chưa đọc kết quả. sau-tien-do.json ghi pair=3, service=1, op=1, link=2. Không tiến trình nền. Browser Use hiện báo quyền Chrome không khả dụng ở chat.\n- Tiếp đúng bước: gắn @Chrome, kiểm STOP/máy, đọc Explore hiện có nếu tab khớp URL. Nếu tab Explore mất, mở lại riêng phép bấm Prometheus p7/00eaea92/booking-service/oc0d4761ef55d4ae54aa0, rồi L5Deep.init()/advance() theo BAN-GIAO-L5.md. Còn 123 kết quả liên kết, các mẫu sâu đang dở, kiểm phát lại và màu/nhãn.\n- Bản bàn giao và prompt đã ghi. Số cuối trong tien-do.json, manifest băm tạo tác. Dòng trạng thái là mot_phan.`);
await append(`${base}/thay-doi-may.md`, `## ${stamp} — kiểm lại máy khi tiếp nhận\n\n- Lệnh đọc: l5-may.ps1 và l5-obs.py qua Git SSH với inventory, resume-empty, dashboard-links. Không phát thao tác ghi lên exp-obs khi tiếp nhận.\n- may-cuoi.json và doi-chieu-hash-may-l5.json giữ hash trước/sau của provider và sáu dashboard đã chuyển. Bốn dashboard lưu trữ giữ byte. Cả hai L4 đang chạy khớp bản trong grafana-l4/. Cả 7 UID trả HTTP 200.\n- Ứng viên UI-03 ở grafana-l5/ui03/ chỉ dựng cục bộ. Giữ hai bản đang chạy trong grafana-l5/*-truoc-ui03.json để đối chiếu và hoàn tác nếu triển khai ở lượt sau.`);
await append(`${task}/LOG.md`, `## L5 — ${stamp} — Codex, laptop Minh, người làm\n\n1. Đã xếp Grafana vào cây lồng và thêm mục lục. Sửa bảng metadata và lời diễn giải panel rỗng. Phủ rộng trên Chrome đủ 66 cặp. Kiểm sâu chốt 39 liên kết, 16 thao tác và 8 service. Tiếp nhận sau gián đoạn và đối chiếu phần đã lưu.\n2. File đổi nằm trong results/T-065/ và mục nối LOG này. Trên máy đổi file provider, vị trí 6 dashboard, thêm mục lục và sửa 2 JSON L4. Xóa RCA cũ đã kiểm rỗng. Không ghi STATE.\n3. Kiểm 7 UID bằng API, 4 hash lưu trữ, 66 PNG, 66 đối chiếu DOM/URL và 27 bản ghi máy. 14 Loki rỗng khớp API. 10 quan sát rỗng chưa phân xử.\n4. L5 một phần. Điều cần Minh là gắn @Chrome cho đúng chat. Phần còn lại và thông tin tiếp nhận ở BAN-GIAO-L5.md. T-065 hỗ trợ giao diện DT18, RQ5 vẫn phụ thuộc thực nghiệm.\n\nBước tiếp mở tab L5 217960284, đọc kết quả Prometheus ở 217960455 nếu còn, rồi chạy L5Deep.init()/advance(). Nếu tab Explore mất, mở lại riêng bước đang dở trên dashboard. Lệnh cuối dự kiến là node results/T-065/l5-tong-hop.mjs manifest.\n\n### Prompt độc lập cho Claude\n\n${prompt}`);
await write(`${base}/codex/L5-trang-thai.json`, JSON.stringify({ ten: 'L5', trang_thai: 'mot_phan', nguon: 'codex-app', cap_nhat: stamp, buoc: 'cho_ket_noi_chrome_de_doc_prometheus_pair3_service1_op1_link2', ly_do: 'Browser Use báo quyền Chrome không khả dụng trong chat sau gián đoạn hạn mức. 66 trang và 39 liên kết còn trên đĩa. Xem BAN-GIAO-L5.md và sau-tien-do.json.' }, null, 2));
