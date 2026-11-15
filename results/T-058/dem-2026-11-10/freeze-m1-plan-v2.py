"""STEER #4 revision, after OOM observations and before any M1 output."""
import datetime,hashlib,json,math
from pathlib import Path
root=Path(__file__).resolve().parent
target=root/'m1-execution-plan-v2.json'
if target.exists(): raise SystemExit('Refuse to overwrite plan v2')
recovery=json.loads((root/'jvm-memory-fix.json').read_text(encoding='utf8'))
r=datetime.datetime.fromisoformat(recovery['finished_utc']).timestamp()
start=math.ceil((r+600)/60)*60
stamp=lambda t:datetime.datetime.fromtimestamp(t,datetime.timezone.utc).isoformat()
files=['src/m1/adapter_flashticket.py','stage-m1.py','run-m1.py','m1-p7-config.json','m1-source-pins.json',
       'flashticket-inventory-source.json','pause-probe-v2.py','light-load-v2.py','fix-jvm-memory.py']
plan={'version':2,'frozen_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'amendment':'Sửa sau khi thấy OOM, trước khi có đầu ra M1, theo STEER #4. Không đổi phương pháp P7 hoặc ngưỡng theo kết quả.',
      'previous_plan':{'path':'m1-execution-plan.json','sha256':hashlib.sha256((root/'m1-execution-plan.json').read_bytes()).hexdigest(),'status':'preserved; both planned cases canceled; no M1 output produced'},
      'observations':['Booking cgroup OOM in both C3 phases; they are not clean baseline windows',
                      'Original t=21:35 window also not used as a clean control per STEER #4'],
      'recovery_confirmed_utc':recovery['finished_utc'],'limits_after':recovery['limits'],
      'stability_rule':'Require no unexpected restart/cgroup OOM and all scheduled load responses 200 from recovery through 10 minute settling and normal method window; otherwise reject the clean-control interpretation and do not inject into an unstable system',
      'normal_start_rule':'ceil((recovery epoch + 600 seconds)/60)*60',
      'planned_cases':[{'opaque_id':'c12e47ab','operator_only_role':'normal after memory repair',
                        't':start+300,'method_bounds_utc':[stamp(start),stamp(start+600)],
                        'raw_bounds_utc':[stamp(start-300),stamp(start+900)]},
                       {'opaque_id':'f4a8c021','operator_only_role':'one reversible process pause',
                        'component':'event-service','reason_for_component':'All three fixed read paths reach event-service; do not pause the service with cyclic unexplained OOM',
                        'scheduled_not_before_epoch':start+960,'scheduled_not_before_utc':stamp(start+960),
                        't_rule':'floor actual confirmed intervention epoch_ns/1e9; only t crosses to request.json',
                        'duration_seconds':300}],
      'load_extension':{'start_utc':'2026-11-10T22:15:00Z','seconds':1200,'rate':1,
                        'output':'light-load-v2.jsonl','workers':64,
                        'note':'The original 21:15-22:15 run remains unchanged; separate continuous extension to 22:35'},
      'freeze_rule':'Wait until each raw upper bound plus export flush; full raw inputs immutable and hashed',
      'method_window_rule':'[t-300,t+300); unchanged P7 API and params; two identical repeat runs per pack',
      'interpretation':'One probe plus one control, not SPEC 3+1; feasibility only; no accuracy or RQ5 claims',
      'files_sha256':{name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in files}}
target.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'frozen':plan['frozen_utc'],'normal':plan['planned_cases'][0],'pause_not_before':plan['planned_cases'][1]['scheduled_not_before_utc']},ensure_ascii=False,indent=2))
