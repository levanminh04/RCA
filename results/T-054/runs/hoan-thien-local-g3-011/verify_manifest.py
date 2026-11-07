"""Verify checkpoint011 without creating files or opening source signals."""
from pathlib import Path
import hashlib
import json

ROOT=Path(__file__).resolve().parents[4]
path=ROOT/'results/T-054/manifest-hoan-thien-local-g3-011.json'
manifest=json.loads(path.read_bytes())
count=0
for group in ['outputs','mutable_current']:
    for rel,pin in manifest[group].items():
        p=ROOT/rel
        assert p.stat().st_size==pin['bytes'],rel
        assert hashlib.sha256(p.read_bytes()).hexdigest()==pin['sha256'],rel
        count+=1
print(json.dumps({'PASS':True,'checked':count,'groups':{k:len(manifest[k])for k in ['outputs','mutable_current']},
                  'main_started':manifest['main_started'],'cloud_checked':manifest['cloud_checked']}))
