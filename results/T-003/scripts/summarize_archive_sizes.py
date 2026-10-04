"""Summarize saved archive indices; no network or telemetry access."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-003'

def read(path):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))

indices = read('results/T-003/runs/sizes-001/archive-index-results.json')
nested = read('results/T-003/runs/sizes-nested-001/nested-index-results.json')
previous = read('results/T-003/runs/checkpoint-001/verification.json')['proposed_download_bytes']
deep = read('results/T-010/runs/run-001/count-summary.json')['groups']
assert len(nested) == 7 and all(x['status'] == 'ok' and x['crc_matches_outer_zip'] for x in nested)
rows = []
for label, task in [('Eadro', 'T-009'), ('DeepTraLog', 'T-010'), ('LEMMA: bốn ZIP IT đề xuất', 'T-011')]:
    selected = [x for x in indices if x['task'] == task and x['status'] == 'ok']
    download = sum(x['download_bytes'] for x in selected)
    expanded = sum(sum(m['uncompressed_bytes'] for m in x['members']) for x in selected)
    bound = task == 'T-009'
    if bound:
        expanded += sum(x['uncompressed_stream_bytes'] for x in nested)
    if task == 'T-010':
        download += deep['graph_parts']['bytes'] - sum(x['download_bytes'] for x in selected if x['variant'] == 'graph_parts')
    rows.append(dict(dataset=label, download_bytes=download, expanded_bytes=expanded,
                     expanded_is_upper_bound=bound, archive_bytes=download))
rows.insert(0, dict(dataset='Nezha: OB + TT, file không nén', download_bytes=previous['nezha_raw_all'],
                    expanded_bytes=previous['nezha_raw_all'], expanded_is_upper_bound=False, archive_bytes=0))
assert [r['download_bytes'] for r in rows] == [previous[k] for k in ['nezha_raw_all','eadro_two_zip','deep_raw_plus_graph','lemma_four_sample_zip']]
totals = dict(download_bytes=sum(r['download_bytes'] for r in rows),
              expanded_upper_bound_bytes=sum(r['expanded_bytes'] for r in rows))
totals['retaining_downloaded_archives_upper_bound_bytes'] = totals['expanded_upper_bound_bytes'] + sum(r['archive_bytes'] for r in rows)
assert totals['download_bytes'] == previous['including_lemma_sample']
result = dict(status='CANDIDATE; no full corpus download approved by this report', rows=rows, totals=totals,
              telemetry_rows_read=0, verified=True)
target = OUT / 'runs/sizes-summary-001'
target.mkdir(exist_ok=False)
(target / 'summary.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
lines = ['# Dung lượng tải và giải nén T-003', '',
         'Đề xuất để Minh duyệt, chưa tải toàn gói. GB = 1.000.000.000 byte. Phạm vi là các file đã đề xuất, không phải toàn bộ mọi dataset.', '',
         '| Phạm vi | Tải (GB) | Nội dung sau giải nén (GB) |', '|---|---:|---:|']
for r in rows:
    lines.append(f"| {r['dataset']} | {r['download_bytes']/1e9:.3f} | {r['expanded_bytes']/1e9:.3f}{' (cận trên)' if r['expanded_is_upper_bound'] else ''} |")
lines += ['', f"Tổng tải: {totals['download_bytes']/1e9:.3f} GB. Nội dung: tối đa khoảng {totals['expanded_upper_bound_bytes']/1e9:.3f} GB theo cách đếm dưới đây. Giữ thêm file tải nén: khoảng {totals['retaining_downloaded_archives_upper_bound_bytes']/1e9:.3f} GB. Chưa cộng file tạm, bản sao khi xử lý và phân bổ block của ổ đĩa.", '',
          '- ZIP: cộng kích thước member từ central directory; chưa giải nén để kiểm nội dung thực tế.',
          '- Eadro: giữ nội dung ZIP (bao gồm XZ bên trong), cộng độ dài TAR sau XZ từ index. TAR còn header/padding nên đây là cận trên cho file cuối, không phải số byte file cuối chính xác. Nếu lưu cả TAR trung gian thì cần thêm chỗ; không nằm trong tổng này.',
          '- DeepTraLog: tính đủ tám phần graph, dù mục lục nằm trong phần ZIP cuối; chưa kiểm việc ghép và giải nén thực. Không gồm gói alllog tùy chọn hoặc kết quả phương pháp đã công bố.',
          '- LEMMA: chỉ bốn ZIP Preprocessed của hai hệ IT: metric/log ngày 20211203 (Product Review), 20240124 (Cloud Computing). Không gồm toàn bộ Original hoặc OT (SWaT/WADI). Mẫu chưa đại diện toàn bộ các bộ IT.', '',
          'Nguồn và số byte chính xác:', '',
          '- [Tổng kiểm và số byte](runs/sizes-summary-001/summary.json).',
          '- [Mục lục ZIP, URL và từng member](runs/sizes-001/archive-index-results.json).',
          '- [Index XZ và CRC đối chiếu ZIP](runs/sizes-nested-001/nested-index-results.json).',
          '- [Inventory tải đề xuất trước đó](runs/checkpoint-001/verification.json); [đủ tám phần graph](../T-010/runs/run-001/count-summary.json).', '',
          'Chi phí lượt kiểm: đọc 494.256 byte mục lục; tải 44.011.656 byte XZ nén vào RAM để đọc footer/index do nguồn không phục vụ Range. Không lưu payload, không giải nén XZ, không đọc dòng metric/log/trace. Giữ bảy lỗi Range ở lượt đầu. Hai lượt chạy mất 16,397 và 52,174 giây; không phải thời gian tải/giải nén toàn gói.', '',
          'Chưa đo thời gian tải/giải nén toàn gói, RAM và file tạm. Chưa gọi những phần này là không thể kiểm. Báo cáo này không cho phép đọc số đo của ứng viên giữ ngoài, không chọn dataset và không đổi cách phản biện.']
(OUT / 'dung-luong-tai-va-giai-nen.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print(json.dumps(dict(verified=True, totals=totals), ensure_ascii=False))
