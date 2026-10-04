#!/bin/bash
# T-006 bước 0.3: tải dữ liệu công khai vào D:\RCA-ext\dl\ và kiểm MD5 theo nguồn.
# Chạy trong Git Bash: bash results/T-006/scripts/tai_du_lieu.sh
# MD5 mong đợi lấy từ API Zenodo (records/<id>, trường files[].checksum) ngày 03/10/2026.
set -u
DL=/d/RCA-ext/dl
mkdir -p "$DL"
tai() {  # tai <url> <tên file> <md5 mong đợi, hoặc "-" nếu nguồn không công bố>
  local url=$1 f=$2 md5=$3
  echo "[$(date '+%F %T')] tải $f từ $url"
  curl -sS -L --fail --retry 3 -o "$DL/$f" "$url" || { echo "LỖI tải $f"; return 1; }
  local got size
  got=$(md5sum "$DL/$f" | cut -d' ' -f1)
  size=$(stat -c %s "$DL/$f")
  echo "[$(date '+%F %T')] $f: $size B, md5 $got, sha256 $(sha256sum "$DL/$f" | cut -d' ' -f1)"
  if [ "$md5" = "-" ]; then echo "  nguồn không công bố md5"; elif [ "$got" = "$md5" ]; then echo "  MD5 KHỚP nguồn"; else echo "  MD5 KHÔNG KHỚP (mong đợi $md5)"; fi
}
tai "https://zenodo.org/records/14590730/files/RE1-OB.zip?download=1" RE1-OB.zip 47cce26ed24140e8974e68f9db2a5e9c
tai "https://zenodo.org/records/14590730/files/RE1-SS.zip?download=1" RE1-SS.zip d2b15cbd3bb3cf6ec5f3cc65f7fac225
tai "https://zenodo.org/records/11046533/files/fse-ob.zip?download=1" fse-ob.zip 4c81245a90b02094566111ddac41bdd8
tai "https://zenodo.org/records/11046533/files/fse-ss.zip?download=1" fse-ss.zip 5603b151ee7b9ebe079d27bc75210763
tai "https://github.com/phamquiluan/baro/releases/download/0.0.4/simple_data.csv" baro-simple_data.csv -
echo "[$(date '+%F %T')] xong"
