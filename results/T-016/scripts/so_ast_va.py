"""T-016 S2: so 5 file vá causal-learn/pyAgrum giữa RCD gốc (373882c) và RCAEval lib (259ea41) theo cây cú pháp
(bỏ docstring, so tập câu import riêng), và SHA-256 bản trong py38-rcdlock so với RCAEval lib."""
import ast
import hashlib

FS = ["causallearn/utils/PCUtils/SkeletonDiscovery.py", "causallearn/utils/Fas.py", "causallearn/graph/GraphClass.py",
      "causallearn/search/ConstraintBased/FCI.py", "pyAgrum/lib/image.py"]
G, R, E = "D:/RCA-ext/work/T-016/src/rcd/", "D:/RCA-ext/src/RCAEval/lib/", "D:/RCA-ext/envs/py38-rcdlock/Lib/site-packages/"


def norm(p):
    t = ast.parse(open(p, encoding="utf-8").read())
    for n in ast.walk(t):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Module)) and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(getattr(n.body[0], "value", None), ast.Constant) and isinstance(n.body[0].value.value, str):
            n.body = n.body[1:] or [ast.Pass()]
    imp = sorted(ast.dump(i) for i in t.body if isinstance(i, (ast.Import, ast.ImportFrom)))
    rest = ast.dump(ast.Module(body=[i for i in t.body if not isinstance(i, (ast.Import, ast.ImportFrom))], type_ignores=[]))
    return imp, rest


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


for f in FS:
    a, b = norm(G + f), norm(R + f)
    print(f"{f}: import {'giống' if a[0] == b[0] else 'KHÁC'}; thân {'giống' if a[1] == b[1] else 'KHÁC'}; "
          f"py38-rcdlock = RCAEval lib: {sha(E + f) == sha(R + f)}")
