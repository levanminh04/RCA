import json,pathlib,math
ROOT=pathlib.Path(__file__).resolve().parents[3]
a=json.loads((ROOT/'results/T-015/runs/pilot/re2ob_checkoutservice_cpu_1.json').read_text(encoding='utf-8'))
b=json.loads((ROOT/'results/T-015/runs/ob-pilot-ec2-2/re2ob_checkoutservice_cpu_1.json').read_text(encoding='utf-8'))
errors=[]
def compare(x,y,path):
    if isinstance(x,dict):
        assert set(x)==set(y),path
        for k in x:compare(x[k],y[k],path+'.'+str(k))
    elif isinstance(x,(float,int)):
        error=abs(x-y);relative=error/max(abs(x),abs(y),1e-300)
        errors.append(error);assert error<=1e-10 and relative<=1e-10,(path,x,y)
    else:assert x==y,path
for field in ['status','ranks','full_ranks','service_ranks_top11','service_ranks_full','counts','scores','spectrum','baseline_slo_ms','operation_services','options']:
    compare(a[field],b[field],field)
for group in ['normal','anomaly']:
    for field in ['graph','audit','trace_count']:compare(a['groups'][group][field],b['groups'][group][field],group+'.'+field)
    for field in ['weights','tracecounts']:compare(a['groups'][group]['official'][field],b['groups'][group]['official'][field],group+'.'+field)
out={'all_passed':True,'same_source_sha256':a['source_sha256']==b['source_sha256'],'rank_exact':a['ranks']==b['ranks'],'numeric_comparisons':len(errors),'maximum_absolute_error':max(errors),'scope':'two pinned EC2 runtimes; include_graph hook and metadata additions do not change shared numeric outputs','first_case_file':'runs/pilot/re2ob_checkoutservice_cpu_1.json','second_case_file':'runs/ob-pilot-ec2-2/re2ob_checkoutservice_cpu_1.json'}
assert out['same_source_sha256']
(ROOT/'results/T-015/runs/pilot-environment-repeat.json').write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out))
