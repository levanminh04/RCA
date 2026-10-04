"""Finalize provenance and registry once; parent owns LOG and common outputs."""
import csv
import hashlib
import json
from pathlib import Path

out=Path(__file__).resolve().parent
work=Path('D:/RCA-ext/work/T-014')
source_rows=[]
downloads=[
    ('https://cran.r-project.org/bin/windows/base/old/4.4.2/R-4.4.2-win.exe',work/'downloads/R-4.4.2-win.exe','825c9a1098481da1fe636207148a23a4'),
    ('https://github.com/dscharrer/innoextract/releases/download/1.9/innoextract-1.9-windows.zip',work/'downloads/innoextract-1.9-windows.zip',None),
    ('https://ndownloader.figshare.com/files/35497658',out/'source/circa.zip','d78eca1de6c12d57d2317163cf872358'),
    ('https://ndownloader.figshare.com/files/35497661',out/'source/README.md','c9bbc94ac9aa6beba2a713d04142a81f'),
    ('https://ndownloader.figshare.com/files/35497664',out/'source/Supplementary-Material-357.zip','4bb3be1a1f035edd97de57f8998bdc22'),
]
for url,path,expected in downloads:
    payload=path.read_bytes()
    md5=hashlib.md5(payload).hexdigest()
    if expected:assert md5==expected,(path,md5,expected)
    sha=hashlib.sha256(payload).hexdigest()
    if path.name=='innoextract-1.9-windows.zip':
        assert sha=='6989342c9b026a00a72a38f23b62a8e6a22cc5de69805cf47d68ac2fec993065'
    source_rows.append({'url':url,'path':path.as_posix(),'bytes':len(payload),'sha256':sha,'md5':md5,
                        'published_checksum_match':True if expected else 'release_sha256_recorded'})
for record in json.loads((out/'r-downloads.json').read_text()):
    source_rows.append({'url':record['url'],'path':Path(record['path']).as_posix(),'bytes':record['bytes'],
                        'sha256':record['sha256'],'md5':record['md5'],
                        'published_checksum_match':record.get('metadata_md5_match','metadata file; hash locally pinned')})
with (out/'source-downloads.csv').open('w',encoding='utf-8-sig',newline='') as stream:
    writer=csv.DictWriter(stream,fieldnames=list(source_rows[0]));writer.writeheader();writer.writerows(source_rows)

marker=out/'registry-finalized.json'
if not marker.exists():
    rows=[]
    for relative in ('cartservice_cpu/1','cartservice_mem/1'):
        case='fse-ob/'+relative;source='D:/RCA-ext/data/fse-ob/'+relative+'/simple_data.csv'
        rows.append([case,source,'CIRCA-original R-pcalg repeat same full600 input','repeat PC matrix on fixed case; diagnostic timings shared','a'])
        rows.append([case,source,'CIRCA-original R-pcalg input column reversal','column-order independence of PC graph; remap before compare','b'])
    case='fse-ob/cartservice_mem/1';source='D:/RCA-ext/data/fse-ob/cartservice_mem/1/simple_data.csv'
    rows.append([case,source,'CIRCA-original linear/SVR RHT before DA failed attempt1',
                 'retained failure attempt; scores computed before nx2.5 DA topological API error; mem-prior-scoring.log','b'])
    rows.append([case,source,'CIRCA-original linear RHT+DA3 failed attempt1',
                 'retained error AttributeError networkx.topological_generations; no rank/fallback emitted','b'])
    with (out/'cases.csv').open('a',encoding='utf-8-sig',newline='') as stream:csv.writer(stream).writerows(rows)
    marker.write_text(json.dumps({'added_rows':len(rows),'source_downloads_successful_bytes':sum(row['bytes'] for row in source_rows),
                                  'extra_failed_attempt_known_bytes':971145,
                                  'network_bytes_known_cumulative':sum(row['bytes'] for row in source_rows)+971145},indent=2),encoding='utf-8')
print(marker.read_text())
