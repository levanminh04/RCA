import hashlib, sys, tarfile, os
def tu_tar(f):
    t = tarfile.open(fileobj=f, mode='r|')
    out = {}
    for m in t:
        if m.isfile() and m.name.endswith('.py'):
            out[m.name] = hashlib.sha256(t.extractfile(m).read()).hexdigest()
    return out
def tu_thu_muc(d):
    out = {}
    for r, _, fs in os.walk(d):
        for x in fs:
            if x.endswith('.py'):
                p = os.path.join(r, x)
                out[os.path.relpath(p, d).replace(os.sep, '/')] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    return out
h = tu_tar(sys.stdin.buffer) if sys.argv[1] == '-' else tu_thu_muc(sys.argv[1])
print(len(h), hashlib.sha256(''.join(k + v for k, v in sorted(h.items())).encode()).hexdigest()[:16])
