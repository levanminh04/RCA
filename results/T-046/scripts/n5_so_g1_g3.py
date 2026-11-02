"""So G1 và G3 theo số đơn vị có cờ ở A/A, thật (lượt b3-sua2) và C-e (b6-sau-khoa-sua2), không nhãn. Chỉ báo cáo."""
import json,statistics,sys,glob,os
sys.path.insert(0,'results/T-046/scripts')
import t046
ca,_=t046.nap_ghep('results/T-046/runs/b3-sua2-aa-001','results/T-046/runs/b3b-aa-001')
out={}
for ds in ('RE2-TT','Nezha-OB'):
    for kieu in ('aa|R0','that|R0'):
        r={}
        for g in ('G0','G1','G3'):
            c='D0' if g=='G0' else 'D1'
            ty=[];so=[];V=0
            for oid,x in ca.items():
                if x['dataset']!=ds: continue
                b=x['cua_so'][kieu]['bang']
                n=t046.so_don_vi_co(b,g,c,{}); so.append(n); ty.append(n/max(t046.so_don_vi_hop_le(b),1))
            r[g]={'don_vi_co_trung_vi':statistics.median(so),'ty_le_trung_vi':round(statistics.median(ty),5)}
        out[f'{ds}|{kieu}']=r
# cặp thật > A/A cùng ca
for ds in ('RE2-TT','Nezha-OB'):
    for g,c in (('G1','D1'),('G3','D1')):
        a=[(t046.so_don_vi_co(x['cua_so']['that|R0']['bang'],g,c,{})/max(t046.so_don_vi_hop_le(x['cua_so']['that|R0']['bang']),1),
            t046.so_don_vi_co(x['cua_so']['aa|R0']['bang'],g,c,{})/max(t046.so_don_vi_hop_le(x['cua_so']['aa|R0']['bang']),1)) for x in ca.values() if x['dataset']==ds]
        out[f'{ds}|that>aa|{g}']=sum(1 for p,q in a if p>q)
print(json.dumps(out,ensure_ascii=False,indent=0))
ce=[json.load(open(f,encoding='utf-8')) for f in glob.glob('results/T-046/runs/b6-sau-khoa-sua2-001/ce/*.json')]
print('ce co G1',statistics.median(x['doi_chung_G1']['so_co']['don_vi_co'] for x in ce),statistics.median(x['doi_chung_G1']['ty_le_don_vi_co'] for x in ce),' G3',statistics.median(x['so_co']['khoa']['don_vi_co'] for x in ce),statistics.median(x['ty_le_don_vi_co'] for x in ce))
k=json.load(open('results/T-046/kiem-sau-khoa-sua2.json',encoding='utf-8'))['K_du']
for a in ('ce|RE2-TT|qua_cong_theo_o','aa|RE2-TT|qua_cong_theo_o','that|RE2-TT|qua_cong_theo_o','that|Nezha-OB|qua_cong_theo_o'):
    print(a,{x:(y['k'],y['n'],y['ty_le']) for x,y in k[a].items()})
t=json.load(open('results/T-046/thang-diem-sua2.json',encoding='utf-8'))
print(t['hoa_khoa_tang1']['Nezha-OB'])
