
## 2026-11-11T18:36:27.7381858Z - tai

```sh
set -euo pipefail
date -u --iso-8601=seconds
test ! -e /opt/rca-tai
dpkg-query -W docker.io docker-ce containerd runc 2>/dev/null || true
sudo -n install -d -m 0755 -o ubuntu -g ubuntu /opt/rca-tai
mkdir -p /opt/rca-tai/k6 /opt/rca-tai/out
install -d -m 0700 /opt/rca-tai/secret
sudo -n apt-get update -qq
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl chrony
sudo -n install -m 0755 -d /etc/apt/keyrings
sudo -n curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo -n chmod a+r /etc/apt/keyrings/docker.asc
. /etc/os-release
printf 'Types: deb\nURIs: https://download.docker.com/linux/ubuntu\nSuites: %s\nComponents: stable\nArchitectures: %s\nSigned-By: /etc/apt/keyrings/docker.asc\n' "$VERSION_CODENAME" "$(dpkg --print-architecture)" | sudo -n tee /etc/apt/sources.list.d/docker.sources
sudo -n apt-get update -qq
sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo -n systemctl enable --now docker chrony
sudo -n docker pull grafana/k6:1.4.2
sudo -n docker image inspect grafana/k6:1.4.2 --format '{{json .RepoDigests}} {{.Architecture}} {{.Size}}'
sudo -n docker version
chronyc tracking
timedatectl show -p NTPSynchronized
date -u --iso-8601=seconds

```

## 2026-11-11T18:36:49.9510552Z - obs

```sh
set -eu; date -u --iso-8601=seconds; test ! -e /opt/rca-tai; sudo -n install -d -m 0755 -o ubuntu -g ubuntu /opt/rca-tai; mkdir -p /opt/rca-tai/k6 /opt/rca-tai/out; install -d -m 0700 /opt/rca-tai/secret
```

Exit: 0

Exit: 0

## 2026-11-11T18:38:35.0898309Z - obs

```sh
set -eu; sudo -n docker run --name rca-tai-version-01 grafana/k6:1.4.2@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 version; sudo -n docker image inspect grafana/k6:1.4.2@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 --format "{{json .RepoDigests}} {{.Architecture}} {{.Size}}"
```

Exit: 0

2026-11-11T18:38:43.3375501Z - obs : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

2026-11-11T18:40:13.1960655Z - obs : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

2026-11-11T18:40:41.4830705Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

2026-11-11T18:40:44.2742716Z - tai : scp results/T-062/tai/fixture.py -> /opt/rca-tai/fixture.py ; sha256=607AFCFB57A58F5A487FA47BD2493F28232A0BF90BDCC1E8990F8F148049DFB8

2026-11-11T18:41:52.1203043Z - obs : scp results/T-062/tai/k6/workload-t062.js -> /opt/rca-tai/k6/workload-t062.js ; sha256=FBBFB55432951E178B058813D07D2F517D6FF79F29E9684BA008907610C0C534

2026-11-11T18:41:53.7663277Z - obs : scp results/T-062/tai/k6/fixtures.json -> /opt/rca-tai/k6/fixtures.json ; sha256=EC13B5B08B5FEF7391BBC9B1B77A0D359E022390B92CB52A9BB4C4333E9BF7FA

2026-11-11T18:41:54.9212311Z - obs : scp results/T-062/tai/k6/cau-hinh.json -> /opt/rca-tai/k6/cau-hinh.json ; sha256=4492649F20E183D21402BE8D04D408F05224D25724B0A0D42F33F7122F2B6F10

## 2026-11-11T18:41:56.1065498Z - obs

```sh
sudo -n docker run --name rca-tai-validate-01 --network none --mount type=bind,src=/opt/rca-tai,dst=/work,readonly -e FT_TEST_ENVIRONMENT=true grafana/k6:1.4.2@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 inspect /work/k6/workload-t062.js
```

Exit: 107

2026-11-11T18:42:05.8274178Z - tai : scp results/T-062/tai/fixture.py -> /opt/rca-tai/fixture.py ; sha256=8EFA3BA2FC9994EE34E4DA6173394027C52ED02E16FC1FAC4C00544BCDF37859

2026-11-11T18:42:10.2539352Z - tai : scp results/T-062/tai/k6/seed-orders.json -> /opt/rca-tai/k6/seed-orders.json ; sha256=ED49A7981EA70DBA90743E50563AE676EBA93673D05C17DFF4B865B0424ED381

2026-11-11T18:42:29.9587788Z - tai : scp results/T-062/tai/k6/workload-t062.js -> /opt/rca-tai/k6/workload-t062.js ; sha256=FBBFB55432951E178B058813D07D2F517D6FF79F29E9684BA008907610C0C534

2026-11-11T18:42:34.0892164Z - tai : scp results/T-062/tai/k6/cau-hinh.json -> /opt/rca-tai/k6/cau-hinh.json ; sha256=4492649F20E183D21402BE8D04D408F05224D25724B0A0D42F33F7122F2B6F10
`n2026-11-11T18:42:38.2278251Z - tai: fixture.py --machine tai reads API and writes /opt/rca-tai/k6/fixtures.json plus fixture-evidence.json only on successful completion. Invocations recorded in fixture-read*.txt; no order POST before A2.

2026-11-11T18:42:57.3795746Z - tai : scp results/T-062/tai/fixture.py -> /opt/rca-tai/fixture.py ; sha256=8E0DE35D3B15561C826CB454EF5760C2E610C41DF5A3E6EEEC69BEF147F56CC9

## 2026-11-11T18:43:01.9077157Z - tai

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /opt/rca-tai/fixture.py --machine tai
```

Exit: 0

## 2026-11-11T18:43:35.6877627Z - tai

```sh
sudo -n docker run --name rca-tai-verify-001 --user "$(id -u):$(id -g)" -v /opt/rca-tai/k6:/scripts:ro -v /opt/rca-tai/secret:/secret:ro grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 inspect --execution-requirements /scripts/workload-t062.js
```

Exit: 107

## 2026-11-11T18:44:24.9320267Z - tai

```sh
sudo -n docker run --name rca-tai-verify-002 --user "$(id -u):$(id -g)" -e FT_TEST_ENVIRONMENT=true -v /opt/rca-tai/k6:/scripts:ro -v /opt/rca-tai/secret:/secret:ro grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 inspect --execution-requirements /scripts/workload-t062.js
```

Exit: 107

## 2026-11-11T18:44:37.9129745Z - tai

```sh
sudo -n docker run --name rca-tai-verify-003 --user "$(id -u):$(id -g)" -v /opt/rca-tai/k6:/scripts:ro -v /opt/rca-tai/secret:/secret:ro grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 inspect -e FT_TEST_ENVIRONMENT=true --execution-requirements /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T18:45:13.6961494Z - tai

```sh
python3 - <<'PY'
import json, base64, urllib.request, urllib.parse
from pathlib import Path
p=Path('/opt/rca-tai/secret/tokens.json')
try:
    v=json.loads(p.read_text())
    body=urllib.parse.urlencode({'grant_type':'refresh_token','client_id':'frontend','refresh_token':v['refresh_token']}).encode()
    with urllib.request.urlopen('http://129.221.208.47:8080/realms/flash-ticket/protocol/openid-connect/token',data=body,timeout=15) as r:
        status=r.status; v=json.load(r)
    p.write_text(json.dumps(v)); p.chmod(0o600)
    claims=json.loads(base64.urlsafe_b64decode(v['access_token'].split('.')[1]+'=='))
    print(json.dumps({'status':status,'issuer':claims['iss'],'expires_in':v['expires_in'],'refresh_expires_in':v['refresh_expires_in']}))
except Exception as e:
    print(json.dumps({'error_type':type(e).__name__,'detail':'no secret emitted'})); raise SystemExit(1)
PY
```

Exit: 0

## 2026-11-11T18:57:09.3066495Z - tai

```sh
set -eu; ids=$(sudo -n docker ps -q --filter 'name=^rca-tai-'); if [ -n "$ids" ]; then sudo -n docker stop --time 45 $ids; fi
```

Exit: 0

2026-11-11T18:59:51.9319847Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T18:59:54.7141355Z - tai

```sh
PYTHONDONTWRITEBYTECODE=1 python3 /opt/rca-tai/fixture.py --machine tai --create-if-empty
```

Exit: 0

2026-11-11T19:00:15.4540569Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T19:00:18.0629996Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/d20261111190011
mkdir out/d20261111190011
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/d20261111190011/
date -u --iso-8601=seconds > out/d20261111190011/start-utc.txt
printf '{"machine":"tai","seconds":300,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/d20261111190011/run.json
sha256sum out/d20261111190011/workload-t062.js out/d20261111190011/cau-hinh.json out/d20261111190011/fixtures.json > out/d20261111190011/inputs.sha256
sudo -n docker run -d --name rca-tai-d20261111190011 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/d20261111190011:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/d20261111190011:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=300 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T19:05:40.5948304Z - tai

```sh
sudo -n docker logs rca-tai-d20261111190011 > /opt/rca-tai/out/d20261111190011/container.log 2>&1; sudo -n docker inspect rca-tai-d20261111190011 --format '{{json .State}}' > /opt/rca-tai/out/d20261111190011/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/d20261111190011/received-utc.txt; cd /opt/rca-tai/out/d20261111190011; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T19:21:58.8914270Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T19:22:01.4692434Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/d2-93651d4c
mkdir out/d2-93651d4c
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/d2-93651d4c/
date -u --iso-8601=seconds > out/d2-93651d4c/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/d2-93651d4c/run.json
sha256sum out/d2-93651d4c/workload-t062.js out/d2-93651d4c/cau-hinh.json out/d2-93651d4c/fixtures.json > out/d2-93651d4c/inputs.sha256
sudo -n docker run -d --name rca-tai-d2-93651d4c --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/d2-93651d4c:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/d2-93651d4c:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T19:46:48.6965232Z - tai

```sh
set -eu; ids=$(sudo -n docker ps -q --filter 'name=^rca-tai-d2-93651d4c$'); if [ -n "$ids" ]; then sudo -n docker stop --time 45 $ids; fi
```

Exit: 0

## 2026-11-11T19:47:46.5436221Z - tai

```sh
sudo -n docker logs rca-tai-d2-93651d4c > /opt/rca-tai/out/d2-93651d4c/container.log 2>&1; sudo -n docker inspect rca-tai-d2-93651d4c --format '{{json .State}}' > /opt/rca-tai/out/d2-93651d4c/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/d2-93651d4c/received-utc.txt; cd /opt/rca-tai/out/d2-93651d4c; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T19:49:06.4105853Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T19:49:08.9691537Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/d2-2e071903
mkdir out/d2-2e071903
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/d2-2e071903/
date -u --iso-8601=seconds > out/d2-2e071903/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/d2-2e071903/run.json
sha256sum out/d2-2e071903/workload-t062.js out/d2-2e071903/cau-hinh.json out/d2-2e071903/fixtures.json > out/d2-2e071903/inputs.sha256
sudo -n docker run -d --name rca-tai-d2-2e071903 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/d2-2e071903:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/d2-2e071903:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

2026-11-11T19:50:18.2752944Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T19:50:20.9261429Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T19:50:23.3391505Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/d2-a2a95419
mkdir out/d2-a2a95419
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/d2-a2a95419/
date -u --iso-8601=seconds > out/d2-a2a95419/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/d2-a2a95419/run.json
sha256sum out/d2-a2a95419/workload-t062.js out/d2-a2a95419/cau-hinh.json out/d2-a2a95419/fixtures.json > out/d2-a2a95419/inputs.sha256
sudo -n docker run -d --name rca-tai-d2-a2a95419 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/d2-a2a95419:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/d2-a2a95419:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T20:15:32.9591528Z - tai

```sh
set -eu; ids=$(sudo -n docker ps -q --filter 'name=^rca-tai-d2-a2a95419$'); if [ -n "$ids" ]; then sudo -n docker stop --time 45 $ids; fi
```

Exit: 0

## 2026-11-11T20:16:31.1460730Z - tai

```sh
sudo -n docker logs rca-tai-d2-a2a95419 > /opt/rca-tai/out/d2-a2a95419/container.log 2>&1; sudo -n docker inspect rca-tai-d2-a2a95419 --format '{{json .State}}' > /opt/rca-tai/out/d2-a2a95419/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/d2-a2a95419/received-utc.txt; cd /opt/rca-tai/out/d2-a2a95419; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T20:17:36.6048217Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T20:17:39.2373450Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T20:17:41.7037362Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/d2-39831c56
mkdir out/d2-39831c56
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/d2-39831c56/
date -u --iso-8601=seconds > out/d2-39831c56/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/d2-39831c56/run.json
sha256sum out/d2-39831c56/workload-t062.js out/d2-39831c56/cau-hinh.json out/d2-39831c56/fixtures.json > out/d2-39831c56/inputs.sha256
sudo -n docker run -d --name rca-tai-d2-39831c56 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/d2-39831c56:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/d2-39831c56:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T20:23:55.6112482Z - tai

```sh
set -eu; ids=$(sudo -n docker ps -q --filter 'name=^rca-tai-d2-39831c56$'); if [ -n "$ids" ]; then sudo -n docker stop --time 45 $ids; fi
```

Exit: 0

## 2026-11-11T20:24:53.7733624Z - tai

```sh
sudo -n docker logs rca-tai-d2-39831c56 > /opt/rca-tai/out/d2-39831c56/container.log 2>&1; sudo -n docker inspect rca-tai-d2-39831c56 --format '{{json .State}}' > /opt/rca-tai/out/d2-39831c56/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/d2-39831c56/received-utc.txt; cd /opt/rca-tai/out/d2-39831c56; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T20:25:44.4577222Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T20:25:47.1159879Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T20:25:49.4677300Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-e610fd62
mkdir out/e1-e610fd62
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-e610fd62/
date -u --iso-8601=seconds > out/e1-e610fd62/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-e610fd62/run.json
sha256sum out/e1-e610fd62/workload-t062.js out/e1-e610fd62/cau-hinh.json out/e1-e610fd62/fixtures.json > out/e1-e610fd62/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-e610fd62 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-e610fd62:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-e610fd62:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T20:37:48.0460618Z - tai

```sh
set -eu; ids=$(sudo -n docker ps -q --filter 'name=^rca-tai-e1-e610fd62$'); if [ -n "$ids" ]; then sudo -n docker stop --time 45 $ids; fi
```

Exit: 0

## 2026-11-11T20:38:58.8630500Z - tai

```sh
sudo -n docker logs rca-tai-e1-e610fd62 > /opt/rca-tai/out/e1-e610fd62/container.log 2>&1; sudo -n docker inspect rca-tai-e1-e610fd62 --format '{{json .State}}' > /opt/rca-tai/out/e1-e610fd62/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-e610fd62/received-utc.txt; cd /opt/rca-tai/out/e1-e610fd62; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T20:39:33.6414071Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T20:39:36.2043542Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T20:39:38.5939679Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-a5539fba
mkdir out/e1-a5539fba
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-a5539fba/
date -u --iso-8601=seconds > out/e1-a5539fba/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-a5539fba/run.json
sha256sum out/e1-a5539fba/workload-t062.js out/e1-a5539fba/cau-hinh.json out/e1-a5539fba/fixtures.json > out/e1-a5539fba/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-a5539fba --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-a5539fba:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-a5539fba:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T21:10:14.6870742Z - tai

```sh
sudo -n docker logs rca-tai-e1-a5539fba > /opt/rca-tai/out/e1-a5539fba/container.log 2>&1; sudo -n docker inspect rca-tai-e1-a5539fba --format '{{json .State}}' > /opt/rca-tai/out/e1-a5539fba/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-a5539fba/received-utc.txt; cd /opt/rca-tai/out/e1-a5539fba; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T21:10:42.5750938Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T21:10:45.1968914Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T21:10:47.6153250Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-1ad3afeb
mkdir out/e1-1ad3afeb
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-1ad3afeb/
date -u --iso-8601=seconds > out/e1-1ad3afeb/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-1ad3afeb/run.json
sha256sum out/e1-1ad3afeb/workload-t062.js out/e1-1ad3afeb/cau-hinh.json out/e1-1ad3afeb/fixtures.json > out/e1-1ad3afeb/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-1ad3afeb --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-1ad3afeb:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-1ad3afeb:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T21:41:24.7125130Z - tai

```sh
sudo -n docker logs rca-tai-e1-1ad3afeb > /opt/rca-tai/out/e1-1ad3afeb/container.log 2>&1; sudo -n docker inspect rca-tai-e1-1ad3afeb --format '{{json .State}}' > /opt/rca-tai/out/e1-1ad3afeb/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-1ad3afeb/received-utc.txt; cd /opt/rca-tai/out/e1-1ad3afeb; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T21:41:52.6757904Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T21:41:55.2110534Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T21:41:57.5746270Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-a89954d1
mkdir out/e1-a89954d1
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-a89954d1/
date -u --iso-8601=seconds > out/e1-a89954d1/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-a89954d1/run.json
sha256sum out/e1-a89954d1/workload-t062.js out/e1-a89954d1/cau-hinh.json out/e1-a89954d1/fixtures.json > out/e1-a89954d1/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-a89954d1 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-a89954d1:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-a89954d1:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T22:12:33.5510539Z - tai

```sh
sudo -n docker logs rca-tai-e1-a89954d1 > /opt/rca-tai/out/e1-a89954d1/container.log 2>&1; sudo -n docker inspect rca-tai-e1-a89954d1 --format '{{json .State}}' > /opt/rca-tai/out/e1-a89954d1/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-a89954d1/received-utc.txt; cd /opt/rca-tai/out/e1-a89954d1; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T22:13:01.1655212Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T22:13:03.7166757Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T22:13:06.1062511Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-2e2a5541
mkdir out/e1-2e2a5541
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-2e2a5541/
date -u --iso-8601=seconds > out/e1-2e2a5541/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-2e2a5541/run.json
sha256sum out/e1-2e2a5541/workload-t062.js out/e1-2e2a5541/cau-hinh.json out/e1-2e2a5541/fixtures.json > out/e1-2e2a5541/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-2e2a5541 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-2e2a5541:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-2e2a5541:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T22:43:42.9330701Z - tai

```sh
sudo -n docker logs rca-tai-e1-2e2a5541 > /opt/rca-tai/out/e1-2e2a5541/container.log 2>&1; sudo -n docker inspect rca-tai-e1-2e2a5541 --format '{{json .State}}' > /opt/rca-tai/out/e1-2e2a5541/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-2e2a5541/received-utc.txt; cd /opt/rca-tai/out/e1-2e2a5541; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T22:44:12.3982729Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T22:44:14.9598418Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T22:44:17.2687378Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-6c1a9fd8
mkdir out/e1-6c1a9fd8
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-6c1a9fd8/
date -u --iso-8601=seconds > out/e1-6c1a9fd8/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-6c1a9fd8/run.json
sha256sum out/e1-6c1a9fd8/workload-t062.js out/e1-6c1a9fd8/cau-hinh.json out/e1-6c1a9fd8/fixtures.json > out/e1-6c1a9fd8/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-6c1a9fd8 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-6c1a9fd8:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-6c1a9fd8:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T23:14:53.2913415Z - tai

```sh
sudo -n docker logs rca-tai-e1-6c1a9fd8 > /opt/rca-tai/out/e1-6c1a9fd8/container.log 2>&1; sudo -n docker inspect rca-tai-e1-6c1a9fd8 --format '{{json .State}}' > /opt/rca-tai/out/e1-6c1a9fd8/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-6c1a9fd8/received-utc.txt; cd /opt/rca-tai/out/e1-6c1a9fd8; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T23:15:22.0882081Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T23:15:24.7270700Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T23:15:27.1055691Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-f728fce2
mkdir out/e1-f728fce2
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-f728fce2/
date -u --iso-8601=seconds > out/e1-f728fce2/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-f728fce2/run.json
sha256sum out/e1-f728fce2/workload-t062.js out/e1-f728fce2/cau-hinh.json out/e1-f728fce2/fixtures.json > out/e1-f728fce2/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-f728fce2 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-f728fce2:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-f728fce2:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-11T23:46:03.5889511Z - tai

```sh
sudo -n docker logs rca-tai-e1-f728fce2 > /opt/rca-tai/out/e1-f728fce2/container.log 2>&1; sudo -n docker inspect rca-tai-e1-f728fce2 --format '{{json .State}}' > /opt/rca-tai/out/e1-f728fce2/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-f728fce2/received-utc.txt; cd /opt/rca-tai/out/e1-f728fce2; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-11T23:46:32.2543812Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-11T23:46:34.8357892Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-11T23:46:37.2658654Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-bf17acbf
mkdir out/e1-bf17acbf
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-bf17acbf/
date -u --iso-8601=seconds > out/e1-bf17acbf/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-bf17acbf/run.json
sha256sum out/e1-bf17acbf/workload-t062.js out/e1-bf17acbf/cau-hinh.json out/e1-bf17acbf/fixtures.json > out/e1-bf17acbf/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-bf17acbf --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-bf17acbf:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-bf17acbf:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-12T00:17:13.2850481Z - tai

```sh
sudo -n docker logs rca-tai-e1-bf17acbf > /opt/rca-tai/out/e1-bf17acbf/container.log 2>&1; sudo -n docker inspect rca-tai-e1-bf17acbf --format '{{json .State}}' > /opt/rca-tai/out/e1-bf17acbf/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-bf17acbf/received-utc.txt; cd /opt/rca-tai/out/e1-bf17acbf; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

## 2026-11-12T00:17:38.2647429Z - tai

```sh
mkdir -p /opt/rca-tai/k6-e1
```

Exit: 0

2026-11-12T00:17:40.7344772Z - tai : scp D:\RCA-flashticket\results\T-062\chay/k6/workload-t062-flash.js -> /opt/rca-tai/k6-e1/workload-t062-flash.js ; sha256=BB4FA737A3C790D863C0E0C431204773037CED9459D0B861B29BD9CA80B6D255

2026-11-12T00:17:49.0465005Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-12T00:17:51.7625453Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-12T00:17:54.0716768Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-00eaea92
mkdir out/e1-00eaea92
cp k6-e1/workload-t062-flash.js out/e1-00eaea92/workload-t062.js
cp k6/cau-hinh.json k6/fixtures.json out/e1-00eaea92/
date -u --iso-8601=seconds > out/e1-00eaea92/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"flash_rate":15,"workload":"flash","image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-00eaea92/run.json
sha256sum out/e1-00eaea92/workload-t062.js out/e1-00eaea92/cau-hinh.json out/e1-00eaea92/fixtures.json > out/e1-00eaea92/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-00eaea92 --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-00eaea92:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-00eaea92:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 -e FT_FLASH_RATE=15 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-12T00:48:30.5072039Z - tai

```sh
sudo -n docker logs rca-tai-e1-00eaea92 > /opt/rca-tai/out/e1-00eaea92/container.log 2>&1; sudo -n docker inspect rca-tai-e1-00eaea92 --format '{{json .State}}' > /opt/rca-tai/out/e1-00eaea92/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-00eaea92/received-utc.txt; cd /opt/rca-tai/out/e1-00eaea92; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0

2026-11-12T00:49:00.3626078Z - tai : PKCE memory pipe -> umask 077; cat > /opt/rca-tai/secret/tokens.json (values omitted)

## 2026-11-12T00:49:02.9458448Z - tai

```sh
sed -i '1s/^\xEF\xBB\xBF//' /opt/rca-tai/secret/tokens.json; test "$(head -c1 /opt/rca-tai/secret/tokens.json)" = '{'
```

Exit: 0

## 2026-11-12T00:49:05.3878154Z - tai

```sh
set -euo pipefail
cd /opt/rca-tai
test ! -e out/e1-e8661e0a
mkdir out/e1-e8661e0a
cp k6/workload-t062.js k6/cau-hinh.json k6/fixtures.json out/e1-e8661e0a/
date -u --iso-8601=seconds > out/e1-e8661e0a/start-utc.txt
printf '{"machine":"tai","seconds":1800,"rate":5,"image":"grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7"}\n' > out/e1-e8661e0a/run.json
sha256sum out/e1-e8661e0a/workload-t062.js out/e1-e8661e0a/cau-hinh.json out/e1-e8661e0a/fixtures.json > out/e1-e8661e0a/inputs.sha256
sudo -n docker run -d --name rca-tai-e1-e8661e0a --user "$(id -u):$(id -g)" --network host \
  -v /opt/rca-tai/out/e1-e8661e0a:/scripts:ro -v /opt/rca-tai/secret:/secret:ro -v /opt/rca-tai/out/e1-e8661e0a:/out \
  -e FT_TEST_ENVIRONMENT=true -e FT_MACHINE=tai -e FT_LOAD_SECONDS=1800 -e FT_LOAD_RATE=5 \
  grafana/k6@sha256:3656673de3f30424e8ebcfa46acd9558d83b6a43612d0f668ffeac953950c6c7 run --quiet --out json=/out/raw.json --summary-export /out/summary.json /scripts/workload-t062.js
```

Exit: 0

## 2026-11-12T01:19:41.6282017Z - tai

```sh
sudo -n docker logs rca-tai-e1-e8661e0a > /opt/rca-tai/out/e1-e8661e0a/container.log 2>&1; sudo -n docker inspect rca-tai-e1-e8661e0a --format '{{json .State}}' > /opt/rca-tai/out/e1-e8661e0a/state.json; date -u --iso-8601=seconds > /opt/rca-tai/out/e1-e8661e0a/received-utc.txt; cd /opt/rca-tai/out/e1-e8661e0a; sha256sum *.json *.js *.log *.txt inputs.sha256 > outputs.sha256
```

Exit: 0
