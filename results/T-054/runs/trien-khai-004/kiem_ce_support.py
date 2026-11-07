"""Ràng buộc C-e hoàn chỉnh trước nhãn, dùng metadata giả."""
import copy
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'results/T-054/scripts'))
from bien_nhan import *
from cham import validate_ce_plan
def denied(fn):
 try:fn()
 except Blocked:return
 raise AssertionError('bad C-e plan accepted')
r={'dataset':'RE2-TT','cases':{'a':{'t':1000,'ce_history':'verified'},'b':{'t':1200,'ce_history':'insufficient'}}}
j={'slot':{'dataset':'RE2-TT','opaque_id':'a','view':'ce','arm':'M1','seed':None,
           'source_sha256':fingerprint(r['cases']['a']),'window':{'t':700,'half_width_s':300}}}
s={'dataset':'RE2-TT','opaque_id':'b','status':'INSUFFICIENT_EVIDENCE','source_sha256':fingerprint(r['cases']['b'])}
p={'jobs':[j],'ce_support':[s]};validate_ce_plan(p,r)
bad=copy.deepcopy(p);bad['ce_support']=[];denied(lambda:validate_ce_plan(bad,r))
bad=copy.deepcopy(p);bad['ce_support'][0]['source_sha256']='x';denied(lambda:validate_ce_plan(bad,r))
bad=copy.deepcopy(p);bad['jobs'].append(j);denied(lambda:validate_ce_plan(bad,r))
bad=copy.deepcopy(p);bad['jobs'][0]['slot']['window']['t']=701;denied(lambda:validate_ce_plan(bad,r))
bad=copy.deepcopy(r);bad['cases']['a']['ce_history']='unknown';denied(lambda:validate_ce_plan(p,bad))
atomic(RUN/'C-e-support-checks.json',{'PASS':True,'checks':6,'scope':'synthetic metadata only; supported+insufficient/missing/forgery/duplicate/window/unknown'})
print('C-e support checks PASS')
