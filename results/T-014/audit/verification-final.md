# Kiểm bổ sung cuối của nhánh người làm

Ngày 04/10/2026. Đây là phép kiểm nội bộ của người làm T-014, không phải REVIEW của Claude. Chỉ đọc nguồn và kết quả đã có; ngoại lệ một lượt scorer mới được nhánh chính cho phép trước chạy. Không học lại graph, không dùng root label, không mở dữ liệu ngoài ca dev đã chọn.

## 1. Những kết luận hiện khớp bằng chứng

- Đã đối chiếu toàn SPEC, hai hồ sơ chính `ho-so-circa-pc.md`/`ho-so-circa-kien-truc.md`, hai nháp nguồn trong `paper/`, bảng đầu vào, đính chính và đề xuất tài liệu chung. Chưa tìm thấy sai số bảng hay kết luận nguyên nhân duy nhất vượt bằng chứng trong các hồ sơ chính tại lúc đọc.
- Bảng MEM25 ở `audit/bao-cao.md:70–80` khớp hai summary JSON: T006 dùng lại Avg@5=0,888; Rgraph+linear=0,864; SVR=0,960; linear+DA=0,856; SVR+DA=0,864. Không cấu hình nào khớp BARO0,74. Đổi backend/chiều/coverage đồng thời chưa tách được tác động riêng; chỉ các thay đổi scorer trên cùng Rgraph được tách. Hồ sơ PC chính giữ đúng giới hạn này.
- Các sửa T001/T005/T006 ở `dinh-chinh-task-cu.md` có fixture/code pin hỗ trợ. Chúng là sửa mô tả hoặc phạm vi kiểm, không tự phủ nhận các số đã đo của T006. Không sửa file task cũ.
- Bảng `yeu-cau-dau-vao.csv` lúc kiểm có header16 cột và cả4 dòng đều16 cột. Các số273→271→270 của PC và272 scored metric của kiến trúc là các tập khác nhau, không phải số mẫu. Hồ sơ phân biệt rõ train111/test10 và PC600 samples.
- Control kiến trúc chính trỏ `runs/normal-normal-architecture-pretrace/`: trace trước pseudo-mốc, train/test trước tiêm thật. Có60/270 metric≥3, max823,7242. Hồ sơ không gọi ranker là incident detector, không gọi đoạn trước tiêm là healthy được kiểm chứng độc lập, không suy false-positive toàn dataset. Control PC dùng graph cached được giới hạn riêng; chưa phải full pipeline PC normal/normal.
- Ví dụ kiến trúc dùng call graph trước mốc, nhưng prune/mapping dựa600 điểm chứa đoạn sau fault. Hồ sơ chính đã ghi đường thông tin này và không gọi so hai nguồn graph là phép đối chứng chỉ thay graph.

## 2. Hai điểm bàn giao để nhánh chính hoàn thiện

1. `yeu-cau-dau-vao.csv:2–3` lúc đọc dùng `chờ WHY` rút gọn. Prompt yêu cầu ghi nguyên cụm `(chờ WHY, xem de-xuat-tai-lieu-chung.md)` ngay tại nơi dùng lựa chọn quan trọng. Hai hồ sơ chính đã dùng cụm đầy đủ, nhưng CSV chưa nhất quán. Đây là sửa dẫn nguồn quyết định, không đổi cấu hình hay số.
2. CSV hiện chỉ4 dòng adaptation/kiểm cơ chế. Hồ sơ kiến trúc phân biệt cấu hình empirical tác giả SVR(sigmoid)+RHT+DA và interval1min với adaptation T014 linear/interval1s. Đề nghị thêm dòng cấu hình empirical này để task G1 không suy yêu cầu input/time scale từ dòng adaptation. Các biến thể R-pcalg/SVR diagnostic thực sự đã chạy cũng nên có dòng nếu bảng được dùng làm bảng mọi biến thể theo yêu cầu người dùng. Chỉ ghi phần đã kiểm; không gọi diagnostic full600+1s là toàn factory/loader gốc. Default `CaseData` gốc vẫn train111/test10 điểm ở interval1min (`circa/model/case.py:27–40`), không phải train2 điểm. Actual windows của từng factory phải dẫn config cụ thể.

Hai điểm trên đã gửi nhánh chính. Nhánh audit không sửa các file chính.

## 3. Phép kiểm rẻ còn thiếu trong SPEC đã được bù

SPEC:69 yêu cầu đảo cả cột và parents. Các phép kiểm cũ chủ yếu đảo cột trong cùng graph. Vì `parents=list(graph.parents(node))` dùng set (`src/circa_kien_truc/scoring.py:43`; CIRCA gốc `circa/alg/ci/__init__.py:85`), đảo cột không chủ động đổi thứ tự predictors của regression.

Nhánh chính cho phép một lượt mới, dự kiến dưới60s, dùng CIRCA0215 trên đúng graph kiến trúc và ca dev đã chọn. Script `check_architecture_original.py` nạp cùng600 input samples, CaseData interval1s/train111/test10/current=mốc+300, graph cùng nodes/edges, không học graph và không chấm nhãn. Nó lưu mọi metric score trước kết luận.

Kết quả `architecture-original.json`:

- 272 candidate scores khớp snapshot RCAEval; RHT max absolute error4,671349529417057e−9; DA max absolute error4,671363740271772e−9. PASS với atol=rtol=1e−7. Đây là cùng graph/context, không phải protocol empirical1min của bài.
- Chủ động đảo list parents của25 node có ít nhất2 parents: PASS cùng tolerance. Max absolute error2,7226058740836834e−7 ở `ts-travel2-service_latency`, score gốc8,59356280976387. Sai khác này lớn hơn absolute tolerance riêng nhưng nhỏ hơn tổng atol+rtol×|score|. Vì vậy chỉ nói khớp theo tolerance, không nói bit-exact hay maxabs≤1e−7.
- Lượt diagnostic tổng4,460697399976198s, trong đó scorer1,3827109999838285s. Laptop dùng chung; không là runtime chính thức. Log giữ FutureWarning của pandas.

Script chỉ subclass graph trong runtime để đổi thứ tự trả parents, không sửa code pin. Thứ tự node/edge và DA base giữ nguyên. Đây chưa phải kiểm DA trên SCC thay hashseed; fixture SCC/ca PC thuộc bằng chứng khác đã có.

Registry mới ở `architecture-original-cases.csv`:2 dòng lý do(b). Nhánh chính cần gộp vào `ca-da-chay.csv`. Không ghi đè `audit/cases.csv` đã chốt manifest. Các file mới không có trong manifest audit cũ; manifest tổng của nhánh chính cần liệt kê chúng.

## 4. Chi phí và tải: không điền tổng giả

`cost-summary.json` chỉ parse timer/log đã có. Các khối không chồng nhau có timer ghi258,08491s cho nhánh fseOB, nhưng thiếu timer cô lập của scorer factor, R-PC repeat và lượt scorer đầu thất bại. Vì vậy exact total là null. Các mốc filesystem CreationTimeUtc→LastWriteTimeUtc của8 log dataset cộng302,6900649s; cộng2 fixture không dữ liệu là339,5315818s. Đây là wall proxy, không benchmark, không guaranteed upper bound: file có thể tạo sau process start, cleanup có thể chạy sau last write. Các cửa sổ quan sát phù hợp budget15min; không được đổi thành câu “tổng method đo đúng258s” hoặc khẳng định đã chứng minh strict budget từ timer đầy đủ. Setup/download/idle/report không cộng vào method runtime.

Saved distinct payload cộng `source-downloads.csv` là130.204.587B. Lượt setup đầu đã nhận971.145B CRAN PACKAGES metadata rồi gặp Bioconductor403; lần2 tải lại và ghi cùng filepath. Vì vậy known cumulative network là131.175.732B, còn CSV của file cuối chỉ chứa payload distinct. Phân biệt hai đơn vị này để tránh gọi tổngCSV là mọi lần tải mạng. Không tải dataset mới. Nguồn: `r-packages-setup.log`, `r-packages-setup-lan2.log`, `moi-truong-r.md` và `source-downloads.csv`.

## 5. Ranh giới còn giữ

FullPC repeat/permutation đang do nhánh chính quản lý trên EC2; nhánh này không tự gọi đã xong trước output. Full normal-only PC graph, full original experiment factory, lệnh/code thật sinh bảng BARO và ảnh hưởng riêng backend/chiều/candidate trên toàn dataset vẫn chưa kiểm theo giới hạn đã ghi. Việc chưa có protocol tác giả không được đổi thành thiếu quyền cài R; R đã dựng userspace và chạy thật. Không có phép methodrun hay dữ liệu mới nào khác trong lượt kiểm cuối này.
