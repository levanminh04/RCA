"""Nối số báo cáo tới JSON; V8 kiểm độc lập từng giá trị và số ngoài dấu."""
import json
from pathlib import Path
from resume_step7 import ROOT, OUT, read, sha, log, write

def pointer(doc, ptr):
    for k in ptr.lstrip('/').split('/') if ptr else []:
        k=k.replace('~1','/').replace('~0','~')
        doc=doc[int(k)] if isinstance(doc,list) else doc[k]
    return doc
def esc(s): return str(s).replace('~','~0').replace('/','~1')
def fmt(value, spec):
    if value is None: return 'N/A'
    if isinstance(value,bool): return 'Đúng' if value else 'Sai'
    if spec=='str': return str(value)
    return format(value,spec)

class Report:
    def __init__(self,name,run):
        self.name=name; self.run=Path(run); self.bindings=[]; self.cache={}
    def num(self,path,ptr='',spec='.6g'):
        path=str(path).replace('\\','/')
        if path not in self.cache:self.cache[path]=read(ROOT/path)
        value=pointer(self.cache[path],ptr); rendered=fmt(value,spec)
        key=str(len(self.bindings))
        self.bindings.append({'id':key,'path':path,'pointer':ptr,'format':spec,'rendered':rendered})
        return '<!--v8:'+key+'-->'+rendered+'<!--/v8-->'
    def save(self,text):
        self.run.mkdir(parents=True,exist_ok=True)
        target=OUT/self.name
        assert not target.exists(),target
        preface='Nguồn từng số và con trỏ JSON: ['+self.name+' — bảng nguồn]('+self.run.relative_to(OUT).as_posix()+'/'+self.name+'.bindings.json). Dấu nguồn ẩn trong bản Markdown để V8 kiểm từng lần xuất hiện.\n\n'
        target.write_text(preface+text.rstrip()+'\n',encoding='utf-8')
        log('Ghi '+target.relative_to(ROOT).as_posix())
        write(self.run/(self.name+'.bindings.json'),{'report':target.relative_to(ROOT).as_posix(),'bindings':self.bindings,'source_hashes':{p:sha(ROOT/p) for p in self.cache}})
