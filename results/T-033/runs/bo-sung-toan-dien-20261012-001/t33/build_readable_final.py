"""Human-readable complete report, preserving earlier progress/final drafts."""
import datetime,hashlib,json,pathlib
P=pathlib.Path(__file__).resolve().parent;ROOT=P.parents[4];e=json.loads((P/'engine-final-summary-001.json').read_text());assert e['status']=='COMPLETE' and e['counts']=={'PASS':240};inputsource=json.loads((ROOT/'results/T-033/runs/checkpoint-handoff-001/artifacts/inputs/source.json').read_text());proxy={x['opaque_id']:x['proxy'] for x in inputsource['cases']};br=['prior_df4','prior_kappa4','prior_precision4','causal_fixed','causal_expanding','compressed_row','compressed_calendar'];cases=[];times=[];pairs=[]
for ci in range(1,31):
 rows={x['branch']:x for x in e['slots'] if x['case']==ci};oid=rows[br[0]]['opaque_id'];x=rows[br[0]];cases.append('|'+ '|'.join(map(str,[ci,oid.removeprefix('dev-'),x['X_shape'][1],rows['causal_fixed']['X_shape'][1],x['native_CP_count']]+[rows[b]['CP_count'] for b in br]+[rows['compressed_row']['input_row_count']]))+'|')
 def delta(t):return 'N/A' if t is None else str(int(t-proxy[oid]))
 ts=[rows[br[0]]['first_native_alarm_time']]+[rows[b]['first_branch_alarm_time'] for b in br];times.append('|'+ '|'.join([str(ci),oid.removeprefix('dev-')]+[delta(t) for t in ts])+'|')
 cr=next(x for x in e['paired_diagnostics'] if x['case']==ci and x['a']=='compressed_row');cf=next(x for x in e['paired_diagnostics'] if x['case']==ci and x['a']=='causal_fixed');pairs.append('|'+ '|'.join(map(str,[ci,len(cr['CP_set_a_only']),len(cr['CP_set_b_only']),len(cf['CP_set_a_only']),len(cf['CP_set_b_only'])]))+'|')
report='''# T033 — báo cáo bổ sung đầy đủ, bản004

Ngày13/10/2026. Tính toán đã hoàn tất; bản002/003 vẫn giữ để truy lịch sử. Báo cáo này thay bản003 về cách diễn đạt, bổ sung bảng đủ30ca và giới hạn so thời điểm báo đầu. Đây là hỗ trợ người làm; không là phản biện chính thức, nghiệm thuG2 hay quyết định chọnP6.

**Đã xử lý đủ các phép kiểm được khai trong gói bổ sung:** K1–K7, gồm cửa sổ trace/log/workload, N-Sigma history/OR/missing, theta thiếu, prior/marginal channels, hai ca underflow, causal preprocessing, đầu vào bậc thang, probe đồ thị và toàn đường congD. Engine có30native shams+210nhánh=240/240PASS. EC2T33 làm ca1–14; EC2T32 làm ca15–30. Không mở test/locked/archive, sửa kết quả cũ hoặc chọn thuật toán bằng nhãn.

Nguồn số chính là `engine-final-summary-001.json`; mỗi ca×nhánh có source pointer, hash, tập cờ thêm/bớt và thời điểm. `engine-input-verification-all30-001.json` kiểm exact210ma trận đầu vào và30bản copy của native arrays. Native shams giữ m/CP exact; summary không chạy lại posterior. Ledger theo câu hỏi ở `ledger-final-004.json`; nguồn cũ được pin bằng catalog/manifest tương ứng.

## K1/K5: đọc được nhiều outcome hơn, chưa có chuẩn vận hành độc lập

Đã so trước/sau10,30,60giây ở toàn bộ điểm/đối chứng hiện hữu trong177cặp khóa. Duration mean gộp theo count; không cộng median hoặc distinct-per-second như độ đo cả đoạn. Mọi cửa sổ giữ raw workload, missing, trace/log count và entity/time. Source: `dev-*--context.json#/windows` và `/channel_metadata`. Các cửa sổ chồng nhau không là mẫu độc lập.

Đã đọc toàn message trong union±60giây:29ca có log và một caN/A. Có2.281.140row,35.242template classes theo ca; grouping thay timestamp/UUID/hexID/số chỉ phục vụ đọc lớp. Token success/error/exception/failed không tự là số request/sự cố. Source: `dev-*--log-semantics.json`; mọi lớp được giữ, không chỉ hai mẫu first/last.

Outcome tồn tại tại các vị trí cụ thể:

- Access log ở `ts-ui-dashboard`:65.581row, gồm65.544HTTP200,28HTTP500,9HTTP503. Method/path/status/time/source-row/hash được giữ trong29NPZ; có bảng từng cửa sổ ở `log-semantics-summary-001.json#/cases/*/windows`.
- Backend log:364.032occurrence `Response(status=...,msg=...,data=...)`, gồm336.754literal status1 và27.278status0. Có46.404serialized ResponseEntity với literalHTTP200. Source: `backend-status-summary-001.json` và29gzip literal records; giữ container/logger/operation prefix/header/row/time/hash. Đây là occurrence/logrow, không mặc nhiên request hay giao dịch duy nhất.

Đã tìm nguồn công khai để hiểu0/1. Response tại commit TrainTicket đã pin ghi1=true,0=false. Trong cùng nguồn, query order có danh sáchnull/rỗng trả0 với `Order is Null.` hoặc `Seat is Null.`. Seat logger in ResponseEntity nhận từ calleeorder; outcome nằm trong logcaller không mặc nhiên là kết quả chínhcalleroperation. Vì vậy business-result0 có thể là không tìm thấy dữ liệu, không chứng minh lỗi hạ tầng. Source và links: `backend-semantics-source-check-001.md`, `backend-primary-sources-002/manifest.json`.

Gap còn lại là **deployment provenance**: HFrevision/rawhash đã pin nhưng không xác định sourcecommit/containerdigest của hệ đã thu log. Literal logger khớp nguồn2021 không chứng minh cùng deployedrevision; bản công khai mới hơn còn đổi logformat. Do đó giải thích convention là có điều kiện theo nguồn, còn benchmark vẫn giữ literal mã/msg và trạng thái chưa xác minh convention. Không dùng “UNKNOWN” để che phầnpubliccode đã đọc.

Kênh/vị trí thiếu được tách rõ: source log chỉ có timestamp/container/message; trong vùng đã đọc không có correlation key/token thuộc parser đã khai. UI không có literaltraceentity tương ứng và65.581accessrow có0span candidate khi chỉ nối literalentity+cùnggiây. Coarse entity/time không phải invocationjoin; cả một candidate cũng chưa đủ xác nhận. Backend outcome cũng chưa có certified trace/span join. `log-correlation-summary-001.json` giữ mọi ca và giới hạn. Không viết “dataset không có outcome ở bất kỳ đâu”, không gán UIstatus cho mọi internalspan.

Literal HTTP200, INFO hay business-status1 không xác nhận toàn hệ khỏe. HTTP500/503 quan sát cũng không tự cho onset/root/cause. Vẫn thiếu chuẩn onset có tác động, negative được kiểm độc lập, faultoff/recovery, clockoffset và sampling/drop/heartbeat completeness. Những dữ kiện chưa ghi không được tạo ra bằng detector threshold hoặc cùng một telemetry window. FlashTicket cần giữ chúng cùng request/transaction outcome và trace/span/correlation links.

Kiểm nguồn/conservation đã có: `root-log-companion-verification-001.json` cho accesslog; `backend-source-verification-001.json` đối chiếu đủ364.032literal occurrences với raw row/offset/hash/time/container/status/msg và cửa sổ. Audit độc lập có file/scope riêng; không đồng nhất selfcheck với phản biện chính thức.

## K2: history/OR có tác động tính toán, chưa chọn history tốt nhất

Giữ x native, bộ cột, k=3, bắt đầu100 và ddof1. Rolling dùng100row/time-slot quá khứ, không phải100finite observations. Bộ hẹp có first-post-proxy sớm hơn18ca, bằng7, muộn hơn5; bộ rộng bằng30/30 trong điều kiện đã có cờ tại proxy. Bằng first-time không có nghĩa toàn đường cờ bằng nhau. Source: `fast-summary-001.json#/nsigma`; từngca giữ cờ thêm/bớt, std0/missing và joint flags trong context.

Đã tính OR/jointcolumn counts thay vì giả định cột độc lập hoặc dùngm×Gaussian-tail như sự thật.60finite-count companions ghi128.687evaluation cells có count<100, gồm121.028cells cócount<2; pandas skipNaN và std ddof1 cần ít nhất2giá trị hữu hạn. Source: `rolling-finite-counts-summary-001.json` và60NPZ. Std0 giữ native strictthreshold semantics; NaN không tự là errorflag. Các cells/cột/giây cùng ca không là đơn vị thử độc lập.

Các contrast trả lời history/aggregation đi vào phép tính thế nào. Chúng không xác nhận Gaussian/stationarity, falsealarm vận hành, lượng hóa docollector hoặc rolling là lựa chọn tối ưu. Chọn history/k/SLI/aggregation choP6 cần causalbaseline và protocol phù hợp với loại nhãn thực có.

## K3: prior, kênh và trạng thái tích lũy

Đã phục hồi120sourceNPZ tại607sourcepoint unique. Nguồn có150BOCPDunits/664unitpoints,57references lặp;160theta-absent unitpoints là157unique đã phục hồi đủ. State trước(i,r) là prior cập nhật nguyên thứ tự X[i−r:i];5.200saved state fields exact. SelectedPDF, normalizer/MAP/CP giữ nguồnexact. Algebra logpdf dùng bound1e−10 khai trước; sai số lớn nhất8,81×10⁻¹³. Source: `theta-summary-001.json`, `theta-domain-annotations-001.json` và proof/fixture.

Predictive df=ν−d+1; nativeν=d+1 nên ban đầudf2mọichiều. Shape ban đầuI vớiκ1. Student-tdf2 không có covariance hữu hạn; báo đúng `predictive shape` và Ψ=inv(precision-scale). Dof danh nghĩa đổi theo d không tự là prior defect.

FF/PF giữ scaleS_F, commonX/history exact30ca. Marginalνsmall=νfull−(dfull−dsmall), μ/κcommon và principalblockΨ khớp định nghĩa: maxΨerror5,94×10⁻¹⁴, commonlogpdferror2,63×10⁻¹³.17ca không thêm kênh giữidentity;13ca có kênh thêm có m/CPset khác.11contrast hữu hạn phân rã chênh growth logratio thành feedbackRparent và **relative conditional-extra likelihood giữa hai parent**. Absolute logdensity phụ thuộc đơn vị, không dùng dấu của nó để gọi kênh hỗ trợ/chốngreset. Source: `marginal-summary-001.json`.

Hai caRparent0 được kiểm tiếp, không bỏ: dev-3ae/dev-ba có normalization underflow tại371/385, PDFdương, shapeSPD/dfdương/Xfinite. Frozen-normalizer loglineage yếu hơn continuation rất nhiều tại contrast. Underflow không giải thích nativeMAP ở những điểm đã kiểm; không suy cho mọi futureCP hoặc nhận đã tái lập fully-renormalized log-domain detector. Source: `zero-lineage-summary-001.json`.

455/607points khôngCP;152CPgrowth có comparator finite, khôngresetMAP0/zeroexcluded trong domain ấy. Previous_m là priorR MAP, nên dấu prioradvantage≤0 vàdensityadvantage≥0 ởwinner là hệ quả comparator/MAP, không mechanismrates. Normalizer/residual là thành phần đại số phụ thuộc, không các nguyên nhân độc lập để cộng tỷ lệ.

Ba prior interventions giữ X/d/time/hazard/engine: df2→4 bằngνd+1→d+3;κ1→4 đổi pseudo-count **vàshape**; precisionI→4I giảm initialshape4lần. Mỗi mức là diagnostic có căn cứ, chưa tối ưu. Mỗi nhánh đổiCPset/m ở30/30ca. TổngCP gần nhau ởdf4/κ4 không bác ảnh hưởng: từng tập/thời điểm khác. Fixed-space sensitivity không gán prioralone cho maskcontrast cũ; NIWmarginal coherence và thêmchannel likelihood giải thích một câu hỏi khác.

## K4: causal preprocessing và vector bậc thang

Causal fixed dùng supplied static latency/error schema, ffillpast, fitminmax100actualraw rồi transform chính100raw làm initialization; alarmrelease từ100. Không dùng100zero synthetic. Suffix contract xét rawprefix≥100 cùngschema/params, khôngroot/proxy. Schema25–48chiều so native22–39: causal/native đổi mask/d/prior cùngscale, không cô lập scalealone.

Expanding prequential scaler đạt suffixcausal nhưng persistentposterior không transport qua hệ tọa độ thay đổi; chỉ là diagnostic, chưa coherent stationary model hoặc thiết kếP6 được chọn. Firstalarm của causal bịrelease>=100 trong khi native có eligibility riêng; **không so như hai detector có cùng thời điểm được phép báo**. Bảngoffset dưới chỉ mô tả output theo policy đã khai, không quality.

Compressed-row bỏ vectortrùng, hazard.02/retainedrow; calendar giữ cùngXnén/map với hazardgap=1−(.98)^gap. Cả hai đổi likelihood/update count,κ/ν,runlengthunit vàCPunit so native; gap không bù evidence/multipleresets đã bỏ. Row↔calendar cô lập hazard exposure có điều kiện trên cùngnén. Alarms map về timestampgốc, không báo delay theo indexnén.

Mỗi nhánh nén đổiCPset29/30ca; dev-575 không đổiCPset dù bỏ10row là identity hợp lệ. Row/calendar tổngCP360/361 nhưng sets khác15/30, không loạihazard vì totals gần nhau. Fixed/expanding sets khác30/30. Các kết quả này không chứng minh collector quantization là nguyên nhân hoặc nén là cách sửa detector.

## K6: cạnh tham gia phép tính, lợi ích đồ thị chưa được nhận thayP6

30ca probe gắn signedmaxabsz latency/error ở service; cạnh là cross-service parent-span nesting cùngtrace. g_v=abs(s_v−mean(s_outneighbors)); noedges=abs(s_v). Cùngsignals, rewiring giữ in/outdegree; finaledges và scorebehavior khác30/30. Source: `fast-summary-001.json#/graph_probe_rows`, từnggraph-probeJSON vàformula.

Đây là feasibility/computational dependency. Formula arbitrary/untuned/singleseed không là detector được chọn hoặc bằng chứng cải thiện. Wholetraceinventory là conditional suppliedschema; edgebaseline100 theo spanSTART không xác minh onlineavailability/completion tại100. Parentedges không tự là synchronous waiting, database/message/host dependency. Đồ thị thống kê từmetric cũng không tự là đồ thị gọi dịch vụ.

DT18 yêu cầu nútservice/thành phần, các kiểucall/message/data và log/trace/metric mapping cùng phép dùngcạnh rõ. P5/P6 cần chọn types/model/features/window/candidates và đối chứng tươngđương; graph/no-relation/random controls dùng khi đánh giá cấu trúc. T033 cung cấp căn cứ/điều kiện thấtbại, không chọnP6 hay giả graphbenefit. T032authorTraceRCA đã chạy được nhánh hỗ trợ đầu vào; không lấy adapter cũ để phủ định mọi phương phápgraph. XemT032REPORT/root-probes-report.

## K7: đã tính toàn đường congD, chưa biết end vật lý

Native predictions/cooldown300 giữ nguyên. Inclusiveproxy→proxy+D có curves cho mọiDquan sát; earlyfirst giữ cạnhfirstpost. BOCPDanypostCP tạiD30/60/120/300/600s là12/23/27/29/30ca. Source: `fast-summary-001.json#/bocpd_post_any_byD`, từngcontext `/bocpd_curve`. Đây là endpoint sensitivity, không chọnDđẹp/chấm lạiP3 hay xác nhận alarmmuộn cùng sự kiện. End/recovery/onset độc lập chưa có, cần record mới để biết physicalD.

## Năm đầu raP4, tồn đọng và bàn giao

Đã nối vớiMRP RQ2/P4/P5/P6, DT18NV2/NV3 và hướng dẫn cô: (1) hạn chế có điều kiện và nguồn; (2) adapter/cài đặt/thiếu đầu vào tách rõ; (3) giả định/cách tính có chain/control; (4) quan hệ thêm ngữ cảnh tính toán, chưa lợi ích; (5) câu thiếu bằng chứng, owner/input và quyết định ảnh hưởng. Sourcecoverage/closure theoK1–K7 ởledger, không chỉ đủSPEC/filecount.

Không còn engine hoặc phép phân xử tính toán đã khai đang chờ. Phần còn lại là finalindependent audit/source-preservation/handoff do root quản; independent audit cóscopefile riêng, không tự biến thành officialreview. Independent onset/cleannegative/end/completeness, deploymentversion/certifiedinvocationjoin và typedrelations chưaquan sát cần record bênngoài hoặc run mới, không thể suy từ cùngtelemetry. Thiết kế P5/P6 và đánh giá trên dữ liệu chưa dùng lúc thiết kế là nghĩa vụ tươnglai, không được T033probe/CPcounts đóng thay.

T33 giữ112slot, nhận116files/5,997MB hash2đầu; T32 giữ128slot với receipt riêng. T33intentionalboundary giữ STARTnative15/16 interruptedmetadata, không tínhPASS/branchfailure. T32supervisor bị FileExistsError do completionmarker trùngworker; workers vẫn hoàn tấtpart0/1 đủ128slot. Giữ lỗi/log, không rerun hoặc fakeexitcode. Tổngelapsed từngslot~19,50h qua2máy, không wallclock/billingcost hay benchmark tốcđộđộcquyền.

Files chính: `engine-final-summary-001.json`, `engine-input-verification-all30-001.json`, `backend-semantics-source-check-001.md`, `ledger-final-004.json`; mọi source/hash ởmanifest/receipt. Chỉworkroot bổ sung được ghi, source/results cũ giữ nguyên; root cập nhậtLOG/STATE/WHY/DECISIONS và quyết định kết thúc theoquyền. Không mởreview/task mới, commit hoặcpush.

## BảngA — đủ30ca, số chiều và sốCP từngnhánh

Các số dưới là sốcờ tính toán, khôngTP/FP/recall. N=1441row native mọi ca; nNén là retainedrows. DF/κ/P là prior df4/κ4/precision4I; CF/CE là causal fixed/expanding; R/C là compressed row/calendar.

|Ca|ID dev|dNative|dCausal|Native|DF|κ|P|CF|CE|R|C|nNén|
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(cases)+'''

## BảngB — firstalarm offset so proxy, đủ30ca

Đơn vịgiây; âm=trướcproxy,0=tại proxy,dương=sauproxy. Proxy là mốc tiêm của protocol, không onset vật lý. Causalrelease>=100 khác nativeeligibility; nén đổi runlength/CPunit. Vì vậy bảng không xếpquality. Từngtimestamp chínhxác và tậpalarm trongsummary.

|Ca|ID dev|Native|DF|κ|P|CF|CE|R|C|
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
'''+ '\n'.join(times)+'''

## BảngC — pairedsets, đủ30ca

R\C/C\R là sốtimestamps chỉ trong row/calendar trên cùngXnén; CF\CE/CE\CF là chỉ trong fixed/expanding cùngrawschema/indices. Hai pair giữ điều kiện của chúng; không dùng pair như isolatedscale effect so native hoặc quality. Source: summary `/paired_diagnostics`; mọi set giữ listtimestamp, không chỉcounts.

|Ca|R\C|C\R|CF\CE|CE\CF|
|---:|---:|---:|---:|---:|
'''+ '\n'.join(pairs)+'\n'
q=P/'report-final-004.md';assert not q.exists();q.write_text(report)
ledger=json.loads((P/'ledger-final-003.json').read_text());ledger['UTC']=datetime.datetime.now(datetime.timezone.utc).isoformat();ledger['report']='report-final-004.md';ledger['clarifications']=['Causalrelease100 differsfromnativealarmeligibility;firstalarmoffsets observationalnotquality','All30percase dims/counts/firsttimes andpairsetsprinted','Compressedunit differsnative, row/calendar sharecompressedX','Referencebusinesssemanticschecked;benchmarkdeploymentversion gapexplicit'];ledger['source_files']+=[{'file':q.name,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}];out=P/'ledger-final-004.json';assert not out.exists();out.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n');print('readable final004+ledgerwritten;30rows×3tables')
