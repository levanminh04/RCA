"""Ghi danh sách trước khi đọc bằng chứng từng ca; chỉ dùng theo-ca và V7."""
from collections import defaultdict
from resume_step7 import OUT, ROOT, RUN, read, sha, log, write, now

def main():
    log('Lệnh có ghi: T-014-main python -B -W ignore scripts/select_manual.py. Chỉ đọc theo-ca.json/V7.json để chọn; chưa đọc telemetry hoặc đặc trưng chi tiết để diễn giải ca.')
    assert read(RUN/'verification.json')['status']=='PASS'
    target=OUT/'runs/manual-selection-001'
    assert not target.exists(); target.mkdir()
    rows=read(OUT/'theo-ca.json')['rows']; v7=read(OUT/'runs/step5-001/V7.json')
    groups=defaultdict(list); reasons=defaultdict(list)
    for i,r in enumerate(rows):
        det=r['detector']; combo='+'.join(r['primary_flags']) or 'D0'
        groups[det+'/tổ hợp/'+combo].append(i)
        for f in r['primary_flags']: groups[det+'/cơ chế/'+f].append(i)
        # Kiểm cả các nhóm xuất hiện chỉ trong độ nhạy khai trước.
        for f,val in r['flags_flat'].items():
            if val is True: groups[det+'/độ nhạy/'+f].append(i)
        if r['first_group']=='S': reasons[i].append('mọi S')
        if r['D0']: reasons[i].append('mọi D0')
    selected_groups={}
    for name,ids in sorted(groups.items()):
        pick=sorted(ids,key=lambda i:(rows[i]['opaque_id'],rows[i]['detector']))[:2]
        selected_groups[name]={'available':len(ids),'picked_row_indices':pick}
        for i in pick: reasons[i].append('mã mờ nhỏ nhất: '+name)
    # Không thêm ngưỡng tương đương: chỉ ghi bằng nhau đúng số hữu tỉ.
    equal=[]
    for oid,c in v7['cases'].items():
        variants=[('B1',c['B1'])]+[(f'B4/w{w}/k{k}',item) for w,z in c['B4'].items() for k,item in z.items()]
        for name,q in variants:
            if q['at_first_valid'] and q['control_n'] and int(q['at_first'])*q['control_n']==q['control_true']:
                equal.append({'scope':'case','name':name,'case_ids':[oid]})
    for name,scopes in v7['aggregate'].items():
        for scope,items in scopes.items():
            for group,q in items.items():
                if q['rates_exactly_equal']:
                    equal.append({'scope':scope,'group':group,'name':name,'case_ids':q['case_ids']})
    for e in equal:
        for i,r in enumerate(rows):
            if r['detector']=='bocpd' and r['opaque_id'] in e['case_ids']:
                reasons[i].append('V7 không phân biệt đúng số: '+e['scope']+'/'+e.get('group','')+'/'+e['name'])
    picks=[{'row_index':i,**{k:rows[i][k] for k in ('opaque_id','detector','cell','primary_flags','first_group','D0')},'reasons':sorted(set(reasons[i]))}
           for i in sorted(reasons,key=lambda i:(rows[i]['opaque_id'],rows[i]['detector']))]
    d={'time_before_manual':now(),'rule':'Trong từng bộ, chọn hai mã mờ nhỏ nhất mỗi cơ chế/tổ hợp cờ chính có ca; bao phủ thêm từng cờ độ nhạy đã khóa. Lấy hợp với mọi S, D0 và mọi ca của V7 bằng nhau đúng số ở cấp ca/ô/root/fault/toàn mẫu. Không đặt ngưỡng gần bằng; không chọn theo kết quả mong muốn. Đọc theo mã mờ rồi bộ phát hiện.',
       'sources':{p:{'sha256':sha(ROOT/p)} for p in ('results/T-029/theo-ca.json','results/T-029/runs/step5-001/V7.json')},
       'groups':selected_groups,'literal_non_discriminating':equal,'selected_count':len(picks),'selected':picks}
    write(target/'selection.json',d)
    text=['# Danh sách đọc tay ghi trước khi đọc','',d['rule'],'','Nguồn: theo-ca.json#/rows và runs/step5-001/V7.json#/cases, #/aggregate. selection.json giữ lý do và con trỏ dòng.','','| Ca | Bộ | Ô | Lý do |','|---|---|---|---|']
    text += ['| '+r['opaque_id']+' | '+r['detector']+' | '+r['cell'].replace('|',' / ')+' | '+ '; '.join(r['reasons'])+' |' for r in picks]
    (target/'selection.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    log('Đã ghi quy tắc/danh sách trước đọc tay: '+str(len(picks))+' cặp; selection.json/md đã lưu. V7 chỉ lấy bằng nhau đúng số, không thêm ngưỡng. Tiếp theo đọc nguồn chi tiết đúng danh sách.')
    print({'selected':len(picks),'cases':len({r['opaque_id'] for r in picks}),'groups':len(selected_groups)})

if __name__=='__main__': main()
