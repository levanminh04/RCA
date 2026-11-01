# T-045: vòng theo dõi một đợt chạy song song, chạy nền, không tốn token khi chờ. Thoát (để đánh thức agent) khi:
#   DUNG          — bộ điều phối tạo tệp DUNG (lỗi đầu tiên, ngoại lệ) hoặc người tạo;
#   PHA_A         — pha A xong (mọi lượt có ca đầu), chỉ báo một lần;
#   XONG          — có sự kiện "xong";
#   CHET          — tiến trình điều phối không còn mà chưa "xong";
#   DUNG_TIEN_DO  — progress.jsonl không đổi quá NGUONG_PHUT phút;
#   MOC           — đã qua MOC_PHUT phút kể từ lần theo dõi này (điểm kiểm định kỳ).
# Dùng: bash results/T-045/scripts/theo_doi.sh <đợt> [MOC_PHUT=60] [NGUONG_PHUT=15]
dot="results/T-045/runs/$1"; moc=${2:-60}; nguong=${3:-15}
pid=$(grep -o '"pid": [0-9]*' "$dot/nguon.json" | grep -o '[0-9]*')
t0=$(date +%s)
while true; do
  if [ -f "$dot/DUNG" ]; then echo "DUNG: $(cat "$dot/DUNG")"; exit 0; fi
  if grep -q '"su_kien": "xong"' "$dot/progress.jsonl"; then echo "XONG"; exit 0; fi
  if grep -q '"pha_A_xong"' "$dot/progress.jsonl" && [ ! -f "$dot/.da_bao_pha_A" ]; then
    touch "$dot/.da_bao_pha_A"; echo "PHA_A"; exit 0; fi
  if ! tasklist //FI "PID eq $pid" //NH | grep -q "$pid"; then
    sleep 5
    if grep -q '"su_kien": "xong"' "$dot/progress.jsonl"; then echo "XONG"; exit 0; fi
    echo "CHET: tiến trình $pid không còn"; exit 0; fi
  tuoi=$(( $(date +%s) - $(stat -c %Y "$dot/progress.jsonl") ))
  if [ $tuoi -gt $(( nguong * 60 )) ]; then echo "DUNG_TIEN_DO: ${tuoi}s không có sự kiện mới"; exit 0; fi
  if [ $(( $(date +%s) - t0 )) -gt $(( moc * 60 )) ]; then echo "MOC: $(grep -c '"don_vi"' "$dot/progress.jsonl") đơn vị xong"; exit 0; fi
  sleep 20
done
