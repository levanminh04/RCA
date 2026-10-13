"""Khóa nhóm/đối chứng từ nguồn đã hash; không đọc telemetry/diễn giải."""
import json
from pathlib import Path
R=Path(__file__).resolve().parents[3]
O=R/'results/T-033'
assert json.loads((O/'runs/prepare-001/source-verification.json').read_text())['status']=='PASS'
rows=json.loads((R/'results/T-029/theo-ca.json').read_text(encoding='utf-8'))['rows']
source=json.loads((O/'runs/prepare-001/inputs/source.json').read_text(encoding='utf-8'))
cases={r['opaque_id']:r for r in source['cases']}
groups={}
for r in rows:
    detector=r['detector']
    oid=r['opaque_id']
    keys=['proxy-first/'+detector+'/'+r['first_group']]
    status=cases[oid]['expected'][detector]['status']
    keys.append('native-status/'+detector+'/'+status)
    if r.get('Miss'): keys.append('post-proxy-Miss/'+detector)
    if r.get('D0'): keys.append('D0/'+detector)
    if not r.get('primary_flags'): keys.append('unexplained-primary/'+detector)
    for flag,value in r.get('flags_flat',{}).items():
        if value is True: keys.append('multi-label/'+detector+'/'+flag)
    for key in keys: groups.setdefault(key,[]).append(r)
locked=[]
for key,members in sorted(groups.items()):
    members.sort(key=lambda r:r['opaque_id'])
    representative=members[0]
    candidates=[r for r in rows if r['detector']==representative['detector'] and r['opaque_id'] not in {x['opaque_id'] for x in members}]
    candidates.sort(key=lambda r:(r['cell']!=representative['cell'],abs((r.get('d') or 0)-(representative.get('d') or 0)),r['opaque_id']))
    control=candidates[0] if candidates else None
    locked.append({'group':key,'all_members':[r['opaque_id'] for r in members],
                   'representative':representative['opaque_id'],'detector':representative['detector'],
                   'control':control['opaque_id'] if control else None,
                   'matching':{'same_detector':True,'same_cell':bool(control and control['cell']==representative['cell']),
                               'same_d':bool(control and control.get('d')==representative.get('d'))},
                   'missing_condition':None if control else 'Không có ca ngoài nhóm cùng detector; phải đối chiếu điểm no-flag trong ca.',
                   'evidence_status':'NOT_YET_REPLAYED_OR_READ'})
doc={'status':'INITIAL_GROUPS_LOCKED_BEFORE_REPLAY_INTERPRETATION',
     'source':'results/T-029/theo-ca.json#/rows',
     'rules':{'representative':'opaque_id nhỏ nhất trong nhóm nguồn',
              'control':'cùng detector/RE2-TT/input metrics; ưu tiên cùng ô, sau đó khoảng cách d nhỏ nhất; tie opaque_id nhỏ nhất. Coverage thật sẽ đối chiếu trước diễn giải, thiếu điều kiện giữ rõ.',
              'new_factorial_groups':'Khóa membership input-equal/collapse/d0/error và CP/m-different/no-difference sau xác minh lõi/nhánh, trước đọc tay; cùng quy tắc ID và ghép điều kiện.',
              'point_control':'CP/flag và điểm lân cận no-CP/no-flag trên cùng lưới, không gọi đó là đúng vận hành.'},
     'groups':locked,'all_case_paths':[{'opaque_id':r['opaque_id'],'detector':r['detector'],'required_paths':['full'] if r['detector']!='bocpd' else ['full','FF','PP','FP','PF']} for r in rows],
     'scope_remaining':'Phần coverage/cadence/quy mô, đường xử lý mới và bằng chứng từng ca chưa được đọc; không suy cơ chế từ đại diện.'}
(O/'bao-phu-nhom.json').write_text(json.dumps(doc,ensure_ascii=False,indent=2),encoding='utf-8')
print('LOCKED',len(locked),'source groups',len(rows),'case-detector paths')
