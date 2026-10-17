# Mapping theo nguồn — T-039

Hỗ trợ người làm, không là phản biện chính thức. Không chạy build/compare hoặc nạp src hiện hành. Chỉ ghi hai file trong run này. Không đọc raw telemetry/nhãn/test/heldout.

## Kiểm nguồn và miền

Đã kiểm hash 6 artifact T-039, 132 graph/3856723 byte và 59 nguồn OB theo registry/acquisition trước dùng. Manifest T-035 khớp hash được giữ trong T-036 pin. Canonical set trùng graph-inventory; không gom graph lịch sử. JSON giữ hash từng file.

Union gồm 10 entity và 55 operation; giữ owner, mỗi original có một proposal. verified chỉ xác nhận định danh theo source snapshot; app-to-dataset revision vẫn OPEN, không xác nhận telemetry đầy đủ.

## Hai cập nhật inventory nguồn root cần hợp

1. `src/adservice/src/main/java/hipstershop/AdService.java:L106–123`: AdServiceImpl.getAds có @WithSpan, L121 gọi updateName("hipstershop.AdServiceImpl/getAds"). Backend hiện để design operation hipstershop.AdService/GetAds runtime_name=null. Root đã xác nhận sẽ ghi actual literal vào runtime_name của design operation. Proposal observed AdServiceImpl/getAds → design GetAds verified=true phụ thuộc cập nhật này; observed AdService/GetAds vẫn candidate chưa verified. Không tự coi hai observed span names là hai alias đã được xác minh.
2. `src/recommendationservice/recommendation_server.py:L63–72,L99–105` và `src/recommendationservice/demo_pb2_grpc.py:L154–157`: local client owner recommendationservice gọi ListProducts, generated path là /hipstershop.ProductCatalogService/ListProducts. Root xác nhận bổ sung declared local client operation; runtime_name vẫn null. Proposal giữ owner recommendationservice, verified=false; không map nhầm sang owner productcatalogservice. Generated RPC path chưa xác minh span-name literal.

## Rà Go và điều kiện

- `src/checkoutservice/main.go:L453–473`: manual ConvertCurrency nhận ctx qua tracer.Start; RPC Convert dùng context.TODO() ở L471. Gọi đồng bộ vẫn có trong code. Không suy span parent hoặc quy nguyên nhân dataset khi chưa nối revision/thư viện.
- Go có 35 relations gọi-đồng-bộ/internal và 0 span-parent. Mọi condition internal nói không khẳng định span parent/runtime ancestry; khả năng gọi theo source không xác nhận nhánh đã chạy.
- `src/shippingservice/main.go:L285–301`: CreateQuoteFromCount đánh giá quoteByCountFloat trước rồi gọi CreateQuoteFromFloat; cả hai nhận ctx từ CreateQuoteFromCount. Không dựng QuoteByCountFloat→CreateQuoteFromFloat.
- Health Go: checkout L174–195, product L180–181,L279–285, shipping L167–187 có register/Check/Watch. Check trả SERVING, Watch trả Unimplemented; runtime_name null. Proto snapshot chỉ khai Check, phần generated health/reflection dependency chưa đọc. Không nhận thư viện coverage đầy đủ.
- `src/shippingservice/main.go:L171–172` đăng ký reflection; chưa có source operation inventory của dependency. Go RPC method descriptors/Invoke chỉ xác nhận method identity; otelgrpc0.23.0 actual naming chưa đọc.

## SQL và tên thư viện

- adservice/SELECT addatabase.aditems: AdService.java:L227–279 xác nhận JDBC query/logical DB, chưa có actual SQL span naming literal; candidates=[]; không tạo operation để match.
- productcatalogservice/sql.conn.query và sql.rows: server.go:L188–214,L217–252,L313–347 và go.mod:L25–27 cho thấy otelsql/QueryContext/rows, nhưng actual naming ở dependency chưa đọc. candidates=[]; không map toàn SQL span sang ReadCatalog/GetProduct.

## Toàn bộ originals và trạng thái

Entity verified 10/10. Operation verified literal 20/55; unverified candidates 32; no candidate 3. Đây là trạng thái định danh, chưa đo cạnh giao/phần riêng hoặc độ phủ telemetry.

| Level | Original giữ nguyên | Trạng thái | Candidate |
|---|---|---|---|
| entity | `adservice` | verified | `adservice` |
| entity | `cartservice` | verified | `cartservice` |
| entity | `checkoutservice` | verified | `checkoutservice` |
| entity | `currencyservice` | verified | `currencyservice` |
| entity | `emailservice` | verified | `emailservice` |
| entity | `frontend` | verified | `frontend` |
| entity | `paymentservice` | verified | `paymentservice` |
| entity | `productcatalogservice` | verified | `productcatalogservice` |
| entity | `recommendationservice` | verified | `recommendationservice` |
| entity | `shippingservice` | verified | `shippingservice` |
| operation | `["adservice","SELECT addatabase.aditems"]` | unmapped, OPEN | [] |
| operation | `["adservice","hipstershop.AdService/GetAds"]` | candidate, unverified | `["adservice","hipstershop.AdService/GetAds"]` |
| operation | `["adservice","hipstershop.AdService/getAdsByCategory"]` | verified | `["adservice","hipstershop.AdService/getAdsByCategory"]` |
| operation | `["adservice","hipstershop.AdService/getRandomAds"]` | verified | `["adservice","hipstershop.AdService/getRandomAds"]` |
| operation | `["adservice","hipstershop.AdServiceImpl/getAds"]` | verified | `["adservice","hipstershop.AdService/GetAds"]` |
| operation | `["cartservice","hipstershop.CartService/AddItem"]` | candidate, unverified | `["cartservice","hipstershop.CartService/AddItem"]` |
| operation | `["cartservice","hipstershop.CartService/EmptyCart"]` | candidate, unverified | `["cartservice","hipstershop.CartService/EmptyCart"]` |
| operation | `["cartservice","hipstershop.CartService/GetCart"]` | candidate, unverified | `["cartservice","hipstershop.CartService/GetCart"]` |
| operation | `["checkoutservice","hipstershop.CartService/EmptyCart"]` | candidate, unverified | `["checkoutservice","hipstershop.CartService/EmptyCart"]` |
| operation | `["checkoutservice","hipstershop.CartService/GetCart"]` | candidate, unverified | `["checkoutservice","hipstershop.CartService/GetCart"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/ChargeCard"]` | verified | `["checkoutservice","hipstershop.CheckoutService/ChargeCard"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/ConvertCurrency"]` | verified | `["checkoutservice","hipstershop.CheckoutService/ConvertCurrency"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/EmptyUserCart"]` | verified | `["checkoutservice","hipstershop.CheckoutService/EmptyUserCart"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/GetUserCart"]` | verified | `["checkoutservice","hipstershop.CheckoutService/GetUserCart"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/PlaceOrder"]` | candidate, unverified | `["checkoutservice","hipstershop.CheckoutService/PlaceOrder"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/PrepOrderItems"]` | verified | `["checkoutservice","hipstershop.CheckoutService/PrepOrderItems"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/PrepareOrderItemsAndShippingQuoteFromCart"]` | verified | `["checkoutservice","hipstershop.CheckoutService/PrepareOrderItemsAndShippingQuoteFromCart"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/QuoteShipping"]` | verified | `["checkoutservice","hipstershop.CheckoutService/QuoteShipping"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/SendOrderConfirmation"]` | verified | `["checkoutservice","hipstershop.CheckoutService/SendOrderConfirmation"]` |
| operation | `["checkoutservice","hipstershop.CheckoutService/ShipOrder"]` | verified | `["checkoutservice","hipstershop.CheckoutService/ShipOrder"]` |
| operation | `["checkoutservice","hipstershop.EmailService/SendOrderConfirmation"]` | candidate, unverified | `["checkoutservice","hipstershop.EmailService/SendOrderConfirmation"]` |
| operation | `["checkoutservice","hipstershop.PaymentService/Charge"]` | candidate, unverified | `["checkoutservice","hipstershop.PaymentService/Charge"]` |
| operation | `["checkoutservice","hipstershop.ProductCatalogService/GetProduct"]` | candidate, unverified | `["checkoutservice","hipstershop.ProductCatalogService/GetProduct"]` |
| operation | `["checkoutservice","hipstershop.ShippingService/GetQuote"]` | candidate, unverified | `["checkoutservice","hipstershop.ShippingService/GetQuote"]` |
| operation | `["checkoutservice","hipstershop.ShippingService/ShipOrder"]` | candidate, unverified | `["checkoutservice","hipstershop.ShippingService/ShipOrder"]` |
| operation | `["currencyservice","grpc.hipstershop.CurrencyService/Convert"]` | candidate, unverified | `["currencyservice","hipstershop.CurrencyService/Convert"]` |
| operation | `["currencyservice","grpc.hipstershop.CurrencyService/GetSupportedCurrencies"]` | candidate, unverified | `["currencyservice","hipstershop.CurrencyService/GetSupportedCurrencies"]` |
| operation | `["currencyservice","hipstershop.CurrencyService/Carry"]` | verified | `["currencyservice","hipstershop.CurrencyService/Carry"]` |
| operation | `["currencyservice","hipstershop.CurrencyService/GetCurrencyData"]` | verified | `["currencyservice","hipstershop.CurrencyService/GetCurrencyData"]` |
| operation | `["emailservice","/hipstershop.EmailService/SendOrderConfirmation"]` | candidate, unverified | `["emailservice","hipstershop.EmailService/SendOrderConfirmation"]` |
| operation | `["frontend","hipstershop.AdService/GetAds"]` | candidate, unverified | `["frontend","hipstershop.AdService/GetAds"]` |
| operation | `["frontend","hipstershop.CartService/AddItem"]` | candidate, unverified | `["frontend","hipstershop.CartService/AddItem"]` |
| operation | `["frontend","hipstershop.CartService/GetCart"]` | candidate, unverified | `["frontend","hipstershop.CartService/GetCart"]` |
| operation | `["frontend","hipstershop.CheckoutService/PlaceOrder"]` | candidate, unverified | `["frontend","hipstershop.CheckoutService/PlaceOrder"]` |
| operation | `["frontend","hipstershop.CurrencyService/Convert"]` | candidate, unverified | `["frontend","hipstershop.CurrencyService/Convert"]` |
| operation | `["frontend","hipstershop.CurrencyService/GetSupportedCurrencies"]` | candidate, unverified | `["frontend","hipstershop.CurrencyService/GetSupportedCurrencies"]` |
| operation | `["frontend","hipstershop.Frontend/Recv."]` | verified | `["frontend","hipstershop.Frontend/Recv."]` |
| operation | `["frontend","hipstershop.ProductCatalogService/GetProduct"]` | candidate, unverified | `["frontend","hipstershop.ProductCatalogService/GetProduct"]` |
| operation | `["frontend","hipstershop.ProductCatalogService/ListProducts"]` | candidate, unverified | `["frontend","hipstershop.ProductCatalogService/ListProducts"]` |
| operation | `["frontend","hipstershop.RecommendationService/ListRecommendations"]` | candidate, unverified | `["frontend","hipstershop.RecommendationService/ListRecommendations"]` |
| operation | `["frontend","hipstershop.ShippingService/GetQuote"]` | candidate, unverified | `["frontend","hipstershop.ShippingService/GetQuote"]` |
| operation | `["paymentservice","grpc.hipstershop.PaymentService/Charge"]` | candidate, unverified | `["paymentservice","hipstershop.PaymentService/Charge"]` |
| operation | `["productcatalogservice","hipstershop.ProductCatalogService/GetProduct"]` | candidate, unverified | `["productcatalogservice","hipstershop.ProductCatalogService/GetProduct"]` |
| operation | `["productcatalogservice","hipstershop.ProductCatalogService/ListProducts"]` | candidate, unverified | `["productcatalogservice","hipstershop.ProductCatalogService/ListProducts"]` |
| operation | `["productcatalogservice","hipstershop.ProductCatalogService/ParseCatalog"]` | verified | `["productcatalogservice","hipstershop.ProductCatalogService/ParseCatalog"]` |
| operation | `["productcatalogservice","hipstershop.ProductCatalogService/ReadCatalog"]` | verified | `["productcatalogservice","hipstershop.ProductCatalogService/ReadCatalog"]` |
| operation | `["productcatalogservice","sql.conn.query"]` | unmapped, OPEN | [] |
| operation | `["productcatalogservice","sql.rows"]` | unmapped, OPEN | [] |
| operation | `["recommendationservice","/hipstershop.ProductCatalogService/ListProducts"]` | candidate, unverified | `["recommendationservice","hipstershop.ProductCatalogService/ListProducts"]` |
| operation | `["recommendationservice","/hipstershop.RecommendationService/ListRecommendations"]` | candidate, unverified | `["recommendationservice","hipstershop.RecommendationService/ListRecommendations"]` |
| operation | `["shippingservice","hipstershop.ShippingService/CreateQuoteFromCount"]` | verified | `["shippingservice","hipstershop.ShippingService/CreateQuoteFromCount"]` |
| operation | `["shippingservice","hipstershop.ShippingService/CreateQuoteFromFloat"]` | verified | `["shippingservice","hipstershop.ShippingService/CreateQuoteFromFloat"]` |
| operation | `["shippingservice","hipstershop.ShippingService/GetQuote"]` | candidate, unverified | `["shippingservice","hipstershop.ShippingService/GetQuote"]` |
| operation | `["shippingservice","hipstershop.ShippingService/QuoteByCountFloat"]` | verified | `["shippingservice","hipstershop.ShippingService/QuoteByCountFloat"]` |
| operation | `["shippingservice","hipstershop.ShippingService/ShipOrder"]` | candidate, unverified | `["shippingservice","hipstershop.ShippingService/ShipOrder"]` |

## Kiểm tra và phần còn mở

Proposal attempt1 dừng trước ghi output vì assertion phân loại không xử lý design method có actual runtime_name khác observed. Đã sửa phân loại; giữ design-name observed unverified và chỉ actual literal verified. Attempt2 kiểm đủ originals/owner/candidate/provenance/hash bằng JSON thuần, không gọi builder.

Root cần hợp đúng hai inventory updates, đối chiếu candidate IDs với document cuối rồi mới dùng proposal. Không tự nâng các RPC trùng văn bản hoặc khác slash/grpc-prefix. Muốn nâng phải có actual naming source của instrumentation đúng revision; không tải dependency bằng quyền này.

Hash source không đồng nghĩa đã đọc mọi semantics của toàn file. Lượt này đọc identity/register/span literal/generated method và các điều kiện Go nêu trên. Coverage toàn snapshot, collector/export schema, Node, lineage nguồn phụ và revision link vẫn OPEN theo task; không nhận đã phân xử từ mapping. Chỉ ghi mapping-proposals.json/source-notes.md; không sửa parts/LOG/STATE/shared code.
