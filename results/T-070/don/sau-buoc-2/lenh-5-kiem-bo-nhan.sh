sudo -n docker exec flash-ticket-obs-grafana sh -c 'grafana server -v 2>/dev/null | head -1; (echo > /dev/tcp/t072-bo-nhan/9172) 2>/dev/null && echo tcp_ok || (nc -z -w3 t072-bo-nhan 9172 && echo tcp_ok_nc) || echo tcp_loi'
sudo -n docker inspect flash-ticket-t072-bo-nhan --format '{{.State.Health.Status}} {{.Config.User}} {{range .Mounts}}{{.Source}}->{{.Destination}} rw={{.RW}};{{end}}'
sudo -n -u ubuntu test -w /srv/flashticket-rca/alerts/bo-nhan && echo ubuntu_ghi_duoc
sudo -n docker logs --since 10m flash-ticket-obs-grafana 2>&1 | grep -ciE "level=error" 
sudo -n docker logs --since 10m flash-ticket-obs-grafana 2>&1 | grep -iE "level=error" | head -5 | cut -c1-250
