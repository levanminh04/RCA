from pathlib import Path
import hashlib, json
import pypdf
import pypdfium2 as pdfium

root = Path('D:/RCA-ext/work/T-017')
out = Path('D:/RCA-flashticket/results/T-017/sources')
out.mkdir(parents=True, exist_ok=True)
manifest = []
for name, path in [('arxiv-v2', root/'2510.04711v2.pdf'), ('fse26', root/'sources-audit/fang2026rethinking-fse.pdf')]:
    reader = pypdf.PdfReader(path)
    texts = [p.extract_text(extraction_mode='layout') for p in reader.pages]
    (out/f'{name}-pages.txt').write_text('\n\n'.join(f'=== PDF PAGE {i+1} ===\n{x}' for i,x in enumerate(texts)), encoding='utf-8')
    pdf = pdfium.PdfDocument(str(path))
    rendered = []
    for i, text in enumerate(texts):
        if 'Table 2.' in text or 'Table 3.' in text:
            image_path = root/f'{name}-page-{i+1}.png'
            pdf[i].render(scale=1.8).to_pil().save(image_path)
            rendered.append(str(image_path))
    manifest.append({'name':name,'path':str(path),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'pages':len(texts),'table_images':rendered})
(out/'pdf-manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
print(json.dumps(manifest,indent=2))
