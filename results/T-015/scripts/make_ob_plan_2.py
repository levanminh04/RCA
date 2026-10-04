import json,pathlib
root=pathlib.Path(__file__).resolve().parents[3]
rows=json.loads((root/'results/T-007/runs/e1/manifest-re2ob.json').read_text(encoding='utf-8-sig'))['files']
cases=sorted(set(r['case'] for r in rows));assert len(cases)==90
remaining=[c for c in cases if c!='re2ob_checkoutservice_cpu_1']
blocks=[remaining[i:i+30] for i in range(0,89,30)]
plan={'cases':cases,'primary_pilot':'re2ob_checkoutservice_cpu_1','blocks':blocks,'pilot_second_seconds':12.067525947997638,'forecast_seconds_remaining':89*12.067525947997638,'method_dataset_budget_seconds':10800,'half_seconds':600,'seed':0,'timing_official':False,'no_baseline_rerun':True}
(root/'results/T-015/runs/ob-plan-ec2-2.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
lines=['#!/usr/bin/env bash','set -eu','TASK_ROOT="$HOME/rca/T-015"']
for i,block in enumerate(blocks,1):
    lines+=['uptime','free -m','ps -eo pid,etimes,%cpu,rss,args --sort=-%cpu | head -12',
        'bash "$TASK_ROOT/results/T-015/scripts/launch.sh" ob-block-'+str(i)+' "$TASK_ROOT/data" '+','.join(block)+' 600 1800 0','date -u']
path=root/'results/T-015/scripts/run_ob_2.sh';path.write_bytes(('\n'.join(lines)+'\n').encode())
assert b'\r' not in path.read_bytes()
print(json.dumps({'blocks':[len(b) for b in blocks],'forecast_remaining_seconds':plan['forecast_seconds_remaining'],'shell_LF':True}))
