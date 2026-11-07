"""Nguồn thật cho chuẩn bị: hash/schema/timestamp; không gọi RCA hoặc ghép điểm với nhãn."""
from pathlib import Path
import sys,json,csv,hashlib,zipfile,datetime as dt,collections,time,io
ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=Path(__file__).resolve().parent
sys.path[:0]=[str(OUT/'scripts'),str(ROOT/'src'),str(ROOT/'results/T-052/scripts')]
from bien_nhan import *
from nguon import compare_sources
from p3 import nezha
from m1 import quan_sat
import pyarrow.parquet as pq
import numpy as np
PRIVATE=Path('D:/RCA-ext/private/T-054/prepare-main-006')
def load(path):return json.loads(Path(path).read_bytes())
def relpin(path):
    p=ref(path)
    if Path(path).resolve().is_relative_to(ROOT):p['path']=Path(path).resolve().relative_to(ROOT).as_posix()
    return p
def check(path,pin):
    assert digest(path)==pin['sha256'],str(path)
    if 'bytes'in pin:assert Path(path).stat().st_size==pin['bytes'],str(path)
def git_digest(path):
    h=hashlib.sha1(b'blob '+str(Path(path).stat().st_size).encode()+b'\0')
    with Path(path).open('rb')as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def temporal(path,cols):return pq.read_table(path,columns=cols).to_pandas()
def tt_temporal_evidence(files,t,contract):
    # Cùng định nghĩa timestamp, F và miền cắt của m1.adapter; không đọc giá trị metric/log/operation.
    mt=temporal(ROOT/files['metrics.parquet']['path'],['time'])['time'].to_numpy(np.int64)
    tr=temporal(ROOT/files['traces.parquet']['path'],['startTime','duration']);st=tr['startTime'].to_numpy(np.int64);en=st+tr['duration'].to_numpy(np.int64)
    lg=temporal(ROOT/files['logs.parquet']['path'],['timestamp'])['timestamp'].to_numpy(float)
    assert len(mt)and len(st)and len(lg)and np.isfinite(lg).all()
    center=(t-300)*10**9;lo=center-300*10**9;hi=center+300*10**9
    series={'metric':mt*10**9,'trace':en[(st>=lo//1000)&(en<hi//1000)]*1000,
            'log':np.rint(lg[(lg>=lo/10**9)&(lg<hi/10**9)]*10**9).astype(np.int64)}
    full={'metric':(int(mt.min())*10**9,int(mt.max())*10**9),'trace':(int(en.min())*1000,int(en.max())*1000),
          'log':(int(round(float(lg.min())*10**9)),int(round(float(lg.max())*10**9)))}
    evidence={};reasons=[]
    for kind in series:
        key={'metric':'RE2-TT metric','trace':'RE2-TT span','log':'RE2-TT log'}[kind]
        r=int(round(contract['quan_sat']['do_phan_giai_r'][key]*10**9));a,b=full[kind]
        q=quan_sat.tinh_nguon([(a,b+r)],[int(v)for v in series[kind]],r,(lo,hi),{'N':(lo,center),'A':(center,hi)},o_s=10*10**9)
        evidence[kind]=q
        if a>lo or b+r<hi:reasons.append(kind+':F_does_not_cover_requested_history')
        if not len(series[kind])or any(q['o'][side].get('OPEN',0)>0 for side in ['N','A']):reasons.append(kind+':A0_observation_not_supported_through_window')
    return {'status':'insufficient'if reasons else'verified','reason':reasons,'window_ns':[lo,center,hi],
            'coverage':evidence,'scope':'Temporal source support/A0 only, not healthy baseline or method output; boundary cells retained as defined in quan_sat.'}

def main():
    started=time.monotonic();PRIVATE.mkdir(parents=True,exist_ok=True)
    protocol=load(OUT/'protocol.json');cohort=read_pin(protocol['cohorts_source']);g1=cohort['G1_source'];check(ROOT/g1['path'],g1)
    split=list(csv.DictReader((ROOT/g1['path']).open(encoding='utf-8-sig')))
    selected={ds:[r for r in split if r['dataset']==ds and r['vai_tro']=='test']for ds in ['RE2-TT','Nezha-OB']}
    for ds,rows in selected.items():assert set(fingerprint([ds,r['case']])for r in rows)==set(cohort['cohorts'][ds]['members_locked_sha256'])
    hfman=load(ROOT/'results/T-002/public-metadata/run-002/source-manifest.json');hf={};source_pins={'G1':g1}
    for f in (ROOT/'results/T-002/public-metadata/run-002/sources').glob('hf-tree-page-*.json'):
        check(f,next(x for x in hfman if x['artifact']=='sources/'+f.name));hf.update({x['path']:x for x in load(f)})
    zpath=Path('D:/RCA-ext/dl/torai-data.zip')
    assert zpath.stat().st_size==91262227 and digest(zpath)=='040dbae0d8740399371945837e34590ca7f8626e63aa23bbc287d165b8ff7c76'
    source_pins['author_archive']=ref(zpath);source_pins['author_archive_original_receipt']=relpin(ROOT/'results/T-005/runs/04-tai-torai-zip.log')
    inventory=load(OUT/'runs/trien-khai-005/local-TT60-inventory.json');inv={x['path']:x for x in inventory['files']}
    contract=read_pin(protocol['m1_contract_ref']);ttrows={};ttevidence={};authorrows={};author_bytes=0;tt_injections={}
    author_base=PRIVATE/'author-A'
    if (PRIVATE/'A-author-source.json').exists():
        author=ref(PRIVATE/'A-author-source.json');adoc=read_pin(author);assert adoc['archive_ref']==ref(zpath)
        tt_injections=load(PRIVATE/'TT-injection-source-metadata.json');ttevidence=load(PRIVATE/'TT-Ce-temporal-evidence.json')
        authorrows=adoc['cases_by_member']
        for r in selected['RE2-TT']:
            case=r['case'];member=fingerprint(['RE2-TT',case]);oid='test-'+member[:10]
            files={fn:{k:inv['data/locked/rcaeval-re2tt-60/'+case+'/'+fn][k]for k in ['path','bytes','sha256']}for fn in ['metrics.parquet','traces.parquet','logs.parquet']}
            for meta in files.values():check(ROOT/meta['path'],meta)
            ttrows[oid]=dict(member_sha256=member,files=files,t=tt_injections[member]['t'],ce_history=ttevidence[oid]['status'])
            for meta in authorrows[member]['files'].values():check(author_base/meta['path'],meta);author_bytes+=meta['bytes']
    else:
        author_base=PRIVATE/'author-A';author_base.mkdir()
        with zipfile.ZipFile(zpath)as z:
            for r in selected['RE2-TT']:
                case=r['case'];member=fingerprint(['RE2-TT',case]);oid='test-'+member[:10];folder,rep=case.removeprefix('re2tt_').rsplit('_',1);prefix='torai-TT/'+folder+'/'+rep+'/'
                b=z.read(prefix+'inject_time.txt');origin=hf[case+'/inject_time.txt']
                assert len(b)==origin['size']and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==origin['oid']
                t=int(b.decode().strip());tt_injections[member]={'t':t,'HF_path':origin['path'],'HF_git_oid':origin['oid'],'zip_member':prefix+'inject_time.txt','sha256':hashlib.sha256(b).hexdigest()}
                files={}
                for fn in ['metrics.parquet','traces.parquet','logs.parquet']:
                    rel='data/locked/rcaeval-re2tt-60/'+case+'/'+fn;pin=inv[rel];check(ROOT/rel,pin)
                    entry=hf[case+'/'+fn];assert pin['sha256']==entry['lfs']['oid']and pin['bytes']==entry['size']
                    files[fn]={k:pin[k]for k in ['path','bytes','sha256']}
                evidence=tt_temporal_evidence(files,t,contract);ttevidence[oid]=evidence
                ttrows[oid]=dict(member_sha256=member,files=files,t=t,ce_history=evidence['status'])
                authorfiles={}
                for name in ['logts','tracets_err','tracets_lat']:
                    rel=folder+'/'+rep+'/'+name+'.csv';dst=author_base/rel;dst.parent.mkdir(parents=True,exist_ok=True)
                    b=z.read(prefix+name+'.csv');dst.write_bytes(b)
                    with dst.open(encoding='utf-8-sig',newline='')as f:header=next(csv.reader(f))
                    assert header and'time'in header and len(header)==len(set(header)),name
                    authorfiles[name]=dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest());author_bytes+=len(b)
                authorrows[member]={'files':authorfiles}
        atomic(PRIVATE/'TT-injection-source-metadata.json',tt_injections)
        atomic(PRIVATE/'TT-Ce-temporal-evidence.json',ttevidence)
        author=atomic(PRIVATE/'A-author-source.json',dict(schema='T054-TORAI-A-SOURCE-1',dataset='RE2-TT',g1_revision=g1['sha256'],data_root=str(author_base),
            grant=relpin(RUN/'preparation-grant.json'),archive_ref=ref(zpath),cases_by_member=authorrows))
    print(json.dumps({'TT_sources':len(ttrows),'A_CSV':180,'A_bytes':author_bytes,'Ce':dict(collections.Counter(x['ce_history']for x in ttrows.values()))}),flush=True)

    # Nguồn OB độc lập: cây Git revision đã pin + fault_list native đã lưu, không lấy mốc từ runtime tự khai.
    t003=load(ROOT/'results/T-003/source-manifest.json');t8pin=next(x for x in t003['manifests']if x['task']=='T-008');check(ROOT/t8pin['path'],t8pin)
    t8=load(ROOT/t8pin['path']);native_labels={};tree=None
    for item in t8['sources']:
        f=ROOT/'results/T-008'/item['path'];check(f,item)
        if item['path'].endswith('fault_list.json')and any(d in item['path']for d in ['2022-08-22','2022-08-23']):
            for hour,events in load(f).items():
                for event in events:
                    pod=event['inject_pod'];svc=nezha.POD_ALIASES[pod]
                    case='OB|'+svc+'|'+event['inject_type']+'|'+event['inject_time'];assert case not in native_labels
                    native_labels[case]={'event':event,'source':relpin(f),'hour':hour}
        if 'tree'in item['path']:
            value=load(f)
            if isinstance(value,dict)and'tree'in value:tree={x['path']:x for x in value['tree']if x['type']=='blob'}
    assert tree is not None
    source_pins['Nezha_metadata_manifest']=t8pin
    obrows={};obsource={};verified_files={};schema_errors=[]
    for r in selected['Nezha-OB']:
        case=r['case'];native=native_labels[case];event=native['event'];t=int(dt.datetime.strptime(event['inject_time'],'%Y-%m-%d %H:%M:%S').replace(tzinfo=dt.timezone.utc).timestamp());day=event['inject_time'][:10]
        # mốc chính inject_time, không đổi sang inject_timestamp của độ nhạy lịch sử.
        names=['rca_data/'+day+'/metric/'+n for n in ['front_service.csv']+[pod+'_metric.csv'for pod in nezha.POD_ALIASES]if 'rca_data/'+day+'/metric/'+n in tree]
        assert len(names)==11
        # Giữ đúng nguồn ba minute-file của baseline Q85/T026; không mở rộng thành 11 file theo cửa sổ.
        for minute in range(t//60,t//60+3):
            hhmm=dt.datetime.fromtimestamp(minute*60,dt.timezone.utc).strftime('%H_%M')
            for kind in ['trace','log']:names.append('rca_data/'+day+'/'+kind+'/'+hhmm+'_'+kind+'.csv')
        files={}
        for name in names:
            rel='data/ngoai-rcaeval/nezha/online-boutique/'+name;path=ROOT/rel;origin=tree[name]
            if rel not in verified_files:
                assert path.is_file()and path.stat().st_size==origin['size'],rel
                assert git_digest(path)==origin['sha'],rel
                pin=ref(path);verified_files[rel]=dict(path=rel,bytes=pin['bytes'],sha256=pin['sha256'])
                with path.open(encoding='utf-8-sig',newline='')as f:header=next(csv.reader(f))
                expected={'metric':['Time','ServiceName'if path.name=='front_service.csv'else'PodName'],
                    'trace':['TraceID','SpanID','ParentID','PodName','OperationName','StartTimeUnixNano','EndTimeUnixNano','Duration'],
                    'log':['Timestamp','TimeUnixNano','PodName','Log']}[path.parent.name]
                # Log tên cột chính xác lấy từ reader đang dùng; đối chiếu bên dưới.
                assert set(expected)<=set(header),(path.name,header)
            files[rel]=verified_files[rel]
        member=fingerprint(['Nezha-OB',case]);oid='test-'+member[:10]
        row=dict(member_sha256=member,files=files,t_ns=t*10**9,trace_guard_s={'2022-08-22':41,'2022-08-23':32}[day])
        nezha._validate_case(dict(row,opaque_id='dev-0000000000'))
        obrows[oid]=row;obsource[member]={'native_source':native['source'],'hour':native['hour'],'inject_time':event['inject_time'],'Git_revision':t8['revision'],'paths':names}
    atomic(PRIVATE/'OB-native-source-evidence.json',obsource);atomic(PRIVATE/'OB-file-source-pins.json',verified_files)
    print(json.dumps({'OB_sources':len(obrows),'OB_unique_files':len(verified_files),'OB_unique_bytes':sum(v['bytes']for v in verified_files.values())}),flush=True)

    runtime_refs={};original_refs={};prep_receipts={};sources={'RE2-TT':ttrows,'Nezha-OB':obrows}
    # Quản lý metadata giữ map/nhãn riêng; method không được gọi ở đây.
    for ds,cases in sources.items():
        key='TT'if ds=='RE2-TT'else'OB'
        runtime=dict(dataset=ds,g1_revision=g1['sha256'],inventory=cohort['inventory'][ds],cases=cases)
        independent=dict(schema='P7-CASE-SOURCE-001',dataset=ds,g1_revision=g1['sha256'],cases_by_member={r['member_sha256']:r for r in cases.values()},
            provenance={'G1':g1,'HF_revision':'afeacb11bcc94dadfd1c8f483ee4377b2b8b614e'if ds=='RE2-TT'else None,
             'source_proof':relpin(PRIVATE/('TT-injection-source-metadata.json'if ds=='RE2-TT'else'OB-native-source-evidence.json'))})
        rp=atomic(PRIVATE/(key+'-runtime.json'),runtime);ip=atomic(PRIVATE/(key+'-independent-source.json'),independent)
        compare_sources(read_pin(rp),read_pin(ip),ds,g1['sha256'])
        from p7_guard_v3 import _case_binding
        hashes={oid:_case_binding(ds,row)for oid,row in cases.items()}
        prep=atomic(PRIVATE/(key+'-preparation-binding.json'),dict(schema='P7-PREPARATION-BINDING-001',dataset=ds,protocol_sha256=ref(OUT/'protocol.json')['sha256'],runtime_sha256=rp['sha256'],private_source_sha256=ip['sha256'],cases=hashes,
            status='SOURCE_CHECKED_NOT_G3_RUNTIME_ATTESTATION',main_allowed=False))
        runtime_refs[ds]=rp;original_refs[ds]=ip;prep_receipts[ds]=prep
    result=dict(PASS=True,runtime_refs=runtime_refs,independent_source_refs=original_refs,preparation_binding_refs=prep_receipts,author_source_ref=author,
        cohort_counts={ds:len(v)for ds,v in sources.items()},TT_files=180,TT_bytes=1309388082,A_csv_files=180,A_csv_bytes=author_bytes,
        OB_unique_files=len(verified_files),OB_unique_bytes=sum(v['bytes']for v in verified_files.values()),
        Ce_support=dict(collections.Counter(x['ce_history']for x in ttrows.values())),source_pins=source_pins,
        telemetry_access='TT timestamp columns/schema only; OB opaque bytes+CSV header only; author ZIP exact cohort3CSV extracted/header only. No RCA/score.',
        G3=False,main_started=False,labels_joined=False,elapsed_s=time.monotonic()-started)
    atomic(RUN/'checkpoint-01-sources.json',result)
    with (ROOT/'tasks/T-054-khoa-g3-chay-p7-a/LOG.md').open('ab')as f:f.write(('\nCheckpoint phần1 nguồn: TT60/OB34 đúng G1 và cohort; TT180hashHF, t từinject_time trong zip tác giả khớpGitblobHF. A180CSV giải nén đúng ca từzip đãpin, không tải mới; OB sourcebytes/Gitblob và mốc native xác minh. C-e phân loại từtimestamp/A0, không chạyM1 hoặc suy khỏe. Nguồn private tách khỏi phương pháp; receipt chuẩn bị không giả G3/attest runtime chính. Chi tiết checkpoint-01-sources.json; chưa chạy/chấm.\n').encode())
    print(json.dumps({k:v for k,v in result.items()if k in ['PASS','cohort_counts','A_csv_files','A_csv_bytes','OB_unique_files','Ce_support','elapsed_s']}))
if __name__=='__main__':
    try:main()
    except BaseException as e:
        import traceback
        atomic(RUN/'sources-failure-r3.json',{'type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()});raise
