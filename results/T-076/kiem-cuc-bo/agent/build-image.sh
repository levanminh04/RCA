#!/usr/bin/env bash
# T-076 bước 4: build image thử từ Dockerfile của nhánh PR. Mạng laptop chặn tải asset GitHub Releases, nên dòng
# `ADD --checksum=... https://github.com/...` được thay bằng COPY từ jar cùng phiên bản lấy ở Maven Central đã kiểm
# đúng SHA-256 ghim trong Dockerfile. Mọi dòng khác giữ nguyên. CI trên GitHub chạy đúng dòng ADD gốc.
#   bash build-image.sh <worktree> <thư mục service> <tên service> <thư mục chứa otel.jar>
set -euo pipefail
export MSYS_NO_PATHCONV=1
W=${1:?}; DIR=${2:?}; SVC=${3:?}; JAR=${4:?}
SHA=$(git -C "$W" rev-parse HEAD)
PIN=$(grep -o 'checksum=sha256:[0-9a-f]*' "$W/$DIR/Dockerfile" | cut -d: -f2)
[ "$(sha256sum "$JAR/otel.jar" | cut -c1-64)" = "$PIN" ] || { echo "otel.jar khác checksum ghim"; exit 1; }
TMP=$(mktemp -p "$JAR" Dockerfile.XXXX)  # đường Windows để docker đọc được (không dùng /tmp của Git Bash)
sed -E 's#^ADD --checksum=sha256:[0-9a-f]+ --chmod=0444 https://github.com/[^ ]+ /otel/opentelemetry-javaagent.jar$#COPY --from=agentjar --chmod=0444 otel.jar /otel/opentelemetry-javaagent.jar#' \
  "$W/$DIR/Dockerfile" > "$TMP"
[ "$(diff "$W/$DIR/Dockerfile" "$TMP" | grep -c '^[<>]')" = 2 ] || { echo "thay dòng ADD không đúng 1 dòng"; exit 1; }
docker buildx build --load --build-context agentjar="$JAR" -f "$TMP" --build-arg SERVICE_VERSION="$SHA" \
  -t "pr17-thu/$SVC:$SHA" "$W/$DIR"
rm -f "$TMP"
docker image inspect "pr17-thu/$SVC:$SHA" --format '{{.Id}} {{.Size}}'
