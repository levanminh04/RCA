"""Fixture T-026 có đáp án tính tay; không mở dữ liệu thật hoặc nhãn thật."""
import csv
import hashlib
import json
import math
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from p3 import nezha
from p3.selector import LoiRunner
from p3.adapters import nezha as adapters

WORK = ROOT / "results/T-026/work"
T = 1661124000 * 10**9
OID = "dev-0123456789"
POD = "adservice-5f6585d649-fnmft"

def csvfile(path, fields, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows(rows)
    return {"path": path, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size}

def wall(ns):
    sec, frac = divmod(ns, 10**9)
    return datetime.fromtimestamp(sec, timezone.utc).strftime("%Y-%m-%d %H:%M:%S") + \
        ".%09d +0000 UTC m=+1" % frac

def trace_frame():
    rows = []
    for i, (seconds, duration) in enumerate([(-80,1000),(-40,2000),(-20,3000),(20,2000),(40,10000)]):
        start = T + seconds * 10**9
        rows.append(dict(traceID=str(i),spanID=str(i),parentSpanID="",
                         serviceName="adservice",methodName="op/path",
                         operationName="op/path",startTime=start//1000,duration=duration,
                         _start_ns=start,_end_ns=start+duration*1000))
    return pd.DataFrame(rows)

def payload_small():
    return {"t_ns":T, "metric":pd.DataFrame({"time":[T-2*10**9,T-10**9,T,T+10**9],
                                            "adservice_CpuUsage-m":[1,1,2,np.nan]}),
            "metric_arrays":{"adservice_CpuUsage-m":{"normal":np.array([1.,1.]),
                                                       "anomalous":np.array([2.,np.nan])}},
            "spans":trace_frame(),
            "logs":pd.DataFrame({"timestamp":[T-1,T,T,T+1],
                                  "container_name":["adservice"]*4,
                                  "message":["ERROR before","ERROR A","ERROR A","fine"]}),
            "window":{}, "provenance":{}}

class ReaderFixture(unittest.TestCase):
    def setUp(self):
        WORK.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=WORK)
        self.root = Path(self.temp.name)
        self.base = self.root/"data/ngoai-rcaeval/nezha/online-boutique/rca_data/2022-08-22"
        self.files = {}
        pods = {}
        for pod, service in nezha.ALIASES.items():
            pods.setdefault(service,pod)
        self.assertEqual(len(pods),10)
        # Resource headers are the original schema, including excluded Node*.
        fields = ["Time","TimeStamp","PodName","CpuUsage(m)","CpuUsageRate(%)",
                  "MemoryUsage(Mi)","MemoryUsageRate(%)","SyscallRead","SyscallWrite",
                  "NetworkReceiveBytes","NetworkTransmitBytes","PodClientLatencyP90(s)",
                  "PodClientLatencyP95(s)","PodClientLatencyP99(s)","PodServerLatencyP90(s)",
                  "PodServerLatencyP95(s)","PodServerLatencyP99(s)","PodWorkload(Ops)",
                  "PodSuccessRate(%)","NodeCpuUsageRate(%)","NodeMemoryUsageRate(%)",
                  "NodeNetworkReceiveBytes"]
        offsets = [-270,-210,-150,-90,-30,30,90,150,210,270]
        for pod in pods.values():
            rows=[]
            for j,offset in enumerate(offsets):
                row={key:"0" for key in fields}
                row.update(Time=wall(T+offset*10**9+123456789),TimeStamp="0",PodName=pod)
                if pod==POD:row["CpuUsage(m)"]=str(j+1)
                rows.append(row)
            self.add(self.base/"metric"/(pod+"_metric.csv"),fields,rows)
        ff=["Time","TimeStamp","ServiceName","SuccessRate(%)","LatencyP50(s)",
            "LatencyP90(s)","LatencyP95(s)","LatencyP99(s)"]
        front=[]
        for j,offset in enumerate(offsets):
            row={key:"0" for key in ff}
            row.update(Time=wall(T+offset*10**9+987654321),TimeStamp="0",
                       ServiceName="Frontend")
            row["LatencyP90(s)"]=str(j+1)
            front.append(row)
        self.add(self.base/"metric/front_service.csv",ff,front)
        tf=["TraceID","SpanID","ParentID","PodName","OperationName",
            "StartTimeUnixNano","EndTimeUnixNano","Duration"]
        rows=[]
        for r in trace_frame().to_dict("records"):
            rows.append(dict(TraceID=r["traceID"],SpanID=r["spanID"],ParentID="",
                             PodName=POD,OperationName=r["operationName"],
                             StartTimeUnixNano=str(r["_start_ns"]),EndTimeUnixNano=str(r["_end_ns"]),
                             Duration=str(r["duration"])))
        rows += [dict(rows[0])]  # An identical occurrence must remain.
        self.add(self.base/"trace/10_00_trace.csv",tf,rows)
        lf=["PodName","TimeUnixNano","Timestamp","Log"]
        timestamp=datetime.fromtimestamp(T//10**9,timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")+".000000001Z"
        lr=[dict(PodName=POD,TimeUnixNano=str(T+1),Timestamp=timestamp,Log="ERROR A")]*2
        self.add(self.base/"log/10_00_log.csv",lf,lr)
        case={"opaque_id":OID,"t_ns":T,"t_ns_sensitivity_A":T-60*10**9,
              "trace_guard_s":41,"files":self.files}
        self.allow={OID:case}

    def add(self,path,fields,rows):
        m=csvfile(path,fields,rows);rel=path.relative_to(self.root).as_posix()
        self.files[rel]={"path":rel,"sha256":m["sha256"],"bytes":m["bytes"]}

    def tearDown(self):
        self.temp.cleanup()

    def load(self):
        return nezha.doc_cua_so(nezha.chon_ca(self.allow,OID,self.root))

    def test_time_precision_and_reject_timezone(self):
        self.assertEqual(nezha.parse_time_ns(wall(T+123456789)),T+123456789)
        with self.assertRaises(LoiRunner):
            nezha.parse_time_ns(wall(T).replace("+0000","+0700"))

    def test_unknown_and_test_codes_before_IO(self):
        with mock.patch.object(Path,"open",side_effect=AssertionError("unexpected IO")):
            for value in ["OB|test|cpu|anything","dev-fffffffffe","../test"]:
                with self.assertRaises(LoiRunner):
                    nezha.chon_ca(self.allow,value,self.root)

    def test_path_scope_before_hash(self):
        for wrong in ["data/locked/x.csv","data/ngoai-rcaeval/nezha/train-ticket/x.csv",
                      "../data/ngoai-rcaeval/nezha/x.csv"]:
            c=json.loads(json.dumps(self.allow))
            rel=next(iter(c[OID]["files"]))
            c[OID]["files"][rel]["path"]=wrong
            with mock.patch.object(Path,"open",side_effect=AssertionError("unexpected IO")):
                with self.assertRaises(LoiRunner):
                    nezha.chon_ca(c,OID,self.root)

    def test_hash_mismatch_rejected(self):
        c=json.loads(json.dumps(self.allow))
        c[OID]["files"][next(iter(self.files))]["sha256"]="0"*64
        with self.assertRaises(LoiRunner):
            nezha.chon_ca(c,OID,self.root)

    def test_native_ordinal_alias_and_repeats(self):
        p=self.load()
        self.assertEqual(p["metric"].shape,(10,166))
        self.assertEqual(p["metric"]["time"].dtype,np.dtype("int64"))
        self.assertEqual(int(p["metric"].time.iloc[0]),T-270*10**9+987654321)
        self.assertEqual(len(p["metric_arrays"]["adservice_CpuUsage-m"]["normal"]),5)
        np.testing.assert_array_equal(p["metric_arrays"]["adservice_CpuUsage-m"]["normal"],[1,2,3,4,5])
        self.assertIn("frontend_FrontLatencyP90-s",p["metric"].columns)
        self.assertEqual(len(p["spans"]),6)
        self.assertEqual(len(p["logs"]),2)
        self.assertEqual(set(p["spans"].serviceName),{"adservice"})
        self.assertEqual(set(p["spans"].operationName),{"op/path"})
        self.assertFalse(any("Node" in c for c in p["metric"].columns))

    def test_conflicting_span_rejected(self):
        rel=next(k for k in self.files if "/trace/" in k)
        path=self.root/rel
        rows=list(csv.DictReader(path.open(encoding="utf-8")))
        rows[-1]["Duration"]="999"
        m=csvfile(path,list(rows[0]),rows)
        self.files[rel].update(sha256=m["sha256"],bytes=m["bytes"])
        with self.assertRaises(LoiRunner):self.load()

    def test_ns_outer_boundaries(self):
        # One ns outside either bound is excluded before unit conversion.
        rel=next(k for k in self.files if "/trace/" in k)
        path=self.root/rel
        rows=list(csv.DictReader(path.open(encoding="utf-8")))
        template=rows[0]
        for i,(start,end) in enumerate([(T-300*10**9-1,T-299*10**9),
                                       (T+299*10**9,T+300*10**9)]):
            rows.append(dict(template,TraceID="outside"+str(i),SpanID="outside"+str(i),
                             StartTimeUnixNano=str(start),EndTimeUnixNano=str(end),
                             Duration=str((end-start)//1000)))
        m=csvfile(path,list(rows[0]),rows)
        self.files[rel].update(sha256=m["sha256"],bytes=m["bytes"])
        self.assertEqual(len(self.load()["spans"]),6)

    def test_sensitivity_A_only_changes_boundary(self):
        a=nezha.chon_ca(self.allow,OID,self.root,view="sensitivity_a")
        self.assertEqual(a["t_ns"],T-60*10**9)
        self.assertEqual(set(a["files"]),set(self.files))

    def test_locator_changes_preserve_input_and_result(self):
        first=self.load()
        with tempfile.TemporaryDirectory(dir=WORK) as other:
            dest=Path(other)
            shutil.copytree(self.root/"data",dest/"data")
            second=nezha.doc_cua_so(nezha.chon_ca(self.allow,OID,dest))
            pd.testing.assert_frame_equal(first["metric"],second["metric"])
            pd.testing.assert_frame_equal(first["spans"],second["spans"])
            pd.testing.assert_frame_equal(first["logs"],second["logs"])
            a=adapters.chay("simplerca",first)[0]
            b=adapters.chay("simplerca",second)[0]
            self.assertEqual(a["items"],b["items"])
            self.assertEqual(a["status"],b["status"])

    def test_all_34_test_names_rejected_before_IO(self):
        split=ROOT/"results/T-021/chia-theo-o/A-phan-tang.csv"
        with split.open(encoding="utf-8-sig",newline="") as f:
            cases=[r["case"] for r in csv.DictReader(f)
                   if r["dataset"]=="Nezha-OB" and r["vai_tro"]=="test"]
        self.assertEqual(len(cases),34)
        for name in cases:
            code="dev-"+hashlib.sha256(name.encode("utf-8")).hexdigest()[:10]
            with mock.patch.object(Path,"open",side_effect=AssertionError("unexpected IO")):
                with self.assertRaises(LoiRunner):nezha.chon_ca(self.allow,code,self.root)

    def test_nested_label_rejected_before_IO(self):
        c=json.loads(json.dumps(self.allow));c[OID]["extra"]={"root":"adservice"}
        with mock.patch.object(Path,"open",side_effect=AssertionError("unexpected IO")):
            with self.assertRaises(LoiRunner):nezha.chon_ca(c,OID,self.root)

class AdapterAnswers(unittest.TestCase):
    def test_trace_guard_exact_cutoff_is_excluded(self):
        p=payload_small()
        cutoff=T-41*10**9
        row=dict(p["spans"].iloc[0]);row.update(traceID="cutoff",spanID="cutoff",
            _start_ns=cutoff-1000000,_end_ns=cutoff,startTime=(cutoff-1000000)//1000,duration=1000)
        p["spans"]=pd.concat([p["spans"],pd.DataFrame([row])],ignore_index=True)
        with mock.patch("p3.adapters.microrank.chay") as call:
            call.return_value={"status":"NO_EVIDENCE","items":[]}
            adapters.chay("microrank",p,41)
            self.assertNotIn("cutoff",set(call.call_args.args[0].traceID))

    def test_simple_equivalence_on_synchronized_input(self):
        from p3.adapters.simplerca import chay as old
        p=payload_small()
        raw=p["metric"].copy(); raw["time"]=raw.time/10**9
        logs=p["logs"].copy(); logs["timestamp"]=logs.timestamp/10**9
        expected=old(raw,p["spans"],logs,T//10**9)
        actual=adapters.chay("simplerca",p)[0]
        self.assertEqual(expected["status"],actual["status"])
        self.assertEqual(expected["items"],actual["items"])

    def test_baro_column_permutation_preserves_keys(self):
        p=payload_small()
        p["metric"]=pd.DataFrame({"time":[T+i*10**9 for i in [-5,-4,-3,-2,-1,0,1,2,3,4]],
                                  "adservice_CpuUsage-m":range(1,11),
                                  "frontend_FrontLatencyP90-s":range(2,12)})
        first=adapters.chay("baro",p)[0]
        p["metric"]=p["metric"].loc[:,list(reversed(p["metric"].columns))]
        second=adapters.chay("baro",p)[0]
        self.assertEqual({it:key for it,_,key in first["items"]},
                         {it:key for it,_,key in second["items"]})

    def test_baro_exact_key_with_native_ns(self):
        values=list(range(1,11))
        p=payload_small()
        p["metric"]=pd.DataFrame({"time":[T+i*10**9 for i in [-5,-4,-3,-2,-1,0,1,2,3,4]],
                                  "adservice_CpuUsage-m":values})
        r=adapters.chay("baro",p)[0]
        self.assertEqual(r["status"],"OK")
        self.assertEqual(r["items"],[("adservice_CpuUsage-m","adservice",(3.5,))])

    def test_simple_known_votes_and_finite_drop(self):
        r=adapters.chay("simplerca",payload_small())[0]
        self.assertEqual(r["status"],"OK")
        # metric=1, trace P95 >3xN-P95=1, log keyword vote=1.
        self.assertEqual(r["items"][0][1:],("adservice",(3.0,)))

    def test_trace_guard_does_not_move_N_to_A(self):
        p=payload_small()
        with mock.patch("p3.adapters.microrank.chay") as call:
            call.return_value={"status":"NO_EVIDENCE","items":[]}
            adapters.chay("microrank",p,41)
            spans,t=call.call_args.args
            self.assertEqual(len(spans),3)  # N one + original A two.
            self.assertEqual(list(spans.traceID),["0","3","4"])
            self.assertEqual(t,T//10**9)
        with mock.patch("p3.adapters.tracerca.chay") as call:
            call.return_value={"status":"ERROR","items":[],"error":"fixture capture"}
            adapters.chay("tracerca",p,32)
            spans,_=call.call_args.args
            self.assertEqual(list(spans.traceID),["0","1","3","4"])

    def test_simple_guard_keeps_metric_log_and_A(self):
        p=payload_small()
        main=adapters.chay("simplerca",p)[0]
        guarded=adapters.chay("simplerca",p,41)[0]
        self.assertEqual(main["diagnostics"]["trace_rows_A_start"],
                         guarded["diagnostics"]["trace_rows_A_start"])
        self.assertEqual(guarded["diagnostics"]["trace_rows_N_start"],1)
        self.assertEqual(guarded["diagnostics"]["trace_rows_removed_N_gap"],2)
        self.assertEqual(main["input_shape"]["metric_rows_N_per_channel"],
                         guarded["input_shape"]["metric_rows_N_per_channel"])
        self.assertEqual(main["input_shape"]["log_rows_A"],guarded["input_shape"]["log_rows_A"])

    def test_tracerca_hand_score(self):
        r=adapters.chay("tracerca",payload_small())[0]
        self.assertEqual(r["status"],"OK")
        self.assertAlmostEqual(r["items"][0][2][0],2/3)
        self.assertEqual(r["items"][0][1],"adservice")

    def test_microrank_groups_answer(self):
        r=adapters.chay("microrank",payload_small())[0]
        self.assertEqual(r["status"],"OK")
        self.assertEqual(r["diagnostics"]["counts"]["normal"],1)
        self.assertEqual(r["diagnostics"]["counts"]["anomaly"],1)

    def test_unsupported_do_not_call_loader_or_ranker(self):
        with mock.patch("p3.adapters.baro.chay",side_effect=AssertionError("ranker called")):
            for name in ["circa","torai_B"]:
                r=adapters.chay(name,None)[0]
                self.assertEqual(r["status"],"UNSUPPORTED")
                self.assertEqual(r["items"],[])

if __name__=="__main__":
    unittest.main(verbosity=2)
