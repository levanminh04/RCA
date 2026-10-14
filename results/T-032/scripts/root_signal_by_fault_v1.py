"""T-032 bản 010 mục 3 (việc 7): chia theo loại lỗi phần đối chiếu metric của bảng "tín hiệu của root nằm ở đâu" (KQ10 mục 3).

Chỉ đếm lại từ runs/root-signal-location-001/summary.json (đã chép về laptop, hash ghi ở LOG phiên 10). Không gọi phương pháp.
Dùng: py -3 -B -X utf8 scripts/root_signal_by_fault_v1.py <thư mục lượt mới>
"""
import hashlib
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "runs/root-signal-location-001/summary.json"
TRACE_POSITIONS = ("own_d", "own_u", "in_d", "in_u", "in_d_edge")


def main():
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=False)
    data = json.loads(SRC.read_text(encoding="utf-8"))
    table = {}
    for c in data["cases"]:
        key = c["dataset"] + "|" + c["fault"]
        t = table.setdefault(key, {"dataset": c["dataset"], "fault": c["fault"], "cases": 0, "cases_with_span_table": 0, "baro_rank1": 0, "simplerca_rank1": 0,
                                   "tracerca_rank1": 0, "tracerca_ok": 0, "root_first_at_any_trace_position": 0, "root_first_by_own_d": 0,
                                   "root_first_only_at_caller_side": 0, "root_metric_votes": [], "root_trace_vote": 0, "root_log_vote": 0,
                                   "root_no_metric_vote": 0, "baro_wrong_and_no_trace_position": 0, "ids_baro_wrong": [], "ids_no_signal_any_channel": []})
        t["cases"] += 1
        if c.get("status") != "OK":
            continue
        t["cases_with_span_table"] += 1
        baro1 = c["baro"]["root_rank_max"] == 1
        simple1 = c["simplerca"]["rank_max"] == 1
        t["baro_rank1"] += baro1
        t["simplerca_rank1"] += simple1
        if c["tracerca_t028"]["status"] == "OK":
            t["tracerca_ok"] += 1
            t["tracerca_rank1"] += c["tracerca_t028"]["rank_max"] == 1
        first = {p for p in TRACE_POSITIONS if c["root_positions"].get(p, {}).get("rank_max") == 1}
        t["root_first_at_any_trace_position"] += bool(first)
        t["root_first_by_own_d"] += "own_d" in first
        t["root_first_only_at_caller_side"] += bool(first) and not (first & {"own_d", "own_u"})
        t["root_metric_votes"].append(c["simplerca"]["metric"])
        t["root_trace_vote"] += c["simplerca"]["trace"] > 0
        t["root_log_vote"] += c["simplerca"]["log"] > 0
        t["root_no_metric_vote"] += c["simplerca"]["metric"] == 0
        if not baro1:
            t["ids_baro_wrong"].append(c["opaque_id"])
            t["baro_wrong_and_no_trace_position"] += not first
        if not first and not baro1 and not simple1:
            t["ids_no_signal_any_channel"].append(c["opaque_id"])
    for t in table.values():
        v = t.pop("root_metric_votes")
        t["root_metric_votes_median"] = statistics.median(v) if v else None
        t["root_metric_votes_min"] = min(v) if v else None
        t["no_signal_any_channel"] = len(t["ids_no_signal_any_channel"])
    totals = {}
    for t in table.values():
        s = totals.setdefault(t["dataset"], {"cases": 0, "cases_with_span_table": 0, "baro_rank1": 0, "simplerca_rank1": 0, "tracerca_rank1": 0,
                                             "root_first_at_any_trace_position": 0, "no_signal_any_channel": 0})
        for k in s:
            s[k] += t[k]
    result = {"schema": "T032-root-signal-by-fault-v1", "design": "results/T-032/thiet-ke-kenh-metric-010.md mục 3",
              "source": {"path": "runs/root-signal-location-001/summary.json", "sha256": hashlib.sha256(SRC.read_bytes()).hexdigest()},
              "note": "Ô dưới 3 ca chỉ để liệt kê. 'no_signal_any_channel': root không đứng đầu ở vị trí trace nào, BARO và SimpleRCA đều không xếp root hạng 1.",
              "by_dataset_fault": dict(sorted(table.items())), "totals": totals, "methods_executed": []}
    (out / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(totals, ensure_ascii=False))
    for k, t in sorted(table.items()):
        print(k, "n", t["cases"], "span", t["cases_with_span_table"], "| baro1", t["baro_rank1"], "simple1", t["simplerca_rank1"], "trace1", t["tracerca_rank1"], "/", t["tracerca_ok"],
              "| any_pos", t["root_first_at_any_trace_position"], "own_d", t["root_first_by_own_d"], "caller_only", t["root_first_only_at_caller_side"],
              "| votes med", t["root_metric_votes_median"], "min", t["root_metric_votes_min"], "no_metric", t["root_no_metric_vote"], "| none", t["no_signal_any_channel"])


if __name__ == "__main__":
    main()
