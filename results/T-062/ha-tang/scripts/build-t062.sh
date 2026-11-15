#!/usr/bin/env bash
# T-062 A2: build 7 service Spring từ nhánh rca/quan-sat-log trên exp-app (ARM). Chạy: nohup bash build-t062.sh <sha> &
set -Eeuo pipefail
SHA=${1:?sha}
export MAVEN_OPTS='-Xmx768m -Djava.awt.headless=true' DOCKER_BUILDKIT=1
R=/home/ubuntu/t062; mkdir -p $R
T=/opt/flash-ticket-build/t062-${SHA:0:8}
git -C /opt/flash-ticket-src fetch -q origin rca/quan-sat-log
[ -d "$T" ] || git -C /opt/flash-ticket-src worktree add --detach "$T" "$SHA"
[ "$(git -C $T rev-parse HEAD)" = "$(git -C /opt/flash-ticket-src rev-parse $SHA)" ]
FULL=$(git -C $T rev-parse HEAD)
echo "[]" > $R/build-manifest.json
for svc in discovery-server api-gateway user-service event-service ticket-service booking-service payment-service; do
  case $svc in discovery-server|api-gateway) p=infrastructure/$svc;; *) p=services/$svc;; esac
  prof=""; [ "$svc" = booking-service -o "$svc" = event-service ] && prof="-P rca-test"
  img=ft-local/$svc:arm64-t062-${FULL:0:8}
  s=$(date -u +%FT%TZ); echo "$s $svc START $prof"
  ( cd $T/$p && bash ./mvnw -B -ntp clean $prof -DskipTests package ) > $R/$svc-build.log 2>&1
  m=$?
  ( cd $T/$p && docker build --build-arg SERVICE_VERSION=$FULL --label org.opencontainers.image.revision=$FULL --label t062.maven-profile="${prof:-none}" -t $img . ) >> $R/$svc-build.log 2>&1
  id=$(docker image inspect $img --format '{{.Id}} {{.Architecture}}')
  hook=$(unzip -l $T/$p/target/$svc-*.jar 2>/dev/null | grep -c RcaFaults || true)
  e=$(date -u +%FT%TZ); echo "$e $svc DONE $id rcaFaultsClasses=$hook"
  python3 - "$R/build-manifest.json" "$svc" "$FULL" "$img" "$id" "$prof" "$s" "$e" "$hook" <<'PY'
import json,sys
f,svc,full,img,idarch,prof,s,e,hook=sys.argv[1:]
d=json.load(open(f)); i,a=idarch.split()
d.append(dict(service=svc,commit=full,image=img,image_id=i,architecture=a,maven_profile=prof or None,tests='skipped (CI chạy trên PR)',started_at=s,finished_at=e,rca_faults_classes_in_jar=int(hook)))
json.dump(d,open(f,'w'),indent=2)
PY
done
date -u +%FT%TZ > $R/build.done
