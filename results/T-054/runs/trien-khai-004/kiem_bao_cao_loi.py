"""TIMEOUT không làm hỏng bảng, không dựng trung gian/vùng chưa có."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'results/T-052/scripts'),str(ROOT/'src')]
from bien_nhan import *
from cham import describe

def job(arm,view='main'):
 return {'slot':{'dataset':'RE2-TT','opaque_id':'fixture','view':view,'arm':arm,'seed':None}}
failed={'status':'TIMEOUT','blocks':[],'method':'M1'}
records={};jobs=[]
for arm in ['M1','baro','simplerca','tracerca']:
 j=job(arm);jobs.append(j);records[fingerprint(j['slot'])]=[failed if arm=='M1' else {'status':'NO_EVIDENCE','blocks':[]}]
ce=job('M1','ce');jobs.append(ce);records[fingerprint(ce['slot'])]=[failed]
p={'jobs':jobs,'inventories':{'RE2-TT':['svc']}}
t=describe(p,records,{'RE2-TT':{'fixture':{'root':'svc','cell':'fixture|svc|cpu','fault':'cpu'}}})
assert t['ce'][0]['N1'] is None and t['ce'][0]['O'] is None and t['ce'][0]['V0'] is None
assert any(r['arm']=='C-c' for r in t['rows']) and not any(r['arm']=='C-g' for r in t['rows'])
assert any(row[3]=='C-g' for row in t['missing'])
assert all(row['metrics']['RR']==0 for row in t['rows'] if row['arm']=='M1')
atomic(RUN/'failure-report-checks.json',{'PASS':True,'C_e_unknown_intermediates_are_NA':True,
 'main_timeout_is_miss':True,'independent_C_c_retained':True,'C_g_missing_graph_reported_not_imputed':True})
print('failure report checks PASS')
