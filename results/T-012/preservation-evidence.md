# Thông tin chung trước đọc số đo — đầu vào quyết định bảo toàn

Ngày 03/10/2026. **CANDIDATE do người làm đề xuất cho root**, chưa tự ghi lựa chọn vào WHY. Q-47 giao Codex quyết định bằng thông tin chung và chấp nhận phần chất lượng chưa xác minh. Tài liệu này không dùng kết quả thuật toán, metric, log hay trace thực. Giới hạn đã đọc: bài, README, schema công bố, metadata kho. Không tải/đọc một hàng Bank.

## OpenRCA Bank: lý do ưu tiên bảo toàn

- FACT nguồn: [bài chính thức ICLR, §2.4 và Appendix A.1–A.2](runs/run-002/sources/openrca-paper.pdf) xác nhận bộ này phát sinh từ AIOps Challenge, sau lựa chọn, đổi tên, hiệu chỉnh và lọc nhãn. Hệ banking có pod, service, lỗi CPU/memory/disk/network/JVM và ba nguồn metric/trace/log. Đây là miền và lịch sử thu thập khác các testbed TrainTicket/SocialNetwork/OnlineBoutique trong T-008–T-010.
- FACT nguồn: [README ghim commit](runs/run-002/sources/openrca-README.md) mô tả `record.csv`, `query.csv`, bộ ba trường root occurrence datetime/component/reason; timezone nhãn UTC+8; Bank chỉ có trace ngang mức pod, không có tầng triển khai dọc. Nhãn thời gian chưa được kiểm là injection hay onset quan sát. Không suy pod thành service, hoặc coi query là incident độc lập.
- FACT nguồn: dữ liệu CC BY-NC 4.0 theo Appendix A.1; [LICENSE repo](runs/run-002/sources/openrca-LICENSE) MIT cho code. Không dùng MIT của repo để thay license telemetry. Ethics Statement thêm cách diễn giải điều khoản phái sinh; giữ link tới license gốc trong bài, không tự suy ra bộ dữ liệu mang SA.
- CANDIDATE: Bank có khả năng phục vụ xếp hạng mức pod và nghiên cứu đồ thị lời gọi. Giả định schema công bố đúng release và ánh xạ nhãn sang entity đo đầy đủ. Sai nếu parent/span thiếu, root không quan sát được, khoảng normal không đủ, clock sai hoặc nhãn không khớp. Chưa đo các phần này vì bảo toàn trước G3.
- **Tiêu chí 9 chưa được chứng minh đủ:** nguồn mới xác nhận lineage AIOps và testbed khác. Injector gốc và collector gốc chưa khóa được theo từng release, nên không khẳng định khác đủ nhóm tác giả + công cụ tiêm + stack thu thập theo MRP§4. Bank là lựa chọn bảo toàn có điều kiện, không phải bằng chứng đã đạt độc lập.
- Bảo toàn phải bao gồm OpenRCA Bank và bản AIOps Bank gốc/phái sinh dùng cùng incident. Đọc AIOps Bank rồi gọi OpenRCA Bank là chưa xem sẽ sai. OpenRCA Telecom/Market chưa tự động được chứng minh độc lập với Bank; quyền đọc chúng cần xét provenance trước.

## Vì sao chưa ưu tiên các phương án còn lại

| Phương án | Bằng chứng liên quan | Hạn chế quyết định từ thông tin chung |
|---|---|---|
| Nezha OB/TT | [T-008](../T-008/the-dataset.md): census nhãn, trace/metric/log, OTel/Tempo/Loki/Prometheus; nhóm Yu và cộng sự | Có bằng chứng root/time tốt. OB khác TT nhưng raw/nhóm/stack chung trong họ Nezha; dùng cùng Prometheus/OTel với ứng viên khác không tự đạt đủ tiêu chí 9. Không có bằng chứng bắt buộc loại; là phương án dự phòng về khả năng chấm. |
| Eadro SN/TT | [T-009](../T-009/the-dataset.md): root/time, ChaosBlade, Jaeger/cAdvisor/Prometheus/InfluxDB, Fluentd/ELK | Khác Nezha ở nhóm/công cụ/trace collector nhưng metric stack chồng lấn; data license còn OPEN. SN/TT chung chiến dịch Eadro không tính thành hai bộ độc lập. |
| AnoMod SN/TT | [record](runs/run-001/sources/anomod-record-18342898.json), [SN README](runs/run-002/sources/anomod-SN_collection-scripts__README.md), [TT README](runs/run-002/sources/anomod-TT_collection-scripts__T-Dataset__README.md) | Nhóm Helsinki và EvoMaster là provenance riêng, nhưng SN cùng ChaosBlade/Jaeger/Prometheus với Eadro. TT dùng ChaosMesh/ChaosBlade và SkyWalking/Prometheus. Nhiều modality không chứng minh root/time từng incident đủ. |
| DeepTraLog | [T-010](../T-010/the-dataset.md) | Trace/log và faulty branches; thiếu xác nhận root/time từng incident, chưa thấy resource metric riêng. Hệ TT và tên nhánh lỗi không tự tạo độc lập. |
| LEMMA IT | [T-011](../T-011/the-dataset.md) | Miền/stack đáng bổ sung, nhưng release chính có metric/log, trace chưa chứng minh; license NC/ND cần giữ đúng nguồn. Không thay trace bằng correlation metric. OT đã bỏ theo Q-47. |
| OpenRCA2 / FSE | [OpenRCA2 §3.1, A.3, A.6](runs/run-001/sources/openrca2-paper-v2.html) | TT dùng lại Fang/FSE; cùng nhóm và campaign, không độc lập. OpenRCA2 public release chưa khóa, labels propagation được tạo từ telemetry + quy tắc PAVE nên không tự là nhãn vùng độc lập với phương pháp. |

## Phạm vi không suy rộng

Bảo toàn Bank không chốt bộ thí nghiệm G1, cách chia dev/test hay kết luận phương pháp. Các số ca/byte và phiên bản nằm trong manifest/bảng nguồn T-012; không dùng độ nhỏ/lớn dữ liệu làm tiêu chí khả năng phân xử. Điều kiện chất lượng giữ OPEN theo quyết định chấp nhận của Minh, không gọi là đã kiểm. Chốt quyết định và kết luận phụ thuộc do root ghi vào WHY trước khi đọc số đo ứng viên khác.
