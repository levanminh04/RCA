"""Audit four approved archives. CSV streams; one NPY member at a time; no RCA."""
import argparse,array,collections,csv,datetime,hashlib,io,json,math,pathlib,re,resource,struct,time,zipfile
import xml.etree.ElementTree as ET
from safe_npy import read_npy,numeric,array_info,Tag,selfcheck
BAD_UTF8=re.compile('[\udc80-\udcff]')

def quantile(values,q):
    if not values: return None
    values=sorted(values); p=(len(values)-1)*q; a=int(p); b=min(a+1,len(values)-1)
    return values[a]+(values[b]-values[a])*(p-a)

def bands(values,times,start,end):
    groups=[[],[],[]]
    mid=(start+end)/2
    for t,v in zip(times,values):
        if not math.isfinite(v): continue
        if start<=t<mid: groups[0].append(v)
        elif mid<=t<end: groups[1].append(v)
        elif end<=t<end+(end-start): groups[2].append(v)
    median=quantile(groups[0],.5)
    if median is None: return {'counts':[len(x) for x in groups],'status':'no_reference'}
    dev=[abs(x-median) for x in groups[0]]
    out={'counts':[len(x) for x in groups],'median':median,'q':[]}
    for q in [.95,.99,.995]:
        threshold=quantile(dev,q)
        out['q'].append({'q':q,'band':threshold,'zero_band':threshold==0,
                         'exceed':[sum(abs(v-median)>threshold for v in g) for g in groups[1:]]})
    return out

def npy_summary(data,cloud):
    header,obj=read_npy(data); out={'header':header,'parser':'static-inert-numpy-subset','keys':list(obj),'cases':[]}
    if len(obj)==1 and isinstance(next(iter(obj.values())),dict) and isinstance(next(iter(obj.values())).get('time'),Tag):
        out['container']='nested log feature dictionary'; obj=next(iter(obj.values()))
    if 'Sequence' in obj:
        shape,code,raw=array_info(obj['Sequence']); tshape,tcode,traw=array_info(obj['time'])
        times=[x[0] for x in struct.iter_unpack('<'+{'i8':'q','i4':'i','f8':'d'}[tcode],traw)]
        entities=obj['Node_Name']
        if shape!=(len(entities),len(times),1): raise ValueError('flat log-feature shape mismatch')
        vals=array.array('d');vals.frombytes(raw)
        c={'kpi':obj['KPI_Label'],'stored_keys':list(obj),'features':[obj['KPI_Feature']],
           'entities':entities,'shape':shape,'layout':'entity,time,feature (preprocessed log feature)',
           'time_min':min(times),'time_max':max(times),'time_count':len(times),'time_unique':len(set(times)),
           'deltas':dict(collections.Counter(times[i]-times[i-1] for i in range(1,len(times)))), 'columns':[]}
        for j,name in enumerate(entities):
            v=vals[j*len(times):(j+1)*len(times)];finite=[x for x in v if math.isfinite(x)]
            col={'name':name,'count':len(v),'nonfinite':len(v)-len(finite),'min':min(finite) if finite else None,
                 'max':max(finite) if finite else None,'constant':bool(finite) and min(finite)==max(finite),
                 'sha256':hashlib.sha256(v.tobytes()).hexdigest()}
            if cloud:
                begin=int(datetime.datetime(2024,1,23,3,10,tzinfo=datetime.timezone.utc).timestamp());col['descriptive_bands']=bands(v,times,begin,begin+86400)
            c['columns'].append(col)
        out['cases'].append(c);out['processing_settings']={k:obj[k] for k in ['step_size','window_size'] if k in obj}; return out
    for key,case in obj.items():
        if not isinstance(case,dict) or 'Sequence' not in case:
            # pod→node mapping dictionaries contain only strings, not arbitrary objects.
            if not all(isinstance(k,str) and isinstance(v,str) for k,v in obj.items()): raise ValueError('unknown non-mapping schema')
            out['mapping']={str(k):str(v) for k,v in obj.items()}; break
        times=[numeric(x) for x in case['time']]
        shape,code,raw=array_info(case['Sequence']); rows,cols=shape
        entities=case.get('Pod_Name',case.get('Node_Name',[])); features=case.get('KPI_Feature',case.get('jaeger_Feature'))
        if rows!=len(times) or cols!=len(entities)+len(features): raise ValueError('entity/time/shape mismatch')
        deltas=collections.Counter(times[i]-times[i-1] for i in range(1,len(times)))
        c={'kpi':key,'stored_keys':list(case),'entities':entities,'features':features,'shape':shape,'dtype':code,
           'time_min':min(times) if times else None,'time_max':max(times) if times else None,
           'time_count':len(times),'time_unique':len(set(times)),'deltas':dict(deltas),'columns':[]}
        vals=array.array('d'); vals.frombytes(raw)
        for j,name in enumerate(entities+features):
            v=vals[j::cols]; finite=[x for x in v if math.isfinite(x)]
            col={'name':name,'count':len(v),'nonfinite':len(v)-len(finite),
                 'min':min(finite) if finite else None,'max':max(finite) if finite else None,
                 'constant':bool(finite) and min(finite)==max(finite),'sha256':hashlib.sha256(v.tobytes()).hexdigest()}
            if cloud:
                start=int(datetime.datetime(2024,1,23,3,10,tzinfo=datetime.timezone.utc).timestamp())
                end=start+86400
                col['descriptive_bands']=bands(v,times,start,end)
            c['columns'].append(col)
        out['cases'].append(c)
    return out

def csv_summary(z,info):
    csv.field_size_limit(30_000_000)
    out={'rows':0,'ragged':0,'empty_cells':collections.Counter(),'event_ids':collections.Counter(),
         'labels':collections.Counter(),'time_min':None,'time_max':None,'decreasing':0,'equal_adjacent':0,
         'hour_counts':collections.Counter(),'numeric':{},'trace_id_fields':[],'invalid_utf8_bytes':0}
    # Surrogateescape preserves undecodable original bytes; counts are reported.
    # It does not replace or repair text in the dataset.
    with z.open(info) as f,io.TextIOWrapper(f,encoding='utf-8-sig',errors='surrogateescape',newline='') as txt:
        reader=csv.reader(txt); header=next(reader); out['header']=header
        out['trace_id_fields']=[x for x in header if 'trace' in x.lower() or 'span' in x.lower()]
        idx={k:i for i,k in enumerate(header)}; tkey='Time' if 'Time' in idx else 'timeStamp' if 'timeStamp' in idx else None
        numeric_keys=[x for x in ['Latency','is_error','Occurrence'] if x in idx]
        nums={k:{'nonfinite':0,'invalid':0,'min':None,'max':None,'sum':0,'count':0} for k in numeric_keys}
        last=None; kpi_bins=collections.defaultdict(lambda:[0,0])
        for row in reader:
            out['rows']+=1
            out['invalid_utf8_bytes']+=sum(len(BAD_UTF8.findall(cell)) for cell in row)
            if len(row)!=len(header): out['ragged']+=1; continue
            for k,i in idx.items():
                if not row[i]: out['empty_cells'][k]+=1
            if 'EventId' in idx: out['event_ids'][row[idx['EventId']]]+=1
            if 'label' in idx: out['labels'][row[idx['label']]]+=1
            if tkey:
                raw=row[idx[tkey]]
                if tkey=='Time':
                    t=raw; hour=raw[:13]
                else:
                    t=int(raw); sec=t/1e6 if t>1e14 else t/1e3 if t>1e11 else t
                    hour=str(int(sec)//3600)
                if out['time_min'] is None or t<out['time_min']: out['time_min']=t
                if out['time_max'] is None or t>out['time_max']: out['time_max']=t
                if last is not None: out['decreasing']+=t<last; out['equal_adjacent']+=t==last
                last=t; out['hour_counts'][hour]+=1
            for k in numeric_keys:
                s=nums[k]
                try: v=float(row[idx[k]])
                except ValueError: s['invalid']+=1; continue
                if not math.isfinite(v): s['nonfinite']+=1; continue
                s['count']+=1; s['sum']+=v; s['min']=v if s['min'] is None else min(s['min'],v); s['max']=v if s['max'] is None else max(s['max'],v)
                if tkey=='timeStamp':
                    bin_key=(row[idx.get('label',0)],int(sec)); kpi_bins[bin_key][0]+=v; kpi_bins[bin_key][1]+=1
        out['numeric']=nums
        if kpi_bins: out['kpi_second_bins']=len(kpi_bins)
    return out

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--data',required=True); parser.add_argument('--results',required=True);parser.add_argument('--only-cloud-log',action='store_true');parser.add_argument('--reuse-run'); args=parser.parse_args()
    run=pathlib.Path(args.results);run.mkdir(parents=True,exist_ok=False); started=time.monotonic(); selfcheck()
    probe='abc\udc80\udcff\u00e9\udc81'; assert len(BAD_UTF8.findall(probe))==sum(0xDC80<=ord(c)<=0xDCFF for c in probe)==3
    archives=[]; summaries=[]; labels=[]; prior_members={};prior_summaries={}
    if args.reuse_run:
        previous=pathlib.Path(args.reuse_run)
        for a in json.loads((previous/'archives.json').read_text()):
            for m in a['members']: prior_members[(a['path'],m['name'])]=m
        for s in json.loads((previous/'summaries.json').read_text()): prior_summaries[(s['archive'],s['member'])]=s
        labels=json.loads((previous/'labels.json').read_text())
    for path in sorted(pathlib.Path(args.data).rglob('*.zip')):
        if args.only_cloud_log and not ('Cloud_Computing' in str(path) and 'Log Data' in str(path)): continue
        astart=time.monotonic(); z=zipfile.ZipFile(path); archive={'path':str(path),'zip_bytes':path.stat().st_size,'member_count':len(z.infolist()),'members':[]}
        for number,info in enumerate(z.infolist()):
            st=time.monotonic(); row={'name':info.filename,'bytes':info.file_size,'compressed':info.compress_size,'crc':info.CRC,'status':'ok'}
            if info.is_dir(): archive['members'].append(row); continue
            old=prior_members.get((str(path),info.filename));old_summary=prior_summaries.get((str(path),info.filename))
            special='Cloud_Computing' in str(path) and 'Log Data' in str(path) and info.filename.endswith('.npy')
            if old and old['status']=='ok' and old.get('crc_checked') and old_summary and not special:
                row=dict(old,reused_from=args.reuse_run)
                if info.filename.endswith('.csv') and 'invalid_utf8_bytes' not in old_summary:
                    old_summary['invalid_utf8_bytes']=0 # first-run strict UTF-8 decoder previously reached EOF
                summaries.append(old_summary);archive['members'].append(row);continue
            try:
                if info.filename.endswith('.csv'):
                    summary=csv_summary(z,info); summary.update(archive=str(path),member=info.filename); summaries.append(summary)
                elif info.filename.endswith('.npy'):
                    data=z.read(info)
                    summary=npy_summary(data,'Cloud_Computing' in str(path)); summary.update(archive=str(path),member=info.filename); summaries.append(summary)
                    del data
                elif info.filename.endswith('.pptx'):
                    inner=zipfile.ZipFile(io.BytesIO(z.read(info))); slides={}
                    for name in inner.namelist():
                        if name.startswith('ppt/slides/slide') and name.endswith('.xml'):
                            slides[name]=' '.join(ET.fromstring(inner.read(name)).itertext())
                    labels.append({'archive':str(path),'member':info.filename,'slides':slides})
                else:
                    with z.open(info) as f:
                        for block in iter(lambda:f.read(1024*1024),b''): pass
                # ZipExtFile validates CRC on reaching EOF, including CSV/NPY/PPTX reads.
                row['crc_checked']=True
            except Exception as exc:
                row.update(status='error',error_type=type(exc).__name__,error=str(exc) if not isinstance(exc,UnicodeDecodeError) else 'invalid UTF-8 at decoded block offset '+str(exc.start))
                # Parser failure must not be reported as failed ZIP integrity.
                try:
                    with z.open(info) as f:
                        for block in iter(lambda:f.read(1024*1024),b''): pass
                    row['crc_checked']=True
                except Exception as crc_exc: row['crc_error']=repr(crc_exc)
            row['elapsed_seconds']=round(time.monotonic()-st,3); archive['members'].append(row)
            if number%50==0 or info.filename.endswith('.npy'): print(json.dumps({'archive':path.name,'member':info.filename,'status':row['status'],'seconds':row['elapsed_seconds']}),flush=True)
            if number%50==0 or number==len(z.infolist())-1 or info.filename.endswith('.npy'):
                (run/'summaries.json').write_text(json.dumps(summaries,ensure_ascii=True,indent=2),encoding='utf-8')
                (run/'labels.json').write_text(json.dumps(labels,ensure_ascii=False,indent=2),encoding='utf-8')
            (run/'progress.json').write_text(json.dumps({'archive':str(path),'member':info.filename,'completed':number+1,'members':len(z.infolist()),'elapsed':time.monotonic()-started}),encoding='utf-8')
        archive['elapsed_seconds']=round(time.monotonic()-astart,3); archives.append(archive)
        (run/'archives.json').write_text(json.dumps(archives,indent=2),encoding='utf-8')
    result={'elapsed_seconds':round(time.monotonic()-started,3),'maxrss_kb':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'archives':len(archives),
            'bytes_uncompressed':sum(x['bytes'] for a in archives for x in a['members']),
            'crc_checked_members':sum(x.get('crc_checked',False) for a in archives for x in a['members']),
            'errors':[dict(archive=a['path'],**x) for a in archives for x in a['members'] if x['status']!='ok'],
            'methods_run':0,'coverage':'Only PR20211203 and Cloud20240124 preprocessed; Original metadata only'}
    (run/'summary.json').write_text(json.dumps(result,indent=2),encoding='utf-8'); print(json.dumps(result),flush=True)

if __name__=='__main__': main()
