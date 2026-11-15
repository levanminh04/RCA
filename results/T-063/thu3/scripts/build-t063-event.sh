#!/usr/bin/env bash
# T-063 thu3: build lại RIÊNG event-service trên exp-app từ nền 6b21ed55 + bản vá hook H3 (h3-pool-event.patch).
# Dùng (exp-app): nohup bash ~/t063/thu3/build-t063-event.sh > ~/t063/thu3/build.out 2>&1 < /dev/null &
# Không đổi image/container nào (chỉ tạo image mới). Triển khai là bước riêng (deploy-t063-event.sh).
set -Eeuo pipefail
BASE=6b21ed55ecfef2217a90d23b560e44af2d425b36
R=/home/ubuntu/t063/thu3; P=$R/h3-pool-event.patch
T=/opt/flash-ticket-build/t063-h3
export MAVEN_OPTS='-Xmx768m -Djava.awt.headless=true' DOCKER_BUILDKIT=1
echo "$(date -u +%FT%TZ) START patch_sha256=$(sha256sum $P | cut -d' ' -f1)"
[ -d "$T" ] || git -C /opt/flash-ticket-src worktree add --detach "$T" "$BASE"
if [ "$(git -C $T rev-parse HEAD)" = "$BASE" ]; then
  git -C $T apply --check $P
  git -C $T apply $P
  # bản vá chỉ được chạm src/rca-test của event-service
  git -C $T status --porcelain | awk '{print $2}' | grep -v '^services/event-service/src/rca-test/' && { echo "DUNG: bản vá chạm ngoài src/rca-test"; exit 3; }
  git -C $T -c user.name=rca-t063 -c user.email=rca-t063@localhost add services/event-service/src/rca-test
  git -C $T -c user.name=rca-t063 -c user.email=rca-t063@localhost commit -q -m "T-063 thu3: hook pool.hold chạy ở event-service (vá trên 6b21ed55; nguồn nhánh rca/quan-sat-log e557307)"
fi
[ "$(git -C $T rev-parse HEAD~1)" = "$BASE" ] || { echo "DUNG: worktree không ở BASE+1"; exit 4; }
FULL=$(git -C $T rev-parse HEAD); echo "commit=$FULL parent=$BASE"
git -C $T diff --stat $BASE HEAD
cd $T/services/event-service
echo "$(date -u +%FT%TZ) TEST RcaFaults*"
bash ./mvnw -B -ntp -P rca-test -Dtest='RcaFaults*' -Dsurefire.failIfNoSpecifiedTests=false test > $R/event-test.log 2>&1 || { echo "DUNG: test lỗi"; tail -40 $R/event-test.log; exit 5; }
grep -E "Tests run:.*Fail" $R/event-test.log | tail -3
echo "$(date -u +%FT%TZ) PACKAGE"
bash ./mvnw -B -ntp clean -P rca-test -DskipTests package > $R/event-build.log 2>&1
IMG=ft-local/event-service:arm64-t063h3-${FULL:0:8}
docker build --build-arg SERVICE_VERSION=$FULL --label org.opencontainers.image.revision=$FULL \
  --label t062.maven-profile="-P rca-test" --label t063.base=$BASE -t $IMG . >> $R/event-build.log 2>&1
JAR=$(ls target/event-service-*.jar | grep -v plain | head -1)
python3 - "$JAR" <<'PY' > $R/jar-kiem.txt
import sys, zipfile
z = zipfile.ZipFile(sys.argv[1]); n = [x for x in z.namelist() if 'RcaFaults' in x]
print('rca_faults_entries', len(n), n)
PY
cat $R/jar-kiem.txt
echo "$(date -u +%FT%TZ) DONE image=$IMG id=$(docker image inspect $IMG --format '{{.Id}} {{.Architecture}}') jar_sha256=$(sha256sum $JAR | cut -d' ' -f1)"
date -u +%FT%TZ > $R/build.done
