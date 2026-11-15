# Xuất mẫu thô mọi metric (trừ metric nội bộ Prometheus/Go) của cửa sổ D2 + E1 T-062 từ Prometheus exp-obs.
# Lý do: storage.tsdb.retention.time = 2d (đọc 12/11 ~19:00Z); gói ca T-062 chỉ có 7 truy vấn.
# Chạy trên exp-obs qua ssh (script đọc từ stdin), chỉ ĐỌC Prometheus, in JSONL ra stdout; không ghi file trên máy.
# Mỗi dòng: {"name": <tên metric>, "resp": <phản hồi /api/v1/query nguyên văn, matrix mẫu thô>}.
import json, sys, urllib.parse, urllib.request

B = 'http://localhost:9090/api/v1/'
S, E = 1794416400, 1794450600  # 11/11/2026 17:00:00Z .. 12/11/2026 02:30:00Z
SKIP = ('prometheus_', 'go_', 'promhttp_')
names = json.load(urllib.request.urlopen(B + 'label/__name__/values', timeout=60))['data']
sys.stdout.write(json.dumps({'meta': {'start': S, 'end': E, 'n_names': len(names), 'skip_prefix': SKIP,
                                      'query': '<name>[<E-S>s] @ E (mẫu thô)'}}) + '\n')
for n in names:
    if n.startswith(SKIP):
        continue
    q = urllib.parse.urlencode({'query': f'{n}[{E - S}s]', 'time': E})
    try:
        r = json.load(urllib.request.urlopen(B + 'query?' + q, timeout=300))
    except Exception as e:  # giữ lỗi theo từng metric, không dừng cả lượt
        r = {'status': 'error', 'error': repr(e)}
    sys.stdout.write(json.dumps({'name': n, 'resp': r}, separators=(',', ':')) + '\n')
    sys.stdout.flush()
