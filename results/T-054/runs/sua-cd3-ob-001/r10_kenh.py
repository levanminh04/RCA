import json
G='D:/RCA-flashticket/'
pt=json.load(open(G+'results/T-054/reports/p7a-013-v2/phan-tich-nhom.json',encoding='utf-8'))
ch=json.load(open(G+'results/T-054/runs/sua-cd3-ob-001/cd3-test-cham.json',encoding='utf-8'))['cases']
for oid,v in sorted(ch.items()):
    if v['status']!='OK': continue
    root=pt['cases']['Nezha-OB'][oid]['root']; cell=v['cell']
    ex=json.load(open(G+pt['trung_gian_theo_ca']['Nezha-OB|'+oid]['M1']['result'],encoding='utf-8'))['records'][0]['extra']
    diem=ex['dau_vao_cd3']['diem']
    callees=sorted({b for a,b in ex['canh'] if a==root and b in diem and b!=root})
    def tom(e):
        ks=[k for k in ex['kenh_co'] if k['thuc_the']==e and k['F_I']==1]
        kp=[k['khoi_phat'] for k in ks if k['khoi_phat']]
        return {'n':len(ks),'kp':min(kp)//10**9 if kp else None,'tu_root':sum(1 for k in ks if k['don_vi'].startswith('canh|'+root+'|')),'loai':sorted({k['don_vi'].split('|')[0] for k in ks})}
    print(oid,cell,'RR',v['RR'],'root',tom(root))
    for c in callees: print('   callee',c,tom(c))
