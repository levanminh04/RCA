"""Continue D/D0 from the preserved valid assignment output; no raw or labels."""
import argparse
from pathlib import Path
import time
from thuc_hien_buoc3_6 import ROOT, sha, readj, writej, now, output_pairs

def main():
    p=argparse.ArgumentParser();p.add_argument('--run-id',required=True);p.add_argument('--from-run',required=True);a=p.parse_args()
    run=ROOT/'results/T-028/runs'/a.run_id
    if run.exists():raise RuntimeError('Preserve existing attempt')
    run.mkdir(parents=True);began=time.perf_counter()
    previous=ROOT/'results/T-028/runs'/a.from_run
    manifest={'task':'T-028','run_id':a.run_id,'status':'running','started_at':now(),
              'reuse_assignment_source':{'path':str((previous/'ca-sai.json').relative_to(ROOT)).replace('\\','/'),'sha256':sha(previous/'ca-sai.json')},
              'codebook':{'path':'results/T-028/codebook.md','sha256':sha(ROOT/'results/T-028/codebook.md')},'method_rerun':False,'raw_read':False,'payload_files':[]}
    writej(run/'manifest.json',manifest)
    for script in Path(__file__).parent.glob('*.py'):
        snap=run/'script-snapshot'/script.name;snap.parent.mkdir(exist_ok=True);snap.write_bytes(script.read_bytes())
    try:
        prior=readj(str((previous/'manifest.json').relative_to(ROOT)))
        assert prior['codebook']['sha256']==manifest['codebook']['sha256']
        d=readj(manifest['reuse_assignment_source']['path'])
        assert len(d['main_rows'])==312
        old_run=d['run'];d['run']=str(run.relative_to(ROOT)).replace('\\','/')
        d['assignment_reused_from']=old_run
        writej(run/'features-no-label-index.json',readj(str((previous/'features-no-label-index.json').relative_to(ROOT))))
        writej(run/'ca-sai.json',d)
        writej(run/'concentration.json',output_pairs(d['main_rows']))
        manifest.update(status='analysis_computed_pending_independent_and_manual',finished_analysis_at=now(),elapsed_s=time.perf_counter()-began,
                        feature_index=str((run/'features-no-label-index.json').relative_to(ROOT)).replace('\\','/'),
                        outputs={'ca-sai.json':sha(run/'ca-sai.json'),'concentration.json':sha(run/'concentration.json')})
    except BaseException as exc:
        manifest.update(status='failed',failed_at=now(),error=repr(exc),elapsed_s=time.perf_counter()-began)
        raise
    finally:writej(run/'manifest.json',manifest)
    print(manifest['status'],manifest['elapsed_s'])

if __name__=='__main__':main()
