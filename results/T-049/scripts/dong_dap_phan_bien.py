"""Đóng bản sửa tài liệu sau phản biện, giữ manifest trước sửa."""
import ast
import difflib
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from dong_ho_so import (LOG, MANIFEST, OUT, ROOT, check_final, info, inventory,
                       prompt_check, read, verify)


def main():
    previous_path = OUT / 'runs/dap-phan-bien-001/ban-truoc/manifest.json'
    previous = read(previous_path)
    assert info(MANIFEST) == info(previous_path), 'Manifest already revised; only read-only checks may follow'
    assert read(OUT / 'runs/dap-phan-bien-001/doi-chieu.json')['PASS'] is True
    changed = {
        'results/T-049/bao-cao.md': 'results/T-049/runs/dap-phan-bien-001/ban-truoc/bao-cao.md',
        'results/T-049/nen-de-nghi-T050.json': 'results/T-049/runs/dap-phan-bien-001/ban-truoc/nen-de-nghi-T050.json',
        'results/T-049/scripts/dong_ho_so.py': 'results/T-049/runs/dap-phan-bien-001/ban-truoc/dong_ho_so.py',
    }
    for name, expected in previous['outputs'].items():
        verify(name, expected, changed.get(name))
    for table in ('current_sources', 'upstream_manifests'):
        for name, expected in previous[table].items():
            actual = ('results/T-049/runs/dap-phan-bien-001/ban-truoc/STATE.md'
                      if name == 'docs/STATE.md' else None)
            verify(name, expected, actual)
    for name, expected in previous['mutable_log_prefixes'].items():
        verify(name, expected, prefix=True)
    for name, expected in read(OUT / 'ma-tran.json')['sources'].items():
        verify(name, expected)
    old_state = (OUT / 'runs/dap-phan-bien-001/ban-truoc/STATE.md').read_text(encoding='utf-8-sig').splitlines()
    new_state = (ROOT / 'docs/STATE.md').read_text(encoding='utf-8-sig').splitlines()
    delta = list(difflib.ndiff(old_state, new_state))
    removed = [v[2:] for v in delta if v.startswith('- ')]
    added = [v[2:] for v in delta if v.startswith('+ ')]
    assert len(removed) == len(added) == 1
    assert all(v.startswith('- **T-049') for v in removed + added)
    report = (OUT / 'bao-cao.md').read_text(encoding='utf-8-sig')
    old_report = (OUT / 'runs/dap-phan-bien-001/ban-truoc/bao-cao.md').read_text(encoding='utf-8-sig')
    assert [v for v in report.splitlines() if v.startswith('|')] == [
        v for v in old_report.splitlines() if v.startswith('|')], 'Original numerical tables changed'
    links = re.findall(r'\]\(([^)]+)\)', report)
    for target in links:
        if '://' not in target:
            assert (OUT / target.split('#')[0]).resolve().is_file(), target
    old_baseline = read(OUT / 'runs/dap-phan-bien-001/ban-truoc/nen-de-nghi-T050.json')
    new_baseline = read(OUT / 'nen-de-nghi-T050.json')
    assert all(new_baseline[k] == v for k, v in old_baseline.items()), 'Baseline decision/configuration changed'
    syntax_files = list((OUT / 'scripts').glob('*.py')) + list((OUT / 'tests').glob('*.py'))
    for path in syntax_files:
        ast.parse(path.read_text(encoding='utf-8-sig'), filename=str(path))
    stage = 'Kiểm lại phản hồi và sửa'
    assert prompt_check(stage) == 8
    receipt = {
        'PASS': True, 'previous_outputs_preserved_or_unchanged': len(previous['outputs']),
        'changed_existing_outputs': changed, 'STATE_changed_lines': 1,
        'phase1_source_hashes_unchanged': 53, 'previous_current_sources_unchanged_except_STATE': True,
        'upstream_manifests_unchanged': 5, 'previous_LOG_prefix_unchanged': True,
        'original_numeric_tables_unchanged': True, 'baseline_configuration_and_status_unchanged': True,
        'report_links': len(links), 'syntax_files': len(syntax_files), 'neutral_prompt_fields': 8,
        'new_method_runs': 0, 'method_code_changes_this_response': 0,
    }
    target = OUT / 'runs/dap-phan-bien-001/kiem-ho-so.json'
    with target.open('x', encoding='utf-8') as f:
        json.dump(receipt, f, ensure_ascii=False, indent=2)
        f.write('\n')
    revised = dict(previous)
    revised['created_at'] = datetime.now(ZoneInfo('Asia/Ho_Chi_Minh')).isoformat()
    revised['status'] = 'DA_DAP_SUA_CHO_MINH_NGHIEM_THU_CHOT_NEN'
    revised['handoff_stage'] = stage
    revised['previous_manifest'] = {'path': previous_path.relative_to(ROOT).as_posix(), **info(previous_path)}
    revised['review_status'] = {
        'review_source': 'results/T-049/runs/dap-phan-bien-001/claude-soat-ket-qua.txt',
        'response': LOG, 'evidence': 'results/T-049/runs/dap-phan-bien-001/doi-chieu.json',
        'R1': 'DUNG', 'R2': 'DUNG_MOT_PHAN_SAI_VI_DU_RR_ROUTE', 'R3': 'DUNG',
        'unresolved_blocking_issue': False, 'reviewer_rechecked_revision': False,
        'retained_correction': 'dev-14372e1209 RR=1/2 at both C and VC, so only three of four route cases have RR=1.',
        'proposal': 'DE_NGHI_DUNG_PHAN_BIEN_VE_TINH_DUNG_MINH_QUYET',
    }
    revised['canonical'] = dict(previous['canonical'], **{'de-xuat-tiep-theo.md': 'results/T-049/de-xuat-tiep-theo.md'})
    revised['current_sources'] = {p: info(ROOT / p) for p in previous['current_sources']}
    revised['mutable_log_prefixes'] = {LOG: info(ROOT / LOG)}
    revised['response_checks'] = receipt
    revised['outputs'] = inventory()
    revised['output_count'] = len(revised['outputs'])
    revised['total_logical_bytes'] = sum(v['bytes'] for v in revised['outputs'].values())
    MANIFEST.write_text(json.dumps(revised, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    check_final()


if __name__ == '__main__':
    main()
