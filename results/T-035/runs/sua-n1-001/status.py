"""Đọc tiến độ và ước lượng chi phí, không sửa kết quả hoặc điều khiển lượt chạy."""
from datetime import datetime, timezone
import json
from pathlib import Path

BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[3]
rows=[json.loads(line) for line in (BASE/'day-du-002/progress.jsonl').read_text('utf-8').splitlines()]
cases=[json.loads(p.read_text('utf-8')) for p in (BASE/'day-du-002/cases').rglob('*.json')]
old=json.loads((ROOT/'results/T-035/runs/day-du-001/summary.json').read_text('utf-8'))['cases']
index={(c['dataset'],c['opaque_id']):c for c in old}
prior=sum(index[(c['dataset'],c['opaque_id'])]['seconds'] for c in cases)
ratio=sum(c['seconds'] for c in cases)/prior if prior else None
start=datetime.fromisoformat(rows[0]['utc'])
print(json.dumps({'completed':len(cases),'total':len(old),
                  'elapsed_minutes':round((datetime.now(timezone.utc)-start).total_seconds()/60,2),
                  'projected_minutes':round(ratio*sum(c['seconds'] for c in old)/60,2) if ratio else None,
                  'last_stage':rows[-1]['stage'],'dataset':rows[-1].get('dataset'),
                  'failure':(BASE/'day-du-002/failure.json').exists(),
                  'summary':(BASE/'day-du-002/summary.json').exists()}))
