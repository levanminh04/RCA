# Phân tích chênh lệch nguồn và graph T-039

Kết quả **tham khảo có điều kiện** vì chưa xác minh ứng dụng/build/image/deployment sinh dataset. Đã dùng đủ graph dev được giao, không chọn ca theo nhãn, không đọc telemetry thô. Đây là phân tích mô tả và source mechanism candidate; chưa có kết luận nguyên nhân vật lý của mọi cạnh thiếu hoặc lợi ích RCA.

Chuỗi bằng chứng máy đọc nằm tại `runs/phan-tich-002/source-to-difference.json`: `/cells` có từng graph/interval/mẫu số; `/chains` có toàn khóa match/static-only/trace-only, source records/provenance, member gốc và danh sách cửa sổ; `/excluded_edge_groups` giữ raw edge, mapping từng đầu và tất cả vị trí bị loại. `/groups` phân xử từng giải thích revision/alias/domain/window/branch/static/telemetry/conversion, không cộng cờ thành phần trăm nguyên nhân.

| Mức | Cửa sổ | Số graph | Cạnh trace gốc | Cạnh đủ điều kiện endpoints | Bị loại |
|---|---|---:|---:|---:|---:|
| entity | A | 2 | 11 | 11 | 0 |
| entity | A | 20 | 13 | 13 | 0 |
| entity | N | 22 | 13 | 13 | 0 |
| entity | full | 22 | 13 | 13 | 0 |
| operation | A | 2 | 52 | 10 | 42 |
| operation | A | 1 | 62 | 9 | 53 |
| operation | A | 19 | 63 | 10 | 53 |
| operation | N | 22 | 63 | 10 | 53 |
| operation | full | 22 | 63 | 10 | 53 |

## G1. Entity RPC paths and window-specific absences

64/66 entity graphs have eligible13/intersection13; two A graphs have11. Same opaque ID N/full contain checkout→email/payment. checkout→currency is static-only in all66.

Graph set changes are observed within saved dev windows. Code Convert uses context.TODO at main.go471; this is a candidate context-propagation difference, not proof that this code generated dataset or sole cause. Other checkout RPC calls with propagated ctx are matched at entity level.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/src/checkoutservice/main.go:L178–239;L451–483`; `results/T-039/sources/augmented-ob-94a01ba4/src/frontend/rpc.go:RPC client calls`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: OPEN: no image/build/deployment link; alias: Exact entity identities verified for this source; still deployment scope conditional; domain_window: SUPPORTED observed difference between A and N/full; full is not whole day; branch: Code has request/error branches; actual execution/calls not known from graph alone; incomplete_static_source: Code call exists, so absence of source record not explanation for this key; external runtime version OPEN; missing_telemetry: Unresolved; no raw-span/export lineage permission/evidence; conversion_error: Set/members/interval checks PASS; graph producer/runtime conversion not proven complete.

Phần cần thêm: Exact app/deployment/export lineage and authorized call/context observations before assigning physical missing-edge cause.

## G2. Source data dependencies versus service-owned SQL spans

Static ad→logical DB, productcatalog→logical DB, cart→Redis are static-only across entity graphs. Three observed SQL operation names have no source literal candidate; do not map sql.rows into a database entity. DB signals shared on instance retain one binding per logical DB.

Source DB/cache endpoint and logical DB name are explicit. Saved operation IDs keep owner application, so SQL spans alone do not supply an independently identified DB/cache component under current mapping. This distinguishes source data capability from trace service-call endpoints; it does not show why all datastore telemetry is absent.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/src/adservice/src/main/java/hipstershop/AdService.java:L237–257`; `results/T-039/sources/augmented-ob-94a01ba4/src/productcatalogservice/server.go:L55–91;L188–214;L238–298`; `results/T-039/sources/augmented-ob-94a01ba4/src/cartservice/src/Startup.cs:Redis vs Local branch`; `results/T-039/sources/augmented-ob-94a01ba4/src/cartservice/src/cartstore/RedisCartStore.cs:Redis calls/health/init`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: OPEN; alias: SQL instrumentation→logical DB identity/operation unverified; cannot turn owner into resource; domain_window: No DB/cache node in all authorized saved graphs; says nothing about whole day; branch: Redis mode conditional on REDIS_ADDR; source configured Redis but actual runtime not verified; incomplete_static_source: Source records exist; exact library/export schema OPEN; missing_telemetry: Cannot separate unrecorded, unexported, unmapped or excluded data using saved graph alone; conversion_error: T039 preserves unknown owner and refuses unsupported aliases; upstream adapter attributes need separately authorized evidence.

Phần cần thêm: OTel DB/cache attributes, endpoint namespace and exporter field mapping; logical DB→instance→host validity intervals.

## G3. Manual span literal versus code function boundaries in AdService

AdImpl/getAds is an explicit renamed @WithSpan span and maps to canonical GetAds. createAdsMap has no @WithSpan; it calls Span.current().updateName. getAdsByCategory/getRandomAds call createAdsMap before renaming their current span. createAdsMap source operation is inventory capability but not proven independent span.

Under this source, helper rename changes current span rather than constructing a helper span. Later category/random rename can overwrite that name. Thus function nesting and span nesting can differ even without lost telemetry. Saved SQL edges from category/random are excluded by SQL mapping, not silently declared static mismatch.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/src/adservice/src/main/java/hipstershop/AdService.java:L116–121;L169–173;L190–197;L227–257`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: OPEN: source mechanism not dataset attribution; alias: Handler explicit literal verified; createAdsMap literal exists but no observed node; domain_window: No createAdsMap node in union authorized operation graphs, not universal runtime absence; branch: Context/random paths conditional; both corresponding caller→helper keys observed in some authorized windows; incomplete_static_source: Agent bytecode/filter/library may alter span behavior; not fully inspected; missing_telemetry: Not established; no need to assume loss to explain source function/span discrepancy; conversion_error: Static source calls are intentionally not span-parent; source records/context preserved; independent key checks PASS.

Phần cần thêm: Exact runtime agent/source link and span naming lifecycle to select operation-level modeling in P6.

## G4. Explicit manual spans, generated RPC names and mapping exclusions

Observed union55 operation nodes:20 verified by explicit runtime literal,32 unverified candidates,3 SQL unmapped. All 66 operation graphs are processed, including raw edges excluded from eligible T. Most63 raw edges reduce to10 eligible; one A reduces9. Trace_fraction1 measures this selected eligible subset.

Entity identity and exact explicit runtime span name require separate evidence. Generated gRPC method path establishes invocation capability/owner, not final instrumentation span name. Same name text without literal proof remains unverified; six slash/grpc prefix candidates are explicit scoped proposals, not automatic normalization. Comparison excludes edges whose endpoint mapping is unverified/unmapped before set intersection.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/src/recommendationservice/recommendation_server.py:L63–84;L98–105`; `results/T-039/sources/augmented-ob-94a01ba4/src/recommendationservice/demo_pb2_grpc.py:L143–158`; `results/T-039/sources/augmented-ob-94a01ba4/src/frontend/main.go:L212`; `results/T-039/sources/augmented-ob-94a01ba4/src/shippingservice/main.go:L285–301`; `results/T-039/sources/augmented-ob-94a01ba4/src/checkoutservice/main.go:L275–306;L432–473`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: OPEN for every mapping; alias: Exact runtime literals supported20; remaining names not verified even when syntax identical; domain_window: All current dev graphs compared; no new window; branch: No exclusion is evidence branch failed to run; excluded raw edges remain saved; incomplete_static_source: Library naming source/exact deployed version absent; missing_telemetry: Excluded edges are present graph data, so cannot call these telemetry missing merely due fraction; conversion_error: Owner-conflict oracle/independent membership checks; source matching not optimized to eligible fraction.

Phần cần thêm: Exact selected library naming/Health binding and binary/build identity, before promoting candidates. Do not create SQL fake operations.

## G5. Client/browser/loadgenerator and exporter domains

Static-only loadgenerator→frontend, web-client→frontend and two browser stylesheets have source locators. Mysql exporter→mysql exists only in exporter deployment variant. gstatic preconnect kept as inventory hint with no HTTP edge. These are not unseen app-to-app RPC claims.

Inventory must include source scopes beyond traced services, while comparison remains dev-adapter. Exporter variant, resource browser requests and external resource hints remain conditional; their static-only status cannot imply internal RPC collector failure.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/src/loadgenerator/locustfile.py:UserBehavior/tasks and requests`; `results/T-039/sources/augmented-ob-94a01ba4/src/frontend/templates/header.html:L26–30`; `results/T-039/sources/augmented-ob-94a01ba4/kubernetes-manifests/mysql_exporter.yaml:L38–55`; `results/T-039/sources/augmented-ob-94a01ba4/kubernetes-manifests/start_with_istio_exporter.sh:L3–4`; `results/T-039/sources/augmented-ob-94a01ba4/kubernetes-manifests/start_demo_with_istio.sh:L3–4`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: Source/deployment image link OPEN; alias: No forced browser/exporter alias to application service; domain_window: SUPPORTED structural scope difference in record contexts; actual sampling boundaries still OPEN; branch: Exporter variants not unioned as simultaneous deployment; browser fetch may not occur; incomplete_static_source: External CSS/Redis exporter defaults/collector config absent; not invented; missing_telemetry: Unresolved and not inferred from external/static-only scope; conversion_error: Incorrect gstatic edge removed during source audit; records/graph now match allowed source relation semantics.

Phần cần thêm: Effective deployment/browser/load profile and collector scope only if runtime coverage claim is requested.

## G6. Operation difference isolated to one saved A window

PrepOrderItems→ConvertCurrency is static-only in one A graph, matched in N/full same opaque ID and other operation graphs. No average is used to hide this cell.

Same source mapping and normalization yield match in N/full, absence in one A. This controls mapping policy for the comparison but does not identify code execution, sampling, failure or branch cause.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/src/checkoutservice/main.go:prepOrderItems and convertCurrency call path`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: Same saved-case graph reference does not resolve deployment provenance; alias: Both endpoints verified explicit literals; mapping policy not changed between windows; domain_window: SUPPORTED observable A vs N/full edge-set difference; branch: Request composition/error return/empty items plausible but not observed here; incomplete_static_source: Call record present; actual runtime revision OPEN; missing_telemetry: Still possible; no evidence separates it from unexecuted branch; conversion_error: Saved output correctly reflects saved graph edge absence under identical mapping; source graph production remains conditional.

Phần cần thêm: Authorized request/span sequence and source revision to attribute this per-window absence.

## G7. Typed unknown, source independence and Node identity

Typed excludes all eligible trace edges as unknown_type, yielding trace denominator0 and null fraction. Unknown type is not known wrong type. Source NodeName from Kubernetes spec.nodeName cannot alone identify dataset Node. Producer of daily Source/Target/Node was not found in seven Python source files audited; not whole repo absence.

Endpoints comparison deliberately removes type; typed comparison refuses unknown. Daily metadata might share trace provenance; alarm.NetworkP90 code derives from trace. None proves independently collected host/network measurements. Lineage.md has exact Nezha source locators.

Bằng chứng: `results/T-039/sources/augmented-ob-94a01ba4/kubernetes-manifests/productcatalogservice.yaml:NODE_NAME valueFrom spec.nodeName`. Các key và source records/members tương ứng lấy bằng ID trong `/groups/*/mismatch_keys` và `matched_counterparts`, dẫn `/chains/*/id`; không chỉ một hình đồ thị.

Phân xử: revision: OPEN; alias: Resource schema/Node mapping OPEN; domain_window: Daily metadata domain not equivalent to dev-adapter windows; branch: Not resolved from type/metadata; incomplete_static_source: Exporter/collector producer not in audited files, exact missing sources identified; missing_telemetry: Cannot infer from unknown typing alone; conversion_error: T039 keeps type unknown and null denominator, oracle verifies this behavior.

Phần cần thêm: Producer/config/input schema/version/effective time; explicit service-instance-pod-host bindings and OTel semantic fields for P9.

## Kết luận giới hạn và bước nhận

Entity endpoints phản ánh các quan hệ service gọi nhau có nguồn; thao tác chỉ so được phần mapping có bằng chứng literal. DB/cache, external/browser, exporter và source-only helper có ý nghĩa/điều kiện khác với các cạnh trace service, nên không gom tất cả thành “trace thiếu”. Graph tĩnh không đại diện một lượt thực thi; graph full không cả ngày. Static-only có thể đồng thời là match ở cửa sổ khác; bảng `/chains/*/occurrences` giữ điều đó.

Sự tương ứng nguồn→bản ghi→khóa→mapping→tập đã kiểm trong T039. Nguyên nhân runtime cần app/deployment/agent/collector lineage cùng dữ liệu được giao đúng quyền. T040 nhận kết quả tham chiếu và các OPEN; P6 chưa được chọn cơ chế từ tỷ lệ; P9 nhận yêu cầu identity, địa chỉ tín hiệu và nguồn độc lập. Đề xuất bổ sung/owner/chi phí tại `de-xuat-bo-sung-nguon.md` và `ban-giao.md`. Chưa nhận đủ inventory toàn deployment, chưa đóng RQ3/RQ5/P5/G3.
