set +e
echo "### users"; getent passwd | awk -F: '$3>=1000 || $1 ~ /ledger|rca|ocarun|opc/' ; getent group rca ledger docker 2>&1
echo "### sudoers_d_names"; ls -la /etc/sudoers.d 2>&1
echo "### shim_count"; ps -eo args | grep -c '[c]ontainerd-shim'
echo "### opt_rca_lab_ignored"; [ -d /opt/rca-lab/.git ] && git -C /opt/rca-lab status --short --ignored 2>&1 | head -50
echo "### opt_rca_lab_branches"; [ -d /opt/rca-lab/.git ] && git -C /opt/rca-lab branch -a 2>&1 | head; git -C /opt/rca-lab log --oneline -3 2>&1
echo "### home_files"; find /home/ubuntu -maxdepth 3 -path /home/ubuntu/.ssh -prune -o -path /home/ubuntu/.cache -prune -o -path /home/ubuntu/.m2 -prune -o -path /home/ubuntu/.local -prune -o -path /home/ubuntu/uvenv -prune -o -path /home/ubuntu/x86-check -prune -o -name .bash_history -prune -o -printf '%M %u %s %TY-%Tm-%TdT%TH:%TM %p\n' 2>&1 | sort -k5 | head -300
echo "### srv_files_l3"; find /srv/rca-lab -maxdepth 3 -not -path '*/trace-goi/*/*' -not -path '/srv/rca-lab/venv-m1/*' -not -path '/srv/rca-lab/collector-gateway/capture/*' -printf '%M %u:%g %s %TY-%Tm-%TdT%TH:%TM %p\n' 2>&1 | sort -k5 | head -1500
echo "### capture_summary"; ls /srv/rca-lab/collector-gateway/capture 2>/dev/null | head -5; ls /srv/rca-lab/collector-gateway/capture 2>/dev/null | wc -l; ls -la /srv/rca-lab/collector-agent 2>&1 | head
echo "### m1_snapshots"; find /srv/rca-lab/m1-snapshots -maxdepth 4 -printf '%M %u:%g %s %p\n' 2>&1 | head -100
