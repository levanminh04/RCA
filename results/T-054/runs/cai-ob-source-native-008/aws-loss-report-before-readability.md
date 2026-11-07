# AWS tạm khóa — hệ quả nếu dữ liệu hai EC2 mất

Ngày06/11/2026. Minh yêu cầu tạm dừng riêng phần cloud, tiếp phần khác và báo hệ quả. Tài khoản bị tạm khóa là USER_CONFIRMED; dữ liệu đã bị xóa là OPEN. Không đăng nhập quản trị AWS, không SSH lại/bật/tắt/cấp máy/tải lại/chạy lại thực nghiệm trong lượt đánh giá này.

## Phần hiện có local
Kiểm hash theo manifest: T048 local outputs+closed_outputs2168/2168; T0491020/1020; T0532654/2654; T032 gói bổ sung6224/6224; T033 gói báo cáo cuối29/29. Đây là các gói cụ thể, không là kiểm đủ mọi file từng tồn tại trênEC2. Chi tiết/đường dẫn và các mục không khớp nằm trong aws-loss-local-audit.json#/groups. T011 kiểm142/142artifacts local khớp. T010 có93/94khớp, riêng the-dataset.md lệch manifestcũ; không dùng thẻ này làm căn cứ mấtraw/đãxácnhậnpackage, không tự mở lại taskđóng.

Nguồn P7: stat hiện tại và metadata đãkiểmhash cho thấy TT180/180file=1.309.388.082byte; Nezha226/226=1.598.103.311byte; TORAI A180/180CSV=9.244.910byte đều cólocal và đúngbyte. Không đọc giá trị test; không băm lại toànraw vì receipt006 cònđượcgiữ. Xem aws-loss-main-source-presence.json. Code/đặc tả/đầu ra008 đang ở repo local, chưa stagecloud. Không có kết quảmainP7 cần cứu vì mainchưa chạy.

## Rủi ro cụ thể T048
ManifestT048#/remote_frozen_artifacts ghi925fileđầyđủ trênEC2_2. Hiện587cólocal đúnghash;338mục không có tại đườnglocal trongmanifest, tổng1.814.750.134byte. Trong đó48ban-ghi.jsonl=152.768.449byte;48trung-gian.jsonl=1.655.201.305byte; phầncòn lại làcommand/kiểm/progress/stdout/stderr. Chúng thuộc24lượt t4-ec2-001-* và24lượt t4b-ec2-001-*, thêm2logcha. Không thấy counterpart.gz hoặc archive trongmanifestT048; chưa chứng minh không cóbackupngoài các đườngđãrà. Xem aws-loss-consequences.json#/T048_remote_catalog_missing_local.

Nếu remote mất và không cóbackupkhác: mấtbản ghi và trung gian gốc của phần này. Báocáo/T4/T4b/luậtC/cơchếvàcác đầu rađãnhậnlocal không tự biến mất hoặc tự sai; nhưng khả năng kiểm lại/chạy phân tích mới trên fullintermediate bị giảm. Manifest/hash chỉ chứng minh đã có bản nào, không phục hồi nội dung. Tái chạy về sau (nếu thật sự cần) là lượt mới với provenance/môi trường mới, không được gọi là lấy lại byte của lượt cũ; không mặc định chạy lại toàn bộ hoặc tự mở taskđãđóng.

## Các phần khác
T032/T033/T049/T053 đã có các gói local nêu trên nên không có căn cứ nói toàn bộ nền nghiên cứu mất. Những scratch/cache/fullraw/lượt hỏng chỉremote chưa cóinventoryđối chiếu toàn bộ vẫnOPEN; không lấy sự cómặt của gói báo cáo làm chứng minh mọi remote fileđãbackup.

Theo inventory005 và data/README, DeepTraLog/LEMMA raw ở rca-t003 trênEC2_2; repo giữ hồsơ/biênnhận/schema/kết quảkhảo sát. Không cóbảnsao raw đượcxácnhậnởcáccây local đãrà. Nếu mất thì cần tải lại đúngrevision/hash khi nguồn còntruycậpđược, kèm kiểmphầncần dùng; chưa tải hoặc đoán ETA/dung lượngmới. Đây không phải nguồnTT/Nezhađangdùngchomain.

Mất môi trườngLinux/T025/py38/codepackage/caches: cần dựng lại trên máyphùhợp từpin/recipe, xácminhsource/env vàparity đúngphần khác; không tự coi Windowsthay Linux tươngđương, cũng khôngphải lýdochạy lạibaseline/devđãhợp lệ. Mốc runtime/identitymáycũ giữ nghĩa lịch sử, không coi là sốđomáymới. DữliệugốcTT/OB/Astage trênEC2 làbản sao nên cóthểchuyểnlại từlocal sauquyền/nguồnmáyphùhợp, không cần tảilạinguồn.

## Hệ quả với kế hoạch hiện tại
Tạmngưng35/25trên2EC2, sync và kiểm máy theo chỉđạoMinh. Không tự dồnmainlênlaptop hoặc cấpmáykhác. Tiếp kiểm/localdocumentation vàchuẩnbịRE3metadata hợp lệ. OBpatch đã có44kiểm source/defaultsynthetic,92kiểmtíchhợp và1DEVworkerexact; candidate008vẫnWAIT_G3. Chưađạt bước3cloud hoặcG3. Hai phần cần giữOPEN khi trìnhG3: quyền/môi trườngmáy chạy thực; nguồn/đơnvị/inventory/support/adapterRE3. CầnMinhquyết hạ tầng sau khi xửlýtàikhoản, không cầnbỏkếtquảnghiêncứuđãcólocal.
