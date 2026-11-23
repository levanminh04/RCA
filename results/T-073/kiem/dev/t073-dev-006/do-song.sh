#!/bin/bash
# T-073 lượt 2: một lần đo sống (điều phối cho phép 20/11). Ghi chỉ ở runs/t073-dev-006, m1/t073-dev, rca-results/t073-dev-001.
O=/srv/rca-lab/runs/t073-dev-006; C=/srv/rca-lab/runs/t073-dev-code/campaigns/online
cd $O
T=$(( $(date +%s) - 900 )); echo "{\"t_hat\":$T,\"bat_dau_utc\":\"$(date -u +%FT%T.%NZ)\"}" > do-song.json
export RCA_ONLINE_OUT=$O RCA_M1_ROOT=/srv/rca-lab/m1/t073-dev RCA_RUN_M1=/opt/rca-lab/campaigns/runner/run_m1.py
python3 -B $C/orchestrator.py mot --t $T --ra /srv/rca-lab/rca-results/t073-dev-001 > orchestrator.out 2>&1
M=$(python3 -c "import json,glob;print(json.load(open(glob.glob('$O/su-co/*.json')[0])).get('ma_ca_m1',''))")
S1=$(python3 -c "import json,glob;s=json.load(open(glob.glob('$O/su-co/*.json')[0]));print([b for b in s['buoc'] if b['ten'].startswith('stage')][-1]['bat_dau_epoch'])")
W=$(python3 -c "print(max(0,int($S1+450-__import__('time').time())))"); echo "cho $W s" >> stage-lai.log; sleep $W
M2=$(python3 -c "import secrets;print(secrets.token_hex(4))")
date -u +%FT%T.%NZ >> stage-lai.log
sudo env RCA_M1_ROOT=/srv/rca-lab/m1/t073-dev PYTHONDONTWRITEBYTECODE=1 /srv/rca-lab/venv-m1/bin/python -B $C/stage_b.py --id $M2 --t $T > stage-lai.out 2>&1; echo "rc=$?" >> stage-lai.log
date -u +%FT%T.%NZ >> stage-lai.log
sudo python3 -c "
import hashlib,json
D='/srv/rca-lab/m1/t073-dev/cases/'
r={'t_hat':$T,'ma_1':'$M','ma_2':'$M2','file':{}}
for f in ('raw-traces.jsonl','raw-logs.jsonl','prometheus.json','inventory.json','request.json'):
    a=open(D+'$M/'+f,'rb').read(); b=open(D+'$M2/'+f,'rb').read()
    r['file'][f]={'sha_1':hashlib.sha256(a).hexdigest(),'sha_2':hashlib.sha256(b).hexdigest(),'bytes_1':len(a),'bytes_2':len(b),'trung':a==b}
for k in ('1','2'):
    m=json.load(open(D+(r['ma_'+k])+'/manifest.json')); r['manifest_'+k]={'created_utc':m['created_utc'],'counts':m['counts'],'chon_file':{p:{x:v[x] for x in ('so_file_mo','so_file_bo','vong_co_the_mat_dau','lan_chot')} for p,v in m['chon_file'].items()}}
open('$O/so-stage-lai.json','w').write(json.dumps(r,indent=1)+'\n')
print(json.dumps({f:v['trung'] for f,v in r['file'].items()}))
" >> stage-lai.log 2>&1
echo XONG >> stage-lai.log
