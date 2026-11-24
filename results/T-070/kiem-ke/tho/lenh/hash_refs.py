import subprocess,re,collections,sys,os
R='D:/RCA-flashticket'; L='D:/Project/flashticket-rca-lab'; F='D:/Project/flash-ticket-platform'
files=subprocess.run(['git','-C',R,'ls-files','tasks','docs','results/T-06*','results/T-07*'],capture_output=True,text=True,encoding='utf-8').stdout.split('\n')
# include untracked md/json in results T-066.. too
unt=[l.split('\t')[0] for l in open(sys.argv[1],encoding='utf-8').read().split('\n')[1:] if l]
files+= [u for u in unt if re.match(r'(results/T-0(6[6-9]|7\d)|tasks/)',u) and u.endswith(('.md','.json','.txt','.sh','.ps1','.py'))]
rx=re.compile(r'(?i)(?:lab|commit|nhánh|HEAD|rca-lab)[^\n]{0,60}?\b([0-9a-f]{7,40})\b')
refs=collections.defaultdict(set)
for f in files:
    if not f: continue
    p=os.path.join(R,f)
    try:
        if os.path.getsize(p)>3_000_000: continue
        t=open(p,encoding='utf-8',errors='replace').read()
    except: continue
    for m in rx.finditer(t):
        h=m.group(1)
        if re.fullmatch(r'\d+',h): continue
        refs[h].add(f)
def has(repo,h):
    r=subprocess.run(['git','-C',repo,'cat-file','-t',h+'^{commit}'],capture_output=True,text=True)
    return r.returncode==0
out=[]
for h,fs in refs.items():
    inlab=has(L,h)
    if inlab:
        anc=subprocess.run(['git','-C',L,'merge-base','--is-ancestor',h,'main']).returncode==0
        st='lab-main' if anc else 'lab-ngoai-main'
    elif has(R,h): st='repo-RCA'
    elif has(F,h): st='repo-FlashTicket'
    else: st='khong-tim-thay'
    out.append((st,h,len(fs),sorted(fs)[:4]))
for o in sorted(out):
    if o[0] in ('lab-ngoai-main','khong-tim-thay','lab-main'): print(o[0],o[1],o[2],';'.join(o[3]))
print(collections.Counter(o[0] for o in out))
