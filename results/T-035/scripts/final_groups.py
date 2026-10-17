"""Hoàn thiện nhóm C3/C7 theo yêu cầu SPEC, không chạy bộ dựng hoặc đọc dữ liệu."""
import json,shutil
from collections import defaultdict
from pathlib import Path
from run import OUT,read,write

backup=OUT/'runs/report-001-before-final-groups';backup.mkdir(exist_ok=False)
for name in ['tu-vung-thao-tac.json','do-phu-theo-nhan.json','thong-ke-do-thi.md']:
    shutil.copyfile(OUT/name,backup/name)
s=read(OUT/'thong-ke-do-thi.json');index={(c['dataset'],c['opaque_id']):c for c in s['cases']}
v=read(OUT/'tu-vung-thao-tac.json')
for c in v['cases']:
    n={o['id'] for o in c['windows']['N']['operations']};a={o['id'] for o in c['windows']['A']['operations']}
    c['operations_A_only']=sorted(a-n);c['operations_N_only']=sorted(n-a)
for ds,x in v['datasets'].items():
    x['A_only_by_case']={c['opaque_id']:c['operations_A_only'] for c in v['cases'] if c['dataset']==ds and c['operations_A_only']}
    x['N_only_by_case']={c['opaque_id']:c['operations_N_only'] for c in v['cases'] if c['dataset']==ds and c['operations_N_only']}
(OUT/'tu-vung-thao-tac.json').write_text(json.dumps(v,ensure_ascii=False,sort_keys=True,indent=1),'utf-8')
l=read(OUT/'do-phu-theo-nhan.json');bycell=defaultdict(list)
for r in l['rows']:
    c=index[(r['dataset'],r['opaque_id'])]
    r['entity_N']=c['windows']['N']['entity_fingerprint'];r['entity_A']=c['windows']['A']['entity_fingerprint']
    r['operation_N']=c['windows']['N']['operation_fingerprint'];r['operation_A']=c['windows']['A']['operation_fingerprint']
    bycell[r['dataset']+'|'+str(r['cell'])].append(c)
for cell,cs in bycell.items():
    l['cells'][cell]['N_A_entity_changed']=sum(c['windows']['N']['entity_fingerprint']!=c['windows']['A']['entity_fingerprint'] for c in cs)
    l['cells'][cell]['N_A_operation_changed']=sum(c['windows']['N']['operation_fingerprint']!=c['windows']['A']['operation_fingerprint'] for c in cs)
    l['cells'][cell]['snapshots']={str(size):{'windows':sum(n.startswith('s'+str(size)+'-') for c in cs for n in c['windows']),
        'distinct':len({w['entity_fingerprint'] for c in cs for n,w in c['windows'].items() if n.startswith('s'+str(size)+'-')})} for size in [60,300] if cs[0]['dataset']=='RE2-TT'}
(OUT/'do-phu-theo-nhan.json').write_text(json.dumps(l,ensure_ascii=False,sort_keys=True,indent=1),'utf-8')
with (OUT/'thong-ke-do-thi.md').open('a',encoding='utf-8') as f:
    f.write('\n## Nhóm thao tác chỉ một phía và cấu trúc theo ô\n\n')
    for ds,x in v['datasets'].items():
        f.write(f'{ds}: {len(x["A_only_by_case"])} ca có thao tác chỉ ở A; {len(x["N_only_by_case"])} ca có thao tác chỉ ở N. Danh sách riêng từng ca/tên tại `tu-vung-thao-tac.json#/datasets/{ds}/A_only_by_case` và `N_only_by_case`; theo cửa sổ tại `#/cases`. Không bỏ nhóm chỉ sau mốc, không tạo nền giả.\n\n')
    f.write('C3 theo ô gồm full, đổi N/A và ảnh chụp tại `do-phu-theo-nhan.json#/cells`. Các nhóm này chỉ là báo cáo sau ghép nhãn, không là đầu vào bộ dựng hoặc căn cứ đã chọn mức P6. Bản trước bổ sung được giữ ở runs/report-001-before-final-groups.\n')
print('Completed C3 cell groups and C7 one-side operations')
