"""Read-only final provisioning hashes; no environment or credential reads."""
import pathlib,hashlib,json,datetime,subprocess
B=pathlib.Path('/opt/flash-ticket-obs/pinned')
assert not (pathlib.Path.home()/'rca-dieu-phoi/STOP').exists(), 'STOP remote'
files={}
for p in [B/'compose.json',*sorted((B/'provisioning/dashboards').rglob('*'))]:
    if p.is_file(): files[str(p)]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
print(json.dumps({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'files':files,'restart_count':subprocess.check_output(['docker','inspect','--format','{{.RestartCount}}','flash-ticket-obs-grafana'],text=True).strip(),'started_at':subprocess.check_output(['docker','inspect','--format','{{.State.StartedAt}}','flash-ticket-obs-grafana'],text=True).strip()}))
