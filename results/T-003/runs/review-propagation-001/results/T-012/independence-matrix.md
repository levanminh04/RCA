# Phả hệ và tính độc lập — chỉ nguồn/metadata

MRP §4 tiêu chí 9 yêu cầu khác nhóm tác giả, công cụ tiêm lỗi và stack thu thập. Dưới đây ghi từng trục, không cộng thành điểm và không coi việc chưa tìm thấy reuse là bằng chứng không reuse. Root bảo toàn ứng viên là quyết định quản lý dữ liệu theo Q-47; chưa tự đồng nghĩa tiêu chí 9 đạt.

## Các họ và bằng chứng

| Họ | Nhóm tác giả/nguồn | Tiêm/tạo lỗi | Stack thu thập | Reuse và giới hạn |
|---|---|---|---|---|
| RCAEval | Pham và cộng sự, [T-002](../T-002/the-rcaeval.md) | stress-ng/tc và sửa code | Prometheus/cAdvisor/Istio, Jaeger, Vector/Loki/Elasticsearch | RE/TT/OB/SS là các biến thể cùng họ; không đếm thành bộ độc lập. T-002 còn review riêng, chỉ dùng mô tả nguồn ở đây. |
| Nezha | Yu/Chen/Li/Zheng và cộng sự, [T-008](../T-008/the-dataset.md) | Byteman/Hypno/Failpoint cho code; công cụ resource còn OPEN trong nguồn đã khóa | OTel→Tempo, Promtail→Loki, cAdvisor/Istio/NodeExporter→Prometheus | TT/OB chung họ; metadata chưa chứng minh raw overlap với RCAEval hoặc không overlap. |
| Eadro | Lee/Yang/Chen/Su/Lyu, [T-009](../T-009/the-dataset.md) | ChaosBlade | Jaeger, cAdvisor/Prometheus→InfluxDB, Fluentd/ELK | SN/TT chung nhóm/pipeline. Cùng Jaeger/Prometheus với RCAEval; không nói hoàn toàn khác stack. |
| DeepTraLog | Zhang và nhóm FudanSELab, [T-010](../T-010/the-dataset.md) | Faulty branches TrainTicket | SkyWalking/Elasticsearch | Dữ liệu trace/log/graph derivation không là các corpus độc lập; faulty versions có thể chung upstream với nghiên cứu TT khác, raw chưa đối chiếu. |
| LEMMA IT | Zheng và cộng sự, [T-011](../T-011/the-dataset.md) | Scenario có kiểm soát; công cụ từng scenario chưa khóa đồng nhất | Product Review OpenShift/Prometheus/Elasticsearch; Cloud Computing CloudWatch/JMeter, một số Prometheus | Original/Preprocessed cùng raw. Khác miền không thay bằng chứng khác injector. OT bỏ khỏi phạm vi theo Q-47; không mở rộng kết luận sang OT. |
| OpenRCA | Xu/Zhang/Zhong/He/Lin/Pei và cộng sự, [paper §2.4](runs/run-002/sources/openrca-paper.pdf) | Nguồn AIOps Challenge; công cụ gốc từng hệ OPEN | Telemetry AIOps đã đổi tên/hiệu chỉnh; collector gốc từng hệ OPEN | **Dùng lại raw AIOps**. Bank/Telecom/Market khác hệ và schema, chưa chứng minh độc lập đủ ba trục. |
| AIOps nguồn của OpenRCA | Nhóm tổ chức/đơn vị cung cấp hệ gốc chưa định danh đầy đủ trong paper OpenRCA | OPEN theo edition/system | OPEN theo edition/system | Quan hệ reuse tới OpenRCA là FACT; exact year/edition mapping chưa khóa nên không đoán Bank chắc chắn là toàn bộ AIOps2021. |
| FSE / OpenRCA2 | Fang/Yang/Zhang/Xu/He và cộng sự, [FSE](runs/run-001/sources/fse-paper-v2.html), [OpenRCA2 §3.1/A.3/A.6](runs/run-001/sources/openrca2-paper-v2.html) | ChaosMesh và bộ cấu hình thí nghiệm | OTel/Prometheus, Parquet; FSE còn Hubble | OpenRCA2 TT xây trên Fang/FSE là FACT reuse. Các hệ OpenRCA2 dùng cùng nhóm/pipeline; OpenRCA1 có tác giả Xu/He chung nhưng nguồn raw AIOps khác. |
| AnoMod | Ping/Mazhar/Wang/Song/Mäntylä, [record](runs/run-001/sources/anomod-record-18342898.json) | SN ChaosBlade/container restart; TT ChaosMesh/ChaosBlade; EvoMaster tạo tải | SN Jaeger, TT SkyWalking, Prometheus và container logs | Theo nguồn là campaign thu mới. SN trùng testbed/collector/injector với Eadro ở nhiều thành phần; không tính đủ độc lập. |
| LO2 v1/v2 | Oulu/Helsinki, [v1 record](runs/run-001/sources/lo2-record-14938118.json), [v2](runs/run-002/sources/zenodo-18937117-latest.json) | Locust erroneous API usage, không phải tiêm resource/network của các họ trên | Docker, Jaeger, Prometheus/NodeExporter; v2 cAdvisor | v1/v2 chung lineage, một số tác giả chung AnoMod. Có trace đơn span ở v1 nên không thay bộ RCA có call graph. |
| TrainTicketTrace | Urbanke/Fischer SCCH, [record](runs/run-002/sources/zenodo-17811972-latest.json) và [conference](runs/run-002/sources/traintickettrace-conference.html) | Seeded faulty versions; công cụ/mapping chưa rõ | OPEN | F-code tương tự DeepTraLog chưa chứng minh reuse raw hoặc độc lập; cần revision/source của faulty versions. |

## Ma trận các họ được yêu cầu

Trong ma trận, **O** nghĩa là chưa đủ chứng minh cả ba trục; **S** là có stack thành phần dùng chung; **G** là có tác giả dùng chung; **R** là reuse raw được nguồn xác nhận. S/G/R không có nghĩa mọi byte giống nhau. Ô không có R không chứng minh không reuse. Mọi cặp chưa có bằng chứng đủ đều chưa được công nhận đạt tiêu chí 9.

| Cặp | Nezha | Eadro | DeepTraLog | LEMMA IT | OpenRCA | OpenRCA2/FSE | AIOps nguồn OpenRCA |
|---|---|---|---|---|---|---|---|
| Nezha | Cùng họ | S: Prometheus/cAdvisor; O | O: cùng TT, collector khác phần trace | S: Prometheus; O injector | O collector/injector AIOps | S: OTel/Prometheus; O | O collector/injector |
| Eadro | — | Cùng họ | S: Elasticsearch; O | S: Prometheus/Elasticsearch; O | O collector/injector AIOps | S: Prometheus; O | O collector/injector |
| DeepTraLog | — | — | Cùng họ | S: Elasticsearch; O | O collector/injector AIOps | O: cùng TT chưa raw mapping | O collector/injector |
| LEMMA IT | — | — | — | Original/preprocessed cùng raw | O collector/injector AIOps | S: Prometheus; O | O collector/injector |
| OpenRCA | — | — | — | — | Hệ khác chưa đủ ba trục | G: Xu/He; raw khác nguồn mô tả, O | R: §2.4 paper |
| OpenRCA2/FSE | — | — | — | — | — | R: TT; chung nhóm/pipeline | O collector/injector |
| AIOps nguồn OpenRCA | — | — | — | — | — | — | Edition/system khác chưa tự độc lập |

RCAEval so Nezha/Eadro/LEMMA/OpenRCA2 đều có thành phần collector chồng; so DeepTraLog chưa định danh reuse faulty branches; so OpenRCA/AIOps thiếu injector/collector gốc. Không khẳng định đã có một cặp đạt toàn bộ tiêu chí 9. **Có bằng chứng đa dạng nguồn là FACT; đủ độc lập là OPEN.**

## Tự phản biện

- Khác hoàn toàn mọi thư viện thu thập không được MRP định nghĩa; không tự phát minh ngưỡng phần trăm overlap. Vì thế báo đúng thành phần chung và phần thiếu, để G1 quyết dựa trên bằng chứng.
- Nhóm tác giả khác không chứng minh chiến dịch khác; cùng tác giả cũng chưa chứng minh cùng raw. OpenRCA/FSE là ví dụ phải tách hai chiều này.
- Tên OpenRCA2 không suy kế thừa raw OpenRCA1; bài chỉ ra TT upstream Fang/FSE. Ngược lại, không tách OpenRCA1 khỏi AIOps chỉ vì đã đổi tên/hiệu chỉnh.
- Hệ Bank có thể thay đổi cơ chế lỗi/quan sát/độ lớn. Vì chưa mở số đo, chọn bảo toàn chỉ giữ cơ hội đánh giá sau G3; không hứa chắc adapter/quality/normal hoặc độ phân xử đạt.
