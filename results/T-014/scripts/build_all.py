import os
os.environ['PYTHONDONTWRITEBYTECODE']='1'
import sys,json,time,csv
from pathlib import Path
import pandas as pd
import pyarrow.parquet as pq
sys.path[:0]=['D:/RCA-flashticket/src','D:/RCA-ext/src/RCAEval']
from circa_kien_truc import service_calls,build_graph
root=Path('D:/RCA-flashticket');out=root/'results/T-014'
inventory=json.loads((out/'runs/inventory.json').read_text())
summary=[]
for row in inventory:
    start=time.monotonic();case=row['case'];source=root/'data/rcaeval'/case
    columns=pq.read_schema(source/'metrics.parquet').names
    tr=pd.read_parquet(source/'traces.parquet',columns=['traceID','spanID','parentSpanID','serviceName','startTime'])
    calls,trace_report=service_calls(tr,row['inject_time'])
    graph,report=build_graph(columns,calls,'D:/RCA-ext/work/T-014/CIRCA')
    report.update(trace=trace_report,nodes=sorted(graph.nodes),edges=sorted(map(list,graph.edges)),case=case,elapsed_diagnostic=time.monotonic()-start)
    (out/'graphs'/f'{case}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    summary.append(dict(case=case,raw_metrics=len(columns)-int('time' in columns),mapped=len(report['mapping'])-len(report['unknown']),unknown=len(report['unknown']),service_nodes=trace_report['service_nodes'],service_edges=trace_report['service_edges'],metric_nodes=len(graph),metric_edges=graph.number_of_edges(),dag=report['dag'],isolated=len(report['isolated']),original_missing=len(report['original_missing_nodes']),auth_without_call='ts-auth-service' in report['service_without_call_edge'],elapsed_diagnostic=report['elapsed_diagnostic']))
    with (out/'runs/build-progress.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps(summary[-1])+'\n')
    print(json.dumps(summary[-1]),flush=True)
    del tr,graph,calls
with (out/'graphs/summary.csv').open('w',newline='',encoding='utf-8') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
