"""Final evidence checks on delivered files, without rerunning experiments."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
read=lambda name:json.loads((root/name).read_text(encoding='utf8'))
checks={}
manifest=read('manifest-digest.json'); plan=read('m1-execution-plan-v2.json')
checks['eight_arm_images']=len(manifest['services'])==8 and all(s['architecture']=='arm64' for s in manifest['services'])
checks['frozen_v2_code_hashes']=all(hashlib.sha256((root/name).read_bytes()).hexdigest()==sha for name,sha in plan['files_sha256'].items())
pins=read('m1-source-pins.json')['pins']
checks['protected_local_39_source_pins']=len(pins)==39 and all(hashlib.sha256((Path('D:/RCA-flashticket')/name).read_bytes()).hexdigest()==sha for name,sha in pins.items())
app=read('runtime-app.json'); obs=read('runtime-obs.json')
apps=[c for c in app['containers'] if c['requested_image'].startswith('ft-local/')]
checks['eight_jvms_running_unpaused']=len(apps)==8 and all(c['running'] and not c['paused'] for c in apps)
checks['required_jvm_flags']=all('-XX:MaxRAMPercentage=50.0' in c['safe_settings']['JAVA_TOOL_OPTIONS'] and '-Duser.timezone=UTC' in c['safe_settings']['JAVA_TOOL_OPTIONS'] for c in apps)
checks['service_env_modes_600']=all(mode=='0o600' for mode in app['private_file_modes'].values())
checks['backend_five_running']=sum(c['running'] for c in obs['containers'])==5
config_checks=[]
for role,data,prefix in [('app',app,'/opt/flash-ticket-app/'),('obs',obs,'/opt/flash-ticket-obs/pinned/')]:
 for source,meta in data['files'].items():
  path=root/'config-public'/role/source.removeprefix(prefix)
  config_checks.append(path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest()==meta['sha256'])
checks['public_config_matches_final_runtime']=all(config_checks)
smoke=read('smoke-api-final.json')
checks['final_api_smoke']=smoke['idempotency_same_order'] and all(c['status'] in [200,201] for c in smoke['checks'])
verify=read('verify-app-final.json')
checks['issuer_and_eureka']=verify['issuer_matches'] and len(verify['eureka'])==6 and all(i['status']=='UP' for a in verify['eureka'] for i in a['instances'])
details=read('m1-feasibility-details.json')
checks['two_repeatable_contract_valid_runs']=all(d['status']=='OK' and d['deterministic_repeat'] and d['source_pins_checked']==39 for d in details.values())
checks['known_target_channel_gap_preserved']=details['f4a8c021']['diagnostics']['NO_VALID_CHANNEL']==['event-service'] and details['f4a8c021']['returned']==16
checks['two_export_scans_passed']=all(read('export-audit-'+id+'.json')['passed'] for id in details)
resource=read('so-do-tai-nguyen.json')
checks['both_failed_c3_windows_preserved']=all(not w['stability_passed'] and len(w['kernel_oom_events'])==1 for w in resource['hosts']['app']['windows'].values())
checks['load_complete_4800']=read('load-impact.json')['sequence_complete_0_to_4799']
checks['operator_jobs_stopped']=not read('final-ops-app.json')['active_job_processes'] and not read('final-ops-obs.json')['active_job_processes']
checks['tunnel_final_http200']=read('tunnel-check-final.json')['gateway_http']==200 and read('tunnel-check-final.json')['grafana_http']==200
report={'checks':checks,'all_passed':all(checks.values()),
        'scope':'Evidence consistency and requested operating constraints; not scientific acceptance of C1-C4',
        'scientific_open':['Redis spans absent','C3 cgroup OOM and no controlled agent overhead comparison',
                           'Pause target lacks valid A channels','Tempo/Loki API reader incomplete',
                           'R01-R10 coverage and full SPEC 3+1 not established'],
        'protected_repos_note':'Final tracked status is not clean: RCA DECISIONS/STATE are modified; this run issued read-only commands there and does not infer a clean-tree baseline'}
(root/'self-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['all_passed']: raise SystemExit('Final consistency check failed')
