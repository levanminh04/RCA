sudo -n bash -s <<'ROOT'
set -euo pipefail; set -x
N=/srv/flashticket-rca; F=/opt/flashticket; A=$N/archive/2026-11; P=/opt/flash-ticket-app
test ! -e $N; test ! -e $F; test ! -e /etc/flashticket-rca; test ! -e /opt/flashticket-rca
install -d -o root -g root -m 755 $N $N/archive $A $A/home $A/build $N/faults $N/faults/toxiproxy
install -d -o root -g root -m 755 $F $F/build
install -d -o ubuntu -g ubuntu -m 755 $F/compose
install -d -o ubuntu -g ubuntu -m 700 $F/env
mv /srv/rca-lab/collector-agent $N/collector
mv /srv/rca-lab/backups $A/backups
rmdir /srv/rca-lab
mv /etc/rca-lab /etc/flashticket-rca
mv /opt/rca-lab /opt/flashticket-rca
mv /opt/flash-ticket-src $F/src
mv /opt/flash-ticket-build/t067-36a3725d $F/build/36a3725d
mv /opt/flash-ticket-build/t067-36a3725d-logs $A/build/
mv /opt/flash-ticket-infra $F/infra
for s in api-gateway booking-service discovery-server event-service payment-service ticket-service user-service; do mv $P/env-t062/$s.env $F/env/; done
for f in keycloak.env client-secrets.json test-users.json l1-buyers.json; do mv $P/env/$f $F/env/; done
mv $P/secrets $F/secrets
mv $P/otel $F/otel
cp -p $P/compose-exp/keycloak.yml $F/compose/keycloak.yml
sed -i -e 's#- /opt/flash-ticket-app/otel:/otel:ro#- /opt/flashticket/otel:/otel:ro#' \
       -e 's#- /opt/flash-ticket-infra/keycloak/keycloak/themes/flash-ticket:#- /opt/flashticket/infra/keycloak/keycloak/themes/flash-ticket:#' \
       -e 's#- /opt/flash-ticket-infra/keycloak/keycloak/import:#- /opt/flashticket/infra/keycloak/keycloak/import:#' $F/compose/keycloak.yml
chown ubuntu:ubuntu $F/compose/keycloak.yml
mv $P/rca-faults/booking-service $N/faults/
mv $P/rca-faults/event-service $N/faults/
rmdir $P/rca-faults
mv $P/rca-toxiproxy/proxies.json $N/faults/toxiproxy/
mv $P/l1-vnpay $N/faults/vnpay
mv /home/ubuntu/t063/inj $N/faults/inject-state
printf '/opt/flashticket/compose\n' > $N/faults/inject-state/compose-dir
chown ubuntu:ubuntu $N/faults/inject-state/compose-dir
mv /home/ubuntu/t063 $A/home/t063
for x in t058 t062 t071 inj.py inj2.py inj3.py build-t062.sh deploy-t062.sh prepare-t062.py rollback-t062.sh; do mv /home/ubuntu/$x $A/home/; done
set +x
echo "== ket qua"
stat -c '%U:%G %a %n' $N $N/collector $N/faults $N/faults/* $N/faults/toxiproxy/proxies.json $A $A/home $F $F/* /etc/flashticket-rca /etc/flashticket-rca/* /opt/flashticket-rca
ls $F/env; cat $N/faults/inject-state/compose-dir
grep -n "/opt/" $F/compose/keycloak.yml
diff <(sed -e 's#/opt/flash-ticket-app/otel#/opt/flashticket/otel#' -e 's#/opt/flash-ticket-infra/#/opt/flashticket/infra/#' $P/compose-exp/keycloak.yml) $F/compose/keycloak.yml && echo "keycloak.yml chi khac 3 duong bind"
ls $P
ROOT
