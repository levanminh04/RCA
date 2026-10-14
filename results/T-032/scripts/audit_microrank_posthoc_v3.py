"""Finish approved checks on the retained RE2 MicroRank pilot; no method run."""
import argparse
import importlib.util
from pathlib import Path
import sys
import traceback
import replay_microrank as r

BASE=Path('/home/ubuntu/rca/T-032')
PINS={
 'replay_microrank.py':'193166089f7d0bf30a2f81551c374bec610f705241f6ad495aa5ff7181126562',
 'capture_microrank.py':'b842b4be0d92470f1fc673e2afb30b5b0b76781c211a4b99ff6518c648b00c8b',
 'compare_microrank_roundoff.py':'7e29b728bbd3c00174b962efd5896a50556d6aa0c68a2dea85e49e2b81ea64a2',
 'check_microrank_t028_v3.py':'324807b59d7b6cbe5062915949b2bd958e0b3ad520cc7e8d1e7dcbff6568a144',
}
OBSERVED=BASE/'runs/re2-ok-001'
NATIVE=BASE/'runs/microrank-native-diagnostic-001'
OBSERVED_CHECK='b53935073c0f64faa77f9baa6299a19baaf7dbcdba40c24772dda958adcb2fb2'
NATIVE_CHECK='d23ce465094077d0ce52706392bf9de2c0bbd9b142dcd3b4ad19f9a60df2a9a4'

def module(name):
 path=BASE/'scripts'/name
 if r.sha(path)!=PINS[name]: raise r.ReplayError('posthoc dependency changed '+name)
 spec=importlib.util.spec_from_file_location('t032_posthoc_'+path.stem,path)
 obj=importlib.util.module_from_spec(spec);spec.loader.exec_module(obj)
 return obj

def audit(out):
 for name,digest in PINS.items():
  if r.sha(BASE/'scripts'/name)!=digest: raise r.ReplayError('dependency mismatch')
 comparator=module('compare_microrank_roundoff.py')
 report=comparator.compare_case('RE2-TT','dev-12a1a88069',OBSERVED,OBSERVED_CHECK,
                               native_run=NATIVE,native_check_sha256=NATIVE_CHECK)
 r.dump(out/'comparison.json',report)
 if not report['record_contract_pass'] or not report['native_observed_exact']['pass']:
  raise r.ReplayError('approved comparison failed; no threshold increase')
 capture=r.verify_capture(OBSERVED/'capture',r.read(OBSERVED/'capture/capture.json'))
 if not capture['pass']: raise r.ReplayError('capture invalid')
 bridge=module('check_microrank_t028_v3.py')
 entry=report['frozen_entry']
 observed_sha=r.sha(OBSERVED/'ban-ghi-0.json')
 trust={'frozen_record_sha256':entry['sha256'],'observed_record_sha256':observed_sha,
        'native_observed_exact':True,'approved_record_comparison_passed':True}
 verdict=bridge.check_t028(repo_root=r.REPO,dataset='RE2-TT',opaque_id='dev-12a1a88069',
    frozen_record_path=r.safe_source(entry['path']),frozen_record_sha256=entry['sha256'],
    observed_record_path=OBSERVED/'ban-ghi-0.json',observed_record_sha256=observed_sha,trusted_check=trust)
 r.dump(out/'t028-check.json',verdict)
 if not all(verdict.get(key) is True for key in ('passed','eligibility','source_verified','frozen_self_check_passed','observed_equivalence_passed')):
  raise r.ReplayError('T028 bridge failed')
 r.dump(out/'check.json',{'status':'PASS','dataset':'RE2-TT','opaque_id':'dev-12a1a88069',
    'methods_executed':False,'native_observed_exact':True,'approved_comparator_passed':True,
    'capture_check':capture,'t028_check_passed':True,'intermediates_eligible':True,'cohort_ready':False,
    'numeric_summary':report['numeric_summary'],'classification':report['classification'],
    'record_bindings':report['record_bindings'],'dependency_hashes':PINS,
    'comparison_sha256':r.sha(out/'comparison.json'),'bridge_sha256':r.sha(out/'t028-check.json'),
    'limits':'T028 graph/local features reused at exact frozen inputs; no native mask/history/physical-cause validation',
    'artifact_manifest':r.artifact_manifest(out)})
 print('ALL_POSTHOC_CHECKS_PASS',flush=True)

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('new_run_dir');args=parser.parse_args()
 if sys.platform!='linux' or Path.home()!=Path('/home/ubuntu'): raise RuntimeError('EC2 only')
 out=r.new_directory(args.new_run_dir)
 r.dump(out/'invocation.json',{'script_sha256':r.sha(__file__),'methods_executed':False})
 try: audit(out)
 except Exception as error:
  r.dump(out/'failure.json',{'status':'FAIL_STOP','error':str(error),'traceback':traceback.format_exc(),
     'methods_executed':False,'intermediates_eligible':False});raise
