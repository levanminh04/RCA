"""Modify only the T019 byte range while holding an OS file lock on Windows."""
import argparse, hashlib, json, msvcrt, pathlib, time, sys
from acquire import ROOT, OUT, dump

def main():
    sys.stdout.reconfigure(encoding='utf-8')
    a=argparse.ArgumentParser();a.add_argument('mode',choices=['start','finish']);n=a.parse_args()
    path=ROOT/'docs/STATE.md'; audit=OUT/('state-'+n.mode+'.json')
    with path.open('r+b',buffering=0) as f:
        f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1048576)
        try:
            f.seek(0);before=f.read();newline=b'\r\n' if b'\r\n' in before else b'\n'
            lines=before.splitlines(keepends=True);found=[i for i,x in enumerate(lines) if x.startswith(b'| T-019 |')]
            assert len(found)<=1
            status='đang làm (04/10/2026)' if n.mode=='start' else 'chờ phản biện (04/10/2026)'
            new=('| T-019 | Thẻ Sock Shop RCAEval | P2 | Codex | Claude | '+status+' | `tasks/T-019-the-sock-shop/` |').encode()+newline
            if found:
                i=found[0];offset=sum(map(len,lines[:i]));old=lines[i];tail=before[offset+len(old):]
            else:
                assert n.mode=='start'
                heading=next(i for i,x in enumerate(lines) if x.startswith('## Mục lục task'.encode()))
                indexes=[i for i,x in enumerate(lines) if i>heading and x.startswith(b'|')]
                i=max(indexes)+1;offset=sum(map(len,lines[:i]));old=b'';tail=before[offset:]
            # Prefix is never rewritten. The old suffix is shifted only to replace the row.
            f.seek(offset);f.write(new+tail);f.truncate(offset+len(new)+len(tail));f.flush()
            f.seek(0);after=f.read();assert after==before[:offset]+new+tail
            assert after[:offset]+after[offset+len(new):]==before[:offset]+before[offset+len(old):]
            dump(audit,{'mode':n.mode,'before_sha256':hashlib.sha256(before).hexdigest(),'after_sha256':hashlib.sha256(after).hexdigest(),'old_row':old.decode(),'new_row':new.decode(),'other_bytes_preserved':True,'prefix_bytes_not_written':offset})
            print(new.decode().strip(),'other bytes preserved')
        finally:
            f.seek(0);msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1048576)

if __name__=='__main__':main()
