import sys, importlib.util
sys.argv=[sys.argv[0]]
exec(open(r"doc_bang_html.py".replace('bang.py','bang.py'),encoding='utf-8').read().split("p=P()")[0])
spec=importlib.util.spec_from_file_location('moc','../moc.py'); moc=importlib.util.module_from_spec(spec); spec.loader.exec_module(moc)
S='./'  # thư mục chứa torai.html (arxiv.org/html/2604.13522v1) và baro.html (arxiv.org/html/2405.09330)
def rows(tab):
    src=None; out={}
    for r in tab['rows'][2:]:
        r=[c.strip() for c in r]
        if len(r)==23:
            if r[0]: src=''.join(r[0].split())
            meth=r[1]; vals=r[2:]
        elif len(r)==22:
            meth=r[0]; vals=r[1:]
        else: continue
        out[(src,meth)]=vals
    return out
p=P(); p.feed(open(S+'torai.html',encoding='utf-8').read())
bad=0
for idx,ref in [(3,moc.TORAI_B2),(4,moc.TORAI_B3)]:
    R=rows(p.tables[idx])
    for (src,meth),cells in ref.items():
        vals=R[(src,meth)]
        for j,f in enumerate(moc.LOI6+['AVERAGE']):
            got=tuple(float(v) for v in vals[3*j:3*j+3])
            if got!=cells[f]: bad+=1; print('LECH',idx,src,meth,f,got,cells[f])
print('TORAI kiem xong, lech',bad)
p=P(); p.feed(open(S+'baro.html',encoding='utf-8').read())
t=p.tables[8]; bad=0
for r in t['rows'][2:]:
    name=r[0].replace('ϵ\epsilon','e').replace('[tinjectt_{\text{inject}}]','[t_inject]').strip()
    key={'CIRCA [t_inject]':'CIRCA[t_inject]','N-Sigma [t_inject]':'N-Sigma[t_inject]','RobustScorer [t_inject]':'RobustScorer[t_inject]','BARO (Ours)':'BARO'}.get(name)
    if not key: continue
    for k,ds in enumerate(['fse-ob','fse-ss']):
        got=[float(x) for x in r[1+5*k:6+5*k]]
        ref=[moc.BARO_B3[ds][key][f] for f in ['cpu','mem','delay','loss','AVG']]
        if got!=ref: bad+=1; print('LECH',key,ds,got,ref)
t=p.tables[7]
for r in t['rows'][2:]:
    key={'N-Sigma':'N-Sigma','BARO (Ours)':'BARO'}.get(r[0].strip())
    if not key: continue
    for k,ds in enumerate(['fse-ob','fse-ss']):
        got=tuple(float(x) for x in r[1+3*k:4+3*k])
        if got!=tuple(float(x) for x in moc.BARO_B2[ds][key]): bad+=1; print('LECH B2',key,ds,got)
print('BARO kiem xong, lech',bad)
