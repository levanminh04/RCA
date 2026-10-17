"""Bộ dựng theo dac-ta-do-thi.md v2; cấu trúc, count, witness, không điểm RCA."""
import json
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

CORE = ['traceID','spanID','parentSpanID','serviceName','operationName','startTime','duration']
FORBIDDEN = {'root','fault','cell','case','label','labels','ground_truth','inject_time','opaque_id_path'}
UNTYPED = 'gọi-chưa-phân-kiểu'
SYNC = 'gọi-đồng-bộ'
MESSAGE = 'thông-điệp'
DATA = 'dữ-liệu'
DEPLOY = 'triển-khai'
TYPES = {'service','gateway','database','cache','broker','identity-provider','external','host','unknown'}


def op_id(entity, operation):
    return json.dumps([entity, operation], ensure_ascii=False, separators=(',',':'))


def from_p3(spans):
    """Chỉ hợp đồng span; không sửa frame của adapter baseline."""
    if FORBIDDEN.intersection(spans.columns):
        raise ValueError('label_column')
    out = spans.copy(deep=False)
    for column in ['kind','attributes','links']:
        if column not in out:
            out[column] = None
    return out


def _string(s):
    return s.fillna('').astype(str)


def _root(s):
    return s.isin(['','0','-1','root','None','nan','null']) | s.str.fullmatch(r'0+')


def _canonical(o):
    return json.dumps(o, ensure_ascii=False, sort_keys=True, separators=(',',':'))


def edge_key(edge):
    """Giữ địa chỉ messaging khi gộp/chiếu; ID bản tin không là cấu trúc."""
    key = (edge['source'], edge['target'], edge['type'],
           edge['evidence_source'], edge['destination'])
    return key + (_canonical(edge['messaging']),) if 'messaging' in edge else key


def _message_address(attrs, producer=False):
    fields = ('broker', 'broker_scope', 'exchange', 'routing_key', 'queue')
    address = {name: attrs.get('messaging.' + name) for name in fields}
    for name in (*fields, 'identity_scope', 'message_id', 'destination'):
        value = attrs.get('messaging.' + name)
        if value is not None and (not isinstance(value, str) or
                                  (not value and name not in ('exchange', 'routing_key'))):
            raise ValueError('messaging_attribute_type')
    verified = attrs.get('messaging.identity_scope_verified')
    if verified is not None and not isinstance(verified, bool):
        raise ValueError('messaging_attribute_type')
    if producer:
        address['queue'] = None
    return address


def _queue_address(address):
    key = [address[name] for name in ('broker', 'broker_scope', 'queue')]
    return key if all(key) else None


def _message_identity(attrs):
    key = tuple(attrs.get('messaging.' + name)
                for name in ('broker', 'broker_scope', 'identity_scope', 'message_id'))
    return key if all(key) and attrs.get('messaging.identity_scope_verified') is True else None


def _message_conflict(left, right):
    # Queue là điểm nhận; destination legacy chưa có nghĩa đủ để so hai phía.
    for name in ('broker', 'broker_scope', 'exchange', 'routing_key', 'identity_scope', 'message_id'):
        a, b = left.get('messaging.' + name), right.get('messaging.' + name)
        if a is not None and b is not None and a != b:
            return True
    return False


class Prepared:
    """Lưu chỉ mục một lần để dựng nhiều khoảng trên cùng span, không I/O."""
    def __init__(self, spans, aliases, universe):
        if FORBIDDEN.intersection(spans.columns):
            raise ValueError('label_column')
        if set(CORE)-set(spans.columns):
            raise ValueError('missing_core')
        self.aliases = dict(aliases)
        self.universe = dict(universe) if isinstance(universe, dict) else {e:'unknown' for e in universe}
        if any(t not in TYPES for t in self.universe.values()):
            raise ValueError('entity_type')
        cols=CORE+[c for c in ['_start_ns','_end_ns','kind','attributes','links'] if c in spans]
        f=spans[cols].copy()
        self.raw_count=len(f)
        for c in ['traceID','spanID','parentSpanID','serviceName']:
            f[c]=_string(f[c])
        if ((f.traceID=='') | (f.spanID=='') | (f.serviceName=='')).any():
            raise ValueError('missing_id')
        # Tất cả đồng hồ phải nguyên; tránh ép duration âm hoặc float thành dữ liệu hợp lệ.
        for c in ['startTime','duration']+[c for c in ['_start_ns','_end_ns'] if c in f]:
            v=pd.to_numeric(f[c],errors='raise')
            if v.isna().any() or not np.isfinite(v).all() or (v != np.floor(v)).any():
                raise ValueError('invalid_time')
            f[c]=v.astype('int64')
        if (f.duration<0).any():
            raise ValueError('invalid_time')
        f['operationName']=f.operationName.where(f.operationName.notna(),None)
        dup=f.duplicated(['traceID','spanID'],keep=False)
        if dup.any():
            check=f.loc[dup].copy()
            for c in ['attributes','links']:
                if c in check: check[c]=check[c].map(_canonical)
            for _,g in check.groupby(['traceID','spanID'],sort=False):
                if len(g.drop_duplicates())!=1:
                    raise ValueError('duplicate_conflict')
        self.raw_times=(f['_start_ns'].to_numpy() if '_start_ns' in f else f.startTime.to_numpy()*1000,
                        f['_end_ns'].to_numpy() if '_end_ns' in f else (f.startTime.to_numpy()+f.duration.to_numpy())*1000)
        f=f.drop_duplicates(['traceID','spanID']).reset_index(drop=True)
        f['serviceName']=f.serviceName.map(lambda x:self.aliases.get(x,x))
        self.f=f
        self.start=f['_start_ns'].to_numpy() if '_start_ns' in f else f.startTime.to_numpy()*1000
        self.end=f['_end_ns'].to_numpy() if '_end_ns' in f else (f.startTime.to_numpy()+f.duration.to_numpy())*1000
        if (self.end<self.start).any():raise ValueError('invalid_time')
        self.roots=_root(f.parentSpanID).to_numpy(dtype=bool)
        keys=pd.MultiIndex.from_frame(f[['traceID','spanID']])
        parents=pd.MultiIndex.from_frame(f[['traceID','parentSpanID']])
        self.parent=keys.get_indexer(parents)
        self.parent[self.roots]=-1
        pairs=f[['serviceName','operationName']].drop_duplicates()
        self.op_map={(e,o):op_id(e,o) for e,o in pairs.itertuples(index=False,name=None)}
        self.op=np.asarray([self.op_map[(e,o)] for e,o in f[['serviceName','operationName']].itertuples(index=False,name=None)],dtype=object)
        self.entities=f.serviceName.to_numpy()
        self.trace_ids=f.traceID.to_numpy()
        self.span_ids=f.spanID.to_numpy()
        self.kinds=f.kind.fillna('').str.upper().to_numpy() if 'kind' in f else np.full(len(f),'',dtype=object)
        self.extended=(any(c in f and f[c].notna().any() for c in ['attributes','links']) or
                       bool(np.isin(self.kinds,['PRODUCER','CONSUMER']).any()))

    def mask(self, interval):
        if interval is None:return np.ones(len(self.f),dtype=bool)
        lo,hi=interval
        if not isinstance(lo,int) or not isinstance(hi,int) or hi<lo:raise ValueError('invalid_interval')
        return (self.start>=lo)&(self.end<hi)

    def graph(self, interval=None):
        keep=self.mask(interval); idx=np.flatnonzero(keep)
        p=self.parent
        resolved=keep & (p>=0)
        resolved &= keep[np.maximum(p,0)] if len(p) else resolved
        children=np.flatnonzero(resolved); pi=p[children]
        raw=self.raw_count if interval is None else int(((self.raw_times[0]>=interval[0])&(self.raw_times[1]<interval[1])).sum())
        roots=int((keep & self.roots).sum()); nresolved=len(children); orphan=int(keep.sum())-roots-nresolved
        if roots+nresolved+orphan!=len(idx):raise AssertionError('partition')
        ent_nodes={e:{'id':e,'type':self.universe.get(e,'unknown'),'source':'trace'} for e in sorted(set(self.entities[idx]))}
        op_nodes={self.op[i]:{'id':self.op[i],'entity':self.entities[i],'operation':self.f.operationName.iloc[i],
                            'source':'trace'} for i in idx[:0]}
        for e,o in self.f.loc[keep,['serviceName','operationName']].drop_duplicates().itertuples(index=False,name=None):
            oid=self.op_map[(e,o)];op_nodes[oid]={'id':oid,'entity':e,'operation':o,'source':'trace'}
        op_edges={}; ent_edges={}; extra=set()
        def add(src,dst,kind,source,count=1,witness=(),destination=None,messaging=None):
            new={'source':src,'target':dst,'type':kind,'evidence_source':source,
                 'event_count':0,'witness':[],'destination':destination}
            if messaging is not None:
                new['messaging']=messaging
                new['queue_metric_address']=_queue_address(messaging)
            key=edge_key(new)
            if key not in op_edges:op_edges[key]=new
            row=op_edges[key]; row['event_count']+=int(count)
            row['witness']=sorted(set(tuple(x) for x in row['witness'])|{tuple(x) for x in witness})[:2]
        if len(children):
            ty=np.where((self.kinds[pi]=='CLIENT')&(self.kinds[children]=='SERVER'),SYNC,UNTYPED)
            # Messaging cha-con được ghi như cây span riêng; cạnh phụ thuộc messaging từ endpoint/link.
            ty=np.where(np.isin(self.kinds[children],['PRODUCER','CONSUMER'])|np.isin(self.kinds[pi],['PRODUCER','CONSUMER']),'span-parent',ty)
            rows=pd.DataFrame({'s':self.op[pi],'d':self.op[children],'type':ty,'i':children})
            for (src,dst,kind),g in rows.groupby(['s','d','type'],sort=True):
                gi=g.i.to_numpy()
                sample=gi[np.lexsort((self.span_ids[gi],self.trace_ids[gi]))[:2]]
                witnesses=[(str(self.f.traceID.iloc[i]),str(self.f.spanID.iloc[p[i]]),str(self.f.spanID.iloc[i])) for i in sample]
                add(src,dst,kind,'trace',len(g),witnesses)
        unresolved_messages=0; message_diagnostics={}; has_messages=False
        if self.extended:
            attrs={i:(self.f.attributes.iloc[i] if 'attributes' in self.f and isinstance(self.f.attributes.iloc[i],dict) else {}) for i in idx}
            def endpoint(name,typ):
                if not name or typ not in TYPES:raise ValueError('endpoint_type')
                if name in ent_nodes and ent_nodes[name]['type'] not in ('unknown',typ):raise ValueError('conflicting_entity_type')
                ent_nodes[name]={'id':name,'type':typ,'source':'trace'};extra.add(name);return name
            producers=defaultdict(list)
            key_indices={(str(self.f.traceID.iloc[i]),str(self.f.spanID.iloc[i])):i for i in idx}
            addresses={i:_message_address(a,self.kinds[i]=='PRODUCER') for i,a in attrs.items()
                       if self.kinds[i] in ('PRODUCER','CONSUMER')}
            has_messages=bool(addresses)
            def issue(reason,i):
                row=message_diagnostics.setdefault(reason,{'count':0,'witness':[]})
                row['count']+=1
                witness=(str(self.f.traceID.iloc[i]),str(self.f.spanID.iloc[i]))
                row['witness']=sorted(set(map(tuple,row['witness']))|{witness})[:2]
            for i,a in attrs.items():
                et=a.get('entity.type')
                if et:
                    if et not in TYPES:raise ValueError('entity_type')
                    ent_nodes[self.entities[i]]['type']=et
                witness=[(str(self.f.traceID.iloc[i]),str(self.f.spanID.iloc[i]))]
                if a.get('db.entity'):
                    dest=endpoint(a['db.entity'],a.get('db.type'))
                    if a.get('db.type') not in ('database','cache'):raise ValueError('database_type')
                    add(self.op[i],dest,DATA,'trace',witness=witness)
                if self.kinds[i]=='CLIENT' and a.get('peer.entity'):
                    dest=endpoint(a['peer.entity'],a.get('peer.type'))
                    # Không đếm lại endpoint nếu SERVER span đã làm witness cho cùng quan hệ.
                    covered=any(self.entities[j]==dest and self.kinds[j]=='SERVER' for j in children[pi==i])
                    if not covered:add(self.op[i],dest,SYNC,'trace',witness=witness)
                if a.get('host.id') and a.get('host.identity_verified') is True:
                    dest=endpoint(a['host.id'],'host');add(self.op[i],dest,DEPLOY,'trace',witness=witness)
                broker=a.get('messaging.broker');dest=a.get('messaging.destination')
                if broker and self.kinds[i] in ('PRODUCER','CONSUMER'):
                    endpoint(broker,'broker')
                    if self.kinds[i]=='PRODUCER':
                        add(self.op[i],broker,MESSAGE,'trace',witness=witness,destination=dest,messaging=addresses[i])
                        identity=_message_identity(a)
                        if identity is not None:producers[identity].append(i)
                    else:add(broker,self.op[i],MESSAGE,'trace',witness=witness,destination=dest,messaging=addresses[i])
            for i,a in attrs.items():
                if self.kinds[i]!='CONSUMER':continue
                if _queue_address(addresses[i]) is None:issue('queue_address_incomplete',i)
                linked=set()
                links=self.f.links.iloc[i] if 'links' in self.f and isinstance(self.f.links.iloc[i],list) else []
                verified=[link for link in links if isinstance(link,dict) and
                          link.get('semantics')=='message_creation' and link.get('semantics_verified') is True]
                if verified:
                    # Không thay bằng ID fallback khi link xác minh bị thiếu/mâu thuẫn.
                    for link in verified:
                        j=key_indices.get((str(link.get('traceID')),str(link.get('spanID'))))
                        if j is None:issue('link_source_unavailable',i)
                        elif self.kinds[j]!='PRODUCER':issue('link_source_not_producer',i)
                        elif _message_conflict(a,attrs[j]):issue('link_scope_conflict',i)
                        else:linked.add(j)
                else:
                    identity=_message_identity(a)
                    if identity is None:issue('identity_unverified',i)
                    else:
                        matches=producers.get(identity,[])
                        if not matches:issue('identity_no_source',i)
                        elif len(matches)>1:issue('identity_ambiguous',i)
                        elif _message_conflict(a,attrs[matches[0]]):issue('identity_scope_conflict',i)
                        else:linked.add(matches[0])
                if not linked:unresolved_messages+=1
                for j in sorted(linked):
                    address=dict(addresses[i])
                    for field in ('exchange','routing_key'):
                        if address[field] is None:address[field]=addresses[j][field]
                    add(self.op[j],self.op[i],MESSAGE,'inferred',witness=[(str(self.f.traceID.iloc[j]),str(self.f.spanID.iloc[j]),str(self.f.traceID.iloc[i]),str(self.f.spanID.iloc[i]))],destination=a.get('messaging.destination'),messaging=address)
        # Gộp qua phép chiếu; giữ nội bộ riêng, giữ deployment witness theo thao tác.
        internal_events=0
        for key,row in op_edges.items():
            src=op_nodes[row['source']]['entity'] if row['source'] in op_nodes else row['source']
            dst=op_nodes[row['target']]['entity'] if row['target'] in op_nodes else row['target']
            if src==dst or row['type']=='span-parent':
                internal_events+=row['event_count'] if src==dst else 0
                continue
            ek=edge_key(dict(row,source=src,target=dst))
            if ek not in ent_edges:ent_edges[ek]=dict(row,source=src,target=dst,event_count=0,witness=[])
            q=ent_edges[ek];q['event_count']+=row['event_count'];q['witness']=sorted(set(map(tuple,q['witness']))|set(map(tuple,row['witness'])))[:2]
        contained=(self.start[pi]<=self.start[children])&(self.end[children]<=self.end[pi])
        same=self.entities[pi]==self.entities[children]
        stats={'raw_spans':raw,'unique_spans':len(idx),'duplicate_rows':raw-len(idx),'roots':roots,
               'parent_references':len(idx)-roots,'resolved_parents':nresolved,'orphans':orphan,
               'same_entity_parent_events':int(same.sum()),'cross_entity_parent_events':int((~same).sum()),
               'parent_contains_child':int(contained.sum()),'parent_not_contains_child':int((~contained).sum()),
               'cross_parent_contains_child':int((contained&~same).sum()),'internal_edge_events':internal_events,
               'unresolved_messages':unresolved_messages,'missing_operation':int(self.f.loc[keep,'operationName'].isna().sum())}
        def sorted_edges(d):return sorted(d.values(),key=lambda r:tuple('' if x is None else x for x in edge_key(r)))
        coverage={e:('has_edge' if any(e in (x['source'],x['target']) for x in ent_edges.values()) else 'span_without_edge' if e in ent_nodes else 'not_observed') for e in sorted(self.universe)}
        entity={'level':'entity','interval_ns':interval,'nodes':[ent_nodes[k] for k in sorted(ent_nodes)],
                'edges':sorted_edges(ent_edges),'inventory':self.universe,'coverage':coverage,
                'outside_inventory':sorted(set(ent_nodes)-set(self.universe)),'stats':stats}
        operation={'level':'operation','interval_ns':interval,'nodes':[op_nodes[k] for k in sorted(op_nodes)],
                   'edges':sorted_edges(op_edges),'belongs_to':[[k,op_nodes[k]['entity']] for k in sorted(op_nodes)],
                   'component_context':[ent_nodes[k] for k in sorted(extra)],'stats':stats}
        if has_messages:
            entity['messaging_diagnostics']=message_diagnostics
            operation['messaging_diagnostics']=message_diagnostics
        return entity,operation

    def vocabulary(self, interval=None):
        keep=self.mask(interval);idx=np.flatnonzero(keep);p=self.parent
        children=idx[(p[idx]>=0)&keep[np.maximum(p[idx],0)]] if len(idx) else idx
        grouped=defaultdict(list)
        for i in children:grouped[int(p[i])].append(self.op[i])
        sigs=defaultdict(set)
        for i in idx:sigs[self.op[i]].add(tuple(sorted(set(grouped.get(int(i),[])))))
        counts=Counter(self.op[idx]);cross=Counter(self.op[children[self.entities[p[children]]!=self.entities[children]]])
        depths=np.full(len(self.f),-1,dtype=np.int32)
        # Memoization: mỗi span được duyệt một lần, không quét toàn bảng theo từng tầng.
        for i in idx:
            if depths[i]!=-1:continue
            chain=[];seen=set();j=int(i);depth=-1
            while depths[j]==-1:
                if j in seen:depth=-2;break
                seen.add(j);chain.append(j)
                parent=int(p[j])
                if parent<0 or not keep[parent] or self.entities[parent]!=self.entities[j]:break
                j=parent
            else:depth=int(depths[j])
            for j in reversed(chain):
                if depth!=-2:depth+=1
                depths[j]=depth
        cycle_count=int((depths[idx]==-2).sum())
        depth_max=pd.DataFrame({'op':self.op[idx],'depth':depths[idx]}).groupby('op').depth.max().to_dict()
        out=[]
        for oid in sorted(counts):
            e,o=json.loads(oid)
            out.append({'id':oid,'entity':e,'operation':o,'span_count':counts[oid],
                        'child_signature_count':len(sigs[oid]),'child_signatures':[list(s) for s in sorted(sigs[oid])],
                        'max_internal_depth':int(depth_max[oid]),'cross_entity_child_events':cross[oid]})
        return {'operations':out,'internal_span_cycle_count':cycle_count}


def build(spans, interval, aliases, universe):
    return Prepared(spans,aliases,universe).graph(interval)


def project(operation):
    """Chiếu độc lập tập nút/cạnh, không dùng đồ thị entity để hoàn thành phép chiếu."""
    owner=dict(operation['belongs_to'])
    nodes=set(owner.values())|{n['id'] for n in operation['component_context']}
    edges=set()
    for e in operation['edges']:
        s=owner.get(e['source'],e['source']);t=owner.get(e['target'],e['target'])
        if s!=t and e['type']!='span-parent':edges.add(edge_key(dict(e,source=s,target=t)))
    return nodes,edges
