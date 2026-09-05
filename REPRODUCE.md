# Reproduce and audit the exact maximum 15

## Fresh checkout

```bash
git clone https://github.com/Lljjcc625/grid9-no-three-no-four.git
cd grid9-no-three-no-four
python3 scripts/audit.py --sanitizers
```

The audit script performs no network requests, Git writes or package installations.

Requirements: Python 3.11+ standard library and a C++17 compiler supporting `unsigned __int128`. GCC on Linux/WSL and GitHub Actions `ubuntu-24.04` are the reference environments. Set `CXX` to select another compiler. Omit `--sanitizers` only if you do not want the additional undefined-behavior-instrumented replay.

The final proof pipeline does not require SciPy, NumPy, SAT packages, a GPU or a commercial solver.

## Fast witness check

```bash
python3 src/verify.py witnesses/witness15.json --n 9 --size 15
```

Expected result: `valid: true`, with 455 triples and 1,365 quadruples checked.

## Regenerate and check the size-16 certificate

```bash
mkdir -p instances proofs results
g++ -O3 -std=c++17 -Wall -Wextra src/prove.cpp -o prove
g++ -O3 -std=c++17 -Wall -Wextra src/check_proof.cpp -o check_proof
python3 src/geometry.py --n 9 --out instances/grid9.json
python3 src/pack.py
./prove instances/groups.txt 16 proofs/n9-k16.trace
printf '%s  %s\n' '02d9106347ad5bdf4264d7301403fca1ad1b5cea6ea332999e9571d60107fd99' 'proofs/n9-k16.trace' | sha256sum -c -
./check_proof proofs/n9-k16.trace 9 16
```

Expected checker result: `VERIFIED_UNSAT`; 6,313,888 nodes, 3,372,584 row-bound leaves, 548,232 column-bound leaves and 2,393,072 branch nodes.

The producer has no node limit and no symmetry reduction. Its input groups have capacity 2 for maximal lines and capacity 3 for maximal circles. The checker does not trust that incidence file: it independently rebuilds geometry from grid coordinates using exact integer determinants.

Pinned SHA-256 identities:

```text
instances/grid9.json
f08dda705dfc93c87abd34704ee7953dd3cded602ee68c33ccd7602120c4fbc5

instances/groups.txt
a839c302019dc321cd9c339371b6cf54cabc99b0a1ded4d944e1d3d12c8c9157

proofs/n9-k16.trace
02d9106347ad5bdf4264d7301403fca1ad1b5cea6ea332999e9571d60107fd99

witnesses/witness15.json
5023e4e2decf9d3d6e61f758776752d1a498877102b544356368d32e195c7a2d
```

## Independent exhaustive search

```bash
g++ -O3 -std=c++17 -Wall -Wextra src/independent.cpp -o independent
./independent 9 16 0 results/unexpected16.json instances/independent-edges.txt
```

Expected result: `EXHAUSTED`, 26,199,928 nodes. A nonzero node limit may return `UNKNOWN`; `UNKNOWN` is never treated as proof.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

The one-command audit also compares all 28,708 genuine forbidden sets, regenerates the full certificate twice and requires byte identity, rejects deliberately corrupted small certificates, checks that a satisfiable small case cannot produce an UNSAT certificate, verifies the 15-point witness and optionally replays the full producer/checker with undefined-behavior instrumentation.

## Historical provenance

The completed source research was originally isolated under `grid9/` in `Lljjcc625/no-four-in-plane-7x7x7-research`, branch `research/grid9-no-three-no-four-20260905`.

- historical GitHub Actions run: `33972726876`
- certificate/audit checkpoint: `02523ff0aed6ec59a58582ed4cd0b78c372344a3`
- final handoff commit: `ddad281bf0412f721f7ad0626453e58f6edf8afb`
- historical Actions artifact ID: `9971408408`
- historical outer ZIP SHA-256: `167cd76fb3dc01ecacdf3a2b93e359bf0eb1b2e4c137786584fd9122b0ae633b`

The public repository's CI regenerates the compressed certificate from source so the result does not depend on the historical private repository or artifact-retention lifetime.
