---
name: test-pg-patch
description: Select, run and interpret validation for a PostgreSQL upstream/core patch using the actual checkout's build, regression, TAP, isolation or contrib infrastructure. Use for changed source behavior and contributor testing plans. Do not use for application unit tests, production database checks or routine query benchmarking.
---

# Test a PostgreSQL patch

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Read [test selection](references/test-selection.md) for infrastructure-specific
choices; use it as a discovery guide, not a command cookbook.

Establish checkout/revision, diff, reproducer, build directory/system, compiler,
configure/Meson options, assertions, TAP availability and platform. Verify that
the executable under test was rebuilt from the changed source. Inspect actual
Makefiles/Meson registrations and list available tests. Never invent a test name,
target or result; avoid running installcheck against an existing database by default.

Select tests by the behavior at risk. Start with a discriminating reproducer and
targeted cases; cover normal, boundary and error paths. For bugs, compare suitable
unpatched and patched trees/builds without altering the user's state. Consider
concurrency schedules, recovery/restart, permissions, locale/encoding and
platform differences where applicable. Check test determinism and registrations.

Run an appropriate build with compiler warnings and assertions, then chosen
tests. Broaden to impacted subsystem/contrib suites and wider suites as risk
warrants. Consider sanitizer configurations for lifetime/undefined-behavior
changes; verify supported flags and dependencies in the current tree/toolchain.
Do not describe sanitizers or platform coverage as performed when unavailable.

For each run record command, working directory, revision, configuration, exit
status, pass/fail/skip and useful log locations. Diagnose logs and expected-output
diffs before changing expectations. Distinguish patch failures, reproducible
baseline failures and environment problems. Do not silence or skip a failing
test merely to get green output.

Return a compact validation matrix plus unexplored risks and next useful tests.
If build dependencies or time/resources prevent a required run, report the
blocker and a reproducible plan. Test evidence applies to the tested revision;
changes made afterward require proportionate revalidation.
