"""Check duration against native span clock, every acquired trace CSV."""
import csv,json,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];BASE=ROOT/'data/ngoai-rcaeval/nezha';OUT=ROOT/'results/T-008/runs/units-001';OUT.mkdir(exist_ok=False);rows=[];began=time.monotonic()
for p in sorted(BASE.rglob('*_trace.csv')):
    count=negative=micro=milli=nano=invalid=0;max_micro=0
    with p.open(encoding='utf-8-sig',newline='') as f:
        for r in csv.DictReader(f):
            count+=1
            try:delta=int(r['EndTimeUnixNano'])-int(r['StartTimeUnixNano']);duration=float(r['Duration'])
            except (ValueError,KeyError):invalid+=1;continue
            negative+=delta<0;micro+=abs(duration-delta/1000)<=1;milli+=abs(duration-delta/1_000_000)<=1;nano+=abs(duration-delta)<=1;max_micro=max(max_micro,abs(duration-delta/1000))
    rows.append(dict(path=p.relative_to(BASE).as_posix(),rows=count,invalid=invalid,negative_span_duration=negative,microsecond_match_within_one_us=micro,millisecond_match_within_one_ms=milli,nanosecond_match_within_one_ns=nano,max_microsecond_residual=max_micro))
(OUT/'result.json').write_text(json.dumps(dict(files=rows,elapsed_seconds=time.monotonic()-began,scope='Duration compared to span End-Start; tolerances reflect recorded integer precision, not score epsilon'),indent=2));print('Checked',len(rows),'files')
