"""Read ZIP directory metadata only. Never download/extract telemetry members."""
from pathlib import Path
import datetime
import hashlib
import json
import ssl
import struct
import urllib.request

RUN = Path(__file__).resolve().parent
meta = json.loads((RUN/'zenodo-record-metadata.json').read_text(encoding='utf-8-sig'))
file = next(x for x in meta['files'] if x['key'] == 'RE3-OB.zip')
url, size = file['links']['self'], file['size']
ctx = ssl.create_default_context()
certs = []
for store in ('ROOT', 'CA'):
    for cert, encoding, trust in ssl.enum_certificates(store):
        if encoding == 'x509_asn' and (trust is True or '1.3.6.1.5.5.7.3.1' in trust):
            certs.append(ssl.DER_cert_to_PEM_cert(cert))
if certs:
    ctx.load_verify_locations(cadata='\n'.join(certs))
receipts = []


def get_range(start, end):
    req = urllib.request.Request(url, headers={'Range': f'bytes={start}-{end}', 'Accept-Encoding': 'identity'})
    with urllib.request.urlopen(req, timeout=30, context=ctx) as response:
        assert response.status == 206, 'Range ignored; refusing to consume body'
        assert response.headers['Content-Range'] == f'bytes {start}-{end}/{size}'
        body = response.read(end-start+2)
        assert len(body) == end-start+1
        receipts.append({'url': url, 'range': [start,end], 'status': 206, 'bytes':len(body),
                         'sha256': hashlib.sha256(body).hexdigest(), 'etag': response.headers.get('ETag'),
                         'utc': datetime.datetime.now(datetime.timezone.utc).isoformat()})
        return body


result = {'scope': 'ZIP central-directory metadata only; no member data or telemetry decoded',
          'source_archive': {k:file[k] for k in ('key','size','checksum')}, 'requests': receipts,
          'telemetry_opened': False}
try:
    # Exact EOCD, not a speculative last64KiB read that might include a data member.
    tail = get_range(size-22, size-1)
    sig, disk, cd_disk, on_disk, count, cd_size, cd_offset, comment = struct.unpack('<4s4H2LH', tail)
    assert sig == b'PK\x05\x06' and comment == disk == cd_disk == 0
    assert on_disk == count and cd_offset+cd_size == size-22 and cd_size < 1024**2
    directory = get_range(cd_offset, cd_offset+cd_size-1)
    entries, offset = [], 0
    while offset < len(directory):
        row = struct.unpack_from('<4s6H3L5H2L', directory, offset)
        assert row[0] == b'PK\x01\x02'
        n, x, c = row[10:13]
        name = directory[offset+46:offset+46+n].decode('utf-8' if row[3]&0x800 else 'cp437')
        entries.append({'name':name, 'flags':row[3], 'method':row[4], 'crc32':row[7],
                        'compressed_bytes':row[8], 'bytes':row[9], 'local_header_offset':row[16]})
        offset += 46+n+x+c
    assert offset == len(directory) and len(entries) == count
    result.update(status='PASS', entries=entries)
    print(json.dumps({'PASS':True, 'entries':len(entries), 'received_bytes':sum(x['bytes'] for x in receipts),
                      'possible_static_metadata':[x['name'] for x in entries if any(k in x['name'].lower() for k in ['pod-node','readme','collect','config','.yaml','.py','.md'])][:50]}))
except Exception as exc:
    result.update(status='FAILED_NO_TELEMETRY_READ', error=repr(exc))
    print(json.dumps({'PASS':False,'error':repr(exc),'telemetry_opened':False}))
finally:
    (RUN/'zip-directory-metadata-001.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
