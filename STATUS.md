# Verified status

## Mathematical claim

For the 9×9 integer grid `{0,...,8}²`, the maximum size of a subset with no three collinear points and no four concyclic points is **15**.

## Lower bound

`witnesses/witness15.json` contains an explicit 15-point set. `src/verify.py` checks all 455 triples and 1,365 quadruples using exact integer determinants.

## Upper bound

Target size 16 is certified UNSAT by the `GRIDPROOF 1` exhaustive-tree format. The independent checker accepted 6,313,888 nodes. The canonical uncompressed proof is 6,313,905 bytes with SHA-256:

`02d9106347ad5bdf4264d7301403fca1ad1b5cea6ea332999e9571d60107fd99`

Because every subset of a valid set is valid, exclusion of size 16 also excludes every larger size.

## Independent cross-check

`src/independent.cpp` is a separate pointwise exhaustive implementation. It rebuilds the geometry using different indexing and determinant code, uses no symmetry reduction, and exhausted 26,199,928 nodes with no size-16 solution.

## Historical independent reproduction

The completed research branch was independently reproduced by GitHub Actions run `33972726876`. The certificate/audit checkpoint is commit `02523ff0aed6ec59a58582ed4cd0b78c372344a3`, and the final handoff commit is `ddad281bf0412f721f7ad0626453e58f6edf8afb` in the source research repository.

## Trust boundary

This is a custom exhaustive-search certificate, not DRAT/LRAT and not a proof-assistant formalization. The mathematical invariant, the standalone checker, the C++ compiler/runtime and integer semantics remain trusted. Negative-certificate tests, deterministic replay, a second exhaustive implementation and CI reproduction reduce—but do not eliminate—that trusted base.
