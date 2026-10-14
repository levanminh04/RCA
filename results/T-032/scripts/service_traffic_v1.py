"""T-032 bản 010 mục 2: số span và số trace của từng dịch vụ trước và sau mốc, 52 ca. Chạy trên EC2, chỉ đọc, KHÔNG dùng nhãn.

Span "sau mốc" khi kết thúc từ mốc trở đi (như hai phương pháp trace). Dùng: python service_traffic_v1.py <thư mục lượt mới>
"""
import json
import sys
from pathlib import Path

import pandas as pd

BASE = Path("/home/ubuntu/rca/T-032")
sys.path.insert(0, str(BASE / "scripts"))
import tracerca_core_and_td_v1 as td  # noqa: E402


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    from replay_tracerca_v3 import table_columns
    from p3 import cua_so, selector
    allow = selector.nap_allowlist(BASE / "repo/results/T-022/allowlist-dev.json")
    index = td.read(BASE / "repo/results/T-024/ban-ghi-dua-vao-cham.json")["records"]
    cases = []
    for row in td.read(td.PLAN)["rows"]:
        dataset, opaque_id = row["dataset"], row["opaque_id"]
        if row["source_status"] == "OK":
            directory = td.REUSED.get(row.get("replay_phase_already_valid"), td.COHORT / "cases" / dataset / opaque_id)
            adapter = td.read(directory / "capture/calls/001-adapter.json")
            spans = pd.DataFrame(table_columns(directory / "capture", adapter["entry"]["input"]))
            t = int(adapter["entry"]["t_seconds"])
        else:
            entry = [e for e in index if e["method"] == "tracerca" and e["opaque_id"] == opaque_id][0]
            t = int(td.read(BASE / "repo" / entry["path"])["window"]["t"])
            files = selector.chon_ca(allow, opaque_id, Path("/home/ubuntu/rca/T-031/repo"), kiem_hash=True, tep=["traces.parquet"])
            spans = cua_so.cat_span(pd.read_parquet(files["traces.parquet"]), t)
        start = spans["startTime"].to_numpy(dtype="int64")
        end = start + spans["duration"].to_numpy(dtype="int64")
        frame = pd.DataFrame({"s": spans["serviceName"].astype(str).to_numpy(), "t": spans["traceID"].astype(str).to_numpy(), "after": end >= t * 1_000_000})
        services = {}
        for (s, after), g in frame.groupby(["s", "after"], sort=True):
            item = services.setdefault(s, {"spans_before": 0, "spans_after": 0, "traces_before": 0, "traces_after": 0})
            key = "after" if after else "before"
            item["spans_" + key] = int(len(g))
            item["traces_" + key] = int(g["t"].nunique())
        cases.append({"dataset": dataset, "opaque_id": opaque_id, "t_seconds": t, "spans": int(len(frame)),
                      "earliest_start_minus_t_s": float((start.min() - t * 1_000_000) / 1e6), "latest_end_minus_t_s": float((end.max() - t * 1_000_000) / 1e6),
                      "services": services})
        print(dataset, opaque_id, len(services), flush=True)
    (out / "summary.json").write_text(json.dumps({"schema": "T032-service-traffic-v1", "cases": cases, "methods_executed": []}, ensure_ascii=False, indent=1) + "\n",
                                      encoding="utf-8")
    print("XONG", len(cases), flush=True)


if __name__ == "__main__":
    main()
