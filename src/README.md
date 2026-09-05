# Trusted computational core

The final result is intentionally split across independently motivated components.

- `prove.cpp` produces a complete `GRIDPROOF 1` exhaustive-tree certificate for target 16. It uses no symmetry reduction and has no node limit.
- `check_proof.cpp` does **not** read the producer's incidence database. Given only the certificate, `n` and `target`, it reconstructs collinearity and zero circle determinants directly from integer grid coordinates and checks full branch coverage.
- `independent.cpp` is a second exhaustive search with different point indexing, determinant code and branching structure. It does not consume the primary certificate or packed geometry.
- `geometry.py` and `pack.py` deterministically generate the primary producer input.
- `verify.py` independently checks explicit witnesses by enumerating every triple and quadruple.

The intended trust boundary and the induction proving certificate coverage are documented in `../docs/certificate-format.md`.
