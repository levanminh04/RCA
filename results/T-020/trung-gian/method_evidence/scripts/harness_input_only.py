import os
import numpy as np
import pandas as pd
def dung_dau_vao(data_path, method, length, placebo=False, khong_trace=False, hoan_vi=None):
    data_dir = os.path.dirname(data_path)
    data = pd.read_csv(data_path)
    if "time.1" in data:
        data = data.drop(columns=["time.1"])
    data = data.loc[:, ~data.columns.str.endswith("_latency-50")]
    if "mm-tt" in data_path or "torai-TT" in data_path:
        time_col = data["time"]
        data = data.loc[:, data.columns.str.startswith("ts-")]
        data["time"] = time_col
    data = data.replace([np.inf, -np.inf], np.nan)
    data = data.ffill()
    data = data.fillna(0)
    with open(os.path.join(data_dir, "inject_time.txt")) as f:
        inject_time = int(f.readlines()[0].strip())
    if placebo:
        inject_time = inject_time - (length * 60 // 2 + 15)
    normal_df = data[data["time"] < inject_time].tail(length * 60 // 2)
    anomal_df = data[data["time"] >= inject_time].head(length * 60 // 2)
    data = pd.concat([normal_df, anomal_df], ignore_index=True)
    data = data.rename(columns={c: c.replace("_latency-90", "_latency") for c in data.columns if c.endswith("_latency-90")})
    rng = np.random.RandomState(hoan_vi) if hoan_vi is not None else None

    def hv(df):
        if rng is None or df is None or len(df.columns) == 0:
            return df
        cols = [c for c in df.columns if c != "time"]
        cols = list(rng.permutation(cols))
        return df[(["time"] if "time" in df.columns else []) + cols]

    if method == "rcd":
        return hv(data), inject_time
    logts = pd.read_csv(os.path.join(data_dir, "logts.csv"))
    traces_err = pd.DataFrame()
    traces_lat = pd.DataFrame()
    if not khong_trace:
        try:
            traces_err = pd.read_csv(os.path.join(data_dir, "tracets_err.csv"))
            traces_lat = pd.read_csv(os.path.join(data_dir, "tracets_lat.csv"))
        except FileNotFoundError:
            pass
    n = length * 4 // 2 if length else 20
    a = logts[logts["time"] < inject_time].tail(n)
    b = logts[logts["time"] >= inject_time].head(n)
    logts = pd.concat([a, b], ignore_index=True)
    if traces_err.shape[0] > 0:
        a = traces_err[traces_err["time"] < inject_time].tail(n)
        b = traces_err[traces_err["time"] >= inject_time].head(n)
        traces_err = pd.concat([a, b], ignore_index=True)
    if traces_lat.shape[0] > 0:
        a = traces_lat[traces_lat["time"] < inject_time].tail(n)
        b = traces_lat[traces_lat["time"] >= inject_time].head(n)
        traces_lat = pd.concat([a, b], ignore_index=True)
    d = {"metric": hv(data.copy(deep=True)), "logts": hv(logts), "tracets_err": hv(traces_err),
         "tracets_lat": hv(traces_lat)}
    return d, inject_time
