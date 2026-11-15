# Xuất nốt 4 metric lỗi ở lượt đầu (xuat.py): truy vấn một phát cả 9,5 giờ của histogram span-metrics làm
# Prometheus exp-obs tự khởi động lại lúc 12/11 19:16:33Z (xem SU-CO.md). Lượt này cắt khúc 10 phút, nghỉ giữa các khúc.
# Chỉ ĐỌC Prometheus; in JSONL ra stdout. Mỗi dòng: {"name", "t_end", "win_s", "resp"}.
import json, sys, time, urllib.parse, urllib.request

B = 'http://localhost:9090/api/v1/'
S, E, W = 1794416400, 1794450600, 600
NAMES = ['up', 'traces_span_metrics_duration_seconds_count', 'traces_span_metrics_duration_seconds_sum',
         'traces_span_metrics_duration_seconds_bucket']


def get(path, **kw):
    return json.load(urllib.request.urlopen(B + path + '?' + urllib.parse.urlencode(kw), timeout=120))


dem = {n: get('query', query=f'count({n})')['data']['result'] for n in NAMES}
sys.stdout.write(json.dumps({'meta': {'start': S, 'end': E, 'win_s': W, 'count_now': dem}}) + '\n')
for n in NAMES:
    t = S + W
    while t <= E:
        try:
            # (t-W, t]: mẫu thô trong khúc; khúc liền nhau không trùng mẫu
            r = get('query', query=f'{n}[{W}s]', time=t)
        except Exception as e:
            r = {'status': 'error', 'error': repr(e)}
            time.sleep(20)  # nếu máy chủ vừa ngã, chờ rồi đi tiếp, không dồn truy vấn
        sys.stdout.write(json.dumps({'name': n, 't_end': t, 'win_s': W, 'resp': r}, separators=(',', ':')) + '\n')
        sys.stdout.flush()
        t += W
        time.sleep(0.3)
