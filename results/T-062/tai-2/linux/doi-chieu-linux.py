"""Compare saved Linux and PowerShell runs, without new traffic."""
import ast
import csv
import datetime as dt
import hashlib
import json
from pathlib import Path
import sys
import tai_linux as ctl

ROOT = Path(__file__).resolve().parent
TAGS = ['l1linux20261113a', 'l1linux20261113b', 'l1ps20261113a', 'l1ps20261113b']
ctl.verify_sources()
runs = {}
for tag in TAGS:
    root = ROOT / 'tai-out' / tag
    ctl.run([sys.executable, str(ROOT / 'linux-support/verify-outputs.py'), str(root)], label='independent verification')
    ctl.run([sys.executable, str(ROOT / 'linux-support/bang-buoc-tai.py'), str(root)], label='30s analysis')
    analysis = json.loads((root / 'analysis.json').read_text())
    bins = json.loads((root / 'buoc-tai.json').read_text())
    cfg = json.loads((root / 'cau-hinh.json').read_text())
    manifest = json.loads(ctl.source('linux-source-manifest.json'))
    sources = {n: ctl.digest(root / n) == manifest['files']['k6/' + n]['sha256']
               for n in ['hanh-trinh.js', 'cau-hinh.json']}
    assert all(sources.values())
    orders = list(analysis['orders'].values())
    purchases = [o for o in orders if o['journey'] == 'purchase']
    starts = []
    for line in (root / 'container.log').read_text().splitlines():
        index = line.find('{')
        if index < 0:
            continue
        try:
            v = json.loads(line[index:])
        except ValueError:
            continue
        if v.get('type') == 'journey_start':
            relative = dt.datetime.fromisoformat(v['utc'].replace('Z', '+00:00')).timestamp() - v['testEpochMs'] / 1000
            starts.append({'seconds': relative, 'scenario': v['scenario'], 'journey': v['journey']})
    runs[tag] = {'tag': tag, 'run': json.loads((root / 'run.json').read_text()),
                 'state': json.loads((root / 'state.json').read_text()),
                 'totals': {n: analysis['totals'].get(n, 0) for n in [
                     'journey_started', 'journey_finished', 'journey_failed', 'route_responses',
                     'http_reqs', 'gateway_401', 'dropped_iterations', 'token_refresh_success', 'token_refresh_failure']},
                 'mixMeasuredPercent': analysis['mixMeasuredPercent'],
                 'purchaseCount': len(purchases),
                 'purchaseCompleted': sum(o['states'][-1] == 'COMPLETED' for o in purchases),
                 'purchaseStateSequences': sorted({tuple(o['states']) for o in purchases}),
                 'getTicketsResponses': analysis['steps'].get('get_tickets', 0),
                 'gatewayMatched': sum(analysis['gateway']['matchedRoutes'].values()),
                 'gatewayMissing': len(analysis['gateway']['missing']),
                 'gatewayMismatches': len(analysis['gateway']['mismatches']),
                 'gatewayOutside': len(analysis['gateway']['extraRequests']),
                 'sourceMatchesRepo': sources, 'stages': bins['journeyStartsByScenario'],
                 'peakActiveByStage': bins['observedPeakActiveJourneysByScenario'],
                 'maxVUsPerScenario': cfg['maxVUs'],
                 'manifestFilesMatched': len(analysis['hashChecks']), 'routes': analysis['routes']}
    runs[tag]['arrivalBounds'] = {'firstSeconds': min(v['seconds'] for v in starts),
                                  'lastSeconds': max(v['seconds'] for v in starts),
                                  'startsNearEnd': [v for v in starts if v['seconds'] >= runs[tag]['run']['seconds'] - 0.1]}
    assert runs[tag]['gatewayMissing'] == 0 and runs[tag]['gatewayMismatches'] == 0
    assert runs[tag]['gatewayMatched'] == runs[tag]['totals']['route_responses']
    assert runs[tag]['purchaseCount'] == runs[tag]['purchaseCompleted']
    assert runs[tag]['getTicketsResponses'] == runs[tag]['purchaseCompleted']

pairs = []
for linux, ps in [('l1linux20261113a', 'l1ps20261113a'), ('l1linux20261113b', 'l1ps20261113b')]:
    left, right = runs[linux], runs[ps]
    assert left['run'] == right['run']
    keys = ['journey_started', 'journey_finished', 'journey_failed', 'gateway_401', 'dropped_iterations',
            'token_refresh_failure', 'route_responses', 'http_reqs', 'token_refresh_success']
    differences = {k: left['totals'][k] - right['totals'][k] for k in keys}
    routes = {route: {'linux': left['routes'].get(route, 0), 'powershell': right['routes'].get(route, 0),
                      'difference': left['routes'].get(route, 0) - right['routes'].get(route, 0)}
              for route in sorted(set(left['routes']) | set(right['routes']))}
    pairs.append({'linux': linux, 'powershell': ps, 'runConfigEqual': True,
                  'differencesLinuxMinusPowerShell': differences, 'routes': routes})

def functions(path):
    tree = ast.parse(path.read_text())
    return {v.name: ast.dump(v, include_attributes=False) for v in tree.body if isinstance(v, ast.FunctionDef)}

final_functions = functions(ROOT / 'tai_linux.py')
lineage = {}
for version in ['v1', 'v2']:
    old = functions(ROOT / ('tai_linux-' + version + '.py'))
    lineage[version] = {n: old[n] == final_functions[n] for n in old.keys() & final_functions.keys()}
    for name in ['start', 'preflight', 'renew_tokens', 'get', 'token_status', 'verify_sources']:
        assert lineage[version][name]

result = {'utc': ctl.utc(), 'runs': runs, 'pairs': pairs,
          'sourceLineageFunctionsUnchanged': lineage,
          'controllerSha256': ctl.digest(ROOT / 'tai_linux.py'),
          'sourceManifestSha256': ctl.digest(ROOT / 'linux-source-manifest.json')}
(ROOT / 'linux-check/comparison.json').write_text(json.dumps(result, indent=2) + '\n')
with (ROOT / 'linux-check/comparison-routes.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['linux', 'powershell', 'route', 'linux_requests', 'powershell_requests', 'difference'])
    for p in pairs:
        for route, counts in p['routes'].items():
            writer.writerow([p['linux'], p['powershell'], route, counts['linux'], counts['powershell'], counts['difference']])
print(json.dumps({'ok': True, 'pairs': pairs, 'runs': {n: {k: v[k] for k in (
    'totals', 'purchaseCompleted', 'gatewayMatched', 'gatewayOutside', 'stages', 'peakActiveByStage')} for n, v in runs.items()}}))
