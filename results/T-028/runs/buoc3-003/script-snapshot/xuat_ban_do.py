"""Render fixed result tables and the evidence limits. No method/raw I/O."""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
NAMES={'baro':'BARO','simplerca':'SimpleRCA','microrank_full':'MicroRank full','tracerca':'TraceRCA','circa_ols_da':'CIRCA OLS+RHT+DA','torai_B':'TORAI B'}
MS=['M1','M2','M3','M4','M5','M6','M0']
TEXT={
 'M1':('Root ngoài tập quan sát O','Rào cản trực tiếp: pipeline không quan sát root trong tập dùng cho lượt xếp hạng. Đã đối chiếu membership từ bản ghi. Chưa tách vì sao: coverage kênh, cửa sổ, mapping hay preprocessing. Không chứng minh root không có lỗi. Can thiệp tăng coverage hoặc giữ preprocessing cần chạy lại phương pháp, ngoài SPEC.'),
 'M2':('Root thuộc O nhưng ngoài tập trả về R','Rào cản trực tiếp của luật trả về. Đã kiểm O/R. TraceRCA lọc ji không hữu hạn; nếu M6 True thì có chuỗi không span A dương theo luật native ⇒ ji NaN ⇒ ngoài R. Chiều ngược chưa được suy: chỉ có N, thiếu baseline hoặc điều kiện khác cũng có thể làm root ngoài R. Trung gian ji không được lưu đầy đủ nên không chạy lại để điền. Các khả năng khác gồm lọc điểm, thiếu quan sát hoặc mapping.'),
 'M3':('Hòa cắt biên top-k','Phân rã trực tiếp bất định hòa từ phân phối chính xác từng seed. Đã kiểm full key, nhóm hòa và khối TORAI; khác thắng/thua giữa seed không bị gọi là hòa. Hòa không giải thích tại sao các điểm giống nhau. Có thể do luật đếm rời rạc, điểm giống nhau, candidate/coverage hoặc thứ tự nội khối. Không đổi tolerance hoặc phá hòa theo nhãn.'),
 'M4':('CIRCA thuộc cohort lỗi làm tròn đã xác nhận','Membership dùng danh sách loại dev19 đã khóa. Đã kiểm diagnostics.nodes sau prune, RHT và full key DA trong các ca đọc tay. Đây là lỗi số học xác nhận cấp ca; chưa chứng minh nó gây từng thất bại của root/DA. Tín hiệu raw, quan hệ gọi, preprocessing và mô hình hồi quy vẫn có thể giải thích một thứ hạng. Không chạy bản sửa/ablation trong task.'),
 'M5':('Ancestor quan sát được chắc chắn trước root','Ứng viên: ancestor trong graph N và ưu tiên thứ hạng cùng xuất hiện. Đã kiểm cha-con trong N, graph quality, full key/khối, proxy P95 và P0 có điều kiện. Chưa xác định thứ tự khởi phát, lan, caller tự bất thường, tải/tài nguyên chung hoặc sự cố đồng thời. P0 không giữ thiên hướng nhận điểm riêng của entity, số kênh/operation hay cấu trúc chấm điểm. Coverage, clock/nền/nhãn, lỗi graph/mapping, thành phần cohort và dao động hữu hạn còn là giải thích khả thi. Can thiệp hoặc đối chứng giữ những yếu tố đó cần phạm vi khác; không được chạy ở đây.'),
 'M6':('Không có bằng chứng cục bộ dương theo luật native','Ứng viên phụ thuộc phương pháp. SimpleRCA dùng score lưu sẵn bằng 0, MicroRank/TraceRCA dùng baseline hữu hạn và không span A đạt luật đã khai, CIRCA xét tập không rỗng trong diagnostics.nodes sau prune với mọi RHT<3. BARO/TORAI N/A. Đã kiểm arithmetic/cửa sổ/availability và độ nhạy proxy; không coi missing là bình thường. Giảm tín hiệu, kênh khác, cửa sổ/clock không khớp, nền chưa sạch, nhãn hoặc coverage vẫn có thể giải thích. Đổi tín hiệu/threshold hoặc chạy can thiệp ngoài phạm vi.'),
 'M0':('Chưa phân loại','Không có M1–M6 True ở seed sai đủ điều kiện theo quy tắc đã chốt. Giữ cả False và N/A; không tạo cơ chế sau khi nhìn kết quả. Đã đọc tay mẫu cố định, lưu score/thứ hạng/availability. Cấu trúc chấm điểm, tín hiệu nhiều nguồn, giảm tín hiệu, coverage và nền/nhãn có thể còn giải thích; dữ liệu quan sát chưa phân xử nguyên nhân.')}


def read(p):return json.loads(p.read_text(encoding='utf-8'))
def fmt(x):return 'N/A' if x is None else str(x) if isinstance(x,int) else f'{x:.6g}'
def table(headers,rows):return '\n'.join(['| '+' | '.join(headers)+' |','| '+' | '.join(['---']*len(headers))+' |']+['| '+' | '.join(str(x).replace('|',' / ') for x in row)+' |' for row in rows])
def fraction(n,d):return f'{n}/{d}' if d else 'N/A (0 ca)'


def main():
 p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);a=p.parse_args();run=ROOT/'results/T-028/runs'/a.run_id
 d=read(run/'ca-sai.json');s=read(run/'summary-tables.json');conc=read(run/'concentration.json');schema=read(run/'schema-tables.json')
 rp=str(run.relative_to(ROOT)).replace('\\','/');rows=d['main_rows'];ss=s['mechanism_tables'];overall=[x for x in ss if x['group_field']=='overall']
 lines=['# Bản đồ hạn chế xếp hạng chế độ (a) — T-028','',
 'Phân tích dev theo codebook đã duyệt, bản chốt `results/T-028/runs/chot-codebook-002/manifest.json`. Rào cản membership/luật trả về được kiểm trực tiếp; các dấu hiệu còn lại là ứng viên, chưa kiểm nhân quả. Primary chỉ phục vụ trình bày. Kết quả này chưa xác nhận hoặc phủ nhận “lan có đáng kể”; không định nghĩa nhãn lan, không kết luận về giá trị đồ thị.','',
 '## 1. Phạm vi và ca sai','',
 'Giữ bảng chính RE2-TT dev30 và Nezha-OB main, tất cả phương pháp/trạng thái. TORAI gộp Hit theo ca, giữ từng seed. Non-OK báo riêng; UNSUPPORTED không là chất lượng ranking hay bằng chứng không có tín hiệu. Sai hạng 1 và 5 không cộng thành hai ca.','',
 f'Nguồn mọi số ở bảng sau: `{rp}/summary-tables.json` → `mechanism_tables` (overall), đối chiếu `{rp}/ca-sai.json` và bước 1 `results/T-028/runs/danh-sach-001/step1.json`.','',
 table(['Dataset','Phương pháp','k','Đúng OK','Sai OK','Non-OK','Tổng','Σ(1−Hit)'],[[x['dataset'],NAMES[x['method']],x['k'],x['n_correct_OK'],x['n_wrong_OK'],str({st:n for st,n in x['status_counts'].items() if st!='OK'}),x['n_cohort'],fmt(x['expected_misses_including_non_OK'])] for x in overall]),'',
 'Tổng mức trượt kỳ vọng có non-OK Hit=0, khác số ca sai ranking. Phần tổng cohort và non-OK riêng giữ mẫu số trong JSON nguồn.','',
 '## 2. Nhãn chính, đa nhãn và đối chứng','',
 f'Nguồn mọi số: `{rp}/summary-tables.json` → `mechanism_tables`. Mỗi ô nhãn là số ca / tổng ca OK sai; tổng cohort ở cột riêng. Bảng JSON còn giữ số nhãn/tổng cohort và số False/N/A.','',
 table(['Dataset','Phương pháp','k','Tổng cohort','Sai OK']+MS,[[x['dataset'],NAMES[x['method']],x['k'],x['n_cohort'],x['n_wrong_OK']]+[fraction(x['primary'][m],x['n_wrong_OK']) for m in MS] for x in overall]),'',
 'Đây là bảng primary theo thứ tự M1→M2→M3→M4→M5→M6→M0; không là nguyên nhân trội. Bảng đa nhãn, đối chứng đúng/sai, số True/False/N/A và phân tầng theo ô/loại lỗi/vị trí/root được xuất đầy đủ tại `bang-theo-o-va-doi-chung.md` và JSON nguồn.','',
 'Các quan hệ cấu trúc cần giữ cạnh đối chứng: M1/M2 kéo theo sai; M3 loại Hit=1; M5 True không thể có ở ca đúng top-1; M6 SimpleRCA kéo theo sai top-1; M6 TraceRCA kéo theo M2. M4 thuộc cohort lỗi chưa chứng minh lỗi đó gây mỗi thất bại. Nhóm đúng hoặc sai rỗng cho đối chứng N/A. Các chênh lệch là liên hệ quan sát, không xác nhận nguyên nhân độc lập.','',
 '## 3. Cơ hội nhận M5 và mức nền P0','',
 'Graph G_N là graph phân tích từ cha-con cùng trace trước mốc; không gọi nó là graph native MicroRank hay graph nhân quả CIRCA. BARO/TORAI không nhận graph này, N-end chỉ là bối cảnh. P0 giữ vị trí root, cấu trúc hòa/khối, chiều dài trả về L và tập quan sát O; hoán vị danh tính O trừ root. Chỉ so số cờ cơ sở M5 True với ΣP0 trên cùng tập đủ điều kiện. Root ngoài R/graph thiếu/ranking không hợp lệ cho N/A. Không dùng primary=M5, không OR P0; TORAI báo từng seed.','',
 f'Nguồn mọi số: `{rp}/summary-tables.json` → `P0_tables` (overall); bảng theo ô ở cùng file.','',
 table(['Dataset','Phương pháp','k','Seed','Đủ điều kiện','Tổng bản ghi','M5 True','ΣP0','Chênh'],[[x['dataset'],NAMES[x['method']],x['k'],x['seed'],x['n_eligible'],x['n_records_total'],x['n_base_M5_True_on_eligible'],fmt(x['sum_P0']),fmt(x['difference'])] for x in s['P0_tables'] if x['group_field']=='overall']),'',
 'Chênh chỉ mô tả sai lệch với kỳ vọng của null. Không có p-value, ngưỡng đáng kể hoặc số liệu “nhãn lan”. Null không giữ thiên hướng nhận điểm của entity, số kênh/operation/cấu trúc phương pháp; không loại được lan, caller tự bất thường, tác động chung hoặc sai lệch clock/nền/graph/nhãn.','',
 '## 4. Tập trung và biến thiên đầu ra','',
 'D là Dice overlap kỳ vọng top-k theo phân phối hạng chính xác, D0 là kỳ vọng hoán vị đều độc lập trên đúng O mỗi ca với L giữ nguyên. Cặp TORAI lấy trung bình tổ hợp seed hợp lệ, mỗi cặp ca đóng góp một lần. Cân đều cặp ô khác nhau; cùng ô giữ riêng.','',
 f'Nguồn mọi số: `{rp}/concentration.json` → `equal_cell_weight_summaries`, `cell_pairs`, `case_pairs`, `within_case_seed_pairs`.','',
 table(['Dataset','Phương pháp','k','Quan hệ ô','Ô/cặp ô đủ','Tổng','D','D0','D−D0','1−D'],[[x['dataset'],NAMES[x['method']],x['k'],'cùng' if x['same_cell'] else 'khác',x['n_cell_units_valid'],x['n_cell_units_total'],fmt(x['D']),fmt(x['D0']),fmt(x['delta']),fmt(x['V'])] for x in conc['equal_cell_weight_summaries']]),'',
 'Bảng từng cặp ô và biến thiên seed ở `bang-theo-o-va-doi-chung.md`. Phương pháp một seed: biến thiên seed N/A. Non-OK và thiếu cặp không điền 0. 1−D gồm bất định phá hòa độc lập; D lặp lại không chứng minh thuật toán bỏ qua dữ liệu ca.','',
 '## 5. Tín hiệu root, proxy và schema','',
 f'Bảng BARO root mọi ca (đúng/sai) ở `BARO-du-lieu-root.md` và `{rp}/BARO-root-data.json`; từng metric/native service và nguồn nằm trong `{rp}/ca-sai.json` → `evidence` và `features-no-label`. Đây là quy ước SimpleRCA (strict metric events, trace start P95, log keyword A), không phải luật BARO thực nhận hoặc chuẩn chung. Score BARO có dấu và coverage giữ cạnh dữ liệu; M6/local_nonpositive BARO=N/A.','',
 'Raw metric khác đầu vào sau preprocessing BARO. Không events không chứng minh không có tín hiệu; log lỗi A có thể là nền. Proxy end-split chỉ là bối cảnh BARO, khác bảng root trace start; P95 span không là end-to-end latency. Không thêm tỷ số khi nền bằng 0. Luật trace native ≥ cộng làm tròn có thể đánh dấu span không đổi khi σN bằng hoặc làm tròn về 0; native flag dương không tự chứng minh phân phối thay đổi (codebook §3.2).','',
 f'Nguồn số độ nhạy: `{rp}/summary-tables.json` → `proxy_tables`, giữ τ=2/3/4, mẫu số đủ/N/A và mã ca đổi cờ. Các bảng đầy đủ ở `bang-theo-o-va-doi-chung.md`. Proxy không đổi nhãn/primary; membership/status/hòa có độ nhạy N/A, không thêm tolerance.','',
 f'Schema dùng audit có sẵn: `{rp}/schema-tables.json`, nguồn `results/T-024/cham-a.json` → `raw_column_audit`. Đã xuất từng cột/ô, bảng chéo root, O/R/input_shape sau preprocessing và tên cột vắng. Bảng đọc được ở `schema-va-coverage.md`. Không classifier/L*/hoán vị nhãn; chưa tách tác động schema khỏi root, loại lỗi hoặc preprocessing. Nezha không có audit schema tương đương trong đầu vào được phép nên phần này N/A; không quét test.','',
 '## 6. Từng nhóm và các giải thích khác','']
 for m in MS:
  lines+=['### '+m+' — '+TEXT[m][0],'',TEXT[m][1],'']
  matched=[x for x in overall if x['multi'][m]]
  lines += [f'Nguồn mọi số nhóm: `{rp}/summary-tables.json` → `mechanism_tables`, multi; ví dụ và đối chiếu tiêu chí ở `{rp}/manual-reading.json` và `doc-tay.md`.','',table(['Dataset','Phương pháp','k','Đa nhãn / OK sai','Đa nhãn / cohort'],[[x['dataset'],NAMES[x['method']],x['k'],fraction(x['multi'][m],x['n_wrong_OK']),fraction(x['multi'][m],x['n_cohort'])] for x in matched]) if matched else 'Không có ca OK sai được gán nhóm này trong bảng chính.','']
 lines+=['## 7. Đối chiếu lời tác giả','',
 table(['Phương pháp','Giới hạn tác giả/hồ sơ','Nguồn'],[
 ['BARO','Giả định metric ảnh hưởng latency/error; lỗi tương quan có thể đưa nhiều affected service lên hạng; khái quát deployment/fault còn hạn chế.','results/T-013/ho-so-baro.md §6; docs/knowledge/K1-phuong-phap-rca.md'],
 ['SimpleRCA','Type I/II; threshold-count kém khi lỗi tinh tế/mạng và root không ồn nhất; triệu chứng đơn giản không là chứng minh nhân quả.','results/T-017/ho-so-simplerca.md §6'],
 ['MicroRank','Lỗi không lệch latency, thiếu trace/instrumentation, overhead và tính reactive; detector không phủ mọi hệ.','results/T-015/ho-so-microrank.md §6'],
 ['TraceRCA RCAEval','Hồ sơ không có giới hạn riêng tác giả; điều kiện baseline/ji/zero-std là suy từ code, không quy cho bài gốc.','results/T-015/tracerca-rcaeval.md §6'],
 ['CIRCA','Nền chưa phủ parent values gây bias; meta/common cause ẩn, DA cần thêm dữ liệu thực.','results/T-014/ho-so-circa-kien-truc.md §6'],
 ['TORAI','Root indicator cần đổi rõ; root yếu có thể đưa affected service lên đầu; lệch mốc và tool/system/fault hạn chế kết luận.','results/T-016/ho-so-torai.md §6']]),'',
 'Lời tác giả là căn cứ đối chiếu khái niệm. Không chuyển thành kết luận cơ chế đã xác nhận trên cohort T-028. Các lỗi triển khai đã sửa và các giả thuyết đọc từ code được tách khỏi lời tác giả.','',
 '## 8. Bảng phụ, kiểm và giới hạn','',
 f'CIRCA dev19 dùng lại evidence dev30, giữ danh sách loại lỗi làm tròn; số/bằng chứng ở `{rp}/ca-sai.json` → `circa_dev19_conditional`, không thay mẫu chính. Nezha A/B/trace_guard chỉ giữ status/Hit có sẵn ở `nezha_saved_sensitivity_flags`; ca ngoài B giữ not_in_cohort, không có đặc trưng hoặc cơ chế mới.','',
 f'Kiểm độc lập: `{rp}/independent-ranking.json`, `{rp}/independent-statistics.json`, `{rp}/provenance-checks.json`; tự kiểm/phạm vi cuối ở `{rp}/final-verification.json`. Mẫu theo mã mờ tăng dần đã khai tại codebook §8; không chọn theo root/Hit hoặc giá trị đặc trưng. Đọc tay: `{rp}/manual-reading.json`, `doc-tay.md`; mọi seed liên quan được giữ.','',
 'RE2 có ít root và graph N lặp lại; Nezha cadence metric thưa, cửa sổ trace N ngắn, clock/mốc/nền sạch còn OPEN theo WHY-37 và nguồn T-026. Giữ các khác biệt U, loại lỗi, độ dài N; so sánh hai dataset chỉ mô tả, không gộp độ chính xác. Test/giữ ngoài chưa mở nên tính đại diện chưa kiểm.','',
 'Bằng chứng kiểm được tới membership, hòa, score/diagnostics lưu sẵn, luật thống kê native, quan hệ caller trong N, schema và mức nền có điều kiện. Chưa phân xử nhân quả, thứ tự khởi phát hoặc các giải thích cạnh tranh đã nêu. Việc chạy lại phương pháp với đầu vào khác/can thiệp nằm ngoài SPEC; không điền trung gian bằng rerun.','',
 'Nơi xử lý câu “lan có đáng kể” vẫn OPEN vì Minh chưa chọn. T-028 không tự giao T-029, không biến câu hỏi đó thành cổng mới. Bằng chứng ở đây là đầu vào cho quyết định tiếp theo của Minh.','']
 (ROOT/'results/T-028/ban-do-han-che-xep-hang.md').write_text('\n'.join(lines),encoding='utf-8')
 detail=['# Bảng phân tầng, đa nhãn và đối chứng T-028','',f'Nguồn mọi số: `{rp}/summary-tables.json` và `{rp}/concentration.json`.','']
 for field in ('overall','cell','fault','nhom_loi','nhom_vi_tri_p75','root'):
  detail += ['## '+field,'',table(['Dataset','Phương pháp','k','Nhóm','Cohort','Sai OK']+MS,[[x['dataset'],NAMES[x['method']],x['k'],x['group'],x['n_cohort'],x['n_wrong_OK']]+[fraction(x['multi'][m],x['n_wrong_OK']) for m in MS] for x in ss if x['group_field']==field]),'']
 detail += ['## Đối chứng cờ cơ sở đúng/sai','',table(['Dataset','Phương pháp','k','Cơ chế','Đúng True/đủ','Đúng N/A','Sai True/đủ','Sai N/A','Trạng thái'],[[x['dataset'],NAMES[x['method']],x['k'],m,fraction(x['base_flags']['correct_OK'][m]['True'],x['base_flags']['correct_OK'][m]['n_eligible']),x['base_flags']['correct_OK'][m]['N/A'],fraction(x['base_flags']['wrong_OK'][m]['True'],x['base_flags']['wrong_OK'][m]['n_eligible']),x['base_flags']['wrong_OK'][m]['N/A'],x['correct_wrong_comparison']] for x in overall for m in MS[:-1]]),'',
 'Các quan hệ cấu trúc tại codebook §5 áp dụng; đối chứng không tự xác nhận nhân quả. TORAI base flags OR trong mọi seed OK; explanation chỉ seed sai.','',
 '## Độ nhạy proxy theo nhóm','',table(['Dataset','Phương pháp','k','Đúng/sai','τ','Split','True/đủ','N/A'],[[x['dataset'],NAMES[x['method']],x['k'],x['ranking_group'],x['tau'],x['split'],fraction(x['n_True'],x['n_eligible']),x['n_NA']] for x in s['proxy_tables'] if x['group_field']=='overall']),'',
 '## Cặp ô D/D0','',table(['Dataset','Phương pháp','k','Ô','Cặp ca đủ/tổng','Seed đủ/tổng','D','D0','D−D0','1−D'],[[x['dataset'],NAMES[x['method']],x['k'],'; '.join(x['cells']),fraction(x['n_case_pairs_valid'],x['n_case_pairs_total']),fraction(x['n_seed_pairs_valid'],x['n_seed_pairs_total']),fmt(x['D']),fmt(x['D0']),fmt(x['delta']),fmt(x['V'])] for x in conc['cell_pairs']]),'',
 '## TORAI biến thiên seed từng ca','',table(['Dataset','Ca','k','Seed','D','D0','D−D0','1−D'],[[x['dataset'],x['opaque_id'],x['k'],str(x['seed_left'])+' / '+str(x['seed_right']),fmt(x['D']),fmt(x['D0']),fmt(x['delta']),fmt(x['V'])] for x in conc['within_case_seed_pairs']]),'']
 (ROOT/'results/T-028/bang-theo-o-va-doi-chung.md').write_text('\n'.join(detail),encoding='utf-8')
 rootlines=['# Dữ liệu root BARO theo quy ước SimpleRCA','',f'Nguồn mọi số: `{rp}/BARO-root-data.json`; mỗi ca có source file aggregate và bản ghi BARO. Không dùng các số này làm threshold/nhãn của BARO; local_nonpositive/M6=N/A. Metric là raw finite, trace start-split, log A; proxy end-split giữ riêng.','']
 for r in rows:
  if r['method']!='baro':continue
  ev=r['evidence'];seed=ev['seed_evidence']['single'];root=r['root'];key=seed['ranking']['entity_keys'].get(root)
  rootlines+=['## '+r['dataset']+' / '+r['opaque_id'],'',f"Root `{root}`; status `{r['status']}`. Score entity BARO `{key}`; O={seed['ranking']['n']}, R={seed['ranking']['L']}; Hit@1={fmt(r['hit@1'])}, Hit@5={fmt(r['hit@5'])}. Nguồn: `{r['source']['records'][0]['path']}` và `{ev['source']['path']}` → `/aggregate`.",'',table(['Metric/native service','Entity','nN','nA','Thiếu N/A','μN','σN ddof0','Events strict','Khả dụng'],[[c+' / '+v['native_service'],v['entity'],v['nN'],v['nA'],str(v['missing_N'])+' / '+str(v['missing_A']),fmt(v['muN']['value']),fmt(v['sigmaN']['value']),fmt(v['events']['value']),v['reason'] or v['availability']] for c,v in ev['root_metric_Simple_convention'].items()]),'']
  for split in ('start','end'):
   rootlines += [table(['Trace split','Native service','Entity','nN','nA','P95N μs','P95A μs','τ2','τ3','τ4','Khả dụng'],[[split,name,v['entity'],v['nN'],v['nA'],fmt(v['P95N']['value']),fmt(v['P95A']['value'])]+[str(v['latency_up'][str(t)]['value']) if v['latency_up'][str(t)]['value'] is not None else 'N/A' for t in (2,3,4)]+[v['reason'] or v['availability']] for name,v in ev.get('root_all_native_trace_'+split,{}).items()]),'']
  rootlines += [table(['Log native service','Entity','Dòng A','Keyword count A','Khả dụng'],[[name,v['entity'],fmt(v['rows_A']['value']),fmt(v['keyword_count_A']['value']),v['reason'] or v['availability']] for name,v in ev.get('root_all_native_logs_A',{}).items()]),'']
 (ROOT/'results/T-028/BARO-du-lieu-root.md').write_text('\n'.join(rootlines),encoding='utf-8')
 schemalines=['# Schema và coverage T-028','',f'Nguồn mọi số: `{rp}/schema-tables.json`; raw audit tại `results/T-024/cham-a.json` → `raw_column_audit`. Union cột raw không gồm time theo audit; time.1 nếu có được báo riêng. Không tác động schema nhân quả hoặc classifier/L*.','',table(['Ca','Ô','Root','Union','Hiện','Vắng','Loại vắng','Cột vắng'],[[r['opaque_id'],r['cell'],r['root'],r['union_n'],r['n_present'],r['n_absent'],str(r['missing_by_type']),'; '.join(r['missing_columns'])] for r in schema['by_case']]),'',
 'Bảng từng cột/ô, từng root/cột và native O/R/input_shape được giữ đầy đủ trong JSON nguồn. Suffix khác nhóm được khai giữ other với tên gốc. Từng ca/bản ghi được đối chiếu preprocessing, không suy dấu cột vắng là feature phương pháp. Nezha phần audit này N/A theo phạm vi đầu vào.','']
 (ROOT/'results/T-028/schema-va-coverage.md').write_text('\n'.join(schemalines),encoding='utf-8')
 conditional=d['circa_dev19_conditional']['rows'];savedflags=d['nezha_saved_sensitivity_flags'];fg=defaultdict(list)
 for r in savedflags:fg[(r['view'],r['method'])].append(r)
 supplementary=['# Bảng có điều kiện và đánh dấu độ nhạy có sẵn','',f'Nguồn mọi số: `{rp}/ca-sai.json` → `circa_dev19_conditional`, `nezha_saved_sensitivity_flags`; nguồn gốc và hash ở bước 1. CIRCA tái dùng evidence dev30; Nezha không có đặc trưng/gán mới cho view phụ.','',
 '## CIRCA dev19','',table(['k','Cohort','Đúng OK','Sai OK','Primary'],[[k,len(conditional),sum(r['status']=='OK' and r[f'hit@{k}']==1 for r in conditional),sum(r[f'wrong_OK_at_{k}'] for r in conditional),str(dict(Counter(r['mechanisms'][str(k)]['assignment']['primary'] for r in conditional if r[f'wrong_OK_at_{k}'])))] for k in (1,5)]),'',
 'Danh sách ca lỗi làm tròn bị loại giữ nguyên trong `circa_dev19_conditional.excluded_confirmed_rounding11`; không thay mẫu chính.','',
 '## Nezha view phụ','',table(['View','Phương pháp','Dấu ca','Ngoài cohort','Đổi status','Đổi Hit1','Đổi Hit5'],[[view,NAMES[method],len(rr),sum(r['cohort_state']=='not_in_cohort' for r in rr),sum(r.get('status_changed') is True for r in rr),sum(r.get('hit@1_changed') is True for r in rr),sum(r.get('hit@5_changed') is True for r in rr)] for (view,method),rr in sorted(fg.items())]),'']
 (ROOT/'results/T-028/bang-phu-co-dieu-kien.md').write_text('\n'.join(supplementary),encoding='utf-8')
 print('main map and full stratified/control tables rendered')


if __name__=='__main__':sys.stdout.reconfigure(encoding='utf-8');main()
