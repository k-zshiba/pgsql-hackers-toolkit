---
name: design-pg-patch
description: Design a PostgreSQL upstream/core feature or bug fix before implementation, including new GUCs, interfaces and behavior changes. Use after source and pgsql-hackers research, or to identify research still needed. Do not use for application schemas, SQL index creation, managed database configuration or an already scoped feedback-only revision.
---

# Design a PostgreSQL patch

Read the [common contributor contract](../../instructions/postgresql-contributor.instructions.md).
Start with the available reproducer, source evidence and prior discussion. If
they are missing, use research-postgresql first; do not fill gaps from memory.

Describe the problem, verified current behavior, desired behavior and smallest
useful patch. For a nontrivial feature, locate prior/rejected proposals and
current discussion. Identify interface/semantics disagreements before substantial
implementation; produce a concise proposal or bounded prototype when discussion
is needed. An explicit request to prototype permits exploratory code, not claims
of community approval or a submission-ready design.

Inspect analogous implementations, callers, tests and history to compare a few
realistic options. Evaluate only relevant dimensions:

- User-visible interface, syntax, semantics, errors and backwards compatibility.
- Affected subsystems, invariants, memory/resource ownership and failure handling.
- Concurrency/locking, WAL/recovery and replication where those paths are touched.
- Catalog/storage impact, extension API/ABI, upgrades and branch suitability.
- Performance measurement, portability and security boundaries.
- Documentation and the regression/TAP/isolation/contrib tests that distinguish
  the intended behavior, including edge cases and a baseline reproducer.

Avoid a checklist filled with invented answers. Explain why a significant risk
applies; mark a material unknown and a way to resolve it. For a new GUC, read
existing definitions, check assign/show hooks and contexts, and define scope,
defaults, validation and visibility from the actual tree. Do not assume every
configuration option belongs in core.

Return a short design note: problem/evidence, chosen semantics, alternatives
and tradeoffs, affected locations, compatibility/risk, validation plan and open
discussion points. Proceed to implement-pg-patch when the scope and assumptions
are justified; stop large implementation at unresolved foundational design
questions and prepare a discussion draft instead. Trivial fixes may use a brief
design note rather than an unnecessary formal process.
