import json, zipfile, argparse
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--data');p.add_argument('--out');a=p.parse_args();out=[]
for f in sorted(Path(a.data).glob('TraceLogData/**/*.zip')):
 with zipfile.ZipFile(f) as z:
  for i in z.infolist():
   if i.is_dir() or i.filename.startswith('__MACOSX') or Path(i.filename).name.startswith('.'):continue
   with z.open(i) as src:
    sample=src.read(2500).decode('utf-8',errors='replace')
   out.append({'archive':str(f.relative_to(a.data)),'member':i.filename,'sample':sample[:2500]})
Path(a.out).write_text(json.dumps(out,indent=2),encoding='utf-8')
print(len(out))
