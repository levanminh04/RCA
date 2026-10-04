import unittest
from dataclasses import replace
import numpy as np
from simplerca import Config, diagnose, score_root
from simplerca.adapter import canonical_service, prepare
import pandas as pd
import argparse
import importlib.util
import io
import json
import sys
from pathlib import Path
from unittest.mock import Mock, patch
from simplerca.adapter import core_input

REPO=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(REPO/'results/T-017/scripts'))
import run_dev


class KnownAnswers(unittest.TestCase):
    def run_case(self, **kwargs):
        base=dict(normal_metrics={'a_cpu':[0,0,0],'b_cpu':[1,1,1]},
                  incident_metrics={'a_cpu':[0,2,3],'b_cpu':[1,1,1]},
                  metric_services={'a_cpu':'a','b_cpu':'b'})
        base.update(kwargs)
        return diagnose(**base)

    def test_known_metric_trace_log(self):
        r=self.run_case(normal_traces={'a':[10]*4},incident_traces={'a':[31]*4},incident_logs={'a':['ERROR fail','exception','ok']})
        self.assertEqual(r['scores']['a'],dict(metric=2,trace=1,log=1,score=4))
        self.assertEqual(r['logs']['a']['count'],2)
        self.assertEqual(r['traces']['a']['threshold'],30)
        self.assertEqual(r['ranks'][0],'a')

    def test_metric_threshold_boundary(self):
        n=[0,2];h=4.0
        r=diagnose({'x':n},{'x':[h,h+1]},{'x':'a'})
        self.assertEqual(r['metrics']['x']['threshold'],h)
        self.assertEqual(r['metrics']['x']['count'],1)

    def test_trace_boundary_zero_and_nan(self):
        r=self.run_case(normal_traces={'b':[10,10,np.nan]},incident_traces={'b':[30,30]})
        self.assertEqual(r['scores']['b']['trace'],0)
        r=self.run_case(normal_traces={'b':[0,0]},incident_traces={'b':[1,1]})
        self.assertEqual(r['scores']['b']['trace'],1)

    def test_missing_empty_log_distinct(self):
        self.assertEqual(self.run_case()['logs']['a']['status'],'unavailable')
        self.assertEqual(self.run_case(incident_logs={})['logs']['a']['count'],0)

    def test_keyword_case_count_once_and_threshold(self):
        r=self.run_case(incident_logs={'a':['error FAIL exception']},config=Config(log_threshold=1))
        self.assertEqual(r['logs']['a']['count'],1)
        self.assertEqual(r['scores']['a']['log'],0)

    def test_normal_control_abstain(self):
        r=self.run_case(incident_metrics={'a_cpu':[0,0,0],'b_cpu':[1,1,1]})
        self.assertEqual(r['status'],'abstain')
        self.assertEqual(score_root(r,'a')['hit_fractional'],0)

    def test_column_order_and_repeat(self):
        x=self.run_case(); y=self.run_case(normal_metrics={'b_cpu':[1,1,1],'a_cpu':[0,0,0]},incident_metrics={'b_cpu':[1,1,1],'a_cpu':[0,2,3]})
        self.assertEqual(x,y); self.assertEqual(x,self.run_case())

    def test_ties_and_unobserved(self):
        r=self.run_case(incident_metrics={'a_cpu':[1,0,0],'b_cpu':[2,1,1]})
        self.assertEqual(r['tie_groups'][0]['services'],['a','b'])
        self.assertEqual(score_root(r,'b')['hit_fractional'],0.5)
        self.assertEqual(score_root(r,'c')['hit_fractional'],0)
        self.assertNotIn('c',r['ranks'])

    def test_modality_only_service(self):
        r=self.run_case(incident_logs={'c':['ERROR']})
        self.assertIn('c',r['ranks']); self.assertEqual(r['scores']['c']['score'],1)

    def test_normal_only_log_identity_without_error_vote(self):
        epoch=1700000000;pod='log-only-pod'
        m=pd.DataFrame({'time':[epoch-2,epoch-1,epoch],'a_cpu':[1,1,2]})
        l=pd.DataFrame({'timestamp':[epoch-3,epoch-1,epoch,epoch+3,epoch-4],
                        'container_name':[pod,pod,'incident-only','after','before'],
                        'message':['ERROR','FAIL EXCEPTION','ERROR','ERROR','ERROR']})
        prepared=prepare(m,None,l,epoch,3,aliases={pod:'normal-only'})
        r=diagnose(**core_input(prepared))
        self.assertEqual(set(r['scores']),{'a','normal-only','incident-only'})
        self.assertEqual(r['scores']['normal-only']['score'],0)
        self.assertEqual(r['logs']['normal-only']['count'],0)
        self.assertEqual(r['logs']['incident-only']['count'],1)
        self.assertEqual(prepared.incident_logs['service'].tolist(),['incident-only'])

    def test_normal_only_log_abstain_with_no_metric_channels(self):
        epoch=1700000000;m=pd.DataFrame({'time':[epoch-1,epoch]})
        l=pd.DataFrame({'timestamp':[epoch-1],'container_name':['only-log'],'message':['ERROR']})
        r=diagnose(**core_input(prepare(m,None,l,epoch,3)))
        self.assertEqual(r['ranks'],['only-log'])
        self.assertEqual(r['status'],'abstain')
        self.assertEqual(r['logs']['only-log']['count'],0)

    def test_adapter_log_missing_and_empty_stay_distinct(self):
        epoch=1700000000
        m=pd.DataFrame({'time':[epoch-2,epoch-1,epoch],'a_cpu':[1,1,2]})
        absent=diagnose(**core_input(prepare(m,None,None,epoch,3)))
        empty=pd.DataFrame(columns=['timestamp','container_name','message'])
        present=diagnose(**core_input(prepare(m,None,empty,epoch,3)))
        self.assertEqual(absent['logs']['a']['status'],'unavailable')
        self.assertEqual(present['logs']['a']['count'],0)

    def test_missing_and_insufficient(self):
        r=self.run_case(normal_metrics={'a_cpu':[np.nan,1],'b_cpu':[1,1,1]})
        self.assertEqual(r['metrics']['a_cpu']['status'],'unavailable')
        self.assertEqual(r['metrics']['a_cpu']['missing_normal'],1)
        with self.assertRaises(ValueError): diagnose({'x':[]},{'x':[1]},{'x':'a'})
        with self.assertRaises(ValueError): diagnose({}, {}, {}, observed_services=[])

    def test_negative_duration(self):
        with self.assertRaises(ValueError): self.run_case(normal_traces={'a':[-1]},incident_traces={'a':[1]})

    def test_alternatives_known(self):
        a=self.run_case(config=Config(metric_aggregation='channels'))
        self.assertEqual(a['scores']['a']['metric'],1)
        b=diagnose({'x':[0,1,2]},{'x':[1.9,2]},{'x':'a'},config=Config(metric_rule='p95'))
        self.assertAlmostEqual(b['metrics']['x']['threshold'],1.9)
        self.assertEqual(b['scores']['a']['metric'],1)

    def test_service_normalization(self):
        pod='ts-auth-service-78fc45d88d-k3cr1'
        self.assertEqual(canonical_service(pod,{pod:'ts-auth-service'}),'ts-auth-service')
        self.assertEqual(canonical_service('ts-assurance-mongo'),'ts-assurance-mongo')
        self.assertEqual(canonical_service('ts-contacts-mongo'),'ts-contacts-mongo')
        self.assertEqual(canonical_service('ts-auth-service'),'ts-auth-service')

    def test_cross_modality_explicit_alias(self):
        epoch=1700000000;pod='a-78fc45d88d-k3cr1'
        m=pd.DataFrame({'time':[epoch-2,epoch-1,epoch],'a_cpu':[0,0,1]})
        t=pd.DataFrame({'startTime':[(epoch-1)*1e6,epoch*1e6],'serviceName':[pod,pod],'duration':[1,4]})
        l=pd.DataFrame({'timestamp':[epoch],'container_name':[pod],'message':['ERROR']})
        from simplerca.adapter import core_input
        r=diagnose(**core_input(prepare(m,t,l,epoch,3,aliases={pod:'a'})))
        self.assertEqual(list(r['scores']),['a']);self.assertEqual(r['scores']['a']['score'],3)

    def test_split_and_units(self):
        t=1700000000
        m=pd.DataFrame({'time':[t-1,t,t+1],'a_cpu':[1,2,3]})
        nm,am,*_=prepare(m,None,None,t,1)
        self.assertEqual(nm['a_cpu'].tolist(),[1]); self.assertEqual(am['a_cpu'].tolist(),[2])
        with self.assertRaises(ValueError): prepare(m.assign(time=m.time*1000),None,None,t,1)

    def test_alias_collision_and_cycle(self):
        epoch=1700000000
        m=pd.DataFrame({'time':[epoch-2,epoch-1,epoch],'a_cpu':[0,0,1],'b_cpu':[0,0,2]})
        with self.assertRaises(ValueError): prepare(m,None,None,epoch,3,aliases={'a':'b'})
        with self.assertRaises(ValueError): prepare(m,None,None,epoch,3,aliases={'a':'b','b':'a'})
        duplicate=pd.DataFrame([[epoch,1,2]],columns=['time','a_cpu','a_cpu'])
        with self.assertRaises(ValueError): prepare(duplicate,None,None,epoch,3)


class FrozenCases(unittest.TestCase):
    def setUp(self):
        self.allowed=[f're2tt_synthetic_{i:02d}' for i in range(30)]
        self.data_root=REPO/'data/rcaeval'

    def test_manifest_unique_and_sorted(self):
        manifest=Mock()
        manifest.read_text.return_value=json.dumps(list(reversed(self.allowed)))
        self.assertEqual(run_dev.load_allowlist(manifest),self.allowed)
        for invalid in (self.allowed[:-1],self.allowed[:-1]+[self.allowed[0]],
                        self.allowed[:-1]+['re2tt_../escape']):
            manifest.read_text.return_value=json.dumps(invalid)
            with self.assertRaises(RuntimeError):run_dev.load_allowlist(manifest)

    def test_same_count_replacement_rejected_before_path_reads(self):
        dirs=[self.data_root/n for n in self.allowed[:-1]+['re2tt_FORBIDDEN_SYNTHETIC']]
        with patch.object(Path,'is_dir',side_effect=AssertionError('unexpected path probe')):
            with self.assertRaises(RuntimeError):
                run_dev.validate_cases(dirs,self.allowed,self.data_root)

    def test_reordering_keeps_exact_identity(self):
        dirs=[self.data_root/n for n in reversed(self.allowed)]
        with patch.object(Path,'is_dir',return_value=True),patch.object(Path,'exists',return_value=False):
            run_dev.validate_cases(dirs,self.allowed,self.data_root)

    def test_resolve_must_keep_identity_even_inside_data_root(self):
        p=Mock();p.name=self.allowed[0]
        for target in (self.data_root/self.allowed[1],REPO/'outside'/self.allowed[0]):
            p.resolve.return_value=target
            with self.assertRaises(RuntimeError):run_dev.guard_case(p,self.allowed,self.data_root)
        p.resolve.return_value=self.data_root.resolve()/p.name
        run_dev.guard_case(p,self.allowed,self.data_root)

    def test_main_rejects_before_writes_or_telemetry(self):
        dirs=[self.data_root/n for n in self.allowed[:-1]+['re2tt_FORBIDDEN_SYNTHETIC']]
        args=argparse.Namespace(run='synthetic-never-created',limit=30,start_index=0)
        with patch.object(argparse.ArgumentParser,'parse_args',return_value=args), \
             patch.object(run_dev,'load_allowlist',return_value=self.allowed), \
             patch.object(Path,'glob',return_value=dirs), \
             patch.object(Path,'exists',return_value=False), \
             patch.object(Path,'mkdir',side_effect=AssertionError('unexpected write')), \
             patch.object(run_dev,'sha',side_effect=AssertionError('unexpected hash')), \
             patch.object(pd,'read_parquet',side_effect=AssertionError('unexpected telemetry')):
            with self.assertRaises(RuntimeError):run_dev.main()

    def test_artifact_filter_uses_frozen_aliases_before_returning_rows(self):
        import pyarrow as pa
        import pyarrow.parquet as pq
        path=Path('D:/RCA-ext/work/T-017/sources-audit/filter_fse_artifact_results.py')
        spec=importlib.util.spec_from_file_location('artifact_filter_regression',path)
        module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
        with patch.object(module,'load_allowlist',return_value=self.allowed), \
             patch.object(Path,'glob',side_effect=AssertionError('artifact must not infer permission from disk')):
            allowed,aliases=module.artifact_aliases()
        self.assertEqual(allowed,self.allowed)
        sink=io.BytesIO()
        names=[self.allowed[0],self.allowed[0].removeprefix('re2tt_'),'re2tt_FORBIDDEN_SYNTHETIC']
        pq.write_table(pa.table({'case':names,'value':[1,2,999]}),sink)
        selected=module.select_case_rows(sink.getvalue(),'case',aliases)
        self.assertEqual(selected['case'].to_pylist(),names[:2])
        self.assertEqual(selected['value'].to_pylist(),[1,2])


if __name__=='__main__': unittest.main()
