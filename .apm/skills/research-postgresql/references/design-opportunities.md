# Finding design opportunities

Use this guide when the task is to find PostgreSQL core refactoring or feature
topics, including architecture design practice. Apply the main research workflow
to candidate areas; do not turn an ordinary bug investigation into a broad audit.

Prefer a bounded problem with observable costs and multiple plausible solutions.
Start with a concrete maintenance difficulty, bug fix, feature request or past
change. State who encounters the problem, what triggers it and its consequence.
If no area is specified, narrow to a subsystem or change history that can be
understood within the user's scope; do not promise an exhaustive core survey.

## Investigation lenses

| Lens | Questions to investigate | Evidence to seek |
| --- | --- | --- |
| Change propagation | Which responsibilities and subsystem boundaries does one requirement cross? Which edits are necessary, and which reflect coupling? | A representative diff and its callers, interfaces and tests; explain why each location changed. |
| Duplication and variation | What is shared, what varies, and do the variants change for the same reason? | Similar implementations and their histories; independent invariants or performance requirements may justify keeping them separate. |
| Extension cost | Where would a plausible new kind of operation require edits? What omission could cause a bug? | Existing additions, repeated dispatch/validation changes and tests for missed cases; separate measured past cost from predicted future cost. |
| State and lifetime | Who creates, owns, changes and releases state? What happens on failure, cancellation or retry? | Actual state transitions, memory/resource ownership and error paths, including concurrency or transaction boundaries where relevant. |
| Testability | What setup is needed to exercise one responsibility? Which dependencies or side effects prevent a discriminating test? | Existing test registrations, fixtures and failure coverage; distinguish necessary integration coverage from avoidable coupling. |

Function length, duplication or edit counts alone do not establish a problem.
Connect a structural observation to a concrete consequence, such as a missed
update, unclear ownership or repeated maintenance effort. Where possible, trace
an actual change from its entry point through data flow, state changes and error
handling, and sketch the responsibility/dependency boundaries.

Read relevant history and discussion to explain why the current structure exists.
Look for compatibility promises, subsystem conventions, hot paths and rejected
alternatives before suggesting abstractions. Do not assume similarity requires
unification, that a generic interface is preferable, or that adding indirection
reduces complexity.

## Bound and compare candidates

For a promising area, consider one or two plausible follow-up changes grounded in
requests or history, such as adding another operation or exercising a failure
path. Mark hypothetical scenarios explicitly. Identify the locations each would
touch and what existing behavior must be preserved; avoid speculative generality.

Compare a few realistic approaches, including keeping the current structure or
making a local fix. Consider responsibility boundaries, dependency direction and
data ownership alongside change size, readability, tests, performance and
compatibility. At this stage, describe the decision the candidate would teach and
the evidence needed to choose; use design-pg-patch for the actual design.

Prefer an initial exercise with a traceable execution path, a single responsibility
or interface to reconsider and a way to validate the result. Assess investigation effort,
cross-subsystem impact and unresolved semantics as well as learning value. A
small feature can provide a useful design choice; a broad rewrite is not a
prerequisite. Learning value alone does not justify an upstream patch.

Return a concise candidate comparison with:

- The concrete problem, supporting source/history/discussion locations and
  remaining uncertainties; report when evidence does not justify a change.
- The current responsibilities and constraints, plus the design choice each
  candidate exposes and its plausible alternatives.
- A bounded scope and exclusions, likely affected code/tests, a validation
  approach and the next investigation needed before design.

For a selected topic, carry these findings into a short design note comparing
alternatives, the reason for the choice and how behavior will be preserved.
If implementation is later requested, revisit the original predictions after
validation: did the anticipated change become easier, what complexity was added,
and which assumptions failed? Topic research itself does not authorize edits or
establish community agreement on a proposed change.
