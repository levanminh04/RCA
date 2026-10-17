"""Bộ đọc bổ sung Node: chỉ xuất giá trị sau lọc thời gian ca dev."""
import csv
from collections import Counter,defaultdict
from p3 import nezha
from p3.selector import LoiRunner


def read_node(selection):
    t=selection['t_ns'];lo=t-300*nezha.NS;hi=t+300*nezha.NS
    pair=Counter();pod_nodes=defaultdict(set);node_pods=defaultdict(set)
    per_minute=defaultdict(lambda:defaultdict(set));empty=0;rows=0;headers={}
    for rel,meta in sorted(selection['files'].items()):
        kind=nezha._relative_path(rel).parts[-2]
        if kind=='metric':
            with nezha._open_source(meta) as f:
                headers[rel]=[c for c in next(csv.reader(f)) if c.startswith('Node')]
            continue
        if kind!='log':continue
        with nezha._open_source(meta) as f:
            reader=csv.DictReader(f);nezha._schema(reader,['Timestamp','TimeUnixNano','PodName','Node'],'log-node')
            for row in reader:
                stamp=int(row['TimeUnixNano'])
                if not lo<=stamp<hi:continue
                if nezha._log_time_ns(row['Timestamp'])!=stamp or row['PodName'] not in nezha.POD_ALIASES:
                    raise LoiRunner('node: clock/pod mismatch')
                pod,node=row['PodName'],row['Node'];rows+=1;empty+=not bool(node)
                pair[(pod,node)]+=1;pod_nodes[pod].add(node);node_pods[node].add(pod)
                per_minute[str(stamp//(60*nezha.NS))][pod].add(node)
    return {'window_ns':[lo,hi],'rows':rows,'empty_node':empty,
            'pairs':[{'PodName':p,'Node':n,'rows':c} for (p,n),c in sorted(pair.items())],
            'pod_to_nodes':{k:sorted(v) for k,v in sorted(pod_nodes.items())},
            'node_to_pods':{k:sorted(v) for k,v in sorted(node_pods.items())},
            'per_minute':{k:{p:sorted(n) for p,n in sorted(v.items())} for k,v in sorted(per_minute.items())},
            'metric_Node_headers':headers,'meaning':'OPEN','deployment_edges_confirmed':False}
