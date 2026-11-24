set +e
echo "### date"; date -u +%FT%TZ; id; sudo -n true 2>&1 && echo SUDO_NOPASS_OK
echo "### df"; df -h -x tmpfs -x squashfs -x overlay
echo "### stat"; for d in /opt /opt/* /srv /srv/* /etc/rca-lab /home/ubuntu /var/lib/flash-ticket-ledger /var/lib/docker; do stat -c '%A %U:%G %n' "$d" 2>&1; done
echo "### du_top"; du -xsh /opt/* /srv/* /etc/rca-lab /var/lib/flash-ticket-ledger 2>&1
echo "### du_home"; cd /home/ubuntu && du -xsh -- * .[!.]* 2>&1 | grep -v -e '\.ssh$' -e bash_history
echo "### docker_ps"; docker ps -a --format '{{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Label "com.docker.compose.project"}}\t{{.Label "com.docker.compose.project.working_dir"}}\t{{.Label "com.docker.compose.project.config_files"}}\t{{.Label "com.docker.compose.service"}}' 2>&1
echo "### docker_compose_ls"; docker compose ls -a 2>&1
echo "### docker_mounts"; for c in $(docker ps -aq 2>/dev/null); do docker inspect --format '{{.Name}}	restart={{.HostConfig.RestartPolicy.Name}}	net={{.HostConfig.NetworkMode}}{{range .Mounts}}	{{.Type}}:{{.Source}}->{{.Destination}}:rw={{.RW}}{{end}}' $c; done
echo "### docker_ports"; docker ps -a --format '{{.Names}}\t{{.Ports}}'
echo "### docker_volumes"; docker volume ls 2>&1
echo "### docker_system_df"; docker system df 2>&1
echo "### docker_images"; docker images --format '{{.Repository}}:{{.Tag}}\t{{.ID}}\t{{.Size}}\t{{.CreatedSince}}' 2>&1
