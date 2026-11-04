"""Dự báo thời gian từ số đo K đã đóng, T1 cùng cửa sổ và pilot."""
import argparse
import bisect
import hashlib
import json
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "results/T-053"
RUNS = OUT / "runs"


def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def rows(path):
    with path.open(encoding="utf-8") as stream:
        return [json.loads(line) for line in stream if line.endswith("\n")]


def interpolate(value, points):
    points = sorted(points)
    index = bisect.bisect_left([x for x, _ in points], value)
    if index == 0:
        return points[0][1]
    if index == len(points):
        return points[-1][1]
    (left, a), (right, b) = points[index-1:index+1]
    return a + (b-a) * (value-left) / (right-left)


def machine_forecast(machine, snapshot, plan, schedule):
    jobs = plan["jobs"]
    pilot_name = f"pilot-{'laptop-2-001' if machine == 'laptop' else 'ec2-2-002'}"
    pilot = {}
    for index in plan["pilot_indices"]:
        data = [r for r in rows(RUNS / f"{pilot_name}-{index:02d}/progress.jsonl")
                if r["event"] == "record"]
        group = jobs[index]["dataset"], jobs[index]["window"]
        ratio = sum(r["cpu_seconds"] for r in data) / data[0]["cpu_seconds"]
        pilot.setdefault(group, []).append((data[0]["cpu_seconds"], ratio))

    def baseline(index):
        job = jobs[index]
        stage = "seed1" if job["window"] == "that" else "ce"
        path = RUNS / f"t1-{stage}-{machine}-001-{index:02d}/progress.jsonl"
        if not path.is_file():
            path = RUNS / f"{pilot_name}-{index:02d}/progress.jsonl"
        data = rows(path)
        point = next(r for r in data if r["event"] == "record" and r["config_id"] == "K-R0")
        setup = next(r for r in data if r["event"] == "loaded")["seconds"]
        return point["cpu_seconds"], setup

    def pilot_equivalent(index):
        job = jobs[index]
        cpu, _ = baseline(index)
        return cpu * interpolate(cpu, pilot[job["dataset"], job["window"]])

    complete = [w for w in snapshot["windows"] if w["meta"]]
    if not complete:
        raise ValueError("Chưa có cửa sổ K đầy đủ để hiệu chỉnh")
    gains = [sum(r["cpu_seconds"] for r in w["records"])
             / pilot_equivalent(int(w["name"].rsplit("-", 1)[1])) for w in complete]
    gain = statistics.median(gains)
    active = {}
    for row in snapshot["host"]:
        if row["event"] == "worker":
            active[row["job"]] = row
        elif row["event"] == "exit":
            active.pop(row["job"], None)
    current = {int(w["name"].rsplit("-", 1)[1]): w for w in snapshot["windows"]}
    remaining, used, setups, estimates = 0, 0, 0, []
    for index in schedule["jobs"]:
        window = current.get(index)
        _, setup = baseline(index)
        if window and window["meta"]:
            used += sum(r["cpu_seconds"] for r in window["records"])
            continue
        factor = gain
        same_kind = [g for g, w in zip(gains, complete)
                     if w["job"]["window"] == jobs[index]["window"]]
        if same_kind and jobs[index]["dataset"] == "RE2-TT":
            factor = statistics.median(same_kind) if len(same_kind) > 1 else (gain+same_kind[0])/2
        if jobs[index]["dataset"] == "Nezha-OB":
            # Chưa có Nezha K hoàn tất trong lát cắt này. Giữ riêng giả định
            # về phần chi phí lặp sau khi cổng đã có cache.
            factor = 2.3
        prediction = pilot_equivalent(index) * factor
        emitted = sum(r["cpu_seconds"] for r in window["records"]) if window else 0
        count = len(window["records"]) if window else 0
        if count >= 2:
            fraction = statistics.median(
                sum(r["cpu_seconds"] for r in w["records"][:count])
                / sum(r["cpu_seconds"] for r in w["records"]) for w in complete)
            prediction = 0.65 * emitted/fraction + 0.35 * prediction
        spent = max(emitted, active.get(index, {}).get("cpu_seconds", 0)-setup-2)
        seconds = max(0, prediction-spent)
        remaining += seconds
        setups += setup if window is None else 0
        used += spent
        estimates.append(dict(job=index, remaining_cpu_seconds=seconds, factor=factor))
    elapsed = snapshot["epoch"] - snapshot["host"][0]["epoch"]
    cores = min(schedule["workers"], used/elapsed)
    work = remaining + setups
    return dict(closed=len(complete), emitted=sum(len(w["records"]) for w in snapshot["windows"]),
                calibrated_factor=gain, factor_range=[min(gains), max(gains)],
                remaining_cpu_hours=remaining/3600, effective_cores=cores,
                remaining_hours=work/cores/3600,
                optimistic_hours=0.9*work/schedule["workers"]/3600,
                conservative_hours=1.2*work/(cores*0.95)/3600,
                per_window=estimates)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("suffix")
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    plan, schedule = read(OUT / "ke-hoach-pha1.json"), read(OUT / "lich-chay.json")
    snapshots = {m: read(RUNS / f"du-lieu-du-bao-{m}-{args.suffix}.json")
                 for m in ("laptop", "ec2")}
    data = {m: machine_forecast(m, snapshot, plan, schedule["machine"][m])
            for m, snapshot in snapshots.items()}
    manifest = read(ROOT / "results/T-047/manifest.json")["outputs"]
    history = {}
    for stage in ("b4-c1-pha2-001", "b6-c1-do-ben-001", "b5-c1-co-che-001"):
        path = ROOT / f"results/T-047/runs/{stage}/progress.jsonl"
        assert sha(path) == manifest[path.relative_to(ROOT).as_posix()]["sha256"]
        log = rows(path)
        field = "elapsed" if stage.startswith("b6") else "seconds"
        history[stage] = log[-1][field] - log[0][field]
    k_hours = max(d["remaining_hours"] for d in data.values())
    # Đây là khoảng vận hành, không phải khoảng tin cậy thống kê.
    later_hours = sum(history.values())/3600 + 0.15
    at = max(d["epoch"] for d in snapshots.values())
    zone = timezone(timedelta(hours=7))
    stamp = datetime.fromtimestamp(at, zone)
    doc = dict(as_of=stamp.isoformat(),machines=data,historical_code_seconds=history,
               K_remaining_hours=k_hours,seal_and_post_code_hours=later_hours,
               all_code_remaining_hours=k_hours+later_hours,
               K_end=(stamp+timedelta(hours=k_hours)).isoformat(),
               all_code_end=(stamp+timedelta(hours=k_hours+later_hours)).isoformat(),
               operational_range_end=[
                   (stamp+timedelta(hours=max(d["optimistic_hours"] for d in data.values())+0.3)).isoformat(),
                   (stamp+timedelta(hours=max(d["conservative_hours"] for d in data.values())+0.75)).isoformat()],
               assumptions=["Phần chấm bắt đầu ngay sau seal pha 1 K",
                            "Không lỗi mới hoặc thay đổi tải lớn",
                            "Nezha chưa có đủ K, dùng pilot và hệ số 2,3",
                            "Không tính đọc, diễn giải hoặc viết báo cáo"],
               source_sha256={p.relative_to(ROOT).as_posix():sha(p) for p in [
                   Path(__file__), OUT/"ke-hoach-pha1.json", OUT/"lich-chay.json",
                   *[RUNS/f"du-lieu-du-bao-{m}-{args.suffix}.json" for m in snapshots]]})
    with args.out.open("x", encoding="utf-8") as stream:
        json.dump(doc, stream, ensure_ascii=False, indent=2)
    print(json.dumps({k:v for k,v in doc.items() if k not in ("machines","source_sha256")},ensure_ascii=False))


if __name__ == "__main__":
    main()
