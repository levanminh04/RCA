import csv,io,json,zipfile,collections,argparse,hashlib
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(exist_ok=False,parents=True);rows=[]
with zipfile.ZipFile(Path(a.data)/'GraphData/graph_data-combined.zip') as z:
    for i in z.infolist():
        if not i.filename.endswith('.csv'):continue
        h=hashlib.sha256();n=0;ids=set();duplicates=0;header=None;empty=collections.Counter();width=collections.Counter();sample=[]
        with z.open(i) as f:
            for line in f:h.update(line)
        with z.open(i) as f:
            rd=csv.reader(io.TextIOWrapper(f,encoding='utf-8-sig',newline=''));header=next(rd)
            for r in rd:
                n+=1;width[len(r)]+=1
                if r:duplicates+=r[0] in ids;ids.add(r[0])
                for j,v in enumerate(r):empty[str(j)]+=v==''
                if len(sample)<3 or i.filename=='id_service.csv':sample.append(r)
        rows.append(dict(member=i.filename,bytes=i.file_size,sha256=h.hexdigest(),header=header,rows=n,unique_first_field=len(ids),duplicate_first_field=duplicates,row_widths=dict(width),empty_fields=dict(empty),rows_or_sample=sample))
(out/'tables.json').write_text(json.dumps(rows,indent=2),encoding='utf-8');print(json.dumps(rows))
