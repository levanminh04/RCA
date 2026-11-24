set +e
echo "### compose_env_labels"; for c in $(docker ps -aq); do docker inspect --format '{{.Name}}	envfile={{index .Config.Labels "com.docker.compose.project.environment_file"}}	img={{.Config.Image}}	created={{.Created}}' $c; done
echo "### vnpay_procs"; for p in $(pgrep -f 'l1-vnpay|tunnel-supervisor|mock-runner'); do echo "--- $p cwd=$(readlink /proc/$p/cwd) ppid=$(ps -o ppid= -p $p)"; tr '\0' ' ' < /proc/$p/cmdline | sed -E 's/(-i )[^ ]+/\1<key-path>/' | cut -c1-400; echo; done
echo "### opt_app_tree"; find /opt/flash-ticket-app /opt/flash-ticket-infra /opt/docs /opt/flash-ticket-build/t067-compose /opt/flash-ticket-build/t067-36a3725d-logs -maxdepth 3 -not -path '*/collector/data/*' -not -path '*/otel/*' -printf '%M %u:%g %s %TY-%Tm-%TdT%TH:%TM %p\n' 2>&1 | sort -k5 | head -400
echo "### collector_data_old"; ls -la /opt/flash-ticket-app/collector/data 2>&1 | head; ls /opt/flash-ticket-app/collector/data 2>/dev/null | wc -l
echo "### compose_path_refs"; for f in /opt/flash-ticket-build/t067-compose/hieu-luc/*.yml /opt/flash-ticket-app/compose-exp/*.yml /opt/rca-lab/observability/collector/agent-compose.yaml; do echo "--- $f"; grep -nE '(^|\s)(- )?(\.|/)[A-Za-z0-9_./-]+|env_file|image:|cpus|mem_limit|container_name' $f 2>&1 | grep -viE 'password|secret=|token' | head -40; done
echo "### toxiproxy_inspect"; docker inspect --format 'labels={{json .Config.Labels}} cmd={{json .Config.Cmd}}' rca-toxiproxy
echo "### rca_faults_stat"; stat -c '%A %U:%G %n' /opt/flash-ticket-app/rca-faults /opt/flash-ticket-app/rca-faults/* 2>&1; sudo -n -l 2>&1 | head -20
