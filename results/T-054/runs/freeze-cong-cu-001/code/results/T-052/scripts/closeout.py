"""Lập báo cáo/hồ sơ từ kết quả, không tạo thêm quyết định khoa học."""
import csv,hashlib,json,pathlib,re,sys,time
from collections import Counter
from datetime import datetime,timezone
from common import ROOT,RUN,read,save,digest,dump,metadata
from m1_danh_gia import pha2
from p3 import nezha

def md(path,text):
    with (ROOT/path).open('x',encoding='utf-8',newline='\n') as f:f.write(text.rstrip()+'\n')

def main():
    data=pha2.giai_ma_json(read('results/T-052/ket-qua-dev.json'))
    rc=pha2.giai_ma_json(read('results/T-052/vung-ce-va-vi-tri-001.json'))
    entries,base,lineage=metadata()
    config={k:base[k] for k in ('bat_tat','nhanh_z','che_do','tham_so_E4','tham_so_E3','tham_so_E5')}
    config['tach_cd3']=True
    fingerprint=hashlib.sha256(dump(config).encode()).hexdigest()
    code={p.relative_to(ROOT).as_posix():digest(p) for folder in ['src/m1','src/m1_danh_gia','src/p3']
          for p in (ROOT/folder).glob('*.py')}
    code.update({p.relative_to(ROOT).as_posix():digest(p) for p in (ROOT/'results/T-052/scripts').glob('*.py')})
    with (ROOT/'results/T-021/chia-theo-o/A-phan-tang.csv').open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f))
    cohorts={}
    for ds in ('RE2-TT','Nezha-OB','RE3-OB'):
        wanted='giu-ngoai' if ds=='RE3-OB' else 'test'
        chosen=[r for r in rows if r['dataset']==ds and r['vai_tro']==wanted]
        members=[hashlib.sha256(json.dumps([ds,r['case']],ensure_ascii=False,separators=(',',':')).encode()).hexdigest() for r in chosen]
        assert len(set(members))==len(members)
        devcells={(r['root'],r['fault']) for r in rows if r['dataset']==ds and r['vai_tro']=='dev'}
        assert not devcells & {(r['root'],r['fault']) for r in chosen}
        cohorts[ds]={'n':len(chosen),'cells':len({(r['root'],r['fault']) for r in chosen}),
                     'members_locked_sha256':members,'TX':Counter(r['tx'] for r in chosen),
                     'symptom_probe_metadata':Counter(r['probe_trieu_chung'] for r in chosen)}
    assert [(cohorts[d]['n'],cohorts[d]['cells']) for d in ('RE2-TT','Nezha-OB','RE3-OB')]==[(60,20),(34,20),(30,10)]
    plan={'status':'DESIGN_AND_FIXTURE_ONLY_NOT_RUNTIME_ALLOWLIST','G1_source':{'path':'results/T-021/chia-theo-o/A-phan-tang.csv','sha256':digest('results/T-021/chia-theo-o/A-phan-tang.csv')},
          'cohorts':cohorts,'opaque_rule':'test- + first10(SHA256(UTF8 JSON [dataset, G1 case], compact separators)); kiểm không trùng trước dùng',
          'runtime_allowlist_materialized':False,'private_labels_materialized':False,
          'private_map_location':'OPEN: chốt đường dẫn trong SPEC P7 trước tạo thật; tách khỏi process phương pháp',
          'inventory':{'RE2-TT':read('results/T-022/mappings/universe-re2tt-dev.json')['U'],'Nezha-OB':nezha.UNIVERSE},
          'entrypoint':'results/T-052/scripts/p7_entry.py','fixture':'results/T-052/runs/trien-khai-001/fixture-p7-001.json',
          'post_permission':['Materialize hash/byte/map từ đúng thành viên G1, không chọn lại ca','Giữ metadata/nhãn phía quản lý; method API chỉ nhận tín hiệu/inventory/alias/tham số phi nhãn','Kiểm nguồn/schema/alias/quan sát ngoài U, dừng vế dữ liệu/adapter chưa phân loại trước chấm','Seal hạng và kiểm seal trước evaluator ghép nhãn'],
          'RE3':'Giữ ngoài, chưa tải/mở. Schema/đơn vị/coverage/kênh/U/alias/adapter và baseline hỗ trợ phải khóa từ metadata được phép trước lần mở duy nhất của bản cuối; danh sách root không là U.'}
    save(ROOT/'results/T-052/ke-hoach-tap-test.json',plan)
    protocol={'status':'CANDIDATE_FOR_G3_REVIEW_NOT_LOCKED','authority_sources':['docs/DECISIONS.md Q-241/Q-242/Q-245–249','tasks/T-052-t13-va-ho-so-g3/LOG.md Phiên 5'],
      'mode':'a','mode_b':'deferred Q-245','effective_config':config,'fingerprint':fingerprint,'source_code':code,
      'matrix':data['scope'],'test_comparisons':'Ma trận nguồn D4/D5, T13 và cặp snapshot D8; chốt manifest chạy trong SPEC P7 trước mở, không chọn theo điểm test.',
      'cohorts_source':'results/T-052/ke-hoach-tap-test.json','window':{'N':'[t-300,t)','A':'[t,t+300)','span_membership':'start>=t-300, end<t+300; N/A theo end; t hợp lệ theo Q-66 cho (a)'},
      'ranking':{'tie':'p3.danh_gia, giữ khối TORAI và kỳ vọng hòa','failure_denominator':'Lỗi phương pháp trên đầu vào hợp lệ, TIMEOUT/NO_EVIDENCE/UNSUPPORTED giữ ở mẫu số; lỗi dữ liệu/runner/env dừng vế trước bảng khoa học','metrics':['MRR','Hit@1/3/5/10','NDCG@5','Avg@5','Retrieval@5','Rerank@1(K=5)','AC@k nguyên gốc tách bảng kỳ vọng hòa']},
      'A4':{'code':'results/T-052/scripts/thong_ke.py','TT':'MRR M1−TORAI B, mean seed trong ca, 60 ca; delta=0.05; lower95CI > -0.05 strict sau Decimal ROUND_HALF_EVEN 12 chữ số',
            'bootstrap':{'implementation':'src/p3/danh_gia.py:208','B':10000,'seed':20261005,'unit':'ô','paired':True,'quantile':'numpy percentile linear; ghim numpy/thứ tự ca và ô'},
            'OB':'Hit@5 M1−SimpleRCA M4; đảo dấu nguyên ô một phía, kể cả dấu bằng thống kê; giữ ô tổng0; H0 bất biến dấu vector tổng ô',
            'alpha_OB':'0.025; 0.05 chỉ nếu E-04 tại P qua và CI làm tròn lo<hi; TT không nhận mức từ OB',
            'worlds':'Chỉ P quyết A4; S_lo/S_hi dùng cùng mẫu, không thêm quyền bác bỏ',
            'report':'Luôn số ô khác0/tổngkhác0/tổngâm/lẫnchiều/ca cảhai trượt; suy biến ghi cùng câu; mức danh nghĩa và điều kiện hoán đổi, không chứng nhận hiệu chuẩn',
            'McNemar':'Phụ theo ca; root chắc hạng1, TORAI đa số >=2/3 seed; all3 độ nhạy; lỗi0; giới hạn phụ thuộc trong ô',
            'failure_statement':'Không đạt E-04. Chưa chứng minh được không thua quá 0,05'},
      'C_e':'M1 cuối, tối đa60 cửa sổ TT t-300, cần lịch sử tới t-600; top mass/returned/O/U/V0/N1 và RR root tương lai ghép sau. Mô tả, không hiệu chuẩn trên test.',
      'regions':'Hai cách E7 tại P, kỳ vọng theo hòa, chia O từng ca, O=0 N/A; vùng hợp riêng. Chưa có P/R/F1 vùng ảnh hưởng công khai.',
      'Cd3':'Tách khỏi method, seal main trước worker riêng, Fraction tử/mẫu, deadline/status riêng. Helper cd3_after_seal; chỉ RE2-TT ở vế khai; không chạy C-d3 mới trên OB.',
      'C15B':'Giữ kết quả đầu của bản khóa làm chính; sửa có dùng test khai/báo riêng, kiểm độc lập bằng dữ liệu phù hợp chưa dùng sau khóa; RE3 chỉ mở một lần bản cuối.',
      'runtime':'Local giữ test theo Q-42; worker/seed/timeout/ngân sách toàn ma trận cần Minh duyệt trong SPEC P7. Không truyền locked lên EC2.',
      'not_yet_authorized':['commit/push khóa','G3','mở test/RE3','chạy P7'],
      'open_before_execution':['Commit/revision khóa sau phản biện và Minh duyệt','SPEC P7 chốt manifest ma trận/worker/deadline/ngân sách tổng và private map','RE3 hợp đồng/adapter/U/schema và dung lượng/quyền mở riêng khi tới bản cuối']}
    save(ROOT/'results/T-052/giao-thuc-p7-a.json',protocol)
    pilot=read(RUN/'ec2-pilot-002/received/output/summary.json');local=read(RUN/'baseline-local-001/summary.json');ob=read(RUN/'ob-local-002/summary.json')
    matrix={'status':'DEV_VERIFIED_NOT_G3_APPROVED','effective_config':config,'fingerprint':fingerprint,'code':code,'lineage':lineage,
       'ranking_sources':{'six_baselines':'372 native records pinned and rescored; ket-qua-dev-doc-lap-001.json','M1_ablation':'KB seal + all 82 native windows, 328 compact comparisons','C_a':'15 native same-EC2 comparisons and code mapping; projection 82 windows, no E7','C_d_regions':'P only; native M1/T12 off/on; no fresh C-d3 OB','C_c_C_g':'52 exact block comparisons using final observed graph and original pinned baseline votes/ranks'},
       'world_support':data['scope'],'scientific_output':'results/T-052/ket-qua-dev.json','regions':'results/T-052/vung-ce-va-vi-tri-001.json',
       'receipts':{'pilot_ec2':pilot,'baseline_local':local,'OB_local':ob},'budget_seconds_initial':3600,
       'machine_policy':'EC2 cho parity native cùng nguồn; local cho bản gọn/chấm/fixture và pilot máy P7. Không cấp máy hay sửa ACL.',
       'remaining':'Bản P7 chưa khóa/được quyền chạy; dự toán toàn test phải tính ma trận/60 C-e/3 seed/worker/memory/chuyển/kiểm và trần Q-40, không nhân một mẫu rồi coi là cận bảo đảm.'}
    save(ROOT/'results/T-052/ma-tran-va-nguon.json',matrix)
    names=['M1','bo-E1','bo-E2','bo-E5','C-a0','C-a1','C-d1','C-d2','C-d3','C-c','C-g','T12-on','baro','simplerca','microrank_full','tracerca','circa_ols_da','torai_B']
    table=['| Vế | TT, 30 ca | OB, 22 ca |','|---|---:|---:|']
    for n in names:
        values=[]
        for ds in ('RE2-TT','Nezha-OB'):
            r=data['worlds']['P'][ds]['summary'][n]
            values.append(('UNSUPPORTED 22/22' if n in ('circa_ols_da','torai_B') and ds=='Nezha-OB' else f"{float(r['MRR']):.6f}"))
        table.append('| '+n+' | '+' | '.join(values)+' |')
    report='''# T-052 — T13 dev và hồ sơ G3(a)

## 1. Tự đánh giá và đối chiếu yêu cầu

Đã triển khai phần được Minh cho phép sau tự soát. Codex là người làm; Claude là người phản biện chính thức. SPEC và mục cuối LOG đã được đọc ở lượt trước khi nhận đề bài; lượt này không phải đánh giá mù. Nhận xét ban đầu dựng lại từ DT18/cô, MRP, quyết định/lý do/bài học, code và kết quả nguồn; sau đó mới đọc lại SPEC và các phản biện/phản hồi.

Nguồn yêu cầu còn cần: RQ3b về hạng, RQ3d về phép dùng quan hệ, mô tả vùng RQ3c và hồ sơ khóa phép kiểm độc lập. RQ3a/(b) hoãn; P/R/F1 vùng cần nhãn độc lập P10, LLM ở P8, áp dụng FlashTicket ở P9/P10. Không coi task dev hoàn tất là đã trả lời các phần ấy.

Nhận xét trước SPEC: phải dùng lại KB/baseline/T12 có hash đúng; kiểm C-a native và cấu hình hiệu lực; giữ các ca bất lợi; báo theo bộ/loại lỗi/ô/vị trí/ca; khóa A4/tập ca/U/nhãn/máy trước test. Dev đã chọn lặp, C/VC×E5 và nguồn tĩnh chưa nối revision, nên chưa thể khẳng định lợi ích độc lập hoặc cơ chế vật lý. LOG Phiên 5 ghi thứ tự tiếp nhận và quyền nguyên văn.

SPEC hiện hành bao phủ các việc này. Giữ nền, ma trận, A4, cohort và phạm vi kết luận. Không có sửa nhỏ SPEC. Phần thiếu ở lúc bắt đầu là công cụ/parity/chấm/fixture/hồ sơ, đã được triển khai dưới quyền có điều kiện; không đổi nghĩa khoa học để đóng checklist. Phần thừa đã tránh: không chạy lại KB, K, toàn baseline hoặc toàn native chỉ để mang mã T-052; không mở lại task cũ hay thêm VC×E5, PageRank đảo, log–span.

## 2. Công việc đã chạy và tính đúng

Đã kiểm lại 29 đầu vào hồ sơ, 13 manifest upstream và 5 nguồn G1; bốn đầu ra bản sửa 003 khớp. Hash nguồn lịch sử và nguồn hiện hành tách riêng. Hai file src đã sửa ở phiên trước được kiểm lineage theo manifest 003; bản Git của chuoi.py cần biểu diễn CRLF để khớp hash nguồn cũ. Không thay manifest nguồn để bỏ qua lệch.

EC2 pilot-002: 15/15 so sánh native trên 5 cửa sổ TT thật/giả và OB, đúng nguồn cũ cũng chạy EC2, khớp mẫu đầu vào, cờ, tập, tầng, khóa, hòa/hạng, verdict/trạng thái và trường bản ghi ở ba worlds. Khác biệt chủ ý: C-a không dựng E7; C-d3 tách. Biên nhận: `runs/trien-khai-001/ec2-pilot-002/received/output/summary.json`. Đã kiểm byte/hash từng file nhận từ EC2.

Đã chiếu/kiểm 82 cửa sổ, tạo 492 bản ghi gọn sau seal; 328 đối chiếu compact KB khớp. Chỉ sau đó evaluator dùng nhãn dev. Đã băm và chấm lại 372 bản ghi baseline, đủ sáu phương pháp; chỉ số khớp nguồn. C-c/C-g được kiểm lại blocks ở 52 ca trên graph cuối và phiếu/hạng gốc, không chỉ chép số tổng. Nguồn: `prepared-seal.json`, `bang-doc-lap-summary.json`, `score-all-summary.json` trong cùng runs.

Local pilot TT: 6/6 baseline giữ trạng thái và thứ tự nhóm hòa so nguồn; TORAI seed0 dùng đúng Python3.8. Worker TORAI mới khớp nguyên đầu ra raw của tuyến cũ trên cùng CSV. OB local: M1/T12 khớp hạng ở ba worlds; đủ sáu tuyến baseline, CIRCA/TORAI vẫn UNSUPPORTED theo giao thức. Đây là các lát cắt dev để kiểm máy, không là cận thời gian cho mọi ca test/ba seed.

16 fixture A4/giao thức đạt, gồm đúng biên, suy biến, chuyển mức, đảo dấu có ô0, seed lẫn, hòa/lỗi, bootstrap ghép ô khác cỡ, Rerank N/A và O=0. 21 kiểm điểm vào P7 đạt trên dữ liệu giả: quyền/cohort/path/hash/nhãn, đổi mã mờ không đổi method output, M1 thật, sáu tuyến baseline bằng spies, ghép nhãn chỉ sau seal. Spies kiểm luồng, không thay kiểm khoa học baseline. Worker C-d3 thật, lỗi, timeout và JSON hỏng đều giữ hash hạng chính.

## 3. Kết quả mô tả trên dev

MRR tại P; các số ở `ket-qua-dev.json#/worlds/P/<dataset>/summary/<vế>`. Sáu baseline giữ đúng variant P3; TORAI trung bình seed trong ca. S_lo/S_hi lưu riêng, không giả rằng C-d có đủ ba worlds.

'''+ '\n'.join(table)+'''

C-a0 là ablation chuỗi đã chọn, không dùng E1/E2/E5; C-a1 vẫn dùng E1 và quan hệ cha–con. C-d2 dùng khởi phát/khóa raw từ bằng chứng M1 đã có E1/E2. C-g chỉ đo thêm E6b sau SimpleRCA; C-c là RRF k=60. Không có đối chứng graph ngẫu nhiên. Không gọi mọi vế này là không đồ thị, hoặc suy lợi ích do topology thật.

M1−C-a0: TT 1 tăng/25 hòa/4 giảm, chênh −0,055556; OB 9 tăng/11 hòa/2 giảm, chênh +0,210844. M1−C-d2: TT 1/28/1; OB 3/17/2, chênh OB −0,026515. Nguồn từng ca: `#/worlds/P/<dataset>/pairs_M1_minus/<vế>`. Vì vậy dev chưa hỗ trợ phát biểu M1 hơn chung nhánh bỏ quan hệ hoặc quy tắc đơn giản. T13 không chọn lại nền theo bảng này.

MicroRank/TraceRCA TT giữ 4 ERROR trong mẫu số; CIRCA/TORAI OB giữ 22 UNSUPPORTED. Không diễn giải 0 của UNSUPPORTED thành hiệu quả thuật toán. SimpleRCA M4 trên OB giữ giới hạn tái lập đã chấp nhận ở T-042; hơn M4 không đồng nghĩa hơn bản đạt số tác giả.

Bảng `do-do-bo-sung.json#/expected_ties` bổ sung Retrieval@5/10 và Rerank@1 theo cùng định nghĩa evaluator; mẫu số bằng 0 ghi null. `#/baseline_native_order` giữ AC@k/Avg@5 nguyên gốc và seed của baseline, tách khỏi kỳ vọng hòa. M1 có một root mỗi ca nên kỳ vọng AC@k bằng Hit@k; không dựng thứ tự native tùy ý từ khối hòa.

Bootstrap/cặp và bảng theo fault/cell/vị trí N p75/p90/ca nằm trong `ket-qua-dev.json`. Vị trí N dựng từ K-R0 giữ span bọc có n_N>0 và G_N; không dùng A hoặc root để chọn nút. Mọi đầu cạnh thuộc tập nút ở 52 ca. Nhóm lịch sử từ nguồn G1 vẫn giữ riêng trong bản độc lập; không đồng nhất vắng quan sát với cô lập vật lý.

## 4. Chuỗi cơ chế và giải thích cạnh tranh

Đã đọc code E1/E2/E5/xếp hạng và frame nguồn sau kiểm hash. `mechanism_traces` trong kết quả lưu mọi ca đổi RR của các cặp chính, kênh root/tầng/top blocks và ca đối chiếu cùng root/fault nếu có. Ghép cùng root/fault không có nghĩa mọi điều kiện quan sát giống nhau.

E2: ở dev-a915aa2424, kênh exclusive của root giữ 3881,562205; E2-C gán cạnh travel→train điểm 4834,194981 cho train, giữ tầng1, khóa ưu tiên max làm RR root 1→1/3. Ca đúng đối chiếu dev-a5cabe5fa7 có root 5256,929712 vẫn vượt train 4506,080790 nên RR vẫn1. Đây là đường đầu vào kênh→gán cạnh→tầng/khóa→hạng, không chứng minh ai gây lỗi vật lý. Frame chính xác: `results/T-053/phan-tich-cap-003.json#/frames/K-E1+E5|dev-a915aa2424/new` và cặp `K-E1+E2+E5`, cùng hai frame của ca đối chiếu.

E5: ở dev-20acb4402d, bỏ latency-90 của root điểm 4209,481569 để lại exclusive 1132,987919; auth còn 1774,479167, root vẫn tầng1 nhưng RR 1→1/2. Frame cùng file, cặp `K-E1+E2`/`K-E1+E2+E5`. Không có ca đúng trùng đầy đủ chữ ký trong phân tích nguồn; giữ giới hạn, không gọi E5 sai vật lý ở mọi ca hoặc quy cho collector. Điểm đối thủ, tín hiệu không quan sát, tải và giả định phân lớp vẫn là các giải thích cần phân xử bằng dữ liệu phù hợp.

E1/E2 dùng span cấp request; graph gộp không đủ tái tạo duration/membership. E5 dùng cạnh và SCC, nhưng tự sinh theo luật không đồng nghĩa nguyên nhân vật lý. E6a sắp tầng/khóa, E7 dùng cạnh để tạo vùng. Kết quả xấu/tốt của C-d2 là phép so cấu hình cụ thể; không cô lập riêng mọi cơ chế.

## 5. Vùng, C-e và thống kê

Nguồn `vung-ce-va-vi-tri-001.json#/summary`: TT hai cách vùng chứa root kỳ vọng 86,67%/96,67%, rộng 2,9/10,7; OB 81,82%/95,45%, rộng 1,590909/2,909091. Tỷ lệ theo O tính từng ca trước gộp; vùng hợp báo riêng. T12 giữ RR nhưng có thể làm rộng vùng TT; không dùng RR bất biến để kết luận không ảnh hưởng.

C-e: 30 cửa sổ, 16 thực thể từng đứng đầu, top hai mỗi5/30, V0 CAUSE_FOUND 30/30, N1 trung bình14,7. RR root tương lai khoảng0,078727. `#/ce_summary` và `#/ce` giữ top mass/returned/O/coverage/root có mặt; không có nền lành độc lập, không dùng RR này chứng minh không thiên lệch hoặc hiệu chuẩn V0.

A4 được cài theo Q-246, không đổi tiêu chí. Ví dụ dev TT có CI M1−TORAI B [−0,066667; 0,122222], chưa đạt công thức E-04 ở lát cắt dev; OB đảo dấu Hit@5 có 3 ô hữu hiệu, p=1/8. Nguồn `ket-qua-dev-doc-lap-001.json#/A4_dev_illustration` và `#/OB_sign_dev_illustration`. Đây là kiểm công cụ/mô tả dev, không phải kết quả P7. Bootstrap vẫn có nguy cơ undercoverage; đảo dấu chỉ có hiệu lực theo H0 đã khai, không được nâng thành kết luận vô điều kiện.

## 6. Quyền, lỗi giữ lại và chi phí

Không sửa SPEC, src hoặc sổ quyết định/lý do ở lượt này. Chỉ thêm công cụ/kết quả/hồ sơ T-052, nối LOG và đổi đúng dòng T-052 STATE. Không mở test/RE3, không khởi động/cấp máy, không đổi ACL khóa, không commit/push. IP mới do Minh cấp; khóa key2.pem hoạt động.

Giữ đủ lượt hỏng: local001 gộp params hai lần; local002 lưu trace có set; local003 khác số thực khoảng2,8e−16 nhưng cờ/tầng/nhóm hạng giữ. Không nới comparator: đổi sang EC2 cùng nguồn rồi đạt so chính xác. EC2-001 thiếu module observer cham và SSH điều khiển hết giờ; đã kiểm worker qua kết nối mới, không chạy trùng. Lượt002 có PID riêng và biên nhận nhận/hash. Một lượt chấm dừng do lỗi bookkeeping evaluator trước ghi kết quả, đã sửa/giữ bản trước. OB-local001 thiếu thư mục log trước baseline, thời gian native chưa lưu đủ; không dùng thời gian ấy. Hash snapshot được bổ sung sau khi lượt ấy đã bắt đầu đọc, khớp; không gọi đó là tiền kiểm. OB-local002 kiểm trước đúng nguồn và ghi thời gian từng bước.

'''+f"EC2 native parity: {pilot['elapsed_seconds']:.3f} giây; local sáu baseline TT: {local['elapsed_seconds']:.3f} giây; OB local toàn lát cắt: {ob['elapsed_seconds']:.3f} giây. Pha chiếu 82 cửa sổ và chấm hợp nhất có thời gian trong prepared-seal/score-all-summary. Phần làm công cụ/đọc nguồn/viết hồ sơ tách khỏi thời gian máy. Dự toán SPEC 5–7 giờ là dự toán công cả gói, không dùng để hợp thức hóa chạy quá60 phút máy. Tổng thời gian máy có biên nhận và phần hỏng/bounds trong manifest thực thi; không khôi phục mốc chưa ghi.\n"+'''
## 7. Phần đã đạt, phần còn mở và bước tiếp

Đã có T13 dev đủ baseline/ablation/đối chứng, vùng/C-e, parity cần để tái dùng, công cụ thống kê và fixture điểm vào P7. Nghiên cứu trả lời các phép so trên dev và một số cơ chế tính toán, chưa chứng minh lợi ích độc lập, cơ chế vật lý chung, hiệu chuẩn verdict hay độ đúng vùng ảnh hưởng.

Hồ sơ G3 ở `ho-so-g3.md`; giao thức và cohort ở hai JSON kèm theo. Chưa xin coi đã khóa G3. Minh còn quyết nghiệm thu/phản biện và bản khóa; SPEC P7 phải chốt ma trận materialize, vị trí private map, worker/ngân sách toàn đợt và quyền mở. RE3 cần hợp đồng nguồn/adapter/U/alias từ metadata được phép trước lượt mở cuối; chưa tải. VC×E5, hướng PageRank đảo, nối log–span, A0 và revision snapshot giữ đúng giới hạn, không tự thêm thử.

Đề xuất tiếp tục một lượt Claude soát đầu ra mới trước quyết G3. Prompt nguyên văn theo mẫu nằm cuối LOG; không tự gửi và không chờ Claude để hoàn thành các phần đã được Minh giao. Commit chỉ là đề xuất khi Minh yêu cầu: `feat(T-052): hoàn tất T13 dev và hồ sơ chuẩn bị G3(a)`.
'''
    md('results/T-052/bao-cao-t13.md',report)
    components=[
      ('Ánh xạ/quan sát','DT18 + kỹ thuật','T043 hợp đồng/Đ19, m1.adapter và quan_sat','Tín hiệu mỗi nguồn, không dùng marker frontend thay timestamp thật; A0/worlds có điều kiện','Thiếu instrumentation/coverage không được collector khôi phục tự động'),
      ('E1-U bật','Ứng viên giữ thông tin request + DT18','WHY-55/58/72–76; native/ablation','TT bỏ E1 giảm; OB bằng. Giữ full/exclusive và nhánh CP đã không đạt điều kiện thử','Thiếu con, bất đồng bộ, clock, span bọc; exclusive không là CPU time'),
      ('E2-C bật','Gán bằng chứng quan hệ; lựa chọn dev','WHY-72/73; K-b/KB/T13','C giữ theo luật trên nền E5 bật, E2 đánh đổi giữa hai bộ; VC là phương án đã thử','Chưa định danh đầu lỗi mạng; VC×E5 chưa phân xử'),
      ('E5 bật','Tách bằng chứng kế thừa theo cạnh/SCC','WHY-62/72/76 và T13 bo-E5','Bỏ E5 giúp TT/hại OB; giữ quyết định nền, không chọn lại theo test','Phân lớp/quan hệ không xác nhận lan vật lý; thiếu matched control đầy đủ ở nhóm quan trọng'),
      ('z+S1/G3-D1','Thang/cổng lựa chọn dev','WHY-67/69/71; T048/T053','Cổng quyết cờ, z đổi độ lớn, S1 phá hòa; đủ T4/T4b đã có, không lặp','c=1 phụ thuộc đơn vị; cực trị/max; không quy mọi ca hại cho IQR'),
      ('E6a/E7','Hạng/vùng đáp ứng DT18','WHY-74/75; code xep_hang/e7','E6b chiều đã thử hại; E7 hai cách mô tả đã kiểm','Chưa đo P/R/F1 vùng; PageRank đảo còn OPEN'),
      ('E3(a)/E3b tắt','Kết cục lựa chọn dev','WHY-66/72/73 và T6','Giữ kênh log lỗi gộp; không đồng nghĩa bỏ log','Drain/direction có thể đổi thông tin; nối log–span ưu tiên phạm vi, chưa bác lợi ích'),
      ('E9/T12 tắt','Lựa chọn nền, đối chiếu snapshot','WHY-76; T051/T13','Giữ cặp T12 mô tả, không chọn snapshot theo test','Revision runtime chưa nối chắc; messaging/data thiếu hai đầu'),
      ('E8/P8/(b)/G-H','Nhu cầu đề tài và các gói sau','MRP P8–P10, Q-245','Không vào đợt hiện tại; G4 khai thiếu P/R/F1 M1 công khai','Không nhận nhiệm vụ nguồn đã hoàn tất')]
    profile='''# Hồ sơ G3(a) — T-052

Trạng thái: hồ sơ dev để phản biện và Minh quyết, chưa khóa G3 hoặc mở dữ liệu. Nguồn quyết định là sổ và LOG; file này không chọn lại thiết kế.

## Sáu câu của cổng

1. Phục vụ DT18-NV2/NV3, bước 2–4 của cô, RQ3b/d và mô tả RQ3c. Hoãn RQ3a/(b) theo quyền đã ghi; P8–P10 còn nghĩa vụ riêng.
2. Dev phân xử được các can thiệp đã khai và một số cơ chế tính toán; chưa tách topology thật, lỗi vật lý, nhãn vùng hoặc khái quát hóa. TT ít topology/root; OB ít ô hữu hiệu; dev chọn lặp.
3. Đủ sáu baseline, giữ variant mạnh đã duyệt và lỗi/mẫu số. C-a0 đạt điểm dev cao hơn SimpleRCA ở hai bộ; M1 không hơn chung C-a0/C-d2. M4 OB có giới hạn tái lập, không che bằng đồng thuận reviewer.
4. Đã kiểm native/frame/flag/khóa/tầng/hạng, 15 đối chiếu EC2, pilot local TT/OB, 52 đối chiếu graph control, kiểm thống kê và firewall. Lượt lỗi và giới hạn của phép kiểm ghi báo cáo/LOG.
5. Có bảng theo dataset/fault/cell/vị trí N p75/p90/ca và ba worlds đúng phạm vi nguồn; cặp thắng/hòa/thua và vùng/C-e giữ riêng. Không cộng cờ thành tỷ lệ nguyên nhân.
6. Căn cứ các thành phần ở bảng dưới. Những câu thiếu bằng chứng giữ OPEN kèm phụ thuộc, không thay bằng mã WHY.

## Căn cứ thành phần

| Thành phần/trạng thái | Mục đích | Nguồn | Phương án và bằng chứng | Điều kiện thất bại/chưa phân xử |
|---|---|---|---|---|
'''+ '\n'.join('| '+' | '.join(r)+' |' for r in components)+'''

## B6 và điều kiện trước P7

- Code, config có nhanh_z/che_do và dấu vân tay: ma-tran-va-nguon.json. Chưa có commit khóa được Minh duyệt.
- Cổng/ε/α/m/δ/δ_d, lớp kênh, SCC/phủ đỉnh, ba worlds/A0 và trạng thái: giữ T043 với đính chính/WHY hiện hành; T13 không thay luật chọn.
- U/alias, hòa/lỗi/fallback, vùng/verdict, cohort/nhãn và thống kê: giao-thuc-p7-a.json và ke-hoach-tap-test.json. U TT68, OB10; không lấy danh sách root làm U. Nhãn chỉ ở evaluator sau seal.
- V0 chỉ truy vết, không quyết mở sự cố hoặc mức tin cậy root cho LLM. Chưa có nhãn lan độc lập dùng để phân tầng; không tự tạo nhãn vòng lặp.
- C-15 B giữ kết quả đầu, bản sửa dùng test báo riêng và kiểm bằng dữ liệu phù hợp mới. RE3 nguyên bộ một lần cho bản cuối, khóa hợp đồng/adapter/U/schema trước lần đó, chưa tải/mở.
- Máy P7 local theo Q-42. Đã có pilot TT/OB, C-e nặng và tuyến TORAI đúng env; số đo lát cắt không là cận tổng. Chốt tổng ma trận, worker theo RAM, 60 C-e/3 seed, timeout và trần trước chạy; chạy >1h cần Minh duyệt riêng.
- Runtime allowlist/hash data/private map thật chỉ materialize sau quyền; cơ chế/fixture và hash thành viên G1 đã có. Vị trí private map chốt trong SPEC P7.

Đây là các mục cần Minh quyết/hoàn tất khi khóa và giao SPEC P7, không phải giấy phép do agent tự cấp. Task T-052 mô tả có thể bàn giao, nhưng chưa đủ để tự mở test.

## Chuyển giao FlashTicket và các câu mở

P9/P10 nhận: hai đầu quan hệ DB/cache/messaging, trace/span/time/membership, alias service ổn định, log trace_id/span_id, quan sát nền lành nhiều tải, nhãn vùng độc lập. Collector không bổ sung được sự kiện chưa được instrumentation ghi. Cần dữ liệu mới sau khóa để kiểm tương tác E5/VC, hướng lan, log–span và độ bền điểm/đơn vị nếu Minh mở phạm vi đó. P8 đánh giá giải thích trung thành riêng. Không tuyên bố đã giải hết RQ2/RQ3/RQ5.

## Đề xuất ghi sổ quyền

Ngoài phạm vi ghi hiện tại: đề xuất nối docs/DECISIONS.md một mục theo đúng lời Minh, ghi Codex tự soát/triển khai có điều kiện T-052, phạm vi LOG/results/đúng dòng STATE và sửa nhỏ SPEC, pilot/chấm dev tối đa60 phút máy; EC2 hiện có tại IP Minh cấp, không cấp máy/mở test/commit/push. LOG đã giữ nguyên quyền; chưa tự ghi sổ ngoài phạm vi.
'''
    md('results/T-052/ho-so-g3.md',profile)
    save(RUN/'closeout-generation.json',{'created_utc':datetime.now(timezone.utc).isoformat(),'source_manifest':'results/T-052/manifest.json',
          'reports_from':'ket-qua-dev.json','cohort_counts':{d:{k:c[k] for k in ('n','cells','TX')} for d,c in cohorts.items()},'SPEC_changed':False,
          'task_status':'phần người làm đã có đầu ra dev, chờ tự kiểm cuối và phản biện; không nghiệm thu/G3'})

if __name__=='__main__':main()
