from pathlib import Path
import json, hashlib
from pypdf import PdfReader

ROOT=Path('D:/RCA-flashticket')
OUT=ROOT/'results/T-020/trung-gian/dataset_evidence'
source='results/T-008/sources/FSE2023_Nezha.pdf'
paper=ROOT/source
reader=PdfReader(paper)
pages=[{'page':i+1,'text':p.extract_text()} for i,p in enumerate(reader.pages)]
(OUT/'nezha-paper-text.json').write_text(json.dumps({'source':source,'sha256':hashlib.sha256(paper.read_bytes()).hexdigest(),'pages':pages},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for p in pages:
    lines=p['text'].splitlines()
    for i,s in enumerate(lines):
        if any(k.lower() in s.lower() for k in ['Byteman','Hypno','Failpoint','Tempo','Promtail','Collector','Node Exporter']):
            print('page',p['page'], 'lines',i+1,' '.join(lines[max(0,i-1):i+3]))
