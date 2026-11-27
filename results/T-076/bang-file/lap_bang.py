"""Sinh bảng C1 (T-076 bước 1) từ danh sách file `git diff --name-status d147d49 bb84d64`. Quy tắc phân loại ghi trong code."""
import sys, re, collections

tsv, xung_dot_f, main_doi_f, out = sys.argv[1:5]
files = [l.rstrip('\n').split('\t') for l in open(tsv, encoding='utf-8') if l.strip()]
xung_dot = {l.strip() for l in open(xung_dot_f, encoding='utf-8') if l.strip()}
main_doi = {l.strip() for l in open(main_doi_f, encoding='utf-8') if l.strip()}

LAB_PHU = 'file phủ lab `test-environment/overrides/` đã đặt'

def loai(f):
    """Trả (nhóm, quyết định, lý do)."""
    if f == '.github/workflows/_maven-verify.yml':
        return 'CI', 'Sửa', 'Bước kiểm B16 chạy cho mọi service trừ keycloak; Assistant (main) sẽ đỏ (REVIEW R5). Sửa: chỉ chạy cho service trong `deploy/observability/b16-services.txt`; service trong danh sách thiếu file mẫu = lỗi'
    if f == '.github/scripts/detect-changes.sh':
        return 'CI', 'Sửa', 'Quy tắc `deploy/observability/*` chọn mọi service trừ keycloak/frontend, gồm cả Assistant. Sửa: chỉ chọn service trong danh sách B16'
    if f == '.github/workflows/_deploy-service.yml':
        return 'CI', 'Giữ', 'Diff ròng so với merge-base chỉ còn hunk truyền `SERVICE_VERSION={github.sha}` cho service Maven; build hai kiến trúc đã có ở main (dòng 79–82, 118). Cần để `service.version` = revision'
    if f == '.env.example':
        return 'Cấu hình gốc', 'Bỏ', 'Chẩn đoán PostgreSQL và tracing Keycloak cho Compose cũ; ngoài phạm vi agent máy 84; Postgres/Keycloak của exp-app cấu hình ở lab'
    if f == '.gitignore':
        return 'Cấu hình gốc', 'Bỏ', '`/.local/rca-test/` thuộc bản nháp `deploy/rca-test` đã chuyển sang repo lab'
    if f.startswith('deploy/app/'):
        if f.endswith('README.md'):
            return 'Compose (dự phòng)', 'Bỏ', 'Thêm mục "Gói a–i" hướng dẫn vận hành thời Compose, trỏ `deploy/rca-test` đã bỏ. Lấy bản main. Cách bật agent ghi trong mô tả PR và `deploy/observability/README.md`'
        if 'keycloak' in f:
            return 'Compose (dự phòng)', 'Bỏ', 'Bật log JSON và tracing native cho Keycloak, nâng bộ nhớ. Keycloak exp-app (`ft-local/keycloak:arm64-776d9c9e`) không có biến `KC_TRACING*`/`KC_LOG_CONSOLE*` (SSH 26/11): không dùng; ngoài phạm vi'
        return 'Compose (dự phòng)', 'Bỏ', 'Nâng `mem_limit`/nhãn log cho Compose; main chạy K8s. Với exp-app, ' + LAB_PHU + ' cùng giá trị (booking, event, payment 1g; discovery 768m; nhãn log cả 7), nên bỏ không đổi cấu hình hiệu lực'
    if f in ('deploy/docker-compose.postgresql.yml', 'deploy/postgres/00-business-databases.sh'):
        return 'Postgres', 'Bỏ', 'Bật log chẩn đoán Postgres (và đổi quyền file 644→755) cho Postgres của nhóm; ngoài phạm vi agent; exp-app có `test-environment/infra/docker-compose.rca-log.yml` riêng'
    if f.endswith('/database/90-erd-reader.sql'):
        return 'Postgres', 'Bỏ', 'Tạo quyền đọc ERD (`*_erd`); không thuộc quan sát, lab không dùng'
    if f == 'services/keycloak-spi/Dockerfile':
        return 'Keycloak', 'Bỏ', '`ENV KC_TRACING_ENABLED=true` nướng vào image Keycloak mà main triển khai lên máy 84: tracing bật mà không có endpoint. Ngoài phạm vi; exp-app không dùng'
    if f == 'docs/project/decision-register.md':
        return 'Tài liệu', 'Giữ', 'GOV-150..156: lịch sử quyết định của Minh cho PR; main dừng ở GOV-149, không trùng mã'
    if f == 'deploy/observability/README.md':
        return 'Chuẩn B16', 'Sửa', 'Viết lại theo K8s: bỏ liên kết `deploy/rca-test`, `.local/rca-test`, danh sách file thời Compose; thêm cách bật/tắt agent qua `ENV_<SVC>` + CD `restart`'
    if f.startswith('deploy/observability/'):
        return 'Chuẩn B16', 'Giữ', 'Schema, bộ kiểm và phụ thuộc của kiểm log B16 trong CI'
    if f.endswith('/Dockerfile'):
        return 'Image', 'Sửa', 'Xung đột. Lấy Dockerfile main (giải nén theo lớp, digest ảnh nền của main, `curl`/`jq`), chèn: tải agent 2.33.1 có checksum, `docker-entrypoint.sh`, `SERVICE_VERSION`, `SERVICE_NAME`. Không lấy đổi digest ảnh nền của PR'
    if f.endswith('/docker-entrypoint.sh'):
        return 'Image', 'Sửa', 'Giữ phần nhận diện tài nguyên và bật/tắt agent; thêm: giải `OTEL_CA_PEM_B64` ra `/tmp/otel-ca.pem`, đặt `OTEL_EXPORTER_OTLP_CERTIFICATE` (SPEC C3b). Vẫn `OTEL_LOGS_EXPORTER=none`'
    if f.endswith('/.dockerignore'):
        return 'Image', 'Giữ', 'Một dòng `!docker-entrypoint.sh` (GOV-156)'
    if f.endswith('/.env.example'):
        return 'Cấu hình service', 'Giữ', 'Tài liệu biến cho chạy local/Compose (`OTEL_*`, ở booking/event thêm `FT_FAULT*`); K8s lấy từ ConfigMap/Secret ở bước 3. exp-app đặt `FT_FAULT*` ở `/opt/flashticket/env/{booking,event}-service.env`'
    if f.endswith('/pom.xml'):
        return 'Build', 'Giữ', 'Thêm `opentelemetry-api` 1.59.0 (booking, payment, ticket) cho telemetry nghiệp vụ; profile `rca-test` (booking, event) chỉ khi build `-P rca-test`'
    if f.endswith('application.yaml'):
        return 'Cấu hình log', 'Giữ', 'Log JSON logstash, customizer `LogFields`, máy in stacktrace an toàn, mức log (B16)'
    if '/src/rca-test/' in f:
        return 'Hook tiêm lỗi', 'Giữ', 'Chỉ vào build `-P rca-test` (exp-app); build production không chứa (SPEC C1)'
    if '/src/test/' in f:
        if f.endswith('ObservabilityTests.java'):
            return 'Kiểm B16', 'Giữ', 'Sinh `target/b16-log-samples.jsonl` cho bước kiểm CI'
        return 'Kiểm B16', 'Giữ', 'Đổi assertion cấu hình log (GOV-155)'
    if f.endswith('.java'):
        if '/dto/' in f:
            return 'Mã nghiệp vụ', 'Giữ', 'Bỏ `@Valid` trùng ở khai báo danh sách; phần tử vẫn `@Valid` nên vẫn kiểm từng phần tử (tránh cảnh báo Hibernate Validator vào log). Kiểm bằng test bước 4'
        if re.search(r'/observability/|Telemetry\.java$|LogFields\.java$|SafeStackTracePrinter|CorrelationFilter|CorrelationIdFilter|LogCustomizer', f):
            return 'Mã quan sát', 'Giữ', 'Lớp hỗ trợ log B16/telemetry (trường log, stacktrace an toàn, correlation, thuộc tính span nghiệp vụ)'
        return 'Mã nghiệp vụ', 'Giữ', 'Chèn lệnh ghi log/telemetry B16, không đổi logic (đọc từng dòng ở bước 5)'
    return '?', '?', 'CHƯA PHÂN LOẠI'

rows = []
for st, f in files:
    nhom, qd, ly = loai(f)
    gc = []
    if f in xung_dot:
        gc.append('**xung đột**')
        if f.endswith('.java'):
            ly += '. Xung đột: lấy logic main, chỉ chèn lệnh ghi log của PR'
        if f == 'services/payment-service/.env.example':
            ly += '. Xung đột: ghép dòng `OTEL_*` vào bản main'
    elif f in main_doi:
        gc.append('main cũng đổi, ghép tự động; đọc lại')
    rows.append((nhom, f, 'thêm' if st == 'A' else 'sửa', qd, ly, '; '.join(gc)))

assert not [r for r in rows if r[0] == '?'], [r for r in rows if r[0] == '?']
dem = collections.Counter(r[3] for r in rows)
with open(out, 'w', encoding='utf-8', newline='\n') as o:
    o.write(f'<!-- SINH_TU_DANH_SACH: {len(rows)} file; Giữ {dem["Giữ"]}, Sửa {dem["Sửa"]}, Bỏ {dem["Bỏ"]} -->\n')
    o.write('| # | Nhóm | File | PR | Quyết định | Lý do | Ghi chú ghép |\n|---|---|---|---|---|---|---|\n')
    for i, (nhom, f, st, qd, ly, gc) in enumerate(sorted(rows, key=lambda r: (r[0], r[1])), 1):
        o.write(f'| {i} | {nhom} | `{f}` | {st} | **{qd}** | {ly} | {gc} |\n')
print(len(rows), dict(dem))
print(collections.Counter((r[0], r[3]) for r in rows))
