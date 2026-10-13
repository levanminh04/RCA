# T033 — báo cáo bổ sung đầy đủ, bản004

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
|1|03d4910932|28|34|21|19|19|44|48|26|14|14|1306|
|2|12a1a88069|33|44|19|25|18|42|18|14|15|14|1240|
|3|14372e1209|29|34|7|5|5|9|13|7|7|7|1421|
|4|16597725c1|34|40|13|9|13|25|20|28|10|10|1239|
|5|16870e660c|28|34|13|13|15|23|51|43|17|17|1249|
|6|1e6d61b5ec|23|25|30|28|30|36|37|32|24|25|973|
|7|20acb4402d|22|30|19|18|14|46|18|38|11|11|1030|
|8|260d332c8d|22|30|22|23|23|58|38|32|16|16|981|
|9|3ae0a6c15a|36|43|14|9|15|32|43|32|13|13|1277|
|10|3defe3d34b|30|42|15|18|16|38|10|12|8|8|1285|
|11|4e68956051|28|31|12|13|12|35|77|35|11|11|1324|
|12|4f8a844308|39|46|7|10|13|15|16|14|7|7|1168|
|13|57546fd87b|28|31|7|7|7|25|21|13|7|7|1431|
|14|59f696a169|27|40|31|32|31|49|26|28|26|26|1230|
|15|746fd74313|32|44|10|12|8|24|14|29|9|9|1253|
|16|7f1b6b071d|33|34|18|18|16|40|51|46|9|9|1182|
|17|8017c6dc70|22|25|23|17|22|49|48|31|19|17|892|
|18|98bc73c499|32|42|14|14|15|29|31|24|13|13|1212|
|19|a505ab3f65|31|44|13|11|11|32|28|14|9|9|1277|
|20|a5cabe5fa7|30|32|18|20|14|30|58|32|18|18|1214|
|21|a915aa2424|32|41|11|15|11|29|31|18|8|9|1232|
|22|b8bd0abf60|32|48|16|15|13|33|7|21|9|11|1186|
|23|ba831dbeb8|36|41|16|19|15|44|32|17|14|14|1282|
|24|bcbd4f46ae|28|34|6|6|6|12|5|6|6|6|1402|
|25|db293894ab|31|33|20|17|15|31|29|23|14|14|1256|
|26|de89e2f9e9|30|39|6|7|7|20|7|9|7|7|1037|
|27|f36d0647d5|33|46|13|14|20|46|31|17|17|17|1249|
|28|f81f88234e|28|32|5|5|5|10|5|4|5|5|1405|
|29|f9a8e05ed7|31|38|9|12|9|14|1|15|8|8|1075|
|30|fbc45b0c67|28|31|9|12|7|32|62|41|9|9|1320|

## BảngB — firstalarm offset so proxy, đủ30ca

Đơn vịgiây; âm=trướcproxy,0=tại proxy,dương=sauproxy. Proxy là mốc tiêm của protocol, không onset vật lý. Causalrelease>=100 khác nativeeligibility; nén đổi runlength/CPunit. Vì vậy bảng không xếpquality. Từngtimestamp chínhxác và tậpalarm trongsummary.

|Ca|ID dev|Native|DF|κ|P|CF|CE|R|C|
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
|1|03d4910932|-36|-49|-15|-594|-570|-553|17|17|
|2|12a1a88069|-592|-605|-592|-659|-609|-609|-584|-588|
|3|14372e1209|-468|-483|-458|-640|-505|-485|-468|-468|
|4|16597725c1|-481|-496|-482|-621|-568|-565|-472|-472|
|5|16870e660c|-106|-106|-106|-241|-598|-555|-106|-106|
|6|1e6d61b5ec|-601|-613|-602|-678|-612|-612|-589|-589|
|7|20acb4402d|-440|-440|-440|-548|-545|-562|-440|-440|
|8|260d332c8d|-594|-606|-595|-666|-563|-612|-590|-590|
|9|3ae0a6c15a|-71|-104|38|-549|-614|-560|1|0|
|10|3defe3d34b|28|-29|33|-517|-443|-465|37|37|
|11|4e68956051|-45|-159|-29|-457|-601|-595|-28|-28|
|12|4f8a844308|-502|-549|-494|-630|-594|-593|-486|-486|
|13|57546fd87b|-305|-325|-302|-602|-577|-551|-305|-305|
|14|59f696a169|-558|-574|-554|-650|-564|-559|-540|-540|
|15|746fd74313|-618|-618|-618|-619|-460|-618|-618|-618|
|16|7f1b6b071d|-365|-365|-365|-471|-589|-589|-365|-365|
|17|8017c6dc70|-449|-459|-443|-616|-606|-595|-347|-347|
|18|98bc73c499|41|38|42|-523|-555|-544|43|43|
|19|a505ab3f65|-336|-358|-331|-583|-521|-439|-308|-308|
|20|a5cabe5fa7|-249|-266|-247|-537|-584|-566|-221|-221|
|21|a915aa2424|-41|-41|-41|-452|-495|-473|-41|-41|
|22|b8bd0abf60|-218|-218|-218|-495|-390|-604|-214|-214|
|23|ba831dbeb8|-172|-172|-172|-642|-520|-469|-170|-170|
|24|bcbd4f46ae|-515|-526|-512|-632|-551|-533|-515|-515|
|25|db293894ab|-508|-519|-507|-655|-505|-483|-501|-501|
|26|de89e2f9e9|-255|-309|-255|-585|-443|-494|-255|-255|
|27|f36d0647d5|32|32|32|-573|-432|-27|32|32|
|28|f81f88234e|-541|-559|-537|-653|-554|-550|-541|-541|
|29|f9a8e05ed7|-603|-613|-602|-678|-473|-552|-574|-574|
|30|fbc45b0c67|-431|-431|-431|-453|-608|-589|-431|-431|

## BảngC — pairedsets, đủ30ca

R\C/C\R là sốtimestamps chỉ trong row/calendar trên cùngXnén; CF\CE/CE\CF là chỉ trong fixed/expanding cùngrawschema/indices. Hai pair giữ điều kiện của chúng; không dùng pair như isolatedscale effect so native hoặc quality. Source: summary `/paired_diagnostics`; mọi set giữ listtimestamp, không chỉcounts.

|Ca|R\C|C\R|CF\CE|CE\CF|
|---:|---:|---:|---:|---:|
|1|0|0|46|24|
|2|8|7|15|11|
|3|0|0|13|7|
|4|1|1|19|27|
|5|0|0|47|39|
|6|2|3|31|26|
|7|0|0|15|35|
|8|1|1|32|26|
|9|7|7|38|27|
|10|0|0|9|11|
|11|0|0|66|24|
|12|1|1|13|11|
|13|0|0|20|12|
|14|0|0|24|26|
|15|0|0|12|27|
|16|1|1|47|42|
|17|4|2|47|30|
|18|0|0|29|22|
|19|1|1|23|9|
|20|0|0|56|30|
|21|0|1|29|16|
|22|2|4|7|21|
|23|0|0|31|16|
|24|0|0|4|5|
|25|3|3|29|23|
|26|0|0|7|9|
|27|2|2|28|14|
|28|0|0|5|4|
|29|1|1|1|15|
|30|1|1|49|28|
