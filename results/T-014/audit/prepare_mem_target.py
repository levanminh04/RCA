"""Target the predeclared MEM cell, not all fse cases; exact T006 len10 input."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from RCAEval.io.time_series import preprocess

source_root=Path('D:/RCA-ext/data/fse-ob')
target=Path('D:/RCA-ext/work/T-014/audit-r/mem-target')
target.mkdir(parents=True,exist_ok=True)
records=[]
sources=sorted(source_root.glob('*_mem/[1-5]/simple_data.csv'))
assert len(sources)==25, len(sources)
for source in sources:
    relative=source.parent.relative_to(source_root).as_posix()
    frame=pd.read_csv(source).drop(columns=['time.1'],errors='ignore')
    frame=frame.loc[:,~frame.columns.str.endswith('_latency-50')]
    frame=frame.replace([np.inf,-np.inf],np.nan).ffill().fillna(0)
    mark=int((source.parent/'inject_time.txt').read_text().strip())
    frame=pd.concat([frame[frame.time<mark].tail(300),frame[frame.time>=mark].head(300)],ignore_index=True)
    frame=frame.rename(columns={c:c.replace('_latency-90','_latency') for c in frame if c.endswith('_latency-90')})
    times=list(map(int,frame.time))
    values=preprocess(frame,dataset='fse-ob',dk_select_useful=False)
    assert len(values)==600 and values.notna().all().all()
    stem=relative.replace('/','_')
    path=target/(stem+'_input.csv')
    values.to_csv(path,index=False)
    record={'case':'fse-ob/'+relative,'source':str(source),'input':str(path),'stem':stem,
            'rows':len(values),'columns':list(values.columns),'times':times,'mark':mark}
    records.append(record)
    print('PREPARED',relative,len(values),len(values.columns),flush=True)
(target/'inputs.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
pd.DataFrame([{'stem':r['stem'],'input':r['input']} for r in records]).to_csv(target/'inputs.csv',index=False)

