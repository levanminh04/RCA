r"""T-006 X1: ví dụ cơ bản trong README của BARO (e35f4ec), mốc loại A.

Mã dưới đây chép từ README ("Basic usage example"), chỉ thay `download_data()` bằng chép file đã tải sẵn từ đúng URL
mặc định của `download_data()` (github.com/phamquiluan/baro/releases/download/0.0.4/simple_data.csv) thành data.csv
trong thư mục hiện tại, và kiểm SHA-256 trước khi đọc.
`baro` lấy từ D:\RCA-ext\src\baro qua sys.path (không cài gói fse-baro), như T-005.
Đầu ra mong đợi theo README: "Anomalies are detected at timestep: 243";
"Top 5 root causes: ['checkoutservice_latency', 'cartservice_mem', 'cartservice_latency', 'cartservice_cpu', 'main_mem']".
Cách dùng: <python của môi trường> vi_du_baro.py   (chạy trong thư mục làm việc riêng)
"""
import hashlib
import json
import shutil
import sys
import time

sys.path.insert(0, r"D:\RCA-ext\src\baro")

SRC = r"D:\RCA-ext\dl\baro-simple_data.csv"
SHA = "3eb6169a63f86c5878c277434936e1f4bbbd7f30dcf7f87dc3496bea8cae7f1a"  # runs/00-tai-du-lieu.log
assert hashlib.sha256(open(SRC, "rb").read()).hexdigest() == SHA, "sai SHA-256 của simple_data.csv"
shutil.copyfile(SRC, "data.csv")

t0 = time.time()
# ---- từ README ----
from baro.anomaly_detection import bocpd
from baro.root_cause_analysis import robust_scorer
from baro.utility import download_data, read_data

# read data from data.csv
data = read_data("data.csv")
# perform anomaly detection
anomalies = bocpd(data)
print("Anomalies are detected at timestep:", anomalies[0])
# perform root cause analysis
root_causes = robust_scorer(data, anomalies=anomalies)["ranks"]
# print the top 5 root causes
print("Top 5 root causes:", root_causes[:5])
# ---- hết phần README ----

MONG_DOI = {"buoc": 243, "top5": ["checkoutservice_latency", "cartservice_mem", "cartservice_latency", "cartservice_cpu", "main_mem"]}
kq = {"buoc": int(anomalies[0]), "top5": list(root_causes[:5]), "so_diem_bat_thuong": len(anomalies),
      "anomalies_10_dau": [int(x) for x in anomalies[:10]], "giay": round(time.time() - t0, 1)}
kq["khop_buoc"] = kq["buoc"] == MONG_DOI["buoc"]
kq["khop_top5"] = kq["top5"] == MONG_DOI["top5"]
print("KET-QUA", json.dumps(kq, ensure_ascii=False))
json.dump(kq, open("ket-qua-vi-du.json", "w"), ensure_ascii=False, indent=1)
