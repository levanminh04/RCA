cd /opt/flashticket-rca
for i in $(seq 1 60); do r=$(python3 -B load/controller/tai_linux.py get --tag kiem-sau-don-001); echo "$r" | grep -q '"Running": *false\|"Running":false' && break; sleep 15; done
echo "$r" | python3 -c "import json,sys;d=json.load(sys.stdin);s=d['result']['state'];print({k:s.get(k) for k in ('Status','Running','ExitCode','OOMKilled','StartedAt','FinishedAt')})"
python3 -B load/controller/tai_linux.py receive --tag kiem-sau-don-001 | cut -c1-400
ls /srv/flashticket-rca/load/tai-out/kiem-sau-don-001/
python3 - <<'PY'
import json
s=json.load(open('/srv/flashticket-rca/load/tai-out/kiem-sau-don-001/summary.json'))
m=s.get('metrics',{})
def g(n,k):
    v=m.get(n,{}); v=v.get('values',v); return v.get(k)
print({'journey_started':g('journey_started','count'),'journey_finished':g('journey_finished','count'),'journey_failed':g('journey_failed','count'),
       'http_reqs':g('http_reqs','count'),'http_req_failed_rate':g('http_req_failed','rate'),'dropped':g('dropped_iterations','count'),
       'p95_expected':g('http_req_duration{expected_response:true}','p(95)')})
PY
