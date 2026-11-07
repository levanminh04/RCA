"""Worker Python 3.8; không nhận root/fault/case ID hay đường dẫn nguồn dữ liệu."""
import json
import pathlib
import sys
import pandas as pd
from p3.adapters import torai
from p3.worker import _json_default

if __name__=='__main__':
    folder=pathlib.Path(sys.argv[1])
    job=json.loads((folder/'job.json').read_text(encoding='utf-8'))
    tabs=[pd.read_csv(folder/(n+'.csv')) for n in ('metric','logts','tracets_err','tracets_lat')]
    result=torai.chay(*tabs,job['t'],job['seed'])
    (folder/'result.json').write_text(json.dumps(result,ensure_ascii=False,default=_json_default),encoding='utf-8')
