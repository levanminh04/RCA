"""Pin the already used upstream code and four local environment patches; no data I/O."""
import json
from pathlib import Path
import subprocess
from activate import ROOT,RUN,pin
from bien_nhan import atomic,digest,read_pin,ref


def main():
    files={}
    upstream=read_pin(pin(RUN/'upstream-pins.json'))
    base=Path('D:/RCA-ext/src/RCAEval')
    for rel,meta in upstream['files'].items():
        path=base/rel
        assert path.stat().st_size==meta['bytes'] and digest(path)==meta['sha256']
        files[str(path)]=ref(path)
    circa=Path('D:/RCA-ext/work/T-014/CIRCA')
    revision=subprocess.check_output(['git','-C',str(circa),'rev-parse','HEAD'],text=True).strip()
    assert revision=='0215e1880096aa02a305c697f1c23cac4600ebd2'
    subprocess.run(['git','-C',str(circa),'diff','--quiet','HEAD'],check=True)
    for rel in subprocess.check_output(['git','-C',str(circa),'ls-files','circa'],text=True).splitlines():
        if rel.endswith('.py'):
            path=circa/rel;files[str(path)]=ref(path)
    patches=read_pin(pin(RUN/'environment-patches.json'))['patches']
    for rel,meta in patches.items():
        path=Path('D:/RCA-ext/envs/py38-rcdlock/Lib/site-packages')/rel
        assert digest(path)==meta['sha256'];files[str(path)]=ref(path)
    atomic(RUN/'local-external-code-pins.json',dict(files=files,upstream_RCAEval_revision=upstream['revision'],
           CIRCA_revision=revision,scope='already used external source and environment patch files, no method rerun'))
    print(json.dumps(dict(PASS=True,files=len(files))))


if __name__=='__main__':main()
