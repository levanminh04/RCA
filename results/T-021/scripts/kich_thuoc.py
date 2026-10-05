"""T-021: dung lượng từng bộ con RCAEval theo cây file Hugging Face đã lưu ở T-002 (không tải).
Chạy: py -3 -X utf8 results/T-021/scripts/kich_thuoc.py --run kich-thuoc-001
"""
import argparse, collections, json, os
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
ap = argparse.ArgumentParser(); ap.add_argument('--run', required=True); a = ap.parse_args()
out_dir = os.path.join(ROOT, 'results/T-021/runs', a.run); os.makedirs(out_dir, exist_ok=False)
src = 'results/T-002/public-metadata/run-002/hf-tree.json'
tree = json.load(open(os.path.join(ROOT, src), encoding='utf-8'))
b, n = collections.Counter(), collections.Counter()
for it in tree:
    if it['type'] == 'file' and '/' in it['path']:
        s = it['path'].split('_')[0]
        b[s] += it.get('size') or 0
        n[s] += 1
out = {'nguon': src, 'bo': {k: {'so_file': n[k], 'byte': b[k]} for k in sorted(b)}}
json.dump(out, open(os.path.join(out_dir, 'ket-qua.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False))
