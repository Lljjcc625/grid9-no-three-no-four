# Publication / archival checklist

This checklist is scoped to creating a durable public Zenodo preprint, not journal peer review.

## Already present

- [x] Public standalone repository.
- [x] Explicit 15-point witness.
- [x] Retained target-16 exhaustive certificate.
- [x] Standalone certificate checker.
- [x] Separately implemented exhaustive cross-check.
- [x] Reproduction script and saved hashes.
- [x] Public preprint-preparation branch.
- [x] Archival author name confirmed as **Jinchen Li**.
- [x] Zenodo DOI reserved: **10.5281/zenodo.22368316**.
- [x] Reserved DOI inserted into the paper and citation metadata.

## Before freezing v1.0

- [ ] Read `paper/main.tex` end to end once.
- [ ] Run `python3 scripts/audit.py --sanitizers` from a clean checkout.
- [x] Build `paper/main.pdf` from the publication source.
- [x] Visually inspect the PDF for clipping/overlap/layout defects.
- [ ] Confirm the certificate and witness SHA-256 values against `manifests/certified-result.json` after the final clean replay.
- [ ] Confirm the AI-use disclosure is accepted as written.

## Freeze and archive

- [ ] Merge the publication-preparation branch after review.
- [ ] Create an annotated Git tag `v1.0`.
- [ ] Create a GitHub Release containing `paper/main.pdf` and the paper source archive.
- [ ] In the existing Zenodo draft, select `Publication / Preprint` and upload the final PDF (and optionally the paper-source ZIP).
- [ ] Publish the Zenodo record so DOI `10.5281/zenodo.22368316` becomes registered.
- [ ] Verify the public Zenodo landing page and DOI resolution.

## Claims

Safe wording: this repository and preprint give a reproducible computer-assisted proof that the exact maximum is 15.

Do not claim completed human peer review, proof-assistant formalization, or worldwide publication priority unless those facts later become true.
