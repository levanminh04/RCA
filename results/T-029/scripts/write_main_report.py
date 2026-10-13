"""Báo cáo C1–C6 và HP-n từ số đã khóa; không chạy phương pháp."""
import statistics
from collections import Counter, defaultdict
from resume_step7 import ROOT, OUT, read, write, sha, log, now
from report_support import Report, esc

TP='results/T-029/theo-ca.json'; NP='results/T-029/n-sigma-cot.json'; BP='results/T-029/bocpd-can-thiep.json'; VP='results/T-029/runs/step5-001/V7.json'
RUN=OUT/'runs/report-main-001'; DP='results/T-029/runs/report-main-001/summary.json'
DETS=('bocpd','nsigma','nsigma_doi_chung')
NAMES={'bocpd':'BOCPD','nsigma':'N-Sigma chính','nsigma_doi_chung':'N-Sigma đối chứng'}

def derive(rows,ns,v7):
    result={'delay':{},'D0':{},'sensitivity_changes':{},'NS_descriptive':{},'V7_direction':{},'HP_cells':{}}
    cells=sorted({r['cell'] for r in rows})
    for det in DETS:
        rs=[r for r in rows if r['detector']==det]
        ds=[r['delay_seconds'] for r in rs if r['delay_seconds'] is not None]
        result['delay'][det]={'n':len(ds),'minimum':min(ds),'median':statistics.median(ds),'maximum':max(ds),'zero':sum(x==0 for x in ds)}
        result['D0'][det]={c:{'n':sum(r['cell']==c for r in rs),'count':sum(r['cell']==c and r['D0'] for r in rs)} for c in cells}
        variants={'N1/2.0':['N1/1.5','N1/3.0'],'N2/10':['N2/5','N2/20'],'N3/10':['N3/5','N3/20']} if det!='bocpd' else {'B2/5':['B2/2','B2/10'],'B3/5':['B3/2','B3/10'],'B4/w30/k3':[f'B4/w{w}/k{k}' for w in (15,30,60) for k in (2,3,5) if (w,k)!=(30,3)]}
        result['sensitivity_changes'][det]={}
        for base,others in variants.items():
            for other in others:
                differences=[{'opaque_id':r['opaque_id'],'cell':r['cell'],'base':r['flags_flat'][base],'variant':r['flags_flat'][other]} for r in rs if r['flags_flat'][base]!=r['flags_flat'][other]]
                result['sensitivity_changes'][det][other]={'base':base,'changed_count':len(differences),'n':len(rs),'changes':differences}
        if det=='bocpd':continue
        result['NS_descriptive'][det]={}
        for cell in ['all']+cells:
            cases=[r['opaque_id'] for r in rs if cell=='all' or r['cell']==cell]
            fs=[ns['cases'][o][det] for o in cases]
            types={}
            for kind in fs[0]['N5_types']:
                numerator=sum(f['N5_types'][kind]['so_bao_cot_giay'] for f in fs); denominator=sum(f['N5_types'][kind]['mau_so_cot_giay'] for f in fs)
                types[kind]={'alarm_column_seconds':numerator,'column_seconds':denominator,'rate':numerator/denominator if denominator else None}
            minutes=[]
            for i in range(len(fs[0]['N6_minutes'])):
                parts=[f['N6_minutes'][i] for f in fs]; num=sum(p['so_giay_bao'] for p in parts); den=sum(p['so_giay'] for p in parts)
                minutes.append({'from':parts[0]['tu'],'to':parts[0]['den_exclusive'],'alarm_seconds':num,'seconds':den,'rate':num/den})
            result['NS_descriptive'][det][cell]={'n':len(cases),'case_ids':cases,'r_obs_min':min(f['r_obs'] for f in fs),'r_obs_max':max(f['r_obs'] for f in fs),'types':types,'minutes':minutes}
    for scope in ('all','cell','root','fault'):
        groups=v7['aggregate']['B4/w30/k3'][scope]
        result['V7_direction'][scope]={}
        for group in groups:
            signs={}
            for name,z in v7['aggregate'].items():
                if name=='B1':continue
                q=z[scope][group]
                delta=None if q['at_first_rate'] is None else q['at_first_rate']-q['nonalarm_rate']
                signs[name]={'difference':delta,'direction':None if delta is None else '+' if delta>0 else '-' if delta<0 else '='}
            unique={x['direction'] for x in signs.values() if x['direction'] is not None}
            result['V7_direction'][scope][group]={'variants':signs,'reverses': '+' in unique and '-' in unique}
    # HP số cờ chỉ tính trên miền hợp lệ; các hàng thiết kế khai là phạm vi khảo sát.
    hp=[('HP-1','N1/2.0'),('HP-2','N2/10'),('HP-3','N3/10'),('HP-4','N4'),('HP-5','B1'),('HP-6','B2/5'),('HP-7','B3/5'),('HP-8','B4/w30/k3')]
    for code,flag in hp:
        relevant=('bocpd',) if flag.startswith('B') else DETS[1:]
        result['HP_cells'][code]={}
        for det in relevant:
            result['HP_cells'][code][det]={}
            for cell in cells:
                cs=[r for r in rows if r['detector']==det and r['cell']==cell]; vals=[r['flags_flat'][flag] for r in cs]
                result['HP_cells'][code][det][cell]={'true':sum(v is True for v in vals),'valid':sum(v is not None for v in vals),'total':len(vals),'NA':sum(v is None for v in vals)}
    return result

def main():
    log('Lệnh có ghi: write_main_report.py, Python T-014-main -B. Bước7 đã hoàn tất; tính thống kê mô tả từ JSON lưu, ghi báo cáo chính C1–C6/HP-n và nguồn số. Không sửa đầu ra bước0–6 hoặc ngưỡng.')
    assert read(OUT/'runs/manual-notes-001/notes.json')['status']=='STEP7_COMPLETE'
    assert not RUN.exists(); RUN.mkdir()
    theo=read(ROOT/TP); ns=read(ROOT/NP); v7=read(ROOT/VP); boc=read(ROOT/BP); rows=theo['rows']
    d=derive(rows,ns,v7); d['time']=now(); d['sources']={p:sha(ROOT/p) for p in (TP,NP,BP,VP)}
    write(ROOT/DP,d)
    r=Report('ban-do-han-che-phat-hien.md',RUN)
    n=lambda path,ptr,spec='.6g':r.num(path,ptr,spec)
    t=['# Bản đồ hạn chế phát hiện ở chế độ (b)','',
       'Báo động đầu thường nằm trước mốc tiêm theo nhãn proxy. BOCPD nhạy với dữ liệu sau mốc qua tiền xử lý; N-Sigma có nhiều báo động nền, nhưng các cờ chưa tách được nguyên nhân thống kê. Bước nhảy telemetry B4 cũng phổ biến ở điểm không báo. Vì vậy bản đồ dưới đây phân biệt bằng chứng can thiệp, liên hệ, đọc tay và phần chưa kiểm.',
       '', 'Phạm vi: '+n(TP,'/row_count')+' cặp, mỗi bộ '+n(TP,'/per_detector/bocpd/all/bocpd/n')+' ca dev RE2-TT. Mốc chung, lưới và các ngưỡng theo [SPEC đã khóa](../../tasks/T-029-p4-han-che-phat-hien/SPEC.md). Root/loại lỗi/ô chỉ nối sau khi [đặc trưng được lưu và băm](runs/step5-001/features-frozen.json). I1/I2/I3 dùng nhãn thời gian cho phân tích; không đổi số P3, không là đầu vào triển khai detector.',
       '', '## C1 — Thất bại ở đâu (liên hệ/mô tả)','',
       'S nghĩa là báo động đầu sau mốc; E-gần/E-xa tách theo cửa sổ RCA có chứa mốc. Miss là không có báo trong đoạn sau mốc, khác với báo động đầu sai. Độ trễ BOCPD là độ lệch vị trí điểm đổi hồi cứu. Độ trễ N-Sigma phải đặt cạnh r_obs trong Nv; báo dày từ trước mốc có thể tiếp tục qua mốc.',
       '', 'Nguồn bảng: `theo-ca.json#/per_detector/<bộ>/cell/<ô>` và `runs/report-main-001/summary.json#/delay`.',
       '', '| Bộ | S | E-gần | E-xa | Miss | Tổng | Độ trễ nhỏ nhất / trung vị / lớn nhất | Số độ trễ bằng không |','|---|---|---|---|---|---|---|---|']
    for det in DETS:
        a=theo['per_detector'][det]['all'][det]; p='/per_detector/'+det+'/all/'+det
        # Giá trị thiếu một nhóm có nghĩa số đếm bằng không, lưu qua summary để có nguồn scalar.
        for key in ('S','E-gần','E-xa'):a['first_groups'].setdefault(key,0)
        # Không sửa JSON nguồn: bảng đếm zero lưu trong report summary riêng.
        d.setdefault('groups',{})[det]={k:a['first_groups'][k] for k in ('S','E-gần','E-xa')}
    write(RUN/'groups.json',d['groups']); GP='results/T-029/runs/report-main-001/groups.json'
    for det in DETS:
        p='/per_detector/'+det+'/all/'+det; q='/delay/'+det
        t+=['| '+NAMES[det]+' | '+' | '.join(n(GP,'/'+det+'/'+key) for key in ('S','E-gần','E-xa'))+' | '+n(TP,p+'/Miss')+' | '+n(TP,p+'/n')+' | '+' / '.join(n(DP,q+'/'+key) for key in ('minimum','median','maximum'))+' | '+n(DP,q+'/zero')+' |']
    t+=['','| Bộ / ô | S | E-gần | E-xa | Miss / tổng |','|---|---|---|---|---|']
    cg={}
    for det in DETS:
        cg[det]={}
        for cell,a in theo['per_detector'][det]['cell'].items():cg[det][cell]={k:a['first_groups'].get(k,0) for k in ('S','E-gần','E-xa')}
    write(RUN/'cell-groups.json',cg); CG='results/T-029/runs/report-main-001/cell-groups.json'
    for det in DETS:
        for cell,a in theo['per_detector'][det]['cell'].items():
            p='/per_detector/'+det+'/cell/'+esc(cell)
            t+=['| '+NAMES[det]+' / '+cell.replace('|',' / ')+' | '+' | '.join(n(CG,'/'+det+'/'+esc(cell)+'/'+key) for key in ('S','E-gần','E-xa'))+' | '+n(TP,p+'/Miss')+'/'+n(TP,p+'/n')+' |']
    t+=['','### Theo từng ca: giữ mọi cặp','', 'Nguồn: `theo-ca.json#/rows/<dòng>`. Danh sách cờ là đa nhãn, không là thứ tự nguyên nhân trội. D0 ở S có thể do tất cả cờ BOCPD không có miền hợp lệ.', '',
        '| Ca | Bộ | Ô | Nhóm | t̂ | t̂⁺ | Độ trễ | Báo sai trong Nv | r_obs Nv | d | Cờ chính |','|---|---|---|---|---|---|---|---|---|---|---|']
    for i,x in enumerate(rows):
        p='/rows/'+str(i)
        t+=['| '+x['opaque_id']+' | '+NAMES[x['detector']]+' | '+x['cell'].replace('|',' / ')+' | '+x['first_group']+' | '+' | '.join(n(TP,p+'/'+k) for k in ('t_hat_index','t_hat_plus_index','delay_seconds','false_alarms_Nv_T025','r_obs_Nv','d'))+' | '+('+'.join(x['primary_flags']) or 'D0')+' |']
    t+=['','## C2 và C6 — Bản đồ hạn chế và nguồn tác giả','',
        'Bảng HP dùng số cờ đúng / cặp hợp lệ / tổng cặp, có N/A riêng. Dòng “phạm vi khảo sát” không là số ca bị lỗi. Đây là kết quả trên dev và các ngưỡng phân tích khóa trước, không là định nghĩa mới của detector.',
        '', '| Mã | Bộ / cơ chế | Mức bằng chứng | Kết luận được phép | Giải thích khác / chưa kiểm | Tác giả |','|---|---|---|---|---|']
    descriptions=[
      ('HP-1','N-Sigma / N1: lịch sử ngắn','liên hệ + đọc tay','Có tỉ lệ báo khoảng đầu cao hơn khoảng cuối ở các ca có N1.','Drift, tải và ffill có thể khác theo thời gian; chưa có can thiệp độ dài lịch sử.','BARO nêu baseline khó với chuỗi phức tạp; chưa thấy cơ chế N1 riêng trong nguồn đã khảo sát.'),
      ('HP-2','N-Sigma / N2: cột báo dày','liên hệ + đọc tay','Chỉ ra cột đóng góp vào báo động đầu; số thay mạnh theo tập cột.','p_j cao chưa tách đuôi không chuẩn, nền không dừng hoặc lịch sử hữu hạn.','[BARO, đánh giá phát hiện](https://arxiv.org/html/2405.09330v1#S4.SS5) nêu báo sai baseline; chưa thấy N2 riêng.'),
      ('HP-3','N-Sigma / N3: E không có cột báo dày tại t̂','liên hệ + đọc tay','Phần còn lại sau N2; ba tỉ lệ là mô tả.','Không chứng minh cộng dồn, độc lập hoặc phân phối chuẩn; một cột thưa cũng đủ gây báo.','Chưa thấy trong nguồn đã khảo sát; công thức OR nằm trong code/hồ sơ N-Sigma.'),
      ('HP-4','N-Sigma / N4: std bằng không','liên hệ + đọc tay','Trung gian xác nhận ngưỡng bằng không tại cột gây báo.','Độ phân giải, tải hoặc nền hằng; chưa phân xử ý nghĩa vận hành của socket.','Code tác giả có phép so này; chưa thấy tác giả nêu riêng như hạn chế trong bài đã khảo sát.'),
      ('HP-5','BOCPD / B1: đầu NaN điền không','liên hệ + đọc tay','Không có cờ B1 ở báo động đầu E của dev này.','Không kiểm mọi dạng missing hoặc tác động điền trước; B1 âm không bác ảnh hưởng thiếu dữ liệu.','Code có fillna; chưa thấy trong nguồn đã khảo sát như hạn chế thực nghiệm.'),
      ('HP-6','BOCPD / B2: dữ liệu sau mốc qua tiền xử lý','can thiệp I1 + đọc tay','Cắt sau mốc làm mất điểm đổi quanh t̂ ở các ca B2.','I1 đổi đồng thời bộ cột và min–max; vẫn nhìn dữ liệu sau t̂ trong tiền tố. B2 sai chưa loại look-ahead.','Code tiền xử lý toàn chuỗi; chưa thấy tác giả nêu hạn chế này trong nguồn đã khảo sát.'),
      ('HP-7','BOCPD / B3: hazard','can thiệp I2 + đọc tay','Không có B3 đúng trên miền được chấm. Số điểm đổi khác vẫn có thể đổi.','Chỉ kiểm trước mốc; chưa chạy toàn bản ghi với hazard khác theo giới hạn chi phí SPEC.','Hazard thay thế có trong code; chưa thấy phân tích B3 trên giao thức này trong nguồn đã khảo sát.'),
      ('HP-8','BOCPD / B4: bước nhảy telemetry trước mốc','liên hệ, V7 + đọc tay','Có bước median lớn; V7 không cho quy mọi cờ thành lời giải thích.','Nền không sạch, biến động tải, MAD nhỏ, nhiều cơ hội qua nhiều cột; chưa có nhãn nền độc lập.','[BARO, giả định đầu vào](https://arxiv.org/html/2405.09330v1#S3.SS1) nêu bất thường hiện ở latency/error; chưa thấy phân xử B4/V7 này.'),
      ('HP-9','D0: không có cờ chính','đọc tay; chưa giải thích','Không ép vào cơ chế. S và E phải tách; miền N/A không là cờ âm.','Covariance/prior, drift và bước nhỏ vẫn có thể góp phần; chưa có can thiệp phân xử chúng.','Chưa thấy trong nguồn đã khảo sát.'),
      ('HP-10','Đầu ra detector và định vị service','liên hệ / thiết kế','N-Sigma cho cột, phân tích E thêm mapping/thứ tự; BOCPD không native attribution.','Báo động kéo dài qua mốc, hòa, root hết cột; chưa chứng minh onset, nhân quả hoặc lan.','[BARO, pipeline](https://arxiv.org/html/2405.09330v1#S3.SS2) tách detector với ranker; chưa thấy rank E như đầu ra native.'),
      ('HP-11','RCA phụ thuộc điểm chạy','can thiệp I3','Chênh ghép cặp có dấu; bảng G cho kết quả có điều kiện theo ô và cohort.','Đổi cửa sổ cũng đổi nền, cột ứng viên và graph CIRCA; chưa tách riêng các đường tác động.','[BARO, độ nhạy thời điểm](https://arxiv.org/html/2405.09330v1#S4.SS8.SSS1) có nêu; chưa thấy phân rã G của T-029.'),
      ('HP-12','Nhãn proxy / thời lượng lỗi D','chưa kiểm D; liên hệ P1','Nguồn chưa xác nhận D; chưa chấm lại P/R/F1. Timeline chỉ mô tả telemetry.','Metric phục hồi không đồng nghĩa lỗi đã hết; root có cột thiếu, Nv khác cho quantile khác.','[RCAEval, tạo dữ liệu](https://arxiv.org/html/2412.17015v2#S3.SS3) mô tả mốc và thu thập; chưa thấy D cho các ca này.'),
      ('HP-13','Schema và nhãn','liên hệ P2','Không có cột đạt phân hoạch root hoàn toàn; có vắng cột liên hệ một root trong dev.','Root và loại lỗi chưa giao chéo đầy đủ; triển khai/thu thập và tổ hợp schema còn có thể giải thích.','Chưa thấy trong nguồn đã khảo sát.'),
      ('HP-14','N-Sigma / N6: nền mở rộng nhận dữ liệu sau mốc','thiết kế + mô tả; chưa kiểm nhân quả','Code nhận dữ liệu đã quan sát vào mean/std; timeline báo thay đổi mật độ.','Giảm báo có thể do phục hồi, đổi tải, ngưỡng tăng hoặc biến động cột; chưa can thiệp cố định nền.','Code tác giả, [hồ sơ N-Sigma](../T-013/ho-so-nsigma-phat-hien.md); không dùng số bài thay kết quả này.')]
    for row in descriptions:t+=['| '+' | '.join(row)+' |']
    t+=['','Nguồn tác giả đã khảo sát: bài BARO bản v1 (phần giả định, mô hình, phát hiện, độ nhạy thời điểm, giới hạn); code BARO ở revision trong [manifest T-013](../T-013/manifest.json), hồ sơ BOCPD/N-Sigma/cửa sổ; nguồn công bố RCAEval đã lưu cho P1. “Chưa thấy” chỉ áp các nguồn đã khảo sát, không là tuyên bố mọi tài liệu đều không có.',
       '', '### Số HP theo từng ô','', 'Nguồn: `runs/report-main-001/summary.json#/HP_cells`; mỗi ô = đúng / hợp lệ / tổng (N/A).', '',
       '| HP | Bộ | Ô | Đúng / hợp lệ / tổng | N/A |','|---|---|---|---|---|']
    for code,dets in d['HP_cells'].items():
        for det,cs in dets.items():
            for cell,z in cs.items():
                p='/HP_cells/'+code+'/'+det+'/'+esc(cell)
                t+=['| '+code+' | '+NAMES[det]+' | '+cell.replace('|',' / ')+' | '+' / '.join(n(DP,p+'/'+k) for k in ('true','valid','total'))+' | '+n(DP,p+'/NA')+' |']
    t+=['','| HP / Bộ | Ô | Số ca / tổng và ý nghĩa |','|---|---|---|']
    for det in DETS:
        for cell,z in d['D0'][det].items():
            p='/D0/'+det+'/'+esc(cell)
            t+=['| HP-9 / '+NAMES[det]+' | '+cell.replace('|',' / ')+' | '+n(DP,p+'/count')+'/'+n(DP,p+'/n')+' D0; xem nhóm S/E từng ca |']
    for code,det in [('HP-10','bocpd'),('HP-10','nsigma'),('HP-10','nsigma_doi_chung'),('HP-11','bocpd'),('HP-11','nsigma'),('HP-12','bocpd'),('HP-13','bocpd'),('HP-13','nsigma'),('HP-13','nsigma_doi_chung'),('HP-14','nsigma'),('HP-14','nsigma_doi_chung')]:
        for cell,z in theo['per_detector'][det]['cell'].items():
            p='/per_detector/'+det+'/cell/'+esc(cell)+'/n'
            t+=['| '+code+' / '+NAMES[det]+' | '+cell.replace('|',' / ')+' | '+n(TP,p)+'/'+n(TP,p)+' phạm vi khảo sát; không đếm tất cả là ca hỏng |']
    t+=['','### Độ nhạy cờ (mọi cấu hình đã khai)','',
       'Nguồn: `theo-ca.json#/per_detector/<bộ>/cell/<ô>/flags`. N1/N2/N3 có thể đổi tập ca; B2 đổi theo dung sai; B3 N/A khi B2 đúng; B4 đổi cả ngưỡng và miền theo w. Không chọn cấu hình có số thuận hơn. Bảng dưới giữ đủ đúng/hợp lệ/tổng và N/A theo từng ô.', '',
       '| Bộ | Ô | Cờ / cấu hình | Đúng / hợp lệ / tổng | N/A |','|---|---|---|---|']
    for det in DETS:
        for cell,z in theo['per_detector'][det]['cell'].items():
            for flag,a in z['flags'].items():
                if (det=='bocpd')!=flag.startswith('B'):continue
                p='/per_detector/'+det+'/cell/'+esc(cell)+'/flags/'+esc(flag)
                # Hợp lệ là tổng đúng+sai, lưu riêng để scalar có nguồn.
                d.setdefault('valid_flag_counts',{}).setdefault(det,{}).setdefault(cell,{})[flag]=a['true']+a['false']
    write(RUN/'valid-counts.json',d['valid_flag_counts']); VC='results/T-029/runs/report-main-001/valid-counts.json'
    for det in DETS:
        for cell,z in theo['per_detector'][det]['cell'].items():
            for flag,a in z['flags'].items():
                if (det=='bocpd')!=flag.startswith('B'):continue
                p='/per_detector/'+det+'/cell/'+esc(cell)
                t+=['| '+NAMES[det]+' | '+cell.replace('|',' / ')+' | '+flag+' | '+n(TP,p+'/flags/'+esc(flag)+'/true')+'/'+n(VC,'/'+det+'/'+esc(cell)+'/'+esc(flag))+'/'+n(TP,p+'/n')+' | '+n(TP,p+'/flags/'+esc(flag)+'/NA')+' |']
    t+=['','### Những ca đổi cờ khi thay cấu hình','', 'Nguồn: `summary.json#/sensitivity_changes`. “Đổi” bao gồm True/False và miền N/A; bảng chỉ ghi khác biệt, danh sách đầy đủ cờ nằm ở theo-ca.json.', '',
        '| Bộ | Cấu hình so với chính | Ca đổi / tổng | Mã ca và chuyển trạng thái |','|---|---|---|---|']
    for det,vs in d['sensitivity_changes'].items():
        for flag,q in vs.items():
            p='/sensitivity_changes/'+det+'/'+esc(flag)
            details='; '.join(x['opaque_id']+': '+str(x['base'])+' → '+str(x['variant']) for x in q['changes']) or 'Không đổi'
            t+=['| '+NAMES[det]+' | '+flag+' so '+q['base']+' | '+n(DP,p+'/changed_count')+'/'+n(DP,p+'/n')+' | '+details+' |']
    t+=['','### V7: báo động cạnh điểm không báo','',
       'B1 chỉ xét cửa sổ quanh i nằm trong Nv. B4 chỉ xét đủ MAD và hai cửa sổ nằm trong nền, cùng miền cho báo động và đối chứng. Mẫu số báo động là ca có t̂ hợp lệ; mẫu số đối chứng là điểm không báo trong miền của từng w. Các ca S vẫn có điểm đối chứng nền nhưng không có t̂ hợp lệ; hai quần thể này không đồng nhất. Đây là tỉ lệ mô tả, không là kiểm định thống kê. N1–N4, B2/B3 V7 N/A vì chứa điều kiện báo động.',
       '', 'Nguồn: `runs/step5-001/V7.json#/aggregate/<cấu hình>/{all,cell}/<nhóm>`.', '',
       '| Phạm vi | Cờ | Đúng tại t̂ / ca hợp lệ | Tỉ lệ tại t̂ | Đúng đối chứng / điểm hợp lệ | Tỉ lệ đối chứng |','|---|---|---|---|---|---|']
    for flag,z in v7['aggregate'].items():
        for scope in ('all','cell'):
            for group,q in z[scope].items():
                p='/aggregate/'+esc(flag)+'/'+scope+'/'+esc(group)
                t+=['| '+group.replace('|',' / ')+' | '+flag+(' — không phân biệt đúng số' if q['rates_exactly_equal'] else '')+' | '+n(VP,p+'/at_first_true')+'/'+n(VP,p+'/at_first_n')+' | '+n(VP,p+'/at_first_rate')+' | '+n(VP,p+'/nonalarm_true')+'/'+n(VP,p+'/nonalarm_n')+' | '+n(VP,p+'/nonalarm_rate')+' |']
    t+=['','Ở cấu hình chính B4, tỉ lệ tại t̂ cao hơn tỉ lệ đối chứng toàn mẫu; điều đó chưa phân xử cơ chế. Khi hạ ngưỡng ở w30/k2, dấu chênh toàn mẫu âm. Các ô có thể khác dấu; bảng tiếp giữ mọi hướng và mọi đổi chiều đã khai. Cờ phổ biến ở điểm không báo không tự thành lời giải thích. Những ca bằng nhau đúng số đã được đọc tay, gồm B4/w60/k2 ở dev-16597725c1 và dev-746fd74313; xem doc-tay.', '',
        '| Phạm vi | Nhóm | Cấu hình B4 | Chênh tỉ lệ tại t̂ − đối chứng | Hướng |','|---|---|---|---|---|']
    for scope,groups in d['V7_direction'].items():
        for group,z in groups.items():
            for flag,q in z['variants'].items():
                p='/V7_direction/'+scope+'/'+esc(group)+'/variants/'+esc(flag)
                t+=['| '+scope+' | '+group.replace('|',' / ')+(' — có đổi chiều' if z['reverses'] else '')+' | '+flag+' | '+n(DP,p+'/difference','+.6g')+' | '+str(q['direction'] or 'N/A')+' |']
    t+=['','### N5/N6: mô tả theo ca và ô','',
       'Nguồn: `n-sigma-cot.json#/cases/<ca>/<bộ>` và `summary.json#/NS_descriptive`. r_obs/r_ind/r_nom không tách nhân quả. r_obs≈r_ind chưa chứng minh độc lập; r_ind khác r_nom có nhiều giải thích. N5 phân loại từ hậu tố; mạng rỗng không chứng minh không có telemetry mạng vì socket/diskio/workload thuộc “khác”. N6 là mật độ từng phút sau mốc; code nền mở rộng hấp thu mọi dữ liệu đã thấy, nhưng giảm báo chưa chứng minh hấp thu gây bỏ sót.', '',
       '| Ca | Bộ | r_obs | r_ind | r_nom | Tỉ lệ lịch sử đầu / giữa / cuối | Loại cột gây báo |','|---|---|---|---|---|---|---|']
    for oid,z in ns['cases'].items():
        for det,f in z.items():
            p='/cases/'+oid+'/'+det
            t+=['| '+oid+' | '+NAMES[det]+' | '+' | '.join(n(NP,p+'/'+k) for k in ('r_obs','r_ind','r_nom'))+' | '+' / '.join(n(NP,p+'/history/'+a+'/ti_le') for a in ('100:200','200:400','400:720'))+' | '+', '.join(f['trigger_types'])+' |']
    t+=['','| Bộ / ô | Loại cột | Báo cột-giây / tổng cột-giây | Tỉ lệ |','|---|---|---|---|']
    for det,groups in d['NS_descriptive'].items():
        for group,z in groups.items():
            for kind,q in z['types'].items():
                p='/NS_descriptive/'+det+'/'+esc(group)+'/types/'+kind
                t+=['| '+NAMES[det]+' / '+group.replace('|',' / ')+' | '+kind+' | '+n(DP,p+'/alarm_column_seconds')+'/'+n(DP,p+'/column_seconds')+' | '+n(DP,p+'/rate')+' |']
    t+=['','| Bộ / ô | Đoạn sau mốc | Giây báo / tổng giây ca | Mật độ báo |','|---|---|---|---|']
    for det,groups in d['NS_descriptive'].items():
        for group,z in groups.items():
            for i,q in enumerate(z['minutes']):
                p='/NS_descriptive/'+det+'/'+esc(group)+'/minutes/'+str(i)
                t+=['| '+NAMES[det]+' / '+group.replace('|',' / ')+' | ['+n(DP,p+'/from')+', '+n(DP,p+'/to')+') | '+n(DP,p+'/alarm_seconds')+'/'+n(DP,p+'/seconds')+' | '+n(DP,p+'/rate')+' |']
    t+=['','Số từng phút từng ca nằm trong `n-sigma-cot.json#/cases/<ca>/<bộ>/N6_minutes`; không gộp phút cuối ngắn thành một phút đầy đủ. Đường cong quan sát có thể giảm hoặc tăng trở lại; chưa có D độc lập để gọi đoạn sau là bình thường.', '',
       '### B5 và I1/I2: số chiều, số điểm đổi theo ca','', 'Nguồn: `bocpd-can-thiep.json#/cases/<ca>`. d có thể đi cùng root/schema và prior; bảng này không quy tác động riêng cho dimension.', '',
       '| Ô | Ca | d | Điểm đổi Nv đầy đủ | I1 | I2 |','|---|---|---|---|---|---|']
    for oid,q in boc['cases'].items():
        p='/cases/'+oid
        t+=['| '+q['cell'].replace('|',' / ')+' | '+oid+' | '+n(BP,p+'/d')+' | '+' | '.join(n(BP,p+'/cp_counts_Nv/'+k) for k in ('full','I1','I2'))+' |']
    t+=['','## C3 — Có chỉ ra vùng không','',
       '**Liên hệ/thiết kế.** [Định vị](dinh-vi.md) giữ từng ca, từng ô, mức nền ngẫu nhiên đều và mọi độ nhạy bỏ cột N2. N-Sigma cung cấp danh sách cột, còn xếp dịch vụ là phân tích thêm mapping. Thứ tự báo động đầu sau mốc chưa phải khởi phát; loại N2 không loại mọi báo động kéo qua mốc. BOCPD không chỉ ra cột hoặc service; bảng bước nhảy tại t̂⁺ là heuristic (quy tắc phân tích), không là output BOCPD. Không kết luận nhân quả, lan hoặc giá trị đồ thị từ bảng này.',
       '', '## C4 — Phụ thuộc mốc biết trước','',
       '**Can thiệp I3.** [Bảng G](a-so-b.md) so ghép cặp Hit@1/Hit@5 ở mốc, t̂⁺ và t̂, giữ non-OK trong mẫu số, TORAI từng seed/ca và CIRCA vượt ngưỡng từng điểm. Δ cửa sổ = Hit(t̂⁺) − Hit(a); Δ sự kiện = Hit(t̂) − Hit(t̂⁺). Dấu âm/dương đều được giữ. I3 chọn nhờ nhãn mốc, không là cận trên hoặc xác nhận lỗi thật. Các chênh đổi cửa sổ còn đổi nền, graph và ứng viên; không là phân xử hai nguyên nhân độc lập.',
       '', 'Kết luận phụ thuộc cohort: bảng G có trường hợp CIRCA DA/BOCPD chênh sự kiện Hit@5 dương trên toàn mẫu nhưng âm ở cohort không vượt tại mọi điểm. Trung bình bằng nhau cũng có thể có ca lên và ca xuống; đọc các bảng ghép cặp thay vì gọi “không ảnh hưởng”.',
       '', '## C5 — Nhãn proxy và schema','',
       '**P1 liên hệ; D chưa kiểm.** [Nhãn proxy và schema](nhan-proxy-va-schema.md) giữ timeline ngoài quantile / cột đủ, đủ/tổng và danh sách thiếu ở cả Nv. Nguồn chưa xác nhận D. Không suy D từ telemetry để chấm lại P/R/F1; số T-025 giữ theo proxy đã khai. Median quay về vùng nền chưa chứng minh lỗi kết thúc.',
       '', '**P2 liên hệ.** Không có cột tách root hoàn toàn theo định nghĩa khóa, nhưng schema vẫn liên hệ một phần với root trong dev. Root và fault chưa giao chéo đầy đủ; không thể quy riêng cho chúng hoặc phủ nhận thông tin trong tổ hợp schema. Không đưa dấu vắng vào phương pháp.',
       '', '## Giới hạn và trạng thái','',
       'Không có số công bố về phát hiện trên cùng RE2-TT và giao thức window để tái lập trực tiếp. Nguồn BARO là đối chiếu định tính. V1–V7 đã có kiểm từ các lượt lưu và hash tiếp nhận; V8 và kiểm V1 cuối được lưu trong lượt kiểm cuối báo cáo. [Đọc tay](doc-tay.md) giữ nguồn, trung gian, mọi S/D0 và ca V7 không phân biệt đúng số.',
       '', 'OPEN: D, clock tuyệt đối, nền sạch và nhãn mốc sự cố thật; ảnh hưởng hazard lên đoạn sau mốc chưa kiểm vì SPEC không chạy toàn bản ghi với hazard khác. Phạm vi chỉ là dev, bản ghi đã chọn vì có sự cố, nền cố định của SPEC. Không áp cho test, dataset giữ ngoài, Nezha, online hoặc nền khác. Không thiết kế P5/P6 ở task này; các phần sau chỉ trỏ HP-n. Chưa phản biện thay Claude hoặc tự đóng task.']
    r.save('\n'.join(t)); log('Báo cáo chính đã ghi đủ C1–C6, HP-n, theo ô/ca/độ nhạy/V7/N5/N6/B5; còn V8 độc lập và kiểm phạm vi cuối. Phần khối prompt G2 dừng riêng vì nguồn không có G2, chờ Minh.')
    print({'status':'WRITTEN','bindings':len(r.bindings)})
if __name__=='__main__':main()
