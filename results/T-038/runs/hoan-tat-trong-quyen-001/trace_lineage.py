"""Tra metadata công khai; không fetch blob/code/image hoặc telemetry."""
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import time
import urllib.request

ROOT=Path(__file__).resolve().parents[4]
RUN=Path(__file__).resolve().parent/'lineage'
RUN.mkdir(exist_ok=False)
requests=[]


def get(url,name):
    start=time.monotonic()
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'T038-metadata-only','Accept':'application/json'})
        with urllib.request.urlopen(req,timeout=30) as response:
            body=response.read();status=response.status
        value=json.loads(body)
        # Metadata response only. No /contents or /git/blobs calls.
        (RUN/name).write_bytes(body)
        requests.append(dict(url=url,status=status,bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),saved=name,elapsed_seconds=time.monotonic()-start))
        return value
    except Exception as e:
        requests.append(dict(url=url,error=repr(e),elapsed_seconds=time.monotonic()-start))
        return None


summaries=[]
for revision in ['259ea4167160256a74ad30004aa3d96a998c846e','www25','ase24']:
    commit=get('https://api.github.com/repos/phamquiluan/RCAEval/git/commits/'+revision,revision+'-commit-metadata.json')
    if not commit:continue
    tree=get('https://api.github.com/repos/phamquiluan/RCAEval/git/trees/'+commit['tree']['sha']+'?recursive=1',revision+'-tree-metadata.json')
    if not tree:continue
    paths=[x for x in tree['tree'] if re.search(r'deploy|docker|kubernetes|helm|collector|jaeger|train.ticket|instrument|otel',x['path'],re.I)]
    summaries.append(dict(axis='RCAEval repository metadata',requested=revision,commit=commit['sha'],tree=commit['tree']['sha'],truncated=tree.get('truncated'),tree_entries=len(tree['tree']),candidate_paths=paths,code_blobs_opened=False,
        interpretation='Candidate paths only; absence of keyword is not proof that source provenance cannot exist. No application build identity inferred from this commit.'))

for key,url in [('zenodo','https://zenodo.org/api/records/14590730'),('figshare','https://api.figshare.com/v2/articles/31048672')]:
    value=get(url,key+'-record-metadata.json')
    if value:
        desc=value.get('metadata',{}).get('description') if key=='zenodo' else value.get('description')
        summaries.append(dict(axis='publication archive metadata',source=key,url=url,description=desc,
            files=[dict(name=x.get('key',x.get('name')),bytes=x.get('size'),checksum=x.get('checksum',x.get('computed_md5'))) for x in value.get('files',[])],
            related_identifiers=value.get('metadata',{}).get('related_identifiers',[]),links=value.get('links',{}),telemetry_files_opened=False,
            interpretation='Record/catalogue only, no download URLs followed. No identity from archive dataset version to app build without explicit link.'))

for name,value in [('requests.json',requests),('metadata-findings.json',summaries)]:
    (RUN/name).write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(request_count=len(requests),received_bytes=sum(r.get('bytes',0) for r in requests),failures=sum('error' in r for r in requests),candidate_counts=[dict(revision=r['requested'],count=len(r['candidate_paths'])) for r in summaries if 'requested' in r],telemetry_or_code_download=False),ensure_ascii=False))
