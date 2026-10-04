"""T-016 S9: thử dịch biên bin 15 s từ -7 đến +7 giây cho hai mẫu log đơn giản nhất của currencyservice
(re2ob_productcatalogservice_loss_1), so tỉ lệ bin trùng với logts.csv bản Figshare (currencyservice_1, _4).
Chạy bằng envs/T-016-cong-cu."""
import pandas as pd

l = pd.read_parquet("data/rcaeval/re2ob_productcatalogservice_loss_1/logs.parquet")
lt = pd.read_csv("D:/RCA-ext/data/torai-OB/productcatalogservice_loss/1/logts.csv").set_index("time")
t0 = 1705342110
for off in range(-7, 8):
    b = t0 + ((l.timestamp - t0 + off) // 15) * 15
    c = l[l.container_name == "currencyservice"].assign(bin=b).groupby(["bin", "message"]).size().unstack().fillna(0)
    c = c.reindex(lt.index).fillna(0)
    a1 = (c["Getting supported currencies..."].values == lt["currencyservice_1"].values).mean()
    a4 = (c["conversion request successful"].values == lt["currencyservice_4"].values).mean()
    print(f"dich {off:+d} s: bin trung currencyservice_1 {a1:.3f}, currencyservice_4 {a4:.3f}")
print("tong dong:", int((l.container_name == "currencyservice").sum()), "so voi tong logts:",
      int(lt[["currencyservice_1", "currencyservice_4"]].to_numpy().sum()))
