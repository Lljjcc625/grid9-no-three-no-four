# Publication / archival checklist

This checklist is deliberately scoped to publishing a durable public result, not journal peer review.

## Already present

- [x] Public standalone repository.
- [x] Explicit 15-point witness.
- [x] Retained target-16 exhaustive certificate.
- [x] Standalone certificate checker.
- [x] Separately implemented exhaustive cross-check.
- [x] Reproduction script and saved hashes.
- [x] Public preprint-preparation branch.

## Before freezing v1.0

- [ ] Read `paper/main.tex` end to end and confirm the author name to archive.
- [ ] Run `python3 scripts/audit.py --sanitizers` from a clean checkout.
- [ ] Build `paper/main.pdf` from the committed source.
- [ ] Confirm the PDF visually and check that all references resolve.
- [ ] Confirm the certificate and witness SHA-256 values against `manifests/certified-result.json`.
- [ ] Decide whether to keep the explicit AI-use disclosure unchanged.
- [ ] Replace `v1.0-prep` with `v1.0` in paper metadata and `CITATION.cff`.

## Freeze and archive

- [ ] Merge the publication-preparation branch after review.
- [ ] Create an annotated Git tag `v1.0`.
- [ ] Create a GitHub Release containing `paper/main.pdf` and a source archive.
- [ ] Connect the repository to Zenodo (or another archival service) and archive the release.
- [ ] Add the resulting DOI to `CITATION.cff`, the README, and the paper's data-availability section.

## Claims

Safe wording: this repository gives a reproducible computer-assisted proof that the exact maximum is 15.

Do not claim completed human peer review, proof-assistant formalization, or worldwide publication priority unless those facts later become true.
