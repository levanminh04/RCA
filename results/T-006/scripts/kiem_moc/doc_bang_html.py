import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.depth=0; s.row=None; s.cell=None; s.cap=None; s.incap=False
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='table': s.depth+=1; s.tables.append({'cap':'','rows':[]}) if s.depth==1 else None
        if s.depth>=1 and t=='tr': s.row=[]
        if s.depth>=1 and t in('td','th'): s.cell=''; s.span=int(a.get('colspan',1))
        if t=='math': s.inmath=True
    def handle_endtag(s,t):
        if t=='table': s.depth-=1
        if s.depth>=1 and t in('td','th') and s.cell is not None:
            s.row.extend([s.cell.strip()]*1+['']*(s.span-1)); s.cell=None
        if s.depth>=1 and t=='tr' and s.row is not None: s.tables[-1]['rows'].append(s.row); s.row=None
    def handle_data(s,d):
        if s.cell is not None: s.cell+=d
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
want=[int(x) for x in sys.argv[2].split(',')]
for i,t in enumerate(p.tables):
    if i in want:
        print('== table idx',i)
        for r in t['rows']: print(' | '.join(c.replace('\n',' ') for c in r))
