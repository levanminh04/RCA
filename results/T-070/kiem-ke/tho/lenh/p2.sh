set +e
echo "### du_srv2"; du -xh --max-depth=2 /srv/rca-lab 2>&1 | sort -k2
echo "### du_opt2"; for d in /opt/rca-lab /opt/rca-tai /opt/flash-ticket-app /opt/flash-ticket-build /opt/flash-ticket-infra /opt/flash-ticket-src /opt/docs; do [ -d $d ] && du -xh --max-depth=2 $d 2>&1 | sort -k2; done
echo "### stat_srv_l2"; find /srv/rca-lab /etc/rca-lab /opt/rca-lab /opt/rca-tai /opt/flash-ticket-app /opt/flash-ticket-build /opt/flash-ticket-infra -maxdepth 2 -type d -printf '%M %u:%g %TY-%Tm-%TdT%TH:%TM %p\n' 2>&1 | sort -k4
echo "### etc_rca_lab_names"; find /etc/rca-lab -printf '%M %u:%g %s %p\n' 2>&1
echo "### crontab_ubuntu"; crontab -l 2>&1
echo "### crontab_root"; sudo -n crontab -l 2>&1
echo "### crontab_users"; for u in $(cut -d: -f1 /etc/passwd); do o=$(sudo -n crontab -l -u $u 2>/dev/null); [ -n "$o" ] && { echo "--- $u"; echo "$o"; }; done
echo "### etc_cron"; ls -la /etc/cron* 2>&1
echo "### cron_d_content"; for f in /etc/cron.d/*; do echo "--- $f"; cat $f 2>&1; done
echo "### systemd_custom_files"; find /etc/systemd/system -maxdepth 2 \( -type f -o -type l \) -printf '%y %p -> %l\n' 2>&1 | sort
echo "### systemd_user"; ls -la /home/ubuntu/.config/systemd/user 2>&1; systemctl --user list-units --all --no-pager 2>&1 | head -40
echo "### list_timers"; systemctl list-timers --all --no-pager 2>&1
echo "### list_units_running_services"; systemctl list-units --type=service --state=running --no-pager --no-legend 2>&1
echo "### list_units_transient"; systemctl list-units --all --no-pager --no-legend 2>&1 | grep -E 'run-|rca|t0[0-9]|flash|ft-|k6|tai' 
echo "### unit_files_enabled"; systemctl list-unit-files --state=enabled --no-pager --no-legend 2>&1
echo "### ps"; ps -eo pid,user,lstart,etime,rss,args --sort=start_time 2>&1 | awk 'NR==1 || ($2!="root" || $0 ~ /python|java|k6|docker-proxy|bash|tmux|screen|nohup|containerd-shim|node|dockerd/)' | cut -c1-260
echo "### tmux_screen"; tmux ls 2>&1; screen -ls 2>&1
echo "### git_checkouts"; find / -xdev -maxdepth 6 -name .git \( -type d -o -type f \) -not -path '/proc/*' -not -path '/home/ubuntu/.cache/*' 2>/dev/null | while read g; do d=$(dirname $g); echo "--- $d"; git -C $d rev-parse HEAD 2>&1; git -C $d rev-parse --abbrev-ref HEAD 2>&1; git -C $d log -1 --format='%h %cI %s' 2>&1; git -C $d status --short 2>&1 | head -30; echo "status_lines=$(git -C $d status --short 2>/dev/null | wc -l)"; git -C $d remote -v 2>&1 | head -2; done
