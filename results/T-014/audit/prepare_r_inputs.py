"""Prepare only the two predeclared fse cases for pcalg diagnostic."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from RCAEval.io.time_series import preprocess

root=Path("D:/RCA-ext/work/T-014/audit-r")
root.mkdir(parents=True,exist_ok=True)
records=[]
for relative in ("cartservice_cpu/1","cartservice_mem/1"):
    source=Path("D:/RCA-ext/data/fse-ob")/relative/"simple_data.csv"
    frame=pd.read_csv(source).drop(columns=["time.1"],errors="ignore")
    frame=frame.loc[:,~frame.columns.str.endswith("_latency-50")].replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    mark=int((source.parent/"inject_time.txt").read_text().strip())
    frame=pd.concat([frame[frame.time<mark].tail(300),frame[frame.time>=mark].head(300)],ignore_index=True)
    frame=frame.rename(columns={c:c.replace("_latency-90","_latency") for c in frame if c.endswith("_latency-90")})
    times=frame.time
    values=preprocess(frame,dataset="fse-ob",dk_select_useful=False)
    stem=relative.replace("/","_")
    target=root/(stem+"_input.csv");values.to_csv(target,index=False)
    records.append({"case":"fse-ob/"+relative,"source":str(source),"input":str(target),"rows":len(values),"columns":list(values.columns),"mark":mark,"times":list(map(int,times))})
(root/"inputs.json").write_text(json.dumps(records,indent=2),encoding="utf-8")
print(json.dumps([{k:v for k,v in r.items() if k not in ("times","columns")} for r in records],indent=2))
