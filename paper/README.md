# Paper

This directory contains preprint v1.0 for the certified result

\[
f(9)=15,
\]

where `f(9)` is the maximum size of a subset of the 9x9 integer grid with no three collinear and no four concyclic points.

**Author:** Jinchen Li (Independent Researcher, China)  
**Reserved Zenodo DOI:** `10.5281/zenodo.22368316`

The DOI becomes registered when the Zenodo record is published.

## Build

From this directory:

```bash
latexmk -pdf main.tex
```

The current draft is self-contained and does not require BibTeX to build; `references.bib` is retained as structured citation metadata for archival use.

## Publication status

This is a computer-assisted proof preprint, not a claim of completed peer review. The mathematical result is backed by the repository's retained certificate and verification suite. The paper text is intended for release under CC BY 4.0; repository code remains under the repository's MIT license.

Before the final GitHub `v1.0` tag, perform one clean replay and visually inspect the PDF produced from the committed source.
