#!/bin/bash
# psql giả lập (KHÔNG kết nối DB): $1 = <db>_db, $2 = application_name; đọc stdin.
# Hành vi theo $FAKE_DIR: <db>.rc (mã thoát, mặc định 0), <db>.out (nội dung in ra; mặc định PHIEN + DA_COMMIT khi rc=0).
db=$1; app=$2; cat > /dev/null
echo "$db $app" >> "$FAKE_DIR/goi.log"
rc=$(cat "$FAKE_DIR/${db%_db}.rc" 2>/dev/null || echo 0)
if [ -f "$FAKE_DIR/${db%_db}.out" ]; then cat "$FAKE_DIR/${db%_db}.out"
else echo "PHIEN 4242 $app 2026-11-24"; [ "$rc" = 0 ] && echo "DA_COMMIT $db 2026-11-24"; fi
exit "$rc"
