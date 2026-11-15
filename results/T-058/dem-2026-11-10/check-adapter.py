"""Small semantic checks for ID/time/source-clock conversion; no research data."""
import importlib.util
from pathlib import Path
import unittest

spec=importlib.util.spec_from_file_location('adapter_ft',Path(__file__).parent/'src/m1/adapter_flashticket.py')
ft=importlib.util.module_from_spec(spec); spec.loader.exec_module(ft)

def string(value): return {'stringValue':value}
def trace_doc(parent=None):
    span={'traceId':'a'*32,'spanId':'b'*16,'name':'GET /items/{id}','kind':2,
          'startTimeUnixNano':'999000000001','endTimeUnixNano':'1000000000999'}
    if parent is not None: span['parentSpanId']=parent
    return {'resourceSpans':[{'resource':{'attributes':[{'key':'service.name','value':string('booking-service')}]},'scopeSpans':[{'spans':[span]}]}]}

class Conversion(unittest.TestCase):
    def test_root_and_integer_units(self):
        rows,cov,diag=ft.normalize_spans([trace_doc()],700*ft.NS,1300*ft.NS,['booking-service'])
        self.assertEqual(rows[0]['parentSpanID'],'')
        self.assertEqual(rows[0]['start_us'],999000000)
        self.assertEqual(rows[0]['duration_us'],1000000)
        self.assertEqual(diag['root_spans'],1)
    def test_zero_parent_and_missing_parent_are_distinct(self):
        rows,_,diag=ft.normalize_spans([trace_doc('0'*16)],700*ft.NS,1300*ft.NS,['booking-service'])
        self.assertEqual(rows[0]['parentSpanID'],'')
        rows,_,diag=ft.normalize_spans([trace_doc('c'*16)],700*ft.NS,1300*ft.NS,['booking-service'])
        self.assertEqual(rows[0]['parentSpanID'],'c'*16)
        self.assertEqual(diag['parent_missing_in_window'],1)
    def test_duplicate_is_deduplicated(self):
        rows,_,diag=ft.normalize_spans([trace_doc(),trace_doc()],700*ft.NS,1300*ft.NS,['booking-service'])
        self.assertEqual(len(rows),1); self.assertEqual(diag['duplicate_records'],1)
    def test_native_time_not_evaluation_time(self):
        labels={'service_name':'booking-service','container_id':'x'}
        b={'channel':'cpu','native':True,'step_seconds':15,
           'result':[{'metric':labels,'values':[[1000,'0.1'],[1015,'0.1'],[1030,'0.2']]}],
           'native_timestamps':[{'metric':labels,'values':[[1000,'999.125'],[1015,'999.125'],[1030,'1029.125']]}]}
        rows,owners,indices,clocks,cov,aliases,diag=ft.normalize_metrics([b],['booking-service'])
        self.assertEqual([r['time'] for r in rows],[999125000000,1029125000000])
        self.assertEqual(diag['repeated_native_points'],1)
        self.assertEqual(list(indices.values()),[[0,1]])
    def test_missing_clock_rejected(self):
        b={'channel':'cpu','native':True,'step_seconds':15,'result':[{'metric':{'service_name':'booking-service'},'values':[[1000,'0.1']]}],'native_timestamps':[]}
        with self.assertRaises(ValueError): ft.normalize_metrics([b],['booking-service'])
    def test_database_prefix_preserves_owner(self):
        labels={'postgresql_database_name':'event_db'}
        b={'channel':'db-size','native':True,'step_seconds':15,'result':[{'metric':labels,'values':[[1000,'12']]}],
           'native_timestamps':[{'metric':labels,'values':[[1000,'999.5']]}]}
        rows,_,_,_,_,aliases,_=ft.normalize_metrics([b],['event_db'])
        self.assertIn('event-db_db-size',rows[0]); self.assertEqual(aliases['event-db'],'event_db')
    def test_nonfinite_remains_missing(self):
        b={'channel':'latency-50','native':False,'step_seconds':15,'result':[{'metric':{'service_name':'booking-service'},'values':[[1000,'NaN']]}]}
        rows,*_=ft.normalize_metrics([b],['booking-service'])
        self.assertIsNone(rows[0]['booking-service_latency-50'])
    def test_malformed_id_rejected(self):
        with self.assertRaises(ValueError): ft.hex_id('root',16)
        with self.assertRaises(ValueError): ft.hex_id('0'*32,32)

if __name__=='__main__': unittest.main()
