# Branch-specific backpatch assessment

Use for a bug fix's stable-branch suitability, not automatic backport execution.
Check the current [support policy](https://www.postgresql.org/support/versioning/)
and the thread's backpatch discussion. Do not freeze a list of supported versions.

- Establish the regression/bug's first affected revision with history and a
  reproducer. Separate a pre-existing bug from a new-feature proposal.
- Inspect each requested branch's corresponding code, tests and interfaces in
  an isolated checkout. Record branch revision and whether the problem reproduces.
- Assess behavior compatibility, public/internal interfaces used by extensions,
  catalog/storage/WAL format, enum/structure layout, dependencies and portability.
  Small diffs can still carry compatibility risks. Stable branches may require
  a narrower fix than the development branch.
- Select branch-appropriate tests and build tools; independently apply/check and
  test the proposed adaptation. Clean applicability alone is insufficient.
- Report an affected-branch matrix, risk/benefit, unavailable evidence and a
  recommendation for human discussion. Committers decide acceptance; do not
  imply a backpatch decision based solely on this toolkit.

Never switch, reset or stash the user's checkout to inspect another branch.
