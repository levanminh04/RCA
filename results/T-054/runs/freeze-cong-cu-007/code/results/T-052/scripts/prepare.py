"""Chiếu trường đã kiểm sang bản gọn T13; pha này không nạp nhãn."""
import copy
import gzip
import json
import time

from common import ROOT, RUN, dump, event, metadata, native_index, native_rows, pin, read, save, timing, digest

BASE = 'K-E1+E2+E5'
MAP = {BASE: 'M1', 'K-E2+E5': 'bo-E1', 'K-E1+E5': 'bo-E2',
       'K-E1+E2': 'bo-E5', 'K-R0': 'C-a0', 'K-E1': 'C-a1'}


def main():
    start = time.perf_counter()
    assert read(RUN / 'ec2-pilot-002/received/output/summary.json')['PASS']
    entries, base, lineage = metadata()
    manifest, index = native_index()
    m51 = read('results/T-051/manifest.json')
    kb_seal_path = 'results/T-051/kb-002/seal.json'
    pin(kb_seal_path, m51['outputs'][kb_seal_path])
    seal = read(kb_seal_path)
    for name, sha in seal.items():
        assert digest('results/T-051/kb-002/' + name) == sha
    kb = {}
    with (ROOT / 'results/T-051/kb-002/ban-ghi.jsonl').open(encoding='utf-8') as stream:
        for line in stream:
            r = json.loads(line)
            kb[(r['opaque_id'], r['config_id'])] = r
    ce = read('results/T-051/kb-002/ce.json')
    output = RUN / 'prepared.jsonl.gz'
    proofs, counts = [], {'that': 0, 'ce': 0}
    with output.open('xb') as raw, gzip.GzipFile(fileobj=raw, mode='wb', mtime=0) as stream:
        for entry in entries:
            job = entry['job']
            item, command = index[(job['opaque_id'], job['window'])]
            rows = native_rows(item, manifest, set(MAP))
            compact_checks = 0
            for cid, name in MAP.items():
                conf = command['configs'][cid]
                assert conf['nhanh_z'] is True and conf['che_do'] == base['che_do']
                assert conf['tham_so_E4'] == base['tham_so_E4']
                expected = dict(base['bat_tat'])
                if name == 'bo-E1': expected['E1'] = 'tat'
                if name == 'bo-E2': expected['E2'] = 'tat'
                if name == 'bo-E5': expected['E5'] = False
                if name in ('C-a0', 'C-a1'):
                    expected.update(E2='tat', E5=False, E1='tat' if name == 'C-a0' else 'U')
                assert conf['bat_tat'] == expected
                rec = rows[cid]
                assert rec['opaque_id'] == job['opaque_id'] and rec['status'] in ('OK', 'NO_EVIDENCE')
                if cid not in ('K-R0', 'K-E1'):
                    old = kb[(job['opaque_id'], cid)] if job['window'] == 'that' else ce[cid][job['opaque_id']]
                    for field in ('blocks', 'status', 'verdict'):
                        assert dump(old[field]) == dump(rec[field]), (job, cid, field)
                    for w in ('P', 'S_lo', 'S_hi'):
                        assert dump(old['worlds'][w]['blocks']) == dump(rec['worlds'][w]['blocks'])
                    assert old['extra']['tang_P'] == rec['extra']['tang_P']
                    compact_checks += 1
                result = {k: copy.deepcopy(rec[k]) for k in ('status', 'blocks', 'sets', 'coverage',
                          'verdict', 'classes', 'do_phu_cham')}
                result['worlds'] = {w: {'blocks': x['blocks']} for w, x in rec['worlds'].items()}
                result['region'] = rec['region'] if name not in ('C-a0', 'C-a1') else None
                result['extra'] = {k: rec['extra'][k] for k in ('tang_P', 'kenh_co', 'kenh_co_the_gioi', 'G_N', 'canh')}
                if name == 'M1':
                    result['controls'] = rec['extra']['doi_chung']
                if name == 'C-a0':
                    nodes = sorted({u['ma'].split('|', 2)[1] for u in rec['extra']['don_vi_phan_vi']
                                    if u['ma'].startswith('op|') and u['n_N'] > 0})
                    assert all(a in nodes and b in nodes for a, b in rec['extra']['G_N'])
                    result['graph_N_nodes'] = nodes
                if name == 'M1' and job['window'] == 'that':
                    path = f"results/T-051/t12-001/{entry['index']:02d}.json"
                    pin(path, m51['outputs'][path])
                    t12 = read(path)
                    assert t12['job'] == job
                    # Vế off phải đúng nền hiện hành trước dùng vế on.
                    for w in ('P', 'S_lo', 'S_hi'):
                        assert dump(t12['worlds'][w]['rank'][0]['blocks']) == dump(rec['worlds'][w]['blocks'])
                    assert dump(t12['worlds']['P']['region'][0]) == dump(rec['region'])
                    result['T12_on'] = {w: {'blocks': x['rank'][1]['blocks']} for w, x in t12['worlds'].items()}
                    result['T12_on_region'] = t12['worlds']['P']['region'][1]
                    result['T12_source'] = path
                package = {'job': job, 'index': entry['index'], 'configuration': name,
                           'source': item['path'], 'source_config': cid, 'record': result,
                           'source_config_sha256': digest(item['path'].rsplit('/', 1)[0] + '/command.json')}
                stream.write((dump(package) + '\n').encode('utf-8'))
                counts[job['window']] += 1
            proofs.append({'index': entry['index'], 'job': job, 'source': item['path'],
                           'config_checks': len(MAP), 'KB_checks': compact_checks})
            event('prepared_window', index=entry['index'], dataset=job['dataset'], window=job['window'])
    save(RUN / 'prepared-seal.json', timing('prepare', start, PASS=True, counts=counts,
        native_windows=82, KB_compact_comparisons=sum(r['KB_checks'] for r in proofs),
        output={'path': output.relative_to(ROOT).as_posix(), 'bytes': output.stat().st_size, 'sha256': digest(output)},
        proofs=proofs, labels_read=False, code_lineage=lineage,
        reuse_limits={'C-a': 'projection validated on EC2 pilot-002 (15 native comparisons); E7 intentionally absent',
                     'C-d': 'P only, keep historical status; no new C-d3 on OB'}))


if __name__ == '__main__':
    main()
