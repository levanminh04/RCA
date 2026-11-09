"""B0 bổ sung T-057: kiểm bản nhận RE3 ngoài repo theo biên nhận T-055. Chỉ đọc.

Chạy từ gốc repo: py -3 -B results/T-057/scripts/b0_re3_nhan.py results/T-057/b0-re3-nhan.json
1. sha256 của ec2_{1,2}.tar.gz, verified-before-labels.json, aggregate-plan.json so với
   results/T-055/runs/cham-001/main-receipt.json (#/transfer, #/snapshot, #/aggregate_plan).
2. Với mọi slot đã giải nén: sha256 verified.json so với snapshot#/slots/<slot>/receipt/sha256;
   sha256 result.json và job.json so với verified.json (#/result/sha256, #/job_sha256).
"""
import glob
import hashlib
import json
import os
import sys

Q = "D:/RCA-ext/T-055/work-re3-score-v1/results/T-054/runs/re3-ban-cuoi-001/received"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(outp):
    rc = json.load(open("results/T-055/runs/cham-001/main-receipt.json", encoding="utf-8"))
    tong = {
        "ec2_1.tar.gz": sha(Q + "/ec2_1.tar.gz") == rc["transfer"]["ec2_1"]["archive_sha256"],
        "ec2_2.tar.gz": sha(Q + "/ec2_2.tar.gz") == rc["transfer"]["ec2_2"]["archive_sha256"],
        "verified-before-labels.json": sha(Q + "/verified-before-labels.json") == rc["snapshot"]["sha256"],
        "aggregate-plan.json": sha(Q + "/aggregate-plan.json") == rc["aggregate_plan"]["sha256"],
    }
    snap = json.load(open(Q + "/verified-before-labels.json", encoding="utf-8"))["slots"]
    n, lech = 0, []
    for v in glob.glob(Q + "/ec2_*/results/T-054/runs/re3-ban-cuoi-001/queue/*/attempt-*/verified.json"):
        d = os.path.dirname(v)
        slot = os.path.basename(os.path.dirname(d))
        vr = json.load(open(v, encoding="utf-8"))
        ok = (slot in snap and sha(v) == snap[slot]["receipt"]["sha256"]
              and sha(os.path.join(d, "result.json")) == vr["result"]["sha256"]
              and sha(os.path.join(d, "job.json")) == vr["job_sha256"])
        n += 1
        if not ok:
            lech.append(slot)
    out = {"lenh": "py -3 -B results/T-057/scripts/b0_re3_nhan.py " + outp, "tong": tong,
           "so_slot_kiem": n, "so_slot_snapshot": len(snap), "slot_lech": lech}
    with open(outp, "x", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False))


if __name__ == "__main__":
    main(sys.argv[1])
