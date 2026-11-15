# -*- coding: utf-8 -*-
"""T-063 bước 2 — phép thử phân xử cơ chế CPU-BOOK (chạy trên exp-app: ssh ... 'python3 -' < thu_cuong_do.py).

Giả thuyết H-cum: với quota 1 lõi (chu kỳ CFS 100 ms) và 2 luồng đốt trên máy 2 lõi, Booking chiếm cả hai lõi trong phần
đầu mỗi chu kỳ rồi bị throttle → tiến trình khác (Postgres, Event…) chờ CPU theo cụm → trễ tăng ở service không phụ thuộc
Booking, dù CPU trung bình 10 s của chúng không đổi. Dự đoán phân biệt: 1 luồng đốt (dùng ≤ 1 lõi liên tục, không chiếm
hai lõi cùng lúc) làm trễ của đường không qua Booking tăng ít hơn rõ so với 2 luồng; áp lực CPU máy (`/proc/pressure/cpu`)
tăng theo cùng chiều.
Giả thuyết khác: H-phu-thuoc (trễ lan qua lời gọi tới Booking) — đường đo ở đây (Gateway → Event → Postgres; Postgres trực
tiếp) không gọi Booking, nên nếu trễ tăng thì không do phụ thuộc gọi.

Cơ chế đốt giống hệt `~/inj.py` ô CPU-BOOK (`docker exec -d BOOK timeout N sh -c ': rcaburn; while :; do :; done'`).
Không gửi nhãn tới ứng dụng. In JSON mỗi dòng. Dọn tiến trình đốt khi kết thúc hoặc lỗi.
"""
import json, os, pathlib, socket, statistics, subprocess, sys, time, urllib.request, datetime as dt

BOOK = 'flash-ticket-booking-service-booking-service-1'
URL = 'http://10.0.0.158:8081/api/v1/events?size=1'
PHA = [('nen_1', 0, 60), ('dot_2_luong', 2, 60), ('nghi_1', 0, 25), ('dot_1_luong', 1, 60), ('nghi_2', 0, 25), ('nen_2', 0, 40)]
HZ = 10.0


def now(): return dt.datetime.now(dt.timezone.utc).isoformat()
def out(**k): print(json.dumps({'t': now(), **k}, ensure_ascii=False)); sys.stdout.flush()
def sh(*c, check=True): return subprocess.run(c, capture_output=True, text=True, check=check).stdout


def cg():
    cid = sh('docker', 'inspect', BOOK, '--format', '{{.Id}}').strip()
    b = pathlib.Path(f'/sys/fs/cgroup/system.slice/docker-{cid}.scope')
    st = dict(l.split() for l in (b / 'cpu.stat').read_text().splitlines())
    return {k: int(st.get(k, 0)) for k in ('usage_usec', 'nr_periods', 'nr_throttled', 'throttled_usec')}


def psi():
    f = pathlib.Path('/proc/pressure/cpu').read_text().split()
    return int([x for x in f if x.startswith('total=')][0].split('=')[1])  # dòng 'some' đứng trước


def stat_cpu():
    v = [int(x) for x in pathlib.Path('/proc/stat').read_text().splitlines()[0].split()[1:]]
    return sum(v), v[3] + v[4]  # tổng, idle+iowait


def pg_rtt():
    s = socket.create_connection(('127.0.0.1', 5432), timeout=3); t = time.perf_counter()
    s.sendall(b'\x00\x00\x00\x08\x04\xd2\x16\x2f'); s.recv(1); s.close(); return (time.perf_counter() - t) * 1000


def http_ms():
    t = time.perf_counter()
    try: code = urllib.request.urlopen(URL, timeout=5).status
    except urllib.error.HTTPError as e: code = e.code
    except Exception: code = -1
    return (time.perf_counter() - t) * 1000, code


def dot(n, giay):
    for _ in range(n):
        sh('docker', 'exec', '-d', BOOK, 'timeout', str(giay), 'sh', '-c', ': rcaburn; while :; do :; done')


def don():
    sh('docker', 'exec', BOOK, 'pkill', '-f', 'rcaburn', check=False)


def q(xs, p):
    xs = sorted(xs); return round(xs[min(len(xs) - 1, int(p * len(xs)))], 2) if xs else None


def main():
    don()
    out(su_kien='bat_dau', pha=PHA, url=URL)
    try:
        for ten, n, giay in PHA:
            c0, p0, (tot0, idl0) = cg(), psi(), stat_cpu()
            if n: dot(n, giay + 2)
            hs, pgs, codes = [], [], {}
            t_end = time.time() + giay; k = 0
            while time.time() < t_end:
                t_next = time.time() + 1 / HZ
                h, c = http_ms(); hs.append(h); codes[c] = codes.get(c, 0) + 1
                try: pgs.append(pg_rtt())
                except Exception: pass
                k += 1
                time.sleep(max(0, t_next - time.time()))
            if n: don()
            c1, p1, (tot1, idl1) = cg(), psi(), stat_cpu()
            ncpu = os.cpu_count()
            out(su_kien='pha', ten=ten, luong=n, giay=giay, mau=k, http_code=codes,
                http_ms={'p50': q(hs, .5), 'p90': q(hs, .9), 'p99': q(hs, .99), 'tb': round(statistics.mean(hs), 2)},
                pg_ms={'p50': q(pgs, .5), 'p90': q(pgs, .9), 'p99': q(pgs, .99), 'tb': round(statistics.mean(pgs), 2) if pgs else None},
                psi_some_ms_moi_giay=round((p1 - p0) / 1000 / giay, 1),
                may_ban_loi=round(ncpu * (1 - (idl1 - idl0) / max(1, tot1 - tot0)), 3),
                booking={'loi_cpu': round((c1['usage_usec'] - c0['usage_usec']) / 1e6 / giay, 3),
                         'ty_le_chu_ky_throttle': round((c1['nr_throttled'] - c0['nr_throttled']) / max(1, c1['nr_periods'] - c0['nr_periods']), 3),
                         'throttled_ms_moi_giay': round((c1['throttled_usec'] - c0['throttled_usec']) / 1000 / giay, 1)})
            time.sleep(2)
    finally:
        don()
        out(su_kien='ket_thuc', so_tien_trinh_dot_con_lai=sh('docker', 'exec', BOOK, 'sh', '-c', "ps -o args | grep -c '^sh -c : rcaburn' || true", check=False).strip())


main()
