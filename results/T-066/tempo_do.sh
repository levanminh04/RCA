#!/usr/bin/env bash
# T-066 bước 10: đo tăng dung lượng Tempo 24 giờ. Mỗi 15 phút một dòng TSV. Chỉ đọc.
# cột: utc, epoch, byte_tempo_volume, byte_blocks, byte_wal, spans_nhan_tong (gateway otlp), spans_xuat_tempo_tong, k6_dang_chay
O=/srv/rca-lab/runs/tempo-do-t066/tempo-24h.tsv
V=/var/lib/docker/volumes/flash-ticket-obs-pinned_tempo-data/_data
end=$(( $(date +%s) + 25*3600 ))
[ -s "$O" ] || echo -e "utc\tepoch\tbyte_volume\tbyte_blocks\tbyte_wal\tspans_nhan\tspans_xuat_tempo\tghi_chu" > "$O"
while [ $(date +%s) -le $end ]; do
  [ -e /srv/rca-lab/runs/tempo-do-t066/DUNG ] && break
  vol=$(sudo -n du -sb $V | cut -f1); blk=$(sudo -n du -sb $V/blocks 2>/dev/null | cut -f1); wal=$(sudo -n du -sb $V/wal 2>/dev/null | cut -f1)
  m=$(curl -s -G http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=sum(otelcol_receiver_accepted_spans_total{job="central-collector"})' | python3 -c 'import json,sys;r=json.load(sys.stdin)["data"]["result"];print(r[0]["value"][1] if r else "NA")')
  x=$(curl -s -G http://127.0.0.1:9090/api/v1/query --data-urlencode 'query=sum(otelcol_exporter_sent_spans_total{job="central-collector",exporter=~".*tempo.*"})' | python3 -c 'import json,sys;r=json.load(sys.stdin)["data"]["result"];print(r[0]["value"][1] if r else "NA")')
  echo -e "$(date -u +%FT%TZ)\t$(date +%s)\t$vol\t$blk\t$wal\t$m\t$x\t" >> "$O"
  sleep 900
done
