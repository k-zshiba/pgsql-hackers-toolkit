---
name: implement-pg-patch
description: Implement a researched, scoped PostgreSQL upstream/core source patch with appropriate documentation and tests. Use when design and target checkout are established. Do not use to invent a large undiscussed feature, modify application code or handle reviewer feedback that belongs to revise-pg-patch.
---

# Implement a PostgreSQL patch

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Confirm the requested scope, actual target revision, existing changes and design
evidence. Resolve material unknowns through research/design before substantial
edits. Existing unrelated work remains untouched.

1. Read analogous code and its callers/callees, README/comments and tests. Note
   the local conventions for errors, allocation/lifetime, locking and cleanup.
   Use the checkout's coding-conventions chapter, not generic modernization.
2. Make a focused diff implementing the chosen behavior. Do not mix unrelated
   refactoring, formatting, performance work or speculative fixes. Include only
   comments that explain intent/invariants beyond what the code already says.
3. Add/update tests and docs with the implementation. Demonstrate the bug on a
   suitable baseline where possible. Check both build-system registrations when
   present, schedules and expected output; inspect generators before modifying
   generated headers, catalogs or parser output. Do not commit generated files
   unless the branch's existing practice requires them.
4. Read `src/tools/pgindent/README` and relevant formatter configuration in the
   checkout. Verify prerequisites, typedef handling and version requirements.
   Format touched files/hunks deliberately and review the resulting diff. A
   whole-tree formatter command from a README is not permission to alter other work.
5. Use test-pg-patch to validate the changed behavior, error paths and relevant
   wider coverage. Review `git diff --check`, tracked/untracked status, docs,
   test registration and patch scope. Fix attributable failures; report baseline
   or environment failures separately with evidence.

Return a change summary tied to behavior, evidence locations, exact validation
and remaining limitations. Use review-pg-patch before preparation for submission.
Create local patch files only from the intended changes and inspect their contents;
do not include user changes, deployment artifacts, build output or secrets.
Do not commit, send or publish unless that action was authorized.
