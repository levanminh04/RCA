"""T-037: reproduce unsupported SMTP against the pinned T-036, no coercion."""
import copy
import ctypes
from ctypes import wintypes
import datetime as dt
import hashlib
import importlib.util
import json
import pathlib
import platform
import subprocess
import sys
import time
import traceback

ROOT = pathlib.Path('D:/RCA-flashticket')
PLATFORM = pathlib.Path('D:/Project/flash-ticket-platform')
BASE = ROOT/'results/T-037'
SNAP = ROOT/'results/T-036/runs/kiem-r1-after-002/code'

def hashfile(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def write(p, data):
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')

def memory():
    class PMC(ctypes.Structure):
        _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [(k, ctypes.c_size_t) for k in ['PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage','QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage']]
    m = PMC(); m.cb = ctypes.sizeof(m)
    kernel = ctypes.WinDLL('kernel32'); kernel.GetCurrentProcess.restype = wintypes.HANDLE
    if not ctypes.WinDLL('psapi').GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(m), m.cb):
        raise OSError('GetProcessMemoryInfo')
    return {'peak_working_set_bytes':m.PeakWorkingSetSize, 'working_set_bytes':m.WorkingSetSize}

def main(run):
    run.mkdir(parents=True, exist_ok=False)
    # All source and code hashes are verified before import/use.
    pre = json.loads((BASE/'runs/tu-ra-001/preflight.json').read_text(encoding='utf-8'))
    verify = []
    for row in pre['manifests'][0]['files']:
        p = ROOT/row['path']
        actual = hashfile(p)
        verify.append({'path':row['path'], 'matches':actual==row['sha256']})
    for row in pre['platform_sources']:
        p = pathlib.Path(row['path'])
        verify.append({'path':str(p), 'matches':hashfile(p)==row['sha256']})
    for row in pre['current_code']:
        verify.append({'path':row['current'], 'matches':hashfile(pathlib.Path(row['current']))==row['sha256']})
    assert all(r['matches'] for r in verify), 'INPUT_DRIFT_STOP'
    write(run/'input-check.json', verify)
    oracle = json.loads((BASE/'counterexample-smtp.json').read_text(encoding='utf-8'))
    sources = []
    for sid, rel in [('FT-B13','docs/architecture/B13-api-and-event-contracts.md'), ('FT-B14','docs/architecture/B14-main-flow-sequences.md'), ('FT-B14-03','docs/diagrams/src/B14-03-ticket-delivery-checkin-sequence.puml')]:
        p = PLATFORM/rel
        sources.append({'id':sid,'kind':'design','revision':pre['platform_head'],'sha256':hashfile(p),'condition':'Nguồn thiết kế local đã ghim; không là runtime'})
    registry = {'sources':sources}
    prov = oracle['source_observation']['provenance']
    doc = {'scope':{'system':'FlashTicket','revision':pre['platform_head']},
           'entities':[{'id':eid,'name':eid,'type':typ,'granularity':'component','role':role,'provenance':prov} for eid,typ,role in [('ticket-service','service','phát/giao vé'),('smtp','external','đối tác SMTP')]],
           'operations':[{'entity':'ticket-service','name':'gửi SMTP','runtime_name':None,'provenance':prov}],
           'relations':[{'id':'smtp-minimal','source':{'entity':'ticket-service','operation':'gửi SMTP'},'target':{'entity':'smtp','operation':None},'type':'gọi-đồng-bộ','channel':'smtp','messaging':None,'context':'Tổng hợp kiểm channel từ nguồn B14 §6, chưa là quan sát runtime','provenance':prov}],
           'resource_bindings':[],'signals':[]}
    write(run/'input.json', doc); write(run/'registry.json', registry)
    (run/'oracle-before-execution.json').write_bytes((BASE/'counterexample-smtp.json').read_bytes())
    # No mutation to shared module or coercion of SMTP into another transport.
    spec = importlib.util.spec_from_file_location('t037_pinned_static',SNAP/'__init__.py',submodule_search_locations=[str(SNAP)])
    mod = importlib.util.module_from_spec(spec);sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
    started = time.perf_counter(); results=[]
    for typ in oracle['independent_expected']['candidate_call_types_tested']:
        variant=copy.deepcopy(doc);variant['relations'][0]['type']=typ
        before=copy.deepcopy(variant)
        try:
            mod.build(variant, registry)
            observed='ACCEPTED'
        except ValueError as e:
            observed=str(e)
        results.append({'type_candidate':typ,'channel':'smtp','observed':observed,'expected':'relation_type','matches_oracle':observed=='relation_type','input_unchanged':variant==before})
    elapsed=time.perf_counter()-started
    result={'task':'T-037','client_date':'2026-10-16','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'command':'py -3 -X utf8 -B results/T-037/check-counterexample.py '+run.name,
            'environment':{'device':platform.node(),'platform':platform.platform(),'python':sys.version,'executable':sys.executable},
            'code_snapshot':str(SNAP),'oracle_sha256':hashfile(BASE/'counterexample-smtp.json'),
            'cases':results,'all_reproduced':all(x['matches_oracle'] and x['input_unchanged'] for x in results),
            'scope':'Only minimal counterexample, not full T037 pilot or graph correctness',
            'seconds_two_build_calls':elapsed,'process_memory':memory(),
            'cost_status':'Small counterexample only; do not extrapolate full T037 cost from this sample'}
    write(run/'result.json', result)
    print(json.dumps(result, ensure_ascii=False))

if __name__=='__main__':
    run=BASE/'runs'/sys.argv[1]
    try:main(run)
    except BaseException:
        run.mkdir(parents=True,exist_ok=True)
        (run/'failure.txt').write_text(traceback.format_exc(),encoding='utf-8')
        raise
