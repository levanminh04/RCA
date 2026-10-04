"""Factor graph backend, edge direction and candidate coverage on two fixed cases.

All configurations use original RHT and the same 1s/111-point/10-point context.
This is a diagnostic with new code/configuration, not a baseline selection.
"""
from datetime import timedelta
import csv
import json
from pathlib import Path
import sys

sys.dont_write_bytecode=True
sys.path.insert(0,"D:/RCA-ext/work/T-014/CIRCA")
import networkx as nx
import numpy as np
import pandas as pd
from circa.alg.ci import RHTScorer
from circa.model.case import CaseData
from circa.model.data_loader import MemoryDataLoader
from circa.model.graph import MemoryGraph,Node

out=Path(__file__).resolve().parent
root=Path("D:/RCA-ext/work/T-014/audit-r")
records=json.loads((root/"inputs.json").read_text())
all_results=[]
with (out/"cases.csv").open("a",encoding="utf-8-sig",newline="") as stream:
    writer=csv.writer(stream)
    for record in records:
        stem=Path(record["input"]).stem.replace("_input","")
        frame=pd.read_csv(record["input"])
        columns=list(frame.columns)
        values=frame.to_numpy()
        old=json.loads((out/(stem+"_comparison.json")).read_text())
        ca=np.array(json.loads((out/(stem+"_graph.json")).read_text())["adj"])
        rp=pd.read_csv(root/(stem+"_pcalg.csv"))
        assert list(rp.columns)==columns
        matrix=rp.to_numpy()
        nodes=[Node(*name.split("_",1)) for name in columns]
        loader={}
        for index,node in enumerate(nodes):
            loader.setdefault(node.entity,{})[node.metric]=list(zip(record["times"],values[:,index]))
        context=CaseData(MemoryDataLoader(loader),nodes[0],record["mark"],interval=timedelta(seconds=1))
        configurations={}
        configurations["RE_PC_actual_RHT"]={"scores":old["rcaeval_scores"],"description":"RCAEval actual reversed PC directions; isolates absent"}
        configurations["RE_PC_actual_RHT_keep_isolates"]={"scores":dict(old["rcaeval_scores"],**old["original_isolate_scores"]),"description":"same reversed directions; graph keeps isolates"}
        correct=nx.DiGraph();correct.add_nodes_from(nodes)
        for a in range(len(ca)):
            for b in range(len(ca)):
                if (ca[a,b],ca[b,a]) in ((-1,-1),(-1,1)):
                    correct.add_edge(nodes[a],nodes[b])
        pcalg=nx.DiGraph();pcalg.add_nodes_from(nodes)
        pcalg.add_edges_from((nodes[a],nodes[b]) for a,b in zip(*np.where(matrix!=0)))
        assert all(a!=b for a,b in pcalg.edges)
        for name,graph in (("RE_PC_orientation_corrected_keep_isolates",correct),("R_pcalg_causalR_full600_keep_isolates",pcalg)):
            scores=RHTScorer().score(MemoryGraph(graph),context,record["mark"]+300)
            configurations[name]={"description":"original RHT on graph; candidate and direction semantics explicit", "scores":{f"{node.entity}_{node.metric}":score.score for node,score in scores.items()},
                                  "edges":[[f"{a.entity}_{a.metric}",f"{b.entity}_{b.metric}"] for a,b in graph.edges],
                                  "dag":nx.is_directed_acyclic_graph(graph),"num_edges":graph.number_of_edges(),
                                  "graph_isolates":[f"{n.entity}_{n.metric}" for n in nx.isolates(graph)]}
            writer.writerow([record["case"],record["source"],name,"factor graph implementation/direction/candidate membership; fixed before new outcomes","b"])
        for name,config in configurations.items():
            config["ranks"]=sorted(config["scores"],key=lambda key:(-config["scores"][key],key))
        result={"case":record["case"],"configurations":configurations,
                "causallearn_correct_edges_not_pcalg":sorted([f"{a.entity}_{a.metric}",f"{b.entity}_{b.metric}"] for a,b in set(correct.edges)-set(pcalg.edges)),
                "pcalg_edges_not_causallearn_correct":sorted([f"{a.entity}_{a.metric}",f"{b.entity}_{b.metric}"] for a,b in set(pcalg.edges)-set(correct.edges)),
                "pcalg_source":"unmodified CIRCA graph/r/causal.R, input full600 deliberately matches RE input; not full original factory context"}
        path=out/(stem+"_r_comparison.json")
        path.write_text(json.dumps(result,indent=2),encoding="utf-8")
        # Ranking has been written before ground-truth service is consulted.
        answer=record["case"].split("/")[1].split("_")[0]
        for name,config in configurations.items():
            services=list(dict.fromkeys(key.split("_",1)[0].replace("-db","") for key in config["ranks"]))
            config["service_ranks_for_evaluation_after_saved"]=services
            config["ground_truth_service_rank_after_saved"]=services.index(answer)+1 if answer in services else None
        path.write_text(json.dumps(result,indent=2),encoding="utf-8")
        all_results.append({"case":record["case"],"num_graph_edge_differences":len(result["causallearn_correct_edges_not_pcalg"])+len(result["pcalg_edges_not_causallearn_correct"]),
                            "configurations":{name:{"num_scored":len(config["scores"]),"top5_metrics":config["ranks"][:5],"true_service_rank":config["ground_truth_service_rank_after_saved"],"num_edges":config.get("num_edges")} for name,config in configurations.items()}})
(out/"r-comparison-summary.json").write_text(json.dumps(all_results,indent=2),encoding="utf-8")
print(json.dumps(all_results,indent=2))
