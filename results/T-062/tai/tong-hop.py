"""Summarize retained k6 NDJSON. Only local output files are read."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

def quantile(values, p):
    if not values: return None
    values = sorted(values)
    index = (len(values)-1)*p
    lo = int(index)
    return values[lo] + (values[min(lo+1,len(values)-1)]-values[lo])*(index-lo)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    root = args.directory
    status = defaultdict(Counter)
    duration = defaultdict(list)
    counts = Counter()
    refresh_times = []
    for line in (root/'raw.json').open(encoding='utf-8'):
        item=json.loads(line)
        if item['type'] != 'Point': continue
        metric, data = item['metric'], item['data']
        tags=data.get('tags') or {}
        route=tags.get('route')
        if metric == 'route_responses': status[route][tags['status']]+=data['value']
        if metric == 'http_req_duration' and route and route != 'auth': duration[route].append(data['value'])
        if metric in ['token_refresh_success','token_refresh_failure','dropped_iterations','iterations']:
            counts[metric]+=data['value']
        if metric == 'token_refresh_success': refresh_times.append(data['time'])
    for name in ['token_refresh_success','token_refresh_failure','dropped_iterations','iterations']:
        counts.setdefault(name, 0)
    routes={}
    for route, codes in sorted(status.items()):
        total=sum(codes.values())
        buckets={name:sum(n for code,n in codes.items() if accept(int(code))) for name,accept in {
            '2xx': lambda c: 200<=c<300, '3xx': lambda c: 300<=c<400,
            '4xx': lambda c: 400<=c<500, '429': lambda c: c==429,
            '5xx': lambda c: 500<=c<600, 'transport': lambda c:c==0,
            '401': lambda c:c==401}.items()}
        routes[route]={'requests':total,'status_counts':dict(codes),'counts':buckets,
                       'percent':{k:100*v/total for k,v in buckets.items()},
                       'duration_samples':len(duration[route]),'p95_ms':quantile(duration[route],.95)}
    values=[v for route in duration.values() for v in route]
    run=json.loads((root/'run.json').read_text())
    state=json.loads((root/'state.json').read_text())
    result={'raw_sha256':hashlib.sha256((root/'raw.json').read_bytes()).hexdigest(),
            'source':'raw.json (route_responses, http_req_duration, token_refresh_*, dropped_iterations, iterations)',
            'run':run,'state':state,'routes':routes,'counters':dict(counts),
            'refresh_times':refresh_times,'gateway_requests':sum(v['requests'] for v in routes.values()),
            'p95_ms':quantile(values,.95),'p95_method':'linear interpolation at (n-1)*0.95; milliseconds',
            'note':'429 and 401 are subsets of 4xx. Auth refresh HTTP calls excluded from gateway counts/p95.'}
    (root/'phan-tich.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    report=['# Chạy thử 5 phút — C1', '',
            f"Máy `{run['machine']}`; cấu hình {run['rate']} req/s, {run['seconds']} giây. Container exit {state['ExitCode']}.",
            f"Gateway: {result['gateway_requests']:g} request; p95 {result['p95_ms']:.3f} ms.",
            '', '| Route | Request | 2xx | 4xx | 429 | 5xx | p95 (ms) |',
            '|---|---:|---:|---:|---:|---:|---:|']
    for route,v in routes.items():
        p=v['percent']
        report.append(f"| {route} | {v['requests']:g} | {p['2xx']:.2f}% | {p['4xx']:.2f}% | {p['429']:.2f}% | {p['5xx']:.2f}% | {v['p95_ms']:.3f} |")
    unauthorized=sum(v['counts']['401'] for v in routes.values())
    report.extend(['', '429 là tập con của 4xx; không cộng hai cột. Lỗi transport và mã cụ thể ở `phan-tich.json#/routes`.',
        f"Refresh thành công: {counts['token_refresh_success']:g}; lỗi refresh: {counts['token_refresh_failure']:g}; HTTP 401: {unauthorized:g}; dropped iterations: {counts['dropped_iterations']:g}.",
        '', 'Nguồn số: `chay-thu-5p/phan-tich.json#/routes`, `#/counters`, `#/gateway_requests`, `#/p95_ms`; dữ liệu gốc `raw.json`, summary k6 `summary.json`, hash trong `outputs.sha256`.',
        'Chỉ xác nhận vận hành tải trong lượt này. Không suy nguyên nhân lỗi ứng dụng hoặc chất lượng RCA từ số đo phía k6.'])
    (root.parent/'chay-thu-5p.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
    print(json.dumps({'gateway_requests':result['gateway_requests'],'p95_ms':result['p95_ms'],'counters':dict(counts),'401':unauthorized,'exit':state['ExitCode']}))

if __name__=='__main__': main()
