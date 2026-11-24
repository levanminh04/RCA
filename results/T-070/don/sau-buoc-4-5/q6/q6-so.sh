OUT=/srv/flashticket-rca/runs/2026-11-24-kiem-online-dev
MOI=$(python3 -c "import json;d=json.load(open('$OUT/su-co/b104d97898.json'));print(d.get('ma_ca') or d.get('ca') or d.get('ma_ca_m1') or '')")
python3 -c "import json;d=json.load(open('$OUT/su-co/b104d97898.json'));print({k:(v if not isinstance(v,(dict,list)) else str(v)[:200]) for k,v in d.items()})" | cut -c1-1500
echo "MOI=$MOI"
cd /opt/flashticket-rca
sudo -n python3 -B rca/online/check_old_case.py so --ca 2d5a56fe --moi $MOI --g1-cu /srv/flashticket-rca/rca/results/dev --g1-moi /srv/flashticket-rca/rca/results/online-dev-001 > $OUT/so-ca-cu.json
cat $OUT/so-ca-cu.json
