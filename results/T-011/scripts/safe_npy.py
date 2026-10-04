"""Static reader for this release's NumPy pickle subset; never imports/calls payload globals.

GLOBAL and REDUCE are interpreted as inert tagged records. Unknown globals/opcodes
are rejected. This does not use pickle.load or NumPy allow_pickle=True.
"""
import ast, pickletools, struct

class Tag:
    def __init__(self, name, args=()): self.name, self.args, self.state = name, args, None

ALLOWED = {'numpy.core.multiarray _reconstruct', 'numpy ndarray',
           'numpy dtype', 'numpy.core.multiarray scalar'}

def read_npy(data):
    if data[:6] != b'\x93NUMPY': raise ValueError('not NPY')
    v=data[6]; width=2 if v==1 else 4
    n=int.from_bytes(data[8:8+width],'little'); offset=8+width+n
    header=ast.literal_eval(data[8+width:offset].decode('latin1'))
    if header['descr'] != '|O': raise ValueError('unexpected NPY dtype')
    stack=[]; memo={}; marker=object()
    def marked():
        i=len(stack)-1
        while stack[i] is not marker: i-=1
        out=stack[i+1:]; del stack[i:]; return out
    for op,a,p in pickletools.genops(data[offset:]):
        k=op.name
        if k=='PROTO':
            if a!=3: raise ValueError('unexpected protocol')
        elif k=='GLOBAL':
            if a not in ALLOWED: raise ValueError('forbidden global '+a)
            stack.append(Tag(a))
        elif k in ('BINUNICODE','SHORT_BINBYTES','BINBYTES','BININT','BININT1','BININT2','LONG1','BINFLOAT'): stack.append(a)
        elif k=='NONE': stack.append(None)
        elif k=='NEWTRUE': stack.append(True)
        elif k=='NEWFALSE': stack.append(False)
        elif k=='MARK': stack.append(marker)
        elif k=='EMPTY_TUPLE': stack.append(())
        elif k=='EMPTY_LIST': stack.append([])
        elif k=='EMPTY_DICT': stack.append({})
        elif k.startswith('TUPLE'):
            if k=='TUPLE': stack.append(tuple(marked()))
            else:
                count=int(k[-1]); values=stack[-count:]; del stack[-count:]; stack.append(tuple(values))
        elif k in ('BINPUT','LONG_BINPUT'): memo[a]=stack[-1]
        elif k in ('BINGET','LONG_BINGET'): stack.append(memo[a])
        elif k=='REDUCE':
            args=stack.pop(); fn=stack.pop()
            if not isinstance(fn,Tag) or fn.name not in ALLOWED: raise ValueError('invalid REDUCE')
            stack.append(Tag(fn.name,args))
        elif k=='BUILD':
            state=stack.pop()
            if not isinstance(stack[-1],Tag): raise ValueError('invalid BUILD')
            stack[-1].state=state
        elif k=='APPEND':
            value=stack.pop(); stack[-1].append(value)
        elif k=='APPENDS':
            values=marked(); stack[-1].extend(values)
        elif k=='SETITEM':
            value=stack.pop(); key=stack.pop(); stack[-1][key]=value
        elif k=='SETITEMS':
            values=marked()
            if len(values)%2: raise ValueError('odd SETITEMS')
            stack[-1].update(zip(values[::2],values[1::2]))
        elif k=='STOP':
            if len(stack)!=1: raise ValueError('unbalanced stack')
            obj=stack[0]
            if obj.name!='numpy.core.multiarray _reconstruct': raise ValueError('unexpected top object')
            state=obj.state
            if state[1]!=() or not isinstance(state[-1],list) or len(state[-1])!=1: raise ValueError('unexpected object container')
            return header,state[-1][0]
        else: raise ValueError('forbidden opcode '+k)
    raise ValueError('missing STOP')

def numeric(tag):
    if not isinstance(tag,Tag): return tag
    if tag.name=='numpy.core.multiarray scalar':
        dtype,raw=tag.args; fmt={'i8':'q','f8':'d'}[dtype.args[0]]
        return struct.unpack('<'+fmt,raw)[0]
    raise ValueError('non-scalar numeric')

def array_info(tag):
    if tag.name!='numpy.core.multiarray _reconstruct': raise ValueError('not ndarray')
    version,shape,dtype,fortran,raw=tag.state
    code=dtype.args[0]; endian=dtype.state[1]
    if code not in ('f8','i8','i4') or endian not in ('<','='): raise ValueError('unexpected primitive dtype')
    count=1
    for n in shape: count*=n
    if not isinstance(raw,bytes) or len(raw)!=count*int(code[1:]) or fortran: raise ValueError('shape/bytes/order mismatch')
    return shape,code,raw

def selfcheck():
    # Hostile input is rejected before any interpretation that could call code.
    header=b"{'descr': '|O', 'fortran_order': False, 'shape': (), }\n"
    payload=b'\x93NUMPY\x01\x00'+len(header).to_bytes(2,'little')+header+b'\x80\x03cos\nsystem\n.'
    try: read_npy(payload)
    except ValueError as e: assert 'forbidden global' in str(e)
    else: raise AssertionError('hostile GLOBAL accepted')
    a=Tag('numpy.core.multiarray _reconstruct'); d=Tag('numpy dtype',('f8',)); d.state=(3,'<')
    a.state=(1,(2,2),d,False,struct.pack('<dddd',1,2,3,4))
    shape,code,raw=array_info(a); assert shape==(2,2) and list(struct.iter_unpack('<d',raw))==[(1.,),(2.,),(3.,),(4.,)]
    a.state=(1,(2,3),d,False,raw)
    try: array_info(a)
    except ValueError: pass
    else: raise AssertionError('shape mismatch accepted')

if __name__=='__main__': selfcheck(); print('safe subset checks passed')
