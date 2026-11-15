#!/usr/bin/env bash
set -Eeuo pipefail
python3 /home/ubuntu/t058/prepare-pinned-obs.py
compose=(docker compose -f /opt/flash-ticket-obs/pinned/compose.json -p flash-ticket-obs-pinned)
"${compose[@]}" config --quiet
"${compose[@]}" pull
"${compose[@]}" run --rm --no-deps collector validate --config=/etc/otel/config.json
docker stop flash-ticket-lgtm
"${compose[@]}" up -d
date -u
touch /home/ubuntu/t058/pinned.started
