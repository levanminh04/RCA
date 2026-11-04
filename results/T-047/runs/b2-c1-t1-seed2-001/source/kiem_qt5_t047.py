"""Lần theo cờ QT5 trên bản ghi đã có, không nhãn và không đổi phương pháp."""
import collections
import json
import sys
from pathlib import Path
import adapter_t047 as ad
import tep_pha1
sys.path.insert(0,str(ad.ROOT/'results/T-045/scripts'))
import soi_ban_ghi


def explain(r):
    groups={}
    for i,u in enumerate(r['extra']['don_vi_phan_vi']):
        g=u['ma'].split('|')[0]
        x=groups.setdefault(g,dict(states=collections.Counter(),units=0,flags=0,examples=[]))
        x['states'][u['trang_thai']]+=1;x['units']+=1
        fl=int(bool(u.get('F_raw_len')))+int(bool(u.get('F_raw_xuong')))
        x['flags']+=fl
        if len(x['examples'])<2 or fl and not any(z.get('F_raw_len') or z.get('F_raw_xuong') for z in x['examples']):
            x['examples'].append(dict(u,pointer=f'/extra/don_vi_phan_vi/{i}'))
    for i,u in enumerate(r['worlds']['P']['don_vi_dem']):
        g=u['ma'].split('|')[0]
        x=groups.setdefault(g,dict(states=collections.Counter(),units=0,flags=0,examples=[]))
        x['states'][u['trang_thai']]+=1;x['units']+=1
        fl=int(bool(u.get('F_raw_len')))+int(bool(u.get('F_raw_xuong')))
        x['flags']+=fl
        if len(x['examples'])<2 or fl and not any(z.get('F_raw_len') or z.get('F_raw_xuong') for z in x['examples']):
            x['examples'].append(dict(u,pointer=f'/worlds/P/don_vi_dem/{i}'))
    for x in groups.values():
        x['states']=dict(x['states'])
    q=soi_ban_ghi.soi(r,False)
    return dict(qt5=q,units_by_group=groups,
                chain='đơn vị hợp lệ/thiếu hỗ trợ → p/chênh/F_raw theo nhóm → số kênh có cờ → tỷ trọng nhóm',
                coverage=r['coverage'],log_statistics=r['extra']['thong_ke_log']['theo_thuc_the'],
                limits='Giải thích tỷ trọng kênh đã ghi, chưa xác nhận bất thường thật hay nguyên nhân gốc.')


def main():
    p=ad.OUT/'runs/b2-t1-seed0-001'
    m=tep_pha1.kiem(p)
    rows,normal={},{}
    with (p/m['tep']).open('r',encoding='utf-8') as f:
        for line in f:
            r=json.loads(line);oid=r['opaque_id']
            diag=json.loads((p/'cases'/oid/'summary.json').read_text(encoding='utf-8'))
            q=soi_ban_ghi.soi(r,False)
            if q['toan_hoa'] or q['so_nguong_cuc_lon'] or q['diem_lon_hon_1e6'] or (q['nhom_chiem'] or 0)>.9:
                rows[oid]=dict(dataset=diag['dataset'],**explain(r))
            elif diag['dataset'] not in normal:
                normal[diag['dataset']]=dict(oid=oid,**explain(r))
    ad.ghi(p/'qt5-phan-xu.json',dict(flagged=rows,counterparts_unflagged=normal,
        code=['src/m1/e4.py:181 (đơn vị đếm)', 'src/m1/chuoi.py:464 (chấm phân vị)',
              'src/m1/chuoi.py:493 (chấm đếm)', 'src/m1/chuoi.py:507 (kênh từ đơn vị)'],
        no_scoring_labels=True,decision='Không đổi cấu hình; người làm đọc flagged cùng counterpart và code trước K.'))
    print(json.dumps({o:{'dataset':x['dataset'],'groups':{g:{k:v for k,v in y.items() if k!='examples'}
                        for g,y in x['units_by_group'].items()},'flagged_channels':x['qt5']['kenh_co_theo_nhom']}
                      for o,x in rows.items()}))


if __name__=='__main__':main()
