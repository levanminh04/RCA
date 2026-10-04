"""Capture only small primary-source metadata and documentation, with byte cap."""
import hashlib,json,urllib.request
from pathlib import Path
from datetime import datetime,timezone
BASE=Path(__file__).resolve().parent
OUT=BASE/'snapshots'; OUT.mkdir(exist_ok=True)
manifest=[]; total=0
HF='afeacb11bcc94dadfd1c8f483ee4377b2b8b614e'
RCA='259ea4167160256a74ad30004aa3d96a998c846e'
def get(name,url,revision=None,limit=1000000):
    global total
    req=urllib.request.Request(url,headers={'User-Agent':'RCA-T019-source-audit/1.0'})
    entry=dict(artifact=str((OUT/name).relative_to(BASE)),url=url,revision=revision,requested_at_utc=datetime.now(timezone.utc).isoformat())
    try:
        with urllib.request.urlopen(req,timeout=45) as response:
            body=response.read(min(limit,3000000-total)+1)
            total+=len(body)
            entry.update(bytes=len(body),sha256=hashlib.sha256(body).hexdigest(),status=response.status,resolved_url=response.geturl())
            (OUT/name).write_bytes(body)
            if len(body)>limit or total>3000000: raise RuntimeError('source-byte-cap-exceeded')
        return body
    except Exception as e:
        entry['error']=repr(e)
        raise
    finally:
        manifest.append(entry)
        (BASE/'network-manifest.json').write_text(json.dumps(dict(total_bytes=total,entries=manifest),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

info=json.loads(get('hf-info.json','https://huggingface.co/api/datasets/phamquiluan/RCAEval'))
get('hf-pinned-info.json',f'https://huggingface.co/api/datasets/phamquiluan/RCAEval/revision/{HF}',HF)
get('rcaeval-tree.json',f'https://api.github.com/repos/phamquiluan/RCAEval/git/trees/{RCA}?recursive=1',RCA)
sock=json.loads(get('sock-shop-repository.json','https://api.github.com/repos/microservices-demo/microservices-demo'))
sha=json.loads(get('sock-shop-commit.json',f"https://api.github.com/repos/microservices-demo/microservices-demo/commits/{sock['default_branch']}"))['sha']
get('sock-shop-tree.json',f'https://api.github.com/repos/microservices-demo/microservices-demo/git/trees/{sha}?recursive=1',sha)
get('sock-shop-README.md',f'https://raw.githubusercontent.com/microservices-demo/microservices-demo/{sha}/README.md',sha)
print(json.dumps(dict(total_bytes=total,hf_head=info['sha'],sock_shop_revision=sha),indent=2))
