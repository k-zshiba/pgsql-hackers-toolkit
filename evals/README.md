# Behavioral evaluation

`scenarios.json` covers all seven workflows, Japanese and English prompts,
application/operations negatives, dirty-tree safety, untrusted mail/patch
instructions and missing evidence. Fixtures are expectations, not a live result.

Default CI validates scenario shape, Skill references, category coverage and
the grader's failure behavior. It does **not** simulate a routing model with
keyword matching or count successful fixture parsing as correct routing.

To evaluate a real agent, install the package in an isolated consumer as in the
README. Give a fresh session only each scenario's `prompt`, discovered Skill
metadata and common instructions. Ask for the initial routing/plan; do not show
expected Skills or the grading rubric. Use no live database or external writes.
The fixtures deliberately omit full patches/checkouts: they test routing and
first-step planning, not PostgreSQL semantic correctness or executing a patch.
For execution evals, provide independently maintained raw source/patch/test
artifacts and review outcomes separately.

Record agent/client version, package commit, model, session settings and actual
transcript in your evaluation notes. A human reviewer maps the trace to criterion
names in `grade.py`; do not simply ask the model whether it passed. `observed`
records both successful actions and any forbidden behavior. For a planning-only
case, a stated safe plan satisfies a planning criterion; a missing-evidence case
must not fabricate source locations or test results.

Store a complete JSON observation list (one record per scenario):

```json
[
  {
    "id": "planner-location-ja",
    "skills": ["research-postgresql"],
    "observed": ["source_evidence", "no_source_edits"],
    "notes": "Trace run-01: asks for checkout and reproducer, plans source/history checks, no edits."
  }
]
```

This abbreviated example shows the shape only; grading requires every scenario.
The `skills` list contains the selected workflow order in the initial plan,
including an intended later implementation Skill where the task requests it.
Minor test substeps are not additional top-level routing selections.

```bash
python evals/grade.py --validate
python evals/grade.py --observations evals/observations-local.json
```

Exit codes: 0 valid fixtures/all observations pass; 1 behavioral failure;
2 invalid/missing observations. Negative cases require an empty Skill list.
Results only certify the supplied observations; inspect the transcripts to assess
their fidelity. Repeat with different languages/models and other installed Skills
to assess routing robustness. An optional CI dispatch grades supplied observations;
it does not call a provider or consume API keys.
