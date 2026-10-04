"""Observe actual causal-learn directed edge and actual rht graph conversion."""
import importlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from causallearn.graph.GeneralGraph import GeneralGraph
from causallearn.graph.GraphNode import GraphNode

head=importlib.import_module("RCAEval.graph_heads.rht")
first,second=GraphNode("a_cpu"),GraphNode("b_cpu")
general=GeneralGraph([first,second]);general.add_directed_edge(first,second)
observed=[]
real_graph=head.MemoryGraph
def capture(graph):
    observed.extend((f"{a.entity}_{a.metric}",f"{b.entity}_{b.metric}") for a,b in graph.edges)
    return real_graph(graph)
head.MemoryGraph=capture
times=np.arange(-300,300)
frame=pd.DataFrame({"a_cpu":np.sin(times/9)+1,"b_cpu":np.cos(times/11)+2,"time":times})
try:
    scores=head.rht(general.graph,0,frame)
finally:
    head.MemoryGraph=real_graph
out={"source_graph":"causallearn.GeneralGraph.add_directed_edge(a,b)",
     "expected_edge":["a_cpu","b_cpu"],"actual_pc_matrix":general.graph.astype(int).tolist(),
     "rht_edges_captured":observed,"scores":scores,
     "directed_edge_reversed":observed==[("b_cpu","a_cpu")]}
Path(__file__).with_name("direction.json").write_text(json.dumps(out,indent=2),encoding="utf-8")
print(json.dumps(out,indent=2))
