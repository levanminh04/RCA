from pathlib import Path
import json,csv,re,hashlib
ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-020/trung-gian/dataset_evidence'
def read(p):
    assert not p.startswith('data/') and 'locked' not in p.lower() and p!='results/T-010/runs/schema-samples.json'
    return (ROOT/p).read_text(encoding='utf-8-sig')
sources={
 'RCAEval sample schemas':'results/T-002/local-inspection/run-002/schemas.json',
 'SockShop schemas':'results/T-019/inspection/schemas.json',
 'Nezha CSV metadata':'results/T-008/runs/file-audit-001/summary.json',
 'Eadro session metadata':'results/T-009/runs/inspect-004/raw-sessions.json',
 'Deep raw aggregate headers':'results/T-010/runs/inspect-002/raw-cases.json',
 'LEMMA preprocessed metadata':'results/T-011/runs/inspect-008/summaries.json',
 'FSE reduced artifact schemas':'results/T-012/runs/fse-file-inspect-003/schemas.json',
 'AnoMod CSV/JSON metadata':'results/T-012/runs/anomod-file-inspect-003/files.json',
}
output=[]
for family,p in sources.items():
    obj=json.loads(read(p));witness=[]
    def walk(x,key=''):
        if isinstance(x,dict):
            for k,v in x.items():
                pointer=key+'/'+str(k)
                if k in {'schema','columns','headers','header','fields'} and isinstance(v,(str,list,dict)):
                    # Headers/schema only. Do not include values/counters/sample rows.
                    witness.append(dict(key=pointer,schema=v))
                else:walk(v,pointer)
        elif isinstance(x,list):
            for i,v in enumerate(x):walk(v,key+'/'+str(i))
    if 'sample schemas' in family:
        witness=[dict(key='/'+k,schema=v) for k,v in obj.items()]
    else:walk(obj)
    distinct={json.dumps(x['schema'],sort_keys=True,ensure_ascii=False):x for x in witness}
    chosen=sorted(distinct.values(),key=lambda x:x['key'])[:8]
    output.append(dict(family=family,source=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest(),witnesses_available=len(witness),distinct_schema_forms=len(distinct),representative_witnesses=chosen,limit='First8 lexicographic schema forms only; not new payload or measurement sample; no release-quality inference'))
(OUT/'schema-witnesses.json').write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

# Read-only copyedit candidates; root applies and reviews. All replacements preserve numeric strings.
replacements={
 'testlabels':'test labels','testgold':'test gold','37phần':'37 phần','40phần':'40 phần',
 'từng37phần':'từng 37 phần','TX1-test':'TX1-test','Seed20261004':'Seed 20261004',
 'khôngTX2':'không TX2','ởtest':'ở test','giữngoài':'giữ ngoài','v130/60':'v1 30/60',
 '30ca':'30 ca','90ca':'90 ca','125ca':'125 ca','100ca':'100 ca','100/20cells':'100/20 cells',
 '10ô':'10 ô','20ô':'20 ô','30ô':'30 ô','33ô':'33 ô','36ô':'36 ô','52ô':'52 ô',
 '56labelrecords':'56 label records','45labelrecords':'45 label records','45physicalinjections':'45 physical injections',
 '136nhãn':'136 nhãn','52ô':'52 ô','10root':'10 root','12root':'12 root','mộtrepeat':'một repeat',
 'trongA':'trong A','ởB':'ở B','trongB':'trong B','trongC':'trong C','datasetpublic':'dataset public',
 'testNezha':'test Nezha','đãTX1':'đã TX1','đãTX2':'đã TX2','chỉTX0':'chỉ TX0','chỉdev':'chỉ dev','sauG3':'sau G3',
 'sauG1':'sau G1','trướcP3':'trước P3','chạyP3':'chạy P3','kết quảP3':'kết quả P3','thẻD':'thẻ D',
 'ởSS':'ở SS','ởRE3':'ở RE3','ởRE2':'ở RE2','cùngC1':'cùng C1','CSVV2':'CSV V2','bảngV2':'bảng V2',
 'nhánh LEMMAOriginal':'nhánh LEMMA Original','LEMMAOriginal':'LEMMA Original','LEMMAOT':'LEMMA OT','loạiQ47':'loại Q47',
 '26captures':'26 captures','132485trace':'132485 trace','10event':'10 event','8valid':'8 valid','2invalid':'2 invalid',
 'từngô':'từng ô','theoô':'theo ô','từngca':'từng ca','mộtseed':'một seed','ba seed':'ba seed','3seed':'3 seed',
 'phươngpháp':'phương pháp','phươngpháp':'phương pháp','phươngán':'phương án','đầu vào':'đầu vào',
 'không3giờ':'không 3 giờ','tối đa3giờ':'tối đa 3 giờ','vượt3h':'vượt 3h','3giờ':'3 giờ','ởD1':'ở D1','ởD2':'ở D2',
 'từngô/ca':'từng ô/ca','góiA':'gói A','góiB':'gói B','góiC':'gói C','trace0':'trace 0','4/6datecaptures':'4/6 date captures',
 'ngân sáchcóthể':'ngân sách có thể','đãduyệt':'đã duyệt','saucalibrationhợp lệ':'sau calibration hợp lệ',
 'nguồnmetadata':'nguồn metadata','laptopbận':'laptop bận','khôngchạyEC2T020':'không chạy EC2 T020',
 'khôngisolatedprimaryruntime':'không isolated primary runtime','timermethodbody':'timer method body',
 'phảighi':'phải ghi','chưađo':'chưa đo','khácseed':'khác seed','quađêm':'qua đêm','ởmáy':'ở máy',
 'cộngvào3h':'cộng vào 3h','vượtquota':'vượt quota','máy riêng/rảnh':'máy riêng/rảnh',
 'progress/timeout':'progress/timeout','môi trườngghim':'môi trường ghim','phạmviwrite':'phạm vi write',
 'dự kiến>1h':'dự kiến >1h','phảibáo':'phải báo','chờduyệt':'chờ duyệt','theoAGENTS':'theo AGENTS',
 'làđề xuất':'là đề xuất','khôngauthorizationchạy':'không authorization chạy','Khôngnêu':'Không nêu',
 'rủirothờihạn':'rủi ro thời hạn','đánh giáFlashTicket':'đánh giá FlashTicket','nằmP9/P10':'nằm P9/P10',
 'saucùng':'sau cùng','đãghi':'đã ghi','cùngdata':'cùng data','từtrain':'từ train',
 'rootcoverage':'root coverage','methodfidelity':'method fidelity','outputfinite':'output finite',
 'reuse':'reuse','tái lập':'tái lập','lượtT005':'lượt T005','chi phíadapter':'chi phí adapter',
 'officialruntime':'official runtime','officialcost':'official cost','inputvariant':'input variant',
 'mode; detect':'mode; detect','vàmode':'và mode','rootMRR':'root MRR','giữfailure':'giữ failure',
 'vàcandidateabsence':'và candidate absence','vìmethodhỏng':'vì method hỏng','tínhaggregate':'tính aggregate',
 'kiểmfake':'kiểm fake','lọtfeatures':'lọt features','vàsensitivitywindows':'và sensitivity windows',
 'hạn chếP4':'hạn chế P4','lạifixture':'lại fixture','phépthống kê':'phép thống kê',
 'sumCPU':'sum CPU','elapsedwall':'elapsed wall','xuyênca':'xuyên ca','nhântraining':'nhân training',
 'mộtlần/incident':'một lần/incident','projectioncóđiềukiện':'projection có điều kiện','gianca':'gian ca',
 'trungbình':'trung bình','fullTT':'full TT','devthực':'dev thực','tổngkhôngchồnglắp':'tổng không chồng lắp',
 'checktrênmộtca':'check trên một ca','nhiềuconfig':'nhiều config','khôngpercaseprediction':'không per case prediction',
 'mộtfit':'một fit','273metric':'273 metric','khôngđủước lượng':'không đủ ước lượng','actualshapeoperations':'actual shape operations',
 'matrixdày':'matrix dày','T015existingruns':'T015 existing runs','trêndev':'trên dev','trướcquota':'trước quota',
 'đâybenchmarkfullbộ':'đây benchmark full bộ','nhẹ về cơchế':'nhẹ về cơ chế','táchextra':'tách extra',
 'khỏimeasurement':'khỏi measurement','khiP3đo':'khi P3 đo','cầnfitperhệseed':'cần fit per hệ seed',
 'Khôngchiếu':'Không chiếu','normalcao':'normal cao','bằngchứngdetectorready':'bằng chứng detector ready',
 'không liên hệEC2':'không liên hệ EC2','cómetadata':'có metadata','chi phíadapter':'chi phí adapter',
 'normalcalibration':'normal calibration','Cácprojection':'Các projection','thêmseed':'thêm seed','hoặcmethodvariant':'hoặc method variant',
 'GDNfit':'GDN fit','đãcó':'đã có','đặthàng':'đặt hàng','khônglàmviệc':'không làm việc','Cácchi phí':'Các chi phí',
 'phảigiữ':'phải giữ','reproductionvscomparison':'reproduction vs comparison','timingcondition':'timing condition','Normaltrain':'Normal train',
 'test data':'test data','đủtime':'đủ time','thời gianca':'thời gian ca','window/cột/budget cóthể':'window/cột/budget có thể',
 'fullprotocol':'full protocol','khôngkhảthi':'không khả thi','khôngchạyđủ':'không chạy đủ','tốcđộ':'tốc độ',
 'RQ3a/b':'RQ3a/b','42hàng':'42 hàng','111điểm':'111 điểm','10điểm':'10 điểm','giảm mẫu15s':'giảm mẫu 15s',
 'thành225s':'thành 225s','model5tick':'model 5 tick','smoother4tick':'smoother 4 tick','normal720':'normal 720',
 '3600/7200tick':'3600/7200 tick','ở1s':'ở 1s','tại10s':'tại 10s','Kservice5/10':'Kservice 5/10',
 'budget__;':'budget__;','cùnghệ':'cùng hệ','ởhệ':'ở hệ','Thêmnormal':'Thêm normal','dùnglabels':'dùng labels',
 'cùngbudget':'cùng budget','tasknày':'task này','labelbudget':'label budget','modea/b':'mode a/b',
 'chế độa':'chế độ a','chế độb':'chế độ b','root/time test':'root/time test','W-time300s':'W-time 300s',
 'sensitivity600s':'sensitivity 600s','từ300/600':'từ 300/600','trướcscore':'trước score','CIRCA1min':'CIRCA 1min',
 'GDN5tick':'GDN 5 tick','trainingbudget':'training budget','đủfit':'đủ fit','nhìnscore':'nhìn score',
 'thresholdstatistical':'threshold statistical','thiếucoverage':'thiếu coverage','priorwork':'prior work',
 'windoweffect':'window effect','graphgain':'graph gain','prefixranking':'prefix ranking','finalmetrics':'final metrics',
 'ConditionalRerank':'Conditional Rerank','moduleperformance':'module performance','trongKservice':'trong Kservice',
 'thứhạng':'thứ hạng','mẫu số0':'mẫu số 0','32GB':'32GB',
}
files=['results/T-020/g1-goi-quyet-dinh.md','results/T-020/05-nhan-va-cua-so.md','results/T-020/06-phuong-an-dataset-va-chia.md','results/T-020/10-ke-hoach-p3-de-xuat.md']
out=[]
for p in files:
    s=read(p)
    for i,line in enumerate(s.splitlines(),1):
        for old,new in replacements.items():
            if old!=new and old in line:
                assert re.sub(r'\s+','',old)==re.sub(r'\s+','',new),(old,new)
                out.append(dict(path=p,line=i,old=old,new=new,kind='spacing-only candidate; root review/apply',source_file_sha256=hashlib.sha256(s.encode('utf-8')).hexdigest()))
with (OUT/'spacing-fixes.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
print(json.dumps(dict(schema_sources=len(output),spacing_candidates=len(out)),ensure_ascii=False))
