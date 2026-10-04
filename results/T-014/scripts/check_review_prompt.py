"""Independently match every literal span of the governing review template."""
from pathlib import Path
import re,json
repo=Path('D:/RCA-flashticket');out=repo/'results/T-014'
template=(repo/'docs/review-prompt.md').read_text(encoding='utf-8-sig')
common=re.search(r'## Prompt chung.*?```text\n(.*?)\n```',template,re.S).group(1)
g1=re.search(r'\*\*G1 — phương pháp, dataset, cách chia:\*\*\n```text\n(.*?)\n```',template,re.S).group(1)
log=(repo/'tasks/T-014-ho-so-circa/LOG.md').read_text(encoding='utf-8-sig')
payload=log.rsplit('## Prompt phản biện cho Claude',1)[1]
payload=re.search(r'```text\n(.*?)\n```',payload,re.S).group(1)
parts=re.split(r'(<[^>]+>)',common)
pattern=''.join('(.*?)' if p.startswith('<') else re.escape(p) for p in parts)
match=re.fullmatch(pattern+'\n\n'+re.escape(g1),payload,re.S)
report=dict(pass_=match is not None,common_literal_spans_unchanged=match is not None,G1_block_unchanged=payload.endswith(g1),placeholders=[p for p in parts if p.startswith('<')],scope='Only neutral placeholder substitution is permitted; no task findings inserted into fixed prompt.')
(out/'runs/review-prompt-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=True));assert report['pass_']
