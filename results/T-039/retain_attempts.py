"""Preserve current exact outputs and honestly labelled historical reconstructions."""
import sys
sys.dont_write_bytecode=True
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('t039_execution',Path(__file__).with_name('execute_pinned.py'))
e=importlib.util.module_from_spec(spec);spec.loader.exec_module(e)
b=e.BASE
current=b/'runs/thuc-thi-snapshot-004/outputs'
for path in [b/'ban-ghi.json',b/'mapping.json']+list((b/'do-thi').rglob('*.json'))+list((b/'doi-chieu').rglob('*.json')):
    target=current/path.relative_to(b);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(path.read_bytes())
archive=b/'runs/khoi-phuc-lich-su-001';archive.mkdir(exist_ok=False)
api=e.pinned();registry=e.read(b/'nguon.json');inventory=e.read(b/'runs/tien-kiem-001/graph-inventory.json')['rows']
rows=[]
for attempt,limit,mapping_path in [('thuc-thi-snapshot-002',3,b/'runs/thuc-thi-snapshot-003/before/mapping.json'),('thuc-thi-snapshot-003',132,b/'runs/thuc-thi-snapshot-004/before/mapping.json')]:
    source=b/'runs'/attempt
    doc=e.read(source/'document.json');mapping=e.read(mapping_path)['rows'];ent,op=api.build(doc,registry)
    dest=archive/attempt
    e.write(dest/'graphs.json',dict(entity=ent,operation=op,mapping=mapping))
    for item in inventory[:limit]:
        graph=e.read(e.ROOT/item['path']);sg=ent if item['level']=='entity' else op
        active=[x for x in mapping if item['level']=='operation' or x['level']=='entity']
        context=dict(system='Nezha-OB',level=item['level'],domain='dev-adapter',trace_revision='T035-v2.1-canonical',revision_link_verified=False,revision_provenance=[])
        result=api.compare(sg,graph,active,context,registry);e.independent(result,sg,graph,active)
        e.write(dest/item['opaque_id']/item['level']/(item['window']+'.json'),result)
    rows.append(dict(attempt=attempt,reconstructed_graphs=limit,document=e.rel(source/'document.json'),mapping=e.rel(mapping_path),state='RECONSTRUCTED_NOT_ORIGINAL_BYTES',reason='Earlier runner wrote canonical outputs without per-attempt copy; inputs and failures were retained. Reconstruction recovers reproducible content, cannot prove original bytes. Current004 exact output is archived separately.'))
e.write(archive/'receipt.json',dict(rows=rows,current_exact_archive=e.rel(current),future_runner='Now saves every graph and mapping into run/outputs as well as canonical paths. No source/shared code was changed.'))
print('retained exact current output and 135 explicitly reconstructed historical comparisons')
