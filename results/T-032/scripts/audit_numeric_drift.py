"""Inspect already-retained diagnostic records; never execute MicroRank."""
import collections
import math
from pathlib import Path
import replay_microrank as r
H=Path('/home/ubuntu/rca/T-032')
O=H/'runs/microrank-numeric-audit-001'
r.new_directory(O)
D=H/'runs/microrank-native-diagnostic-001'
old=H/'runs/re2-ok-001'
audit=[]
entry,frozen,index,hashes=r.source_for('RE2-TT','dev-12a1a88069',audit)
check=r.read(D/'check.json')
for folder,manifest in [(D,check),(old,r.read(old/'check.json'))]:
    for row in manifest['artifact_manifest']:
        assert r.sha(folder/row['path'])==row['sha256'],row['path']
native=r.read(D/'ban-ghi-0.json')
observed=r.read(old/'ban-ghi-0.json')
diff=r.compare_records(frozen,native)
assert diff==check['native_vs_frozen']['differences']
assert not r.compare_records(observed,native)
numeric=[x for x in diff if x['kind']=='float_exact']
rows=[]
for x in numeric:
    a,b=x['expected'],x['actual']
    assert math.isfinite(a) and math.isfinite(b)
    rows.append({'pointer':x['pointer'],'absolute':abs(a-b),
                 'relative_to_larger_magnitude':abs(a-b)/max(abs(a),abs(b)) if max(abs(a),abs(b)) else None,
                 'ulps_at_expected':abs(a-b)/math.ulp(a)})
result={'status':'DIAGNOSTIC_RECORD_AUDIT_ONLY','method_executed':False,'eligible_for_mechanism':False,
        'frozen_path':entry['path'],'frozen_sha256':entry['sha256'],
        'native_check_sha256':r.sha(D/'check.json'),'observed_check_sha256':r.sha(old/'check.json'),
        'difference_count':len(diff),'float_exact_count':len(numeric),'other_difference_count':len(diff)-len(numeric),
        'native_observed_exact':True,'by_top_field':dict(collections.Counter(x['pointer'].split('/')[1] for x in diff)),
        'max_absolute':max((x['absolute'] for x in rows),default=0),
        'max_relative_to_larger_magnitude':max((x['relative_to_larger_magnitude'] or 0 for x in rows),default=0),
        'max_ulps_at_expected':max((x['ulps_at_expected'] for x in rows),default=0),
        'rows':rows,'limits':'Describes existing drift only. No platform cause identified, no tolerance chosen, no permission to resume or run A-prime.'}
r.dump(O/'audit.json',result)
r.dump(O/'source-checks.json',{'checks':audit})
r.dump(O/'manifest.json',{'files':r.artifact_manifest(O)})
print({k:v for k,v in result.items() if k not in ('rows',)},flush=True)
