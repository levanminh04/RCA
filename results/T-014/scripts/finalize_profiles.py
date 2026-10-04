"""Publish the technical profiles from saved evidence; no new method run."""
from pathlib import Path
import re

root=Path('D:/RCA-flashticket/results/T-014')
for kind in ['pc','kien-truc']:
    text=(root/f'paper/ho-so-circa-{kind}-draft.md').read_text(encoding='utf-8-sig')
    text=text.replace('Đây là nháp nguồn cho người làm T-014 tích hợp; ví dụ PC mặc định đã có kiểm số học và raw input độc lập.',
                      'Ví dụ mặc định đã được tính lại độc lập từ raw input tới từng điểm số. Hồ sơ phục vụ P1/G1; cấu hình P3 còn OPEN.')
    text=text.replace('Đây là nháp nguồn; số thực nghiệm phải bổ sung từ file kết quả.',
                      'Các phép kiểm dưới dẫn trực tiếp file kết quả. Hồ sơ phục vụ P1/G1; cấu hình P3 còn OPEN.')
    if kind=='pc':
        extra='''
**Quy mô và kiểm trên ca thật.** PC mặc định học 600×273, hoàn tất trên EC2 sau1796.2688s; RHT0.8317s và270 score hữu hạn. Supervisor quan sát peak RSS5,204,905,984B. Đây là thời gian có instrumentation, không phải benchmark sạch: máy dùng chung, monitor chỉ chứng minh không thấy Python/R worker khác trong lượt hoàn tất, không loại trừ tải nền. Hai lượt dừng360.1923/780.3469s vẫn tính vào tổng. Nguồn: `runs/ec2-default-003/progress.jsonl`, `supervisor.jsonl`, `status.json`; tổng ngân sách ở `runs/chi-phi-tong.json`.

**Phân biệt phép kiểm.** Scorer trên graph lưu sẵn lặp và đảo thứ tự cột khớp; nó chưa chứng minh PC discovery bất biến theo permutation. FullPC permutation được xếp hàng trên EC2 với4170s gồm cả chờ; kết quả cuối ở `runs/ec2-default-permuted/status.json` và `kiem-tra-va-doi-chieu-spec.md`. Đối chứng normal/normal trên graph học từ incident có76/268metric≥3, top security_mem922.01035; đây chỉ là kiểm scorer có điều kiện trên fault graph, không thay PC học riêng hai cửa sổ normal. Không diễn giải top1 đó là root có nghĩa. Nguồn: `runs/pc-cached-checks.json`.

Graph ca thật có112SCC tổng, trong đó6SCC nhiều hơn một node, lớn nhất149. RHT trên hashseed0/1 được so riêng với DA trong `paper/crossseed-pc.json`: dùng actual iteration order để khớp số là kiểm thực thi, không bảo đảm suy ancestor trong SCC. PCdepth0 alpha.05 trên cùng273biến chưa trả graph sau2703.969s trên laptop dùng chung; không suy cap depth luôn rẻ hơn. Chưa lấy stack để phân xử chi phí orientation và skeleton, nên nguyên nhân runtime còn OPEN. Nguồn: `runs/pc-depth0-alpha005/status.json`.

**Điều tra số công bố.** Ô MEMfseOB của T006 Avg5=.888, so mốc công bố=.74. Trên25ca MEM đã được phép chạy trước, backend R/pcalg gốc với linearRHT cho.864; SVR cho.960; linear+DA cho.856; SVR+DA cho.864 (`audit/mem-target-summary.json`, `audit/mem-prior-config-summary.json`). Không cấu hình nào tái lập.74. Backend, hướng cạnh và coverage cùng đổi ở đối chiếu graph; phần giảm.024 không tách được thành đóng góp riêng của mỗi yếu tố. Scorer gốc và RCAEval dùng cùng graph/window khớp trên2ca (`audit/summary.json`); vì vậy chưa có bằng chứng quy toàn khoảng lệch cho công thức RHT. Giao thức sinh bảng công bố, windows/preprocessing/phiên bản cụ thể vẫn OPEN; cần lệnh/artifact tương ứng để phân xử. Không chọn biến thể từ độ khớp hay accuracy.

'''
        text=text.replace('## 8. Đường nhãn',extra+'## 8. Đường nhãn')
        text += '\nAdapter `src/circa_kien_truc/scoring.py` của T014 chỉ hỗ trợ các suffix đã mapping, đủ ca TT đang kiểm. Wrapper PC gốc chỉ tách `service_metric`, có thể nhận suffix khác như load; không suy adapter T014 là triển khai PC phổ quát.\n'
    else:
        extra='''
**Kiểm builder trên30ca.** Với schema raw dev, unknown0; cạnh service20–55, cạnh metric492–1163, metric cô lập159–183. Auth không có cạnh gọi ở cả30ca. Call/meta graph có24ca cyclic dù metric graph trả DAG cả30. Native YAML/StructuralGraphFactory khớp mọi cạnh và native candidate coverage ở30ca; giữ mapped isolates là phần adapter bổ sung, không phải coverage native. Đối chiếu công thức DAG độc lập chỉ áp dụng6ca có call/meta DAG. Nguồn: `graphs/aggregate.json`, `graphs/summary.csv`, `runs/native-yaml-equivalence.json`, `runs/independent-graph-comparison.json`.

Graph canonical được dựng với hashseed0 lưu trước khi khởi Python. Seed0 rebuild không đổi30graph; seed1 đổi cạnh ở24ca cyclic (`runs/builder-hashseed-0.json`, `builder-hashseed-1.json`). Graph lượt đầu chưa lưu hashseed được giữ riêng, không gọi nó là seed0. Cạnh thay có thể do thứ tự SCC và forwarding; native equivalence không chứng minh giả định causal DAG đúng. Không tự sửa cạnh để khớp lý thuyết.

**Phạm vi reference.** Call graph chỉ dùng trace trước mốc. Riêng graph chấm ví dụ được dựng lại trên các cột sau preprocessing/dropconstant của toàn600điểm quanh mốc, gồm sau fault; việc giữ/bỏ metric vì vậy chưa độc lập incident. Dựng lại mapping sau prune có thể đổi forwarding, không chỉ lấy rawgraph bỏ node. So hai nguồn graph còn khác coverage, mật độ và khả năng học fault regime; không được gọi là phép đối chứng đã cô lập hiệu quả đồ thị. Mapping/retention và scorer chung **(chờ WHY, xem de-xuat-tai-lieu-chung.md)**.

**Đối chứng trước mốc không đạt.** Control chặt dùng trace trước pseudo-mốc, train/test trước tiêm thật;60/270metric≥3. Preprocessing dùng720điểm trước tiêm thật, gồm sau pseudo-mốc; không coi đây là pipeline online chỉ nhìn quá khứ tại pseudo-mốc. Phép kiểm độc lập2160thành phần số học,1080mảng raw và37472span/20call edges PASS (`paper/normal-pretrace-verification.json`). Top security_mem không có cha: train mean219.968521MB, scale.001778914MB, test221.433856MB nên score823.7242. Đó là deviation thật của chuỗi nhưng chưa có căn cứ gọi là fault/root. Drift/warmup, tải biến thiên, reference ngắn/phương sai nhỏ hoặc khoảng pre-injection không hoàn toàn healthy đều là giải thích khả thi (`runs/normal-sanity-explained.json`, `runs/normal-normal-architecture-pretrace/snapshot.json`). Không đổi cửa sổ để ép PASS; một control P1 không ước lượng false-positive toàn dataset/P4.

Scoring+ghi snapshot ví dụ272metric mất4.063s (`runs/example-architecture/interpretation.json`), không phải latency scorer thuần hay benchmark chính thức. Timing builder/scorer/những lượt hỏng giữ trong logs; tổng ở `runs/chi-phi-tong.json`.

'''
        text=text.replace('## 8. Đường nhãn',extra+'## 8. Đường nhãn')
        text=text.replace('Khác CIRCA-PC, nguồn graph không học từ tương quan metric của incident.',
                          'Nguồn quan hệ gọi và luật cạnh không học từ tương quan metric của incident; candidate preprocessing trong phép tái lập vẫn có thể dùng dữ liệu sau mốc.')
        text=text.replace('`runs/normal-normal-architecture/interpretation.json`','`runs/normal-normal-architecture-pretrace/interpretation.json`')
    (root/f'ho-so-circa-{kind}.md').write_text(text,encoding='utf-8')

# Preserve the paper's actual statement; distinguish it from code output.
p=root/'de-xuat-tai-lieu-chung.md';text=p.read_text(encoding='utf-8-sig')
detail=(root/'paper/dinh-chinh-k1-threshold.md').read_text(encoding='utf-8-sig')
oldnew=detail.split('## Đoạn cũ → đoạn mới\n',1)[1]
start=text.index('File đích: K1 §C.6, dòng Detector/score.')
end=text.index('File đích: K1 §C.6, chèn sau Giới hạn tác giả',start)
text=text[:start]+'File đích: K1 §C.6, dòng Detector/score.\n\n'+oldnew+'\n\n'+text[end:]
p.write_text(text,encoding='utf-8')

p=root/'moi-truong.md';text=p.read_text(encoding='utf-8-sig')
text=text.replace('Cách đã dựng, khi môi trường py312-pin của T-006 đã có:',
                  'Cách dựng lại tương đương, khi môi trường py312-pin của T-006 đã có (lượt thực tế dùng trình quản lý gói bundled; uv không nằm trên PATH):')
text=text.replace('uv pip install --python D:/RCA-ext/envs/T-014-main/Scripts/python.exe --cache-dir D:/RCA-ext/work/T-014/cache pyarrow==18.1.0 networkx==2.8.8',
                  '& D:/RCA-ext/envs/T-014-main/Scripts/python.exe -m pip install --cache-dir D:/RCA-ext/work/T-014/cache pyarrow==18.1.0 networkx==2.8.8')
p.write_text(text,encoding='utf-8')
print('Published two nine-section profiles and clarified common-document proposal/environment reconstruction.')
