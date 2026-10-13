"""Chấm mô tả N-Sigma từ intermediates đã xác minh, không đổi detector."""
import hashlib
import json
import os
from pathlib import Path

import numpy as np

H=Path(os.environ['T033_HOME']).resolve()
S=json.loads((H/'inputs/source.json').read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def segments(flags,times):
    result=[]; start=None
    for i,v in enumerate(flags):
        if v and (start is None): start=i
        if start is not None and (not v or i==len(flags)-1):
            end=i if v else i-1
            result.append({'start_index':start,'end_index':end,'start_time':int(times[start]),
                           'end_time':int(times[end]),'points':end-start+1,
                           'crosses_proxy':bool(start<720<=end)})
            start=None
    return result

def main():
    allrows=[]; indexes=[]
    for item in S['cases']:
        oid=item['opaque_id']
        for det in ('nsigma','nsigma_doi_chung'):
            found=[]
            for run in ('nsigma-first-001','nsigma-rest-001'):
                record=H/'runs'/run/(oid+'--'+det+'.json')
                if record.is_file(): found.append(record)
            assert len(found)==1, (oid,det,'source incomplete or duplicate')
            record=found[0]; meta=json.loads(record.read_text()); assert meta['status']=='PASS'
            path=record.parent/meta['output_npz']; assert sha(path)==meta['sha256']
            with np.load(path,allow_pickle=False) as z:
                times=z['times']; flags=z['Z']; anyflag=flags.any(axis=1)
                evaluated=z['evaluated']; mu=z['mean']; sd=z['std']; count=z['count']
                pre=(times<item['proxy'])&evaluated
                post=(times>=item['proxy'])&evaluated
                assert len(times)==1441 and np.all(np.diff(times)==1) and times[720]==item['proxy']
                alarms=times[anyflag].astype(int).tolist()
                assert alarms==item['expected'][det]['alarms']
                finite=np.isfinite(mu)&np.isfinite(sd)
                pi=np.flatnonzero(anyflag&post)
                first=int(pi[0]) if len(pi) else None
                ni=np.flatnonzero(anyflag)
                rows={'opaque_id':oid,'detector':det,'status':'VALID_NATIVE',
                      'source_npz':str(path.relative_to(H)),'source_sha256':meta['sha256'],
                      'first_alarm_index':int(ni[0]) if len(ni) else None,
                      'first_post_proxy_index':first,'t_hat_plus':int(times[first]) if first is not None else None,
                      'signed_seconds_from_proxy':int(times[first]-item['proxy']) if first is not None else None,
                      'no_post_alarm_to_end':first is None,'followup_end_time':int(times[-1]),
                      'pre_proxy':{'flag_points':int(np.sum(anyflag&pre)),
                                   'native_evaluated_points':int(pre.sum()),
                                   'fraction_flag_points':float(np.sum(anyflag&pre)/pre.sum()),
                                   'time_first_evaluated':int(times[np.flatnonzero(pre)[0]]),
                                   'time_last_evaluated':int(times[np.flatnonzero(pre)[-1]]),
                                   'seconds_grid_coverage':int(pre.sum()),
                                   'finite_statistics_cells':int(finite[pre].sum()),
                                   'all_evaluated_cells':int(pre.sum()*flags.shape[1]),
                                   'points_with_any_finite_statistics':int(finite[pre].any(axis=1).sum()),
                                   'points_with_all_finite_statistics':int(finite[pre].all(axis=1).sum()),
                                   'flags_with_nonfinite_statistics':int((flags[pre]&~finite[pre]).sum())},
                      'consecutive_true_segments':segments(anyflag,times),
                      'interpretation':'Thời gian đến strict vượt ngưỡng so proxy; cờ trước proxy không tự là false alarm vận hành; không biết onset thật.'}
                rows['first_post_alarm_in_preexisting_segment']=any(seg['crosses_proxy'] and seg['start_index']<=first<=seg['end_index'] for seg in rows['consecutive_true_segments']) if first is not None else None
                allrows.append(rows)
                indexes.append({'opaque_id':oid,'detector':det,'npz':str(path.relative_to(H)),
                                'sha256':meta['sha256'],'arrays':['x','count','mean','std','threshold','margin','Z','columns','times','evaluated'],
                                'not_evaluated_before':100,'nan_semantics':'False native khi so NaN; số đếm là non-NaN sau fill, không phải số raw quan sát độc lập.'})
    output=H/'runs/nsigma-delay-001'; output.mkdir(exist_ok=False)
    (output/'delay.json').write_text(json.dumps({'status':'PASS','rows':allrows,'scope':'N-Sigma only; BOCPD pending'},ensure_ascii=False,indent=2))
    (output/'intermediate-index.json').write_text(json.dumps({'status':'PASS','items':indexes},ensure_ascii=False,indent=2))
    print('PASS 60 N-Sigma delay/density/segments sources verified')

if __name__=='__main__': main()
