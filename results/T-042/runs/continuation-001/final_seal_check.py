"""Read-only postseal integrity, file set and exact prompt check; no output files."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path('D:/RCA-flashticket');OUT=ROOT/'results/T-042/runs/continuation-001'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def read(path):return json.loads(path.read_text(encoding='utf-8-sig'))
def block(text,heading):return text.split(heading,1)[1].split('```text',1)[1].split('```',1)[0].strip('\r\n')


def main():
    manifest=read(OUT/'manifest.json')
    expected={row['path'] for row in manifest['files']}
    actual={p.relative_to(ROOT).as_posix() for p in OUT.rglob('*') if p.is_file() and p!=OUT/'manifest.json'}
    assert expected==actual,(sorted(expected-actual),sorted(actual-expected))
    for row in manifest['files']:
        path=ROOT/row['path'];assert path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],row['path']
    for path,row in manifest['controls'].items():assert sha(ROOT/path)==row['sha256'],path
    old=read(ROOT/manifest['parent_manifest']['path']);assert sha(ROOT/manifest['parent_manifest']['path'])==manifest['parent_manifest']['sha256']
    for row in old['files']:assert sha(ROOT/row['path'])==row['sha256']
    initial=read(OUT/'initial-controls.json')
    for path in ['docs/WHY.md','docs/DECISIONS.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md']:
        meta=initial[path];assert hashlib.sha256((ROOT/path).read_bytes()[:meta['bytes']]).hexdigest()==meta['sha256']
    source=(ROOT/'docs/review-prompt.md').read_text(encoding='utf-8-sig');common=block(source,'## Prompt chung')
    prompt=(OUT/'prompt-claude.txt').read_text(encoding='utf-8-sig')
    prefix=common.split('Thông tin lượt này:',1)[0]
    suffix=common.split('\nKhông sửa ngoài phạm vi trên',1)[1]
    assert prompt.startswith(prefix) and '\nKhông sửa ngoài phạm vi trên'+suffix in prompt
    stage=block(source,'### Soát kết quả');gate=block(source,'### G2 — Baseline và phân tích hạn chế')
    assert prompt.endswith(stage+'\n\n'+gate+'\n')
    log=(ROOT/'tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md').read_text(encoding='utf-8-sig')
    assert log.endswith(prompt+'```\n')
    assert '**chờ phản biện**' in next(l for l in (ROOT/'docs/STATE.md').read_text(encoding='utf-8-sig').splitlines() if l.startswith('- **T-042 —'))
    audit=read(OUT/'state-row-change.json');assert audit['other_lines_equal']
    controlsrc=read(ROOT/'results/T-042/nguon.json');source_checks=0
    for row in controlsrc['checks']:
        path=Path(row['path'])
        if path.is_relative_to(ROOT/'src'):
            assert sha(path)==row['expected_sha256'];source_checks+=1
    result=subprocess.run(['git','diff','--check','--','docs/STATE.md','docs/WHY.md','docs/DECISIONS.md','tasks/T-042-doi-chieu-baseline-nezha-ob/LOG.md','results/T-042'],cwd=ROOT,capture_output=True,text=True)
    assert result.returncode==0,(result.stdout,result.stderr)
    total=sum(p.stat().st_size for p in (ROOT/'results/T-042').rglob('*') if p.is_file());assert total<300*2**20
    print(json.dumps(dict(status='PASS',new_files_excluding_manifest=len(expected),old_science_files_preserved=len(old['files']),shared_src_pins=source_checks,
                         controls_current=True,append_only_prefixes=True,prompt_common_stage_G2_exact=True,file_set_exact=True,
                         total_T042_bytes=total,total_T042_MiB=total/2**20,STATE='awaiting_review',accepted=False)))


if __name__=='__main__':main()
