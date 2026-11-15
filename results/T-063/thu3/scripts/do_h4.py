#!/usr/bin/env python3
"""T-063 thu3 — đo lưu lượng AMQP broker→Booking và tồn queue Booking (chỉ đọc, chạy trên exp-app).
Dùng: nohup python3 do_h4.py <file-ra.jsonl> <giây> [chu kỳ 15] &
Nguồn: rabbitmqctl trong container broker (không gọi HTTP của app). Kết nối của Booking = kết nối chứa channel đang tiêu thụ booking.accept-payment.q."""
import json, subprocess, sys, time, datetime as dt
RA, DUR = sys.argv[1], int(sys.argv[2]); STEP = int(sys.argv[3]) if len(sys.argv) > 3 else 15
RB = ['docker', 'exec', 'flash-ticket-infra-rabbitmq-1', 'rabbitmqctl', '-q']
def q(*a): return [l.split('\t') for l in subprocess.run(RB + list(a), capture_output=True, text=True, timeout=60).stdout.splitlines()[1:]]
end = time.time() + DUR
while time.time() < end:
    t0 = time.time()
    try:
        ch = {c[0]: c[1] for c in q('list_consumers', 'queue_name', 'channel_pid')}
        conn_pid = None
        if 'booking.accept-payment.q' in ch:
            cp = {c[0]: c[1] for c in q('list_channels', 'pid', 'connection')}
            conn_pid = cp.get(ch['booking.accept-payment.q'])
        conns = {c[0]: c[1:] for c in q('list_connections', 'pid', 'send_oct', 'recv_oct', 'send_cnt', 'recv_cnt', 'state')}
        qs = {c[0]: [int(c[1]), int(c[2]), int(c[3])] for c in q('list_queues', 'name', 'messages_ready', 'messages_unacknowledged', 'consumers') if c[0].startswith('booking.')}
        rec = {'t': dt.datetime.now(dt.timezone.utc).isoformat(), 'epoch': round(t0, 1), 'booking_conn': conn_pid,
               'conn': conns.get(conn_pid), 'n_conn': len(conns), 'queues': qs}
    except Exception as e:
        rec = {'t': dt.datetime.now(dt.timezone.utc).isoformat(), 'err': str(e)[:200]}
    with open(RA, 'a') as f: f.write(json.dumps(rec) + '\n')
    time.sleep(max(1, STEP - (time.time() - t0)))
