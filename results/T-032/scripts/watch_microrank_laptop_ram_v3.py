"""Q-108/Q-126 repair: independently sample the existing 95% system-RAM rule.
No method/data imports, replay, case selection, tolerance or new RAM criterion.
Writes only a new T-032 monitor run, retaining v1/v2 and every RCA artifact.
"""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time

REPO=Path("D:/RCA-flashticket")
BASE=REPO/"results/T-032"
COHORT=BASE/"runs/microrank-laptop-cohort-001"
MAX_PERCENT=95.0
POLL_S=0.05

def now():
    return datetime.now(timezone.utc).isoformat()

def dump_new(path,value):
    with path.open("x",encoding="utf-8",newline="\n") as stream:
        json.dump(value,stream,ensure_ascii=False,indent=2,allow_nan=False)
        stream.write("\n")

def read(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))

def source_identity():
    status=read(COHORT/"status.json")
    segment=COHORT/"segments"/status["segment_id"]
    path=segment/"controller-identity.json"
    if not path.is_file():
        return status,None
    return status,read(path)

def same_process(psutil,identity):
    try:
        process=psutil.Process(identity["pid"])
        return process if abs(process.create_time()-identity["creation_time"])<0.001 and process.is_running() else None
    except psutil.NoSuchProcess:
        return None

def stop_owned_controller(psutil,identity):
    process=same_process(psutil,identity)
    if process is None:
        return []
    owned=process.children(recursive=True)+[process]
    stopped=[]
    for child in reversed(owned[:-1]):
        try:
            stopped.append({"pid":child.pid,"creation_time":child.create_time()})
            child.terminate()
        except psutil.NoSuchProcess:
            pass
    try:
        stopped.append({"pid":process.pid,"creation_time":process.create_time()})
        process.terminate()
    except psutil.NoSuchProcess:
        pass
    gone,alive=psutil.wait_procs(owned,timeout=5)
    for child in alive:
        child.kill()
    gone,alive=psutil.wait_procs(alive,timeout=5)
    if alive:
        raise RuntimeError("Owned controller/worker tree did not stop")
    return stopped

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    parser.add_argument("--source-sha256",required=True)
    args=parser.parse_args()
    expected=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    if expected!=args.source_sha256:
        raise RuntimeError("Reviewed monitor source differs")
    output=Path(args.output).resolve()
    if not output.is_relative_to(BASE.resolve()) or output.is_relative_to(COHORT.resolve()) or output.is_symlink():
        raise RuntimeError("Monitor output outside new approved T032 run")
    output.mkdir(parents=True,exist_ok=False)
    import psutil
    own=psutil.Process()
    dump_new(output/"process.json",{"pid":own.pid,"creation_time":own.create_time(),"argv":sys.argv,
        "source_sha256":expected,"rule":"existing Q126 system RAM >=95%; no preworker free-RAM gate"})
    count=0
    peak=0.0
    max_gap=0.0
    last=None
    last_log=0.0
    began=time.perf_counter()
    result={"status":"MONITORING_EXISTING_RAM_RULE","started_utc":now(),"max_system_ram_percent":MAX_PERCENT,"poll_s":POLL_S}
    with (output/"samples.jsonl").open("x",encoding="utf-8",newline="\n") as stream:
        while True:
            stamp=time.perf_counter()
            if last is not None:
                max_gap=max(max_gap,stamp-last)
            last=stamp
            memory=psutil.virtual_memory()
            count+=1
            peak=max(peak,memory.percent)
            status,identity=source_identity()
            if stamp-last_log>=10 or memory.percent>=MAX_PERCENT:
                stream.write(json.dumps({"at_utc":now(),"system_ram_percent":memory.percent,
                    "available_bytes":memory.available,"peak_sampled_percent":peak,"sample_count":count,
                    "max_sample_gap_s":max_gap,"segment_id":status["segment_id"]})+"\n")
                stream.flush()
                last_log=stamp
            if memory.percent>=MAX_PERCENT:
                result.update(status="STOP_SYSTEM_RAM_95",observed_percent=memory.percent,
                    threshold_utc=now(),controller_identity=identity,current_status=status)
                dump_new(output/"ram-threshold-stop.json",result)
                result["stopped_owned_identities"]=[] if identity is None else stop_owned_controller(psutil,identity)
                break
            if status["status"]=="FAIL_STOP":
                result.update(status="MONITOR_CLOSED_BRANCH_FAIL_STOP",current_status=status)
                break
            if status["status"]=="PASS_FULL52_LAPTOP_EXACT":
                if identity is None or same_process(psutil,identity) is None:
                    result.update(status="MONITOR_CLOSED_FULL52",current_status=status)
                    break
            time.sleep(POLL_S)
    result.update(ended_utc=now(),elapsed_s=time.perf_counter()-began,sample_count=count,
        peak_sampled_system_ram_percent=peak,max_sample_gap_s=max_gap,
        actual_worker_peak_note="Worker Windows lifetime peak stays in existing controller/case cost; this process only samples system RAM.")
    dump_new(output/"terminal.json",result)
    files=[{"path":q.relative_to(output).as_posix(),"bytes":q.stat().st_size,
        "sha256":hashlib.sha256(q.read_bytes()).hexdigest()} for q in sorted(output.rglob("*")) if q.is_file()]
    dump_new(output/"closed.json",{"status":result["status"],"files":files,"manifest_excludes":["closed.json"]})
    return 2 if result["status"]=="STOP_SYSTEM_RAM_95" else 0

if __name__=="__main__":
    sys.dont_write_bytecode=True
    raise SystemExit(main())
