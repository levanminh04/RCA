# Rà 27 mục nguồn còn OPEN

Đây là tự kiểm hỗ trợ người làm T-038, không phải lượt phản biện. Kết quả chi tiết nằm trong `findings.json#/records`; số tổng hợp nằm ở `#/summary`. Đầu vào là bản coverage trước lượt bổ sung, nguồn theo plan đã duyệt và oracle đọc tay. Mọi file nguồn được kiểm số byte và Git blob trước khi giải mã. Không sửa coverage hay đồ thị gốc.

| Nhóm | Số path cũ OPEN | Kết quả đề nghị | Bằng chứng và giới hạn |
|---|---:|---|---|
| Ảnh hướng dẫn Train Ticket | 11 | read | README lịch sử trỏ đúng từng ảnh; đã xem trực tiếp: giao diện đặt vé/quản trị và ảnh cấu hình Selenium. Hành động trên giao diện không được đổi thành cạnh service. |
| Ảnh theme/dashboard | 12 | read | Năm logo trình duyệt, năm wireframe bố cục, một hình minh họa và một splash AmazeUI. Dockerfile đưa thư mục static vào nginx; ảnh không chứa log, trace hay metric. |
| Ảnh avatar | 1 | read | README/code face detection và ảnh chân dung fixture, không có nội dung telemetry. |
| VIM swap trong chart MySQL | 1 | excluded có điều kiện | Header VIM và vị trí trực tiếp dưới `templates/`; loader Helm ở hai baseline được README nêu bỏ dotfile theo default rule. Chưa suy ra phiên bản Helm thực đã triển khai. |
| `old-docs/Lib/myproject.zip` | 1 | read với độ sâu rõ | Đã đọc Java/POM an toàn và metadata container/class/activation; chưa xác nhận bytecode tương đương source hay activation trong lần thu RE2-TT. |
| PDF Json2Shiviz lịch sử | 1 | open về nội dung | Vai trò tài liệu converter đã phân loại. Chỉ đọc metadata/resources: sáu trang, mười ảnh, không outline. Chưa mở body có thể chứa mẫu log bị cấm. |
| **Tổng** | **27** | **25 read, 1 excluded, 1 open** | Tất cả mục cũ đã có hồ sơ và lý do riêng. |

Nếu tích hợp đúng các đề nghị này vào bản coverage đầu vào: **2783 read, 43 excluded, 1 open**, tổng **2827 path**. Đây là số phân hoạch nội dung nguồn đã lưu, không phải số service hay số blob Git duy nhất. `old_open_roles_partitioned=true`; `content_scope_complete=false`, `source_semantics_complete=false`, `evaluated_runtime_lineage_complete=false`.

## Căn cứ loader Helm

README chart ghi Helm 2.11+ hoặc 3.0-beta3+. Đã xem chỉ đọc trang HTML nguồn chính thức của [Helm 2.11 Rules.AddDefaults](https://github.com/helm/helm/blob/v2.11.0/pkg/ignore/rules.go#L46-L50), [Helm 2.11 LoadDir](https://github.com/helm/helm/blob/v2.11.0/pkg/chartutil/load.go#L260-L315), [Helm 3.0.0-beta.3 Rules.AddDefaults](https://github.com/helm/helm/blob/v3.0.0-beta.3/internal/ignore/rules.go#L46-L50) và [Helm 3.0.0-beta.3 LoadDir](https://github.com/helm/helm/blob/v3.0.0-beta.3/pkg/chart/loader/directory.go#L43-L107). Hai baseline đều thêm rule `templates/.?*` mặc định và kiểm ignore trước khi đọc nội dung file. Vì vậy việc không có `.helmignore` không làm swap này thành template theo các loader đã kiểm.

Cơ chế tra cứu là search/open/find trên các trang GitHub HTML primary. Không fetch raw blob, không tải/lưu thêm source snapshot, không nhúng mã Helm vào helper và không thực thi Helm. Chỉ giữ URL, symbol, nhận xét ngắn và literal rule. Hai lượt URL Helm 3 sai trả lỗi, không sinh file nguồn. Phép kiểm local là regexp tự viết cho đường dẫn cụ thể và năm ca đối chiếu; không thay thế toàn bộ parser ignore của Helm hay xác nhận mọi phiên bản tương lai.

## Archive và phạm vi runtime

Hướng dẫn lịch sử yêu cầu cài thư viện `myproject` vào Maven local repository. Container có 22 entry, sáu JAR lồng nhau; đã đọc toàn bộ 161 Java source an toàn của hai source JAR, hai POM, manifest, `spring.factories` và tên class của binary JAR trong bộ nhớ. Không giải nén ra filesystem, không chạy bytecode, không render javadoc. Namespace embedded là `org.springframework.cloud.sleuth`; không được đồng nhất với bản loose có namespace khác chỉ vì cùng vai trò monitoring.

Đã đối chiếu 43 POM hiện hành, profile/systemPath và build references đã lưu. Không có direct reference tới thư viện monitoring lịch sử hay converter Json2Shiviz. Root POM liệt kê 42 module ứng dụng/thư viện hiện hành, không đưa converter trong `old-docs/` vào build. Presence và auto-configuration entrypoint của archive chưa chứng minh dependency đã resolve hay thư viện đã active khi thu RE2-TT. Cần image digest/build manifest, resolved dependencies và instrumentation agent config của lần thu để kết luận lineage hoặc runtime naming. Không thêm entity Zipkin, application call hay alias operation từ sự hiện diện của archive.

## PDF còn thiếu đúng phần nào

Đã áp dụng [PDF skill](C:/Users/84583/.codex/plugins/cache/openai-primary-runtime/pdf/26.1013.11914/skills/pdf/SKILL.md) cho kiểm metadata. `build.gradle` xác định `TraceTranslator`; file regular expression cạnh PDF mô tả schema chuyển log. Bằng chứng này cùng partition module/build đủ xếp tài liệu vào công cụ offline lịch sử, ngoài inventory ứng dụng hiện hành được khai báo. Việc chưa mở body không chặn partition đó.

Body PDF vẫn chưa đọc vì mười ảnh chưa được phân vùng thành hướng dẫn hay mẫu log thật, trong khi mẫu Json2Shiviz vẫn bị cấm mở. Phần thiếu chỉ ảnh hưởng phát biểu phụ thuộc nội dung hướng dẫn/schema/naming lịch sử hoặc lineage. Công cụ đọc/render đã có; không có thiếu helper hay lý do phải chạy source. Nếu cần phân xử nội dung, đầu vào cụ thể là danh sách trang/vùng an toàn hoặc bản manual đã bỏ mẫu từ chủ nguồn, hay quyền Minh cho xem mẫu liên quan. Ước lượng sau đầu vào đó: khoảng mười phút, chưa kiểm. Không cần tải/build mới.

## Tự kiểm và bàn giao

Oracle ghi các quan sát đọc tay/đọc hình và expected trước helper bổ sung này; đây không phải oracle trước extractor Java cũ. Helper kiểm identity, kích thước ảnh, phân hoạch đủ 27 path, container metadata, module/build references, metadata PDF và tổng 2827. Tất cả 43 kiểm hiện tại đạt; không mở raw telemetry, Jaeger, workbook debug, mẫu Json2Shiviz hoặc index cách ly. Không tải source/image mới và không chạy ứng dụng.

File được ghi trong thư mục coverage được giao: `oracle.json`, `inspect_open.py`, `findings-initial.json`, `findings.json`, `report.md`. Bản initial được giữ trước khi bổ sung diễn giải phạm vi PDF và phép đối chiếu module/build. Chưa thay quyết định hay shared code; root tích hợp bằng con trỏ `findings.json#/records` và `#/summary`, giữ các giới hạn nội dung/lineage riêng.
