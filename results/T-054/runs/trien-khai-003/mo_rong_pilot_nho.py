"""Thêm đúng hai ca dev cho M1/T12 và A4; không nhân lại toàn ma trận dev."""
import copy
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=OUT/'runs/trien-khai-003'
sys.path[:0]=[str(OUT/'scripts'),str(RUN)]
from chuan_bi_pilot import build,MAIN,ENV
from bien_nhan import atomic,read_pin,ref,fingerprint
from dieu_phoi import status

assert status(RUN/'pilot-local-007/queue')['controller'] is None
p,a=build('pilot-local-008',{'RE2-TT':['dev-03d4910932'],'Nezha-OB':['dev-2bfc97b01e']},
          arms=('M1','T12-on'),baseline_arms={'RE2-TT':('torai_B',),'Nezha-OB':('simplerca',)},include_cd3=False)
plan=read_pin(p);q=Path(plan['directory']);q.mkdir()
# Cả hai gói đo dùng cùng cap một giờ, không reset đồng hồ hoặc chi phí nhóm.
prior=RUN/'pilot-local-007';old_plan=read_pin(ref(prior/'plan.json'));state=status(prior/'queue')
for key,row in state['jobs'].items():
    cost=read_pin(ref(Path(row['attempt'])/'cost.json'))
    atomic(q/key/'attempt-prior-cost'/'cost.json',cost)
start=read_pin(ref(prior/'queue/budget-start.json'));start['plan_sha256']=fingerprint(plan)
atomic(q/'budget-start.json',start)
atomic(RUN/'pilot-local-008/continuation.json',{'additional_cases_only':True,'slots':len(plan['jobs']),
       'prior_plan':ref(prior/'plan.json'),'whole_pilot_start_preserved':True,
       'method_group_costs_preserved':True,'test_opened':False})
r=subprocess.run([MAIN,'-B',str(OUT/'scripts/p7.py'),'run','--plan',p['path'],'--sha256',p['sha256'],
                  '--authority',a['path'],'--authority-sha256',a['sha256']],env=ENV,capture_output=True)
atomic(RUN/'pilot-local-008/launch.json',{'exit_code':r.returncode,'stdout':r.stdout.decode('utf-8'),'stderr':r.stderr.decode('utf-8')})
print(r.stdout.decode('utf-8'));print(r.stderr.decode('utf-8'));r.check_returncode()
