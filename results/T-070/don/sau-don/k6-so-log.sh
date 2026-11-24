trung=0; khac=0; khong=0
for c in $(sudo -n docker ps -a --filter name=rca-tai- --filter status=exited --format '{{.Names}}'); do
  src=$(sudo -n docker inspect $c --format '{{range .Mounts}}{{if eq .Destination "/out"}}{{.Source}}{{end}}{{end}}')
  f=$(echo "$src" | sed 's#^/srv/rca-lab/load-runs#/srv/flashticket-rca/archive/2026-11/load-runs#')
  if [ -z "$src" ] || [ ! -f "$f/container.log" ]; then echo "NGOAI_LE $c src=$src"; khong=$((khong+1)); continue; fi
  a=$(sha256sum < "$f/container.log" | cut -c1-64); b=$(sudo -n docker logs $c 2>&1 | sha256sum | cut -c1-64)
  if [ "$a" = "$b" ]; then trung=$((trung+1)); else echo "KHAC $c $f"; khac=$((khac+1)); fi
done
echo "trung=$trung khac=$khac ngoai_le=$khong"
sudo -n docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}'
