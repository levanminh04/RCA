"""Full streaming Eadro ZIP/TAR inspection; standard library; no model/unpickle."""
import argparse, codecs, collections, csv, datetime, hashlib, io, json, math, re, statistics, tarfile, time, zipfile
from pathlib import Path

class HashReader:
    def __init__(self,src):self.src=src;self.hash=hashlib.sha256()
    def read(self,n=-1):
        b=self.src.read(n);self.hash.update(b);return b
    def readline(self,n=-1):
        b=self.src.readline(n);self.hash.update(b);return b
    def __getattr__(self,k):return getattr(self.src,k)

def array_items(f):
    decoder=json.JSONDecoder(); buf=''; pos=0; eof=False; opened=False; done=False
    while not done:
        if pos >= len(buf)-1 and not eof:
            buf=buf[pos:]+f.read(65536);pos=0;eof=not bool(buf)
        while pos<len(buf) and buf[pos].isspace():pos+=1
        if not opened:
            if pos==len(buf):continue
            assert buf[pos]=='[';pos+=1;opened=True;continue
        if pos<len(buf) and buf[pos]==',':pos+=1;continue
        if pos<len(buf) and buf[pos]==']':done=True;pos+=1;break
        try: val,end=decoder.raw_decode(buf,pos)
        except json.JSONDecodeError:
            more=f.read(65536)
            if not more:raise
            buf=buf[pos:]+more;pos=0;continue
        yield val;pos=end
    assert not (buf[pos:]+f.read()).strip(), 'trailing array payload'

def trace_scan(src):
    counts=collections.Counter(); services=collections.Counter(); edges=collections.Counter(); keys={}; refs=[]; traceids=set(); clocks=[]; schemas=collections.Counter(); latency=collections.defaultdict(list)
    for tr in array_items(codecs.getreader('utf-8')(src)):
        counts['trace_records']+=1;traceids.add(tr.get('traceID')); ps=tr.get('processes',{});schemas[tuple(sorted(tr))]+=1
        for s in tr.get('spans',[]):
            counts['spans']+=1;tid=s.get('traceID');sid=s.get('spanID');key=(tid,sid)
            svc=ps.get(s.get('processID'),{}).get('serviceName','MISSING'); services[svc]+=1
            if not tid or not sid:counts['null_ids']+=1
            signature=hashlib.sha256(json.dumps([svc,s],sort_keys=True,separators=(',',':')).encode()).digest()
            if key in keys:
                counts['duplicate_keys']+=1;old=keys[key];conflict=old[3] or old[2]!=signature;counts['duplicate_conflicting_rows']+=old[2]!=signature;keys[key]=(old[0]+1,svc,old[2],conflict)
            else:keys[key]=(1,svc,signature,False)
            st=s.get('startTime');dur=s.get('duration');
            if isinstance(st,(int,float)) and isinstance(dur,(int,float)):
                clocks.extend((st,st+dur));counts['negative_duration']+=dur<0;latency[svc].append((st/1e6,dur))
            else:counts['invalid_clock']+=1
            parent=[r for r in s.get('references',[]) if r.get('refType')=='CHILD_OF']
            if not parent:counts['root_no_CHILD_OF']+=1
            else:
                counts['span_parent_required']+=1;counts['span_multiple_parents']+=len(parent)>1
                for r in parent:refs.append((r.get('traceID'),r.get('spanID'),svc,st/1e6 if isinstance(st,(int,float)) else None))
            counts['status_error_tag']+=any(t.get('key')=='error' and t.get('value') is True for t in s.get('tags',[]))
    edge_times=[]
    for tid,sid,svc,ts in refs:
        counts['parent_references']+=1;k=keys.get((tid,sid))
        if k is None:counts['parent_missing']+=1
        elif k[0]!=1:counts['parent_ambiguous']+=1
        else:
            counts['parent_unique']+=1
            if k[1]!=svc:edges[(k[1],svc)]+=1;edge_times.append((ts,k[1],svc))
        if k is not None and not k[3]:
            counts['parent_unique_identity']+=1
            if k[0]!=1 and k[1]!=svc:edges[(k[1],svc)]+=1;edge_times.append((ts,k[1],svc))
        elif k is not None:counts['parent_conflicting_identity']+=1
    assert counts['parent_references']==counts['parent_unique']+counts['parent_missing']+counts['parent_ambiguous']
    counts['conflicting_span_keys']=sum(v[3] for v in keys.values())
    return dict(counts=dict(counts),trace_ids=len(traceids),unique_span_keys=len(keys),services=dict(services),time_min_us=min(clocks) if clocks else None,time_max_us=max(clocks) if clocks else None,schemas=[dict(keys=list(k),count=v) for k,v in schemas.items()],service_edges=[dict(parent=k[0],child=k[1],count=v) for k,v in sorted(edges.items())]), keys,traceids,edge_times,latency

def log_scan(src,keys,traceids):
    x=json.load(src);out=[]
    for svc,lines in x.items():
        counts=collections.Counter();levels=collections.Counter();clocks=[];prev=None;schema=type(lines).__name__
        for line in lines:
            counts['lines']+=1
            mt=re.match(r'(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\.\d+)',line)
            if mt:stamp=mt.group(1)
            else:
                mt=re.match(r'\[(\d{4}-[A-Za-z]{3}-\d\d \d\d:\d\d:\d\d\.\d+)\]',line);stamp=mt.group(1) if mt else None
            if stamp:
                fmt='%Y-%m-%d %H:%M:%S.%f' if '-' in stamp[:7] and stamp[5:7].isdigit() else '%Y-%b-%d %H:%M:%S.%f'
                ts=datetime.datetime.strptime(stamp,fmt).replace(tzinfo=datetime.timezone.utc).timestamp();clocks.append(ts);counts['descending_adjacent']+=prev is not None and ts<prev;prev=ts
            else:counts['no_parsed_timestamp']+=1
            m=re.search(r'Span reported: ([0-9a-f]+):([0-9a-f]+):([0-9a-f]+):',line)
            if m:counts['payload_trace_id']+=1;counts['trace_matches']+=m[1] in traceids;counts['span_matches']+=(m[1],m[2]) in keys
            m=re.search(r'\b(TRACE|DEBUG|INFO|WARN|ERROR)\b|<(trace|debug|info|warning|error)>',line)
            if m:levels[(m[1] or m[2]).upper()]+=1
        out.append(dict(service=svc,container=schema,counts=dict(counts),levels=dict(levels),time_min_assuming_UTC=min(clocks) if clocks else None,time_max_assuming_UTC=max(clocks) if clocks else None,trace_id_column=False))
    return out

def metric_scan(src,service):
    rr=csv.DictReader(codecs.getreader('utf-8-sig')(src));columns=rr.fieldnames;rows=[];gaps=collections.Counter();bad=collections.Counter();seen=set();dups=0;prev=None
    for r in rr:
        ts=float(r['timestamp']);dups+=ts in seen;seen.add(ts)
        if prev is not None:gaps[str(ts-prev)]+=1
        prev=ts;values={}
        for k in columns:
            if k=='timestamp':continue
            try:v=float(r[k])
            except (ValueError,TypeError):bad[k]+=1;v=None
            if v is not None and not math.isfinite(v):bad[k]+=1;v=None
            values[k]=v
        rows.append((ts,values))
    channels={k:dict(nonfinite_or_invalid=bad[k],constant=len({r[1][k] for r in rows if r[1][k] is not None})<=1) for k in columns if k!='timestamp'}
    return dict(service=service,rows=len(rows),columns=columns,time_min=min(seen) if seen else None,time_max=max(seen) if seen else None,duplicate_timestamp=dups,delta_histogram=dict(gaps),channels=channels),rows

def quantile(xs,q):
    ys=sorted(xs);p=(len(ys)-1)*q;lo=math.floor(p);hi=math.ceil(p);return ys[lo]+(ys[hi]-ys[lo])*(p-lo)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--data',required=True);ap.add_argument('--out',required=True);a=ap.parse_args();out=Path(a.out);out.mkdir(parents=True,exist_ok=False);started=time.monotonic()
    results=[];inventory=[];labels=[];metrics={};edges={};hashes=[];pending=[]
    def case_result(dataset,origin,case):
        r=next((r for r in results if r['dataset']==dataset and r['origin']==origin and r['case']==case),None)
        if r is None:r=dict(dataset=dataset,origin=origin,case=case);results.append(r)
        return r
    def finish_logs():
        for dataset,origin,case,blob in pending:
            ck=dataset+'|'+origin+'|'+case;keys,tids=contexts.get(ck,({},set()));case_result(dataset,origin,case)['logs']=log_scan(io.BytesIO(blob),keys,tids)
        pending.clear()
    def scan(name,src,size,dataset,origin):
        src=HashReader(src)
        digest=hashlib.sha256();blob=src.read() if name.endswith(('fault.json','metadata.json')) or '.fault-' in name else None
        if blob is not None:
            digest.update(blob);r=json.loads(blob)
            if '.fault-' in name:labels.append(dict(dataset=dataset,member=name,origin=origin,label=r))
            inventory.append(dict(dataset=dataset,origin=origin,member=name,bytes=size,sha256=digest.hexdigest(),metadata=r));return
        # Raw files are read to EOF by parsers, including ZIP CRC. Container/member
        # hashes are separately streamed below for complete integrity coverage.
        case=name.split('/spans.json')[0] if name.endswith('/spans.json') else name.split('/logs.json')[0] if name.endswith('/logs.json') else name.split('/metrics/')[0]
        ck=dataset+'|'+origin+'|'+case
        if name.endswith('/spans.json'):
            t,keys,tids,ee,lat=trace_scan(src);case_result(dataset,origin,case)['trace']=t;contexts[ck]=(keys,tids);edges[ck]=ee;print('trace',name,t['counts']['spans'],flush=True)
        elif name.endswith('/logs.json'):
            # TAR normally orders spans first; ZIP caller also explicitly does so.
            pending.append((dataset,origin,case,src.read()))
        elif '/metrics/' in name and name.endswith('.csv'):
            m,v=metric_scan(src,Path(name).stem);case_result(dataset,origin,case).setdefault('metrics',[]).append(m);metrics.setdefault(ck,{})[m['service']]=v
        else:
            for chunk in iter(lambda:src.read(1024*1024),b''):digest.update(chunk)
            inventory.append(dict(dataset=dataset,origin=origin,member=name,bytes=size,sha256=digest.hexdigest(),decoded=False));return
        inventory.append(dict(dataset=dataset,origin=origin,member=name,bytes=size,parsed=True,sha256=src.hash.hexdigest()))
    for f in sorted(Path(a.data).rglob('*.zip')):
        dataset='SN' if f.name.startswith('SN') else 'TT';contexts={}
        with zipfile.ZipFile(f) as z:
            valid=[i for i in z.infolist() if not i.is_dir() and '__MACOSX' not in i.filename and not Path(i.filename).name.startswith('.')]
            plain=[i for i in valid if not i.filename.endswith(('.xz','.txz','.tgz'))]
            plain.sort(key=lambda i:(0 if '/spans.json' in i.filename else 1,i.filename))
            for i in plain:
                with z.open(i) as src:scan(i.filename,src,i.file_size,dataset,'outer')
            finish_logs()
            for i in valid:
                if not i.filename.endswith(('.xz','.txz','.tgz')):continue
                contexts={};origin=i.filename
                with z.open(i) as src, tarfile.open(fileobj=src,mode='r|*') as tar:
                    for member in tar:
                        if not member.isfile():continue
                        child=tar.extractfile(member)
                        with child:scan(member.name,child,member.size,dataset,origin)
                    # force compressed parent to EOF for CRC/truncation check
                    while src.read(1024*1024):pass
                finish_logs()
                print('nested complete',origin,flush=True)
            bad=z.testzip();assert bad is None
        hashes.append(dict(archive=str(f),all_zip_members_crc_ok=True,bytes=f.stat().st_size))
    # Match fault label file/session by the neutral release session identifier.
    faults=[];normal=[];seenlabels=set()
    for l in labels:
        rec=l['label'];session=Path(l['member']).name.replace('.fault-','.').removesuffix('.json')
        if not rec.get('faults') and (l['dataset'],session) not in normal:normal.append((l['dataset'],session))
        for fault in rec.get('faults',[]):
            key=(l['dataset'],session,json.dumps(fault,sort_keys=True))
            if key not in seenlabels:faults.append(dict(dataset=l['dataset'],session=session,record=fault));seenlabels.add(key)
    root_positions=[]
    for r in results:
        ck=r['dataset']+'|'+r['origin']+'|'+r['case'];session=Path(r['case']).name
        for fault in [x for x in faults if x['dataset']==r['dataset'] and x['session']==session]:
            ff=fault['record'];rawroot=ff.get('name',ff.get('service',ff.get('container','')));root=rawroot.removeprefix('dockercomposemanifests_').removesuffix('_1') if r['dataset']=='TT' else rawroot.removeprefix('socialnetwork-').removesuffix('-1')
            # Source labels use keys name/start/duration; preserve any unsupported format.
            fs=ff.get('start');dur=ff.get('duration');pairs={(u,v) for ts,u,v in edges.get(ck,[]) if fs is not None and ts is not None and fs<=ts<=fs+dur}
            root_positions.append(dict(dataset=r['dataset'],case=r['case'],raw_label=ff,root=root,root_present_in_trace=root in r['trace']['services'],interval_edges=len(pairs),in_degree=len({u for u,v in pairs if v==root}),out_degree=len({v for u,v in pairs if u==root}),alias_verified=False if root=='nginx-thrift' else True))
    # Quantile probes on metrics only. First no-fault session supplies reference;
    # remaining no-fault sessions are controls. No clock correction or epsilon.
    probes=[];refs={};reference_ids={}
    for dataset in ('SN','TT'):
        ids=sorted(ck for ck in metrics if ck.startswith(dataset+'|') and any(ds==dataset and sess==Path(ck.split('|',2)[2]).name for ds,sess in normal))
        ids=list({Path(ck.split('|',2)[2]).name:ck for ck in ids}.values())
        if not ids:continue
        reference_ids[dataset]=ids[0];refs[dataset]=metrics[ids[0]]
        thresholds={}
        for svc,rs in refs[dataset].items():
            for ch in rs[0][1] if rs else []:
                xs=[v[ch] for _,v in rs if v[ch] is not None]
                if not xs:continue
                med=statistics.median(xs);dev=[abs(x-med) for x in xs]
                thresholds[(svc,ch)]=(med,{q:quantile(dev,q) for q in (.95,.99,.995)},len(xs))
        periods=[(ck,None,None,'normal-control',None) for ck in ids[1:]]
        observed_sessions=set()
        for ck in sorted(metrics,key=lambda x:(x.split('|')[1]!='outer',x)):
            if not ck.startswith(dataset+'|'):continue
            session=Path(ck.split('|',2)[2]).name
            if session in observed_sessions:continue
            observed_sessions.add(session)
            for f in faults:
                if f['dataset']==dataset and f['session']==session:
                    ff=f['record'];st=ff.get('start');du=ff.get('duration')
                    if st is not None and du is not None:periods.append((ck,st,st+du,'injection',ff))
        for ck,st,en,regime,ff in periods:
            for svc,rs in metrics[ck].items():
                for ch in rs[0][1] if rs else []:
                    base=thresholds.get((svc,ch))
                    if base is None:continue
                    med,qs,nref=base;xs=[v[ch] for ts,v in rs if (st is None or st<=ts<=en) and v[ch] is not None]
                    for q,band in qs.items():probes.append(dict(dataset=dataset,case=ck,service=svc,channel=ch,regime=regime,label=ff,q=q,reference=reference_ids[dataset],reference_n=nref,n=len(xs),median=med,band=band,zero_band=band==0,exceed=sum(abs(x-med)>band for x in xs)))
    summary=dict(raw_sessions=len(results),sessions_by_dataset=dict(collections.Counter(r['dataset'] for r in results)),spans=sum(r['trace']['counts']['spans'] for r in results),labels=len(faults),labels_by_dataset=dict(collections.Counter(x['dataset'] for x in faults)),normal_label_sessions=len(normal),zip_archives_crc=hashes,inventory_members=len(inventory),probe_rows=len(probes),elapsed_seconds=round(time.monotonic()-started,3),no_model_execution=True,note='native clocks retained; no-fault reference/control is descriptive, not design decision; all final members are raw CSV/JSON; all archives duplicate raw; no model')
    for name,value in [('raw-sessions',results),('nested-inventory',inventory),('labels-all',labels),('root-positions',root_positions),('symptom-metrics',probes),('summary',summary)]:
        (out/(name+'.json')).write_text(json.dumps(value,indent=2),encoding='utf-8')
    print(json.dumps(summary),flush=True)

if __name__=='__main__':main()
