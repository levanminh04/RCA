"""Pinned source-contract fixtures; no telemetry reads or network."""
import ast
from collections import defaultdict
import contextlib
import hashlib
import io
import json
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable, Dict, List, Optional, Tuple
import zipfile
import numpy as np
import pandas as pd
from simple_runner import ROOT, OUT, SOURCE, load_kernels, read, sha, write


def main():
    folder=OUT/'source-contract-002';folder.mkdir(exist_ok=False)
    pins={x['file']:x for x in read(ROOT/'results/T-017/sources/download-manifest.json')}
    zp=SOURCE/'zenodo/rcabench-platform-feat-fse26.zip'
    assert sha(zp)==pins['zenodo/rcabench-platform-feat-fse26.zip']['sha256']
    sources=[]
    with zipfile.ZipFile(zp) as archive:
        pyfiles=[n for n in archive.namelist() if n.endswith('.py')]
        texts={n:archive.read(n).decode('utf-8-sig') for n in pyfiles}
        for suffix in ['cli/dataset_transform/make_nezha.py','src/rcabench_platform/v2/evaluation/ranking.py',
                       'src/rcabench_platform/v2/experiments/report.py','src/rcabench_platform/v2/experiments/single.py',
                       'src/rcabench_platform/v2/sources/convert.py']:
            key=next(k for k in texts if k.endswith(suffix));data=archive.read(key)
            sources.append(dict(member=key,bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
        maker=texts[next(k for k in texts if k.endswith('cli/dataset_transform/make_nezha.py'))]
        six={name:[k for k,v in texts.items() if name in v] for name in ['normal_logs.parquet','abnormal_logs.parquet','normal_metrics.parquet','abnormal_metrics.parquet','normal_traces.parquet','abnormal_traces.parquet']}
        assert all(not any(k.endswith('cli/dataset_transform/make_nezha.py') for k in refs) for refs in six.values())
        assert '"Duration": "duration"' in maker and '"level",' in maker
        tree=ast.parse(maker)
        cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='MultiDateDatasetLoader')
        clazz=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='NezhaDatasetLoader')
        # Exact expressions in both constructors, evaluated with metadata-only stubs.
        joins=[]
        for node in [cls,clazz]:
            for expr in ast.walk(node):
                if isinstance(expr,ast.Call) and isinstance(expr.func,ast.Attribute) and expr.func.attr=='join' and any(isinstance(a,ast.Constant) and a.value=='rca_data' for a in expr.args):
                    joins.append(dict(class_name=node.name,line=expr.lineno,expression=ast.unparse(expr)))
    kernels,kernelpins=load_kernels();ns,_,nz=kernels
    adapterpath=SOURCE/'github/orig/src/simplerca/nezha_adapter.py'
    assert sha(adapterpath)==pins['github/orig/src/simplerca/nezha_adapter.py']['sha256']
    tree=ast.parse(adapterpath.read_text(encoding='utf-8-sig'))
    cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='NezhaDataAdapter')
    nsadapter=dict(pd=pd,Path=Path,Any=Any,Callable=Callable,AlgorithmAnswer=dict,AlgorithmArgs=SimpleNamespace,debug=lambda:False)
    exec(compile(ast.Module(body=[cls],type_ignores=[]),str(adapterpath),'exec'),nsadapter)
    fixture=folder/'missing-paired-files';fixture.mkdir()
    stdout=io.StringIO()
    with contextlib.redirect_stdout(stdout):
        answer=nsadapter['NezhaDataAdapter'](nz['nezha_rca'])(SimpleNamespace(input_folder=fixture,output_folder=fixture,dataset='nezha-ob'))
    assert answer==[] and stdout.getvalue().count('not found, returning empty DataFrame')==6
    write(folder/'fixtures.json',dict(status='PASS',source_files=sources,kernel_pins=kernelpins,
        zip_sha256=sha(zp),python_files_scanned=len(pyfiles),paired_file_references=six,
        native_adapter_absent_paired_inputs=dict(answer=answer,warnings=stdout.getvalue().splitlines(),
            interpretation='Exact adapter returns six empty dataframes and empty diagnosis; singular Nezha generator output is not renamed by its pinned convert/caller path; other RCABench readers do reference paired files'),
        source_contracts=[
          dict(claim='generator writes singular log/metric/trace parquet; CLI adapter asks six N/A plurals',source='make_nezha.py:97,106,115; nezha_adapter.py:29-46'),
          dict(claim='metric output long; NezhaRCA expects wide and does not pivot nezha dataset',source='make_nezha.py:156-179; nezha_adapter.py:49-51,95-115'),
          dict(claim='Duration unchanged; kernels divide as if nanoseconds',source='make_nezha.py:213,225; main.py:440; nezha_rca.py:259'),
          dict(claim='generator does not create severity',source='make_nezha.py:292-312,340-365'),
          dict(claim='normal from construct_data first minute, not P3 preincident5min; author abnormal until next inject minus1min',source='make_nezha.py:476-495,530-584,616-624'),
          dict(claim='native MRR filters hit; report default aggregates raw outputs; single-case fill0 path also exists',source='ranking.py:46-59; report.py:19-31,64-65; single.py:110')],
        duplicate_path_joins=joins,
        not_claimed=['No claim that current artifact produced Table2','No claim every evaluator path uses conditional MRR','No inference that low dev scores falsify all variants'],
        labels_read=False,telemetry_read=False))
    write(folder/'invocation.json',dict(script_sha256=sha(__file__),runtime=__import__('sys').executable))


if __name__=='__main__':main()
