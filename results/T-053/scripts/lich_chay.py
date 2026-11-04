"""Lập lịch T1/K theo số đo pilot. Không khởi động lượt."""
import argparse
import json
from collections import defaultdict
from pathlib import Path

from doi_chieu import RUNS, jsonl, read


def measurements(run, indices):
    rows = []
    for i in indices:
        folder = RUNS / f"{run}-{i:02d}"
        progress = list(jsonl(folder / "progress.jsonl"))
        complete = read(folder / "kiem.json")
        records = [r for r in progress if r["event"] == "record"]
        assert len(records) == 4 and all(not r["exceptions"] for r in records)
        load = next(r for r in progress if r["event"] == "loaded")
        rows.append(dict(job=i, seconds=complete["wall_seconds"], setup=load["seconds"],
                         r0=records[0]["elapsed"], total=sum(r["elapsed"] for r in records),
                         result_bytes=sum(x["bytes"] for x in complete["files"].values()),
                         peak_rss=max(r["peak_rss"] for r in records),
                         samples=load["n"]))
    host = [r for r in jsonl(RUNS / run / "progress.jsonl") if r["event"] == "host"]
    return rows, dict(min_available=min(r["available"] for r in host),
                      min_disk=min(r["disk_free"] for r in host),
                      cpu_max=max(r["cpu_percent"] for r in host))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("laptop")
    p.add_argument("ec2")
    p.add_argument("out", type=Path)
    p.add_argument("--laptop-workers", type=int, required=True)
    args = p.parse_args()
    plan = read(RUNS.parent / "ke-hoach-pha1.json")
    indices, jobs = plan["pilot_indices"], plan["jobs"]
    data = {}
    for name, run, count in (("laptop",args.laptop,args.laptop_workers),("ec2",args.ec2,2)):
        measured, host = measurements(run, indices)
        data[name] = dict(measured=measured, host=host, workers=count,
                          t1=0, k=0, bytes=0, jobs=[])
    group = lambda i: (jobs[i]["dataset"], jobs[i]["window"])

    def cost(name,i):
        rows = data[name]["measured"]
        item = min((r for r in rows if group(r["job"]) == group(i)),
                   key=lambda r: abs(jobs[r["job"]]["source_bytes"] - jobs[i]["source_bytes"]))
        ratio = max(1, jobs[i]["source_bytes"] / jobs[item["job"]]["source_bytes"])
        repeat = 4 if jobs[i]["window"] == "that" else 1
        return dict(t1=ratio*(item["setup"]+item["r0"])*repeat,
                    k=ratio*(item["setup"]+item["total"]*4),
                    bytes=round(ratio*item["result_bytes"]*(4+repeat/4)))

    # Chi phí dự báo từ nhóm gần nhất theo byte. Ca nặng đi trước; ưu tiên
    # EC2 trong nhóm đầu, rồi cân tổng thời gian ước tính qua số tiến trình đã đo.
    estimated = {i: {name: cost(name,i) for name in data} for i in range(len(jobs))}
    ordered = sorted(range(len(jobs)), key=lambda i: -estimated[i]["ec2"]["k"])
    for j,i in enumerate(ordered):
        chosen = min(data, key=lambda name: (
            data[name]["t1"]+data[name]["k"]+estimated[i][name]["t1"]+estimated[i][name]["k"]
        )/data[name]["workers"]) if j >= 12 else "ec2"
        entry = data[chosen]
        entry["jobs"].append(i)
        for k,v in estimated[i][chosen].items():
            entry[k] += v
    phase_wall = {k:max(d[k]/d["workers"] for d in data.values()) for k in ("t1","k")}
    # Dự toán có dự phòng cho biến động ca, chuyển đầu ra và kiểm.
    forecast = (phase_wall["t1"] + phase_wall["k"]) * 1.35 + 30*60
    with args.out.open("x", encoding="utf-8") as f:
        json.dump(dict(machine=data, phase_wall=phase_wall, forecast_seconds=forecast,
                       estimated_local_closed_bytes=sum(d["bytes"] for d in data.values())),
                  f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
