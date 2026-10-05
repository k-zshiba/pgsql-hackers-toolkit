---
name: review-pg-patch
description: Critically review a PostgreSQL upstream/core patch, CommitFest submission or author self-review for correctness, tests, compatibility and community readiness. Use when asked to find problems in a core diff. Do not use for SQL/application reviews, routine database tuning or implementing a feedback revision.
---

# Review a PostgreSQL patch

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Identify the patch version/series, base revision, author intent, whole discussion,
previous review and CommitFest record. Verify latest attachments and prerequisites.
Review is about finding problems and exposing uncertainty; do not simply restate
the author's rationale or accept existing green CI as sufficient.

Check applicability in an isolated tree, with a non-mutating applicability check
first when appropriate. Record conflicts and version mismatch rather than
rewriting the user's dirty checkout. Read analogous source, callers/callees,
invariants, history and tests to challenge the patch's assumptions.

Review relevant risks: functional correctness, boundaries, error paths,
memory/resource cleanup, concurrency/locking, WAL/recovery, portability,
API/ABI and compatibility. Examine docs, test coverage/registration,
coding conventions, comments, patch scope, commit message and description.
Do not fill irrelevant checklist fields or hypothesize unsupported bugs.

Use test-pg-patch for discriminating builds/tests. Try to falsify the design:
look for a concrete input, interleaving or error that would violate an invariant.
For each finding give severity/impact, evidence location, why it fails and a
reproducer or suggested verification. Separate confirmed defects from questions
and possible risks. Assess branch-specific suitability through research for
backpatch requests.

Return findings first, ordered by impact, then questions and validation limits.
State inspected version/revision and exactly what was run. If no problems were
found, say so with coverage limits; do not claim correctness is proved. A partial
review is useful when its boundary is explicit. Use prepare-pgsql-hackers-post
for a concise threaded review draft; sending it or changing CommitFest status
requires explicit authorization.
