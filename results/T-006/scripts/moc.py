r"""T-006: các mốc đã công bố dùng để so. Mỗi mốc ghi nguồn. Số chép từ bảng HTML, không gõ từ trí nhớ.

Nguồn:
- TORAI_B2, TORAI_B3: bài TORAI, arXiv 2604.13522v1, bản HTML https://arxiv.org/html/2604.13522v1 (tải 03/10/2026),
  Bảng 2 (Online Boutique, torai-OB) và Bảng 3 (Sock Shop, torai-SS). Mỗi ô: (T1, T3, A5) = (AC@1, AC@3, Avg@5).
- BARO_B3: bài BARO, arXiv 2405.09330, bản HTML https://arxiv.org/html/2405.09330 (tải 03/10/2026), Bảng 3 (Avg@5 mức
  service), các dòng [t_inject] và dòng BARO. Cột CPU, MEM, DELAY, LOSS, AVG.
- BARO_B2: cùng bài, Bảng 2 (Precision, Recall, F1 phát hiện bất thường).
- README_BARO: README repo BARO e35f4ec (ví dụ cơ bản; RQ1; RQ2).
- TORAI_MD: docs/TORAI.md của RCAEval 259ea41 (đầu ra mong đợi của TORAI trên torai-ob, chỉ Avg@5).
- SETUP_MD: docs/SETUP.md của RCAEval 259ea41 (đầu ra mong đợi của RCD trên online-boutique, 1 lần chạy).
"""

LOI6 = ["cpu", "mem", "disk", "socket", "delay", "loss"]

# Bảng 2 bài TORAI (torai-OB). Khóa: (nguồn dữ liệu, phương pháp).
TORAI_B2 = {
    ("Metric", "CIRCA"): {"cpu": (0.73, 0.93, 0.88), "mem": (0.67, 0.93, 0.89), "disk": (0.80, 0.87, 0.85),
                          "socket": (0.67, 0.87, 0.83), "delay": (0.47, 0.80, 0.75), "loss": (0.67, 0.93, 0.88),
                          "AVERAGE": (0.67, 0.89, 0.85)},
    ("Metric", "RCD"): {"cpu": (0.87, 1.00, 0.94), "mem": (0.67, 0.87, 0.81), "disk": (0.73, 0.87, 0.81),
                        "socket": (0.80, 0.93, 0.91), "delay": (0.27, 0.60, 0.52), "loss": (0.20, 0.53, 0.44),
                        "AVERAGE": (0.59, 0.80, 0.74)},
    # Dòng BARO của Bảng 2 trùng từng số với Bảng 4 (Train Ticket); nghi chép nhầm, không dùng (SPEC).
    ("Metric+Log", "TORAI"): {"cpu": (0.67, 0.80, 0.81), "mem": (0.87, 1.00, 0.97), "disk": (0.93, 1.00, 0.95),
                              "socket": (0.80, 0.87, 0.84), "delay": (0.73, 1.00, 0.92), "loss": (0.77, 1.00, 0.93),
                              "AVERAGE": (0.80, 0.95, 0.91)},
    ("Metric+Log+Trace", "TORAI"): {"cpu": (0.92, 1.00, 0.98), "mem": (0.67, 1.00, 0.93), "disk": (1.00, 1.00, 1.00),
                                    "socket": (0.87, 0.93, 0.95), "delay": (0.67, 0.73, 0.76), "loss": (0.87, 1.00, 0.96),
                                    "AVERAGE": (0.83, 0.95, 0.93)},
}

# Bảng 3 bài TORAI (torai-SS, không có trace).
TORAI_B3 = {
    ("Metric", "BARO"): {"cpu": (0.00, 1.00, 0.80), "mem": (0.20, 1.00, 0.83), "disk": (0.00, 0.93, 0.77),
                         "socket": (0.00, 0.93, 0.71), "delay": (0.00, 0.87, 0.68), "loss": (0.20, 1.00, 0.80),
                         "AVERAGE": (0.07, 0.96, 0.76)},
    ("Metric", "CIRCA"): {"cpu": (0.87, 1.00, 0.97), "mem": (0.87, 0.93, 0.95), "disk": (0.87, 0.87, 0.89),
                          "socket": (0.67, 1.00, 0.92), "delay": (0.67, 0.87, 0.85), "loss": (0.47, 0.87, 0.81),
                          "AVERAGE": (0.74, 0.92, 0.90)},
    ("Metric", "RCD"): {"cpu": (0.47, 0.73, 0.68), "mem": (0.27, 0.40, 0.36), "disk": (0.47, 0.67, 0.61),
                        "socket": (0.47, 0.87, 0.77), "delay": (0.40, 0.73, 0.64), "loss": (0.20, 0.40, 0.35),
                        "AVERAGE": (0.38, 0.63, 0.57)},
    ("Metric+Log", "TORAI"): {"cpu": (0.93, 1.00, 0.98), "mem": (1.00, 1.00, 1.00), "disk": (0.93, 0.93, 0.95),
                              "socket": (0.84, 0.93, 0.94), "delay": (0.75, 0.88, 0.86), "loss": (0.60, 1.00, 0.92),
                              "AVERAGE": (0.84, 0.96, 0.94)},
}

# Bảng 3 bài BARO (Avg@5 mức service; dữ liệu fse-*; 4 loại lỗi).
BARO_B3 = {
    "fse-ob": {
        "CIRCA[t_inject]": {"cpu": 0.9, "mem": 0.74, "delay": 0.9, "loss": 0.55, "AVG": 0.77},
        "N-Sigma[t_inject]": {"cpu": 0.9, "mem": 0.93, "delay": 0.94, "loss": 0.66, "AVG": 0.86},
        "RobustScorer[t_inject]": {"cpu": 0.9, "mem": 0.94, "delay": 0.94, "loss": 0.65, "AVG": 0.86},
        "BARO": {"cpu": 0.91, "mem": 0.96, "delay": 0.95, "loss": 0.62, "AVG": 0.86},
    },
    "fse-ss": {
        "CIRCA[t_inject]": {"cpu": 0.97, "mem": 0.98, "delay": 0.98, "loss": 0.88, "AVG": 0.95},
        "N-Sigma[t_inject]": {"cpu": 0.98, "mem": 0.98, "delay": 0.98, "loss": 0.9, "AVG": 0.96},
        "RobustScorer[t_inject]": {"cpu": 0.98, "mem": 0.98, "delay": 0.98, "loss": 0.86, "AVG": 0.95},
        "BARO": {"cpu": 0.97, "mem": 0.98, "delay": 0.98, "loss": 0.87, "AVG": 0.95},
    },
}

# Bảng 2 bài BARO: (Precision, Recall, F1).
BARO_B2 = {
    "fse-ob": {"N-Sigma": (0.54, 1, 0.7), "BARO": (0.69, 1, 0.82)},
    "fse-ss": {"N-Sigma": (0.56, 1, 0.72), "BARO": (0.6, 1, 0.75)},
}

README_BARO = {
    "vi_du_co_ban": {"buoc_phat_hien": 243,
                     "top5": ["checkoutservice_latency", "cartservice_mem", "cartservice_latency", "cartservice_cpu", "main_mem"]},
    "rq2_fse_ob_avg5": {"cpu": 0.91, "mem": 0.96, "delay": 0.95, "loss": 0.62, "all": 0.86},
    "rq1_fse_ob_bocpd": (0.76, 1.00, 0.87),
}

TORAI_MD = {"cpu": 0.96, "mem": 0.93, "disk": 1.0, "socket": 0.93, "delay": 0.8, "loss": 0.84}

SETUP_MD = {"cpu": 0.94, "mem": 0.67, "disk": 0.68, "delay": 0.25, "loss": 0.51}
