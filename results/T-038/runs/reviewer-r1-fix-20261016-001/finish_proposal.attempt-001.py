"""Summarize validated candidate artifacts within the reviewer's write boundary."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

import prepare_repair as repair

HERE, ROOT, BASE = repair.HERE, repair.ROOT, repair.BASE


def handoff():
    source = (ROOT / 'docs/review-prompt.md').read_text(encoding='utf-8-sig')
    def block(title):
        return re.search(r'```text\n([\s\S]*?)\n```', source[source.index(title):]).group(1)
    common = block('## Prompt chung')
    values = [
        ('mã và đường dẫn; nếu đề xuất đang trong chat, dán nguyên văn', 'T-038; tasks/T-038-p5b-trainticket/; results/T-038/; results/T-038/runs/reviewer-r1-fix-20261016-001/'),
        ('soát SPEC / soát kết quả / người làm đáp phản biện / kiểm lại phản hồi và sửa', 'người làm đáp phản biện'),
        ('gói, cổng hiện tại; ngoài task thì ghi loại đề xuất', 'P5, chuẩn bị G3'),
        ('tên theo SPEC; ngoài task thì ghi vai trò dự kiến', 'Codex phiên triển khai là người làm; Codex phiên độc lập được Minh chỉ định là người phản biện kết quả. Giữ vai trò chính thức'),
        ('danh sách đường dẫn và git diff từ commit gốc nếu có', 'AGENTS.md; docs/STATE.md; SPEC.md và LOG.md T-038; docs/MRP.md, WHY.md, DECISIONS.md, LESSONS.md; docs/reference/sources/DT18-de-tai-va-nhiem-vu.md; docs/reference/sources/advisor-2026-09-23.md; registry nguồn của task và nguồn được dẫn'),
        ('đường dẫn theo thứ tự thời gian; không có thì ghi không có', 'tasks/T-038-p5b-trainticket/REVIEW.md; báo cáo trong chat ngày 16/10/2026 do Minh chuyển; các tài liệu trước theo LOG và thư mục task'),
        ('đường dẫn, revision, manifest, hướng dẫn môi trường/lệnh chạy; không áp dụng thì ghi không áp dụng', 'src/do_thi/; src/do_thi_tinh/; results/T-035/manifest.json; results/T-036/runs/doi-chieu-smtp-001/manifest.json; results/T-038/manifest.json; results/T-038/runs/reviewer-r1-fix-20261016-001/manifest.json, oracle.json, apply-plan.json, checks/ và candidate/; Windows Python 3.12, -X utf8 -B'),
        ('chỉ trả lời trong chat, hoặc file và phần được phép ghi chính xác', 'chỉ đọc và trả lời trong chat. Chưa cấp quyền tiếp nhận hoặc sửa file qua prompt này. Không tải, mở dữ liệu khóa/telemetry thô, chạy thực nghiệm mới, dùng subagent hoặc tự mở/gửi chat. Được kiểm hash và tính lại độc lập trong bộ nhớ từ dữ liệu được phép đọc')]
    for old, new in values:
        common = common.replace('<' + old + '>', new)
    assert not re.search(r'<[^>]+>', common)
    return common + '\n\n' + block('### Người làm đáp phản biện') + '\n\n' + block('### G3 — Khóa thiết kế trước khi mở test') + '\n'


def main():
    summary = repair.load(HERE / 'candidate/summary.json')
    assert summary['all_pass'] and summary['graph_count'] == 1069
    comparison = repair.load(HERE / 'checks/comparison.json')
    assert comparison['all_pass']
    document = repair.load(HERE / 'candidate/ban-ghi.json')
    graphs = {level: repair.load(HERE / 'candidate/do-thi' / name) for level, name in [('entity', 'thuc-the.json'), ('operation', 'thao-tac.json')]}
    previous = repair.load(HERE / 'before/phan-tich-chenh-lech.json')
    grouped, union = defaultdict(list), defaultdict(set)
    full, chains, excluded = [], [], {}
    selected = {('ts-admin-basic-info-service', 'ts-config-service'), ('ts-food-service', 'ts-station-service'),
                ('ts-seat-service', 'ts-travel-service'), ('ts-seat-service', 'ts-travel2-service'),
                ('ts-travel-service', 'ts-order-service'), ('ts-travel2-service', 'ts-order-other-service')}
    selected |= {(r['source']['entity'], r['target']['entity']) for r in repair.load(HERE / 'delta.json')}
    for row in summary['rows']:
        family = Path(row['input']).stem.split('-')[0]
        for name, counts in row['views'].items():
            grouped[(row['level'], family, name)].append(counts)
        if family != 'full':
            continue
        assert repair.sha(ROOT / row['output']) == row['output_sha256']
        result = repair.read_compressed(ROOT / row['output'])
        full.append({key: row[key] for key in ['input', 'output', 'level', 'views']})
        for name, view in result['views'].items():
            for category in ['S', 'T', 'intersection', 'static_only', 'trace_only']:
                union[(row['level'], name, category)].update(repair.canonical(k) for k in view[category])
            for side, rows in view['exclusions'].items():
                for item in rows:
                    excluded.setdefault((row['level'], name, side, item['reason']), dict(output=row['output'], exclusion=item))
        if row['level'] == 'entity':
            view = result['views']['endpoints']
            for key in view['S'] + view['trace_only']:
                if (key[0], key[1]) not in selected:
                    continue
                category = 'intersection' if key in view['intersection'] else 'static_only' if key in view['static_only'] else 'trace_only'
                chains.append(dict(input=row['input'], output=row['output'], key=key, category=category,
                    static_members=[g for g in view['members']['static'] if g['key'] == key],
                    trace_members=[g for g in view['members']['trace'] if g['key'] == key]))
    stats = []
    for (level, family, name), rows in sorted(grouped.items()):
        values = {}
        for key in ['S', 'T', 'intersection', 'static_only', 'trace_only', 'static_fraction', 'trace_fraction']:
            distinct = sorted({r[key] for r in rows if r[key] is not None})
            values[key] = dict(min=min(distinct) if distinct else None, max=max(distinct) if distinct else None,
                null_count=sum(r[key] is None for r in rows), distinct=distinct)
        stats.append(dict(level=level, family=family, view=name, graph_count=len(rows), values=values))
    analysis = dict(previous)
    analysis.update(status='REVIEWER_REPAIR_PROPOSAL_NOT_ADOPTED',
        comparison_run=HERE.relative_to(ROOT).as_posix() + '/candidate',
        numerical_source=(HERE / 'candidate/summary.json').relative_to(ROOT).as_posix(),
        family_stats=stats, full_graphs=full,
        full_union=[dict(level=k[0], view=k[1], category=k[2], keys=[json.loads(x) for x in sorted(v)]) for k, v in sorted(union.items())],
        exclusions=[dict(level=k[0], view=k[1], side=k[2], reason=k[3], **v) for k, v in sorted(excluded.items())],
        chain_examples=chains,
        source_counts=dict(entities=len(document['entities']), operations=len(document['operations']), relations=len(document['relations']),
            bindings=len(document['resource_bindings']), signals=len(document['signals']),
            entity_types=dict(Counter(r['type'] for r in document['entities'])), signal_kinds=dict(Counter(r['kind'] for r in document['signals'])),
            entity_graph_edges=len(graphs['entity']['edges']), operation_graph_edges=len(graphs['operation']['edges'])),
        R1_infrastructure_delta=(HERE / 'delta.json').relative_to(ROOT).as_posix(),
        R1_source_audit=(HERE / 'source-audit.json').relative_to(ROOT).as_posix(),
        historical_analysis=(HERE / 'before/phan-tich-chenh-lech.json').relative_to(ROOT).as_posix(),
        numerical_comparison_unchanged=False, task_accepted=False, producer_outputs_modified=False)
    repair.save('candidate/phan-tich-chenh-lech.json', analysis)
    repair.save('candidate/doi-chieu/index.json', dict(status='REVIEWER_PROPOSAL_NOT_ADOPTED',
        current_run=HERE.relative_to(ROOT).as_posix() + '/candidate',
        summary=(HERE / 'candidate/summary.json').relative_to(ROOT).as_posix(),
        graph_count=1069, outputs=[r['output'] for r in summary['rows']]))
    table = ['| Mức/miền/view | Graph | S | T | Giao | Riêng tĩnh | Riêng trace |', '|---|---:|---:|---:|---:|---:|---:|']
    def interval(value):
        return str(value['min']) if value['min'] == value['max'] else str(value['min']) + '–' + str(value['max'])
    for row in stats:
        table.append('| ' + '/'.join([row['level'], row['family'], row['view']]) + ' | ' + str(row['graph_count']) + ' | ' + ' | '.join(interval(row['values'][k]) for k in ['S', 'T', 'intersection', 'static_only', 'trace_only']) + ' |')
    body = '''# Bản đề nghị sửa R1 — chưa tiếp nhận vào kết quả hiện hành

Bản này được tạo bởi người phản biện sau lời Minh “DUYỆT SỬA TRONG PHIÊN NÀY”. Đây là gói sửa cụ thể đã kiểm; không là quyền đổi vai hoặc ghi đè đầu ra của người làm. Các root output, LOG/STATE/SPEC và shared code vẫn giữ nguyên.

Nguồn tĩnh bổ sung ba dependency dữ liệu: Skywalking → Elasticsearch, Alertsnitch → MySQL và Nacos → MySQL. Webhook HTTP Alertmanager → Alertsnitch giữ kiểu gọi chưa phân loại; cấu hình HTTP không xác nhận synchronous execution hoặc delivery. Mọi quan hệ có điều kiện profile và locator tới nguồn đã kiểm Git blob/SHA; không chép credential vào bản ghi.

Mô hình đề nghị có 110 entity, 993 operation, 513 relation, 50 binding và 139 signal. Có 170 cạnh entity, 343 cạnh operation; phép chiếu có 122 cạnh và phần entity-only có 48 cạnh. Nguồn số: checks/model.json và candidate/phan-tich-chenh-lech.json#/source_counts.

Kiểm đủ 1.069 graph: ở 979 graph entity, endpoints thêm 4 S/static-only, typed thêm 3 S/static-only và 1 unknown exclusion. Toàn phía trace và giao giữ nguyên. 90 kết quả operation bằng nguyên bản trước. Có kiểm độc lập từng khóa/members/phân hoạch loại trừ/mẫu số, input, lặp và đảo thứ tự. Không phải thực nghiệm RCA mới. Nguồn số: checks/comparison.json và candidate/summary.json#/rows.

''' + '\n'.join(table) + '''

Đây là min–max từng graph trong từng miền, không là số nguyên nhân hay độ phủ instrumentation. Mẫu số trace rỗng vẫn null; không đổi thành 0% coverage. Năm cặp riêng trace và các chuỗi source/mapping chưa có bằng chứng runtime giữ giới hạn cũ.

source-audit.json giữ riêng các địa chỉ UI→OAP, Prometheus alert/scrape và client discovery còn cần semantics/binding hoặc biểu diễn unknown protocol. Không ép chúng vào channel HTTP/RPC/internal để đóng mô hình. Grafana Deployment đã xem không cung cấp datasource address; vai trò visualization không tạo cạnh. Các phần này chưa cho semantic/runtime completeness; owner và bằng chứng cần nằm ngay từng mục.

R1 là lỗi trích/bản ghi nguồn: assembler cũ liệt kê các thành phần nhưng không đưa các dependency cấu hình này vào relations. Không quy lỗi cho dataset/collector. Bản sửa đề nghị chỉ phục hồi thông tin có nguồn, chưa xác minh lineage, lợi ích RCA, thiết kế P6, RQ3/RQ5/G3 hoặc quyền mở test.
'''
    repair.text('candidate/phan-tich-chenh-lech.md', body)
    handoff_text = handoff()
    repair.text('handoff.txt', handoff_text)
    repair.text('candidate/prompt-claude.txt', handoff_text)
    repair.text('candidate/kiem-dung-dan.md', '# Bản kiểm đề nghị sửa R1 — chưa tiếp nhận\n\n' +
        'checks/source-verification.json: 8/8 điều kiện chuỗi cấu hình đạt; nguồn kiểm byte/Git blob/SHA trước dùng. ' +
        'checks/model.json: literal delta, prefix bản ghi cũ, entity-only/phép chiếu, inventory/tín hiệu và đảo thứ tự đạt. ' +
        'checks/comparison.json: đủ1069 graph, oracle tập/members/phân hoạch/mẫu số/input/lặp/đảo đạt;90 operation bằng nguyên bản trước. ' +
        'Oracle literal được ghi trước prepare_repair.py. Không chạy lại app, baseline, mở raw/test/heldout hoặc đổi shared code. ' +
        'Trạng thái là candidate của người phản biện; root output và pin hiện hành chưa thay.\n')
    repair.text('candidate/ban-giao.md', '# Bàn giao bản đề nghị sửa R1 — chưa tiếp nhận\n\n' +
        'Bốn bản ghi và nguồn ở delta.json/oracle.json, số ở checks/model.json và checks/comparison.json. ' +
        'Đầu ra đầy đủ trong candidate/. Manifest riêng bảo vệ gói. Người làm cần tự soát và trình/thi hành phạm vi tiếp nhận được Minh duyệt; ' +
        'không chạy script cũ để ghi đè lịch sử hoặc coi candidate này là bản hiện hành. ' +
        'Mapping, graph trace và shared pin giữ nguyên; các địa chỉ chưa phân xử ở source-audit.json. ' +
        'Chưa nghiệm thu task/P6/G3/test/commit.\n')
    replacements = []
    for candidate in ['ban-ghi.json', 'nguon.json', 'do-thi/thuc-the.json', 'do-thi/thao-tac.json',
                      'do-thi/chieu-thao-tac.json', 'do-thi/chi-thuc-the.json',
                      'phan-tich-chenh-lech.json', 'phan-tich-chenh-lech.md',
                      'kiem-dung-dan.md', 'ban-giao.md', 'doi-chieu/index.json', 'prompt-claude.txt']:
        original = BASE / candidate
        proposed = HERE / 'candidate' / candidate
        replacements.append(dict(producer_path=original.relative_to(ROOT).as_posix(),
            expected_current_sha256=repair.sha(original) if original.is_file() else None,
            proposed_artifact=proposed.relative_to(ROOT).as_posix(), proposed_sha256=repair.sha(proposed)))
    repair.save('apply-plan.json', dict(task='T-038', status='REVIEWER_PROPOSAL_NOT_ADOPTED',
        automatic_apply_implemented=False, official_role='reviewer', role_change_authorized=False,
        exact_proposed_root_replacements=replacements,
        additional_producer_work_before_adoption=[
            'Preserve exact before-state and create a producer-authorized run for adoption and reproducibility.',
            'Regenerate the producer manifest and current_run/current_model selectors after validating copied outputs and final file scope.',
            'Record authorization, response/repair and handoff in the producer LOG and only the T-038 STATE row within separately granted role/write scope.',
            'Resolve or explicitly retain the source-address limitations in source-audit.json without promoting them to runtime facts.'
        ],
        prohibited_in_this_reviewer_run=['publish current producer artifacts', 'write LOG/STATE/SPEC/decisions/shared code',
            'change role', 'open locked data', 'run RCA experiments', 'commit/push'],
        unaffected=['all source files', 'T-035 graph inputs', 'mapping', 'T-036 common pin', 'other branches'],
        numerical_evidence='checks/comparison.json', source_evidence='checks/source-verification.json'))
    repair.text('README.md', '# Gói sửa R1 của người phản biện\n\n' +
        'Đã materialize và kiểm bản sửa đề nghị. **Chưa áp dụng vào kết quả hiện hành.** ' +
        'Người phản biện giữ vai trò và giới hạn ghi; không thay LOG/STATE/SPEC hoặc file người làm.\n\n' +
        'Đọc apply-plan.json, oracle.json, delta.json, source-audit.json, checks/model.json, checks/comparison.json, ' +
        'candidate/phan-tich-chenh-lech.md và handoff.txt. Hash trong manifest.json. ' +
        'before/ giữ các đầu ra gốc được đối chiếu; protected-before.json bảo vệ mọi artifact cũ. ' +
        'Không có script tự tiếp nhận. Người làm hoặc phiên triển khai có quyền phải tiếp nhận qua phạm vi Minh duyệt.\n\n' +
        'Lệnh đã chạy: py -3 -u -X utf8 -B results/T-038/runs/reviewer-r1-fix-20261016-001/prepare_repair.py prepare; ' +
        'cùng script với compare; finish_proposal.py. Dùng run mới nếu cần tái lập, không ghi đè lượt này.\n')
    # Keep all producer-owned old bytes, including current manifests and LOG/STATE, intact.
    protected = repair.load(HERE / 'protected-before.json')
    repair.verify_protected(protected)
    ast.parse((HERE / 'prepare_repair.py').read_text(encoding='utf-8'))
    ast.parse(Path(__file__).read_text(encoding='utf-8'))
    for path in HERE.rglob('*.json'):
        repair.load(path)
    repair.save('checks/final-verification.json', dict(all_pass=True,
        status='VALIDATED_REPAIR_PROPOSAL_NOT_PRODUCER_ADOPTION',
        protected_preexisting_files_unchanged=len(protected),
        producer_models_graphs_mappings_manifests_reports_LOG_STATE_SPEC_unchanged=True,
        candidate_models_and_1069_comparisons_pass=True, json_and_python_parse_pass=True,
        reviewer_role_retained=True, no_commit_or_push_or_other_thread_action=True,
        semantic_inventory_and_runtime_and_RCA_benefit_remain_open=True))
    files = []
    for path in sorted(HERE.rglob('*')):
        if path.is_file() and path != HERE / 'manifest.json':
            files.append(dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size, sha256=repair.sha(path)))
    repair.save('manifest.json', dict(task='T-038', client_date='2026-10-16',
        created_utc=datetime.now(timezone.utc).isoformat(), status='VALIDATED_REVIEWER_REPAIR_PROPOSAL_NOT_ADOPTED',
        official_role='reviewer', producer_outputs_modified=False,
        baseline_manifest_sha256=repair.sha(HERE / 'before/manifest.json'), pin=repair.load(HERE / 'pin.json'),
        files=files, file_count=len(files), total_payload_bytes_excluding_manifest=sum(f['bytes'] for f in files),
        no_test_heldout_raw_or_download=True, no_task_acceptance_or_role_change_or_commit_push=True))
    print(repair.canonical(dict(status='PROPOSAL_COMPLETE_NOT_ADOPTED', files=len(files), graphs=1069,
        bytes=sum(f['bytes'] for f in files), protected_unchanged=len(protected))), flush=True)


if __name__ == '__main__':
    main()
