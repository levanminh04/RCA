"""T-016 S12: kiểm kmeans_1d (tinh_tay.py) với sklearn KMeans 1.2.2 trên cột thử ngẫu nhiên (chỉ để kiểm, không dùng
trong kết quả). In số cột lệch tâm (rtol 1e-12) và số cột lệch mã bin sau rời rạc hóa."""
import sys
import numpy as np
sys.path.insert(0, ".")
import tinh_tay as T  # noqa: E402
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.preprocessing import KBinsDiscretizer  # noqa: E402

rng = np.random.RandomState(1)
lech_tam = lech_bin = tong = 0
for t in range(3000):
    n = rng.randint(6, 90)
    kind = t % 4
    if kind == 0:
        x = rng.randn(n) * rng.rand() * 10
    elif kind == 1:
        x = rng.poisson(rng.rand() * 4, n).astype(float)
    elif kind == 2:
        x = np.r_[np.zeros(rng.randint(1, 4)), rng.randint(100, 200, n)].astype(float)
    else:
        x = rng.choice([0., 1., 2., 7., 7.5], n)
    if x.min() == x.max():
        continue
    u = np.linspace(x.min(), x.max(), 6)
    init = (u[1:] + u[:-1]) * 0.5
    a = np.sort(KMeans(n_clusters=5, init=init[:, None], n_init=1).fit(x[:, None]).cluster_centers_[:, 0])
    b = np.sort(T.kmeans_1d(x, init))
    tong += 1
    lech_tam += not np.allclose(a, b, rtol=1e-12, atol=1e-9)
    kb = KBinsDiscretizer(n_bins=5, encode="ordinal", strategy="kmeans").fit(x[:, None]).transform(x[:, None])[:, 0]
    mine, _ = T.roi_rac_hoa(__import__("pandas").DataFrame({"c": x}))
    lech_bin += not np.array_equal(kb.astype(int), mine["c"].to_numpy())
print(f"kmeans_1d so với sklearn KMeans: {tong} cột thử; lệch tâm {lech_tam}; lệch mã bin so với KBinsDiscretizer {lech_bin}")
