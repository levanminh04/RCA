"""Bank metadata only: public listing and ZIP directory if server honors ranges.

No telemetry bodies or predictions are read. A non-range binary response is closed.
"""
import datetime,hashlib,json,re,struct,urllib.request
from pathlib import Path
B=Path(__file__).resolve().parents[1];O=B/'runs/bank-metadata-001'
def save(n,x):(O/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def main():
    O.mkdir(exist_ok=False)
    raw=(B/'runs/review-sources-001/sources/drive-root.html').read_text(encoding='utf-8')
    encoded=re.search(r"window\['_DRIVE_ivd'\] = '(.*?)';",raw,re.S).group(1)
    decoded=re.sub(r'\\x([0-9a-fA-F]{2})',lambda m:chr(int(m[1],16)),encoded).replace('\\/','/').replace('\\"','"')
    listing=json.loads(decoded)[0]
    rows=[dict(id=x[0],name=x[2],mime=x[3],bytes=x[13],created_epoch_ms=x[9],modified_epoch_ms=x[10]) for x in listing]
    save('drive-inventory.json',dict(source='runs/review-sources-001/sources/drive-root.html',files=rows,observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),mutable_drive_not_immutable_revision=True))
    bank=next(x for x in rows if x['name']=='Bank.zip');attempts=[];members=[]
    url='https://drive.google.com/file/d/'+bank['id']+'/view'
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=40) as f: page=f.read()
    (O/'bank-file-view.html').write_bytes(page)
    # This endpoint is the public download link embedded in Drive file metadata.
    text=page.decode('utf-8');urls=re.findall(r'https[^"<> ]*(?:download|export=download)[^"<> ]*',text)
    save('download-links.json',urls)
    targets=['https://drive.usercontent.google.com/download?id='+bank['id']+'&export=download&confirm=t',
             'https://drive.google.com/uc?export=download&id='+bank['id']]
    for u in targets:
        start=max(0,bank['bytes']-65557);end=bank['bytes']-1
        row=dict(url=u,requested_range=f'bytes={start}-{end}',bytes_body_read=0)
        try:
            req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Range':row['requested_range']})
            with urllib.request.urlopen(req,timeout=40) as f:
                row.update(status=f.status,content_type=f.headers.get('Content-Type'),content_range=f.headers.get('Content-Range'),etag=f.headers.get('ETag'),last_modified=f.headers.get('Last-Modified'))
                if f.status!=206 or f.headers.get('Content-Range')!=f'bytes {start}-{end}/{bank["bytes"]}':
                    row['error']='Server did not return the exact range; binary body not read'
                    if 'text/html' in (f.headers.get('Content-Type') or ''):
                        html=f.read(262144);row['bytes_body_read']=len(html);(O/('attempt-'+str(len(attempts))+'.html')).write_bytes(html)
                else:
                    data=f.read(65558);row['bytes_body_read']=len(data);(O/'zip-tail.bin').write_bytes(data)
                    pos=data.rfind(b'PK\x05\x06')
                    if pos<0:raise ValueError('no ZIP EOCD; no telemetry read fallback')
                    vals=struct.unpack_from('<4s4H2LH',data,pos);row['zip_directory_size']=vals[5];row['zip_directory_offset']=vals[6]
                    # Directory metadata only. No local header or member inflation here.
                    off=vals[6];size=vals[5]
                    if off>=start:directory=data[off-start:off-start+size]
                    else:
                        req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Range':f'bytes={off}-{off+size-1}'})
                        with urllib.request.urlopen(req,timeout=40) as d:
                            if d.status!=206:raise ValueError('directory request not206')
                            directory=d.read(size+1)
                            if len(directory)!=size:raise ValueError('directory size mismatch')
                    (O/'zip-directory.bin').write_bytes(directory);p=0
                    while p<len(directory):
                        v=struct.unpack_from('<4s6H3L5H2L',directory,p)
                        if v[0]!=b'PK\x01\x02':raise ValueError('directory signature')
                        name=directory[p+46:p+46+v[10]].decode('utf-8' if v[3]&2048 else 'cp437')
                        members.append(dict(name=name,compressed_bytes=v[8],bytes=v[9],crc32=v[7],local_header_offset=v[16],compression=v[4]))
                        p+=46+v[10]+v[11]+v[12]
                    row['member_count']=len(members)
        except Exception as e:row['error']=str(e)
        attempts.append(row)
        if members:break
    save('range-attempts.json',attempts);save('zip-members.json',members)
    labels=[x for x in members if x['name'].lower().endswith(('record.csv','records.csv'))]
    save('summary.json',dict(bank=bank,drive_listing_ok=True,zip_directory_ok=bool(members),label_members=labels,telemetry_values_read=False,predictions_read=False,
         label_census_complete=False,limit='Drive lists only ZIP, no separately downloadable record.csv. ZIP range directory/label access depends on exact range support; do not fetch entire Bank archive to work around this.'))
    print(json.dumps(dict(bank=bank,attempts=attempts,members=len(members),labels=labels),ensure_ascii=False))
if __name__=='__main__':main()
