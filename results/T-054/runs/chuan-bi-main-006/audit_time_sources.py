"""Ghi hiện trạng timestamp, không ép nguồn thiếu thành đủ hoặc gọi phương pháp."""
from pathlib import Path
import sys,json,csv,copy
import numpy as np
import pyarrow.parquet as pq
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;PRIVATE=Path('D:/RCA-ext/private/T-054/prepare-main-006')
sys.path[:0]=[str(ROOT/'results/T-054/scripts'),str(ROOT/'src')]
from bien_nhan import *
from m1 import quan_sat
sources=read_pin(ref(RUN/'checkpoint-01-sources.json'));rt=read_pin(sources['runtime_refs']['RE2-TT']);author=read_pin(sources['author_source_ref'])
evidence=read_pin(ref(PRIVATE/'TT-Ce-temporal-evidence.json'));contract=read_pin(read_pin(ref(ROOT/'results/T-054/protocol.json'))['m1_contract_ref']);corrected=copy.deepcopy(evidence)
r=int(round(contract['quan_sat']['do_phan_giai_r']['RE2-TT log']*1e9));Arows={};differences=[];status_changes=[];bin_changes=[];zero_sides=[];short_cases=[]
for oid,row in rt['cases'].items():
    t=row['t'];lo=(t-600)*10**9;mid=(t-300)*10**9;hi=t*10**9
    values=pq.read_table(ROOT/row['files']['logs.parquet']['path'],columns=['timestamp']).to_pandas()['timestamp'].to_numpy(float)
    stamps=[int(x*10**9)for x in values if lo/1e9<=x<hi/1e9];F=(int(round(float(values.min())*1e9)),int(round(float(values.max())*1e9))+r)
    q=json.loads(canonical(quan_sat.tinh_nguon([F],stamps,r,(lo,hi),{'N':(lo,mid),'A':(mid,hi)},o_s=10*10**9)))
    old=evidence[oid]['coverage']['log'];assert q['F']==old['F']
    if q!=old:differences.append(oid)
    if q['o']!=old['o']:bin_changes.append(oid)
    reasons=[x for x in evidence[oid]['reason']if not x.startswith('log:')]
    if F[0]>lo or F[1]<hi:reasons.append('log:F_does_not_cover_requested_history')
    if not stamps or any(q['o'][side]['OPEN']>0 for side in ['N','A']):reasons.append('log:A0_observation_not_supported_through_window')
    status='insufficient'if reasons else'verified'
    if status!=row['ce_history']:status_changes.append(oid)
    corrected[oid]['coverage']['log']=q;corrected[oid]['reason']=reasons;corrected[oid]['status']=status
    details={}
    for name,meta in author['cases_by_member'][row['member_sha256']]['files'].items():
        with (Path(author['data_root'])/meta['path']).open(encoding='utf-8-sig',newline='')as f:times=[float(x['time'])for x in csv.DictReader(f)]
        assert all(np.isfinite(times))and times==sorted(times),oid
        n=sum(x<t for x in times);an=sum(x>=t for x in times)
        details[name]={'rows_N_available':n,'rows_A_available':an,'N_selected':min(20,n),'A_selected':min(20,an),'time_min':min(times)if times else None,'time_max':max(times)if times else None,'t':t}
        if n==0 or an==0:zero_sides.append({'opaque_id':oid,'table':name,'N':n,'A':an})
        if n<20 or an<20:short_cases.append(oid)
    Arows[oid]=details
assert not status_changes,status_changes
atomic(PRIVATE/'TT-Ce-temporal-evidence-exact-log-int.json',corrected)
atomic(PRIVATE/'A-timestamp-support-check.json',Arows)
atomic(RUN/'source-temporal-final-check.json',dict(PASS=True,scope='Completed metadata audit, NOT all A sources method-ready',Ce_log_exact_int_rounding_checked_cases=60,Ce_history_status_unchanged=True,
    Ce_log_H_rounding_differences=differences,Ce_log_boundary_bin_differences=bin_changes,corrected_evidence=ref(PRIVATE/'TT-Ce-temporal-evidence-exact-log-int.json'),
    A_timestamp_audit_cases=60,A_timestamp_audit_CSV=180,A_zero_side_tables=zero_sides,A_short_cases=sorted(set(short_cases)),
    A_source_readiness='OPEN_SOURCE_LIMITATION_BEFORE_METHOD_EXECUTION'if zero_sides else'NO_EMPTY_TIME_SIDE',method_started=False))
atomic(RUN/'temporal-check-failure-resolution.json',dict(initial_assertions='tuple/list comparison mismatch, then real A source had no normal-time rows; do not treat data as all-supported',
    status='audit completed without forcing readiness',real_H_differences=len(differences),boundary_count_differences=len(bin_changes),history_status_changes=0,A_zero_side_tables=zero_sides))
p=RUN/'private-artifact-pins.json';(RUN/'private-artifact-pins-before-timecheck.json').write_bytes(p.read_bytes());p.write_bytes(canonical({p.as_posix():ref(p)for p in PRIVATE.rglob('*')if p.is_file()})+b'\n')
print(json.dumps({'audit_completed':True,'Ce_status_changes':len(status_changes),'rounding_H_differences':len(differences),'boundary_bin_changes':len(bin_changes),'A_zero_side_tables':zero_sides,'A_short_cases':len(set(short_cases))}))
