"""Read archive directory metadata only; never read/decompress member payloads."""
import argparse, json, zipfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--plan',required=True);p.add_argument('--out',required=True);a=p.parse_args()
rows=[]
for item in json.loads(Path(a.plan).read_text(encoding='utf-8')):
    path=Path(a.data)/item['path'];row={'path':item['path'],'telemetry_rows_read':0,'payload_crc_verified':False}
    if path.suffix!='.zip':
        row.update(status='split_part',reason='not independent ZIP; directory absent')
    else:
        try:
            with zipfile.ZipFile(path) as z:
                infos=z.infolist()
                row.update(status='directory_ok',members=[{'name':i.filename,'bytes':i.file_size,'compressed_bytes':i.compress_size,'crc32_expected':format(i.CRC,'08x'),'compression_type':i.compress_type,'directory':i.is_dir()} for i in infos],member_count=len(infos),uncompressed_bytes=sum(i.file_size for i in infos))
        except Exception as ex:row.update(status='directory_error',error=str(ex))
    rows.append(row)
Path(a.out).write_text(json.dumps({'items':rows,'telemetry_rows_read':0,'payload_crc_verified':False},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'archives':len(rows),'directory_ok':sum(r['status']=='directory_ok' for r in rows),'errors':sum(r['status']=='directory_error' for r in rows),'telemetry_rows_read':0}))
