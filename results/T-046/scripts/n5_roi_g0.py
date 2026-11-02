"""A/A và thật: tách qua cổng, cờ của G3 theo áp dụng G3 hay rơi G0; b trung vị. Không nhãn."""
import json,sys,statistics,collections
sys.path.insert(0,'results/T-046/scripts')
import t046
ca=t046.nap_luot('results/T-046/runs/b3-sua2-aa-001')
A=0.01
o={}
for x in ca.values():
    ds=x['dataset']
    for k in ('aa|R0','that|R0'):
        for u in x['cua_so'][k]['bang']['pv']:
            if not(u['hop_le'] and u['trong_U']): continue
            r=(u.get('khoi') or {}).get('roi_G0')
            for d,h in u['huong'].items():
                m=o.setdefault((ds,k,u['nhom'],r or 'G3'),{'n':0,'qua':0,'co':0})
                m['n']+=1;m['qua']+=int(h['p_G3']<A);m['co']+=int(h['p_G3']<A and h.get('chenh_duong',h.get('chenh',0)>0))
for k,m in sorted(o.items(),key=str): print(k,m,round(m['qua']/m['n'],4),round(m['co']/m['n'],4))
