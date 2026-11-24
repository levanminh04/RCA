#!/bin/bash
# usage: ssh.sh app|obs|tai < script
case $1 in
 app) K='D:/RCA-ext/keys/exp-app/ssh-key-2026-11-10 (1).key'; T=ubuntu@129.221.208.47; KH=D:/RCA-ext/overnight-T058/out/known_hosts;;
 obs) K='D:/RCA-ext/keys/exp-obs/ssh-key-2026-11-10.key'; T=ubuntu@213.35.116.128; KH=D:/RCA-ext/overnight-T058/out/known_hosts;;
 tai) K='D:/RCA-ext/keys/Hahaa123.pem'; T=ubuntu@3.24.8.49; KH=D:/RCA-ext/keys/known_hosts;;
esac
'C:/Program Files/Git/usr/bin/ssh.exe' -i "$K" -o BatchMode=yes -o ConnectTimeout=15 -o StrictHostKeyChecking=accept-new -o UserKnownHostsFile=$KH $T 'bash -s'
