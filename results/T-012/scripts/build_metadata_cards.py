"""Rebuild metadata-only cards, inventory and source/label matrix from saved inputs."""
import hashlib,json,re
from pathlib import Path

B=Path(__file__).resolve().parents[1]
R1='runs/run-001/sources/'
R2='runs/run-002/sources/'
def link(name,path):return f'[{name}]({path})'
def main():
    if (B/'runs/cards-review-003/validation.json').exists():
        raise RuntimeError('Source-only checkpoint builder superseded: use write_review_cards.py with saved baseline and a fresh run ID.')
    profiles=json.loads((B/'profiles.json').read_text(encoding='utf-8'))
    records=[]
    for p in sorted((B/R2).glob('zenodo-*-latest.json')):
        d=json.loads(p.read_text(encoding='utf-8'));m=d['metadata'];files=d.get('files',[])
        records.append({'requested_record':int(p.name.split('-')[1]),'resolved_record':d['id'],'doi':d.get('doi'),'publication_date':m.get('publication_date'),'version_field':m.get('version'),'license':m.get('license'),'files':[{'key':f['key'],'bytes':f['size'],'checksum':f.get('checksum')} for f in files],'file_bytes_sum':sum(f['size'] for f in files),'source':p.relative_to(B).as_posix()})
    (B/'runs/run-002/record-summary.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    headings=['Danh tính, nguồn và phạm vi đã kiểm','Bảng chung tiêu chí 1–9','Nhãn, số ca và khả năng phân xử','Schema thật và chất lượng ba nguồn tín hiệu','Dữ liệu bình thường và mốc thời gian','Ước lượng thô triệu chứng lan — tiêu chí 7','Task nào chấm được bằng nhãn hiện có?','Rò nhãn và thông tin phục vụ G1','Kích thước và chi phí','Những điều còn mở']
    out=['# Thẻ dataset 2025–2026 — khảo sát nguồn có giới hạn','Ngày truy cập 03/10/2026. Hoàn tất thẻ trong phạm vi **nguồn/metadata**, không phải hoàn tất kiểm chất lượng dữ liệu. Tất cả biến thể dưới đây: telemetry đã tải = 0 byte; số ca thực đọc telemetry = 0. Không đọc dữ liệu khóa hoặc hàng Bank. FACT nguồn chỉ xác nhận điều tài liệu công bố. Không chuyển thành FACT file. Q-47 cho phép chọn bảo toàn và chấp nhận phần chất lượng chưa xác minh; quyết định của gói xem WHY, không lấy thẻ này thay quyết định.','Nguồn và revision: [manifest mới](runs/run-002/source-manifest.json), [manifest cũ](runs/run-001/source-manifest.json), [record summary tính lại](runs/run-002/record-summary.json). [Sổ tìm](search-ledger.md) ghi giới hạn truy vấn; [lineage](independence-matrix.md) xét đủ các trục; [kế hoạch kiểm](inspection-plan.md) giữ nguyên giới hạn metadata.']
    matrix=['# Ma trận nguồn, nhãn và task — T-012','Các số là số công bố hoặc metadata, chưa phải census archive. Không dùng số query làm số incident.','| Biến thể | Root/time/trace theo nguồn | Xếp hạng | Phát hiện thời gian / trace | Vùng | License | Nguồn |','|---|---|---|---|---|---|---|']
    for p in profiles:
        src='; '.join(link(x['name'],x['path']) for x in p['sources'])
        out+=['',f"# {p['name']}"]
        content=[
          f"FACT nguồn: {p['identity']}\n\nNguồn: {src}.\n\nGiấy phép dữ liệu/code: {p['license']}\n\n{p['version']} Dữ liệu đã có/được phép/đã kiểm: không tải telemetry trong T-012; không quyết quyền đọc qua thẻ. Không có census file để suy tổng incident.",
          '| Tiêu chí | Kết quả và giới hạn |\n|---|---|\n'+ '\n'.join(f'| {i+1} | {x} |' for i,x in enumerate([p['access'],p['labels'],p['trace'],p['modalities'],p['positions'],p['faults'],'OPEN — chưa kiểm số đo; không suy lan từ mô tả bài.',p['normal'],p['independence']]))+f'\n\nNguồn cho bảng: {src}.',
          f"{p['counts']}\n\nRoot × fault × repetition/date: **OPEN — chưa có census nhãn riêng của đúng artifact**. {p['census_reason']} Không lấy archive, số trace, số query hoặc số test API thay số incident RCA.\n\nVị trí root/bậc vào–ra raw, số node/cạnh, root có mặt: OPEN vì chưa mở trace. Cùng testbed không bảo đảm cùng đồ thị; root vắng trace không tự là node cô lập.",
          f"Schema công bố: {p['schema']}\n\n{p['trace']} {p['modalities']}\n\nSchema file thật, số span/root sentinel/parent cần resolve/unique-parent/missing-parent/ambiguous-parent: OPEN; không có mẫu số nên không tính tỷ lệ. Metric cadence/gap/NaN/constant/trùng/đơn vị/clock và log ID cột/payload/ghép trace đều chưa đo. Code/schema công bố không thay quan sát file thật.",
          f"{p['normal']}\n\n{p['time']} Thời gian trước/sau, độ dài normal và recovery theo ca/kênh: OPEN. Một timestamp hay tên cửa sổ không chứng minh đồng hồ khớp; nhãn tiêm không tự là onset/end quan sát được.",
          'OPEN — chưa kiểm. Không tải số đo trong lượt khảo sát nguồn này; với họ Bank, bảo toàn theo quyết định gói tới G3. Không chạy q=.95/.99/.995, không có OR hay tỷ lệ kênh bất thường ngoài root. Tải chung, thay đổi workload, sai đồng hồ và lỗi collector đều là giải thích khả thi khác nếu sau này quan sát đồng thời nhiều service bất thường.',
          '| Task | Chấm được đến đâu theo nguồn |\n|---|---|\n'+f"| Xếp hạng | {p['ranking']} |\n| Phát hiện thời gian | {p['detection']} |\n| Vùng ảnh hưởng | {p['region']} |\n| Bất thường trace | {p['trace_task']} |\n\nCác khả năng có điều kiện chỉ dùng nhãn ở bước chấm. Khả năng học có giám sát, ngân sách nhãn và baseline chạy được còn OPEN; chưa chạy phương pháp RCA.",
          f"{p['leakage']}\n\n{p['independence']} Chưa thiết kế adapter hoặc chia dev/test. Nhãn/tên ca/mốc lỗi chỉ dùng census/chấm; không làm đầu vào detector tự phát hiện. Với OpenRCA, query có thể cho sẵn khoảng và số lỗi; không coi protocol query đó là phát hiện liên tục không biết trước số lỗi.",
          f"{p['size']}\n\nNguồn byte archive: [record summary](runs/run-002/record-summary.json); từng checksum/revision trong manifest. Chi phí giải nén/RAM/thời gian đọc mẫu/adapter: OPEN, không suy từ dung lượng nén hoặc yêu cầu chạy agent LLM. Telemetry tải ở T-012 bằng 0; chi phí nguồn được ghi ở manifest.",
          '| Điều còn mở | Vì sao / đầu vào cần | Người và kết luận phụ thuộc |\n|---|---|---|\n'+f"| Nhãn/census và nguồn release | {p['census_reason']} | Codex khi gói được giao kiểm file; giới hạn số ca, RQ1/RQ3 |\n| Chất lượng trace/metric/log, normal, clock | Không mở telemetry trong phạm vi nguồn; cần đúng release và quyền đọc | Codex sau quyền phù hợp; Bank sau G3 |\n| Độc lập | {p['independence']} | G1: nguồn injector/collector/reuse; không tự đạt tiêu chí 9 |\n| Ràng buộc nguồn riêng | {p['open']} | Chủ nguồn cung cấp làm rõ; Codex ghi bằng chứng; Minh quyết sử dụng |\n\nPhạm vi bằng chứng: danh tính/provenance/tài liệu và metadata công khai. Chưa phân xử chất lượng tín hiệu hay lợi ích đồ thị; không kết luận dataset thắng/thua từ phần chưa đo."
        ]
        for i,(h,c) in enumerate(zip(headings,content),1):out +=[f'## {i}. {h}',c]
        matrix.append('| '+' | '.join([p['name'],p['labels']+' '+p['trace'],p['ranking'],p['detection']+' '+p['trace_task'],p['region'],p['license'],src])+' |')
    (B/'the-dataset.md').write_text('\n\n'.join(out)+'\n',encoding='utf-8')
    (B/'task-and-source-matrix.md').write_text('\n\n'.join(matrix[:3])+'\n'+'\n'.join(matrix[3:])+'\n',encoding='utf-8')
    checks={'profiles':len(profiles),'headings_per_profile':10,'all_source_paths_exist':all((B/x['path']).exists() for p in profiles for x in p['sources']),'telemetry_bytes_downloaded':0,'telemetry_cases_read':0,'latest_record_ids':{str(x['requested_record']):x['resolved_record'] for x in records}}
    (B/'runs/run-002/card-validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(checks,ensure_ascii=False))
if __name__=='__main__':main()
