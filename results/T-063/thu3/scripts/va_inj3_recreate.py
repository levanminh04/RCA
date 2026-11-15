p = 'D:/RCA-flashticket/results/T-063/thu3/scripts/inj3.py'
s = open(p, encoding='utf-8').read()


def thay(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:70])
    s = s.replace(a, b)


thay("Khác inj2.py: ô POOL-EVENT-4/5 (thử cường độ), CONSUMER-BOOK-SLOW-X3, BINH-THUONG-X3; đầu dò thêm `rabbit_booking`\n",
     "Khác inj2.py: ô POOL-EVENT-4/5 (thử cường độ), CONSUMER-BOOK-SLOW-X3, BINH-THUONG-X3, RECREATE-PAY (yêu cầu phiên C,\n"
     "results/T-064/phien-c/YEU-CAU-O.md: tạo lại container payment một lần tại t, cùng image/compose/env); đầu dò thêm `rabbit_booking`,\n"
     "`payment_container` (Id, StartedAt) và ")
thay("(rabbitmqctl trong container broker) và `pool_event` (bản ghi pool cuối trong audit Event).",
     "`pool_event` (bản ghi pool cuối trong audit Event); `rabbit_booking` dùng rabbitmqctl trong container broker.")
thay("""    'BINH-THUONG-X3': dict(kind='none'),
""", """    'BINH-THUONG-X3': dict(kind='none'),
    'RECREATE-PAY': dict(kind='recreate', container=PAY, project='flash-ticket-payment-service', compose='payment-service.yml'),
""")
thay("""    elif c['kind'] == 'pause':
        sh('docker', 'pause', c['container'])
        (STATE / f'{cell}.pause-deadline').write_text(str(time.time() + seconds))
""", """    elif c['kind'] == 'pause':
        sh('docker', 'pause', c['container'])
        (STATE / f'{cell}.pause-deadline').write_text(str(time.time() + seconds))
    elif c['kind'] == 'recreate':
        # tạo lại đúng một lần với image đang chạy, compose/env -t062 không đổi (cùng cách deploy-t062.sh); không tự hoàn tác
        cu = sh('docker', 'inspect', c['container'], '--format', '{{.Id}} {{.Config.Image}} {{.State.StartedAt}}').split()
        r = subprocess.run(['docker', 'compose', '-p', c['project'], '-f', c['compose'], 'up', '-d', '--force-recreate', '--no-deps'],
                           cwd=str(A / 'compose-t062'), env={**os.environ, 'IMAGE': cu[1]}, capture_output=True, text=True, timeout=180)
        moi = sh('docker', 'inspect', c['container'], '--format', '{{.Id}} {{.Config.Image}} {{.State.StartedAt}}').split()
        out(op='recreate', cell=cell, rc=r.returncode, cu_id=cu[0], cu_started=cu[2], moi_id=moi[0], moi_started=moi[2], image=moi[1],
            stderr_tail=r.stderr[-200:])
        if r.returncode != 0 or moi[0] == cu[0] or moi[1] != cu[1]: raise RuntimeError('recreate không đúng: rc/Id/image')
""")
thay("""    elif c['kind'] == 'pause':
        r = subprocess.run(['docker', 'unpause', c['container']], capture_output=True, text=True)""",
     """    elif c['kind'] == 'recreate':
        pass  # tạo lại là thao tác một lần, không có trạng thái để gỡ
    elif c['kind'] == 'pause':
        r = subprocess.run(['docker', 'unpause', c['container']], capture_output=True, text=True)""")
thay("""    r['payment_state'] = sh('docker', 'inspect', PAY, '--format', '{{.State.Status}} {{.State.Paused}}', check=False).strip()
""", """    r['payment_state'] = sh('docker', 'inspect', PAY, '--format', '{{.State.Status}} {{.State.Paused}}', check=False).strip()
    r['payment_container'] = sh('docker', 'inspect', PAY, '--format', '{{.Id}} {{.State.StartedAt}} {{.RestartCount}}', check=False).strip()
""")
compile(s, p, 'exec')
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ok')
