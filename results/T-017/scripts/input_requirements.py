import csv
from pathlib import Path
header='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
base={'phuong_phap':'SimpleRCA (M4 theo mô tả bài)','vai_tro':'xếp hạng ứng viên service biết trước thời điểm',
 'tin_hieu_bat_buoc':'ít nhất một modality khả dụng; bản đủ ba nguồn cần metric+trace+log',
 'tin_hieu_tuy_chon':'các modality còn lại; thiếu ghi unavailable',
 'dinh_dang_va_ten_cot_can':'lõi nhận maps đã chia window; adapter RCAEval prepare bắt buộc bảng metric.time(seconds epoch) dù không có metric channel; metric service_metric; trace serviceName/startTime(microsecond epoch)/duration(cùng unit hai cửa sổ); log timestamp(seconds epoch)/container_name/message; aliases tường minh; chua_kiem: đơn vị vật lý duration',
 'can_do_thi':'không; không dùng parentSpanID hoặc statusCode',
 'can_moc_su_co':'adapter cần t chia normal/incident; từ injection chỉ hợp chế độ biết mốc; lõi không nhận t',
 'du_lieu_binh_thuong_toi_thieu':'metric >=2 finite/channel; trace >=1 duration/service; log fixed threshold không cần normal. Đây là tối thiểu toán học; chưa đủ hiệu chỉnh statistical false alerts',
 'can_nhan_de_hoc':'không nhãn root/fault; mốc là đầu vào known-incident; root chỉ chấm sau serialize',
 'don_vi_xep_hang':'service/entity quan sát được (union); DB giữ riêng khi chưa có alias kiến trúc; tie groups; lexical chỉ hiển thị; allzero abstain',
 'tham_so_mac_dinh_quan_trong':'metric mean+3std0; events; P95linear trace>3x; log substr ERROR/FAIL/EXCEPTION count>0; window half300s',
 'phu_thuoc_do_dai_cua_so':'có; metric event-count tăng theo length/sampling/channel; P95/log count đổi theo window; không so score thô giữa dataset',
 'chi_phi':'chua_kiem: cost/thời gian chính thức vì laptop dùng chung; scan metric cells/log chars/span values và quantiles/grouping; chạy từng ca; paper RE2TT5.99s/case khác code/hardware',
 'duong_nhan_rui_ro':'root/path/fault/Type hoặc SLI chọn theo root; injection trong self-detection; file boundary tiết lộ injection; aliases không theo root',
 'ghi_chu':'(chờ WHY, xem de-xuat-tai-lieu-chung.md); chưa xác định program sinh0.80; normal/normal thực có alert; không calibrated cause detector'}
variants=[('primary events sigma log0 half300',{}),('metric P95',{'tham_so_mac_dinh_quan_trong':'đổi metric threshold=historical P95linear; còn lại primary'}),
 ('metric channels',{'tham_so_mac_dinh_quan_trong':'mỗi metric có bất kỳ vượt ngưỡng chỉ1phiếu; còn lại primary'}),
 ('log threshold1',{'tham_so_mac_dinh_quan_trong':'log count>1; còn lại primary'}),('log threshold10',{'tham_so_mac_dinh_quan_trong':'log count>10; còn lại primary'}),
 ('trace factor2',{'tham_so_mac_dinh_quan_trong':'trace P95 incident>2x normal; còn lại primary'}),('trace factor4',{'tham_so_mac_dinh_quan_trong':'trace P95 incident>4x normal; còn lại primary'}),
 ('window half600',{'tham_so_mac_dinh_quan_trong':'normal[t-600,t),incident[t,t+600); còn lại primary'})]
rows=[]
for name,changes in variants:rows.append({**base,'bien_the':name,**changes})
for modality,required,normal,param in [('metric rule','metric time+service_metric','>=2 finite historical points/channel','mean+3std0 hoặc P95; mỗi point>threshold alert'),('trace rule','trace service+duration hai cửa sổ','>=1 span mỗi service mỗi cửa sổ','P95linear; factor3; strict>'),('log rule','log service+message cửa sổ incident','không cho fixed threshold; baseline không được dùng để hiệu chỉnh spike','ERROR/FAIL/EXCEPTION case-insensitive substring; một count/dòng; count>0')]:
    rows.append({**base,'bien_the':modality,'vai_tro':'rule tạo alert nội bộ; không là detector streaming đã đánh giá', 'tin_hieu_bat_buoc':required,'tin_hieu_tuy_chon':'không','du_lieu_binh_thuong_toi_thieu':normal,'tham_so_mac_dinh_quan_trong':param,'don_vi_xep_hang':'alert/channel hoặc service; không riêng root ranking','chi_phi':'chua_kiem: thời gian riêng chính thức; scan dữ liệu modality và quantile nếu có'})
path=Path('D:/RCA-flashticket/results/T-017/yeu-cau-dau-vao.csv')
with path.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=header);w.writeheader();w.writerows(rows)
assert len(header)==16 and all(set(r)==set(header) for r in rows)
print('rows',len(rows),'columns',len(header))
