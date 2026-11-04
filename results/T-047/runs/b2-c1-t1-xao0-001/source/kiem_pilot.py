"""Soi pilot, đối chiếu trực tiếp T-046, dự báo chưa kiểm cho toàn gói."""
import json
from pathlib import Path
import adapter_t047 as ad


def main():
    p = ad.OUT / 'runs/b1-pilot-001'
    rows = []
    for d in sorted((p / 'cases').iterdir()):
        s = json.loads((d / 'summary.json').read_text(encoding='utf-8'))
        q = json.loads((d / 'qt5.json').read_text(encoding='utf-8'))[0]
        old = json.loads((ad.ROOT / 'results/T-046/runs/b10-kiem-src-001/ca' / (d.name+'.json')).read_text(encoding='utf-8'))
        oq = old['cua_so']['that|R0']['QT5']
        diff = {k: [v, q.get(k)] for k, v in oq.items() if v != q.get(k)}
        flags = {k: q[k] for k in ('diem_lon_hon_1e6', 'toan_hoa', 'so_nguong_cuc_lon') if q[k]}
        if (q['nhom_chiem'] or 0) > .9:
            flags['nhom_chiem'] = q['nhom_chiem']
        rows.append(dict(dataset=s['dataset'], oid=d.name, seconds=s['seconds'], peak_rss=s['peak_rss'],
                         qt5=q, difference_T046=diff, flags=flags))
    # Thời gian K cũ gồm 16 cấu hình/ca, đã kiểm theo manifest; cộng chi phí G3 là ứng viên mô hình.
    old_k = {}
    for name in ('b2b-k16-re2-001', 'b2b-k16-re2-mocgia-001', 'b5-k16-nezha-001'):
        paths = list((ad.ROOT / 'results/T-045/runs' / name / 'ca').glob('*/progress.jsonl'))
        vals = [json.loads(x.read_text(encoding='utf-8').splitlines()[-1]) for x in paths]
        old_k[name] = dict(n=len(vals), sum_seconds=sum(v['giay_nap']+v['giay_pha1'] for v in vals))
    byds = {x['dataset']: x for x in rows}
    r, n = byds['RE2-TT']['seconds'], byds['Nezha-OB']['seconds']
    t1_cpu = 4*(30*r+22*n)+30*r
    # G3 metric dùng chung; E1 đổi op, E2 thêm edge; không phải 16 lần độc lập.
    # Đây là dự báo chưa kiểm; dùng thêm 3 R0/ca làm phần tăng G3 và 4 giây khởi động/job.
    old_cpu = sum(x['sum_seconds'] for x in old_k.values())
    k_cpu = old_cpu+3*(60*r+22*n)
    pred = dict(workers=2, t1_seconds=(t1_cpu+238*4)/2,
                K_seconds=(k_cpu+82*4)/2, postprocess_seconds=1800,
                status='CHUA_KIEM', total_seconds=(t1_cpu+238*4+k_cpu+82*4)/2+1800+236.719,
                assumptions=['Thời gian pilot đại diện trung bình; ca lớn có thể lâu hơn.',
                             'Cache giữ qua 16 cấu hình cùng ca; phần tăng G3 mô hình hóa bằng thêm 3 R0/ca trên thời gian K cũ.',
                             'Khối K chưa đo bằng code mới; cập nhật dự báo theo tiến độ thật, vượt 7h thì dừng.'],
                can_be_wrong=['E3/cache hoặc ca lớn tốn hơn mô hình; paging hay giảm tốc khi RAM thiếu.'],
                dependent='Khả năng hoàn tất trong ngân sách, không dùng để kết luận RCA.')
    out = dict(pilot=rows, old_K_runtime=old_k, projection=pred,
               PASS=all(not x['difference_T046'] and not x['flags'] for x in rows))
    ad.ghi(p / 'kiem-pilot.json', out)
    print(json.dumps({k: v for k, v in out.items() if k != 'pilot'}, ensure_ascii=False, indent=1))
    if not out['PASS'] or pred['total_seconds'] > 7*3600:
        raise SystemExit('STOP pilot/dự báo')


if __name__ == '__main__':
    main()
