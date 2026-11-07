"""Build the reviewable code/opaque-metadata packet without opening test payloads."""
from collections import Counter
import json
from pathlib import Path
import re
import sys
import tarfile

from activate import ROOT, RUN, pin
from bien_nhan import atomic, digest, read_pin, ref
from dieu_phoi import memory_request


def main():
    protocol = read_pin(pin(RUN / 'protocol-candidate.json'))
    code = read_pin(pin(RUN / 'code-pins.json'))['files']
    files = {p: dict(meta, source_path=p) for p, meta in code.items()}
    def add(path, destination=None):
        origin = Path(path)
        if not origin.is_absolute():
            origin = ROOT / origin
        rel = origin.relative_to(ROOT).as_posix()
        files[destination or rel] = dict(ref(origin), source_path=rel)
    for name in ('protocol-candidate.json', 'dispatch-contract.json', 'placement.json', 'failure-policy.json',
                 'environments.json', 'code-pins.json', 'environment-patches.json', 'OB-group-decision.json',
                 'preparation-permission.json', 'sources/TT-runtime.json', 'sources/TT-independent.json',
                 'prepared/ec2_1-plan.json', 'prepared/ec2_2-plan.json'):
        add(RUN / name)
    # Full-cohort metadata is kept; private label/source maps stay on the laptop.
    for key in ('cohorts_source', 'm1_contract_ref'):
        read_pin(protocol[key]); add(protocol[key]['path'])
    contract = read_pin(protocol['dispatch_contract_ref'])
    for key in ('sensitivity_decision_ref',):
        read_pin(contract[key]); add(contract[key]['path'])
    read_pin(contract['budget']['decision_ref']); add(contract['budget']['decision_ref']['path'])
    for evidence in read_pin(pin(RUN / 'failure-policy.json'))['code_evidence']:
        source = ROOT / evidence['path']
        assert source.stat().st_size == evidence['bytes'] and digest(source) == evidence['sha256']
        add(source)
    for host in ('ec2_1', 'ec2_2'):
        plan = read_pin(pin(RUN / 'prepared' / (host + '-plan.json')))
        for job in plan['jobs']:
            if job.get('static_snapshot'):
                read_pin(job['static_snapshot']); add(job['static_snapshot']['path'])
    upstream = read_pin(pin(RUN / 'upstream-pins.json'))
    for rel, expected in upstream['files'].items():
        source = RUN / 'upstream/rcaeval' / rel
        assert source.stat().st_size == expected['bytes'] and digest(source) == expected['sha256']
        add(source, 'upstream/rcaeval/' + rel)
    forbidden = ('source-bundle.json', 'OB-runtime.json', 'OB-independent.json', 'aggregate-plan.json', 'local-plan.json')
    assert not any(path.endswith(forbidden) for path in files)
    for dest, meta in files.items():
        assert not dest.startswith('data/') and not Path(dest).is_absolute() and '..' not in Path(dest).parts
        if dest.endswith('.json'):
            value = (ROOT / meta['source_path']).read_text(encoding='utf-8')
            assert not re.search(r're2tt_[A-Za-z0-9_-]+_(?:cpu|mem|delay|loss|disk|socket|http)[A-Za-z0-9_-]*_\d+', value), dest
            assert '"cases_by_member":' not in value or dest.endswith('TT-independent.json'), dest
    packet = dict(schema='T054-013-CODE-OPAQUE-METADATA', files=files, raw_test_files=0,
                  private_label_or_original_source_maps=0, upstream_revision=upstream['revision'])
    atomic(RUN / 'main-packet.json', packet)
    with tarfile.open(RUN / 'main-code-metadata.tar.gz', mode='x:gz', dereference=True) as archive:
        for destination, meta in sorted(files.items()):
            archive.add(ROOT / meta['source_path'], arcname=destination, recursive=False)
        archive.add(RUN / 'main-packet.json', arcname=(RUN / 'main-packet.json').relative_to(ROOT).as_posix())
    # Existing 012 scenario: one source copy + four DEV-derived output copies + 2GiB operating space.
    # Include source bytes from metadata only, once per distinct destination.
    cloud = read_pin(pin(RUN / 'cloud-verification.json'))
    old_outputs = read_pin(pin(ROOT / 'results/T-054/manifest-hoan-thien-local-g3-011.json'))['outputs']
    storage_path = 'results/T-054/runs/hoan-thien-local-g3-011/storage-copy-accounting.json'
    storage = read_pin(dict(old_outputs[storage_path], path=storage_path))
    conditions = dict(schema='T054-013-LAUNCH-CONDITIONS', hosts={}, local={})
    for host, evidence in [('ec2_1', 'ec2-large-disk'), ('ec2_2', 'ec2-small-disk'), ('local', None)]:
        plan = read_pin(pin(RUN / 'prepared' / (host + '-plan.json')))
        source = {m['path']: m['bytes'] for job in plan['jobs'] for m in job['source']['files'].values()}
        largest = max(memory_request(plan, job) for job in plan['jobs'])
        required_ram = largest + plan['resources']['reserve_bytes']
        if evidence:
            # 8GiB scenario exceeds the previous ~5.27GiB estimate for 35 TT; not a proved upper bound.
            conditions['hosts'][host] = dict(instance_id=cloud['hosts'][evidence]['instance_id'],
                 required_free_disk_bytes=8 * 1024**3, required_free_ram_bytes=required_ram,
                 source_bytes=sum(source.values()), source_files=len(source), workers=plan['workers'],
                 disk_basis='retained conservative scenario >=012 35-TT forecast; monitor actual growth, no deletion')
        else:
            conditions['local'] = dict(required_free_disk_bytes=storage['corrected_planning_bytes'], required_free_ram_bytes=required_ram,
                 source_files=len(source), source_bytes=sum(source.values()), workers=plan['workers'],
                 disk_basis='011 10.062GiB retained scenario, originals already present; opaque TT uses hardlinks')
    atomic(RUN / 'launch-conditions.json', conditions)
    strict = cloud['PASS']
    rows = [row for host in cloud['hosts'].values() for row in host['rows']]
    different = [row for row in rows if not row['PASS']]
    assert len(rows) == 15 and len(different) == 1
    atomic(RUN / 'parity-disposition.json', dict(strict_exact_all=strict, exact_rows=14, total_rows=15,
        accepted_for_preparation=True, exception=pin(RUN / 'numeric-parity-Ce-decision.json'),
        lineage=pin(RUN / 'numeric-parity-Ce-lineage.json'), unchanged_strict_result=pin(RUN / 'cloud-verification.json'),
        note='One observed comparison accepted by Minh; no tolerance added to the method or future comparisons'))
    print(json.dumps(dict(PASS=True, packet_files=len(files), packet_bytes=(RUN/'main-code-metadata.tar.gz').stat().st_size)))


if __name__ == '__main__':
    main()
