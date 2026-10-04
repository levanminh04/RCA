"""Update only T-015 byte span, keeping all other bytes; fail on a concurrent edit."""
import hashlib,json,pathlib,sys
sys.stdout.reconfigure(encoding='utf-8')

ROOT=pathlib.Path(__file__).resolve().parents[3]

def main():
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('status'); a=ap.parse_args()
    p=ROOT/'docs/STATE.md'; original=p.read_bytes()
    lines=original.splitlines(keepends=True)
    newline=b'\r\n' if b'\r\n' in original else b'\n'
    indexes=[i for i,l in enumerate(lines) if l.startswith(b'| T-015 |')]
    new=('| T-015 | Hồ sơ MicroRank, TraceRCA và detector trace | P1 | Codex | Claude | '+a.status+' | `tasks/T-015-ho-so-microrank/` |').encode()+newline
    if indexes:
        assert len(indexes)==1
        i=indexes[0]; start=sum(map(len,lines[:i])); old=lines[i]; tail=b''.join(lines[i+1:])
    else:
        table=original.index('## Mục lục task'.encode())
        last=max(i for i,l in enumerate(lines) if l.startswith(b'| T-') and sum(map(len,lines[:i]))>table)
        start=sum(map(len,lines[:last+1])); old=b''; tail=original[start:]
    assert p.read_bytes()==original,'STATE changed concurrently; reread'
    with p.open('r+b') as f:
        f.seek(start); f.write(new+tail); f.truncate()
    after=p.read_bytes()
    assert after[:start]==original[:start]
    assert after[start+len(new):]==original[start+len(old):]
    record={'status':a.status,'before_sha256':hashlib.sha256(original).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'outside_t015_bytes_identical':True,'old_line':old.decode().strip(),'new_line':new.decode().strip()}
    out=ROOT/'results/T-015/runs/state-changes.jsonl'
    with out.open('a',encoding='utf-8') as f: f.write(json.dumps(record,ensure_ascii=False)+'\n')
    print(json.dumps(record,ensure_ascii=False))

if __name__=='__main__':main()
