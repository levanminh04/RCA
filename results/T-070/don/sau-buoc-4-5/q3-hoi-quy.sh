set -euo pipefail
R=/srv/flashticket-rca/rca; H=b0f79a4dffd552f6e6026172b9058cd54ee9272475d927e35f19e22b04411b8d; M=$R/method/$H; RA=$R/hoi-quy-sau-don
date -u +%FT%TZ
sudo -n test ! -e $RA
sudo -n install -d -o rca -g rca -m 750 $RA
for ca in 46aab4be ebd5ef38; do
  extra=""; [ $ca = ebd5ef38 ] && extra="--dung-lai-dau-vao"
  sudo -n -u rca env PYTHONDONTWRITEBYTECODE=1 $R/venv/bin/python -B $M/src/m1_ft/chay_ca.py --id $ca \
    --cau-hinh $M/results/T-064/bien-the/V082-V066+H8a/cau-hinh.json --ban V082-V066+H8a --ra $RA --goc $R \
    --bo-sung "$R/bo-sung-hoi-quy/{id}/prometheus-bo-sung.json" $extra 2>&1 | tail -2
done
echo "== so voi chuan"
sudo -n sha256sum $RA/*/method-output-*.json $R/v082-hoi-quy/*/method-output-*.json
sudo -n sh -c "ls $RA/*"
date -u +%FT%TZ
