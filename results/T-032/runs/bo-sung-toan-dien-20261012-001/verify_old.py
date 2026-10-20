import pathlib,json,hashlib,time
R=pathlib.Path(__file__).resolve().parents[4];O=pathlib.Path(__file__).parent
d=json.loads((O/'old-files-before.json').read_text(encoding='utf-8'));controlled={'docs/DECISIONS.md','docs/WHY.md','docs/STATE.md','tasks/T-032-g2-nguyen-nhan-xep-hang/LOG.md','tasks/T-033-g2-nguyen-nhan-phat-hien/LOG.md'}
bad=[];count=0;start=time.time()
for row in d['files']:
 if row['path'] in controlled:continue
 p=R/row['path'];h=hashlib.sha256()
 try:
  with p.open('rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  if h.hexdigest()!=row['sha256']:bad.append({'path':row['path'],'reason':'hash mismatch'})
 except FileNotFoundError:bad.append({'path':row['path'],'reason':'missing'})
 count+=1
 if count%10000==0:print(json.dumps({'checked':count,'bad':len(bad),'elapsed_s':round(time.time()-start,1)}),flush=True)
result={'old_immutable_files_checked':count,'controlled_files_excluded':sorted(controlled),'changed_or_missing':bad,'status':'PASS' if not bad else 'FAIL','elapsed_s':time.time()-start}
(O/'old-immutable-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=False),flush=True)
