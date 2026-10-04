"""Snapshot current IT metadata only; never request archive or telemetry payload."""
import argparse
import hashlib
import json
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
OLD = BASE / 'runs/run-001'

def dump(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='source-final-001')
    parser.add_argument('--verify', action='store_true')
    parser.add_argument('--discussion-followup', action='store_true')
    parser.add_argument('--license-terms', action='store_true')
    args = parser.parse_args()
    run = BASE / 'runs' / args.run
    if args.verify:
        manifest = json.loads((run/'manifest.json').read_text(encoding='utf-8'))
        for item in manifest['sources']:
            if 'path' in item:
                b = (run/item['path']).read_bytes()
                assert len(b) == item['bytes'] and hashlib.sha256(b).hexdigest() == item['sha256']
        print('PASS snapshot bytes/hash', len(manifest['sources']))
        return
    (run/'sources').mkdir(parents=True, exist_ok=False)
    start = time.monotonic()
    manifest = {'started_utc':datetime.now(timezone.utc).isoformat(), 'scope':'IT metadata, source code README/LICENSE and issue metadata only; no archive or telemetry', 'sources':[]}
    def fetch(name, url):
        item = {'name':name,'url':url,'requested_utc':datetime.now(timezone.utc).isoformat()}
        manifest['sources'].append(item)
        try:
            request = urllib.request.Request(url, headers={'User-Agent':'RCA-source-verification/1'})
            with urllib.request.urlopen(request, timeout=25) as r:
                data = r.read(4_000_001)
                assert len(data) <= 4_000_000
                item.update(status=r.status, final_url=r.url, link_header=r.headers.get('Link'))
            (run/'sources'/name).write_bytes(data)
            item.update(path='sources/'+name, bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
            return data
        except Exception as exc:
            item['error'] = str(exc)
            return None
        finally:
            dump(run/'manifest.json',manifest)
            print(name, item.get('bytes',item.get('error')),flush=True)
    old = json.loads((OLD/'manifest.json').read_text(encoding='utf-8'))
    if args.license_terms:
        for variant in ('by-nc','by-nd'):
            fetch('cc-'+variant+'-4.0.html',f'https://creativecommons.org/licenses/{variant}/4.0/legalcode.en')
        manifest.update(elapsed_seconds=round(time.monotonic()-start,3), downloaded_bytes=sum(x.get('bytes',0) for x in manifest['sources']))
        dump(run/'manifest.json',manifest)
        return
    if args.discussion_followup:
        for name, numbers in {'Product_Review_Original':[1], 'Product_Review_Preprocessed':[1], 'Cloud_Computing_Original':[1], 'Cloud_Computing_Preprocessed':[1,2]}.items():
            for number in numbers:
                fetch(f'{name}__discussion-{number}.json', f'https://huggingface.co/api/datasets/Lemma-RCA-NEC/{name}/discussions/{number}')
        manifest.update(elapsed_seconds=round(time.monotonic()-start,3), downloaded_bytes=sum(x.get('bytes',0) for x in manifest['sources']))
        dump(run/'manifest.json',manifest)
        return
    comparison = {'datasets':{}, 'telemetry_archives_downloaded':0,'telemetry_cases_inspected':0}
    for name, rev in old['dataset_revisions'].items():
        prefix = 'https://huggingface.co/api/datasets/Lemma-RCA-NEC/'+name
        info = json.loads(fetch(name+'__current-info.json',prefix))
        current = info['sha']
        readme = fetch(name+'__README.md',f'https://huggingface.co/datasets/Lemma-RCA-NEC/{name}/raw/{current}/README.md')
        tree = json.loads(fetch(name+'__tree.json',prefix+f'/tree/{current}?recursive=true&limit=1000'))
        fetch(name+'__commits.json',prefix+'/commits/main')
        fetch(name+'__discussions.json',prefix+'/discussions')
        oldtree = json.loads((OLD/'sources'/(name+'__tree.json')).read_text(encoding='utf-8'))
        fields = lambda xs: sorted((x['path'],x.get('size'),x.get('oid'),x.get('lfs',{}).get('oid')) for x in xs if x['type']=='file')
        comparison['datasets'][name] = {'old_revision':rev,'current_revision':current,'same_revision':rev==current,'same_file_inventory':fields(tree)==fields(oldtree),'same_readme_bytes':readme==(OLD/'sources'/(name+'__README.md')).read_bytes(),'license_frontmatter':info.get('cardData',{}).get('license'),'license_body_nd':b'cc-by-nd-4.0' in readme.lower(),'archive_files':sum(x['path'].endswith('.zip') for x in tree),'archive_bytes':sum(x.get('size',0) for x in tree if x['path'].endswith('.zip'))}
    commit = json.loads(fetch('github-head.json','https://api.github.com/repos/lemma-rca/rca_baselines/commits/main'))
    rev = commit['sha']
    comparison['github'] = {'old_revision':old['github_revision'],'current_revision':rev,'same_revision':rev==old['github_revision']}
    for path in ['README.md','LICENSE']:
        fetch('code__'+path, f'https://raw.githubusercontent.com/lemma-rca/rca_baselines/{rev}/{path}')
    fetch('github-issues-all.json','https://api.github.com/repos/lemma-rca/rca_baselines/issues?state=all&per_page=100')
    fetch('paper-abs.html','https://arxiv.org/abs/2406.05375')
    fetch('author-current-site.html','https://www.lemmarca.info/')
    fetch('author-site.html','https://lemma-rca.github.io/')
    fetch('author-catalog.html','https://lemma-rca.github.io/docs/data.html')
    manifest.update(elapsed_seconds=round(time.monotonic()-start,3), downloaded_bytes=sum(x.get('bytes',0) for x in manifest['sources']))
    dump(run/'manifest.json',manifest)
    dump(run/'comparison.json',comparison)

if __name__ == '__main__':
    main()
