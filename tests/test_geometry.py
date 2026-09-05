import sys, unittest, random
from pathlib import Path
from itertools import combinations
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from geometry import generate,edges,circle,line,canonical_bytes
from verify import verify,determinant

class GeometryTests(unittest.TestCase):
    def test_basic(self):
        self.assertFalse(verify([(0,0),(1,1),(2,2)])['valid'])
        self.assertFalse(verify([(0,0),(1,0),(1,1),(0,1)])['valid'])
        self.assertTrue(verify([(0,0),(1,0),(2,1),(0,2)])['valid'])
        for pts in [[(0,0),(0,0)],[(9,0)],[(0.0,0)]]:
            with self.assertRaises(ValueError):verify(pts)
    def test_small_exhaustive(self):
        for n in (2,3,4):
            data=generate(n);pts=data['points'];t,q=edges(data)
            td={s for s in combinations(range(n*n),3) if determinant([[*pts[i],1] for i in s])==0}
            qd={s for s in combinations(range(n*n),4) if determinant([[pts[i][0]**2+pts[i][1]**2,*pts[i],1] for i in s])==0 and not any(z in td for z in combinations(s,3))}
            self.assertEqual(set(t),td);self.assertEqual(set(q),qd)
            self.assertEqual(canonical_bytes(data),canonical_bytes(generate(n)))
    def test_d4_and_random(self):
        d=generate(9);pts=d['points'];t,q=edges(d);ts,qs=set(t),set(q)
        for flip in (False,True):
            for turns in range(4):
                perm=[]
                for x,y in pts:
                    if flip:x=8-x
                    for _ in range(turns):x,y=8-y,x
                    perm.append(y*9+x)
                self.assertEqual(ts,{tuple(sorted(perm[i] for i in e)) for e in ts})
                self.assertEqual(qs,{tuple(sorted(perm[i] for i in e)) for e in qs})
        rng=random.Random(20260905)
        for _ in range(200):
            ids=sorted(rng.sample(range(81),rng.randrange(3,18)));chosen=set(ids)
            bad=any(set(e)<=chosen for e in ts) or any(set(e)<=chosen for e in qs)
            self.assertEqual(not bad,verify([pts[i] for i in ids])['valid'])
    def test_n3_bruteforce_maximum(self):
        d=generate(3);t,q=edges(d);forbidden=[sum(1<<i for i in e) for e in t+q]
        best=max(m.bit_count() for m in range(1<<9) if not any(m&e==e for e in forbidden))
        self.assertEqual(best,5)

if __name__=='__main__':unittest.main()
