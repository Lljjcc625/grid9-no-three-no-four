# Paper

This directory contains the public preprint preparation draft for the certified result

\[
f(9)=15,
\]

where `f(9)` is the maximum size of a subset of the 9x9 integer grid with no three collinear and no four concyclic points.

## Build

From this directory:

```bash
latexmk -pdf main.tex
```

The current draft is self-contained and does not require BibTeX to build; `references.bib` is retained as structured citation metadata for later archival use.

## Status

`v1.0-prep` is a publication-preparation draft. The mathematics is backed by the repository's retained certificate and verification suite, but this version is not claimed to be peer reviewed and has no DOI yet.

Before freezing `v1.0`, replace the GitHub-handle author name with the preferred archival author name if desired, perform a final human read-through, then create a GitHub Release and an archival deposit.
