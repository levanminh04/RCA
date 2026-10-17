"""Sinh tài liệu v2 từ bản v1 giữ nguyên và bằng chứng của lượt sửa đã duyệt."""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[3]
OUT = ROOT / 'results/T-035'


def read(path):
    return json.loads(path.read_text('utf-8'))


def replace_once(text, old, new):
    assert text.count(old) == 1, old
    return text.replace(old, new)


def render():
    c = read(BASE / 'comparison.json')
    assert c['pass'] and c['reused_cases'] == 0
    old_fixtures = [read(BASE / f'fixture-cu-seed{i}-002/result.json') for i in range(3)]
    new_fixtures = [read(BASE / f'fixture-v2-seed{i}-002/result.json') for i in range(3)]
    boundary = [read(BASE / f'boundary-seed{i}-002/result.json') for i in range(3)]
    assert all(x['pass'] for x in boundary)
    assert all(x['pass'] for x in new_fixtures)
    assert all(all(y['pass'] for y in x['fixtures']) and x['label_rejection'] for x in old_fixtures)
    old_n, new_n = len(old_fixtures[0]['fixtures']), new_fixtures[0]['passed']
    source = lambda name: (BASE / 'before/results/T-035' / name).read_text('utf-8')
    table = source('thong-tin-theo-quan-he.md')
    replacements = {
        '| Phát→broker |': '| Phát→broker | PRODUCER, broker ổn định, broker_scope triển khai/vhost, exchange và routing_key; ngữ cảnh tạo bản tin | B16 §3, §5 và B13 §5.1. Một phần: kiến trúc quy định exchange/routing, chưa xác nhận các trường trace export | Thiếu | Thiếu | P9a xác minh adapter và địa chỉ phát; không ép địa chỉ phát thành queue nhận |',
        '| Broker→nhận |': '| Broker→nhận | CONSUMER, broker, broker_scope, queue, messageId, delivery attempt, processing instance | B16 §3, §5; B13 §5.1–5.2: queue theo consumer, có sự kiện nhiều consumer. Một phần, chưa kiểm runtime | Thiếu | Thiếu | P9a kiểm queue riêng, delivery khác processing, retry và clock; không nối chỉ vì timestamp gần |',
        '| Nối logic gửi→nhận |': '| Nối logic gửi→nhận | Link tạo bản tin đã xác minh trỏ PRODUCER trong miền và trường cùng hiện diện tương thích; hoặc broker + broker_scope + identity_scope đã xác minh + messageId, nguồn tạo duy nhất | B16 §3 cho messageId và link; B13 giữ ID qua publish lại. Một phần: thiếu namespace ID và nghĩa link trong export thật | Thiếu | Thiếu | P9a kiểm fanout/batch/retry/redelivery, collision, nguồn ngoài miền. Không đòi exchange bằng queue; không fallback ID che link mâu thuẫn; correlation không đủ |',
        '| Metric→entity/host/broker/operation |': '| Metric→entity/host/broker/operation | service/instance/host; queue_metric_address = broker + broker_scope + queue khi đủ; operation metric chỉ khi đo đúng scope | B16 §4–5, §7: cardinality, queue ready/unacked, host. Chưa xác nhận namespace queue trong trace/metric export | Metric entity, không là metric từng operation | Resource channels và tên Node*; Node* values không đọc trong task | P9a thống nhất địa chỉ, giữ queue khác nhau sau gộp/chiếu. Thiếu scope/queue thì chưa gắn metric; ID bản tin/attempt không là nhãn; không sao metric chung thành bằng chứng độc lập |',
    }
    for prefix, row in replacements.items():
        lines = [line for line in table.splitlines() if line.startswith(prefix)]
        assert len(lines) == 1
        table = replace_once(table, lines[0], row)
    table += f'''\n## Hợp đồng v2 và bằng chứng kiểm

Địa chỉ phát, queue nhận và namespace ID là ba thông tin khác nhau. `messaging.destination` cũ không tự xác định queue hoặc identity scope. Hợp đồng chính xác và các trường diagnostic nằm tại dac-ta-do-thi.md §7. Cạnh nhận/logic giữ queue khi gộp và chiếu; nhiều cạnh mang một metric address chỉ tham chiếu một chuỗi chung.

{new_n} fixture bổ sung đã đạt ở ba seed, gồm các trường hợp dương/âm và địa chỉ queue; nguồn `runs/sua-n1-001/fixture-v2-seed0-002/result.json#/fixtures`, các lượt seed1/seed2 cùng thư mục. Đây là bằng chứng bộ dựng theo hợp đồng, chưa là dữ liệu FlashTicket thật. Nguồn kiến trúc bổ sung: D:/Project/flash-ticket-platform/docs/architecture/B13-api-and-event-contracts.md §5.1–5.2; hash nguồn trong runs/sua-n1-001/input-verification.json. Các yêu cầu P9a vẫn cần Minh duyệt riêng.
'''
    report = source('thong-ke-do-thi.md')
    report = report.replace('| 1. Mô hình chung đủ nút/cạnh | Đạt | dac-ta-do-thi.md; fixture; thành phần thiếu dev vẫn có trong mô hình |',
                            '| 1. Mô hình chung đủ nút/cạnh | Đạt theo hợp đồng v2, chờ nghiệm thu | dac-ta-do-thi.md; fixture cũ và bổ sung; routing/instrumentation FlashTicket thật chưa kiểm |')
    report = report.replace('| 9. C9 đầy đủ | Đạt | Bảng quan hệ, lý do và nơi nhận; runtime FlashTicket chưa kiểm |',
                            '| 9. C9 đầy đủ | Đạt ở mức hợp đồng v2, chờ nghiệm thu | Địa chỉ phát/queue/ID scope tách riêng; bảng nguồn và nơi nhận; runtime FlashTicket chưa kiểm |')
    report = report.replace('T-036 nhận mô hình v1,', 'T-036 nhận mô hình v2,')
    report = replace_once(report, 'Chi phí lượt đầy đủ:', 'Chi phí lượt đầy đủ v1 (giữ làm lịch sử):')
    report = replace_once(report, 'Kết quả task đã hoàn tất để chờ Claude phản biện và Minh nghiệm thu.',
                          'Đầu ra hiện chờ phiên Codex sạch tự soát toàn task theo lời Minh, rồi phản biện chính thức và Minh nghiệm thu.')
    report = report.replace('Prompt Claude trong LOG Phiên 6 và prompt-claude-soat-ket-qua.txt; Minh chuyển thủ công.',
                            'Prompt hiện tại trong LOG Phiên 7 và runs/sua-n1-001/; giữ prompt Phiên 6 làm lịch sử; Minh chuyển thủ công.')
    report += f'''\n## 7. Sửa hợp đồng messaging và hồi quy v2

V1 chưa phủ đúng địa chỉ phát khác queue nhận: cùng destination vừa là điều kiện nối, vừa là địa chỉ metric. Vì vậy kết luận đạt tiêu chí 1/9 của bản trước cần bản sửa. V2 tách ba thông tin, kiểm link/ID có điều kiện và giữ queue qua gộp/phép chiếu. Bản trước, thiết kế, oracle và mọi lượt kiểm được giữ tại runs/sua-n1-001/. Căn cứ lựa chọn ở WHY-52, lời duyệt Q-154.

{old_n} fixture cũ, {new_n} fixture messaging và 3 ca biên thiếu attributes/links đạt ở seed 0/1/2. Phản chứng bằng code v1 được giữ riêng; thất bại của oracle v2 gồm cả khác schema, không diễn giải thành {new_n} lỗi độc lập. Trường hợp fanout có địa chỉ phát khác queue nhận là bằng chứng trực tiếp của thiếu sót và bản sửa; xem fixture_design.md, fixture-v1-001/result.json và fixture-v2-seed0-002/result.json trong lượt này. Ba ca biên dùng oracle riêng ghi trước sửa nhánh thiếu dữ liệu; nguồn boundary-oracle-before-code.json và boundary-seed0-002/result.json. Lượt dev đầu dừng để hoàn thiện nhánh này sau tự kiểm, được giữ nguyên ở day-du-001/interruption.json; lượt đầy đủ cuối là day-du-002.

Chạy lại {c['case_count']} ca, không dùng lại pilot: {c['window_count']} khoảng, {c['graph_count']} graph lưu khớp từng byte bản cũ; nội dung từng ca ngoài thời gian/chi phí máy, vocabulary, Node, coverage và K1/K2/K4/K5 đều khớp. Nguồn `runs/sua-n1-001/comparison.json#/cases`, `#/graphs`, `#/all_K1_K2_K4_K5`. Không ghi đè graph hoặc JSON thống kê cũ. Vì đầu ra đồng nhất, các bảng mô tả và phân nhóm cũ giữ nguyên; đây là kiểm hồi quy, không là bằng chứng messaging đã xuất hiện trên dev.

Lượt mới mất {c['seconds']/60:.2f} phút, RAM đỉnh {c['peak_rss_bytes']/1024**3:.2f} GiB; nguồn `comparison.json#/seconds`, `#/peak_rss_bytes` trong lượt sửa. Tiến độ từng khoảng ở day-du-002/progress.jsonl. Sửa này xác nhận hành vi bộ dựng trên fixture và hồi quy trong miền đã kiểm; chưa xác nhận routing thật, nghĩa Node, cơ chế RCA hoặc lợi ích đồ thị. Chưa tự nghiệm thu T-035/P5/G3. Minh yêu cầu phiên Codex sạch tự soát lại toàn task; Claude vẫn là người phản biện chính thức.
'''
    checks = source('kiem-dung-dan.md')
    checks += f'''\n## Kiểm bản v2 sau sửa hợp đồng messaging

Quyền và thiết kế: Q-154, WHY-52 bổ sung; runs/sua-n1-001/design.md. Oracle được ghi trước sửa code, bằng chứng thứ tự ở oracle-before-code.json; fixture_design.md giải thích từng phép phân xử. Kiểm đầu vào cũ theo manifest trước khi dùng: input-verification.json trong lượt sửa; bản manifest và graph cũ được giữ nguyên.

- {old_n} fixture cũ đạt ở seed0/1/2, kết quả byte giống nhau: fixture-cu-seed0-002 đến fixture-cu-seed2-002/result.json.
- {new_n} fixture mới đạt ở seed0/1/2: fixture-v2-seed0-002 đến fixture-v2-seed2-002/result.json. Kiểm exact cạnh, count, witness, metric address, diagnostic, phép chiếu API và phép chiếu độc lập ở cả hai mức. Các fixture giữ operation ổn định qua retry và qua hai queue cùng consumer.
- Ba ca consumer/producer thiếu toàn attributes/links đạt seed0/1/2: boundary-seed0-002 đến boundary-seed2-002/result.json. Oracle và bản trước nhánh sửa ở boundary-oracle-before-code.json, boundary-before/; lượt fail giữ ở boundary-before-001. Span loại CONSUMER vẫn được ghi unresolved và thiếu địa chỉ khi các cột tùy chọn đều null hoặc vắng.
- Code v1 chạy trên cùng oracle mới ở fixture-v1-001/result.json. Oracle còn kiểm schema v2 nên không dùng số fail làm số lỗi ngữ nghĩa riêng; đọc từng actual/expected. Không xóa lượt fail.
- Hồi quy đầy đủ: {c['case_count']} ca/{c['window_count']} khoảng, K1/K2/K4/K5 đạt; {c['graph_count']} graph byte bằng bản cũ; mọi trường kết quả ca trừ chi phí máy bằng nhau. comparison.json lưu từng phép so. Node/vocabulary cũng được so; không chạy lại tính điểm RCA hoặc nguồn phụ mức ngày.

Các đường dẫn trên tính từ runs/sua-n1-001/. K3/K6/K8 và số phân nhóm cũ được giữ với bằng chứng cũ; không khai là đã thực nghiệm lại các phép ấy. Đầu ra đồ thị, stats/coverage/checks và input không đổi hỗ trợ dùng lại kết quả mô tả trong đúng phạm vi. Fixture là dữ liệu giả kiểm hợp đồng, không chứng minh instrumentation FlashTicket hay lợi ích RCA.
'''
    return {'dac-ta-do-thi.md': (BASE / 'contract-v2.md').read_text('utf-8'),
            'thong-tin-theo-quan-he.md': table,
            'thong-ke-do-thi.md': report, 'kiem-dung-dan.md': checks}


def main():
    documents = render()
    for name, text in documents.items():
        (OUT / name).write_text(text, encoding='utf-8')
    print(json.dumps({'written': list(documents)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
