"""Produce human readable numerical examples from saved result files only."""
import json,csv,math
from pathlib import Path
import pandas as pd
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-013'
s=json.loads((OUT/'kiem-tra.json').read_text(encoding='utf-8'));run=Path(s['run_dir']).resolve()
def fmt(x):return f'{float(x):.10g}'
def mapping(ranks,kind):
    out=[]
    for m in ranks:
        v=m.split('_')[0];v=v.replace('-db','') if kind=='RE' else v
        if v not in out:out.append(v)
    return out
lines=['# Ví dụ tính tay — hai ca chọn trước khi nhìn kết quả','',f'Nguồn mọi số: `{run.relative_to(ROOT)}`; run được trỏ bởi `kiem-tra.json`. Code independent/official ở `scripts/kiem_co_che.py`; file CSV ghi từng metric, quantile/mean/std/scale và điểm. MốcA dùng lại T-006, không benchmark toàn dataset. Mọi thời gian chỉ tham khảo trên máy bận.','', '## 1. Quy tắc và đầu vào','']
for c in s['selection']['selected']:
    lines += [f"- {c['tag']}: `{c['case']}`, shape {c['shape']}; chọn theo rule SPEC. Timestamp injection {c['inject_time']} cùng đơn vị giây với time. Nhãn root chỉ nối sau khi lưu ranks."]
lines += ['', 'TT là metrics.parquet lớn nhất trong30ca dev, không phải ca có tổng metrics+trace lớn nhất củaT-005. OB trùng hash mẫuREADME (một bản trùng); không chọn vì rank đẹp. Hash trong chon-ca/manifest. Rule ca/mapping dùng để minh họa **chờ WHY, xem de-xuat-tai-lieu-chung.md**.', '', '## 2. Tính RobustScorer và N-Sigma từng bước','']
aggregation=[]
for tag in ['TT','OB']:
    lab=json.loads((run/(tag+'-labels-after-rank.json')).read_text(encoding='utf-8'));root=next(iter(lab.values()))['root']
    lines += ['',f'### {tag}: vì sao root (service gốc) `{root}` đứng ở hạng đó','', '| Window/scorer | Metric | median hoặc mean | IQR hoặc std | scale hiệu dụng | max hậu | điểm |','|---|---|---:|---:|---:|---:|---:|']
    for length in [10,20]:
        for scorer in ['robust','standard']:
            key=f'{tag}-L{length}-{scorer}';df=pd.read_csv(run/(key+'-metric.csv'));ranks=json.loads((run/(key+'-ranks.json')).read_text(encoding='utf-8'))['ranks']
            rootrows=df[df.metric.str.split('_').str[0]==root].sort_values('score',ascending=False);rootmetric=rootrows.iloc[0]
            selected=pd.concat([df.nlargest(2,'score'),rootrows.head(1)]).drop_duplicates('metric')
            for _,r in selected.iterrows():
                center=r['median'] if scorer=='robust' else r['mean']
                lines.append(f"| {length}/{scorer} | {r.metric} | {fmt(center)} | {fmt(r.scale_raw)} | {fmt(r.scale_effective)} | {fmt(r.max_post)} | {fmt(r.score)} |")
            for kind in ['BR','RE']:
                sr=mapping(ranks,kind);pos=sr.index(root)+1
                aggregation.append({'case':tag,'length':length,'scorer':scorer,'mapping':kind,'root':root,'best_root_metric':rootmetric.metric,'best_root_score':float(rootmetric.score),'root_service_rank':pos,'higher_services':pos-1,'candidate_services':len(sr),'top5':';'.join(sr[:5])})
    table=[r for r in aggregation if r['case']==tag and r['mapping']=='BR']
    lines += ['', '| Window/scorer | Root service rank | Số service đứng trước | Metric thắng của root | Điểm root |','|---|---:|---:|---|---:|']
    for r in table:lines.append(f"| {r['length']}/{r['scorer']} | {r['root_service_rank']} | {r['higher_services']} | {r['best_root_metric']} | {fmt(r['best_root_score'])} |")
    ex=pd.read_csv(run/(f'{tag}-L10-robust-metric.csv')).nlargest(1,'score').iloc[0]
    lines += ['',f"Ví dụ thế số metric đầu RobustScorer L10: ({fmt(ex.max_post)} − {fmt(ex['median'])})/{fmt(ex.scale_effective)} = {fmt(ex.score)}. Vì sort giảm rồi bỏ trùng service, root đứng sau đúng số service trong bảng. Đây là lý do số học của thứ hạng, chưa chứng minh service đứng đầu là nguyên nhân thật."]
    if tag=='TT':lines += ['', 'Ở caTT này, nhiều latency service khác lệch mạnh hơn metric củaauth. Khả năng khác gồm latency nền rất nhỏ, symptom/tải đổi, thiếu metric phản ánh lỗi tạiroot hoặc loại cột hằng; task không xác minh lan truyền/nhân quả. Không gọi thứ hạng này là bằng chứng đồ thị có ích.']
    else:lines += ['', 'Ở OB L10 N-Sigma, recommendationservice_mem có nền std rất nhỏ nên lên trước cartservice; RobustScorer giữ cartservice đầu. Đổi L20 thay nền/cực đại và N-Sigma đưa cartservice lên đầu. Điều này có thể do gai nền, xu thế hoặc snapshot, không tự chứng minh tính khái quát của một scorer.']
lines += ['', '## 3. Nối mốc A của OB','']
a=pd.read_csv(run/'OB-README-A-cut243-metric.csv').nlargest(5,'score')
lines += ['Cùng bytes mẫuREADME, tiền xử lýread_data tương đương khi không cắt quanh injection; dùng điểm243 đã được T-006 tái lập BOCPD. T-013 không chạy lại BOCPD fullOB, chỉ tính lại từng điểm ranker độc lập tại243. Đây là điểm đầu được detector trả, không phải mốc injection360 trong file.','', '| Hạng metric | Metric | Điểm độc lập=official |','|---:|---|---:|']
for i,(_,r) in enumerate(a.iterrows(),1):lines.append(f'| {i} | {r.metric} | {fmt(r.score)} |')
lines += ['', 'Top5 metric trùngREADME. Gộp service làm checkoutservice hạng1, cartservice hạng2; lỗiCPU ởcartservice không có nghĩa metricCPU phải cao nhất. Avg@5=0.86 mốcA tập lấy từ `trung-gian/T006-moc-A-reused.json`; không tính Avg@5 toàn tập từ ví dụ này.','', '## 4. BOCPD: một bước posterior và hai prefix thật','']
lines += ['Với prior một chiều, x1=0: density=0.3535533906; mass đổi đoạn=0.007071067812, mass kéo dài=0.3464823228; chia tổng trở thành q1=(0.02,0.98). Giá trị chính xác trong check `hand-prior-density`. Với ca đa biến, cùng công thức mass/normalization; dimension và x1 khác nên density khác, posterior bước1 vẫn(q0,q1)=(0.02,0.98) nếu hữu hạn.','', '| Ca prefix | T | d sau preprocessing | Sai số posterior max | cps official=independent |','|---|---:|---:|---:|---|']
ns_summaries=[]
for tag in ['TT','OB']:
    c=next(x for x in s['checks'] if x['check']==tag+'-prefix120-bocpd')
    lines.append(f"| {tag} | {c['T']} | {c['normalized_dims']} | {fmt(c['posterior_max_abs_error'])} | {c['anomalies']} |")
lines += ['', 'Hai prefix lấy120 dòng đầu, trước injection. Chỉ điểm120 là sentinel ngoài0..119; không có changepoint trongrange. NPZ lưu toànR official/independent, detailJSON lưu maxes và modeposterior cuối. Raw code không có nhánh fallback xếp cột; trả điểm này do lỗiindex, không vì phát hiện được nguyên nhân. Synthetic đổi gầnbiên/hazard khác cũng kiểm, không suy từ12điểm rằng detector bỏ sót toànbộ dữ liệu.','', '## 5. N-Sigma phát hiện: thế số trên từng ca','', '| Ca/metric tại điểm100 | value | mean quá khứ | sample std | 3std | hit |','|---|---:|---:|---:|---:|---|']
for tag in ['TT','OB']:
    df=pd.read_csv(run/(tag+'-nsigma-detail.csv'));finite=df[(df.i==100)&df.std_ddof1.notna()].iloc[0]
    lines.append(f"| {tag}/{finite.metric} | {fmt(finite.value)} | {fmt(finite['mean'])} | {fmt(finite.std_ddof1)} | {fmt(finite.threshold)} | {bool(finite.hit)} |")
    c=next(x for x in s['checks'] if x['check']==tag+'-nsigma-full')
    ns_summaries += ['',f"{tag}: list {c['count']} alarm, {c['distinct']} timestamp phân biệt. Điểm đầu list {fmt(c['first_list'])}; thời điểm sớm nhất {fmt(c['earliest_time'])}. Official và independent trùng từng phần tử; đảo cột giữ multiset nhưng đổi list.",'']
lines += ns_summaries
lines += ['Synthetic hai cột: list[108,100], đảo cột[100,108]; không truyền list[0] thẳng làm mốc sớm nhất. Chuỗi periodic normal200điểm có0alarm; rawshort≤100 có0alarm. Trong đoạn trước injection thật có thể vẫn có gai/tải/missing; “trước tiêm” là proxy nền, không nhãn chứng minh mọi điểm hoàn toàn bình thường.','', '## 6. Invariant và các phép kiểm không đạt','']
core=[x for x in s['checks'] if 'rank_matches' in x and x['check'].startswith(('TT-','OB-'))]
err=max(x['max_normalized_score_error'] for x in core)
lines += [f"Các CSV hai ca khớp từng điểm, sai số normalized lớn nhất{fmt(err)}. Hai codeBR/RE và lặp lại khớp trong cấu hình đã nêu. Đảo cột giữ điểm; hòa có thể đổi vị trí nên không khẳng định rankinvariance tuyệt đối. Normal-normal vẫn córank và điểm lớn; không gán nó là nguyên nhân có nghĩa. Xem kiem-tra.json để kiểm từng invariant, kể cả lỗi/NaN/[] và sentinel; không đánh dấu mọi test là PASS chỉ vì lệnh chạy hết."]
(OUT/'vi-du-tinh-tay.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
pd.DataFrame(aggregation).to_csv(OUT/'trung-gian/service-rank-ca.csv',index=False,encoding='utf-8-sig')

header='phuong_phap,bien_the,vai_tro,tin_hieu_bat_buoc,tin_hieu_tuy_chon,dinh_dang_va_ten_cot_can,can_do_thi,can_moc_su_co,du_lieu_binh_thuong_toi_thieu,can_nhan_de_hoc,don_vi_xep_hang,tham_so_mac_dinh_quan_trong,phu_thuoc_do_dai_cua_so,chi_phi,duong_nhan_rui_ro,ghi_chu'.split(',')
rows=[
 ['BARO','BR DataFrame RobustScorer','RCA','metric numeric','không','time + service_metric; suffix _mem đổi MB','không','cần điểm tách; injection chỉ chế độ a hoặc detector hợp lệ','nền/hậu >=2 và metric không hằng mỗi nửa để còn candidate; đủ thống kê chưa tác giả bảo đảm','không','metric; gộp service bằng max/dedup','RobustScaler median IQR25-75; dk=False; max signed','median/IQR/max post/tập cột đổi','quantile nền + O(dT); nhẹ hơn BOCPD','mốc injection/window/biên; anomalies index khác timestamp','đã khớp từng điểm hai ca; chưa chốt cửa sổP3'],
 ['BARO','RE DataFrame baro','RCA','metric numeric','không','time + service_metric; dataset khácNone để preprocess thông thường','không','cần điểm tách; injection chế độa','>=2 mỗi nửa để không bị bỏ hằng; nửa rỗng lỗi','không','metric; main service dedup và bỏ -db','dataset=None không preprocess; dk=False; signed max','baseline/max/candidate đổi','quantile nền + O(dT)','runner SLI từroot không được hàm đọc; injection/window/biên','dataset=None có thể ranktime; không có detector trong hàm'],
 ['BARO','BR dict fast path','RCA','dict metric -> [timestamp,value]','không','timestamp numeric cùng đơn vị injection; key metric_service mapping','không','inject_time bắt buộc','>=4 mẫu trước; >=1 mẫu sau; codebỏ metric thiếu','không','metric; scores trả trực tiếp','upper median; quartile index; abs(max-med); IQR0->1','index quantiles và maxpost đổi','sort O(sum n_j log n_j)','mốc/time/path upstream','khác DataFrame và công thức hai phía; synthetic đã kiểm; chưa chạy dict trên toàn caTT'],
 ['N-Sigma','BR/RE RCA','RCA đối chứng','metric numeric','không','như DataFrame BARO; cùng branch dataset','không','cần điểm tách, chế độa hoặc detector hợp lệ','>=2 mỗi nửa còn cột biến thiên; không có ngưỡng đủ statistically bảo đảm','không','metric -> service max/dedup','StandardScaler ddof0; max signed; không k','mean/std/max/candidate đổi','O(dT) sau tiền xử lý','injection/window/biên và inputmapping','khác detector abs/ddof1; đã khớp từng điểm hai ca'],
 ['BOCPD','BR bocpd wrapper','phát hiện điểm đổi','metric latency/error numeric; khôngmatch thì fallbackmọicột','metric numeric khác qua fallback','cột chứa latency hoặc _error; index mapping và cadence rõ','không','raw không cần; tái lập reproduce cắt quanhinjection','không warmup khai báo; cần T>=2 có cột khônghằng; đủ nền normal chưa bảo đảm','không','không xếp hạng; cps chỉsố dòng','hazard1/50; nu=d+1 kappa1 mu0 S=I; |diff mode|>1','minmax/prior/covariance/T²/biên đổi','runtime tổng O(sum T_i²d_i³); peak tuần tự O(max(T_i²+T_id_i²))','futureminmax; injection-cut; symmetric boundaries','prefixposterior đãkhớp; sentinelT là lỗi; fullTT khôngrun>1h'],
 ['N-Sigma','BR nsigma detector','phát hiện bất thường','time và mọi metric numeric','không','đúng cột time; data thứtựtime; không autonormalize','không','raw không; runnerw300 có injection','T>=101 mặc định; mỗi mean/std cần >=2 mẫu hợp lệ; representativenormal OPEN','không','khôngrank; listtimestamp theo metric; cótrùng','k3 startsfrom100; past expanding; std ddof1; abs >3std','cửa sổrecording và lịch sử nền đổi','O(dT²); input O(dT), alarm O(dT)','injectioncut/symmetric boundary; fullwindownormalizeupstream','fullhai ca khớplist; đổi cột giữset/multiset nhưng đổi list; sortedset là runner']]
with (OUT/'yeu-cau-dau-vao.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.writer(f);w.writerow(header);w.writerows(rows)
print('Generated numerical examples, service aggregation and exact 16-column input CSV.')
