---
name: research-postgresql
description: Investigate PostgreSQL upstream/core source, planner bugs, internals hypotheses, git history, pgsql-hackers discussions or CommitFest proposals. Use to find implementation locations and verify behavior before a core patch. Do not use for SQL syntax help, application queries, routine slow-query tuning or database administration.
---

# Research PostgreSQL

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Establish the actual checkout/revision and the question being answered. For
primary-source navigation, consult [source discovery](references/source-discovery.md)
only when source/history/list discovery is needed.

1. Separate the observed symptom from the suggested explanation. For a bug,
   obtain or build a minimal reproducer and record version/configuration. A
   plausible explanation is a hypothesis until the relevant path is verified.
2. Search the checkout with `rg` for the operation, error text or symbol. Read
   complete surrounding functions and analogous implementations. Trace callers,
   callees, ownership/lifetime, error paths and subsystem invariants; read nearby
   README files, comments and tests. Record what you actually inspected.
3. Inspect path-specific history with `git log`, `git blame` and `git show`.
   Trace relevant commit discussion links and renamed code. Shallow/missing
   history is a limitation, not evidence that there was no earlier decision.
4. Search pgsql-hackers using several concrete terms and synonyms. Open whole
   threads, read replies and relevant attachments, and connect CommitFest
   records to their thread/version. Investigate rejected alternatives; distinguish
   a participant's view from an agreed design. Search failure means unknown.
5. Test the smallest discriminating hypothesis, when practical and authorized.
   Identify counterexamples and reconcile source/doc/thread disagreements using
   the correct branch and dates. Do not change implementation during a
   research-only request.

Return a concise answer with evidence locations, affected code/tests, competing
explanations, unresolved questions and the next useful investigation. Distinguish
what source, docs and discussion establish from inference. For backpatch research,
load [branch assessment](references/backpatch.md). Hand off an implementation
request to design once evidence is sufficient; do not equate locating a symbol
with understanding its semantics.
