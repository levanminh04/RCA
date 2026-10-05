"""T-021 bước 2–3: ghi bốn bảng chính từ census-002, vi-tri-001 và các thẻ dataset gốc.

Số ca/root/ô/TX đọc từ runs/census-002 (tính lại từ file gốc). Các ô chữ dẫn file:dòng của thẻ gốc.
Chạy: py -3 -X utf8 results/T-021/scripts/build_bang.py
"""
import csv, json, os, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
R = lambda *p: os.path.join(ROOT, *p)
OUT = R('results/T-021')
census = json.load(open(R('results/T-021/runs/census-002/census-summary.json'), encoding='utf-8'))

T2 = 'results/T-002/the-rcaeval.md'
T8 = 'results/T-008/the-dataset.md'
T9 = 'results/T-009/the-dataset.md'
T10 = 'results/T-010/the-dataset.md'
T11 = 'results/T-011/the-dataset.md'
T12 = 'results/T-012/the-dataset.md'
T19 = 'results/T-019/the-sock-shop.md'
K3 = 'docs/knowledge/K3-dataset-ung-vien.md'
Q59 = 'docs/DECISIONS.md Q-59'

# (dataset, tải được, quyền dùng Q-59, nhãn root, thời điểm, tín hiệu phương pháp cần, kết luận lớp 1, nguồn)
DK = [
    ('RE2-TT', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm, không phải onset', 'đạt: metric, trace cha–con, log 89/90 ca; log không có trace_id', 'ĐẠT', f'{T2}:33-41; data/README.md:9'),
    ('RE2-OB', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'đạt: metric, trace, log', 'ĐẠT (nhưng TX2 toàn bộ)', f'{T2}:188-196'),
    ('RE2-SS', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'một phần: metric, log; KHÔNG có trace', 'ĐẠT cho phương pháp metric/log; trace: không', f'{T19}:208-210'),
    ('RE1-TT', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'một phần: chỉ metric (census: 0 trace, 0 log)', 'ĐẠT cho phương pháp metric', 'results/T-021/runs/census-002/census-summary.json'),
    ('RE1-OB', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'một phần: chỉ metric', 'ĐẠT cho phương pháp metric (TX2 toàn bộ)', 'results/T-021/runs/census-002/census-summary.json; results/T-006/kiem-dung-dan.md:60-66'),
    ('RE1-SS', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'một phần: chỉ metric', 'ĐẠT cho phương pháp metric', f'{T19}:33-41'),
    ('RE3-TT', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'đạt: metric, trace, log (kiểm 1 ca)', 'ĐẠT', f'{T2}:316-324'),
    ('RE3-OB', 'đạt (138 MB, chưa tải)', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'OPEN: metadata có trace/log/metric; schema chưa kiểm', 'ĐẠT theo metadata; schema OPEN', f'{T2}:449-457'),
    ('RE3-SS', 'đạt', 'đạt (MIT)', 'đạt', 'đạt: lúc tiêm', 'một phần: metric, log; không trace', 'ĐẠT cho phương pháp metric/log', f'{T19}'),
    ('Nezha-OB', 'đạt', 'đạt theo Q-59 (chưa có giấy phép văn bản)', 'đạt', 'đạt: lúc tiêm; hai cách hiểu đồng hồ cho cùng nhóm vị trí ở OB', 'đạt: trace cha–con, log có trace_id, metric', 'ĐẠT', f'{T8}:15-23; {Q59}'),
    ('Nezha-TT', 'đạt', 'đạt theo Q-59', 'đạt', 'OPEN: hai giả thuyết đồng hồ đổi nhóm vị trí ở một phần sự kiện', 'đạt: trace, log có trace_id, metric', 'ĐẠT; đồng hồ OPEN', f'{T8}:108-116; results/T-021/runs/vi-tri-001/tom-tat.json'),
    ('Eadro-SN', 'đạt', 'đạt theo Q-59', 'đạt', 'đạt cho metric/log; OPEN cho trace (timestamp trace lệch biểu kiến so với nhãn)', 'đạt: trace, log, metric', 'ĐẠT; ghép trace theo thời gian OPEN', f'{T9}:13-21; {T9}:95'),
    ('Eadro-TT', 'đạt', 'đạt theo Q-59', 'đạt', 'đạt cho metric/log; OPEN cho trace (như SN)', 'đạt: trace, log, metric', 'ĐẠT; ghép trace theo thời gian OPEN', f'{T9}:140-148; {T9}:282'),
    ('DeepTraLog-TT', 'đạt', 'OPEN (điều khoản chưa đủ)', 'KHÔNG: chỉ nhãn trace bất thường, không nhãn root service', 'KHÔNG: không mốc tiêm/onset', 'trace, log', 'KHÔNG ĐẠT (thiếu nhãn root và thời điểm)', f'{T10}:16; {T10}:146-148'),
    ('LEMMA-PR/Cloud', 'đạt (mẫu); bản gốc 53 GB + 33 GB', 'đạt theo Q-59 (cc-by-nc; ghi chú ND mâu thuẫn)', 'một phần: một entity nhãn mỗi ngày mẫu, không census root×lỗi', 'OPEN: mốc tiêm/normal chưa xác minh', 'KHÔNG có trace (mẫu); metric, log', 'KHÔNG ĐẠT cho trace; nhãn root mỏng', f'{T11}:13-27'),
    ('FSE-2026-TT (bản rút gọn)', 'đạt', 'OPEN (phạm vi license raw)', 'một phần: 8/10 ca hợp lệ, nhiều ca có nhiều root', 'đạt: start/end tiêm', 'trace (đã đo), metric, log', 'ĐẠT HÌNH THỨC nhưng quá nhỏ (8 ca)', f'{T12}:15-17; {T12}:73'),
    ('AnoMod-SN/TT', 'đạt', 'đạt (CC-BY-4.0)', 'KHÔNG: tên thí nghiệm, không nhãn root theo sự cố', 'KHÔNG: chưa có gold incident/onset', 'trace, metric, log', 'KHÔNG ĐẠT', f'{T12}:85-87; {T12}:144-146'),
    ('TrainTicketTrace', 'OPEN (chưa tải)', 'OPEN', 'OPEN: tên archive là version', 'OPEN', 'OPEN (bài nói có trace/metric/log)', 'OPEN', f'{T12}:209-211'),
    ('TRCA-TT/OB', 'đạt', 'OPEN (dữ liệu dùng lại của Nezha)', 'đạt (trùng nhãn Nezha)', 'như Nezha', 'như Nezha', 'TRÙNG BYTE Nezha, không là bộ mới', f'{T12}:293-295'),
    ('OpenRCA-Bank', 'đạt (2,83 GB nén, 26,4 GB giải nén; chưa tải)', 'đạt theo Q-59 (CC BY-NC 4.0)', 'đạt: component (pod/node), 14 root', 'đạt: thời điểm bản ghi; không phải lúc tiêm', 'theo bài: metric, trace, log; chất lượng chưa kiểm (giữ tới G3)', 'ĐẠT theo nguồn; chất lượng OPEN', f'{T12}:491-501'),
    ('OpenRCA-Telecom', 'OPEN (chưa tải)', 'đạt theo Q-59 (CC BY-NC 4.0)', 'theo README', 'theo README', 'theo bài A.3', 'OPEN (chưa census)', f'{T12}:405; {T12}:413-415'),
    ('OpenRCA-Market', 'OPEN (chưa tải)', 'đạt theo Q-59 (CC BY-NC 4.0)', 'theo README', 'theo README', 'theo bài A.3', 'OPEN (chưa census)', f'{T12}:588-590'),
    ('OpenRCA-2.0 (TT, OTel Demo, Hotel)', 'KHÔNG: chưa có bản công khai ghim', 'OPEN', 'theo bài', 'theo bài', 'theo bài có trace', 'KHÔNG ĐẠT (chưa phát hành)', f'{T12}:678-680'),
    ('LO2 v1/v2', 'OPEN', 'OPEN', 'KHÔNG: nhãn API đúng/sai, không root service', 'một phần', 'KHÔNG: mỗi trace một span (v1)', 'KHÔNG ĐẠT', f'{T12}:948-950'),
    ('BARO-FSE-OB (fse-ob)', 'đạt (bản cục bộ)', 'đạt', 'đạt', 'đạt', 'chỉ metric', 'chỉ để tái lập (TX2 100 ca)', 'results/T-006/kiem-dung-dan.md:60-66'),
    ('FAMOS TrainTicket', 'OPEN (287 MB, chưa mở)', 'đạt (CC-BY-4.0)', 'OPEN', 'OPEN', 'OPEN', 'OPEN (chưa kiểm trên file)', 'results/T-012/final-leads.md:9'),
    ('GAIA/MicroSS', 'theo README (git, nhiều phần zip)', 'đạt (Apache 2.0)', 'một phần: bản ghi tiêm theo instance (1.448 lần)', 'đạt: start + thời lượng', 'theo README: trace, metric, log; bản V1.10 bỏ trace tháng 8', 'OPEN (chưa kiểm trên file)', f'{K3}:154-166'),
    ('DejaVu (A–D)', 'theo README (Zenodo)', 'OPEN', 'đạt theo README (faults.csv)', 'theo README', 'KHÔNG trace span: metric + đồ thị FDG', 'OPEN (chưa kiểm trên file)', f'{K3}:214'),
    ('Dữ liệu TraceRCA (IWQoS 2021)', 'theo README (OneDrive, Tsinghua Cloud)', 'OPEN', 'OPEN: README không mô tả nội dung', 'OPEN', 'OPEN', 'OPEN (chưa kiểm trên file)', f'{K3}:215'),
    ('Dữ liệu mẫu MicroRCA', 'đạt (thư mục data trong repo)', 'OPEN', 'OPEN: chỉ là ví dụ', 'OPEN', 'KHÔNG trace span: thời gian phản hồi giữa service + tài nguyên', 'KHÔNG ĐẠT (dữ liệu ví dụ, không trace span)', f'{K3}:216'),
]

DL = [  # dataset, tác giả, công cụ tiêm lỗi, hệ thu thập, kết luận Q-60(c), nguồn
    ('Eadro-SN/TT', 'khác (Lee, Yang, Chen, Su, Lyu — CUHK)', 'khác (ChaosBlade)', 'khác: Jaeger, cAdvisor/Prometheus→InfluxDB, Fluentd/ES do nhóm Eadro dựng', 'KHÁC', 'results/T-009/sources/paper.html:257,814,822'),
    ('Nezha-OB/TT', 'khác (Yu, Chen, ... Zheng — SYSU)', 'khác cho lỗi mã nguồn (Byteman/Hypno/Failpoint); CPU/mạng OPEN', 'khác: OTel Collector/Tempo, Promtail/Loki, Prometheus do nhóm Nezha dựng', 'KHÁC (trục công cụ tiêm một phần OPEN)', f'{T8}:5'),
    ('OpenRCA-Bank/Telecom/Market', 'khác (Xu và cộng sự) nhưng dữ liệu gốc AIOps Challenge', 'OPEN', 'OPEN', 'OPEN', 'results/T-020/trung-gian/dataset_evidence/independence-axes.csv (đối chiếu); results/T-012/runs/run-002/sources/openrca-paper.txt:196'),
    ('FSE-2026-TT', 'khác (Fang, ..., He)', 'khác (ChaosMesh)', 'khác (OTel, Hubble)', 'KHÁC', 'results/T-012/runs/run-001/sources/fse-paper-v2.html:287,1353,1365'),
    ('DeepTraLog-TT', 'khác (Zhang, Peng, ... Fudan)', 'khác (nhánh TT có lỗi)', 'khác (SkyWalking/ES)', 'KHÁC (nhưng không đạt lớp 1)', f'{T10}'),
    ('LEMMA', 'khác (Zheng, Chen — NEC)', 'khác (theo kịch bản)', 'khác (OpenShift Prometheus/ES; CloudWatch)', 'KHÁC (nhưng không trace)', 'results/T-011/runs/run-001/sources/paper-v4.html:239'),
    ('AnoMod', 'khác (Helsinki)', 'ChaosBlade/ChaosMesh', 'Prometheus, Jaeger/SkyWalking', 'KHÁC (nhưng không đạt lớp 1)', f'{T12}:79'),
    ('TRCA', 'ẩn danh', 'trùng Nezha (byte)', 'trùng Nezha (byte)', 'TRÙNG Nezha', f'{T12}:293'),
    ('RCAEval RE1/RE2/RE3', 'trùng (cùng họ)', 'trùng', 'trùng', 'TRÙNG (mốc so)', f'{T2}:41'),
    ('GAIA/MicroSS', 'khác (CloudWise)', 'riêng (script tiêm của nhóm)', 'riêng', 'KHÁC theo README (chưa kiểm)', f'{K3}:154-166'),
]


def main():
    with open(os.path.join(OUT, 'dieu-kien-toi-thieu.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dataset', 'tai_duoc', 'quyen_dung_Q59', 'nhan_root', 'thoi_diem_loi', 'tin_hieu_phuong_phap_can',
                    'so_ca', 'so_root', 'so_o', 'tx', 'ket_luan_lop1', 'nguon'])
        for r_ in DK:
            key = r_[0].split(' ')[0]
            c = census.get(key) or census.get(key.replace('-2026-TT', '-2026-TT'))
            if c is None and key.startswith('FSE'):
                c = census.get('FSE-2026-TT')
            so = (c['cases'], c['roots'], c['cells'], json.dumps(c['tx'])) if c else ('', '', '', '')
            w.writerow(list(r_[:6]) + list(so) + list(r_[6:]))
    with open(os.path.join(OUT, 'doc-lap.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dataset', 'tac_gia', 'cong_cu_tiem_loi', 'he_thu_thap', 'ket_luan_Q60c', 'nguon'])
        w.writerows(DL)
    # tiếp xúc: tổng hợp từ census-002 (mỗi mức có nguồn trong census-cases.csv)
    rows = list(csv.DictReader(open(R('results/T-021/runs/census-002/census-cases.csv'), encoding='utf-8')))
    agg = collections.defaultdict(lambda: collections.Counter())
    src = collections.defaultdict(set)
    probe = collections.Counter()
    for x in rows:
        agg[x['dataset']][x['tx']] += 1
        src[(x['dataset'], x['tx'])].add(x['tx_nhom'] + ': ' + x['tx_nguon'].split('#')[0].split('!')[0])
        if x['probe_trieu_chung']:
            probe[x['dataset']] += 1
    with open(os.path.join(OUT, 'tiep-xuc.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dataset', 'tx', 'so_ca', 'ca_da_do_trieu_chung_gan_root', 'nguon', 'ghi_chu'])
        notes = {'RE1-OB': 'TX2 qua bản Zenodo cục bộ (T-006 chạy BARO/N-Sigma/RCD qua main.py); danh tính bản HF chưa đối chiếu byte -> coi như TX2 (thận trọng)',
                 'RE2-TT': '60 ca TX1: v1 đọc schema, độ phủ trace của cả 90 ca (MRP §4:120); T-020 ghi TX0 là sai (REVIEW T-020 R1)',
                 'OpenRCA-Bank': 'chỉ đọc record.csv 8.668 byte (nhãn); không đọc telemetry'}
        for ds in sorted(agg):
            for tx, n in sorted(agg[ds].items()):
                w.writerow([ds, tx, n, probe[ds] if tx == 'TX1' and probe[ds] else '',
                            ' | '.join(sorted(src[(ds, tx)])), notes.get(ds, '')])
    # vị trí root: tóm tắt theo ô từ vi-tri-001, cộng OPEN cho bộ không có bậc
    vt = list(csv.DictReader(open(R('results/T-021/runs/vi-tri-001/vi-tri-theo-o.csv'), encoding='utf-8')))
    tom = collections.defaultdict(lambda: collections.Counter())
    roots = collections.defaultdict(lambda: collections.defaultdict(set))
    for x in vt:
        k = (x['dataset'], x['do_thi'], x['gia_thuyet_dong_ho'])
        tom[k][(x['nhom_p75'], x['nhom_p90'])] += 1
        roots[k][(x['nhom_p75'], x['nhom_p90'])].add(x['root'])
    lech = {'RE2-TT': 'đồ thị trước mốc tiêm của từng ca (gần Q-60(b)); chỉ có cho 30 ca dev; 60 ca test suy theo root',
            'RE2-OB': 'chỉ 1 ca mẫu', 'RE3-TT': 'chỉ 1 ca mẫu',
            'Eadro-SN': 'toàn file, có cả đoạn tiêm; hub OPEN (chỉ lưu bậc root)', 'Eadro-TT': 'toàn file, có cả đoạn tiêm; hub OPEN',
            'Nezha-OB': 'phút chồng ±60 s quanh lúc tiêm; hub OPEN', 'Nezha-TT': 'phút chồng ±60 s quanh lúc tiêm; hub OPEN; hai đồng hồ khác nhau'}
    with open(os.path.join(OUT, 'vi-tri-root.csv'), 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f)
        w.writerow(['dataset', 'do_thi', 'gia_thuyet_dong_ho', 'nhom_p75', 'nhom_p90', 'so_o', 'root', 'lech_Q60b', 'nguon'])
        for k in sorted(tom):
            for (g75, g90), n in sorted(tom[k].items()):
                w.writerow([k[0], k[1], k[2], g75, g90, n, ';'.join(sorted(roots[k][(g75, g90)])),
                            lech.get(k[0], ''), 'results/T-021/runs/vi-tri-001/vi-tri-theo-o.csv'])
        for ds in ['RE3-OB', 'RE1-TT', 'OpenRCA-Bank', 'RE2-TT (60 ca test)', 'RE3-SS', 'RE2-SS', 'RE1-SS']:
            w.writerow([ds, '', '', 'OPEN', 'OPEN', '', '', 'không có bậc đã lưu; TX0 hoặc không trace', ''])


if __name__ == '__main__':
    main()
