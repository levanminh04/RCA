"""Freeze selected MIT functions, sources and allowed dev inventory, without editing shared clones."""
import ast, hashlib, json, pathlib, subprocess

ROOT = pathlib.Path(__file__).resolve().parents[3]
OUT = ROOT / 'results/T-015'
MK = pathlib.Path('C:/Users/84583/AppData/Local/Temp/claude/D--RCA-flashticket/faa9e437-da55-49ba-b763-6e8484c8c9a6/scratchpad/ext/MicroRank')
TR = MK.parent / 'TraceRCA'
RE = pathlib.Path('D:/RCA-ext/src/RCAEval')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    manifest = {'sources': [], 'dev_cases': []}
    for repo, expected in [(MK,'efd85e8e6f0fad30f6f8aaf0555e3324d8f5f982'),(TR,'b9087c72d201fbb17d724114cd389de4854815ad'),(RE,'259ea4167160256a74ad30004aa3d96a998c846e')]:
        actual = subprocess.check_output(['git','-C',str(repo),'rev-parse','HEAD'],text=True).strip()
        assert actual == expected, (repo,actual)
        manifest['sources'].append({'repo':str(repo),'revision':actual,'clean':not subprocess.check_output(['git','-C',str(repo),'status','--porcelain'],text=True).strip()})
    dest = ROOT / 'src/microrank'
    dest.mkdir(parents=True,exist_ok=True)
    text = '# MIT code extracted verbatim from IntelligentDDS/MicroRank; see PROVENANCE.json.\nimport numpy as np\nimport math\n\n'
    funcs=[]
    for rel,names in [('pagerank.py',['pageRank','trace_pagerank']),('online_rca.py',['calculate_spectrum_without_delay_list'])]:
        p=MK/rel; s=p.read_text(encoding='utf-8'); tree=ast.parse(s)
        for n in tree.body:
            if isinstance(n,ast.FunctionDef) and n.name in names:
                text += ast.get_source_segment(s,n)+'\n\n'
                funcs.append({'function':n.name,'source':str(p),'line':n.lineno,'end_line':n.end_lineno,'source_sha256':sha(p)})
    (dest/'official.py').write_text(text,encoding='utf-8')
    licence=next(p for p in MK.iterdir() if p.name.lower().startswith('license'))
    (dest/'LICENSE').write_bytes(licence.read_bytes())
    (dest/'PROVENANCE.json').write_text(json.dumps({'revision':manifest['sources'][0]['revision'],'functions':funcs,'sha256':sha(dest/'official.py')},ensure_ascii=False,indent=2),encoding='utf-8')
    for p in sorted((ROOT/'data/rcaeval').glob('re2tt_*')):
        assert p.is_dir()
        manifest['dev_cases'].append({'case':p.name,'files':{f.name:{'bytes':f.stat().st_size,'sha256':sha(f)} for f in p.iterdir() if f.name in ['traces.parquet','inject_time.txt','metrics.parquet']}})
    assert len(manifest['dev_cases'])==30
    manifest['paper']={'path':str(MK/'WWW2021_MicroRank.pdf'),'sha256':sha(MK/'WWW2021_MicroRank.pdf')}
    for p in sorted((ROOT/'results/T-007/runs/py312-pin').glob('*.tar.gz')):
        if p.name.startswith(('microrank','tracerca')):
            manifest.setdefault('reused',[]).append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
    (OUT/'manifest-inputs.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'dev_cases':30,'functions':len(funcs),'official_sha256':sha(dest/'official.py')}))

if __name__=='__main__': main()
