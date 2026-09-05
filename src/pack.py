"""Convert deterministic exact JSON groups to a compact C++ search input."""
import json,argparse,hashlib
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--instance',default='instances/grid9.json');p.add_argument('--out',default='instances/groups.txt');a=p.parse_args()
d=json.loads(Path(a.instance).read_text());groups=[(2,g['points']) for g in d['lines']]+[(3,g['points']) for g in d['circles']]
s=f"{d['n']} {len(groups)}\n"+''.join(f"{cap} {len(pts)} "+' '.join(map(str,pts))+'\n' for cap,pts in groups)
Path(a.out).write_text(s);print(hashlib.sha256(s.encode()).hexdigest())
