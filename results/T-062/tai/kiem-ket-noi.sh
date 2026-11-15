date -u --iso-8601=seconds
for port in 8081 8080; do
  printf 'curl --connect-timeout 3 --max-time 6 http://129.221.208.47:%s\n' "$port"
  curl --connect-timeout 3 --max-time 6 -sS -o /dev/null -w 'HTTP %{http_code}; total %{time_total}s\n' "http://129.221.208.47:$port"
  printf 'exit=%s\n' "$?"
done
