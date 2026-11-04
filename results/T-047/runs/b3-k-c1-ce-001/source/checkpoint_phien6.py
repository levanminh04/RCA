"""Checkpoint khi K tiếp tục chạy nền; không chốt ngân sách hoặc chấm nhãn."""
import hashlib
import json
import time
from datetime import datetime
from pathlib import Path

import psutil

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-047'


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''):
            h.update(b)
    return h.hexdigest()


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def main():
    audit = OUT / 'runs/phien6-checkpoint-001'
    audit.mkdir(exist_ok=False)
    stamp = datetime.now().astimezone().isoformat(timespec='seconds')
    budget = read(OUT / 'runs/ngan-sach.json')
    used = budget['prior_seconds'] + time.time() - budget['start_epoch']
    run = OUT / 'runs/b3-k-c1-that-001'
    monitor = (run / 'monitor.jsonl').read_bytes()
    monitor = monitor[:monitor.rfind(b'\n')+1]
    (audit / 'K-monitor-snapshot.jsonl').write_bytes(monitor)
    events = [json.loads(x) for x in monitor.splitlines() if x.strip()]
    forecasts = [x for x in events if x['event'] == 'forecast_after_completed_case']
    forecast = forecasts[-1] if forecasts else None
    phases = {}
    for name in ('seed0-001', 'seed1-001', 'seed2-001', 'xao0-002', 'ce-001'):
        p = OUT / ('runs/b2-c1-t1-' + name)
        m = read(p / 'pha1.json')
        assert sha(p / m['tep']) == m['sha256']
        phases[p.relative_to(ROOT).as_posix()] = m
    assert sum(x['so_ban_ghi'] for x in phases.values()) == 238
    t1 = read(OUT / 't1.json')
    assert t1['PASS'] and len(t1['doi_chieu_T046']) == 82
    complete = {}
    for p in sorted((run / 'cases').iterdir()):
        if (p / 'summary.json').is_file():
            m = read(p / 'phase1/pha1.json')
            assert m['so_ban_ghi'] == 16 and sha(p / 'phase1' / m['tep']) == m['sha256']
            complete[p.name] = m
    # Sửa riêng schema của bản soi QT5, không sửa bản 001 hoặc phương pháp.
    early = read(OUT / 'runs/c1-k-trung-gian-001/qt5-phan-xu.json')
    for oid, case in early['cases'].items():
        qs = {q['config_id']: q for q in read(run / 'cases' / oid / 'qt5.json')}
        for cid, row in case['configs'].items():
            row['raw_flag_channels'] = qs[cid]['kenh_co_theo_nhom']
            row['intrinsic_channels'] = None
            row['intrinsic_group_note'] = 'Không phân nhóm F_I trong lượt soi QT5 này; không suy UNKNOWN thành thiếu kênh.'
    early['schema_correction'] = 'Bản001 hỏi trường nhom không export trong kenh_co nên ra UNKNOWN. Bản002 lấy nhóm bằng đúng soi_ban_ghi đã tính QT5; không đổi đầu ra M1. Trạng thái đơn vị và số raw ở001 vẫn đúng.'
    corrected = OUT / 'runs/c1-k-trung-gian-001/qt5-phan-xu-002.json'
    corrected.write_text(json.dumps(early, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    processes = []
    for p in psutil.process_iter(['pid', 'cmdline']):
        try:
            cmd = p.info['cmdline'] or []
            if any('chay_k_c1.py' in x or 'chay_t047_v3.py' in x for x in cmd):
                processes.append(dict(pid=p.pid, cmd=cmd))
        except psutil.Error:
            pass
    checkpoint = dict(schema='T047-running-checkpoint-v1', time=stamp, task_complete=False,
        scoring_labels_read=False, controller_exec_session=80353, controller_command='scripts/chay_k_c1.py',
        active_processes=processes, budget=budget, used_seconds_at_checkpoint=used,
        latest_forecast=forecast, T1=phases, K_complete_cases=complete,
        early_check='results/T-047/runs/c1-k-trung-gian-001/kiem.json',
        next='Không khởi động trùng K. Đọc controller/monitor/result; khi đủ K thật/giả và hash LOG, đọc QT5 rồi pha2.',
        limits='Manifest checkpoint chỉ băm file tĩnh/ca hoàn tất; không chứng nhận đủ ma trận hoặc cơ chế. Live K tiếp tục sinh đầu ra.')
    (audit / 'checkpoint.json').write_text(json.dumps(checkpoint, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    files = {}
    for p in sorted(OUT.rglob('*')):
        if not p.is_file() or p.name in ('manifest.json', 'manifest-tiep-tuc-phien6.json'):
            continue
        rel = p.relative_to(OUT).as_posix()
        if rel == 'runs/c1-k-dieu-phoi-001/progress.jsonl':
            continue
        if rel.startswith('runs/b3-k-c1-'):
            if not rel.startswith('runs/b3-k-c1-that-001/'):
                continue
            tail = rel[len('runs/b3-k-c1-that-001/'):]
            keep = tail == 'command.json' or tail.startswith('source/')
            if tail.startswith('cases/'):
                parts = tail.split('/')
                keep = len(parts) >= 3 and parts[1] in complete and (parts[2] == 'phase1' or parts[2] in ('summary.json', 'qt5.json'))
            if not keep:
                continue
        files[p.relative_to(ROOT).as_posix()] = dict(bytes=p.stat().st_size, sha256=sha(p))
    manifest = dict(schema='T047-partial-static-manifest-v1', time=stamp, task_complete=False,
        scoring_labels_read=False, outputs=files, phase1_T1=phases, K_complete_cases=complete,
        source_correction='Q-233/C1', src_cong_sha256=sha(ROOT / 'src/m1/cong.py'),
        checkpoint='results/T-047/runs/phien6-checkpoint-001/checkpoint.json',
        mutable_exclusions=['live K monitor/logs/controller progress/unfinished cases; later-created files'],
        note='Dùng manifest này cho phần Phiên6 đã băm; manifest.json chính cũ không mô tả đầu ra mới. K tiếp tục tự động, không tính file live là lệch hash.')
    (OUT / 'manifest-tiep-tuc-phien6.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    p = ROOT / 'docs/STATE.md'
    lines = p.read_bytes().splitlines(keepends=True)
    idx = [i for i,x in enumerate(lines) if x.startswith(b'- **T-047 ')]
    assert len(idx) == 1
    i = idx[0];nl = b'\r\n' if lines[i].endswith(b'\r\n') else b'\n'
    line = '- **T-047 — chạy khối K lượt thứ hai:** **K pha1 đang chạy tự động; checkpoint để tiết kiệm usage** (02/11/2026, Phiên6). Codex làm, Claude phản biện. C1/Q-233 một commit, chưa push; T1 mới238lượt đạt,82đối chiếu T046 không lệch. K giữ16cấu hình,3worker+điều phối, dự báo và trần tổng8giờ; chưa đọc nhãn chấm/chọn khối. Không khởi động trùng. Tiếp nhận từ [LOG](../tasks/T-047-khoi-k-luot-2/LOG.md) và [checkpoint](../results/T-047/runs/phien6-checkpoint-001/checkpoint.json); hash phần tĩnh ở manifest-tiep-tuc-phien6.json. Chưa hoàn tất task.'
    lines[i] = line.encode()+nl;p.write_bytes(b''.join(lines))
    prompt = (OUT / 'prompt-claude-phien6.txt').read_text(encoding='utf-8')
    log = f'''\n## Kết thúc lượt tương tác Phiên6 để giữ usage — {stamp}

Minh hỏi hiện chỉ theo dõi hay cần tính toán và báo sắp hết usage. Máy đang tính K, không chỉ chờ. Codex chốt checkpoint và để controller đã duyệt tiếp tục; không dừng worker, không chốt ngân sách chờ Minh khi worker còn chạy. Không nghiệm thu task tại checkpoint này.

1. Đã làm: áp đúng C1, ghi Q233, một commit; hồi quy/pilot và chạy lại đủ T1; điều tra/sửa guard trong results; K tiếp tục tự động thật rồi C-e với kiểm/dự báo/hash. T1 đạt, native52/30 trước-sau C1 giống hệt,82đối chiếuT046 không lệch; D5 58/0. K hiện có {len(complete)} ca thật hoàn tất16cấu hình, các ca khác đang chạy; trạng thái sau mốc này lấy từ progress/result, không từ con số checkpoint. Kiểm sớm12ca R0/T1 và Kdu/T046 đạt,20cờQT5 đều tỷ trọngnhóm>90%, không có cờ vô hạn/đồng loạt/nguồnunsupported trong phần đãsoi. Đã đọc3ca cócờ và1ca cùngdataset khôngcờ ở4cấuhình: raw trace/log tồn tại, đơnvị đãchấm; nhiều đơnvịlog LOW_SUPPORT, bậtE3 làm thay tập log đượcchấm. Không suy tỷtrọng thành thiếu đầu vào hoặc bất thường thật. Chi tiết ở qt5-phan-xu-002.json; bản001 giữ lỗi trường chẩnđoán nhom không export, không phải lỗi phươngpháp.
2. File đổi: đúng2hàm src đãduyệt và dòngQ233 đãcommit; scripts/tests/runs, báo cáo tiếnđộ, prompt và manifest checkpoint trong results; nốiLOG, chỉdòngT047STATE. Giữ thayđổi cósẵn. Đã báo vi phạm5filepytestcache ngoài phạmvi; Minh duyệt dọn và5fileđãxóa sau sao lưu/hash, thưmụcrỗng còn do côngcụ chặn xóa ('blocked by policy'). Không lách côngcụ, không thêmcommit/push/cloud/lockeddata.
3. Kiểm: T044374/T04516/T04646; T047 hiện171testqua; giữlượt fixture11lỗi do thiếuparent basetemp. Guardrace47/768 trước,0/768 sau; cả47 cùng lệchprefixWindows sauresolve. Hai instance lỗiT1 lịch sử thiếu giátrị tại phépso nên chưa chứngminh hồi tố từnginstance. SourceC1 giữhash; các phaseT1 vàKca hoàn tất được kiểmhash trong checkpoint. Manifest tĩnh mới không băm file K live.
4. Phần còn lại: K chưađủ16×52 và16×30; chưaD2/chấm/chọn/1000bootstrap/độnhạy/bảng2×2/phânxửcơchế/báocáocuối. T1 chỉhỗtrợ kiểm càiđặt; không xácnhận hiệuchuẩnG3, giảthuyết kếthừa/tựsinh hoặc hiệuquảRCA/RQ3. GiữOPEN G3gầnhằng, phầncầntrướcG3 vàcác taskkếtiếp. Dựbáo tại checkpoint vẫnCHUA_KIEM, Kgiả chưa đo. Trần8giờ giữnguyên; nếucontrollerdừngvì dựbáovượt/error thì trìnhMinh, không tự giảmthiết kế hoặc nới thời gian.

Bước tiếp chính xác: đọc checkpoint.json, manifest-tiep-tuc-phien6.json; kiểm sourcehash vàcácfile tĩnh trước dùng lại. Xem runs/c1-k-dieu-phoi-001/result.json vàprogress; runs/b3-k-c1-that-001/result.json, monitor.jsonl và Kce tươngứng. Nếuprocess còn chạy, không chạytrùng. NếuK đủ và đốichiếu đạt, đọctấtcả QT5 cầnphânxử rồi Python ghim -B results/T-047/scripts/pha2_t047.py --that results/T-047/runs/b3-k-c1-that-001 --ce results/T-047/runs/b3-k-c1-ce-001 --run results/T-047/runs/b4-c1-pha2-001. Gate trongscript phải kiểm haihash KđãghiLOG trướcD2/nhãn/E_X. Sauđó theoSPEC dùng co_che_t047.py, do_ben_t047.py, so_sanh_t047.py; đọcchuỗi/counterpart thật, không coi FACTS_ONLY đãphânxử. Không chạy nếu dựbáovượt trần hoặc nguồn/tiêu chí cònlệch chưađược giải thích. Không chạy lại cácscript chốtPhiên5. Sau mọi kiểm/báocáocuối mới dùng kiem_phien6.py và chot_ngan_sach_phien6.py, không dùng chúng khi worker cònchạy.

Ngân sách: snapshot dùng {used/60:.2f}/480phút, sốnày tiếptục tăng trong lúcKchạy. Không đổi start/prior/cap hiện tại. Khi nối sau lúc controller đã dừng, dựng đúng mốc dừng từ progress/result và chỉ loại khoảng sau đó thực sự không chạy/chờ Minh; lưu vết tính, không trừ phần K đang chạy hoặc điều tra. Không xác định chắc khoảng chờ thì giữ OPEN/trình, không reset. Nếu K dừng do forecast thì cần trình điều kiện dừng trước chạy phụthuộc.

Lệnh cuối của lượt tương tác: Python ghim -B results/T-047/scripts/checkpoint_phien6.py; controller đang chạy riêng từ chay_k_c1.py, tool session80353. Môi trường: D:/RCA-ext/envs/py312-pin/Scripts/python.exe -B; PYTHONPATH gồm D:/RCA-ext/envs/T-016-cong-cu/Lib/site-packages; D:/RCA-flashticket/src; D:/RCA-flashticket/results/T-047/scripts. PYTHONDONTWRITEBYTECODE=1, PYTHONIOENCODING=utf-8, PYTHONHASHSEED=0. Tests sau dùng -p no:cacheprovider và basetemp trong results. Đề xuất commit kết quả T047 chỉ sau Minhduyệt riêng; mộtcommitC1/Q233 hiệnđãxong, pushchưađượcduyệt.

### Prompt Claude — Minh chuyển thủ công, chưa tự gửi

```text
{prompt.rstrip()}
```
'''
    with (ROOT / 'tasks/T-047-khoi-k-luot-2/LOG.md').open('a', encoding='utf-8') as f:
        f.write(log)
    print(json.dumps(dict(checkpoint=str(audit / 'checkpoint.json'), static_files=len(files),
        K_complete_cases=len(complete), T1_PASS=True, used_minutes=used/60,
        forecast_total_minutes=forecast['total_seconds']/60 if forecast else None,
        controller_continues=True, scoring_labels_read=False)))


if __name__ == '__main__':
    main()
