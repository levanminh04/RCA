"""Root synthesis of audited intermediate evidence; no method execution."""
from pathlib import Path
import csv, json, shutil
from collections import Counter

ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'results/T-020'
MID=OUT/'trung-gian'

def rows(path):
    with path.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def write(name,rs):
    with (OUT/name).open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)

def availability(name):
    # Availability is at the explicitly inspected part, not the entire release.
    if name in ['RE1-SS','RE2-SS','RE3-SS']:
        return {'metric':'có','trace':'không','log':'không' if name=='RE1-SS' else 'có'}
    if name in ['RE1-TT','RE1-OB']:
        return dict(metric='có theo file inventory; schema chưa kiểm',trace='không',log='không')
    if name=='BARO-FSE-OB':
        return dict(metric='có',trace='không',log='không')
    if name.startswith(('RE2-TT','RE2-OB','RE3-TT')):
        return dict(metric='có',trace='có',log='có một phần' if name=='RE2-TT' else 'có')
    if name=='RE3-OB': return dict(metric='chưa kiểm',trace='chưa kiểm',log='chưa kiểm')
    if 'metric ngày' in name: return dict(metric='có',trace='không trong phần này',log='không trong phần này')
    if 'trace+log' in name: return dict(metric='không resource metric trong phần này',trace='có',log='có')
    if name.startswith('DeepTraLog'): return dict(metric='không resource metric',trace='event graph' if 'processed' in name else 'có',log='có')
    if name.startswith(('Eadro','AnoMod','FSE fault')): return dict(metric='có',trace='có',log='có')
    if name.startswith('LEMMA'):
        return dict(metric='có' if 'sample' in name else 'chưa kiểm',trace='không' if 'sample' in name else 'chưa kiểm',log='có' if 'sample' in name else 'chưa kiểm')
    return dict(metric='chưa kiểm',trace='chưa kiểm',log='chưa kiểm')

def main():
    for source,target in [
        ('dataset_evidence/01-bang-tieu-chi-hop-nhat.csv','01-bang-tieu-chi-hop-nhat.csv'),
        ('dataset_evidence/01-bang-tieu-chi-hop-nhat.md','01-bang-tieu-chi-hop-nhat.md'),
        ('exposure_ledger/02-so-ca-da-nhin.csv','02-so-ca-da-nhin.csv'),
        ('exposure_ledger/02-so-ca-da-nhin.md','02-so-ca-da-nhin.md'),
        ('dataset_evidence/03-task-cham-duoc-va-che-do-b.md','03-task-cham-duoc-va-che-do-b.md'),
        ('method_evidence/yeu-cau-hop-nhat.csv','yeu-cau-dau-vao-hop-nhat.csv'),
        ('method_evidence/07-checklist-doc-nhanh.md','07-danh-sach-phuong-phap-va-doc-nhanh.md'),
    ]: shutil.copyfile(MID/source,OUT/target)
    criteria=rows(OUT/'01-bang-tieu-chi-hop-nhat.csv')
    requirements=rows(OUT/'yeu-cau-dau-vao-hop-nhat.csv')
    assert all(all(str(v).strip() for v in x.values()) for x in criteria)
    assert len(requirements)==42
    matrix=[]
    for i,req in enumerate(requirements):
        method=req['phuong_phap'];variant=req['bien_the'];needed=req['tin_hieu_bat_buoc']
        if method.startswith(('MicroRank','TraceRCA','Detector trace')) or (method.startswith('SimpleRCA') and variant=='trace rule'): need=['trace']
        elif method.startswith('SimpleRCA') and variant=='log rule':need=['log']
        elif method.startswith('SimpleRCA') and variant=='metric rule':need=['metric']
        elif method.startswith('SimpleRCA'):need=['metric','trace','log']
        elif method.startswith('DecompRCA — bộ xếp'):need=[]
        elif method.startswith('TORAI'):need=['metric','log']
        else:need=['metric']
        for ds in criteria:
            have=availability(ds['dataset'])
            impossible=[x for x in need if have[x].startswith('không')]
            unknown=[x for x in need if have[x] in ['chưa kiểm','event graph']]
            status='cần adapter'
            reason='định danh/time/cadence và numeric schema; tách label khỏi features; chưa chạy trên phần mới'
            if impossible:
                if method.startswith('TORAI') and impossible==['log']:
                    reason='metric adapter; truyền logts chỉ time theo fallback đã kiểm; đây là TORAI thiếu log, phải tách điều kiện'
                elif method.startswith('SimpleRCA') and variant not in ['trace rule','log rule']:
                    reason='bản giảm modality, ghi rõ nguồn thiếu; không gọi là bản đủ ba tín hiệu; root ceiling vẫn kiểm'
                elif impossible==['metric'] and have['trace']=='có':
                    reason='CANDIDATE: tạo chuỗi latency/error từ trace không dùng nhãn; đổi loại bằng chứng, chưa kiểm; không thay metric tài nguyên'
                else:
                    status='không chạy được';reason='thiếu tín hiệu bắt buộc: '+', '.join(impossible)+' trong phần này; không suy thêm root/cạnh từ label'
            if unknown and status!='không chạy được':
                status='chưa kiểm';reason='schema/chất lượng bắt buộc chưa đọc; MRP §4 chốt cách chia ở G1 trước khi chạy phương pháp trên dữ liệu mới'
            if 'gốc' in variant or 'goc:' in variant or 'empirical SVR' in variant or method.startswith('DecompRCA'):
                if status!='không chạy được':
                    status='chưa kiểm';reason+='; hồ sơ gốc/biến thể chưa có pipeline thực trên bộ này'
            if method.startswith('GDN') and "report='best'" in variant:
                reason+='; default dùng testlabels chọn threshold: chỉ tái lập, không là baseline blind hợp lệ'
            if method.startswith('GDN') and "report='val'" in variant:
                reason+='; vẫn chuẩn hóa test tương lai trong code; sửa train/val-only riêng, chưa đủ hiệu chỉnh'
            if 'đề xuất chế độ b' in variant:
                reason+='; diagnostic b chưa đạt false-alarm normal, không suy ready từ fixed columns'
            if method=='CIRCA' and 'Kiến trúc' in variant:
                reason+='; cần graph kiến trúc từ inventory/config độc lập gold hoặc trace normal; thiếu nguồn graph thì chưa có bản kiến trúc hợp lệ, không tạo cạnh từ nhãn'
            if 'schema chưa kiểm' in have['metric'] and 'metric' in need and status!='không chạy được':
                status='chưa kiểm';reason+='; file inventory không chứng minh metric schema/cadence/normal của release chưa mở'
            root='OPEN: phải kiểm source root-mapping/candidate theo từng ca ở P3; không chèn root từ label; nếu vắng thì Hit@k trần=0'
            if status=='không chạy được':root='không có output đúng bài toán của cặp này; không tính Hit@k'
            effort='thấp: rename/unit/time' if ds['family']=='RCAEval' else 'vừa–cao: parse/link/clock/schema; CANDIDATE chưa kiểm'
            if status=='không chạy được':effort='không khắc phục chỉ bằng adapter định dạng'
            budget='quan sát: '+req['chi_phi']+'; tổng bộ×seed xem runtime.csv và phụ lục10; bộ mới chưa kiểm; Q40=10800s tổng, không mỗi seed'
            matrix.append(dict(id=f'M{i+1:02d}',phuong_phap=method,bien_the=variant,dataset=ds['dataset'],trang_thai=status,
                ly_do=reason,tin_hieu_can=needed,tin_hieu_co=json.dumps(have,ensure_ascii=False),
                adapter=reason,cong_suc=effort,suy_khong_nhan='CANDIDATE: id/time/unit từ telemetry; root alias chỉ từ inventory độc lập, không dùng gold; cần kiểm P3',
                don_vi_xep_hang=req['don_vi_xep_hang'],normal_can=req['du_lieu_binh_thuong_toi_thieu'],normal_co=ds['C8'],
                tap_ung_vien_va_tran_Hit=root,biet_moc_hay_tu_phat_hien=req['can_moc_su_co'],nhan_hoc=req['can_nhan_de_hoc'],
                dieu_kien_cham='Tách mode a/b; root gold chỉ evaluator, không fit/tune bằng testlabels; D4 đề xuất mốc ngoài cho mode a, Minh cần làm rõ ngân sách time-label test với MRP §4; mode b không crop/inject/filename/future stats. Không xếp chung khác điều kiện.',
                chi_phi_tong=budget,khi_gia_dinh_sai='thiếu id/kind/pod/parent, clock không đồng bộ, normal quá ngắn, root vắng/cột hằng; P3 kiểm adapter trên dev đã duyệt',
                nguon=req['source']+'; '+ds['sources']))
    write('04-phuong-phap-x-dataset.csv',matrix)
    counts=Counter(x['trang_thai'] for x in matrix)
    text=f'''# Ma trận phương pháp × phần dữ liệu — CANDIDATE, chưa duyệt\n\n{len(requirements)} dòng yêu cầu gốc × {len(criteria)} phần dữ liệu = {len(matrix)} cặp. [CSV đầy đủ](04-phuong-phap-x-dataset.csv) có nguồn, tín hiệu cần/có, normal, đơn vị, candidate ceiling, label budget và công sức từng cặp. Không có ô “chạy nguyên trạng”: kiểm chạy trong hồ sơ thường dùng adapter, nên không đồng nhất với raw dataset. Phân loại hiện tại: {dict(counts)}.\n\n“Cần adapter” xác nhận tín hiệu của phần đã xem và mô tả đường chuyển không dùng nhãn; **chưa bảo đảm pipeline mới đã chạy**. “Chưa kiểm” có giả định, trường hợp sai và việc P3 cần làm; không dùng chữ “có file” để suy schema. “Không chạy được” chỉ trong phần tín hiệu đã chỉ định. Không thêm trace giả cho Sock Shop. Chuỗi request latency tạo từ trace là tín hiệu dẫn xuất, không thành metric tài nguyên cùng điều kiện.\n\nHai hàng DecompRCA chỉ là prior work đã đọc để bàn Retrieval; không thêm vào danh sách RCA đã duyệt. GDN là detector, không RCA. SimpleRCA các rule đơn lẻ là alert nội bộ, không detector streaming đã xác lập.\n\n## Header và chua_kiem\n\nSáu bảng nguồn đều giữ 16 cột nghiệp vụ và bốn cột provenance. Không có header mismatch. {sum(x['chua_kiem_preserved']=='True' for x in requirements)} hàng có chua_kiem trong nguồn được giữ nguyên. Mỗi giá trị nguyên bản nằm ở [yêu cầu hợp nhất](yeu-cau-dau-vao-hop-nhat.csv); không điền minimum statistical calibration bằng số dòng chạy được.\n\n## Nhãn và tập ứng viên\n\nKhông dùng root gold để thêm một node bị vắng hoặc chọn SLI. P3 cần lập tập metric→service, operation→service, graph-node→service từ telemetry/inventory không nhãn. Báo số ca gold có mặt trước khi accuracy; vắng gold thì Hit@k trần 0. Không có candidate universe đã đo đầy đủ cho các release chưa mở. Root-level mapping ở [bảng V4](trung-gian/dataset_evidence/root-mapping.csv) là evidence/OPEN, không quyết định schema.\n\n## Chi phí\n\nCột riêng giữ số quan sát và tính chất phép đo. [Runtime đã có](trung-gian/method_evidence/runtime.csv), [nhãn/cửa sổ](05-nhan-va-cua-so.md) và [kế hoạch P3](10-ke-hoach-p3-de-xuat.md) quy ngân sách toàn bộ×seed. Không dùng chi phí làm điểm chọn dataset. Không lấp ô bằng lượt chạy mới trong T020.\n'''
    (OUT/'04-phuong-phap-x-dataset.md').write_text(text,encoding='utf-8')
    (OUT/'runs/matrix-assertions.json').write_text(json.dumps({'requirements':len(requirements),'dataset_parts':len(criteria),'pairs':len(matrix),'statuses':dict(counts),'headers_match':True,'criteria_no_blank':True},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('matrix',len(matrix),dict(counts))

if __name__=='__main__':main()
