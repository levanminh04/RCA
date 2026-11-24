import subprocess, os, json, sys, collections
R='D:/RCA-flashticket'
out=subprocess.run(['git','-C',R,'ls-files','-o','--exclude-standard','-z'],capture_output=True).stdout.decode('utf-8','replace').split('\0')
rows=[]
for p in out:
    if not p: continue
    try: st=os.stat(os.path.join(R,p)); rows.append((p,st.st_size,int(st.st_mtime)))
    except Exception as e: rows.append((p,-1,0))
with open(sys.argv[1],'w',encoding='utf-8') as f:
    f.write('duong_dan\tbyte\tmtime_epoch\n')
    for r in rows: f.write(f'{r[0]}\t{r[1]}\t{r[2]}\n')
print(len(rows), sum(r[1] for r in rows if r[1]>0))
