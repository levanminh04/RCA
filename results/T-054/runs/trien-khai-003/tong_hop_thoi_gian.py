"""Thời gian thực đo và kịch bản lạnh có giả định; không tự tạo ETA hoặc cap main."""
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4];OUT=ROOT/'results/T-054';RUN=OUT/'runs/trien-khai-003'
sys.path.insert(0,str(OUT/'scripts'))
from bien_nhan import atomic,read_pin,ref
from dieu_phoi import status

one=read_pin(ref(RUN/'pilot-local-007/summary.json'))
two=read_pin(ref(RUN/'pilot-local-008/summary.json'))
diag=read_pin(ref(RUN/'diagnostic-thread-001/summary.json'))
start=read_pin(ref(RUN/'pilot-local-008/queue/budget-start.json'))
end=status(RUN/'pilot-local-008/queue')['last_event']['utc']
end_epoch=datetime.fromisoformat(end).timestamp()
attempts=[]
for p in RUN.glob('pilot-local-*/queue/*/attempt-[0-9]*/cost.json'):
    cost=read_pin(ref(p));attempts.append({'ref':ref(p),'cost':cost})
groups={}
for packet in (one,two):
    for k,values in packet['group_wall_s'].items():groups.setdefault(k,[]).extend(values)
primary_cost={(r['dataset'],r['arm'],r['seed']):r['cost_s'] for r in one['method_statuses']}
matrix=read_pin(ref(OUT/'matrix.json'))
main_seconds=sum(primary_cost[(j['dataset'],j['arm'],j['seed'])] for j in matrix['main'])
aux_A_seconds=60*sum(primary_cost[('RE2-TT','torai_A',seed)] for seed in (0,1,2))
ce_scenario_60=60*primary_cost[('RE2-TT','M1',None)]
doc={'schema':'T054-TIMING-EVIDENCE-1','status':'MEASURED_DEV_AND_CONDITIONAL_SERIAL_SCENARIO_NOT_MAIN_ETA',
 'inputs':{'packet1':ref(RUN/'pilot-local-007/summary.json'),'packet2':ref(RUN/'pilot-local-008/summary.json'),
           'diagnostic':ref(RUN/'diagnostic-thread-001/summary.json'),'matrix':ref(OUT/'matrix.json')},
 'measured':{'unique_DEV_cases':4,'registered_slots':40,'diagnostic_calls_separate':1,
   'retained_attempts_with_cost':len(attempts),'all_attempt_wall_s_including_repeats':sum(x['cost']['wall_s'] for x in attempts),
   'diagnostic_wall_s':diag['wall_s'],
   'pilot_elapsed_start_to_final_supervisor_stop_s':end_epoch-start['started_epoch'],
   'elapsed_includes_gaps_and_debugging':True,'first_start_epoch':start['started_epoch'],'last_supervisor_stop_UTC':end,
   'sum_latest_selected_40_slot_attempts_s':one['sum_attempt_wall_s']+two['sum_attempt_wall_s'],
   'score_s':one['score_s']+two['score_s'],'group_cost_samples_s':groups},
 'scenario':{'not_ETA':True,'worker_count':1,'model':'replicate first packet cost for each slot of main matrix, isolated/cold driver as currently implemented',
   'main_1342_slots_seconds':main_seconds,'auxiliary_A_180_slots_seconds':aux_A_seconds,
   'C_e_H60_if_same_cost_as_mainTT_seconds':ce_scenario_60,
   'main_plus_A_hours':(main_seconds+aux_A_seconds)/3600,
   'main_plus_A_plus_Ce60_hours':(main_seconds+aux_A_seconds+ce_scenario_60)/3600,
   'C_d3_supported_solver_not_predicted':True,
   'assumptions':['all future cases same cost as first sample per method/seed',
                  'no input/E4 reuse across arms; current worker resets cache each slot',
                  'no concurrency speedup assumed; no cloud main permission',
                  'A source for main cohort not yet granted; C-e H not yet verified'],
   'when_wrong':['case/channel/operation counts and solver branch differ','cache/bundle or worker concurrency changes',
                 'I/O/memory/paging differs','support/windows/timeouts changed before lock'],
   'dependent_decision':'cannot choose overnight start/cap/main finish from these numbers; need implement/measure authorized bundle and 2/3-worker scheduling first'},
 'main_ETA':None,'main_ETA_reason':'representative C-e and numeric parity policy, input/E4 bundle reuse and 2/3 throughput not completed',
 'test_opened':False,'main_started':False,'attempts':attempts}
atomic(RUN/'thoi-gian-va-kich-ban.json',doc)
print(json.dumps({'measured':doc['measured'],'scenario':doc['scenario'],'main_ETA':None},ensure_ascii=False))
