import sys,os,re,json,hashlib,subprocess,collections
R='D:/RCA-flashticket'; A='D:/RCA-archive'
rows=[l.split('\t') for l in open(sys.argv[1],encoding='utf-8').read().split('\n')[1:] if l]
out_tsv=sys.argv[2]; out_sum=sys.argv[3]
TEMP_EXT=re.compile(r'\.(lock|pid)$|\.partial-[^/]*$|/__pycache__/|\.tmp$')
TEXT_EXT={'.md','.py','.json','.txt','.sh','.ps1','.yml','.yaml','.csv','.tsv','.sha256','.out','.stderr','.stdout','.js','.cjs','.err','.log','','.z','.raw'}
def klass(p,b):
    if TEMP_EXT.search(p): return 'c-tam'
    e=os.path.splitext(p)[1].lower()
    if b>=1_000_000 or e in ('.gz','.tgz','.tar','.jsonl') or re.search(r'/(runs|ca|chay|thu2|thu3|kiem|bien-the|cham|du-lieu-l4|may-l11|may-l8b|nguon-l4|tai|tai-2|kiem-r)/',p): return 'b-dau-ra-chay'
    if e in TEXT_EXT: return 'a-ho-so-nhe'
    return 'b-dau-ra-chay'
# manifests
tracked=subprocess.run(['git','-C',R,'ls-files'],capture_output=True,text=True,encoding='utf-8').stdout.split('\n')
allfiles=[t for t in tracked if t]+[r[0] for r in rows]
MAN=re.compile(r'(SHA256SUMS[^/]*|\.sha256|manifest[^/]*\.json|MANIFEST[^/]*|NEN-[^/]*\.jsonl|nen[^/]*\.jsonl)$',re.I)
mans=[f for f in allfiles if f.startswith(('results/','tasks/','docs/')) and MAN.search(os.path.basename(f))]
covered=collections.defaultdict(set)
H=re.compile(r'^([0-9a-f]{64})\s+\*?(.+?)\s*$')
def addp(man,s):
    s=s.strip().replace(chr(92),'/')
    if not s or len(s)>400: return
    d=os.path.dirname(man)
    for cand in (os.path.normpath(os.path.join(d,s)).replace(chr(92),'/'), os.path.normpath(s).replace(chr(92),'/'), s.lstrip('./')):
        covered[cand].add(man)
def walk(man,o):
    if isinstance(o,dict):
        for k,v in o.items():
            if isinstance(k,str) and ('/' in k or '.' in k): addp(man,k)
            walk(man,v)
    elif isinstance(o,list):
        for v in o: walk(man,v)
    elif isinstance(o,str) and ('/' in o or re.search(r'\.\w{2,5}$',o)): addp(man,o)
nman=0
for m in mans:
    p=os.path.join(R,m)
    try:
        if os.path.getsize(p)>50_000_000: continue
        t=open(p,encoding='utf-8',errors='replace').read()
    except: continue
    nman+=1
    if m.endswith('.json'):
        try: walk(m,json.loads(t)); continue
        except: pass
    for line in t.split('\n'):
        mm=H.match(line)
        if mm: addp(m,mm.group(2)); continue
        if line.startswith('{'):
            try: walk(m,json.loads(line))
            except: pass
# archive hash index
arch={}
for root,ds,fs in os.walk(A):
    for f in fs:
        if f.endswith('.sha256') or f=='SHA256SUMS':
            for line in open(os.path.join(root,f),encoding='utf-8',errors='replace'):
                mm=H.match(line)
                if mm: arch[mm.group(1)]=os.path.relpath(os.path.join(root,f),A).replace(chr(92),'/')+' :: '+mm.group(2)
asz=collections.defaultdict(set)
for root,ds,fs in os.walk(A):
    for f in fs:
        try: asz[f].add(os.path.getsize(os.path.join(root,f)))
        except: pass
def sha(p):
    h=hashlib.sha256()
    with open(p,'rb') as fh:
        for ch in iter(lambda: fh.read(1<<20),b''): h.update(ch)
    return h.hexdigest()
res=[]; hashed=0
for p,b,m in rows:
    b=int(b); k=klass(p,b)
    man=sorted(covered.get(p,()))
    ar=''
    if k=='b-dau-ra-chay' and b in asz.get(os.path.basename(p),()):
        try:
            hv=sha(os.path.join(R,p)); hashed+=b; ar=arch.get(hv,'khong-khop-hash')
        except Exception as e: ar='loi-doc'
    parts=p.split('/'); task=parts[1] if parts[0]=='results' and len(parts)>1 else parts[0]
    sub='/'.join(parts[:3]) if len(parts)>3 else '/'.join(parts[:2])
    res.append((p,b,k,task,sub,len(man),man[0] if man else '',ar))
with open(out_tsv,'w',encoding='utf-8') as f:
    f.write('duong_dan\tbyte\tloai\ttask\tthu_muc\tso_manifest_dan\tmot_manifest\tkho_RCA-archive\n')
    for r in res: f.write('\t'.join(map(str,r))+'\n')
agg=collections.defaultdict(lambda: collections.Counter())
for r in res:
    a=agg[r[4]]; a['file']+=1; a['byte']+=r[1]; a[r[2]+'_file']+=1; a[r[2]+'_byte']+=r[1]
    if r[5]: a['co_manifest_file']+=1; a['co_manifest_byte']+=r[1]
    if r[7] and r[7] not in ('khong-khop-hash','loi-doc'): a['co_trong_kho_file']+=1; a['co_trong_kho_byte']+=r[1]
json.dump({'so_manifest_doc':nman,'byte_da_bam':hashed,'theo_thu_muc':{k:dict(v) for k,v in sorted(agg.items())}},open(out_sum,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
tot=collections.Counter()
for r in res: tot[r[2]+'_file']+=1; tot[r[2]+'_byte']+=r[1]; tot['man_'+str(bool(r[5]))+'_'+r[2]]+=r[1]
print(nman,hashed,dict(tot))
