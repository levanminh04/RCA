"""Kiểm K trước nhãn: ma trận/hash/chế độ, QT5, K-đủ T046, R0 T1."""
import argparse
import collections
import copy
import json
import sys
from pathlib import Path
import adapter_t047 as ad
import tep_pha1
sys.path[:0] = [str(ad.ROOT/'results/T-046/scripts'),str(ad.ROOT/'results/T-045/scripts')]
import b10_kiem_src as b10
import t1_tong_hop as old_t1
from p3 import nezha


def kiem(path, fake=False):
    path = ad.duong_ra(path)
    meta = tep_pha1.kiem(path)
    expected_n = 30 if fake else 52
    if meta['so_ca'] != expected_n or meta['so_ban_ghi'] != expected_n*16 or len(meta['cau_hinh']) != 16:
        raise ValueError('ma trận K không đủ')
    U = json.loads((ad.ROOT/'results/T-022/mappings/universe-re2tt-dev.json').read_text(encoding='utf-8'))['U']
    rows, flags, by_cfg = [], [], collections.Counter()
    for d in sorted((path/'cases').iterdir()):
        diag = json.loads((d/'summary.json').read_text(encoding='utf-8'))
        oid,ds = d.name,diag['dataset']
        m = tep_pha1.kiem(d/'phase1')
        checks = {}
        with (d/'phase1'/m['tep']).open('r',encoding='utf-8') as f:
            for line in f:
                r = json.loads(line)
                cid = r['config_id']
                by_cfg[cid] += 1
                q = old_t1.soi_ban_ghi.soi(r,False)
                fl = {k:q[k] for k in ('diem_lon_hon_1e6','toan_hoa','so_nguong_cuc_lon',
                     'cot_metric_chua_khai_nguon','nguon_metric_unsupported','coverage_unsupported') if q[k]}
                if (q.get('nhom_chiem') or 0)>.9:
                    fl['nhom_chiem']=q['nhom_chiem']
                if fl:
                    flags.append(dict(oid=oid,config_id=cid,flags=fl))
                if cid == 'K-R0':
                    ref_run='b2-t1-ce-001' if fake else 'b2-t1-seed0-001'
                    p=ad.OUT/'runs'/ref_run/'cases'/oid/'phase1/records/00000.json'
                    ref=json.loads(p.read_text(encoding='utf-8'))
                    a,b=copy.deepcopy(r),copy.deepcopy(ref)
                    for x in (a,b):
                        x.pop('config_id');x.pop('variant')
                    checks['R0_T1_differences']=old_t1.truong_lech(a,b)
                if cid == 'K-E1+E2+E3+E5':
                    case=dict(aliases={},inventory=U if ds=='RE2-TT' else nezha.UNIVERSE)
                    summary,_,_=b10.tom_tat(r,case,'K-du')
                    p=ad.ROOT/'results/T-046/runs/b10-kiem-src-001/ca'/f'{oid}.json'
                    previous=json.loads(p.read_text(encoding='utf-8'))['cua_so'][('ce' if fake else 'that')+'|K-du']['tom_tat']
                    checks['Kdu_T046_differences']={k:[previous.get(k),summary.get(k)] for k in set(previous)|set(summary)
                                                   if previous.get(k)!=summary.get(k)}
                    checks['Kdu_summary']=summary
        rows.append(dict(oid=oid,dataset=ds,checks=checks))
    out=dict(path=str(path.relative_to(ad.ROOT)),phase1=meta,cases=rows,config_counts=dict(by_cfg),QT5_can_doc=flags,
             computational_PASS=all(not x['checks'].get('R0_T1_differences') and not x['checks'].get('Kdu_T046_differences')
                                    and len(x['checks'])==3 for x in rows))
    ad.ghi(path/'kiem-k-pha1.json',out)
    if not out['computational_PASS']:
        raise ValueError('STOP K đối chiếu lệch; xem kiem-k-pha1.json')
    print(json.dumps(dict(path=out['path'],PASS=True,QT5_flag_records=len(flags))))
    return out


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--fake',action='store_true')
    a=p.parse_args();kiem(a.run,a.fake)
