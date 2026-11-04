import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "src"))

"""Chấm cặp đổi thang trên tập dev đã ghim."""
from collections import Counter
from fractions import Fraction

from m1_danh_gia import pha2


SIZES = {"RE2-TT": 30, "Nezha-OB": 22}
WORLDS = ("P", "S_lo", "S_hi")


def doi_thang(scored, reference, candidate, cells):
    """Chỉ gọi sau khi kiểm cờ, tầng và độ hợp lệ của bản ghi native."""
    old = scored["cau_hinh"][reference]["ca"]
    new = scored["cau_hinh"][candidate]["ca"]
    cells = set(cells)
    if old.keys() != new.keys():
        raise ValueError("Hai vế khác tập ca")
    if Counter(case["dataset"] for case in old.values()) != SIZES:
        raise ValueError("Sai mẫu số dev")
    expected = {case["o"] for case in old.values()}
    if len(cells) != 23 or expected != cells:
        raise ValueError("Sai tập 23 ô đã ghim")
    for oid, case in old.items():
        other = new[oid]
        if (case["dataset"], case["o"]) != (other["dataset"], other["o"]):
            raise ValueError(f"Lệch ánh xạ ô tại {oid}")
        if set(case["theo_the_gioi"]) != set(WORLDS) or set(other["theo_the_gioi"]) != set(WORLDS):
            raise ValueError(f"Lệch thế giới tại {oid}")
    return pha2.ket_cuc_cap(
        scored, reference, candidate, cells, "doi_thang", "luat_C",
        moc_gia=None, delta_d_co_dinh={d: Fraction(1, n) for d, n in SIZES.items()},
    )


def do_ben(scored, reference, candidate, *, seed, samples):
    """Bootstrap ghép theo ô trong từng dataset, và bỏ lần lượt một ô."""
    import numpy as np
    from m1_danh_gia import rr

    if samples <= 0:
        raise ValueError("Cần số mẫu bootstrap dương")
    ca = scored["cau_hinh"][reference]["ca"]
    cells = {c["o"] for c in ca.values()}
    design = [dict(ma=oid, dataset=c["dataset"], o=c["o"]) for oid, c in sorted(ca.items())]

    def delta(weights):
        result = {}
        for world in WORLDS:
            pair={"cau_hinh":{cid:scored["cau_hinh"][cid] for cid in (reference,candidate)}}
            stats = pha2.mrr_cau_hinh(pair, weights, world)
            result[world] = {d: stats[candidate][d] - stats[reference][d] for d in stats[reference]}
        return result

    rng = np.random.default_rng(seed)
    values = [delta(rr.lay_mau_o(design, rng)) for _ in range(samples)]
    limits = {
        world: {
            d: list(map(float, np.quantile([float(row[world][d]) for row in values], [0.025, 0.975])))
            for d in values[0][world]
        }
        for world in WORLDS
    }
    return {
        "seed": seed,
        "samples": samples,
        "khoang_phan_vi": limits,
        "bo_tung_o": {
            cell: delta({oid: int(c["o"] != cell) for oid, c in ca.items()})
            for cell in sorted(cells)
        },
    }


def cham_ban_ghi(records, labels):
    """Chấm bản ghi đã kiểm hash. labels chỉ chứa tập dev đúng cửa sổ."""
    from m1_danh_gia import m5, rr
    from p3 import danh_gia

    configs = {}
    for record in records:
        oid = record["opaque_id"]
        cases = configs.setdefault(record["config_id"], {"ca": {}})["ca"]
        if oid in cases or oid not in labels:
            raise ValueError(f"Mã ca trùng hoặc ngoài tập chấm: {oid}")
        label = labels[oid]
        root = label["root"]
        ok = record["status"] == "OK"
        normal_graph = {tuple(edge) for edge in (record.get("extra") or {}).get("G_N", [])}
        world_scores = {}
        for world in WORLDS:
            blocks = pha2._blocks(record, world)
            distribution = rr.phan_bo(blocks, root) if ok else {}
            world_scores[world] = {
                "RR": rr.rr_ca(blocks, root, ok),
                "hit1": rr.hit1_ca(blocks, root, ok),
                "hang": rr.hang_ky_vong(blocks, root) if ok else None,
                "M5": ok and m5.co_M5(blocks, root, normal_graph),
                "do": danh_gia.do_ca(distribution, ok),
            }
        cases[oid] = {
            "dataset": label["dataset"], "o": label["o"], "status": record["status"],
            "verdict": record.get("verdict"), "theo_the_gioi": world_scores,
        }
    if not configs or any(v["ca"].keys() != labels.keys() for v in configs.values()):
        raise ValueError("Ma trận chấm thiếu ca hoặc cấu hình")
    return {"cau_hinh": configs}



def tong_hop(scored, ce):
    from m1_danh_gia import rr
    from p3 import danh_gia

    output = {}
    for cid, config in scored["cau_hinh"].items():
        ca = config["ca"]
        output[cid] = {}
        for world in WORLDS:
            table = {}
            for dataset in ("gop", *SIZES):
                selected = {o: c for o, c in ca.items() if dataset == "gop" or c["dataset"] == dataset}
                values = {o: dict(c["theo_the_gioi"][world]["do"], status=c["status"]) for o,c in selected.items()}
                table[dataset] = dict(
                    danh_gia.tong_hop(values),
                    MRR=rr.mrr({o: c["theo_the_gioi"][world]["RR"] for o,c in selected.items()}),
                    M5=sum(c["theo_the_gioi"][world]["M5"] for c in selected.values()),
                )
            fake = ce[cid]
            valid = [x[world] for x in fake.values()
                     if x["status"] == "OK" and x[world]["V0"] != "INSUFFICIENT_EVIDENCE"]
            table["C-e"] = {
                "total": len(fake), "valid": len(valid),
                "insufficient": sum(x[world]["V0"] == "INSUFFICIENT_EVIDENCE" for x in fake.values()),
                "CAUSE_FOUND": sum(x["V0"] == "CAUSE_FOUND" for x in valid),
                "mean_N1": sum((Fraction(x["N1"]) for x in valid), Fraction(0))/len(valid) if valid else None,
                "V0_rate": Fraction(sum(x["V0"] == "CAUSE_FOUND" for x in valid),len(valid)) if valid else None,
                "status": "chưa kiểm được" if not valid else "descriptive",
            }
            output[cid][world] = table
    return output


def t4_candidates(scored, ce, summary, reference):
    """Chỉ đánh dấu đủ điều kiện trình Minh, không tự đổi tham số."""
    from m1_danh_gia import rr

    output = {}
    baseline = scored["cau_hinh"][reference]["ca"]
    cells = {x["o"] for x in baseline.values()}
    for cid,config in scored["cau_hinh"].items():
        if cid == reference:
            continue
        per_world = {}
        for world in WORLDS:
            old = {o: c["theo_the_gioi"][world]["RR"] for o,c in baseline.items()}
            new = {o: c["theo_the_gioi"][world]["RR"] for o,c in config["ca"].items()}
            mapping = {o:c["o"] for o,c in baseline.items()}
            old_cell, new_cell = rr.rr_o(old,mapping),rr.rr_o(new,mapping)
            positive = sum(new_cell[c] > old_cell[c] for c in cells)
            negative = sum(new_cell[c] < old_cell[c] for c in cells)
            delta = {d: summary[cid][world][d]["MRR"] - summary[reference][world][d]["MRR"]
                     for d in ("gop",*SIZES)}
            valid_pairs = [(ce[reference][o][world],ce[cid][o][world]) for o in ce[reference]
                           if ce[reference][o]["status"] == ce[cid][o]["status"] == "OK"
                           and ce[reference][o][world]["V0"] != "INSUFFICIENT_EVIDENCE"
                           and ce[cid][o][world]["V0"] != "INSUFFICIENT_EVIDENCE"]
            fake_ok = bool(valid_pairs) and (
                sum(b["N1"]-a["N1"] for a,b in valid_pairs) <= 0
                and sum((b["V0"]=="CAUSE_FOUND")-(a["V0"]=="CAUSE_FOUND") for a,b in valid_pairs) <= 0)
            flags = {
                "delta_above_001": delta["gop"] > Fraction(1,100),
                "positive_cells_more": positive > negative,
                "dataset_bound": all(delta[d] >= -Fraction(1,n) for d,n in SIZES.items()),
                "M5_not_increase": all(summary[cid][world][d]["M5"] <= summary[reference][world][d]["M5"] for d in SIZES),
                "C-e_not_increase": fake_ok,
            }
            per_world[world] = {"delta_MRR":delta,"P":positive,"M":negative,
                                "checks":flags,"passes_numeric":all(flags.values()),
                                "C-e_pairs":len(valid_pairs)}
        output[cid] = {
            "worlds":per_world,
            "candidate_pending_chain_and_fragility":all(x["passes_numeric"] for x in per_world.values()),
        }
    return output



def collect_controllers(folders, labels, allocation=None):
    """Kiểm hash từng cửa sổ trước chấm. Mỗi cấu hình–ca–cửa sổ chỉ xuất hiện một lần."""
    from kiem import read_run
    from chay import read

    scored = {"cau_hinh": {}}
    fake = {}
    index = {}
    hashes = {}
    for folder in folders:
        status = read(folder/"kiem.json")
        if status["success"]:
            if status["jobs"] != len(status["finished"]):
                raise ValueError(f"Controller thiếu cửa sổ {folder}")
        elif not (status.get("partial_verified") and status["error"] == "resource_repartition"
                  and status["jobs"] == len(status["finished"]) + len(status["remaining"])):
            raise ValueError(f"Controller chưa hoàn tất hoặc thiếu bằng chứng đóng từng cửa sổ {folder}")
        for child in status["finished"]:
            where = folder.parent/child
            command, metadata, pairs = read_run(where)
            hashes[child] = metadata
            for record, detail in pairs():
                oid,cid,kind = record["opaque_id"],record["config_id"],detail["window"]
                if allocation is not None:
                    device = "ec2" if "-ec2-" in folder.name else "laptop"
                    if allocation[oid] != device:
                        continue
                key=(cid,oid,kind)
                if key in index:
                    raise ValueError(f"Lượt chấm trùng {key}")
                index[key]=child
                if record["status"] not in ("OK","NO_EVIDENCE"):
                    raise ValueError(f"Bản ghi lỗi trước chấm {child}")
                if kind == "that":
                    one = cham_ban_ghi([record],{oid:labels[oid]})["cau_hinh"][cid]["ca"][oid]
                    scored["cau_hinh"].setdefault(cid,{"ca":{}})["ca"][oid]=one
                else:
                    states=detail["trace"]["world_state"]
                    if set(states)!=set(WORLDS):
                        raise ValueError("Mốc giả thiếu thế giới")
                    fake.setdefault(cid,{})[oid]={"status":record["status"],"dataset":detail["dataset"],
                                                  **{w:{"N1":states[w]["N1"],"V0":states[w]["V0"],
                                                        "valid_units":states[w]["valid_units"]} for w in WORLDS}}
    return scored,fake,index,hashes



def main():
    import argparse
    import hashlib
    import json
    import time
    from contextlib import redirect_stdout,redirect_stderr
    from chay import ROOT,OUT,read,dump,sha,configs
    from kiem import read_run

    parser=argparse.ArgumentParser(description="Chấm T-048 sau đóng hash pha 1")
    parser.add_argument("step",choices=("T4","T4b"))
    parser.add_argument("run_id")
    parser.add_argument("controllers",nargs="+")
    parser.add_argument("--bootstrap",type=int,default=1000)
    args=parser.parse_args()
    folder=(OUT/"runs"/args.run_id).resolve()
    if folder.parent!=(OUT/"runs").resolve():
        raise ValueError("Đường chấm ngoài T-048")
    folder.mkdir()
    started=time.monotonic()
    with (folder/"stdout.log").open("x",encoding="utf-8") as stdout,(
        folder/"stderr.log").open("x",encoding="utf-8") as stderr,redirect_stdout(stdout),redirect_stderr(stderr):
        matrix=read(OUT/"ma-tran.json")
        controllers=[(OUT/"runs"/name).resolve() for name in args.controllers]
        hashes={}
        for ctrl in controllers:
            if ctrl.parent!=(OUT/"runs").resolve():
                raise ValueError("Nguồn controller ngoài T-048")
            status=read(ctrl/"kiem.json")
            source=read(ctrl/"command.json")
            if source["plan"]["source_sha256"]!=matrix["source_sha256"]:
                raise ValueError("Nguồn phương pháp khác ma trận")
            for child in status["finished"]:
                _,meta,_=read_run(ctrl.parent/child)
                hashes[child]=meta
        command={"argv":sys.argv,"step":args.step,"controllers":[str(p) for p in controllers],
                 "source_sha256":matrix["source_sha256"],"phase1":hashes,
                 "tool_sha256":{p.name:sha(p) for p in Path(__file__).parent.glob("*.py")},
                 "bootstrap_n":args.bootstrap,"bootstrap_seed":20261103}
        (folder/"command.json").write_text(dump(command)+"\n",encoding="utf-8")
        with (ROOT/"tasks/T-048-thang-diem-tham-so-e4/LOG.md").open("a",encoding="utf-8") as log:
            log.write(f"\n- Hash trước pha 2 {args.step}: {folder.relative_to(ROOT).as_posix()}/command.json#/phase1. Đã kiểm từng native/trung gian trước bước đọc nhãn.\n")
        sys.path.insert(0,str(ROOT/"results/T-045/scripts"))
        from pha2_khoi_k import nap_nhan
        labels=nap_nhan(False)
        t0_path=ROOT/"results/T-043/ks16/dem-sau-ghep-nhan.json"
        manifest=read(ROOT/"results/T-043/manifest.json")
        expected=[p["sha256"] for p in manifest["outputs"] if p["path"]==t0_path.relative_to(ROOT).as_posix()]
        if len(expected)!=1 or sha(t0_path)!=expected[0]:
            raise ValueError("Nguồn T0 lệch hash")
        t0=read(t0_path)
        if {(c["opaque_id"],c["dataset"],c["cell"]) for c in t0["cases"]} != {
            (o,c["dataset"],c["o"]) for o,c in labels.items()}:
            raise ValueError("Tập ca/ô khác T0")
        scored,fake,index,closed=collect_controllers(controllers,labels,matrix["allocation"])
        declared=configs()
        expected_configs={c for c in declared if c.startswith("R0-E4")} if args.step=="T4" else {
            "R0-E4-S1-e0.05-a0.01",*matrix["stages"]["T4b"]}
        if set(scored["cau_hinh"])!=expected_configs or set(fake)!=expected_configs:
            raise ValueError("Sai tập cấu hình chính")
        re_ids={o for o,c in labels.items() if c["dataset"]=="RE2-TT"}
        if any(x["ca"].keys()!=labels.keys() for x in scored["cau_hinh"].values()) or any(set(x)!=re_ids for x in fake.values()):
            raise ValueError("Thiếu ca hoặc sai mẫu số")
        summary=tong_hop(scored,fake)
        output={"step":args.step,"complete":True,"scored":scored,"ce":fake,"summary":summary,
                "E_X":sorted({c["o"] for c in labels.values()}),
                "phase1":closed,"source_controllers":args.controllers,
                "index":[dict(config_id=c,opaque_id=o,window=w,child=child) for (c,o,w),child in index.items()]}
        if args.step=="T4":
            output["candidates"]=t4_candidates(scored,fake,summary,"R0-E4-S1-e0.05-a0.01")
        (OUT/("t4.json" if args.step=="T4" else "t4b.json")).write_text(dump(output)+"\n",encoding="utf-8")
        metadata={"closed":True,"records":len(index),"configs":len(expected_configs),
                  "cases":len(labels),"fake_windows":len(re_ids),"cells":len(output["E_X"]),
                  "wall_seconds":time.monotonic()-started,
                  "output_sha256":sha(OUT/("t4.json" if args.step=="T4" else "t4b.json"))}
        (folder/"kiem.json").write_text(dump(metadata)+"\n",encoding="utf-8")



def mechanism_summary(run_id):
    """Ghép chẩn đoán đã đóng, giữ từng ca/cặp và không cộng nhóm chồng lấn."""
    import json,math,time
    import numpy as np
    from collections import defaultdict
    from chay import OUT,read,dump,sha
    from m1_danh_gia.pha2 import giai_ma_json

    folder=OUT/'runs'/run_id
    folder.mkdir()
    start=time.monotonic()
    score_path=OUT/'t4b.json'
    assert sha(score_path)==read(OUT/'runs/cham-t4b-full-001/kiem.json')['output_sha256']
    t4b=giai_ma_json(read(score_path))
    provenance={}
    cases=[]
    contexts={}
    controls=[]
    b2_rows=[]
    shared=[]
    for device in ('laptop','ec2'):
        for stem in ('b2-t4b','native-t4b','shared-pv-t4b'):
            name=f'{stem}-{device}-001'
            meta=read(OUT/'runs'/name/'kiem.json')
            assert meta['closed']
            if stem=='b2-t4b':
                assert not meta['exceptions']
            provenance[name]=dict(sha256=sha(OUT/'runs'/name/'kiem.json'),metadata=meta)
            if stem in ('b2-t4b','shared-pv-t4b'):
                raw=OUT/'runs'/name/'trung-gian.jsonl'
                assert sha(raw)==meta['trace_sha256']
                rows=[giai_ma_json(json.loads(x)) for x in raw.read_text(encoding='utf-8').splitlines()]
                (b2_rows if stem=='b2-t4b' else shared).extend(rows)
        name=f'b4-t4b-{device}-002'
        root=OUT/'runs'/name
        meta=read(root/'kiem.json')
        assert meta['closed'] and sha(root/'ban-ghi.jsonl')==meta['phase2_sha256']
        assert sha(root/'trung-gian.jsonl')==meta['context_sha256']
        rows=[giai_ma_json(json.loads(x)) for x in (root/'ban-ghi.jsonl').read_text(encoding='utf-8').splitlines()]
        assert len(rows)==meta['totals']['cases']
        cases.extend(rows)
        for row in (giai_ma_json(json.loads(x)) for x in (root/'trung-gian.jsonl').read_text(encoding='utf-8').splitlines()):
            contexts[(row['opaque_id'],row['base'])]=row['worlds']
        provenance[name]=dict(sha256=sha(root/'kiem.json'),metadata=meta)
        name=f'controls-t4b-{device}-002'
        root=OUT/'runs'/name
        meta=read(root/'kiem.json')
        assert meta['closed'] and sha(root/'trung-gian.jsonl')==meta['controls_sha256']
        assert meta['B4_sha256']==provenance[f'b4-t4b-{device}-002']['metadata']['phase2_sha256']
        controls.extend(giai_ma_json(json.loads(x)) for x in (root/'trung-gian.jsonl').read_text(encoding='utf-8').splitlines())
        provenance[name]=dict(sha256=sha(root/'kiem.json'),metadata=meta)
    expected={(o,base) for base in ('R0','E1+E2') for o in t4b['scored']['cau_hinh']['R0-E4-S1-e0.05-a0.01']['ca']}
    assert len(cases)==104 and {(c['opaque_id'],c['base']) for c in cases}==expected and set(contexts)==expected
    matrix=read(OUT/'ma-tran.json')
    expected_windows={(j['opaque_id'],j['window']) for j in matrix['jobs']}
    assert len(b2_rows)==82 and {(r['opaque_id'],r['window']) for r in b2_rows}==expected_windows
    assert len(shared)==164 and {(r['opaque_id'],r['window'],r['base']) for r in shared}=={(o,w,b) for o,w in expected_windows for b in ('R0','E1+E2')}
    (folder/'command.json').write_text(dump(dict(source_sha256=sha(score_path),provenance=provenance,tool_sha256=sha(Path(__file__)),group_policy='Mỗi nhóm là phép chẩn đoán đã định nghĩa; có thể chồng lấn. Không đổi luật C.'))+'\n',encoding='utf-8')

    # Read native scores alone after the recorded phase-1 hashes; avoid rereading GB of full traces.
    used={}
    native_hashes={}
    children={r['child'] for r in t4b['index'] if r['config_id'].endswith('-z-S1')}
    for child in sorted(children):
        root=OUT/'runs'/child
        meta=read(root/'kiem.json')
        assert sha(root/'ban-ghi.jsonl')==meta['phase1_sha256']
        native_hashes[child]=meta['phase1_sha256']
        for line in (root/'ban-ghi.jsonl').open(encoding='utf-8'):
            r=json.loads(line)
            if not r['config_id'].endswith('-z-S1'):
                continue
            base=r['config_id'].removesuffix('-z-S1')
            matches=[v for v in t4b['index'] if v['config_id']==r['config_id'] and v['opaque_id']==r['opaque_id'] and v['child']==child]
            if len(matches)>1:
                times={j['t']*10**9:j['window'] for j in matrix['jobs'] if j['opaque_id']==r['opaque_id'] and 't' in j}
                kind=times[r['window']['A'][0]]
                matches=[v for v in matches if v['window']==kind]
            assert len(matches)==1
            kind=matches[0]['window']
            pv={u['ma'] for u in r['extra']['don_vi_phan_vi']}
            worlds={w:{(c['don_vi'],c['huong']):c['s'] for c in r['extra']['kenh_co_the_gioi'][w] if c['don_vi'] in pv} for w in WORLDS}
            assert all(worlds[w]==worlds['P'] for w in WORLDS)
            key=(r['opaque_id'],kind,base)
            assert key not in used
            used[key]=worlds['P']
    assert len(used)==164

    distributions=defaultdict(lambda:dict(IQR=[],raw_z=[],used_z=[]))
    extreme_used=[]
    for row in b2_rows:
        for base,data in row['bases'].items():
            active=used[(row['opaque_id'],row['window'],base)]
            for unit in data['z_distribution']:
                iqr=unit['IQR']
                level='IQR_zero' if iqr==0 else ('positive_below_floor' if iqr<10*sys.float_info.epsilon else 'at_or_above_floor')
                key=(base,row['dataset'],row['window'],level)
                target=distributions[key]
                target['IQR'].append(iqr)
                target['raw_z'].extend((unit['z_len'],unit['z_xuong']))
                for direction in ('len','xuong'):
                    point=active.get((unit['unit'],direction))
                    if point is not None:
                        assert point==unit['z_'+direction] and math.isfinite(point)
                        target['used_z'].append(point)
                        extreme_used.append(dict(base=base,opaque_id=row['opaque_id'],window=row['window'],dataset=row['dataset'],unit=unit['unit'],direction=direction,z=point,IQR=iqr,c=unit['c'],A_extrema=unit['A_extrema']))
    def describe(values):
        return dict(n=len(values),minimum=min(values),q25=float(np.quantile(values,.25)),median=float(np.median(values)),q75=float(np.quantile(values,.75)),q95=float(np.quantile(values,.95)),maximum=max(values)) if values else dict(n=0)
    distribution=[dict(base=b,dataset=d,window=w,IQR_group=g,**{k:describe(v) for k,v in values.items()}) for (b,d,w,g),values in sorted(distributions.items())]

    groups={}
    for base in ('R0','E1+E2'):
        groups[base]={}
        for world in WORLDS:
            counts=Counter()
            memberships=defaultdict(list)
            for case in (c for c in cases if c['base']==base):
                oid=case['opaque_id']
                data=case['mechanism']['worlds'][world]
                rr=data['RR']
                eid='R0-E4-S1-e0.05-a0.01' if base=='R0' else 'E1+E2-E4-S1'
                for cid,key in ((eid,'E4_S1'),(base+'-z-S1','z_S1'),(base+'-z-S0','z_S0')):
                    assert rr[key]==t4b['scored']['cau_hinh'][cid]['ca'][oid]['theo_the_gioi'][world]['RR']
                delta=rr['z_S1']-rr['E4_S1']
                outcome='helped' if delta>0 else ('harmed' if delta<0 else 'unchanged')
                counts['cases_'+outcome]+=1
                counts['root_absent']+=not contexts[(oid,base)][world]['root_ranked']
                if rr['E4_S1']>rr['E4_S0']:
                    memberships['m_improves_E4_RR'].append(oid)
                if rr['z_S1']!=rr['z_S0']:
                    memberships['m_changes_z_RR'].append(oid)
                if rr['z_remove_one_A_extreme']!=rr['z_S1']:
                    memberships['remove_one_extreme_changes_RR'].append(oid)
                for flip in data['flips']:
                    counts['root_rival_transitions']+=1
                    before,after=flip['before_relation'],flip['after_relation']
                    sat=flip['sat_only_relation']==after
                    non=flip['non_sat_only_relation']==after
                    maxima=flip['root_E4']['max_channels']+flip['rival_E4']['max_channels']
                    satmax=[k for k in maxima if k in flip['channels'] and flip['channels'][k]['r_A_one']]
                    collapse=bool(flip['E4_max_rendered_tied'] and satmax and sat)
                    cross=flip['cross_type_max_competition'] and flip['revert_winning_PV_group_relation']!=after
                    tags={
                        'sat_group_reproduces_transition':sat,
                        'non_sat_group_reproduces_transition':non,
                        'both_groups_separately_reproduce':sat and non,
                        'E4_max_tie_with_sat_max':bool(flip['E4_max_rendered_tied'] and satmax),
                        'sat_max_tie_transition_reproduced':collapse,
                        'm_already_separated_sat_max_tie':bool(collapse and flip['first_key_before']==1 and before!=0),
                        'count_scale_transition_supported':cross,
                        'count_scale_pure_count_opponent':cross and flip['pure_count_opponent'],
                        'overlap_sat_updates_count_scale':sat and cross,
                    }
                    flip['diagnostic_tags']=tags
                    flip['pair_favors_root']=after<before
                    flip['whole_case_delta_RR']=delta
                    for tag,yes in tags.items():
                        if yes:
                            counts[tag+'_pairs']+=1
                            memberships[tag+'_'+outcome].append(oid)
            groups[base][world]=dict(counts=dict(counts),case_membership={k:sorted(set(v)) for k,v in memberships.items()})
    control_groups={}
    for base in ('R0','E1+E2'):
        rows=[r for r in controls if r['base']==base and r['world']=='P']
        control_groups[base]=dict(P_pairs=len(rows),P_cases=sorted({r['opaque_id'] for r in rows}),P_correct_pairs=sum(r['both_correct_top1'] for r in rows),P_correct_cases=sorted({r['opaque_id'] for r in rows if r['both_correct_top1']}),P_sat_max_tie_pairs=sum(r['E4_max_tied'] and bool(r['saturated_E4_max_channels']) for r in rows),P_cross_type_pairs=sum(r['cross_type_max_competition'] for r in rows))
    output=dict(complete=True,source_sha256=sha(score_path),provenance=provenance,native_score_hashes=native_hashes,formula=dict(unique_base_windows=164,PV_units=sum(r['PV_units'] for r in shared),finite_oracle_units=sum(r['finite_oracle_units'] for r in shared),old_reference_oracle_completed_by_equal_new_samples=sum(r['old_reference_missing_oracle'] for r in shared),actual_native_exceptions=0,extreme_fixture='runs/kiem-cuc-tri-z-001/kiem.json',distribution=distribution,largest_used_z=sorted(extreme_used,key=lambda r:(-r['z'],r['opaque_id'],r['unit']))[:20]),groups=groups,control_groups=control_groups,cases=cases,contexts=[dict(opaque_id=o,base=b,worlds=v) for (o,b),v in sorted(contexts.items())],controls=controls,OPEN=[dict(question='Tương tác gói cổng × điểm',missing='z+S1 ghép E4+S1 trên G0/D0 cùng revision/ca/khóa',impact='Không quy chênh riêng cho thay cổng; phép so chính chỉ trên G3/D1',next='Trình phép bổ sung và chi phí theo B4, không tự mở ma trận'),dict(question='Lặp lại ngoài dev',missing='Dữ liệu độc lập theo giao thức đã khóa',impact='Không suy hiệu quả P7 từ dev đã dùng chọn nhiều lần',next='G3/test và đánh giá độc lập do Minh duyệt riêng'),dict(question='Miền số học cực trị của z',missing='Quyết định xử lý/biểu diễn số tại các phản ví dụ ngoài dev',impact='Không khẳng định mọi mẫu hữu hạn cho thang z hợp lệ',next='Trình phạm vi sửa src riêng; giữ native lỗi, không chọn điểm thay thế')],interpretation='Các nhóm chẩn đoán chồng lấn; bằng chứng theo cặp không tự là nguyên nhân duy nhất của ΔRR toàn ca. Controls cùng điều kiện không là ca độc lập ở ba thế giới.')
    (OUT/'co-che.json').write_text(dump(output)+'\n',encoding='utf-8')
    (folder/'kiem.json').write_text(dump(dict(closed=True,cases=len(cases),controls=len(controls),output_sha256=sha(OUT/'co-che.json'),wall_seconds=time.monotonic()-start))+'\n',encoding='utf-8')
    return {b:groups[b]['P'] for b in groups}

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="co-che":
        print(mechanism_summary(sys.argv[2]))
    else:
        main()
