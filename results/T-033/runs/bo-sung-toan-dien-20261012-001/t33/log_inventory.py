import importlib.util,json,pathlib
import pandas as pd
sp=importlib.util.spec_from_file_location('w',pathlib.Path(__file__).with_name('worker-v3.py'));w=importlib.util.module_from_spec(sp);sp.loader.exec_module(w)
item=w.S['cases'][0];df=pd.read_parquet(w.raw_path(item,'logs.parquet'));print(json.dumps({'columns':df.columns.tolist(),'messages':df.groupby('container_name',sort=False).first()['message'].head(8).tolist()},ensure_ascii=False))
