"""Ghi nhận xét đã đọc và trình bày trung gian; số nối JSON để V8 kiểm."""
from resume_step7 import ROOT, OUT, read, write, log, sha, now
from report_support import Report, esc

def main():
    log('Đã đọc mọi bằng chứng chi tiết của 43 cặp theo danh sách: raw tại t̂, mean/std/ngưỡng và p_j N-Sigma; median/MAD và nền hằng B4; I1/I2; V7 đúng miền. Lệnh có ghi: write_manual_report.py, Python T-014-main -B. Lưu nhận xét theo ca và doc-tay, không gọi phương pháp hoặc đổi cờ.')
    run=OUT/'runs/manual-notes-001'; assert not run.exists(); run.mkdir()
    path='results/T-029/runs/manual-evidence-002/evidence.json'; e=read(ROOT/path); assert e['status']=='PASS'
    notes=[]
    for r in e['rows']:
        if r['detector']=='bocpd':
            b=r['B4_raw']['30']; s=r['intervention']['sensitivity']['5']
            if r['group']=='S':
                observation='Bản đầy đủ không có điểm đổi trong Nv, nhưng tiền tố I1 và I2 đều có. Cờ B1–B4 tại báo động đầu là N/A vì ngoài miền nền; D0 ở đây không có nghĩa đã thử và bác mọi cơ chế. Tiền xử lý tương lai có thể làm mất điểm đổi nền, không chỉ tạo điểm đổi.'
            elif r['D0']:
                observation='D0 ở cấu hình chính: điểm đổi quanh t̂ còn ở I1 và I2, B1 không trúng, B4 hữu hạn dưới ngưỡng chính. Cờ độ nhạy có thể đổi; chưa giải thích được điểm đổi ở cấu hình chính.'
            else:
                observation=('B2 đúng: cắt phần sau mốc làm điểm đổi quanh t̂ không còn trong dung sai chính. Can thiệp đổi cả min–max và bộ cột; chưa tách tác động riêng. ' if s['B2'] else 'B2 sai: I1 giữ điểm đổi quanh t̂; điều này chưa loại look-ahead bên trong tiền tố. ')
                if b['valid'] and b['flags']['3']:observation+='B4 đúng cho bước median ở cột ghi trong bảng; đây là đổi telemetry, chưa biết nền có sự cố khác hay chỉ đổi tải. '
                else:observation+='B4 chính không trúng; cột nền hằng đổi được ghi riêng, không nâng thành B4. '
                if s['B3'] is False:observation+='Hazard I2 không làm mất điểm đổi đang xét; không phủ nhận ảnh hưởng lên các điểm đổi khác.'
            alternative='Biến động tải, drift, cadence/điền trước và covariance/prior đa biến đều có thể góp phần. Không có nhãn nền sạch hoặc mốc sự cố khác để phân xử. Điểm không báo có B4 thường xuyên; không dùng tần suất đó làm lời giải thích. D và clock tuyệt đối còn OPEN.'
        else:
            observation='Các cột trong bảng thực sự vượt ngưỡng hai phía từ lịch sử đã quan sát; danh sách cột gây báo và p_j đã đối chiếu Z lưu trước nối nhãn. '
            if 'N1' in r['flags']:observation+='Tỉ lệ khoảng đầu so với khoảng cuối thỏa N1; liên hệ với vị trí sớm chưa chứng minh lịch sử ngắn là nguyên nhân. '
            if 'N2' in r['flags']:observation+='Có cột gây báo có p_j cao trong Nv; cột báo dày là phân rã trực tiếp, không là đối chứng cơ chế. '
            if 'N3' in r['flags']:observation+='Không có cột gây báo đạt N2 chính. N3 không chứng minh OR nhiều cột gây báo, độc lập hoặc đuôi phân phối. '
            if 'N4' in r['flags']:observation+='Có std quá khứ bằng không và giá trị hiện tại khác mean: ngưỡng bằng không đủ giải thích phép so số học ở cột đó; chưa giải thích vì sao telemetry đổi. '
            alternative='Lịch sử hữu hạn, nền không dừng, phân phối không chuẩn, điền trước, độ phân giải metric hoặc tải thay đổi đều chưa được tách. V7 N/A cho N1–N4 vì định nghĩa chứa điều kiện báo động. Báo động trong Nv được gọi sai theo nhãn proxy, không khẳng định hệ thực tế bình thường.'
        notes.append({'opaque_id':r['opaque_id'],'detector':r['detector'],'observation':observation,'alternative':alternative,'evidence_level':'đọc tay; liên hệ, can thiệp I1/I2 nếu áp dụng','evidence_pointer':'/rows/'+str(len(notes))})
    write(run/'notes.json',{'time':now(),'evidence':{'path':path,'sha256':sha(ROOT/path)},'rows':notes,'status':'STEP7_COMPLETE','selected_count':len(notes)})
    rp=Report('doc-tay.md',run); n=lambda ptr,spec='.6g':rp.num(path,ptr,spec)
    t=['# Đọc tay hạn chế phát hiện','',
       'Quy tắc và danh sách đã ghi trước: [selection.json](runs/manual-selection-001/selection.json), [bảng danh sách](runs/manual-selection-001/selection.md). Chọn mã mờ nhỏ nhất trong từng nhóm; lấy hợp mọi S, D0 và V7 bằng nhau đúng số. Không có ngưỡng gần bằng hoặc lựa chọn theo kết quả mong muốn.',
       '', 'Đã đọc '+n('/row_count')+' cặp thuộc '+n('/raw_case_count')+' ca. Các số dưới đây ở [evidence.json](runs/manual-evidence-002/evidence.json#/rows); nguồn telemetry, hash và con trỏ theo-ca nằm tại từng dòng JSON. Nhận xét tại [notes.json](runs/manual-notes-001/notes.json#/rows). Lượt trích đầu hỏng do kiểu đường dẫn, giữ ở manual-evidence-001; không có đầu ra khoa học thay thế.',
       '', '“Không phân biệt” dùng khi tỉ lệ đúng bằng nhau, không là kiểm định tương đương. B1 không trúng và đối chứng cũng không trúng chỉ cho biết cờ vắng. Với B4 ở cấu hình w60/k2, ca dev-16597725c1 và dev-746fd74313 có cờ ở mọi điểm không báo hợp lệ: không phân biệt, không dùng cờ này để giải thích báo động. Các cấu hình khác vẫn phải xem tỉ lệ cạnh nhau, không tự gọi phân biệt vì chưa bằng đúng số.',
       '', 'Mức bằng chứng đọc tay bổ sung việc soi trung gian; không biến liên hệ thành nhân quả. Mọi giải thích khác dưới đây là CANDIDATE/chưa kiểm, không là quyết định hoặc lỗi hệ đã xác nhận. Không đủ nhãn nền sạch, thời lượng lỗi hoặc mốc sự cố khác trong task để phân xử.']
    for i,(r,no) in enumerate(zip(e['rows'],notes)):
        p='/rows/'+str(i); t+=['','## '+r['opaque_id']+' / '+r['detector'],'',
              'Ô: '+r['cell'].replace('|',' / ')+'; nhóm '+r['group']+'; cờ chính '+('+'.join(r['flags']) or 'D0')+'. t̂='+n(p+'/t_hat')+'; t̂⁺='+n(p+'/t_hat_plus')+'.',
              '', 'Nguồn: `'+r['source']+'#/` và `theo-ca.json'+r['row_pointer']+'`; telemetry `'+r['raw_source']+'`. Lý do chọn giữ nguyên trong selection.json.', '', no['observation'],'',no['alternative']]
        if r['detector']=='bocpd':
            t+=['','| Bản chạy | Điểm đổi trong Nv |','|---|---|']
            for key in ('full','I1','I2'):t+=['| '+key+' | '+n(p+'/intervention/cp_counts_Nv/'+key)+' |']
            t+=['','| w | Cột có bước chuẩn hóa lớn nhất | Median trước | Median sau | MAD | Bước tuyệt đối | Bước chuẩn hóa | Số cột nền hằng đổi |','|---|---|---|---|---|---|---|---|']
            for w,b in r['B4_raw'].items():
                q=p+'/B4_raw/'+w
                t+=['| w'+w+' | '+(b.get('max_column') or 'N/A: ngoài miền')+' | '+' | '.join(n(q+'/'+k) if k in b else 'N/A' for k in ('before','after','mad','jump','normalized','constant_count'))+' |']
                if b.get('constant_change_columns'):t+=['','Nền hằng đổi riêng (MAD bằng không): '+', '.join(b['constant_change_columns'])+'. Không cộng vào B4.','']
            t+=['','| Cờ V7 | Tại t̂ | Điểm không báo đúng / tổng | Tỉ lệ điểm không báo |','|---|---|---|---|']
            pairs=[('B1','/B1',r['V7']['B1'])]+[(f'B4/w{w}/k{k}',f'/B4/{w}/{k}',x) for w,z in r['V7']['B4'].items() for k,x in z.items()]
            for name,tail,x in pairs:
                q=p+'/V7'+tail
                equal=x['at_first_valid'] and int(x['at_first'])*x['control_n']==x['control_true']
                t+=['| '+name+(' — không phân biệt đúng số' if equal else '')+' | '+n(q+'/at_first')+' | '+n(q+'/control_true')+'/'+n(q+'/control_n')+' | '+n(q+'/control_rate')+' |']
        else:
            t+=['', 'r_obs='+n(p+'/r_obs')+'; r_ind='+n(p+'/r_ind')+'; r_nom='+n(p+'/r_nom')+'. Độ trễ và t̂⁺ phải đọc cạnh r_obs, không coi là thời điểm bắt đầu sự cố.',
                '', '| Cột gây báo | Giá trị | Mean quá khứ | Std quá khứ | Độ lệch | Ngưỡng | p_j trong Nv |','|---|---|---|---|---|---|---|']
            for j,c in enumerate(r['trigger_raw']):
                q=p+'/trigger_raw/'+str(j)
                t+=['| '+c['column']+' | '+' | '.join(n(q+'/'+k) for k in ('value','past_mean','past_std','difference','threshold','p_j'))+' |']
            t+=['','| Khoảng lịch sử | Báo cột-giây / tổng | Tỉ lệ |','|---|---|---|']
            for interval,h in r['history'].items():
                q=p+'/history/'+esc(interval)
                t+=['| '+interval+' | '+n(q+'/so_bao_cot_giay')+'/'+n(q+'/mau_so_cot_giay')+' | '+n(q+'/ti_le')+' |']
    rp.save('\n'.join(t)); log('Bước 7 hoàn tất; danh sách được giữ trước bằng chứng. doc-tay đã ghi đầy đủ trung gian/nguồn/giải thích khác, còn V8 kiểm số cùng các báo cáo bước 8.')
    print({'status':'STEP7_COMPLETE','rows':len(notes),'bindings':len(rp.bindings)})
if __name__=='__main__':main()
