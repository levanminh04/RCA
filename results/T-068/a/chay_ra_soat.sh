#!/usr/bin/env bash
# T-068 A bước 0: chạy ra_soat.py cho 28 ca có gói trên laptop (song song 4). Chỉ đọc gói.
set -u
cd /d/RCA-flashticket
OUT=results/T-068/a/ra-soat; mkdir -p "$OUT"
CA=results/T-065/may-l11/du-lieu/V082-V066+H8a
job() {
  local ca=$1 src=$2
  case $src in
    t062) sha=$(PYTHONIOENCODING=utf-8 py -3 -I -c "import json;print(json.load(open('results/T-062/manifest.json',encoding='utf-8'))['files']['ca/$ca/cases/$ca/raw-traces.jsonl']['sha256'])")
          py -3 -I results/T-068/a/ra_soat.py --ca $ca --file-ca $CA/$ca.json --trace results/T-062/ca/$ca/cases/$ca/raw-traces.jsonl --sha $sha --out $OUT/$ca.json ;;
    dev2) sha=$(grep " \*./ca/$ca.tgz$" results/T-063/thu2/SHA256SUMS | cut -d' ' -f1)
          py -3 -I results/T-068/a/ra_soat.py --ca $ca --file-ca $CA/$ca.json --tgz results/T-063/thu2/ca/$ca.tgz --tgz-sha $sha --out $OUT/$ca.json ;;
    dev3) sha=$(grep " \*./ca/$ca.tgz$" results/T-063/thu3/thu/SHA256SUMS | cut -d' ' -f1)
          py -3 -I results/T-068/a/ra_soat.py --ca $ca --file-ca $CA/$ca.json --tgz results/T-063/thu3/thu/ca/$ca.tgz --tgz-sha $sha --out $OUT/$ca.json ;;
    arch) sha=$(grep "  $ca/raw-traces.jsonl$" D:/RCA-archive/hash-lists/exp-obs-cases.sha256 | cut -d' ' -f1)
          py -3 -I results/T-068/a/ra_soat.py --ca $ca --file-ca $CA/$ca.json --trace D:/RCA-archive/exp-obs/cases/$ca/raw-traces.jsonl --sha $sha --out $OUT/$ca.json ;;
  esac
  echo "exit=$? $ca"
}
export -f job; export OUT CA
PYTHONIOENCODING=utf-8 py -3 -I -c "
import json
for x in json.load(open('$CA/chi-muc.json',encoding='utf-8'))['su_co']:
    n=x['nguon']; print(x['ma'], 'arch' if x['ma']=='ebd5ef38' else n)
" | tr -d '\r' | xargs -P 4 -n 2 bash -c 'job "$0" "$1"'
