"""Independent exhaustive verifier; does NOT import generator/search code."""
import argparse, hashlib, json
from itertools import combinations, permutations
from math import comb
from pathlib import Path


def determinant(rows):
    n=len(rows); total=0
    for p in permutations(range(n)):
        term=(-1)**sum(p[i]>p[j] for i in range(n) for j in range(i+1,n))
        for i in range(n): term*=rows[i][p[i]]
        total+=term
    return total


def verify(points,n=9,expected=None):
    if expected is not None and len(points)!=expected:
        raise ValueError('wrong cardinality')
    if any(len(p)!=2 or any(type(v) is not int or not 0<=v<n for v in p) for p in points):
        raise ValueError('coordinates must be in-range integers')
    if len({tuple(p) for p in points})!=len(points): raise ValueError('duplicate points')
    bad_t=[];bad_q=[]
    for t in combinations(points,3):
        if determinant([[x,y,1] for x,y in t])==0: bad_t.append(t)
    for q in combinations(points,4):
        if determinant([[x*x+y*y,x,y,1] for x,y in q])==0: bad_q.append(q)
    return {'valid':not bad_t and not bad_q,'n':n,'size':len(points),
            'triples_checked':comb(len(points),3),'quadruples_checked':comb(len(points),4),
            'collinear_triples':bad_t,'zero_circle_determinant_quadruples':bad_q}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('witness');p.add_argument('--n',type=int,default=9);p.add_argument('--size',type=int)
    a=p.parse_args(); raw=Path(a.witness).read_bytes(); data=json.loads(raw)
    points=data['points'] if isinstance(data,dict) else data
    result=verify(points,a.n,a.size);result['witness_sha256']=hashlib.sha256(raw).hexdigest()
    print(json.dumps(result,indent=2)); raise SystemExit(0 if result['valid'] else 1)
