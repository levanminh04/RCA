echo "### compose_labels"; for c in $(docker ps -aq); do docker inspect --format '{{.Name}}	envfile={{index .Config.Labels "com.docker.compose.project.environment_file"}}	created={{.Created}}	img={{.Config.Image}}' $c; done
echo "### runs_t072_e3_01_names"; ls -la /srv/rca-lab/runs/t072-e3-01 /srv/rca-lab/runs/t072-e3-01-cfg 2>&1 | head -40
echo "### rca_results_top"; ls -la /srv/rca-lab/rca-results /srv/rca-lab/rca-results/chi-muc /srv/rca-lab/rca-results/t065-l11-001 2>&1 | head -60
echo "### capture_count_by_kind"; ls /srv/rca-lab/collector-gateway/capture | sed -E 's/-20.*//' | sort | uniq -c
echo "### trace_goi_files"; ls -la /srv/rca-lab/trace-goi | head; 
echo "### ss"; ss -tlnp 2>/dev/null | head -30
echo "### python_yaml"; python3 -c 'import yaml;print(yaml.__version__)' 2>&1
