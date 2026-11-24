echo "### ss"; ss -tln 2>/dev/null | head -30
echo "### opt_rca_tai_l1"; ls -la /opt/rca-tai /opt/rca-tai/k6 /opt/rca-tai/k6-e1 2>&1
echo "### home"; ls -la /home/ubuntu 2>&1 | grep -v -E 'bash_history|\.ssh'
echo "### docker_bin"; command -v docker k6 2>&1; systemctl is-active docker
echo "### load_runs_sample"; ls -la /srv/rca-lab/load-runs/t073-e5-01-x1 2>&1 | head -30
