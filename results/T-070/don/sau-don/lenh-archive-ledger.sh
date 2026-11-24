sudo -n bash -s <<'ROOT'
set -euo pipefail
L=/srv/flashticket-rca/ledger; A=/srv/flashticket-rca/archive/2026-11
test ! -e $A/ledger
install -d -o ledger -g ledger -m 700 $A/ledger
sha256sum $L/*.jsonl > /root/ledger-truoc.sha256
for f in e2e-001 t069-chinh t069-lap t069-thu t073-e5-01; do mv $L/$f.jsonl $A/ledger/; done
cd $A/ledger && sed "s#$L/#$A/ledger/#" /root/ledger-truoc.sha256 | sha256sum -c - ; rm /root/ledger-truoc.sha256
stat -c '%U:%G %a %n' $L $A/ledger $A/ledger/*
ls -A $L | wc -l
ROOT
sudo -n -u rca test -x /srv/flashticket-rca/archive/2026-11/ledger; echo "rca qua A/ledger rc=$?"
