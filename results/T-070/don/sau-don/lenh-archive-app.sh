sudo -n bash -s <<'ROOT'
set -euo pipefail; set -x
A=/srv/flashticket-rca/archive/2026-11
test ! -e $A/compose-t067; test ! -e $A/flash-ticket-app; test ! -e $A/opt-docs
mv /opt/flash-ticket-build/t067-compose $A/compose-t067
mv /opt/flash-ticket-app $A/flash-ticket-app
mv /opt/docs $A/opt-docs
mv /srv/flashticket-rca/faults/deploy-don-2026-11.tsv $A/build/
set +x
ls /opt; ls $A; ls /opt/flash-ticket-build
ROOT
