"""Tổng hợp hồ sơ T-053 từ kết quả đã đóng; không chạy lại phương pháp."""
import json
import math
import sys
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'src'))
from m1_danh_gia.pha2 import giai_ma_json, ma_hoa_json

BASE = ROOT / 'results/T-053'


def read(name):
    return giai_ma_json(json.loads((BASE / name).read_bytes()))


def write(name, value):
    with (BASE / name).open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(ma_hoa_json(value), stream, ensure_ascii=False, indent=2)


def num(x):
    return '—' if x is None else f'{float(x):.6f}'


def normalize(x, key=''):
    if isinstance(x, dict):
        return {k: normalize(v, k) for k, v in x.items()}
    if isinstance(x, list):
        values = [normalize(v) for v in x]
        return sorted(values, key=lambda v: json.dumps(v, sort_keys=True)) if key in ('channels', 'inherited') else values
    return x


def stage_times():
    rows = {}
    for path in sorted((BASE / 'runs').glob('*/progress.jsonl')):
        with path.open(encoding='utf8') as stream:
            first = json.loads(next(stream))
            if first.get('event') != 'start':
                continue
            rest = list(stream)
        last = json.loads(rest[-1])
        rows[path.parent.name] = dict(path=path.relative_to(ROOT).as_posix(),
            started_epoch=first.get('epoch'), finished_epoch=last.get('epoch'),
            elapsed_seconds=last.get('elapsed'), workers=first.get('workers'),
            windows=len(first.get('jobs', [])), event=last.get('event'),
            errors=last.get('errors'), pending=last.get('pending'))
    return rows


def main():
    metrics = read('runs/k-cham-001/chi-so.json')
    kq = read('runs/k-cham-001/kq.json')['cau_hinh']
    law = read('runs/k-cham-001/khoi-k.json')
    boot = read('runs/bootstrap-ec2-001/do-ben.json')
    mechanism = read('co-che.json')
    pairs = read('phan-tich-cap-003.json')
    regression = read('runs/phan-tich-cap-cli-hoi-quy-002.json')
    assert normalize(pairs) == normalize(regression)
    independent = read('runs/kiem-pha2-doc-lap-001.json')
    assert independent['PASS']
    full = {}
    changes = {}
    old = giai_ma_json(json.loads((ROOT / 'results/T-047/khoi-k/kq.json').read_bytes()))['cau_hinh']
    for cid, cfg in sorted(kq.items()):
        full[cid] = {'tong_hop': metrics[cid]['tong_hop'], 'theo_ca': {'ce': metrics[cid]['theo_ca']['ce'], 'that': {}}}
        changes[cid] = {}
        for oid, case in sorted(cfg['ca'].items()):
            values = {}
            for w, score in case['theo_the_gioi'].items():
                h1, h5 = score['do']['hit@1'], score['do']['hit@5']
                values[w] = dict(MRR=score['RR'], Hit1=h1, Hit3=score['do']['hit@3'], Hit5=h5,
                    NDCG5=score['do']['ndcg@5'], Retrieval5=h5,
                    Rerank1_K5=h1/h5 if h5 else None, M5=score['M5'],
                    **metrics[cid]['theo_ca']['that'][oid][w])
            full[cid]['theo_ca']['that'][oid] = dict(dataset=case['dataset'], o=case['o'], theo_the_gioi=values)
        for w in ('P', 'S_lo', 'S_hi'):
            by_dataset = {}
            for ds in ('gop', 'RE2-TT', 'Nezha-OB'):
                ids = [o for o,c in cfg['ca'].items() if ds == 'gop' or c['dataset'] == ds]
                delta = {o: cfg['ca'][o]['theo_the_gioi'][w]['RR']-old[cid]['ca'][o]['theo_the_gioi'][w]['RR'] for o in ids}
                before = sum((old[cid]['ca'][o]['theo_the_gioi'][w]['RR'] for o in ids), Fraction()) / len(ids)
                after = sum((cfg['ca'][o]['theo_the_gioi'][w]['RR'] for o in ids), Fraction()) / len(ids)
                by_dataset[ds] = dict(n=len(ids), MRR_E4=before, MRR_z=after, delta=after-before,
                    tot_hon=sum(v>0 for v in delta.values()), xau_hon=sum(v<0 for v in delta.values()),
                    bang=sum(v==0 for v in delta.values()))
            changes[cid][w] = by_dataset
    write('chi-so-day-du.json', full)
    runtime = {}
    for host in ('laptop','ec2'):
        rows = [json.loads(x) for x in (BASE / f'runs/k-{host}-001/progress.jsonl').read_text().splitlines()]
        assert rows[-1]['event'] == 'end' and not rows[-1]['errors'] and not rows[-1]['pending']
        runtime[host] = dict(seconds=rows[-1]['elapsed'], workers=rows[0]['workers'], windows=len(rows[0]['jobs']),
            started_epoch=rows[0]['epoch'], finished_epoch=rows[-1]['epoch'])
    combined = max(v['finished_epoch'] for v in runtime.values())-min(v['started_epoch'] for v in runtime.values())
    summary = dict(status='hoàn tất phần người làm, chờ phản biện và Minh quyết',
        generated_utc=datetime.now(timezone.utc).isoformat(),
        observation=dict(cases=52, fake_windows=30, cells=23, configurations=16, records=1312,
            arithmetic_exception_activations_dev=0, changes_fixed_config=changes,
            changed_pair_outcomes=len(mechanism['pair_changes']), compared_pairs=len(law['cap'])),
        selector=dict(main=law['chon_khoi'], buoc8=law['buoc8'], STOP=law['STOP'], defaults=law['mac_dinh_ap']),
        bootstrap={k:v for k,v in boot.items() if k != 'mau_goc'},
        runtime=dict(phase1_runs=stage_times(), K=runtime, K_wall_seconds=combined, T047_K_wall_seconds=5087.078+4165.016,
            bootstrap_ec2_seconds=boot['remote_seconds'], price_usd_per_hour=read('runs/preflight-001.json')['price']),
        checks=dict(independent=independent, paired_analysis_reproduced_semantically=True),
        decisions=dict(D24_current='E4+S1', D24_candidate='z+S1', K_dev_candidate='E1+E2+E5',
            T049='Minh quyết sau phản biện', G3_test='chưa mở'))
    write('tong-hop.json', summary)

    text = '''# T-053 — Kiểm z+S1 và chạy lại khối K

Codex làm; Claude phản biện chính thức. Hoàn tất phần thực hiện ngày 03/11/2026, chờ phản biện và Minh quyết. E4+S1 vẫn là D24 hiện hành. Các số dưới đây là số dev đã dùng nhiều lần để thiết kế.

## Kết quả cần quyết

**Quan sát:** đủ 16 cấu hình z+S1 trên 52 ca thật và 30 cửa sổ giả, tổng 1.312 bản ghi. T1 phần chịu ảnh hưởng đạt 238 bản ghi. Không lỗi native hay kích hoạt nhánh tính lại số học trên dev. Bản ứng viên cục bộ sửa được các trường hợp tràn trung gian đã kiểm; điểm hoặc tổng khóa cuối ngoài miền float64 vẫn giữ hành vi lỗi gốc.

**Kết cục theo luật đã khóa:** E1+E2+E5 được chọn ở P, S_lo và S_hi. Bước 8 trình E2 vì trái chiều theo dataset. Không có STOP của helper. Kết quả này chưa cho phép tự dùng làm nền T-049.

**Đề xuất Codex:** trình gói E1+E2+E5 như ứng viên dev nếu Minh chốt z+S1 và chấp nhận đánh đổi E2. Giữ nguyên kết cục của bộ chọn. Bootstrap mô tả độ bền, không dùng để đổi cấu hình thắng thành E2 đơn.

**Minh còn quyết:** chốt D24; cách xử lý E2 trái chiều; nền và quyền chạy T-049; các phép kiểm còn thiếu trước khóa thiết kế/G3. Task không nghiệm thu thay Minh, không mở test, không sửa mã dùng chung và không commit/push.

Nguồn số chính: [tổng hợp](tong-hop.json) `/observation`, `/selector`, `/bootstrap`; [bộ chọn](runs/k-cham-001/khoi-k.json) `/chon_khoi`, `/buoc8`, `/STOP`; [độ bền](runs/bootstrap-ec2-001/do-ben.json). Phân số gốc nằm trong JSON; bảng làm tròn sáu chữ số.

## Phạm vi và bảo toàn phép so

Chỉ dùng allowlist 30 RE2-TT và 22 Nezha-OB, 23 ô T0. Cửa sổ giả là 30 RE2 với mốc cũ trừ 300 giây. Giữ G3/D1, S1, ε=0,05, α=0,01, h=1. Ma trận là tích đầy đủ E1, E2-C, E3(a), E5; E3(b), E9, T12 tắt. `che_do.thang=E4+T4c` cùng cờ z biểu diễn z+S1 trong adapter, không có nghĩa đã đổi D24. [Ma trận](ma-tran.json), [kế hoạch pha 1](ke-hoach-pha1.json), [lịch](lich-chay.json).

Trước dùng lại đã đối chiếu manifest T-047 và T-048, revision và nguồn trực tiếp. Không tái dùng bản ghi T-048 để thay phần T1/K cần kiểm vì chưa đủ trung gian chứng minh loại trừ tràn và ghép đúng máy. T4/T4b giữ là bằng chứng cũ đã kiểm hash, không chạy lại. [Audit dùng lại](runs/doi-chieu-tai-dung-001.json). Mỗi cửa sổ giữ đủ 16 vế cùng máy; laptop 47 cửa sổ, EC2 35. Nhãn chỉ ghép sau seal pha 1 đã ghi trong LOG. [Seal](runs/k-dong-pha1-001/seal.json), [kiểm đủ](runs/k-dong-pha1-001/kiem.json), [lệnh chấm](runs/k-cham-001/command.json).

Phép đối chiếu toàn K kiểm 3.936 vế thế giới so bản ghi T-047. Cờ, hợp lệ, U, gán, đồ thị, F_I và tầng giữ nguyên; khóa, hòa và thứ hạng có thể đổi do đổi điểm. Có 3.870 vế đổi khối/hòa/hạng. Vì vậy có thể đọc thay đổi K này là ảnh hưởng của thang điểm trong giao thức hiện tại. Không suy bất biến ngoài tập đã kiểm. [Kiểm K](runs/kiem-k-day-du-001.json) `/counts`, `/differences`, `/changed_blocks`.

## Ngoại lệ số học và T1

Oracle Decimal độc lập kiểm median/type-7 IQR, sàn IQR, hai hướng z và tổng khóa. Bản cục bộ giữ nguyên đường native thông thường. Khi NumPy báo tràn, tính lại chính xác bằng Fraction rồi chuyển float nếu hai điểm cuối còn biểu diễn được. Sàn IQR giữ đúng điều kiện cũ, không tự tăng sàn hoặc cắt điểm. [Công cụ](scripts/z_on_dinh.py), [fixture](runs/kiem-z-002/kiem.json) `/checks`, `/chain`.

Phản ví dụ IQR tràn: IQR thực khoảng 2e308 không biểu diễn float64, nhưng z thực ±0,75 hữu hạn. Native dùng IQR=inf và cho z=0; ứng viên trả ±0,75. IQR/c trong chẩn đoán vẫn có thể là inf, với giá trị chính xác lưu trong dấu vết. Không diễn giải trường `huu_han` như cam kết mọi trung gian đều hữu hạn. Trường hợp phép trừ tràn nhưng phép chia trả z=±3 được khôi phục. Trường hợp một hướng thực sự vô hạn giữ chính sách loại cả đơn vị gốc, kể cả hướng còn lại hữu hạn. Hai kênh điểm 1e308 riêng lẻ hữu hạn có thể làm tổng khóa tràn và native ERROR; chưa có chính sách khóa mới. Những trường hợp sau cần Minh quyết nếu muốn đổi hành vi trước đưa vào mã dùng chung.

Đã kiểm biên sàn dưới/bằng/trên, mẫu thường, cờ 0 nhưng tính z lỗi vẫn làm mất hợp lệ, hai hướng và tổng khóa. Lượt fixture đầu lỗi schema S_mem của công cụ được giữ; lượt sửa đạt. Bản tính lại chưa kích hoạt trên dev, nên lợi ích xử lý cực trị chỉ được xác nhận trong fixture.

T1 chạy R0-z cho 52 ca × seed 0/1/2, 52 ca xáo và 30 giả, tổng 238. Hạng/hòa/khóa bất biến khi đổi seed hoặc xáo cùng máy; đối chiếu cờ/hợp lệ/gán với nguồn cũ đạt. Max lệch p liên máy nhỏ khoảng 5,55e-16 trong kiểm T1, không qua ngưỡng. Pilot đủ 36 bản ghi mỗi máy, max lệch p khoảng 9,44e-16, không đổi quyết định hay thứ hạng. Cache bật/tắt trùng đúng tám bản ghi kiểm riêng. [T1](runs/t1-kiem-001.json), [pilot](runs/doi-chieu-pilot-001.json), [cache](runs/doi-chieu-cache-001.json).

## Độ đo cùng thang z+S1

MRR là trung bình nghịch đảo thứ hạng, tính kỳ vọng khi hòa. Hit@k và NDCG@5 dùng cùng quy tắc hòa. Retrieval@5 là Hit@5 của danh sách được trả về; Rerank@1 trong K=5 là tổng Hit@1 chia tổng Retrieval@5. Đây là phép phân rã đánh giá, không chứng minh có bước rerank riêng trong phương pháp. M5 là ca có thực thể phía trên root trong G_N chắc chắn đứng trước root, không phải tỷ lệ trượt top 5. N1 là số thực thể tầng 1; V0 là verdict gốc.

Nguồn bảng: [độ đo](runs/k-cham-001/chi-so.json) `/<config>/tong_hop/that/{gop,dataset}/.../P`. [Đầy đủ](chi-so-day-du.json) có ca/ô/dataset/ba thế giới và N1/V0 thật/giả. [Bản chấm](runs/k-cham-001/kq.json) `/cau_hinh/<config>/ca/<id>/theo_the_gioi/<world>` giữ RR, thứ hạng, M5 và độ đo theo ca. Số gộp theo ca, không trung bình đều các ô. Các ô chỉ dùng đúng vai trò trong luật.

| Cấu hình | MRR gộp | RE2-TT | Nezha-OB | Hit@1 | Hit@3 | Hit@5 | NDCG@5 |
|---|---:|---:|---:|---:|---:|---:|---:|
'''
    order = ['R0','E1','E2','E3','E5','E1+E2','E1+E3','E1+E5','E2+E3','E2+E5','E3+E5','E1+E2+E3','E1+E2+E5','E1+E3+E5','E2+E3+E5','E1+E2+E3+E5']
    for c in order:
        t = metrics['K-'+c]['tong_hop']['that']
        g = t['gop']['gop']['P']
        row = [g['MRR'], t['dataset']['RE2-TT']['P']['MRR'], t['dataset']['Nezha-OB']['P']['MRR'], g['Hit1'],g['Hit3'],g['Hit5'],g['NDCG5']]
        text += '| '+c+' | '+' | '.join(map(num,row))+' |\n'
    text += '''
Gói thắng có MRR 1411/1560, Hit@1 43/52, Retrieval@5=1, Rerank@1=43/52 và M5=0 ở P. Gộp ba thế giới không được dùng như ba mẫu độc lập. V0 ở cửa sổ giả vẫn CAUSE_FOUND trên cả 30 cửa sổ của mọi cấu hình/thế giới. N1 hợp lệ không đồng nghĩa `verdict` đã phân biệt được lỗi. Không có nhãn bất thường thực thể ở C-e để hiệu chuẩn N1.

## Bộ chọn và các cặp chịu ảnh hưởng

Lượt loại đầu bỏ E1 và mọi cấu hình có E3, tổng chín cấu hình; lượt hai không loại thêm. Bảy cấu hình còn lại: R0, E2, E5, E1+E2, E1+E5, E2+E5, E1+E2+E5. E1+E2+E5 có MRR cao nhất trong tập còn lại. Bước 8 giữ E2 trong danh sách trình Minh; E1/E3/E5 nhất quán. Không thiếu cặp hay phụ thuộc thế giới ở lựa chọn chính. `can_Minh_truoc_task2=False` của helper chỉ nói cờ C-e chưa kiểm, không thay quyền Minh quyết tổng thể. `mac_dinh_ap` có mặc định bước 6 giữ gói thắng và gắn cờ; không dùng việc helper không ghi thêm mặc định bước 8 để xóa cờ trình E2.

δ=0,01, δ_d(RE2)=1/30, δ_d(Nezha)=1/22. Ngưỡng ô strict 0,05; P/M tính trong E_X, P′/M′ ngoài E_X. Vế C-e dùng trung bình chênh N1 ghép hợp lệ, HẠI khi tăng strict >h. Thứ tự HẠI riêng → trái chiều dataset → HẠI MRR → đủ ô → GIÚP → không tác dụng → trái chiều ô được giữ nguyên. K dùng `khoi_K`, không thay bằng bộ quyết định `luat_C` từng thành phần. Chi tiết đủ 43 cặp ở bảng sau, thế giới P. Các thế giới khác lưu nguyên trong JSON.

| Cặp tắt → bật | Kết cục | ΔMRR gộp | ΔRE2 | ΔNezha | P/M/P′/M′ | E_X | ΔN1 giả | C-e | UV6/E5 |
|---|---|---:|---:|---:|---|---:|---:|---|---|
'''
    for key,v in law['cap'].items():
        v=v['theo_the_gioi']['P']
        dm=v['dMRR'];ce=v['moc_gia']
        text += '| '+key.replace('|',' → ')+' | '+v['ket_cuc']+' | '+' | '.join(num(dm[x]) for x in ('gop','RE2-TT','Nezha-OB'))+' | '+ '/'.join(str(v[x]) for x in ('P','M','P_phay','M_phay'))+f" | {v['so_o_E_X']} | {num(ce['tang'])} | {ce['ve']} | {v['UV6']}/{v['dieu_kien_E5']} |\n"
    text += '''
E1+E5 → gói thắng khi thêm E2: RE2 giảm 7/180, Nezha tăng khoảng 0,152166. Hai chiều vượt δ_d nên kết cục TRAI_CHIEU_DATASET, dù gộp tăng. E1+E2 → gói thắng khi thêm E5: gộp tăng 29/1560, P=2/M=1 trong 20 ô E_X, điều kiện E5 không hại, N1 giả giảm 29/15; kết cục GIUP. Gói thắng → đủ E3: UV-6 HẠI, N1 giả tăng 88/15 và MRR giảm 1/60. Không coi đóng góp thành phần là cộng tuyến hay đồng nhất trên mọi nền.

## So với K dưới E4+S1

Nguồn [tổng hợp](tong-hop.json) `/observation/changes_fixed_config/<config>/<world>/<dataset>` và [cơ chế](co-che.json) `/pair_changes`, `/per_case`. Chỉ bảng sau so đổi thang trong cùng cấu hình. Bảng trước mới là phép so giữa cấu hình dưới cùng z.

| Cấu hình cố định | MRR E4 | MRR z | ΔMRR | Ca tốt hơn/xấu hơn/bằng |
|---|---:|---:|---:|---|
'''
    for c in order:
        v=changes['K-'+c]['P']['gop']
        text += f"| {c} | {num(v['MRR_E4'])} | {num(v['MRR_z'])} | {num(v['delta'])} | {v['tot_hon']}/{v['xau_hon']}/{v['bang']} |\n"
    text += '''
Bộ chọn cũ trả E1+E2, bộ chọn mới trả E1+E2+E5. Có 19/43 cặp đổi kết cục theo luật. Ví dụ R0→E1 từ GIUP thành HAI; R0→E1+E2 từ GIUP thành TRAI_CHIEU_DATASET; E2→E1+E2 từ GIUP thành KHONG_TAC_DUNG. Chênh lệch giữa hai gói thắng qua hai thang trộn cả thay thang và thay cấu hình, không dùng nó làm tác dụng riêng của E5.

## Độ nhạy và độ bền

Tính lại đủ bộ chọn với h=0,5 và 2 vẫn chọn E1+E2+E5 ở cả ba thế giới. Cờ E2 trình Minh vẫn giữ. Đây là kiểm hai dung sai thực dụng, chưa xác nhận h=1 đã hiệu chuẩn. [Độ nhạy](runs/k-cham-001/do-nhay.json) `/<h>/chon_khoi`, `/buoc8`, `/cap`.

Bootstrap lấy mẫu ô ghép, cùng trọng số cho mọi cấu hình/vế/thế giới, seed khai trước 20261102, đủ 1.000 mẫu. Bội số 1 tái lập bộ chọn chính. Mẫu số bảng luôn là 1.000, giữ cả 107 mẫu chọn R0 nhưng không đạt ràng buộc bước 8. Các tần suất không phải xác suất gói đúng.

| Kết cục mẫu bootstrap | Số/1.000 |
|---|---:|
'''
    for key, n in sorted(boot['tan_suat_thang'].items(), key=lambda x:-x[1]):
        text += f'| {key} | {n} |\n'
    text += f"| R0 không đạt bước 8 | {boot['loai']['buoc8_khong_E1_E2_E5']} |\n"
    text += '''
Có 893 mẫu đạt chọn. E1 bật ở 463, E2 ở 790, E3 ở 0, E5 ở 462 mẫu. Cờ trái chiều dataset xuất hiện ở 636 mẫu khi chọn và 549 mẫu ở cặp của gói thắng; xung đột bước 8 ở 20 mẫu. Không có cờ C-e chưa kiểm hoặc phụ thuộc thế giới ở gói thắng. Gói chính chỉ thắng 249 mẫu, nên không có bằng chứng lựa chọn ổn định duy nhất trên dev. Đây là lý do giới hạn độ chắc chắn khi trình nền T-049, không là luật chọn mới.

Bootstrap laptop dừng do D đầy lúc flush mẫu 448. Giữ nguyên lượt lỗi và đủ 448 dòng JSON đã ghi; progress chỉ xác nhận 447. Lượt EC2 hoàn tất đủ 1.000, 448 mẫu đầu trùng byte với laptop. [Độ bền chính](runs/bootstrap-ec2-001/do-ben.json), [kiểm tiền tố](runs/bootstrap-ec2-001/local-prefix-check.json). Bản co-che.json chỉ được đổi sang JSON gọn sau khi lưu nguyên bản lossless và kiểm JSON bằng nhau; không thay dữ kiện. [Audit](runs/co-che-format-001.json), [bản gốc](runs/co-che-format-original-001/transfer.json).

## Cơ chế tính toán đã lần theo

Nút là service, metric và kênh log E3 gắn tại service; trace cha–con cung cấp quan hệ. E3 bật thêm hướng giảm cho kênh thao tác và tỷ lệ thành công, bên cạnh việc thay log lỗi gộp bằng mẫu Drain. E1 dùng quan hệ span để trừ thời gian con khỏi span cha và tạo exclusive time. E2 dùng bằng chứng cạnh và gán điểm cạnh cho bên được gọi C. E5 dùng đồ thị có hướng N∪A và SCC để phân loại lan/không lan rồi tạo F_I. Điểm z không tham gia phép quyết định F_I của E5. S1 xếp trong tầng bằng khóa từ tín hiệu giữ lại, ưu tiên điểm lớn nhất. Vì vậy cùng cổng/gán/F_I mà thay độ lớn điểm có thể đổi tác hại của việc bỏ một kênh. R0 bỏ E1/E2/E3/E5 nên là ứng viên đối chứng không quan hệ của phép thử hiện tại; chưa chứng minh đủ mạnh so baseline P3 trên giao thức tương đương.

Bốn vế E4/z × tắt/bật được lưu ở [phân tích cặp](phan-tich-cap-003.json) `/pairs`, `/frames`. Mỗi frame chỉ nguồn native/trung gian và mẫu đầu vào. Đối chứng ca đúng ghép cùng dataset, loại lỗi, root được quan sát, có kênh/có F_I, nhóm kênh, lớp lan và M5 trên vế tắt. Không có ca thỏa chữ ký ghi null. Ghép này giúp kiểm giải thích nhưng không là can thiệp ngẫu nhiên; không loại trừ nhiễu vật lý giữa các ca.

1. **E5 đổi từ rất hại sang không hại ở một ca.** `dev-a5cabe5fa7`, root ts-travel-service, loss. Dưới E4, E1+E2→E1+E2+E5 làm RR 1→1/12. E5 bỏ kênh latency do đường lan qua SCC, điểm lớn nhất của root từ 0,95 xuống khoảng 0,436667. Dưới z, cùng quyết định bỏ đó, exclusive `find ts.trip` của root còn lại đạt 5256,929712, cao hơn ts-train-service khoảng 4506,080790; RR vẫn 1. Mẫu N của `find ts.trip` có median 1170,5 và IQR 156,5. Đổi kết quả đến từ thứ tự các điểm còn lại, không phải E5 đã đổi cờ hay chứng minh nhãn lan đúng vật lý. Không tìm được ca đúng trùng chữ ký cho ví dụ này.
2. **E5 vẫn hại ở ca loss khác.** `dev-20acb4402d`, root ts-order-service. Dưới z, bỏ latency-90 của root có z=4209,481569 làm điểm lớn nhất còn lại là exclusive `find ts.orders` z=1132,987919. Kênh exclusive `UserRepository.findByUsername` của ts-auth-service z=1774,479167 vượt root; RR 1→1/2. Cả hai vẫn ở tầng 1. N latency-90 có median khoảng 0,022985294 và IQR 0,000618132; N `find ts.orders` có median 1309, IQR 186,25, Amax 212328. Chuỗi số và bỏ kênh đủ giải thích lỗi xếp hạng tính toán. Chưa phân xử lý do vật lý khiến hai hoạt động lệch hoặc latency phản ánh triệu chứng/cause thế nào. Dưới E4 cùng cặp RR 1→1/6. Đây là ca duy nhất E5 làm RR xấu đi trong cặp nền thắng hiện tại. Thiếu ca đúng trùng chữ ký, nên không suy phổ quát từ ca này.
3. **E2 đánh đổi trong RE2.** `dev-a915aa2424`, root ts-travel-service. Từ E1+E5 sang gói thắng, exclusive `find ts.trip` của root giữ z=3881,562205. E2 thêm cạnh travel→train gán cho ts-train-service, z=4834,194981, làm RR root 1→1/3. N cạnh median 2059/IQR 518, Amax 2506172; N kênh root median 1041/IQR 158,75, Amax 617239. Tăng số kênh root 1→3 không bù được ưu tiên max. Đối chứng đúng `dev-a5cabe5fa7` cùng chữ ký giữ root 5256,929712 cao hơn train 4506,080790 nên vẫn RR=1. Có cơ chế xếp hạng cụ thể cho ca hại và điều kiện ca đúng; chưa suy cạnh gán C luôn đúng hoặc luôn sai.
4. **E1 có lợi phụ thuộc nền.** Tại `dev-a5cabe5fa7`, từ E2+E5 sang gói thắng RR 1/4→1. Exclusive `find ts.trip` z=5256,929712 được giữ không lan, thay max root khoảng 3441,656834 trước đó, vượt các đối thủ train/route. Không có đối chứng đúng trùng chữ ký. Tác dụng này không mâu thuẫn với E1 đơn bị loại trên nền R0.

Các ví dụ có đối chứng đúng được lưu, gồm RE2 E5 delay `dev-fbc45b0c67`↔`dev-4e68956051`, E5 frontend-return `dev-5ada15752d`↔`dev-1ac905bc95`, và E3 `dev-1ac905bc95`↔`dev-8ecd9880ed`. Các frame bốn vế chỉ rõ các khóa/kênh còn lại. Không cộng các cờ chồng lấn thành tỷ lệ nguyên nhân. Lợi ích/rủi ro E3 cũng chịu vế N1 và UV-6; không quy mọi ca hại cho một đặc tính log chung.

5. **E3 làm sai một ca Nezha đã đúng.** `dev-1ac905bc95`, frontend-return, gói thắng giữ log lỗi gộp F_I=1, điểm 1 và RR=1. Thêm E3 thay log gộp bằng các mẫu: `mau_moi` điểm 1 bị E5 gán F_I=0, mẫu thường giảm `mau:4` còn F_I=1 với điểm 0,589458. E3 đồng thời mở hướng giảm của exclusive `CartService/GetCart`, F_raw_xuong=1 với p khoảng 0,001 và z=2,421622. Cartservice và productcatalogservice vượt frontend, RR 1→1/3; dưới E4 cùng cặp RR 1→1/2. Mẫu thường frontend có n_N=723, n_A=709, nhưng thời lượng quan sát hai phía khác nhau và điểm xét theo rate, không chỉ so số dòng. Đối chứng checkout-return `dev-8ecd9880ed` giữ `mau_moi` F_I=1 cùng exclusive `PlaceOrder` điểm 2,272727 nên vẫn RR=1. Chuỗi này phân biệt việc thay tín hiệu log, mở hướng giảm và ưu tiên max; chưa phân xử mẫu giảm là hậu quả tải/đường thực thi hay cơ chế lỗi vật lý. Vế UV-6 ghi HẠI là kết cục luật, không đủ để quy mọi lỗi E3 cho Drain.
6. **Một tác hại E5 có thể bị điểm mới che.** Nezha frontend-return `dev-5ada15752d` có log lỗi gộp điểm 1 bị E5 gán F_I=0 nên root từ tầng 1 xuống 2. Dưới E4, shippingservice có điểm 0,8 nên RR 1→1/2 khi bật E5. Dưới z, shippingservice đã có điểm 3,983333 và đứng trước root ngay ở vế tắt, nên RR 1/2→1/2 dù E5 vẫn bỏ cùng tín hiệu. Đối chứng đúng cùng chữ ký `dev-1ac905bc95` không bị loại log gộp và giữ tầng 1/RR=1. Quan sát không còn chênh RR không chứng minh thao tác bỏ kênh đã đúng. Ngược lại ở RE2 train-delay `dev-fbc45b0c67`, E4 có RR 1/2→1 khi E5 bỏ triệu chứng đối thủ; z đã đưa root lên đầu bằng latency-90 18498,855871 trước E5, nên RR 1→1. Đối chứng `dev-4e68956051` cũng giữ RR=1 dưới z nhờ exclusive `TrainTypeRepository.findById` 13723,204545. Đây là ví dụ thay thang làm mất độ phân xử về tác dụng biên của E5, không xác nhận cơ chế lan vật lý.

## Mục tiêu nguồn, bằng chứng còn thiếu và tác động

DT18-NV2/NV3 và bước 2/4 của cô yêu cầu vai trò tính toán của đồ thị cùng đánh giá bằng độ đo phù hợp. T-053 bổ sung lựa chọn dev cho MRP P6/RQ3b, đã phân biệt đổi thang cố định với chọn lại thành phần. Các chuỗi trên xác nhận cơ chế tính toán của một số thay đổi thứ hạng. Chúng chưa xác nhận root cause vật lý hoặc lợi ích RCA trên dữ liệu độc lập.

| Phần còn mở | Bằng chứng cần và phạm vi | Quyết định chịu ảnh hưởng |
|---|---|---|
| Sàn c=1 và thang đo kênh | Phép tách latency-90/IQR, kiểm đổi đơn vị và ảnh hưởng điểm lớn trên cùng dev. Chưa thực hiện vì ma trận T-053 khóa; dự toán phải dựa lát cắt nếu Minh chọn mở gói. | Khái quát tính ổn định z và lý do chốt D24 ngoài dev hiện tại. |
| Tương tác cổng × điểm | Cùng cấu hình, thay riêng cổng và thang với tín hiệu/ô giữ chung. T-053 chỉ giữ G3/D1. Chi phí toàn ma trận tương tự thêm một K khoảng 1 giờ 40 theo lần đo này, chưa có pilot cho phương án mới. | Quy lợi ích cho z độc lập với cổng. Không chặn việc báo phép so đã làm dưới G3/D1. |
| Tác dụng riêng của quan hệ | T13/đối chứng bỏ quan hệ và quy tắc đơn giản trên cùng đồ thị, cùng tín hiệu/cửa sổ/coverage/ngân sách; vẫn cần Minh duyệt gói và ước lượng riêng. | RQ3d và khẳng định lợi ích do đồ thị. |
| Đối chứng không đồ thị đủ mạnh | R0+z cần đối chiếu baseline P3 mạnh trên giao thức tương đương, không dùng số công bố khác giao thức làm chứng minh. | QT7 và bộ đối chứng trước G3. |
| Hiệu quả độc lập, tự phát hiện, vùng ảnh hưởng, FlashTicket | P7 và các gói tương ứng sau khi Minh khóa thiết kế và mở dữ liệu. T-053 chỉ dùng mốc tiêm theo chế độ đã cấp. | RQ3 tổng thể, RQ3a/c, áp dụng sản phẩm. |
| Chính sách cực trị khi triển khai chung | Nếu chọn z, cần đề xuất riêng mã dùng chung và hợp đồng điểm/khóa thật sự ngoài miền, giữ lỗi, kiểm lại phần phụ thuộc trước chạy chính thức. Không đề nghị clipping hay giữ một hướng qua task này. | D24 triển khai chính thức và nền T-049. |

Không có bằng chứng ở đây để quy các hạn chế trên cho collector hoặc kết luận bổ sung trường sẽ sửa được RCA. Hạn chế chọn lặp trên dev và độ bền thấp phải đi cùng mọi lần sử dụng số. T-049/T13 chưa được chạy và quyền mở G3/test chưa được cấp.

## Hai máy, thời gian và các lượt lỗi

Đúng instance cũ đã kiểm IMDS và host key; không chép khóa. Tái dùng dev read-only sau kiểm byte/hash hai máy. EC2 2 vCPU, laptop i5-1240P RAM 16 GB. Thử laptop 2/3/4 tiến trình trên sáu cửa sổ mất 235,578/205,688/211,765 giây; chọn 3 vì tăng lên 4 giảm thông lượng. EC2 chọn 2 tiến trình. Ca nặng ưu tiên EC2. CPU, RSS cây tiến trình, RAM/đĩa và thông lượng nằm trong progress/host của từng lượt. [Preflight](runs/preflight-001.json), [lịch đo](lich-chay.json). Thời gian từng lượt pilot/T1/K, kể cả lỗi, ở [tổng hợp](tong-hop.json) `/runtime/phase1_runs`; không cộng các lượt đồng thời thành giờ chờ. Pha chấm chưa đo riêng thời gian từ đọc đầu vào tới độ nhạy, nên không dùng nó cho so ngân sách phương pháp.

'''
    text += f"K laptop {runtime['laptop']['seconds']:.3f} giây; EC2 {runtime['ec2']['seconds']:.3f} giây. Thời gian chờ đồng thời {combined:.3f} giây, khoảng {combined/3600:.3f} giờ. T-047 K thật+giả từng mất 9252,094 giây, khoảng 2,570 giờ. Hai máy đã rút thời gian chờ K; không nhanh gấp đôi vì EC2 chỉ 2 vCPU và T-047 vốn đã dùng 3 worker theo ca. Công việc hiện tại thêm capture/oracle, khác máy/thang điểm, nên tỷ số này không phải benchmark tốc độ phương pháp. Thời gian thử đủ 16 cấu hình không phải ngân sách chạy một cấu hình theo Q-40.\n\n"
    text += '''Pilot đầu EC2 lỗi thiếu networkx trong môi trường T-031; lượt sau dùng môi trường T-025 ghim và kiểm đủ. Hai lần SSH chờ sau khi remote đã xong được giữ trong log; giữ liên lạc mỗi 30 giây và resume sau kiểm hash đã giúp tự chuyển đủ các stage tiếp. Không chạy trùng cửa sổ đã đóng. Lỗi bootstrap do đầy D và các bản chẩn đoán trước sửa được giữ. Bản phân tích cặp 001/002 có lỗi phạm vi biến ghép đối chứng/phạm vi chọn ví dụ, không dùng làm kết luận; bản 003 và CLI đã tái lập cùng dữ liệu sau chuẩn hóa thứ tự danh sách chẩn đoán. Không ảnh hưởng score hoặc selector. [Lịch sử lossless](runs/phan-tich-cap-history-001/manifest.json).

Trần đã duyệt 8 giờ đợt máy và 8 giờ EC2. Đợt bắt đầu khoảng 14:35, hoàn tất lượt phương pháp 17:58, bootstrap EC2 thêm 232,161 giây; thời điểm đóng hồ sơ và kiểm task nằm trong [kiểm cuối](runs/kiem-cuoi-001.json). Giá tham chiếu máy công khai 0,1197 USD/giờ, trần 8 giờ khoảng 0,96 USD; lưu trữ/IP và hóa đơn tài khoản riêng. Instance đã chạy trước task, không tự dừng máy. Không dùng dự toán hoặc giờ tồn tại của instance như hóa đơn T-053.

## Tái lập và bàn giao

Môi trường laptop Python 3.12 ghim tại `D:/RCA-ext/envs/py312-pin/Scripts/python.exe`, PYTHONPATH thêm `D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages`, PYTHONHASHSEED=0, OPENBLAS_NUM_THREADS=1, OMP_NUM_THREADS=1. EC2 dùng `/home/ubuntu/rca/T-025/envs/main/bin/python`. Nguồn/hash và argv thực nằm trong command từng lượt và manifest. Không chạy lại vào đường dẫn đã tồn tại.

- Phần phương pháp: `scripts/chay_chinh.py` theo lệnh/PID 003 và lịch trong LOG. Không cần chạy lại khi đầu ra đã khép và đúng hash.
- Chấm: `scripts/cham_k.py --seal runs/k-dong-pha1-001/seal.json --out <thư mục T-053 mới>`, với đường dẫn đầy đủ tính từ repo. Lượt đã chấm chính ở k-cham-001; bootstrap hợp lệ ở bootstrap-ec2-001.
- Kiểm pha 2: `scripts/kiem_pha2.py` dùng đầu vào đã đóng và oracle tie độc lập. Kết quả đã có, dùng đường dẫn đầu ra mới nếu cần chạy lại.
- Phân tích bốn vế: `scripts/phan_tich_cap.py --out <tệp mới trong results/T-053>`.
- Tổng hợp hiện tại: `scripts/ket_qua.py`; giữ các đầu ra và chọn tên mới nếu tái lập.

[Manifest](manifest.json) đóng toàn bộ tệp kết quả. [Prompt Claude](prompt-claude.md) chép mẫu chung/công đoạn/G3, Minh chuyển thủ công. LOG giữ tự rà, quyền chạy, dự toán, seal trước nhãn, lỗi và lệnh tiếp nhận. STATE chỉ chuyển T-053 sang chờ phản biện. Đề xuất commit sau khi Minh duyệt: `research(T-053): kiểm z+S1 và chạy lại K trên dev`.
'''
    (BASE / 'bao-cao.md').write_text(text, encoding='utf-8', newline='\n')
    print('REPORT',len(text),'chars;',len(full),'configs;',len(law['cap']),'pairs')


if __name__ == '__main__':
    main()
