"""Record actual downloads and approved inspection scope without reading locked data."""
import datetime, json
from pathlib import Path

R=Path(__file__).resolve().parents[3]
B=R/'results/T-003'
def read(p): return json.loads((R/p).read_text(encoding='utf-8-sig'))
def write(p,t): (R/p).write_text(t,encoding='utf-8')

def main():
    out=B/'runs/resources-final-001';out.mkdir(parents=True,exist_ok=False)
    specs=[('Nezha','T-008','download-001'),('Eadro','T-009','download-001'),
           ('DeepTraLog base','T-010','download-002'),('DeepTraLog all-log','T-010','download-003'),
           ('LEMMA IT sample','T-011','download-001')]
    rows=[]
    for name,task,run in specs:
        p=f'results/{task}/runs/{run}/manifest.json';m=read(p)
        assert all(x['status']=='ok' and x['actual_bytes']==x['bytes'] for x in m['items'])
        rows.append(dict(dataset=name,manifest=p,files=len(m['items']),download_bytes=sum(x['actual_bytes'] for x in m['items']),elapsed_seconds=m.get('elapsed_seconds')))
    total=sum(x['download_bytes'] for x in rows);assert total==5477786503
    inv=read('results/T-009/runs/inspect-004/nested-inventory.json')
    sizes={origin:sum(x['bytes'] for x in inv if x['origin']==origin) for origin in {x['origin'] for x in inv}}
    counts={origin:sum(x['origin']==origin for x in inv) for origin in sizes}
    logical=sum(x['bytes'] for x in inv)
    old=read('results/T-003/runs/sizes-summary-001/summary.json')
    # This is a logical all-member expansion, not an observed filesystem footprint.
    expansion=dict(nezha=3038134642,eadro_final_member_occurrences=logical,
        deep_base=7517863017,deep_alllog=3085469085,lemma=17500872729)
    report=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),downloads=rows,
        download_bytes=total,source_inventory_bytes=5264569871,conditional_alllog_bytes=213216632,
        eadro_final_member_bytes_by_origin=sizes,eadro_final_member_counts_by_origin=counts,
        logical_expansion=expansion,logical_expanded_bytes=sum(expansion.values()),
        caveat='Eadro counts representations including repeated files. Deep base size from directory inventory; CRC confirms members. Streamed inspections do not materialize this expansion. Archives, duplicate combined ZIP copies, scratch and allocation blocks are separate.',
        previous_directory_inventory='results/T-003/runs/sizes-summary-001/summary.json',
        extra_source_request_bytes_not_in_payload_total='metadata/source snapshots, range/index requests, failed attempts and rehash reads are separately recorded by their run manifests')
    (out/'summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    table='\n'.join(f"| {x['dataset']} | {x['files']} | {x['download_bytes']:,} | {x['elapsed_seconds']} |" for x in rows)
    write('results/T-003/dung-luong-tai-va-giai-nen.md',f'''# Dung lượng thực và cách xử lý T-003

Đã tải đúng gói Q-47 và phần all-log có điều kiện của DeepTraLog. Tổng payload dataset: **{total:,} byte (5,478 GB thập phân)**. Đây không phải tổng lưu lượng mạng mọi request. Nguồn, từng file, byte/hash và thời gian: [tổng kiểm](runs/resources-final-001/summary.json) và các download manifest được dẫn trong đó. Các lần thử lỗi vẫn giữ.

| Phần | File tải | Byte thực | Thời gian download của run (giây) |
|---|---:|---:|---:|
{table}

## Sau giải nén

| Phần | Byte nội dung member | Phạm vi |
|---|---:|---|
| Nezha | 3.038.134.642 | CSV không nén, không cộng bản giải nén lần nữa |
| Eadro | {logical:,} | File cuối CSV/JSON trong outer và nested; không gồm TAR header/padding, có biểu diễn trùng |
| DeepTraLog base | 7.517.863.017 | Raw/normal và graph: [mục lục](runs/sizes-001/archive-index-results.json), CRC và parsing ở T-010 |
| DeepTraLog all-log | 3.085.469.085 | Một member log, đọc tới EOF/CRC đạt: [inspect-007](../T-010/runs/inspect-007/summary.json) |
| LEMMA bốn ZIP IT | 17.500.872.729 | 2.431 member đọc tới EOF/CRC đạt: [báo cáo](../T-011/kiem-file.md) |

Tổng logical theo biểu diễn: {sum(expansion.values()):,} byte. Đây là lượng nội dung qua decompressor; **không phải số byte đang chiếm đĩa**, cũng không phải số quan sát độc lập. Eadro nested trùng outer được chứng minh bằng hash; không cộng chúng thành sự cố mới. Kiểm bằng streaming nên không cần ghi toàn bộ nội dung ra đĩa. Lượt mục lục cũ dùng Eadro TAR làm cận trên ở [sizes-summary-001](runs/sizes-summary-001/summary.json); số file cuối ở bảng này thay cận trên đó cho đúng scope đã kiểm.

## Hai máy, thời gian và giữ dữ liệu

Nezha/Eadro lưu laptop trong data/ngoai-rcaeval/. DeepTraLog/LEMMA lưu EC2 mới 3.26.62.217, /home/ubuntu/rca-t003/data/. Không dùng instance T-007. ZIP nguồn còn giữ; Deep có bản ZIP ghép trung gian nên cần cộng riêng khi đo đĩa. Không tải Original LEMMA hoặc OT, không tải telemetry Bank. [Kế hoạch/phạm vi đã thực hiện](ke-hoach-kiem-file.md) và [hướng dẫn dựng lại](../../data/README.md).

Thời gian kiểm thực được ghi riêng trong từng run: [Nezha](../T-008/the-dataset.md), [Eadro](../T-009/the-dataset.md), [DeepTraLog](../T-010/the-dataset.md), [LEMMA](../T-011/kiem-file.md). Các bước chồng thời gian, lần sửa tái dùng kết quả và lượt dừng không được cộng thành benchmark throughput toàn dataset. Chưa có số tiền AWS thực từ billing; không gán ước lượng thành chi phí hóa đơn. EC2 vẫn chạy, không tự Stop/terminate hoặc xóa sau khảo sát. Mục đích tải là kiểm file thật cho thẻ và cho phản biện tái lập, chưa chọn dataset thí nghiệm.
''')
    write('results/T-003/de-xuat-phan-bo-ec2.md','''# Bố trí đã thực hiện theo Q-47

EC2 mới 3.26.62.217/key2 dành cho DeepTraLog và LEMMA IT mẫu tại /home/ubuntu/rca-t003/{data,scripts,results}/. Nezha và Eadro ở laptop. Không dùng IP 3.104.124.160 của T-007. Báo cáo preflight cũ ec2-preflight-2026-10-03.json mô tả instance cũ, giữ lịch sử và không dùng làm năng lực máy mới.

Máy mới được kiểm SSH/df/free trước tải: root còn38.226.227.200byte, RAM8.153.149.440byte, không swap; bằng chứng trong LOG parent mục kiểm instance mới. Key2 đã sửa ACL theo quyền Minh, không ghi nội dung key. Host fingerprint của preflight chưa được đối chiếu qua AWS độc lập. Không cài môi trường RCA/training.

Các ZIP/CSV nguồn được giữ, kiểm bằng streaming; kết quả/script/hash chép về repo. [Dung lượng thực](dung-luong-tai-va-giai-nen.md) phân biệt logical expansion và dung lượng đĩa. Không tự dọn sau khảo sát, không mở Bank/locked. Chưa Stop/terminate EC2; Minh quyết thao tác dọn/Stop sau khi xem kết quả. Chi phí tiền thực cần AWS billing, chưa đo trong task.
''')

if __name__=='__main__':main()
