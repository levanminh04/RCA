xoa=0; giu=0
for c in $(sudo -n docker ps -a --filter name=rca-tai- --filter status=exited --format '{{.Names}}'); do
  src=$(sudo -n docker inspect $c --format '{{range .Mounts}}{{if eq .Destination "/out"}}{{.Source}}{{end}}{{end}}')
  f=$(echo "$src" | sed 's#^/srv/rca-lab/load-runs#/srv/flashticket-rca/archive/2026-11/load-runs#')
  if [ -n "$src" ] && [ -f "$f/container.log" ] && [ "$(sha256sum < "$f/container.log" | cut -c1-64)" = "$(sudo -n docker logs $c 2>&1 | sha256sum | cut -c1-64)" ]; then
    sudo -n docker rm $c >/dev/null && xoa=$((xoa+1))
  else echo "GIU $c"; giu=$((giu+1)); fi
done
echo "da_xoa=$xoa giu=$giu"
sudo -n docker ps -a --format '{{.Names}} {{.Status}}'
