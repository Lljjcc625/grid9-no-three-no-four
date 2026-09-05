"""Exact line/circle enumeration. Standard library only; point id = n*y+x."""
from itertools import combinations
from math import gcd
from functools import reduce
import argparse, hashlib, json
from pathlib import Path


def normalize(t):
    g = reduce(gcd, t)
    t = tuple(v // g for v in t)
    return tuple(-v for v in t) if next(v for v in t if v) < 0 else t


def line(a, b):
    u, v = b[1]-a[1], a[0]-b[0]
    return normalize((u, v, -u*a[0]-v*a[1]))


def circle(a, b, c):
    x, y = a
    u, v = b[0]-x, b[1]-y
    s, t = c[0]-x, c[1]-y
    A = u*t-v*s
    if A == 0:
        return None
    z = x*x+y*y
    p, q = b[0]**2+b[1]**2-z, c[0]**2+c[1]**2-z
    B, C = v*q-t*p, s*p-u*q
    return normalize((A, B, C, -A*z-B*x-C*y))


def generate(n):
    if not 1 <= n <= 30:
        raise ValueError('n must be between 1 and 30')
    points = [(x,y) for y in range(n) for x in range(n)]
    lines, circles = {}, {}
    for i,j in combinations(range(n*n), 2):
        lines.setdefault(line(points[i],points[j]), set()).update((i,j))
    for i,j,k in combinations(range(n*n), 3):
        key = circle(points[i],points[j],points[k])
        if key is not None:
            circles.setdefault(key, set()).update((i,j,k))
    return {'n':n, 'points':points,
            'lines':[{'equation':k,'points':sorted(v)} for k,v in sorted(lines.items()) if len(v)>=3],
            'circles':[{'equation':k,'points':sorted(v)} for k,v in sorted(circles.items()) if len(v)>=4]}


def edges(data):
    triples = sorted(t for group in data['lines'] for t in combinations(group['points'],3))
    quads = sorted(t for group in data['circles'] for t in combinations(group['points'],4))
    assert len(triples)==len(set(triples))
    assert len(quads)==len(set(quads))
    return triples,quads


def canonical_bytes(data):
    return (json.dumps(data,sort_keys=True,separators=(',',':'))+'\n').encode()


def save(data,path):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    raw=canonical_bytes(data); path.write_bytes(raw)
    t,q=edges(data)
    return {'n':data['n'],'lines':len(data['lines']),'circles':len(data['circles']),
            'collinear_triples':len(t),'concyclic_quadruples':len(q),'sha256':hashlib.sha256(raw).hexdigest()}

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--n',type=int,default=9);p.add_argument('--out',default='instances/grid9.json')
    a=p.parse_args();print(json.dumps(save(generate(a.n),a.out),indent=2))
