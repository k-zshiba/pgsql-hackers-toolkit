---
name: revise-pg-patch
description: Revise a PostgreSQL upstream/core patch into v2, v3 or later from reviewer feedback and pgsql-hackers discussion, then retest and explain changes. Use for feedback-driven patch iterations. Do not use for a first undiscussed feature, application maintenance or generating an unverified version bump alone.
---

# Revise a PostgreSQL patch

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Establish current patch/base, latest thread/version, feedback messages and the
user's working changes. Read replies after the supplied feedback; a later
message may resolve or change an earlier request. Do not assume v3 is latest.

Create a compact issue ledger only as detailed as needed:

| Feedback / message | Required change or question | Resolution evidence | State |
| --- | --- | --- | --- |
| Reviewer point | correctness, semantics, test, docs/style or disagreement | source/test/reply | addressed, open or deferred |

Separate must-fix defects, design questions, optional improvements, conflicting
feedback and out-of-scope suggestions. Validate each proposed fix against the
current source and original intent. Explain disagreements rather than silently
implementing all suggestions. Route changed semantics through research/design;
do not turn feedback into unrelated refactoring.

Implement agreed focused changes using local conventions. Add regression coverage
for review-discovered bugs and preserve intended prior behavior. Rebuild/retest
the final revision through test-pg-patch, including affected older cases and
relevant wider coverage. Inspect the diff from the previous patch, not just the
new aggregate diff; a `git range-diff` is useful for deliberately identified
commit series but is not applicable to every uncommitted patch workflow.

Review the revised patch and generate local versioned attachments only from the
intended changes. Verify applicability, actual version/base and series ordering.
Return a feedback ledger, material vN changes, exact validation and unresolved
issues. Use prepare-pgsql-hackers-post for the reviewer response or revised
submission draft. Do not claim full resolution when issues remain; preserve the
existing thread and require explicit authorization for any external posting.
