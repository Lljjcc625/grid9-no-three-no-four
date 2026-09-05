# Exact maximum: 15 points in the 9×9 grid

This repository contains a certificate-driven computer-assisted proof of the following finite geometry result.

Let

\[
G=\{0,1,\ldots,8\}\times\{0,1,\ldots,8\}.
\]

Among subsets \(S\subseteq G\) with

1. no three distinct points collinear, and
2. no four distinct points concyclic,

the exact maximum cardinality is

\[
\boxed{15}.
\]

Equivalently, a valid 15-point configuration exists and no valid 16-point configuration exists.

## Why this repository exists

The goal is not to preserve a solver's `UNSAT` line. The goal is to preserve a small, inspectable and reproducible proof pipeline.

The project separates four kinds of evidence:

- an explicit 15-point witness checked using exact integer arithmetic;
- a complete exhaustive-search proof certificate for the 16-point nonexistence claim;
- a standalone checker that reconstructs the geometry and validates every proof node;
- a separately implemented exhaustive search used as an independent cross-check.

The final checker does not require a commercial solver, a GPU, network access or nonstandard Python packages.

## Certified result

The historical proof run accepted **6,313,888 proof nodes**:

- 2,393,072 branching nodes;
- 3,372,584 row-bound leaves;
- 548,232 column-bound leaves.

A second point-by-point exhaustive implementation independently exhausted **26,199,928 nodes** without symmetry reduction and also found no valid 16-point set.

The canonical uncompressed certificate from the completed research run has SHA-256

```
02d9106347ad5bdf4264d7301403fca1ad1b5cea6ea332999e9571d60107fd99
```

A fresh GitHub Actions runner independently reproduced the audit in historical run `33972726876`. The source research handoff was finalized at commit `ddad281bf0412f721f7ad0626453e58f6edf8afb`, with the remote-certificate/audit checkpoint at `02523ff0aed6ec59a58582ed4cd0b78c372344a3`.

## Reproduce

With Python 3.11+ and a C++17 compiler:

```bash
python3 scripts/audit.py --sanitizers
```

See [`REPRODUCE.md`](REPRODUCE.md) for the individual stages and [`docs/certificate-format.md`](docs/certificate-format.md) for the proof grammar and coverage invariant.

## Trust boundary

This is a computer-assisted proof, not a Lean/Isabelle formalization and not a claim of human peer review. The retained method uses exact integer determinant tests, a documented exhaustive-search certificate format, an independently implemented checker, a second exhaustive implementation, cross-compiler runs, corruption tests and CI reproduction.

The certificate format is custom rather than DRAT/LRAT, so the checker and its documented invariants are part of the trusted computing base. The repository is structured to make that boundary explicit rather than hiding it behind solver output.

## Project history

The work began as an isolated subproject inside `Lljjcc625/no-four-in-plane-7x7x7-research` on branch `research/grid9-no-three-no-four-20260905`. It was split into this standalone public repository after the 9×9 result reached a completed, independently rechecked state.

No claim of publication priority is made here. The repository is intended to make the computation reproducible, auditable and useful as an example of certificate-driven finite mathematics.

## License

Code and repository text are released under the MIT License unless a file states otherwise.
