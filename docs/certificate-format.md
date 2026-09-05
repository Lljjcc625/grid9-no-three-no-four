# GRIDPROOF version 1: certificate grammar and soundness

## Accepted result

The complete `n=9,target=16` certificate was accepted in the original sandbox, independently reproduced in GitHub Actions run `33972726876`, and accepted again after downloading the remote artifact. It contains 6,313,888 proof nodes. Its uncompressed SHA-256 is `02d9106347ad5bdf4264d7301403fca1ad1b5cea6ea332999e9571d60107fd99`.

This is a custom finite exhaustive-search certificate, not a DRAT/LRAT or proof-assistant proof. The checker does not trust the producer's geometry database, symmetry claims, branch heuristic, node totals or status strings.

## Format

ASCII header: `GRIDPROOF 1 n target\n`.
Then one byte per node in preorder:

- byte 0: row-capacity terminal;
- byte 1: column-capacity terminal;
- byte 16+r: branch on unprocessed row r.

Every required child subtree follows immediately. No other byte is valid. The checker consumes the whole file exactly, rejecting truncation and trailing bytes. The expected n and target are independently supplied on the command line and must match the header.

## State invariant

A state has a valid selected set S, unprocessed rows R, and candidate set A. A is exactly the points in R individually compatible with S. Initially S is empty, R comprises all rows, and A is the grid. Adding p removes p, points completing a collinear triple with p and one old selected point, and points completing a zero-determinant quadruple with p and two old selected points. This accounts for all newly possible forbidden subsets. Processing a row removes the entire row from A and R. Thus the invariant is preserved inductively.

The checker reconstructs all geometric masks from coordinates. It tests every triple by integer shoelace area and every quadruple by the full 24-term Leibniz determinant with rows `[x^2+y^2,x,y,1]`. Four-collinear zero determinants are harmless additional exclusions: any such set already violates the triple condition. On a set with no collinear triple, zero determinant is equivalent to four points lying on the unique circle through the first three.

## Terminal soundness

Put q=target-|S|. Each remaining row r permits at most `min(2, |A intersect row r|)` additional points. Their sum U is therefore an upper bound. A byte-0 node is accepted only when U<q.

For each column c, at most `min(2-|S intersect column c|, |A intersect column c|)` additional points can be selected. A byte-1 node is accepted only when the sum of these values is less than q.

These are integer bounds derived solely from the prohibition on collinear triples. No numerical optimization or unproved structural lemma is involved.

## Branch coverage and induction

At a byte-(16+r) node, r must be an unprocessed row. Let `u_r=min(2, |A intersect row r|)` and `lower=max(0, q-(U-u_r))`. Every valid completion must select at least lower and at most two points in row r, and cannot exceed q.

The checker explicitly enumerates every such geometry-compatible choice: increasing pairs first, increasing singletons next, then the empty choice when allowed. It recursively requires a certificate for every choice. Incompatible choices cannot belong to a valid completion by the state invariant. Choices below lower cannot reach the target by the remaining-row upper bound. Hence, if all required children exclude every completion, their parent excludes every completion. A branch with no possible child is vacuously closed by exhaustive coverage.

Each branch removes one row, so the tree is finite. Reaching the target size is rejected, never accepted as a proof leaf. Induction from checked terminals to the initial full-grid state proves that an accepted file certifies UNSAT for the pinned n,target. No symmetry reduction, orbit assumption or external case-family manifest is used.

## Arithmetic and trust boundary

For n<=9, a 4x4 determinant product has absolute value at most 128*8*8=8192. The sum of 24 terms has absolute value at most 196608. Signed 64-bit integers are ample. Bitset indices are at most 80. Floating point is used only for elapsed-time reporting, never for geometry, capacities or proof acceptance.

The trust boundary is the induction above, the C++ checker implementation/compiler/runtime, and integer semantics. This is not a proof-assistant kernel. A separately implemented pointwise exhaustive search corroborates the result, visiting 26,199,928 nodes with independently generated geometry and no symmetry reduction.

## Executed checks

Full proof regeneration was byte-identical. All 2,712 collinear triples and 25,996 genuine circle quadruples matched the independently generated sets. Full producer/checker replay under undefined-behavior instrumentation passed in both the local and fresh-run environments.

Small-certificate negative tests rejected truncation, trailing bytes, a false row-bound leaf, an invalid branch byte, an invalid magic header and a mismatched expected target. A satisfiable `n=4,target=6` run refused to retain an UNSAT certificate. These tests supplement, rather than replace, the soundness and coverage argument.
