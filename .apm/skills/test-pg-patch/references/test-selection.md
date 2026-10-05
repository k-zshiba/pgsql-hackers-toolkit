# Choose validation from the current tree

Read local `src/test/README`, `src/test/perl/README`,
`src/test/isolation/README`, the relevant `GNUmakefile`/`Makefile` and
`meson.build`, plus branch-matching documentation. Online starting points:
[regression tests](https://www.postgresql.org/docs/devel/regress.html),
[TAP](https://www.postgresql.org/docs/devel/regress-tap.html),
[Meson](https://www.postgresql.org/docs/devel/install-meson.html).

| Risk | Likely infrastructure | Verify before using |
| --- | --- | --- |
| SQL-visible semantics/errors | pg_regress SQL and expected output | Schedule prerequisites, expected ordering, locale, planned output |
| Concurrent SQL behavior | Isolation specs and permutations | Expected interleavings, blocking points, termination and determinism |
| Restart, replication, backup, CLI, multi-node state | TAP suites | Cluster helpers, TAP enabled, Perl dependencies, logs and cleanup |
| Extension/contrib changes | That module's regression/TAP suite | Build/install prerequisites and test registration |
| New nodes/catalogs/generated code | Build plus relevant semantic tests | Generator inputs, tracked outputs, both supported build systems |
| Memory/resource lifetime or UB | Assertions, warnings, suitable sanitizers | Compiler/build flags, false positives, platform dependencies |
| Broad shared infrastructure | Impacted suites, then wider tests | What the broad command actually covers and excludes |
| Performance claim | Reproducible comparison on equivalent builds | Dataset/configuration, repetitions, variance and correctness |

Make and Meson coexist on some branches. Inspect the selected branch rather
than requiring tools absent from it. In Make builds, look for `check`,
`check-world`, directory-specific targets, `check-tests` and `PROVE_TESTS`
handling where defined. Test setup and prerequisite schedules matter: an
isolated SQL test may depend on objects created by earlier tests.

For configured Meson builds, `meson test -C <build-dir> --list` discovers names.
Inspect setup suites and the temporary installation's freshness before selecting
subsets. Selecting a single TAP test must not silently test stale binaries.
Use the tree's suite names; online examples may belong to a different revision.

Prefer temporary instances and non-root test execution. Test suites can remove
their own test data directories: verify paths and avoid live clusters. Commands
requiring network services or special extra suites must be identified in the plan.

Expected files are assertions, not snapshots to replace after any failure.
Inspect `regression.diffs`, TAP script/postmaster logs and retained node state.
Fix semantics or nondeterminism when those caused the difference. Record skips
and disabled suites, including TAP tests omitted by build configuration.
