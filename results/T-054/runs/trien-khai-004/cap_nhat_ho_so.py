"""Đồng bộ hồ sơ sau gói thu gọn, không khóa G3 hoặc mở dữ liệu."""
import copy
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];RUN=Path(__file__).resolve().parent;OUT=ROOT/'results/T-054'
sys.path.insert(0,str(OUT/'scripts'))
import os
for key in ('OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','OMP_NUM_THREADS'):
    os.environ[key]='1'
os.environ['PYTHONHASHSEED']='0'
sys.path.extend(['D:/RCA-ext/src/RCAEval','D:/RCA-ext/src/baro','D:/RCA-ext/work/T-014/CIRCA',
                 'D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages'])
from bien_nhan import *
from dieu_phoi import status
from lap_ho_so import preflight

def update(name,value):
    (OUT/name).write_bytes(canonical(value)+b'\n')

assert status(RUN/'pilot-2-worker-001/queue')['controller'] is None
measurement=read_pin(ref(RUN/'pilot-2-worker-001/summary.json'));assert measurement['PASS']
decision=ref(RUN/'quyet-dinh-minh.json')
policy=read_pin(ref(RUN/'failure-policy-dev.json'))
policy.update(scope='CANDIDATE_FOR_G3_NOT_LOCKED',main_allowed=False,
              timeout_s={'main_slot':600,'C-d3':60},unknown_errors='BLOCKED, stop dispatch, report without labels; no automatic retry')
policy.pop('candidate_main_timeout_s',None)
policy_ref=atomic(RUN/'failure-policy-g3-candidate.json',policy)
settings={'status':'CANDIDATE_FOR_G3_NOT_MAIN_PERMISSION','host':'local Windows','workers':2,'BLAS_OMP_threads':1,
 'timeout_s':{'main_slot':600,'C-d3':60},'monitor':policy['monitor'],
 'budget':{'mode':'UNTIL_COHORT_COMPLETE','wall_s':None,'method_dataset_s':{},'decision_ref':decision},
 'retry':'none automatically; preserve every failed/partial attempt',
 'operational_error':'stop new dispatch; preserve active workers/outputs; report before further action',
 'time_rule':'No fixed cumulative cap. On errors, infinite loop/nonprogress or tens of hours unfinished: stop/report Minh.',
 'cache':'isolated slots; no shared cross-arm data/E4 cache introduced; performance optimization deferred, no new gate',
 'worker_selection_evidence':ref(RUN/'pilot-2-worker-001/summary.json'),
 'numeric_exception':decision,'failure_policy_candidate':policy_ref,
 'not_an_ETA':'Small packet confirms overlap/parity and observed memory only; no claim of full-cohort speedup.'}
settings_ref=atomic(RUN/'de-xuat-khoa-g3.json',settings)

p=read_pin(ref(OUT/'protocol.json'))
p.update(status='CANDIDATE_NOT_LOCKED',real_execution_ready=False,
 implementation='Gói thu gọn đã kiểm vận hành 1/2 worker, lỗi/timeout và C-e dev. Dừng để Minh xét G3; chưa main/test.',
 readiness='PREPARATION_REVIEW_READY_WAIT_G3_AND_SOURCE_GRANTS',
 resolved_choices={'numeric':decision,'sensitivities':decision,'no_cumulative_time_cap':decision},
 execution_candidate=settings_ref,
 open_choices=['Minh duyệt G3 đúng gói code/config/env/matrix/policy vận hành',
               'quyền nguồn và materialize private test94 + label bindings từ G1',
               'nguồn 3 CSV tác giả TORAI A đúng cohort TT, ngoài A4',
               'duyệt ghi chính thức DECISIONS/WHY và commit khóa theo phạm vi trình'],
 open_before_execution=['Dừng báo Minh trước chạy chính theo lệnh phiên 5.',
   'Phản biện độc lập/các quyết định khóa theo quy trình repo do Minh chuyển thủ công.',
   'G3 và grant nguồn/test/A riêng; sau grant dựng map/plan cụ thể, kiểm hash và attest trước dispatch.',
   'RE3 H1/H2/H3 riêng cho bản cuối; chưa adapter/telemetry, không được dùng grant test94 mở RE3.'])
for k in ['case_permutation','error_excluded']:
    p['A4'][k]['status']='USER_CONFIRMED_SENSITIVITY_ONLY';p['A4'][k]['decision']=decision
p['A4']['sensitivity_wrapper']='results/T-054/scripts/cham.py:approved_sensitivities'
p['A4']['error_excluded']['CI']='paired cell bootstrap on retained pairs; empty subset N/A; report n/cells; never transfer alpha'
p['A4']['case_permutation']['comparison']='exact integer scaled sums, two-sided >= observed; no floating epsilon'
p['before_A4']['seal']='T054 snapshot verifies full A4 and failure receipts before labels; C-e plan covers every TT member as supported job or source-bound insufficient row.'
p['before_A4']['core_note']='a4_v2 primary formulas unchanged; T054 implements the two approved sensitivities including error-excluded CI.'
p['pilot_evidence']['two_worker_Ce']=ref(RUN/'pilot-2-worker-001/summary.json')
p['pilot_time']={'historical_local_cap_s':3600,'historical_cap_scope':'old DEV pilot, not main ETA',
                 'main_cumulative_cap':None,'main_time_decision':decision,'new_packet_elapsed_s':measurement['elapsed_s']}
p['authority_sources'].append('tasks/T-054-khoa-g3-chay-p7-a/LOG.md Phiên 5; results/T-054/runs/trien-khai-004/quyet-dinh-minh.json')
p['decision_changes']=[decision]
p['source_code'].update({x.relative_to(ROOT).as_posix():ref(x)['sha256'] for x in (OUT/'scripts').glob('*.py')})
p['fingerprint']=fingerprint({k:v for k,v in p.items()if k!='fingerprint'})
update('protocol.json',p)

source=read_pin(ref(OUT/'source-manifest.json'))
source['own_scripts']={x.relative_to(ROOT).as_posix():ref(x)for x in (OUT/'scripts').glob('*.py')}
source['authority']=ref(RUN/'quyen-minh.txt');source['current_pilot']=ref(RUN/'pilot-2-worker-001/metadata.json')
source['previous_manifest']=ref(OUT/'manifest-trien-khai-003.json')
source['lineage_current']={'pilot_code':str(RUN/'pilot-2-worker-001/code'),
 'final_code_note':'Final logging/timeout/description corrections after the measured packet; science methods/config unchanged.',
 'decisions':decision,'candidate':settings_ref}
update('source-manifest.json',source)
auth=read_pin(ref(OUT/'authorization.json'))
auth.update(source=ref(RUN/'quyen-minh.txt'),stop_before_main=True,
 pilot_scope='approved targeted local DEV checks only; no broad baseline rerun; current P7 cumulative time decision is separate',
 current_decisions=decision,g3=False,test_grant=False,RE3_telemetry=False,commit_push=False)
auth['pilot_plan_refs'].append(ref(RUN/'pilot-2-worker-001/plan.json'));update('authorization.json',auth)
pilot=read_pin(ref(OUT/'pilot-plan.json'))
pilot.update(status='TARGETED_DEV_CHECK_COMPLETE_STOP_FOR_G3_REVIEW',
 local_concurrency={'workers_checked':[1,2],'no_3_4_search':True,'selected_candidate':2,'evidence':ref(RUN/'pilot-2-worker-001/summary.json')},
 remaining_before_pilot=[],remaining_before_main=p['open_choices'],
 current_decisions=decision,budget=settings['budget'],
 note='Baseline G2 and checkpoint003 retained. Only two new M1 slots: missing C-e TT + OB two-worker comparison. No further broad pilot planned.')
pilot['additional_local_2_worker']=ref(RUN/'pilot-2-worker-001/summary.json');update('pilot-plan.json',pilot)
reuse=read_pin(ref(OUT/'reuse.json'));reuse['checkpoint004']={'retained_G2_and_DEV':True,'new_method_calls':2,
 'evidence_reuse_not_shared_runtime_cache':True,'no_additional_broad_DEV_runs':True,'evidence':ref(RUN/'pilot-2-worker-001/summary.json')};update('reuse.json',reuse)
env=read_pin(ref(OUT/'environment.json'));env['numeric_decision']=decision;env['candidate_workers']=2
env['main_thread_exception_not_approved']=True;env['note']='Main remains 1 thread; three observed parity differences accepted, no general tolerance.';update('environment.json',env)
atomic(RUN/'preflight-final.json',preflight())

report=f'''# T-054 — điểm dừng trước G3/chạy chính

**Đã hoàn thành gói chuẩn bị thu gọn Minh duyệt. Đang dừng để xét G3; chưa chạy chính, chưa mở test.** Không gọi đây là G3 đã đạt: phản biện/duyệt khóa và quyền nguồn vẫn riêng.

## Kết quả và căn cứ

| Việc | Kết quả | Nguồn |
|---|---|---|
| Tái dùng đầu ra cũ | Checkpoint003 khớp 3.558 pin trước sửa; giữ 40 slot/4 ca, G2 và mọi lượt hỏng. Không lặp baseline dev diện rộng. | LOG phiên5, before.json; manifest003 |
| Điều phối | Plan chỉ 1/2 worker; một supervisor; giữ token/PID khi nhận lại; DRAIN không phát mới; lỗi vận hành dừng phát, unrun không TIMEOUT. Mỗi nhóm method×dataset một slot đồng thời. | operational-checks.json; final2-branch-checks.json |
| Lô mới có mục đích | Hai M1 slot: C-e TT dev-a5cabe5fa7 và main OB dev-607751ac0a. Cả hai OK, khớp toàn trường khoa học so nguồn đã pin. OB khớp normalized input lượt một worker cũ. | pilot-2-worker-001/summary.json#/rows |
| Thực đo 2 worker | {measurement['elapsed_s']:.3f} s trôi; overlap {measurement['overlap_s']:.3f} s; đỉnh RSS cây đồng thời lấy mẫu {measurement['concurrent_sampled_peak_tree_rss']:,} byte. Không có clock anomaly, maxgap từng slot <5 s. | cùng summary#/elapsed_s,/overlap_s,/concurrent_sampled_peak_tree_rss,/rows |
| C-e | Tuyến thật từ source/A0→t−300→method→seal→nhãn dev→mô tả đạt. Bằng chứng lịch sử từ native command/coverage đã pin, không gán là nền khỏe. Test phải có mỗi ca một job hỗ trợ hoặc dòng insufficient gắn đúng source; thiếu/trùng/sai bị chặn trước nhãn. | nguon.original_dev_sources; cham.validate_ce_plan; pilot-2-worker-001/descriptive.json |
| ERROR/TIMEOUT | Quy tắc operation mới MicroRank/TraceRCA đọc lại đúng normalized input và đếm N/A; không phân loại chỉ từ chuỗi lỗi. TIMEOUT chỉ từ method start/invocation/deadline/monitor hợp lệ, giữ M4/CIRCA/TORAI variants. Prep/nguồn/clock gap/ERROR lạ vẫn BLOCKED và dừng phát. | failure-policy-g3-candidate.json; operational/final-branch/failure-report checks |
| Độ nhạy | Cả cặp bị loại nếu bất kỳ seed lỗi; giữ NO_EVIDENCE/UNSUPPORTED, CI trên cặp còn lại, rỗng N/A. Hoán vị ca hai phía10.000, seed20261005,+1, so tổng nguyên chính xác. Không đổi phép chính/mức OB. | sensitivity-checks.json; cham.approved_sensitivities |

## Đã chốt theo lời Minh

Nguồn USER_CONFIRMED: quyet-dinh-minh.json. Chấp nhận đúng ba sai khác số học cũ, không dung sai chung; 1 luồng giữ nguyên. Duyệt hai công thức độ nhạy. Không đặt trần cộng dồn P7; chạy đủ, lỗi/không tiến triển/hàng chục giờ chưa xong thì dừng/báo. Đây là ngoại lệ P7, giữ lịch sử Q-40/P3. Sổ chính thức chưa tự ghi; nội dung xin nối nằm trong de-xuat-ghi-so.md.

## Bố trí trình khóa

Local, tối đa2 worker, mỗi phương pháp1 luồng; slot độc lập. Không thêm cache liên vế: đây là lựa chọn vận hành ít công, không biến tối ưu hiệu năng thành điều kiện khoa học. Chọn2 từ bằng chứng overlap/parity và RAM quan sát, không khẳng định nhanh gấp2. Timeout đề nghị600 s/slot, C-d3 60 s; poll0,1 s, maxgap strict<5 s; không tự retry. Các số vận hành này là CANDIDATE để Minh khóa trong de-xuat-khoa-g3.json. Không thay cấu hình phương pháp, cohort hoặc seed.

Matrix giữ94 ca chính: TT60/Nezha34, 1.342 slot chính, C-d3 TT60 riêng, C-e tối đa60; A phụ180 ngoài A4. RE3 không thuộc grant94, không bị bỏ: hợp đồng metadata pha1 đã có ở trien-khai-003/hop-dong-re3.json; H1 schema/H2 adapter và quyền sửa src còn riêng, chưa cài adapter RE3 hoặc mở telemetry. Không nhận TT adapter là RE3 adapter.

## Còn trước khi được phát main

1. Minh xét/khóa G3 đúng byte code, cấu hình/env/matrix, policy và ngoại lệ; phản biện theo quy trình Minh chọn chuyển thủ công. Đồng thuận agent không thay bằng chứng/duyệt Minh.
2. Grant nguồn TT60 + OB34, các cửa sổ/vế/chấm đã khai; dựng private source/label bindings từ G1/nguồn độc lập sau grant, kiểm hash và attestation trước dispatch. Chưa mở nguồn để điền checklist.
3. TORAI A vẫn phụ, cần quyền đúng ba CSV tác giả của cohort TT trước phần A. Grant một ca dev không phải grant cohort. Không chọn lại A/B hoặc tự bỏ A.
4. Minh duyệt nội dung nối DECISIONS/WHY và commit khóa nếu dùng. Chưa commit/push. Các nguồn/hạn chế M4, tiếp xúc TX1/file chung, revision benchmark snapshot OPEN, bootstrap ít ô và cơ chế vật lý chưa phân xử giữ nguyên.

Không có lô pilot/benchmark tiếp theo mặc định. Công việc sau grant là dựng/băm/đối chiếu map/plan cụ thể rồi chạy đúng bản khóa; lỗi phát hiện mới thì dừng đúng phần phụ thuộc, giữ đầu ra và báo Minh.

## Thời gian, giới hạn

Lô mới mất khoảng4 phút10 giây, không phải thêm3 giờ pilot. Kịch bản một worker lạnh25–27 giờ trước đây không là ETA toàn task. Lô2 slot không phải phép so thời gian1/2 trên cùng lô; vì vậy không suy tốc độ tăng hay ETA toàn cohort. Không chạy thêm chỉ để săn ETA; tiến độ thật sẽ cung cấp dự báo khi chạy chính được phép.

RAM host/paging chưa được ghi đầy đủ trong lô thật; không tuyên bố không paging. Driver cuối đã bổ sung quan sát RAM khả dụng/pagefile, kiểm trên mẫu giả. Dung lượng tạm/output toàn cohort chưa có upper bound thực đo; phải theo dõi đĩa và dừng vận hành khi thiếu. Lần chấm lô mới đầu hỏng vì helper chưa canonicalize cell; đã giữ lỗi/script đầu và sửa helper, không lặp method. Kiểm pipeline phát hiện timestamp lấy trước deadline; sửa capture thời điểm quan sát hạn và kiểm lại, giữ lượt hỏng.

Task chưa xong pha2, chưa trả lời RQ3 độc lập, không xác nhận vùng ảnh hưởng/nhân quả vật lý hoặc P/R/F1 phát hiện. Kết quả âm và giới hạn dev vẫn giữ.
'''
report_dir=OUT/'reports/tu-soat-004';report_dir.mkdir(exist_ok=False)
(report_dir/'bao-cao.md').write_text(report,encoding='utf-8')
(OUT/'ho-so-g3.md').write_text(report,encoding='utf-8')
(OUT/'runbook.md').write_text('''# Vận hành T-054 — dừng trước G3

Hiện hành: LOG phiên5, manifest-trien-khai-004.json, reports/tu-soat-004/bao-cao.md. Gói thu gọn đã kiểm; chưa LOCKED_G3, chưa main/test. Không chạy lại helper pilot cũ/create-only.

1. Kiểm checkpoint bằng Python main -X utf8 -B results/T-054/runs/trien-khai-004/kiem_checkpoint.py --manifest results/T-054/manifest-trien-khai-004.json. Chỉ đọc.
2. Đọc de-xuat-khoa-g3.json, failure-policy-g3-candidate.json, de-xuat-ghi-so.md. Chờ Minh xét G3/nguồn/commit; không tự đổi cờ quyền.
3. Sau đúng grant: dựng nguồn runtime/private/label độc lập theo G1/metadata gốc, đủ60TT/34OB và ce_history từng TT; kiểm hash, attest_runtime v3. C-e đủ lịch sử mới tạo job tại t−300, còn lại thêm ce_support gắn source hash. TORAI A map riêng đúng3CSV/mỗi member, đủ3seed, ngoài A4. Không dùng đường dẫn/nhãn làm đầu vào phương pháp.
4. Lập plan bất biến từ matrix/config/env đã khóa: workers2, threads1, budget UNTIL_COHORT_COMPLETE không trần cộng dồn, timeout600s/C-d3 60s, poll0,1s/maxgap<5s nếu Minh duyệt đúng đề nghị. Main M1 seal trước C-d3; lỗi C-d3 giữ main. Ghim source/env/code/plan/authority; p7 run vẫn cần G3+test grant. Không phát plan DEV hoặc mặc định sinh từ hồ sơ cũ thành test.
5. status chỉ đọc; drain dừng phát mới và cho active kết thúc; resume chỉ cùng plan/root, nhận lại PID/token, không chạy đôi. Không auto retry. Lỗi nguồn/adapter/prep/clock hoặc method ERROR chưa phân xử: BLOCKED và dừng phát. Chỉ ERROR operation-mới đã khóa hoặc TIMEOUT đủ pha/monitor mới được tính trượt. Giữ mọi raw/partial/receipt.
6. Theo dõi tiến độ, RAM/đĩa/pagefile, không để máy sleep. Không tạo trần cộng dồn; khi lỗi, không tiến triển/lặp vô tận hoặc hàng chục giờ chưa xong, dừng/báo Minh. Không tự đổi cấu hình/chấm lượt chưa chạy thành TIMEOUT.
7. Đủ A4 và mọi binding/phân loại trước ghép nhãn. Các bảng phải khai support/missing; TIMEOUT không có trung gian thì N/A, không dựng N1/O/vùng=0. RE3 H1/H2/nguồn/adapter còn riêng cho bản cuối; không mở bằng grant94. Không SSH/cloud hoặc commit/push nếu chưa có quyền.

Lô thật2 slot có code snapshot trong pilot-2-worker-001/code. Code cuối bổ sung metadata giám sát và sửa nhánh timeout/mô tả sau lô; final checks riêng, không gọi byte code cuối là byte tạo mọi pilot. Freeze006 là ứng viên để xét khóa, không tự là G3.
''',encoding='utf-8')
print('current documents synchronized; G3/main/test remain false')
