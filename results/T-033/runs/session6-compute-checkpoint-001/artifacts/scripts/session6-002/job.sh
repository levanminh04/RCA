#!/bin/bash
set -u
B=/home/ubuntu/rca/T-033
cd "$B" || exit 1
run="$1"
config="$2"
config_sha="$3"
ledger="$4"
ledger_sha="$5"
pins_sha="$6"
if [ -e "runs/$run" ] || [ -e "runs/$run--control" ] || [ -e "runs/$run.shell.pid" ]; then exit 2; fi
export T033_HOME="$B" PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8
export TMPDIR="$B/tmp" XDG_CACHE_HOME="$B/cache" MPLCONFIGDIR="$B/cache/mpl"
export PYTHONPATH=/home/ubuntu/rca/T-025/src/baro:/home/ubuntu/rca/T-025/repo/src
export T033_PROCESSING_LEDGER_PATH="$ledger" T033_PROCESSING_LEDGER_SHA256="$ledger_sha" T033_PINS_SHA256="$pins_sha"
export T033_ACTIVE_PROCESS_STARTED_UTC="$(date -u +%Y-%m-%dT%H:%M:%S.%NZ)"
start_ns="$(date +%s%N)"
printf '%s\n' "$$" > "runs/$run.shell.pid"
/home/ubuntu/rca/T-025/envs/main/bin/python -B -X utf8 scripts/session6-002/accounted_worker.py --config "$config" --config-sha256 "$config_sha" > "runs/$run.out" 2> "runs/$run.err"
rc=$?
end_ns="$(date +%s%N)"
printf '{"start_ns":%s,"end_ns":%s,"exit_code":%s,"scope":"shell before Python import through Python exit"}\n' "$start_ns" "$end_ns" "$rc" > "runs/$run.processing-timer.json"
printf '%s\n' "$rc" > "runs/$run.exit"
exit "$rc"
