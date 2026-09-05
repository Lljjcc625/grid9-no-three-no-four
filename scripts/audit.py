#!/usr/bin/env python3
"""Reproduce and independently check the complete 9x9 result (stdlib + C++17)."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import shlex
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'instance': 'f08dda705dfc93c87abd34704ee7953dd3cded602ee68c33ccd7602120c4fbc5',
    'groups': 'a839c302019dc321cd9c339371b6cf54cabc99b0a1ded4d944e1d3d12c8c9157',
    'proof': '02d9106347ad5bdf4264d7301403fca1ad1b5cea6ea332999e9571d60107fd99',
    'witness': '5023e4e2decf9d3d6e61f758776752d1a498877102b544356368d32e195c7a2d',
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sanitizers', action='store_true', help='also replay producer/checker with undefined-behavior instrumentation')
    args = parser.parse_args()
    os.chdir(ROOT)
    for name in ('results', 'proofs', 'manifests', 'instances'):
        Path(name).mkdir(exist_ok=True)
    commands = []
    started = time.monotonic()
    compiler = shlex.split(os.environ.get('CXX', 'g++'))
    require(bool(compiler), 'empty compiler command')
    log = Path('results/audit.log').open('w', encoding='utf-8')

    def run(command: list[str], *, reject: bool = False) -> subprocess.CompletedProcess:
        start = time.monotonic()
        result = subprocess.run(command, text=True, capture_output=True, timeout=180, check=False)
        commands.append({'command': command, 'returncode': result.returncode, 'seconds': time.monotonic()-start})
        log.write('$ ' + shlex.join(command) + '\n' + result.stdout + result.stderr + '\n')
        log.flush()
        if reject:
            require(result.returncode != 0, 'invalid certificate accepted: ' + shlex.join(command))
        else:
            require(result.returncode == 0, 'command failed: ' + shlex.join(command) + '\n' + result.stderr)
        return result

    def data_run(command: list[str]) -> dict:
        return json.loads(run(command).stdout)

    def pinned(path: str, key: str) -> None:
        require(digest(Path(path)) == EXPECTED[key], 'hash mismatch: ' + path)

    def stable(data: dict) -> dict:
        return {k:v for k,v in data.items() if not k.endswith('seconds')}

    with tempfile.TemporaryDirectory(prefix='grid9-audit-') as tmp:
        temp = Path(tmp)
        compiler_version = run(compiler + ['--version']).stdout.splitlines()[0]
        enumeration = data_run([sys.executable, 'src/geometry.py', '--n', '9', '--out', 'instances/grid9.json'])
        pinned('instances/grid9.json', 'instance')
        run([sys.executable, 'src/pack.py'])
        pinned('instances/groups.txt', 'groups')
        run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'])
        pinned('witnesses/witness15.json', 'witness')
        witness = data_run([sys.executable, 'src/verify.py', 'witnesses/witness15.json', '--n', '9', '--size', '15'])
        require(witness['valid'] and witness['triples_checked']==455 and witness['quadruples_checked']==1365, 'invalid size15 witness')
        binaries = {}
        for name in ('prove', 'check_proof', 'independent'):
            binary = temp / name
            run(compiler + ['-O3', '-std=c++17', '-Wall', '-Wextra', 'src/' + name + '.cpp', '-o', str(binary)])
            binaries[name] = str(binary)
        retained = Path('proofs/n9-k16.trace.gz')
        retained_check = False
        if retained.exists():
            raw = gzip.decompress(retained.read_bytes())
            require(hashlib.sha256(raw).hexdigest()==EXPECTED['proof'], 'retained compressed proof does not match pinned uncompressed hash')
            retained_check = True
        proof = 'proofs/n9-k16.trace'
        generation = data_run([binaries['prove'], 'instances/groups.txt', '16', proof])
        pinned(proof, 'proof')
        require(Path(proof).stat().st_size == 6313905, 'wrong proof byte count')
        checked = data_run([binaries['check_proof'], proof, '9', '16'])
        expected_counts = {'status':'VERIFIED_UNSAT','n':9,'target':16,'nodes':6313888,
                           'row_bound_leaves':3372584,'column_bound_leaves':548232,
                           'branch_nodes':2393072,'collinear_triples':2712,
                           'zero_determinant_quadruples':29152}
        require(stable(checked)==expected_counts, 'unexpected certificate-check result')
        replay = temp / 'replay.trace'
        data_run([binaries['prove'], 'instances/groups.txt', '16', str(replay)])
        require(replay.read_bytes()==Path(proof).read_bytes(), 'nondeterministic proof regeneration')
        independent_edges = temp / 'independent-edges.txt'
        independent = data_run([binaries['independent'], '9', '16', '0', str(temp/'unexpected16.json'), str(independent_edges)])
        require(independent['status']=='EXHAUSTED' and independent['nodes']==26199928, 'independent search did not fully exhaust expected space')
        sys.path.insert(0, str(ROOT/'src'))
        from geometry import edges
        triples, quads = edges(json.loads(Path('instances/grid9.json').read_text()))
        direct = [tuple(map(int, line.split())) for line in independent_edges.read_text().splitlines()]
        primary = {(3,*e) for e in triples} | {(4,*e) for e in quads}
        require(len(direct)==len(set(direct)) and set(direct)==primary, 'independent forbidden-set mismatch')
        require(len(triples)==2712 and len(quads)==25996, 'wrong forbidden-set counts')
        small_json, small_groups, small_proof = (temp / x for x in ('grid4.json','groups4.txt','n4-k7.trace'))
        data_run([sys.executable,'src/geometry.py','--n','4','--out',str(small_json)])
        run([sys.executable,'src/pack.py','--instance',str(small_json),'--out',str(small_groups)])
        data_run([binaries['prove'],str(small_groups),'7',str(small_proof)])
        small = data_run([binaries['check_proof'],str(small_proof),'4','7'])
        require(small['status']=='VERIFIED_UNSAT' and small['nodes']==195, 'small proof check failed')
        raw = small_proof.read_bytes(); offset = raw.index(b'\n')+1
        corruptions = {
            'truncated': raw[:-1], 'trailing': raw+b'\0',
            'false-row-bound': raw[:offset]+b'\0'+raw[offset+1:],
            'invalid-branch': raw[:offset]+b'\xff'+raw[offset+1:],
            'wrong-magic': b'X'+raw[1:],
        }
        rejected = []
        for name, payload in corruptions.items():
            path = temp/(name+'.trace'); path.write_bytes(payload)
            run([binaries['check_proof'],str(path),'4','7'],reject=True)
            rejected.append(name)
        run([binaries['check_proof'],str(small_proof),'4','6'],reject=True)
        rejected.append('mismatched-target')
        sat_path = temp/'must-not-exist.trace'
        run([binaries['prove'],str(small_groups),'6',str(sat_path)],reject=True)
        require(not sat_path.exists(), 'SAT run retained a purported UNSAT certificate')
        sanitized = False
        if args.sanitizers:
            for name in ('prove','check_proof'):
                binary = temp/(name+'-ubsan')
                run(compiler + ['-O1','-std=c++17','-fsanitize=undefined','-fno-sanitize-recover=all','src/'+name+'.cpp','-o',str(binary)])
            sanitized_proof = temp/'sanitized.trace'
            data_run([str(temp/'prove-ubsan'),'instances/groups.txt','16',str(sanitized_proof)])
            require(digest(sanitized_proof)==EXPECTED['proof'], 'instrumented producer proof mismatch')
            sanitized_result=data_run([str(temp/'check_proof-ubsan'),str(sanitized_proof),'9','16'])
            require(stable(sanitized_result)==expected_counts, 'instrumented checker mismatch')
            sanitized = True
        with retained.open('wb') as target:
            with gzip.GzipFile(filename='',mode='wb',fileobj=target,compresslevel=9,mtime=0) as zipped:
                zipped.write(Path(proof).read_bytes())
        require(gzip.decompress(retained.read_bytes())==Path(proof).read_bytes(), 'compression round trip failed')
        summary = {
            'status':'VERIFIED', 'target16':'UNSAT', 'maximum':15,
            'certificate_check':stable(checked), 'independent_search':stable(independent),
            'witness_verification':witness, 'enumeration':enumeration,
            'geometry_cross_check':'ALL_28708_FORBIDDEN_SETS_EQUAL',
            'proof_replay':'BYTE_IDENTICAL','negative_tests_rejected':rejected,
            'sat_producer_refuses_certificate':True,
            'proof_sha256':EXPECTED['proof'],'witness_sha256':EXPECTED['witness'],
        }
        manifest = {
            'format':'GRIDPROOF 1','n':9,'target':16,'symmetry_reduction':False,
            'uncompressed':{'path':proof,'bytes':Path(proof).stat().st_size,'sha256':digest(Path(proof))},
            'compressed':{'path':str(retained),'bytes':retained.stat().st_size,'sha256':digest(retained)},
            'sources':{str(p.relative_to(ROOT)):digest(p) for p in sorted((ROOT/'src').glob('*')) if p.is_file()},
            'witness':{'path':'witnesses/witness15.json','sha256':EXPECTED['witness']},
        }
        write_json(Path('results/audit-summary.json'),summary)
        write_json(Path('manifests/certificate.json'),manifest)
        write_json(Path('results/audit-environment.json'),{
            'python':sys.version,'compiler':compiler_version,'platform':platform.platform(),
            'elapsed_seconds':time.monotonic()-started,'commands':commands,
            'retained_compressed_proof_checked':retained_check,
            'full_undefined_behavior_sanitizer_replay_passed':sanitized,
        })
        print(json.dumps(summary,indent=2,sort_keys=True))
    log.close()


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('AUDIT FAILED: ' + str(exc),file=sys.stderr)
        raise SystemExit(1)
