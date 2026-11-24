#!/bin/bash
# df GIẢ LẬP (máy chủ) cho thử v3/chay.sh.
echo "Filesystem 1B-blocks Used Available Use% Mounted on"
echo "/dev/sda1 0 0 $(cat "$FAKE/df_host") 0% /"
