"""Prepare approval material only; never apply common code or adopt a pin."""
from pathlib import Path
import json, hashlib, shutil, re
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent
PKG=RUN/'package'
OLD=ROOT/'results/T-038/runs/hoan-tat-trong-quyen-001/smtp'
OUT=ROOT/'results/T-038'
def load(p): return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def save(p,v): Path(p).write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def write(p,v): Path(p).write_text(v,encoding='utf-8')
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rel(p): return Path(p).relative_to(ROOT).as_posix()

log=ROOT/'tasks/T-038-p5b-trainticket/LOG.md'
with log.open('a',encoding='utf-8') as f:
    f.write('\nCheckpoint cùng phiên sau nén ngữ cảnh: preview V2 đã PASS29, rebuild nguyên mô hình T037/T039 và frozen TT; candidate chỉ sửa comparator, builder byte-identical T037 đã hỗ trợ SMTP. Đang hoàn thiện plan/docs/filelist/hồi quy đầy đủ và kiểm bất biến; tiếp tục trong cùng phiên theo Minh giao, không chạy lại số đã hợp lệ.\n')

inputs={}
for task in ('T-036','T-037','T-038','T-039'):
    p=ROOT/f'results/{task}/manifest.json'
    m=load(p)
    inputs[task]={'path':rel(p),'sha256':sha(p),'created_utc':m.get('created_utc'),'current_run':m.get('current_run'),'status':m.get('status')}
for p in [ROOT/'src/do_thi_tinh'/x for x in ('__init__.py','build.py','compare.py','README.md')]:
    inputs[rel(p)]={'sha256':sha(p),'bytes':p.stat().st_size}
save(PKG/'input-state.json',inputs)

newruns={t:f'results/{t}/runs/doi-chieu-smtp-001/' for t in ('T-036','T-037','T-038','T-039')}
assert all(not (ROOT/p).exists() for p in newruns.values())
oracle=load(PKG/'kiem-preview-001/checks.json')
assert oracle['all_ok'] and len(oracle['checks'])==29
budget={'candidate_only':True,'measured':False,'machine_minutes':37,'output_bytes_approx':600000000,'network_source_download_bytes':0,
        'stages':[{'scope':'shared T036 + R1 + SMTP','minutes':2,'bytes':50000000},
                  {'scope':'T037 full model + existing fixtures','minutes':10,'bytes':150000000},
                  {'scope':'T038 full 1069 comparisons','minutes':10,'bytes':150000000},
                  {'scope':'T039 full 132 comparisons','minutes':5,'bytes':100000000},
                  {'scope':'one T038 full rerun allowance','minutes':10,'bytes':150000000}],
        'TT_RAM_GiB_planning':0.5,'other_peak_RAM':'OPEN; measure per process; do not add or extrapolate uncontrolled runs',
        'supersedes':'historical 31min/550MB proposal with incomplete FT/OB replay scope'}
plan='''# Gói thay đổi đối chiếu SMTP và hợp nhất phiên bản — V2

Ngày 16/10/2026. **CANDIDATE, chờ Minh duyệt áp dụng.** Lượt này chỉ cập nhật hồ sơ T-038. Không sửa shared, SPEC, WHY/DECISIONS hoặc chuyển pin. Bản V1 đã giữ nguyên tại `../before/package-v1/`. File máy đọc: `plan.json`; bằng chứng phiên bản/hash: `input-state.json`; bản sửa tài liệu: `docs-before-after.json`.

## Trạng thái đã kiểm trên artifact hiện tại

| Nhánh | Hiện trạng | Điều không được suy ra |
|---|---|---|
| T-036 | Hợp đồng R1 và snapshot `results/T-036/runs/kiem-r1-after-002/code/` là mốc lịch sử; root manifest giữ nguyên. | Live code hôm nay không còn đồng nhất R1 do delta T-037 đã được duyệt. Đây không phải manifest hỏng. |
| T-037 | **Đã hỗ trợ SMTP và dựng mô hình đầy đủ theo thiết kế có điều kiện.** Minh đã cho sửa SMTP, kiểm lại và tiếp tục T-037, giữ T-038/T-039 nguyên pin. `runs/graph-003/` có model/graph/snapshot; `result.json#/passed`=1598, `/failed`=0. Builder nhận SMTP ở hai loại gọi; type thực tế SMTP còn chưa phân kiểu. Comparator vẫn là quy tắc cấu trúc R1. | Chưa nghiệm thu; chưa có runtime proof, chưa chuyển hai nhánh khác. Không gọi lựa chọn so cấu trúc đã được ghi giới hạn là lỗi triển khai T-037. |
| T-038 | Model005 và **1069 graph dev** đã đối chiếu dưới snapshot R1. Quan hệ SMTP có nguồn vẫn chưa đưa vào model hiện hành. | Quyền cập nhật gói này chưa cho đổi code/model/pin. Lineage/runtime nguồn TT vẫn có điều kiện. |
| T-039 | **Đã có model, mapping và bộ đối chiếu đầy đủ 132 graph dev**, run `thuc-thi-snapshot-004`. `execute_pinned.py` nhập trực tiếp snapshot T-036 gốc theo quyền Minh, không nhập live src. | Chưa nghiệm thu; inventory toàn deployment, runtime/Node/alias còn OPEN. Không còn tình huống “chưa có converter để hồi quy”. |

Nguồn trạng thái: manifest từng task được hash trong `input-state.json`; quyền T-037 tại `results/T-037/runs/tiep-smtp-001/authorization.txt`, hợp đồng tại `results/T-037/hop-dong-smtp.md`; kết quả T-039 tại `results/T-039/doi-chieu/tong-hop.json`, run verification và cost. Hash toàn268/5324/842artifact T037/T038/T039 đã kiểm trước dùng. Số1069 lấy `results/T-038/doi-chieu/index.json`; số132 lấy `results/T-039/runs/thuc-thi-snapshot-004/cost.json#/graph_count`.

## Chính xác điều xin Minh quyết

**Việc đã có:** biểu diễn `channel=smtp` trên `gọi-đồng-bộ` và `gọi-chưa-phân-kiểu`, `messaging=null`, không tạo broker/người nhận giả. Giữ builder T-037 đã kiểm, không xin thêm enum từ đầu. Snapshot/hợp đồng mới sẽ tiếp nhận delta có quyền này cùng thay đổi comparator nếu Minh chọn.

**Thay đổi mới đề xuất:** comparator nhận call `channel` tùy chọn (http/rpc/internal/smtp). Với SMTP tường minh, cả khóa `endpoints` và `typed` giữ marker `['smtp', null]`; HTTP/RPC hoặc trace không channel không có marker này. Vì vậy same-owner SMTP không còn khớp với HTTP/RPC/trace thiếu channel. Typed vẫn loại type chưa biết. Không suy channel từ static, không sửa graph T-035; adapter P9 muốn phát channel cần nguồn và quyền riêng.

Đây là **đổi nghĩa phép đối chiếu**, kể cả view endpoints, rồi **chuyển ba nhánh sang cùng manifest mới**; không thể duyệt dưới tên “chỉ bổ sung SMTP”. `kiem-preview-001/comparison-before-after.json` lưu đầu vào và hai kết quả: cùng synthetic SMTP static/trace thiếu channel, giao endpoints hiện tại là1, ứng viên là0. Chênh này là hệ quả thiết kế chủ ý, chưa là bằng chứng lợi ích RCA hay lỗi kết quả lịch sử.

Nút là service/component và operation có nguồn; cạnh SMTP hướng client→mail-server external, không tới hộp người nhận. Type phụ thuộc bằng chứng chờ của client, không suy từ tên mail hoặc delivery về sau. TT delta giữ `gọi-chưa-phân-kiểu`, operation nguồn và `runtime_name=null` khi chưa nối instrumentation. Port/host/cờ TLS, branch/retry/outcome giữ trong context/provenance; marker null không xác minh authority/port/TLS/delivery. Không thêm schema địa chỉ tổng quát. Projection, ownership, entity-only, binding/signal và shared metric giữ nghĩa cũ. Phép tính dùng cạnh là chuẩn hóa khóa, chiếu và các tập so; chưa có scoring/ranking RCA.

## Code và tài liệu cũ → mới

- **build.py và __init__.py:** dùng nguyên byte baseline T-037 graph003 hiện hành; không nằm trong patch sửa shared. Snapshot mới vẫn phải chứa chúng và hash đúng.
- **compare.py:** patch chính xác `proposed-shared-code.patch`, từ comparator hiện hành sang optional call channel/marker SMTP. Không thay API export hoặc HTTP/RPC legacy ngoài phân tách SMTP đã nêu.
- **README shared:** bản đầy đủ dự kiến `README.shared-proposed.md`; phân biệt R1 lịch sử, delta SMTP T037 và pin mới sau PASS.
- **Hợp đồng T036 mới trong run:** diễn giải call channel đã có, optional trace field, SMTP key cả hai view, unknown/missing channel/exclusions/denominators và giới hạn địa chỉ. Giữ `results/T-036/hop-dong.md` và root manifest lịch sử.
- **SPEC ba nhánh:** nối phụ lục version/adoption, giữ nguyên đoạn pin gốc như lịch sử và ngoại lệ T037/T039 đã có; không thay lời duyệt cũ. Hash/created_utc pin mới chỉ điền từ manifest thực sau kiểm. Các đoạn trước/sau và phụ lục T036 có ở `docs-before-after.json`.
- **WHY/DECISIONS:** dự thảo ghi lựa chọn đổi comparator, phương án giữ quy tắc cấu trúc hiện tại và tác động phiên bản; nguyên lời duyệt/date/mã chưa có thì để OPEN. Không ghi đề xuất thành quyết định.

## Phạm vi ghi xin duyệt và tác động

Danh sách chính xác ở `plan.json#/proposed_writes`; mọi phạm vi dưới đây chỉ có hiệu lực **sau Minh duyệt gói V2**, không suy từ quyền T038 hiện tại.

| File/phạm vi | Việc dự kiến |
|---|---|
| `src/do_thi_tinh/compare.py`, `README.md` | Áp đúng patch và README preview; builder dùng lại nguyên trạng. |
| `results/T-036/runs/doi-chieu-smtp-001/` | Hồ sơ sửa mới: before/oracle/hợp đồng/code snapshot/hash, check runner, mọi lần chạy/kết quả/chi phí, manifest pin và bàn giao/prompt. Không ghi root manifest T036. |
| `tasks/T-036-p5b-hop-dong-chung/SPEC.md` và LOG | Nối phụ lục sửa được duyệt và LOG thực; T036 gốc đã đóng vẫn là lịch sử. |
| `tasks/T-037-p5b-flashticket/SPEC.md`, `tasks/T-038-p5b-trainticket/SPEC.md`, `tasks/T-039-p5b-online-boutique/SPEC.md` và LOG tương ứng | Nối phụ lục quyền/pin mới và tiến trình thực tế; giữ delta T037, direct-snapshot T039 và pin cũ cho output cũ. |
| `docs/WHY.md`, `docs/DECISIONS.md` | Chỉ nối lý do/version và nguyên quyết định thực sau duyệt; nội dung dự thảo xem before→after. |
| `docs/STATE.md` | Chỉ dòng T036–T039, cập nhật tuần tự bản mới nhất; không tự nghiệm thu hoặc đổi G3. |
| `results/T-037/runs/doi-chieu-smtp-001/` | Pin loader/runner mới; snapshot full model/graph003/registry/fixture, dựng và so đầy đủ fixture hiện có với hai comparator, giữ tập/members/loại trừ/mẫu số và diff. Không thay counterexample/rejection oracle lịch sử. |
| `results/T-038/runs/doi-chieu-smtp-001/` | Pin loader/engine/compare runner mới, delta SMTP có nguồn, rebuild hai mức và so đủ1069 graph; per-graph output/diff nằm trong run mới. |
| `results/T-039/runs/doi-chieu-smtp-001/` | Pin loader và `execute_common.py` tiếp nhận từ **execute_pinned.py đã có**; rebuild full model, replay **đủ132 graph**, output/diff từng graph trong run mới. Không kiểm smoke thay replay. |
| Bản hiện hành của T037/T038/T039 liệt kê trong plan.json | Sau cả ba nhánh PASS mới cập nhật model/graph/mapping/registry khi có delta, chỉ mục/phân tích/kiểm/bàn giao/prompt/manifest với pin mới. Giữ byte trước trong before/ và mọi output cũ nguyên pin. Coverage/source không tự tăng do đổi comparator. Nếu thất bại giữ trạng thái chuyển chưa xong, không đánh tráo pin. |

Tên run đều đã kiểm chưa tồn tại khi trình V2. Nếu có nhánh thay đổi trước khi áp dụng, kiểm lại input-state, báo chênh và cập nhật đề xuất; không áp patch lên baseline khác. Không có quyền sửa T035, nguồn ứng dụng, repo platform, raw/test/heldout, dependency hay môi trường; không tải thêm, commit/push hoặc gửi agent.

## Tiếp nhận runner và hồi quy đầy đủ

1. Kiểm hash tất cả baseline/manifest, giữ pin cũ. Chép oracle literal trước sửa; dùng snapshot độc lập để so R1, T037 đã SMTP và candidate, không gọi live hiện tại là R1. Chạy lại toàn checker T036/R1 và SMTP regression T037 trong run mới, giữ mọi lỗi.
2. Loader mới nhận đường dẫn/SHA/created_utc manifest mới tường minh, kiểm hash từng module snapshot và live rồi import namespace riêng; không HEAD/fallback R1. ROOT/input/output root tường minh. `T038/engine.py:pinned_api` hardcode R1/live hash nên giữ lịch sử, tạo runner mới; chỉ sửa SPEC không đổi runner là chưa đủ.
3. T037 dùng full model/registry `graph-003`, snapshot `input-code-hashes.json`, `runner.py`, `assemble-complete.py`, oracle/fixtures đã có, không giả định thiếu converter. So nguyên model không delta, cả hai mức/projection/entity-only/shared signals và mọi fixture; phân tách thay đổi comparator chủ ý khỏi bất biến builder. Không biến fixture thành runtime trace thật.
4. T038 đóng băng1069 input/mapping/context; lưu baseline R1, candidate cùng model cũ, rồi candidate với delta SMTP để **tách ảnh hưởng comparator khỏi thêm quan hệ**. So từng tập S/T/giao/hiệu/members/exclusions/mẫu số, hai mức/full/N/A/s60/s300; kiểm nguồn/unknown/unmapped, lặp/đảo và input bất biến. Không bỏ cạnh thiếu trace để tăng giao.
5. T039 runner hiện tại nhập `results/T-036/runs/kiem-r1-after-002/code`; giữ file đó, tạo `execute_common.py` từ logic thực với pin_loader. Dựng lại model hiện có và replay132 graph cùng mapping/context, so từng tập/members/exclusions/mẫu số. Không biến “không có SMTP được ghi” thành lý do bỏ hồi quy hoặc đóng source/runtime OPEN.
6. Xuất diff riêng từng tác động; phần không SMTP phải bằng baseline nếu không có hệ quả thiết kế đã khai báo. Mọi khác biệt ngoài dự kiến phải lần theo đầu vào→mapping→key→set; không sửa oracle để PASS. Tiếp nhận cả ba đầy đủ mới publish các bản hiện hành theo cùng pin. Mỗi output mang pin của lượt sinh ra nó; chuyển hiện hành không viết lại lịch sử. Kiểm complete diff/phạm vi/LOG append-only/STATE đúng dòng/prompt chuẩn, rồi Minh quyết riêng nghiệm thu.

**Tự kiểm hiện có:** `oracle-before-code.json` ghi24case literal và5case hồi quy trước candidate; `kiem-preview-001/checks.json` **29/29 đạt**. Có rebuild exact-equal legacy T036, frozen T038, **full model T037 hiện tại và T039 hiện tại**, và phản ví dụ thay semantics. `candidate-code-hashes.json` cho biết builder không sửa. Đây chưa phải full1069/132 comparator replay, chưa phải adoption/common manifest; phần ấy chờ quyền chung vì thay giao thức và bản dùng ba nhánh. Không có SMTP thật/network hoặc evidence delivery.

## Phương án, câu hỏi nguồn và giới hạn

- **Giữ comparator cấu trúc hiện tại + tiếp nhận builder SMTP:** là phương án ít thay đổi, hợp lệ nếu ghi rõ chỉ so cấu trúc. Đây là baseline T037 đã có, không phải unsupported. Chưa phân biệt hai protocol cùng owner; Minh có thể chọn phương án này thay marker và phải cập nhật gói trước áp dụng.
- **Marker SMTP đề xuất:** phân biệt chặng SMTP trong phép so; trace thiếu protocol sẽ có thêm thiếu bằng chứng tương ứng, không chứng minh cạnh nguồn sai hoặc runtime không gửi. Có thể làm giảm giao khi telemetry thiếu channel. Đây là giả định thiết kế để thử, chưa là chọn phương pháp P6.
- **Schema transport/authority/port/TLS tổng quát:** phân biệt sâu hơn nhưng cần telemetry/adapter/chuẩn hóa có nguồn và quyền riêng; marker hiện tại không trả lời câu hỏi ấy. Đổi taxonomy mail/broker không có căn cứ cho cạnh gửi hiện tại.

Đáp ứng DT18-NV2, MRP P5 và bước1 của cô ở biểu diễn quan hệ/địa chỉ có nguồn và so hai nguồn; không xác nhận cơ chế phát hiện/ranking, RQ3/RQ5, lợi ích đồ thị, G3 hay mở test. Runtime lineage TT/OB, hiệu lực thư viện/TLS/delivery, phạm vi deployment và alias vẫn OPEN. Để phân xử runtime cần image/build/instrumentation/deployment và trace channel có provenance từ chủ nguồn qua Minh; không thể lấy fixture hoặc cờ thiếu dữ liệu thay bằng chứng. Nếu cần authority/port/TLS, trình schema/thu thêm tương ứng trước kết luận. Mapping sai mail-server/channel do suy đoán/type tự nâng hoặc accepted=delivered là điều kiện thất bại, phải dừng kết luận phụ thuộc.

## Chi phí cập nhật

**Dự toán CANDIDATE chưa đo:37 phút máy, khoảng600MB output**, chạy tuần tự trong một phiên, không tải nguồn. Gồm shared2phút/50MB, T03710/150, T03810/150, T0395/100, dự phòng một lượtTT10/150. Không dùng dự toán V1 31phút/550MB vì chưa gồm hồi quy đầy đủ FT/OB. RAMTT dự trù0.5GiB; các peak khác chưa đo, không cộng peak. Thời gian soạn/đọc và mọi lỗi chưa biết không phải benchmark; nếu một lượt dự kiến >1giờ hoặc phát sinh phạm vi/tải khác thì báo Minh đúng luật hiện hành.

Số đã đo chỉ để tham khảo: TT pin cũ `kha-thi.json#/full_and_pilot_runs` ~4–6phút cho1069; OB run004 `cost.json`132graph,3.669giây, peak71557120bytes, **isolated_benchmark=false**, không ngoại suy sang full regression. Preview29 chỉ đo trong `checks.json#/elapsed_seconds`, không đo peak riêng. Kế hoạch37phút là dự trù tác vụ/kiểm/phân tích, không suy từ phép nhân thời gianOB. Giữ mọi lượt và cập nhật số thực sau chạy.

## Tiêu chí gói được áp dụng xong sau duyệt

Hợp đồng/README/WHY/DECISIONS/SPEC đúng nghĩa comparator mới; patch chỉ compare và builder giữ byte T037; toàn T036/R1/SMTP và full model/fixture T037,1069TT,132OB có artifact so tập/members/loại trừ/mẫu số, input/ordering/hash/projection/mapping; tách delta TT và comparator. Pin manifest mới tồn tại/được hash và cả ba runner dùng đúng nó, output cũ nguyên pin. Trạng thái OPEN khoa học giữ đúng nguồn, Minh quyết nghiệm thu riêng. Nếu chỉ preview đạt thì gói vẫn **chưa áp dụng**.
'''
write(PKG/'plan.md',plan)

specdirs={'T-036':'T-036-p5b-hop-dong-chung','T-037':'T-037-p5b-flashticket','T-038':'T-038-p5b-trainticket','T-039':'T-039-p5b-online-boutique'}
specs=[f'tasks/{d}/SPEC.md' for d in specdirs.values()]
logs=[f'tasks/{d}/LOG.md' for d in specdirs.values()]
current={}
for t in ('T-037','T-038','T-039'):
    names=['ban-ghi.json','nguon.json','mapping.json','do-thi/thuc-the.json','do-thi/thao-tac.json','phan-tich-chenh-lech.md','phan-tich-chenh-lech.json','kiem-dung-dan.md','kha-thi.json','ban-giao.md','prompt-claude.txt','manifest.json']
    names+=['doi-chieu/index.json'] if t=='T-038' else (['doi-chieu/tong-hop.json'] if t=='T-039' else [])
    current[t]=[f'results/{t}/{n}' for n in names if (ROOT/f'results/{t}/{n}').is_file()]
save(PKG/'plan.json',{'version':2,'status':'CANDIDATE_NOT_APPLIED_AWAITING_MINH_APPROVAL','input_state':'input-state.json',
    'current_facts':{'T037_SMTP_representation_implemented':True,'T037_full_model_exists':True,'T039_full_comparator_exists':True,'T039_graph_count':132,'T038_graph_count':1069},
    'new_decisions':['change SMTP matching semantics including endpoints','publish new common manifest and adopt via all three actual runners','T038 add provenance-backed SMTP relation using existing builder support'],
    'not_new_work':['add SMTP enum to builder','create missing T037 model','create missing T039 comparer'],
    'proposed_writes':{'modify_shared_exact_patch':['src/do_thi_tinh/compare.py'],'modify_shared_docs':['src/do_thi_tinh/README.md'],
         'unchanged_shared':['src/do_thi_tinh/build.py','src/do_thi_tinh/__init__.py'],
         'new_run_output_scopes':list(newruns.values()),'permission_and_pin_documents':specs+logs+['docs/WHY.md','docs/DECISIONS.md','docs/STATE.md'],
         'current_outputs_after_all_adoption_pass':current,
         'run_files':{'common':['before/','pin.json','pin_loader.py','oracle.json','checks/','cost.json','diff.json','manifest.json','ban-giao.md','prompt-claude.txt'],
                      'T036':['hop-dong.md','nguon.json','code/__init__.py','code/build.py','code/compare.py','code-hashes.json','check_regression.py'],
                      'T037':['check_adoption.py','ban-ghi.json','nguon.json','do-thi/','doi-chieu/'],
                      'T038':['engine_smtp.py','compare_dev_smtp.py','ban-ghi.json','nguon.json','mapping.json','do-thi/','doi-chieu/'],
                      'T039':['execute_common.py','ban-ghi.json','nguon.json','mapping.json','do-thi/','doi-chieu/']}},
    'runner_adoption':{'T037':'graph-003 full model + runner.py/assemble-complete.py and existing fixtures; input-code-hashes.json',
                      'T038':'new explicit loader, preserve engine.py:pinned_api and compare_dev.py legacy; comparator-only vs relation-delta factorial check',
                      'T039':'new execute_common.py adapts current execute_pinned.py; full132 replay; legacy runner snapshot import remains historical'},
    'regression':{'T037':'full current model and all existing fixtures','T038':1069,'T039':132,'compare':['sets','members','exclusions','denominators','projection','mapping','unknown','ordering','input hashes']},
    'semantics':{'change':'SMTP marker at endpoints and typed','marker':['smtp',None],'trace_channel_optional':True,'infer_missing_channel':False,'authority_port_tls_delivery_verified':False},
    'preview':{'checks':29,'all_ok':True,'result':'kiem-preview-001/checks.json','full_comparison_replay':False,'adoption':False},'cost':budget})

readme='''# Bộ dựng từ bản ghi có nguồn và bộ đối chiếu

Hai API build/compare và project giữ nguyên exports, Python3.12 standard library, không nhận nhãn/không tự đọc file. Hợp đồng R1 lịch sử ở results/T-036/hop-dong.md. T037 đã có delta builder SMTP được Minh duyệt, ghi tại results/T-037/hop-dong-smtp.md; comparator trước bản mới vẫn so cấu trúc theo giới hạn ghi ở đó.

Sau khi gói V2 được Minh duyệt và toàn hồi quy đạt, hợp đồng/pin mới là results/T-036/runs/doi-chieu-smtp-001/manifest.json và hop-dong.md. Runner phải nhận đường dẫn/SHA/created_utc từ manifest thực và kiểm module snapshot/live; không lấy HEAD hoặc đổi nhãn output cũ. Snapshot R1/T037 cũ vẫn nguồn của kết quả cũ.

Builder nhận smtp ở hai loại gọi, messaging=null; unknown không tự thành sync. Comparator mới nhận optional call channel; SMTP giữ marker ở endpoints/typed, trace thiếu channel không tự được điền từ static. Typed loại unknown. Context/provenance giữ host/port/TLS/outcome nhưng matching không xác minh authority/TLS hoặc delivery. HTTP/RPC legacy giữ quy tắc cấu trúc đã khai báo. Graph T035 nguyên bản không đổi, adapter P9 muốn phát channel cần quyền/nguồn riêng.

Resource binding/signal không tự thành cạnh runtime; shared metric không nhân mỗi operation. Hồi quy T036/R1/SMTP và T037 full model/fixture, TT1069, OB132 dùng runner nhận pin tường minh ở các run doi-chieu-smtp-001, lưu mọi lượt kể cả lỗi. Chỉ cập nhật bản hiện hành sau tất cả đạt; không suy nghiệm thu task/G3/test/commit. Các trường hợp cần authority/port/TLS hoặc runtime proof phải trình dữ liệu/schema riêng.
'''
write(PKG/'README.shared-proposed.md',readme)
appendix='''\n## Phụ lục V2: đối chiếu SMTP và tiếp nhận phiên bản chung (chỉ nối sau Minh duyệt)\n\nGiữ pin/ngoại lệ/đầu ra lịch sử trong nội dung cũ. T037 đã hỗ trợ SMTP theo delta được duyệt; T039 đã có132graph dùng snapshot gốc. Gói V2 đổi comparator (optional call channel và marker SMTP cả endpoints/typed) và chuyển cả ba nhánh sang manifest results/T-036/runs/doi-chieu-smtp-001/manifest.json sau hồi quy đầy đủ. Builder giữ nguyên byte T037. Quyền ghi đúng plan.json V2 đã duyệt; hồi quy T036/R1/SMTP, full model/fixture T037,1069TT,132OB và so tập/members/exclusions/mẫu số/input/hash/ordering phải đạt, tách comparator khỏi delta TT. Giữ script/output/pin cũ; runner mới kiểm manifest+snapshot/live tường minh. Các bản hiện hành chỉ chuyển sau cả ba PASS. created_utc/SHA manifest mới lấy từ file thực đã kiểm, hiện OPEN. Nguyên lời và ngày Minh duyệt lấy từ quyết định thực; không suy nghiệm thu task/G3/test/commit.\n'''
drafts=[]
for s in specs:
    text=(ROOT/s).read_text(encoding='utf-8-sig')
    paras=[p for p in text.split('\n\n') if 'Cả T-037/T-038/T-039 dùng cùng snapshot' in p]
    drafts.append({'path':s,'before_sha256':sha(ROOT/s),'before_pin_paragraphs':paras,'operation':'append exact version appendix; preserve existing approval and pin history','after_append':appendix})
drafts.append({'path':'src/do_thi_tinh/README.md','before_sha256':sha(ROOT/'src/do_thi_tinh/README.md'),'operation':'replace whole file','after_file':rel(PKG/'README.shared-proposed.md')})
why='''\n### Bổ sung lý do: phân biệt protocol SMTP trong đối chiếu và hợp nhất phiên bản\n\nChọn (sau Minh duyệt): giữ builder SMTP T037 đã kiểm; comparator optional call channel/marker SMTP ở cả hai view; unknown giữ nguyên. Vì sao: phân biệt cùng owner nhưng khác chặng protocol khi so nguồn, đáp ứng nhu cầu kỹ thuật P5/DT18-NV2, không là bằng chứng sửa hạn chế RCA. Đã xét giữ comparator cấu trúc (hợp lệ nếu chấp nhận giới hạn hiện tại), marker SMTP và schema địa chỉ tổng quát. Gói đề nghị marker; không xác minh authority/port/TLS/delivery.\n\nBằng chứng: T037 graph003 và delta đã duyệt; T038 nguồn MailService/config có provenance; T039 run004 có comparer132graph; preview V2 oracle29/checks và comparison-before-after chỉ chứng minh hành vi synthetic/rebuild. Full1069/132 replay và tiếp nhận chung chưa chạy ở giai đoạn đề xuất, chỉ ghi kết quả sau artifact thực. Trace thiếu channel có thể giảm giao theo thiết kế; không phải cạnh nguồn sai hoặc không có runtime. Mapping nhầm/channel suy/type tự nâng và accepted=delivered là failure. Runtime/build/instrumentation/địa chỉ vẫn OPEN cần dữ liệu chủ nguồn. Phụ thuộc: biểu diễn TT SMTP, khả năng so P5b và common pin; chưa chọn P6/khẳng định lợi ích/G3.\n'''
drafts += [{'path':'docs/WHY.md','operation':'append after actual approval; assign source register id without collision','before_sha256':sha(ROOT/'docs/WHY.md'),'after_append':why},
           {'path':'docs/DECISIONS.md','operation':'append exact actual Minh approval/date/id only after approval','before_sha256':sha(ROOT/'docs/DECISIONS.md'),
            'proposed_record':'Minh duyệt gói V2 đổi phép đối chiếu SMTP và chuyển phiên bản chung theo plan.json/filelist; dùng lại builder T037, kiểm full T037/1069TT/132OB trước tiếp nhận. Nguyên lời/ngày/mã quyết định: OPEN cho tới khi Minh duyệt thực. Không suy nghiệm thu/test/commit.'}]
save(PKG/'docs-before-after.json',{'status':'DRAFT_NOT_APPLIED','replacements':drafts,'LOG':'append real approval/actions/checks only','STATE':'only four task rows after approved action, read latest under exclusive file lock'})

# Current entry redirects; every byte of the V1 package is preserved in before/package-v1.
target=rel(PKG)
write(OLD/'plan.md',f'''# Gói SMTP hiện hành — V2 ngày16/10/2026\n\n**Bản kế hoạch hiện hành:** [đổi phép đối chiếu SMTP và hợp nhất phiên bản](../../../cap-nhat-goi-smtp-001/package/plan.md).\n\nT037 đã hỗ trợ SMTP và có mô hình; T039 đã đối chiếu đủ132graph. Điều còn xin duyệt là đổi quy tắc matching, tiếp nhận delta TT và chuyển ba nhánh sang một manifest mới, hồi quy đầy đủ T037/1069TT/132OB. Chưa áp dụng code/pin.\n\nFile kế hoạch trước đây và toàn bộ24file V1 giữ nguyên tại [bản lưu](../../../cap-nhat-goi-smtp-001/before/package-v1/plan.md). Patch/oracle/checks26 trong thư mục cũ này là **vật liệu V1 lịch sử**, không phải patch hiện hành. V2 có patch chỉ comparator và29checks; xem plan.json/docs-before-after.json/package-manifest trong thư mục V2.\n'''.replace('../../../cap-nhat','../../cap-nhat'))
save(OLD/'plan.json',{'status':'SUPERSEDED_BY_V2','current_plan':target+'/plan.json','current_markdown':target+'/plan.md','historical_package':rel(RUN/'before/package-v1'),'warning':'old patch/build change, 26 checks and cost are historical only'})
save(OLD/'package-verification.json',{'status':'SUPERSEDED_BY_V2','historical_verification':rel(RUN/'before/package-v1/package-verification.json'),'current_package':target,'active_pin_changed':False})
# Keep remaining V1 materials as historical, explicitly indexed after entry-point update.
save(OLD/'package-manifest.json',{'status':'HISTORICAL_V1_WITH_CURRENT_V2_REDIRECT','current_package':target,'original_package':rel(RUN/'before/package-v1'),
     'files':[{'path':p.relative_to(OLD).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(OLD.rglob('*')) if p.is_file() and p.name!='package-manifest.json']})

summary=f'''# Gói SMTP V2 chờ Minh duyệt\n\nT037 **đã hỗ trợ SMTP và dựng full model có điều kiện**; T039 **đã đối chiếu132graph** bằng snapshot R1. Hai task vẫn chờ phản biện, chưa nghiệm thu. T038 vẫn dùng pin R1 và chưa đưa quan hệ SMTP vào model.\n\n[Gói hiện hành](runs/cap-nhat-goi-smtp-001/package/plan.md) đề xuất **đổi phép đối chiếu SMTP và hợp nhất phiên bản dùng chung**, dùng nguyên builder T037, patch chỉ comparator và cập nhật README/hợp đồng/pin theo filelist. Đây là thay đổi semantics (cả endpoints), không chỉ thêm hỗ trợ SMTP. Giữ lựa chọn so cấu trúc hiện tại là phương án hợp lệ nếu Minh chọn chấp nhận giới hạn đó.\n\nCó29checks preview đạt, gồm rebuild nguyên full model T037/T039 và phản ví dụ semantics; chưa là full comparator replay. Sau duyệt phải hồi quy T036/R1/SMTP, full model/fixture T037, **1069TT và132OB** bằng runner/pin mới, tách ảnh hưởng comparator khỏi deltaTT. Kế hoạch dự trù37phút máy/600MB, chưa đo; thay dự toán V1.\n\nXem plan.json, docs-before-after.json, input-state.json, patch và package-manifest trong thư mục V2 để duyệt cụ thể. BảnV1 giữ tại runs/cap-nhat-goi-smtp-001/before/package-v1/. Chưa sửa shared/SPEC/WHY/DECISIONS hay chuyển pin; không suy nghiệm thu/G3/test/commit. Runtime lineage, authority/TLS/delivery và các OPEN nguồn vẫn giữ nguyên.\n'''
write(OUT/'goi-sua-SMTP.md',summary)
for name in ('ban-giao.md','hoan-tat-trong-quyen.md','de-nghi-tiep-theo.md'):
    text=(RUN/f'before-{name}').read_text(encoding='utf-8-sig')
    text=text.replace('26 checks','29 checks V2').replace('26checks','29checks V2').replace('26 checks','29 checks V2').replace('26 checks','29 checks V2')
    text=text.replace('31 phút máy/550 MB','37 phút máy/600 MB')
    text=text.replace('SMTP trong hợp đồng chung chưa được duyệt/áp dụng','T038 chưa tiếp nhận SMTP và gói đổi comparator/common pin chưa được duyệt/áp dụng')
    text=text.replace('phần áp dụng sửa SMTP chung còn chờ Minh duyệt gói cụ thể','phần tiếp nhận SMTP ở T038, đổi comparator và common pin còn chờ Minh duyệt gói V2')
    text+='\n\nCập nhật16/10/2026: T037 đã hỗ trợ SMTP/full model; T039 đã so132graph dùng snapshot gốc. GóiV2 tại runs/cap-nhat-goi-smtp-001/package/plan.md xin đổi semantics comparator và phiên bản chung; dùng nguyên builder T037. Preview29 đạt, chưa replay1069TT/132OB bằng comparator mới. Kế hoạch hồi quy đầy đủ cả ba nhánh và dự trù37phút/600MB thay góiV1; không đổi model/so/pin hiện hành hoặc nghiệm thu.\n'
    write(OUT/name,text)
for name in ('hoan-tat-trong-quyen.json','kha-thi.json'):
    d=load(RUN/f'before-{name}')
    d['SMTP_current_state']={'T037_SMTP_representation_implemented':True,'T037_full_model_exists':True,'T039_full_comparator_exists':True,
        'T038_active_model_SMTP_adopted':False,'proposed_comparator_change_applied':False,'common_pin_converged':False,'proposal':target+'/plan.md'}
    if name=='kha-thi.json':
        d['SMTP_preview_V1_historical']=d.pop('SMTP_preview')
        d['SMTP_preview']={'checks':29,'elapsed_seconds':oracle['elapsed_seconds'],'RAM_measured':False,'active_pin_changed':False,'result':target+'/kiem-preview-001/checks.json'}
        d['proposed_shared_future_cost']=budget
    else:
        d['next_authorization_needed']={'action':'Approve V2 comparator semantics change, adopt existing SMTP builder support and new common pin after full FT/TT/OB regression','proposal':target+'/plan.md'}
    save(OUT/name,d)
with (OUT/'LICH-SU.md').open('a',encoding='utf-8') as f:
    f.write('\n16/10/2026 — Cập nhật gói SMTP V2 theo artifact hiện tại: T037 có SMTP/full model, T039 có132graph comparer. Giữ toàn góiV1 và manifest cũ trong runs/cap-nhat-goi-smtp-001/before/. V2 chỉ đổi đề xuất comparator/common pin,29preview đạt; model005/1069kết quả T038 không thay.\n')
prompt=(RUN/'before-prompt-claude-smtp.txt').read_text(encoding='utf-8-sig')
prompt=prompt.replace('runs/hoan-tat-trong-quyen-001/smtp','runs/cap-nhat-goi-smtp-001/package')
prompt=prompt.replace('Đề xuất sửa hợp đồng SMTP chung','Đề xuất V2 đối chiếu SMTP và phiên bản chung')
prompt=prompt.replace('results/T-036/manifest.json và snapshot kiem-r1-after-002/code; results/T-038/manifest.json;',
                      'results/T-036/manifest.json và snapshot kiem-r1-after-002/code; results/T-037/manifest.json, hop-dong-smtp.md và runs/graph-003/; results/T-038/manifest.json; results/T-039/manifest.json và execute_pinned.py;')
write(OUT/'prompt-claude-smtp.txt',prompt)
print('Prepared V2 plan/docs and current entry points; preview 29 PASS; shared and pins untouched.')
