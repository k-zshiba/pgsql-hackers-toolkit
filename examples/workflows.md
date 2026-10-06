# Example contributor tasks

These are prompts to adapt to real evidence, not assertions about PostgreSQL
internals. Supply your source path, reproducer, thread/CommitFest URL and patches
where relevant. Unknown information must remain unknown.

## Planner bug research

```text
Use research-postgresql in /path/to/postgresql at the actual checked-out
revision. This SQL reproducer produces the unexpected plan below. Find the
responsible paths, callers, tests and relevant history/list discussions.
Do not edit yet. Explain what the evidence confirms and what needs testing.
```

Expected output: resolved checkout/revision, evidence-supported implementation
locations, a qualified hypothesis and discriminating next experiment.

## New GUC proposal

```text
I propose a PostgreSQL core GUC for the behavior described here. Research
existing mechanisms and prior/rejected pgsql-hackers proposals. Design
scope, default, semantics, hooks, compatibility and relevant tests from
current source. Prepare discussion questions before substantial code.
```

Expected path: research → design → proposal draft; implementation follows only
when justified. The fact that a user names a GUC does not establish that a new
one is the best interface.

## CommitFest review

```text
Review this CommitFest entry and attached patch. Verify the latest thread,
version/base and prerequisites. Use an isolated tree for applicability,
inspect source invariants and run appropriate tests. Findings first,
with reproduction/evidence and explicit review coverage limits. Draft only.
```

Expected path: review, testing as needed, a concise threaded review draft.
No modification of CommitFest or sending mail is implied.

## Revised v3 patch

```text
Use revise-pg-patch for this series and feedback. Read subsequent replies,
classify required changes and open design questions, make the agreed
focused revision, then test the final tree. Explain v3 changes and any
unresolved feedback. Prepare local attachments and a response draft.
```

Expected output: issue/resolution ledger, versioned local patch, validation
evidence, concise changes and unresolved questions. Keep prior user work safe.

## Backpatch suitability

```text
Research whether this core bug fix belongs on the requested stable
branches. Verify support status, bug introduction and corresponding code
per branch. Assess API/layout/behavior risks and branch-specific tests.
Give a recommendation with unknowns; do not switch or cherry-pick my tree.
```

Expected output: branch/revision/evidence matrix and a qualified recommendation.

## Out of scope

```text
How do I add an index to my application's customer table?
My production SELECT is slow; how should I tune it?
```

These should not activate this toolkit's core-development Skills. A source-level
PostgreSQL bug discovered later may justify reclassifying the task, with evidence.
